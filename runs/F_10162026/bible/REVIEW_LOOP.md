# Review loop — 10/16 F1 bible

## Round 1 (reviewer agent, blocker-only)
- BLOCKER (CONTRADICTED): "-ONE FRIDGE ISN'T MUCH. ADD UP EVERY GADGET ON YOUR BLOCK… AND IT'S A **DATA CENTER**!!"
  → "-ONE FRIDGE ISN'T MUCH. BUT EVERY GADGET ON YOUR BLOCK… IN YOUR WHOLE TOWN?" / "-THAT'S A **BIG NETWORK** FOR IT TO LIVE IN!!"
  Sources: ABC 2yvhtqQ7bBk 1:11–1:31 ("not enough to replace a data center… quite a big network for this thing to play around in"); Anthropic (2M+ TV boxes ≈ 40 H100s, "a tiny amount of compute").
- Dropped as house format: mechanical "no URL on cue" ×2 (source line sits under OUT:).

## Round 2
Only the changed line: string-matched against the ABC transcript by the writer; no new figure. Not re-run through the agent. `check_bible.py` clean.

## Still blocking
None.

## Passed to the producer (9 WARNINGs, 8 NOTEs), not fixed
W1 Out points 1–2 s early vs captions (0:19→~0:20, 1:30→~1:31, 5:10→~5:11); cut on the words.
W2 Clip 1 BUTT drops ABC reporter's "This is not like taking over people's personal devices" (0:31–0:38).
W3 Gates setup "the real danger" vs his "years away" line.
W4 Clip 2 opens mid-question (end of Tapper's bioterror question).
W5 "Unplug one gadget… can infect it again" vs later "unplug it" advice. Suggested: "PLUG IT BACK IN… AND THE ONE NEXT TO IT CAN INFECT IT AGAIN."
W6 "Two things to change tonight" promise vs a five-step list.
W7 "…AND IT HAS NO WAY IN!!" is absolute (pre-infected boxes, phishing). Suggested: "AND YOU MAKE IT A LOT HARDER TO GET IN."
W8 "There it is on the screen" for IC3.GOV with no on-screen cue.
W9 "ONE AI COPIED ITSELF TO EVERY MACHINE": it set up a smaller model (Llama 3.1-8B) on 8/8 nodes in 4 of 5 trials, run from a separate server.
N1 Mechanical URL blockers dropped. N2 Clip 1 BUTT starts mid-sentence at 0:53. N3 Anthropic/Claude disclosure on air? N4 Australia portal was a statistics service; "no patient records" is OpenAI's and officials' word. N5 Lon intro partially confirmed; sponsor ties open. N6 "No hacker needed" (tease) — Guan: no hacking in the test. N7 "Cyber attacks are coming in the next year" slightly overstates Gates' "probably… most dramatically." N8 Neither clip visually confirmed.
