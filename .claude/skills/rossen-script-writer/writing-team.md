# How a bible gets written: research packet, writer, director

Producer, 11/11/2026. Adopted after the 11/18 F2, written twice from the same
outline. One version was written by the session that had also done the research.
Its first draft needed seven fact and legal fixes, and its voice was plain, because
it never read Jeff before writing. The other was written by a separate writer
subagent that started from a verified-facts brief and read Jeff's voice guide and
aired livestreams first. It avoided every trap in the brief and sounded more like
Jeff. It also ran long and gave away outcomes in headers until a director caught it.
The lesson: **the preparation made the difference, and splitting research,
writing and directing keeps each one honest.**

The process has three roles and runs in this order.

| Step | Who | Output |
|---|---|---|
| 1. Research packet | The director (this session) | `bible/research_packet.md` |
| 2. Voice prep + draft | The writer (one subagent) | `bible/draft_v1.md`, `bible/sources.md` |
| 3. Director rounds (up to 3) | The director reviews; the writer edits | `bible/draft_v2.md`, `bible/draft_v3.md`, `bible/REVIEW_NOTES.md` |
| 4. Review loop (`review-loop.md`) | A fresh reviewer agent | `bible/REVIEW_LOOP.md` |
| 5. Build, verify, deliver | The director | the two `.docx` files |

**Skip the split** only for a small targeted edit to an existing bible (a line or
two, no new facts or clips), or when the producer says so. Then the session writes
directly, still from the packet's facts.

## Step 1: the research packet (the director)

Before anyone writes a line, the director builds `bible/research_packet.md` from
`templates/research-packet.md`. Its job is that the writer never has to guess a
fact, and never walks into a trap the director already found. It holds:

- **Every fact the copy may use**, each with its source, the date of the case, and
  the date of the report. A fact the director couldn't confirm is marked so, and
  the writer may not use it as a fact.
- **Every clip, re-checked against its transcript**: the link the bible will use
  (the YouTube copy when one exists, per CLAUDE.md), the in and out points, the
  outcue verbatim, and the copy it was timed on. Read the **whole window plus
  about 20 seconds after the out**. Note anything inside it that can't air: a
  phone number or address read aloud, a minor, an accusation whose answer falls
  outside the cut. Give the corrected in or out point.
- **Traps**: things that look true and aren't, or that are true but unsafe. For example:
  - a detail the outline adds that the source doesn't say;
  - an accused person who must never be called a thief;
  - a named company whose non-response has to be said aloud;
  - a refund that covered something other than what it sounds like;
  - advice that fails the people the scam targets (a "confirmation email" number when the
    scam is a fake email; the back of an airline credit card, which reaches the bank).
- **What the director decided** about clip numbering, cues the skill turns into red
  production lines (an open package, a demo), the sponsor, and the guest.
- **The open decisions** for the producer, so the writer can carry two or three as red cues.

The packet carries **facts, not wording**. Never put a sample line in it (see
"The writer brief" below).

## Step 2: voice prep and the draft (the writer)

Spawn **one** writer subagent with the Agent tool (`subagent_type:
"general-purpose"`, `model: "sonnet"`), with the brief from
`templates/writer-brief.md`, filled in. Keep that same agent alive across rounds
with SendMessage, so it keeps its context.

The brief makes the writer read, in this order:

1. `CLAUDE.md` and this skill's `SKILL.md`, plus every file the skill marks
   "every draft".
2. **Voice, read for how Jeff talks, not for rules** (mandatory, every bible):
   - `references/producer-kit/rossen-voice.md`, all of it.
   - Three aired livestream transcripts from the `rossen-pre-bible` skill's
     `references/transcripts/`: always `Gh1ueu7ovlQ.txt` and `SjaMwcIQXyU.txt`,
     plus the one closest to this show's topic. Pick it by title from
     `rossen-pre-bible/references/channel-uploads.txt`. For a search or phone
     scam that is `jmUfTCWWDVM.txt`.
3. The approved outline, and the research packet.

Then the writer writes the whole bible (DRAFT or FINAL, per SKILL.md), runs
`scripts/check_bible.py`, clears every ERROR, and writes the source log markdown.
It does not build the `.docx` and does not run the review loop.

**Every word in the bible is the writer's.** The director never edits the draft
file.

## Step 3: director rounds (up to three)

The director reads each draft against the outline, the packet and the
transcripts, and sends notes. **Notes are problems plus the move to make, never
replacement lines.** Example wording in a note gets copied almost verbatim (seen
twice in testing). Describe the move ("reaction first, then what the clip proved";
"hold the outcome for the clip"; "make it a callback to the woman from Illinois"),
not the line. Write each round's notes verbatim into `bible/REVIEW_NOTES.md`,
and have the writer save each round as a new file (`draft_v2.md`, `draft_v3.md`)
without touching the previous one.

**The director's checklist**, in the order the 11/18 drafts needed it:

1. **Spoilers.** A header, a runway, a pre-sponsor tease or a `NEXT` line that
   gives away what the clip reveals: an outcome, a refund, an arrest. Headers
   are the most common miss. A header asks the question; the clip answers it.
2. **Source drift.** Every paraphrase of a clip, checked against its transcript
   ("never dealt with" must not become "never heard of"). Every attribution goes to
   the person the package actually shows. Don't guess a job title for an unnamed
   speaker.
3. **Invented details or feelings.** Second-person scenes are fine. Beats made up
   inside them are not: a confirmation that never arrived, a drive nobody mentioned,
   a feeling no one stated.
4. **Overclaims.** A pre-recorded demo called "live" or "right now". A refund
   stated as full when it was partial, or tied to the wrong tickets. A rule stated
   absolutely when it has exceptions ("not in the app means no reservation").
5. **Legal.** Accused people framed as charged, not convicted, in the tease and
   the "next" lines too. A named company's non-response said aloud after a clip
   that implicates it. Nothing in a clip window that can't air.
6. **Advice that fails the target.** Test every red flag and step against the
   people the scam targets (SKILL.md, Ryan's rule 5).
7. **Unfinished research.** A company response left as an open decision when it
   can be found. A spelling or detail left as a question when a source settles it.
8. **Structure.** RED FLAG said about once a story. Every case ends on one usable
   takeaway. Every tease promise is paid off by name. The pre-sponsor tease names
   specifics. No outlet in spoken copy. No unbooked guest in black.
9. **Length and repetition.** Each takeaway said once in its stop and once in the
   protection list, not five times. Cut lines that restate the clip or the
   button. Tease about 180 words at most. Don't cut to hit a word band; cut what
   is said twice.
10. **Lines lifted from the brief or the packet.** Rewrite them.

Stop after the third round even if small things remain, and list what's left for
the producer. Usually round 1 carries most of the notes, round 2 is a tightening
pass, and round 3 is the build.

## Step 4: the review loop

After the director's last round, run `review-loop.md` on the final draft. It is a
fresh agent and it looks only for BLOCKERs: wrong facts, unsafe advice, legal
exposure. Facts and legal problems get one more independent read before anything
reaches the producer. Fixes in this loop go through the writer as notes, like any
other round. Its two-round stop still applies.

## Step 5: build, verify, deliver

The writer builds both files with `build_bible.py` and `build_source_log.py`
under the standard titles. The director runs `verify_format.py` and
`check_bible.py` once more, then delivers per CLAUDE.md. The chat reply follows
"Output" in SKILL.md and adds what changed in each round and what's still open.

## Files in the run folder

`bible/research_packet.md`, `bible/draft_v1.md` … `draft_vN.md`, `bible/sources.md`,
`bible/REVIEW_NOTES.md`, `bible/REVIEW_LOOP.md`, and the two `.docx` files. Commit
them all.
