# FRIDAY 08/07/2026 — "Amazon OWES You Money" — pipeline run report

**Theme:** Amazon refunds you never claimed · A-to-Z guarantee denials · the $309.5M retrocharge settlement
**Scope:** **clip 1 only**, by request. Beats 2-5 were identified during extraction but not queried, searched, or graded.
**Sidecar hints:** none. No `beats_hint.json` next to `script.docx` — hints-vs-generated comparison is **N/A this run**.

## Preflight

| Check | Result |
|---|---|
| pandoc | missing → installed via `apt-get` |
| yt-dlp | 2026.07.04 ✅ |
| faster-whisper | missing → installed via `pip` |
| ffmpeg | already present ✅ |
| `BRAVE_API_KEY` | **present and authorizing (HTTP 200)** ✅ — full coverage, run was *not* degraded by a missing key |
| YouTube **search** (flat-playlist) | ✅ OK |
| YouTube **captions** (per-video page) | ✅ OK **after fixing four missing local dependencies** (initially read as bot-walled) |
| YouTube **media bytes** | ❌ **BLOCKED** — googlevideo 403s this datacenter IP, not fixable here |

The search key question you flagged as a stop condition is clean: Brave is present and authorizes, so this run had the full three-surface coverage, not the ~70% YouTube-only fallback. No beat failure here is an artifact of a missing key.

**The caption wall came down; the media wall did not.** Both paths initially returned "Sign in to confirm you're not a bot," and I first reported that as environmental. That was premature — the caption failure was four missing local dependencies, not a block:

1. **JS runtime** — installed deno. yt-dlp needs one to solve the `n` challenge; without it formats silently vanish ("Only images are available").
2. **Challenge solver** — `pip install yt-dlp-ejs`. The `--remote-components ejs:github` route fails on the agent proxy's TLS re-termination; the pip package ships the same script locally.
3. **PO token provider** — built and ran the bgutil server, plus `pip install bgutil-ytdlp-pot-provider`, with `NO_PROXY=127.0.0.1,localhost` so yt-dlp reaches it directly.
4. **axios >= 1.16.1 inside that server** — it ships 1.13.5, which sends non-CONNECT requests the agent proxy rejects with **405**, so every token mint failed with a 500. The proxy README names this exact cause and `$HTTPS_PROXY/__agentproxy/status` confirmed it. Upgrading to 1.18.1 fixed it.

Captions then fetched cleanly with `--skip-download --ignore-no-formats-error` (that flag matters — subtitles are found but yt-dlp aborts on format selection without it).

**Media bytes are genuinely blocked.** googlevideo 403s this datacenter IP under every player client even with a valid PO token, and the proxy status endpoint showed no org-policy denials for the CDN — so this is YouTube's edge refusing the IP, not your egress policy. Nothing in this container gets around it.

## Beat table

| Beat | Role | Or. | Outcome | Source | In–Out · Outcue |
|---|---|---|---|---|---|
| 08-07-b01 | explainer_demo/creator_long | H | **PICK ✅** | In the Black `_8W0-cK5XTQ` (creator_long, 270s) | 1:02–1:41 · "worth a shot though" — **verified at 00:01:39.600–00:01:41.510** |

**Source mix, 1 beat:** creator_long 1.

**Status: clean pick, verified outcue.** No caveats on this one.

## Search results

322 raw candidates → 257 unique YouTube · 55 news_web · 9 reddit. 14 queries via YouTube, 8+8 via the two Brave endpoints.

Register breakdown of the raw pool: shorts 86 · news 73 · anchor 73 · platform 61 · victim 29.

## The pick

The script arrived with clip 1 **already filled in** by the producer: `_8W0-cK5XTQ`, "DO THIS every time a Amazon package arrives late," In the Black, 270s.

The generated queries surfaced that exact video at **rank 1**, hit by **11 of 14 query strings** spanning all five registers (anchor, news, victim, platform, shorts). That convergence is real independent evidence the footage is right — arrived at without reference to what was already in the doc.

It also fits the beat on every axis metadata can see: an established consumer-finance channel doing an actual screen-recorded walkthrough of the Amazon guaranteed-delivery refund path, which is precisely what `explainer_demo/creator_long` asks for (and a role where a good creator video is the *natural* source, not a degraded affiliate substitute). 270s comfortably contains the proposed 39s segment plus setup runway.

**The outcue is verified.** The transcript puts "worth a shot though" at **00:01:39.600–00:01:41.510**, in context:

> "...but I've been rejected and your mileage may vary, it's still **worth a shot though**. / So let's get into how to do this..."

The producer's OUT of 1:41 lands on the phrase, immediately before he pivots to the how-to. **The IN of 1:02 also checks out** — at 1:02 he says "in the past I've successfully gotten three different types of compensation by reaching out to Amazon via their chat feature online," which is exactly what the script's "ask the agent flat out for an account credit, you have to say the words" sets up. The 39 seconds between cover the Prime-extension history, the $10-plus account credit, and the possibility of a full refund.

Both draft timecodes were accurate as written. No adjustment needed.

Tone check off the transcript: he is candid that the ask sometimes fails ("I've been rejected, your mileage may vary") rather than selling it as a guaranteed hack. Consumer-protective and plain — right register for the show.

The transcript is saved to the run directory as `transcript_8W0-cK5XTQ.en.vtt` so the verification is auditable.

## Pass-one shortlist (metadata triage)

Five survivors, all `creator_long` except one `first_person`. Hard filters removed compilations, AI-slop channels ("Amazon Refund Method Free," "How to hack Amazon in easy," and a cluster of free-Prime-membership bait), one junk-title artifact, and a large volume of off-topic Amazon-seller-side content that the broad queries pulled in.

| # | Source | Type | Dur | Note |
|---|---|---|---|---|
| 1 | In the Black `_8W0-cK5XTQ` | creator_long | 270s | rank 1, 11-query convergence |
| 2 | MrHowTo `s4i6WQdHF00` | creator_long | 180s | direct topical match |
| 3 | Learn with Freddie `jHzGq_Ztb5c` | creator_long | 147s | 2025 full-guide framing |
| 4 | Tada Yada `DZ06YW82Qh8` | creator_long | 282s | topical, weaker channel signal |
| 5 | aleks dude `sKhE-ez4dGQ` | first_person | 88s | the one candidate that actually shows the *chat-agent* ask, which is the beat's closing line ("you have to say the words") |

The diversity floor did not need to fire — the shortlist was already mixed, and `creator_long` is the natural type for this role rather than a monoculture to break up.

Candidate 5 is worth a human look if the producer wants the "ask the agent flat out for an account credit" line landed on screen by a real person rather than described. It was not promoted over candidate 1 because at 88s from an unknown individual channel it is the weaker source, and whether the chat exchange is legible on camera is a framing question no transcript answers.

## Gaps and what I worked around

- **Zero query-side failures.** The beat returned 322 candidates and the right video at rank 1. No re-query was needed. Per the diagnose-before-repair rule, this was never a query problem, so nothing was swapped.
- **No script-touching repair was proposed**, so **Checkpoint 2 never triggered.** The pick matches what the script already says; no case swap, no name change, no rewritten setup lines. Nothing needed your approval.
- **Transcript ladder: rung 1 reached, after a detour.** The first pass through `fetch_many` returned null on all 5 and I reported an environmental block. Re-diagnosing found four fixable local dependencies instead. Rung 1 now works for any captioned YouTube video in this container. Rung 2 (Whisper) remains unavailable — it needs media bytes, which are genuinely blocked, so it is not a workaround for anything here.
- **I initially called this wrong.** Three bot-wall symptoms look identical — throttle, missing dependency, and true IP block — and the preflight protocol distinguishes the first from the third but has no step for the second. I logged UNVERIFIED on a wall that was mostly a dependency gap. Logged in `beat_yield.md` as a process lesson so the next run checks yt-dlp's own warnings (JS runtime / solver / PO token) before concluding anything is environmental.
- **`fetch_many` contract respected** — bare video IDs, not full URLs. The double-prefix bug that has bitten a prior run did not recur; the nulls here are the bot wall, confirmed by the raw yt-dlp error text.
- **No downloads, no cuts.** As designed — there is no automated download-and-cut stage in `rossen_harvest`. The deliverable is the located pick plus timecodes for a human to pull. In this environment the bytes were gated anyway.

## Beats not covered (out of scope this run)

Clips 2-5 exist in the script and were read during extraction but not processed, per your "clip 1 only" instruction. For planning:

| Clip | Or. | Shape | Note |
|---|---|---|---|
| 2 | V | TikTok, late-package refund demo | already filled in draft |
| 3 | V | TikTok, "delivered but nothing there" shoppers | already filled in draft |
| 4 | H | ABC7 $12,000 tiny home, denied twice | **news_web (abc7.com), not YouTube** — expect LOCATED, no caption track |
| 5 | V | TikTok, $309.5M settlement latest | already filled in draft |

Three of the four are vertical TikTok, which needs the Whisper path — still unavailable, since media bytes are blocked. Clip 4 is an abc7.com link with no caption track, so it stays a manual pull regardless.

The picture has improved for anything on captioned YouTube: that path now verifies properly in this container. But none of clips 2-5 are captioned YouTube, so running them here would still produce unverified outcues. They need either media access or a hand check.

## Deliverables written

- `beats.json` — beat 08-07-b01 with four-register queries
- `candidates.json` — 322 candidates
- `shortlist.json` — 5 pass-one survivors
- `picks.json` — the flagged pick, outcue verified with cue range and context
- `transcript_8W0-cK5XTQ.en.vtt` — the caption file the outcue was verified against
- `clips/manifest.json` — handoff manifest for the edit bay
- `FRIDAY_08072026_BIBLE_updated.docx` — filled Bible doc, clip 1 link + timecodes in blue, verification noted
- `report.md` — this file
- appended to `.claude/skills/rossen-beat-extractor/reference/beat_yield.md` — logged as `PICK`, with the full dependency recipe that brought the caption path back up, so the next run does not repeat the misdiagnosis. The `UNVERIFIED` outcome value stays in the header table; it is still the right label for a genuine transcript dead end, which this turned out not to be.
