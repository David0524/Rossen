# The pre-delivery review loop

Added 10/7/2026 at the producer's request. Before a bible reaches the producer,
the writer runs `rossen-bible-final-reviewer` on its own draft in a background
agent, fixes **BLOCKERs only**, and checks again. Everything else goes to the
producer as notes.

Why: on the 10/14 and 10/9 bibles the reviewer caught three things a machine
should fix before a person ever sees the draft:
- a clip out point that aired an unanswered sexual-harassment accusation;
- "WATCHED FOR WEEKS" against a transcript that says "months";
- "DO NOTHING AND YOU GO BACK TO ORIGINAL MEDICARE," which would have cost
  viewers their drug coverage.

Those are facts, safety and legal problems. Taste is not, and the loop never
touches it.

## When it runs

After `check_bible.py` is clean and **before** `build_bible.py`. That gives
the order: draft → check → fix → **review loop** → build → verify → deliver.

Skip it only if the producer says so ("skip the review"), or if the request is
a small targeted edit to an existing bible: a line or two, with no new facts,
clips or numbers. A whole-bible rewrite or a new story gets the loop.

## Each round

1. **Spawn one reviewer agent** with the Agent tool (general-purpose). Give it
   the prompt below. Running it as a separate agent keeps the review honest: it
   reads the draft cold instead of trusting what the writer meant.
2. **Read its BLOCKERs.** For each one:
   - **A fact it marks CONTRADICTED, with a source of the same scope:** make the
     smallest edit that fixes it, using the reviewer's source. Never invent a
     replacement figure.
   - **Unsafe advice or a contact detail that doesn't work:** fix it to what the
     issuing body's page says.
   - **Legal exposure** (an unanswered accusation, guilt stated as fact, a clip
     window that airs something it shouldn't): fix the wording or the clip's
     in/out from the transcript. **A clip change is never silent.** List it in
     the chat reply and update the outline's Videos row to match.
   - **A blocker the writer can't fix from the sources** (an unfilled company
     response, a clip nobody has watched): don't guess. Turn it into an open
     decision (`(((PRODUCER - …)))`) and list it.
3. **Re-run `check_bible.py`** so a fix doesn't break the format or the length
   band.
4. **Run round 2 only if round 1 changed anything.** Round 2 checks only the
   lines that changed and anything they touch: tease-and-body figures, and the
   "next" lines.

**Hard stop after two rounds.** If BLOCKERs remain, deliver anyway and put
them at the top of the chat reply as "still blocking, needs you." Don't keep
looping: a loop that runs until the reviewer has nothing left to say just
churns and costs tokens.

## What the loop must not do

- **No WARNINGs or NOTEs get fixed.** Voice, tease wording, header escalation,
  bold, "caught in the act," a number repeated in the tease: those are the
  producer's taste calls. She keeps some on purpose (see "Producer one-offs are
  not rules" in SKILL.md). Pass them through as notes.
- **No restructuring.** Don't reorder stories, add or cut a story, or add a
  clip. The loop edits lines.
- **No touching Drive or Google Docs.** It works on the local `draft.md` only.
- **No sources in the document.** Sources go in the chat reply and
  `SOURCE_LOG.md`, as before.

## Reviewer agent prompt

Fill in the paths. Keep the rest as written.

```
Use the rossen-bible-final-reviewer skill (read
/home/user/Rossen/.claude/skills/rossen-bible-final-reviewer/SKILL.md and
follow it) on this pre-delivery draft:

  Draft: <run folder>/draft.md
  Show: <MM/DD> <F1 Friday live | F2 Wednesday>
  Stage: final. Clips are picked from the outline: <run folder>/outline.md
  Source list: <run folder>/SOURCE_LOG.md, plus transcripts.json if present

This is the writer's own check before the producer sees it, so it is
BLOCKER-ONLY:
- Run mechanical_pass.py --stage final and the fact-check tiers as the skill
  says. Search the web for anything not confirmed by the run's sources.
- Return ONLY the BLOCKERs, as a list. Each one gets: the exact line from the
  draft (quoted), the problem, its confidence label, the source (URL or
  transcript + timecode) and its scope, and the smallest fix the sources
  support.
- Then one line with the count of WARNINGs and NOTEs, and a list of them, one
  line each. Do not elaborate on them.
- Numbered clip markers, filled OUT: lines and the source line under OUT: are
  the house format at this stage. They are not defects.
- Do not write files. Do not edit the draft. Do not touch Google Drive.
- Do not claim to have watched any clip.
```

## Logging

Write `REVIEW_LOOP.md` in the run folder:
- per round: each BLOCKER, what changed (before → after), and its source;
- the BLOCKERs still open;
- the WARNINGs and NOTEs passed through.

Commit it with the bible.

The chat reply leads with a short "Review loop" paragraph: the number of
rounds, what was fixed, what's still blocking, and the number of notes left
for the producer. The full producer-facing review (`rossen-bible-final-reviewer`
with all three artifacts) still runs separately when the producer asks for it.
