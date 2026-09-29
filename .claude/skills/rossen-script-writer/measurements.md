# Measurements

Every number the house style rests on, with where it came from. Load this when
sizing a draft, checking voice, or arguing with a target.

- [Provenance and confidence](#provenance-and-confidence)
- [Document length](#document-length)
- [Line length and syntax](#line-length-and-syntax)
- [Prosody rates](#prosody-rates)
- [Graphics rates](#graphics-rates)
- [The negative space](#the-negative-space)
- [What he reaches for](#what-he-reaches-for)
- [Story selection](#story-selection)

## Provenance and confidence

Two tiers, and it matters which one a number sits in.

**Tier 1 — re-verified mechanically** against the eight bibles in the project
library plus the two aired segments in `reference-segments.md`. Trust these.

**Tier 2 — from the original 19-transcript / 141,477-spoken-word corpus**, which
included bibles no longer in the library. Not independently re-checkable. Still
the best available figure; treat as sound but not audited.

Where a Tier 2 target conflicted with the visible library, the range below has
been widened to cover both rather than picking a winner. Two targets moved this
way — the `???` rate and the graphics ceiling — and both are noted inline.

## Document length

Rendered in house format (Arial, 23/18pt, Letter, 1" margins, 1.15 spacing).

### Wednesday / F2 TOP STORIES

**The whole-document contract is fixed. The story count is not.** Confirm the
count before laying anything out; it changes only how the fixed budget divides.

| Block | Pages | Words | Bullets | Clips |
|---|---|---|---|---|
| Tease block | 3 | 210–340 | 9–21 | 0 |
| Body | 15–19 | 1,700–2,300 | ~136 | 10–12 |
| **Whole document** | **18–22** | **1,700–2,300** | **~136** | **10–12** |

Tier 1 on the whole-document row: the aired F2 07/10 bible measures 2,007 spoken
body words, 136 bullets, 11 clip beats. Tier 2 on the division below.

The tease is always 3 pages. **The A story is 40–55% of the body words and about
half the clips, in every shape.** Front-loaded far harder than feels natural.
Every story after A is lighter, and gets lighter as the rundown goes on.

### How the fixed budget divides, by shape

| Shape | Division |
|---|---|
| **A+B — the default** | A story 7–8 pages, 690–1,050 words, 41–51 bullets, 5–7 clips. B story 6–9 pages, 700–1,200 words, 4–6 clips. B is shorter than A but it is a full second segment, not a tag. |
| **3–5 story rundown** | A story keeps its 40–55% share. The rest split what's left, descending. Two-to-four pages and 0–3 clips each is normal; a trailing story with **zero** clip beats is normal and correct. |
| **Single-topic umbrella** (`TOP 5 FACEBOOK SCAMS`) | One subject, numbered sub-stories across the whole body. The strongest sub-story takes the A-story share and its clips; the rest run short and even, 1–2 clips each, some with none. |

**Never invent a beat, a graphic, or a victim to fill a slot.** If a story carries
two clips and the band suggests four, write the two and flag the deficit as a
producer cue. An empty trailing story is a correct extraction, not a gap.

**The A story is a ceiling, not a target.** 41–51 bullets and 5–7 clips. An A
story reaching ~75 bullets across seven headers is too long, and it almost always
means subtopics multiplied where people should have.

### Friday

10–12 pages total. One content story of Wednesday quality, then the guest. The
content story runs 0–4 clip beats — the aired 07/03 coupon-page show has **zero**,
because the segment is a screen-share walkthrough instead.

## Line length and syntax

Across 396 aired body bullets: **mean 11.6 words, median 11** (Tier 2).
Re-verified Tier 1: the F2 07/10 bible runs mean 11.9 / median 12; the ATM lead
story runs mean 12.5 / median 11. The target holds.

Only 8–14% of bullets run five words or shorter; roughly 60–68% land between 6
and 15. A bullet is a full clause carrying a fact, not a clipped fragment.
**Over-fragmenting is the most common failure mode** — it reads punchy and
delivers nothing.

Word count is not the whole rule — **syntax is.** Aired lines are clauses and
fragments with ellipses as breath marks, written to be said:

> -SO WHEN YOU TRY TO INSERT YOUR DEBIT CARD... IT WON'T GO IN... YOU THINK THE
> MACHINE IS BROKEN.
> -THAT'S EXACTLY WHAT THEY WANT.

Rejected drafts write complete sentences with subordinate clauses and appositive
lists, written to be read:

> -MORE THAN 400,000 PRODUCTS WERE COVERED BY THAT ORDER - FAULTY CO DETECTORS,
> UNSAFE HAIRDRYERS, FLAMMABLE KIDS' SLEEPWEAR.

Three ideas in one line, which becomes two or three lines in house style. So:
**one idea per line.** An appositive list is a signal to split — put the count on
one line and the examples on the next. Ellipses inside a line are breath marks
and belong there; a comma-spliced inventory does not.

## Prosody rates

Aired copy has volume changes written into it. A draft that reads at one constant
medium intensity gives Jeff no direction about where to push.

| Marker | Aired rate | Source |
|---|---|---|
| Lines carrying `!` or `!!` | **0.10–0.18 of spoken lines** | Tier 1: 0.114 (F2 07/10), 0.150 (ATM lead story) |
| `???` | **0–2 per document** | Tier 1: 1 in two of eight bibles, 0 in the other six |
| Inline bold runs | several per story | Tier 1: 26 in the ATM lead story, 72 across F2 07/10 |
| Dash-breaking standalone lines | a few per document | e.g. `THIS IS GENIUS AND SCARY!!` |

**The `???` target was revised down.** An earlier version of this skill required
"at least one `???` in every story with clips." Measured against the library that
is roughly four times the aired rate — six of eight bibles contain none at all.
So: `???` is a tool for the question that hands off to a clip, not a quota. Use
it where a handoff genuinely asks something. Do not manufacture one per story.

The exclamation rate is the one prosody number worth enforcing, because drafts
fail it in one direction only — flat. `check_bible.py` errors below 0.08.

Emphasis comes from punctuation, caps and bold, which survive paraphrase. It
never comes from a constructed sentence, which does not.

## Graphics rates

**Story-type conditional. This is not a document-wide ceiling.**

| Story shape | Graphic cards | Evidence |
|---|---|---|
| Threat / scam story | **0–1** | Tier 1: seven of eight bibles contain zero |
| List-shaped story or explainer — what-to-buy, price limits, a named-company run | **3–4 is in register** | Tier 1: the aired 06/22 what-not-to-buy segment has four `CREATE FULL SCREEN GRAPHIC` cards plus four `TAKE FULLSCREEN` logo cards |

An earlier version of this skill capped the whole document at one or two and
called four "over-produced." That is right for a threat story and wrong for a
list-shaped one — 06/22's what-not-to-buy segment is exactly the case that earns
cards, and it earns them because of what it is, not where it sits. The rule is
about whether the content **has to be read rather than heard**: a dated list, a
set of price limits, a click path, a run of company logos. If it can be said, say
it.

## The negative space

The tell of a generic consumer reporter. Raw occurrences across the 141k-word
spoken corpus (Tier 2). He essentially never says these:

| Word | Count | | Word | Count |
|---|---|---|---|---|
| `folks` | 2 | | `utilize` | 2 |
| `consumers` | 8 | | `individuals` | 1 |
| `however` | 2 | | `the bottom line` | 1 |
| `allegedly` | 3 | | `here's the thing` | 1 |
| `reportedly` | 1 | | `furthermore` / `moreover` | 0 |
| `alleged` | 0 | | `in conclusion` | 0 |

No anchor connective tissue. No hedging. No formal register. He says `buy` (113)
not `purchase` (8). He says `you`, not `consumers` — 4,587 times, roughly one
word in every thirty. `check_bible.py` errors on any of these.

## What he reaches for

| Phrase | Count | | Phrase | Count |
|---|---|---|---|---|
| `right now` | 347 | | `insane` | 32 |
| `you guys` | 187 | | `exploding` | 28 |
| `by the way` | 185 | | `brand new` | 25 |
| `crazy` | 65 | | `pause` | 24 |
| `watch this` | 34 | | `protect yourself` | 22 |

`right now` is the single most characteristic thing he says. Everything is
happening *right now*. Write currency into the copy.

Note two of these are **his, not the writer's**: `by the way` (185 occurrences,
none scripted) and `watch this` (his live handoff, spoken the instant before a
clip rolls). See the ad-lib rules in SKILL.md.

## What is ad-lib and stays out of the document

In every transcript, in zero bibles. These are his, not the writer's:

- The open — *"Welcome to Rossen Reports. I am Jeff Rossen"* plus an
  urgency-of-arrival line (*"had to get on the air,"* *"packed show today"*).
- The `by the way` asides. 185 of them, none scripted.
- `WATCH THIS` — his live handoff, spoken the instant before a clip rolls. Never
  write it. The setup lines above the marker are your job; that is his.
- The close — a plug for another video, then *"we'll see you next time."* Every
  show. Never in a bible. The document ends at `-END OF SHOW`.

## First person — lived, not editorial, and never invented

Sparse but real, and it is house style. **One or two per document, hard cap**,
usually in a hook:

- `I HATE SCAMMERS, BUT I LOVE IT WHEN THEY GET BUSTED`
- `THAT'S FREE MONEY YOU'VE EARNED AND I'D BE DEVASTATED IF I LOST MINE!`
- `I HAVE NEVER BEEN A FAN OF EXPIRATION DATES… I'LL SHOW YOU WHY`

The good ones give him **his own experience as raw material** — what he
received, what his team sees, what he has never seen before: `LIKE THIS ONE I
RECEIVED!`. Weaker drafts substitute editorial opinion — `I HATE THAT IT TAKES A
FEDERAL LAWSUIT...` — and then use more of it than the cap allows.

**Hard honesty rule: never invent a fact about Jeff's life.** A draft wrote
`I DO THIS ON MY OWN ACCOUNT... IT TAKES ABOUT 90 SECONDS`. Nothing sourced
that. His habits, his accounts, his family, what he owns, what he has personally
tried — none of it goes in the document unless the user supplied it or a producer
confirmed it. When a first-person line would be good but you do not know it is
true, write it as an open decision instead:

```
(((JEFF - DO YOU DO THIS ON YOUR OWN ACCOUNT? IF SO, SAY SO HERE)))
```

## Story selection

Channel top performers: DEBIT CARD ALERT (1.5M), THESE Apps Are SPYING on You
(1.4M), They Know You're STEALING at Self-Checkout (1M), GENIUS Envelope Scam
(885K), 5 Walmart Scams (810K), GENIUS Tipping Scam (807K).

Every one takes something the viewer already does every single day — a debit
card, phone apps, self-checkout, the mail, Walmart, a tipping screen — and turns
it against them. None is an exotic fraud. **The mundane daily object weaponized
is the pattern.** `GENIUS` is his word for a cleverly built scam and it recurs in
the titles that perform.

When ranking candidate angles, prefer the one that violates the body, the home,
or privacy over the one that only costs money. For a story about a rental
platform, the booking-fee scam is the default angle and hidden cameras is the
real one. Same topic, different beat, and the second one performs.
