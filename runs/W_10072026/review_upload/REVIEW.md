# 10/07 LIVE BIBLE — FINAL REVIEW (uploaded draft)

**What was reviewed:** the uploaded `10_07_LIVE_BIBLE_ClaudeCode_opus5.5_medium.docx`, saved here as `10_07 LIVE BIBLE (uploaded, opus5.5 medium).docx` and converted to `draft.md` in this folder, one paragraph per line. It is **not** the bible in `runs/W_10072026/draft.md`. It has different copy, 6 clips instead of 14, a guest (Jim Stickley) and a second sponsor (Chapter). Every clip cue was checked against `runs/W_10072026/outline.md`, the approved Stage: videos manifest.

**Stage:** the clip manifest is locked (the outline is approved at Stage: videos). Every cue carries its URL as a hyperlink on its `((URL: …))` line. The mechanical pass reads plain text and reported "no URL" on all 6 cues. That is a conversion artifact, and it is overruled in the tables below.

**Source list supplied:** yes. The run's `SOURCE_LOG.md`, the pre-bible pages and the outline Gaps were used first, and everything else was searched. `mechanical_pass.py` has no `--outline` flag, so it ran without one; the outline cross-check below was done by hand. The ERRORs from `check_bible.py` were imported, not re-derived.

**Fact-check coverage:** 44 of 50 claims were fully searched. 6 Tier 3/4 items are logged UNVERIFIED because the budget ran out: the social and phone settings paths and two background framings.

**VERDICT: NOT READY.** There are 5 BLOCKERs, and one of them is a fabricated-sounding attribution.

## Fastest path to READY

These are one-line edits and clear four of the five BLOCKERs:

1. **#1:** change `A NEW REPORT SHOWS THAT 15 PEOPLE WHO WERE JAILED…` to `THE POLICING PROJECT COUNTS AT LEAST 16 PEOPLE WRONGLY ARRESTED BECAUSE OF A FACE-RECOGNITION MATCH. 16.`
2. **#2:** change `LAST SUMMER, US MARSHALS SHOWED UP…` to `IN JULY OF LAST YEAR, US MARSHALS SHOWED UP…`.
3. **#3:** cut `THIS IS FROM A LEAKED INTERNAL MCDONALD'S TRAINING DOCUMENT` and the two quoted greetings, or produce the document. The public version is McDonald's own 9/23 announcement.
4. **Typos Jeff will read cold (#21, #22):**
    - Tease: `TO FINDING YOUR FACE` → `TO FIND YOUR FACE`.
    - Tease: `A COLORADO MOM` → `A DENVER WOMAN`.
5. **Hedge fixes (#16–#18):**
    - Starbucks: `SCRAPPED` → `PULLED BACK ON`.
    - Burger King: `SAY THEY'RE MAKING IT EASIER` → `SAY THEY'RE WORKING ON AN EASIER WAY`.
    - Portillo's: `NOW HAS` → `HAS LONG HAD`.
6. **#19:** Facebook path: add the `"AUDIENCE AND VISIBILITY"` step.
7. **#12:** rename the clip 2 label so "FLOCK" isn't on the prompter.
8. **#6:** move each `OUT:` line directly under its marker (6 cues).

These need a ruling or new writing, not a pass edit:

9. **#4:** clip 3 (CNET beacons) isn't in the approved outline. Either cut it, which leaves a 2-line runway to rewrite, or run it through the pipeline for a Videos row and timecodes.
10. **#5:** C has no protection beat. The outline's C4 "Get a person" fix was dropped. This is writing, so it goes to `rossen-script-writer`.
11. **#8:** outline drift. 9 of 14 approved clips are gone, including all of Isaacs and the Google Timeline fix that the A title promises. A guest was also added. This needs a producer ruling (#8–#10).
12. **#13:** the Clearview removal room note is missing.

## BLOCKERs

| # | Story / section | Issue | Confidence | Source | Scope |
|---|---|---|---|---|---|
| 1 | A / hook | "A NEW REPORT SHOWS THAT 15 PEOPLE WHO WERE JAILED ON FACE-RECOGNITION MISTAKES ALONE. 15." Wrong count, wrong verb, and it isn't a report. The line is also ungrammatical. | CONTRADICTED | [Fox News, 9/28](https://www.foxnews.com/us/grandmother-sues-alleged-ai-facial-recognition-error-led-months-jail-experts-sound-alarm) | Clare Garvie, Policing Project: "at least 16 known instances" of wrongful **arrest** on a face match, nationwide, to date. The count covers face recognition only. |
| 2 | A / Lipps | "LAST SUMMER, US MARSHALS SHOWED UP AT HER HOUSE." | CONTRADICTED | Fox News, 9/28; WCYB transcript | The arrest was July 2025. On a 10/7/2026 air date, "last summer" means summer 2026. |
| 3 | C / McDonald's | "THIS IS FROM A LEAKED INTERNAL MCDONALD'S TRAINING DOCUMENT… 'ENJOY YOUR MEAL!' AND 'SEE YOU SOON!'" No leak is reported anywhere. Make It Golden was announced publicly. | UNVERIFIED | — | — |
| 4 | B / clip 3 | The CNET "Next Big Thing – Beacons" clip isn't in the approved outline. It has no Videos row, no in/out, no outcue, no transcript and no grade. Its runway is 2 lines (check_bible). With the manifest locked, an unvetted clip can't be shot. | | | |
| 5 | C / structure | C runs clip 6 and the Starbucks beat, then ends with no protection beat (mechanical pass). The outline's C4 fix is gone: walk in and order at the counter, ask for a person at the speaker, check the screen and the bag. | | | |

BLOCKER 3 is the highest-risk item in the draft. It puts invented quotes on a named company as a "leak." It is a one-line cut.

## WARNINGS

| # | Story / section | Issue |
|---|---|---|
| 6 | All cues | Imported from check_bible: `OUT:` isn't directly beneath the marker on any of the 6 cues. On clips 1, 2 and 5 it comes after the URL and timecode lines; on clips 3, 4 and 6 it comes after the URL line. The extractor and `verify_format.py` both require `OUT:` directly under the marker. |
| 7 | B / clip 3 runway | 2 lines, against the 6-line minimum (check_bible). This goes away if #4 is cut. |
| 8 | Whole show / outline drift | **Cut from the approved outline:**<br>• A2 and A3, the WCYB clips.<br>• A5 and A6, all of Lindsey Isaacs.<br>• A8 and A9, Elser's car and the chief's email.<br>• A10, the Google Timeline demo that is A's title payoff ("your phone may be deleting the proof").<br>• B3, the NBC CT plate cameras.<br>• C2, Burger King.<br>• C3, Ecomix.<br>**Added:**<br>• CNET clip 3.<br>• An expert segment.<br>• Walmart and Macy's beacon copy.<br>• Portillo's and Starbucks.<br>Which draft goes forward is the producer's call. |
| 9 | Guest | Jim Stickley is in the tease and runs an expert segment. The outline says "Guest: none." Confirm he's booked. "MORE THAN 30 YEARS" is PARTIALLY CONFIRMED: his own bios say 20+, 25+ and 30+ years in different places. CEO of Stickley on Security is confirmed. |
| 10 | Sponsor | The second break is Chapter; the outline has OmniWatch at both breaks. Confirm the sponsor order. Placement itself is fine: after A, and after B, each with a tease. |
| 11 | B / Target | Target is off-limits as a subject (facts-to-get-right). The 9/29 ruling kept the basket clip "but don't lean on the brand." The draft names Target about 9 times, including "TARGET'S OWN PRIVACY POLICY SAYS IT SELLS YOUR DATA." That claim is true per the policy, but it makes Target the story. Say "a big store chain" and keep Walmart as the named policy. |
| 12 | A / clip 2 label | The prompter line reads `…OFFICER WHO USED FLOCK CAMERAS`. The room rule is no "Flock" by name. Rename it `9NEWS — DENVER WOMAN WRONGLY ACCUSED OF PACKAGE THEFT`. Also check the clip audio, which may name the company. |
| 13 | A / protection | The room note asked for Clearview data removal: clearview.ai/privacy-and-requests, 13 state portals, and whether more states are coming (Oklahoma's law takes effect 1/1/2027). It isn't in the draft. The social-media-private note is covered by tips 2 and 3. |
| 14 | A / Lipps | "MORE THAN A THOUSAND MILES FROM HOME." She spent 108 days of it in a **Tennessee** jail before extradition (Fox). Cut the clause. |
| 15 | A / Lipps | "NEARLY 6 MONTHS." July 2025 to Dec 24, 2025 is about 5–5½ months, and CBS says "months." PARTIALLY CONFIRMED. This is the same open producer decision as on the run's own bible (108 days vs. nearly six months). |
| 16 | C / Starbucks | "HIGH-TECH DRINK MACHINES IN ABOUT 10,000 STORES… THEN IT SCRAPPED THE PLAN." That was April 2025, about 18 months before air. Niccol said Siren "just not something that we need to be rolling out across all 10,000 stores" and kept it for the busiest stores. "Scrapped" overreaches. Say "pulled back," and date it ("LAST YEAR"). |
| 17 | C / Burger King | "THEY SAY THEY'RE MAKING IT EASIER…" Burger King is **developing** a way to reach a human, and voice AI is still in about 1,500 drive-thrus (Restaurant Business, NRN, 9/23–24). The pre-bible's rule: "backing off forcing the bot," not "ditching it." |
| 18 | C / Portillo's | "NOW HAS WORKERS OUTSIDE…" Portillo's has used outside order-takers for years (QSR). Presenting it as a new turn is wrong. |
| 19 | A / protection | The Facebook path skips a step. The current path is Settings & privacy → Settings → **Audience and visibility** → Posts → Limit past posts. Jeff reads the path aloud, so a missing step leaves viewers stuck. |
| 20 | A / company response | There's no response line. The city of Fargo "does not comment on pending litigation" (ABC). Its then-chief said "errors were made" and apologized (MPR). The Columbine Valley officer faces discipline (Colorado Sun). One line would cover it. |
| 21 | Tease / body | Caps typos Jeff will read cold: `…MAKE IT HARDER FOR AI TO FINDING YOUR FACE`, and the broken `A NEW REPORT SHOWS THAT 15 PEOPLE WHO WERE JAILED` (see #1). `BLUE TOOTH` is Target's own spelling inside the quote. Fine as written, but Jeff will read it cold. |
| 22 | Tease | "A COLORADO MOM." Nothing loaded says Elser is a mother; sources call her a Denver woman and a financial advisor. UNVERIFIED. Say "A DENVER WOMAN." |

## NOTES

| # | Story / section | Issue |
|---|---|---|
| 23 | All cues | Numbered, not `XXX`. check_bible logs these as 6 ERRORs. Numbered cue blocks are this week's requested house form, so it isn't a defect here. |
| 24 | All cues | None was visually confirmed. Clips 1, 2 and 5 are consistent with their outline rows and caption transcripts. Clips 4 and 6 have no transcript (MANUAL, per outline). Clip 3 has title metadata only. |
| 25 | B / clip 5 | The marker says `VERTICAL BROLL` (picture only), but the cue carries sound-up outcues plus a DECIDE on sound up vs. mute. If sound up wins, drop `BROLL`. The line after the clip ("THAT'S INSTACART PITCHING THE STORES…") only lands with audio. |
| 26 | C / clip 6 | The outline said to call C1 later (McDonald's Jan 2023 vs. Taco Bell Jul 2025). The draft picked McDonald's without flagging it. |
| 27 | Length | 1,662 spoken body words (band 1,700–2,300). Tease 274. 6 clips, which is about two per segment. |
| 28 | A / structure | The header "BUT THIS NEXT ONE IS EVEN SCARIER… BECAUSE IT'S ON HER OWN DOORBELL!!" is followed by a 5-line guest intro before the doorbell story starts. Move the header below "JIM, WHAT'S GOING ON?" |
| 29 | Expert | There's one Jim question plus a tips handoff. The Ghost Tapping skeleton calls for four numbered expert questions. |
| 30 | A / Lipps | Clearview AI is now confirmed from the suit coverage (Fox, 9/28). That upgrades the run log's open "pull the complaint" item. |

Details and sources for every claim are in `SOURCE_LOG.md`. Inline flags are in `ANNOTATED_BIBLE.md`.
