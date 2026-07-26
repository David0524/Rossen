# FRIDAY 08/07/2026 — "Amazon OWES You Money" — pipeline run report

**Theme:** Amazon refunds you never claimed · A-to-Z guarantee denials · the $309.5M retrocharge settlement
**Scope:** **clip 1 only**, by request. Beats 2-5 were identified during extraction but not queried, searched, or graded.
**Sidecar hints:** none. No `beats_hint.json` next to `script.docx` — hints-vs-generated comparison is **N/A this run**.

## Preflight

| Check | Result |
|---|---|
| pandoc | missing → installed via `apt-get` |
| yt-dlp | 2026.07.04 ✅ |
| faster-whisper | missing → installed via `pip` |
| ffmpeg | already present ✅ |
| `BRAVE_API_KEY` | **present and authorizing (HTTP 200)** ✅ — full coverage, run was *not* degraded by a missing key |
| YouTube **search** (flat-playlist) | ✅ OK |
| YouTube **captions** (per-video page) | ❌ **BOT-WALLED** |
| YouTube **media bytes** | ❌ **BLOCKED** |

The search key question you flagged as a stop condition is clean: Brave is present and authorizes, so this run had the full three-surface coverage, not the ~70% YouTube-only fallback. No beat failure here is an artifact of a missing key.

**What did go wrong is the other two YouTube paths.** They fail independently of search, and this run hit the worst pairing: search answered normally (322 raw candidates) while both the per-video page and media bytes were gated. That takes out rung 1 and rung 2 of the transcript ladder at the same time — no captions to read, and no bytes for Whisper to transcribe — leaving rung 3 (honest unverified flag) as the only reachable outcome for any YouTube candidate.

I confirmed this is a block and not a rate-limit throttle before reporting it, per protocol: probed once, did not loop or iterate player clients, then re-confirmed several minutes later through the ordinary `fetch_many` path at normal pace on all five shortlist videos — **0 of 5**. Not a burst artifact.

## Beat table

| Beat | Role | Or. | Outcome | Source | In–Out · Outcue |
|---|---|---|---|---|---|
| 08-07-b01 | explainer_demo/creator_long | H | **UNVERIFIED pick** | In the Black `_8W0-cK5XTQ` (creator_long, 270s) | 1:02–1:41 · "worth a shot though" — **carried from producer draft, not confirmed** |

**Source mix, 1 beat:** creator_long 1.

## Search results

322 raw candidates → 257 unique YouTube · 55 news_web · 9 reddit. 14 queries via YouTube, 8+8 via the two Brave endpoints.

Register breakdown of the raw pool: shorts 86 · news 73 · anchor 73 · platform 61 · victim 29.

## The pick, and why it stands despite no transcript

The script arrived with clip 1 **already filled in** by the producer: `_8W0-cK5XTQ`, "DO THIS every time a Amazon package arrives late," In the Black, 270s.

The generated queries surfaced that exact video at **rank 1**, hit by **11 of 14 query strings** spanning all five registers (anchor, news, victim, platform, shorts). That convergence is real independent evidence the footage is right — arrived at without reference to what was already in the doc.

It also fits the beat on every axis metadata can see: an established consumer-finance channel doing an actual screen-recorded walkthrough of the Amazon guaranteed-delivery refund path, which is precisely what `explainer_demo/creator_long` asks for (and a role where a good creator video is the *natural* source, not a degraded affiliate substitute). 270s comfortably contains the proposed 39s segment plus setup runway.

**What I could not do is verify the outcue**, and the pipeline's central rule is that an unverified outcue never gets asserted as verified. So the pick carries `outcue_verified: false` and the timecode is flagged as producer-supplied throughout — `picks.json`, `clips/manifest.json`, and the Bible doc. Nothing was invented; nothing was promoted to fill the gap.

**This means the editor must confirm 1:02–1:41 against the source before cutting.** The phrase "worth a shot though" was never located in a transcript by this run.

## Pass-one shortlist (metadata triage)

Five survivors, all `creator_long` except one `first_person`. Hard filters removed compilations, AI-slop channels ("Amazon Refund Method Free," "How to hack Amazon in easy," and a cluster of free-Prime-membership bait), one junk-title artifact, and a large volume of off-topic Amazon-seller-side content that the broad queries pulled in.

| # | Source | Type | Dur | Note |
|---|---|---|---|---|
| 1 | In the Black `_8W0-cK5XTQ` | creator_long | 270s | rank 1, 11-query convergence |
| 2 | MrHowTo `s4i6WQdHF00` | creator_long | 180s | direct topical match |
| 3 | Learn with Freddie `jHzGq_Ztb5c` | creator_long | 147s | 2025 full-guide framing |
| 4 | Tada Yada `DZ06YW82Qh8` | creator_long | 282s | topical, weaker channel signal |
| 5 | aleks dude `sKhE-ez4dGQ` | first_person | 88s | the one candidate that actually shows the *chat-agent* ask, which is the beat's closing line ("you have to say the words") |

The diversity floor did not need to fire — the shortlist was already mixed, and `creator_long` is the natural type for this role rather than a monoculture to break up.

Candidate 5 is worth a human look if the producer wants the "ask the agent flat out for an account credit" line landed on screen by a real person rather than described. It was not promoted over candidate 1 because at 88s with an unknown individual channel it is the weaker source, and without a transcript I cannot confirm the chat exchange is legible on camera.

## Gaps and what I worked around

- **Zero query-side failures.** The beat returned 322 candidates and the right video at rank 1. No re-query was needed. Per the diagnose-before-repair rule, this was never a query problem, so nothing was swapped.
- **No script-touching repair was proposed**, so **Checkpoint 2 never triggered.** The pick matches what the script already says; no case swap, no name change, no rewritten setup lines. Nothing needed your approval.
- **Transcript ladder exhausted, not skipped.** Rung 1 (captions) attempted through the real library path on all 5 — all null. Rung 2 (Whisper) unavailable, because media bytes are blocked and Whisper's reach is exactly as wide as media access; it is a transcription step, not a way around a block. Rung 3 is where this landed, correctly.
- **`fetch_many` contract respected** — bare video IDs, not full URLs. The double-prefix bug that has bitten a prior run did not recur; the nulls here are the bot wall, confirmed by the raw yt-dlp error text.
- **No downloads, no cuts.** As designed — there is no automated download-and-cut stage in `rossen_harvest`. The deliverable is the located pick plus timecodes for a human to pull. In this environment the bytes were gated anyway.

## Beats not covered (out of scope this run)

Clips 2-5 exist in the script and were read during extraction but not processed, per your "clip 1 only" instruction. For planning:

| Clip | Or. | Shape | Note |
|---|---|---|---|
| 2 | V | TikTok, late-package refund demo | already filled in draft |
| 3 | V | TikTok, "delivered but nothing there" shoppers | already filled in draft |
| 4 | H | ABC7 $12,000 tiny home, denied twice | **news_web (abc7.com), not YouTube** — expect LOCATED, no caption track |
| 5 | V | TikTok, $309.5M settlement latest | already filled in draft |

Three of the four are vertical TikTok, which needs the Whisper path — unavailable while media is blocked. If you want 2-5 run, it is worth doing from an environment with working YouTube media access, or accepting unverified outcues across the board.

## Deliverables written

- `beats.json` — beat 08-07-b01 with four-register queries
- `candidates.json` — 322 candidates
- `shortlist.json` — 5 pass-one survivors
- `picks.json` — the flagged pick, outcue marked unverified
- `clips/manifest.json` — handoff manifest for the edit bay
- `FRIDAY_08072026_BIBLE_updated.docx` — filled Bible doc, clip 1 link + timecodes in blue, unverified status called out
- `report.md` — this file
- appended to `.claude/skills/rossen-beat-extractor/reference/beat_yield.md` (added a new `UNVERIFIED` outcome value to the log's header table in the same commit, since a pick with an unreachable transcript did not fit the existing vocabulary)
