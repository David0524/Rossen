# Research: Amazon settlement refunds and unclaimed money / fake refund letters
For W 10/28/2026. Researched Mon Oct 19, 2026. All view counts and relative upload ages were observed Oct 19, 2026, on YouTube search-result pages or the channel RSS feed.

**Access notes**
- **TikTok:** both seed TikToks were refused. yt-dlp returned "Unexpected response from webpage request" for kctv5/7694358090921102622 and usrrnrb/7696136627411766541. These are manual pulls, and nothing below describes their content.
- **YouTube video pages:** bot-walled. yt-dlp returned "Sign in to confirm you're not a bot" and HTTP 429, and a curl of the watch pages returned a stub. Exact upload dates for third-party videos therefore could not be pulled. Ages below are YouTube's relative "Xw ago" labels from search results.
- **Rossen Reports dates:** these are exact, from the channel RSS feed.

---

## ROSSEN REPORTS UPLOADS (collision check)
Source: https://www.youtube.com/feeds/videos.xml?channel_id=UC7PYy5Tx1WhbnGKc3KJeRKw (the last 15 uploads, with publish timestamps in UTC and views as of Oct 19).

| Published (UTC) | ID | Title | Views |
|---|---|---|---|
| 2026-10-16 | 1BA0UiY4bu8 | If THIS Is Your Password — Change It Immediately! | 54,098 |
| 2026-10-15 | xs__ci9ri4Q | Costco Is CHANGING Kirkland — THESE Prices Just COLLAPSED (October 2026) | 702,355 |
| 2026-10-14 | enqBc2rmTsk | NEVER Take a Free Sample at the Mall (Here's Why) | 207,933 |
| 2026-10-12 | 32v9tr1MRnQ | Home Depot Is Discontinuing THESE Items — Prices Just CRASHED (October 2026) | 225,081 |
| 2026-10-09 | hFjph0RtINw | They're Mailing THIS Card to Seniors — DON'T Activate It! | 297,369 |
| 2026-10-08 | hBCTHTfOgJQ | Sam's Club Is Discontinuing THESE Items — Prices Just CRASHED (October 2026) | 656,616 |
| 2026-10-07 | JXqXs2BpixE | If You See THIS On Your Shopping Cart — You Are Being TRACKED | 98,847 |
| 2026-10-06 | e2V_QRWAzuo | 25 INSANE Amazon Prime Day Deals — Prices Just CRASHED (October 2026) | 149,173 |
| 2026-10-05 | pLHPUxDYxY4 | NEW at DOLLAR GENERAL: 10 Items That WON'T LAST (And 6 to Avoid) — October 2026 | 242,962 |
| 2026-10-02 | 7JVhqMsooHU | 20 EARLY Amazon Prime Day Deals That WON'T LAST — October 2026 | 376,835 |
| 2026-10-01 | 0EBULN09efw | NEW at COSTCO: 10 Items That WON'T LAST (And 5 to Avoid) — October 2026 | 1,384,102 |

These late-September uploads carry October titles. They were also in the feed but are not October uploads:
- 9/30, "Don't Post THIS Photo Online…"
- 9/28, "NEW at ALDI… October 2026"
- 9/25, "The NEW Delivery Scam EXPLODING in 2026…"
- 9/24, "Walmart Is Discontinuing… (October 2026)"

**Did the Oct 16 show (1BA0UiY4bu8) cover the Amazon settlement?**
- **The description doesn't say so.** It covers AI hijacking smart homes, then "Plus: the best Amazon deals, secret promo codes, and your live deal requests with our partners at DealSeek." It does not mention the settlement or refunds.
- **We can't rule it out.** We could not get the transcript because YouTube is bot-walled, so it's possible the settlement aired in the deals block without a mention in the description.
- **Repo history raises the risk.** `runs/W_10142026/jeff_approval.md` line 15 says "Not on this show: Amazon settlement (suggested for the 10/16 F1)." The 10/14 pitch sheet, story #4, pitched it for the 10/16 F1. There is no 10/16 run folder in the repo.
- **Ask the producer** whether it aired on 10/16 before pitching story A.

None of the other October titles above mention the Amazon settlement, Walmart refunds or unclaimed money. YouTube search also surfaced older Amazon-scam episodes from the channel:
- "Hidden Amazon Charges Are HITTING Accounts — Say THIS For a Refund", streamed about 2 months ago, 55,363 views (QFB-oaVnpHs)
- "Amazon's 'Keep It' Refund Is a TRAP", streamed about 5 months ago, 836,382 views (DUSdiGq_C08)

---

## STORY A: Amazon Prime settlement refunds, real vs. fake

### Confirmed facts
- **FTC press release, Sept 17, 2026:** https://www.ftc.gov/news-events/news/press-releases/2026/09/ftc-announces-additional-payments-consumers-stemming-ftcs-amazon-prime-settlement
  - The maximum total payment rose from $51 to $200. People already paid can get an additional $149.
  - People who used 11–20 Prime benefits in a one-year period are newly eligible, which covers "millions" of additional consumers. No exact count is given.
  - All future payments are automatic, with no claim or form, and go out by Venmo, PayPal or mailed check.
  - The new round begins Oct 1, 2026. Amazon checks the acceptance threshold in Feb 2027. Supplemental $149 payments begin in Apr 2027 "if needed."
  - Amazon has issued more than $845 million in redress as of Sept 2026.
  - Scam lines: the FTC is "not contacting people about refunds in the Amazon matter"; "no one from Amazon will ever ask you for money to get a refund"; the FTC "will never demand money, make threats, tell you to transfer money, or promise you a prize."
- **FTC Amazon refunds page, dated Sept 2026:** https://www.ftc.gov/enforcement/refunds/amazon-refunds
  - Payments expire 60 days after they're issued.
  - The settlement requires $1.5B in refunds.
  - Contact: admin@SubscriptionMembershipSettlement.com.
  - Quotes: "Only scammers say they can get you special access or a guaranteed refund"; "The FTC will never ask you to pay to get a refund"; "Don't pay anyone who promises you a refund in exchange for a fee"; "don't give personal information to anyone who contacts you promising a refund."

### Warnings about FAKE settlement-refund messages (sources loaded)
- **KSL.com, Matt Gephardt, Sept 30, 2026:** https://www.ksl.com/article/51630330/amazon-prime-refunds-are-coming-scammers-may-be-too
  - Scammers may email a "click this link to get your refund" message that is really malware, or try to get access to bank accounts.
  - Anyone asking you to act to "release" the money is a red flag.
  - The only named warner is the FTC. No victims are named.
- **WBAY (Green Bay), Tammy Elliott, Nov 14, 2025:** https://www.wbay.com/2025/11/14/consumer-first-alert-amazon-refund-emails-are-real-beware-scams
  - This covers the first ($51) round.
  - Wisconsin's Division of Consumer Protection warns that a call or text asking for personal information or money is a scam.
  - Administrator Michelle Reinen: "there is nothing a consumer needs to do to receive a refund."
- **PCWorld, Alaina Yee, Nov 25, 2025:** https://www.pcworld.com/article/2983363/watch-out-dont-get-scammed-about-amazon-prime-refunds.html
  - Fake messages ask you to pay an "overdue Prime balance" or prepay a renewal, or ask for your name, address, phone or payment info.
  - They use lookalike claim forms and links that aren't Amazon or the settlement site, offer help getting a bigger refund, or claim to come from the FTC.
  - This is a tech-press piece, not an official warning.
- **Albuquerque Journal "Scam Watch," Jan 18, 2026 (opinion, no author):** https://www.abqjournal.com/opinion/opinion-amazon-refunds-are-leading-to-scams/2961245
  - Describes people posing as the FTC or Amazon who threaten or demand a money transfer before a refund, and fee-based "guaranteed refund" offers.
  - Lists the NM Consumer Protection Division at 505-490-4060.
- **WVVA, Heather Olinger, Feb 24, 2026:** https://www.wvva.com/2026/02/24/scam-week-you-should-rethink-this-refund/
  - Covers a related Amazon "recall refund" smishing text that leads to a fake Amazon login asking for username and password.
  - It is not settlement-specific.
- **Not found:** a BBB warning, a state AG warning, or an FTC consumer alert specifically about fake Amazon *settlement* refund messages. The FTC consumer-alert archives for Sept and Oct 2026 have no Amazon refund alert.

### Video in hand (YouTube, relative age and views as of 10/19)
- **KSL News Utah, "Amazon Prime refunds are coming. Scammers may be, too":** https://www.youtube.com/watch?v=agEeWFAueso
  - About 2 weeks old, 5,208 views, 2:22.
  - This is the best match: same story as the KSL article above.
- **KSDK News, "VERIFY: Do you need to file a claim to get Amazon settlement refund?":** https://www.youtube.com/watch?v=SPY4dsQQbe8
  - About 9 days old, 873 views, 2:03.
- **WUSA9, "Refund checks from an Amazon Prime settlement are arriving in mailboxes now":** https://www.youtube.com/watch?v=mff8NrTcRw0
  - 3,316 views. Age not captured, so it is likely the first round.
- **WBAY, "Amazon refund emails are real, but beware of scams":** https://www.youtube.com/watch?v=g6n6rFw1MHk
  - About 11 months old (first round), 603 views, 0:51.
- **FOX 32 Chicago, "How Amazon Prime members can claim refunds in $2.5B settlement":** https://www.youtube.com/watch?v=GF9FBxsI7cQ
  - About 9 months old, 22,258 views, 9:38.
- **GMA, "Who's eligible to get money from $2.5 billion Amazon settlement":** https://www.youtube.com/watch?v=nL9OTUoyurg
  - About 1 year old, 67,977 views.
- **Not news, don't use as fact:** "Retired Couple Loses $690,500 Life Savings to Fake Amazon Refund Scam…" by the Zarkon channel, https://www.youtube.com/watch?v=HBO81kJVaLI, about 9 months old, 20,407 views. This is a story channel, it is unverified, and it isn't tied to the settlement.
- **Seed:** KCTV5 TikTok, blocked from here, manual pull.

### Victims
- **Could not find** a named US victim of a fake Amazon settlement-refund message.
- The UK police warnings (West Mercia, Lincolnshire) describe Amazon impersonation and "overpayment" losses. They are undated or older, outside the US, and not settlement-related.

### Official steps (sourced)
- **Do nothing to get paid:** payments are automatic by PayPal, Venmo or check (FTC release, 9/17/26).
- **Accept or cash within 60 days** (FTC Amazon refunds page).
- **Never pay a fee or give personal info.** The FTC isn't contacting anyone, and Amazon never asks for money (FTC release and refunds page).
- **Official contact:** SubscriptionMembershipSettlement.com and admin@SubscriptionMembershipSettlement.com (FTC refunds page).
- **Report** at ReportFraud.ftc.gov.

### Could not find
- A BBB, state AG or FTC consumer alert specifically about fake settlement-refund texts or emails asking for fees, passwords or forms. The fee/password/form patterns come from the FTC's general refund lines, plus PCWorld and KSL.
- A victim.
- Exact upload dates for third-party YouTube videos (bot wall).
- Whether the 10/16 show covered the settlement.
- What the KCTV5 TikTok shows.

---

## STORY B: Walmart money-transfer refunds, unclaimed property and fake refund letters

### Confirmed facts
- **FTC press release, Oct 15, 2026:** https://www.ftc.gov/node/337957 (the canonical slug couldn't be resolved because ftc.gov returned 403 to curl).
  - Title: "FTC Sends More than $9.8 Million to Consumers Harmed by Walmart's Failure to Stop Scammers that Used its Wire Transfer Services to Take Millions from Customers."
  - More than $9.8M to **65,022** consumers, by **check**.
  - Cash within **90 days**.
  - Administrator: **Rust Consulting Inc., 1-833-472-1990**.
  - Quote: "The Commission never requires people to pay money or provide account information to get a payment." Also: "The FTC will never demand money, make threats, tell you to transfer money, or promise you a prize."
- **FTC Walmart refunds page, dated Oct 2026:** https://www.ftc.gov/enforcement/refunds/walmart-refunds
  - Covers eligible transfers made at Walmart between **Jan 2015 and Dec 2024**.
  - The June 2025 settlement was $10M.
  - Quote: "The FTC will never threaten you, say you must transfer money to 'get a refund,' or promise you a prize. That's a scam."
- **NAUPA (unclaimed.org):**
  - https://unclaimed.org/what-is-unclaimed-property/: "Approximately 1 in 7 people do!" have unclaimed property. States hold "billions of dollars." The page gives no exact total.
  - https://unclaimed.org/can-i-really-search-for-free/: "There is no fee to search for and claim your unclaimed property" through official state programs. Paid finders exist and are "in most cases legal," some states cap their fees, and they must usually register. The page also says "there are also many unclaimed property scams across the United States."
  - Homepage https://unclaimed.org: MissingMoney.com is "a free website, managed by NAUPA," and the page links to each state program.
  - **No current dollar total** for property held or returned appears on unclaimed.org. The figures in search snippets ($70B held, $4.49B returned in FY2024) are from bitcoin.com and are unverified, so don't use them.
- **NAUPA/NAST advisory, July 12, 2023:** https://nast.org/wp-content/uploads/naupa-and-nast-warn-public-of-fraudulent-attempts.pdf
  - "NAUPA and NAST will never directly contact individuals regarding unclaimed property, and any such communication should be treated as fraudulent."
  - "claiming unclaimed property is always free."
  - Search only at unclaimed.org and missingmoney.com.

### Official warnings about fake unclaimed-money contacts and fake letters
- **FTC consumer alert, Mar 30, 2026, "How to handle unexpected calls about unclaimed funds":** https://consumer.ftc.gov/consumer-alerts/2026/03/how-handle-unexpected-calls-about-unclaimed-funds
  - Scammers call or text claiming you're owed thousands. They use fake agency names, a specific dollar amount and urgency, and they ask for personal info or an upfront "processing" fee.
  - Quote: "The government won't call or text and ask you to pay them to search for unclaimed funds."
  - It points people to unclaimed.org/search and their state's .gov site.
- **FTC consumer alert, July 9, 2026, "Unclaimed life insurance money? It's a scam":** https://consumer.ftc.gov/consumer-alerts/2026/07/unclaimed-life-insurance-money-its-scam
  - Fake "law firm" **letters** say a client with your last name died and named you heir to a policy worth millions, to be split among you, charities and the firm.
  - Advice: "Don't respond." "Never send money or information to a stranger who promises big rewards."
- **WRTV Indianapolis, Jul 21, 2026 (updated Sep 3):** https://www.wrtv.com/news/wrtv-investigates/feds-warn-scam-letters-claim-you-have-unclaimed-insurance-money
  - FTC consumer education specialist Terri Miller: "The money doesn't actually exist at all." and "The end game for the scammer is to get you on the phone."
- **Vermont Treasurer Mike Pieciak, Apr 28, 2026 (via vermontbiz):** https://vermontbiz.com/node/243162
  - Scammers call and text Vermonters about unclaimed property. Several were targeted, and no losses were reported.
  - Pieciak: "If you have a claim, contact our office and we'll help you recover it—free of charge."
- **Not found:** any warning about fake letters that piggyback on the **Walmart** FTC refund specifically. The FTC's own "never requires payment or account information" line is the only on-point guidance.

### Video in hand (YouTube, as of 10/19)
- **WISH-TV, "FTC warns of phishing scam involving fake letters about unclaimed insurance money":** https://www.youtube.com/watch?v=ElUrIfYNjvM
  - About 2 months old, 1,058 views, 1:44.
- **WRTV Indianapolis, "FTC warns scammers are impersonating FTC employees with phone calls and texts":** https://www.youtube.com/watch?v=206lRs8LxkA
  - About 3 months old, 510 views.
- **KFOR, "Spotting an unclaimed property scam letter":** https://www.youtube.com/watch?v=8jsotkn968A
  - About 1 year old, 1,890 views, 1:33.
- **NBC10 Boston, "What to know about finding unclaimed money":** https://www.youtube.com/watch?v=g7C9-A7SJhw
  - 3,616 views. Age not captured.
- **TODAY, "How to find unclaimed money":** https://www.youtube.com/watch?v=6rnWXnarnG4
  - 36,001 views. Age not captured.
- **New Jersey Dept. of the Treasury, "What is Unclaimed Property?":** https://www.youtube.com/watch?v=cEs_jCVKxCs
  - 53,115 views. Official, age not captured.
- **Walmart refund:** no local-news video on the Oct 15 checks was found.
  - Only small explainer channels turned up: "Is That FTC Walmart Refund Check a Scam? How to Tell" (Steve Rhode, meeJZevlcDA, 2 days old, 9 views) and "Walmart $9.8 Million Refunds…" (XEZApmVIhGA, 2 days old, 2 views).
  - The older lawsuit coverage is about 4 years old: GMA gCab26Xezhk, 5,734 views; News On 6 qRxnWOXRKuM; KOAA cOy12RgO84U.
- **Seed:** usrrnrb TikTok, blocked from here, manual pull. We could not confirm what it claims about fake refund letters following the Walmart payout.

### Victims
- **Could not find** any victim of a fake Walmart-refund letter or a fake unclaimed-money finder in 2026.

### Official steps (sourced)
- **Real Walmart checks come by mail.** Cash them within 90 days, and direct questions to Rust Consulting at 1-833-472-1990, using the number from ftc.gov rather than one printed on a letter.
- **Never pay or give account info** to get a payment (FTC 10/15/26).
- **Search free** at your state's .gov unclaimed-property site via unclaimed.org/search, or at MissingMoney.com (FTC 3/30/26 and NAUPA).
- **NAUPA/NAST never contact individuals directly** (2023 advisory).
- **Report** at ReportFraud.ftc.gov.

### Could not find
- A fake-letter warning tied to the Walmart refunds.
- Any victim.
- A current NAUPA dollar total for property held or returned.
- A local TV package on the Walmart checks.
- Exact YouTube upload dates.
- The TikTok seed content.
