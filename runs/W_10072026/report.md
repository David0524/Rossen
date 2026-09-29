# Pipeline report — W 10/07/2026 (Wednesday)

Outline: `outline.md` → `10_07_OUTLINE_WED.docx` (Stage: videos). Picks: `picks.json` (contract clean). Manifest: `clips/manifest.json`.
Nothing in this pipeline watched a video. Every timecode below comes from a caption transcript; no clip was downloaded or cut.

**Source mix, 11 clip beats:** affiliate 3 · network 3 · first_person 2 (manual TikToks) · creator_short 1 · creator_long 1 · (A5 throttled, no pick graded)

| Beat | Role | Clip | Platform | Source type | Segment(s) · outcue | Status | Rung |
|---|---|---|---|---|---|---|---|
| A2 | victim_interview | ABC News 4 / WCYB EcWQI5Zrj4Q | youtube | affiliate | 0:16–0:31 "a state she'd never even visited" | WEAK | 1 |
| A3 | authority_report | ABC News 4 / WCYB EcWQI5Zrj4Q | youtube | affiliate | 0:31–0:46 "an arrest warrant to be issued for her" · 0:46–1:00 "between April and May of 2025" | PICK | 1 |
| A4 | victim_interview | CBS News 6gUOZ7tYfZ8 | youtube | network | 1:16–1:46 "the same clothes she was booked in in July" | PICK | 1 |
| A5 | authority_report | KVRR SGFrtUVY6nc | youtube | affiliate | — | THROTTLED | 3 |
| A6 | authority_report | CBS News 6gUOZ7tYfZ8 | youtube | network | 0:00–0:19 "for false arrest" · 0:42–0:57 "what she believes was malicious prosecution" | PICK | 1 |
| B1 | explainer_demo/creator_short | Instacart IO1wx3zBR6s | youtube | creator_short | 0:00–0:43 "them and even add them back" · 0:48–1:08 "your customer's" | PICK · CROP (reused) | 1 |
| B2 | first_person_rant | @user60342208753 TikTok | tiktok | first_person | — | MANUAL · UNVERIFIED | 3 |
| B3 | authority_report | NBC Connecticut jTKvp41lHZc | youtube | affiliate | 0:17–0:51 "now using them to prevent theft. It's an" · 1:22–1:37 "accountability, data retention." | PICK (reused) | 1 |
| C1 | evidence | @typical_redhead_ / @kristinealise TikToks | tiktok | first_person | — | MANUAL · UNVERIFIED (two options, call later) | 3 |
| C2 | authority_report | NBC News lsqR0oxtvOw | youtube | network | 1:11–1:16 "hospitality is fundamentally human" · 1:24–1:44 "AI, please remove that item" | WEAK | 1 |
| C3 | authority_report | Ecomix Simple sXSImjg6CMU | youtube | creator_long | 0:16–0:29 "Not on the app. On hospitality." | WEAK | 1 |

## Callouts
- **No usable clip (`flagged: null`):** none. A5 has a link but no transcript (THROTTLED).
- **Weak picks, re-check by a human:** A2 (reporter VO, no Lipps soundbite), C2 (Feb Burger King AI-headset story, not the Sept 23 drive-offs), C3 (47-view channel, possible synthetic voice).
- **Source-type monoculture:** none at ≥70%. Story A is 100% affiliate/network by design (no non-news source cleared the filters; diversity floor found nothing to promote on A2–A4). Cheap swaps where the runner-up was a different type: A6 runner-up is the attorney's radio interview (creator_long, IAiYyMtiLpY); C1 runner-up is Sambucha's horizontal test (creator_long, j1i-84ICREA, 15:16–15:22 Wendy's AI "I am not a human").
- **Diversity floor promotions that lost pass two:** A6 (Midwest Communications radio interview) and C2 (Burger King AI drive-thru raw footage OCNwXK-L5ic — captions null, not graded).
- **Rung 3 only:** A5 (bot wall, two spaced attempts), B2 and C1 (native TikTok; no captions; media blocked so no Whisper).
- **Manual lane:** B2 https://www.tiktok.com/@user60342208753/video/7679448051202657566 · C1 https://www.tiktok.com/@typical_redhead_/video/7192248491853303086 and https://www.tiktok.com/@kristinealise/video/7522285144254795038
- **Degraded:** media bytes blocked the whole run (Whisper off). YouTube caption path bot-walled mid-run: 12 of 26 IDs captioned after one spaced retry; 14 still null (throttle, not a confirmed block). Brave key worked.
- **Prior-run reuse:** B1 and B3 carried from LIVE_10072026 (via rossen-story-outline/references/example_1007_videos.md) and re-verified against captions this run. No re-search.

## Air risks
- 🚨 CBS says "Angela Lipscomb" on air at 0:32 and 1:08. Picked segments avoid both.
- Jail time: CBS "nearly 6 months"; ABC News 4 "two months" in North Dakota jail (custody end of October, released end of December). Say "months."
- Which image was searched: attorney says AI examined surveillance video; outline row says fake-ID photo. Settle from the complaint.

## To finish in a fresh session
1. Re-run captions for A5 (SGFrtUVY6nc, jgRCzv-_GJM) and the A2 alternates (nwRB9NTx6IU, hoxhMfWyC8g) — a Lipps-on-camera soundbite would lift A2 from WEAK.
2. C1: make the call between the two TikToks.
3. C2/C3: graphic fallback unless a drive-offs or retraining package appears.
