# Beat yield log

Appended every pipeline run, every beat — not just failures. The point is to
learn which roles/orientations reliably yield an airable clip and which are
structural dead ends, so the bible can be written toward what sources exist.

Columns: run · beat · role · orientation · outcome · why / source
Outcomes: PICK (verified outcue) · LOCATED (case found, no caption-able source)
· SWAP (needs script change) · EMPTY (nothing cleared the bar)
· WEAK (flagged, low score or flags) · MANUAL (native post is the pick) · THROTTLED (bot wall; transcript not reached) · SHOW-PRODUCED (DEMO, never EMPTY) · REUSED (verified pick carried from a prior run, re-verified)

## Run F2_07292026 (AI voice-clone / agency impersonation / back-to-school)

| Beat | Role | Or. | Outcome | Why / source |
|---|---|---|---|---|
| F2b-b01 | victim_interview | H | LOCATED | Del Mastro $5,400 case on ABC7 SF (news_web); no captioned YT twin |
| F2b-b02 | explainer_demo | H | PICK (swap) | FOX4 Dallas gMXuQ4MusPk 2:00-2:12 "it's my voice artificially generated" (Greg Bull/Noviello; script rewritten off Dickherber) |
| F2b-b03 | victim_interview | H | PICK (swap) | KATU sPIIFyPyKKE 1:37-2:30 "It's your child" (Tina/Hillsboro $2,500; reframed from raw-audio to recount) |
| F2b-b04 | authority_report | H | LOCATED | Olathe PD kids-voice case on KMBC/KCTV (news_web); no captioned YT twin |
| F2b-b05 | victim_interview | H | LOCATED | Schildhorn on FOX29/CNN (news_web); YouTube only AI-slop reposts |
| F2b-b06 | victim_interview | H | PICK | WFLA As4nS5aOVnw 0:38-1:02 "so she gave it to them" (Brightwell $15K, exact) |
| F2b-b07 | authority_report | H | EMPTY | IC3 alert I-072026-PSA (5 days old); only generic FBI-scam packages |
| F2b-b08 | evidence | V | EMPTY | No fake-IC3-site/deepfake-official screen recording (vertical evidence) |
| F2b-b09 | authority_report | H | PICK | WPRI rkZMNuoNfqA 1:25-1:48 "deposit money into a Bitcoin ATM" (fit: not agent/badge angle) |
| F2b-b10 | authority_report | H | PICK | WCNC JUbuCpPGX3g 0:27-0:55 "the S standing for secure" (fit: not IRS-CI specific) |
| F2b-b11 | evidence | V | EMPTY | No nurse/coach/tuition scam-text screen recording (vertical evidence) |
| F2b-b12 | explainer_demo | H | EMPTY | No Target Circle barcode-scan demo (KPRC hit = boarding-pass barcodes) |

**Yield:** 5 PICK (incl. 2 approved swaps) / 3 LOCATED / 4 EMPTY of 12.
**Pattern:** vertical `evidence` 0/2 (both empty) — worst category, again. Named
victims frequently source only to news_web (no captions) — LOCATED, not PICK.
`authority_report` on <2-week-old federal alerts (b07) too new for captioned video.
Brave news_web leg was decisive: b02/b01/b04/b05/b06 exact cases surfaced only there.

## Run W_10072026 (A face-match wrongful arrest · B store/grocery tracking · C fast food brings back humans)

| Beat | Role | Or. | Outcome | Why / source |
|---|---|---|---|---|
| 10-07-A2 | victim_interview | H | WEAK | ABC News 4/WCYB EcWQI5Zrj4Q 0:16-0:31 "a state she'd never even visited" — reporter VO; no Lipps soundbite reached (NBC/WLOS captions throttled; WDAY not found) |
| 10-07-A3 | authority_report | H | PICK | ABC News 4/WCYB EcWQI5Zrj4Q 0:31-0:46 "an arrest warrant to be issued for her" BUTT 0:46-1:00 "between April and May of 2025" (attorney Rice) |
| 10-07-A4 | victim_interview | H | PICK | CBS News 6gUOZ7tYfZ8 1:16-1:46 "the same clothes she was booked in in July" (correspondent, not victim; CBS misnames her "Lipscomb" at 0:32/1:08) |
| 10-07-A5 | authority_report | H | THROTTLED | KVRR SGFrtUVY6nc (chief admits mistakes) — caption bot wall on two spaced attempts |
| 10-07-A6 | authority_report | H | PICK | CBS News 6gUOZ7tYfZ8 0:00-0:19 "for false arrest" BUTT 0:42-0:57 "what she believes was malicious prosecution" |
| 10-07-A8 | — | — | SHOW-PRODUCED | Jeff demo: location history on his phone |
| 10-07-B1 | explainer_demo/creator_short | V BROLL | REUSED · PICK · CROP | Instacart IO1wx3zBR6s 0:00-0:43 / 0:48-1:08, from LIVE_10072026, re-verified |
| 10-07-B2 | first_person_rant | V | MANUAL | TikTok @user60342208753 7679448051202657566 (no captions; media blocked) |
| 10-07-B3 | authority_report | H | REUSED · PICK | NBC Connecticut jTKvp41lHZc 0:17-0:51 / 1:22-1:37, from LIVE_10072026, re-verified |
| 10-07-B4 | — | — | SHOW-PRODUCED | Jeff demo: store-app location/Bluetooth off |
| 10-07-C1 | evidence | V | MANUAL | Two options, call later: @typical_redhead_ 7192248491853303086 (McDonald's McNuggets, via TODAY) · @kristinealise 7522285144254795038 (Taco Bell "one thousand waters", via Daily Dot). Search leg found only 2023 roundups |
| 10-07-C2 | authority_report | H | WEAK | NBC News lsqR0oxtvOw 1:11-1:16 / 1:24-1:44 — Feb BK "Patty" headset story, not the Sept 23 drive-offs quote; no drive-off video found |
| 10-07-C3 | authority_report | H | WEAK | Ecomix Simple sXSImjg6CMU 0:16-0:29 "Not on the app. On hospitality." — 47-view channel, possible AI narration; no network package on the retraining |

**Yield:** 4 PICK (1 reused) + 1 PICK·CROP (reused) / 3 WEAK / 2 MANUAL / 1 THROTTLED / 2 SHOW-PRODUCED, of 11 clip beats + 2 demos.
**Degraded run:** media bytes blocked all run (no Whisper); YouTube caption path bot-walled mid-run — 5/26 on pass 1, 7 more on one spaced retry (~7 min later), 14 still null. Throttle, not block: the retry path recovered some IDs.
**Pattern:** a named victim with heavy national coverage (Lipps) still yielded no reachable soundbite — network pieces were correspondent live shots. Trade-press-only corporate announcements (Burger King drive-offs, McDonald's Make It Golden) are near-unsourceable on YouTube within 2 weeks; plan graphics. Sourcability scan got C2/C3 right (commentary_only → WEAK).
**Process note:** prior-run reuse (Step 7) worked — two picks carried and re-verified on rung 1 in one call, zero search spend.

## Run W_10142026 (A mall skincare pressure sales · B caregiver $5 deed · C fake AI property-tax video)

| Beat | Role | Or. | Outcome | Why / source |
|---|---|---|---|---|
| 10-14-A2 | victim_interview | H | PICK | First Coast News 3iz8G25Taxg 0:42-0:58 "Didn't tell anybody" BUTT 2:10-2:21 "what was happening" |
| 10-14-A3 | victim_interview | H | PICK | ABC15 Arizona Xh8ZOedc2hM 1:09-1:37 "times, at least" BUTT 1:52-2:09 "I'm ashamed" |
| 10-14-A4 | victim_interview | H | PICK | CBS LA 6OGQNCnZTfE 0:18-0:53 "in separate transactions" BUTT 1:03-1:26 "Uh no, I did not" |
| 10-14-A5 | news_report | H | PICK | CBS LA I_AnpuMDlls 2:04-2:37 "our state attorney general" BUTT 4:41-5:09 "independently operated tenant" |
| 10-14-A6 | news_report | H | PICK | CBS LA g9e4ElDgYG8 0:22-0:33 "the B and Co name remains" BUTT 3:03-3:27 "making large purchases at multiple stores" |
| 10-14-A7 | news_report | H | PICK | KOIN 6 VaEws6itP08 0:32-0:48 "bh28 skincare consultants" BUTT 2:22-3:11 "bank teller called police" |
| 10-14-B1 | victim_interview | V | PICK | WSMV 4 Nashville (Short, repost of WMBF) 3EzgKCWb83Q 0:39-1:11 "dead for 3 days" BUTT 1:43-2:22 "this is my dad's house" |
| 10-14-B2 | victim_interview | H | PICK | WMBF News 7WXREQ4_5Vo 3:10-3:38 "even after he died" |
| 10-14-B3 | news_report | H | PICK | WMBF News ikapZ9dVJ5I 0:59-1:27 "I was relieved" |
| 10-14-C1 | evidence | H | PICK | Denver7 ibgJMgcsihI 0:12-0:27 "It's completely AI" |
| 10-14-C2 | news_report | H | PICK | Denver7 ibgJMgcsihI 0:28-0:54 "whole new challenge" |

**Yield:** 11 PICK of 11 clip beats (B1/B2 rows swapped at Checkpoint 3 so both match orientation). Source mix: affiliate 10 · network 1 (Inside Edition alternate only).
**Degraded run:** captions bot-walled 15/16 on the first pass and again on a 7-min spaced retry at concurrency 2; mweb client returned no tracks. A third pass ~30 min later got 11/16, a fourth 13/16. Throttle, not block — it needed time, not workarounds. Media bytes blocked all run (no vertical beats needed Whisper).
**Pattern:** HAVE rows from the pre-bible carried the run — 8 of 11 picks were the pre-bible's own links. Harvest search missed three exact-match local packages (ABC15, KOIN 6, WMBF original) that a plain targeted yt-dlp search found at rank 1; generic titles ("widow", "bee") drowned the harvest ranking. A news piece that airs the scam video (Denver7) solved an evidence/BROLL beat without naming any real channel as the scam.
