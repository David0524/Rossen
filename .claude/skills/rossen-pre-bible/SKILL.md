---
name: rossen-pre-bible
description: Research and pitch candidate stories for an upcoming Jeff Rossen (Rossen Reports) show, then render the approved slate as a Pre-Bible Pitch Sheet .docx — a ranked shortlist plus one page per story with the working tease, the hook, the mechanics, the footage needed, the protection payoff, and a segregated sources-and-verification block. Between the chat shortlist and the .docx, it drafts the plain-text pitch email that goes to Jeff for a yes/no. Use whenever the user asks for story ideas, pitches, a pitch sheet, a pre-bible, a slate, a pitch email, "write up the pitches for Jeff," a rundown of candidates, "what should we cover Wednesday," "find me stories for Friday," "vet these pitches," "have we covered this," "what's hot on other channels," or wants to brainstorm what a show could be before anyone writes it. Also use to re-rank, add to, or revise an existing pitch sheet. Do NOT use to write the bible itself — that is rossen-script-writer, and it runs after this.
---

# Pre-Bible Pitch Sheet

The document that exists **before** the bible. Jeff and the producers read it in a
meeting and say yes or no to each story. Nothing gets written until they do.

Downstream consumer: `rossen-script-writer`. Everything here is sized so an approved
page can be handed straight to it.

| File | Load when |
|---|---|
| `references/producer-kit/jeff-and-ryan-rules.md` | **Load every run.** Jeff's A-story rules, Ryan's rubric, the audience data, the team's pitch workflow. From the producer kit; outranks this file where they differ. |
| `references/ranking.md` | Ranking, the sexy beat, confidence, viral flags. **Load every run.** |
| `references/producer-kit/show-formats-2026-09.md` | Step 0. What F1 and F2 are right now, who's who, the regular experts. |
| `references/producer-kit/story-board-2026-09-29.md` | Before pitching. Aired, pipeline, banked, and **dead, and why**. A snapshot: ask for the live one. |
| `scripts/coverage_check.py` | **Before any candidate reaches the shortlist.** Searches 62 aired transcripts. |
| `scripts/video_info.sh`, `scripts/competitor_search.sh` | Confirming a video's date and views; Ryan's heat check. Need `yt-dlp`. |
| `references/producer-kit/titles.md` | Writing Potential Packaging. The channel's title patterns and top performers. |
| `references/producer-kit/facts-to-get-right.md` | Before any number goes in a pitch. |
| `references/producer-kit/channel-facts.md`, `competitive-landscape.md` | Making the case for a story; reading competitor numbers. |
| `references/producer-kit/help-line-summary.md` | Looking for a victim. Caller IDs only, never names or numbers. |
| `references/show-shapes.md` | Checking slot fit, or deciding how many stories a slate needs. |
| `references/pitch-email.md` | Step 2. The house pitch email, field by field. Example: `references/examples/pitch-email-2026-09-28-F2-A-options.md`. |
| `scripts/check_pitch_email.py` | **Before handing over the email. Always.** |
| `references/sheet-format.md` | Rendering the document. Exact section order and headers. |
| `scripts/build_sheet.py` | Building the `.docx`. |
| `scripts/check_sheet.py` | **Before delivering. Always.** |
| `templates/story_page.md` | The per-story skeleton to fill. |

## Step 0 — know what show this is, before anything else

Establish, in this order, and **state them back to the user in your first reply**:

1. **Today's actual date.** Read it from the environment. Do not assume.
2. **The airdate.** Ask if it wasn't given. "Next show" is not an airdate.
3. **The day of the week for that airdate** — Wednesday or Friday. Compute it; don't
   take a verbal label on faith. A user who says "the Friday show" about a date that
   falls on a Wednesday has made a mistake you need to surface now, not after
   research.
4. **What that day's shape requires.** Wednesday is the **F2**: taped the
   Friday before, posted Wednesday, so the working deadline is the taping. Ask
   whether it's the call-in show or a story show (A, B, C plus an expert).
   Friday is the **F1**: live, lead story with an expert, sponsor, deals. See
   `references/producer-kit/show-formats-2026-09.md` and
   `references/show-shapes.md`.

The day of week governs how many stories you need and what kind. Researching a
slate before you know which show it feeds is the most expensive mistake available
here, because stories are not interchangeable between them: deals stories belong
to Friday (Jeff moved the Prime Day price check to the F1), and an A story has
to be a scam.

Time-sensitivity is scored against **the airdate**, not today. A back-to-school
story with a window closing August 20 is live for an August 12 show and dead for a
September 3 one.

## The three steps, and the gates between them

This skill is three steps and **the gates are not optional**.

**Step 1 — pitch, in chat.** Research candidates, rank them, and present the
shortlist *as a message*, not a file. For each: headline, the sexy beat, proposed
slot, confidence, viral flag, and one or two lines on why. Then stop and ask which
ones are in. Offer more than the slate needs — the user is choosing, and a
shortlist with no losers isn't a choice. **For A stories, four or five options
with a recommended order** (Jeff: "Kyle & David need to provide more options
each week"). Each A must be a scam with a villain, broad enough for the whole
audience, and big enough to carry the show; state the one-line viewer advice.
Test every scam pitch two ways and say so when either is weak: **audience fit**
(is a 55+ viewer the target, or only a spectator?) and **the extended threat**
(the beat that puts the viewer in personal danger). Check the story board's dead
list before anything reaches the user.

**Step 2 — the pitch email, after the user picks.** For the stories the user kept,
draft the plain-text pitch email that goes to Jeff. Numbered stories, one dense
lead sentence each, a `Coverage:` list of dated source links, three `Potential
Packaging:` titles, and flag lines at the bottom. Exact format and rules:
`references/pitch-email.md`. Run `scripts/check_pitch_email.py` on it before
handing it over. Deliver it in chat, ready to paste, and stop. Jeff answers the
email; the answer is the next gate.

**Step 3 — build, after Jeff's answer.** Only once the user reports which stories
Jeff approved do you write the `.docx`, and only for those.

**Do not skip a step because the research went well.** The temptation is real:
you have five good stories, the document is obvious, producing it feels like
service. It is not — it is spending the user's review on a document half of which
they were going to cut. Rejected pitches cost one line in chat, a few lines in an
email, and twelve lines in a document.

If the user hands you a story list and says build it, the gates are already
satisfied for those stories. If they hand you stories and ask for the email, start
at Step 2. Say which step you're on and go.

## Rank by clickability. This is the whole game.

The rank order is **how many people click**, not how much money is at stake and not
how badly someone was hurt.

A check-in scam and a hidden camera in the rental are the same story. One of them
gets clicked. Your job on every candidate is to find the version of the beat that
gets clicked, and put *that* in the shortlist — not the accurate topic label.

> Airbnb → the beat is **hidden cameras**, not check-in fraud.
> EBT skimming → the beat is **something is filming your hands**, not card cloning.
> Loyalty breach → the beat is **a stranger can pay as you at the counter**, not
> credential stuffing.

The mechanism is never the beat. The beat is what it does to a person's body, home,
children, money they touch every day, or sense of being watched — **as long as
our viewer is the target.** Surveillance our viewers support (the Flock
plate-camera show flopped) is a spectator story. Stories with Target as the
title or main story are dead ("didn't perform well"); a passing mention is fine. See "How this squares with the sexy-beat rule" in
`references/producer-kit/jeff-and-ryan-rules.md`. A pure wallet story — prices, fees, coupons —
can be excellent and still not lead, because money is abstract and a camera is not.
It goes later in the show, and it says so on its page.

Full rubric, the demotion rule, and the confidence and viral scales:
`references/ranking.md`. Load it.

## Confidence is one blended rating: will this make a show?

`HIGH` / `MEDIUM` / `LOW`. One number, blending clickability, sourcing, footage,
and timing.

**It is not a sourcing score.** A great story with a fixable research gap is HIGH
with a flag, not MEDIUM. A perfectly sourced story nobody clicks is LOW. If your
rating tracks how well-documented the story is rather than how likely it is to air,
you have graded the wrong axis — go back.

Sourcing risk travels **separately**, in the verification block, where it can be
fixed without dragging the rating down.

## Viral is preferred, not required

An existing viral clip is a large thumb on the scale — it means the footage problem
is already solved and the audience has pre-validated the beat. Flag it loudly:
column on the shortlist, callout on the story page.

But it is a bonus, not a gate. A story with no footage and a great beat still
belongs on the sheet — with `FOOTAGE — BE HONEST ABOUT THIS` saying plainly that
it's Jeff, graphics and a screen-share, so the room decides that going in rather
than discovering it in the read.

Thresholds and how to record a viral clip: `references/ranking.md`.

## Evidence grounding — the iron rule

This skill produces research that a human checks and then puts on television. The
rule: **every material claim rests on a source you actually loaded, with a
retrievable anchor. Never on plausible inference.**

Three failures matter more than the rest:

**You cannot watch video.** You can find where a clip lives and describe it from
its title, description, or transcript. You cannot confirm what is on screen and you
cannot produce a timecode or an outcue. Say so, in the document, every time. Never
write a timecode. Never write an outcue. Those are the bible's job and they come
from a human who watched the footage.

**Flag the sexiest line hardest.** The single highest-value behavior in this
document. The most quotable line in a pitch is reliably the least-supported one,
because it's the reframe that made the story worth pitching. When the beat outruns
the sourcing, say exactly that, at the exact line, in the verification block —
*"this is the cold open and it contains one inference; source it or soften it."*
Do not let it slide because it's the good part. It being the good part is why it
must be flagged.

**Confirmed and unconfirmed never share a paragraph.** Every story gets a
`**Confirmed:**` run and a `**NEEDS VERIFICATION:**` run, visually separated. A
reader skimming for what's safe must be able to find it without parsing prose.

Never invent a statistic, a victim, a quote, a dollar figure, or a source. If you
cannot find it, the finding is *"I could not find this"* — which is genuinely
useful and is what the room needs to hear. Filling the hole with something
plausible is the one unrecoverable failure here, because it looks exactly like
research until it's on air.

Confirm every competitor video's upload date (`scripts/video_info.sh`, or the
page itself): search results don't show dates and a "trending" clip is often a
year old. Reports from advocacy groups or vendors are leads, not sources.
Help-line callers are referred to by caller ID only; never promise a victim
their money back.

Attribute weak sources rather than laundering them: advocacy-group estimates,
vendor blogs, single-outlet claims, and self-reported surveys get named as such at
the point of use. `⚠️` for check-before-air, `🚨` for legal or a load-bearing
inference.

## Don't re-pitch what already aired — run the coverage check

Never call a topic "not covered" without running
`python3 scripts/coverage_check.py "pattern|synonym" --context` over the 62
transcripts (Mar 18 to Sep 29, 2026) and reading the context. Ten-plus hits
over several minutes is a segment; a few is a B/C story or an aside; watch for
false matches ("tractor" in "contractor"). Then check the story board snapshot,
`references/channel-uploads.txt`, and the bible library for anything newer.

**No repeat inside three months, and B and C stories count** — titles are vague
on purpose and a livestream covers four or five topics. Older coverage is fine
to revisit with a genuinely new angle; say when it ran. **A keyword miss is not
proof:** the Mar 20 to Apr 15 shows have no transcripts (deed fraud ran as a B
story Apr 8 and the checker can't see it). If you couldn't check, say so first.

Check the calendar for collisions with shows already scheduled (a Social
Security pitch was pulled because the Medicare show was a week away). Worked
examples of what "covered" looks like: `references/coverage-notes/`.

## Slot fit is checked, and failures go on page one

Every story page carries a **SLOT FIT** line testing it against the day's shape.
Every sheet's page one carries a slate-level verdict.

If the slate can't fill the show — no A candidate that's actually a scam, a
Friday lead too thin to carry the segment before the deals, a B that collides
with something already scheduled, fewer stories than the confirmed count —
**say so on page one.** Do not quietly produce a sheet that looks complete and
isn't. Shapes: `references/show-shapes.md`.

## Output

Page one is the ranked shortlist table. Every story after gets **its own page**, hard
page break, one page each. Then the sources-and-verification block at the back.

One page is a real ceiling. When a story won't fit, cut material — tighten the
mechanics run, drop the weakest footage line — and **tell the user it was tight**.
Never shrink the type, narrow the margins, or spill onto a second page. If it truly
cannot fit, that is a finding: the story is two stories, or it isn't shaped yet.

Sources and flags live at the back, never mixed into the pitch pages. Producers read
the front to decide; whoever writes reads the back before drafting.

Build with `scripts/build_sheet.py`, then run `scripts/check_sheet.py`, then render
to PDF and **look at the pages** to confirm the one-page rule actually held —
python-docx cannot tell you where a page broke. Procedure in
`references/sheet-format.md`.

## Deliver it with the open questions

End every sheet with `OPEN QUESTIONS FOR THE MEETING` — the real decisions the room
has to make. Which story leads. Where two candidates collide. What needs legal.
Which sexy line needs a ruling before anyone drafts. Whether a footage gap is
acceptable.

This section is not a formality and it is not a summary. It is the reason the
document exists: the sheet's job is to get decisions made in the meeting instead of
discovered on shoot day.
