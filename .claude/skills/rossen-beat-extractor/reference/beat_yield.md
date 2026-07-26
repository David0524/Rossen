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

**Patched 2026-07-25 (same session).** Both defects fixed in `shorts.py` +
harvest wiring. Re-run on the same beat: the orientation gate verified 130
YouTube candidates and dropped **106 as landscape (82% of the leg)**; the two
YouTube picks that originally had to be found by hand now surface from the
pipeline. `site:youtube.com/shorts` out-produced the `#shorts` suffix 18 to 1.
Native-social yield unchanged at 0 tiktok / 0 instagram — that gap was not what
was patched. See `runs/SMOKE_VERTICAL/report.md` addendum.

## Run F1_07312026 (Airbnb/VRBO rental scam + DealSeek Friday)

| Beat | Role | Or. | Outcome | Why / source |
|---|---|---|---|---|
| F1-b01 | victim_interview | H | PICK | Scripps DWYM (Matarese) 0:18-0:55 "straight to voicemail" (Laura Gentry, $950 Zelle); pulled off WCPO's Uplynk stream, Whisper-verified |
| F1-b02 | authority_report | H | PICK (butt seg 2) | Same Scripps package 0:59-1:19 "not really part of this transaction" (Kevin Brasler, Consumers' Checkbook) |
| F1-b03 | victim_interview | H | PICK (2 segs) | Inside Edition VfwRWgw_M3I 0:30-1:38 "up in the scam" + 1:51-2:49 "coming up on surfing websites" (Allie Conti); recovered via the outlet's own Facebook upload after installing deno |
| F1-b04 | victim_interview | H | LOCATED | CBS LA WMofFj3FJDQ (Jeff Branch, Santa Monica Mountains) — confirmed the right case via KNX's write-up; same bot-wall |

**Yield:** 3 PICK / 1 LOCATED / 0 EMPTY of 4. Both LOCATED are environment
artifacts, not sourcing failures — every beat in this episode has a confirmed,
live source. On a machine with normal YouTube access this is plausibly 4/4.
Confirmed: a 25-minute-cooldown retry of the full 19-clip shortlist also returned
0/19 captions, so the wall is persistent here rather than a rate-limit from the
3,053-query search. Do not read these two LOCATED rows as evidence about the
material.

**Only 4 beats.** Friday format: one story block plus the DealSeek segment. The
DOJ block (Goel/Raheja) carries no PLAY CLIP marker and is a Jeff read, correctly
excluded. Low beat count is the script, not the extractor.

**Pattern — the sourcability scan paid for itself three times.** It answered all
three producer questions before any search ran: it confirmed the b01/b02 BUTT by
finding Gentry and Brasler quoted in one Scripps article, it disproved the
"we have not confirmed video exists" note on Conti, and it identified the Branch
package. All four targets then surfaced at rank 1-2 in the real search. Contrast
F2, where three beats reached Checkpoint 3 empty because no scan ran.

**Pattern — `news_web` is not a dead end when the outlet is Scripps.** F2 logged
five LOCATED beats as unusable because affiliate sites carry no captions. That is
only half true: Scripps stations expose an Uplynk HLS manifest in the page HTML,
which ffmpeg can pull and Whisper can transcribe. That converted what F2 would
have logged as LOCATED into two real PICKs with verified outcues. Worth trying on
every future news_web beat before writing it off.

**Pattern — the diversity floor fired on 4 of 4 beats and its promotion lost pass
two 4 of 4 times.** Same signal the grader skill warns about. Two runs of this
and the hard filters upstream need a look.

**Pattern — when YouTube is walled, try the outlet's own social upload, and
install deno first.** b03 looked dead: Inside Edition's site 404s and Facebook
initially reported 0 formats. Installing deno (the JS runtime yt-dlp warns about)
changed that — the same Facebook URL then exposed a downloadable render, at the
identical duration as the YouTube cut, so the timecodes transferred straight to
the YouTube link. Two beats in this run were rescued by going to a non-YouTube
host: Scripps/Uplynk for b01-b02, Facebook for b03. Try both before logging
LOCATED.

**Environment:** YouTube search fine, individual video pages fully bot-walled
(all player clients; mweb needs a PO token for subs, tv returns DRM). Brave key
present. faster-whisper working. Two documented CLI stages (`captions`, `clip`)
were missing and were built during this run.

## Run AMAZON_ATOZ (single beat, Amazon A-to-Z Guarantee)

| Beat | Role | Or. | Outcome | Why / source |
|---|---|---|---|---|
| ATOZ-b01 | victim_interview | H* | PICK | ABC7/KABC 7 On Your Side 0:22-1:55 "and I was denied twice" (Pam Skinner, Menifee, $12K tiny home never arrived); transcript via ABC7's own HLS stream + Whisper |

*Orientation assumed, not producer-authored — the excerpt carried no PLAY CLIP marker.

**Pattern — "scam" is a poisoned token on retailer beats.** The first pass on this
beat returned 732 candidates and almost nothing usable, because "Amazon refund
scam" is overwhelmingly the phishing-text story, not the denied-claim story.
Dropping "scam" and leading on the outcome shape (denied → escalated → paid)
turned it around. Add to the glossary: for retailer dispute beats, search the
resolution, not the crime.

**Pattern — the investigative-franchise register earned its place again.** A
dedicated `franchise` register ("7 On Your Side", "Call for Action",
"Troubleshooters", "2 On Your Side", "Contact 13", "Action 9") is what put the
pick's neighbourhood in reach. This is the second run where the franchise
register was decisive; it is currently documented only as a note in the glossary
and should probably be promoted to a first-class register in the generator.

**Thin beat, honestly.** 953 candidates on the good pass, of which only 11 were
affiliate and on-topic. The shape the script asks for — a woman, on camera,
explicitly denied — is rare. Most Amazon-refund video is phishing coverage or
seller-side tutorials.

**Fit caveat worth remembering:** no local package says the words "A-to-Z
Guarantee." Consumer desks say "appealed" and "denied." When a beat is built
around a brand-name process, expect the clip to carry the experience and the
script to carry the term.

## Run AMAZON_RETROCHARGE (single beat, $309.5M returns settlement)

| Beat | Role | Or. | Outcome | Why / source |
|---|---|---|---|---|
| RETRO-b01 | authority_report | H* | EMPTY | No reachable broadcast video on the $309.5M "no-hassle returns"/retrocharge settlement. Print-only (Reuters, Verge, PCMag, Law360). Sole TV package — PIX11 2026-01-29 — is 403-walled here and no Nexstar sibling carried it |

*Orientation assumed; no PLAY CLIP marker in the excerpt.

**Pattern — concurrent settlements from the same company are a live trap.** Two
Amazon settlements are running at once: the $309.5M returns/retrocharge case
(Jan 2026, Seattle) and the $2.5B Prime/FTC case (claims deadline 2026-07-27).
Every reachable "Amazon settlement" video is the Prime one, and the GMA version
cut cleanly — right words, wrong settlement. The triage only kept it out because
the beat carried an explicit `disambiguation` field and the scorer applied a
negative weight to Prime/FTC/$2.5B tokens. **Recommend adding a `disambiguation`
field to the beat record whenever a beat names a specific case, amount or docket
from a company with other live litigation**, and having the grader treat a
mismatch there as a hard filter rather than a scoring penalty.

**Pattern — authority_report can be EMPTY because the news is old, not because
the search failed.** This settlement peaked in print in late January and went
quiet; the claim form is still "coming soon" after preliminary approval. There
is no fresh video because there is no fresh news. That is worth reporting to the
producer as a script note ("the latest is that nothing has happened yet") rather
than logging as a sourcing failure. Re-run when the claims window opens; a
"you may be owed money" package is near-certain then.

**Running total on `authority_report` for dated federal/legal actions: F2-b07
EMPTY (IC3 alert 5 days old), RETRO-b01 EMPTY (settlement quiet since January).
Both ends of the recency curve fail — too new for video, and too old for video.
The airable window for this role looks narrow.**
