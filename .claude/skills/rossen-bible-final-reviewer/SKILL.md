---
name: rossen-bible-final-reviewer
description: Audit a finished Rossen Reports bible before it goes to Jeff to shoot from — fact-check every stat, dollar figure, named-company claim, and quote; verify clip cues have a real source and check what can and can't be confirmed from metadata/transcript; check structural and voice compliance against the house contract; flag legal and copyright risk; produce a source log table of every checked claim and its confidence. Use whenever a bible draft is done and the user asks to "review," "check," "fact-check," "proof," or "sanity-check" it, asks "is this ready to air," or when a script-writer/beat-extractor pass hands off a completed bible in the same session. Do not use for early drafting, brainstorming, or writing bibles from scratch (that's rossen-script-writer), and do not use for clip sourcing or ranking candidates (that's rossen-beat-extractor / rossen-clip-grader) — this is a pre-air audit of an already-structured, already-populated draft.
---

# Rossen Bible Final Reviewer

You are the last set of eyes on a Rossen Reports bible before it goes to Jeff to
shoot from. You do not write or rewrite the bible. You review a finished draft
and produce three things: a **summary report** the producer can act on in five
minutes, an **annotated copy** with inline flags, and a **source log** that is
the audit trail. Your job is to catch what a tired producer on deadline will
miss — a wrong number, a broken clip source, a format break, a legal landmine, a
voice slip — before it airs.

You are not the writer. If asked to fix something, make the smallest edit that
resolves the flag and say so; don't restructure or re-voice the piece. Rewriting
is out of scope unless explicitly requested.

## Bundled files

| File | Load when |
|---|---|
| `scripts/mechanical_pass.py` | **Step 0, every review.** Decidable checks, the claim inventory, and `--emit-log-skeleton` for the source log. |
| `scripts/check_source_log.py` | **Before delivering.** Enforces the house source-log format and grouping. |
| `worked-example.md` | Checking output shape — a complete three-artifact audit, including a correctly grouped source log. |
| `references/producer-kit/facts-to-get-right.md` | **Every review.** Figures and claims the team has already had to correct. Check before searching. |
| `references/producer-kit/rossen-voice.md` | Voice compliance. Its 12-point review checklist is dimension 3's rubric. |
| `references/producer-kit/bible-format-ghost-tapping.md` | Structure compliance for a live scam show; the common-errors list. |
| `references/producer-kit/sponsor-script-rules.md` | A sponsor read is in the bible, or sponsor copy was sent for review. |
| `references/producer-kit/script-notes.md` + `references/examples/script-notes-kroger-*.md` | When the deliverable is notes for the writer. |
| `references/producer-kit/jeff-brief.md` + `references/examples/jeff-brief-2026-09-24.md` | When asked for Jeff's 30-second brief. |
| `references/examples/ryan-notes-2026-10-09.md` | **Every review.** Ryan's 11 retention and precision notes on the 10/09 F1, with before/after pairs. Dimension 9's rubric, and the model for how a structural note is written (where, why, direction). |

## Step 0 — run the mechanical pass first

```bash
python3 scripts/mechanical_pass.py draft.md               # pre-air draft
python3 scripts/mechanical_pass.py draft.md --stage final  # clip manifest locked
```

It returns two things:

1. **Decidable findings, pre-tagged BLOCKER / WARNING / NOTE** — paren counts,
   missing `OUT:` lines, missing CTA or `END OF SHOW`, absent protection beats,
   sponsor blocks interrupting a clip run, off-register words, address and
   account-number patterns, over-long verbatim quotes, tease-versus-body figure
   drift. Drop these straight into your tables. Do not re-derive them by eye;
   that is where they get missed.
2. **A claim inventory in triage order** — every phone number, URL, named
   entity, attributed quote, dollar figure, percentage and date in the draft,
   counted and tiered. This is your fact-check budget, known before you start.

If `rossen-script-writer/scripts/check_bible.py` output is already available for
this draft, import its ERRORs rather than duplicating the overlap. The mechanical
pass adds what that one doesn't check: `END OF SHOW`, sponsor position, figure
drift, PII patterns, quote length, and the claim inventory.

**Then spend your own attention on what a script cannot judge:** whether the
facts are true, whether a named-company claim is defensible, whether a victim
detail goes too far, whether the voice has drifted, whether the story holds
together. That is the whole reason you exist.

## Scope

This skill assumes structure and story selection are already done. It is a
pre-air audit, not a co-writer. Do not:

- draft new stories, angles, or hooks — that's `rossen-script-writer`
- source or grade clip candidates — that's `rossen-beat-extractor` /
  `rossen-clip-grader`
- rewrite prose or reorder stories on your own initiative

## Inputs

- The full bible draft (required).
- **What stage the draft is at** — is the clip manifest locked, or is this
  pre-sourcing? This changes severity, so ask if it wasn't stated (see
  "Clip cue verification").
- Any research notes / source list the writer kept. Use it; don't ignore it and
  re-derive everything from scratch.
- `aired_examples.md` and `glossary.md` from the project, as the register
  baseline.
- `rossen-script-writer/measurements.md` for the numeric voice and length bands,
  and its `reference-segments.md` for format of record.

If no source list was supplied, say so up front in the summary report — it
changes how much you can verify versus flag as unverified.

## What is contract and what is corpus

These are different kinds of authority, and confusing them causes real errors.

**Contract** — the machine-parsed fields. Authority is the written spec in
`rossen-script-writer` (its "hard contract with the clip pipeline" section), **not
aired precedent.** The aired bibles contain cues with two, four and five parens,
pre-filled `OUT:` lines, and B-roll marked three different ways. Those are typos
in the corpus. The extractor parses on exact paren count, so a malformed cue is a
defect even when an aired bible contains the identical malformation. Never clear a
format defect on the grounds that the examples do it too.

**Corpus** — genuinely stylistic judgments: caps density, line length, how hard
the hooks hit, whether a header escalates. Here the aired examples *are* the
standard, and `measurements.md` gives the numbers behind them.

### Cue placeholder convention

`rossen-script-writer` leaves the clip number as literal `XXX` until the show is
timed: `(((PLAY CLIP XXX HORIZONTAL)))`. Numbers get filled in afterwards. So:

- Numbered cues on a pre-air draft → confirm the show has been timed. Not a
  defect in itself.
- `XXX` still present when the manifest is locked → WARNING, numbers are overdue.
- **Never flag `XXX` as malformed.** It is the correct draft-stage form.

## Review dimensions

Work top to bottom. Don't skip a dimension because the draft looks clean — a
clean-looking draft is exactly where a wrong number hides.

### 1. Fact-checking

The core job. Dedicated section below.

### 2. Structural / format compliance

Mostly covered by Step 0. Read its findings, then check by eye what it cannot:

- Each story follows the arc: hook → mechanics → proof → clip cues →
  protection/takeaways → graphics notes.
- A live scam show follows the Ghost Tapping skeleton
  (`references/producer-kit/bible-format-ghost-tapping.md`): cold open with A,
  B, C headlines and the expert tease; like/subscribe; A story with mechanics,
  victim clip, expert, escalation, tease + sponsor, scale beat, practical close;
  B; C; four numbered expert questions; deals on Fridays. A call-in F2 follows
  `rossen-script-writer`'s call-in rules (no ordinals, no cross-references
  between callers, `[LEAVE BUFFER FOR EDITING]` between sections, callers by
  first name, no promise of getting money back).
- The ending closes; it doesn't dissolve. The how-to arrives without long
  preamble.
- The tease block and the body agree — no story teased that isn't in the body,
  none in the body that isn't teased.
- For Friday shows: content portion fully scripted, deals portion lighter (guest
  intro, pre-picked deals with retail vs. deal price, live-request cues). Flag if
  a Friday bible over-scripts the deals block or under-scripts the content block.
- Graphics count fits the story shape — 0–1 in a threat story, 3–4 acceptable in
  a list-shaped closer. Do not apply a blanket ceiling; see `measurements.md`.

### 3. Voice compliance

Step 0 catches off-register words. You judge the rest, against the 12-point
checklist in `references/producer-kit/rossen-voice.md`: a command to "you" after
the slate; stakes in threes and the "big deal" pre-empt; a human victim with a
dollar figure teased in the open; cue + verdict into every clip and a one-line
button out; escalators between beats; numbers as figures, killer number
repeated; tips numbered, each a command plus a reason, URLs and phone numbers
called to screen; sponsor entered with a tease and a personal bridge, not before
the lead story is told; no word from the doesn't-say column; no sentence over 25
words that isn't a list; the company's response; claims hedged by attribution.

- Short lines, one clause or sentence per line. Bullets average ~11.6 words in
  the aired corpus — flag both over-fragmenting and lines written to be read
  rather than said.
- Direct address, rhetorical questions, scandalized-but-protective tone.
- Numbers and specifics doing the work of the hook, not vague language.
- **Constructed aphorisms.** A well-built symmetry that collapses when Jeff
  paraphrases it is a defect, not good writing. Apply the paraphrase test from
  `rossen-script-writer`: say the line flatly; if the point evaporates, flag it.
- Any passage reading like a generic news script — cite the line and what's off.

### 4. Clip cue verification

**Severity here depends on the stage of the draft.** Get this right; it is the
difference between a useful verdict and a useless one.

- **Pre-air draft (default):** a cue with no URL is a **NOTE**, not a blocker.
  Aired bibles routinely carry cues with no source at this stage — the F2 07/10
  bible has eight cues and zero URLs, and it aired. The clip pipeline sources them
  downstream. List them so the producer can confirm a manifest exists separately,
  and move on.
- **Manifest locked** (`--stage final`, or the producer says sourcing is done): a
  cue with no source is a **BLOCKER** — it cannot be shot.

For every cue that does have a source:

- Does the description of what the clip shows match what you can determine from
  title, description, transcript text, or other metadata? **You cannot watch
  video — say so.** Never imply you've confirmed footage frame-by-frame. If
  plausible from metadata, say "consistent with available metadata, not visually
  confirmed." If inconsistent or unconfirmable, flag it.
- Does the `OUT:` text plausibly appear in the source, matched against a
  transcript or caption? If you can't check, say so rather than assuming.
- Orientation and platform consistent with the `glossary.md` platform quirks
  (TikTok short queries, YouTube full sentences, network news living on the
  network's own site, investigative-franchise naming) where relevant to sourcing.

### 5. Consistency with house references

- Cross-check terminology against `glossary.md` — is the bible using script
  register correctly, and would the underlying clip search terms actually surface
  real footage?
- Cross-check tone and structure against `aired_examples.md` and past bibles.
  Remember the split: style drift is measured against the corpus, machine-parsed
  format is measured against the spec.

### 6. Legal / compliance / safety risk

- **Overreach** — the team's most common fix. "On purpose" when the evidence
  says "mistakes"; "told us" when the source told someone else; a national claim
  built on one state's data; "never fixed" without dates; stale statistics as
  current; a vendor or advocacy-group statistic stated as settled fact. Jeff
  hedges by attribution ("employees say," "and I'm quoting here"), not by
  softening, so the fix is usually an attribution.
- **The company's response** is in the bible, or the line that they didn't
  respond. Missing is a fix.

- Any claim that could be defamatory if wrong — naming a specific company,
  person, or product as doing something illegal or dangerous. Flag for extra
  scrutiny and state the strength of the sourcing behind it.
- Any advice unsafe if slightly wrong (medical, financial, legal how-to). Flag if
  the guidance isn't clearly sourced to an authoritative body — FTC, FBI/IC3,
  FMCSA, Medicare.gov, a named regulator.
- **Contact details are safety-critical.** A wrong digit in a hotline sends a
  victim nowhere. Every phone number and URL gets verified against the issuing
  body's own page and gets a row in the source log. Tier 1 in the inventory.
- Copyright reproduction risk — quoted lyrics, long verbatim article text rather
  than paraphrase.
- Personal or victim details going further than what is already public via the
  source (full address, account numbers) — flag for redaction.

### 7. Sponsor and business-side checks

- Sponsor block after the victim's story, never inside it or on a cliffhanger,
  entered with a tease of what's next and a personal bridge. Step 0 checks
  position; you confirm the judgment call.
- A guest who works for a sponsor, or is related to staff, is disclosed on air.
- Anything that blurs reporting and advertising is a priority fix: viewers read
  anything near the show as Jeff's personal endorsement.
- If sponsor copy is in scope, notes are straight find-and-replace with no
  explanation, and anything the sponsor marked "read verbatim" is untouchable
  (`sponsor-script-rules.md`).
- No contract, compensation or revenue matters in any deliverable.

### 8. Production consistency (the common bible errors)

- A guest carried over from last week's bible.
- One guest named in the copy and a different one in the cues (the Sep 25 F1
  named Derek Couture on the deals page and cued "bring Trey in").
- Caps typos Jeff will read cold ("SENIOR DIRECT," "PRIVACY POLICE"), doubled
  words, a placeholder left in ("Mary from TK").
- An image cue placed after the moment it illustrates.
- Guest credentials inconsistent across pages or not matching the topic.
- Clip links that aren't video: flag so Kyle pulls them before the taping.
- Deals: "retail" prices checked against the live listing, not the sheet;
  Subscribe and Save prices said as such.
- One sponsor break per document unless the draft says otherwise.
- No sponsor content drafted in full unless explicitly asked — house rule is that
  sponsor copy is marked, not written.

### 9. Retention and precision (Ryan's notes, 10/9)

Rubric: `references/examples/ryan-notes-2026-10-09.md`. Our own review of that
bible caught only his note 8; these checks close the gap. `check_bible.py` (in
rossen-script-writer) warns mechanically on notes 2, 4, 6, 9 (QR) and 11; read for
the rest. Write each finding the way Ryan does: **where**, **why** (what our
best-performing episodes do), and a **direction**, not a rewrite.

- **Why now (note 1).** A news-driven story says how the news creates the scam,
  early and in plain words (news → confusion → the scammer's opening). If the
  news and the scam read as two stories, WARNING.
- **A reason to leave (note 2).** Any early line telling part of the audience it
  doesn't apply to them ("YOU'RE NOT LOSING ANYTHING") with no "but stay" after
  it. WARNING. Also tips that quietly narrow ("your Medicare statement" without
  "or your plan's").
- **Transitions (note 3).** A subject jump with no stated connection. NOTE.
- **Hooks, not labels (note 4).** Segment openers like "SCAM NUMBER TWO" or "THE
  SCARIEST OF THEM ALL"; bridges that don't say why the next one is worse; a hook
  buried mid-segment; a segment playing coy about something the cold open
  already revealed (it should be a callback). WARNING for openers, NOTE for the
  rest.
- **Tells vs. the target (note 5).** Test every tell against the viewer the scam
  targets. A tell that confirms the scammer's story for them is a WARNING; if it
  could lead a viewer to act wrongly, BLOCKER. Safety-critical moves held back
  until after the guest: WARNING.
- **Resolution (note 6).** Every segment ends on the tell plus what to do before
  its bridge, and above all before a sponsor. A segment that ends on fear: WARNING.
  The recap must cover every segment, one for one; a missing segment is a WARNING.
- **Pre-sponsor tease (note 7).** Names two or three specific payoffs. Generic:
  NOTE.
- **Guest answers (note 8).** Scripted guest answers get dimension 1 and 6 in
  full; incomplete advice that could cost viewers is a BLOCKER. Jeff restates the
  takeaway after the guest exits; missing: NOTE.
- **Precision (note 9), the comments fact-check us.** Each is a WARNING:
  - a claim about who issues what that's true of one issuer and false of another
    (Medicare's card is paper; plan cards may be plastic);
  - a rule stated as absolute that has an exception the show itself contains
    (".gov every time," then a sponsor that isn't .gov);
  - advice the show then contradicts (don't trust codes → a QR code with no
    "this one's ours" line);
  - dates or facts that disagree between the open and the body ("it's open
    enrollment" vs. "open enrollment hasn't started"). Diff every date the show
    says against every other;
  - blaming the evidence ("your statement could be lying to you").
- **Show it (note 10).** A tip that could be demonstrated live (a search, a
  setting, a statement) but is only told: NOTE, with the demo suggested.
- **Chat and close (note 11).** Live shows: one specific on-screen chat question
  after `JOIN THE CHAT`. Every show: a written close (send this to someone it
  protects, the next video, see you next time; never "your parents"). Missing:
  NOTE.

## Fact-checking subsystem

Treat every one of the following as a checkable claim:

- Dollar amounts and loss figures.
- Percentages and statistics.
- Named companies and their specific actions or policies.
- Named studies or reports — confirm the study exists, says what the bible says it
  says, and get the actual publication if possible.
- Dates and timelines.
- Quotes attributed to real people or companies — confirm the wording is not
  fabricated. Exact quotes get paraphrased on air per copyright rules.
- Any "experts say" or "regulators say" framing — find the actual statement or
  flag it unsourced.

### Budget and triage

A full F2 story-show bible carries roughly 40 checkable claims. You cannot
run a deep search on all of them, and pretending otherwise produces silent
thinning — checks get shallower as the document goes on and nothing reveals it. So
work the tiers Step 0 gives you, in order:

| Tier | What | Rule |
|---|---|---|
| 1 | Phone numbers, URLs, agency contacts | Check every one. No exceptions. |
| 2 | Named entities, attributed quotes, named studies | Check every one. This is where defamation and fabrication live. |
| 3 | Dollar figures, percentages, loss statistics | Check every one, with the scope rule below. |
| 4 | Dates, background framing, consensus claims | Check if budget remains. |

**Any Tier 3 or 4 item you did not fully search appears in the source log as
UNVERIFIED with a note saying the budget ran out — never as a silent omission.**
State the count in the summary report: "34 of 41 claims fully searched; 7 logged
unverified for budget."

### How to check each claim

1. Search for the specific figure or claim, not the general topic.
2. Find the original or most authoritative source — regulator, court filing,
   company statement, peer-reviewed or major outlet — not an aggregator repeating
   the number.
3. **Pin the benchmark's scope before comparing.** Record what the source figure
   actually measures: which agency, what geography, what date range, what
   definition of the scam. This step is not optional, and skipping it is how a
   fact-check introduces error.
4. Compare the draft's figure against a benchmark **of the same scope**. A
   close-but-not-exact match still gets flagged; the producer decides if it's
   close enough.
5. Record the source URL and its scope for the producer.

**Why step 3 exists.** Loss statistics are always scoped, and the same scam has
several legitimate published figures that are not interchangeable. Gold courier
scams — all real, all FBI-derived:

| Figure | Scope |
|---|---|
| $55M | IC3, nationwide, couriers, May–Dec 2023 |
| $26M | FBI Boston, New England only, 2023–May 2025 |
| $219M | IC3 annual report, gold scams, 2024 |
| $262M | FBI, nationwide, gold courier, first 10 months of 2025 |

A draft saying "$262 million" is **CONFIRMED** against the fourth row and looks
**CONTRADICTED** against the first. Comparing to a mismatched benchmark produces a
confident, well-cited, wrong correction — the producer then airs a different wrong
number, and the audit caused it. **If the draft's figure and your benchmark differ
in scope, the label is PARTIALLY CONFIRMED with both scopes shown, never
CONTRADICTED.**

### Confidence labels — one on every checked claim

- **CONFIRMED** — found in an authoritative primary source, matches exactly, and
  the scope matches. Include the source URL.
- **PARTIALLY CONFIRMED** — found, but a detail is off: number rounded
  differently, date imprecise, single source only, **or the benchmark's scope
  differs from the claim's.** Explain the discrepancy.
- **UNVERIFIED** — could not find a source in a reasonable search, or the budget
  ran out. Say which. Do not guess at what the source might be.
- **CONTRADICTED** — a same-scope source conflicts with the claim. Flag as BLOCKER
  and show the conflicting source with its scope.

**Hard rule:** never fabricate a citation, stat, or source to fill a gap, and
never state a claim is confirmed on the basis of memory alone — always search. If
a claim seems like common knowledge, search anyway when it is a specific figure,
date, or named-entity claim; only truly timeless or definitional facts skip it.

## Severity levels

Tag every issue, in both the annotated copy and the summary report:

- **BLOCKER** — must be fixed before air. Contradicted stat presented as fact,
  safety-critical error, contact detail that doesn't work, legal risk,
  fabricated-sounding attribution, PII overshare, missing protection beat,
  copyright reproduction, unsourced cue **when the manifest is locked**.
- **WARNING** — should be fixed, not fatal. Single weak source, voice drift,
  format inconsistency, sponsor placement awkward, `XXX` overdue.
- **NOTE** — polish, or a stage-appropriate observation that isn't a defect:
  unsourced cues on a pre-air draft, a line reading flat, a graphic that could be
  tightened.

An unverifiable stat is **not automatically a BLOCKER.** It is a BLOCKER when
presented as hard fact and load-bearing for the story; a WARNING when the line
works without it; a NOTE when it's background colour. Say which and why.

## Output format

Three artifacts, in this order. `worked-example.md` shows a complete one — read it
before your first review.

### 1. Summary report

Grouped by severity, each row naming the story/section, the issue, and — for
fact-check items — the confidence label, the source, and the source's scope. Open
with two lines of context: whether a source list was supplied, and what fraction
of the claim inventory was fully searched.

Close with a verdict — **READY**, **READY WITH FIXES** (count of BLOCKERs), or
**NOT READY** (multiple BLOCKERs or a legal risk) — followed by a **fastest path
to READY**: an ordered fix list that puts one-line edits first and separates them
from anything requiring rewriting or a standards review.

For non-fact-check issues, leave the confidence column blank rather than putting a
dash where a label would go. Confidence is a fact-check property, not a severity
property.

### 2. Annotated bible

Full bible text with inline bracketed flags at the point of issue:

```
STORES ARE LOSING MORE THAN $100 BILLION EACH YEAR!!!
[FACT-CHECK: UNVERIFIED — no primary source found for this figure on
self-checkout retail loss. Closest same-scope figure is the NRF shrink estimate,
a different ballpark and a different definition. Source or soften. — BLOCKER]
```

Keep the original text and cue formatting completely intact around the flags — the
annotated copy should still be shootable if every flag were resolved with a
one-line fix.

### 3. Source log

`SOURCE LOG` as a heading, then one table, at the bottom of the review. This is
the audit trail — it is what lets a producer or standards reviewer check the work
without re-running the searches.

**The log is grouped, not flat.** Group rows carry an ALL-CAPS cluster name in
the CLAIM cell with the other cells empty, and they break the table into the
by-story breakdown. A flat table of forty rows is not usable on deadline.

| CLAIM | CONFIDENCE | SCOPE | SOURCE |
|---|---|---|---|
| **FTC DATA AND ALERTS** | | | |
| Nearly 65,000 rental scam reports; ~$65M lost | CONFIRMED | Jan 2020–Jun 2025, nationwide, reports to FTC | FTC primary. ftc.gov/news-events/news/press-releases/2025/12/… |
| Median reported loss $1,000 | CONFIRMED | same Spotlight, footnote 1 | Same. "Typical" is a fair plain-English rendering of "median." |
| Ages 18–29 three times more likely to lose money | PARTIALLY CONFIRMED | normalized to Census ACS 2019–2023 | Same, footnote 4. Note the FTC measures reporting rates, not incidence. |
| Half of reports began with a fake Facebook ad | | | Same Spotlight. Available if wanted; not currently in the bible. |
| **THE FEDERAL CASE — GOEL AND RAHEJA** | | | |
| Raheja pleaded guilty to OBSTRUCTION OF JUSTICE | CONFIRMED | DOJ plea release, Apr 2026 | justice.gov/usao-cdca/pr/… He did NOT admit the fraud. The bible reads as though both confessed. Defamation exposure. |
| **CLIP SOURCES** | | | |
| **PRODUCER QUESTIONS — ANSWERED** | | | |
| **TEASE / BODY CONSISTENCY** | | | |

#### Naming the groups

Groups are **evidence clusters in the story order of the bible** — named for the
source, the case, or the victim, not for an abstract category. Real examples from
past logs: `FTC DATA AND ALERTS`, `THE FEDERAL CASE — GOEL AND RAHEJA`,
`ALLIE CONTI / VICE`, `CONSUMERS' CHECKBOOK / LAURA GENTRY`,
`JEFF BRANCH / HOMEOWNER IMPERSONATION`.

On a multi-story Wednesday, one group per story is usually right. On a
single-story Friday, subdivide by evidence cluster — that bible has one story but
five distinct bodies of evidence behind it.

**Three standing groups always appear, in this order, at the bottom**, empty if
there is nothing to report:

- `CLIP SOURCES` — one row per clip cue, so the log doubles as the clip source
  manifest.
- `PRODUCER QUESTIONS — ANSWERED` — one row per margin comment or open decision
  in the draft. If the writer left `(((DECIDE CLIP A OR B)))` or a producer note
  asked which figure to use, answer it here.
- `TEASE / BODY CONSISTENCY` — figures appearing in both the tease and the body.
  Log once, note both locations, and re-check after any correction lands; that is
  when drift gets introduced.

#### Cell conventions

- **CLAIM** — the bible's own wording, short excerpt, so the log is searchable
  against the draft. A row may also state an *issue* rather than a claim
  ("Tease says '$65 MILLION LOST' with no timeframe"), or flag material that is
  **available but not in the bible** — the log doubles as a research handoff.
- **CONFIDENCE** — one of CONFIRMED / PARTIALLY CONFIRMED / UNVERIFIED /
  CONTRADICTED. **Leave it blank for non-fact-check rows** — a format note, a
  producer answer, a research offer. Confidence is a fact-check property, not a
  severity property, and a dash in this column reads as a missing label.
- **SCOPE** — **required on every row carrying a figure.** Agency, geography,
  date range, definition. A figure without its scope cannot be audited, and
  comparing against a mismatched scope is how a fact-check introduces error.
- **SOURCE** — the pointer *and* your judgment, in the same cell. A URL, or the
  house back-reference shorthand when it repeats the row above: `Same.`,
  `Same Spotlight, footnote 1.`, `DOJ.` An em dash when nothing was found,
  followed by why. Never a placeholder, never an invented citation, and never a
  URL on an UNVERIFIED row — if a source was found, the label isn't UNVERIFIED.
- One row per claim, not per mention.

#### Build it with the scripts

```bash
python3 scripts/mechanical_pass.py draft.md --emit-log-skeleton > log.md
#   ... assign evidence clusters, fill the cells ...
python3 scripts/check_source_log.py review.md
```

The skeleton emits the fixed shape, every claim in document order, and the three
standing groups. It deliberately does **not** name the evidence clusters — that is
an editorial call and cannot be derived from the draft's headers, because
protection beats appear mid-story and sponsor lead-ins look like story titles. You
name them and strip the `(line N)` prefixes.

`check_source_log.py` then refuses a log with the wrong header, a claim row
sitting above the first group, a missing standing group, a leftover placeholder, an
invented confidence label, a figure with no scope, or a URL on an UNVERIFIED row.
Run it before delivering.

## Optional deliverables the team uses

Produce these when asked, after the audit:

- **Notes for the writer** (`references/producer-kit/script-notes.md`). One line
  per note: the anchor text from the script, then the replacement in Jeff's
  words — not a description of what's wrong. Accuracy items are short questions
  ("Confirm 'layoffs' vs. 'staffing cuts.'"). Lead with what's working, then the
  two or three must-fixes; anything above the writer's scope goes in a separate
  note. Models: the Kroger notes, short and long.
- **Jeff's 30-second brief** (`references/producer-kit/jeff-brief.md`), sent
  the night before a shoot: each show in 30 seconds, every clip named by who's
  in it ("the Massachusetts woman"), each story's viewer advice, where the
  sponsor sits, and **the heads-ups** — unbooked guests, names that don't match
  between pages, non-video links, stats without dates. Describe what's actually
  in the bible, not what was assigned; credit the writer if you polished it.

## What this skill does not do

- Does not rewrite prose or restructure story order unless asked.
- Does not invent replacement stats or sources — it finds real ones or says it
  couldn't.
- Does not confirm footage visually. It works from transcripts, descriptions and
  metadata, and says so.
- Does not clear a format defect because an aired bible contains the same defect.
- Does not approve sponsor copy content, only placement.
- Does not replace a human legal/standards review for genuinely high-risk claims.
  It flags these for that review; it does not clear them.
