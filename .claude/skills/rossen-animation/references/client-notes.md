# What the client said, and what fixed it

The general notes from earlier films (readability, pacing, sync, legibility, centring) are in `craft.md` §0 and §9. This
file collects the notes from the tease rounds. Each row is a real note from a review round (Friday tease, Wednesday car-scams
tease); most apply to every film type. Check your plan and your contact sheet
against every row before showing anything.

| the note | the cause | the fix (now a rule) |
|---|---|---|
| "The opening scene is crowded. You can push the car to the right even if it is out of the social media borders." | Four figures and a car squeezed inside the safe box | Scenery may run off the frame edges; only text and key action must stay in the safe zone. Stage wide sets bigger than the frame. |
| "I have no clue what that first graphic is at 0:23" | A bare oil can pinned on Jeff's board, out of context | Recap props must be recognizable at a glance: show each story as a small picture of its key moment (a pinned photo), not an isolated object. |
| "The license plate doesn't look enough like a license plate." | A plain rectangle with text | Draw real cues: a 2:1 plate, a holder, a stamped rim, bolts, a blank sticker, embossed characters (no real state design). Key props must read as what they are. |
| "Let the end card loop one more time." | The loop played once | Every tease ends on its loop ×2 (CLAUDE.md). |
| "Make a 1–2 s intro card: title the video, Rossen's logo. The start is abrupt." | The film opened cold | Every video opens on a title card (CLAUDE.md), a pickup of whole beats before bar 0. |
| "That first transition is a little jarring. Slow it down / make it a fade." | The card vanished, then a 0.2 s push | The title card holds still, fades its words over ~0.2 s, and the first scene dissolves in over one beat (with a gentle dive), finishing as the first card lands. |
| "The end card says LIVE ON YOUTUBE. Change that to the YouTube, Instagram, Facebook logos." | A text chip | The loops' LIVE ON row shows the platform logos, drawn from their files untouched, after the print finish. |
| "I don't love how the street/pavement looks. The dotted scenes can get overwhelming." | Dots on the sky and on the ground | One dotted field per scene at most: light dots in the sky, flat drawn ground (a kerb, slab joints); close-ups on textured cream. |
| "Did you cut the frames per second?" / "Everything feels very laggy." | Puppets on twos (12 drawings/s) | Everything on ones (24 fps). Never on twos. |
| "The car in the intro drives in backwards." | The car faces left but entered from the left | A vehicle enters nose first: it comes in from the side it faces away from. Check the direction of every mover on a strip. |
| (Found in critique) the jaw drop was hidden behind the cash | The occluder left one beat after the reaction | A reaction must be visible when it happens: clear anything in front of a face before the face acts. Check reactions on a strip. |
| "Jeff asked for his logo to appear in the corner throughout the video… except on the intro and outro cards." | — | `logoBug()` top-left, tight in the corner at (40, 48) (first placed at y 300: "why is it so far from the top"), official logo untouched and opaque, from the first scene to the outro. |
| "Their opens already act as title card" (series) / keep the rules FOLLOW FOR ending | — | Series episodes need no extra title card; their recurring parts stay as approved. |
| (Standing direction) text hard to read | Tilted, bouncing, fast cards | Cards level, from 1.05× at most, dead still, 70–76 px, read-twice time, no camera drift under them (craft.md §0). |

## The acting pass that made it feel alive (keep it)

- Breathing on every character (±1.2 %, each on its own phase).
- Heads trail a landing (`lag()`), then settle.
- A face swap is a squint (2–3 frames), then the new face with a take that overshoots and settles.
- Things that stop overshoot a touch and settle (the parked car rocks on its springs, a puff of exhaust).
- A character who reacts turns toward the cause first ("lead the eye"), then reacts.

## Cards that worked (Wednesday)

SELLING YOUR CAR? · WHILE YOU'RE / DISTRACTED... · YOUR CAR: / WORTHLESS · BUYING A CAR / ONLINE? · THE DEALERSHIP / ISN'T REAL ·
THE CAR / DOESN'T EXIST · $3,000 / IN TICKETS · IT'S NOT / YOUR CAR · SOMEONE COPIED / YOUR PLATE · WE'LL SHOW YOU / THE RED FLAGS.

Pattern: a question to open, then the turn of each story in two short lines, a dollar figure where there is one, and the
promise last (level, two bars).

## Lessons the client picked from the outside references (2026-09-28)
The client noted REFERENCES.md lessons 11, 13, 14 and 15 and saw the 5 s demo (`intro/style-demo.js`,
`out/rossen-style-demo/rossen-style-demo.mp4`). Verdict: "some potential here as long as we're smart about how we use it."
So these are tools to use on purpose, not defaults on every shot. Never retrofit them into approved films.
- **14, real paper** (a CC0 scan through every ink, `paperFinish`): the most broadly useful, and quiet. Fine for new films.
  Keep it fixed in screen space. The scan must be CC0 and logged.
- **15, yellow as the warning ink**: a story device for a film with a reveal (the tell, the fake part). Print blue and black
  until the moment, then let the yellow arrive with it. Don't recolour puppet art unless it serves that reveal.
- **13, dots as shading locked to parts** (`shadedPart`): for characters staged big (hero shots). At small sizes it reads as
  noise, and over dark art it's invisible. Build it once per part at load, never per frame.
- **11, print marks** (crop marks, registration targets, colour bar): one framing device per film at most, e.g. the title
  card or an evidence close-up, not every scene. Keep the marks out of the logo bug's corner and the caption area. They are
  decoration; nothing readable goes in them.
