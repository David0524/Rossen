# Beat yield log

Appended every pipeline run, every beat — not just failures. The point is to
learn which roles/orientations reliably yield an airable clip and which are
structural dead ends, so the bible can be written toward what sources exist.

**This file is the single canonical log.** It lives here, beside
`aired_examples.md`, so it travels with the skill when the skill is deployed.
There was briefly a second copy at the repo root (`reference/beat_yield.md`)
and runs appended to that one while this one sat frozen — see "Log split"
at the bottom. Append here and nowhere else.

## Schema

`| Beat | Role | Or. | Cands | Outcome | Pick | Source | Why / notes |`

| Outcome | Meaning |
|---|---|
| `PICK` | Flagged, with an outcue verified verbatim against a transcript |
| `WEAK` | Flagged, but soft fit — a human should re-check before air |
| `MANUAL` | Exact case found, but only off captioned YouTube (news_web/affiliate site). No timecode, no outcue. Logged as `LOCATED` before 08-07 |
| `SWAP` | Original case was unsourceable; script changed on producer approval |
| `SHOW-PRODUCED` | Removed from the clip pipeline and assigned to production |
| `EMPTY` | Nothing cleared the bar. An honest gap |
| `CORRECTED` | Changed after delivery — record what was wrong and how it was caught |

---

## Run F2_07292026 (AI voice-clone / agency impersonation / back-to-school)

Candidate counts were not recorded this run.

| Beat | Role | Or. | Cands | Outcome | Pick | Source | Why / notes |
|---|---|---|---|---|---|---|---|
| F2b-b01 | victim_interview | H | — | MANUAL | Del Mastro $5,400 | news_web | ABC7 SF; no captioned YT twin |
| F2b-b02 | explainer_demo | H | — | SWAP | gMXuQ4MusPk | affiliate | FOX4 Dallas 2:00-2:12 "it's my voice artificially generated" (Greg Bull/Noviello; script rewritten off Dickherber) |
| F2b-b03 | victim_interview | H | — | SWAP | sPIIFyPyKKE | affiliate | KATU 1:37-2:30 "It's your child" (Tina/Hillsboro $2,500; reframed from raw-audio to recount) |
| F2b-b04 | authority_report | H | — | MANUAL | Olathe PD kids-voice | news_web | KMBC/KCTV; no captioned YT twin |
| F2b-b05 | victim_interview | H | — | MANUAL | Schildhorn | news_web | FOX29/CNN; YouTube only AI-slop reposts |
| F2b-b06 | victim_interview | H | — | PICK | As4nS5aOVnw | affiliate | WFLA 0:38-1:02 "so she gave it to them" (Brightwell $15K, exact) |
| F2b-b07 | authority_report | H | — | EMPTY | — | — | IC3 alert I-072026-PSA (5 days old); only generic FBI-scam packages |
| F2b-b08 | evidence | V | — | EMPTY | — | — | No fake-IC3-site/deepfake-official screen recording |
| F2b-b09 | authority_report | H | — | PICK | rkZMNuoNfqA | affiliate | WPRI 1:25-1:48 "deposit money into a Bitcoin ATM" (fit: not agent/badge angle) |
| F2b-b10 | authority_report | H | — | PICK | JUbuCpPGX3g | affiliate | WCNC 0:27-0:55 "the S standing for secure" (fit: not IRS-CI specific) |
| F2b-b11 | evidence | V | — | EMPTY | — | — | No nurse/coach/tuition scam-text screen recording |
| F2b-b12 | explainer_demo | H | — | EMPTY | — | — | No Target Circle barcode-scan demo (KPRC hit = boarding-pass barcodes) |

**Yield:** 5 PICK (incl. 2 approved swaps) / 3 MANUAL / 4 EMPTY of 12.
**Pattern:** vertical `evidence` 0/2 (both empty) — worst category, again. Named
victims frequently source only to news_web (no captions) — MANUAL, not PICK.
`authority_report` on <2-week-old federal alerts (b07) too new for captioned video.
Brave news_web leg was decisive: b02/b01/b04/b05/b06 exact cases surfaced only there.

---

## F2 08-05-2026 (run 2026-07-24)

| Beat | Role | Or. | Cands | Outcome | Pick | Source | Why / notes |
|---|---|---|---|---|---|---|---|
| 08-05-b01 | explainer_demo/creator_long | H | 275 | PICK | DZ06YW82Qh8 | creator_long | 2 segments, screen walkthrough (score 82) |
| 08-05-b02 | evidence | V | 305 | EMPTY | — | — | Phantom delivery doorbell cam; TikTok content |
| 08-05-b03 | victim_interview | H | 871 | PICK | 23OPFKfjQ5I | affiliate | CBC Go Public, Amazon fake graphics card, named victim (84) |
| 08-05-b04 | authority_report | H | 317 | PICK | ttBoYQjmaVc | affiliate | WHAS11/ABC FTC $2.5B settlement, FTC chair quote (87) |
| 08-05-b05 | first_person_rant | V | 211 | WEAK | mff8NrTcRw0 | creator_short | News explainer not first-person reaction; TikTok content (68) |
| 08-05-b06 | authority_report | H | 239 | PICK | ggDHtb-4GWQ | affiliate | CPSC distributor ruling, 400K products (88) |
| 08-05-b07 | evidence | V | 226 | EMPTY | — | — | Lakkzoom heater too recent (July 22); no video yet |
| 08-05-b08 | evidence | H | 306 | PICK | ytkn-av0Dd8 | affiliate | WDIV grill brush, named victim Linda, magnet test (86) |
| 08-05-b09 | evidence | V | 102 | PICK | 55hbVRTDICA | creator_short | YouTube Short, exact Amazon recall text scam (80) |
| 08-05-b10 | authority_report | H | 366 | PICK | g6n6rFw1MHk | affiliate | WBAY Amazon-specific settlement scam warning (82) |
| 08-05-b11 | explainer_demo/creator_long | H | 364 | PICK | erKRMlCUNkc | affiliate | Ohio tax-free weekend, reporter at store checkout (90) |

**Summary:** 11 beats, 8 PICK, 1 WEAK, 2 EMPTY. Both empties are vertical.
Vertical platform search not built at this point.

---

## F2 08-05-2026 (run 2026-07-24 · fresh full-coverage session, same script)

Second independent run on the identical script. Beats re-extracted from scratch
(agreed with the run above on count/roles/orientation, 11/11). The two empties
above (b02, b07) plus the weak b05 were diagnosed and **case-swapped** to
sourceable horizontal cases on producer approval; setup lines rewritten in the
Bible.

| Beat | Role | Or. | Cands | Outcome | Pick | Source | Why / notes |
|---|---|---|---|---|---|---|---|
| 08-05-b01 | explainer_demo/creator_long | H | 254 | WEAK | _8W0-cK5XTQ | creator_long | In the Black; general late-delivery credit demo, soft fit vs guaranteed-delivery path (78) |
| 08-05-b02 | victim_interview | H | 178 | SWAP | yEfQr9uDnH8 | affiliate | SWAP from vertical phantom-delivery; KXAN pkg-never-arrived victim (LSO), misleading tracking (74) |
| 08-05-b03 | victim_interview | H | 468 | PICK | IuxwwAdVGB8 | affiliate | WSPA empty-box; named victim Becky Allen, 3rd-party seller no-refund; all-affiliate pool (80) |
| 08-05-b04 | authority_report | H | 289 | PICK | zTgyswYFvsY | network | ABC News; checks out now, $51, PayPal/Venmo/check; floor promoted Money Instructor (lost) (88) |
| 08-05-b05 | authority_report | H | 154 | SWAP | IOqVtw1War4 | affiliate | SWAP from vertical payout-reaction; WUSA9 'Where's the money' checks explainer; re-roled to authority (79) |
| 08-05-b06 | authority_report | H | 241 | PICK | o_iCvhqaWiI | network | WKYC Consumer Reports; CPSC distributor ruling, 400K units, Amazon intermediary argument (85) |
| 08-05-b07 | authority_report | H | 185 | SWAP | N1D4PvPen9w | affiliate | SWAP from Lakkzoom heater (too recent); KSNT Anker power-bank fire recall, Amazon-sold, 481K units (80) |
| 08-05-b08 | evidence | H | 310 | PICK | j7i0NTk3Qwk | affiliate | WKBN27; named victim Sally Meyer, wire bristle in throat, 'should be off the market' (86) |
| 08-05-b09 | evidence | V | 110 | CORRECTED | lorifullbright/7530796393783446798 | first_person | Original pick (LPF9ETVTrSw, "Ryan Mack") was mislabeled vertical by a duration<=75s proxy in triage.py — verified via yt-dlp as 1920x1080 landscape, not vertical, and content was a generic screen-record voiceover. User caught it. Replaced with a genuinely vertical (1080x1920) native TikTok post: Lori Fullbright, a real crime/consumer reporter, face-to-camera on her personal account, naming the exact scam. Found via a hand-tuned site:tiktok.com query against Brave's web endpoint after the bulk harvest returned zero native TikTok candidates for this beat. (83) |
| 08-05-b10 | authority_report | H | 341 | PICK | WZYjk1fX5hs | affiliate | News19 WLTX; fake class-action settlement email, how-to-spot tells (84) |
| 08-05-b11 | explainer_demo/creator_long | H | 445 | PICK | erKRMlCUNkc | affiliate | WTOL 11; reporter rings up school-supply cart at checkout, computes savings; traditional 3-day Ohio (84) |

**Summary:** 11 beats, all flagged (transcript-verified outcues). 6 PICK, 1 WEAK
(b01), 3 SWAP (b02/b05/b07 were empty as vertical native-social/recency gaps →
swapped to sourceable horizontal cases), 1 CORRECTED post-delivery (b09 — see
notes). Source mix: affiliate 7 · network 2 · creator_long 1 · first_person 1
(affiliate 64%). Full coverage, not degraded. b11 independently reproduced the
prior run's pick (erKRMlCUNkc).

**Process bug found and fixed this run:** `triage.py`'s `orientation_of()`
treated any YouTube candidate under 60s as vertical/Shorts-equivalent. That's
false — orientation cannot be inferred from duration, and this run shipped a
1920x1080 landscape video against a vertical beat (b09) before it was caught.
Fixed to label short-duration YouTube candidates as unverified rather than
vertical, and to require an actual `yt-dlp` width/height check before any
candidate is presented as satisfying a vertical hard filter. Also: the bulk
`rossen_harvest search` pass surfaced only 2 native TikTok candidates across
~2,975 candidates this whole episode — thin enough that any vertical beat
returning few/no native candidates should get a hand-tuned
`site:tiktok.com`/`site:instagram.com` query against Brave's web endpoint as a
follow-up, not a YouTube proxy pick.

---

## F2 08-07-2026 (run 2026-07-24)

Friday single-story format (FBI reload/imposter scam + DealSeek segment).
**4 beats, not the usual 10-12** — that is the script's real shape, not an
extraction miss: four `PLAY CLIP` markers, cold open and sponsor/tease blocks
correctly dropped.

| Beat | Role | Or. | Cands | Outcome | Pick | Source | Why / notes |
|---|---|---|---|---|---|---|---|
| 08-07-b01 | authority_report | H | 594 | SWAP | cEMIokXkpwA | affiliate | FOX 13 Tampa Bay. SWAP from Manatee County/Xin Liu — that case has **no video in existence** (print only). Butt-cut slice 1 of 2. Outcue "come by to pick it up" verified 65.20–70.00s (90) |
| 08-07-b02 | confrontation_bust | H | 554 | SWAP | cEMIokXkpwA | affiliate | **Same source as b01**, honoring the script's BUTT marker. Courier arrival lands at 1:34 inside the segment. Outcue "charged with grand theft" verified 123.16–127.28s (92) |
| 08-07-b03 | evidence | V | — | SHOW-PRODUCED | — | — | Screen-recording-of-a-webpage beat. Excluded from search at Checkpoint 1 on producer approval; no third-party clip can show the script's specific tells (links bounce to home, one-step form). Predicted by the sourcability scan *before* any search ran |
| 08-07-b04 | victim_interview | H | 588 | MANUAL | CBS NY /l-i-romance-scam-victim…468000 | network | Exact case match (Long Island, $468,000, re-victimized while seeking help). news_web, **no caption track → no timecode and no outcue proposed**. Reporter Tim McNicholas. Vintage unconfirmed (script flags 2024) (130) |

**Summary:** 4 beats. 2 PICK-grade verified picks (one source, butt-cut), 1
MANUAL without timecode, 1 SHOW-PRODUCED. 0 EMPTY. Source mix: affiliate 2 ·
network 1 · show_produced 1 — but b01/b02 share a source, so the episode draws
on **two distinct clips**. Not degraded; Brave key present and live-tested
(HTTP 200), all three surfaces ran.

**Sourcability scan earned its keep.** It flagged b01/b02 as `commentary_only`
and b03 as `none` at Checkpoint 1, before any search. All three predictions
held: the Manatee case really had no video, and b03 really had no third-party
source. The one correction the scan needed was in the *optimistic* direction —
it was YouTube-only, and Brave later surfaced the Manatee case in print
(Bradenton Herald, Patch, Pulse of Manatee), which a page fetch of MySuncoast
confirmed was text-only with no video and no mention of Xin Liu or Det. Cummings.

**Diversity floor fired twice and lost twice.** b01 promoted GeekSpin (82) over
News4JAX (90); b04 promoted Duluth PD (84) over NBC10 Philadelphia (86). Both
lost pass two — GeekSpin has no back catalog and reads as a narrated
press-release readout, Duluth PD is a recovery-*success* story, the inverse of
the beat. Two floor promotions losing pass two in a 3-beat searched run is the
pattern the grader skill says to watch: if it repeats, the upstream hard filters
need a look rather than the floor.

**Process bug found and fixed this run (recall, not correctness):** vertical
beats never reached the YouTube backend at all — `__main__.py` gated the call on
`orientation != "vertical"`, so a vertical beat's `shorts` register ran
**nowhere**, despite the query-generator skill stating Shorts run on every
orientation. Shorts are the only vertical surface with a reachable search index
in a TikTok-blocked environment, and they were closed on exactly the beats that
needed them. Fixed with a `ShortsBackend` search surface on both orientations;
the 60s ceiling is applied in Python rather than via `--match-filter` because
`--flat-playlist` returns null durations and a null silently *passes* a match
filter. Contributed 56 candidates. Note this run could not exercise it against a
vertical beat, since the only vertical beat (b03) went show-produced — worth
re-checking on the next script with a live vertical beat.

**Whisper was not run, and the reason generalizes.** The ask was to lean on it
for Shorts/TikTok/Reels. It consumes bytes something else must fetch first, and
in this environment YouTube media (audio *and* video, confirmed with
`-f bestaudio`) and TikTok are both blocked — so it had zero reachable sources.
The skill now documents a transcript ladder in cost order (captions, which cover
Shorts too and are free → Whisper → flag unverified) and states that Whisper's
reach is bounded by media access rather than being a way around a block.

**Rate-limiting was misdiagnosed as a hard block mid-run, and this is the lesson
worth keeping.** At Checkpoint 1 captions measured 0/6 on video IDs the 08-05 run
had captioned successfully, and I reported them hard-blocked. Twenty minutes
later the normal `fetch_many` path returned **11/12**. The 0/6 was self-inflicted:
a dozen `--list-subs` probes in two minutes, several looping over player clients,
tripped a rate limiter that returns the same "not a bot" string a real block
does. Probe once per path, never loop player clients as a first move, and retry
through the real code path after a wait before concluding. Calling a throttle a
block costs a whole run — it converts every pick to an unverified outcue.

---

## Log split (2026-07-24, resolved)

For a stretch this log existed in two places with **divergent schemas and zero
episode overlap**: this file held only F2_07292026, while a second copy at the
repo root `reference/beat_yield.md` accumulated 08-05 (×2) and 08-07. Runs
appended to the root copy while the one that ships with the skill sat frozen.

Root cause: no skill documented the logging step or its path. "Append every beat
to `reference/beat_yield.md`" was a per-run instruction with an ambiguous
relative path, and it resolved differently depending on where the run happened
to be working. The two schemas then drifted independently — this file used
`Outcome` (PICK/LOCATED/SWAP/EMPTY), the root copy used `Status`
(OK/WEAK/EMPTY/SWAP/CORRECTED) plus `Candidates`/`Score` columns.

Fixed by merging both into this file under the unified schema above (nothing
dropped; `LOCATED` normalized to `MANUAL`, `OK` to `PICK`), leaving a pointer
stub at the old root path, and documenting the log explicitly in
`rossen-pipeline` Step 8 with this exact path.
