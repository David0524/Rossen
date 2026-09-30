# Dependencies and preflight

Load this before Step 1, every run. Nothing here carries over from a prior chat.

- [What this pipeline needs that the skill does not ship](#what-this-pipeline-needs-that-the-skill-does-not-ship)
- [Install](#install)
- [Probe the network paths](#probe-the-network-paths)
- [Throttling is not blocking](#throttling-is-not-blocking)
- [Degraded-run rules](#degraded-run-rules)

## What this pipeline needs that the skill does not ship

Check all four before Step 1 and report anything missing **at Checkpoint 0**. Do
not begin a run with a missing dependency and discover it at Step 3.

| Dependency | What it is | If absent |
|---|---|---|
| `rossen_harvest` Python package (with `harvest/requirements.txt`) | The search + transcript CLI. Steps 3 and 5 are entirely this. | **Stop.** There is no fallback — see below. |
| The three sibling skills | `rossen-beat-extractor`, `rossen-query-generator`, `rossen-clip-grader`. Steps 1, 2, 4 and 6 are "read the sibling and apply it." | **Stop.** Do not improvise their logic. |
| `reference/aired_examples.md`, `reference/glossary.md` | Ground truth for beat extraction and register translation. Shipped with the sibling skills; in some deployments they sit in the project root instead. | Locate them before Step 1; say where you found them. |
| `beat_yield.md` | The append-only yield log Step 9 writes. | Run `python3 scripts/init_yield_log.py` — it writes the canonical header at the canonical path. |

**Resolve the siblings by skill name, not by filesystem path.** Earlier versions
of this document hardcoded `.claude/skills/<name>/SKILL.md`, which is one
deployment's layout and not the only one — the same skills also live under
`skills/`, under an account-level skills directory, and as installed skills with
no repo at all. Find them wherever this session exposes skills and say which path
you used. A hardcoded path that resolves to nothing has already caused a run to
proceed without reading a sibling at all.

**On the missing-package case.** Step 3's rule — never reimplement a stage in an
ad-hoc script, because the CLI already handles caching, dedupe, concurrency limits
and graceful backend failure — is still right, and it means an absent
`rossen_harvest` is a hard stop rather than an invitation to write a scraper. Say
so plainly, name what is missing, and ask for the package or for permission to run
a **beats-only** pass: Steps 1–2 plus the Checkpoint 1 table are genuinely useful
on their own and need no package. That is a real partial deliverable; a
hand-rolled search is not.

## Install

```bash
pip install -r harvest/requirements.txt   # yt-dlp, faster-whisper
python3 -c "import yt_dlp; print('yt-dlp ok')"
python3 -c "import faster_whisper; print('faster-whisper ok')"
which ffmpeg || echo "MISSING ffmpeg — brew install ffmpeg / apt install ffmpeg"
echo "${BRAVE_API_KEY:+brave}${SERPER_API_KEY:+serper}" || true
export PYTHONPATH="$(pwd)/harvest"   # required for `import rossen_harvest`
```

`requirements.txt` covers the only two non-stdlib Python deps; everything else is
stdlib. A fresh session has neither installed and no cached pip state, so run the
install line every time rather than assuming it carried over. `ffmpeg` is a system
binary, not pip-installable — check it separately.

## Probe the network paths

**Every check above can pass while the pipeline is functionally dead.** `import
yt_dlp` succeeding says the library is installed; it says nothing about whether
YouTube will *answer*. These four probes are not optional — run them and read the
result before Step 1.

```bash
# 1. SEARCH reachable? (flat-playlist metadata — the Step 3 path)
yt-dlp --flat-playlist --dump-json "ytsearch1:scam" >/dev/null 2>&1 \
  && echo "search OK" || echo "SEARCH DEAD"

# 2. CAPTIONS reachable? (per-video page — the Step 5 path, and the one
#    that verifies every outcue in the run)
yt-dlp --skip-download --list-subs "https://www.youtube.com/watch?v=aircAruvnKk" 2>&1 \
  | grep -q "not a bot" && echo "CAPTIONS BOT-WALLED" || echo "captions OK"

# 3. MEDIA bytes reachable? (the Whisper path — audio counts as media)
yt-dlp -f bestaudio -o /tmp/probe.%\(ext\)s --no-warnings \
  "https://www.youtube.com/watch?v=aircAruvnKk" >/dev/null 2>&1 \
  && echo "media OK" || echo "MEDIA BLOCKED"

# 4. BRAVE actually authorizes? (a present key is not a working key)
curl -s -o /dev/null -w "brave HTTP %{http_code}\n" \
  -H "X-Subscription-Token: $BRAVE_API_KEY" \
  "https://api.search.brave.com/res/v1/web/search?q=test&count=1"
```

**These three YouTube paths fail independently.** Search is a different endpoint
from the video page, which is different again from media bytes, and in a
shared-egress environment (a cloud container behind a pooled IP) they degrade in
that order — search survives longest, media dies first.

## Throttling is not blocking

**Distinguish them before you report either.** The "Sign in to confirm you're not
a bot" response is returned for *both*, and they need opposite responses.

Measured on 2026-07-24: a rapid diagnostic burst — a dozen `--list-subs` calls in
a couple of minutes, several of them looping over player clients — drove the
caption path to **0 of 6** on video IDs a prior run had captioned successfully. It
looked exactly like a hard IP block. Twenty minutes later the ordinary
`fetch_many` path, hitting the same host at its normal pace, returned **11 of
12**. Nothing was fixed; the burst had simply tripped a rate limiter.

So: probe **once** per path, never in a loop, and never iterate player clients as
a first move — that iteration is itself what trips the limiter. If a probe fails,
wait several minutes and retry once through the real code path (`fetch_many`)
before concluding anything. Report a hard block only after a spaced-out retry
through the normal path also fails.

Calling a throttle a block costs a whole run: it converts every pick to an
unverified outcue and pushes the producer toward a degraded deliverable they did
not need to accept.

## Degraded-run rules

**Captions bot-walled → stop at Checkpoint 0 for a ruling.** Do not run search
and grade into a dead end: without captions there is no transcript, without a
transcript no outcue can be verified, and this pipeline's central rule is that an
unverified outcue never gets written. A full run under that condition produces
picks whose timecodes are all unverified — a legitimate deliverable only if the
producer agreed in advance to receive one. Alternate
`--extractor-args youtube:player_client=…` values are worth **one** attempt
(`mweb` dodges the bot-check), but verify it returns real caption tracks rather
than an empty list: a client answering "no automatic captions" for a video you
know is captioned is degraded, not working.

**No web search key → YouTube only**, roughly 70% of normal coverage and no
TikTok, Instagram, Facebook or native network video. Say so plainly at Checkpoint
0 and ask whether to proceed degraded or stop and set a key. Do not quietly run a
crippled pipeline. If the run prints a `DEGRADED` line, `BRAVE_API_KEY` was
missing and every `news_web`/social/vertical beat got nothing — stop rather than
grading a half-empty pool.

**Media blocked → Whisper is off the table for the whole run.** It is not a way
around a block; it is a transcription step that consumes bytes something else had
to fetch. Do not plan around it for any platform, and expect vertical beats to
land at rung 3.
