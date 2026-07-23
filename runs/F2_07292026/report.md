# F2 TOP STORIES — 07/29/2026 — pipeline run report

**Theme:** AI voice-clone scams · FBI/FTC/IRS impersonation · back-to-school
**Beats:** 12 (12 PLAY CLIP markers; no tease-trap) · **Sidecar hints:** none (`beats_hint.json` absent — hints-vs-generated comparison N/A this run)
**Preflight:** yt-dlp ✅ · ffmpeg ✅ · **BRAVE_API_KEY present** ✅ (full coverage) · pandoc missing (docx extracted via python)

## Outcome summary

| Outcome | Count | Beats |
|---|---|---|
| Clean pick (verified outcue) | 3 | b06, b09, b10 |
| Case located, news_web-only, no captions → manual timecode | 3 | b01, b04, b05 |
| Swap needed (script change) → **awaiting approval** | 2 | b02, b03 |
| Empty (nothing cleared the bar) | 4 | b07, b08, b11, b12 |

**Source mix of picks (3):** affiliate 3.
**Cut status:** BLOCKED — YouTube byte-download is bot-walled in this environment. Captions and metadata work (different endpoint); media bytes are gated across all yt-dlp clients. The 3 picks carry verified URL + in/out + verbatim outcue; the editor pulls the bytes.

## Beat-by-beat

| Beat | Role | Or. | Outcome | Source | In–Out · Outcue |
|---|---|---|---|---|---|
| b01 | victim_interview | H | **flag (located)** | ABC7 SF "Bay Area mom" (news_web) | Del Mastro/$5,400 case confirmed; no caption-able YouTube twin → manual timecode |
| b02 | explainer_demo | H | **swap?** | FOX4 Dallas generic expert demo | Ann Dickherber's KMOV demo not discretely findable; swap = different expert |
| b03 | evidence | H | **swap?** | FOX2 St. Louis (news_web) / KATU (diff. family) | "Rachel/MO recorded call" is caption-less; KATU Hillsboro plays cloned audio but is a different family |
| b04 | authority_report | H | **flag (located)** | KMBC 9 / KCTV Olathe (news_web) | Olathe PD kids-voice case confirmed; no YouTube twin → manual timecode |
| b05 | victim_interview | H | **flag (located)** | FOX29 Philadelphia / CNN (news_web) | Schildhorn case confirmed; only AI-slop reposts on YouTube → manual timecode |
| b06 | victim_interview | H | **PICK ✅** | WFLA Ch.8 (affiliate) `As4nS5aOVnw` | 0:38–1:02 · "so she gave it to them" |
| b07 | authority_report | H | **empty** | — | IC3 alert I-072026-PSA (5 days old); only generic FBI-scam packages, no case-match |
| b08 | evidence | V | **empty** | — | No fake-IC3-site screen recording / deepfake-official clip. Vertical evidence — hardest category |
| b09 | authority_report | H | **PICK ✅** | WPRI 12 (affiliate) `rkZMNuoNfqA` | 1:25–1:48 · "deposit money into a Bitcoin ATM" |
| b10 | authority_report | H | **PICK ✅** | WCNC (affiliate) `JUbuCpPGX3g` | 0:27–0:55 · "the S standing for secure" |
| b11 | evidence | V | **empty** | — | No nurse/coach/tuition scam-text screen recording. Vertical evidence — hardest category |
| b12 | explainer_demo | H | **empty** | — | No Target Circle barcode-scan demo (KPRC "barcode/scan" hit was boarding-pass barcodes, unrelated) |

## Gaps and what I worked around

- **Vertical evidence is the worst category, confirmed.** Both vertical `evidence` beats (b08, b11) came back empty. Native TikTok/IG post discovery for a generic query is the known Brave boundary; neither had a caption-able screen-recording match. This is the category to pre-flag at script time.
- **The exact-case vs caption-able split.** Five named/specific beats (b01, b04, b05, and the swap pair b02/b03) had their true case only on **news_web** (affiliate's own site) with **no caption-able YouTube twin**. The hard outcue rule can't be met without a transcript, so these are flagged with the located source rather than given a fabricated outcue. This is the single biggest yield-limiter this episode and it is a sourcing-reach problem, not a query problem — the queries found the right case, the footage just isn't on captioned YouTube.
- **Brave earned its place.** b02's Ann Dickherber demo returned **zero** on yt-dlp; only Brave's news_web leg found the KMOV/First Alert 4 St. Louis coverage. Same for the affiliate originals behind b01/b04/b05/b06 — the news_web leg is what surfaced the exact cases. A YouTube-only run would have flagged more of these dead with no idea the footage existed.
- **b02 re-query (per the diagnose-before-repair rule).** Good proper nouns + no case-match = query miss, so I re-queried b02 alone before concluding. The specific Dickherber demo genuinely isn't discretely uploaded; only a different expert's demo (FOX4 Dallas) is caption-able → that's a swap, held for approval.
- **Download wall.** All three picks' byte-downloads are bot-gated by YouTube in this environment. Not a pipeline failure — captions/metadata came through, timecodes are verified. Editor pulls from the URLs.

## Awaiting approval (script-touching repairs)

- **b02** — swap the named expert. Script says "Ann Dickherber, Wentzville MO." Her demo isn't discretely sourceable; **FOX4 Dallas "Expert demonstrates how AI voice scams work"** (`gMXuQ4MusPk`, 279s, caption-verified) delivers the same "watch a voice get cloned in seconds" payload with a different expert. Using it changes the name/location in the script.
- **b03** — swap the named victim. Script says "a Missouri mother named Rachel." Her recorded call is FOX2 St. Louis (news_web, caption-less); **KATU "Hillsboro family"** (`sPIIFyPyKKE`, caption-verified) plays a real cloned-voice call from a different family. Using it changes the name/location.

## Timing / notes

- Search ran long (~7 min) — Brave free-tier is serialized at ~1 req/s; 12 beats × 2 endpoints. Expected, not a fault.
- CLI reality: the pipeline's `captions` and `clip` subcommands do not exist in `rossen_harvest` (only `search`/`harvest`/`eval`). Used the package's `transcripts` module for captions and yt-dlp+ffmpeg for cutting.
