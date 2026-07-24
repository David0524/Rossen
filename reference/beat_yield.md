# Beat yield log

Appended after every pipeline run. One row per beat. Tracks what the pipeline found, what it missed, and why.

## F2 08-05-2026 (run 2026-07-24)

| Beat | Role | Or. | Candidates | Pick | Source | Score | Status | Notes |
|------|------|-----|-----------|------|--------|-------|--------|-------|
| 08-05-b01 | explainer_demo/creator_long | H | 275 | DZ06YW82Qh8 | creator_long | 82 | OK | 2 segments, screen walkthrough |
| 08-05-b02 | evidence | V | 305 | — | — | — | EMPTY | Phantom delivery doorbell cam; TikTok content |
| 08-05-b03 | victim_interview | H | 871 | 23OPFKfjQ5I | affiliate | 84 | OK | CBC Go Public, Amazon fake graphics card, named victim |
| 08-05-b04 | authority_report | H | 317 | ttBoYQjmaVc | affiliate | 87 | OK | WHAS11/ABC FTC $2.5B settlement, FTC chair quote |
| 08-05-b05 | first_person_rant | V | 211 | mff8NrTcRw0 | creator_short | 68 | WEAK | News explainer not first-person reaction; TikTok content |
| 08-05-b06 | authority_report | H | 239 | ggDHtb-4GWQ | affiliate | 88 | OK | CPSC distributor ruling, 400K products |
| 08-05-b07 | evidence | V | 226 | — | — | — | EMPTY | Lakkzoom heater too recent (July 22); no video yet |
| 08-05-b08 | evidence | H | 306 | ytkn-av0Dd8 | affiliate | 86 | OK | WDIV grill brush, named victim Linda, magnet test |
| 08-05-b09 | evidence | V | 102 | 55hbVRTDICA | creator_short | 80 | OK | YouTube Short, exact Amazon recall text scam |
| 08-05-b10 | authority_report | H | 366 | g6n6rFw1MHk | affiliate | 82 | OK | WBAY Amazon-specific settlement scam warning |
| 08-05-b11 | explainer_demo/creator_long | H | 364 | erKRMlCUNkc | affiliate | 90 | OK | Ohio tax-free weekend, reporter at store checkout |

**Summary:** 11 beats, 8 OK, 1 weak, 2 empty. Empty beats are vertical. Vertical platform search not built.

## F2 08-05-2026 (run 2026-07-24 · fresh full-coverage session, same script)

Second independent run on the identical script. Beats re-extracted from scratch (agreed with the run above on count/roles/orientation, 11/11). The two empties above (b02, b07) plus the weak b05 were diagnosed and **case-swapped** to sourceable horizontal cases on producer approval; setup lines rewritten in the Bible.

| Beat | Role | Or. | Candidates | Pick | Source | Score | Status | Notes |
|------|------|-----|-----------|------|--------|-------|--------|-------|
| 08-05-b01 | explainer_demo/creator_long | H | 254 | _8W0-cK5XTQ | creator_long | 78 | WEAK | In the Black; general late-delivery credit demo, soft fit vs guaranteed-delivery path |
| 08-05-b02 | victim_interview | H | 178 | yEfQr9uDnH8 | affiliate | 74 | SWAP | SWAP from vertical phantom-delivery; KXAN pkg-never-arrived victim (LSO), misleading tracking |
| 08-05-b03 | victim_interview | H | 468 | IuxwwAdVGB8 | affiliate | 80 | OK | WSPA empty-box; named victim Becky Allen, 3rd-party seller no-refund; all-affiliate pool |
| 08-05-b04 | authority_report | H | 289 | zTgyswYFvsY | network | 88 | OK | ABC News; checks out now, $51, PayPal/Venmo/check; floor promoted Money Instructor (lost) |
| 08-05-b05 | authority_report | H | 154 | IOqVtw1War4 | affiliate | 79 | SWAP | SWAP from vertical payout-reaction; WUSA9 'Where's the money' checks explainer; re-roled to authority |
| 08-05-b06 | authority_report | H | 241 | o_iCvhqaWiI | network | 85 | OK | WKYC Consumer Reports; CPSC distributor ruling, 400K units, Amazon intermediary argument |
| 08-05-b07 | authority_report | H | 185 | N1D4PvPen9w | affiliate | 80 | SWAP | SWAP from Lakkzoom heater (too recent); KSNT Anker power-bank fire recall, Amazon-sold, 481K units |
| 08-05-b08 | evidence | H | 310 | j7i0NTk3Qwk | affiliate | 86 | OK | WKBN27; named victim Sally Meyer, wire bristle in throat, 'should be off the market' |
| 08-05-b09 | evidence | V | 110 | lorifullbright/7530796393783446798 | first_person | 83 | CORRECTED | Original pick (LPF9ETVTrSw, "Ryan Mack") was mislabeled vertical by a duration<=75s proxy in triage.py — verified via yt-dlp as 1920x1080 landscape, not vertical, and content was a generic screen-record voiceover. User caught it. Replaced with a genuinely vertical (1080x1920) native TikTok post: Lori Fullbright, a real crime/consumer reporter, face-to-camera on her personal account, naming the exact scam. Found via a hand-tuned site:tiktok.com query against Brave's web endpoint after the bulk harvest returned zero native TikTok candidates for this beat. |
| 08-05-b10 | authority_report | H | 341 | WZYjk1fX5hs | affiliate | 84 | OK | News19 WLTX; fake class-action settlement email, how-to-spot tells |
| 08-05-b11 | explainer_demo/creator_long | H | 445 | erKRMlCUNkc | affiliate | 84 | OK | WTOL 11; reporter rings up school-supply cart at checkout, computes savings; traditional 3-day Ohio |

**Summary:** 11 beats, all flagged (transcript-verified outcues). 6 OK, 1 weak (b01), 3 case-swapped (b02/b05/b07 were empty as vertical native-social/recency gaps → swapped to sourceable horizontal cases), 1 corrected post-delivery (b09 — see notes). Source mix: affiliate 7 · network 2 · creator_long 1 · first_person 1 (affiliate 64%). Full coverage, not degraded. b11 independently reproduced the prior run's pick (erKRMlCUNkc).

**Process bug found and fixed this run:** `triage.py`'s `orientation_of()` treated any YouTube candidate under 60s as vertical/Shorts-equivalent. That's false — orientation cannot be inferred from duration, and this run shipped a 1920x1080 landscape video against a vertical beat (b09) before it was caught. Fixed to label short-duration YouTube candidates as unverified rather than vertical, and to require an actual `yt-dlp` width/height check before any candidate is presented as satisfying a vertical hard filter. Also: the bulk `rossen_harvest search` pass surfaced only 2 native TikTok candidates across ~2,975 candidates this whole episode — thin enough that any vertical beat returning few/no native candidates should get a hand-tuned `site:tiktok.com`/`site:instagram.com` query against Brave's web endpoint as a follow-up, not a YouTube proxy pick.

## F2 08-07-2026 (run 2026-07-24)

Friday single-story format (FBI reload/imposter scam + DealSeek segment). **4 beats, not the usual 10-12** — that is the script's real shape, not an extraction miss: four `PLAY CLIP` markers, cold open and sponsor/tease blocks correctly dropped.

| Beat | Role | Or. | Candidates | Pick | Source | Score | Status | Notes |
|------|------|-----|-----------|------|--------|-------|--------|-------|
| 08-07-b01 | authority_report | H | 594 | cEMIokXkpwA | affiliate | 90 | SWAP | FOX 13 Tampa Bay. SWAP from Manatee County/Xin Liu — that case has **no video in existence** (print only). Butt-cut slice 1 of 2. Outcue "come by to pick it up" verified 65.20–70.00s |
| 08-07-b02 | confrontation_bust | H | 554 | cEMIokXkpwA | affiliate | 92 | SWAP | **Same source as b01**, honoring the script's BUTT marker. Courier arrival lands at 1:34 inside the segment. Outcue "charged with grand theft" verified 123.16–127.28s |
| 08-07-b03 | evidence | V | — | — | — | — | SHOW-PRODUCED | Screen-recording-of-a-webpage beat. Excluded from search at Checkpoint 1 on producer approval; no third-party clip can show the script's specific tells (links bounce to home, one-step form). Predicted by the sourcability scan *before* any search ran |
| 08-07-b04 | victim_interview | H | 588 | CBS NY /l-i-romance-scam-victim…468000 | network | 130 | MANUAL | Exact case match (Long Island, $468,000, re-victimized while seeking help). news_web, **no caption track → no timecode and no outcue proposed**. Reporter Tim McNicholas. Vintage unconfirmed (script flags 2024) |

**Summary:** 4 beats. 2 verified picks (one source, butt-cut), 1 manual clip without timecode, 1 show-produced. 0 empty. Source mix: affiliate 2 · network 1 · show_produced 1 — but b01/b02 share a source, so the episode draws on **two distinct clips**. Not degraded; Brave key present and live-tested (HTTP 200), all three surfaces ran.

**Sourcability scan earned its keep.** It flagged b01/b02 as `commentary_only` and b03 as `none` at Checkpoint 1, before any search. All three predictions held: the Manatee case really had no video, and b03 really had no third-party source. The one correction the scan needed was in the *optimistic* direction — it was YouTube-only, and Brave later surfaced the Manatee case in print (Bradenton Herald, Patch, Pulse of Manatee), which a page fetch of MySuncoast confirmed was text-only with no video and no mention of Xin Liu or Det. Cummings.

**Diversity floor fired twice and lost twice.** b01 promoted GeekSpin (82) over News4JAX (90); b04 promoted Duluth PD (84) over NBC10 Philadelphia (86). Both lost pass two — GeekSpin has no back catalog and reads as a narrated press-release readout, Duluth PD is a recovery-*success* story, the inverse of the beat. Two floor promotions losing pass two in a 3-beat searched run is the pattern the grader skill says to watch: if it repeats, the upstream hard filters need a look rather than the floor.

**Process bug found and fixed this run (recall, not correctness):** vertical beats never reached the YouTube backend at all — `__main__.py` gated the call on `orientation != "vertical"`, so a vertical beat's `shorts` register ran **nowhere**, despite the query-generator skill stating Shorts run on every orientation. Shorts are the only vertical surface with a reachable search index in a TikTok-blocked environment, and they were closed on exactly the beats that needed them. Fixed with a `ShortsBackend` search surface on both orientations; the 60s ceiling is applied in Python rather than via `--match-filter` because `--flat-playlist` returns null durations and a null silently *passes* a match filter. Contributed 56 candidates. Note this run could not exercise it against a vertical beat, since the only vertical beat (b03) went show-produced — worth re-checking on the next script with a live vertical beat.

**Whisper was not run, and the reason generalizes.** The ask was to lean on it for Shorts/TikTok/Reels. It consumes bytes something else must fetch first, and in this environment YouTube media (audio *and* video, confirmed with `-f bestaudio`) and TikTok are both blocked — so it had zero reachable sources. The skill now documents a transcript ladder in cost order (captions, which cover Shorts too and are free → Whisper → flag unverified) and states that Whisper's reach is bounded by media access rather than being a way around a block.

**Rate-limiting was misdiagnosed as a hard block mid-run, and this is the lesson worth keeping.** At Checkpoint 1 captions measured 0/6 on video IDs the 08-05 run had captioned successfully, and I reported them hard-blocked. Twenty minutes later the normal `fetch_many` path returned **11/12**. The 0/6 was self-inflicted: a dozen `--list-subs` probes in two minutes, several looping over player clients, tripped a rate limiter that returns the same "not a bot" string a real block does. Probe once per path, never loop player clients as a first move, and retry through the real code path after a wait before concluding. Calling a throttle a block costs a whole run — it converts every pick to an unverified outcue.
