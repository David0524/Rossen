# rossen_harvest

YouTube harvest and the Task 1 eval harness. Metadata and thumbnails only,
no video bytes touched.

## Install

    pip install yt-dlp

No other dependencies for the YouTube + Brave harvest and eval. Stdlib for
everything else.

**For vertical transcription** (TikTok/Reels/X video, which ship no
captions — see `vertical_transcribe.py`):

    pip install faster-whisper

CPU-only via CTranslate2, no torch, no GPU required. Do **not** install
`curl-cffi` speculatively — in this environment it made TikTok downloads
fail (TLS handshake reset) where plain yt-dlp succeeded. Only add it if
you've confirmed plain requests are actually being blocked in your
environment; it is not a default-on dependency.

## Task 1: measure the query generator

This is the first thing to run and nothing downstream should be trusted
until it is done.

1. Have Claude Code read `.claude/skills/rossen-query-generator/SKILL.md`
   and generate queries for every YouTube row in `rossen_eval_worksheet.csv`.
   Write them to `queries.json` in the shape of `queries.example.json`.

2. Run:

       python -m rossen_harvest eval queries.json rossen_eval_worksheet.csv --out eval.json

Output: recall@30 overall, a per-register breakdown, per-role breakdown,
rank distribution, and the list of misses.

Read the register table carefully. Three columns:

- **best rank** — the register that surfaced the clip highest
- **any rank** — every register that found it at all
- **unique contribution** — hits that ONLY that register found

Unique contribution is the one that matters. A register with high "any"
and zero "unique" is redundant and can be dropped from the query budget.
That is how the weighting table in the skill gets replaced with measured
weights instead of inferred ones.

**Interpretation:** above 70%, build the harvest on it. Below 50%, the
glossary is the problem, fix it before writing more code.

The 8 vertical rows cannot be resolved by yt-dlp search and are skipped.
Search those by hand. They are the only evidence about whether the victim
and platform registers earn their place.

## Production harvest

    python -m rossen_harvest search queries.json --out candidates.json

(`search` and `harvest` are the same command.) Runs two backends, dedupes
across both, and writes to `harvest.db`.

- **YouTube** (`youtube.py`) — horizontal beats, as before.
- **Brave** (`brave.py`) — the leg YouTube cannot reach: network and
  affiliate video on the outlet's own site (`news_web`), and the vertical
  platforms. A beat is routed to Brave when its `platforms` include any of
  `news_web, tiktok, instagram, facebook, x, reddit`, or when it is
  vertical. **Vertical beats are no longer skipped** — Brave is their only
  search coverage.

### Shorts and the orientation gate (`shorts.py`)

Added 2026-07-25 after the vertical smoke test found two defects.

**The Shorts duration ceiling was stale.** The pipeline gated on
`duration < 60`, YouTube's limit until October 2024; it is now three
minutes. `SHORTS_MAX_DURATION` is 180. Duration is only a pre-filter — the
real test is `is_short()`, which checks whether `GET /shorts/<id>` returns
200 or redirects to `/watch`. Nothing else can tell a 119-second Short from
a 119-second normal upload.

**The `#shorts` suffix underperformed.** Suffixed `ytsearch` queries matched
description text rather than format and returned mostly landscape news
packages. Beats that want Shorts now also run `site:youtube.com/shorts …`
through the Brave web endpoint as a synthetic `shorts_web` register, which
constrains on the URL path and cannot return a non-Short. Both legs run;
which one earns its budget is a question for the eval.

**Orientation is read from pixels, never from duration.** This is the
vertical postmortem fix. `verify_orientation()` uses yt-dlp's format
dimensions when available and otherwise the original-aspect-ratio thumbnail
(`oardefault.jpg` / `oar2.jpg`) — a landscape video has no `oar` variant at
all, so a 404 is the answer. It works when media bytes are blocked, which
they were in the smoke-test environment. The harvest step runs the gate
automatically over YouTube candidates on vertical beats:

    --no-verify-orientation   skip the gate (offline work only)
    --drop-landscape          remove verified-landscape candidates, not just flag them

`unknown` is never treated as a pass, and `--drop-landscape` only removes
candidates positively verified landscape — a network wobble must not
silently shrink the funnel. TikTok and Instagram are not gated here: both
serve landscape into portrait slots (the smoke test found a 640x360 clip on
a `/reel/` URL) but probing them costs a media fetch, so it belongs in the
grader's shortlist pass.

    python3 tests/test_shorts.py    # 44 tests, network stubbed

Brave needs `BRAVE_API_KEY` in the environment. Without it, the run prints
a `DEGRADED` warning naming every beat that lost coverage and continues
YouTube-only rather than failing. `--no-brave` forces YouTube-only
deliberately.

### What Brave does and does not surface

Confirmed against the live API:

- **Strong:** off-YouTube network/affiliate video (`news_web`), Reddit
  threads, and — for a *named* person — the press coverage that points to
  their own social post. This is the self-recorded-beat workflow: search
  the name, find the coverage, hand the producer the native post link.
- **Partial:** the Brave *video* endpoint is YouTube-heavy. It widens
  YouTube and Shorts discovery but rarely returns a native TikTok or
  Instagram post for a generic query.
- **Still a gap:** generic discovery of native TikTok/IG/X *posts* (not
  tied to a named person or a news story) needs an authenticated scraper
  or a paid social-search API. Brave is a real but partial answer there,
  and the routing is honest about it rather than pretending otherwise.

Two Brave endpoints run per eligible beat: web (news/anchor plus the
victim/platform strings that name a specific social post) and video
(short-form and confrontation strings). Per-endpoint query count is capped
by `--brave-cap` (default 8) because the free tier rate-limits at roughly
one request per second; calls are serialized and spaced automatically, and
every result is cached like any other query.

## Notes

- **Caching.** Keyed on the full `ytsearch30:{query}` string, two week TTL.
  The eval will be re-run many times while tuning; there is no reason to
  re-hit YouTube for a scored query, and yt-dlp throttles if you do.
  Delete `harvest.db` to force a cold run.
- **Concurrency** defaults to 5 with jitter. Raising it invites throttling.
- **Dedupe is per beat, not global.** One clip legitimately serves two
  beats in an episode and collapsing across beats would hide that.
- **Wire packages.** The same affiliate package appears on dozens of
  Nexstar and Sinclair channels under near-identical titles. This is a
  within-YouTube collision so cross-platform matching never catches it.
  Fuzzy title match at 0.86, earliest upload date survives, because that
  is usually the originating station and it is what matters for clearance.
  Tune `TITLE_THRESHOLD` in `dedupe.py` if it over- or under-collapses.


    python3 tests/test_offline.py
    python3 tests/test_brave.py

33 offline tests covering YouTube normalization, compilation detection,
wire package collapse, cache TTL, and URL parsing, plus 32 for Brave:
platform/id detection, date and duration parsing, web and video result
normalization, and cross-backend dedupe (a Brave-found YouTube URL
collapses with the yt-dlp candidate for the same video). The Brave
network call is exercised live on first real run, not in the suite.

## NOT VALIDATED

`YouTubeBackend.search` has never run against YouTube. It was written in
an environment with no access to it. The yt-dlp option dict and the
`ytsearch30:` invocation follow documented usage, but the exact shape of
a flat-playlist entry should be confirmed on first run:

    python3 -c "
    from yt_dlp import YoutubeDL
    with YoutubeDL({'quiet':True,'extract_flat':True,'skip_download':True}) as y:
        i = y.extract_info('ytsearch3:paypal scam', download=False)
    print(list(i['entries'][0].keys()))
    "

If `view_count`, `upload_date`, or `thumbnails` are absent from flat
entries, `from_ytdlp` in `candidates.py` needs adjusting. That is the
single most likely thing to break on first run.

## Transcripts without Whisper

`transcripts.py` fetches YouTube auto-captions via yt-dlp. No model
download, no ffmpeg, no GPU, no transcode. About a second per clip
instead of thirty, and no media bytes touched.

    from rossen_harvest.transcripts import fetch_many
    transcripts = fetch_many([c.video_id for c in shortlist], cache=cache)
    print(transcripts["I3667lq1L2o"].as_prompt())   # feed to grader pass 2

Tradeoffs, in exchange for the entire time budget:

- Caption chunks are 1-3s granular, not word level. Output is padded
  1.0s early and 1.5s late so the editor trims rather than hunts.
- Auto-captions have no speaker separation. A news package reads as one
  stream, so telling the reporter from the victim is harder.
- 5-10% of videos have captions disabled. `fetch_transcript` returns
  None; the grader should demote, not guess.

The outcue anchor survives intact. `Transcript.find(phrase)` locates a
quote and returns its cue, including phrases spanning cue boundaries, so
the grader can still be required to quote verbatim and the pipeline can
still verify the quote sits near the proposed out point.

Whisper can be added later as an optional accuracy pass on flagged clips
only. Nothing here forecloses it.


    python3 tests/test_offline.py       # 33 tests
    python3 tests/test_transcripts.py   # 24 tests
