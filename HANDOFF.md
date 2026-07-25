# Rossen Reports clip discovery system — handoff

Read this fully before doing anything. It is the complete context for a new
session.

**Last updated 2026-07-24**, after the F2 08-07 run. If you are reading this and
the newest directory in `runs/` is later than `F2_08072026`, this document is
stale — trust the run's `report.md` and
`.claude/skills/rossen-beat-extractor/reference/beat_yield.md` over anything here.

---

## 0. Start here — the 60-second version

```bash
# 1. You are probably NOT on the default branch. Check.
git branch --show-current

# 2. Deps are never preinstalled in a fresh container.
pip install -r harvest/requirements.txt
export PYTHONPATH="$(pwd)/harvest"

# 3. pandoc is NOT installed. Use the zipfile fallback in the beat-extractor
#    skill to convert a .docx. Do not waste a turn discovering this.

# 4. Probe the network paths before trusting them. See §4.
```

To run the pipeline on a script: read
`.claude/skills/rossen-pipeline/SKILL.md` and follow it. It is the orchestrator
and it is current. This document is context; that document is the procedure.

---

## 1. What this system does

Jeff Rossen hosts a live consumer-protection show. Every 30 to 40 minute episode
contains beats where Jeff reacts to a clip pulled from YouTube, TikTok,
Instagram, Facebook, or Reddit. Clips are usually unpolished: a local news
affiliate interviewing a scam victim, someone ranting in their car, doorbell cam
footage, a screen recording of a scam text.

Finding those clips was manual. A producer read the script, guessed search terms,
searched four platforms, watched candidates, found in and out points, logged
sources, and handed the result to edit. Searching and timestamping consumed all
the time.

**This system automates the finding and the timecoding.** Script in, a picks
manifest plus a filled Bible `.docx` out. A human reviews; Claude makes the
initial pick.

### The core insight the design rests on

The hard part is not video processing. It is vocabulary mismatch.

A script says *romance scam targeting seniors through Facebook Messenger*. The
clip that works on air is someone crying in their car saying *my mom sent forty
thousand dollars to a guy who said he was deployed overseas*. Those share almost
no words. Search the script's language and you get PSAs. Search the victim's
language and you get the clip that airs.

### Optimization target

**Recall, not precision, at harvest.** Thirty scannable candidates per beat, not
the correct four. Precision comes later from the grader, which has more
information. The expensive layer (transcripts) is reserved for the handful that
survive triage.

---

## 2. Current state

### Built and working

| Component | Status |
|---|---|
| `rossen_harvest` search | **Working.** Three surfaces: YouTube long-form, YouTube Shorts, Brave (web + video). Dedupes across all. SQLite cache, 2-week TTL |
| `transcripts.py` | **Working.** Caption fetch via yt-dlp, no media download. `fetch_many` takes **bare video IDs**, not URLs |
| `vertical_transcribe.py` | Built, **never successfully run** — needs media bytes, which are blocked here. See §4 |
| `dedupe.py` | Working. Fuzzy title match within platform, keeps earliest upload |
| 4 skills in `.claude/skills/` | All exercised across three real runs |
| `rossen-script-writer` | In repo as of 2026-07-24; previously account-only |
| Test suite | **128 pass.** Plain scripts, not pytest — run `python3 harvest/tests/<f>.py` |

`python3 -m rossen_harvest --help` lists exactly two subcommands: `harvest`
(alias `search`) and `eval`. Nothing else exists.

### Not built — do not claim otherwise

| Component | Notes |
|---|---|
| **Download-and-cut** | **There is no `clip` subcommand.** No code downloads video or trims it. Step 7 is a hand-written manifest, a handoff to the edit bay. Never say clips were pulled or cut |
| FCPXML export | No writer exists |
| Airtable push | Schema decided (§5), never built |
| PySceneDetect timecode snap | Not built. Timecodes come from caption cue boundaries, padded |
| Authenticated social scraper | The remaining real gap. Brave cannot reliably surface a native TikTok/IG post for a generic query |
| `clearance-triage`, `pull-sheet-writer`, `post-mortem-analyzer` skills | Never built |

### Runs completed

`runs/F2_07292026`, `runs/F2_08052026`, `runs/F2_08072026`. Each carries
`beats.json`, `candidates.json`, `shortlist.json`, `picks.json`,
`clips/manifest.json`, `report.md`, and a filled Bible `.docx`. Read the newest
`report.md` for what actually happened most recently.

---

## 3. Branches — read before committing

Work has been happening on feature branches, **not** the default branch.
`claude/rossen-pipeline-script-hcflp6` carried the 08-05 and 08-07 work and is
currently furthest ahead. `claude/rossen-pipeline-run-id57xe` is kept
fast-forwarded to match.

Confirm with `git log --oneline -5` and `git branch -r` before assuming. If the
branch you were assigned has an already-merged PR, start fresh from the default
branch rather than stacking on merged history.

---

## 4. Environment realities — verify, do not assume

This is the section that saves the most time, and every item was learned the
hard way.

**`pandoc` is not installed.** The beat-extractor skill has a `zipfile` +
`ElementTree` fallback for `.docx`. Use it directly.

**Deps are not preinstalled and no pip cache carries over.** Run
`pip install -r harvest/requirements.txt` every fresh session. `ffmpeg` is a
system binary and *is* present — check separately, it is not pip-installable.

**`export PYTHONPATH="$(pwd)/harvest"`** or `import rossen_harvest` fails.

**Network paths fail independently, and the preflight's import checks prove
nothing about them.** Measured 2026-07-24:

| Path | State |
|---|---|
| YouTube search (`--flat-playlist`) | ✅ works |
| YouTube captions (per-video page) | ✅ works — but throttles easily, see below |
| YouTube **media bytes** (incl. `-f bestaudio`) | ❌ blocked |
| Direct YouTube page fetch (WebFetch) | ❌ bot-walled, redirects to `/sorry` |
| TikTok | ❌ "Your IP address is blocked" |
| Brave API | ✅ HTTP 200 — but test the key, presence ≠ authorization |

**The throttle-vs-block trap.** Rate limiting and a real block return the
*identical* "Sign in to confirm you're not a bot" string. In this run a rapid
diagnostic burst — a dozen `--list-subs` calls in two minutes, several looping
over player clients — drove captions to **0 of 6** on IDs a prior run had
captioned fine. It looked exactly like a hard IP block. Twenty minutes later the
normal `fetch_many` path returned **11 of 12**. Nothing was fixed; the burst had
tripped a limiter.

So: probe **once** per path, never in a loop, never iterate
`player_client` as a first move (that iteration is what trips it). If a probe
fails, wait several minutes and retry through the real code path before
concluding anything. Calling a throttle a block costs a whole run — it converts
every pick to an unverified outcue and pushes the producer toward a degraded
deliverable they never needed to accept.

**Whisper's reach equals your media access, and no wider.** It transcribes bytes
something else must fetch. With YouTube media and TikTok both blocked,
`vertical_transcribe.py` has zero reachable sources and should not be planned
around. It is correct code that this environment cannot exercise.

---

## 5. Decisions already made — do not relitigate

**Script is always upstream and finalized.** Clips never drive the script. Never
infer that a clip existed first.

**Orientation is a hard constraint, not a hint.** Producer-authored, and
predicted the platform correctly in 26 of 26 observed cases. Horizontal beats
never search TikTok. **One deliberate exception:** a YouTube Short surfaced
against a horizontal beat carries `surfaced_for: horizontal` and is scored, not
auto-failed — the framing question goes to a human. Shorts run on *both*
orientations.

**No city in the news register.** Affiliates carry national wire packages, so the
affiliate that surfaces is usually nowhere near the event. Search the story, not
the location.

**Four registers.** news, victim, platform, anchor. Anchor is the literal proper
nouns and is the highest-hit-rate single query on dated-event beats.

**Seven clip roles.** `victim_interview`, `confrontation_bust`, `evidence`,
`explainer_demo` (splitting `creator_short` / `creator_long`), `authority_report`,
`debunk`, `first_person_rant`.

**A candidate can have many segments.** Four of 24 aired beats were butt-cuts
pulling 2–3 slices from one source. A `BUTT` marker in the script means the
segments above and below come from the **same source** — prefer one source cut
twice over two sources.

**The outcue is the verification anchor, and it is never invented.** Every
proposed segment carries a verbatim transcript quote from the out point, verified
with `Transcript.find()` — not by eye. If you cannot find the phrase, your
timecode is wrong. If no transcript is reachable, ship the pick with **no**
outcue and flag it unverified. An honest gap beats a fabricated quote.

**Timecode arithmetic happens in code, never in the model.** Report the
timestamps the transcript gives you.

**Airtable schema (unbuilt but decided).** Beats and Candidates tables, linked.
Thumbnail as attachment passed by URL. Gallery grouped by beat, sorted by score.
Status: New / Flagged / Rejected / Approved.

---

## 6. What is measured vs. what is assumed

Be honest about this distinction. It determines what to trust.

### Measured from 24 aired segments across 3 episodes

| Finding | Value |
|---|---|
| Aired segment length | median 67s, IQR 50–95s, range 10–161s |
| Total airtime per beat | median 88s |
| First in-point, horizontal | median 34s (anchor toss + standup always cut) |
| First in-point, vertical | median 0s (hook is front-loaded) |
| Orientation → platform accuracy | 26 of 26 |

The horizontal in-point finding is counterintuitive and worth internalizing: a
candidate whose first 30 seconds are generic is a normally structured news
package, not a weak clip.

### Measured from one recall@30 eval (horizontal/YouTube, n=8 testable)

**recall@30 = 0.889.** Median best-rank 1.

| register | found it | found it first | uniquely found it |
|---|---|---|---|
| platform | 8 | 2 | **1** |
| news | 6 | 4 | 0 |
| anchor | 5 | 2 | 0 |
| victim | **0** | 0 | 0 |

`platform` is the workhorse even on YouTube. `victim` contributed **nothing** on
horizontal/YouTube — but it was theorized to matter on vertical, which this eval
never tested. Treat it as unproven, not disproven.

### Measured across three pipeline runs

**Vertical `evidence` beats have yielded nothing in 4 of 4 attempts.** This is
the strongest structural finding in the system and it argues for catching those
beats at extraction rather than after a full search. Neither of the two
previously-split yield logs showed this alone — it only appeared on merging them.

### Assumed, never validated

- **The per-role register weighting table.** Inferred from 26 rows. Most likely
  thing to be wrong.
- **The tone section of the clip grader.** Written from reading three scripts.
  Asserts the show is sympathetic to victims and never sneering, with a hard rule
  against scambaiting that mocks the caller. If Jeff's real register is more
  aggressive toward scammers, this produces quietly wrong picks rather than
  obviously wrong ones. **Worth confirming with the user.**
- **The glossary.** Starter entries. Update it from every post-mortem.

---

## 7. Skills: the repo is the source of truth

The five Rossen skills exist in **two** places and they drift:

- `.claude/skills/` in this repo — **canonical**. Version history, diffs, commit
  messages explaining the measurement behind each change.
- The user's Claude account — a **deployment target**. Skills sync down into a
  session (account IDs in `~/.claude/skills/manifest.json`). No history, no diff,
  no way to tell which of two copies is newer.

As of 2026-07-24 the account copies had drifted *behind* the repo and carried
**no `reference/` folders at all** — while three skills instruct the reader to
read `reference/aired_examples.md` or `reference/glossary.md`. A skill pointing at
a missing file degrades silently: the model proceeds uncalibrated rather than
erroring.

Edit here, commit, rebuild `dist/skills/*.zip` (script in
`dist/skills/README.md`), re-upload. **Never edit in the account and expect it to
come back.**

### The yield log has exactly one canonical path

```
.claude/skills/rossen-beat-extractor/reference/beat_yield.md
```

Append there and nowhere else. A bare `reference/beat_yield.md` used to resolve
to a second file at the repo root; three runs appended to that one while the copy
shipping with the skill sat an episode behind, and the two drifted into
incompatible schemas with zero overlapping episodes. They are now merged, the old
path holds a pointer stub, and `rossen-pipeline` Step 9 documents the full path.
Do not restart that split.

---

## 8. Open items, in rough priority order

**1. The Shorts fix is unexercised against a live vertical beat.** Vertical beats
previously never reached the YouTube backend at all, so their `shorts` register
ran nowhere. Fixed 2026-07-24 with `ShortsBackend`, and it contributed 56
candidates — but only against *horizontal* beats, because 08-07's single vertical
beat went show-produced. The next script with a live vertical beat should confirm
it end to end.

**2. `victim` register is untested on vertical.** It scored zero on
horizontal/YouTube. Vertical is where it was theorized to matter. An eval there
would either justify its query budget or free it up.

**3. The diversity floor promoted a loser twice in one run** (b01 GeekSpin over
News4JAX; b04 Duluth PD over NBC10). Per the grader skill, if that repeats across
episodes the upstream hard filters need a look, not the floor. Watch it.

**4. Native social posts remain unreachable.** Brave finds the press coverage that
*points at* a named person's own post, which is the self-recorded workflow, but it
will not reliably surface a native TikTok/IG post for a generic query. Closing
this needs an authenticated scraper. Deliberately last: ~30% of volume and 100%
of the fragility.

**5. F2 08-07 b04 vintage is unconfirmed.** The CBS clip is an exact case match
but the script flags it as a 2024 package and the page exposed no publication
date.

---

## 9. Working style

**Diagnose before repairing.** Zero candidates for a beat is a query problem, not
a search problem. Re-query before concluding a case is unsourceable — and when
you do conclude it, say which queries you ran.

**Stop at the checkpoints.** After beats and queries, before search. Before any
repair proposal touches the script. A case swap changes what Jeff says on air;
that is the producer's call, never a silent fix.

**An honest gap beats a bad pick.** A wrong flagged clip gets discovered in the
edit bay, which costs more than an empty beat discovered at the contact sheet.
`SHOW-PRODUCED` is not a failure and must never be logged as `EMPTY` — a beat
correctly identified as unsourceable *before* search ran is the sourcability scan
working.

**Say what actually happened.** No clips are downloaded or cut by this pipeline.
Report per-platform counts as printed. If a stage runs long, say so. If you were
wrong earlier in the session, correct it plainly and move on — one run here
misdiagnosed a throttle as a block, and saying so was more useful than defending
it.

**Run the tests.** 128 pass. They are plain scripts, run individually:

```bash
for t in harvest/tests/*.py; do python3 "$t"; done
```

Do **not** reach for pytest. It collects zero tests (there are no `test_`
functions — each file is a script with a `check()` helper) and dies with
`caught unexpected SystemExit` on the module-level `sys.exit`. A green pytest run
here would mean nothing ran.
