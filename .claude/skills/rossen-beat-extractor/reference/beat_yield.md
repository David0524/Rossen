# Beat yield log

Appended every pipeline run, every beat — not just failures. The point is to
learn which roles/orientations reliably yield an airable clip and which are
structural dead ends, so the bible can be written toward what sources exist.

Columns: run · beat · role · orientation · outcome · why / source
Outcomes: PICK (verified outcue) · LOCATED (case found, no caption-able source)
· SWAP (needs script change) · EMPTY (nothing cleared the bar)

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

## Run SMOKE_VERTICAL 2026-07-25 — ⚠️ SMOKE TEST, NOT AN EPISODE

**DO NOT COUNT IN ANY YIELD TALLY.** Single synthetic fixture beat exercising the
vertical path (gift-card rack scam). No air intent. Excluded from episode stats
because n=1, hand-probed, and the beat was written to be sourceable.

| Beat | Role | Or. | Outcome | Why / source |
|---|---|---|---|---|
| smoke-vertical-b01 | explainer_demo/creator_short | V | PICK ×3 (one per platform, as specified) | shorts: CTV News ZVQPxS16At0 (1080x1920, auto-captions) · tiktok: @cbsmornings 7451654556297055518 (1080x1920 ffprobe on decoded stream, Whisper-verified) · instagram: HuffPost DSk4bzkklJh (720x1280 decoded) |

**Per-platform yield (pipeline harvest leg, `python -m rossen_harvest search`):**
315 raw → 244 after dedupe. news_web 117 · youtube 107 · reddit 20 ·
**tiktok 0 · instagram 0**. The documented native-social gap reproduced exactly:
every tiktok.com URL Brave returned was a `/discover/` browse page, correctly
demoted to news_web by the `/video/` path detector in `brave.py`. Zero Instagram
of any kind from the pipeline leg.

Both social picks came from **hand-run targeted Brave probes outside the pipeline**
(`site:instagram.com/reel …`, `tiktok.com/video …`), not from the harvest command.
That is the honest read: the pipeline's native-social yield for this beat was 0/244,
consistent with the 8/7,549 (~0.11%) baseline. Do not read "3 platforms, 3 picks"
as the pipeline clearing the bar — it did not.

**Orientation bug (vertical postmortem) — reproduced live, four ways:**
- `PNjdcz3eG9o` 25s but **1280x720 landscape**; `oI05QvICQo8` 21s but **1280x720**.
  Duration-only inference ships landscape against a vertical beat. Exactly the bug.
- `DSqkiUoD5eW` **640x360 landscape at 58s on an Instagram /reel/ URL** — defeats
  duration inference AND platform-name inference simultaneously.
- `_RTe-ddhxoY` **540x960 vertical but NOT a Short** (/shorts/ 303→/watch).
  Inverse error: right orientation, wrong format bucket.
- Every sub-60s YouTube result across 9 Shorts-dialect queries was landscape.

**Method note:** `oardefault.jpg` / `oar2.jpg` (original-aspect-ratio thumbnail,
ffprobed) is a cheap, reliable vertical discriminator when media bytes are blocked
— landscape videos have no `oar` variant at all. Cross-validated both directions
against yt-dlp format tables. Worth folding into the harvest step.

**Environment:** YouTube media bytes unavailable (bot wall + DRM on tv client, no
JS runtime); metadata still reachable via android_vr client. TikTok and Instagram
media download fine. faster-whisper 1.2.1 installs and runs on CPU — the TikTok
no-caption gap is closable here.
