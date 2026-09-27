# 10/07 LIVE — "Your Store Is Watching You" + "Is That Prime Day Deal Real?" — pipeline run LIVE_10072026

Script: `10_07_LIVE_BIBLE_-_YOUR_STORE_IS_WATCHING_YOU.docx` · companion `SOURCE_LOG.md` · airdate Wed 10/07/2026.

```
Outcomes, 7 beats:  1 PICK (approved swap) · 3 LOCATED (manual lane) · 3 THROTTLED
Verified segments:  2 (on the A4 swap candidate only) — every other YouTube pick is blocked, not missing
```

**The run stopped short of full grading for one reason: YouTube bot-walled this container.** Every caption fetch after the
search phase hit "Sign in to confirm you're not a bot" — 72 errors, still blocked after a 10-minute cooldown and a retry
through the normal path. Per the hard rule, those beats are recorded **THROTTLED, not empty**: the shortlists are good and the
blocked calls were not cached, so re-running Step 5 later re-fetches cleanly. Nothing was flagged without a verified outcue.

## Brave API

Working. Both endpoints the harvester uses returned 200 throughout: **0 failures across ~130 Brave calls** (pre-scan, native-post
lookups, and the Step 3 harvest). Response headers show 50 req/s and a monthly field of `0/0`, unlike the old free plan's 1 req/s
and 2,000/month — consistent with a metered plan. Your $0 cap did not block anything on this run.

## Beat table

| Beat | Role | Or. | Pri | Outcome | Best source | Status |
|---|---|---|---|---|---|---|
| A1 | first_person_rant | V | 1 | **LOCATED** | TikTok @user60342208753 `/video/7679448051202657566` | manual; ID decodes to **2026-08-29**, the script's date; outcue UNVERIFIED |
| A2 | authority_report | H | 2 | **THROTTLED** | NBC Connecticut `jTKvp41lHZc` · fallback Fox News CT (foxnews.com, 5/16/2026) | captions blocked; Fox CT is a manual pull available now |
| A3 | explainer_demo/short | V b-roll | 3 | **THROTTLED** | Omni Talk Short `jqTpde_UWs4` · Instacart `IO1wx3zBR6s` (horizontal) | captions blocked; b-roll, so eyeball-able now |
| A4 | victim_interview | H | 2 | **PICK (approved swap)** | Lesleigh Nurse, CBS/WKRG `kEN0nL8mtXw` | 2 verified segments; script rewritten |
| A5 | explainer_demo/long | H | 2 | **THROTTLED** | More Perfect Union / Consumer Reports `osxr7xSxsGo` (~4.76M) | captions blocked |
| B1 | first_person_rant | V | 1 | **LOCATED** | TikTok @kb.montalbano `/video/7523672986004606238` | manual; ID decodes to 2025-07-05; outcue UNVERIFIED |
| B2 | explainer_demo/short | V | 2 | **LOCATED (profile only)** | TikTok @semyajnotsemaj | permalink could not be pinned |

## A4 — swap APPROVED and applied (checkpoint 2 closed)

Brianna Jones has **no video anywhere reachable** — YouTube zero on three variants, confirmed on retry while search was live;
Charlotte Observer, FOX8 and WAVY are text. That is a genuine absence, not the throttle. ⚠️ Name collision: a WCJB post about a
Brianna Jones who was a Walmart *manager* in a fraud case is a different person.

Proposed swap, graded and verified:

> **Lesleigh Nurse, Semmes, Alabama** — CBS News / WKRG `kEN0nL8mtXw` (144s, captioned).
> **IN 0:00 – OUT 0:41** — outcue: "up to court by then she said the damage to her reputation had already been done"
> **IN 0:52 – OUT 1:02** — outcue: "anything wrong why would i pay for something that i didn't do but it turns"

Malfunctioning self-checkout, stopped by asset protection, arrested and mugshotted over $48 of groceries, charge dropped when
Walmart didn't show up, then a **$2.1M jury verdict**. It fits "think what you would do if this happened to you" better than
any explainer. Three things change if you take it: it's a different woman, it's an older case (suit filed 2018), and **no AI
camera is involved** — the "AI is watching your hands" line cannot sit directly over this clip. (Captions on this clip are
rolling auto-captions, so the outcue strings carry some doubled phrasing; they are verbatim from the track.)

The script's own DECIDE fallback — a news explainer on Walmart's self-checkout cameras — has only weak candidates (2019
aggregators, a KHOU short of unknown date, and a FRANCE 24 fact-check that may cut *against* the segment's framing and could not
be read this run).

## Manual lane

- **A1** `https://www.tiktok.com/@user60342208753/video/7679448051202657566` — pull the live view count on show day.
- **B1** `https://www.tiktok.com/@kb.montalbano/video/7523672986004606238` — confirm it's the cart post; 2025, keep it off any "this week" line.
- **B2** `https://www.tiktok.com/@semyajnotsemaj` — scroll to mid-July 2024. Distractify has the product and quote.

None watched. yt-dlp's TikTok extractor is failing this run, so no TikTok metadata or transcript was reachable.

## Worked around

- **YouTube bot wall on captions** — waited, retried once through the normal path, recorded THROTTLED. Did not attempt to get
  around the bot check.
- **Zero-result names diagnosed before recording** — Brianna Jones, Montalbano and Jaymes each re-queried; search was live
  (other queries returning results in between), so the zeros are real absences on YouTube.
- **NBC Connecticut added by hand** — found in the pre-scan, missed by the harvest.
- **Native permalinks confirmed by ID timestamp**, not by watching.
- No `pandoc` — XML fallback. Nexstar and Charlotte Observer pages block direct fetch.
- No `beats_hint.json` next to the script, so no hints-vs-generated comparison is possible.
- No clips downloaded or cut; there is no cut stage.

## To finish this run

Re-run captions for A2, A3, A5 (and the A4 alternates) once YouTube stops bot-checking this container — no query changes needed.
Then pass two can flag picks with verified outcues.

## Deliverable — filled bible

`10_07_LIVE_BIBLE_-_YOUR_STORE_IS_WATCHING_YOU_FILLED.docx` — the original document edited in place. 432 of 441 source paragraphs
byte-identical; the 9 rewritten for the approved swap each kept their own paragraph and run properties; 28 inserted paragraphs
all use the source's Arial / 18pt / spacing. Blue = verified clip, amber = manual pull or pending captions, no timecode invented
anywhere a transcript was unavailable.

**Swap corrections found while applying it:** her name is spelled **Lesleigh** and the store is in **Semmes**, Alabama — the
auto-captions render it "sims", and an earlier note of mine said "Mims". Confirmed against CBS News, NBC News and WVTM.

**Script lines changed for the swap (A4 block + one cold-open line):** Jones's setup replaced with Nurse's facts from the tape; a
bridge line inserted so the AI-camera lines don't sit directly over a case that involved no AI; post-clip lines now carry the
$2.1M verdict, the attributed $300M civil-recovery testimony, and that Walmart said it would appeal.

**Before air:** confirm the appeal outcome; attribute the $300M figure as testimony; confirm Eric Gardner is on camera in A5.
