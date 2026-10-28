# Final review — 11/04 WED -- YOU'RE OWED MONEY

Reviewed 10/28/2026 by rossen-bible-final-reviewer. Bible under review: the producer's upload `11-04_Wed_--_Youre_Owed_Money.docx`, converted to `draft.md` (the earlier Claude draft is in git, commit dc6b58b). Stage: **final** (clips locked from `outline.md`).

- **Sources supplied:** yes. `SOURCE_LOG.md`, `outline.md`, `transcripts.json`, the show plan (there's no separate pre-bible .md for this show). New producer material was checked fresh: the 50-million figure, the state-search demo, OmniWatch's scan, Prime's price, open enrollment, and the LOCAL 12 YouTube link.
- **Coverage:** 37 inventory items; all Tier 1–3 checked; Tier 4 checked. 4 clips (1, 7's TikTok alternate, 11, the new Costco clip) can't be reached from here (TikTok), so their content and times are UNVERIFIED, not searched short. `mechanical_pass.py` has no `--outline` flag; it was run with `--stage final` and clips were checked against the outline by hand. `check_bible.py` ERRORs (9) are imported below. Two of the mechanical pass's 11 "no URL" BLOCKERs were conversion artifacts (a blank line between marker and OUT:), fixed in the conversion, not real defects.
- **No clip was watched.** Clip checks use transcripts, captions and metadata.

## SUMMARY REPORT

### BLOCKERS (8)

| # | Where | Issue | Confidence | Source / scope |
|---|---|---|---|---|
| B1 | A, sponsor bridge | "ALL SCAMMERS NEEDED WAS A NAME AND SOCIAL SECURITY NUMBER" misstates the father-and-son case: they were finders their victims hired, using forged documents and fictitious addresses. Fix: "ALL THEY NEEDED WAS A NAME, AN ADDRESS AND SOME FORGED PAPERWORK." | CONTRADICTED | California AG press release, July 30, 2010 (oag.ca.gov); one case, 2007–2009 conduct |
| B2 | A, clip 1 (Pearlman) | No OUT:; ranges written as bold black lines (print as 23pt headers Jeff reads); URL 4 lines below the marker. New ranges (0:05–0:58 BUTT 1:56–2:15) differ from the outline and can't be checked (TikTok). | | Outline A2 Videos row |
| B3 | B, clip 7 (Lori) | Source line above the marker, no OUT:, ranges as bold black lines, stray "))))", page break between lead-in and clip. Slice 2:32–2:49 dropped (fine if intended; update the outline). | | More Perfect Union captions, uE5THiD-kTk |
| B4 | B, clip 8 (Anderson) | Link swapped to YouTube pI4Eehj-0LI (Oct 28, 2022 upload, different title), with Google tracking parameters. Times were verified on LOCAL 12's page video (Oct 27, 2022, 2:20), not this copy; its captions were bot-walled twice. Revert to the page link or re-time on the YouTube copy. | | local12.com page video (Whisper) vs YouTube pI4Eehj-0LI (unchecked) |
| B5 | B, clip 9 (Lynda) | Source line unclosed; 1:49–2:03 slice dropped but OUT: still reads that slice's outcue "(NOT AT THE REGISTER)". Restore the slice or change OUT: to "(…ON ANY PARTICULAR WEEK)". | | WHIO page video (Whisper) |
| B6 | C, Costco clip | (((PLAY CLIP XXX))): no number, no orientation, no OUT:, link not in the red source line. Not in the outline (new 10/28). Unverifiable (TikTok short link). | | — |
| B7 | Whole show | Clip numbers run 1–9, 11, XXX after clip 10 (GMA) was cut. Must run 1..N in air order (check_bible ERROR). Renumber: Paige → 10, Costco → 11. | | |
| B8 | C | Clips 11 and the Costco clip run after the show's last protection beat: C ends with no takeaway (mechanical BLOCKER). The button after Paige and the "only the main member" line came out. Smallest fix: restore "-ONLY THE MAIN SAM'S CLUB PLUS MEMBER GETS WALMART+." after Paige, and finish the Costco takeaway line. | | corporate.walmart.com; clickorlando.com (Oct 20, 2026) |

### WARNINGS (16)

| # | Where | Issue | Confidence | Source / scope |
|---|---|---|---|---|
| W1 | Tease C | "TWO COSTCO PERKS MOST MEMBERS NEVER USE" no longer matches the body (a clip of several perks); "most" unsourced. | | |
| W2 | A, clip 1 | Runway 2 lines (checker ERROR 6–10); the 2002 Ruby Tuesday detail and 2023 date came out, so the video reads as new. | | Yahoo/AT&T, Nov 2023 |
| W3 | A, Barbara | "Date it on air" dropped: FOX 13 is Sept 3, 2025. | CONFIRMED | FOX 13 page metadata |
| W4 | A, Breznocks | "Back in 2021" dropped. | | CBS Sacramento (outline) |
| W5 | A, father and son | "Back in 2010" and the JEFF note (charged; outcome not confirmed) came out: a 2010 prosecution reads as current. | CONFIRMED | CA AG, July 30, 2010 |
| W6 | A, demo | Cue says MISSINGMONEY.COM; the steps search "[state] unclaimed property" on a state .gov site. | | |
| W7 | B, Lori | "SHE COMPLAINED TO DOLLAR GENERAL": she wrote to the Oklahoma AG and Dollar General answered with the gift card; "2022" dropped. | PARTIALLY CONFIRMED | More Perfect Union captions 2:09–3:22 |
| W8 | B, sponsor bridge | "…A LOT OF US NEVER" / "CHECK… OUR MEDICARE PLAN." split across two paragraphs. | | |
| W9 | B, NY | "LAST MONTH… SENT SECRET SHOPPERS": the release dates the announcement, not the shopping. | PARTIALLY CONFIRMED | ag.ny.gov, Oct 15, 2026 |
| W10 | C | "ALMOST 100 DOLLARS LESS THAN PAYING FOR BOTH" is Walmart's claim, now unattributed. | CONFIRMED (as Walmart's claim) | corporate.walmart.com, Oct 20, 2026 |
| W11 | C, Paige | No button after clip 11; OUT: not in the house format; primary-member caveat gone (precision). | | |
| W12 | C, Costco header | "THEY DON'T WANT YOU TO KNOW ABOUT" says Costco hides perks it advertises. | | costco.com member benefits pages |
| W13 | C, Costco | "KYLE CUT OUT AD IN THE MIDDLE" in bold black prints as a header Jeff reads; make it a red cue. | | |
| W14 | B, Jeff video | Supercut still to cut. | | SUPERCUT_HANDOFF.md |
| W15 | Whole show | Exclamation-line rate 0.079 (check_bible ERROR, band 0.08–0.20); 5 lines over 16 words; 3 runs of clips with no takeaway (A clips 1–3, B 6–8); 8 outside clips counted in one segment (A has 5). | | check_bible / mechanical |
| W16 | Whole show | Two sponsor breaks (producer decision; Chapter inside B after Lori, OmniWatch after A). | | |

### NOTES (14)

Tease B "THEN THE CHECKOUT HABIT" (checker false positive; paid off by name) · "NEARLY 50 MILLION" is NAUPA via Yahoo/Moneywise, PARTIALLY CONFIRMED · demo: add "not an ad, make sure it ends in dot gov" · Florida flow: "CLAIM"/"CLAIMED PROPERTY CART" confirmed, "personal account" depends on the recording · "REPEART" typo; tips lost their numbering · Barbara "claimed it herself": the detective helped (PARTIALLY CONFIRMED) · OmniWatch free scan CONFIRMED; the black line has no dash and is sponsor copy (house: marked, not written) · "THEN INSPECTORS…" dangles after the break · "AND WHEN A PRICE SHOWED UP WRONG" needs "?" · NY segment lost its header · C header "COMBINING": bundled, not merged · "$20" → "20 DOLLARS"; gas line lost "PARTICIPATING" · (((GRAPHIC 002))) → (((INSERT GRAPHIC 002))) · Costco fragment "BEFORE YOU PAY FULL PRICE SOMEWHERE ELSE…" trails off; "WATCH THIS VIDEO NEXT" names no video. Mechanical: 11 cues not visually confirmed; 7 JEFF notes (all guard airing lines).

### VERDICT: NOT READY — 8 BLOCKERs (one factual, seven clip-format/contract)

**Fastest path to READY**

One-line edits (no judgment needed):
1. B1: replace the father-and-son bridge line (exact text in the table).
2. B2, B3, B5, B6: rewrite the four clip blocks into marker / OUT: / red source line (exact text in the annotated bible).
3. B7: renumber Paige → CLIP 10, Costco → CLIP 11 VERTICAL.
4. B8: add "-ONLY THE MAIN SAM'S CLUB PLUS MEMBER GETS WALMART+." after clip 10 and finish the Costco takeaway.
5. W8, W13, NOTE typos: join the split line; Kyle's note to a red cue; REPEAT; "?".

Needs a call from you:
6. B4: keep LOCAL 12's verified page link, or have someone re-time on the YouTube copy.
7. Dates (W2–W5, W7): restore "date it on air" lines, or accept them undated.
8. W1, W10, W12: tease, Walmart attribution, Costco header wording.
9. Clip 5 (Delaware): the open producer cue.


## ANNOTATED BIBLE

**11/04 WED**

-BEFORE YOU THROW AWAY ONE MORE LETTER ABOUT MONEY YOU'RE OWED… WATCH THIS VIDEO!!

**THE STATE MAY BE HOLDING MONEY WITH YOUR NAME ON IT**

-A WOMAN KEPT GETTING LETTERS ABOUT MONEY THAT WAS HERS.

-SHE WAS SO SURE IT WAS A SCAM… SHE CALLED THE **POLICE**!!

-AND WHAT THE DETECTIVE FOUND IN HER MAIL PILE CHANGED HER LIFE.

-AND ONE STATE IS ACCUSED OF SELLING A MAN'S **AMAZON STOCK** FOR 8 THOUSAND DOLLARS…

-BY THE TIME HE FOUND OUT, IT WAS WORTH MORE THAN 100 THOUSAND!!

-PLUS THE **FREE SEARCH** THAT SHOWS IF YOUR STATE IS HOLDING YOURS.

**—------------------------------------------------**

**THE FEDERAL GOVERNMENT AND 20 STATES JUST FILED A MASSIVE LAWSUIT AGAINST DOLLAR GENERAL**

-YOU GRAB IT OFF THE SHELF. YOU SEE THE PRICE. YOU THINK YOU KNOW WHAT YOU'RE PAYING.

-NOW THE GOVERNMENT IS SUING… OVER WHAT HAPPENS AT CHECKOUT.

-THEN THE **CHECKOUT HABIT** THAT PROTECTS YOU.

[NOTE — the checker reads this as giving away a step. It's a promise, paid off by name in B's list ("THAT'S THE CHECKOUT HABIT I PROMISED YOU"). No change needed; "THEN" could be "PLUS".]

**—------------------------------------------------**

**PAYING FOR WALMART+ AND SAM'S CLUB? YOU MAY BE PAYING TWICE**

-WALMART JUST BUNDLED THEM… FOR **120 DOLLARS** A YEAR.

-ALREADY PAYING FOR BOTH? WAIT UNTIL YOU SEE WHAT ONE SHOPPER GOT BACK.

-PLUS TWO **COSTCO** PERKS MOST MEMBERS NEVER USE.

[WARNING — TEASE / BODY: the body no longer has two Costco perks; it's a TikTok rundown of several. "Most members never use" has no source. Fix: "-PLUS **COSTCO** PERKS YOU'RE ALREADY PAYING FOR."]

**—------------------------------------------------**

HIT LIKE AND SUBSCRIBE

JOIN THE CHAT

[[PAGE BREAK]]

**THERE'S MONEY OUT THERE WITH YOUR NAME ON IT… AND YOU'VE NEVER LOOKED**

-STATES ARE HOLDING ABOUT **70 BILLION DOLLARS** THAT BELONGS TO PEOPLE LIKE YOU. {{JEFF PLEASE NOTE: $70 billion and "about 1 in 7" are estimates from NAUPA, the state unclaimed-property administrators' group. Most finds are small, often under $1,000.}}

-NEARLY 50 MILLION AMERICANS ARE OWED MONEY BY THEIR STATE.

[FACT-CHECK: PARTIALLY CONFIRMED — NAUPA's "one in seven Americans (about 50 million people)" as reported by Yahoo Finance/Moneywise (Apr 22, 2026); not yet read on NAUPA's own page. One other guide says 33 million. Consider "ABOUT ONE IN SEVEN OF US." — NOTE]

-OLD PAYCHECKS. BANK ACCOUNTS. INSURANCE CHECKS. EVEN STOCK.

-AND MOST PEOPLE NEVER LOOK.

**THIS MAN SEARCHED HIS WIFE'S NAME… AND FOUND A JOB SHE HAD 20 YEARS AGO**

-THIS GUY DECIDED TO SEARCH FOR HIS WIFE.

[WARNING — runway is 2 lines (checker ERROR: 6–10). The 2002 Ruby Tuesday detail and the 2023 date came out, so this 2023 video now reads as new. Fix: restore "-BACK IN 2002, SHE WORKED AT A RUBY TUESDAY." and "-HE POSTED THIS BACK IN 2023."]

-SO WHAT WAS STILL SITTING THERE IN HER NAME???

-LISTEN TO THIS.

(((PLAY CLIP 1 VERTICAL)))

**0:05 - 0:58 (DOT GOV)**

[BLOCKER — CLIP 1 FORMAT: no OUT: line; the ranges are bold black lines (they render as 23pt headers Jeff reads), not the red source line; the URL sits 4 lines below the marker. These ranges also differ from the outline (plan: 0:05–0:12 BUTT 0:52–0:58 BUTT 1:56–2:15) and can't be checked from here (TikTok). Fix: "OUT: (HAD MONEY IN THERE)" then "((([TikTok @pearlmania500](URL) · 0:05 - 0:58 (DOT GOV) · BUTT · 1:56 - 2:15 (HAD MONEY IN THERE))))"; update the outline row.]

**BUTT**

**1:56 - 2:15 (HAD MONEY IN THERE)**

((([TikTok @pearlmania500](https://www.tiktok.com/@pearlmania500/video/7220912200855178538))))

-A PAYCHECK. FROM TWO DECADES AGO!! STILL WAITING FOR HER.

-SO DON'T JUST SEARCH YOUR NAME. SEARCH YOUR FAMILY'S TOO.

[[PAGE BREAK]]

**HERE'S HOW TO PROTECT YOURSELF**

-HERE'S THE **FREE SEARCH** I PROMISED YOU.

(((SHOW-PRODUCED: DEMO - MISSINGMONEY.COM SEARCH ON SCREEN. SCREEN RECORDING OR SCREENSHOTS, NOT LIVE)))

[WARNING — the cue says MISSINGMONEY.COM, but the steps below search "[state] unclaimed property" and use a state .gov site (Florida's). Fix the cue: "(((SCREEN RECORDING - STATE UNCLAIMED PROPERTY SEARCH, FLORIDA)))". The (((END SCREENSHARE))) below then closes it.]

-TYPE YOUR **STATE’S NAME** AND **“UNCLAIMED PROPERTY.”**

-FOR EXAMPLE **“FLORIDA UNCLAIMED PROPERTY.”**

-CLICK ON THE **DOT GOV** LINK.

[NOTE — searching "[state] unclaimed property" also returns ads and paid finder sites. One line closes it: "-NOT AN AD. MAKE SURE THE ADDRESS ENDS IN DOT GOV."]

-WE WILL GO WITH A **PERSONAL ACCOUNT**.

[FACT-CHECK: PARTIALLY CONFIRMED — Florida's site (fltreasurehunt.gov/ClaimSearch) uses "CLAIM" and a "CLAIMED PROPERTY CART"; "personal account" and "name and city" match the screen recording only if it's Florida's site. Other states differ. — NOTE]

-ENTER YOUR **NAME AND CITY**.

-THEN CHECK THE RESULTS.

-CLICK **CLAIM**, **ADD TO CART**, AND CHOOSE WHETHER THIS IS FOR YOURSELF OR SOMEONE ELSE.

-FINALLY CLICK **CONTINUE** AND COMPLETE THE FORM.

(((END SCREENSHARE)))

-REPEART FOR EVERY STATE YOU'VE EVER LIVED OR WORKED IN.

[NOTE — typo: REPEAT. The list also lost its numbering (NUMBER ONE…); Jeff numbers tips.]

-SEARCH YOUR MAIDEN NAME. MISSPELLINGS. NICKNAMES.

-AND LOVED ONES WHO HAVE PASSED. FAMILY CAN OFTEN CLAIM IT.

-NEVER PAY A FINDER. NEVER GIVE YOUR SOCIAL SECURITY NUMBER TO SOMEONE WHO CALLED YOU.

-CHECK AGAIN EVERY YEAR. NEW MONEY LANDS ALL THE TIME!! 
[[PAGE BREAK]]

**THINK THAT LETTER ABOUT YOUR MONEY IS A SCAM? CHECK BEFORE YOU TOSS IT**

-IN FLORIDA, BARBARA IS **88**.

-LETTER AFTER LETTER SHOWED UP.

-ALL OFFERING TO GET HER MONEY SHE WAS OWED… FOR A CUT.

-SHE WAS SURE IT WAS A SCAM. SO SHE CALLED THE POLICE.

-AN **ELDER FRAUD DETECTIVE** WENT THROUGH HER MAIL PILE.

-AND IN THERE WAS ONE LETTER FROM THE **STATE OF FLORIDA** ITSELF.

-SO WHAT WAS SHE OWED???

-HERE SHE IS, TALKING TO FOX 13. LISTEN.

(((PLAY CLIP 2 HORIZONTAL)))
OUT: (BEST THING THAT EVER HAPPENED TO ME)

((([FOX 13 Tampa Bay](https://www.fox13news.com/news/elderly-florida-woman-collects-108k-unclaimed-funds-after-thinking-she-was-getting-scammed) · 0:20 - 0:31 (GIVES MONEY AWAY) · BUTT · 0:56 - 1:22 (FIND OUT BEFORE I DIED) · BUTT · 1:35 - 1:51 (BEST THING THAT EVER HAPPENED TO ME))))

-108 THOUSAND DOLLARS!! FROM A JOB SHE HAD 30 YEARS AGO.

[WARNING — date dropped: FOX 13's story is Sept 3, 2025, and the outline flagged "date it on air." Add "-THAT WAS LAST YEAR."]

-SHE CLAIMED THE MONEY HERSELF AND NEVER NEEDED THE HELP OFFERED IN THOSE LETTERS. {{JEFF PLEASE NOTE: The letters were from law firms and private investigators ("finders"). FOX 13 says they're allowed to contact people for a fee, using Florida public records. The detective helped her claim it free at fltreasurehunt.gov.}}

[FACT-CHECK: PARTIALLY CONFIRMED — the detective helped her check fltreasurehunt.gov and fill out the paperwork (FOX 13, 1:26–1:32). "Herself" means without a finder, which is true. — NOTE]

-THESE COMPANIES ARE CALLED **FINDERS**. THEY WANT A CUT.

-YOU DON'T NEED THEM. SEARCHING AND CLAIMING ARE **FREE**.

[[PAGE BREAK]]

**SO HOW DOES YOUR MONEY END UP WITH THE STATE? IT'S THE LAW**

-A COMPANY OWES YOU MONEY. A REFUND. A DEPOSIT. A LAST PAYCHECK.

-IF IT CAN'T REACH YOU FOR A FEW YEARS…

-THE LAW MAKES IT HAND THAT MONEY TO YOUR STATE. {{JEFF PLEASE NOTE: How long depends on the state and the account, usually one to five years; three is common.}}

-THE STATE HOLDS IT IN YOUR NAME. UNTIL YOU CLAIM IT.

-SOUNDS SIMPLE. IT ISN'T.

[[PAGE BREAK]]

**EVEN WHEN YOU FIND IT… THE STATE MAY NOT HAND IT OVER**

-SUSAN FOUND HER OWN MONEY ON THE **ILLINOIS** STATE SITE.

-**19,379 DOLLARS**. ESCROW MONEY FROM A REAL ESTATE DEAL.

-SHE LEFT IT BEHIND ABOUT A DECADE AGO.

-SHE SENT THE STATE PILES OF PAPERWORK.

-AND THE STATE AGREES IT'S HER MONEY.

-SO WHY CAN'T SHE GET IT???

-HERE SHE IS, TALKING TO ABC7 CHICAGO. LISTEN.

(((PLAY CLIP 3 HORIZONTAL)))
OUT: (A LOOPHOLE THAT THEY NEED TO FIGURE OUT)

((([ABC7 Chicago I-Team](https://www.youtube.com/watch?v=dbBueUfmuSI) · 0:15 - 0:25 (THAT I CHANGED MY NAME) · BUTT · 1:00 - 1:20 (A LOOPHOLE THAT THEY NEED TO FIGURE OUT))))

-THE STATE WANTS SIGNATURES FROM TWO OTHER COMPANIES IN THAT DEAL…

-AND BOTH ARE **OUT OF BUSINESS**!!

-THE TREASURER'S OFFICE SAYS IT HAS TO FOLLOW THE LAW.

-THAT WAS LAST YEAR. SO IF YOU FIND MONEY… CLAIM IT RIGHT AWAY. DON'T SIT ON IT.

[[PAGE BREAK]]

**YOU DON'T EVEN HAVE TO LOSE TRACK OF IT. THEY CAN TAKE IT ANYWAY**

-EUGENE AND ANN LIVED IN THE SAME HOUSE IN **CALIFORNIA** FOR 30 YEARS.

-SAME ADDRESS. NOTHING LOST.

-THEY HAD **275 THOUSAND DOLLARS** IN INVESTMENTS AT **CHARLES SCHWAB**.

-THEY JUST HADN'T TOUCHED THE ACCOUNT IN THREE YEARS.

-THEN HIS STATEMENT CAME… AND IT WAS A COLUMN OF ZEROS!!

-SO WHERE DID IT GO???

-HERE'S CBS SACRAMENTO. WATCH THIS. THIS IS CRAZY.

[[PAGE BREAK]]

(((PLAY CLIP 4 HORIZONTAL)))
OUT: (THAT'S A LOT OF NERVE)

((([CBS Sacramento](https://www.youtube.com/watch?v=80djyAsS-YE) · 0:12 - 0:46 (TO THE STATE'S UNCLAIMED PROPERTY PROGRAM FOR SAFEKEEPING) · BUTT · 1:01 - 1:15 (THIS IS UNCONSTITUTIONAL STEALING) · BUTT · 2:32 - 2:48 (THAT'S A LOT OF NERVE))))

-"A LOT OF NERVE."

[WARNING — date dropped: this CBS Sacramento case is from 2021. Restore "AND THIS WAS BACK IN 2021."]

-SCHWAB AND THE STATE BOTH SAY THEY SENT **WARNING LETTERS**. HE SAYS HE NEVER GOT THEM. {{JEFF PLEASE NOTE: After reporters stepped in he could claim it all. At the time of the report the state had returned $50,000 in cash and the stock was still being transferred back.}}

-SO LOG INTO EVERY ACCOUNT YOU HAVE. AT LEAST ONCE A YEAR.

**AND HERE'S THE PART THAT'LL MAKE YOU SICK… SOME STATES SELL IT**

-IF IT'S STOCK, SOME STATES DON'T JUST HOLD IT. THEY SELL IT.

-ONE MAN BOUGHT **AMAZON** STOCK BACK IN THE '90S.

-WHEN HE WENT TO CASH IT OUT, IT WAS WORTH MORE THAN **100 THOUSAND DOLLARS**.

-BUT THE STATE OF **DELAWARE** HAD ALLEGEDLY ALREADY SOLD IT. YEARS EARLIER.

-SO HOW MUCH DID IT SELL FOR???

-HERE'S CBS NEWS CALIFORNIA. WATCH THIS. THIS IS NUTS.

(((PLAY CLIP 5 HORIZONTAL)))
OUT: (BY THE TIME YOU FIND YOUR UNCLAIMED FUNDS)

((([CBS News California](https://www.youtube.com/watch?v=1Grj5UvPLwo) · 2:09 - 2:23 (FOR JUST $8,000) · BUTT · 2:56 - 3:07 (BY THE TIME YOU FIND YOUR UNCLAIMED FUNDS))))

**-8 THOUSAND DOLLARS. BY THE TIME HE FOUND OUT, IT WAS WORTH MORE THAN 100 THOUSAND. UNREAL!** {{JEFF PLEASE NOTE: The Delaware sale is an allegation in the CBS report. The man isn't named or shown, and the clip carries no response from Delaware.}}

-AND IN **CALIFORNIA**, THE LAW SAYS THE STATE HAS TO SELL IT WITHIN **20 MONTHS**.

-LAWMAKERS FROM BOTH PARTIES ARE PUSHING TO STOP THAT.

-SO DON'T WAIT. THE LONGER IT SITS, THE MORE YOU CAN LOSE.

(((PRODUCER - CLIP 5 IS A FIFTH OUTSIDE CLIP IN A, AND THE MAN IS NEVER NAMED OR SHOWN. KEEP IT, OR FOLD THE DELAWARE SALE INTO JEFF'S LINES AND CUT THE CLIP?)))

[PRODUCER QUESTION — still open. A has 5 outside clips (house standard about two a segment).]

[[PAGE BREAK]]

**AND THE MINUTE YOU START LOOKING… THE CROOKS SHOW UP**

-THE SECOND PEOPLE START SEARCHING, SCAMMERS SEE AN OPENING.

-IN CALIFORNIA, A FATHER AND SON OFFERED TO RECOVER PEOPLE'S UNCLAIMED MONEY.

-PROSECUTORS SAY THEY USED **FORGED DOCUMENTS** AND FAKE ADDRESSES… AND STOLE MORE THAN **1.6 MILLION DOLLARS**!!

(((TAKE STILL - CALIFORNIA ATTORNEY GENERAL PRESS RELEASE, JULY 30, 2010)))

-THEY HAD YOUR NAME. YOUR ADDRESS. AND YOUR TRUST.

[WARNING — the 2010 date and the JEFF note (charged in 2010; outcome not confirmed) came out, so a 16-year-old prosecution now reads as current. Restore "-THAT WAS BACK IN 2010." and the note.]

-HERE'S YOUR RED FLAG: ANYONE WHO CONTACTS **YOU** FIRST… AND WANTS A CUT, A FEE OR YOUR SOCIAL SECURITY NUMBER.

-SEARCHING IS FREE. CLAIMING IS FREE. DO IT YOURSELF.

-THAT FATHER AND SON? ALL SCAMMERS NEEDED WAS A NAME AND SOCIAL SECURITY NUMBER.

[FACT-CHECK: CONTRADICTED — the California AG's release (July 30, 2010) says they used "forged documents and fictitious mailing addresses" and were finders their victims hired; it says nothing about Social Security numbers. Fix: "-THAT FATHER AND SON? ALL THEY NEEDED WAS A NAME, AN ADDRESS AND SOME FORGED PAPERWORK." — BLOCKER]

-NOW IMAGINE A STRANGER ALREADY HAS YOURS… FROM A DATA BREACH.

(((SPONSOR TEASE - KILL BANNERS)))

-YOU’D WANT TO KNOW IF YOUR INFORMATION IS OUT THERE.

-THAT’S WHERE OUR SPONSOR, **OMNIWATCH**, COMES IN.

THEY OFFER A FREE DARK WEB SCAN SO YOU CAN SEE IF YOUR PERSONAL INFORMATION IS OUT THERE.

[FACT-CHECK: CONFIRMED — omniwatch.com/scan and /features/dark-web-monitoring (free scan of email, phone and other identifiers). Sponsor's own claim. NOTE: no leading dash; house rule is sponsor copy marked, not written, so confirm this matches OmniWatch's talking points.]

(((OMNIWATCH SPOT)))

[[PAGE BREAK]]

**THE PRICE ON THE SHELF IS A PROMISE… AND THE REGISTER ISN'T ALWAYS KEEPING IT**

-I'VE BEEN WARNING YOU ABOUT THIS.

-THREE WEEKS AGO, WE SHOWED YOU WHAT CAN HAPPEN AT CHECKOUT.

-WATCH THIS.

(((ROLL JEFF VIDEO - OCT 14, 2026 SHOW - REGISTER SUPERCUT, STORE-NEUTRAL LINES ONLY, STILL TO CUT)))

[WARNING — production: the supercut isn't cut yet (SUPERCUT_HANDOFF.md). Store-neutral lines only.]

**NOW THE FTC AND 20 STATES ARE SUING**

-THEY SAY FOR YEARS, **DOLLAR GENERAL** CHARGED MORE AT THE REGISTER THAN ON THE SHELF.

-THE LAWSUIT SAYS THEY KNEW. AND DIDN'T FIX IT.

-IT'S A QUARTER HERE. FIFTY CENTS THERE.

-SO MOST PEOPLE NEVER CATCH IT.

-DOLLAR GENERAL HAS MORE THAN **20,000 STORES**.

-SO WHAT DID PEOPLE ACTUALLY FIND???

-HERE'S ABC NEWS. LISTEN TO THIS.

(((PLAY CLIP 6 HORIZONTAL)))
OUT: (WE WILL DEFEND THIS LITIGATION VIGOROUSLY)

((([ABC News / GMA](https://abcnews.com/video/137597689/) · 0:08 - 1:14 (WE WILL DEFEND THIS LITIGATION VIGOROUSLY))))

-TRAIL MIX. 2.75 ON THE SHELF… 5 DOLLARS AT THE REGISTER. THAT'S ALMOST DOUBLE!!

-SO NEVER ASSUME THE SHELF PRICE IS WHAT YOU'LL PAY. {{JEFF PLEASE NOTE: Filed Monday, Oct 26. These are allegations; nothing has been decided. The trail mix and chips examples are shoppers' complaints quoted in the suit.}}

[[PAGE BREAK]]

**YOU COULD BE PAYING THIS EVERY WEEK… AND NEVER KNOW IT**

-IN **OKLAHOMA**, LORI BUYS THE SAME THING EVERY WEEK. KITTY LITTER.

-ON THE SHELF? **8.95**.

-AT THE REGISTER? **10 DOLLARS**. WEEK AFTER WEEK.

-SHE NOTICED. SHE COMPLAINED TO DOLLAR GENERAL.

[FACT-CHECK: PARTIALLY CONFIRMED — she asked staff at the register, then wrote to the Oklahoma attorney general; Dollar General answered that letter with the $10 gift card (More Perfect Union captions 2:09–3:22). The 2022 date also came out. Fix: "-SHE NOTICED. SHE WROTE TO HER STATE'S ATTORNEY GENERAL." + "-THIS STARTED BACK IN 2022." — WARNING]

-SO WHAT DID THEY GIVE HER???

-LISTEN TO HER.

[[PAGE BREAK]]

((([YOUTUBE @moreperfectunion](https://www.youtube.com/watch?v=uE5THiD-kTk))))

[BLOCKER — CLIP 7 FORMAT: the source line sits above the marker, there's no OUT:, the ranges are bold black lines with a stray "))))", and a page break separates the lead-in from the clip (runway reads as 0 lines). The 2:32–2:49 slice ("I KNOW IT'S JUST NOT ME") was dropped; fine if intended, but update the outline. Fix: marker, then "OUT: (WELL, I DO)", then "((([More Perfect Union](https://www.youtube.com/watch?v=uE5THiD-kTk) · 1:46 - 2:29 (WHAT THE PRICE SAYS ON THE SHELF) · BUTT · 3:03 - 3:25 (IT WAS INSULTING) · BUTT · 8:18 - 8:34 (WELL, I DO))))".]

(((PLAY CLIP 7 HORIZONTAL)))

**1:46 - 2:29 (WHAT THE PRICE SAYS ON THE SHELF) BUTT**

**3:03 - 3:25 (IT WAS INSULTING)**

**BUTT**

**8:18 - 8:34 (WELL, I DO))))**

-A 10-DOLLAR GIFT CARD. THAT'S NOT A REFUND!!

-IF THE REGISTER IS HIGHER THAN THE TAG… SAY SO BEFORE YOU PAY.

-SHE CAUGHT IT BECAUSE SHE CHECKED WHAT SHE WAS PAYING.

-AND HERE’S ANOTHER BILL A LOT OF US NEVER

[WARNING — copy error: this line is split across two paragraphs ("…NEVER" / "CHECK… OUR MEDICARE PLAN."), so it prints as two prompter lines. Join them.]

CHECK… OUR MEDICARE PLAN.

(((SPONSOR TEASE - KILL BANNERS)))

-OPEN ENROLLMENT IS HAPPENING RIGHT NOW. IT ENDS DECEMBER 7.

-OUR SPONSOR, **CHAPTER**, CAN HELP YOU TAKE A SECOND LOOK.

(((CHAPTER SPOT)))

[[PAGE BREAK]]

**THEN INSPECTORS WENT STORE TO STORE… EVERY ONE IN THE COUNTY!!**

[NOTE — after the Chapter break, "THEN" no longer follows anything. "INSPECTORS WENT STORE TO STORE…"]

-THIS MAN IN **OHIO** SHOPS WHEREVER THE DEAL IS.

-HE'S BEEN GOING TO DOLLAR GENERAL FOR YEARS.

-BUT HIS RECEIPTS DIDN'T MATCH THE SHELF.

-SO HE TOOK THEM TO THE **COUNTY AUDITOR**.

-INSPECTORS CHECKED EVERY DOLLAR GENERAL IN THE COUNTY.

-SO HOW MANY FAILED???

-HERE'S LOCAL 12 IN CINCINNATI. CHECK THIS OUT.

(((PLAY CLIP 8 HORIZONTAL)))
OUT: (HE SAYS IT'S IMMORAL)

((([LOCAL 12 Cincinnati](https://www.youtube.com/watch?v=pI4Eehj-0LI&time_continue=3&source_ve_path=MjM4NTE&embeds_referring_euri=https%3A%2F%2Fwww.google.com%2Fsearch%3Fsca_esv%3D0b049a37ecbfba99%26rlz%3D1C1UEAD_enUS1087US1087%26sxsrf%3DAPpeQnssRMtPeKW121zAXuHJyeKg8phGQg%3A17931&themeRefresh=1) · 0:20 - 0:54 (EIGHT AND A HALF) · BUTT · 1:10 - 1:58 (HE SAYS IT'S IMMORAL))))

[BLOCKER — CLIP 8 SOURCE CHANGED: the link is now YouTube pI4Eehj-0LI ("20 Dollar General stores investigated for price discrepancies", uploaded Oct 28, 2022), with Google tracking parameters. The 0:20–0:54 / 1:10–1:58 times and outcues were verified on LOCAL 12's own page video (Oct 27, 2022, 2:20), a different upload with a possibly different intro. Captions on the new copy were bot-walled twice from here. Fix: go back to the verified page link, or check these times on the YouTube copy; trim the URL to https://www.youtube.com/watch?v=pI4Eehj-0LI.]

-ALL 20 FAILED!! ONE CREAMER: 2 DOLLARS ON THE SHELF. 4.35 AT THE REGISTER.

-SO WATCH THE SCREEN AS EVERY ITEM SCANS.

[[PAGE BREAK]]

**SO WHY DOESN'T ANYBODY FIX IT? A FORMER EMPLOYEE TELLS YOU**

-LYNDA WORKED AT DOLLAR GENERAL FOR **FOUR YEARS**, IN OHIO.

-ONE DAY A WEEK IS SUPPOSED TO BE FOR **PRICE CHANGES**.

-BUT THE SAME WORKERS RUN THE REGISTER, STOCK THE SHELVES AND CLEAN THE STORE.

-SO THE OLD TAGS STAY UP.

-AND WHEN A PRICE SHOWED UP WRONG

[NOTE — missing "?"]

-WHAT WAS SHE TOLD???

-HERE SHE IS, TALKING TO WHIO. LISTEN.

(((PLAY CLIP 9 HORIZONTAL)))
OUT: (NOT AT THE REGISTER)

((([WHIO Dayton](https://www.whio.com/news/local/i-team-former-dollar-general-employee-speaks-out-about-price-swapping-allegations/GJYUFBCY4NFHBLGLBCWOVLOEUQ/) · 0:55 - 1:43 (PRICE CHANGES THAT NEEDED TO BE DONE ON ANY PARTICULAR WEEK)

[BLOCKER — CLIP 9: the source line is unclosed (no "))))") and the 1:49–2:03 slice is gone, but OUT: still reads "(NOT AT THE REGISTER)", which is that slice's outcue. Either restore " · BUTT · 1:49 - 2:03 (NOT AT THE REGISTER))))" or change OUT: to "(PRICE CHANGES THAT NEEDED TO BE DONE ON ANY PARTICULAR WEEK)" and close the line. The new 0:55 in-point is fine (her quote starts at 0:55.9, WHIO).]

-NOT ALLOWED TO FIX IT. AT THE REGISTER!!

-SHE SAYS THAT'S WHAT A MANAGER TOLD HER.

[[PAGE BREAK]]

-LAST MONTH, NEW YORK'S ATTORNEY GENERAL SENT SECRET SHOPPERS INTO 11 DOLLAR GENERAL STORES.

[WARNING — precision: the NY AG release (Oct 15, 2026) dates the announcement, not the shopping. Fix: "-LAST MONTH, NEW YORK'S ATTORNEY GENERAL SAID ITS SECRET SHOPPERS…". The header above this segment was removed, so it now follows a page break with no header (NOTE).]

-THEY WERE OVERCHARGED ON ABOUT **14 PERCENT** OF WHAT THEY BOUGHT.

-NOW EVERY DOLLAR GENERAL IN NEW YORK HAS TO POST SIGNS. THEY'LL HONOR THE **LOWEST PRICE**. {{JEFF PLEASE NOTE: New York's settlement is $1.875 million in food and goods donated, not refunds to shoppers.}}

**HERE'S HOW TO PROTECT YOURSELF**

(((INSERT GRAPHIC 001)))

-NUMBER ONE. SNAP A PHOTO OF THE **SHELF TAG** BEFORE YOU CHECK OUT.

-NUMBER TWO. **WATCH THE SCREEN** AS EACH ITEM SCANS. THAT'S THE CHECKOUT HABIT I PROMISED YOU.

-NUMBER THREE. PRICE HIGHER THAN THE TAG? SHOW THEM THE PHOTO. ASK THEM TO MATCH IT.

-NUMBER FOUR. CHECK YOUR RECEIPT **BEFORE YOU LEAVE** THE STORE.

-NUMBER FIVE. REPORT IT TO YOUR STATE'S **ATTORNEY GENERAL**. ONE MAN'S RECEIPTS STARTED THE OHIO CASE.

[[PAGE BREAK]]

**WALMART JUST ANNOUNCED THEY’RE COMBINING THEIR TWO MEMBERSHIP PROGRAMS**

[NOTE — they're bundled, not merged: both memberships still exist on their own. "WALMART JUST BUNDLED ITS TWO MEMBERSHIPS" is exact.]

-**WALMART** **PLUS** AND **SAM'S CLUB PLUS** COME TOGETHER.

-ONE PRICE. **120 DOLLARS** A YEAR.

-THAT'S ALMOST 100 DOLLARS LESS THAN PAYING FOR BOTH.

[WARNING — Walmart's own figure, now stated as fact. Restore the attribution: "-WALMART SAYS THAT'S ALMOST 100 DOLLARS LESS…" (corporate.walmart.com, Oct 20, 2026).]

-AND IT'S COMING RIGHT FOR AMAZON.

-FOR THE YEAR, IT’S ABOUT $20 CHEAPER THAN PRIME.

[FACT-CHECK: CONFIRMED — Prime is $139 a year (amazon.com/amazonprime); $139 − $120 = $19. NOTE: write it as Jeff says it, "ABOUT 20 DOLLARS". Clip 10 (GMA, the CEO's "$139 Prime" line) was cut here, so clip numbers now skip 10 (checker ERROR).]

-SO WHAT DO YOU GET?

(((GRAPHIC 002)))

[NOTE — house cue is (((INSERT GRAPHIC 002))). Image prompt was given in chat on 10/28.]

-FREE DELIVERY… FROM WALMART AND FROM SAM'S CLUB.

-A STREAMING SERVICE. YOUR PICK OF PEACOCK OR PARAMOUNT+.

-10 CENTS OFF A GALLON OF GAS… AT MORE THAN 17,000 STATIONS.

[FACT-CHECK: PARTIALLY CONFIRMED — Walmart says "more than 17,000 participating stations" (Oct 20, 2026). Add "PARTICIPATING"; the JEFF note on the fine print came out. — NOTE]

-AND YOU GET INTO SAM'S CLUB… WITH 2 PERCENT BACK ON ELIGIBLE PURCHASES!!

-ONLY HAVE WALMART+? IT'S 22 DOLLARS MORE TO ADD ALL THE SAM'S CLUB PLUS PERKS.

-SAM'S CLUB MEMBER? 60 DOLLARS MORE GETS YOU PLUS… AND WALMART+ COMES WITH IT.

-ALREADY HAVE SAM'S CLUB PLUS? WALMART+ IS FREE. JUST TURN IT ON IN THE APP.

[[PAGE BREAK]]

**AND IF YOU’RE ALREADY PAYING FOR BOTH? YOU MAY BE OWED MONEY BACK**

-YOU JUST NEED TO LINK THE TWO ACCOUNTS.

-WALMART SAYS MOST MEMBERS GET A **PRORATED REFUND** FOR WALMART+.

-PAIGE SHOPS AT SAM'S CLUB. SHE PAID FOR BOTH.

-SO SHE LINKED HER ACCOUNTS IN THE APP.

-AND THE REFUND SHOWED UP.

-SO HOW MUCH CAME BACK???

-CHECK THIS OUT.

(((PLAY CLIP 11 VERTICAL)))
OUT: 0:13   “MEMBERSHIP”

[WARNING — CLIP 11 FORMAT: OUT: should carry the outcue in parens and the red source line the range: "OUT: (PRO-RATED WALMART PLUS MEMBERSHIP)" / "((([TikTok @paigeanne80](URL) · 0:00 - 0:13 (PRO-RATED WALMART PLUS MEMBERSHIP))))". Unverified (TikTok). There's no button after the clip: it goes straight into the Costco header (voice: a one-line button out of every clip). The $14.29 line and "only the main Sam's Club Plus member gets Walmart+" came out; the second is a precision WARNING, since household members will look for a Walmart+ they don't get.]

((([TikTok @paigeanne80](https://www.tiktok.com/@paigeanne80/video/7698845156170042638))))

**NEXT IF YOU'RE A COSTCO MEMBER… WE FOUND HIDDEN PERKS THAT THEY DON’T WANT YOU TO KNOW ABOUT**

[WARNING — overreach: "THEY DON'T WANT YOU TO KNOW ABOUT" says Costco hides these; Costco advertises its member perks on its own site. Fix: "IF YOU'RE A COSTCO MEMBER… HIDDEN PERKS YOU'RE ALREADY PAYING FOR". "NEXT" isn't needed in a header.]

-WATCH THIS

(((PLAY CLIP XXX)))

[BLOCKER — CLIP CONTRACT: no number, no orientation, no OUT:, and the link isn't in the red source line. This clip isn't in the outline (new 10/28) and can't be checked from here (TikTok short link). Fix: "(((PLAY CLIP 11 VERTICAL)))" (renumbered after clip 10's cut), "OUT:" (blank, manual), "((([TikTok](https://www.tiktok.com/t/ZPLD19Yxe/))))". Runway is 2 lines (checker ERROR); add who made it and what's in it once someone has watched it.]

[https://www.tiktok.com/t/ZPLD19Yxe/](https://www.tiktok.com/t/ZPLD19Yxe/)

**KYLE CUT OUT AD IN THE MIDDLE**

[WARNING — a production note in bold black prints as a 23pt header Jeff reads. Make it red: "(((EDIT - KYLE CUT OUT THE AD IN THE MIDDLE)))".]

-HOW MANY OF THOSE DID YOU KNOW ABOUT? TELL US IN THE COMMENTS.

-YOU'RE ALREADY PAYING FOR THE MEMBERSHIP…

-SO USE WHAT COMES WITH IT. BEFORE YOU PAY FULL PRICE SOMEWHERE ELSE…

[NOTE — fragment: "BEFORE YOU PAY FULL PRICE SOMEWHERE ELSE…" trails off. Either "…CHECK WHAT YOUR MEMBERSHIP ALREADY COVERS." or cut it.]

[[PAGE BREAK]]

-YOUR STATE. THE REGISTER. YOUR MEMBERSHIPS. THAT'S MONEY THAT'S ALREADY YOURS… GO GET IT!!

-SEND THIS TO SOMEONE WHO'S NEVER SEARCHED FOR THEIR MONEY… BEFORE THE NEXT LETTER SHOWS UP!!

-AND WATCH THIS VIDEO NEXT.

[NOTE — no video named and the producer cue came out. Name the end-screen video.]

-SEE YOU NEXT TIME.

-END OF SHOW


## SOURCE LOG

| CLAIM | CONFIDENCE | SCOPE | SOURCE |
|---|---|---|---|
| **UNCLAIMED PROPERTY — NAUPA AND HOW IT WORKS** | | | |
| States holding about $70 billion | PARTIALLY CONFIRMED | NAUPA estimate, all states, 2026 | NAUPA as reported by Recording Law (9/23/2026), AOL (3/29/2026). Not yet read on unclaimed.org itself. |
| Nearly 50 million Americans owed money | PARTIALLY CONFIRMED | NAUPA "one in seven (about 50 million people)" | Yahoo Finance / Moneywise, Apr 22, 2026, citing NAUPA. One state guide says 33 million; scope differs. |
| A company that can't reach you for a few years must hand it to the state | PARTIALLY CONFIRMED | Dormancy 1–5 years, varies by state and property | General; JEFF note carries the range. |
| Searching and claiming are free | CONFIRMED | NAUPA, official state programs | https://unclaimed.org/search/ |
| Demo: search "[state] unclaimed property", click the .gov link, CLAIM, cart | PARTIALLY CONFIRMED | Florida's site only | https://www.fltreasurehunt.gov/ClaimSearch — "CLAIM" button and "CLAIMED PROPERTY CART". Other states differ. |
| **ALEX PEARLMAN / TIKTOK** | | | |
| Wife's paycheck from a 2002 Ruby Tuesday (header: "a job she had 20 years ago") | PARTIALLY CONFIRMED | One creator, video April 2023 | Yahoo/AT&T, Nov 26, 2023, quoting Pearlman. Clip itself unreachable. |
| **BARBARA / FOX 13** | | | |
| Barbara, 88, Florida; letters from finders; called police; $108,000 from a job 30 years ago | CONFIRMED | One case, published Sept 3, 2025 | FOX 13 page video, Whisper 0:20–1:51. |
| "She claimed the money herself" | PARTIALLY CONFIRMED | Same | Same, 1:26–1:32: the detective helped her claim at fltreasurehunt.gov; no finder. |
| Finders are legal and charge a fee | CONFIRMED | Florida | Same, 2:31–2:43. |
| **SUSAN UDVANCE / ABC7 CHICAGO** | | | |
| $19,379 in escrow money; state agrees it's hers; two defunct companies; treasurer says it must follow the law | CONFIRMED | One case, Jan 28, 2025 | https://www.youtube.com/watch?v=dbBueUfmuSI captions 0:00–1:39. |
| **THE BREZNOCKS / CBS SACRAMENTO** | | | |
| $275,000 at Charles Schwab moved after three years; warning letters; he says he never got them | CONFIRMED | One case, 2021 | CBS Sacramento captions 80djyAsS-YE 0:03–3:04. |
| **DELAWARE AND CALIFORNIA STOCK SALES / CBS NEWS CALIFORNIA** | | | |
| Amazon stock sold for $8,000; worth 100K+ when he tried to cash out | CONFIRMED | One investor; sold 2008, valued ~2015 | CBS News California captions 1Grj5UvPLwo 2:09–2:23; NPR Planet Money, Feb 13, 2020. |
| California must sell within 20 months | CONFIRMED | California law | Same, 2:56–3:07. |
| Lawmakers from both parties pushing to stop it | PARTIALLY CONFIRMED | Federal bill (Liccardo, Lawler), not California | Same, 2:30–3:00. |
| **FATHER AND SON / CALIFORNIA AG** | | | |
| Offered to recover unclaimed money; forged documents and fake addresses; stole $1.6 million+ | CONFIRMED | Charged July 2010; conduct 2007–2009 | https://oag.ca.gov/news/press-releases/father-and-son-charged-stealing-16-million-unclaimed-funds-dozens-californians — outcome not confirmed. |
| "All scammers needed was a name and Social Security number" | CONTRADICTED | Same case | Same. The release cites forged documents and fictitious mailing addresses; no SSNs. |
| **OMNIWATCH** | | | |
| Free dark web scan to see if your personal information is out there | CONFIRMED | Sponsor's own offer | https://www.omniwatch.com/scan — free scan of email, phone and other identifiers. |
| **DOLLAR GENERAL — FTC SUIT AND GMA** | | | |
| FTC and 20 states sued Dollar General; register more than shelf for years; knew and didn't fix it | CONFIRMED | Allegations, filed Oct 26, 2026 | https://www.ftc.gov/news-events/news/press-releases/2026/10/ftc-state-partners-sue-dollar-general-charging-consumers-more-advertised-many-products |
| Trail mix $2.75 shelf, $5 register; "we will defend this litigation vigorously" | CONFIRMED | One shopper complaint quoted in the suit | ABC News/GMA video 137597689, Whisper 0:30–1:14. |
| More than 20,000 stores | CONFIRMED | Company-wide | Same, 1:14. |
| **LORI HARTLINE / MORE PERFECT UNION** | | | |
| Kitty litter $8.95 tag, $10 register, week after week | CONFIRMED | One shopper, began May 2022 | More Perfect Union captions uE5THiD-kTk 1:38–2:29. |
| "She complained to Dollar General" | PARTIALLY CONFIRMED | Same | Same, 2:49–3:22: she asked staff, then wrote to the Oklahoma AG; Dollar General answered with a $10 gift card. |
| **BUTLER COUNTY / LOCAL 12** | | | |
| All 20 stores failed; creamer $2 shelf, $4.35 register | CONFIRMED | Butler County, OH, Oct 2022 | LOCAL 12 page video (Oct 27, 2022), Whisper 0:20–1:58. Not checked on the new YouTube copy. |
| **LYNDA SWANK / WHIO** | | | |
| Four years at Dollar General; one day a week for price changes; manager said not at the register | CONFIRMED | One former employee, Nov 2022 | WHIO page video (Nov 23, 2022), Whisper 0:55–2:03. |
| **NEW YORK ATTORNEY GENERAL** | | | |
| Secret shoppers at 11 stores overcharged on about 14% of items; lowest-price signs | CONFIRMED | Western New York, 11 stores; announced Oct 15, 2026 | https://ag.ny.gov/press-release/2026/attorney-general-james-secures-1875-million-food-and-goods-dollar-general |
| "Last month… sent secret shoppers" | PARTIALLY CONFIRMED | Same | Same. Dates the announcement, not the shopping. |
| **MEDICARE OPEN ENROLLMENT / CHAPTER** | | | |
| Open enrollment happening now, ends December 7 | CONFIRMED | Oct 15 – Dec 7, every year | https://www.medicare.gov/health-drug-plans/open-enrollment |
| **WALMART+ AND SAM'S CLUB PLUS** | | | |
| $120 a year; almost $100 less than paying for both | CONFIRMED | Walmart's own figures, Oct 20, 2026 | https://corporate.walmart.com/news/2026/10/meet-your-120-life-hack — Walmart's claim; attribute it. |
| About $20 cheaper than Prime | CONFIRMED | Prime $139/yr vs $120 | https://www.amazon.com/amazonprime |
| Free delivery, Peacock or Paramount+, 10 cents a gallon at 17,000+ stations, Sam's Club access, 2% back | CONFIRMED | Walmart's list; gas at participating stations | Same Walmart release, footnotes 1–5. |
| +$22 for Walmart+ members; +$60 for Club members; Plus members turn Walmart+ on in the app; prorated refund | CONFIRMED | Same | Same. |
| Paige's $14.29 refund | UNVERIFIED | One shopper | — TikTok unreachable from the container. |
| **COSTCO** | | | |
| "Hidden perks they don't want you to know about" | UNVERIFIED | Claim about Costco's intent | — No source for Costco hiding anything. |
| **CLIP SOURCES** | | | |
| Clip 1 — Pearlman, TikTok 7220912200855178538, 0:05–0:58 (DOT GOV) BUTT 1:56–2:15 (HAD MONEY IN THERE) | UNVERIFIED | Producer's ranges; outline had three slices | — TikTok unreachable; format BLOCKER B2. |
| Clip 2 — FOX 13 page, 0:20–1:51, three slices | CONFIRMED | Matches outline A3 | FOX 13 page video, Whisper. |
| Clip 3 — ABC7 dbBueUfmuSI, 0:15–0:25 BUTT 1:00–1:20 | CONFIRMED | Matches outline A5 | https://www.youtube.com/watch?v=dbBueUfmuSI |
| Clip 4 — CBS Sacramento 80djyAsS-YE, three slices to 2:48 | CONFIRMED | Matches outline A6; response line follows | CBS captions. |
| Clip 5 — CBS News California 1Grj5UvPLwo, 2:09–2:23 BUTT 2:56–3:07 | CONFIRMED | Matches outline A7 | CBS captions. |
| Jeff video — 10/14 show supercut | | Still to cut | SUPERCUT_HANDOFF.md |
| Clip 6 — ABC News/GMA 137597689, 0:08–1:14 | CONFIRMED | Matches outline B2 | Whisper. |
| Clip 7 — More Perfect Union uE5THiD-kTk, 1:46–2:29 BUTT 3:03–3:25 BUTT 8:18–8:34 | CONFIRMED | Outline B3 minus the 2:32–2:49 slice | Captions; format BLOCKER B3. |
| Clip 8 — LOCAL 12, now YouTube pI4Eehj-0LI | UNVERIFIED | Times verified on the page video, not this copy | — Captions bot-walled twice; BLOCKER B4. |
| Clip 9 — WHIO page, 0:55–1:43 (slice 2 dropped) | CONFIRMED | 0:55 in-point verified (her quote at 0:55.9) | WHIO Whisper; OUT: mismatch BLOCKER B5. |
| Clip 10 — GMA PQORnk7zuLc | | Cut by producer | Outline C1 row needs updating. |
| Clip 11 — Paige TikTok 7698845156170042638, out 0:13 | UNVERIFIED | Producer's out-point | — TikTok unreachable. |
| Costco clip (unnumbered) — TikTok short link ZPLD19Yxe | UNVERIFIED | New, not in outline | — TikTok unreachable; BLOCKER B6. |
| **PRODUCER QUESTIONS — ANSWERED** | | | |
| (((PRODUCER - CLIP 5 IS A FIFTH OUTSIDE CLIP IN A…))) | | | Still open. Recommendation unchanged: keep only if A has the time; the clip carries the $8,000 that the button repeats. |
| Paige's surname and permission (cue removed in this version) | | | Not answered in the document. Confirm before air. |
| Chapter talking points (cue removed) | | | Not answered in the document. The bridge makes no claim beyond open enrollment dates. |
| **TEASE / BODY CONSISTENCY** | | | |
| Delaware $8,000 / 100K+ in tease and A body | CONFIRMED | Same story | Tease lines 7–8 and A button agree after the 10/28 fix. |
| "Free search" promise | | | Paid off by name: "HERE'S THE FREE SEARCH I PROMISED YOU." |
| "Checkout habit" promise | | | Paid off by name in B's list. |
| "Two Costco perks" in tease | | | Body no longer has two named perks (W1). |
