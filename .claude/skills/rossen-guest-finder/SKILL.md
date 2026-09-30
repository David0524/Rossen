---
name: rossen-guest-finder
description: Find and vet bookable guests for a Jeff Rossen (Rossen Reports) show — reporters who covered the story, experts, insiders, demonstrators, victims, and the right-of-reply contact at the accused company — then produce a Guest Sheet .docx with a direct way to reach each one. Use whenever the user asks who to book, who can speak to a story, needs a victim or an expert or a reporter, asks to find contacts, wants a guest sheet, says "who do we get for this," "find me someone who," "we need a face for this segment," or wants to fill a guest slot on an existing slate. Also use to re-vet or replace guests already booked. Do NOT use to pick archival clips — that is rossen-beat-extractor and rossen-clip-grader.
---

# Guest Sheet

Turns an approved story into a list of people somebody can call today.

Runs after `rossen-pre-bible` and before `rossen-script-writer`.

| File | Load when |
|---|---|
| `references/roles-and-registers.md` | Choosing who a story needs and where to hunt. **Load every run.** |
| `references/contact-protocol.md` | Any time you are producing contact info. Which is every run. **Load every run.** |
| `references/sheet-format.md` | Rendering the document. Exact section order and headers. |
| `scripts/build_sheet.py` | Building the `.docx`. |
| `scripts/check_sheet.py` | **Before delivering. Always.** |
| `templates/guest_page.md` | The per-guest skeleton to fill. |

## Step 0 — know what you're casting for

Establish and state back in one line:

1. **Today's actual date.** Read it from the environment. Contacts rot.
2. **The airdate**, and how many days out.
3. **The story.** If handed an approved pre-bible page, read it.
4. **The format** — studio, remote, phone, pre-tape, or live.

If the user says "assume," assume, state the assumption in one line, and proceed.

## Build the document. Do not pitch in chat.

Research, then produce the `.docx`. No shortlist message, no approval gate, no
asking which names are in. Offer more names than the slate needs and let the
document be the thing they cut from.

**Never write a slate verdict, a coverage assessment, or a summary judgment about
whether the sheet is good enough.** Not on page one, not anywhere. The user reads
the names and decides. A machine grading its own output is noise.

## Who actually says yes

Rank candidates by whether appearing serves them. In descending order of what
converts:

**Reporters and journalists who covered the story.** The highest-yield guest type
available and historically underused. Someone who published an investigation or a
local piece on this exact subject is proven on camera, pre-vetted by their own
newsroom, factually deep, and works in an industry where promoting your own work
is the job. They can say most of what a plaintiff's attorney can say and carry no
litigation risk. Start here on every story.

**Anyone with something to promote right now** — a book, a report, a campaign, a
study, a service, a case. The promotion is the incentive and it is reliable.

**Practitioners who can demonstrate.** They sell the thing they are showing, so
appearing is marketing.

**Attorneys and plaintiffs last.** They are easy to find, which is why they
dominate a lazy search, and they are the most constrained: active litigation,
counsel clearance, gag terms, and a client who has already won and no longer needs
press. One is usually enough. Do not build a sheet out of them.

## The pitch, in the outreach line

Rossen Reports averages roughly 600,000 viewers per show — a figure the show
supplies; do not research it or restate it as an independent finding. Publicity is
the offer. Every contact line carries one short sentence on what this person gets
by appearing, because that is what the booker says when the phone picks up.

## Roles are plain words

`victim`, `reporter`, `expert`, `insider`, `official`, `advocate`,
`demonstrator`, `company`.

No underscores, no backticks, no code formatting in the document. This is
something a person reads, not a spreadsheet. Write `victim`, not
`victim_firsthand`.

Definitions and the search registers that find each:
`references/roles-and-registers.md`.

## Mine local news first

Anyone who already did a standup with a local affiliate has proven they will go on
camera, been vetted by another newsroom, and left tape you can judge. Start there
on every story, before anything else. It also surfaces the reporter, who is often
the better guest.

## Contact means an email, a phone number, or a LinkedIn

Something a producer can act on right now, without another search.

**A team page, a newsroom index, a general "contact our press office," or a "route
through comms" is not a contact.** Neither is a news agency's newsdesk standing
between you and the person. If that is all you have, you have not finished the
job — keep digging.

Where to actually find one: a journalist's own X or LinkedIn bio (many publish
their work email outright), their personal site, a firm's contact page, a
published main line, a company newsroom address.

**No contact means no guest.** If you cannot produce a real one, cut the person
from the sheet and say in a line why they were cut. The only exception is a guest
so valuable the user would chase them anyway — and then say plainly that the
contact is the open problem.

Where the only honest route runs through someone else — an attorney for a private
individual — the contact line is that named person with their own real contact.
A cold approach to someone at home about the worst week of their life gets hung
up on.

Every contact carries a short source-and-date tag. A publicist who moved firms in
March is worse than no contact. Details: `references/contact-protocol.md`.

**Never invent a contact.** Never construct an email from a pattern, even when you
have seen a colleague's address and the format looks obvious. Never use a
people-search or data-broker result, including one showing a masked address.

## Bookability is appearance history, nothing more

It is not a prediction. Nobody can forecast whether a person answers an email, and
a sheet that pretends otherwise is inventing information.

State only what the record shows:

- `STRONG` — has done many media appearances
- `SOME` — has done a few, or one
- `NONE FOUND` — no appearances located

One clause of evidence after it and nothing else. `STRONG — regular CNN and
podcast appearances`. Never a probability, never a guess at their mood, never
"likely to say yes."

## Right of reply is a guest slot

Every story naming a company gets a `company` entry — corporate communications,
the media inquiry address, the outside PR firm.

Log the attempt with a date in the outreach log. "We reached out and did not hear
back" is only sayable if somebody did.

## Evidence grounding

**Every material claim rests on a source you actually loaded.** Never on plausible
inference.

**You cannot watch video.** Find where a prior appearance lives and link it so a
human can open it. Do not write caveats about not having watched it — this is an
internal document and the reader already knows. Just never describe how someone
performs on camera, because you do not know.

**Verify credentials at the source** — the board, the docket, the directory — not
the subject's own bio page.

Never invent a name, an affiliation, a credential, or a contact. "I could not find
a way to reach this person" is a real finding.

This document carries no verification block, no outreach log, and no open
questions. It is a list of people and how to reach them. Anything that needs
fact-checking belongs to `rossen-bible-final-reviewer`, which audits the bible
before air — do not duplicate it here.

## The company entry is minimal

A `company` guest is a comment request, not a booking. It gets a name and a
contact and nothing else — no why-them, no prior on camera, no bookability, no
confirmed run.

Keep it on every story that names a company. It is one line of work and it is the
difference between being able to say "we reached out" and not.

## Output

Page one is the guest table. Every guest after gets **its own page**, hard page
break. The document ends with the last guest.

Build with `scripts/build_sheet.py`, run `scripts/check_sheet.py`, render to PDF
and **look at the pages**. python-docx cannot tell you where a page broke.
Procedure in `references/sheet-format.md`.
