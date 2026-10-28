# Sheet format and rendering

Load when building the document.

## Document order

```
PRE-BIBLE PITCH SHEET
Prepared <date> · <slate description> · <how it was researched>

THE SHORTLIST — RANKED          <- table, page 1: # | Story | Lead title | Viral clip (with URL); then HOW THESE WERE BUILT (two lines)
SLATE FIT                        <- verdict line under the table
                                 [page break]
1. <STORY HEADLINE>              <- one page, hard break after
                                 [page break]
2. <STORY HEADLINE>
                                 [page break]
...
THE GAP — AND WHAT I'D RESEARCH NEXT    <- only when the slate is short
                                 [page break]
RESEARCH SOURCES & VERIFICATION FLAGS
  READ THIS FIRST
  STORY 1 — <NAME>
    Confirmed: ...
    Sources: ...
    NEEDS VERIFICATION: ...
  STORY 2 — ...
  STORIES CUT — SOURCING PRESERVED       <- when anything was dropped
OPEN QUESTIONS FOR THE MEETING
```

The back matter is not page-limited. One page per story applies to the pitch pages
only — a verification block gets whatever room the flags need, and cramping it is
how a legal problem reaches air.

## The story page

**Template v3, Oct 26, 2026.** Packaging first, cases underneath (Oct 26 v2), plus
three additions from the packaging-first and coverage lessons: the score on the
page, the title's origin, and a coverage line. Skeleton in `templates/story_page.md`.

| Section | Always? | Notes |
|---|---|---|
| Status line | Yes | `**Status:** READY · **Score:** 12/14 (Fear 2, Heat 1, ...) · **Lead test:** passes 2 of 3`. Replaces the old Slot / Confidence line; slots are decided in the meeting. RE-PITCH and RETURNING THEME go in Status. |
| `POTENTIAL PACKAGING` | Yes | Exactly three titles. The first is the lead title on the cover table. |
| `**Built on:**` line | Yes | Under the titles: the proven title or format it copies, with views or lift. This is the packaging-first trail. |
| `THE PITCH` | Yes | Two to four sentences: beat, why now, what the viewer can check. |
| `CASES` | Yes | One bullet per case, real loss first: bold place and date, what happened, outlet and date in italics. CHECK / LEGAL inline. For a roundup, one bullet per scam with its own clip. |
| `VIRAL CLIP` callout | Yes | Blockquote starting `**VIRAL CLIP**` (or `**CLIP**` under the 500K bar). Shaded box. A story without one is not pitched. |
| `COVERAGE CHECK` | Yes | The closest thing we've aired or filmed, with dates, and the sources checked: transcripts, the Rossen Stories coverage table, Drive bibles since the newest transcript, the story board. Added after the celebrity-scam miss (Oct 26). |
| `FOOTAGE WE NEED` | Yes | The get, then supporting footage and demos. |
| `THE PAYOFF` | Yes | The protection steps. |

A WORKING TEASE is optional now; the packaging does its job on this page, and
the bible writer drafts the tease.

**No emoji anywhere** (David, Oct 26). Write markers as words: `CHECK:` for
check before air, `LEGAL:` for legal risk or a load-bearing claim, `VIRAL CLIP`
for the callout. `check_sheet.py` errors on emoji.

### WORKING TEASE

All caps, blockquoted, in Jeff's voice. This is a *sample* of how the cold open
could sound, so the room can hear the story — the bible writer will rewrite it.

Short clipped lines, direct address, escalation, and the alarming thing first. It
should sound like the tease blocks in the aired bibles, because that's what it's
previewing.

Frame it as broadly as the cases are: every noun has to be true of every case
(`A FREE SAMPLE OR A CRAZY DISCOUNT`, `STORE` not `MALL` unless every case is in
a mall). Lead with the victim whose money is actually gone; a near-miss goes
second. If the tease promises a named payoff (`THE ONE MOVE`), THE PAYOFF below
says which step it is. Ryan's notes, `producer-kit/jeff-and-ryan-rules.md`.

Do not write a tease the sourcing can't support. This is the exact place the
flagging rule bites — if the best line in the tease is an inference, it is going in
the verification block by name.

### Why now, inside THE HOOK

When a story is pegged to news (plans cut, a law, a recall, a breach), say how
the news creates the scam: **the news → the confusion it causes → the scammer's
opening**, ending on one anchor line ("The letter is real. The call isn't.").
Ryan's first note on the 10/9 F1 was that the plan-cut news and the scams read
as two separate stories because no document ever wrote this chain
(`../rossen-script-writer/references/examples/ryan-notes-2026-10-09.md`). It
starts here, so the outline's Peg and the bible's segment 1 inherit it.

### THE PAYOFF

Real, specific, actionable protection steps. Phone numbers, URLs, settings paths,
the physical thing to do. Anything you couldn't confirm gets `*(verify)*` inline.
Where a story has more than one victim case, add the one-line tell for each
(`After Kathryn: no price on anything means walk out`) — the bible places a red flag
after every case.
Test each step against the people the scam targets: a red flag that confirms the
scammer's story for them ("no letter? don't believe the call," when the letters
are real) needs the move that works for everyone (hang up, call them yourself).
A step that can be shown on Jeff's phone gets `*(demo)*`.

## Rendering

`scripts/build_sheet.py` takes a markdown source file and emits the `.docx`. It
handles US Letter sizing, the shortlist table, hard page breaks between stories,
and the caps/bold conventions.

```bash
python3 scripts/build_sheet.py sheet.md -o "Pre_Bible_Pitch_Sheet.docx"
python3 scripts/check_sheet.py sheet.md
```

Then **look at the pages**:

```bash
soffice --headless --convert-to pdf "Pre_Bible_Pitch_Sheet.docx"
pdftoppm -jpeg -r 80 "Pre_Bible_Pitch_Sheet.pdf" page
ls page-*.jpg
```

Read the images. python-docx cannot tell you where a page actually broke, so the
one-page-per-story rule is only real if you have looked. If a story spilled, cut
material and rebuild — never shrink type or margins.

## Style

- Story headlines: all caps, numbered, matching how they'd read on air.
- Teases: all caps, blockquoted.
- Everything else: sentence case prose. The sheet is read in a meeting, not off a
  teleprompter. **Do not write the whole document in caps** — that's the bible's
  convention, not this one. The exemplar reserves caps for headlines and teases.
- No emoji. `CHECK:` check before air · `LEGAL:` legal, or a load-bearing inference · `VIRAL CLIP` callout.
- Bold the thing the reader must not miss. Sparingly, or it stops working.
