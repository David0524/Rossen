---
name: "rossen-script-writer"
description: Write or revise a Bible Script for the Jeff Rossen show (Rossen Reports) — the shooting outline Jeff runs off the teleprompter, with tease block, story segments, clip beats, graphics cues and sponsor placement — plus its companion source log. Use this whenever the user asks to write the script, draft this week's show, build a bible or Bible Script, turn an approved outline (with videos) into the bible, promote a draft bible to final, write an F1 (Friday live) or F2 (taped, airs Wednesday) show or a call-in episode, hands over show topics or stories to be turned into a rundown, or asks to revise an existing bible for length, voice, story order or clip beats. Do not use for general writing, articles, blog posts, or scripts for any other show, for pitching stories (rossen-pre-bible) or for finding and grading clips (rossen-story-outline).
---

# Rossen Reports Bible Script writer

## Bundled files — load what the task needs

| File | Load when |
|---|---|
| `references/line-rules.md` | **Every draft and every voice pass.** The team's line-level rules: open, clip in/out, tips, hedging, first person. |
| `references/producer-kit/rossen-voice.md` | Every draft. Jeff's voice from five livestreams and the 12-point checklist. |
| `references/clip-contract.md` | Placing clip beats; any marker error from the checker. DRAFT/FINAL markers, BROLL, orientation, lead-ins. |
| `running-orders.md` | Laying out a document. Skeletons for every show shape and the Friday walkthrough. |
| `references/producer-kit/bible-format-ghost-tapping.md` | Background on the skeleton every scam bible follows. |
| `references/producer-kit/call-in-show-format.md` | Any call-in F2. |
| `references/examples/bible-rewrite-nancy-mary.txt` | Writing or rewriting a call-in bible. |
| `references/revising.md` | A marked-up bible coming back; a voice or length pass; promoting DRAFT to FINAL. |
| `references/examples/bible-sent-10-14.txt` | **Every story-show draft.** The 10/14 F2 as the producer sent it to Jeff, after her edits. What a finished FINAL looks like (`.docx` beside it). |
| `references/examples/ryan-notes-2026-10-09.md` | **Every draft.** Ryan's 11 structure and retention notes on the 10/09 F1, with before/after pairs. The worked example for "Retention: Ryan's structure rules". |
| `review-loop.md` | **Every new bible or whole-bible rewrite, before building.** The BLOCKER-only reviewer loop: the agent prompt, the fix rules, the two-round stop. |
| `references/producer-kit/facts-to-get-right.md` | Before any number goes in. |
| `reference-segments.md` | Checking line-level layout against aired copy. |
| `measurements.md` | Sizing a draft, checking voice, or arguing with a target. |
| `docx-format.md` | Rendering both deliverables. |
| `references/producer-kit/sponsor-script-rules.md` | Only if asked to write or edit sponsor copy. |
| `references/producer-kit/youtube-description.md` | Only if asked for the YouTube description. |
| `scripts/check_bible.py` | **Before delivering. Always.** |
| `scripts/build_bible.py`, `scripts/build_source_log.py`, `scripts/verify_format.py` | Rendering and confirming. |

The workflow is **draft → check → fix → repeat → review loop → build →
verify**. The review loop (`review-loop.md`) runs the final reviewer on the
draft in a background agent and fixes **BLOCKERs only**: wrong facts, unsafe
advice, legal exposure. It stops after two rounds, and every WARNING and NOTE
goes to the producer untouched.

## Precedence — one order, applied everywhere

When two sources disagree, the higher one wins:

1. The user's instruction in this session.
2. **Standing production rules** (next section) and the rest of this SKILL.md.
3. `references/line-rules.md` and `references/clip-contract.md`.
4. `reference-segments.md` — aired copy, the record for line-level layout and
   register, but not for marker syntax (aired typos are normalized) or for rules
   the team has since changed.
5. The producer-kit files and `running-orders.md`.
6. `measurements.md` — corpus numbers, which describe what aired, not what is
   required.

If a lower file contradicts a higher one, follow the higher one and mention the
conflict in the chat reply so the file can be fixed.

## Standing production rules — apply without asking

- **Sponsor is OmniWatch.** Never ask. Two breaks in one Wednesday is normal.
  Mark placement and write the tease into each break; write the sponsor copy
  only if asked. When the outline names a different sponsor for a break (10/14's
  second break was Chapter), use the outline's.
- **Wednesday default is one A story plus one small B story.** A 3–5 story
  rundown and a single-topic umbrella show (`TOP 5 FACEBOOK SCAMS`) are standard
  variants. Confirm the story count before laying out; if the user hasn't said,
  ask once, and if you must proceed, use A + B and say so. Each story after A is
  lighter; a trailing story with zero clip beats is normal. There is no
  good-news closer.
- **Friday's deals guest is Trey Donovan** (co-founder of DealSeek). Use another
  name only if the user gives one, and then make every cue match.
- **Outside clips: about two per segment** (Matt's standard), counted
  separately from BROLL, screen shares and demos. Write to the material the
  outline carries; never invent a clip to fill a slot.
- **Clip age is not a flag.** Footage back to 2010 is fine; don't annotate age.
  The only constraint: old footage never sits under a "brand new" or "this week"
  line, and the news peg must be current.
- **US cases first.** Canadian cases are acceptable support; a US case leads.
- **Deals stories belong to Friday**, not Wednesday.
- **Target is not off-limits, but never the title or the main story** (Jeff,
  10/7). A passing mention inside a bigger story is fine.
- **The audience is 55+.** Nothing kids-focused, and never address the viewer
  as someone's grown child (`YOUR PARENTS`).

## Input and stage

The bible is written **from the approved Outline w/ Videos** (`rossen-story-outline`):
the beats, the clip picked for each, its transcript excerpt, orientation and
timecodes. The pre-bible pitch sheet is upstream of that and is a weaker input —
it has unwatched candidate clips and stories Jeff hasn't approved.

Decide the stage first and say which one you are writing:

| Stage | When | Clip markers | `OUT:` |
|---|---|---|---|
| **DRAFT** | Clips not yet locked, or only a pre-bible / topic was supplied | `(((PLAY CLIP XXX HORIZONTAL)))` | blank |
| **FINAL** | The outline's clips are picked, transcribed and timed | `(((PLAY CLIP 1 HORIZONTAL)))`, numbered in air order | the transcribed outcue, then the red source line |

**Clips come first (producer, 10/7/2026).** The clip pipeline runs on the
approved outline before the bible is written, so the normal case is a FINAL
written from the Outline w/ Videos with its clips already picked, numbered and
timed. A FINAL clip beat is the marker, `OUT:` with the outcue, then one red
source line exactly as the outline's Videos row gives it (the sent 10/14 bible
is the model):

```
(((PLAY CLIP 3 HORIZONTAL)))
OUT: (FINAL OUTCUE)
((([Outlet](URL) · 0:18 - 0:53 (OUTCUE) · BUTT · 1:03 - 1:26 (OUTCUE))))
```

A MANUAL clip (no transcript) keeps a blank `OUT:` and just the link line.
Never add, cut, move or swap a clip from the outline without saying so.

If you are handed a pre-bible instead of an outline, write a DRAFT, use only the
stories the user names (or the sheet's recommended slate, stated as an
assumption), and say in the reply that the outline stage hasn't run. Carry every
NEEDS VERIFICATION flag from the sheet forward — those are hard constraints on
the copy, not background.

Promoting a DRAFT to FINAL is an in-place edit; see `references/revising.md`.

## First, and it governs everything: a bible is not a script

It is a **talking points outline that runs on Jeff's teleprompter** so he does
not get lost or off track during a live show. He improvises around it. He almost
never reads a line as written.

So never write a line whose value depends on him delivering it verbatim. Write
the things he **cannot** improvise:

- the exact figure, and who published it
- the proper nouns — company, agency, state, platform, product
- the mechanics of the scam, in the order they happen
- the turn into each clip
- the protection steps

He supplies the performance, the asides, and the outrage. The document supplies
the spine and the facts. **In a FINAL, the bible carries what Jeff says, and no
more**: the clips are already chosen, so product model names, towns, timelines,
the accused's age and bond, parent companies and reporters' names stay in the
outline and the source log (see "What the producer cuts before it goes to
Jeff"). **In a DRAFT**, before clips exist, the runway is still the pipeline's
search query, so it carries more searchable specifics than Jeff will say.

### The aphorism trap

These all came out of one draft:

> A GUARANTEE IS A PROMISE. AN ESTIMATE IS A GUESS. REMEMBER THAT.
> THAT IS BRILLIANT, AND IT IS EVIL.
> THIS IS EVERY RETAILER YOU SHOP AT. NOT ONE.

Well-built lines — that is the problem. Each is a constructed symmetry that
collapses the moment Jeff paraphrases it. The aired equivalent is `THIS IS
GENIUS AND SCARY!!` — a **reaction cue**. It tells Jeff how to feel about the
fact above it and leaves the wording to him. If a line would sit comfortably in
a well-edited magazine article, cut it.

#### The paraphrase test

A permitted mechanism reveal and a banned aphorism look almost identical. **Say
the line in flat plain words. If the point survives, the contrast was in the
facts — keep it. If the point evaporates, the contrast was in the sentence — cut
it.**

| Line | Said flatly | Verdict |
|---|---|---|
| `EVERY OTHER SCAM TEXT THREATENS YOU. THIS ONE GIVES YOU SOMETHING.` | "unlike the others, this one offers you money" | **Keep.** A fact about the scam. |
| `YOUR GUARD DROPS, BECAUSE NOBODY EXPECTS FREE MONEY TO BE THE TRAP.` | "people don't suspect free money" | **Keep.** |
| `A GUARANTEE IS A PROMISE. AN ESTIMATE IS A GUESS.` | "they're different things" | **Cut.** The line was the point. |
| `THIS IS EVERY RETAILER YOU SHOP AT. NOT ONE.` | "this affects all of them" | **Cut.** |

**Watch for this when adding intensity.** A draft told to add spikes reaches for
sentence architecture (`NOT TWENTY DOLLARS. NOT FIVE. ZERO.`). **Intensity comes
from punctuation, caps and bold, which survive paraphrase — never from a built
sentence.** `check_bible.py` lists aphorism candidates; run the test on each.

## Build stories out of people, not policies

A threat story is **a sequence of humans, each with a mini-arc** — who they are,
what happened, the twist, what they did next. The aired ATM story is four people
in a row: the couple at the glued Chase ATM, the man who put his card in his own
mailbox, the woman who opened her door to a "bank employee," the woman at the
LAPD detention center. A rejected draft ran guaranteed-delivery policy → A-to-Z
guarantee → settlement math → eligibility. No people.

**Jeff can riff for ninety seconds on a woman who tracked down her own stolen
debit card. He cannot riff on the A-to-Z Guarantee.** When a beat's subject is a
policy, a settlement or a dollar total, find the person it happened to and make
them the subject.

- Every clip beat in a threat story introduces its human **before** the clip,
  by identity — never "her," then roll.
- **Identity comes from the source, never from inference.** Use what the
  reporting says: name, age, place, relationship, job. Do not upgrade it to make
  the person vivid — no `GRANDMOTHER`, `WIDOW`, `RETIRED`, `LIFE SAVINGS`,
  `SINGLE MOM` unless a source says so. If all you have is
  `KAREN WHITAKER, 79, BERMUDA DUNES`, that is the introduction. The same rule
  covers what happened: no detail about the scam, the loss or the outcome that
  the source doesn't state.
- Policy and settlement mechanics belong in the mechanics run and the protection
  list, not as the spine.

**Scope.** The rule governs threat stories — scams, fraud, hidden fees,
dangerous products, anything with a victim. A non-scam segment (a money-saver, a
what-not-to-buy) uses demo and walkthrough beats instead: what you are about to
be shown, why it will surprise you, then the marker. An unidentified subject is
fine there (`THIS SHOPPER SHOWS YOU WHAT TO KEEP OUT OF YOUR CART`).

**No findable victim** in a threat story means a weak segment. Say so in the
chat reply and propose the human angle rather than writing the policy tour — the
vacated robocall rule becomes the person getting seven spam calls a day.

## Mid-story headers are turns, not labels

A mid-story header is a spoken line that happens to be bold, and the run of them
has to climb. Aired, in order, from one story:

> BUT THE MOST SURPRISING THING YET WAS ABOUT TO HAPPEN TO THEM!
> THIEVES ARE STEALING YOUR DEBIT CARD, RIGHT OUT OF YOUR MAIL BOX!
> BUT THIS NEXT ATM / DEBIT CARD SCAM IS EVEN MORE DANGEROUS
> NOW, A SCAM SO SHOCKING, YOU NEVER WOULD EXPECT IT!!

Rejected: `THE GUARANTEED DELIVERY REFUND` / `NOW - THE SIZE OF THESE CHECKS`.
Those file the material instead of escalating it. Every mid-story header is
sayable and the sequence escalates (`BUT`, `EVEN MORE`, `NOW`, `WORSE`, `IT GETS
CRAZIER`, `WAIT UNTIL YOU HEAR THIS`, `YOU AREN'T GOING TO BELIEVE THIS
VIDEO…`). A noun phrase with no verb is almost always a label. The protection
header is fixed and flat on purpose: `HERE'S HOW TO PROTECT YOURSELF`.

## The hard contract with the clip pipeline

Scripts are parsed by `rossen-beat-extractor` and the rest of the pipeline.
Break these and it fails **silently**. `check_bible.py` enforces all of it; full
detail and variants in `references/clip-contract.md`.

- Every clip beat on its own line, three parens each side, orientation always:
  `(((PLAY CLIP XXX HORIZONTAL)))` in DRAFT, `(((PLAY CLIP 1 HORIZONTAL)))` in
  FINAL. `OUT:` directly beneath — blank in DRAFT, the outcue in FINAL.
- **Under `OUT:` in a FINAL, one red source line and nothing else** —
  `((([Outlet](URL) · in - out (OUTCUE) · BUTT · …)))`, as in the sent 10/14
  bible. No clip-context block, no transcript, no description: those go in the
  companion source log, which also carries every link and timecode. A DRAFT has
  nothing under the marker.
- Mute footage Jeff talks over carries `BROLL`:
  `(((PLAY CLIP XXX VERTICAL BROLL)))`.
- Stills, graphics and screen shares use their own cues and are never clip beats.
- Orientation is a hard constraint: the pipeline will not search the other kind.
- The tease block closes on `HIT LIKE AND SUBSCRIBE` / `JOIN THE CHAT`, every
  time. **Never a `PLAY CLIP` marker inside the tease or a sponsor tease.**

## The setup lines are the search query (in a DRAFT)

In a FINAL the clip is already chosen: write the 6 to 10 dash lines to it, from
its transcript excerpt in the outline, setting up the person and the question
it answers. Six lines of the *story*, not six lines of search terms. The rest of
this section governs a DRAFT.

In a DRAFT, the 6 to 10 dash lines immediately above a clip marker are the *only* thing the
pipeline reads to decide what footage to find. Name the searchable specifics
there, even when Jeff would obviously say them: the dollar figure exactly, the
relationship, the platform or company, the agency, the object, the state or
regulator.

Strong:

```
-A RETIRED POLICE OFFICER JUST LOST NEARLY $10,000.
-HE SPENT HIS CAREER PUTTING CRIMINALS AWAY...
-...AND A FAKE PAYPAL INVOICE GOT HIM.
-LISTEN TO WHAT HAPPENED TO HIM.

(((PLAY CLIP XXX HORIZONTAL)))
OUT:
```

Weak: `-SCAMS LIKE THIS ARE EVERYWHERE.` / `-TAKE A LOOK.` Do not shorten the
runway to save space; `check_bible.py` errors on more than one runway under six
lines. He expands on air — the 06/22 bible wrote `WATCH WHAT HAPPENED TO THIS
OLYMPIAN!!` and on air he added Walmart, self-checkout and the police. The
pipeline heard none of it.

When a segment exists because something happened this week, put the proper
nouns in the copy: *Temu fined $232 million by the EU*. Those exact strings are
the highest-yield search the pipeline can run.

### Setups plant a question — one the clip actually answers

The runway opens a loop the clip closes. The tell of a dead setup is
interchangeability: if it could sit above any other clip in the show, it does no
work (`HERE'S WHAT WE KNOW RIGHT NOW` four times in one draft). Aired setups fit
only their clip: `AND GUESS WHAT CHASE DID WHEN THEY COMPLAINED???`

- State what is at stake, then withhold the outcome. Never tell the payoff
  before the clip rolls — a recovery, an arrest or a death the clip reveals
  belongs in the button after it, not the runway.
- **The question must be one the clip answers.** In FINAL, build it from the
  outline's transcript of that clip. In DRAFT, when nobody has watched the clip,
  build the question only from facts the source reporting states — never from a
  guess about what the clip shows, and never from foreshadowing the source
  doesn't support (`SHE HAD NO IDEA WHERE THIS WAS HEADED` implies a link
  between events that a pre-bible flag may forbid). If no honest question is
  available, use a plain role lead-in and move on.
- No role phrase repeats more than twice in a document.

## What the producer cuts before it goes to Jeff

Learned from the 10/14 bible: the draft (1,744 spoken words, 10 clips) against
the version the producer sent (1,373 words, 9 clips). The full sent text is in
`references/examples/bible-sent-10-14.txt`. Write the first draft this way so
the producer is not making the same cuts every week.

**No other news outlet is named in a spoken line.** Extremely rare exceptions
only, and the producer makes them. `CBS LOS ANGELES CAUGHT ONE STORE` became
`THIS REPORTER CAUGHT ONE STORE`; `THE OWNER TOLD ABC15` became `THE OWNER
SAID`; `WMBF NEWS PULLED THE PAPERWORK` became `THE NEWS PULLED THE PAPERWORK`;
`INSIDE EDITION COULDN'T REACH HER` became `REPORTERS COULDN'T REACH HER`;
`CBS REPORTS LAPD IS INVESTIGATING` became `LAPD IS INVESTIGATING`. Outlets
still appear in the red clip source lines, which Jeff does not read. Agencies,
police departments, regulators, courts and companies are still named.

**Victims: first name or "this woman," never a surname.** `KATHRYN TAYLOR IS
84` became `THIS WOMAN IS 84`; `LETTIE IS 79` became `NOW THIS WOMAN IS 79`;
`NORA ROWLAND` became `NORA`; `JIMMY WRIGG` became `THIS MAN`. A first name the
victim used on camera is fine (Donna, Amanda, Nora). Identify people by who
they are (age, situation), which still satisfies the people rule. **The
accused keep their full names**, with the police department and the charge.

**Locate by state, not by town.** `IN FLORIDA…` / `AND IN ARIZONA…` / `BUT IN
WASHINGTON STATE…` as the victim headers, so the geography does the escalating.
Cities, the victim's home state of origin and street-level detail come out.

**Cut what Jeff won't say.** The producer cut product model names (`GENESIS
Z`, `SAPPHIRE X`), timelines with dates (`MARCH 2024… APRIL 17TH…` became
`WITHIN WEEKS OF TAKING THE JOB`), the accused's age, bond and next court
date, the parent company, the congressman, the reporter's name, the victim's
late father's name and job, and callbacks to past shows (`WE TOLD YOU ABOUT
THESE BACK IN MAY`). One fact per line, only the facts that move the story.

**The viewer is 55+: they are the family, not the adult child.** `TALK TO YOUR
PARENTS` became `TALK TO YOUR FAMILY`; `IF YOU HAVE A PARENT WITH HELP AT
HOME` became `IF YOU HAVE LOVED ONES WITH HELP AT HOME`. Never write the viewer
as someone's grown child looking after an elderly parent.

**Feelings over puzzles.** `SO WHY WOULD SHE KEEP A $26,000 BILL A SECRET???`
became `SHE WAS SO ASHAMED, SHE DIDN'T TELL ANYBODY.` Say why a victim did
what they did when the source says it; save the `???` for the handoff into a
clip.

**Make small numbers hit.** `A DOLLAR 44!!` gained `ALMOST 50 PERCENT MORE THAN
THE SALE PRICE`. Translate a small dollar gap into a percentage, a total or a
yearly cost. Explain a product in a word when the audience may not know it:
`RING VIDEO DOORBELL`.

**Attribution: keep it where it protects the show, drop it where it doesn't.**
`SHE'S ACCUSED, NOT CONVICTED` and `WARRANTS ALLEGE` stay. But a settled fact
loses the hedge (`SHE SAYS THE CHARGES WERE DROPPED` became `THE CHARGES WERE
LATER DROPPED BUT STILL…`), and a quote the family gave on camera does not need
`HER FAMILY SAYS`. A trailing `BUT STILL…` hands Jeff the riff.

**Lead-ins are short:** `LISTEN TO THIS.` / `LOOK AT THIS.` / `WATCH WHAT
HAPPENED.` The question above carries the setup.

**The tease and the "next" lines hide the payoff.**
- `HIS CAREGIVER ANSWERS: YOUR DAD DIED` became `HIS CAREGIVER ANSWERS… WITH
  SHOCKING NEWS`.
- The C tease stopped naming the store (Walmart) and the outcome (the
  register charges more). Set up the moment, cut before the payoff.
- `NEXT, THE WALMART REGISTER THAT CHARGED MORE THAN THE SIGN` became `NEXT,
  THE STORE CHECKOUT THAT CHARGED TOO MUCH`. A "next" line is a tease too.
- Three or four lines per story in the tease; join two beats on one line with
  `…`. End the A tease on the promise of the fix (`PLUS THE ONE MOVE THAT
  STOPS THIS BEFORE IT STARTS.`).
- **The body does not repeat the tease's headline.** Each story opens on a new
  header that puts the viewer in the moment: `WHAT REALLY HAPPENS WHEN YOU SIT
  DOWN FOR THAT FREE DEMO`; `YOU TRUST THEM WITH YOUR DAD… THEN THE DEED HAS
  THEIR NAME ON IT`; `THE PRICE ON THE SHELF ISN'T ALWAYS WHAT YOU PAY`.

**One clip per person.** Where two clips cover the same person or the same
store, the producer folds them into one beat (10/14 dropped the separate
Chisholm interview and kept the store package). Flag it rather than doing it
silently, since it changes the outline.

**Scale beat early in a consumer C story:** `AND IT'S NOT JUST ONE STORE. LAST
YEAR [CHAIN] AND [CHAIN] STORES WERE FINED FOR…`, before the first clip.

**Graphics:** when a protection list becomes a full-screen graphic, put
`(((INSERT GRAPHIC 001)))` (bold red) directly under its `HERE'S HOW TO PROTECT
YOURSELF` header, numbered in show order, and write the ChatGPT image prompt in
the chat reply.

**Bold:** roughly one bold phrase in about half the spoken lines: the figure,
the place, the company, the key thing to do (`**WATCH THE SCREEN**`, `**THE
SAME DAY**`). Not whole lines.

**Open decisions** still go in the draft (see "Leave the document open"), but
they are for the producer: the version sent to Jeff has none. They get
answered and removed before it goes out.

## Length

Size by the confirmed story count (`check_bible.py --stories N` does the same).
Measured bands and provenance in `measurements.md`.

- **A story:** front-loaded hardest — roughly 600–850 spoken words, a ceiling of
  about 50 bullets. A story reaching ~75 bullets means subtopics multiplied where
  people should have.
- **Each later story:** roughly 230–520 words, lighter as it goes.
- **Tease:** the open plus a headline block per story, about 60–80 words a
  story.
- **F1 (Friday live):** 10–12 pages; a content story of Wednesday quality with
  0–4 clip beats, sponsor, then the deals guest.
- **Call-in F2:** no length bands; follow `call-in-show-format.md`.
- **Reference point:** the 10/14 F2 as sent (three stories, no expert)
  measured 1,373 spoken body words and 9 clips; its draft ran 1,744 and the
  producer cut it down. Write to the per-story bands, not up to them.
- **Bullets average ~11.6 words.** Over-fragmenting is the most common failure.
  One idea per line; ellipses as breath marks.
- **Graphics are story-type conditional** — 0–1 in a threat story, 3–4 in a
  list-shaped closer.

## Structure

Skeletons for every show shape are in `running-orders.md`. What governs
regardless:

- **The scam-story spine:** mechanics, victim clip, **the tell**, expert,
  escalation (`BUT IT GETS WORSE`), tease + sponsor, scale beat (`THIS IS NOT A
  ONE-OFF`), your bank might not have your back, practical close. B is the same
  shape, shorter, often a screen demo. Lead with the most fear-inducing story,
  not the biggest dollar figure.
- **Every victim case ends with a tell — a usable takeaway before the next case
  starts.** One line, after the case's last clip button: `-HERE'S THE TELL:
  NOBODY FROM A STORE DRIVES YOU TO THE BANK.` Don't hold all the advice for the
  guest or the closing list; the best-performing live shows hand the viewer
  something useful throughout (Ryan, Oct 8, 2026: "four clips run before any
  protection tip"). The closing `HERE'S HOW TO PROTECT YOURSELF` list still runs,
  and may repeat a tell as a numbered step. The tell is Jeff's line, not the
  expert's. The checker warns on three sound clips with no `THE TELL`, `THE RED
  FLAG` or protection line between them.
- **Inside a story, lead with the case where the money is actually gone.** A
  real loss sets the stakes; a near-miss (stopped by a bank teller, caught in
  time) is a strong warning but lands second. Ryan, on 10/14: "Move the $26k scam
  first since the victim actually lost money." The header follows the lead case,
  so `COST HER $26,000` beats `ALMOST COST HER $50,000`. This orders *cases
  within a story*; the rule above orders *stories within a show*.
- **Every promise in the tease is paid off by name.** If the tease says `THE ONE
  MOVE`, `THE 5-SECOND HABIT` or `THE ONE PIECE OF PAPER`, the body says that
  phrase where it lands: `-HERE'S THE ONE MOVE I PROMISED YOU: DON'T SIT DOWN.`
  An unlabeled payoff reads as a broken promise to a live viewer. The checker
  errors on any tease promise the body never repeats.
- **Frame the scam as broadly as its cases are.** Every noun in a story's header
  and tease lines has to be true of every case in it. When the cases come in
  different ways — one through a free sample, one through a cheap facial — name
  both (`A FREE SAMPLE OR A CRAZY DISCOUNT`) or step up a level (`STORE`, not
  `MALL`, when not every case is in a mall). Narrow framing shrinks the audience
  and is inaccurate about the cases it doesn't fit.
- **Experts are named only when booked.** If the user or the outline hasn't
  confirmed the guest, write `(EXPERT JOINS THE ROOM)` in the story, keep the
  tease generic (`A FRAUD EXPERT JOINS ME`), and carry the suggested name as an
  open decision: `(((PRODUCER - EXPERT NOT BOOKED. SUGGESTED: AMY NOFZIGER, AARP.
  CONFIRM OR CUT)))`. Never put an unbooked person's name or organization in
  black copy.
- **The sponsor goes after the victim's story, never inside it or on a
  cliffhanger.** Tease what's next, then `BUT FIRST, A QUICK WORD FROM OUR
  SPONSOR`, then a personal bridge into OmniWatch. First read usually lands 13–20
  minutes in. A second break is fine at the next real story boundary. Disclose on
  air any guest who works for a sponsor or is related to staff.
- **Friday deals are not scripted.** The live-request pitch with specific
  examples (`YOU WANT A DYSON? TELL US.`) goes **before** the guest intro, then
  `TREY, WHAT'S GOING ON? LET'S GET RIGHT TO IT.` Ask for the deal list and
  prices if not supplied; **do not invent products or prices.** Quote the current
  price from the deal link, and say when a price is Subscribe and Save.

## Retention: Ryan's structure rules

Ryan's notes on the 10/09 F1 (`references/examples/ryan-notes-2026-10-09.md`,
read it) extend his 10/14 notes in Structure above (a tell after every case,
the money-lost case first, tease promises paid off by name). They are the layer
above line voice: **make the logic easy to follow, and
give every segment a reason to keep watching.** The line-level rules above make
a page sound like Jeff. These make a viewer stay to the end. The reviewer checks
every one of them.

### 1. Spell out why now, as a chain

When a story hangs on news (plans cut, a law, a recall, a data breach), say how
the news creates the scam, in plain words, early: **news → confusion → the
scammer's opening.** "Plans are changing. People are confused. And confusion is
exactly what scammers wait for." Then one line that anchors it and doubles as a
hook: `THE LETTER IS REAL. THE CALL ISN'T.` Without the chain, the news and the
scam read as two separate stories. The outline's `Why now` line is where this
comes from.

### 2. Never hand the viewer a reason to leave

Early in a video, any line that says "this doesn't apply to you" is permission
to leave: `IF YOU HAVE ONE… LISTEN UP`, `IF YOU'RE ON ORIGINAL MEDICARE… YOU'RE
NOT LOSING ANYTHING`. Keep the fact and flip the conclusion: `BUT DON'T GO
ANYWHERE. THE SCAMMERS DON'T CARE WHICH PLAN YOU'RE ON… THEY'RE CALLING
EVERYONE.` Widen the audience instead (the debit card episode: these scams
aren't just attacking seniors, they're attacking everybody). Watch for quiet
narrowing in tips too: "check your Medicare statement" becomes "…or your plan's
statement." `check_bible.py` warns on exclusion phrases.

### 3. Every transition names the connection

A jump from one subject to the next (letters → calls) says how they connect, or
it's a spot where viewers drift. Quote the scammer (`"YOUR PLAN IS ENDING."`),
tie it back (`SOUND FAMILIAR? IT'S THE SAME THING THE REAL LETTER SAYS.`), then
the proof number.

### 4. Every segment opens on a hook, not a label

`HERE ARE THE THREE SCAMS`, `SCAM NUMBER TWO…`, `THE SCARIEST OF THEM ALL` are
labels: they tell viewers where they are, not why to stay. "Scariest" is a
promise viewers have heard a thousand times; **the specific reason it's
scariest is the hook.** This extends "Mid-story headers are turns, not labels"
to segment openers and bridges.

- **Bridges say why the next one is worse.** Find the axis the segments climb
  on. On 10/9 each scam asked less of the viewer: the phone (you can hang up) →
  the mailbox (`NEVER ANSWER UNKNOWN NUMBERS? THIS ONE DOESN'T NEED YOU TO.`) →
  your own search (`THOSE TWO COME TO YOU. THIS ONE, YOU GO LOOKING FOR.`) →
  your statement (`THOSE THREE NEED YOU TO DO SOMETHING. THIS ONE DOESN'T.`).
  Order the segments so the axis climbs.
- **Move buried hooks to the top.** A striking fact mid-segment (`STOLEN
  MEDICARE IDENTITIES SELL FOR AS LITTLE AS 8 DOLLARS`) opens the segment,
  against the big number. A curiosity hook (`THE FAKE CARD LOOKS NICER THAN THE
  REAL ONE. AND THAT'S THE GIVEAWAY.`) leads; the reveal comes inside.
- **Don't play coy about what the open already revealed.** If the cold open
  named the catheters, `WAIT UNTIL YOU HEAR WHAT HE WAS BILLED FOR` insults the
  viewer. Make it a callback: `REMEMBER THE VETERAN FROM THE TOP OF THE SHOW?`

`check_bible.py` warns on label openers.

### 5. A tell has to work for the people the scam targets

Test every tell against the viewer the scam is aimed at. `NO LETTER? DON'T
BELIEVE THE CALL` fails everyone who did get a real letter, and for them it
confirms the scammer's story. Add the move that works for everyone: `EVEN IF
YOUR LETTER IS REAL, YOU DON'T FIX IT WITH THE PERSON WHO CALLED YOU. HANG UP.
CALL … YOURSELF.` **Safety-critical moves go in the segment, not after the
guest**: viewers who leave early still leave protected.

### 6. Resolve every segment before the bridge

Each segment runs **hook → setup → clip → button → the tell → what to do →
bridge**. Never leave a segment on fear with no move, and never cut to a sponsor
from one: viewers who leave at the ad leave scared and unprotected. One action
line is enough (`DON'T CALL THE NUMBER ON IT. REPORT IT TO 1-800-MEDICARE.`).
The protection list or recap may repeat them; **the recap covers every segment,
one for one**.

### 7. Name the payoffs before the ad

The tease before `BUT FIRST, A QUICK WORD FROM OUR SPONSOR` names two or three
specific things still ahead, by name: `FACEBOOK. A JOB SCAM. THE MICROSOFT
SCAM.` (envelope episode). A generic `STICK AROUND` gives no reason to sit
through a read. `check_bible.py` warns when the lines before the sponsor carry
no specifics.

### 8. Guests: safe scripted answers, then Jeff's bottom line

A guest's scripted answer gets the same safety check as Jeff's lines (the 10/9
"do nothing" answer would have cost viewers drug coverage). After `(((GUEST
EXITS)))`, Jeff restates the takeaway in one or two lines: `SO HERE'S THE
BOTTOM LINE: NOBODY LEGITIMATE CALLS YOU FIRST. YOU CALL THEM.`

### 9. Say it precisely: the comments fact-check us

Lines that are almost right are exactly what the comments catch.
- **Who issues what.** `IF YOURS IS PLASTIC, IT'S A FAKE` alarms people holding
  a real plastic plan card. Say which issuer: `THE ONE FROM MEDICARE ITSELF`.
- **Rules with exceptions.** `.GOV EVERY TIME` is true for Medicare's own site,
  but the sponsor isn't a .gov: `ANYTHING ELSE IS A PRIVATE COMPANY. THAT
  DOESN'T MAKE IT A SCAM. BUT IT ISN'T MEDICARE.`
- **Don't contradict our own advice.** After telling viewers not to trust codes
  and links that show up unexpectedly, a QR code needs a line one beat before
  it: this one is ours, you watched us put it up, you know where it goes.
  `check_bible.py` warns on a QR cue without it.
- **Dates agree across the show.** `IT'S OPEN ENROLLMENT` in the open and `OPEN
  ENROLLMENT HASN'T EVEN STARTED` later can't both be true.
- **Don't blame the evidence.** The statement isn't "lying to you"; it shows you
  the fraud.

### 10. Show it, don't just say it

The strongest retention device in our hits is Jeff's own phone or computer,
mirrored, with "let's do this together." When a tip can be done live (search
"Medicare" and count the Sponsored results, open the settings menu, check the
statement), write it as a demo: `LET ME SHOW YOU. PULL UP MY PHONE.` /
`(((LIVE DEMO: JEFF'S PHONE MIRRORED)))`, plus a red cue to rehearse it. When
there's a real-versus-fake, put them side by side: `(((POP UP: FAKE CARD NEXT
TO A REAL ONE)))`.

### 11. Seed the chat and write the close

- **Seed the chat (live shows).** After `JOIN THE CHAT`, one specific on-screen
  question as a red cue: `(((ON SCREEN: HAVE YOU GOTTEN ONE OF THESE CALLS? WHAT
  DID THEY SAY?)))`. A second in the first half can feed the guest; write `JEFF:
  (READS ONE QUESTION FROM THE CHAT)` into the guest block. Where-are-you-watching-
  from stays Jeff's ad-lib.
- **Write the close.** Three short beats before `-END OF SHOW`: share it with
  someone it protects (`SEND THIS TO SOMEONE ON MEDICARE… BEFORE THEIR PHONE
  RINGS!!`; never "your parents"), the next video to watch, and `SEE YOU NEXT
  TIME.` On a Friday it closes the content half, right before the deals handoff
  (`OK. NOW LET'S SAVE YOU SOME MONEY!!`), as in Ryan's revision; the deals half
  is unscripted. The ending closes; it doesn't dissolve.

## Voice

Full rules in `references/line-rules.md`; corpus tables in `measurements.md`.

- **ALL CAPS is prompter ergonomics, not style.** He is scanning, not reading.
- **Spikes, not a plateau.** `!!` and `!!!` on roughly one spoken line in eight
  (the checker errors below 0.08); `???` on a handoff question where it earns it,
  0–2 per document; **inline bold** on the words to hit, with a countable target
  (a name, a figure, the trick); a few lines that break the dash pattern to stand
  alone. Re-read the paraphrase test before adding any of it.
- **He says `you`, not `consumers`.** `right now` is the most characteristic thing
  he says. No anchor connective tissue, no hedging, no formal register.
- **Tone: not PG, not bleak.** Grim material, deaths included, is allowed when it
  is genuinely the story — but don't build unbroken dread. He swears
  occasionally; don't sanitize his voice and don't manufacture profanity.
- On air, soften the most violent verbs; don't locate victims below the state
  level unless the place is the story.

## Leave the document open

A bible is a working document the team marks up. Carry **two or three open
decisions** as red production cues, at the places where the call genuinely isn't
yours:

```
(((DECIDE CLIP A OR B - A IS THE VICTIM INTERVIEW, B IS THE BUST)))
(((JEFF - GRAPHIC HERE, OR DO YOU WANT TO RAPID-FIRE THE LIST?)))
(((PRODUCER - CONFIRM THIS FIGURE BEFORE AIR, SINGLE SOURCED)))
```

Open decisions are staging and preference calls. They are not a licence to leave
research undone.

## Research and honesty

Sometimes the stories arrive with the request; sometimes only a topic does.
When researching, go to primary sources — FTC, BBB Scam Tracker, FBI IC3, state
AG, CFPB, court filings, company statements. Exact figures with source and date.
Named victim cases and expert quotes, preferring original local reporting.
Confirm recency.

- **Never invent a quote, statistic, victim, source, identity detail or clip.**
  If it cannot be found, say so and flag it. Mark anything single-sourced.
- **A source's caution is a constraint on the copy.** When the pre-bible or
  outline says "never imply X," "use no figure," "attribute every time," or
  "keep it alleged," the bible obeys it in the tease, the runways, the buttons
  and the headers — and the source log records how.
- **Police department and jurisdiction must be exact** in arrest stories. Never
  frame a past-tense reversal in the present tense. Stats tied to an expert or a
  report go to the right source, not a paraphrased one.
- **You cannot watch video.** You can describe a clip from its transcript or
  description. You cannot confirm what's on screen or time a moment. Say so.
- Live numbers (view counts, prices) are pulled on show day; mark them.

## Output — two files, named for the A story

1. **The bible** `.docx`, built with `scripts/build_bible.py` and confirmed with
   `scripts/verify_format.py`. Black is what Jeff says; red is a production
   instruction. No sources section inside it — a citation may go inline as a
   hyperlink on the named source, nothing more.
2. **The companion source log** `.docx`, built with
   `scripts/build_source_log.py`. One row per added claim, with its status
   (CONFIRMED / PARTIALLY CONFIRMED / UNVERIFIED / CONTRADICTED), source URL and
   scope note; plus the clip table — beat id or clip number, orientation, role,
   candidate URL, timecodes (FINAL), and what the clip is known to show and from
   what (transcript, title, description). Every caution flag carried from the
   input gets a row saying how the copy honours it.

**File names: the A-story headline plus the air day and date**, never a generic
show label:

```
HE SAID HE WAS TOM SELLECK - WED 10_14.docx
HE SAID HE WAS TOM SELLECK - WED 10_14 - SOURCE LOG.docx
```

Add ` - DRAFT` before `.docx` on a DRAFT bible. Format detail in
`docx-format.md`.

The chat reply is short: first the **review loop** summary (rounds run,
BLOCKERs fixed with before → after, any still blocking, and the count of notes
left for the producer), then the stage, anything assumed (story count), any clip
change against the outline, anything declined and why, the open decisions, and
what in the source log needs a human before air. The loop's log is
`REVIEW_LOOP.md` in the run folder.

## Do not over-correct

Recent drafts got real things right; fixing everything above must not cost
them: teaser architecture and separators; the like/subscribe close; the sponsor
tease at a real story boundary; mechanism reveals that pass the paraphrase test;
and the **operational specificity** — exact click paths, the settlement URL, the
hotline numbers — which lives in the mechanics run, the walkthrough and the
protection list.

## Producer one-offs are not rules

The producer sometimes keeps a line the reviewer flagged because she likes how it
sounds. In the sent 10/14 bible she kept `THIS REPORTER CAUGHT ONE STORE IN THE
ACT`, `ONE OWNER GOT BUSTED!!`, the 50-OR-60 number in both the tease and the
header, and the CBS clip's out point. Those were one-offs. **Do not copy them
into new drafts**: write the careful version (accused framing, payoff held for
the clip) and let the producer choose the louder one.

## Self-check before delivering

Run `python3 scripts/check_bible.py draft.md --day wednesday --stories 2 --stage draft`
(adjust day, story count and stage) and clear every ERROR. Then read for what a
script can't see:

- The user's instructions — show day, story count, guest, stage — were followed,
  and anything assumed is stated in the reply.
- Every caution flag from the input is honoured in the copy, including the
  tease, and logged.
- Every person is introduced by identity drawn from the source, with nothing
  added to make them vivid.
- No setup spoils its clip; no setup asks a question the clip can't be shown to
  answer; no setup is interchangeable.
- Mid-story headers are sayable and climb.
- The `line-rules.md` checks pass: command hook, cue + verdict in and a button
  out of every clip, numbered tips with reasons, sponsor entered with a tease and
  a bridge, the company's response, no doesn't-say words.
- No unbooked expert named in black copy; guest names match between copy and
  cues.
- Every aphorism candidate the checker named has had the paraphrase test.
- First person: one or two lines, nothing invented about Jeff's life.
- Two or three open decisions left for the team.
- Both files exist and are named for the A story and date.
- FINAL: clips match the outline, numbered in air order, `OUT:` and the red
  source line from the Videos rows, nothing added, cut or swapped without saying
  so.
- The producer's cuts (`What the producer cuts before it goes to Jeff`): no news
  outlet in a spoken line; victims by first name or `THIS WOMAN`/`THIS MAN`;
  state, not town; no `YOUR PARENTS`; the tease and every `NEXT,` line hold the
  payoff back; no story's body opens on its tease headline; no slate or
  like/subscribe housekeeping copy.
- Ryan's retention rules (`references/examples/ryan-notes-2026-10-09.md`): the
  why-now chain said early; no line hands viewers a reason to leave; every
  transition names the connection; segment openers are hooks and each bridge
  says why the next one is worse; every tell works for the people the scam
  targets; every segment ends on what to do before the bridge or sponsor; the
  pre-sponsor tease names specific payoffs; Jeff restates the takeaway after the
  guest; precise claims (issuer, exceptions, QR line, dates that agree); a live
  demo where a tip can be shown; an on-screen chat question; a written close.
- The review loop ran (or the producer waived it): BLOCKERs fixed or listed as
  still blocking, no WARNING or NOTE "fixed", any clip change stated and
  mirrored in the outline, `REVIEW_LOOP.md` written.

Then build and verify:

```bash
python3 scripts/build_bible.py draft.md "HE SAID HE WAS TOM SELLECK - WED 10_14 - DRAFT.docx"
python3 scripts/build_source_log.py sources.md "HE SAID HE WAS TOM SELLECK - WED 10_14 - SOURCE LOG.docx"
python3 scripts/verify_format.py "HE SAID HE WAS TOM SELLECK - WED 10_14 - DRAFT.docx"
```
