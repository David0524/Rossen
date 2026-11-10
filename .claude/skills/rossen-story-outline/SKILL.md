---
name: "rossen-story-outline"
description: Build the Outline w/ Videos for a Jeff Rossen (Rossen Reports) show — the show in air order, beat by beat, with each beat's clip already found, graded, linked and quoted, written for the room to review and edit, plus a Build Sheet that carries what Claude and the clip pipeline need — after Jeff says yes to the pre-bible pitch email and before anyone writes the bible. Two phases, one document - beats from the approved pre-bible, then the clip pipeline (beat extraction, queries, search, grading) run on those beats, with the picks written back into the outline. Use whenever the user asks for an outline, story outline, outline with videos, beat sheet, "find the clips for the outline," "show me the story and the clips before you write it," "lay out the show," or Jeff has approved the pitches and the next step is the bible. Also use to re-order, cut or revise beats, or swap a clip, in an existing outline. Do NOT use to pitch stories (rossen-pre-bible) or write the teleprompter script (rossen-script-writer).
---

# Rossen Outline w/ Videos

## Where this sits

pre-bible → pre-bible email → **outline w/ videos** → bible → bible review

The pre-bible decides *which* stories and Jeff approves them by email. The bible is
written for Jeff's teleprompter. The outline is the step in between: **the show in
air order, with the footage for every beat already found and quoted, readable and
editable by the room in a few minutes, before a single teleprompter line exists.**
The room approves shape and clips together, where moving a beat or swapping a clip
costs one block instead of a rewrite.

Clip search, grading and verified timecodes happen **here**, not after the bible.
The bible is written from the approved outline and never goes back through the
pipeline.

## One document, two readers (v3, producer, 11/10/2026)

The outline had two jobs pulling against each other. TJ's 11/11 outline read like
the show and was easy to review and edit by hand, but it dropped what the story and
the pipeline depend on: case dates, clip status, the hold-back line, sources. Ours
carried all of that in tables that machines read well and people don't. So the
outline is now **one document with two layers**:

| Layer | Who it's for | What it is |
|---|---|---|
| **The outline** (front) | The room: producer, TJ, Jeff | The show top to bottom in air order. On-air headlines, talking points, each clip where it plays with its timecodes and soundbite, the break, the protection steps, the close. No tables. A beat is one block; moving a beat is cut and paste. |
| **The Build Sheet** (back, after a page break) | Claude and the pipeline | The story's spine, the beats table (full names, places, dates, tags, what each clip adds, search specifics), Jeff notes, fix sources, open calls. Keyed to the front by beat id and clip number. The room can skip it. |

**The front is the source of truth for the show**: order, headlines, talking points,
which clips, which cuts. When the room edits the front (moves a block, cuts a clip,
rewrites a line), Claude brings the Build Sheet into line before anything else, and
`check_outline.py` fails until the two agree. **The Build Sheet is the source of
truth for the facts** behind the show: who, when, sources.

Both layers are written in plain sentences, with no ⚠️, status words or other
machine markers (producer, 11/10/2026); see the clip notes under *One block per
beat*.

| File | Load when |
|---|---|
| `templates/outline.md` | Every run. The skeleton to fill. |
| `references/example_v3_1111.md` | Every run. The 11/11 outline in v3, including the producer's edits to the protection list. |
| `scripts/check_outline.py` | **Before every build.** `--stage beats` after Phase 1, `--stage videos` after Phase 2. |
| `scripts/build_outline.py` | Rendering the `.docx`. |
| `references/example_0925.md`, `references/example_1007_videos.md` | Old table format (v2). The beat register and the Videos-row reasoning still apply; the layout doesn't. `check_outline.py` still reads v2 outlines. |
| `references/producer-kit/other-formats.md` | The seven-beat bible assignment, meeting recap, guest-prep agenda, deals talking points. |
| `references/examples/rundown-2026-09-18-F2-car-show.md` | A proposed A-to-E rundown with dated links, the shape the team vets. |

## Inputs

The outline is built **from the approved pre-bible**, the stories Jeff said yes to
in the pitch email, before any bible exists. Never draft the bible first and outline
it after.

| Pre-bible | Outline |
|---|---|
| THE HOOK, HOW IT WORKS | The beats, in order (front) |
| Named people in the hook and sources | Who (Build Sheet) |
| FOOTAGE WE NEED / BE HONEST ABOUT THIS | Clip tags (`HAVE` = a URL is already in the pre-bible) |
| THE PAYOFF | The protection steps (front) and their sources (Build Sheet) |
| NEEDS VERIFICATION, flagged lines | Jeff should know and Open calls (Build Sheet) |
| Slot, confidence | The show list and Weight |

**Keep the pre-bible to hand through Phase 2.** Its names, handles, figures, places
and dates are what the clip search runs on; copy the ones each beat needs into its
Build Sheet row (Search specifics).

If a beat needs a person or clip the pre-bible doesn't have, write the gap; don't
research-and-invent to fill it. Confirm before laying anything out:

1. **Airdate and day of week**: compute the day; don't trust the label.
2. **Story count.** Wednesday default is **one A story + one small B story.** Three to
   five stories, one long A, and single-topic umbrella shows are real variants.
   **Ask** if not stated.
3. **Guest**, if any (expert on a content story; deals guest on Friday).

Sponsor: write the break as **a generic ad lead-in** unless the producer names the
spots (producer, 11/4: "two sponsors this week, so we kept the lead-in generic").

# The outline (front)

Written for the room to read and edit. **Sentence case** for everything except the
on-air headlines. No tables, no `(((PLAY CLIP)))` markers, no `OUT:` lines. The
talking points are sayable sentences, close to how Jeff would put it, so the
producer can rewrite a line and the bible writer keeps the edit; they are not the
prompter copy (no caps, no `!!`, no dash bullets).

## Page one

```
# 11/11 WED — <WORKING TITLE>
*Airdate Wed Nov 11, 2026 · tapes Fri Nov 6 · A only · no guest · 1 break · Stage: videos*

## SUMMARY
Three sentences: what happens, why the viewer should care, what they walk away able to do.

## THE SHOW
1. Tease (opens on clip 1: the family's own video of a burglar crawling across the living room)
2. ONE NEIGHBOR FOUND THE BURGLARS' CAMERA… AND POLICE TURNED IT INTO A TRAP (clip 1)
3. …
4. //// Break: generic ad lead-in
5. HERE'S HOW TO PROTECT YOURSELF (clips 7–8)
6. Close
```

- **The header line** ends `Stage: beats` until Phase 2 lands, then `Stage: videos`.
- **THE SHOW** is a numbered list, not a table: every headline in air order with
  its clip numbers, every break, the guest's entrance, the deals handoff on a
  Friday, the close. The first line names the **open package**, the video the
  super tease runs over (usually the A story's strongest real result).
- Nothing else on page one. The story's spine and the open calls live in
  the Build Sheet; open calls also go in the chat reply and the run's `OPEN.md`.

## The tease

`## THE TEASE`, its tag line (`` `A1 · the hook` ``, the hook beat's row in the
Build Sheet), then three to six talking points in air order. It follows the
bible's tease rules so the room reviews the real promise:
- **The first two points grab** (Jeff, 11/11): the most startling moment in the
  open package and what it means for you. No warm-up.
- People are someone the viewer is **going to see** (`You're going to see this
  family's own camera catch…`), never `This family…` (Jeff, 11/11).
- It sells, never tells: nothing past the **Hold back** line. Name the payoff
  promise (`the 30-second walk`) so the body can pay it off by name.
- Evergreen: no holiday, season or relative date (Jeff, 11/11).

## One block per beat

Every beat is one block, in air order. A beat is one turn in the story: the moment
the viewer learns something new or meets someone new. It becomes one headline in
the bible.

```
## ONE NEIGHBOR FOUND THE BURGLARS' CAMERA… AND POLICE TURNED IT INTO A TRAP
`A2 · Braintree, MA · June 2024`

- This family went away on vacation, and burglars broke in.
- Their own indoor camera caught them crawling across the living room.
- Then a neighbor noticed something odd in the bushes across the street.
- So what did the neighbor see?

**CLIP 1 (HORIZONTAL):** [CBS Boston (WBZ) — Crime ring targeted Braintree neighborhood](https://www.youtube.com/watch?v=K-0vvz2MhsE) · Jul 16, 2024 · 2:39
  - **0:31–1:01 ("REALLY, REALLY SHOCKING") // BUTT 1:21–1:32 ("CAMOUFLAGED INTO THE BUSHES")**
  - *Soundbite: "Chilling moments inside a family's home while they're away on vacation…" // "…duct tape around it so that it would be camouflaged into the bushes."*

- **Out:** They got caught because somebody looked… and now the cameras are back.
- **Red flag:** a camera pointed at a house is a crime in progress. Police left it and set a trap.
```

The parts, in order:

1. **Headline** (`## `, ALL CAPS): the on-air header, written the way it will
   appear in the bible. A newspaper headline (Jeff, 11/04): **subject first, a
   plain verdict verb, and the impact on you**. Headlines climb: each is worse,
   closer or bigger than the last. Never open on a state (`IN CALIFORNIA…`) and
   never summarize the plot or give away the payoff.
2. **Beat tag** (one line in backticks): `<beat id> · <place> · <month year>`. An
   old case is dated by a Jeff should know line, not a flag on the tag. Beat
   ids are the story letter plus the beat number (`A2`); they key the block to its
   Build Sheet row. The tag is all the room needs to place the case; the full
   identity lives in the Build Sheet.
3. **Talking points**: three to six bullets, one thought each, 25 words at most.
   The last one before a clip sets up the question the clip answers, never its
   answer. They carry the story, not the search terms (those are in the Build
   Sheet).
   - **People, not policies.** Each point that introduces a person says who they
     are (`this family`, `a man who lives across the street`), never a policy,
     a settlement or a dollar total standing in for a person.
   - **No one-off names** (Jeff, 11/04): `this woman`, not `Sherri`. A person the
     story keeps coming back to may be named; mark them `· character` in the Build
     Sheet.
   - **No outlets** (Jeff, 11/11): not `CBS shows this`. The clip line names the
     outlet; the talking points never do.
   - **Every clip after the first is brought in on an escalator** (Jeff, 11/11):
     the first point of the block moves the story forward (`And now it's
     spreading…`, `But it gets worse…`, `Now they're at your door…`), along the
     Climb. Place and date never open a block.
   - **Evergreen**: no holiday, season or relative date.
4. **The clip** (Phase 2; a placeholder in Phase 1, below):
   - `**CLIP n (ORIENTATION):** [Outlet — short title](URL) · upload date · length`.
     Clips are numbered 1..N in air order across the whole show.
   - Sub-bullet: **in–out in bold**, each segment with its outcue in caps and
     quotes, `//` and `BUTT` between segments: `**0:31–1:01 ("REALLY, REALLY
     SHOCKING") // BUTT 1:21–1:32 ("CAMOUFLAGED INTO THE BUSHES")**`. The times are
     on the copy the link points to (if the transcript came from a different copy,
     re-time it or say so in a `Note:` line).
   - Sub-bullet: `*Soundbite: "…" // "…"*`, verbatim from the transcript, the key
     words of each segment, about 60 words a segment at most, `…` for cuts. This is
     how the room judges a clip without opening it.
   - Sub-bullet, **only when it applies**, one plain sentence on what the editor
     or the producer has to do, under one of three labels:
     - `No times yet: …` when no transcript reached the clip (a manual-lane post,
       or captions and Whisper both blocked). Say why and how to get the times;
       no in–out line, no soundbite, never an invented timecode.
     - `Legal: …` when the window carries an accusation, an unanswered claim, a
       minor or personal data. Give the tighter cut or the blur.
     - `Note: …` for anything else the edit needs: a weak pick, an orientation
       crop, times taken from a different copy than the link.
     A clean clip shows nothing.

   **The outline carries no machine markers** (producer, 11/10/2026): no ⚠️ or
   other emoji, no status words (`PICK`, `WEAK`, `MANUAL`, `THROTTLED`, `EMPTY`,
   `UNVERIFIED`, `LEGAL`, `CROP`) and no Status column. Everything is said in a
   plain sentence the room can read. The pipeline's status vocabulary stays in its
   run folder (`picks.json`, `report.md`) and the run's `OPEN.md`.
5. **Out:** the line Jeff comes back in on: react, then pull forward to the next
   reason to keep watching (Jeff, 11/04). Never a date, a hedge or an attribution.
6. **Red flag:** after each victim case, the takeaway in one plain line, tested
   against the people the scam targets (Ryan, 10/9). The bible says `RED FLAG`
   about once a story; the outline can label every one.

Beats without a clip still get a block: a Jeff-on-camera turn has headline, tag
and talking points only; a guest beat says `**GUEST:** <name, role>` and lists the
questions; a demo says `**DEMO (show-produced):** <what Jeff shows>`.

**Open on a real result (Jeff, 11/04).** The first block after the tease is the
story's most compelling real outcome, ahead of any statistics. In a threat story
that is the case where the money is actually gone; a near-miss lands second
(Ryan, 10/8). In a money-back or how-to story it is the biggest win.

**Every clip adds something (Jeff, 11/04).** Each clip adds evidence, stakes or a
development (written in the Build Sheet's Adds column). Two clips with the same
answer: cut one now and say so in Open calls.

## The break

```
////////////////////
**BREAK** — generic ad lead-in. *Next:* the $60 gadget that can blind your doorbell camera, and the "delivery driver" at your door.
////////////////////
```

After a victim's story and its red flag, never inside a case or on a cliffhanger.
The *Next* names two or three specific payoffs. Two breaks are normal on a long
Wednesday; one is fine.

## HERE'S HOW TO PROTECT YOURSELF

The payoff, in TJ's form (producer, 11/4: the producer replaced ours with his):

```
## HERE'S HOW TO PROTECT YOURSELF
`A8 · the fix`

1. **CHECK YOUR BUSHES… AND YOUR NEIGHBOR'S**
   - Look in bushes, planters and trees, and along fences.
   - Look for anything pointed at your front door or driveway: a small camera or an old phone, a battery pack, tape, fake leaves or fake grass.
2. **FOUND ONE? DON'T TOUCH IT. CALL POLICE.**
   - …
3. **GET A CAMERA THAT KEEPS RECORDING**
   - So what holds up against a jammer? Listen.
   - **CLIP 7 (HORIZONTAL):** [NBC News — …](https://…) · Dec 6, 2025 · 1:34
     - **1:03–1:17 (RECORDS ON AN SD CARD)**
     - *Soundbite: "…"*
   - …
```

- Numbered steps, a bold command, plain sub-bullets in sentence case. **No source
  parentheticals here**: each step's source goes in the Build Sheet (`The fix:
  sources`), keyed by step number.
- A clip that proves a step sits under it, in the same clip form, nested.
- The tease's named promise lands here by name (`the 30-second walk`).
- A step that can be shown (a search, a setting, a statement) is written as a
  `DEMO` line; on a taped F2, offer a graphic or screenshot instead of a live demo.

## The close

`## CLOSE`: share it with someone it protects, the next video, see you next time.

# The Build Sheet (back)

After the close, a page break, then `# BUILD SHEET` and one italic line: *For
Claude and the pipeline. The room can skip this page.* On a multi-story show, the
spine and the beats table repeat per story under `## A`, `## B`.

## Spine

One line each, per story:

- **In one sentence**: the whole story, start to end, as you'd tell a friend.
- **Hold back**: the payoff the tease, the headlines and every *Next* must not
  give away (10/14: "YOUR DAD DIED" and "THE REGISTER IS RINGING UP MORE THAN THE
  SIGN" went out in a tease).
- **Peg**: why this story on this show. It picks the story; the copy stays
  evergreen (Jeff, 11/11). When the peg is news, write the why-now chain: the
  news → the confusion it causes → the scammer's opening, and the line that
  anchors it (Ryan, 10/9).
- **Climb**: the axis the blocks get worse on (closer to you, faster, bigger,
  less you can do). Order the blocks so it climbs; the bible says it out loud
  between clips (Jeff, 11/11).
- **Framing**: the one phrase for how it starts and where, true of every case
  (`a free sample or a crazy discount`, `in a store`, not `at the mall`).
- **Open package**: clip number and what is on screen.
- **Payoff point**: the beat where the method lands, after the real result, the
  stakes and at least one complication (Jeff, 11/04).
- **Weight**: share of the show and clip count.

## Beats

`| Beat | Clip | Who | Tag | Adds | Search specifics |`

One row per front block, same order, same ids.

- **Beat**: the id from the block's tag (`A2`).
- **Clip**: the clip number, or `—`.
- **Who**: the human at the center, by identity, with full name, age, place and
  **when** in parentheses: `Kathryn Taylor, 84, Fernandina Beach FL (June 2025)`.
  Names, towns and dates live here for the room and the source log; the bible
  drops surnames and towns. `You (the viewer)` is fine for the hook and the fix.
  A company, an institution, a category or a blank is not a person: write the
  gap (`Unnamed — need a name`). Add `· character` if the person carries more than
  one beat (the bible may keep the first name).
- **Tag**: `HAVE · HORIZONTAL`, `FIND · VERTICAL`, `FIND · VERTICAL BROLL`, `DEMO`,
  `GUEST`, `JEFF` or `STILLS`.

| Tag | Means | Phase 2 |
|---|---|---|
| `HAVE · <ORIENTATION>` | A candidate URL is already in the pre-bible. Not watched. | Verified, graded, or routed to the manual lane |
| `FIND · <ORIENTATION>` | The pipeline has to search for it. | Searched and graded |
| `DEMO` | The team records a phone or screen demo. | Not searched: show-produced |
| `GUEST` | A live guest carries the beat. | — |
| `JEFF` | Jeff on camera, no roll. | — |
| `STILLS` | Screenshots or pop-ups. The show wants video; a story leaning on stills is salvage. Open call. | — |

  **Orientation is a hard constraint**: the pipeline won't search the other kind.
  A victim telling a reporter is `HORIZONTAL`; someone talking to their own phone,
  a doorbell or security camera, or a screen recording is `VERTICAL`. Never invent
  a clip to fill a slot.
- **Adds**: what the clip adds, in a few words: `evidence: the real result`,
  `stakes: hours, not weeks`, `development: they can blind your camera`.
- **Search specifics**: the names, handles, figures, places, dates, outlets and
  agencies the pipeline searches on, from the pre-bible. Never a specific that is
  in neither document; write `thin` instead.

## Jeff should know

One line per fact, keyed by beat (`A5: all seven are charged; none convicted as of
May`): a nuance that guards a line, the limit of a number, something left out on
purpose and why, who a claim belongs to, a legal status, a case's date. The bible
turns each into a `JEFF PLEASE NOTE` comment on the line it guards. About a dozen
in a Wednesday show; `None.` if none.

## The fix: sources

One line per protection step, keyed by number, each ending with the issuing body's
page in parentheses (`Step 4: hold mail, free, 3 to 30 days (USPS FAQ)`). A step you
couldn't source says `no source yet` and goes in Open calls. Every phone number and URL is checked against the issuer's
own page. Then the **do-nothing test** for any step involving a deadline, an
enrollment, a plan, a dispute window or a default: what happens to the viewer who
does nothing, or only this step? If it leaves them worse off, add the step that
closes it (10/9: "do nothing and you go back to Original Medicare" would have cost
Advantage members their drug coverage).

**Dating.** Every case more than six months before the airdate gets a Jeff
should know line that starts with its date (`A2: June 2024, reported July 2024.`).
The copy stays evergreen; add `Say the year on air.` only when leaving it out would
mislead a viewer, and the bible then says `IN 2024`. There is no Gaps section
(producer, 11/10/2026): a fact the copy must guard is a Jeff should know line; a
thing a person still has to do is an Open call.

## Open calls

The rulings and the work the room owes before the bible is written, each a plain
sentence: which story leads, a missing name, a clip with no times yet, a weak or
risky clip, a beat with no clip found, a stills-heavy beat, a fix step with no
source yet, a single-source claim, the sponsor spots. `None.` if none. Repeat them in the chat reply and the run's
`OPEN.md`: the producer reads those, not the back page.

# Phase 1 — Beats

From the approved pre-bible: page one, the tease, a block per beat with headline,
tag and talking points, the protection steps, the close, and the whole Build Sheet. Each clip slot is a placeholder the pipeline fills:

```
**CLIP — FIND · VERTICAL:** a doorbell or security-camera video of someone planting a camera in a bush
```

Check: `python3 scripts/check_outline.py outline.md --stage beats`. The beats are
the pipeline's Checkpoint 1: the room can move, cut or re-orient blocks here,
before any search budget is spent. If the user says to run straight through, run
straight through.

A story runs **5–9 beats** for an A, **2–4** for a B; a one-long-A show (11/11)
can run to 10. More means it's two stories, or it isn't shaped yet: say so in Open
calls. Friday: outline the content block fully; the deals half is one line in THE
SHOW (`Deals — Trey Donovan, live requests`), no clip beats. A call-in F2 outlines
two callers and the expert; callers by caller ID in the Build Sheet, first names
only in the front. Clips: about two outside clips a segment (the house standard,
set by former Head of Content Matt Raub), freshest first; when a story wants more,
say so in Open calls.

# Phase 2 — Videos

Runs `rossen-pipeline` on the outline. **Needs Claude Code with the `rossen_harvest`
package**: search, captions and Whisper don't run in claude.ai chat. In chat, finish
Phase 1, deliver the beats outline, and say Phase 2 runs in Claude Code.

1. **Beats.** `rossen-beat-extractor`, outline mode, reads the Build Sheet's Beats
   table: one beat record per `HAVE` / `FIND` row. `beat_id` is `MM-DD-<beat id>`
   (`11-11-A2`). `script_text` is the block's talking points plus the row's Who and
   Search specifics.
2. **Queries, search, grade**: the pipeline's Steps 2–6, with its Checkpoints 1–3.
3. **Write the picks back**: replace each placeholder with the clip line, the
   in–out line and the soundbite (and a `No times yet:`, `Legal:` or `Note:` line
   if one applies); fill the row's Clip number; number the clips 1..N in air order; update THE SHOW; flip the header to
   `Stage: videos`.

Full candidate lists, shortlists, queries and grades stay in the pipeline's run
folder (`picks.json`, `report.md`).

**Read the whole window, not just the outcue.** Before a clip is written in, read
every transcript line between its in and out points (each segment of a butt cut)
plus about 20 seconds past the out. Give it a `Legal:` line and an Open call,
with a tighter cut proposed from the transcript, when the window contains an
accusation against an identifiable person, a claim whose answer falls outside the
cut, a minor, a medical detail beyond what the story needs, or an address, plate
or account number. (10/14: a butt cut aired the store's claim that the victim
"sexually harassed" employees; his attorney's "baseless" started one second after
the out.) `check_outline.py --transcripts transcripts.json` scans every window.

**Time it on the copy you link.** A site cut and its YouTube upload drift by
seconds and sometimes are different packages (11/11: a source line relabeled to
KTLA's upload of a different story). If the transcript is from another copy, say
which in a `Note:` line under the clip.

You cannot watch video. Every timecode, outcue and soundbite comes from a
transcript or it isn't written. A missing clip is a finding: an honest "no clip
found" Open call costs less than a bad pick discovered in the edit bay.

Check: `python3 scripts/check_outline.py outline.md --stage videos --transcripts transcripts.json`.

# Build

1. Fill `templates/outline.md` → `outline.md` in the run folder.
2. `python3 scripts/check_outline.py outline.md --stage beats|videos`: fix every
   ERROR, read every WARN.
3. `python3 scripts/build_outline.py outline.md -o "Outline F2 11_11.docx"`, under
   the standard title `Outline <SHOW> <M/DD>` (producer, 10/14/2026), `/` written as
   `_` in the file name; a Google Doc copy is named `Outline F2 11/11`.
4. `soffice --headless --convert-to pdf` it, then look at the pages.

Deliver the `.docx`. Revisions land in the file. If the room edits a Google Doc
copy, read it back, update the front of `outline.md` to match, then bring the Build
Sheet into line and re-run the checker.

# Handoff to the bible

Once the room approves the outline, `rossen-script-writer` writes from it: **same
blocks, same order, same clips.**

| Outline | Bible |
|---|---|
| THE SHOW, open package | Running order; the tease's first lines |
| THE TEASE | The super tease (in caps, prompter form) |
| Block headline | The mid-story header, as written |
| Talking points | The runway lines, in caps |
| Clip line + in–out line | `(((PLAY CLIP n ORIENTATION)))`, `OUT:` with the last outcue, and the red source line |
| Soundbite | What the runway's question sets up; never copied into the bible |
| `No times yet:`, `Legal:`, `Note:` | A red producer cue, or the fix it names |
| Out | The bold re-entry line after the clip |
| Red flag | The takeaway line after the case |
| Break | `BUT FIRST, A QUICK WORD FROM OUR SPONSORS` and the sponsor cues |
| Protection steps | `HERE'S HOW TO PROTECT YOURSELF`, numbered; sources go to the source log |
| Build Sheet: Hold back | The limit on the tease, headlines and *Next* lines |
| Build Sheet: Jeff should know (dating included) | `JEFF PLEASE NOTE` comments |
| Build Sheet: Who | The source log; the bible says `THIS WOMAN` |

A beat or clip the writer wants to add, cut, move or swap is a change to the
outline first: say which block.
