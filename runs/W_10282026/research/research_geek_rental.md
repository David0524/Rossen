# Research: Fake Geek Squad refund scam + Rental car / Turo bogus damage bills
For Wed Oct 28, 2026. Researched Mon Oct 19, 2026 (01:3x UTC). Every fact below comes from a page loaded in this session.

## Access problems (read first)
- **YouTube bot-walled:** yt-dlp (android, ios, tv_embedded, web_embedded and mweb clients) returned "Sign in to confirm you're not a bot" / HTTP 429 at 01:38 and 01:39 UTC. No upload dates or view counts could be pulled. YouTube oEmbed still answers, but it gives only title and channel. Per CLAUDE.md: wait 5+ minutes, then retry once through `fetch_many`. A 30-minute wait has cleared it before.
- **TikTok blocked:** WebFetch of https://www.tiktok.com/@nexttech57/video/7696128227668004126 returned only "TikTok - Make Your Day". Caption, views and date are unverified, so the 2.1M figure is still the producer's seed number. Manual pull.
- Note: `video_info.sh` takes VIDEO IDs, not full URLs (`bash video_info.sh 1_wUVS5szfw`).

---

## (A) Fake Geek Squad "refund" scam

### Confirmed facts
- **FTC press release, May 24, 2024:** "consumers in 2023 submitted about 52,000 reports about scammers impersonating Best Buy or its Geek Squad tech support brand." This made Best Buy/Geek Squad the most impersonated company, ahead of Amazon (about 34,000). The release gives no dollar loss figure for Geek Squad. https://www.ftc.gov/news-events/news/press-releases/2024/05/new-ftc-data-shed-light-companies-most-frequently-impersonated-scammers
- **FTC Consumer Alert, Oct 25, 2022 (Alvaro Puig), "How to recognize a fake Geek Squad renewal scam":** texts or emails say you'll be charged hundreds of dollars to renew a Geek Squad membership and push you to call within 24 hours. If you call, the scammer may ask for remote access. Some pose as having refunded you by mistake and have you buy gift cards to "repay" them. https://consumer.ftc.gov/consumer-alerts/2022/10/how-recognize-fake-geek-squad-renewal-scam
- **FBI IC3 PSA, March 28, 2018:** in the tech-support refund scam, the criminal "transferred funds among the victim's own accounts (checking, savings, retirement, etc.)" so it looks like the victim was overpaid, then asks for the difference back. This is the documented mechanism behind the "fake $29,900 refund" on screen. https://www.ic3.gov/PSA/2018/PSA180328
- **How it typically starts (sourced):** a fake Geek Squad renewal or invoice email with a phone number to call. Sources: the FTC 2022 alert above; Hammonton police account (Hoodline: an "email falsely claiming that a Geek Squad membership was due for renewal"); Fairfield CT case (an email claiming a $525 Geek Squad charge).

### Video in hand
- **TikTok @nexttech57/7696128227668004126:** blocked. Views, date and caption are unverified.
- **YouTube "Woman conned out of $30k in Geek Squad renewal scam"** https://www.youtube.com/watch?v=YvKDfXAzekM. Title comes from a search result only. The search snippet called it about 1,047 days old (about late 2023), which makes it NOT recent. It appears to be the El Cajon (CBS 8 San Diego) case. Views and date are unconfirmed because of the bot wall.
- No 2026 local-TV YouTube clip was confirmed. Search surfaced scambaiter and creator videos (e.g. https://www.youtube.com/watch?v=e_zPF2xUuwo "Scammer Tries to Steal $20,000… But Wastes 3 Hours Instead"), but none of their metadata could be verified.

### Victims with real losses
1. **Hammonton, NJ: 81-year-old woman, lost $20,000 (cash).** Hoodline, Sept 22, 2026, citing Breaking AC News. https://hoodline.com/2026/09/hammonton-grandmother-loses-20k-in-geek-squad-cash-drop-scam-police-say/
   - In August she got an email falsely saying her Geek Squad membership was due for renewal. A caller told her $20,000 "had been deposited into her account by mistake and had to be returned." Police said Trust Bank confirmed no such wire transfer had occurred.
   - She withdrew $20,000, boxed it and handed it to a man in a parking lot at 10 N. White Horse Pike around 3 p.m. on Aug 22, using a passcode. She reported it on Aug 23.
   - Charged: Houfeng Zhong, 40, and Hui Ming Lin, 46, both of New York. The Ohio State Highway Patrol detained them. The article does not list the specific charges, and the victim is unnamed.
   - Not local TV. Hoodline is an aggregator, and the original is breakingac.com, which was not loaded.
2. **Fairfield, CT: elderly woman, attempted theft (no loss).** Hartford Courant via Yahoo, Feb 8, 2024. https://www.yahoo.com/news/man-allegedly-posing-geek-squad-191900122.html
   - The email claimed a $525 charge. The caller got remote access, convinced her she'd been mistakenly sent $25,000, and pressured her to withdraw $20,000 for a home pickup.
   - Bin Sun, 27, of Brooklyn was arrested during police surveillance and charged with attempted first-degree larceny. This case is OLD.
3. **Orlando: Helene Brotman, net loss $2,000** (scammers took $3,500 and the bank refunded $1,500). WFTV, Oct 22, 2020. https://www.wftv.com/news/action9/scammers-pretending-be-popular-it-techs-costing-consumers-thousands/D5ELWWJXB5EKFA5U2NFT7O4XT4/
   - This case is OLD. The article includes a Best Buy statement (below).
- **Close call (no loss confirmed): Kaye Allen, Greenville TX.** Dallas Morning News "Watchdog" (Dave Lieber), on Yahoo, updated Oct 7, 2026. https://www.yahoo.com/news/us/articles/greenville-woman-close-call-shows-113000620.html
   - The email was about McAfee software she never bought. The caller offered a $455 refund through what she believed was a "Geek Squad business portal." The amount then changed to about $45,500 (the article also says $45,550), and it appeared in her bank account. Callers pushed her to send it back.
   - She hung up and called her bank's fraud department. She suspects the HopToDesk remote-access tool was used.
   - This is a strong 2026 example of the inflated-refund screen, but not a loss.
- **El Cajon, CA, $30,000:** the CBS 8 article https://www.cbs8.com/article/news/local/woman-lost-30k-geek-squad-email-scam/509-ece785f3-959b-463d-b745-ad8610eedb14 returned 403, so it is NOT verified. The YouTube search snippet dates it to about late 2023.

### Official warnings / protection steps
- **FTC (2022 alert):** don't call the number in the message; contact the company at a number you know is real; don't give remote access; check bank and card accounts and ask for reversals; report at ReportFraud.ftc.gov.
- **FBI IC3 (2018 PSA):** "Do not give unknown, unverified persons remote access to devices or accounts." "Resist the pressure to act quickly." Report at ic3.gov.
- **Best Buy's own page ("Protect Yourself"):**
  - "we generally don't make unsolicited calls to customers"
  - To confirm a contact, call 1-888-BEST BUY (1-888-237-8289).
  - Report scams to abuse@BestBuy.com.
  - The page shows a "Fraudulent Geek Squad membership renewal notice" image.
  - The page itself is undated.
  - https://www.bestbuy.com/site/privacy-policy/protect-yourself/pcmcat266100050002.c?id=pcmcat266100050002
- **Best Buy quoted to WFTV (2020):** customers "can always call Best Buy at 1-888-BESTBUY if they need tech support."
- **Mistaken Zelle/Venmo deposit variant:** found only in older BBB-sourced consumer pieces (e.g. https://www.koaa.com/news/on-your-side/scammers-accidentally-sending-money-experts-say-dont-send-it-back). Those pages were NOT opened, so their dates and quotes are unverified. The advice reported in search snippets is to contact your bank or the app rather than send money back.

### Could not find / needs verification
- **TikTok:** the 2.1M views and the $29,900 figure are unverified. No news report uses $29,900.
- **"5 local news reports":** only one 2026 loss case (Hammonton) was found, and it comes through an aggregator. No 2026 local-TV story with a named victim who lost money turned up.
- **A claim that "FBI as of Aug 27, 2026 is collecting details on Geek Squad impersonation" (from an AI search summary):** NOT confirmed. Two searches found no FBI or IC3 page. Do not use it.
- **A "52,000 reports in 2024" claim seen in blogs:** the FTC page says 2023. Use 2023.
- **Recent Best Buy statement specifically about the fake emails:** could not find one newer than the undated web page and the 2020 quote.
- **Any 2026 YouTube local-news clip with views and upload date:** blocked by the YouTube bot wall.

---

## (B) Rental car / Turo bogus damage bills

### Confirmed facts: KSL "Get Gephardt" Turo case
Source: KSL.com, Oct 5, 2026, by Matt Gephardt and Sloan Schrage. https://www.ksl.com/article/51632567/draper-woman-fights-to-get-turo-host-booted-after-making-fraudulent-rental-car-damage-claims-against-her
- **Renter:** Hope Orr of Draper, Utah (age not given). The host is unnamed.
- **Charges:** $165 for an alleged smoking violation, plus a planned $500 for alleged tire damage pending the host's estimate.
- **The host's photos:** a close-up of a tire with a nail or screw, plus a lighter, ash and loose tobacco. Orr's own photos showed tread that didn't match.
- **The reverse image search:** it found the same tire photo in a **Reddit post "from years ago."** The original was less cropped and showed the tire on a different car model. **KSL does NOT say "4 years old."** Use "years-old Reddit photo" unless the Reddit post is pulled.
- **The host's text:** "I've done more than 5,000 tire claims in the last nine years." Unverified by KSL. The host has 13 cars, rented more than 6,600 times.
- **Turo's first response:** it found the claim valid about 20 minutes after Orr sent her comparison, then removed the claims after the reverse image search.
- **Turo spokesperson:** "incidents like this are rare." A host who falsifies claims is removed. Turo said "this guest was refunded in full" for the whole rental "as a gesture of goodwill" and confirmed the host was banned. Policy allows a fee of up to $2,000 for a host who submits false claims.
- **Orr:** she went to KSL after Turo executives didn't respond. Quote: "He's clearly taking advantage of the system and making money off of customers."
- **Host's text to Orr:** "You won't be able to get out of this."

### Video in hand
- https://www.youtube.com/watch?v=1_wUVS5szfw
  - **Title (via YouTube oEmbed):** "Car rental service attempts to scam Utah woman out of hundreds."
  - **Channel:** KSL News Utah.
  - **Upload date, views (539K seed), description:** NOT confirmed because of the YouTube bot wall. Retry later.
  - It appears to be the TV version of the Oct 5, 2026 KSL story above, matched by title and subject. That link is an inference, not confirmed from the description.

### Other recent cases (2025–2026)
- **InvestigateTV (Gray), June 29, 2026** (Daniela Molina, Rachel DePompa, Scotty Smith). https://www.investigatetv.com/2026/06/29/rental-car-ai-scanners-flag-alleged-damage-leaving-customers-with-surprise-bills/
  - **Jessica Fields (Georgia, Hertz, Atlanta airport):** billed $350 ($160 for two dents plus $190 in administrative fees), or $290 if paid that day. The alert came about 17 minutes after checkout. Hertz sent it to collections in May. She fought it for 10 months, and the claim was closed with "no financial responsibility."
  - **Jessica Paciolla (Pennsylvania, Sixt, Orlando):** billed $1,500 for two scratches, including a $200 processing fee. Sixt closed it as "goodwill," blaming a "routing error."
  - **Consumer Federation of America's Ben Winters:** the scanners "are not required to prove how accurate they are."
- **First Alert 4 / KMOV St. Louis, July 1, 2026** (Heather Sullivan). https://www.firstalert4.com/2026/07/01/rental-car-damage-bill-shock-how-protect-yourself-incorrect-bills-before-you-drive-off/
  - **Sheilah Williams, 70, St. Louis (Enterprise):** a $2,000 hail-damage bill. Enterprise dropped it.
  - **Karl Erickson, Seattle (Hertz, Colorado Springs):** about $1,300, billed about 3.5 weeks after return. It was resolved after weeks of letters.
  - **Elliott:** "the ding and dent scam."
  - **Hertz:** billable damage occurs in about 3% of rentals.
  - **The 55+ angle:** Williams is 70.
- **Consumer Rescue: Chad Gross (Colorado), Hertz at Houston IAH, $1,638.** The article also says $1,648 in two places. Published Oct 28, 2024, updated May 31, 2026. https://consumerrescue.org/travel-troubles/hertz-rental-car-damage-scam-report/
  - The evidence photos showed a different Malibu, with an Oklahoma plate instead of his Texas plate.
  - Hertz sent the bill to collections and put him on its Do Not Rent list, then admitted the mistake and offered 1,900 points.
  - The original incident is from 2024.

### AI damage scanner (Hertz / UVeye) with dates
- **The Autopian, July 10, 2025.** https://www.theautopian.com/customers-outraged-with-hertz-ai-scanners-they-say-automatically-charge-for-questionable-damages/
  - **Adam Foley:** charged $190 for a roof ding and hood mark, or $125 if paid that day.
  - **Another renter:** charged $440 for a wheel scuff ($250 repair, $125 processing, $65 admin), originally via The Drive.
  - **Hertz:** "Over 97 percent of cars scanned with this technology have not detected any billable damage." Live agents review flagged images. "Our damage policy has not changed."
- **FOX 26 Houston, Aug 20, 2025** (Heather Sullivan). https://www.fox26houston.com/news/rental-cars-using-ai-damage-hertz-billing
  - Hertz uses UVeye and planned 100 airport locations by the end of 2025.
  - Sixt uses a similar system called "Car Gate."
  - **Zhenguo Lin (Hertz, Atlanta):** billed $220 ($80 damage plus $140 fees), removed after a BBB complaint.
  - **Hertz:** more than 97% of 500,000 scanned rentals showed no billable damage.

### Official advice / protection steps (sourced)
- **Photos and video:** take them at pickup AND drop-off, every angle, including the roof and interior. Sources: KSL, InvestigateTV, KMOV, FOX 26, Consumer Rescue.
- **Get the scanner report:** "do not leave until you get the AI scanner report" (Paciolla, InvestigateTV).
- **Ask for evidence before paying:** before-and-after images, the damage location, the repair cost and an invoice (Christopher Elliott, FOX 26).
- **Dispute in writing:** dispute and keep records; ask for an additional review (KMOV).
- **Check your own coverage:** check personal auto insurance and credit-card rental coverage before buying the counter coverage, which is about $30–$60 a day (Elliott, FOX 26).
- No FTC or state AG guidance specific to rental damage bills was found.

### Hotel resort fee (low priority)
- No source was found for a Hilton $75/night resort fee. The only $75 figure is a nightly *deposit* at YOTEL San Francisco, Select by Hilton, per a resortfeechecker.com search snippet (page not opened). Treat the claim as unsourced.

### Could not find / needs verification
- **Seed video stats:** the 1_wUVS5szfw upload date, the 539K views and the description are unconfirmed (YouTube bot wall).
- **"4-year-old" Reddit photo:** KSL says only "years ago." The Reddit post was not found.
- **"5,000 tire claims":** this is the host's own claim in a text, not verified by KSL or Turo. Attribute it: "the host bragged…"
- **Avis or Budget 2026 cases:** none confirmed. Avis/Budget appeared only in reader comments, not reporting.
- **BBB complaint counts for Hertz:** not found as a number. The articles say only that complaints "surged."
