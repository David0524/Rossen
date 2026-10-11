# 10/14 LIVE BIBLE — FINAL REVIEW (uploaded draft)

**What I reviewed:** your uploaded `10_14_Wed -- THIS FREE SAMPLE COST HER $26000.docx`.
- It's saved in this folder as `10_14_Wed -- THIS FREE SAMPLE COST HER 26000 (uploaded).docx` and converted to `draft.md` here, one paragraph per line, with the hyperlinks kept.
- It is your edit, not `runs/W_10142026/draft.md`. Story A now has 4 clips: the CBS LA Chisholm interview (6OGQ) is gone and the CBS "store dark" package is clip 3.
- Every cue was checked against `runs/W_10142026/outline.md`, the approved Stage: videos manifest.

**Stage:** final. The clip manifest is locked. Every cue has its URL as a hyperlink on the line under `OUT:`.
- The mechanical pass reads plain text, so it reported "no URL" on all 9 cues. That's a conversion artifact; I've overruled it below.
- `check_bible.py` flagged the numbered markers and the filled `OUT:` lines. That is the house format you asked for at this stage, so it isn't a defect.
- I imported the rest of `check_bible.py` as-is.

**Source list supplied:** yes. I used the run's `SOURCE_LOG.md` and the caption transcripts (`transcripts.json`) first, then searched the web for everything else.

**Fact-check coverage:** 42 of 44 claims fully searched. Two are logged UNVERIFIED:
- "employee fixed it only because she asked" — the write-up page wouldn't load.
- Clip 9's content — a TikTok with no transcript.

I can't watch video. Clip descriptions below are checked against transcripts and metadata only.

**The three-critic panel's findings are folded in.** All of them were re-checked against the sources before they went in.

**VERDICT: NOT READY.** 3 BLOCKERs, and one is a legal risk (#1).

## Fastest path to READY

One-line edits:

1. **#1:** the letter starts at 3:03, so every frame of the current BUTT is the accusation. Two ways to fix it, both cut from the same transcript:
   - **Recommended:** swap the BUTT to **2:39–3:02**, Voigtman: "This is um fraud… it's not going to change unless people speak up." New outcue `(UNLESS PEOPLE SPEAK UP)`. Change the button to `HIS ATTORNEY SAYS THE STORE IS DEFLECTING. CBS REPORTS LAPD IS INVESTIGATING.`
   - **Or:** keep 3:03 and run it to **3:40**, through the rebuttal ("calling the harassment claim baseless… likely criminal behavior by B&H company and its employees"). New outcue `(AND ITS EMPLOYEES)`. Change the button to `THE STORE'S LAWYER MADE ACCUSATIONS ABOUT HIM IN A LETTER. HIS ATTORNEY CALLS THEM BASELESS.` This airs the accusation, so take it to standards.
2. **#2:** cut `TARGET AND`. Change the line to `AND IT'S NOT JUST ONE STORE. LAST YEAR DOLLAR GENERAL PAID MORE THAN A MILLION DOLLARS IN PENNSYLVANIA FOR RINGING UP MORE THAN THE SHELF.`
3. **#3:** `WATCHED THE STORE FOR WEEKS` → `FOR MONTHS`.
4. **#12:** `YOUR COUNTRY'S FREE PROPERTY-FRAUD ALERT` → `YOUR COUNTY'S`. Add `IF YOUR COUNTY OFFERS ONE.`
5. **#4 (header):** `CBS LOS ANGELES CAUGHT ONE STORE IN THE ACT` → `CBS LOS ANGELES WENT AFTER ONE OF THESE STORES`.
6. **#4 (tease):** `HIS CAREGIVER TOOK HIS HOUSE FOR $5` → `POLICE SAY HIS CAREGIVER TOOK HIS HOUSE FOR $5`.
7. **#6:** `POLICE SAY THE 27-YEAR-OLD OWNER… KEPT FLATTERING HER… AND THEN DROVE HER TO HER CREDIT UNION` → `SHE SAYS THE 27-YEAR-OLD OWNER… KEPT FLATTERING HER. COURT RECORDS SAY HE TOOK HER TO HIS CAR AND SENT HER INTO HER CREDIT UNION.`
8. **#7:** `HE'S CHARGED, NOT CONVICTED` → `HE WAS CHARGED WITH ATTEMPTED THEFT IN JANUARY 2025 AND PLEADED NOT GUILTY.`
9. **#11:** start the $5.6M line with `AND` instead of `BUT`. Add `AND SELLING FOOD THAT WEIGHED LESS THAN THE LABEL.`
10. **#19:** the B close says `NEXT, THE WALMART REGISTER THAT CHARGED MORE THAN THE SIGN`. That gives away the payoff the C tease now holds back. Match it to the tease.

These need a ruling or new writing:

11. **#8:** the title says "free sample," but the woman in it went in for a $25 facial. Retitle around the demo chair, or keep the title and stop it pointing at Taylor.
12. **#9 and #10:**
    - #9: Lettie's "50 or 60" is spent in the tease and the header before the runway asks for it.
    - #10: Chisholm is never named or introduced. Bring back his identity from the CBS story (30, developmentally disabled, settlement money), or restore clip 6OGQ.
13. **#13:** Taylor timeline. She's "IS 84" on the prompter, but her report aired June 2025. This was the open producer decision in the source log.
14. **#14:** the Walmart response cue is still blank.
15. **#15:** someone has to watch clip 9 before its header and runway stay as written.

## BLOCKERs

| # | Story / section | Issue | Confidence | Source | Scope |
|---|---|---|---|---|---|
| 1 | A / clip 3 (CBS LA, BUTT 3:03–3:27) | The BUTT window has the reporter reading the store lawyer's letter "claiming that Victor Chisholm sexually harassed" employees. The cut ends at "making large purchases at multiple stores," so his attorney's "baseless" rebuttal is outside the clip. The button then says "THAT'S THE STORE'S LAWYER, SAYING THAT MAN SPENDS BIG…": it's the reporter reading a letter, and it leaves out the harassment claim Jeff will have just aired. That is an unanswered sexual-misconduct accusation against a developmentally disabled man. **The out point was my pick at the outline stage. This one is on me.** | CONFIRMED (that it's in the clip) | CBS LA transcript g9e4ElDgYG8: letter 3:03–3:26, rebuttal 3:26–3:40 | the clip's in/out per the manifest |
| 2 | C / runway | "LAST YEAR TARGET AND DOLLAR GENERAL STORES WERE FINED FOR RINGING UP MORE THAN THE SHELF." Target is off-limits as a subject (facts-to-get-right). The Target half is also two single North Carolina stores ($1,140 Wilmington, $735 Raleigh), said as if it were national. Dollar General is solid: $400K Colorado, $1.55M Pennsylvania, both 2025. | PARTIALLY CONFIRMED | [NCDA&CS, 11/3/2025](https://www.ncagr.gov/news/press-releases/2025/11/03/7-stores-pay-fines-following-price-scanning-errors); [Colorado AG](https://coag.gov/2025/400k-settlement-with-dollar-general-for-overcharging-customers); [WBNG](https://www.wbng.com/2025/12/09/dollar-general-pay-155m-settlement-pennsylvania-allegedly-overcharging-consumers/) | NC: single-store state inspection fines, Q2–Q3 2025. DG: state AG settlements, 2025. |
| 3 | A / Topanga runway | "CBS LOS ANGELES WATCHED THE STORE FOR WEEKS." The CBS package says "For months now, we've documented B and Co's employees." It's a one-word fix, but the label is CONTRADICTED, so it's a BLOCKER by rule. | CONTRADICTED | CBS LA transcript g9e4ElDgYG8, 0:50 | the same CBS package |

## Overruled mechanical findings

| Finding | Ruling |
|---|---|
| 9× "No URL or source pointer" (mechanical pass, `--stage final`) | Conversion artifact. Each cue has its link on the `((([Outlet](URL) · in - out…)))` line. Overruled. |
| 9× "malformed clip marker" and 7× "OUT: line is pre-filled" (check_bible) | Numbered markers and filled outcues are the house format at this stage (CLAUDE.md, 10/14 build). Not a defect. |
| 2 sponsor blocks (mechanical pass) | The approved outline has OmniWatch at both breaks, after A and after B, each with a tease in. That placement is right. |

## WARNINGs

| # | Story / section | Issue | Confidence | Source | Scope |
|---|---|---|---|---|---|
| 4 | Tease, A header | Lines that state guilt as fact: "ONE OWNER GOT BUSTED!!" (tease), "CBS LOS ANGELES CAUGHT ONE STORE IN THE ACT" (header), "HIS CAREGIVER TOOK HIS HOUSE FOR $5" (tease). The body itself says "NOBODY AT BEE & CO. HAS BEEN CHARGED" and "SHE'S ACCUSED, NOT CONVICTED." The tease and headers should match. The clip shows staff "pushing samples," which isn't a crime. | | | |
| 5 | A / clip 3 runway | Five lines (check_bible). It ends on "WATCH WHAT HAPPENS," which promises a confrontation. The clip opens on the already-closed store, so the next line, "ON SEPTEMBER 24… THAT BEE & CO. CLOSED," repeats what viewers just saw. | | | |
| 6 | A / Donna | "POLICE SAY THE 27-YEAR-OLD OWNER, HAI BARANETZ, KEPT FLATTERING HER… AND THEN DROVE HER TO HER CREDIT UNION." KOIN has the flattery as Donna's account. Court records say he took her to his car and asked her to go into her bank. Police are the source for the teller and the arrest. | PARTIALLY CONFIRMED | KOIN transcript VaEws6itP08, 1:35–2:45; [The Columbian, 2/5/2025](https://www.columbian.com/news/2025/feb/05/vancouver-mall-skin-care-store-owner-accused-of-trying-to-scam-75-year-old-woman-out-of-50000-say-court-documents/) | |
| 7 | A / Donna | "HE'S CHARGED, NOT CONVICTED." Docket Alarm lists *State v. Baranetz* (Clark Co. 25-1-00113-06) as active. He pleaded not guilty on 1/29/2025, and trial was set for 4/21/2025. The current docket isn't publicly visible. Date the charge rather than saying "now." | PARTIALLY CONFIRMED | [Docket Alarm](https://www.docketalarm.com/cases/Washington_State_Clark_County_Superior_Court/25-1-00113-06/BARANETZ_HAI/); The Columbian | charged Jan 2025, status as of Oct 2026 |
| 8 | Title / tease | "THIS FREE SAMPLE COST HER $26,000." The $26,000 woman is Taylor, who went in for a paid "$25 FACIAL" (the body's own header). The free-sample hook fits the scheme (Topanga staff "pushing samples," Donna's eye cream), but "COST HER" points at Taylor. Expect viewers to catch it in the comments. | | First Coast News transcript 3iz8G25Taxg | |
| 9 | Tease / A Lettie | "SHE SAID NO 50 OR 60 TIMES" appears in the tease, then in the header ("THIS WOMAN SAYS SHE SAID NO 50 OR 60 TIMES!!"), then the runway asks "SO HOW MANY TIMES DID SHE SAY NO???" The clip pays off a question that was already answered twice. | | | |
| 10 | A / Topanga | "ONE MAN SAYS THEY GOT HIM FOR MORE THAN 50 THOUSAND DOLLARS." He gets no name and no identity before the clip, which breaks the people-first rule. The figure is right: more than $40,000 in charges plus more than $10,000 in tips. Dropping 6OGQ also removed his own story, so the first time viewers meet him is in the store's letter (see #1). This is outline drift from approved beat A4 and needs a producer ruling. | CONFIRMED (figure) | CBS LA transcript 6OGQNCnZTfE | Chisholm, Bee & Co. Topanga |
| 11 | C / digital tags | "WALMART SAYS THE TAGS DON'T USE YOUR PERSONAL DATA… BUT LAST YEAR IT PAID 5.6 MILLION DOLLARS… OVER REGISTERS RINGING UP MORE THAN THE SHELF!!" The "BUT" links the tags to a settlement that wasn't about tags. That settlement covered both charging more than the lowest posted price and underweight goods. | PARTIALLY CONFIRMED | [Sonoma County DA](https://da.sonomacounty.ca.gov/walmart-settles-consumer-protection-case-for-scanner-price-overcharges-and-false-advertising) | Aug 2025, four California county DAs, $5,639,801.92 |
| 12 | B / protection | "SIGN UP FOR YOUR COUNTRY'S FREE PROPERTY-FRAUD ALERT" is a typo for "COUNTY'S" that Jeff will read cold. "IT EMAILS YOU WHEN ANYTHING IS FILED" overpromises, because not every county offers it. | | | |
| 13 | A / Taylor | "KATHRYN TAYLOR IS 84." Her report aired June 2025, so this reads as current. This is the producer decision from the source log and is still open. | PARTIALLY CONFIRMED | FCN transcript; Moneywise/Yahoo 6/26/2025 | age as of June 2025 |
| 14 | C / response | `(((WE REACHED OUT TO WALMART…)))` is unfilled. A named company needs its response, or the line saying it didn't respond. | | | |
| 15 | C / clip 9 | The header "AND THIS SHOPPER SAYS WATCH THEM!!" and the runway "SO WHAT DID HE FIND ON THOSE DIGITAL TAGS???" describe a clip nobody has watched. No transcript exists. Also: Wrigg is known for Walmart meat-weight videos, so the digital-tag content isn't confirmed. | UNVERIFIED | — no transcript; caption only ("Digital Price Tags And Pricing") | |
| 16 | C / clip 8 | "AN EMPLOYEE FIXED IT TO A DOLLAR. BUT ONLY BECAUSE SHE ASKED." The SOURCE_LOG write-up says an employee overrode it to $1. "Only because she asked" isn't in anything we have, and the write-up page didn't load on re-check. | UNVERIFIED | — the wegotthiscovered page returned no body on re-fetch; the earlier search summary has no "asked" | |
| 17 | Whole show | 1,410 spoken body words against the 1,700–2,300 Wednesday band, and 9 clips against the 10–12 band (check_bible). Fine if the show is timed that way; flagging it so it's a choice. | | | |
| 18 | C / clips 8–9 | MANUAL TikToks with no in/out or outcue. Kyle sets them on the pull. | | | |

## NOTES

| # | Story / section | Issue |
|---|---|---|
| 19 | B close | "NEXT, THE WALMART REGISTER THAT CHARGED MORE THAN THE SIGN" gives away what the new C tease holds back. |
| 20 | Tease C | It says the same thing twice. Two openers: "THAT SALE SIGN LOOKS LIKE A GREAT DEAL" and "YOU SEE THE BIG YELLOW SIGN." Two promises: "THE 5-SECOND HABIT" and "WE'LL SHOW YOU HOW TO CATCH IT." Keep one of each. |
| 21 | A / Lettie | "A SALESMAN AT A MALL KIOSK STOPPED HER." ABC15 says she was approached by a salesman while walking through a local mall; it doesn't say "kiosk." The source log has "mall kiosk demo." It's minor. "Approached her in the mall" is safer. |
| 22 | A / protection | "THESE PRICES ARE NEVER ON A TAG" is an absolute nobody has sourced. "NEVER SIGN A 'FINAL SALE' FORM" doesn't match these cases: ABC15's owner says the no-refund policy is printed on the receipt. |
| 23 | A / clip 1 | The runway "NOT HER DAUGHTER. NOT HER SISTER." comes right before Taylor saying "My sister's across the street." That's mild repetition, fine for a teleprompter. |
| 24 | Voice | 8 "???" and a 15% exclamation-line rate, both above the corpus. "CHECK THIS OUT" is used twice (cap). Headers flagged "no verb" do have verbs. |
| 25 | Graphics | Story C's protection block is being made into a full-screen graphic (prompt delivered 10/7). Add a `(((CREATE FULL SCREEN GRAPHIC XXX)))` cue at "HERE'S HOW TO PROTECT YOURSELF" in C so the control room knows. |

## What's working

- **Story B builds well:** the doorbell, then the $5 deed, then the arrest. "HER FATHER WAS DEAD. AND SHE WAS THE ONE IN HANDCUFFS" lands.
- **Accused people are framed correctly in the story bodies:** "WARRANTS ALLEGE," "SHE'S ACCUSED, NOT CONVICTED," "COURT RECORDS SAY," "NOBODY AT BEE & CO. HAS BEEN CHARGED."
- **The Florida Bee and Co is kept apart from Mazal's Bee & Co.**
- **Responses are in for:** Royal Bee's owner, Bee & Co.'s lawyer, Inside Edition couldn't reach Smalls, and Smalls calling police on the WMBF crew.
- **Tier 1 contacts verified:**
  - ReportFraud.ftc.gov.
  - Eldercare Locator 1-800-677-1116 ([ACL](https://eldercare.acl.gov/Public/About/Contact_Info/Index.aspx)).
- **Clip 1–7 outcues** were string-matched against the transcripts in the run's source log. I re-checked the windows for clips 3 and 4.
