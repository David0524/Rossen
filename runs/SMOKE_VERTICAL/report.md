# SMOKE TEST — vertical path, single beat

**Run:** SMOKE_VERTICAL · 2026-07-25 · branch `claude/gift-card-vertical-beat-test-glmu54` (HEAD `e81d096`, 2026-07-24 vertical fix)
**Status:** ⚠️ Smoke test. Not an episode. Excluded from yield tallies.

Fixture: `vertical_test.txt` (gift-card rack scam). Fed to the beat extractor as
plain text; pandoc/docx conversion skipped as instructed.

---

## 1. Beat extraction — both assertions confirmed

| Field | Value |
|---|---|
| `beat_id` | `smoke-vertical-b01` |
| `clip_role` | **`explainer_demo/creator_short`** ✅ |
| `orientation` | **`vertical`** ✅ |
| `platforms` | `shorts, tiktok, instagram` |
| `news_anchor` | `FTC gift card draining warning` |
| `priority` | 1 |

**Role derivation.** The lead-in *"WATCH HIM SHOW YOU HOW TO CHECK A CARD BEFORE
YOU BUY IT"* is a defense-demonstration tell, not a victim tell (*"listen to what
happened to him"*) and not a confrontation tell (*"watch what happens when"*).
That lands `explainer_demo`. The `(((PLAY CLIP XXX VERTICAL)))` marker splits the
role to `creator_short` rather than `creator_long`, per the extractor's platform
split. Orientation comes from the producer-authored marker and is treated as a
hard constraint, not a hint.

**No figure invented.** The FTC line carries no dollar amount or case count in the
fixture. The anchor register was generated without one — `FTC gift card draining
warning`, not a fabricated total.

## 2. Query generation — all four registers plus the shorts dialect

`runs/SMOKE_VERTICAL/queries.json`. 22 strings: `platform` 6 (lead register for
this role), `victim` 5 (also-run), `news` 4, `anchor` 2, `shorts` 5.

Shorts dialect written to spec — short, hashtag-heavy, emotion-forward, person and
feeling ahead of mechanism: `#scamalert check the gift card`, `gift card already
empty #shorts`, `he checked it before buying #scamalert`.

`platform_map` runs all three platforms in the role's map: shorts, tiktok, instagram.

## 3. Harvest — one candidate per platform, verified

### YouTube Short
- **URL:** https://www.youtube.com/shorts/ZVQPxS16At0
- **Title:** How to spot if a gift card has been tampered with before your purchase
- **Uploader:** CTV News · 119s · 2025-12-12 · 6,345 views
- **Orientation — VERIFIED vertical.** Two independent non-duration pixel reads:
  yt-dlp format table lists every video rendition portrait (fmt 137 **1080x1920**,
  fmt 248 1080x1920, fmt 136 720x1280); and `ffprobe` on the original-aspect-ratio
  thumbnail `oardefault.jpg` returns **1080x1920**. A decoded-frame probe was *not*
  possible — YouTube media bytes are bot-walled and DRM-blocked in this environment.
  Stated as a limitation rather than papered over.
- **Genuinely a Short:** `GET /shorts/ZVQPxS16At0` → HTTP 200, no redirect.
- **Caption track:** **yes** — auto-captions `en-orig`, `en`. No Whisper needed.
- **Caveat:** at 119s it clears the current 3-minute Shorts ceiling but would be
  **excluded by the harvest step's `--match-filter "duration < 60"`**. See §5.

### TikTok
- **URL:** https://www.tiktok.com/@cbsmornings/video/7451654556297055518
- **Title:** Scammers may access gift card numbers and PINs before they're even purchased
- **Uploader:** cbsmornings · 30.57s
- **Orientation — VERIFIED vertical, strongest available method.** Media downloaded
  (2.99 MiB) and `ffprobe` run on the decoded video stream:
  `width=1080 height=1920 duration=30.566667`. This is the real frame.
- **Caption track:** **none**, as expected — yt-dlp returns no subtitles and no
  automatic captions. Whisper is required for a verbatim outcue.
- **Whisper: available and verified working here.** `faster-whisper 1.2.1` installed
  and transcribed this clip on CPU. Opening cues:
  `[0.00-3.00] "So look at it, if the protective sticker has been removed,"`
  `[3.00-6.08] "if that barcode has been scratched off really any signs"`
  `[6.08-8.52] "of tampering, go talk to a store manager."`
  The transcript confirms this clip *is* the beat's defense demo, not merely adjacent.

### Instagram
- **URL:** https://www.instagram.com/reel/DSk4bzkklJh/
- **Uploader:** HuffPost (senior reporter Monica Torres) · 151.57s
- **Orientation — VERIFIED vertical.** Media downloaded (11.72 MiB), `ffprobe` on
  the decoded stream: **720x1280**. yt-dlp additionally lists a 1080x1920 rendition.
  Portrait on both reads.
- **Caption track:** **none.** Whisper required; confirmed available.
- **Fit caveats, flagged not hidden:** 151s is long for `creator_short`, and the
  presenter is a woman while the script says *"WATCH HIM."* Surfaced as-is rather
  than swapped — this is an orientation smoke test, not an air pick.

## 4. The vertical postmortem bug — reproduced live, four distinct ways

This is the headline result. The bug is not theoretical and it is not rare.

| Video | Duration | Real dimensions | What a naive check concludes |
|---|---|---|---|
| `PNjdcz3eG9o` (Tampa Bay 28) | **25s** | **1280x720** | duration <75s → "vertical" → **ships landscape** |
| `oI05QvICQo8` (WBIR) | **21s** | **1280x720** | same failure at 21 seconds |
| `DSqkiUoD5eW` (WTHR) | **58s** | **640x360** | it's a `/reel/` URL *and* sub-60s → **both** heuristics fail at once |
| `_RTe-ddhxoY` (Nichelle Laus) | 80s | 540x960 | vertical, but `/shorts/` **303→/watch** — not a Short. Inverse error |

**Every single sub-60s YouTube result across nine Shorts-dialect queries was
landscape.** Local-news packages dominate that duration band and they are all 16:9.
Duration is not merely a weak orientation proxy on this topic — it is anti-correlated.

**Useful method found:** the original-aspect-ratio thumbnail (`oardefault.jpg` /
`oar2.jpg`) is a cheap, reliable discriminator when media bytes are blocked —
landscape videos have **no `oar` variant at all** (confirmed: `PNjdcz3eG9o` 404s on
`oar`, while `_RTe-ddhxoY` returns 540x960 matching its yt-dlp read exactly).
Recommend folding this into the harvest step as a pre-download orientation gate.

## 5. Per-platform yield — reported honestly

**Pipeline harvest leg** (`python -m rossen_harvest --db … search`), the number that
should be counted:

```
315 raw -> 244 after dedupe across 1 beat (youtube + brave)
by platform: news_web 117 · youtube 107 · reddit 20 · tiktok 0 · instagram 0
```

**Native-social yield from the pipeline: 0 of 244.**

That is the expected, correct result, not a failed test. It matches the documented
8/7,549 (~0.11%) baseline and it matches the query-generator skill's own warning:
every `tiktok.com` URL Brave returned was a `/discover/` browse page, and
`brave.py`'s `/video/` path detector correctly demoted all of them to `news_web`
rather than miscounting them as TikTok candidates. Instagram returned nothing at all.

**The two social picks in §3 came from hand-run targeted Brave probes outside the
pipeline** (`site:instagram.com/reel …`, `tiktok.com/video …`), not from the harvest
command. Do not read "three platforms, three candidates" as the pipeline clearing
the bar — it did not. Generic discovery of native TikTok/IG posts still needs an
authenticated scraper or a paid social-search API, exactly as the README states.

### Two concrete defects this run surfaced

1. **The Shorts duration filter is stale.** `--match-filter "duration < 60"` encodes
   the legacy Shorts ceiling. YouTube Shorts now run to 3 minutes. The best YouTube
   candidate for this beat (119s, genuinely served at `/shorts/`) would be silently
   dropped by the harvest step. Recommend raising to `duration < 180` and gating on
   the `/shorts/` URL resolving rather than on duration.
2. **The `#shorts` suffix actively hurt recall here.** Suffixed queries returned
   almost exclusively landscape local-news packages and off-topic sticker-removal
   craft videos. The on-topic Shorts were found by `site:youtube.com/shorts` via
   Brave instead. Worth measuring properly before trusting the suffix convention.

## 6. Environment

| Capability | Status |
|---|---|
| YouTube metadata | OK via android_vr client (web client bot-walled after search volume; 429 → "Sign in to confirm you're not a bot") |
| YouTube media bytes | **Blocked** — DRM on tv client, no JS runtime for the n-challenge |
| TikTok metadata + media | OK (plain yt-dlp; `curl-cffi` deliberately not installed, per README) |
| Instagram metadata + media | OK |
| `faster-whisper` | **Installs and runs on CPU** — 1.2.1, verified end-to-end on the TikTok pick |
| `BRAVE_API_KEY` | Present; both web and video endpoints live |

---

# Addendum — both defects patched and re-measured

Patched in `harvest/rossen_harvest/shorts.py` (new), with wiring in
`__main__.py`, `youtube.py` and `candidates.py`. Skill docs updated.

## What changed

1. **Shorts ceiling 60s → 180s**, and duration demoted to a pre-filter.
   The authoritative format test is now `is_short()` — whether
   `GET /shorts/<id>` returns 200 or redirects to `/watch`.
2. **`site:youtube.com/shorts` added as a second Shorts leg**, run as a
   synthetic `shorts_web` register on the Brave web endpoint. The `#shorts`
   suffix leg is kept, not replaced; which one earns its budget is now an
   eval question.
3. **Pixel orientation gate** (`verify_orientation`) runs automatically over
   YouTube candidates on vertical beats. `--drop-landscape` removes the
   failures; `unknown` is never treated as a pass.
4. **Bug found in the patch itself and fixed.** `harvest_beat` concatenated
   registers before truncating to `--brave-cap`, so `shorts_web` landed at
   the tail and ran zero queries. Job selection is now round-robin across
   registers, so a cap starves every register evenly instead of starving the
   last one entirely. Regression test added.

## Re-run, same beat, same queries

```
before:  315 raw -> 244 deduped   news_web 117 · youtube 107 · reddit 20 · tiktok 0 · instagram 0
after:   318 raw -> 141 deduped   news_web 108 · youtube  24 · reddit  9
         orientation gate: 130 youtube candidates on vertical beats —
           verified vertical 23 · landscape 106 · unknown 1 · served as Shorts 29
```

**106 of 130 YouTube candidates on this vertical beat were verified landscape
and dropped — 82% of that leg.** Every one of them would previously have
reached the grader as a nominally valid candidate for a vertical beat.

## The result that matters

Both YouTube picks in §3 — CTV News `ZVQPxS16At0` and `94SwHPegzDI` — were
found **by hand, outside the pipeline**, in the original run. After the patch
they surface **from the pipeline itself**, along with 21 other verified-vertical
Shorts. The `shorts_web` register contributed 18 candidates; the `#shorts`
suffix register contributed 1.

That last ratio is the sharpest read on defect 2: on this beat the
path-constrained web search out-produced the hashtag suffix 18 to 1.

## What did not change

Native-social yield is still **0 TikTok, 0 Instagram** from the pipeline. That
gap is not what was patched and remains real — generic discovery of native
TikTok/IG posts still needs an authenticated scraper or a paid social-search
API. The two social picks in §3 still came from hand-run probes.

Reddit dropped 20 → 9 and news_web 117 → 108 purely from the round-robin cap
reshuffling which eight queries each Brave endpoint spends its quota on. Not a
regression, but worth knowing the cap now spreads across five registers
instead of concentrating in two.

## Tests

`python3 tests/test_shorts.py` — 50 tests, network stubbed, fixtures are the
real videos from this run. Existing suites unchanged and passing: 33 offline,
32 Brave, 24 transcripts, 16 vertical-transcribe.

`shorts.py` was also validated against live network on all five smoke-test
videos, and agrees with the yt-dlp format tables in both directions.
