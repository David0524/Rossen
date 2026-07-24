---
name: rossen-pipeline
description: Run the full Rossen Reports clip pipeline end to end. Use whenever the user hands over a show script and wants clips found, graded, downloaded, and cut, or says anything like "here's the script, find the clips", "run the pipeline", "get me clips for this episode". Orchestrates the beat extractor, query generator, multi-source search, clip grader, and the download-and-cut stage. Also use to resume a partially completed run.
---

# Rossen Reports pipeline

One script in, cut clips plus a manifest and an FCPXML out. Target wall
clock is under 10 minutes for a 10-12 beat episode.

You do the judgment. The `rossen_harvest` package does the mechanical
work. Never reimplement a stage in an ad-hoc script; the CLI already
handles caching, dedupe, concurrency limits and graceful backend failure.

## Preflight

```bash
python3 -c "import yt_dlp; print('yt-dlp ok')"
which ffmpeg || echo "MISSING ffmpeg — brew install ffmpeg"
echo "${BRAVE_API_KEY:+brave}${SERPER_API_KEY:+serper}" || true
```

No web search key means **YouTube only**, roughly 70% of normal coverage
and no TikTok, Instagram, Facebook or native network video. Say so
plainly and ask whether to proceed degraded or stop and set a key. Do not
quietly run a crippled pipeline.

## Step 1 — Beats

Read `.claude/skills/rossen-beat-extractor/SKILL.md` and its
`reference/aired_examples.md`. Convert the script:

```bash
pandoc -t plain --wrap=none script.docx -o script.txt
```

Extract beats. Drop the cold open and every mid-show tease. Expect 10-12
beats. If you get more than 16, you are extracting teases; re-read the
traps section.

## Step 2 — Queries

Read `.claude/skills/rossen-query-generator/SKILL.md` and its
`reference/glossary.md`. Generate four registers per beat.

Merge steps 1 and 2 into one `beats.json`: each object needs `beat_id`,
`clip_role`, `orientation`, `platforms`, `visual_spec`, `script_text`,
`offsite_likely`, and a `queries` dict of register to string list.

**Orientation is a hard filter, not a hint.** It is producer-authored and
predicted the platform correctly in 26 of 26 observed cases. Horizontal
beats do not get TikTok queries.

## Step 3 — Search

```bash
python3 -m rossen_harvest search beats.json --out candidates.json
```

Runs two backends and dedupes across both. **YouTube** (yt-dlp) takes
horizontal beats. **Brave** (needs `BRAVE_API_KEY`) takes the leg YouTube
cannot reach: off-YouTube network and affiliate video (`news_web`), Reddit,
and vertical beats — which the YouTube backend skips entirely, so Brave is
their only coverage. A beat routes to Brave when its `platforms` include
`news_web, tiktok, instagram, facebook, x, reddit`, or when it is vertical.
Caches to `harvest.db`.

Honest coverage boundary, so you read the counts correctly: Brave is strong
on `news_web` and Reddit, and for a *named person* it finds the press
coverage that points to their own social post (that is the self-recorded
workflow — search the name, hand over the native link). It does **not**
reliably surface a native TikTok/Instagram/X *post* for a generic query;
its video endpoint is YouTube-heavy. So a vertical beat coming back heavy on
`youtube` and `news_web` with no native social is the tool working as built,
not a query failure. Closing that last gap needs an authenticated social
scraper, which is not wired in.

Report the per-platform counts (the command prints them). A beat returning
zero candidates is a query problem; revise its queries and re-run that beat
alone. If the run printed a `DEGRADED` line, `BRAVE_API_KEY` was missing and
every `news_web`/social/vertical beat got nothing — stop and set the key
rather than grading a half-empty pool.

## Step 4 — Grade, pass one

Read `.claude/skills/rossen-clip-grader/SKILL.md`. Apply the metadata
triage to `candidates.json`. Hard filters first, then score, then the
diversity floor. Narrow each beat to **5**.

Metadata only here. Do not fetch captions for 300 clips.

Tag every shortlisted candidate with a `source_type` and report the mix
per beat. Where the diversity floor fired, say which candidate it promoted
and what it displaced.

## Step 5 — Captions

Write the shortlist to `shortlist.json`, then:

```bash
python3 -m rossen_harvest captions shortlist.json --out transcripts.json
```

No downloads, no Whisper, about a second per clip. 5-10% of clips have
captions disabled and come back null. Demote those, do not guess at
their content.

**Vertical shortlist entries (TikTok/Reels/X) need a separate pass — they carry no caption track at all, so the step above always returns null for them.** Use `vertical_transcribe.py`:

```python
from rossen_harvest.vertical_transcribe import fetch_many_vertical
from rossen_harvest.cache import Cache

vertical_transcripts = fetch_many_vertical(
    [c["url"] for c in shortlist if c["platform"] == "tiktok"],
    cache=Cache("harvest.db"), model_size="base.en",
)
```

Downloads each clip and transcribes locally with faster-whisper (CPU, no GPU). Not free like the caption fetch — budget real seconds per clip, not a fraction of one — so run it on the shortlist only, never on 30 raw candidates. Returns the same `Transcript` shape as YouTube captions (`source == "whisper"`), so pass two's outcue verification (`.find()`, `.segment()`) works identically. Requires `pip install faster-whisper`; do not add `curl-cffi` speculatively for TikTok — it has caused TLS failures where plain yt-dlp succeeded. If a vertical pick has no Whisper transcript available in your environment, flag its outcue as unverified rather than inventing one — same rule as everything else in this pipeline.

## Step 6 — Grade, pass two

Same skill, transcript section. Score tone, authenticity, quality and fit.
Flag one clip per beat and propose in/out points.

Every proposed segment needs a verbatim `outcue` quote from the
transcript. Verify it before writing: the phrase must actually appear
near the proposed out point. If you cannot find it, your timecode is
wrong. Do not invent the quote.

If nothing is good enough for a beat, say so and flag nothing. A bad pick
costs more than an honest gap, because it gets discovered in the edit bay.

Write `picks.json`:

```json
[{"beat_id":"b03","url":"https://...","title":"...","platform":"youtube",
  "segments":[{"in":"0:33","out":"1:21","outcue":"when I sent the money out"}]}]
```

Multiple segments per pick are normal. Four of 24 aired beats were
butt-cuts pulling 2-3 slices from one source.

## Step 7 — Cut

```bash
python3 -m rossen_harvest clip picks.json --outdir clips
```

Downloads each pick once at 720p, cuts every segment, writes
`clips/manifest.json` and `clips/clips.fcpxml`.

Timecodes are padded 1s early and 1.5s late, because caption boundaries
are 1-3s granular. The editor trims; that is cheaper than discovering a
clipped first syllable.

## Step 8 — Report + filled Bible doc

**Primary deliverable: an updated Bible `.docx`** with every clip beat filled
in. At each `PLAY CLIP` marker embed, in **blue text** (`1155CC`), a clickable
video hyperlink plus the `IN`–`OUT` timecodes and the verbatim outcue. Beats
with no clip get a red (`C0392B`) "no clip found — <reason>" line. Beats whose
exact case exists only off captioned YouTube (news_web/affiliate site) get the
source link in blue marked "MANUAL CLIP — no captions" (no invented timecode).
When an approved case-swap changes what the script says, rewrite the affected
setup lines in place so the doc reads as a shootable rundown.

Build it with docx-js (see the `docx` skill); use `ExternalHyperlink` for the
links and set run `color:"1155CC"` on link + timecode runs. This is the
standard output format going forward — the producer reads the doc, not a
terminal table.

Alongside the doc, give a compact table: beat, role, chosen clip, platform,
source type, duration, outcue. Above it, one line with the episode source mix:

```
Source mix, 10 beats:  affiliate 8 · first_person 1 · creator_long 1
```

Then call out, explicitly:

- beats with no usable clip
- beats where the pick was weak and a human should re-check
- any source type holding 70% or more of the picks, plus the beats where
  the runner-up was a different type — those are the cheap swaps if the
  producer wants variety
- beats where the diversity floor promoted a candidate that then lost in
  pass two
- clips that failed to download
- whether the run was degraded by a missing search key

## Timing

| Step | Expected |
|---|---|
| 1-2 beats and queries | ~1 min |
| 3 search | ~2 min |
| 4 triage | ~1 min |
| 5 captions | ~1 min |
| 6 grade | ~1.5 min |
| 7 cut | ~2 min |

Roughly 8-9 minutes. If a stage runs far over, say so rather than waiting
silently.

## Resuming

Every stage writes a file and `harvest.db` caches searches and captions
for two weeks. To resume, start at the first stage whose output file is
missing. Delete `harvest.db` only to force a genuinely cold run.
