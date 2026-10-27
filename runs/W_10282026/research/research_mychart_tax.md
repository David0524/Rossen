# Research: MyChart "Medicare Kit" phishing + fake property-tax notices
Prepared Mon 10/19/2026 for the Wed 10/28/2026 show. Only pages actually loaded are cited.

**Access notes (read first)**
- beckershospitalreview.com: HTTP 403 on every URL, both WebFetch and curl ("Please enable JS"). The Wayback copy exists (snapshot 2026-09-02) but the proxy blocked it too. **I could not read the Becker's article.** The 41 count below comes from outlets that cite it.
- consumeraffairs.com, fingerlakesdailynews.com, kzst.com, einnews.com: HTTP 403.
- YouTube: yt-dlp metadata calls (video_info.sh and the default client) were bot-walled ("Sign in to confirm you're not a bot"), so there are **no exact upload dates.** Views and relative age ("1mo ago" and so on) come from YouTube's own search-results page, fetched 10/19/2026. "1mo ago" means roughly 4–8 weeks before 10/19, so about mid-Aug to mid-Sept. Before an outline, retry video_info.sh after a 5+ minute wait, as CLAUDE.md says.
- I have not watched any clip. The descriptions below come only from titles and YouTube description snippets.

---

## STORY A: MyChart "Medicare Kit" phishing

### Confirmed facts
| Fact | Source (loaded) | Date |
|---|---|---|
| A fake email or text says the recipient was "selected" for a free "MyChart Medicare Kit" or "Senior Health Package." The buttons say "Claim Your Reward" / "Start Survey" / "Claim Kit Now." Per Epic, the link leads to a countdown clock, then a short survey, then a "free" kit that asks for a small shipping fee at the last step. The sites collect names, addresses, phones, emails and card numbers. A second version, "Your results are ready," leads to a fake MyChart sign-in page that steals passwords and may install malware. | Denver Health: https://www.denverhealth.org/news/2026/10/beware-fake-mychart-emails | Oct 9, 2026 |
| Epic's position, paraphrased by Denver Health: the rise comes from scammers exploiting the MyChart brand. It is "not a security problem with MyChart itself," and patients can keep using it. | same | Oct 9, 2026 |
| Epic's Trevor Berceau (director of R&D), quoted: "The increase in attempts is due to scammers taking advantage of the popularity of the MyChart brand" and "If something doesn't feel right, however, stop and check." He says this is not a security problem with MyChart. Systems named: Texas Health, Avera Health (SD), Methodist Health System (TX), Premier Health (OH), Sentara Health (VA). The article says "more than a dozen" systems. | Healthcare Dive (Jill Hughes): https://www.healthcaredive.com/news/health-systems-warn-patients-of-mychart-phishing-scam/828597/ | Aug 24, 2026 |
| Berceau posted about the scams on July 27. AHCJ says 41 systems have warned patients and cites Becker's Health IT. Epic guidance: MyChart does not run giveaways, and a countdown timer is a sign of a fake. | AHCJ (Karen Blum): https://healthjournalism.org/blog/2026/09/mychart-phishing-scam/ | Sept 16, 2026 |
| **PA AG Dave Sunday**: "Scammers are always looking for new ways to obtain as much of your personal information as possible," and "Stay on the lookout for this new scam tactic, and contact your medical office." The AG says no "MyChart Medicare Kit" program or reward exists. **The release does not mention a fee or any dollar amount.** Report to scams@attorneygeneral.gov or 1-800-441-2555. | PA AG: https://www.attorneygeneral.gov/taking-action/ag-sunday-warns-pennsylvanians-of-phishing-scam-targeting-mychart-patient-portal-users/ | **Aug 28, 2026** |
| WPXI covered the AG warning. | https://www.wpxi.com/news/local/mychart-patient-portal-scams-prompt-warning-pennsylvania-attorney-general/7PSLCJ5IMZHOXJYIDVRREMQ5FI/ | Aug 28, 2026 |
| Philadelphia-area systems: Penn Medicine, Jefferson Health, Temple Health, Main Line Health, Virtua. Virtua's Tom Gordon: "The leverage with healthcare is you're going to have a certain reaction." No victims are reported. | Philadelphia Inquirer (Sarah Gantz): https://www.inquirer.com/health/mychart-medicare-phishing-scam-philadelphia-20260902.html | Sept 2, 2026 |
| Penn Medicine has "received few reports from patients." Main Line Health is not aware of any patient who was affected. | NBC10 (Kate Reilly): https://www.nbcphiladelphia.com/investigators/consumer/mychart-text-email-fake-message-phishing-scam/4454876/ | Aug 27, 2026 |
| University Health (San Antonio) warning. Subject lines include "Your MyChart Medicare Kit Awaits" and "Here's your senior package." Spokesperson Elizabeth Allen: "People shouldn't click on strange links." She also said MyChart and Epic "are not going to send out free offers." None of its patients are known to be affected. | KSAT: https://www.ksat.com/news/local/2026/08/18/latest-phishing-scam-is-targeting-medicare-patients/ | Aug 18, 2026 |
| Sentara alert: subject lines include "Your MyChart Medicare Kit Awaits" and "Complete the MyChart Survey." | https://www.sentara.com/aboutus/news/incident-information | undated on the page |
| National Desk / Sinclair: MyChart has about 190M patients worldwide. One scam email says "You've been selected" for a 2026 Medicare Health Kit. Gizmodo obtained 166 MyChart-related FTC complaints through FOIA (not all are phishing). | CBS Austin / TNND (Maria Tedesco): https://cbsaustin.com/news/nation-world/mychart-urges-patients-to-stay-alert-of-phishing-scam-medical-results-ftc-fake-login | Sept 15, 2026 |

**The "41 health systems" count.** It is attributed to Becker's by AHCJ (Sept 16) and by Money Talks News (Oct 7). Money Talks News says the count came from ConsumerAffairs "by late August." I could not read Becker's to confirm the number or its list of systems. A search snippet shows Becker's URL slug is `6-health-systems-…` with a "41" headline (it was updated as the count grew). The earlier version was headlined "21 health systems."

### $9.95 / $29.95 victim: who reported it
- **Primary:** Gizmodo (Matt Novak, **Sept 8, 2026**), https://gizmodo.com/that-free-mychart-medicare-kit-is-a-scam-2000805167. It is from an FTC consumer complaint that Gizmodo obtained through FOIA. **Indiana complainant, August 2026, age 50–59.** Exact quote: "They then charge you the 9.95 and immediately try charging your card another 29.95 for another scam company." The same article has other complaints with no dollar amounts: Minnesota (age 70–79, the card later showed a charge listed as an animal/pet service), Illinois (age 70–79, paid shipping with a Mastercard) and Oklahoma (age 60–64, paid shipping after a survey).
- The Cool Down (Leigh Cook, Sept 15, 2026), https://www.thecooldown.com/?p=789399, repeats the Indiana quote and credits Gizmodo's FOIA. No age is given.
- **Conflict:** Money Talks News (Kendall Blythe, Oct 7, 2026), https://www.moneytalksnews.com/a-fake-mychart-message-offers-a-free-medicare-kit-dozens-of-health-systems-are-warning-patients/, describes the victim as "in their 70s" and credits ConsumerAffairs. Gizmodo's primary source says **50–59**. Use Gizmodo and do not say "in their 70s" for the $9.95 victim. The 70–79 complainants in Gizmodo are different people with no dollar figures.

### Video in hand (YouTube; views and age observed 10/19/2026 from YouTube search; exact upload dates not retrievable)
| Video | Channel | Views | Age | Length | What it appears to show (title/snippet only) |
|---|---|---|---|---|---|
| https://www.youtube.com/watch?v=vATdvkX57eU "Scammers are impersonating MyChart. Here's how to protect yourself." | CBS Philadelphia | 169,755 | 1mo ago | 2:29 | "CBS News Philadelphia is In your Corner with a warning…" A consumer piece. **This is the strongest by far.** The snippet doesn't say whether it covers the kit or the results variant. |
| https://www.youtube.com/watch?v=BO59Vj2ExE8 "Beware: Scammers pretending to be from MyChart asking for personal information" | NBC10 Philadelphia | 12,154 | 1mo ago | 1:50 | Probably the broadcast version of NBC10's Aug 27 story (reporter Valeria Aponte-Feliciano). That story is about the Medicare Kit. |
| https://www.youtube.com/watch?v=EmFb8Cs6uYA "How to avoid falling victim to MyChart scams" | NBC4 Washington | 3,896 | 1mo ago | 2:19 | Consumer reporter Susan Hogan. Emails and texts made to look like MyChart. |
| https://www.youtube.com/watch?v=F0Bxcj4PN6g "Phishing scam: MyChart urges patients to stay alert" | The National Desk | 1,837 | 1mo ago | 0:44 | Likely the companion to the TNND Sept 15 article ("2026 Medicare Health Kit"). |
| https://www.youtube.com/watch?v=FJYTdma558o "Scammers target MyChart users nationwide" | CBS Chicago | 1,201 | 3w ago | 0:54 | "Scammers are now impersonating the patient…" |
| https://www.youtube.com/watch?v=ZqTemmgRnLs "Scammers impersonating MyChart to steal personal data" | CBS Chicago | 614 | 3w ago | 1:58 | same |
| https://www.youtube.com/watch?v=alOlxsKuEy0 "Fake MyChart emails target patients with frightening test results" | WMAR-2 | 1,201 | 1mo ago | 1:09 | The **test-results** variant, not the kit. |
| https://www.youtube.com/watch?v=THc4cwcbq2c "Sentara Health warns patients about phishing scam" | 13News Now | 103 | 2mo ago | 0:30 | The snippet names the subject line "Your MyChart Medicare kit awaits." **This is explicitly the kit.** |
| https://www.youtube.com/watch?v=ytH8i5ZNJnI "Surge in Sentara MyChart scams" | 13News Now | 298 | 2mo ago | 2:18 | Derek Lytle "spoke with a…" (cut off). Possibly a person on camera. |
| https://www.youtube.com/watch?v=NHoq4TfAjaw "Latest phishing scam targets Medicare patients, University Health warns" | KSAT 12 | 237 | 2mo ago | 2:02 | Matches the KSAT Aug 18 article (Medicare Kit). |
| https://www.youtube.com/watch?v=ks2EXsSAZWI "AG warns of phishing scam targeting MyChart users" | WTAJ | 402 | 1mo ago | 0:31 | The PA AG warning. |
| https://www.youtube.com/watch?v=E0fERit3KLU "Money Matters: MyChart phishing scheme" | FOX59 | 554 | 1mo ago | 2:09 | Zach Myers. Indianapolis, the same state as the $9.95 complainant. |
| https://www.youtube.com/watch?v=toRDqRiEycw "Hospitals warn patients of MyChart scam…" | WKYC | 676 | 1mo ago | 1:58 | A multi-topic segment. |
| https://www.youtube.com/watch?v=nrhyf3xdajI "Fake MyChart emails stealing your personal info" | WOOD TV8 | 528 | 1mo ago | 0:35 | |
| https://www.youtube.com/watch?v=db0SwhAta28 "MyChart warns users of increase in fraudulent emails…" | WTVO/WQRF | 204 | 1mo ago | 0:30 | |
| https://www.youtube.com/watch?v=fBtPvzGCjkg "ECU Health patients react to reports of MyChart phishing scams" | WITN-TV | 70 | n/a | n/a | Patient reactions. Possibly people on camera. |
| Non-TV explainer clips: Money Instructor nrCED_kaFW8 (967 views, 2mo), Ritter Insurance Kmj_A0sqBos (796, 1mo), Putnam County District Library VMgXnJOUDP0 (263, 11d) | | | | | Low value. Not news footage. |

### Victims with real losses
- Indiana FTC complainant (Gizmodo FOIA, Sept 8): paid **$9.95**, then a **$29.95** charge was attempted. That is the only dollar figure I found.
- The MN, IL and OK complainants entered card details or paid shipping (Gizmodo). No amounts were given.
- I found no named or on-camera victim. Every health system that addressed it (University Health, Main Line Health, Penn) said there were no or few known affected patients.

### Official warnings / protection steps
- PA AG (Aug 28): no such program exists. Don't reply to the message or click links in it, including "unsubscribe." Never share passwords or verification codes. Ignore "go to a computer to verify/unlock" prompts. Use only the official app or site. 1-800-441-2555 / scams@attorneygeneral.gov.
- Denver Health (Oct 9): the MyChart logo doesn't prove a message is real. Hover over links to check them. Log in by typing the address or using the app. **If you entered card details, call your bank, report the fraud and get a new card.** If you entered a password, change it right away. If you ran keyboard shortcuts or downloaded something, disconnect and get the computer checked. Report Medicare fraud at 1-800-MEDICARE or HHS OIG. AARP Fraud Watch helpline: 877-908-3360.
- Epic, via Healthcare Dive and AHCJ: no giveaways, a countdown timer is a red flag, it will never ask you to press keyboard shortcuts or change your contact info, and don't pay money or send personal info.

### Could not find / needs verification
- **Becker's article itself:** the exact count today, the list of systems and the publication date. The page was 403 and the archive was blocked.
- Exact YouTube upload dates for every clip (bot-walled). Retry video_info.sh.
- Whether the CBS Philadelphia clip (169K views) covers the kit or the test-results variant. The snippet doesn't say.
- Epic's original July 26/27 MyChart blog post (not loaded).
- No named victim and no victim on camera.

---

## STORY B: Fake property tax / foreclosure notices

### Warning about the seed
**The seed URL (https://lacounty.gov/2026/10/14/county-officials-warn-property-owners-about-fake-property-tax-relief-scam-copy/) does NOT describe a scam.** Its headline says "Fake Property Tax Relief Scam," but the body is the Assessor's Misfortune & Calamity disaster-relief release (Oct 14/15, 2026; PIO Stephen R. Whitmore). It looks like a CMS "-copy" page that kept an old headline. **Don't cite it.** It doesn't mention Louisiana or New York.

The actual LA County warning is about the **IRS "Form 1098-SR" tax-freeze scam (social media, online videos, phone calls), not mailed notices**. Random Lengths News, **Sept 8, 2026**, https://www.randomlengthsnews.com/archives/2026/09/08/fake-property-tax-scam/77354. It names Assessor Jeff Prang, Treasurer-Tax Collector Elizabeth Buenrostro Ginsberg, Auditor-Controller Oscar Valdez and DCBA Director Rafael Carbajal: "No such IRS form or federal property tax relief program exists." No victims or losses are reported.

### Which scam each source describes
| Source (loaded) | Date | Scam |
|---|---|---|
| Random Lengths (LA County) — above | Sept 8, 2026 | **AI/video 1098-SR freeze**, not mail |
| Wisconsin DOR release: https://www.revenue.wi.gov/Pages/News/2026/Property-Tax-Relief-Scam.pdf | Sept 3, 2026 | **AI video.** It points viewers to a "Senior Homeowner Tax Review Request" or "IRS Form 1098-SR," and the phone number in it reaches scammers. Sec. David Casey: "This is an AI-generated video designed to trick seniors into sharing Social Security numbers and banking details, or paying fees for nonexistent filing services." |
| Douglas County, **Colorado**: https://www.douglasco.gov/consumer-alert-viral-video-promotes-fake-federal-property-tax-form/ | Aug 6, 2026 | **AI video** ("Senior Homeowner Tax Review Request"). Assessor Toby Damisch: "Artificial intelligence can make false information look and sound convincing." Residents have called asking for the form. No losses reported. |
| Teller County, CO (Gazette): https://gazette.com/2026/08/07/assessor-warns-of-property-tax-scam/ | Aug 7, 2026 | **AI video/social** freeze claims. Assessor Kurt Schoenberger: "We've already had several calls to our office." |
| Montgomery County, OH (WDTN): https://www.wdtn.com/news/fake-senior-homeowner-tax-relief-scam-targets-area/amp/ | "2 months ago" (no exact date on the page) | **YouTube video**, "Senior Homeowner Tax Review Request." It was taken down after calls. Auditor Karl Keith: "If you see something online and are unsure whether it is legitimate, call us." |
| LA County DCBA "Fake Property Tax Bills": https://dcba.lacounty.gov/scam-alerts/fake-property-tax-bills/ | **July 8, 2025** (not 2026) | **Fake bills** that say "pay immediately or face legal action." The page doesn't say whether they come by mail or whether they use real parcel data. Real LA secured bills are mailed in October. TTC 888-807-2111; DCBA 800-593-8222. |
| Kent County, MI bulletin: https://content.govdelivery.com/accounts/KENTCOMI/bulletins/3d48691 | **Mar 3, 2025** | Foreclosure-rescue, "tax specialist" and deed-theft scams aimed at delinquent owners. Treasurer Peter MacGregor: "My office will only contact homeowners if they are delinquent with their property taxes." |
| Lake County, IN (Chicago Tribune via Yahoo): https://www.yahoo.com/news/taxpayers-warned-delinquent-property-tax-213500686.html | **June 23, 2023** | **Mailed fake "Distraint Warrant"** delinquent-tax letters with an 800 number that threaten seizure. Three taxpayers brought letters in, and none paid. The same scam was noted in PA, NY and FL. Treasurer John Petalas: "I am concerned someone will pay them." |

**The mailed-fake-notice story (the producer's actual pitch) has no confirmed 2026 county warning that I could load.**
- Wayne County, NY Treasurer, "fake property tax, foreclosure notices" (Facebook messages plus mailed letters), per a search snippet only: https://www.fingerlakesdailynews.com/local/wayne-county-treasurer-warns-of-fake-property-tax-foreclosure-notices/. The page returned **403**, so I don't have its date or details. **Needs verification.** A separate Wayne County NY item (fltimes, about a 2025 redemption deadline) concerns a real law firm's solicitation that used public records. It is not a forgery.
- Louisiana: I found nothing from 2026. Search snippets show older items only: Ascension Parish sheriff, Nov 2025, a private firm's "Property Assessment Profile" mailer (WBRZ); Cameron Parish 2022; Tangipahoa 2024. None of these were loaded.
- **I could not find the source of the "counties from Louisiana to New York" phrase.**

### Video in hand (YouTube search, observed 10/19/2026; no exact upload dates)
**AI-video / 1098-SR freeze scam (2026, current):**
| Video | Channel | Views | Age | Length | Shows (title/snippet) |
|---|---|---|---|---|---|
| https://www.youtube.com/watch?v=AQSvg5ovvWA "AI video scam warning" | FOX 9 Minneapolis | 815 | 2mo ago | 7:12 | St. Louis County, MN warns about AI videos promoting fake tax relief |
| https://www.youtube.com/watch?v=CG3exs1XGiY "AI video scam targets senior homeowners, Franklin County Auditor's office issues warning" | WSYX ABC 6 | 389 | 2mo ago | 1:23 | Columbus, OH |
| https://www.youtube.com/watch?v=ibgJMgcsihI "Douglas County assessor warns seniors about viral AI property tax scam on YouTube" | Denver7 | 261 | 2mo ago | 1:34 | Matches the Douglas Co. CO alert |
| https://www.youtube.com/watch?v=Wb39bvgsXEM "Fake property tax relief form spreading in AI videos" | 23ABC KERO (Bakersfield) | 212 | 2mo ago | 2:33 | "1098-SR" in AI-generated videos |
| https://www.youtube.com/watch?v=DZ_HvZmFZJ4 "Fake AI video falsely claims Congress created senior property tax freeze program" | WXOW 19 (La Crosse WI) | 45 | 1mo ago | 0:39 | The Wisconsin DOR warning |
| https://www.youtube.com/watch?v=7gRqupmZdxA (also xzFxoNPBxlA) "Property tax scam warning" | WDTN | 85 | 3w ago | 0:27 | No useful snippet. Probably the Montgomery Co. OH AI-video item, **not confirmed** |

**Mailed fake tax / foreclosure letters:** I found **no 2026 local TV clip.** Everything found is old: WFMY "Scam letter circulating, claims you owe taxes" MvWr91LstFI (1,031 views, 2y), WCNC Mecklenburg letter KBjdKwRQeNQ (312, 1y), KOB New Mexico letter h2MY6SLwLo0 (393, 11mo), News 5 Cleveland owo9ylIRcL4 (914, 1y), KTVE Lincoln Parish LA "fake property tax notices" O3y3GyhY7uU (57, 4y), Tampa Bay 28 AkSDxF4y7FU (5y). Also: Shasta County DA "fake property tax **email** scam," Action News Now uMqECejbwFw (28 views, 1mo). That one is email, not mail, and its article wasn't found.

### Victims with real losses
- **None found for either scam.** All the 2026 warnings report calls or inquiries only (Douglas CO, Teller CO, Montgomery OH). Lake County IN (2023): none of the three paid.

### Official warnings / protection steps
- Call the county treasurer/assessor using a number from the official site, not one printed on the letter or shown in the video (LA DCBA 2025; Lake Co. IN 2023; Montgomery Co. OH).
- No federal form or program freezes local property tax. Property tax is purely local and state (WI DOR, LA County, Douglas CO).
- Don't give an SSN or bank details, and don't pay a "filing fee" (WI DOR, Douglas CO).
- Report to the FTC / state consumer protection; WI hotline (800) 422-7128; LA DCBA 800-593-8222.
- Legitimate relief to point to instead: Ohio Homestead (exempts $29,000; Montgomery Co. says about $550/yr savings; 937-225-4341).

### Could not find / needs verification
- A 2026 warning about **mailed** fake tax/foreclosure notices built from public-record data. The Wayne County NY item is 403 and unverified, and there is no Louisiana item from 2026.
- Any victim who paid.
- Any 2026 TV clip of the **mailed-notice** version.
- The source of the "Louisiana to New York" framing.
- **Recommendation:** the provable, video-backed 2026 story is the **AI-video "Senior Homeowner Tax Review Request / 1098-SR" scam**, not mailed foreclosure notices. Re-scope the pitch, or treat the mailed version as unconfirmed.
