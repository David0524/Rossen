# Beat yield log

Appended every pipeline run, every beat — not just failures. The point is to
learn which roles/orientations reliably yield an airable clip and which are
structural dead ends, so the bible can be written toward what sources exist.

Columns: run · beat · role · orientation · outcome · why / source
Outcomes: PICK (verified outcue) · LOCATED (case found, no caption-able source)
· SWAP (needs script change) · EMPTY (nothing cleared the bar)
· UNVERIFIED (right footage identified and agreed, but no transcript was
reachable in the run environment, so the outcue is carried forward unconfirmed
— distinct from LOCATED, where the source itself has no caption track, and from
PICK, which asserts a verified outcue)

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

## Run FRIDAY_08072026 (Amazon owes you money — refunds / A-to-Z / $309.5M settlement)

Scope: **clip 1 only**, by request. Beats 2-5 extracted but not searched.

| Beat | Role | Or. | Outcome | Why / source |
|---|---|---|---|---|
| 08-07-b01 | explainer_demo/creator_long | H | UNVERIFIED | In the Black `_8W0-cK5XTQ` 1:02-1:41 "worth a shot though" — right footage, confirmed independently at rank 1 by 11 of 14 queries; outcue carried from producer draft because captions AND media bytes were both bot-walled all run |

**Yield:** 1 UNVERIFIED of 1 searched.

**Environment block, and why it matters more than the yield.** YouTube's three
paths fail independently and this run hit the worst combination: flat-playlist
**search worked fine** (322 raw candidates), while the **per-video page and media
bytes were both bot-walled**. That kills rung 1 and rung 2 of the transcript
ladder simultaneously — no captions, and Whisper has nothing to transcribe —
leaving rung 3 as the only available outcome for every YouTube candidate in the
run. Confirmed as a block rather than a throttle per the preflight protocol:
probed once, then re-confirmed several minutes later through the ordinary
`fetch_many` path at normal pace, 0 of 5. Not a burst artifact.

**The useful positive finding: search-side cross-validation substitutes for
sourcability when transcripts are dead.** The script arrived with clip 1 already
filled in by the producer. The generated queries surfaced that exact video at
**rank 1**, hit by 11 of 14 query strings spanning all five registers. That
convergence is independent evidence the footage is right even with zero
transcript access — worth reaching for whenever the caption path is down, in
place of asserting a verified outcue.

**Register note (n=1, do not over-read).** The `anchor` register found the
target first here — consistent with the weighting table's `anchor` lead for
`explainer_demo/creator_long`. `victim` also technically surfaced it, which is
the first time `victim` has contributed on a horizontal/YouTube beat; the prior
eval had it at 0 for 8. One data point, and the video was found by nearly every
register, so this is not evidence `victim` earns its budget.
