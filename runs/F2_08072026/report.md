# F2 Bible — Friday 08/07/2026 — pipeline run report

Run date: 2026-07-24 · Script: `F2_BIBLE__FRIDAY_0807_1.docx` · 4 beats

```
Source mix, 4 beats:  affiliate 2 · network 1 · show_produced 1
```

Two of the four picks (b01, b02) are the **same source**, cut as a butt-cut, so
the episode draws on **two distinct clips** plus one production task.

## What you're getting

| Beat | Role | Or. | Pick | Platform | Source type | Dur | Outcue |
|---|---|---|---|---|---|---|---|
| b01 | authority_report | H | FOX 13 Tampa Bay — *Florida man helps deputies catch scammer* | youtube | affiliate | 35s cut | ✅ "come by to pick it up" |
| b02 | confrontation_bust | H | FOX 13 Tampa Bay — *same source, butt-cut* | youtube | affiliate | 51s cut | ✅ "charged with grand theft" |
| b03 | evidence | V | — show-produced — | — | — | — | n/a |
| b04 | victim_interview | H | CBS News NY — *L.I. romance scam victim who lost $468,000* | news_web | network | 112s | ⚠️ none — no captions |

Both b01/b02 outcues were verified with `Transcript.find()` against the auto-caption
track, not read by eye. Cue spans: `come by to pick it up` at 65.20–70.00s,
`charged with grand theft` at 123.16–127.28s.

## Deliverables

- `F2_BIBLE_FRIDAY_08072026_FILLED.docx` — the primary deliverable. Blue hyperlinks
  + IN/OUT + verbatim outcue at each PLAY CLIP marker; red for the case-swap, the
  show-produced beat, and the manual clip.
- `clips/manifest.json` — the pull list.
- `picks.json`, `shortlist.json`, `candidates.json`, `transcripts.json`, `beats.json`.

**Nothing was downloaded or cut.** There is no download-and-cut code path in
`rossen_harvest` — `--help` lists exactly two subcommands, `harvest`/`search` and
`eval`. Picks were located, graded against transcript, and logged with exact
timecodes for someone else to pull. Step 7 is a handoff, not a render.

## Beats with no usable clip

**b03 (fake IC3 recovery page)** — flagged empty as a *production task*, not a
search failure. This is a screen-recording-of-a-webpage beat: no third-party clip
can be guaranteed to show the two tells the script calls out (every other link
bounces to the home page, one-step intake form). Approved as show-produced at
Checkpoint 1. This was predicted by the sourcability scan before any search ran,
which is the scan working as designed.

## Beats where a human should re-check

**b04** ships as **MANUAL CLIP — no captions**. The CBS video page carries no
caption track, so no outcue could be verified and **no timecode was proposed
or invented**. Two open items:
- Vintage unconfirmed. The script's own note flags it as a 2024 package and asks
  confirm-or-swap; the page did not expose a publication date.
- Clearance is network (CBS News New York), not affiliate.

A fully-verified fallback is logged in `picks.json` but is **not** the pick:
WKMG Apopka (171s, outcue `I feel manipulated` verified at 158.32–162.48s). It is
a different victim and the second scam is a repeat *romance* scam, not a
*recovery* scam, so it does not deliver the script's turn.

## Case swaps (approved at Checkpoint 2)

**b01 and b02 were both swapped off the Manatee County / Xin Liu case.** That case
has **no video in existence** — not a query problem. Evidence:
- Four distinct YouTube query formulations returned only *The Axiom Lens*, an
  AI-narrator repost channel the beat-extractor skill names as unclearable.
- Brave surfaced the case in print only: Bradenton Herald, Patch, Pulse of Manatee.
- A page fetch of MySuncoast (WWSB ABC7 Sarasota, the local affiliate) confirmed a
  **text-only** story from March 2025 that never names Xin Liu or Det. Gary Cummings.

Replaced with the Bruce Fredy / Hillsborough County case, which keeps the story in
the Tampa Bay market and honors the script's `BUTT` marker with one source cut
twice. Setup lines were rewritten in place in the .docx so the doc reads as a
shootable rundown. **Facts lost in the swap:** Xin Liu, Det. Gary Cummings,
$3.5M/40 victims, the 79-year-old crypto victim, the 27-month sentence.

## Source-type concentration

No type holds 70%+ of picks. With only two distinct clips the mix is
affiliate 1 · network 1, so there is no monoculture to break up.

## Diversity floor

Fired on **two** beats in pass one, and in both cases the promoted candidate
**lost pass two** — the pattern the grader skill says to report:

| Beat | Promoted | Displaced | Outcome |
|---|---|---|---|
| b01 | GeekSpin (creator_long, 82) | News4JAX (90) | lost — no back catalog, likely a narrated press-release readout |
| b04 | Duluth PD (raw_footage, 84) | NBC10 Philadelphia (86) | lost — recovery-success story, inverse of the beat |

Two floor promotions losing pass two in a 3-beat run is worth watching. Per the
skill, that pattern repeating across episodes means the floor is promoting filler
and the upstream hard filters need a look, not that variety is unavailable.

## Was the run degraded?

**No — but this needed a correction mid-run.** `BRAVE_API_KEY` was present and
live-tested (HTTP 200), so no `DEGRADED` line fired and all three surfaces ran.

At Checkpoint 1 I reported YouTube captions as hard-blocked, based on 0/6 on video
IDs that the 08/05 run had captioned successfully. **That was wrong.** It was
transient rate-limiting triggered by my own rapid diagnostic burst — a dozen
`--list-subs` calls in two minutes, several looping over player clients. Twenty
minutes later the normal `fetch_many` path returned **11/12**. The preflight in
`SKILL.md` has been amended to distinguish throttling from blocking, because
calling a throttle a block costs a whole run: it converts every pick to an
unverified outcue and pushes the producer toward a degraded deliverable they
never needed to accept.

What genuinely *is* blocked in this environment: YouTube **media bytes**
(audio and video alike — confirmed with `-f bestaudio`), and **TikTok** ("Your IP
address is blocked"). Direct YouTube page fetches also bot-wall. Consequence for
the vertical path below.

## Clips that failed to download

None attempted — there is no download stage. One shortlist entry returned no
caption track: WCVB Boston `0la8ZdNqStY` (1 of 12), demoted rather than guessed at.

## Search counts

```
2166 raw -> 1736 after dedupe across 3 searched beats (youtube + brave)
  by platform: youtube 1380 · news_web 282 · shorts 56 · reddit 16 · tiktok 1 · instagram 1
  b01: 594   b02: 554   b04: 588
```

No beat returned zero candidates, so no query revision was needed.

## Pipeline changes made during this run

**Vertical beats never reached the YouTube backend.** `__main__.py` gated the whole
call on `orientation != "vertical"`, so a vertical beat's `shorts` register ran
nowhere — even though the query-generator skill states Shorts run on every
orientation. Shorts were the only vertical surface with a reachable search index
here, and they were closed on exactly the beats that needed them. Fixed: Shorts is
now its own search surface (`ShortsBackend`) running on both orientations, with
the `#shorts` suffix and a 60s ceiling applied in Python — not via
`--match-filter`, because `--flat-playlist` returns null durations and a null
silently *passes* a match filter. Null durations are kept and flagged unknown.
Contributed 56 candidates this run, including a b02 shortlist entry.

**On Whisper and vertical video.** The ask was to lean on Whisper harder for
Shorts/TikTok/Reels. Testing says that is the wrong lever *in this environment*:
Whisper consumes bytes something else must fetch first, and both YouTube media and
TikTok are blocked here, so it has zero reachable sources. It was not run. The
skill now documents a transcript ladder in cost order — captions (which cover
Shorts too, free) → Whisper → flag unverified — and states plainly that Whisper's
reach is bounded by media access rather than being a way around a block. Also
generalized `vertical_id()` past TikTok to Shorts/Reels/X/Facebook, since the id
is the cache key and an unmatched URL re-paid for a download and a Whisper run on
every tracking-param variant of the same clip.

128 tests pass, 23 new in `harvest/tests/test_shorts.py`.
