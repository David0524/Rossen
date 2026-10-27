# The quality gate

Every story on the weekly slate passes this gate before the user sees it. Added
Oct 25, 2026. The thresholds are a first guess and are tuned from the user's
"good enough to pitch / not good enough" verdicts (`calibration-log.md`). When
the log disagrees with this file, the log's latest adjustment wins.

Quality beats count: **never pad the slate with a story that fails.** If fewer
than ten pass after the full search, deliver the ones that passed, say how many
fell short, and list what would get the near-misses over the line.

## Hard gates (all must pass)

| Gate | Passes when |
|---|---|
| **H1 Villain and target** | Someone is doing it to the viewer (a scammer, a thief, a company), and a 55+ viewer is the target, not a spectator. **Not niche:** if the viewer has to be going through a specific life event to be the target (a recent death, a move, a hospital stay), it fails. (Round 1: the funeral story was "too niche… unless they had a recent death.") |
| **H2 Happening now** | At least one dated source you opened, from the last 12 months, shows it is still hitting people. |
| **H3 A real case** | At least one documented victim or loss (a dollar figure or concrete harm) from a named outlet, court or agency. |
| **H4 Fresh for us** | Not covered, judged against **fresh** coverage data (Step 0 item 5: shows aired *and* filmed-but-not-aired since the newest transcript). The same scam that had a segment (ten or more transcript hits) in the last **six months** is covered, even with new cases. Not on the dead list, not off the list (refunds, payouts), not pitched to Jeff and passed without a new angle. (Round 1: three of eight stories were already done or filmed.) Search by **mechanism, not wording**: run at least five phrasings of the scam (for an account opened in your name: "in your name", "opened an account", "identity theft", "your address", "welcome letter"), then read the matching passages. (Oct 26: the Aug 12 show covered accounts opened in your name with different words, and an exact-phrase search missed it.) |
| **H5 One-line advice** | The protective move fits in one sentence. |
| **H6 A clip exists** | At least one video package **on this specific scam** (local news, network or consumer creator) with views and approximate upload date recorded. No exceptions: a demo or screen-share plan does not replace a clip. (Round 1: "Clips are super important.") |

A story that fails a gate goes on the **cut list** with the gate it failed. The
cut list is part of the deliverable: it shows the search was wide and lets the
user overrule a cut.

## Score (0–2 each, 14 total)

| | 2 | 1 | 0 |
|---|---|---|---|
| **Fear beat** | Threatens something used every day, and the extended threat is stated | A real threat, but abstract or one step removed | Wallet or curiosity only |
| **Heat** | A clip on the theme over 500K, or local news over 200K | Over 50K | Under 50K or none |
| **Track record** | Theme lift 1.5× or better (`performance-map.md`) | 0.9× to 1.5×, or new territory | Under 0.9× |
| **Breadth** | Three or more cases or variations | Two | One |
| **Peg** | A dated event in the last three weeks, or a strong tie to the airdate's season | Proof it's still happening (rung 3), or a loose seasonal tie | None |
| **Newness** | Never a segment on our channel | A returning theme with a new angle | Close to something recent |
| **Producibility** | Clips plus an obvious expert or demo | One of the two | Neither |

- **Pitch** at **9 or more, and Heat of at least 1** (a clip over 50K on the scam itself).
- **A-caliber** at **10 or more with a Fear beat of 2.** The weekly slate should
  be mostly A-caliber; a story under that is labelled `B/C only`.
- Show the score on every card as the seven numbers, so the user can see why.
- **Tie-break (soft, from round 1):** at equal scores, prefer a scam or con the viewer can be tricked into over street theft ("I don't love these blue collar crime ones but it's okay"). Street-theft stories still pitch; they just don't lead the slate. Revisit after round 2.

## The lead test (for anything recommended as F1 lead or F2 A)

A story that passes the gate is good enough to pitch. To be *recommended* as a
lead it must also pass at least two of these three (round 2: "fine, but I want to
be blown away"):

1. **Proven right now.** 1M+ combined views on audience-matched channels in the
   last 75 days (`scripts/channel_heat.py`).
2. **Stop-and-check.** The viewer can check something on their own phone, card,
   car, house or mailbox the moment they hear it ("is my house paid off?", "is
   this setting on?"). The channel's biggest overperformers all do this.
3. **Six-word title.** It fits the channel's title pattern without a clause of
   explanation (`producer-kit/titles.md`).

If nothing on the slate passes the lead test, say so on top: "nothing here is a
blow-away lead" is a finding, not a failure.

## Asking for the verdict

End the Step 1 reply by asking the user to mark each story **Pitch** or **Don't
pitch**, with a word on why for any "Don't." Log every verdict in
`calibration-log.md` (or, when the skill folder is read-only, give the user the
log lines to add). After two rounds, compare verdicts to scores: if the user
rejects stories that scored 9 or more, find the shared reason and turn it into a
gate or a weight change; if they accept stories you cut, loosen that gate.
