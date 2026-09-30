---
name: "rossen-story-outline"
description: Build the Outline w/ Videos for a Jeff Rossen (Rossen Reports) show — the plain-English, beat-by-beat map of every story with each beat's clip already found, graded and linked — after Jeff says yes to the pre-bible pitch email and before anyone writes the bible. Two phases, one document - beats from the approved pre-bible, then the clip pipeline (beat extraction, queries, search, grading) run on those beats, with the picks written back into the outline. Use whenever the user asks for an outline, story outline, outline with videos, beat sheet, "find the clips for the outline," "show me the story and the clips before you write it," "lay out the show," or Jeff has approved the pitches and the next step is the bible. Also use to re-order, cut or revise beats, or swap a clip, in an existing outline. Do NOT use to pitch stories (rossen-pre-bible) or write the teleprompter script (rossen-script-writer).
---

# Rossen Outline w/ Videos

## Where this sits

pre-bible → pre-bible email → **outline w/ videos** → bible → bible review

The pre-bible decides *which* stories and Jeff approves them by email. The bible is
written for Jeff's teleprompter and is hard to read as a story. The outline is the
step in between: **the show as a narrative, with the footage for every beat already
found, readable in a few minutes, before a single teleprompter line exists.** The
room approves shape and clips together, where moving a beat or swapping a clip
costs one row instead of a rewrite.

Clip search, grading and verified timecodes happen **here**, not after the bible.
The bible is written from the filled outline and never goes back through the pipeline.

| File | Load when |
|---|---|
| `templates/outline.md` | Every run. The skeleton to fill. |
| `references/example_0925.md` | Phase 1. The beats register and format. |
| `references/example_1007_videos.md` | Phase 2. A real Videos table from a real run. |
| `scripts/check_outline.py` | **Before every build.** `--stage beats` after Phase 1, `--stage videos` after Phase 2. |
| `scripts/build_outline.py` | Rendering the `.docx`. |
| `references/producer-kit/amanda-assignment.md` + `references/examples/amanda-assignment-2026-09-20-F1-phone.md` | When the bible goes to Amanda instead of `rossen-script-writer`: the assignment email. |
| `references/producer-kit/other-formats.md` | The seven-beat bible assignment, meeting recap, guest-prep agenda, deals talking points, call-in producer brief. |
| `references/examples/rundown-2026-09-18-F2-car-show.md` | A proposed A-to-E rundown with dated links, the shape the team vets. |

## Inputs

The outline is built **from the approved pre-bible** — the stories Jeff said yes to
in the pitch email — before any bible exists. Never draft the bible first and
outline it after.

What carries over from each approved pre-bible page:

| Pre-bible | Outline |
|---|---|
| THE HOOK, HOW IT WORKS | The beats, in order |
| Named people in the hook and sources | Who |
| FOOTAGE WE NEED / BE HONEST ABOUT THIS | Clip tags (`HAVE` = a URL is already in the pre-bible) |
| THE PAYOFF | The fix |
| NEEDS VERIFICATION, flagged lines | Gaps and Decisions |
| Slot, confidence | Running order and weight |

**Keep the pre-bible to hand through Phase 2.** Its names, handles, figures, places
and dates are what the clip search runs on; the outline row alone is too thin.

If a beat needs a person or clip the pre-bible doesn't have, write the gap — don't
research-and-invent to fill the row. Confirm before laying anything out:

1. **Airdate and day of week** — compute the day; don't trust the label.
2. **Story count.** Wednesday default is **one A story + one small B story.** Three to
   five stories and single-topic umbrella shows are real variants. **Ask** if not stated.
3. **Guest**, if any (expert on a content story; deals guest on Friday).

Sponsor is **OmniWatch**. Don't ask. Two breaks in one Wednesday is normal.

## What the outline is — and is not

It is **written for reading, not for Jeff's mouth.**

- **Sentence case, plain prose.** No ALL CAPS body, no dash lines, no `(((PLAY CLIP)))`
  markers, no `OUT:`, no tease copy. Timecodes live only in the Videos tables.
- **One row per beat.** A beat is one turn in the story — the moment the viewer
  learns something new or meets someone new. Each beat becomes one mid-story header
  in the bible, so the outline's beat order *is* the bible's structure.
- **"What happens" is one sentence, ≤25 words.** If it needs two, it's two beats.

# Phase 1 — Beats

## The beat table

`| # | Beat | Who | What happens | Clip |`

**Beat** — two to five words naming the turn: *The call*, *It gets worse*, *The fix*.

**Who** — the human at the center of that beat, by identity: *Massachusetts woman,
new-phone owner*; *Utah man, never ordered a phone*; *Jim Stickley, ethical hacker*.
`You (the viewer)` is fine for the hook and the fix. **This column is where the
people-not-policies rule becomes visible.** A company (*Lowe's*), an institution
(*Texas Attorney General*), a category (*shoppers*, *people posting online*) or a
blank is not a person — the room should see that at a glance. Write the gap
honestly (`Unnamed — need a name`) rather than dressing a category up as a person.

**Clip** — a tag, then optionally a short note:

| Tag | Means | Phase 2 |
|---|---|---|
| `HAVE · VERTICAL` / `HAVE · HORIZONTAL` | A candidate URL is already in the pre-bible. **Not watched.** | Verified, graded, or routed to the manual lane |
| `FIND · VERTICAL` / `FIND · HORIZONTAL` | The pipeline has to search for it. | Searched and graded |
| `DEMO` | Team records a phone/screen demo as video. | Not searched — show-produced |
| `GUEST` | Live guest carries the beat. | — |
| `JEFF` | Jeff on camera, no roll. Normal for hooks, turns and fixes. | — |
| `STILLS` | Screenshots/pop-ups. **The show wants video.** A story leaning on stills is salvage, not a pitch — flag it in Decisions. | — |

Add `BROLL` after the orientation for mute footage Jeff talks over
(`FIND · VERTICAL BROLL`) — it sources differently.

**Orientation is a hard constraint.** The pipeline will not search the other kind,
so author it deliberately: a victim telling a reporter is `HORIZONTAL` (YouTube,
network, affiliate); someone talking to their own phone, a doorbell or security cam,
or a screen recording is `VERTICAL` (TikTok, Reels, Facebook).

Never invent a clip to fill a slot. A B story with zero clip beats is normal.

## Per story, around the table

- **In one sentence** — the whole story, start to end, as you'd tell a friend.
- **Peg** — why it's on *this* show. Old footage is fine; an old peg is not.
- **Weight** — share of the show, and clip-beat count. The A story takes most of both;
  every story after gets lighter.
- **Beat table.**
- **Videos** — Phase 2 fills it. Leave the heading out until then.
- **The fix** — the protection steps, one line each, plain.
- **Gaps** — only what's missing or unconfirmed *that changes the story's shape*:
  an unnamed victim, a clip that may not exist, the sexiest line resting on one
  source. ⚠️ at the point of use. Full sourcing stays in the pre-bible's source block;
  don't recopy it.

## Page one: the show at a glance

- **Running order** table: `| Slot | What | Weight | Clips |` — tease, each story,
  each sponsor break (OmniWatch unless the assignment says otherwise) after the
  victim's story and never on a cliffhanger, guest entrances, deals, end. After Phase 2, `Clips` reads `found/needed` (`3/4`).
- **The show in three sentences.**
- **The ride** — one line on where tension builds and where it lets go. Grim is
  allowed when it's the story; unbroken dread is not. No mandatory good-news
  closer, but if the show never exhales, say so.
- **Decisions before we write** — the rulings the room owes before drafting: which
  story leads, a missing name, a stills-heavy beat, a line that needs legal, and
  after Phase 2 every `EMPTY`, `WEAK` or orientation-crossed clip. Not a summary.
  If there are none, write "None."

Friday: outline the content block fully. The deals half is one row in the running
order (`Deals — [guest], live requests`) — no deal list here, and no clip beats.
Name the deals guest (Trey Donovan or Derek Couture) once it's confirmed.

A live scam show's beats follow the Ghost Tapping order: mechanics, victim clip,
expert, escalation, sponsor, scale beat, practical close; then B, C, and four
expert questions. A call-in F2 outlines two callers plus the expert; callers by
caller ID in the outline, first names only on air.

Clips: Matt's standard is about two outside clips per segment, freshest first,
each with its upload date and length, video links rather than news-site pages.
When a story wants more, say so in Decisions.

**Header line** carries `**Stage:** beats` until Phase 2 lands, then `**Stage:** videos`.

Check: `python3 scripts/check_outline.py outline.md --stage beats`. The beat table
is the pipeline's Checkpoint 1 — the room can move, cut or re-orient beats here,
before any search budget is spent. If the user says to run straight through, run
straight through.

# Phase 2 — Videos

Runs `rossen-pipeline` on the outline. **Needs Claude Code with the `rossen_harvest`
package** — search, captions and Whisper don't run in claude.ai chat. In chat,
finish Phase 1, deliver the beats outline, and say Phase 2 runs in Claude Code.

1. **Beats.** `rossen-beat-extractor`, outline mode: one beat record per `HAVE` /
   `FIND` row. `beat_id` is `MM-DD-<story><row>` — `10-07-A5` is story A, beat row 5 —
   so every pick traces back to its row. `DEMO`, `GUEST`, `JEFF` and `STILLS` rows are
   not clip beats. `script_text` is the row's Who and What happens **plus that beat's
   specifics from the pre-bible**. A `HAVE` row naming a native TikTok/Reels/X post
   goes to the manual lane: that post is the pick.
2. **Queries, search, grade** — the pipeline's Steps 2–6, with its Checkpoints 1–3.
3. **Write the picks back** into a `### Videos` table under each story's beat table,
   then flip the header to `**Stage:** videos` and update page one.

Full candidate lists, shortlists, queries and grades stay in the pipeline's run
folder (`picks.json`, `report.md`). The outline carries only the pick per beat.

## The Videos table

`| # | Clip | Shows | In–Out | Status |`

- **#** — the beat row number. Every `HAVE`/`FIND` row gets exactly one Videos row.
- **Clip** — `[Outlet or creator — short title](URL)`. Renders as a blue link.
- **Shows** — what the clip shows, from title, description and transcript. One line.
  Never "confirmed on screen": nobody in this pipeline watched it.
- **In–Out** — `0:17–0:51 "now using them to prevent theft"`, outcue verbatim from
  the transcript. Butt cuts: `0:17–0:51 "…" BUTT 1:22–1:37 "…"`. `WHOLE CLIP` when it
  runs start to end. `—` when there's no transcript to read.
- **Status** — the yield-log vocabulary, plus one qualifier:

| Status | Means |
|---|---|
| `PICK` | Found, graded, outcue verified against a transcript. |
| `WEAK` | Flagged but low-scoring or carrying flags. Goes in Decisions. |
| `MANUAL` | The native post is the pick. Link handed over, no invented timecode. |
| `SWAP` | The room approved a different case than the row named. Rewrite the row's Who and What happens to match. |
| `THROTTLED` | Shortlist exists; transcript fetch was blocked. Re-run the pipeline's Step 5. |
| `EMPTY` | Searched, nothing usable. Give the reason. Goes in Decisions: cut the beat, swap the case, or Jeff on camera. |
| `· UNVERIFIED` | Suffix, e.g. `MANUAL · UNVERIFIED`: the outcue never reached a transcript. |

Add `· CROP` when the pick's orientation crosses the row's, and put it in Decisions.

You cannot watch video. Every timecode and outcue comes from a transcript or it
isn't written. A missing clip is a finding, not a gap to paper over — a bad pick
costs more than an honest `EMPTY`, because it's discovered in the edit bay.

Check: `python3 scripts/check_outline.py outline.md --stage videos`.

## Length

Page one plus one page per story, hard page breaks. The Videos table may push a
story onto a second page — that's fine; never cut beats or clips to fit. An A story
runs **5–9 beats**; a B story **2–4**. More than nine means the A story is two
stories, or it isn't shaped yet — say so in Decisions.

## Build

1. Fill `templates/outline.md` → `outline.md`.
2. `python3 scripts/check_outline.py outline.md --stage beats|videos` — fix every
   ERROR, read every WARN.
3. `python3 scripts/build_outline.py outline.md -o "MM_DD_OUTLINE_<SHOW>.docx"`
4. `soffice --headless --convert-to pdf` it, then look at the pages.

Deliver the `.docx`. Revisions land in the file.

## Handing off to Amanda

When the bible is being written by Amanda rather than `rossen-script-writer`,
the handoff is the assignment email (`references/producer-kit/amanda-assignment.md`;
model: the Sep 20 phone-scams assignment). Per story: a headline Jeff will
understand; what happens, in order, in two or three bullets; the frame (the
callback or why it's ours); **what to find** (the victim with a dollar figure,
the demo, the company's response on the record); the close (the viewer advice);
then dated links, freshest clip first. Include our own earlier episodes when
there's a callback, with the timestamp. One guest ask per show, with a fallback;
if someone's already booked and may not fit, say so. Two working titles. For a
live scam show, give the seven beats in Ghost Tapping order
(`other-formats.md`). Copy Jeff and Ryan.

## Handoff to the bible

Once the room approves the outline w/ videos, `rossen-script-writer` writes from
it: **same stories, same order, same beats, same clips.** Each beat row becomes a
bold mid-story header. Each Videos row becomes a numbered clip marker carrying its
URL, in–out ranges and outcue. `JEFF`, `GUEST` and `DEMO` rows become header plus
dash lines. A beat or clip the writer wants to add, cut, move or swap is a change
to the outline first — say which row.
