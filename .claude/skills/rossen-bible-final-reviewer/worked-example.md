# Worked example — a complete audit

A full three-artifact review of a two-story draft, shown end to end so the output
shape is unambiguous. Read this before your first review.

The draft audited here is a deliberately damaged version of the aired F2 07/10
bible (home mover scams + gold bar scam), used because it exercises every finding
class: a wrong figure, a fabricated study, a fabricated quote, a defamation
exposure, a bad hotline digit, a wrong agency, off-register voice, a verbatim
lift, PII overshare, a malformed cue, a missing `OUT:`, a mid-story sponsor, a
missing protection beat, and a missing `END OF SHOW`.

Note especially:

- **Non-fact-check issues have a blank Confidence cell**, not a dash.
- **Every figure row carries a Scope**, and one claim is `PARTIALLY CONFIRMED`
  purely because the benchmark's scope didn't match.
- **Unsourced clip cues are NOTEs**, because this is a pre-air draft.
- The verdict is followed by an ordered fix path that separates one-line edits
  from work that has to go back to the writer.

---

## 1. SUMMARY REPORT

**Stage:** pre-air draft, clip manifest not locked.
**Source list supplied:** no — every claim was re-derived from scratch.
**Fact-check coverage:** 16 of 18 inventory items fully searched. 2 Tier 4
background items logged UNVERIFIED for budget, noted in the log.

**VERDICT: NOT READY** — 8 BLOCKERs, one of which needs legal review rather than
an edit.

### Fastest path to READY WITH FIXES

The first four are one-line edits and clear half the blockers:

1. Hotline digit `8071` → `9071`, and `DEPARTMENT OF JUSTICE` →
   `DEPARTMENT OF TRANSPORTATION` (BLOCKERs 4, 5).
2. Cut the Harvard study line and the Abbate quote (BLOCKERs 2, 3). Neither is
   load-bearing; the story works without them.
3. Redact the address and account digits (BLOCKER 7).
4. Paraphrase the block quote (BLOCKER 6).
5. Replace the `1.4 BILLION` figure with a same-scope sourced number and put the
   source on screen (BLOCKER 1). The correct figure is smaller, so this is a line
   rewrite, not a swap.
6. Cut the Mayflower / Two Men and a Truck line (BLOCKER 8). If a named-company
   beat is wanted, it needs sourcing **and** standards review — not a pre-air fix.
7. Write a protection beat for the gold story (BLOCKER 9). This is actual writing
   and belongs with `rossen-script-writer`, not this pass.

### BLOCKERs

| # | Story / section | Issue | Confidence | Source | Scope |
|---|---|---|---|---|---|
| 1 | Gold / losses | "MORE THAN 1.4 BILLION DOLLARS" is ~5x the largest published same-scope figure | CONTRADICTED | fbi.gov | nationwide, gold courier, first 10 mo. 2025 = $262M |
| 2 | Movers / hook | "A NEW HARVARD BUSINESS SCHOOL STUDY FOUND 41%… UNLICENSED" — no such study | UNVERIFIED | — | — |
| 3 | Movers / hook | Quote attributed to FBI Deputy Director Paul Abbate — no record of the statement | UNVERIFIED | — | — |
| 4 | Movers / protection | Hotline given as 1-800-424-**8071** | CONTRADICTED | oig.dot.gov/report-fraud-hotline | current — correct is 1-800-424-**9071** |
| 5 | Movers / protection | Directs viewers to the **DEPARTMENT OF JUSTICE'S** OIG | CONTRADICTED | oig.dot.gov/investigations/household-goods-moving-fraud | current — household goods moving fraud is DOT OIG |
| 6 | Movers / mechanics | 40-word verbatim block quote staged to be read on air | | | |
| 7 | Movers / victim | Full home address and partial account number on screen | | | |
| 8 | Movers / hostage scam | Two real national carriers named as "the two worst offenders" running a criminal scheme, unsourced | UNVERIFIED | — | — |
| 9 | Gold / structure | Story has no protection / takeaways beat at all | | | |

BLOCKER 8 is flagged **for human legal/standards review**, not cleared or
resolvable here. Naming identifiable companies as criminal operators is defamation
exposure regardless of what sourcing turns up.

### WARNINGS

| # | Story / section | Issue |
|---|---|---|
| 10 | Movers / mechanics | "HOWEVER, CONSUMERS SHOULD BE AWARE THAT CERTAIN INDIVIDUALS MAY UTILIZE THESE PLATFORMS TO ALLEGEDLY DEFRAUD THEM. THE BOTTOM LINE IS THAT DUE DILIGENCE REMAINS PARAMOUNT" — generic news copy, not Jeff. Six off-register words in two lines |
| 11 | Movers / clip 2 | Cue written `((PLAY CLIP 2 HORIZONTAL))` — two parens. Aired bibles contain the same typo; the extractor parses on exact paren count, so it is still a defect |
| 12 | Movers / clip 3 | Cue has no `OUT:` line beneath it |
| 13 | Gold / sponsor | Second sponsor block dropped mid-story between two clip beats, with no takeaway or story boundary separating it from the previous clip |
| 14 | Document end | No `END OF SHOW` marker |
| 15 | Movers / protection | Draft sends viewers to DOT OIG to *file a complaint*. Per DOT OIG's own page, consumer complaints against a mover go to FMCSA's National Consumer Complaint Database, 1-888-368-7238; the OIG hotline is for reporting fraud. Worth splitting on air |

### NOTES

| # | Story / section | Issue |
|---|---|---|
| 16 | All clip cues | 8 cues, none carrying a URL. **Stage-appropriate** — aired bibles carry unsourced cues pre-air and the clip pipeline sources them downstream. Listed so the producer can confirm a manifest exists separately |
| 17 | All clip cues | None visually confirmed. This review works from titles, descriptions and transcripts only |
| 18 | All clip cues | All 8 cues numbered rather than `XXX`. Confirm the show has been timed |
| 19 | Movers / clip 5 | "AGOYU" — confirm spelling and that the app is still live before it goes on screen. A named free app is an implicit endorsement |
| 20 | Movers / AI section | Stray backslash in "I FOUND A \FREE APP" will render on the prompter |

---

## 2. ANNOTATED BIBLE

Excerpts at the point of issue. Original text and cue formatting preserved
exactly, so the copy stays shootable if every flag is resolved with a one-line fix.

```
-IT'S EXTORTION

-A NEW **HARVARD BUSINESS SCHOOL** STUDY FOUND 41% OF MOVING COMPANIES
ADVERTISING ONLINE ARE COMPLETELY UNLICENSED.
[FACT-CHECK: UNVERIFIED — no Harvard Business School study on moving-company
licensing found; the 41% figure appears in no source located. Cut, or replace
with an FMCSA or BBB figure the producer can cite on screen. — BLOCKER]

-AND THE COPS AREN'T DOING ANYTHING TO HELP!

-F-B-I DEPUTY DIRECTOR **PAUL ABBATE** TOLD ROSSEN REPORTS: "THIS IS THE FASTEST
GROWING FRAUD IN AMERICA AND WE ARE LOSING THE FIGHT."
[FACT-CHECK: UNVERIFIED — statement not found in FBI press material, testimony,
or reporting. Attributing an unfindable quote to a named sitting official is the
highest-risk item in this draft. Produce the transcript or cut. — BLOCKER]
```

```
-**MAYFLOWER** AND **TWO MEN AND A TRUCK** ARE THE TWO WORST OFFENDERS RUNNING
THIS HOSTAGE SCAM RIGHT NOW.
[LEGAL: UNVERIFIED — names two real national moving brands as the worst
perpetrators of a criminal scheme with no citation. Defamation exposure. Not
something this pass can clear; needs human legal/standards review even if a
source is produced. — BLOCKER]
```

```
CALL 1-800-424-8071
[FACT-CHECK: CONTRADICTED — DOT OIG's fraud hotline is 1-800-424-9071
(oig.dot.gov/report-fraud-hotline, current). A wrong digit on a hotline aired to
millions sends victims nowhere. — BLOCKER]

OR EMAIL: HOTLINE@OIG.DOT.GOV
[CONFIRMED — matches oig.dot.gov, current.]
```

```
-AND IT HAS ALREADY COST AMERICANS MORE THAN **1.4 BILLION DOLLARS.**
[FACT-CHECK: CONTRADICTED — the largest published same-scope figure is $262M
(FBI, nationwide gold courier, first 10 months of 2025). Other real figures exist
at different scopes and are not interchangeable: $55M (IC3, nationwide couriers,
May–Dec 2023), $26M (FBI Boston, New England, 2023–25), $219M (IC3, gold scams,
2024). Whichever the producer picks, the scope has to go on screen with it. Note
this line will need rewriting rather than a number swap, since the real figure is
much smaller. — BLOCKER]
```

```
**((PLAY CLIP 2 HORIZONTAL))**
[FORMAT: two parens, contract is three. The aired 06/22 bible contains the same
typo — that does not clear it, the extractor parses on exact count. — WARNING]

**OUT: (FIND)**
```

```
**(((PLAY CLIP 3 HORIZONTAL)))**
[FORMAT: no OUT: line beneath this cue. Every other cue in the document has one.
— WARNING]
```

---

## 3. SOURCE LOG

Grouped by evidence cluster, in the story order of the bible — the by-story
breakdown is the point of the table, not decoration. Clip cues get their own
group so the log doubles as the clip source manifest. The three standing groups
appear in every log, empty if there is nothing to report.

| CLAIM | CONFIDENCE | SCOPE | SOURCE |
|---|---|---|---|
| **MOVING FRAUD — UNSOURCED CLAIMS** | | | |
| "HARVARD BUSINESS SCHOOL STUDY FOUND 41%… UNLICENSED" | UNVERIFIED | — | — No such study located. Cut, or replace with an FMCSA or BBB figure the producer can cite on screen. |
| "PAUL ABBATE TOLD ROSSEN REPORTS: THIS IS THE FASTEST GROWING FRAUD…" | UNVERIFIED | — | — Not in FBI press material, testimony or reporting. Highest-risk item in the draft. |
| "MAYFLOWER AND TWO MEN AND A TRUCK ARE THE TWO WORST OFFENDERS" | UNVERIFIED | — | — Defamation exposure. Routed to standards review; not cleared here. |
| **MOVING FRAUD — FEDERAL SOURCING** | | | |
| "CALL 1-800-424-8071" | CONTRADICTED | current | oig.dot.gov/report-fraud-hotline — correct number is 1-800-424-9071. |
| "DEPARTMENT OF JUSTICE'S OFFICE OF INSPECTOR GENERAL" | CONTRADICTED | current | oig.dot.gov/investigations/household-goods-moving-fraud — household goods moving fraud is DOT OIG. |
| "HOTLINE@OIG.DOT.GOV" | CONFIRMED | current | Same page. Matches. |
| "FMCSA.DOT.GOV/PROTECT-YOUR-MOVE" | CONFIRMED | current | fmcsa.dot.gov/protect-your-move — live, carries the registered-mover database. |
| "INTERSTATE MOVERS MUST BE LICENSED BY THE DOT" | CONFIRMED | interstate household goods | Same. FMCSA registration required. |
| "INTRASTATE MOVERS MUST BE LICENSED BY THE STATE" | UNVERIFIED | — | — Tier 4, budget ran out. True in general, varies by state. |
| Complaint routing | | | DOT OIG's own page sends consumer complaints to FMCSA's National Consumer Complaint Database, 1-888-368-7238; the OIG hotline is for fraud allegations. Draft conflates the two. Available if wanted; not currently split in the bible. |
| **THE MOVING TAX STING** | | | |
| "A STATE MOVING TAX OF 18%" | PARTIALLY CONFIRMED | single market, single sting | Station investigation behind clip 1. The tactic is well documented; the specific 18% traces only to that one sting. |
| **GOLD COURIER — FBI AND IC3 FIGURES** | | | |
| "MORE THAN 1.4 BILLION DOLLARS" | CONTRADICTED | nationwide, gold courier, first 10 mo. 2025 = $262M | fbi.gov. Three other real figures exist at other scopes and are not interchangeable: $55M (IC3, nationwide couriers, May–Dec 2023), $26M (FBI Boston, New England, 2023–25), $219M (IC3, gold scams, 2024). Whichever the producer picks, the scope goes on screen with it. |
| "THE F-B-I SAYS LOSSES ARE EXPLODING… ESPECIALLY AMONG OLDER AMERICANS" | CONFIRMED | over-60, nationwide, 2023 | fbi.gov/news/stories/elder-fraud-in-focus — losses up ~11% to $3.4B; couriers called out specifically. |
| "NEVER BUY GOLD, SILVER, CRYPTOCURRENCY, OR GIFT CARDS BECAUSE SOMEONE ON THE PHONE TELLS YOU TO" | CONFIRMED | nationwide guidance | ic3.gov/PSA/2024/PSA240129 — matches IC3 language. |
| **GOLD COURIER — THE $700,000 WIDOW** | | | |
| "SCAMMED OUT OF $700,000… 79 YEAR OLD WIDOW" | UNVERIFIED | — | — Cannot identify the case without the clip source. Sourcing clip 8 also sources this figure. |
| **CLIP SOURCES** | | | |
| Clip 1 — hidden-camera moving-tax sting, `OUT: (NOT THAT I'M AWARE OF)` | UNVERIFIED | — | — No URL. Stage-appropriate; cue text unverifiable without a source. |
| Clip 2 — woman whose goods were held hostage, `OUT: (FIND)` | UNVERIFIED | — | — No URL. Also a two-paren cue. |
| Clip 3 — family sent an unlicensed third-party crew | UNVERIFIED | — | — No URL. Also no `OUT:` line. |
| Clip 4 — police siding with the mover, `OUT: (ONLY TOOK MY MATTRESS)` | UNVERIFIED | — | — No URL. |
| Clip 5 — AGOYU room-scan estimate app, `OUT: (costs even further)` | UNVERIFIED | — | — No URL. Confirm the app name and that it is live before it goes on screen. |
| Clip 6 — courier victim interview, `OUT: (OUT OF THERE IN A MONTH)` | UNVERIFIED | — | — No URL. |
| Clip 7 — police catching a pair of collectors, `OUT: (MONEY LAUNDERING CHARGES)` | UNVERIFIED | — | — No URL. |
| Clip 8 — $700k widow, alert store owner, `OUT: (WE'RE SCAMMING THE SCAMMERS)` | UNVERIFIED | — | — No URL. Carries the $700,000 figure. |
| **PRODUCER QUESTIONS — ANSWERED** | | | |
| Margin note: "BANNERS" on the DOT OIG block | | | Both the phone number and the email want banners. The number is wrong in this draft — fix before the banner is built. |
| Margin note: "ADD RED ARROW TO THIS" on the registered-mover database | | | Screenshot 3 is the right frame for the arrow; it is the search box itself. |
| **TEASE / BODY CONSISTENCY** | | | |
| Gold courier loss figure | | body only | Appears in the body, not the tease. Nothing to keep in sync today, but re-check after the figure is corrected — that is when drift gets introduced. |
| Mover hostage amounts, "5, 10, EVEN 20 THOUSAND DOLLARS EXTRA" | | body only | No tease counterpart. |

**Coverage statement:** 16 of 18 inventory items fully searched. Two Tier 4 items
are logged UNVERIFIED because the search budget ran out, not because a search
failed. No claim in this log rests on memory alone.

**Video:** none of the 8 cues was visually confirmed. Where a source URL exists,
the most this review can say is "consistent with available metadata, not visually
confirmed." In this draft no cue carries a URL, so none could be checked at all.
