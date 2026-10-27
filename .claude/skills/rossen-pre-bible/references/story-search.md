# Finding stories: theme-first search

Load this for every Step 1 run, before any searching. It replaces "start with
this month's news" as the way candidates are found. Added Oct 25, 2026 after the
team reported the old search returning the same few stories every week.

## Why the old search kept repeating itself

It started from the freshest news items (FTC alerts, this month's competitor
videos) and pitched those items as the stories. Fresh-news feeds are short and
everyone draws from them, so each week surfaced the same handful, including
stories the team doesn't want (Amazon refunds). Three habits caused it:

1. **Item-first.** It pitched *a news item* instead of *a theme* the item belongs to.
2. **Recency-first.** It treated "this month" as a requirement, which shrinks the pool.
3. **No memory.** It didn't check what it had already pitched and been passed on.

## The rules that replace them

**1. Pitch the theme. The item is one case inside it.** A MyChart phishing email
is not the story; *phishing that looks like a place you trust* is the story, and
MyChart is one case alongside the bank alert, the toll text and the delivery
notice. Build every pitch as: the theme → two or three cases (lead with the one
where a victim really lost money) → the tells → the one protective move. A pitch
that is only one news item is not ready.

**2. Recency is optional. "Happening now" is not.** A story can be evergreen as
long as it is still hitting people today. Use the peg ladder and stop at the
first rung you can source:

| Rung | Peg | Example |
|---|---|---|
| 1 | A dated event in the last ~3 weeks (arrest, alert, lawsuit, viral clip) | "Police in ___ arrested ___ on ___" |
| 2 | The season or calendar for the **airdate** (`seasonal-calendar.md`) | Holiday deliveries → package scams |
| 3 | Proof it's still happening: one dated case, alert or local package from the last 12 months | A local station package from this spring |
| 4 | None of the above | Not pitchable yet. Goes under THE GAP |

Say which rung the peg is on in the pitch. Never present an old case as new;
the evidence rules in SKILL.md still govern every date.

**3. Fear sells, as long as it's true.** Our fear-framed shows do about twice
what the rest do (`performance-map.md`). Push every candidate to the version
that threatens something the viewer has or does every day: their account,
card, phone, mailbox, home, identity, or being watched or blamed. The threat
must be one the sources support. Fear built on an overstated claim is the one
thing worse than a dull pitch, so the "flag the sexiest line hardest" rule
applies with full force.

**4. Proven themes can come back.** A theme that performed well (lift 1.5× or
better in `performance-map.md`) is welcome again with new cases or a new angle.
Label it `RETURNING THEME — last aired <date>, <lift>` so Jeff sees it up front.
A new angle means a **different scam inside the theme**, not new cases of the
same scam: gift card draining had a segment Jul 29, so fresh arrests didn't make
it new (round 1). Same scam with a segment in the last six months is covered. New beats a rerun; a fresh angle on a winner beats
a brand-new theme that misses.

**5. A themed slate is an option, not a rule.** When the A, B and C can share a
theme without being the same story (three kinds of trusted-sender phishing; three
ways your mailbox gets used against you), offer that slate as one of the options.

## The search, step by step

### 0. Heat scan first: what is exploding right now in our audience's lane

Added Oct 25, 2026, after David: "These are all fine but I want to be blown away."
Theme-first search finds *fine* stories. The blow-away stories are the ones
already doing millions on channels that share our audience (retirement and real
estate creators, phone-setting creators, consumer news) that Jeff hasn't done.
Run this before anything else:

```bash
python3 scripts/channel_heat.py --days 75
```

Any topic that two or more of those channels hit at 500K+ in the last 75 days is
a lead candidate by default, and it goes to the top of the shortlist with its
combined heat stated ("2.2M + 970K in 60 days"). Then build it out with the
steps below. A topic Jeff already pitched is still worth re-pitching when the heat
has jumped since; label it `RE-PITCH` and lead with the new numbers.

### a. Check what's already been pitched (anti-repeat)

Before searching, find the last four weeks of pitches: the pitch emails, the
`Rossen Stories` doc in Drive (its "Already with Jeff and Ryan" and System
tabs), and the story board. Ask the user if you can't reach them. Then:

- A candidate pitched before and not picked **does not come back** unless it has
  a genuinely new angle or new cases. If it returns, mark it `RE-PITCH — first
  pitched <date>` and say what's new in one line.
- A candidate pitched twice without approval is retired. Don't re-pitch it.

### b. Choose the themes to search (breadth quota)

Pick at least **six themes** from `theme-bank.md` for every run, with this mix:

- **Three or more from the winning categories** (top half of `performance-map.md`):
  mail and delivery, bank and card, privacy and being watched, phone/text/email,
  social media and online fakes, home and safety.
- **One seasonal theme** for the airdate (`seasonal-calendar.md`).
- **One new-territory theme** the channel hasn't built a show around (the
  "never a segment" list in `theme-bank.md`, or something you find that fits the
  fear test).
- **At most one** from the weak lanes (retail, Amazon policy, deals, travel,
  health), and only for a B or C or the Friday deals slot.

Rotate: don't open with the same theme two weeks running, and don't let two A
options share a theme.

### c. Search each theme wide, not just new

For each theme, run the theme's queries across time, not only this month:

```bash
python3 scripts/theme_search.py --theme phishing --windows month,year,any
python3 scripts/theme_search.py --list                       # all themes
python3 scripts/theme_search.py --queries "patient portal scam" "fake hospital bill text"
```

It searches YouTube sorted by views in each window, drops our own channel and
known non-signal channels, merges duplicates, and prints the top results per
theme. Read it for **cases and heat**, not for the story: a 2M local package
from last year is proof the theme clicks and a case you can cite (dated), even
if it's not the peg.

Then widen with the other sources, in this order:

1. **Plain-language searches**, the way a victim or their kid would type it
   ("my mom got a letter that", "they emptied my account after", "I clicked a
   text from"). These surface local news cases that keyword searches miss.
2. **Local TV investigative units and consumer reporters** (any time window).
3. **Our help-line clusters** (`producer-kit/help-line-summary.md`, caller IDs only)
   and viewer emails. Three callers on one thing is a theme.
4. **Official alerts** (FTC, FBI IC3, state AGs, AARP, BBB Scam Tracker). Use these
   to confirm a theme is current and to source numbers, not as the idea
   source. Everyone else reads them too.
5. **Our own top Facebook posts and comments** for what our audience reacts to.

### d. Build each candidate out from the theme

For every theme that has heat or a strong case, write the pitch around it:

- **The beat**: the fear version, in one line, second person.
- **The cases**: two or three, each with a date and source, real loss first.
- **The variations**: the other forms the same scam takes (this is what makes
  it broad enough for an A; Ryan's "free sample *or* extreme discount").
- **The extended threat**: the beat that puts the viewer in personal danger.
- **The one move**: the protective advice in a sentence.
- **The peg**: its rung on the ladder.

If you can't write the cases line, the theme isn't ready; put it under THE GAP
with what's missing.

### e. Score and cut

Then run the existing kill list, coverage check and ranking (`ranking.md`).
Order the shortlist by clickability; break ties with the theme's lift in
`performance-map.md` before time-sensitivity.

## Off the list (don't pitch)

- **Refund and payout stories**: Amazon refunds, settlement or class-action
  money, "how to claim your money back." The team doesn't want them; they're a
  wallet story with no threat. A scam that *impersonates* a refund (a fake FTC
  refund call) is a scam and can be pitched under the impostor or phishing theme,
  framed on the threat, never the payout.
- **Deals and price comparisons as anything but the Friday deals slot.**
- Everything on the story board's dead list and Jeff's rules (Target-centered,
  not a scam for an A, too niche, our viewer is a spectator).

## Show the search in the pitch reply

Under the Step 1 shortlist, add one line: the themes searched, the windows, and
which candidates are new themes, returning themes or re-pitches. It lets the
user see the breadth at a glance and catch a repeat before Jeff does.
