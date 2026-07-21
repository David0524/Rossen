# rossen_harvest

YouTube harvest and the Task 1 eval harness. Metadata and thumbnails only,
no video bytes touched.

## Install

    pip install yt-dlp

No other dependencies. Stdlib for everything else.

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

    python -m rossen_harvest harvest queries.json --out candidates.json

Dedupes and writes to `harvest.db`. Vertical beats are skipped, since
the orientation marker is a hard platform constraint.

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

33 offline tests covering normalization, compilation detection, wire
package collapse, cache TTL, and URL parsing. The network call itself is
not covered and has never been executed. See below.

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
