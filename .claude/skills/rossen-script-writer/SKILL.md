---
name: rossen-script-writer
description: Write a Bible Script for the Jeff Rossen show (Rossen Reports) — the shooting outline Jeff runs off the teleprompter, with tease block, story segments, clip beats, graphics cues and sponsor placement. Use this whenever the user asks to write the script, draft this week's show, build a bible or Bible Script, write a Wednesday or Friday show, hands over show topics or stories to be turned into a rundown, or asks to revise an existing bible for length, voice, story order or clip beats. Do not use for general writing, articles, blog posts, or scripts for any other show.
---

# Rossen Reports Bible Script writer

## First, and it governs everything: a bible is not a script

It is a **talking points outline that runs on Jeff's teleprompter** so he does
not get lost or off track during a live show. He improvises around it. He
almost never reads a line as written.

So never write a line whose value depends on him delivering it verbatim.
No crafted triplets, no punchlines, no rhetorical set-pieces that collapse if
he paraphrases. Write the things he **cannot** improvise:

- the exact figure, and who published it
- the proper nouns — company, agency, state, platform, product
- the mechanics of the scam, in the order they happen
- the turn into each clip
- the protection steps

He supplies the performance, the asides, and the outrage. The document supplies
the spine and the facts.

**Corollary that matters more than it looks:** the bible must carry *more*
searchable specifics than Jeff will actually say, because the clip pipeline
only ever reads the document. The Voice section below has the worked example.

## The hard contract with the clip pipeline

Scripts are parsed by `rossen-beat-extractor` and the rest of the harvest
pipeline. Break these and it fails **silently**, which is worse than failing
loudly. This section is not stylistic.

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
  with two, four, and five parens, and one with no orientation at all — those
  are mistakes. Normalize every time.

### Not clip beats

These are stills and art, sourced separately. Never counted as clip beats:

```
(((TAKE ... SCREENSHOT)))
(((TAKE ... STILL)))
(((TAKE FULLSCREEN)))
(((CREATE FULL SCREEN GRAPHIC XXX)))
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

This is the single highest-leverage thing in this skill. The 6 to 10 dash
lines immediately above a clip marker are the *only* thing the pipeline reads
to decide what footage to find.

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

Do not shorten the runway to save space. The runway is the input.

### Lead-in phrasing sets the clip role

The last line before the marker tells the extractor what kind of footage this
is. Past scripts are consistent about this and the consistency is load-bearing.

| Lead-in | Signals |
|---|---|
| LISTEN TO WHAT HAPPENED TO HIM / THINK WHAT YOU WOULD DO | victim interview |
| WATCH WHAT HAPPENS WHEN / HE SET UP A REAL STING / BUSTED HIM IN THE ACT | confrontation or bust |
| HAVE A LOOK / HERE YOU CAN SEE | evidence footage |
| HERE'S WHAT WE KNOW RIGHT NOW | network or wire report |
| WATCH HIM SHOW YOU HOW | explainer or demo |

### Dated news beats need their proper nouns

When a segment exists because something happened this week, put the specifics
in the copy: the company, the dollar amount, the agency, the state, the ruling.
*Temu fined $232 million by the EU.* *Maryland banning dynamic pricing.* Those
exact strings are the highest-yield search the pipeline can run. If they live
only in your head, the pipeline never sees them.

## Length — measured from the aired bibles, treat as hard

Rendered in house format (Arial, 23/18pt, Letter, 1" margins, 1.15 spacing).

### Wednesday / F2 TOP STORIES

| Block | Pages | Words | Bullets | Clips |
|---|---|---|---|---|
| Tease block | 3 | 210–340 | 9–21 | 0 |
| Story 1 (lead) | 7–8 | 690–790 | 41–51 | 5–7 |
| Story 2 | 2–4 | 240–520 | 20–31 | 1–3 |
| Story 3 | 2–6 | 230–490 | 17–31 | 1–4 |
| Story 4 (closer) | 3–5 | 175–300 | 14–25 | 1–2 |
| **Whole document** | **18–22** | **1,700–2,300** | | **10–12** |

Four stories. Always four. The tease is always 3 pages. Story 1 is always
7–8 pages — about 40% of the body and half the clips. It is front-loaded far
harder than feels natural.

### Friday

10–12 pages total. One content story of Wednesday quality, then the guest.

### Line length

Across 396 aired body bullets: **mean 11.6 words, median 11.** Only 14% run
five words or shorter; 60% land between 6 and 15. A bullet is a full clause
carrying a fact, not a clipped fragment. Over-fragmenting is the most common
failure mode — it reads punchy and delivers nothing.

## Wednesday running order

```
**SHOW TITLE / DATE**

**STORY 1 HEADLINE**              <- tease, all caps, clipped, urgent
-4 to 6 dash lines
**—------------------------------------------------**
**STORY 2 HEADLINE**
-4 to 6 dash lines
**—------------------------------------------------**
**STORY 3 HEADLINE**
**—------------------------------------------------**
**STORY 4 HEADLINE**

HIT LIKE AND SUBSCRIBE
JOIN THE CHAT
                                  <- pipeline boundary. tease ends here.
**STORY 1 TITLE**
-hook lines
-mechanics, in order
**MID-STORY BEAT HEADER**         <- bold caps, turns the story
-setup lines carrying specifics
(((PLAY CLIP XXX HORIZONTAL)))
OUT:
... repeat 5-7 times ...
**HERE'S HOW TO PROTECT YOURSELF**
-flat run of dash lines

(((SPONSOR TEASE - KILL BANNERS)))
**I'M ALWAYS LOOKING FOR WAYS TO PROTECT YOU FROM SCAMS…**
-OUR SPONSOR TODAY DOES JUST THAT.
(((PLAY SPONSOR)))

**STORY 2 TITLE**  ... **STORY 3 TITLE** ... **STORY 4 TITLE**

-END OF SHOW
```

Sponsor drops at a story boundary — after story 1 or story 2, whichever reads
better — never mid-story. Where the sponsor's product connects to the story
just told, bridge into it thematically rather than generically.

Story 4 is the exhale. It is never a scam: a price cut, a money-saver, a
what-not-to-buy. It closes the show on good news.

## Friday running order

Content story is fully written to Wednesday standard. The deals half is not
scripted.

```
**DATE — CONTENT STORY TITLE**
-tease lines for the content story
________________________________________
-THE HOTTEST AMAZON DEALS OF THE WEEK WITH THE FOLKS FROM DEALSEEK
-deal count and headline discount
________________________________________
-PLUS, YOUR LIVE REQUESTS
-HIT LIKE AND SUBSCRIBE
-JOIN THE CHAT

[content story, full treatment, 0-4 clip beats]

(((SPONSOR TEASE - KILL BANNERS)))
(((PLAY SPONSOR)))

**NOW, ONTO MY FAVORITE PART OF FRIDAYS**
**-BRING IN [GUEST]-**
-I WANT TO BRING IN [GUEST], FROM DEALSEEK.COM
((QR CODE UP))                    <- two parens, not three

- PRODUCT NAME
- RETAIL PRICE: $X
- DEAL PRICE: $Y
- Z% OFF WITH THE PROMO CODE      <- or PRICE DROP, or SUB & SAVE

(((JEFF AND [GUEST] LIVE DEAL REQUESTS)))

-END OF SHOW-
```

Ask which deals expert is on — it varies by episode (Trey Donovan, Nader
Marcos). Ask for the deal list and prices if not supplied; do not invent
products or prices.

## Voice

Measured from 141,477 spoken words across 19 aired transcripts, not inferred.

**ALL CAPS is prompter ergonomics, not style.** He is scanning, not reading.

### The negative space — the tell of a generic consumer reporter

Counts are raw occurrences across the whole 141k-word corpus. He essentially
never says these:

| Word | Count | | Word | Count |
|---|---|---|---|---|
| `folks` | 2 | | `utilize` | 2 |
| `consumers` | 8 | | `individuals` | 1 |
| `however` | 2 | | `the bottom line` | 1 |
| `allegedly` | 3 | | `here's the thing` | 1 |
| `reportedly` | 1 | | `furthermore` / `moreover` | 0 |
| `alleged` | 0 | | `in conclusion` | 0 |

No anchor connective tissue. No hedging. No formal register. He says `buy`
(113) not `purchase` (8). He says `you`, not `consumers` — 4,587 times,
roughly one word in every thirty.

### What he reaches for

| Phrase | Count | | Phrase | Count |
|---|---|---|---|---|
| `right now` | 347 | | `insane` | 32 |
| `you guys` | 187 | | `exploding` | 28 |
| `by the way` | 185 | | `brand new` | 25 |
| `crazy` | 65 | | `pause` | 24 |
| `watch this` | 34 | | `protect yourself` | 22 |

`right now` is the single most characteristic thing he says. Everything is
happening *right now*. Write currency into the copy.

### What is ad-lib and stays out of the document

In every transcript, in zero bibles. These are his, not the writer's:

- The open — *"Welcome to Rossen Reports. I am Jeff Rossen"* plus an
  urgency-of-arrival line (*"had to get on the air,"* *"packed show today"*).
- The `by the way` asides. 185 of them, none scripted.
- `WATCH THIS` — his live handoff, spoken the instant before a clip rolls.
  Never write it. The setup lines above the marker are your job; that is his.
- The close — a plug for another video, then *"we'll see you next time."*
  Every show. Never in a bible. The document ends at `-END OF SHOW`.

### He expands on air, so over-specify in the document

The 06/22 bible wrote:

```
-WATCH WHAT HAPPENED TO THIS OLYMPIAN!!
-SHE SAYS IT RUINED HER LIFE!!
```

What he actually said on 07/01:

> "Look what happened at a **Walmart** to this Olympian. She's an Olympic
> athlete. She was at the **self-checkout**. They **called the cops** in. And
> she says it ruins her life. Watch this."

He added the retailer, the location, and the police. The clip pipeline hears
none of that — it reads only the document. So the searchable specifics have to
be in the bullets, even when Jeff would obviously say them anyway.

### First person

Sparse but real, and it is house style — confirmed in the bibles, not just
ad-libbed. One or two per document, usually in a hook:

- `I HATE SCAMMERS, BUT I LOVE IT WHEN THEY GET BUSTED`
- `THAT'S FREE MONEY YOU'VE EARNED AND I'D BE DEVASTATED IF I LOST MINE!`
- `I HAVE NEVER BEEN A FAN OF EXPIRATION DATES… I'LL SHOW YOU WHY`

### Story selection

The channel's top performers: DEBIT CARD ALERT (1.5M), THESE Apps Are SPYING
on You (1.4M), They Know You're STEALING at Self-Checkout (1M), GENIUS Envelope
Scam (885K), 5 Walmart Scams (810K), GENIUS Tipping Scam (807K).

Every one takes something the viewer already does every single day — a debit
card, phone apps, self-checkout, the mail, Walmart, a tipping screen — and
turns it against them. None is an exotic fraud. The mundane daily object
weaponized is the pattern. `GENIUS` is his word for a cleverly built scam and
it recurs in the titles that perform.

## Research and honesty

Sometimes the stories arrive with the request; sometimes only a topic does. Be
ready for either. When researching:

- Go to primary sources — FTC, BBB Scam Tracker, FBI IC3, state AG, CFPB,
  court filings, company statements.
- Exact figures with source and date. Not rounded, not stale.
- Named victim cases and expert quotes, preferring original local reporting.
- Confirm recency. A scam trend from 2023 is not a story happening *right now*.

**Never invent a quote, statistic, victim, or source.** If it cannot be found,
say so and flag it. Mark anything single-sourced or inferred.

**You cannot watch video.** You can find where a clip lives and describe it
from its transcript or description. You cannot confirm what is on screen or
timestamp a moment. Say so rather than implying otherwise.

Citations go **inline as hyperlinks on the named source**, matching how aired
bibles link a study or a resource URL. Keep any `unconfirmed` or `TBD` flags
short and inline right at the relevant cue. **Do not add a sources or
verification section to the document** — no reference bible has one. The fuller
source rundown and verification notes go in the chat reply, outside the
document.

## Output

Deliver the bible as a `.docx` in house format. Build it with the `docx` npm
library using explicit run-level formatting — pandoc and plain
markdown-to-docx conversion do not reproduce this:

| Element | Format |
|---|---|
| Everything | Arial |
| Headers, story titles, mid-story beat headers | 23pt bold black |
| Spoken body lines | 18pt regular black, bold only on emphasized words |
| All production cues — clip, `OUT:`, graphic, sponsor, screenshot | 18pt **bold red FF0000** |
| Graphic card list items | 18pt regular red |
| CTA lines | 18pt regular black |
| `END OF SHOW` | 18pt bold black |
| Hyperlinks | blue 1155CC, underlined |

Page: US Letter, 1" margins all sides, line spacing 1.15. Blank paragraph
between distinct bullets and beats. **No** blank paragraph between a clip cue
and its `OUT:` line, or inside a graphic card.

Red versus black is the whole point of the colour: black is what Jeff says,
red is a production instruction.

Then, **in the chat reply and not in the document**, append a clip manifest:

```
CLIP MANIFEST
b01  HORIZONTAL  victim interview     retired officer / PayPal invoice / $10,000
b02  VERTICAL    evidence             garage fire / lithium leaf blower
b03  HORIZONTAL  confrontation bust   police sting / gold courier / $700,000
```

Then the source rundown and anything needing a human check.

## Self-check before delivering

- Re-read the user's actual instructions for this request — show day, sponsor,
  guest name, story constraints — and confirm each was followed. State
  explicitly anything missed or assumed rather than silently deviating.
- Four stories. 10–12 clip beats. 18–22 pages Wednesday, 10–12 Friday.
- Story 1 is roughly 7–8 pages and carries about half the clips.
- Every clip marker: three parens, orientation chosen, `XXX` literal, `OUT:`
  beneath it, URL and timecode blank.
- No `PLAY CLIP` inside the tease or a sponsor tease block.
- `HIT LIKE AND SUBSCRIBE` / `JOIN THE CHAT` closes the tease.
- Bullets average around 11 words. Not five.
- No invented quotes, stats, or sources; unverified items flagged inline.
- Nothing invented that no past bible contains. Follow the formula.

---

# Reference segments — verbatim from aired bibles

Lifted unedited from the library. These are the format of record. When anything
above disagrees with these, these win.

## The tease block — `F2 TOP STORIES, week of 07/13`

340 words, 3 pages. Four story blocks separated by rules, CTA closes it.
No PLAY CLIP marker anywhere in here. Ever.

```
**ATM/DEBIT CARD SCAMS ARE EXPLODING**

-WE'RE EXPOSING** NEW ATM/DEBIT CARD SCAMS** THAT COULD DRAIN YOUR BANK ACCOUNT BEFORE YOU EVEN KNOW WHAT HAPPENED. 

-CRIMINALS ARE GLUING ATM CARD SLOTS TO FORCE YOU TO TAP YOUR CARD... THEN STEALING YOUR MONEY AFTER YOU WALK AWAY. 

-OTHER SCAMMERS ARE CONVINCING VICTIMS TO LEAVE THEIR CARDS IN THEIR OWN MAILBOXES FOR "SAFE PICKUP." 

-FAKE BANK EMPLOYEES ARE CALLING PEOPLE... THEN SHOWING UP AT THEIR FRONT DOOR TO TAKE THEIR DEBIT CARDS. 

-AND WE'LL SHOW YOU THE SIMPLE MISTAKE MILLIONS OF PEOPLE MAKE EVERY DAY... FORGETTING TO GET THEIR DEBIT CARD BACK... 

-WE'LL SHOW YOU EXACTLY HOW EACH SCAM WORKS... AND THE SIMPLE STEPS TO STOP THEM.

**—------------------------------------------------**

**FAKE LOAN APPROVAL SCAM **

-THIS NEW ROBOCALL SCAM MIGHT BE THE LARGEST ONE I HAVE SEEN YET. IT’S EVERYWHERE!!

-HUNDREDS OF THOUSANDS OF YOU ARE BEING TARGETED.

-YOU’RE PHONE IS BEING SPAMMED 5, 6, 7 PLUS TIMES A DAY!

-YOU GET A PHONE CALL SAYING YOU'VE BEEN APPROVED FOR A MASSIVE LOAN... EXCEPT YOU NEVER APPLIED FOR ONE. 

-THE FTC IS SOUNDING THE ALARM ABOUT A NEW WAVE OF FAKE LOAN APPROVAL CALLS DESIGNED TO PANIC YOU INTO CALLING BACK. 

-WE'LL SHOW YOU WHY THAT ONE PHONE CALL COULD LEAD TO IDENTITY THEFT... AND WHAT YOU SHOULD DO INSTEAD.

**—----------------------------------------------------**

**FAKE A-I BOOKS SCAM ON AMAZON**

-THERE IS AN EXPLOSION OF DANGEROUS AI GENERATED BOOKS FLOODING AMAZON!

-SOME ARE FILLED WITH FALSE INFORMATION.

-SOME ARE IMPERSONATING REAL AUTHORS.

-AND SOME CONTAIN ADVICE EXPERTS SAY COULD ACTUALLY PUT YOUR LIFE AT RISK.

-WE'LL SHOW YOU HOW TO SPOT THEM BEFORE YOU WASTE YOUR MONEY... OR WORSE, YOUR HEALTH.

**—------------------------------------------------**

**WALMART IS SLASHING PRICES!**

-THEN, GOOD NEWS!!!  

-AFTER YEARS OF STICKER SHOCK AT THE GROCERY STORE, WALMART IS CUTTING PRICES ON THOUSANDS OF EVERYDAY ITEMS. 

-FROM HAMBURGER AND HOT DOGS TO FRESH PRODUCE, HOUSEHOLD ESSENTIALS, AND BACK TO SCHOOL SUPPLIES... 

-WE'LL SHOW YOU WHAT'S GETTING CHEAPER, HOW MUCH YOU CAN SAVE, AND HOW TO TAKE ADVANTAGE OF THE BIGGEST DISCOUNTS.

HIT LIKE AND SUBSCRIBE

JOIN THE CHAT
```

## Lead story — `F2 TOP STORIES, week of 07/13`

786 words, 51 bullets, 5 clip beats, 7 pages. The shape of every story 1. Note
the 6-10 setup lines carrying specifics before each clip, and the protection
list landing at the end as a flat run of dashes.

```
**THIS NEW ATM/DEBIT CARD SCAM TAKES YOUR MONEY WITHOUT STEALING YOUR CARD**

-CRIMINALS AREN'T TRYING TO STEAL YOUR CARD ANYMORE….

-THEY JUST NEED TO TRICK YOU INTO DOING SOMETHING THAT SEEMS HARMLESS. 

 -USING YOUR BANK'S **TAP TO PAY** FEATURE AT THE ATM... 

-THEN STEAL YOUR MONEY AFTER YOU THINK YOUR TRANSACTION IS OVER.

-HERE'S HOW IT WORKS.

-THE SCAMMERS SABOTAGE THE ATM BY **PUTTING SUPERGLUE INSIDE THE CARD SLOT**

-SO WHEN YOU TRY TO INSERT YOUR DEBIT CARD... IT WON'T GO IN… YOU THINK THE MACHINE IS BROKEN.

-THAT'S EXACTLY WHAT THEY WANT.

THIS IS GENIUS AND SCARY!!

**(((PLAY CLIP 1 HORIZONTAL)))**

**OUT: ****(ON THEIR ACCOUNT)**

**BUT THE MOST SURPRISING THING YET WAS ABOUT TO HAPPEN TO THEM!**

**THEY REPORTED IT TO THE BANK MANAGER…AND FILED CLAIMS WITH CHASE…**

**-REMEMBER, THEY’VE BEEN SCAMMED ON A CHASE ATM…**

**-AND GUESS WHAT CHASE DID WHEN THEY COMPLAINED???**

**(((PLAY CLIP 2 - HORIZONTAL)))**

**OUT: (ATM MACHINE)**

**THIEVES ARE STEALING YOUR DEBIT CARD, RIGHT OUT OF YOUR MAIL BOX!**

**-AND THE SHOCKING DETAIL… THEY CONVINCE YOU TO PUT IT THERE! **

-THEIVES CONVINCED THIS NEXT VICTIM THAT HIS ACCOUNT WAS COMPROMISED… HOW?

-THEY HAD INFO ABOUT RECENT TRANSACTIONS THAT WERE ACCURATE.

-THAT’S ALL THEY NEEDED! THEY ALSO MANAGED TO GET HIS PIN OUT OF HIM!

-THEN THEY TOLD HIM TO PUT THE COMPROMISED DEBIT CARD IN HIS MAILBOX… AND THAT A MEMBER OF HIS BANK WOULD COME BY TO TAKE IT

-AND THE SCAM IS 100% CAUGHT ON CAMERA… TAKE A LOOK

**(((PLAY CLIP 3 HORIZONTAL)))**

**OUT: (OFFICIAL I.D.)**

**BUT THIS NEXT ATM / DEBIT CARD SCAM IS EVEN MORE DANGEROUS**

-IT STARTS WITH A PHONE CALL.

-THE CALLER CLAIMS TO BE FROM YOUR BANK'S FRAUD DEPARTMENT.

-THEY TELL YOU THEY'VE DETECTED SUSPICIOUS ACTIVITY ON YOUR DEBIT CARD AND NEED TO HELP SECURE YOUR ACCOUNT.

-THEY USUALLY HAVE YOUR NAME, ADDRESS AND SOME ACCOUNT INFORMATION THEY BOUGHT ON THE DARK WEB.

-AND THE CALL SOUNDS BELIEVABLE BECAUSE **BANKS DO CONTACT CUSTOMERS** ABOUT POTENTIAL FRAUD.

-BUT THEN COMES THE TWIST…INSTEAD OF ASKING YOU TO VISIT A BRANCH OR WAIT FOR A REPLACEMENT CARD…

-THEY TELL YOU THEY'LL SEND AN EMPLOYEE TO YOUR HOME TO COLLECT YOUR COMPROMISED CARD

-THAT SAME DAY… SOMEONE ACTUALLY SHOWS UP AT YOUR FRONT DOOR.

-THEY'RE WELL DRESSED… PROFESSIONAL… CALM.

-THEY IDENTIFY THEMSELVES AS A BANK EMPLOYEE.

-THEY ASK FOR YOUR DEBIT CARD.

-TO TRY AND GET YOU TO LOWER YOUR GUARD DOWN, THEY CUT IT IN HALF RIGHT IN FRONT OF YOU.

-YOU THINK..."MY CARD IS DESTROYED. NOBODY CAN USE IT NOW."

-BUT THAT'S EXACTLY WHAT THE SCAMMERS WANT YOU TO BELIEVE.

**(((PLAY CLIP 4 HORIZONTAL)))**

**OUT: ****(NOT SOMETHING THEY DO)**

**-NOW, A SCAM SO SHOCKING, YOU NEVER WOULD EXPECT IT!!**

**-THIS IS A WARNING… ****REMEMBER TO GET YOUR CARD BACK… FROM ANYONE!**

-THIS NEXT VICTIM WENT TO THE LAPD DETENTION CENTER TO HELP OUT A RELATIVE

-SHE HANDED HER DEBIT CARD TO THE OFFICER AND THEN A FEW DAYS LATER, SHE REALIZED SOMETHING SHOCKING… HER DEBIT CARD WAS MISSING

-AFTER SOME FRAUDULENT CHARGES WERE MADE SHE CONTACTED CITIBANK WHO WOULDN’T HELP… THEY TOLD HER TO CONTACT THE POLICE

-SHE TRIED CONTACTING THE LAPD A DOZEN TIMES AND GOT NOWHERE

-SO SHE DECIDED TO TAKE MATTERS INTO HER OWN HANDS

-YOU WON’T BELIEVE WHAT SHE FOUND!!!

-JUST GOES TO SHOW THERE ARE THIEVES EVERYWHERE!

**(((PLAY CLIP 5 HORIZONTAL)))**

**OUT: ****(JUSTICE IS GOING TO BE SERVED)**

**HERE’S HOW TO PROTECT YOURSELF**

-IF YOUR DEBIT CARD WON'T GO INTO THE ATM, DON'T ASSUME THE MACHINE IS BROKEN. 

-USE ANOTHER ATM OR GO INSIDE THE BANK.

NEVER ACCEPT HELP FROM A STRANGER AT AN ATM, ESPECIALLY IF THEY TELL YOU TO TAP YOUR CARD OR ENTER YOUR PIN.

-ALWAYS SHIELD YOUR PIN AND MAKE SURE YOUR ATM SESSION HAS COMPLETELY ENDED BEFORE WALKING AWAY.

-YOUR BANK WILL NEVER SEND SOMEONE TO YOUR HOME TO COLLECT OR DESTROY YOUR DEBIT CARD.

-IF SOMEONE CLAIMS THEY'RE FROM YOUR BANK, CLOSE THE DOOR AND CALL YOUR BANK USING THE NUMBER ON THE BACK OF YOUR CARD.

-NEVER HAND YOUR DEBIT CARD TO ANYONE WHO SHOWS UP AT YOUR HOUSE.

-NEVER LEAVE YOUR DEBIT CARD IN YOUR MAILBOX OR GIVE IT TO A COURIER BECAUSE SOMEONE CALLED YOU.

-NEVER WALK AWAY FROM A CASHIER, RESTAURANT, OR DRIVE THRU WITHOUT CONFIRMING YOUR DEBIT CARD HAS BEEN RETURNED.

-MAKE IT A HABIT TO SAY, "I NEED MY CARD BACK," BEFORE YOU LEAVE.

-TURN ON INSTANT TRANSACTION ALERTS SO YOU'LL KNOW IMMEDIATELY IF SOMEONE USES YOUR CARD.

**(((OMNIWATCH SPONSOR -   KILL BANNERS)))**

**I’M ALWAYS LOOKING FOR WAYS TO PROTECT YOU FROM SCAMS…**

-OUR SPONSOR TODAY DOES JUST THAT. 

-HERE’S HOW TO GET A FREE ACCOUNT SCAN RIGHT NOW AND GET EVEN MORE PROTECTION.

**((((PLAY OMNIWATCH SPONSOR))))**
```

## Middle story — `F2 BIBLE 07/10`

441 words, 25 bullets, 3 clip beats, 3 pages.

```
**THE NEW GOLD RUSH SCAM!**

-WE'VE WARNED YOU ABOUT GIFT CARD SCAMS… WIRE TRANSFER SCAMS… AND CRYPTO SCAMS

-BUT NOW THERE'S A NEW SCAM THAT MAY BE THE MOST BRAZEN YET.

-CRIMINALS AREN'T ASKING FOR CASH… THEY'RE TELLING YOU TO BUY GOLD BARS OR COINS… AND THEN HAND THEM TO A STRANGER WHO SHOWS UP AT YOUR FRONT DOOR.

-THIS IS CALLED THE GOLD COURIER SCAM.

-AND IT HAS ALREADY COST AMERICANS MORE THAN **262 MILLION DOLLARS.**

-THE F-B-I SAYS LOSSES ARE EXPLODING... ESPECIALLY AMONG OLDER AMERICANS

-THE SCAM STARTS WITH A POP UP… OR AN EMAIL… OR PHONE CALL

-SAYING YOUR BANK ACCOUNT… YOUR RETIREMENT SAVINGS OR EVEN YOUR COMPUTER, HAS BEEN COMPROMISED

-THEY CLAIM TO BE FROM YOUR BANK… THE FBI… THE TREASURY DEPARTMENT

-THEY TELL YOUR MONEY ISN’T SAFE, BUT HERE’S HOW YOU CAN PROTECT IT…. WITHDRAW IT… BUY REAL GOLD FROM A LEGITIMATE DEALER

-THEN A GOVERNMENT COURIER WILL BE BY TO PICK IT UP… AND WALK AWAY WITH YOUR LIFE SAVINGS

**(((PLAY CLIP 6 HORIZONTAL)))**

**OUT: (OUT OF THERE IN A MONTH)**

**YOU HEAR THE WORDS, CONVERT CASH TO GOLD FROM ANYBODY… RUN!**

-I HATE SCAMMERS, BUT I LOVE IT WHEN THEY GET BUSTED

-MANY OF THESE TYPES OF CRIME START OVERSEAS, BUT THEY NEED A LOCAL TO DO THEIR DIRTY WORK… AND THAT DOES NOT MAKE THEM INNOCENT!

-WATCH WHAT HAPPENS WHEN POLICE CATCH UP TO A PAIR OF SCAMMERS HIRED TO COLLECT

**(((PLAY CLIP 7 HORIZONTAL)))**

**OUT: (MONEY LAUNDERING CHARGES)**

**THIS NEXT VICTIM WAS SCAMMED OUT OF $700,000!!**

-A 79 YEAR OLD WIDOW WAS TARGETED AND BELIEVED WHAT SCAMMERS WERE TELLING HER

-THAT HER SOCIAL SECURITY FUNDS WERE BEING USED TO SUPPORT TERRORISM AND IN ORDER TO FIX IT, SHE HAD TO WITHDRAW IT AND BUY GOLD COINS

-BUT THANKS TO AN ALERT STORE OWNER, AND LOCAL POLICE, THE SCAMMER NEVER GOT HIS HANDS ON THAT $700,000!

-BUT HE DID GET A “SWEET SURPRISE” INSTEAD

**(((PLAY CLIP 8 HORIZONTAL)))**

**OUT: (WE’RE SCAMMING THE SCAMMERS)**

**HERE’S HOW TO PROTECT YOURSELF**

-STOP THE MOMENT ANYONE TELLS YOU TO "MOVE" YOUR MONEY TO KEEP IT SAFE.

-NEVER BUY GOLD, SILVER, CRYPTOCURRENCY, OR GIFT CARDS BECAUSE SOMEONE ON THE PHONE TELLS YOU TO.

-HANG UP AND CALL YOUR BANK USING THE NUMBER ON THE BACK OF YOUR CARD.

-IF SOMEONE CLAIMS TO BE FROM THE F-B-I, TREASURY, OR LOCAL POLICE… CALL THE AGENCY DIRECTLY USING A PUBLICLY LISTED NUMBER.

-IF A STRANGER SHOWS UP TO COLLECT GOLD, CASH, OR VALUABLES… DO NOT OPEN THE DOOR.

-CALL 911 IMMEDIATELY.

-AND IF YOU THINK YOU'VE BEEN TARGETED… REPORT IT TO THE F-B-I'S INTERNET CRIME COMPLAINT CENTER AS SOON AS POSSIBLE.
```
