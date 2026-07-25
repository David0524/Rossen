# Handoff message — paste this into the new Claude Code chat

Everything below the line is the message. It is self-contained: a session that
reads only this can work correctly without any prior chat.

---

You are picking up the **Rossen Reports clip discovery system**. This message is
your full handoff. Read it before running anything.

## Repo and branch

Repo `David0524/Rossen`. Check out **`claude/rossen-pipeline-script-hcflp6`** —
**not** the default branch. Current head is `cb0380e`. That branch has the
skills, the harvest package, three completed runs, and the docs.
`claude/rossen-pipeline-run-id57xe` is kept fast-forwarded to the same commit;
either works, but confirm with `git branch -r` and `git log --oneline -5` rather
than trusting this message — the branch will go stale once the work merges.

Two docs in the repo go deeper than this message. Read `HANDOFF.md` first — it is
current as of 2026-07-24 and is the full context. `NEW_SESSION_PROMPT.md` has
paste-ready prompts for specific tasks.

## What this system does

Jeff Rossen hosts a live consumer-protection show. Each episode has beats where
Jeff reacts to a clip — a local affiliate interviewing a scam victim, doorbell
cam footage, someone ranting in their car. Finding and timecoding those clips was
manual and consumed all the producer's time.

This system automates it: **a script goes in, a picks manifest plus a filled
Bible `.docx` comes out.** A human reviews; you make the initial pick.

The design rests on one insight: **the hard part is vocabulary mismatch, not
video processing.** A script says *romance scam targeting seniors through
Facebook Messenger*. The clip that airs is someone crying in their car saying *my
mom sent forty thousand dollars to a guy who said he was deployed overseas*.
Those share almost no words. Search the script's language and you get PSAs.

Optimize for **recall at harvest** — thirty scannable candidates per beat, not
the correct four. Precision comes later from the grader, which knows more.

## Setup — run this first, every session

```bash
git branch --show-current                      # confirm you're on the right branch
pip install -r harvest/requirements.txt        # never preinstalled, no pip cache carries over
export PYTHONPATH="$(pwd)/harvest"             # or `import rossen_harvest` fails
which ffmpeg                                   # system binary, IS present, not pip-installable
echo "${BRAVE_API_KEY:+brave key present}"
```

**`pandoc` is NOT installed.** Do not plan around it. The beat-extractor skill
has a `zipfile` + `ElementTree` fallback for converting a `.docx`. Use that
directly rather than discovering the gap.

**`BRAVE_API_KEY` should be set in this environment** — the user is adding it.
Verify it actually authorizes, don't just check that it exists:

```bash
curl -s -o /dev/null -w "brave HTTP %{http_code}\n" \
  -H "X-Subscription-Token: $BRAVE_API_KEY" \
  "https://api.search.brave.com/res/v1/web/search?q=test&count=1"
```

If it's missing or unauthorized, the search step prints a `DEGRADED` line and
runs **YouTube-only at roughly 70% coverage** — no `news_web`, no Reddit, no
vertical coverage. **Stop and say so rather than grading a half-empty pool.** On
the last run, Brave is what surfaced the exact-case CBS clip that became the b04
pick, and the print coverage that proved another case had no video at all.

**A cold `harvest.db` is expected and fine.** It's gitignored because it's a
rebuildable cache (searches and captions, 2-week TTL). A fresh clone has none;
search re-runs in about 3 minutes. Only delete it deliberately to force a cold run.

## Environment realities — verify, don't assume

Measured 2026-07-24 on one egress IP. **If your own probe disagrees, your probe
is right and this message is stale.**

| Path | State |
|---|---|
| YouTube search (`--flat-playlist`) | works |
| YouTube captions (per-video page) | works — but throttles easily |
| YouTube **media bytes** (incl. `-f bestaudio`) | blocked |
| Direct YouTube page fetch via WebFetch | bot-walled, redirects to `/sorry` |
| TikTok | blocked — "Your IP address is blocked" |
| Brave API | works |

**The trap that cost the most last run:** rate limiting and a hard block return
the *identical* "Sign in to confirm you're not a bot" string. A rapid diagnostic
burst — a dozen `--list-subs` calls in two minutes, several looping over
`player_client` values — drove captions to **0 of 6** on video IDs a prior run
had captioned successfully. It looked exactly like a hard IP block, and I
reported it as one at a checkpoint. Twenty minutes later the normal `fetch_many`
path returned **11 of 12**. Nothing had been fixed; the burst had tripped a
limiter.

So: probe **once** per path, never in a loop, and never iterate player clients as
a first move — that iteration is itself what trips it. If a probe fails, wait
several minutes and retry through the real code path before concluding anything.
Calling a throttle a block converts every pick in the run to an unverified outcue
for no reason.

**Whisper's reach equals your media access and no wider.** `vertical_transcribe.py`
transcribes bytes something else must fetch. With YouTube media and TikTok both
blocked, it has zero reachable sources here. It is correct code this environment
cannot exercise — don't plan around it, and don't treat it as a way around a block.

## What exists, and what does not

**Working:** `rossen_harvest` search across three surfaces (YouTube long-form,
YouTube Shorts, Brave web+video) with dedupe and SQLite caching; `transcripts.py`
caption fetch (no media download — and note `fetch_many` takes **bare video IDs**,
not URLs, or every fetch silently returns None); five skills in `.claude/skills/`;
**128 passing tests**.

**Does not exist — never claim otherwise:**
- **No download-and-cut stage.** `python3 -m rossen_harvest --help` lists exactly
  two subcommands, `harvest` (alias `search`) and `eval`. Nothing downloads or
  trims video. Step 7 is a hand-written manifest — a handoff to the edit bay.
  Say picks were *located and timecoded*, never that clips were pulled or cut.
- No FCPXML writer, no Airtable push, no PySceneDetect snap, no authenticated
  social scraper.

**Tests are plain scripts, not pytest:**
```bash
for t in harvest/tests/*.py; do python3 "$t"; done
```
Don't use pytest — it collects zero tests and dies on the module-level
`sys.exit`, so a green pytest run would mean nothing ran.

## Where things stand

Three runs completed: `runs/F2_07292026`, `runs/F2_08052026`, `runs/F2_08072026`.
Read the newest `report.md` for detail.

Most recent (F2 08-07, a 4-beat Friday single-story script): b01 and b02 both
picked from **one** FOX 13 Tampa Bay package cut twice as a butt-cut, outcues
verified verbatim; b03 assigned show-produced; b04 is a CBS News New York clip
shipping as `MANUAL CLIP — no captions` with **no timecode**, because no caption
track exists and none was invented.

## Hard rules — these are not negotiable

- **Every segment needs an outcue found verbatim in the transcript**, verified
  with `Transcript.find()`, never by eye. If you can't find the phrase, your
  timecode is wrong. If no transcript is reachable, ship the pick with **no**
  outcue and flag it unverified. Never invent or paraphrase one.
- **If nothing clears the bar, flag the beat empty.** A bad pick gets discovered
  in the edit bay and costs more than an honest gap.
- **Diagnose before repairing.** Zero candidates for a beat is a query problem,
  not a search problem. Re-query before calling a case unsourceable, and say
  which queries you ran.
- **Orientation is a hard filter, not a hint** — producer-authored, correct in
  26 of 26 observed cases. One deliberate exception: a YouTube Short surfaced
  against a horizontal beat carries `surfaced_for: horizontal` and gets scored
  with the framing question flagged for a human, not auto-failed. Shorts run on
  *both* orientations.
- **A `BUTT` marker means both segments come from the same source.** Prefer one
  source cut twice over two sources.
- **A case swap changes what Jeff says on air.** That is the producer's call —
  propose it, never do it silently.
- **`SHOW-PRODUCED` is not a failure** and must never be logged as `EMPTY`. A
  beat correctly identified as unsourceable *before* search ran is the
  sourcability scan working.

## Logging — one canonical path

Append every beat of every run to **exactly** this path:

```
.claude/skills/rossen-beat-extractor/reference/beat_yield.md
```

Not a bare `reference/beat_yield.md`. That ambiguity already split this log
once: three runs appended to a second copy at the repo root while the copy that
ships with the skill sat an episode behind, and the two drifted into incompatible
schemas with zero overlapping episodes before anyone noticed. They're merged now
and the old path holds a pointer stub. Don't restart the split.
`rossen-pipeline` Step 9 has the schema and outcome vocabulary.

## Skills: the repo is the source of truth

The five Rossen skills live both in `.claude/skills/` here and in the user's
Claude account. **The repo is canonical**; the account is a deployment target
with no history and no diff. The account copies have drifted behind before and
lost their `reference/` folders entirely — which fails *silently*, because a
skill pointing at a missing file just proceeds uncalibrated rather than erroring.

Edit here, commit, rebuild `dist/skills/*.zip` (script in `dist/skills/README.md`)
so the user can re-upload. Never edit in the account expecting it to come back.

## Open items, in priority order

1. **The Shorts fix is unexercised against a live vertical beat.** Vertical beats
   previously never reached the YouTube backend at all — their `shorts` register
   ran nowhere. Fixed with `ShortsBackend`, and it contributed 56 candidates, but
   only against *horizontal* beats, because 08-07's single vertical beat went
   show-produced. Confirm it end to end on the next script with a live vertical beat.
2. **Vertical `evidence` beats have yielded nothing in 4 of 4 attempts** across
   two episodes — the strongest structural finding in the system. Catch these at
   extraction, not after a full search and grade.
3. **The `victim` register scored zero** on horizontal/YouTube in the one
   recall@30 eval (0.889 overall; `platform` was the workhorse). It was theorized
   to matter on vertical, which was never tested.
4. **The diversity floor promoted a loser twice in one run.** If that repeats
   across episodes, the upstream hard filters need a look, not the floor.
5. **F2 08-07 b04 vintage unconfirmed** — the CBS clip is an exact case match but
   the script flags it as a 2024 package and the page exposed no publication date.

## Working style

Work autonomously; don't ask permission for anything reversible. Stop at two
checkpoints when running the pipeline: after beats and queries before search, and
before any repair proposal touches the script.

Report what actually happened — per-platform counts as printed, stages that ran
long, steps that were skipped. If you get something wrong mid-session, correct it
plainly and move on. The last run misdiagnosed a throttle as a hard block, and
saying so plainly was more useful than defending it.
