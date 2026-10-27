# W_11042026 — pipeline report (Wed 11/4 F2)

Run Oct 27, 2026 in Claude Code (cloud container), resuming the claude.ai chat handoff at Checkpoint 0.
Run folder renamed from the chat's `2026-11-04_F2` to the house `W_11042026`.

## Checkpoint 0 — preflight

| Check | Result |
|---|---|
| `rossen_harvest` | OK (repo `harvest/`) — the chat's hard stop doesn't apply here |
| faster-whisper | installed this session |
| ffmpeg | OK |
| Brave key | OK (authorizes) |
| YouTube search | OK |
| YouTube captions | OK on the probe; 3 of 4 IDs on the first `fetch_many`; GMA `PQORnk7zuLc` bot-walled twice |
| YouTube audio | blocked (as usual from this container) |
| TikTok | refuses requests (one probe); manual lane, per CLAUDE.md |

## What kind of run this was

Every clip beat was a `HAVE` row with a link and proposed in/out points in the show plan, so this was a
**verify pass, not a search**: transcripts for every reachable clip, every outcue checked against them, cuts
snapped to sentence boundaries. No `rossen_harvest search`, no `candidates.json` / `shortlist.json`: nothing
failed verification, so there was nothing to search for. A beat that had failed would have gone to search.

Source mix, 12 beats: affiliate 5 · network 3 · first_person 2 · creator_short 1 · documentary 1

| Beat | Role | Clip | Platform | Source type | Length | Outcue / status | Rung |
|---|---|---|---|---|---|---|---|
| A1 | explainer_demo/creator_short | @financeunfolded | TikTok | creator_short | 0:17 | MANUAL · UNVERIFIED (BROLL) | 3 |
| A2 | first_person_rant | @pearlmania500 | TikTok | first_person | 2:58 | MANUAL · UNVERIFIED | 3 |
| A3 | victim_interview | FOX 13 (Sept 3, 2025) | news_web | affiliate | 2:43 | "best thing that ever happened to me" · PICK | 2 (Whisper) |
| A5 | victim_interview | ABC7 Chicago (Jan 28, 2025) | YouTube | affiliate | 3:42 | "a loophole that they need to figure out" · PICK | 1 |
| A6 | victim_interview | CBS Sacramento | YouTube | affiliate | 3:06 | "that's a lot of nerve" · PICK · LEGAL | 1 |
| A7 | authority_report | CBS News California | YouTube | network | 3:50 | "by the time you find your unclaimed funds" · PICK | 1 |
| B1 | authority_report | ABC News / GMA (Oct 27, 2026) | news_web | network | 1:31 | "we will defend this litigation vigorously" · PICK | 2 (Whisper) |
| B2 | victim_interview | More Perfect Union | TikTok | documentary | 8:41 | MANUAL · UNVERIFIED | 3 |
| B3 | victim_interview | LOCAL 12 (Oct 27, 2022) | news_web | affiliate | 2:20 | "he says it's immoral" · PICK | 2 (Whisper) |
| B4 | victim_interview | WHIO (Nov 23, 2022) | news_web | affiliate | 2:47 | "not at the register" · PICK | 2 (Whisper) |
| C1 | authority_report | GMA (Oct 20, 2026) | YouTube | network | 3:29 | "Amazon's $139 a year prime" · PICK | 2 (Whisper on the abcnews.com copy) |
| C2 | first_person_rant | @paigeanne80 | TikTok | first_person | 0:26 | MANUAL · UNVERIFIED | 3 |

## Callouts

- **No usable clip:** none. 8 PICK (16 of 16 outcues verified against a transcript), 4 MANUAL.
- **Weak / re-check:** A3, Whisper hears "Everybody gives money away" where the plan heard "Nobody" (one listen). A6, the plan's outcues didn't match its timecodes (0:52 → "website", 1:21 → the attorney intro, 2:58 → "the state says it has six months"); re-cut to verified ends. A7, narration only: the Delaware man is never named or shown. C1, timecodes from the abcnews.com copy (3:28) of the YouTube piece (3:29); allow ±1 s.
- **LEGAL:** A6. Eugene says "pure theft" and "unconstitutional stealing"; Schwab's and the state's answer (warning letters sent) runs 2:58–3:05, after the cut. Fix: end the last slice at 3:05 "he never received them".
- **Source-type monoculture:** none (affiliate 5 of 12).
- **Runner-up of a different type / diversity floor:** n/a (verify pass, no shortlists).
- **Rung 3 only:** A1, A2, B2, C2 — TikTok refuses requests from this container; the plan's in/out for them are unchecked.
- **Manual lane:** [A1](https://www.tiktok.com/@financeunfolded/video/7023899798654782726) · [A2](https://www.tiktok.com/@pearlmania500/video/7220912200855178538) · [B2](https://www.tiktok.com/@moreperfectunion/video/7350333548567596330) · [C2](https://www.tiktok.com/@paigeanne80/video/7698845156170042638)
- **Degraded:** YouTube audio blocked (irrelevant: news-site video carried Whisper); one YouTube ID bot-walled (worked around via abcnews.com); TikTok unreachable.
- **Dates found:** Barbara (FOX 13) Sept 3, 2025; Udvance (ABC7) Jan 28, 2025, not Oct 2025 as the chat outline had it; spelling confirmed "Lynda Swank" (WHIO page).
