# Worked example: Jeff's notes on the 11/11 F2 ("Burglars Are Planting Cameras in Your Bushes")

Source: Jeff's feedback on the 11/11 Wednesday bible (one long A story: burglary crews hiding cameras in
bushes), relayed by David, Nov 9 2026. The bible is in `runs/W_11112026/bible_v2/` (the producer's
revision: `F2 Wed 11_11 -- BURGLARS ARE PLANTING CAMERAS IN YOUR BUSHES (producer rev 11-04).docx`).
These five notes sit on top of his 11/04 notes (`jeff-notes-2026-11-04.md`) and agree with them. Where
an older rule says otherwise, these win.

## Jeff's five notes

1. **Grab people more at the beginning.**
2. **Make it evergreen.** No holiday stuff, etc.
3. **No "this family" in the tease.** Maybe "you're going to see this family."
4. **Amp up between videos.** Keep amping up: in how we present things, moving the story forward each
   time. "And now it's spreading."
5. **No need for "CBS shows this…"**

## Where the 11/11 bible missed, with the fix

### Note 1 — the top eased in

As written, the first spoken lines were an instruction and a setup:

```
-BEFORE YOU LEAVE HOME FOR THE HOLIDAYS… YOU NEED TO WATCH THIS VIDEO!!
BURGLARS ARE WATCHING YOUR HOUSE… AND THEY KNOW WHEN YOU'RE AWAY
-THIS FAMILY WAS AWAY ON VACATION… AND THEIR OWN CAMERA CAUGHT A BURGLAR CRAWLING ACROSS THE LIVING ROOM.
```

The most arresting thing in the show (a burglar on his hands and knees in a family's living room, and
a camera in the bush across the street that told the crew nobody was home) arrived third, after a
holiday reference. Direction:

```
-A BURGLAR… CRAWLING ACROSS SOMEONE'S LIVING ROOM. AND THE FAMILY WASN'T HOME.
-HE KNEW THEY WERE GONE… BECAUSE A HIDDEN CAMERA WAS WATCHING THEIR FRONT DOOR.
-IF YOU HAVE BUSHES IN FRONT OF YOUR HOUSE… YOU NEED TO WATCH THIS!!
```

The rule: **the first two lines are the most startling moment in the open package, said plainly, and
what it means for you.** The command hook can come third. No warm-up, no date, no "before you…" line
ahead of the picture.

### Note 2 — the copy dated itself

Lines that will age the video, and their direction:

| Written | Problem | Direction |
|---|---|---|
| `BEFORE YOU LEAVE HOME FOR THE HOLIDAYS` | Holiday | `BEFORE YOU LEAVE HOME AGAIN` / `THE NEXT TIME YOU LEAVE HOME` |
| `AND THIS HOLIDAY SEASON, THE CAMERAS ARE BACK` | Holiday, and wrong (the cases were October) | `AND NOW, THE CAMERAS ARE BACK` / `AND NOW IT'S SPREADING` |
| `THIS SPRING, AUTHORITIES IN LOS ANGELES COUNTY ARRESTED SEVEN PEOPLE` | Season | `AUTHORITIES IN LOS ANGELES COUNTY ARRESTED SEVEN PEOPLE` |
| `THIS WAS LAST DECEMBER, IN TEXAS` | Relative date | `IN TEXAS…` (date in a JEFF note) |
| `THIS WAS LAST YEAR, IN LOS ANGELES` | Relative date | `IN LOS ANGELES…` |

The rule: **no holidays, seasons or relative dates (`THIS FALL`, `LAST DECEMBER`, `LAST YEAR`, `THIS
WEEK`) in spoken copy.** A case's date goes in a JEFF note. If leaving the date out would mislead a
viewer about what to do (an old rule that has since changed), say the year (`IN 2024`), never a
relative date. The peg still decides which stories we pick and lives in the outline; the copy doesn't
carry it. This replaces the outline's old `⚠️ date it on air: LAST YEAR / LAST FALL` instruction.

### Note 3 — "this family" in the tease

```
-THIS FAMILY WAS AWAY ON VACATION… AND THEIR OWN CAMERA CAUGHT A BURGLAR…
```

In the tease nobody is on screen yet, so `THIS` points at nothing. Direction:

```
-YOU'RE GOING TO SEE THIS FAMILY'S OWN CAMERA… CATCH A BURGLAR CRAWLING ACROSS THEIR LIVING ROOM.
-YOU'LL MEET A NEIGHBOR WHO SPOTTED THE CREW'S CAMERA… AND WHAT POLICE DID NEXT IS BRILLIANT.
```

The rule: **the tease introduces people as what the viewer is about to see or meet** (`YOU'RE GOING TO
SEE`, `YOU'LL MEET`, `WAIT UNTIL YOU SEE`). `THIS WOMAN` / `THIS FAMILY` is for the body, over the
video. It still follows 11/04: no names, and the person stays generic.

### Note 4 — the energy dipped between clips

The 11/11 bridges mostly moved forward (`AND THIS FALL, THE CAMERAS ARE BACK`, `AND ONCE THAT CAMERA IS
IN… THESE CREWS DON'T WAIT LONG`, `AND SOME CREWS DON'T EVEN HIDE. THEY KNOCK`), but several clips
were introduced flat, on place and date (`THIS WAS LAST YEAR, IN LOS ANGELES`, `THIS WAS LAST DECEMBER,
IN TEXAS`). Each new clip has to arrive as **the next, bigger thing**:

| Flat | Amped |
|---|---|
| `THIS WAS LAST YEAR, IN LOS ANGELES.` | `AND NOW IT'S SPREADING… IN LOS ANGELES, THEY DIDN'T EVEN WAIT A DAY.` |
| `IT'S CALLED A JAMMER.` | `BUT IT GETS WORSE. THEY CAN TURN YOUR OWN CAMERA AGAINST YOU.` |
| `THIS MAN WASN'T HOME AND HIS DOORBELL CAMERA CAUGHT A WOMAN KNOCKING.` | `AND NOW THEY'RE NOT EVEN HIDING. THEY WALK RIGHT UP TO YOUR DOOR.` |

The rule: **the line that brings in each clip after the first escalates**: scope (`AND NOW IT'S
SPREADING`), speed (`THEY DIDN'T EVEN WAIT A DAY`), closeness (`RIGHT UP TO YOUR DOOR`) or severity
(`BUT IT GETS WORSE`). Pick an axis from the outline's Climb line and climb it out loud. Place and date
are never the opener for a new clip.

### Note 5 — "Here's CBS Boston"

The 10/21 rule had Jeff name each outlet once, in its clip's lead-in, for fair use (`-HERE'S CBS
BOSTON. WATCH THIS.`). Jeff doesn't want it. **No outlet in any spoken line**, lead-ins included. The
lead-in is the moment (`-WATCH WHAT HAPPENS WHEN THEY COME BACK.`); the outlet stays in the red source
line, and the edit credits it on screen. Agencies, police departments, courts and companies are still
named.

## Checker

`check_bible.py` warns on all four mechanical notes: dated lines (holidays, seasons, relative dates),
`THIS FAMILY` / `THIS WOMAN` in the tease, a stretch between two clips with no escalator, and any outlet
named in spoken copy. Note 1 (grab them at the top) is judgment: the reviewer reads the first three
spoken lines against the open package.
