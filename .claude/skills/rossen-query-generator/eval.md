# Evaluation

Load this when re-running the eval, tuning register weights, or deciding whether
a register earns its budget. The conclusions live in the per-role table in
`SKILL.md`; the evidence lives here.

- [The metric](#the-metric)
- [Measured results, horizontal/YouTube](#measured-results-horizontalyoutube)
- [How to read a small sample](#how-to-read-a-small-sample)
- [Data quality — check this before trusting any number](#data-quality--check-this-before-trusting-any-number)
- [The vertical eval, not yet run](#the-vertical-eval-not-yet-run)

## The metric

**Does the clip that actually aired appear in the top thirty results for at least
one generated query.** Nothing else. Track per register so weighting is tuned from
data rather than assumption, and report *which* register hit, not just whether one
did.

Three columns, because coverage alone cannot tell you what to cut:

| Column | Question |
|---|---|
| **any** | did this register find the target at all |
| **best** | did it find it at the highest rank of any register |
| **unique** | was it the *only* register that found it |

`unique` is the column that changes decisions. A register with wide `any` and zero
`unique` is buying rank quality, not reach — worth keeping only if rank matters,
and cuttable first when budget is tight.

## Measured results, horizontal/YouTube

One recall@30 run against `rossen_eval_worksheet.csv`. Horizontal/YouTube beats
only, n=9 rows, **8 testable** after the data-quality bug below.

**recall@30 = 0.889.** Above the 70% "build on it" threshold. When a query hits it
ranks well: median best-rank 1, max 3.

| register | any | best | unique |
|---|---|---|---|
| platform | 8 | 2 | **1** |
| news | 6 | 4 | 0 |
| anchor | 5 | 2 | 0 |
| victim | **0** | 0 | 0 |

**Independently reproduced, 2026-07-28.** A separate probe on a different index
(general web search rather than `ytsearch30`) and a different beat instance ran the
published `victim` string for the `05-06-b03` worked example — `I was a cop and I
got scammed` — and returned nothing related to the target across ten results. The
published `anchor` string for the same beat returned the aired subject's affiliate
package at **rank 1**. Different method, same conclusion on both registers. That
is now two independent measurements of `victim` = 0 on horizontal/YouTube.

## How to read a small sample

- **`platform` is the workhorse on horizontal/YouTube.** It found every hit that
  surfaced at all, and it is the only register with a `unique` hit. Strongest
  evidence yet that `platform` earns its budget even on YouTube, not just
  TikTok/Shorts.
- **`victim` found nothing, twice, on horizontal/YouTube.** It is now *disproven
  for this role/orientation*, not merely unproven — which is why the per-role table
  marks it optional on the horizontal rows. It remains **untested on vertical**,
  which is where it was theorized to matter, so it stays in the vertical rows
  unqualified until the vertical eval runs.
- **`news` and `anchor` have wide `any` and zero `unique`.** Every hit they found,
  `platform` also found. Their value is rank quality — `news` took best-rank 4 of 8
  times — and dated-event beats, where `anchor` is naturally strong. Keep them;
  they are cheap and they improve rank. Do not expect them to extend reach.
- **The one miss** was a beat whose aired clip was titled in a station's
  "Investigates" franchise style rather than plain headline syntax. That produced
  the investigative-franchise entry in `glossary.md`, and the 2026-07-28 probe
  above hit through exactly that pattern — a "Contact 5" package — which is weak
  but real evidence the entry works.

## Data quality — check this before trusting any number

**URL casing corruption silently drops rows.** Roughly half the YouTube URLs in
one copy of `rossen_eval_worksheet.csv` were found fully uppercased, which corrupts
case-sensitive video IDs.

**The same corruption is in `aired_examples.md`, the shipped calibration set** —
measured 2026-07-28: **13 of 26 URLs uppercased, 12 IDs unrecoverable.** Confirmed
against a sibling: the clip-grader cites `watch?v=I3667lq1L2o`; `aired_examples.md`
has `I3667LQ1L2O`. Earlier versions of this document warned about the worksheet
only, so the calibration set was carrying the same bug unflagged.

Before any eval run:

```bash
python3 scripts/normalize_urls.py reference/aired_examples.md
python3 scripts/normalize_urls.py rossen_eval_worksheet.csv
```

The corruption is **lossy**. Scheme and host lowercase safely; a case-sensitive
video ID does not — once `I3667lq1L2o` became `I3667LQ1L2O` the original is gone.
The script reports those IDs as UNRECOVERABLE so they get re-sourced by title.
**Never guess at casing, and never count a corrupted row as an eval miss** — it is
a data-quality drop and scoring it as a miss understates recall.

**Survivor-bias caveat on the 0.889.** The reported figure rests on the 8 rows that
survived the corruption — plausibly the rows that happened to be lowercase, which
is not a random subset of the 9. Treat 0.889 as directional. It is above the
threshold, it is not a precise estimate, and it should be re-run on a repaired set.

## The vertical eval, not yet run

**This is the named gap and it is the largest open question in the skill.** Three
of five registers — `platform`, `shorts`, `victim` — have their theorized home on
vertical surfaces, and none has been measured there.

Scope, so it can be run without re-deciding the design:

- **Population.** The vertical beats in `aired_examples.md` — 7 of 26 — plus any
  vertical rows in the worksheet. Repair casing first; TikTok handles are
  case-sensitive too and several are corrupted.
- **Surfaces.** TikTok native search and YouTube Shorts (`ytsearch30:<query>
  #shorts` with `--match-filter "duration < 60"`). Do not substitute a general web
  index — Brave returns real TikTok `/video/` permalinks in roughly 19% of raw
  results, so a web-index proxy will understate TikTok recall badly.
- **Registers to separate.** `platform` TikTok-dialect vs `shorts` dialect must be
  scored apart. They are different strings for different indexes and collapsing
  them is what left Shorts unmeasured in the first place.
- **The decision it settles.** Whether `victim` keeps its place in the vertical
  rows of the per-role table. It has been measured at zero twice on horizontal; if
  it also contributes nothing on vertical, it should be cut outright rather than
  carried on a theory.

Report the same three columns. Append the result here and update the per-role
table's annotations in the same commit.
