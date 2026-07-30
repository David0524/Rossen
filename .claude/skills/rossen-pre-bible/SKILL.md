---
name: rossen-pre-bible
description: Research and pitch candidate stories for an upcoming Jeff Rossen (Rossen Reports) show, then render the approved slate as a Pre-Bible Pitch Sheet .docx — a ranked shortlist plus one page per story with the working tease, the hook, the mechanics, the footage needed, the protection payoff, and a segregated sources-and-verification block. Use whenever the user asks for story ideas, pitches, a pitch sheet, a pre-bible, a slate, a rundown of candidates, "what should we cover Wednesday," "find me stories for Friday," or wants to brainstorm what a show could be before anyone writes it. Also use to re-rank, add to, or revise an existing pitch sheet. Do NOT use to write the bible itself — that is rossen-script-writer, and it runs after this.
---

# Pre-Bible Pitch Sheet

The document that exists **before** the bible. Jeff and the producers read it in a
meeting and say yes or no to each story. Nothing gets written until they do.

Downstream consumer: `rossen-script-writer`. Everything here is sized so an approved
page can be handed straight to it.

| File | Load when |
|---|---|
| `references/ranking.md` | Ranking, the sexy beat, confidence, viral flags. **Load every run.** |
| `references/show-shapes.md` | Checking slot fit, or deciding how many stories a slate needs. |
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
4. **What that day's shape requires** — see `references/show-shapes.md`.
5. **For a Wednesday, the story count. Ask; never assume it.** A Wednesday runs
   A+B by default (two stories), sometimes a 3–5 story rundown, sometimes a
   single-topic umbrella show. Those need different research: two deep stories,
   or one deep plus several light, or one topic with five sourced instances.
   Getting this wrong wastes the whole pass.

The day of week and the story count govern how many stories you need and what
kind. Researching a slate before you know which show it feeds is the most
expensive mistake available here, because a Friday needs one story and a Wednesday
needs anywhere from one topic to five, and stories are not interchangeable between
them.

Time-sensitivity is scored against **the airdate**, not today. A back-to-school
story with a window closing August 20 is live for an August 12 show and dead for a
September 3 one.

## The two steps, and the gate between them

This skill is two steps and **the gate is not optional**.

**Step 1 — pitch, in chat.** Research candidates, rank them, and present the
shortlist *as a message*, not a file. For each: headline, the sexy beat, proposed
slot, confidence, viral flag, and one or two lines on why. Then stop and ask which
ones are in. Offer more than the slate needs — the user is choosing, and a
shortlist with no losers isn't a choice.

**Step 2 — build, after approval.** Only once the user has said yes or no to each
story do you write the `.docx`.

**Do not skip to step 2 because the research went well.** The temptation is real:
you have five good stories, the document is obvious, producing it feels like
service. It is not — it is spending the user's review on a document half of which
they were going to cut. Rejected pitches cost one line in chat and twelve lines in
a document.

If the user hands you a story list and says build it, the gate is already satisfied
for those stories. Say which ones you're proceeding on and go.

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
children, or sense of being watched. A pure wallet story — prices, fees, coupons —
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

Attribute weak sources rather than laundering them: advocacy-group estimates,
vendor blogs, single-outlet claims, and self-reported surveys get named as such at
the point of use. `⚠️` for check-before-air, `🚨` for legal or a load-bearing
inference.

## Don't re-pitch what already aired

Check every candidate against the bible library in the project before it reaches
the shortlist.

**Exact repeats are out. Similar is fine when there is a genuinely new angle or new
information** — a new case, a new ruling, a new mechanic, a fresh wave. When you
pitch an adjacent story, say what already ran and what's new about this one, in one
line, on the story page. Let the room judge the distance.

## Slot fit is checked, and failures go on page one

Every story page carries a **SLOT FIT** line testing it against the day's shape.
Every sheet's page one carries a slate-level verdict.

If the slate can't fill the show — **nothing strong enough to be the A story**,
fewer stories than the confirmed shape needs, an umbrella pitch with unsourced
sub-stories, a Friday content story too thin to carry a segment — **say so on page
one.** Do not quietly produce a sheet that looks complete and isn't.

**A slate of all threat stories is not a failure and must not be flagged as one.**
There is no required non-scam closer. Shapes: `references/show-shapes.md`.

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
