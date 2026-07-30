# F2 TOP STORIES — airdate 08/12/2026 (Wednesday) — pipeline run F2_08122026

Script in: `F2_TOP_STORIES_07_30__AIRDATE_08_05_1.docx` (filename airdate stale; producer confirmed 08/12).
Deliverable: `F2_TOP_STORIES_08122026_BIBLE_updated.docx`.

The bible is the **original `.docx` edited in place**, not a regenerated document. All 431 source
paragraphs are preserved byte-identical and in order; 37 paragraphs were inserted, every one built
from the source's own paragraph and run properties (Arial, `w:sz 36`, `line=276 before=0 after=0`).
Font, size and spacing are unchanged. The only added properties are `w:color` — blue `1155CC` for a
located clip, red `C0392B` for a gap, amber `B7791F` for a caveat — and `w:u` on the eight
hyperlinks, all of which resolve to external relationships.

**Show day inferred as Wednesday, then confirmed by the producer.** Band 10–12, met.

```
Source mix, 8 located beats:  affiliate 6 · network 1 · creator_short 1
Outcomes, 11 beats:  5 PICK · 1 PICK (gated) · 2 LOCATED · 2 EMPTY · 1 SHOW-PRODUCED
```

## Beat table

| Beat | Role | Or. | Pri | Outcome | Source | IN–OUT | Outcue |
|---|---|---|---|---|---|---|---|
| b01 | victim_interview | H | 1 | **PICK** | InvestigateTV (YT) | 1:02–2:13 · 2:57–3:44 | "consequences. You understand?" · "for almost every day of my life since." |
| b02 | explainer_demo | H | 2 | **PICK** | InvestigateTV (YT) | 4:01–4:50 | "frightening how quick that happened." |
| b03 | victim_interview | H | 2 | **PICK** | InvestigateTV (YT) | 5:11–5:41 | "to be punished for what they did." |
| b04 | victim_interview | H | 1 | **PICK** | ABC7 / ABC News (YT) | 0:10–1:03 · 1:19–1:48 | "was a scam. The money was gone. With AI," · "scam your money." |
| b05 | explainer_demo | H | 2 | **EMPTY** | — | — | flagged null, see below |
| b06 | authority_report | H | 2 | **LOCATED** | KMBC 9 (news_web) | manual | no captions — no invented timecode |
| b07 | explainer_demo/creator_short | V | 1 | **LOCATED** | @pearlmania500 (TikTok) | manual | UNVERIFIED — native post, no caption track |
| b08 | authority_report | H | 2 | **PICK** | FOX 5 DC (YT) | 1:03–1:59 | "time through that fast track program" |
| b09 | victim_interview | V | 1 | **EMPTY** | — | — | flagged null, see below |
| b10 | confrontation_bust | H | 3 | **PICK (gated)** | WJZ (YT) | 1:00–1:39 | "said it doesn't make sense in retrospect" |
| b11 | other / screen share | H | 3 | **SHOW-PRODUCED** | — | — | Jeff walks missingmoney.com live |

All 8 proposed outcues were verified verbatim with `Transcript.find()` against the fetched caption track. Zero unverifiable.

## The headline result: one package carries three beats

b01, b02 and b03 all resolve to a single source — InvestigateTV's 01-23-26 package,
`https://www.youtube.com/watch?v=LZoQ5aiVibA`, 442s, captioned. The script marks b02 and b03
as BUTT FROM B01, and that is exactly how it plays: four segments off one download.

This also cancels an expected swap. Run F2_07292026 rewrote its Dickherber beat onto FOX4 Dallas
because Ann Dickherber returned nothing on YouTube. She still returns nothing by name — but she is
*inside* this package, cloning reporter Lauren Trager's voice on camera at 4:28, with Trager's
reaction at 4:48. **No swap needed this week.**

## Empty beats

**b05 — Erin West.** Five sources graded, ~2.5 hours of transcript. Her House Select Committee
testimony says "I call it the scamdemic" at 2:45 but never mentions voice cloning. The 19-minute
Operation Shamrock talk, the 63-minute Asset Reality podcast and the 59-minute AARP webinar return
**zero** hits for "anxiety", "clone" or "cloning" across 3,600+ cues. The two things the script has
her say are not attributable to her in any sourceable footage. Flagged nothing rather than airing
the wrong expert under her name.

**b09 — Susan Udvance.** Zero video coverage across 817 harvested candidates (216 vertical + 601 on
a horizontal twin run), a targeted re-query, and three direct yt-dlp searches. Brave surfaces only
her LinkedIn and ZoomInfo as a Chicago real-estate advisor — which corroborates the West Loop escrow
detail, so the case is real, but that is not footage. Everything that did surface is I-CASH
promotional coverage: right outlet, right program, opposite story. This reads like an indexing gap
rather than an absence; the detail level in the script suggests someone watched the I-Team package.
Worth one phone call to ABC7 Chicago.

## Manual lane

**b06 — Olathe PD.** The exact case exists, dated 02-03-26, matching the script's cited date. KMBC 9
and FOX4KC both carry it. **Zero** YouTube candidates mention Olathe at all across 619 harvested —
the entire beat lives on news_web. Same verdict the prior run reached on the same department.
`https://www.kmbc.com/article/olathe-police-warn-scam-child-abduction-money/70238283`

**b07 — Alex Pearlman.** Native post found:
`https://www.tiktok.com/@pearlmania500/video/7220912200855178538` — captioned "Literally billions of
unclaimed funds in every state. Go get your money", which is the script's line verbatim. Per the
skill this is the pick and no repost was graded. TikTok ships no caption track and faster-whisper is
not installed here, so the outcue is marked UNVERIFIED rather than invented.

## Source concentration and the cheap swaps

**Affiliate holds 6 of 8 located beats (75%) — above the 70% threshold.** Beats where the runner-up
was a different source type, i.e. the cheap swaps if you want variety:

- **b01** — runner-up is CNN (`ruNDY0OBpg4`, network, 539s). Different case though; you would be
  trading the exact victim for a different one, which is a script change, not a free swap.
- **b02** — third-ranked is GMA (`yxFMjTaiLOY`, network). Anchor-led, no demo. Weak trade.
- **b04** — the pick is already the non-affiliate (ABC News field package via ABC7); its runner-up is
  affiliate. This is the one beat pulling the mix *away* from monoculture.

**Diversity floor:** fired on 6 of 10 beats. It could only promote once — `@deesale00` on b08 — and
that promotion **lost in pass two** (scored 40 against the FOX 5 pick's 86; it shows the demand side,
not the treasury being flooded). On b03, b04, b06, b09 and b10 the floor fired with nothing eligible
to promote, so those shipped as pure affiliate with the reason recorded. Per the skill's note, a
floor that repeatedly promotes filler is a signal about the hard filters upstream, not about variety
being unavailable — worth watching if it repeats next run.

## Script-accuracy items (Checkpoint 3 — need your call)

These touch what the show says, so nothing was changed.

1. **b02 pronouns.** Script says "watch **his** face" and "she made **his** voice say whatever she
   wanted". The reporter whose voice gets cloned is Lauren Trager, a woman. One-word fixes.
2. **b04 dollar figure.** Script: "HE DEMANDED 20,000 DOLLARS… LOST OVER 5,000" and "FIVE HOURS".
   The ABC package says the caller demanded she wire **$5,400** and does not mention $20,000 or five
   hours. Not necessarily wrong — other coverage may carry it — but it is unsourced in the clip you
   would be rolling.
3. **b05.** Either re-attribute the two claims or cut the beat. Note the line "a few seconds of your
   voice… sounds exactly like you" is spoken almost verbatim by an unnamed expert at **1:10 in the
   b04 ABC package** — so the content is available, under a different name.
4. **b08 recency.** The FOX 5 DC package is dated 2023 and references "all of 2022". The script frames
   the TikTok stampede as current ("THE SECOND THIS TRENDS"). Also, "AN APPROVED CLAIM CAN PAY OUT IN
   ABOUT TEN DAYS" is not in the package. The Bradley Earl triple-digits line **is** on tape.
5. **b09.** If ABC7 Chicago cannot supply the I-Team package, this beat needs a swap or a cut.
6. **b10.** The script's own doubt is confirmed on tape: at 10:02 in the CBS Boston news conference an
   official says "we haven't seen any evidence of AI being used by this crew in this case." The WJZ
   package does reference a separate victim "scammed out of $38,000 using a replicated voice" at 1:38.
   Your call whether that is close enough to run.

## Run conditions

- Not degraded. `BRAVE_API_KEY` present, both backends ran, no `DEGRADED` line.
- 7,214 raw → 5,725 deduped across 11 search beats. Platform mix: youtube 4,630 · news_web 1,032 ·
  reddit 53 · tiktok 10. Low TikTok yield is the documented Brave boundary, not a query failure.
- **Three beats were re-queried after the first pass**, all on the diagnosis that good proper nouns
  returning nothing is a query miss, not a search failure: b04 (recovered the ABC7 package — the
  prior run had this case as LOCATED-only, so re-querying upgraded it to a PICK), b08 and b09.
- **One caption fetch was throttled, not empty.** Three nulls came back; two carried
  "Sign in to confirm you're not a bot". Waited and retried through the normal path: `7uB0tMldnlo`
  recovered, the other two are genuinely caption-disabled. Both are low-scoring fallbacks, neither is
  a pick. No throttle was laundered into a dead beat.
- `pandoc` is not installed; used the `zipfile`/XML fallback the extractor skill documents.
- No clips were downloaded or cut. There is no cut stage in this run — picks are located, verified
  against transcript, and logged for someone else to pull.

## Infrastructure note

The six validator commands in the runbook referenced scripts that had never been committed, in any
branch, in the repo's history — along with `dependencies.md` and `schemas.md`, which the pipeline
SKILL.md does not reference either. The five scripts were written this run at the exact paths named,
encoding contracts transcribed from the four SKILL.md files. All ran clean:

```
check_beats --day wednesday   0 errors
check_queries                 0 errors, 1 expected warn (b09 orientation DECIDE)
contract_check beats          0 errors
check_grades one              0 errors
check_grades two              0 errors
contract_check picks          0 errors
```
