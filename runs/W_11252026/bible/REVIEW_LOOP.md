# Review loop: F2 Wed 11/25 (draft_v3 → draft_v4)

## Round 1: fresh reviewer agent (rossen-bible-final-reviewer, BLOCKER-only) on draft_v3

**BLOCKERs (2, both errors in the director's research packet):**

1. **San Jose arrests.** The JEFF note said no one was caught. NBC Bay Area's update (Aug 24, 2026) says "San Jose police on Monday confirmed arrests have been made in connection to the case." The Aug 26 story covers three people detained over strong-armed jewelry robberies on the same Almaden Expressway block. The director re-checked both pages.
   - Before: "Police hadn't answered when this aired… Don't say anyone was caught."
   - After: "San Jose police confirmed arrests in this case… arrested, not charged or convicted. Attribute it."
   - The spoken copy is unchanged.
2. **Renton pleas.** Only two pleaded not guilty; one has a bench warrant; no plea is reported for the fourth (FOX 13, captions 3:51-4:07 and 4:59-5:05).
   - Before: "THE GROUP IS ACCUSED. THEY'VE PLEADED NOT GUILTY."
   - After: "THE GROUP IS CHARGED… NOT CONVICTED."
   - The JEFF note is corrected to match. Prosecutors charged all the suspects, per the captions at 3:44.

**Reviewer warnings the director fixed, because they are facts and not taste:**

3. **Lynnwood status.** The couple was booked on suspicion; no formal charges are reported.
   - Before: "THEY'RE CHARGED… NOT CONVICTED."
   - After: "POLICE ARRESTED BOTH… BUT NOBODY'S BEEN CONVICTED."
   - The JEFF note is corrected.
4. **Timecodes against the captions:**
   - Open package: 1:21-1:28.
   - Clip 1, segment 2: in at 1:15.
   - Clip 2: out at 3:44.
   - Clip 3: out 1 at 5:48, now marked "cut before the first name"; out 2 at 6:00.
   - Clip 5: out 2 at 1:04.
   - Clip 7: 0:46-1:42.

## Round 2: the director checked the changed lines against the sources

Every change in the v3 → v4 diff matches its source. `check_bible.py` reports 0 errors and 7 warnings, all expected. `verify_format.py` confirms the house format. Stopped here.

## Still blocking

None.

## Passed through to the producer (WARNINGs and NOTEs, not fixed)

1. The sponsor block follows a clip run with no takeaway beat before it (mechanical).
2. Line 170 joins "$1,500" and "within 30 minutes". Police say the cards were used within 30 minutes; the $1,500 Fred Meyer spend isn't separately timed.
3. "HER PHONE WARNED HER" sits beside "not every GPS tracker". It's her account, and true for her.
4. "HERE'S THE WARNING GOING OUT IN UTAH": nobody has watched clip 6. It may be ABC4's 2025 American Fork dent-repair warning, a related scam rather than hers.
5. "Get in, shut the door, lock it" and "let it go" have no police source (UNVERIFIED). Culpeper's advice backs only the car-won't-start line.
6. "A SHERIFF IS WARNING": the warning is from Aug 2025, so the present tense makes it sound current.
7. Line 74: the three rings and the Tuskegee Airman are said in the runway, then again in clip 2.
8. "TESLA PARKED NEARBY": the source says only "from a Tesla."
9. Tease: "HIS GOLD CHAIN VANISHES" is the couple's account, stated as fact.
10. Clips 4 and 7 use site links. The YouTube search was blocked, so no YouTube copy could be re-checked.
11. No clip has been visually confirmed.
