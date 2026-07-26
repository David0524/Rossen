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
| 08-07-b01 | explainer_demo/creator_long | H | PICK | In the Black `_8W0-cK5XTQ` 1:02-1:41 "worth a shot though" — outcue verified against captions at 00:01:39.600-00:01:41.510; also surfaced independently at rank 1 by 11 of 14 queries |

**Yield:** 1 PICK of 1 searched.

**The caption bot-wall is fixable in-container, and here is the recipe.** This
run first read as the worst case: search worked (322 candidates) while the
per-video page and media bytes both returned "Sign in to confirm you're not a
bot," which kills rungs 1 and 2 of the transcript ladder together. It was
initially logged UNVERIFIED on that basis. That was premature — the wall came
down completely once four missing pieces were installed:

1. **A JS runtime** — `curl -fsSL https://deno.land/install.sh | sh -s -- -y`.
   yt-dlp needs one to solve the `n` challenge; without it formats silently
   vanish and you get "Only images are available."
2. **The challenge solver** — `pip install yt-dlp-ejs`. Do NOT rely on
   `--remote-components ejs:github`; that fetch dies on the agent proxy's TLS
   re-termination. The pip package ships the same script locally.
3. **A PO token provider** — clone `Brainicism/bgutil-ytdlp-pot-provider`,
   `npm install && npx tsc` in `server/`, run `node build/main.js --port 4416`,
   and `pip install bgutil-ytdlp-pot-provider` for the yt-dlp side. Export
   `NO_PROXY=127.0.0.1,localhost` so yt-dlp reaches it directly.
4. **axios >= 1.16.1 inside that server** — it ships 1.13.5, which sends
   plain-HTTP (non-CONNECT) requests that the agent proxy rejects with **405**,
   so every token mint fails with a 500. `npm install axios@latest` in
   `server/` fixes it. The proxy README names this exact cause; the
   `$HTTPS_PROXY/__agentproxy/status` endpoint shows the `not_connect` failures
   that confirm it.

Then fetch captions with `--skip-download --ignore-no-formats-error`. The
`--ignore-no-formats-error` flag matters: subtitles are found and listed, but
yt-dlp aborts on format selection before writing them without it.

**Media bytes stayed blocked** — googlevideo 403s the datacenter IP under every
client even with a valid PO token, and the proxy status endpoint showed no
org-policy denials, so that is YouTube's edge, not the egress policy. That is
the honest boundary: **captions are recoverable in this environment, media is
not.** Whisper-dependent surfaces (TikTok, Reels, native X) therefore remain
unreachable here, while any captioned YouTube pick can be fully verified.

**Process lesson, and it is the expensive one.** Three bot-wall symptoms look
identical — throttle, missing-dependency, and true IP block — and they have
different fixes. The preflight protocol correctly distinguishes throttle from
block, but has no step that distinguishes *missing local dependency* from
either. This run's wall was almost entirely the former. Add a dependency check
to the caption probe before concluding a wall is environmental: if yt-dlp warns
about a JS runtime, a challenge solver, or a PO token, that is a fixable local
gap, not a block. Calling it a block costs the run its verified outcues.

**Search-side cross-validation is a real signal, and it held up.** The script
arrived with clip 1 already filled in by the producer. The generated queries
surfaced that exact video at **rank 1**, hit by 11 of 14 query strings spanning
all five registers. When the transcript later came through, it confirmed the
pick — the segment delivers precisely the chat-agent/account-credit payload the
script sets up. So the convergence heuristic predicted correctly here. Worth
reaching for when captions are genuinely unreachable, but note it was used this
run as a substitute for a verification that turned out to be *available*, which
is the wrong trade whenever the dependency fixes above are on the table.

**Producer-supplied timecodes were accurate.** Both ends of the draft in/out
checked out against the transcript: OUT 1:41 lands on "worth a shot though"
(1:39.6-1:41.5), and IN 1:02 opens on "in the past I've successfully gotten
three different types of compensation by reaching out to Amazon via their chat
feature." No adjustment needed. First run where a draft timecode was verified
rather than replaced — worth tracking whether that holds.

**Register note (n=1, do not over-read).** The `anchor` register found the
target first here — consistent with the weighting table's `anchor` lead for
`explainer_demo/creator_long`. `victim` also technically surfaced it, which is
the first time `victim` has contributed on a horizontal/YouTube beat; the prior
eval had it at 0 for 8. One data point, and the video was found by nearly every
register, so this is not evidence `victim` earns its budget.
