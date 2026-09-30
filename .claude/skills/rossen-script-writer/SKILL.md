---
name: "rossen-script-writer"
description: Write or revise a Bible Script for the Jeff Rossen show (Rossen Reports) — the shooting outline Jeff runs off the teleprompter, with tease block, story segments, clip beats, graphics cues and sponsor placement. Use this whenever the user asks to write the script, draft this week's show, build a bible or Bible Script, write an F1 (Friday live) or F2 (taped, airs Wednesday) show or a call-in episode, hands over show topics or stories to be turned into a rundown, or asks to revise an existing bible for length, voice, story order or clip beats. Do not use for general writing, articles, blog posts, or scripts for any other show.
---

# Rossen Reports Bible Script writer

## Bundled files — load what the task needs

| File | Load when |
|---|---|
| `references/producer-kit/rossen-voice.md` | **Every draft and every voice pass.** Jeff's voice from five livestreams: show template, clip handling, tips, sponsor and deals handoffs, says/doesn't-say table, 12-point checklist. From the team; outranks this document where they differ. |
| `references/producer-kit/bible-format-ghost-tapping.md` | Laying out a live scam show. The Ghost Tapping skeleton every bible now follows, cue notation, common errors. |
| `references/producer-kit/call-in-show-format.md` | Any call-in F2. Run of show, the open that worked, taping-out-of-order rules. |
| `references/examples/bible-rewrite-nancy-mary.txt` | Writing or rewriting a call-in bible. Matt's rewrite of episode 2 (`.docx` beside it). |
| `references/producer-kit/facts-to-get-right.md` | Before any number goes in. |
| `references/producer-kit/sponsor-script-rules.md` | Only if asked to write or edit sponsor copy. |
| `references/producer-kit/youtube-description.md` | Only if asked for the YouTube description. |
| `reference-segments.md` | Checking format of record. **Verbatim aired segments; they outrank this document.** |
| `measurements.md` | Sizing a draft, checking voice, or arguing with a target. Every number and its provenance. |
| `docx-format.md` | Rendering the deliverable. |
| `scripts/check_bible.py` | **Before delivering. Always.** Mechanical compliance check. |
| `scripts/build_bible.py` | Rendering the `.docx`. |
| `scripts/verify_format.py` | Confirming the render matched house format. |

The workflow is **draft → check → fix → repeat → build → verify**. The checker
catches the things that reliably slip on a first pass — flat prosody, short
setup runways, malformed markers — so do not treat it as optional polish.

## First, and it governs everything: a bible is not a script

It is a **talking points outline that runs on Jeff's teleprompter** so he does
not get lost or off track during a live show. He improvises around it. He almost
never reads a line as written.

So never write a line whose value depends on him delivering it verbatim. No
crafted triplets, no punchlines, no rhetorical set-pieces that collapse if he
paraphrases. Write the things he **cannot** improvise:

- the exact figure, and who published it
- the proper nouns — company, agency, state, platform, product
- the mechanics of the scam, in the order they happen
- the turn into each clip
- the protection steps

He supplies the performance, the asides, and the outrage. The document supplies
the spine and the facts.

**Corollary that matters more than it looks:** the bible must carry *more*
searchable specifics than Jeff will actually say, because the clip pipeline only
ever reads the document.

### The aphorism trap

This rule gets broken by *good* writing, which is why it keeps getting broken.
These all came out of one draft:

> A GUARANTEE IS A PROMISE. AN ESTIMATE IS A GUESS. REMEMBER THAT.
> THAT IS BRILLIANT, AND IT IS EVIL.
> THIS IS EVERY RETAILER YOU SHOP AT. NOT ONE.

They are well-built lines. That is the problem. Each is a constructed symmetry
that collapses the moment Jeff paraphrases it, and he will. Nothing survives
except a half-remembered rhythm.

The aired equivalent is `THIS IS GENIUS AND SCARY!!` — a **reaction cue**. It
tells Jeff how to feel about the fact above it and leaves the wording to him.

Reaction cues yes, aphorisms no. If a line would sit comfortably in a
well-edited magazine article, cut it.

#### The paraphrase test — this is the discrimination that matters

A *permitted* mechanism reveal and a *banned* aphorism look almost identical on
the page. The test that separates them: **say the line in flat plain words. If
the point survives, the contrast was in the facts — keep it. If the point
evaporates, the contrast was in the sentence — cut it.**

| Line | Said flatly | Verdict |
|---|---|---|
| `EVERY OTHER SCAM TEXT THREATENS YOU. THIS ONE GIVES YOU SOMETHING.` | "unlike the others, this one offers you money instead of threatening you" | **Keep.** Point survives — it is a fact about the scam. |
| `YOUR GUARD DROPS, BECAUSE NOBODY EXPECTS FREE MONEY TO BE THE TRAP.` | "people don't suspect an offer of free money" | **Keep.** Point survives. |
| `A GUARANTEE IS A PROMISE. AN ESTIMATE IS A GUESS.` | "a guarantee and an estimate are different things" | **Cut.** Point evaporates. The line *was* the point. |
| `THIS IS EVERY RETAILER YOU SHOP AT. NOT ONE.` | "this affects all of them" | **Cut.** Point evaporates. |

**Watch for this specifically when adding intensity.** Pushing prosody is the
condition that manufactures aphorisms — a draft told to add spikes reaches for
sentence architecture, and produces `NOT TWENTY DOLLARS. NOT FIVE. ZERO.` or
`THAT IS ONE VAN… IN ONE TRAFFIC STOP.` Both die on paraphrase. **Intensity
comes from punctuation, caps and bold, which survive paraphrase — never from a
built sentence, which does not.** `check_bible.py` flags aphorism candidates; run
the paraphrase test on each one it names.

## Build stories out of people, not policies

The highest-leverage rule in threat stories, and the one most badly missed.

A story is **a sequence of humans, each with a mini-arc** — who they are, what
happened, the twist, what they did next. It is not a taxonomy of a company's
rules.

The aired ATM story is four people in a row: the couple at the glued Chase ATM,
the man who put his card in his own mailbox, the woman who opened her door to a
"bank employee," the woman at the LAPD detention center. Each gets a turn.

A rejected draft ran: guaranteed delivery policy → phantom delivery → A-to-Z
guarantee → settlement math → eligibility criteria. Five subtopics, no people;
victims appeared only as clip fodder, with no name, no situation, no turn.

The test: **Jeff can riff for ninety seconds on a woman who tracked down her own
stolen debit card. He cannot riff on the A-to-Z Guarantee.**

So when a beat's subject is a policy, a guarantee, a settlement, a regulation or
a dollar total, find the person it happened to and make them the subject. The
policy becomes the thing they ran into, not the thing the segment is about.

- Every clip beat has a human subject introduced **before** the clip, by
  identity: *a retired police officer*, *a 79-year-old widow*, *a famous
  behavioral researcher who teaches at Harvard*. Never introduce someone as
  "her" and roll.
- Policy and settlement mechanics are load-bearing facts, but they belong in the
  mechanics run and the protection list, not as the spine of the segment.

### Scope: this rule governs threat stories

Threat stories — scams, fraud, hidden fees, dangerous products, anything with a
victim. That is every A story (Jeff: an A story has to be a scam), most B
stories, and most Friday content stories.

**It does not govern a non-scam segment** — a consumer B or C story, a
money-saver, a what-not-to-buy — where there is no victim to identify and no
mini-arc to build. The aired 06/22 closer proves it:
its clip setup is `THIS SHOPPER SHOWS YOU WHAT TO KEEP OUT OF YOUR CART`. No
name, no identity, no arc, and it is in register.

For non-scam segments the clip beats are **demo and walkthrough beats** — a
creator showing you the aisle, an expert showing you the click path, Jeff on
location. Write them as: what you are about to be shown, why it will surprise
you, then the marker. An unidentified subject is fine. The searchable-specifics
rule still applies in full; it is the *people* rule that does not.

### When a threat story has no findable victim

A segment built on a rule, a fine or a settlement with no findable victim is a
weak segment. **Say so in the chat reply and propose a different angle rather
than writing it.** Do not quietly write the policy tour.

The reframe is almost always available: the ruling is not the story, the person
living under it is. A vacated robocall-consent rule becomes the person getting
seven spam calls a day — which is exactly the aired FAKE LOAN APPROVAL tease.
State the swap explicitly, then write the human version.

## Mid-story headers are turns, not labels

A mid-story header is **a spoken line that happens to be bold**, and the run of
them has to climb. Jeff reads them out loud; they are the escalation.

Aired, in order, from one story:

> BUT THE MOST SURPRISING THING YET WAS ABOUT TO HAPPEN TO THEM!
> THIEVES ARE STEALING YOUR DEBIT CARD, RIGHT OUT OF YOUR MAIL BOX!
> BUT THIS NEXT ATM / DEBIT CARD SCAM IS EVEN MORE DANGEROUS
> NOW, A SCAM SO SHOCKING, YOU NEVER WOULD EXPECT IT!!

Each is worse than the last. `THINK THAT'S BAD? HOW ABOUT THIS GUY` does the same
job. Rejected, from one draft: `THE GUARANTEED DELIVERY REFUND` /
`WHEN AMAZON SAYS NO - THE A-TO-Z GUARANTEE` / `NOW - THE SIZE OF THESE CHECKS`.
Those are article subheads. They file the material instead of escalating it, so
the story moves sideways to the next subtopic and never gets worse.

- Every mid-story header is sayable. If Jeff cannot read it aloud as a line of
  copy, it is a label. Rewrite it.
- The sequence escalates. Reach for `BUT`, `EVEN MORE`, `NOW`, `WORSE`,
  `THINK THAT'S BAD`, `AND THE SHOCKING DETAIL`.
- A noun phrase with no verb is almost always a label.
  `NOW - THE SIZE OF THESE CHECKS` becomes
  `NOW WAIT UNTIL YOU SEE HOW SMALL THESE CHECKS ACTUALLY ARE!!`
- Exception: the protection header is fixed and flat on purpose,
  `HERE'S HOW TO PROTECT YOURSELF`. That one never escalates.

## The hard contract with the clip pipeline

Scripts are parsed by `rossen-beat-extractor` and the rest of the harvest
pipeline. Break these and it fails **silently**, which is worse than failing
loudly. This section is not stylistic. `check_bible.py` enforces all of it.

### Clip markers

Every clip beat, on its own line, exactly three parens:

```
(((PLAY CLIP XXX HORIZONTAL)))
OUT:
```

or

```
(((PLAY CLIP XXX VERTICAL)))
OUT:
```

- `XXX` stays literal. It is the planning placeholder. Numbers get filled in
  before air, when the show is timed and clips are cropped.
- The `OUT:` line is always present, directly beneath, left blank.
- Leave URL and timecode lines blank. The pipeline fills them.
- Exactly three opening and three closing parens. Aired bibles contain typos
  with two, four and five parens, a hyphen before the orientation, and one with
  no orientation at all — those are mistakes. Normalize every time.

### Silent B-roll Jeff talks over

A recurring beat type that is **not** a sound-on clip: footage that runs mute
while he narrates. It sources differently, so mark it differently. Aired
documents write it several ways; use this one:

```
(((PLAY CLIP XXX VERTICAL BROLL)))
OUT:
```

The `BROLL` token tells the extractor to treat the beat as picture-only — no
outcue to find, no transcript to match. Without it a mute beat gets harvested as
a talking clip and the search comes back wrong. Aired precedents:
`(((PLAY CLIP 6 BROLL VERTICAL)))` on 06/22 and
`(PLAY CLIP SHOP WITH POINTS 2 HORIZONTAL - BROLL JEFF WILL TALK OVER)` on
06/26. Both are the same thing written inconsistently. Add
`**(JEFF TALK OVER)**` above the marker when it helps the control room.

### Not clip beats

Stills, art and screen work, all sourced separately. Never counted as clip beats:

```
(((TAKE ... SCREENSHOT)))
(((TAKE ... STILL)))
(((TAKE FULLSCREEN)))
(((CREATE FULL SCREEN GRAPHIC XXX)))
(((JEFF SCREEN SHARE)))
(((END SCREENSHARE)))
```

### Butt cuts

When one source will be cut into several segments, `BUTT` on its own line
between them. Roughly one beat in six.

### Orientation is a hard constraint, not a formatting detail

The pipeline will not search the other kind. Choose deliberately:

| Footage | Orientation | Where it lives |
|---|---|---|
| Victim telling their story to a reporter | HORIZONTAL | YouTube, network, local affiliate |
| Someone venting to their phone camera | VERTICAL | TikTok, Reels, Facebook |
| Doorbell cam, security cam, screen recording of a scam text | VERTICAL | TikTok, Facebook, Reddit |
| Reporter or creator confronting a scammer | either | pick by where that footage actually lives |

### The boundary marker

The pipeline drops everything before the first `HIT LIKE AND SUBSCRIBE` or
`JOIN THE CHAT` line. That marker closes the tease block every time, without
exception.

**Never put a `PLAY CLIP` marker inside the tease block, or inside a
`TEASE // SPONSOR` block.** The tease restates each story in beat language and
reads exactly like body copy; a marker in there produces an unresolvable
duplicate beat.

## The setup lines are the search query

This is the single highest-leverage thing in this skill. The 6 to 10 dash lines
immediately above a clip marker are the *only* thing the pipeline reads to
decide what footage to find.

Name the searchable specifics in the setup, even when Jeff would obviously say
them anyway:

- the dollar figure, exactly
- the relationship — *her mother*, *a retired police officer*, *this couple*
- the platform or company — Facebook Marketplace, PayPal, Zelle, Chase, Temu
- the agency — FBI, US Marshals, FTC, local police
- the object — gold bars, a leaf blower, a debit card, an empty white envelope
- the state or regulator, when a rule or fine is involved

Strong — produces a good search:

```
-A RETIRED POLICE OFFICER JUST LOST NEARLY $10,000.
-HE SPENT HIS CAREER PUTTING CRIMINALS AWAY...
-...AND A FAKE PAYPAL INVOICE GOT HIM.
-LISTEN TO WHAT HAPPENED TO HIM.

(((PLAY CLIP XXX HORIZONTAL)))
OUT:
```

Weak — produces a useless search:

```
-SCAMS LIKE THIS ARE EVERYWHERE.
-TAKE A LOOK.

(((PLAY CLIP XXX HORIZONTAL)))
OUT:
```

Do not shorten the runway to save space. **The runway is the input.**
`check_bible.py` errors on more than one runway under six lines.

He also expands on air, which is why over-specifying matters. The 06/22 bible
wrote `-WATCH WHAT HAPPENED TO THIS OLYMPIAN!!`; on air he added the retailer
(Walmart), the location (self-checkout) and the police. The pipeline heard none of
it, because the pipeline only reads the document.

### Setups plant a question, they do not make announcements

The runway carries the specifics *and* opens a loop the clip closes.

The tell of a dead setup is interchangeability. If it could be dropped above any
other clip in the show without breaking, it is doing no work:

> HERE'S WHAT WE KNOW RIGHT NOW.   (one draft used this four times)
> LISTEN TO WHAT HAPPENED TO HER.

Aired setups only fit the one clip they sit above, because each asks something
that clip answers:

> AND GUESS WHAT CHASE DID WHEN THEY COMPLAINED???
> YOU WON'T BELIEVE WHAT SHE FOUND!!!
> BUT HE DID GET A "SWEET SURPRISE" INSTEAD

Per clip beat:

- Identify the person by who they are before any pronoun — in threat stories.
- State what is at stake, then withhold the outcome. The clip is the payoff, so
  never summarize what happens in it.
- No role phrase repeats more than twice in a document. `HERE'S WHAT WE KNOW
  RIGHT NOW` is capped at **two** uses per bible — it is a wire-report signal,
  not a default lead-in.

### Lead-in phrasing sets the clip role

The last line before the marker tells the extractor what kind of footage this
is. Past scripts are consistent about this and the consistency is load-bearing.
Treat the table as the *final* line of a runway whose line above it asks the
question — a role phrase alone is not a setup.

| Lead-in | Signals |
|---|---|
| LISTEN TO WHAT HAPPENED TO HIM / THINK WHAT YOU WOULD DO | victim interview |
| WATCH WHAT HAPPENS WHEN / HE SET UP A REAL STING / BUSTED HIM IN THE ACT | confrontation or bust |
| CHECK THIS OUT / HERE YOU CAN SEE | evidence footage |
| HERE'S WHAT WE KNOW RIGHT NOW | network or wire report |
| WATCH HIM SHOW YOU HOW / LET ME SHOW YOU | explainer, demo or screen share |

### Dated news beats need their proper nouns

When a segment exists because something happened this week, put the specifics in
the copy: the company, the dollar amount, the agency, the state, the ruling.
*Temu fined $232 million by the EU.* *Maryland banning dynamic pricing.* Those
exact strings are the highest-yield search the pipeline can run. If they live
only in your head, the pipeline never sees them.

## Length

Full tables, per-block bands and provenance in `measurements.md`. The numbers
that shape the draft while writing it:

- **F2 story show (airs Wednesday):** A, B, usually C, plus an expert. 18–22
  pages and 1,700–2,300 spoken body words is the budget; confirm the story
  count and divide it, A story front-loaded hardest (about 40% of the body; 41–51
  bullets is a ceiling). Tease about 3 pages, 210–340 words.
- **Outside clips:** Matt's standard is about two per segment (see
  `measurements.md`; the older 10–12-per-show band came from the four-story
  format). Write to the material and flag when a story wants more.
- **Call-in F2:** two callers plus an expert, audio only. No clip band; follow
  `references/producer-kit/call-in-show-format.md`.
- **F1 (Friday live):** 10–12 pages. A lead story (sometimes a B) of F2
  quality with an expert, 0–4 clip beats, sponsor, then the deals guest.
- **Bullets average ~11.6 words.** Not five. Over-fragmenting is the most common
  failure mode.
- **Graphics are story-type conditional** — 0–1 in a threat story, 3–4 in a
  list-shaped closer. See `measurements.md`; do not apply a blanket ceiling.

## Structure

Full skeletons for both show days, and the Friday screen-share walkthrough
pattern, are in `running-orders.md`. Load it before laying out a document. What
governs regardless:

- **A live scam show follows the Ghost Tapping skeleton**
  (`references/producer-kit/bible-format-ghost-tapping.md`; that show did 1.2M):
  cold open with A, B, C headlines and the expert tease → like/subscribe/chat →
  A story: mechanics, victim clip, expert, escalation (`BUT IT GETS WORSE`),
  tease + sponsor, scale beat (`THIS IS NOT A ONE-OFF`), your bank might not have
  your back, practical close → B story, same shape, shorter, often a screen demo
  → C story → four numbered expert questions → deals block on Fridays.
- **Confirm the show type and story count before laying out.** F2 is either
  that story show or the call-in show. There is no required good-news closer.
- **The sponsor goes after the victim's story, never inside it or on a
  cliffhanger.** Tease what's next, then `BUT FIRST, A QUICK WORD FROM OUR
  SPONSOR`, then a personal bridge into the product. First read usually lands
  13–20 minutes in, after the lead story is told. Where the product connects to
  the story just told, bridge thematically. Take the sponsor from the assignment
  (OmniWatch is the usual; Chapter, Monarch and others also run). Disclose on air
  any guest who works for a sponsor or is related to staff.
- **Friday deals.** The deals half is not scripted. The live-request pitch, with
  specific examples (`YOU WANT A DYSON? TELL US.`), goes **before** the guest
  intro, then `TREY, WHAT'S GOING ON? LET'S GET RIGHT TO IT.` — never `HEY TREY,
  SO GREAT TO SEE YOU`. The guest has been Trey Donovan or Derek Couture of
  DealSeek; ask who's on and make every cue match (one bible named Derek on the
  deals page and cued Trey). Ask for the deal list and prices if not supplied;
  **do not invent products or prices.** Quote the current price from the deal
  link, not the deal sheet, and say when a price is Subscribe and Save. Three of the five Friday bibles in the
  library are built on a screen-share walkthrough rather than clip beats; that
  form has its own pattern in `running-orders.md`.

## Voice

Full corpus tables in `measurements.md`. What governs while writing:

**ALL CAPS is prompter ergonomics, not style.** He is scanning, not reading.

**The copy needs spikes, not a plateau.** `!!` and `!!!` on the lines that land,
throughout and not once per document — aired documents carry an exclamation on
roughly one spoken line in eight. `???` on a handoff question where it earns it.
**Inline bold inside a line** marking the words to hit: `PUTTING SUPERGLUE
INSIDE THE CARD SLOT`, `TAP TO PAY`. Lines that break the dash pattern to stand
alone, like `THIS IS GENIUS AND SCARY!!`. A draft with near-zero of these is
flat and needs another pass — not more words, just marked intensity. Re-read the
paraphrase test above before adding any of it.

**He says `you`, not `consumers`** — 4,587 times, one word in thirty. No anchor
connective tissue, no hedging, no formal register. `right now` is the single most
characteristic thing he says; write currency into the copy. The banned-word list
is in `measurements.md` and the checker errors on all of it.

### Ad-lib and first person

Two short rules with the detail, examples and counts in `measurements.md`:

- **Ad-lib stays out** — the 185 `by the way` asides, the close, the chat
  shout-outs. The document ends at `-END OF SHOW`. **But the team's line-level
  rules below override this for the open, the clip intros and the post-clip
  buttons**: Matt writes those into every bible he notes, because Jeff rewrites
  his lines an hour before the show and a page that already sounds like him
  saves him work.
- **First person: one or two lines per document, hard cap.** Lived, not
  editorial — `I HATE SCAMMERS, BUT I LOVE IT WHEN THEY GET BUSTED`.

**Hard honesty rule: never invent a fact about Jeff's life.** A draft wrote
`I DO THIS ON MY OWN ACCOUNT... IT TAKES ABOUT 90 SECONDS`. Nothing sourced that.
His habits, his accounts, his family, what he owns, what he has personally tried
— none of it goes in the document unless the user supplied it or a producer
confirmed it. When a first-person line would be good but you do not know it is
true, write it as an open decision instead:

```
(((JEFF - DO YOU DO THIS ON YOUR OWN ACCOUNT? IF SO, SAY SO HERE)))
```

## The team's line-level rules

From Matt Raub's notes on every recent bible and the voice profile
(`references/producer-kit/rossen-voice.md` — run its 12-point checklist before
delivering). These are written into the document:

- **The command hook.** After the slate (`WELCOME TO ROSSEN REPORTS. I AM JEFF
  ROSSEN.`), a direct order to the viewer with `YOU` in it, tied to the story, in
  the first 15 seconds: `DO NOT USE TAP-TO-PAY WHEREVER YOU SHOP UNTIL YOU WATCH
  THIS VIDEO.`
- **The open stacks stakes in threes, pre-empts the objection** (`AND BEFORE
  YOU'RE LIKE, "BIG DEAL." OH, IT'S A BIG DEAL.`), **promises proof** (`IT'S
  CAUGHT ON CAMERA`), **teases a human victim with a dollar figure**, and
  promises the fix.
- **Like and subscribe with the why** (`REALLY HELPS THE ALGORITHM... WE'RE
  INDEPENDENT, NO CORPORATE OVERLORDS`), where-are-you-watching-from, then the
  launch line `ALL RIGHT, LET'S GET RIGHT TO IT.`
- **Clip in: cue plus verdict**, as the runway's last line: `WATCH THIS. THIS IS
  CRAZY.` / `CHECK THIS OUT.` / `ROLL CLIP ONE. THIS IS NUTS.` Never `JUST
  WATCH` or `TAKE A LOOK`. The runway above it still carries the specifics and
  the question.
- **Clip out: a one-line button** that reacts and restates what the clip proved:
  `JUST THAT FAST, AND NOBODY KNOWS.` Never clip-to-clip or clip-to-header
  without one (a `BUTT` between segments of one source is the exception).
- **Tips are numbered** (`NUMBER ONE.`), each a command plus a reason. URLs and
  phone numbers are called to screen and repeated: `REPORTFRAUD.FTC.GOV. THERE IT
  IS ON THE SCREEN.`
- **The company's response is in the bible**, or `THEY DIDN'T GET BACK TO US.`
- **Hedge by attribution, never by softening:** `EMPLOYEES SAY`, `CONSUMER
  REPORTS FOUND`, `AND I'M QUOTING HERE`. No "on purpose" without evidence, no
  "told us" when they told someone else, no national claim from one state's
  data, no "never fixed" without dates, no vendor or advocacy statistic stated
  as settled fact.
- **Numbers as he says them:** `FIFTEEN THOUSAND`, `200 THOUSAND DOLLARS`, and
  the killer number repeated (`ONE IN THREE. ONE IN THREE KROGER STORES.`).
- **Words he doesn't say** (the checker errors on them): outrageous, totally
  amazing, functionally, discrepancies, fluctuations, furthermore, additionally,
  customers, shoppers, consumers, individuals, listeners, recently, currently.
  Say `viewers`, not `listeners`.
- **Every scam carries the extended threat** — the beat that puts the viewer in
  personal danger. **Get to the how-to faster**; viewers have asked for less
  preamble. **The ending closes**; it doesn't dissolve.
- **Links in the bible should be video.** Flag any clip that lives only on a
  news site so it gets pulled ahead of the taping.

Common errors to catch before delivering: a guest carried over from last week;
one guest named in copy and another in the cues; caps typos Jeff will read cold
(`SENIOR DIRECT`, `PRIVACY POLICE`); a placeholder left in (`MARY FROM TK`); an
image cue after the moment it illustrates; inconsistent guest credentials.

The aphorism ban and the paraphrase test still apply to all of it: a cue plus a
verdict is a reaction cue, not a built sentence.

## Leave the document open

A bible is a **working document the team marks up**, not a finished deliverable.
Aired bibles carry unresolved decisions in them, plus producer margin comments
asking Jeff whether he wants a graphic or a rapid-fire list.

A draft that answers every question and offers no choices reads finished, which
is worse for the workflow: it gives the team nothing to push back on and quietly
makes calls that belong to Jeff or the producer.

Carry **two or three open decisions** in every bible, as red production cues, at
the places where the call genuinely is not yours:

```
(((DECIDE CLIP A OR B - A IS THE VICTIM INTERVIEW, B IS THE BUST)))
(((JEFF - GRAPHIC HERE, OR DO YOU WANT TO RAPID-FIRE THE LIST?)))
(((PRODUCER - CONFIRM THIS FIGURE BEFORE AIR, SINGLE SOURCED)))
```

Open decisions are choices about staging and preference. They are not a licence
to leave research undone, and not a way to duck a call the material already
settles.

## Revising an existing bible

A marked-up bible coming back is as common as a new one. Do not regenerate the
document — **edit in place.** A rewrite loses the producer's accepted lines and
silently reverses decisions already made.

0. **Rewriting a whole bible** (not a targeted note): keep the formatting, the
   order, every fact, every cue, every guest line and the guests' timing.
   Rewrite Jeff's lines only. Truncate interviews so Jeff narrates the setup and
   the guest speaks at the three or four moments that need their voice. Flag
   factual problems as notes; never fix them silently.
1. **Read the whole bible first**, then locate what the note actually targets: a
   story, a beat, a header run, a length band, or the voice across the document.
2. **Change only that.** If a note says story 3 is long, cut story 3 — do not
   re-pitch story 2 or re-order the show.
3. **Watch the coupled constraints.** Cutting a story changes the clip count and
   the page total; cutting clips changes story 1's share of them; re-ordering
   stories moves the sponsor boundary. Re-check the tease block against any story
   that changed, since the tease restates each one.
4. **Preserve open decisions** that are still open. Close one only if the note
   closes it.
5. **Run `check_bible.py` on the revised file** and report what moved.
6. **Say what you changed and what you left**, briefly, in the chat reply. If a
   note cannot be followed without breaking a hard contract — the tease boundary,
   the marker format, a length band — say that instead of quietly splitting the
   difference.

For a voice or length pass across the whole document, work story by story and
re-run the checker after each, so a fix in one story does not push another out of
band.

## Research and honesty

Sometimes the stories arrive with the request; sometimes only a topic does. Be
ready for either. When researching:

- Go to primary sources — FTC, BBB Scam Tracker, FBI IC3, state AG, CFPB, court
  filings, company statements.
- Exact figures with source and date. Not rounded, not stale.
- Named victim cases and expert quotes, preferring original local reporting.
- Confirm recency. A scam trend from 2023 is not a story happening *right now*.

**Never invent a quote, statistic, victim, or source.** If it cannot be found,
say so and flag it. Mark anything single-sourced or inferred.

**Never invent a clip to reach a beat count.** If the supplied material carries
three clips and story 1 wants five to seven, write the three and flag the deficit
as a producer cue. The count is a target, not a licence.

**You cannot watch video.** You can find where a clip lives and describe it from
its transcript or description. You cannot confirm what is on screen or timestamp
a moment. Say so rather than implying otherwise.

**Do not add a sources or verification section to the document** — no reference
bible has one. Citations go inline as hyperlinks on the named source. The fuller
source rundown and verification notes go in the chat reply. See `docx-format.md`.

## Output

Deliver the bible as a `.docx` in house format, built with
`scripts/build_bible.py` and confirmed with `scripts/verify_format.py`. Full
spec, classification table and deliverables list in `docx-format.md`.

Red versus black is the whole point of the colour: **black is what Jeff says, red
is a production instruction.**

In the chat reply and not in the document: the clip manifest, then the source
rundown and anything needing a human check, then anything you declined to write
and why.

## Do not over-correct

Recent drafts got real things right. Fixing everything above must not cost these:
teaser architecture and the separator rules; the like/subscribe close; the
sponsor tease at a real story boundary in house phrasing; mechanism reveals that
pass the paraphrase test.

And keep the **operational specificity** — exact click paths, the settlement URL,
the hotline numbers. The aired bibles are lighter on this and it is genuinely
useful to Jeff. It lives in the mechanics run, the walkthrough and the protection
list, where it does not compete with the people.

## Self-check before delivering

Run `python3 scripts/check_bible.py draft.md --day wednesday   # or friday, callin` first and clear
every ERROR. It covers marker format, `OUT:` lines, tease-boundary violations,
runway depth, bullet-length distribution, exclamation rate, banned register,
lead-in repetition, and flags aphorism candidates. Then read for the things a
script cannot see:

- Re-read the user's actual instructions — show day, sponsor, guest name, story
  constraints — and confirm each was followed. State explicitly anything missed
  or assumed rather than silently deviating.
- Every threat story is a sequence of people with mini-arcs, not a tour of
  policies, and every clip beat introduces its human by identity before the clip.
- Any non-scam segment is a demo segment, not carrying an invented victim to
  satisfy the people rule.
- The voice profile's 12-point checklist passes: command hook, stakes, victim
  tease with a dollar figure, cue + verdict into every clip and a button out,
  escalators, numbers as figures, numbered tips with reasons, sponsor entered
  with a tease and a bridge, no doesn't-say words, the company's response.
- Guest and deals-guest names match between copy and cues.
- Any threat angle with no findable victim was flagged and re-pitched, not
  quietly written as a policy tour.
- Mid-story headers are sayable lines that escalate, not article subheads.
- No setup is interchangeable; each asks something its clip answers.
- Every aphorism candidate the checker named has been run through the paraphrase
  test, and the intensity in the draft comes from punctuation and bold rather
  than built sentences.
- Silent B-roll beats carry the `BROLL` token; screen-share segments use the
  screen-share cues, not clip markers.
- First person: one or two lines, lived not editorial, and nothing invented about
  Jeff's life.
- Two or three open decisions left for the team.
- Graphics count fits the story shape, not a blanket ceiling.
- No invented quotes, stats, sources, clips, products or prices; unverified items
  flagged inline.
- Nothing invented that no past bible contains. Follow the formula.

Then build and verify:

```bash
python3 scripts/build_bible.py draft.md "07_29 F2 BIBLE.docx"
python3 scripts/verify_format.py "07_29 F2 BIBLE.docx"
```
