---
name: "rossen-pipeline"
description: Run the Rossen Reports clip pipeline on an approved story outline — the videos half of the "outline w/ videos" stage, before the bible is written. Use whenever an outline's beats need clips found, graded, and logged with verified timecodes, or the user says anything like "find the clips for the outline", "run the pipeline", "get me clips for this episode". Orchestrates the beat extractor, query generator, multi-source search, and clip grader. There is no automated download-and-cut stage — see Step 7. Also use to resume a partially completed run, or to back-fill the eval set from an aired bible.
---

# Rossen Reports pipeline

## Where this sits

pre-bible → pre-bible email → **outline w/ videos** → bible → bible review

One approved outline in (plus the pre-bible it came from), a picks manifest plus the
filled **outline w/ videos** `.docx` out. The bible is written afterwards, from that
outline, by `rossen-script-writer` — it never comes back through this pipeline. The
outline format, its Videos table and status vocabulary belong to
`rossen-story-outline`; read it before Step 8.

You do the judgment. The `rossen_harvest` package does the mechanical work. Never
reimplement a stage in an ad-hoc script; the CLI already handles caching, dedupe,
concurrency limits and graceful backend failure. If the package is absent that is
a hard stop, not an invitation — see `dependencies.md`.

## Bundled files

| File | Load when |
|---|---|
| `dependencies.md` | **Before Step 1, every run.** What must exist, install, network probes, degraded-run rules. |
| `schemas.md` | Writing or reading any stage file. The three handoff contracts. |
| `scripts/contract_check.py` | **After Steps 2 and 6.** Validates a stage file against the siblings' schemas. |
| `scripts/init_yield_log.py` | Once, if `beat_yield.md` is absent. |

## Checkpoints

Four producer-facing stops. **These are the pipeline's control vocabulary and this
document owns them** — the sibling skills refer to them by number and expect them
to exist. Stop and surface; do not roll past one on your own initiative.

| # | After | Surface | The decision |
|---|---|---|---|
| **0** | Preflight | Missing dependencies, dead network paths, absent search key | Proceed, proceed degraded, or stop |
| **1** | Steps 1–2 | Beat table: id, outline row, role, orientation, priority, `sourcability`, `source_native`, routing lane | Approve the beat list; rule on low-sourcability beats; confirm the manual lane |
| **2** | Steps 3–4 | Per-beat candidate counts, per-platform mix, shortlist source-type mix, diversity-floor promotions | Proceed to the expensive transcript stage, or revise queries on thin beats |
| **3** | Steps 5–6 | Picks with verified outcues, unverified beats, empty beats | Accept the picks, or send specific beats back |

**Checkpoint 1 is where this pipeline saves or wastes its whole budget.** The beat
extractor's sourcability scan exists to catch un-sourceable beats here, before any
search runs. In a prior F2 run three beats reached Checkpoint 3 as `flagged: null`
after full search, download and transcript grading; all three were predictable
from a five-second search, and the scan would have caught them at Checkpoint 1.
Run the scan, put its verdict in the beat table, and take the ruling.

An empty beat at Checkpoint 1 costs nothing. An empty beat at Checkpoint 3 wasted
every search and download in between.

## Show-day calibration

**Ask which show day before Step 1.** Wednesday and Friday are different jobs and
a single expectation is wrong for one of them. Measured across the aired corpus:

| | Clip beats | Orientation | Typical surfaces | Wall clock |
|---|---|---|---|---|
| **Wednesday** (top stories) | **10–12** | mostly horizontal | YouTube affiliate, network | ~8–9 min |
| **Friday** (one content story + deals guest) | **0–5** | mostly vertical | native TikTok / Reels | ~4–5 min |

These bands were measured on aired bibles. An outline's clip beats are its `HAVE`/`FIND`
rows, so the count is the same thing measured earlier; an A+B Wednesday sits at the low
end (the 10/07 run had 7). Aired counts: Wednesday 11 and 11. Friday 0, 2, 3, 4, 5, 5. **A Friday show with
three beats is a correct extraction, not an under-extraction**, and 07/03 aired
with zero clip beats because its content segment was a screen-share walkthrough.
The deals half of a Friday is never a clip beat.

Only the Wednesday band supports the old "more than 16 means you are extracting
teases" heuristic. On a Friday, more than 8 means you are extracting teases or
picking up the deals block.

Corpus orientation split: **15 of 40 aired cues are vertical**, and of cues that
carry a URL, **12 of 20 are non-YouTube native social**. Read the coverage boundary
in Step 3 with those numbers in mind.

## Step 1 — Beats

Read the `rossen-beat-extractor` skill, **outline mode**, and its `aired_examples.md`.
Input is the approved outline's markdown source and the pre-bible. One beat per
`HAVE`/`FIND` row; `beat_id` is `MM-DD-<story><row>` (`10-07-A5`), so every pick maps
back to its outline row. `DEMO` rows are logged `SHOW-PRODUCED` at Checkpoint 1;
`GUEST`, `JEFF` and `STILLS` rows are not beats.

Script mode — an aired bible via `pandoc -t plain --wrap=none` — is for back-filling
the eval set only. There, drop the cold open and every mid-show tease.

**Run the sourcability scan on every beat.** It is part of the extractor, not an
optional extra, and it is the whole reason Checkpoint 1 exists. Every beat comes
out with `sourcability` and `source_native` populated.

## Step 2 — Queries and routing

Read the `rossen-query-generator` skill and its `glossary.md`. Generate **five
register keys** — `news`, `victim`, `platform`, `anchor`, `shorts`. The generator
describes four registers and then splits the platform register into a Shorts
dialect that Step 3 consumes by name; four keys silently halves the Shorts leg.
See `schemas.md`.

Merge Steps 1 and 2 into `beats.json`: **the extractor's record passed through
untouched, plus `queries`.** Do not reduce it. `priority`,
`expected_segments`, `sourcability`, `source_native` and `news_anchor` all get
consumed downstream, and dropping a field here is how it stops existing for the
rest of the run.

```bash
python3 scripts/contract_check.py beats beats.json
```

**Orientation is a hard filter, not a hint.** Producer-authored, and it predicted
the platform correctly in 26 of 26 observed cases. Horizontal beats do not get
TikTok queries.

### Route each beat into a lane before any search runs

This is the other half of Checkpoint 1, and it is what keeps the pipeline from
spending its whole budget to rediscover something the scan already knew.

| Lane | Condition | What happens |
|---|---|---|
| **Search** | `sourcability: high` or `commentary_only`, and `source_native: none` | Steps 3–6 as normal |
| **Manual** | `source_native` is `tiktok`/`instagram`/`x` — a native post exists | Skips search. Hand the producer the direct link to the original post (or profile + date + caption fragment if the permalink can't be pinned). Per the extractor, that post *is* the pick — not a YouTube repost |
| **Show-produced** | `sourcability: none` and the show can shoot it | Leaves the clip pipeline; it is a production task. Log as `SHOW-PRODUCED`, never `EMPTY` |
| **Drop** | `sourcability: none` and no swap available | Cut at Checkpoint 1, with the reason |

The manual lane is not a failure mode — for a vertical episode it may be most of
the beats, and it produces a better clip than a scraped repost would. Aggregator
channels frequently carry the only findable YouTube copy, but they re-narrate over
the subject's audio or are bot-walled from download, and neither is clean or
clearable.

**Surface the lane assignment in the Checkpoint 1 table** and take the producer's
ruling before spending anything.

## Step 3 — Search

```bash
python3 -m rossen_harvest search beats.json --out candidates.json
```

Search-lane beats only. Runs three surfaces, dedupes across all of them, caches to
`harvest.db`.

**YouTube long-form** (yt-dlp) takes horizontal beats. Orientation stays a hard
filter: a horizontal beat is never answered with a portrait clip.

**YouTube Shorts** (`ShortsBackend`) runs on **every** beat, both orientations. It
is its own search surface, not a byproduct of the long-form query — it appends
`#shorts` and applies a 60s ceiling, because the suffix alone leaks long-form
uploads and the ceiling alone leaves you searching all of YouTube. It runs the
`shorts` and `platform` registers only; `news`/`anchor` are noun-heavy headline
syntax and do not reach Shorts titles. Shorts surfaced against a horizontal beat
are tagged `surfaced_for: horizontal` so the grader rules on framing rather than
the harvester silently overriding the producer's orientation call.

**Brave** (needs `BRAVE_API_KEY`) takes the leg YouTube cannot reach: off-YouTube
network and affiliate video (`news_web`), Reddit, and native social posts. A beat
routes to Brave when its `platforms` include `news_web, tiktok, instagram,
facebook, x, reddit`, or when it is vertical.

### Honest coverage boundary

Brave is strong on `news_web` and Reddit, and for a *named person* it finds the
press coverage that points to their own social post. It does **not** reliably
surface a native TikTok/Instagram/X *post* for a generic query; its video endpoint
is YouTube-heavy. So a vertical beat coming back heavy on `youtube` and `news_web`
with no native social is the tool working as built, not a query failure. Closing
that gap needs an authenticated social scraper, which is not wired in.

**This is why the manual lane exists.** Non-YouTube native social is 12 of 20
URL-bearing aired cues. Routing those beats at Checkpoint 1 rather than searching
for them is not a workaround; it is the correct use of a tool that cannot reach
them, and it saves the search, the download and the grade.

Report per-platform counts (the command prints them). A search-lane beat returning
zero candidates is a query problem; revise its queries and re-run that beat alone.

## Step 4 — Grade, pass one

Read the `rossen-clip-grader` skill. Apply the metadata triage to
`candidates.json`. Hard filters first, then score, then the diversity floor.
Narrow each beat to **5**.

Metadata only here. Do not fetch captions for 300 clips.

Tag every shortlisted candidate with a `source_type` and report the mix per beat.
Where the diversity floor fired, say which candidate it promoted and what it
displaced. Carry `beat_id`, `orientation`, `priority` and `expected_segments`
through to `shortlist.json`.

**Checkpoint 2 here** before spending the transcript stage.

## Step 5 — Captions

**There is no `captions` subcommand.** `python3 -m rossen_harvest --help` lists
only `harvest`/`search` and `eval` — caption fetching is a library call:

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
`https://www.youtube.com/watch?v=` prefix internally, so a full URL
double-prepends into an invalid one and every fetch silently returns None — this
has actually happened. Strip each URL to the ID first.

No downloads, no Whisper, about a second per clip. 5–10% of clips have captions
disabled and come back null. Demote those; do not guess at their content.

### The transcript ladder — cost order, never skip a rung

| Rung | Applies to | Cost | Gets you |
|---|---|---|---|
| 1. Caption fetch | YouTube long-form **and Shorts** | ~1s/clip, metadata only | Verified outcue |
| 2. Whisper | TikTok/Reels/X, and captionless Shorts | Real seconds/clip + media bytes | Verified outcue |
| 3. Flag unverified | Anything rungs 1–2 could not reach | Free | An honest gap |

**Rung 1 covers Shorts.** A Short is an ordinary YouTube video with an ordinary
caption track — same index, same `fetch_many` call, same bare-id contract. Do not
send a Short to Whisper before trying the caption fetch; that pays seconds and a
download for what a metadata call returns free. This is the most common way to
waste time in this step.

**Rung 3 is a real outcome, not a failure state.** Both rungs above depend on
network paths that fail independently. When media bytes are blocked Whisper cannot
run at all; when the video page is bot-walled captions die too. Where both are
blocked, rung 3 is the only rung, and the correct output is a pick with an
explicitly unverified outcue, flagged in the report and the outline's Videos table. Never
promote a guess. **Spend rung 2 on `priority: 1` beats first** — that is what the
field is for.

Record the rung reached on every pick.

### Vertical shortlist entries

TikTok/Reels/X carry no caption track, so the step above always returns null:

```python
from rossen_harvest.vertical_transcribe import fetch_many_vertical
from rossen_harvest.cache import Cache

vertical_transcripts = fetch_many_vertical(
    [c["url"] for c in shortlist if c["platform"] == "tiktok"],
    cache=Cache("harvest.db"), model_size="base.en",
)
```

Downloads each clip and transcribes locally with faster-whisper (CPU). Real seconds
per clip — shortlist only, never 30 raw candidates. Returns the same `Transcript`
shape as captions (`source == "whisper"`), so pass two's `.find()` / `.segment()`
verification works identically. Do not add `curl-cffi` speculatively for TikTok; it
has caused TLS failures where plain yt-dlp succeeded.

Use `vertical_id(url)` — not `tiktok_id` — for anything cache-key shaped. It
resolves TikTok, Shorts, Reels, X and Facebook video to a `(platform, id)` pair,
where `tiktok_id` returns None for everything but TikTok. The id *is* the cache
key: an unmatched URL caches on the raw string, so one Reel arriving with different
tracking params (`?igsh=`, `?utm_source=`) caches two or three times and pays for a
fresh download and a fresh Whisper run each time. Aired bibles routinely carry
TikTok links with `?_r=`/`?_t=` params, so this is the normal case, not an edge one.

## Step 6 — Grade, pass two

Same skill, transcript section. Score tone, authenticity, quality and fit. Flag one
clip per beat and propose in/out points.

Every proposed segment needs a verbatim `outcue` from the transcript. Verify before
writing: the phrase must actually appear near the proposed out point. If you cannot
find it, your timecode is wrong. Do not invent the quote.

**Check `expected_segments`.** A beat the extractor marked as expecting 2–3
segments and that came back with one is probably a missed butt-cut, not a clean
single. Four of 24 aired beats were butt-cuts pulling 2–3 slices from one source.

If nothing is good enough for a beat, say so and flag nothing. A bad pick costs
more than an honest gap, because it gets discovered in the edit bay.

Write `picks.json` — **the grader's pass-two object passed through**, plus
`platform`, `title` and `transcript_rung`. Not a reduction. Step 8's report is
built entirely from `ranked`, `source_mix` and `diversity_floor_applied`; a
five-field picks file makes six of its seven required callouts impossible. Schema
in `schemas.md`.

```bash
python3 scripts/contract_check.py picks picks.json
```

### Snap in-points before writing

The grader reports raw transcript timestamps and explicitly leaves snapping to
this pipeline. Do it here: Jeff talks into the clip, so for each segment move the
in-point to a clean entry **2–5 seconds before** the moment, on a sentence
boundary in the transcript rather than mid-clause. Leave the out-point where the
outcue lands. If a segment cannot be entered cleanly without 30 seconds of anchor
setup, note it — the clip is weaker than its content suggests.

**Checkpoint 3 here.**

## Step 7 — Manifest (no automated cut stage)

**There is no `clip` subcommand and no download-and-cut code path in
`rossen_harvest`.** `--help` lists exactly two subcommands, `harvest` (alias
`search`) and `eval` — nothing that downloads or trims video. The only
`yt-dlp`/`ffmpeg` call in the package is inside `vertical_transcribe.py`'s
`download_audio()`, which pulls audio only, into a scratch `.wav`, solely to feed
Whisper; it does not save video or take in/out points. There is no FCPXML writer.

So this step is a handoff, not a render: hand-write `clips/manifest.json` from
`picks.json` — one entry per beat with URL, platform, `source_type`, and segments.
That file plus the outline w/ videos `.docx` are the deliverable. Pulling and cutting happens
downstream, manually. **Don't claim clips were downloaded or cut**; say what
happened, which is that picks were located, verified against transcript, and logged
with exact timecodes for someone else to pull.

If a real cut stage is built later (video pull + ffmpeg trim + FCPXML writer as an
actual `clip` subcommand), rewrite this step. Until then this is accurate, not
aspirational.

## Step 8 — Report + outline w/ videos

**Primary deliverable: the outline w/ videos `.docx`.** Write each pick back into its
story as a `### Videos` row, exactly as `rossen-story-outline` specifies — beat row
number, `[source — title](URL)`, what it shows, in–out with the verbatim outcue
(`BUTT` between segments), and status. Manual-lane beats get the native post link and
`MANUAL`, no invented timecode. Rung-3 beats get `· UNVERIFIED`. Empty beats get
`EMPTY` and a reason, and go into the outline's Decisions. When an approved swap
changes the case, rewrite that beat row's Who and What happens in the outline —
there is no script yet to rewrite. Flip the header to `**Stage:** videos`, update the
running order's `found/needed`, then:

```bash
python3 <skills-dir>/rossen-story-outline/scripts/check_outline.py outline.md --stage videos
python3 <skills-dir>/rossen-story-outline/scripts/build_outline.py outline.md -o "MM_DD_OUTLINE_<SHOW>.docx"
```

The producer reads the outline, not a terminal table.

Alongside it, a compact table — beat, role, chosen clip, platform, source type,
duration, outcue — and above that, the episode source mix:

```
Source mix, 10 beats:  affiliate 8 · first_person 1 · creator_long 1
```

Then call out, explicitly — every one of these reads a field from `picks.json`, so
run `contract_check.py picks` first:

- beats with no usable clip (`flagged: null`)
- beats where the pick was weak and a human should re-check (`score`, `flags`,
  `reasoning`)
- any source type at 70% or more of the picks (`source_mix`), plus the beats where
  the runner-up was a different type (`ranked`) — those are the cheap swaps
- beats where the diversity floor promoted a candidate that then lost pass two
  (`diversity_floor_applied` + `ranked`)
- beats that reached only rung 3, and why
- beats routed to the manual lane, with their native links
- whether the run was degraded by a missing search key or a dead network path

## Step 9 — Append to the beat yield log

Every run, every beat — not just failures. One row per beat, appended to **exactly
this path**, inside the beat-extractor skill:

```
<skills-dir>/rossen-beat-extractor/reference/beat_yield.md
```

Write the full path, not a bare `reference/beat_yield.md`. That ambiguity has
already caused a real failure: a bare relative path resolved to a second file at
the repo root, and for three runs the pipeline appended there while the copy
shipping with the skill sat frozen an episode behind. The two drifted into
incompatible schemas with zero overlapping episodes before anyone noticed. The log
lives inside the skill because that is what travels when the skill is deployed to
an account.

If the log does not exist, create it with its canonical header rather than
improvising columns:

```bash
python3 scripts/init_yield_log.py
```

Read the schema and outcome vocabulary from the log's own header — `PICK`, `WEAK`,
`MANUAL`, `SWAP`, `SHOW-PRODUCED`, `EMPTY`, `THROTTLED`, `CORRECTED`. If you need a new outcome
value, add it to that header table in the same commit so the next run inherits it
instead of coining a synonym.

Beyond per-beat rows, log what only becomes visible across runs:

- **Structural dead ends.** Vertical `evidence` has gone 0-for-4 across two
  episodes. That is the most useful thing in the file — it tells whoever
  writes the outline to stop planning beats that cannot be sourced, which is cheaper than sourcing
  them well.
- **Process bugs found and what fixed them**, with enough detail that a future run
  recognizes the symptom. Two of the three most costly errors in this pipeline's
  history were diagnosis errors, not search failures: orientation inferred from
  duration, and rate-limiting read as a hard IP block.
- **Sourcability-scan calibration** — predictions it got right or wrong, and
  whether manual-lane routing produced a usable clip.

`SHOW-PRODUCED` is not a failure and must never be logged as `EMPTY`. A beat
correctly identified as un-sourceable *before* search ran is the scan working.

## Timing

| Step | Wednesday | Friday |
|---|---|---|
| 1–2 beats, queries, routing | ~1 min | ~1 min |
| 3 search | ~2 min | ~1 min |
| 4 triage | ~1 min | <1 min |
| 5 captions / Whisper | ~1 min | ~2 min (Whisper-heavy) |
| 6 grade + snap | ~1.5 min | ~1 min |
| 7 manifest | <1 min | <1 min |

Roughly 8–9 minutes Wednesday, 4–5 Friday. Friday spends less on search and more
on Whisper, because its beats are vertical. If a stage runs far over, say so rather
than waiting silently.

## Resuming

Every stage writes a file, and `harvest.db` caches searches and captions for two
weeks. To resume, start at the first stage whose output file is missing — then run
`contract_check.py` on the last file that *does* exist before building on it, since
a resumed run is exactly where a reduced stage file survives unnoticed. Delete
`harvest.db` only to force a genuinely cold run.
