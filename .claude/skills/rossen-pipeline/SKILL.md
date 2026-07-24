---
name: rossen-pipeline
description: Run the full Rossen Reports clip pipeline end to end. Use whenever the user hands over a show script and wants clips found, graded, and logged with verified timecodes, or says anything like "here's the script, find the clips", "run the pipeline", "get me clips for this episode". Orchestrates the beat extractor, query generator, multi-source search, and clip grader. There is no automated download-and-cut stage — see Step 7. Also use to resume a partially completed run.
---

# Rossen Reports pipeline

One script in, a picks manifest plus a filled Bible `.docx` out. Target
wall clock is under 10 minutes for a 10-12 beat episode. There is no
automated download-and-cut stage — pulling and trimming video happens
downstream of this pipeline, by hand. See Step 7.

You do the judgment. The `rossen_harvest` package does the mechanical
work. Never reimplement a stage in an ad-hoc script; the CLI already
handles caching, dedupe, concurrency limits and graceful backend failure.

## Preflight

```bash
pip install -r harvest/requirements.txt   # yt-dlp, faster-whisper — not preinstalled in a fresh session
python3 -c "import yt_dlp; print('yt-dlp ok')"
python3 -c "import faster_whisper; print('faster-whisper ok')"
which ffmpeg || echo "MISSING ffmpeg — brew install ffmpeg / apt install ffmpeg"
echo "${BRAVE_API_KEY:+brave}${SERPER_API_KEY:+serper}" || true
export PYTHONPATH="$(pwd)/harvest"   # required for `import rossen_harvest` to resolve
```

### Then probe the network paths, because the imports above prove nothing

Every check above can pass while the pipeline is functionally dead. `import
yt_dlp` succeeding says the library is installed; it says nothing about whether
YouTube will *answer*. These four probes are not optional — run them and read
the result before Step 1:

```bash
# 1. SEARCH reachable? (flat-playlist metadata — the Step 3 path)
yt-dlp --flat-playlist --dump-json "ytsearch1:scam" >/dev/null 2>&1 \
  && echo "search OK" || echo "SEARCH DEAD"

# 2. CAPTIONS reachable? (per-video page — the Step 5 path, and the one
#    that verifies every outcue in the run)
yt-dlp --skip-download --list-subs "https://www.youtube.com/watch?v=aircAruvnKk" 2>&1 \
  | grep -q "not a bot" && echo "CAPTIONS BOT-WALLED" || echo "captions OK"

# 3. MEDIA bytes reachable? (the Whisper path — audio counts as media)
yt-dlp -f bestaudio -o /tmp/probe.%\(ext\)s --no-warnings \
  "https://www.youtube.com/watch?v=aircAruvnKk" >/dev/null 2>&1 \
  && echo "media OK" || echo "MEDIA BLOCKED"

# 4. BRAVE actually authorizes? (a present key is not a working key)
curl -s -o /dev/null -w "brave HTTP %{http_code}\n" \
  -H "X-Subscription-Token: $BRAVE_API_KEY" \
  "https://api.search.brave.com/res/v1/web/search?q=test&count=1"
```

**These three YouTube paths fail independently.** Search is a different
endpoint from the video page, which is different again from media bytes, and
in a shared-egress environment (a cloud container behind a pooled IP) they
degrade in that order — search survives longest, media dies first.

**Distinguish throttling from blocking before you report either.** The
"Sign in to confirm you're not a bot" response is returned for *both*, and
they need opposite responses. Measured on 2026-07-24: a rapid diagnostic
burst — a dozen `--list-subs` calls in a couple of minutes, several of them
looping over player clients — drove the caption path to **0 of 6** on video
IDs a prior run had captioned successfully. It looked exactly like a hard IP
block. Twenty minutes later the ordinary `fetch_many` path, hitting the same
host at its normal pace, returned **11 of 12**. Nothing was fixed; the burst
had simply tripped a rate limiter.

So: probe **once** per path, never in a loop, and never iterate player
clients as a first move — that iteration is itself what trips the limiter.
If a probe fails, wait several minutes and retry once through the real code
path (`fetch_many`) before concluding anything. Report a hard block only
after a spaced-out retry through the normal path also fails. Calling a
throttle a block costs a whole run: it converts every pick to an unverified
outcue and pushes the producer toward a degraded deliverable they did not
need to accept.

**If captions are bot-walled, say so at Checkpoint 1 and stop for a ruling.**
Do not run search and grade into a dead end: without captions there is no
transcript, without a transcript no outcue can be verified, and this pipeline's
central rule is that an unverified outcue never gets written. A full run under
that condition produces picks whose timecodes are all unverified — which is a
legitimate deliverable only if the producer has agreed in advance to receive
one. Alternate `--extractor-args youtube:player_client=...` values are worth
one attempt (`mweb` dodges the bot-check), but verify it returns real caption
tracks rather than an empty list — a client that answers with "no automatic
captions" for a video you know is captioned is degraded, not working.

`harvest/requirements.txt` covers the only two non-stdlib Python deps in
the package (`yt-dlp`, `faster-whisper`); everything else is stdlib.
A fresh session/container has neither installed and no cached pip state,
so run the install line every time rather than assuming it carries over
from a prior chat. `ffmpeg` is a system binary, not pip-installable —
check it separately.

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

Runs three surfaces and dedupes across all of them. Caches to `harvest.db`.

**YouTube long-form** (yt-dlp) takes horizontal beats. Orientation stays a
hard filter here: a horizontal beat is never answered with a portrait clip.

**YouTube Shorts** (`ShortsBackend`) runs on **every** beat, both orientations.
It is its own search surface, not a byproduct of the long-form query — it
appends `#shorts` and applies a 60s ceiling, because the suffix alone leaks
long-form uploads and the ceiling alone leaves you searching all of YouTube.
It runs the `shorts` and `platform` registers only; `news`/`anchor` are
noun-heavy headline syntax and do not reach Shorts titles. Shorts surfaced
against a horizontal beat are tagged `surfaced_for: horizontal` so the grader
rules on framing rather than the harvester silently overriding the producer's
orientation call.

**Brave** (needs `BRAVE_API_KEY`) takes the leg YouTube cannot reach:
off-YouTube network and affiliate video (`news_web`), Reddit, and native
social posts. A beat routes to Brave when its `platforms` include
`news_web, tiktok, instagram, facebook, x, reddit`, or when it is vertical.

> **Fixed 2026-07-24.** Vertical beats used to skip the YouTube backend
> wholesale, so their `shorts` register never ran anywhere — even though the
> query-generator skill states Shorts run on every orientation. That left
> Shorts, the only vertical surface with a reachable search index, entirely
> unsearched on exactly the beats that needed it most, while Brave answered
> those beats with YouTube results through its more YouTube-heavy video
> endpoint. Vertical beats now reach Shorts directly. See `test_shorts.py`.

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

**There is no `captions` subcommand.** `python3 -m rossen_harvest --help`
lists only `harvest`/`search` and `eval` — caption fetching is a library
call, not CLI. Write the shortlist to `shortlist.json`, then call
`transcripts.fetch_many` directly:

```python
from rossen_harvest.transcripts import fetch_many
from rossen_harvest.cache import Cache
import json

shortlist = json.load(open("shortlist.json"))
youtube_ids = [c["url"].split("v=")[-1].split("&")[0] for c in shortlist
               if c["platform"] == "youtube"]

transcripts = fetch_many(youtube_ids, cache=Cache("harvest.db"))
```

**`fetch_many` takes bare video IDs, not full URLs.** It builds the
`https://www.youtube.com/watch?v=` prefix internally, so passing a full URL
double-prepends it into an invalid one and every fetch silently returns
None — this has actually happened in a prior run. Strip each URL down to
just the ID before calling it.

No downloads, no Whisper, about a second per clip. 5-10% of clips have
captions disabled and come back null. Demote those, do not guess at
their content.

### The transcript ladder — try these in cost order, never skip a rung

Whisper is the expensive rung, not the default one. Work down:

| Rung | Applies to | Cost | Gets you |
|---|---|---|---|
| 1. Caption fetch | YouTube long-form **and Shorts** | ~1s/clip, metadata only | Verified outcue |
| 2. Whisper | TikTok/Reels/X, and captionless Shorts | Real seconds/clip + media bytes | Verified outcue |
| 3. Flag unverified | Anything rung 1-2 could not reach | Free | An honest gap |

**Rung 1 covers Shorts.** A Short is an ordinary YouTube video with an ordinary
caption track — same index, same `fetch_many` call, same bare-video-id contract.
Do not send a Short to Whisper before trying the caption fetch on it; that pays
seconds and a download for something a metadata call returns for free. This is
the single most common way to waste time in this step.

**Rung 2 is for surfaces that genuinely ship no captions** — TikTok, Reels,
native X video — plus the minority of Shorts with captions disabled.

**Rung 3 is a real outcome, not a failure state.** Both rungs above depend on
network paths that fail independently (see Preflight). When media bytes are
blocked, Whisper cannot run at all — it needs the audio it is transcribing.
When the video page is bot-walled, captions die too. In an environment where
both are blocked, rung 3 is the *only* available rung, and the correct output
is a pick with an explicitly unverified outcue, flagged as such in the report
and the Bible doc. Never promote a guess to fill the gap.

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

Use `vertical_id(url)` — not `tiktok_id` — for anything cache-key shaped. It
resolves TikTok, Shorts, Reels, X and Facebook video to a `(platform, id)`
pair, where `tiktok_id` returns None for everything but TikTok. That matters
because the id *is* the cache key: an unmatched URL caches on the raw string,
so one Reel arriving with different tracking params (`?igsh=`, `?utm_source=`)
caches two or three times and pays for a fresh download and a fresh Whisper
run on each variant.

**Whisper's reach is exactly as wide as your media access, and no wider.**
It is not a way around a block — it is a transcription step that consumes
bytes something else had to fetch. If yt-dlp cannot download the clip,
Whisper has nothing to transcribe and returns None. So when the preflight
media probe fails, do not plan around Whisper for *any* platform; it is off
the table for the whole run, and rung 3 is where those beats land.

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

## Step 7 — Manifest (no automated cut stage)

**There is no `clip` subcommand and no download-and-cut code path in
`rossen_harvest`.** `python3 -m rossen_harvest --help` lists exactly two
subcommands, `harvest` (alias `search`) and `eval` — nothing that downloads
video or trims it. The only `yt-dlp`/`ffmpeg` call in the package is inside
`vertical_transcribe.py`'s `download_audio()`, and that pulls audio only,
into a scratch `.wav`, solely to feed Whisper — it does not save video or
take in/out points. There is also no code that writes an FCPXML.

So this step is a handoff, not a render: hand-write `clips/manifest.json`
from `picks.json` — one entry per beat with its URL, platform, source_type,
and segments (in/out/outcue). That file plus the Bible `.docx` (Step 8) are
the deliverable. Pulling the actual video and cutting it happens downstream,
manually, in whatever tool the edit bay uses — outside this pipeline. Don't
claim clips were downloaded or cut; say what actually happened, which is
that picks were located, verified against transcript, and logged with exact
timecodes for someone else to pull.

If a real automated cut stage gets built later (yt-dlp video pull + ffmpeg
trim + FCPXML writer as an actual `clip` subcommand), rewrite this step to
describe it. Until then this description is accurate, not aspirational.

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
| 7 manifest | <1 min (hand-write, no download/cut) |

Roughly 8-9 minutes. If a stage runs far over, say so rather than waiting
silently.

## Resuming

Every stage writes a file and `harvest.db` caches searches and captions
for two weeks. To resume, start at the first stage whose output file is
missing. Delete `harvest.db` only to force a genuinely cold run.
