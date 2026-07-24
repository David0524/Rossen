# F2 Top Stories — Wednesday, August 5 — clip pipeline report

Run date 2026-07-24. Full-coverage run (BRAVE_API_KEY set — not degraded). 11 beats, all 11 flagged with transcript-verified verbatim outcues. Three beats (b02, b05, b07) were empty at grading and were case-swapped to sourceable cases on approval; their script setup lines are rewritten in the Bible. b09's original pick was corrected post-delivery (see Correction below) after user review caught it was not actually vertical.

**Source mix, 11 beats:**  affiliate 7 · network 2 · creator_long 1 · first_person 1

| Beat | Role | Chosen clip | Platform | Source | Dur | Outcue(s) |
|---|---|---|---|---|---|---|
| b01 | creator_long | In the Black | youtube | creator_long | 4:31 | 1:02–1:41 "worth a shot though" ; 2:34–3:53 "10 credit easy" |
| b02 *(swap)* | victim_interview | KXAN | youtube | affiliate | 3:02 | 0:43–1:15 "still hasn't received it" |
| b03 | victim_interview | WSPA 7News | youtube | affiliate | 2:21 | 0:34–0:55 "reimburse us" |
| b04 | authority_report | ABC News | youtube | network | 1:39 | 0:16–1:00 "get a check in the mail" |
| b05 *(swap)* | authority_report | WUSA9 | youtube | affiliate | 1:16 | 0:03–0:30 "capped at $51" |
| b06 | authority_report | WKYC Channel 3 | youtube | network | 3:52 | 1:01–1:41 "injury or death" ; 1:57–2:22 "products out of homes" |
| b07 *(swap)* | authority_report | KSNT News | youtube | affiliate | 0:42 | 0:01–0:37 "full refund or gift card" |
| b08 | evidence | WKBN27 | youtube | affiliate | 0:46 | 0:01–0:37 "off the market" |
| b09 | evidence | Lori Fullbright | tiktok | first_person | 2:28 | 0:00–0:35 "these are criminals" |
| b10 | authority_report | News 19 WLTX | youtube | affiliate | 2:11 | 0:04–1:37 "just a few dollars" |
| b11 | creator_long | WTOL 11 | youtube | affiliate | 2:07 | 0:23–1:37 "cents on the dollar" |

## Correction (post-delivery, user-caught)

**b09's original pick was wrong on two axes, and the user caught both.** The first delivered version of this report flagged a YouTube video ("Amazon Refund Text SCAM" by Ryan Mack) as the vertical evidence pick for b09. It was neither:

1. **Not actually vertical.** Verified via `yt-dlp --print "%(width)sx%(height)s"`: **1920x1080, 16:9 landscape.** It had been classified vertical purely because it was under 75 seconds long — a duration-as-orientation proxy in `triage.py` that is simply false (plenty of ordinary horizontal YouTube uploads run under a minute). This slipped past the pipeline's own stated hard rule that orientation is a hard filter, not a hint.
2. **Low-quality as content even set orientation aside.** A narrated "here's what happens when you tap the link" explainer over presumably a screen recording — generic tips content, not the raw/authentic material Jeff's segments want.

**Root cause:** the automated harvest pass (`rossen_harvest search`) returned **zero native TikTok candidates for b09** across the whole run (in fact only 2 native TikTok candidates surfaced across all 2,975 candidates in the entire episode — confirming the skill doc's warning that Brave's video endpoint is YouTube-heavy and rarely surfaces native TikTok/IG permalinks). Rather than diagnosing that as a discovery gap and escalating, the grading pass quietly accepted a horizontal YouTube video as a stand-in.

**Fix applied:**
- Ran a hand-tuned `site:tiktok.com` query directly against Brave's **web** endpoint (not the video endpoint the bulk pass uses) — this surfaced real `/video/` permalinks the bulk pipeline missed.
- Verified the winning candidate's actual pixel dimensions before trusting it (1080x1920 — genuinely vertical).
- Whisper-transcribed it via `vertical_transcribe.py` and verified the outcue verbatim, same as every other pick.
- **New b09 pick:** Lori Fullbright (a real on-air crime/consumer reporter) posting a direct face-to-camera safety-tip video on her personal TikTok, naming the exact fake-Amazon-recall-text scam. `first_person` source type, vertical, unproduced — the kind of raw, homemade delivery the show wants, not a screen-record-and-voiceover.
- **`triage.py` patched**: the function that mislabeled short-duration YouTube videos as vertical/Shorts now returns an explicit `youtube_short_duration_UNVERIFIED` label instead of asserting orientation, with a comment requiring a real `yt-dlp` dimension check before any short-duration YouTube candidate can be presented as satisfying a vertical beat.

This was a real gap in how this run approached vertical sourcing broadly, not just a one-beat error — the bulk pipeline's TikTok/IG discovery is thin (2 native candidates in ~3,000), and the fix that worked here (targeted `site:` web-endpoint queries, not the generic bulk video-search pass) should be the default escalation whenever a vertical beat comes back with zero-to-few native social candidates, rather than falling back to a YouTube proxy.

## Call-outs (per Step 8)

**No beat is empty.** All 11 carry a verified pick. Three began empty and were case-swapped (below); one (b09) was corrected post-delivery (see Correction above).

**Weak pick a human should re-check:**
- **b01 (score 78)** — "In the Black" is the general *late-delivery credit* ask (get a $10 credit / Prime extension via chat), not Jeff's exact *guaranteed-delivery shipping-fee* path (Your Orders → Problem with an order → Shipment is late). Same family, softer fit. If a tighter demo of the specific guaranteed-delivery-fee refund exists, swap it; otherwise this is show-produced territory (Jeff walks the screens himself).

**Case-swaps applied (were empty at grading, all three vertical → now horizontal):**
- **b02** phantom "delivered" doorbell evidence → **KXAN** package-never-arrived investigation (named victims, "misleading tracking"). Not Amazon's own scan; it's a shipping-company story. Setup rewritten.
- **b05** first-person "payouts under a dollar" reaction → **WUSA9** "Where's the money" authority piece on the checks (capped at $51, is-it-a-scam). Re-roled first_person → authority. Setup rewritten.
- **b07** Lakkzoom immersion-heater fire evidence → **KSNT** Anker power-bank fire recall (Amazon-sold, 33 fires/explosions, 481K units). Product changed; the 98K-units / 235-fires / July-22 specifics are rewritten out.

Why they were empty (diagnosed, not query failures): b02 & b05 are native-social gaps — the reaction/doorbell content lives on TikTok/IG, which Brave's video endpoint does not reliably surface; b07 was a recency gap — Lakkzoom was recalled ~2 weeks pre-air with no citizen or news video yet.

**Source-type concentration:** affiliate holds **7 of 11 (64%)** — just under the 70% flag line. Non-affiliate/network variety: b01 (creator_long), b09 (first_person, TikTok).
- **b04** (network ABC) — runner-up was Money Instructor (**creator_long**), the diversity-floor promotion.

**Diversity floor:**
- **b04** — floor fired (all-network survivors), promoted Money Instructor (creator_long); it then lost pass two to the ABC network package. Expected "floor promoted filler" pattern — worth watching if it repeats across episodes.
- **b03** — floor could not fire: the entire survivor pool was affiliate, no non-affiliate cleared the hard filters, so it shipped affiliate-only (floor promotes, never invents).

**Clips that failed to download:** none were attempted — there is **no automated download-and-cut stage** in this codebase. Picks were located, verified against transcript, and logged with exact timecodes for a human to pull. Separately: 6 of 37 shortlisted YouTube captions came back null (terminated channel / geo-blocked / captions off) and were demoted; the b02-shortlist TikTok candidate transcribed to music only ("Thanks for watching") and was dropped. YouTube *video-byte* downloads 403 in this environment (metadata/captions work) — not exercised here because the pipeline does not pull video.

**Degraded?** No. BRAVE_API_KEY was present; YouTube + Brave both ran.

## Method notes
- Beats extracted independently and cross-checked against a prior committed run on the same script — full agreement on count (11), roles, and orientation.
- Orientation enforced as a hard filter in triage. **This failed once** — see Correction above — and has been patched.
- Every outcue was located in the cue-level transcript with the grader's own `find()` normalization; the out-timecode is read off the matched cue, never computed by hand. See `build_picks.py`.
- Native TikTok/IG discovery via the bulk `rossen_harvest search` pass is thin (2 native candidates surfaced across ~3,000 this run). When a vertical beat comes back with few or no native candidates, the effective fix is a hand-tuned `site:tiktok.com` / `site:instagram.com` query against Brave's **web** endpoint (not the bulk pass's video endpoint), followed by a real `yt-dlp` dimension check on any hit before it's trusted as vertical.
