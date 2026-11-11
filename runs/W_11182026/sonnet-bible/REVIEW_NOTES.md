# Review notes to the writer, verbatim

## Round 1 (on sonnet_draft_v1.md)

Strong draft. The research is careful and the voice is close. Fix these, as moves, in your own words:

1. Spoiler in a header (the AmEx segment). The header tells viewers she got her money back, and then the runway asks whether she ever saw it again. Rewrite the header so it holds the outcome for clip 5; the header should promise the question, not answer it.
2. Same problem, the Texas family's second segment. Both the header and the runway lines (Frontier's refund of the airport flights plus vouchers) give away what clip 8 reveals. Keep the stakes and the missed wedding in the runway, and move the refund/voucher facts after the clip, into the button and the lines that follow.
3. Ambiguous "this woman" opening the AmEx segment. Three women have passed by then (Illinois, Maryland, the Frontier email). Make it an explicit callback to the Illinois woman whose flight he canceled, so viewers know who it is.
4. Unfinished research, the Dallas site name. FOX 4's own headline and article spell it "Fly-n-Fare"; the "Flying Fair" spelling is just auto-captions. Resolve the JEFF note instead of leaving it as a question. Whether Jeff says the name aloud is your call; the non-response, four emails and BBB F lines are right.
5. Attribution drift, stop 1. The "not how airlines work" bite in the WOWT package is unattributed in the transcript, so "a travel advisor says" may name the wrong person. Either attribute it to a travel expert generically or to what the package shows, without guessing a job title.
6. Overclaim, twice: "no trip in the app, you don't have a reservation" (booking-sites segment and protection step two). A third-party site's confirmation code isn't always the airline's own record locator, so a viewer could panic over a real booking. Make the move: look it up in the airline's app, and if it isn't there, call the airline at the saved number before assuming anything.
7. Repetition. The "open the airline's own app" takeaway now lands four or five times before the protection list, and the protection list restates most of them again. Cut the repeats inside the stops so each stop's takeaway is something new (the rental logo, the AI answer, the code, the pre-checked box, the tracker), and let the protection list be the one place they're gathered. Don't trim to hit the word band; trim what's said twice.
8. The Rivlin button. The first bold line after clip 2 answers the question, then bridges to "not just one man," but the next two lines go back to his story (date of birth, charges backed out). Reorder so the forward pull comes last, after his story is closed.
9. Timecodes, from the captions: clip 2 last out lands on "with" at 4:47.9, so out at 4:49; clip 3 out "canceled it" ends about 1:24, so 1:24; clip 5 starts on "After we contacted" at 2:00.4 and "transaction" ends about 2:11, so 2:00 - 2:11; clip 6 out 1:11; clip 7 "unclick a box" ends 0:53.4, so 0:54. Match the OUT lines to the new outs.
10. The sponsor bridge: keep it to the stock bridge only. The skill says sponsor copy is written only if asked, so cue the spot and leave the read to the producer.

Then re-run check_bible.py, save as sonnet_draft_v2.md, update the source log if anything changed, and reply with the checker counts and what you changed.

## Round 2 (on sonnet_draft_v2.md)

All ten round-1 notes landed. The spoilers are gone, the Illinois callback reads clearly, Fly-n-Fare is resolved, and the overclaim is fixed. The bridge question is fine: keep the stock bridge as you have it.

One thing left, and it's the biggest: length. At about 1,800 spoken words, Jeff is reading more than he can riff on, and the room will cut it anyway. This is not about the word band. Do a tightening pass on these moves, with no new facts and no new lines:

1. Inside each stop, cut lines that restate what the clip just said, or what the button just said. Keep the specific (number, place, company) and drop the paraphrase around it.
2. The Points Guy beat runs long for a beat with no clip of its own. Keep the finding, where the numbers sat, and Google's response; drop the connective lines.
3. The AmEx segment: one of its lines is the company's boilerplate about reviewing claims. Keep it only if it carries something the viewer can use.
4. The protection section: the credit-card explanation and the dispute advice now say the same thing in three places (the AmEx segment, the Texas button and the protection list). Keep it once in the stops and once in the list.
5. The pre-sponsor tease and the tease at the top both promise the one rule. That's correct; just make sure nothing else in the pre-sponsor tease repeats the top tease word for word.
6. Aim for every stop to end on one usable takeaway line, not two or three.

Then re-run check_bible.py, save as sonnet_draft_v3.md, update the source log if needed, build both deliverables with build_bible.py and build_source_log.py (titles below), run verify_format.py on the bible, and reply with the checker counts, the spoken body word count and the tease word count.
- Bible: /home/user/Rossen/runs/W_11182026/sonnet-bible/F2 Wed 11_18 -- <Working Title> -- SONNET.docx
- Source log: /home/user/Rossen/runs/W_11182026/sonnet-bible/F2 Wed 11_18 -- <Working Title> -- SONNET -- SOURCE LOG.docx
Pick the working title from Kyle's three title options in the outline. Use the synced skill's scripts.

## Round 3 (final check on sonnet_draft_v3.md; no notes sent, three-round stop)

Checker: 0 errors, 6 warnings (clip count, word band, aphorism candidates, nine outside clips, false name hit on ICELANDAIR, demo placement). 1,586 spoken body words, tease 176 by the checker's count (144 spoken), 13 JEFF notes, 1 RED FLAG line. verify_format: house format confirmed.

Still open (not sent back):
- Texas header "...AND WERE STUCK WITH THE BILL!!" overstates: clip 8 shows them getting some money back (Frontier refunded the airport flights plus vouchers). A header that holds the outcome without asserting the opposite would be safer.
- Lines after the Google demo are a producer cue until the demo is recorded.
- Clip 9 (FOX 5) and clip 1 (WOWT) timed on site copies; clip 4 (TikTok) manual.
- Open decisions in copy: demo lines, clip 9 cut (FOX 5 vs Reid's original), AirTag link. Not in copy: title, demo owner, guest (none booked), the Instagram reel.
