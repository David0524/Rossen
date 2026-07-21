# Rossen Reports clip discovery system — handoff

You are picking up a partially built system. This document is the complete context. Read it fully before doing anything.

---

## 1. What this system does

Jeff Rossen hosts a live consumer-protection show. Every 30 to 40 minute episode contains 10 to 12 beats where Jeff reacts to a clip pulled from YouTube, TikTok, Instagram, Facebook, or Reddit. Clips are usually unpolished: a local news affiliate interviewing a scam victim, someone ranting in their car, doorbell cam footage, a screen recording of a scam text.

Finding those clips was manual. A producer read the script, guessed search terms, searched four platforms, watched candidates, found in and out points, logged sources, and handed the result to edit. Searching and timestamping consumed all the time.

**This system automates that.** Script in, flagged clips with in and out points out.

Going forward the show scripts arrive with clip placeholders and no clips. The system fills them. A human reviews, but Claude makes the initial pick.

### The core insight the design rests on

The hard part is not video processing. It is vocabulary mismatch.

A script says *romance scam targeting seniors through Facebook Messenger*. The clip that works on air is someone crying in their car saying *my mom sent forty thousand dollars to a guy who said he was deployed overseas*. Those share almost no words. Search the script's language and you get PSAs and explainers. Search the victim's language and you get the clip that airs.

So the system generates queries in the register real people use, not editorial register.

### Optimization target

**Recall, not precision, at the harvest stage.** Thirty scannable candidates per beat, not the correct four. Precision is applied later by the grader, which has more information.

No vision model culling of the funnel. No frame-level watching of every candidate. The expensive layer is reserved for the handful of clips that survive triage.

---

## 2. Current state

### Built and working

| Component | Status |
|---|---|
| `rossen-beat-extractor` skill | Built, not yet validated on a live script |
| `rossen-query-generator` skill | Built, **never measured** — see §6 |
| `rossen-clip-grader` skill | Built, not yet validated |
| `parse_beats.py` | Working. Extracts beat/clip pairs from past scripts |
| `beats.json` | 26 clip rows across 24 beats from 3 episodes. Ground truth |
| `rossen_eval_worksheet.csv` | Eval scaffold, one column unfilled |

### Not built

| Component | Notes |
|---|---|
| YouTube harvest | yt-dlp → SQLite → Airtable. **Build this next** |
| Airtable push | Schema decided, see §5 |
| Timecode extraction pipeline | Download, Whisper, PySceneDetect, write back |
| Web search leg | Needed for `authority_report` beats, see §7 |
| `clearance-triage` skill | Sorts flagged clips into fair use / needs permission / licensed / hard no |
| `pull-sheet-writer` skill | Approved set out to edit's document format |
| `post-mortem-analyzer` skill | Aired episode + candidate pool in, eval set out |

---

## 3. Install

```bash
mkdir -p ~/rossen-clips/.claude/skills
cd ~/rossen-clips
# copy the three skill folders into .claude/skills/
# copy parse_beats.py, beats.json, rossen_eval_worksheet.csv into the repo root
```

Resulting layout:

```
~/rossen-clips/
├── .claude/skills/
│   ├── rossen-beat-extractor/
│   │   ├── SKILL.md
│   │   └── reference/aired_examples.md
│   ├── rossen-query-generator/
│   │   ├── SKILL.md
│   │   └── reference/glossary.md
│   └── rossen-clip-grader/
│       └── SKILL.md
├── parse_beats.py
├── beats.json
└── rossen_eval_worksheet.csv
```

Skills are filesystem-based in Claude Code; no upload step. Project skills load from `.claude/skills/` in the starting directory and every parent up to the repo root, so start Claude Code from `~/rossen-clips`.

**Restart Claude Code once after creating a brand-new top-level skills directory** — it needs a restart before it watches the folder. After that, edits to any `SKILL.md` take effect inside a running session.

Verify: `ls .claude/skills/*/SKILL.md` should list three files.

### Dependencies

```bash
brew install ffmpeg
python3 -m venv .venv && source .venv/bin/activate
pip install yt-dlp pyairtable faster-whisper scenedetect pillow anthropic opentimelineio
```

Playwright and stealth patching are deliberately deferred. Scraped platforms are the most fragile piece and the smallest share of volume.

---

## 4. The pipeline

```
finalized script (.docx, clip placeholders empty)
  │
  ├─ 1. BEAT EXTRACTOR (skill)
  │     → beat records: role, orientation, visual_spec, news_anchor, priority
  │
  ├─ 2. QUERY GENERATOR (skill)
  │     → 4 registers × 6-10 queries, platform-tagged
  │
  ├─ 3. HARVEST (code, NOT BUILT)
  │     yt-dlp --flat-playlist --dump-json "ytsearch30:{query}"
  │     → metadata + thumbnail only, no video bytes
  │     → normalize, dedupe, cache to SQLite, push to Airtable
  │
  ├─ 4a. CLIP GRADER pass 1 (skill)
  │     metadata triage, 30 → 5
  │
  ├─ 4b. download + Whisper transcribe the 5 (code, NOT BUILT)
  │
  ├─ 4c. CLIP GRADER pass 2 (skill)
  │     tone/authenticity/quality/fit → flag one, propose in/out + outcue
  │
  ├─ 5. TIMECODE SNAP (code, NOT BUILT)
  │     PySceneDetect shot boundaries, snap in/out in CODE not in the model
  │
  └─ 6. write back to Airtable → export FCPXML/EDL via opentimelineio
```

**Note the transcription moved.** The original design transcribed only after a human flagged a clip. Because Claude now does the flagging, transcription happens on the top five *before* the flag decision. Consequence: the timecode extractor no longer needs to transcribe, the transcript already exists. Do not build it twice.

---

## 5. Decisions already made — do not relitigate

**Script is always upstream and finalized.** Clips never drive the script. Never infer that a clip existed first.

**Orientation is a hard constraint, not a hint.** Scripts mark `(((PLAY CLIP XXX HORIZONTAL)))` or `VERTICAL`. This is producer-authored and predicted the platform correctly in 26 of 26 observed cases. Horizontal resolved to YouTube or a news site every time. Vertical resolved to TikTok or Facebook every time. Horizontal beats never search TikTok.

**No city in the news register.** Affiliates carry national wire packages, so the affiliate that surfaces is usually nowhere near the event. The first aired clip in the sample is an `everythinglubbock.com` URL about a Southern California couple. Search the story, not the location.

**Four registers, not three.** News, victim, platform, plus an **anchor** register added during build: the literal proper nouns from the beat. `Temu $232 million fine`. `Maryland dynamic pricing ban`. Several beats exist only because a dated event happened, and one anchor query almost certainly outperforms any amount of victim-register phrasing on those.

**Seven clip roles, not four.** The original taxonomy was `rant / victim_interview / evidence / explainer_demo`. Tagging the real data added three: `confrontation_bust` (Rossen loves the bust; at least 5 of 26), `authority_report` (network/wire coverage of a development), and `debunk` (viral claim disproven; inverted search). `explainer_demo` also splits into `creator_short` (vertical, 15-60s) and `creator_long` (horizontal, multi-minute) because they share no platform or query syntax.

**Airtable schema.** Two tables minimum, Beats and Candidates, linked. Thumbnail as an attachment field passed as a URL so Airtable hosts it. Gallery view grouped by beat, sorted by score. Status single select: New / Flagged / Rejected / Approved.

**A candidate can have many segments.** Four of 24 aired beats were butt-cuts pulling 2 to 3 slices from one source. The Airtable schema and the FCPXML export both need one-to-many between candidate and timecode. This is normal, not an edge case.

**Timecode arithmetic happens in code, never in the model.** The grader reports transcript timestamps; PySceneDetect snaps them to shot boundaries so clips do not start mid-shot.

**The outcue is the verification anchor.** Every proposed segment carries a verbatim transcript quote from the out point. A correct out point is one where that phrase appears in the Whisper transcript within about a second of the proposed timestamp. This is the show's own convention — past scripts write `:38-2:01 (THIS IS WHAT THE SCAMMERS DID)` — so there are 24 worked examples to calibrate against.

---

## 6. What is measured vs. what is assumed

Be honest about this distinction. It determines what to trust.

### Measured from 24 aired segments across 3 episodes

| Finding | Value |
|---|---|
| Aired segment length | median 67s, IQR 50–95s, range 10–161s |
| Total airtime per beat | median 88s, range 26–166s |
| First in-point, horizontal | median 34s |
| First in-point, vertical | median 0s |
| Orientation → platform accuracy | 26 of 26 |
| Source mix | roughly 70% YouTube/news, 30% social |

The in-point finding is counterintuitive and worth internalizing: news packages open with an anchor toss and reporter standup that gets cut every time, so the usable material starts about half a minute in. A horizontal candidate whose first 30 seconds are generic is a normally structured news package, not a weak clip. Intuition says the opposite.

### Assumed, never validated

- **Every query in the query generator.** The registers are structurally sound and the vocabulary is drawn from real scripts, but not one query has been run against a live search engine. The build environment had no network access to YouTube.
- **The per-role register weighting table** in the query generator. Inferred from 26 rows. Most likely thing to be wrong.
- **The tone section of the clip grader.** Written from reading three scripts. It asserts the show is consumer-protective and sympathetic to the victim, never sneering at the person who got scammed, with a hard rule against scambaiting content that mocks the caller. If Jeff's real register is more aggressive toward scammers, this section produces quietly wrong picks rather than obviously wrong ones. **Ask the user to confirm.**
- **The glossary.** Starter entries only. It drifts and needs updating from every post-mortem.

---

## 7. Known gaps

**`authority_report` beats will not surface through `ytsearch30:`.** The Temu fine clip in the sample lived on `today.com`. Network news video often sits on the network's own site, not YouTube. These beats need a web search leg alongside the yt-dlp harvest. Architectural decision still open.

**Vertical platform harvest is unbuilt.** TikTok, Instagram, and Facebook need Playwright with a logged-in persistent context, saved session state, randomized dwell, and possibly a residential proxy. Roughly 30% of volume and 100% of the fragility. Wrap each platform behind a common interface so a broken scraper returns zero results instead of crashing the run. Deliberately last.

**Duplicate wire packages within YouTube.** The same affiliate package appears on dozens of Nexstar and Sinclair channels with near-identical titles. This is a *within-platform* collision, so cross-platform fuzzy title matching will not catch it. Dedupe by fuzzy title inside YouTube and keep the earliest upload date, which is usually the originating station and matters for clearance.

**yt-dlp rate limiting.** 30 results × 4 registers × 24 beats is a lot of requests. Cap concurrency around 5 and cache to SQLite keyed on query string — the eval will be re-run many times while tuning and there is no reason to re-hit YouTube for a scored query.

---

## 8. First tasks, in order

### Task 1 — Measure the query generator

This is the highest-value unblocked work. Nothing downstream should be trusted until it is done.

For each row in `rossen_eval_worksheet.csv`, read `.claude/skills/rossen-query-generator/SKILL.md`, generate queries in all four registers, run each through:

```bash
yt-dlp --flat-playlist --dump-json "ytsearch30:{query}"
```

Check whether the video ID in the `url` column appears in the results. Write back which register hit, at what rank, and on which exact query string. Report hit rate by register and by clip role.

About 18 of 26 rows are YouTube and resolvable this way. The 8 vertical rows need manual searching by the user.

**Interpretation:** above 70% hit rate, the query generator is good enough to build the harvest on. Below 50%, fix the glossary first. Whatever the number, the per-register breakdown replaces the assumed weighting table with measured weights.

### Task 2 — Build the YouTube harvest

yt-dlp → normalize to a common Candidate shape → dedupe → SQLite cache → Airtable push.

Candidate shape: `platform, url, title, thumbnail_url, duration, published, views, uploader, query_that_found_it, register, beat_id`.

### Task 3 — Wire the grader

Pass one on harvested metadata, download and transcribe the top five, pass two, write flag and proposed segments back to Airtable.

### Task 4 — Timecode snap and export

PySceneDetect boundaries, snap in code, export FCPXML or EDL with opentimelineio so the editor imports timecodes instead of retyping them.

### Then

`post-mortem-analyzer` is the highest-leverage remaining skill: it turns each aired episode into eval data that tunes the grader's weights and the query generator's registers. `clearance-triage` may be more urgent depending on how legal review currently works — ask.

---

## 9. Working style

The user is direct and technically capable. Match it.

- No sugar coating. Say what is broken.
- Distinguish measured from assumed, every time. The value of this system is that its parameters came from real data, and that value evaporates the moment inference gets presented as measurement.
- Do not relitigate §5.
- When something cannot be validated in the current environment, say so plainly rather than shipping unearned confidence.
- Avoid the term "cross-functional." Avoid em dashes.
