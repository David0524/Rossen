# Lessons for a Rossen animation skill

These are the non-obvious things learned while making the Rossen Reports animations in this repo:

- the 15 s LIVE intro
- the pencil-style title sequence
- the case-file screen-print intro, in 16:9 and 9:16
- the 9:16 MyChart-scam explainer

Most of these came from a bug, a failed render, or a correction from the client. Each one is written as a rule, with the reason behind it.

---

## 0. Standing client direction (read this first, applies to every new video)

### Text must be easy to read
Viewer feedback: the text was hard to read because of motion, speed and everything being "fun": tilted cards, bouncing, wobbling and swinging. Readability now beats playfulness for any text a viewer has to read.

- **Readable text sits straight.** Captions, cards, labels and anything with a sentence on it use rotation 0.
  - Tilt is only for short decorative stamps of one or two words (LIE #1, FAKE!), at most ±0.03 rad.
  - Never tilt and move a piece of text at the same time.
- **Text lands, then holds still.** When a caption or card has landed, nothing about it moves: no bob, sway, swing, beat pulse, shake or drifting camera under it.
  - Let the pictures around it carry the energy: Jeff, the Scammer, props.
  - A swinging price tag must settle within about 0.3 s, or not swing at all.
- **Gentle landings.** Readable text pops in from 1.05× at most (not 1.1–1.3×), overshoots by 2% or less, and is still within about 0.2 s. A short slide or a straight cut also works. It still arrives on the beat (`SLAM`).
- **One thing to read at a time.** While a caption is landing, no other text on screen is moving. Have at most two text groups on screen at once: the caption plus one prop label.
- **Don't let text get squeezed.** If `fitText` would shrink a line below about 85% of its natural width, rewrite the line or split it across two or three lines instead.
  - Example: "AN ETHICAL HACKER / SHOWS YOU HOW / TO STOP IT".
- **Stay high contrast, on a plain chip.** Use cream on black, black on yellow, or cream on blue. Never put text straight onto halftone dots, pattern or motion.
- **Give reading time.** Every caption holds for its full bar (2.5 s at 96 BPM), with about 5 words per line at most. If an idea needs more words, give it two bars; don't speed up.
- **Check it.** For each caption, grab the frame about 0.3 s after it lands and view it at half size, which is roughly a phone at arm's length. If you have to squint, fix it.
- **In code, for new films:** the shared defaults were written for the "fun" look. Override them rather than changing the kits, so the approved videos render unchanged.
  - The `vertkit.js` captions (tilt ±0.012, pop from 1.3) and the per-film `chip()` helpers (tilt, from 1.1, 6% wobble): pass rotation 0 and a landing of 1.05 or less, and drop the wobble.
  - `stampLand` from 1.55, and the tilted `stampFit` calls: fine for one-word decorative stamps only.
  - The loops' beat pulse (4.5–6% scale on LIVE TODAY, the time card and the day chip) is approved as is. Don't retrofit approved videos unless asked.

### Transitions: more creative and interactive, but not every time
- **Budget:** in a 30–60 s piece, plan 2–3 signature transitions. The rest are simple pushes or clean cuts on the downbeat. Never put two signature transitions back to back.
- **"Interactive"** means the transition is an action the viewer can follow, done by a character or a prop. Examples:
  - Jeff rips the scene away like a page, flicks it, or pulls it off like a sticker.
  - A fishing hook yanks the scene out of frame.
  - The Scammer pulls a thread and the camera follows it to the next scene.
  - A tap on a button, or on a phone screen, dives into what it opens.
  - A magnifier lens widens until it becomes the next scene.
  - A door, vault or folder opens onto the next scene.
  - A card flips over to reveal the next scene on its back.
  - A camera flash freezes the frame into a Polaroid.
  - A rubber stamp slams down and covers the frame.
  - A zipper or tear strip opens the frame.
- **Where they go:** on story turns (hook to escalation, scam to Jeff's fix, fix to sign-off), not in the middle of an idea.
- **Rules for every transition:**
  - It lands on a downbeat and takes 0.5 s or less.
  - It never covers, distorts or shrinks a caption. The caption is readable just before and just after.
  - Never draw a caption inside a zooming window (the 0:15 bug in the Friday tease).
- **Plan them up front.** Label each transition in the timeline comment at the top of the film (for example `[SIGNATURE: hook yanks the phone]` or `[push]`) so they can be reviewed before rendering.

---

## 1. Before building anything

- **Check the brief against the assets.** A brief can contradict its own files. One asked to "match the red to the official logo", but the logo contains no red. Another asked for a red-accented palette when both logos were blue and yellow. Sample the logo's actual pixel colours before choosing inks. If there's a conflict, flag it and ask; don't guess. The client's answer was "use the logo's blue as the main ink". Once decided, that palette carries forward to later jobs, so reuse it and say so.
- **"If an asset is missing, stop" means stop.** Confirm every asset exists before writing code: character art, both logos, audio. Don't create stand-ins.
- **"Find audio yourself" means recorded samples, never synthesis.** CC0 sources that worked:
  - VSCO 2 Community Edition orchestra (strings, brass, woodwinds, percussion)
  - VSCO 1 drum kit
  - Kenney's Interface, Impact, RPG and Casino packs (foley)

  Keep the downloaded packs, because later jobs need more sounds from them. Copy only the files you use into the repo, and write a `samples_used.txt` alongside each score.
- **Rules about brands:**
  - Third-party names such as "MyChart" or "Medicare" may appear as plain text in a system font. Never draw or imitate their logos, including an app-tile glyph that could read as one; the tile shows only the name.
  - Fake URLs must look obviously garbled, like `htp://myc-hart.l0gin-kit.zz/?!`, and must not use a real top-level domain.
  - When the story says "type in the real site", show a placeholder ("YOUR PROVIDER'S SITE"), not an address.
  - No other company names anywhere, including in UI chrome.
- **Two logos, two roles.** The stylized logo (hand-drawn or screen-print) can be used inside scenes. The official logo appears only in the sign-off. There it is:
  - drawn with `drawImage` from the file, uniformly scaled
  - never textured or recoloured
  - excluded from the print-finish overlay
  - held completely still for at least the last second

  Verify stillness by pixel-diffing the final frames.
- **Logo fidelity checks can mislead.** A textured logo scaled by a non-integer factor shows about 5/255 mean per-pixel difference against a Lanczos resize, even when drawn perfectly. That's resampling, not tampering. Check two things instead: the mean colour of the opaque interior (it should match within about 1 level), and the ink's bounding box. Don't "fix" it by rounding the placement, because that changes already-approved renders.

## 2. Timing, rhythm and pacing (the most frequent client notes)

- **Choose the BPM before drawing anything, and build every scene on that grid.**
  - 144 BPM felt rushed for an older audience.
  - 96 BPM (beat 0.625 s = 15 frames at 24 fps, bar 2.5 s) worked: one scene or idea per bar.
- **Every scene must last a whole number of bars.** "There's an extra beat in each scene" meant scene lengths had drifted off the bar grid. Scenes that hold for extra beats feel wrong even when the viewer can't say why.
- **Pace everything the same.** The client objected more to uneven pacing than to speed: one scene fast, the next lingering. Judge it as both viewer and listener.
- **Landings finish on the beat.** Anything that lands (stamps, cards, letters, a character popping in) starts moving about 0.14 s early (`SLAM`) and arrives exactly on the beat: `land(t, t0) = seg(t, t0 - SLAM, t0)`. Starting on the beat looks and sounds late.
- **Place foley by its attack, not by the file's start.** Samples have leading silence and slow onsets. Find the first sample above 50% of peak and align that point to the picture. Trim leading silence on load.
- **Repeated sound effects must sit on the groove.** For card placements, for example, put them on eighth notes in the song's rhythm. The client heard "card blast" sounds that ignored the beat as wrong.
- **Measure sync on the final mp4.** Compute an onset envelope (5 ms hop, positive log-energy difference). Every big hit should land within about 10 ms of its picture beat. Don't trust the plan; measure the file.
- **Caption reading time sets the length.** At 2.5 s per caption (comfortable for an older audience) and one idea per bar, the story spine determines the duration. Pick the length the story needs. The MyChart explainer came to 17 bars plus a 2 s logo = 44.5 s.
- **Hook in the first two seconds.** The key object (the fake email) must be on screen from frame 0, fully legible, with its caption already landed. Add energy by making it bounce as it settles, not by building up to it. For intros, "the show is starting" should be clear by second 3.
- **Sampler details:**
  - Repitch by resampling.
  - The VSCO note names run an octave below concert pitch; use one convention consistently.
  - Tune the kick and timpani into the song's key (they were a fraction of a semitone sharp).
  - Soft-clip with tanh before normalizing.
- **Loudness targets:**
  - Standalone music: `loudnorm I=-16:TP=-2`, then `alimiter`.
  - Voiceover bed: see section 8.

## 3. The screen-print "case file" look

- **Inks:** a limited palette. Each colour ink is printed slightly off register (for example blue at [4,-3], yellow at [-4,3]) and has its own halftone screen angle. Black keylines have a rough edge. Paper texture goes underneath and a paper-speck overlay goes on top of every frame except the official logo.
- **Keep the accent small.** Too much yellow looked cheap. Use it for small highlights only (roughly 10% of the frame or less).
- **Stamps and word labels must be fully opaque.** A semi-transparent stamp let content show through and got flagged. On a same-coloured background, add an offset black drop shadow.
- **Shared helpers can hide off-palette colour.** An old kit function sprayed red ink spatter on every stamp. Audit every colour a shared helper draws.
- **Legibility beats decoration.** Never put particles or confetti over text or logos. For text on busy backgrounds, use black paper chips with cream text. See section 0: readable text sits straight and holds still.
- **Phone-readable sizes on a 1080-px-wide frame:** captions about 70–76 px, labels 44 px or more, small print 30 px minimum. Keep each caption to about 16 characters per line, two lines, ALL CAPS. `fitText` shrinks text to fit its box instead of letting it overflow the card.
- **Transitions should come from props.** Section 0 sets how many and where (2–3 signature transitions per piece, on story turns). Props that worked:
  - a folder cover flipping open
  - zooming through a magnifier lens
  - clicking a button and zooming through it
  - a Polaroid snapshot of a frozen frame
  - a page turn
  - a fishing hook snagging and yanking a card
  - a camera rising or dropping between two stacked scenes
  - a rubber stamp covering the frame before the logo
- **A "dive" into a rectangle needs matching proportions.** When zooming into a rect (for example a folder's inner page) until it becomes the next scene, that rect must have the frame's aspect ratio, or the cut distorts.

## 4. Paper-cutout puppets from reference art

- **Cutting the parts:**
  - Mask the background by flood-filling from the image border through non-foreground pixels, then dilating and eroding to fill small holes.
  - Cut the parts with hand-placed polygons over a coordinate-grid preview of the reference.
  - Store each part's bounding box and pivot in JSON.
  - Keep the original pixels; only the cut lines are new.
- **Preview before animating.** Render each part tinted a different colour over grey, plus test poses with the parts rotated. Mistakes are obvious there and invisible in the code, for example the mic top belonging to the head, or a rod mask taking a chunk of the coat.
- **A rotating part must not carry its neighbours' pixels.** Otherwise it leaves a hole when it moves. Three fixes, in order of preference:
  - Mask by colour so the part is only itself (mittens by hue, a reel by radius, a rod by a narrow band).
  - Fill whatever lies underneath with a tiled patch of the surrounding texture.
  - Also fill the paper-coloured gaps between the part and the body.
- **Curved props need curved masks.** A straight band along a curved rod left a sliver of its outline behind. Everything outside the body silhouette and not in the head zone belongs to the rod.
- **Erase anything the film will animate procedurally, and draw it in code.** Examples: fishing line, hook, strings. That lets it cast, snag and reel.
- **Rotation sign conventions differ.** Positive canvas `rotate` is clockwise; positive PIL `Image.rotate` is counter-clockwise. Test poses in PIL use the opposite sign.
- **Character notes the client caught:**
  - Jeff needed feet.
  - He had a doubled arm.
  - His head peeked in at the bottom edge before his entrance.

  Start entrances far enough off-screen for his scale. Re-check whenever a global scale changes; after the 86% content scale, a start position of 2600 was no longer off-screen.
- **Props held in the hand:** compute the direction from the shoulder to the hand, then draw fingers and thumbs as capsules in the character's own print style (its skin ink plus halftone). Pasted icons look wrong.
- **Pivot bookkeeping:** return the world position of the hand or rod tip from the puppet function, using `getTransform().inverse()` times the part transform, so props and lines can attach to it.

## 5. Vertical 9:16 (TikTok and Reels)

- **Re-lay out each scene; never crop landscape.** Scenes spread action across the width. Stack content top to bottom and use vertical camera moves: scroll-throughs, drop-downs, rising reveals. For example: panning down an evidence board, LIVE as L-I over V-E, Polaroids side by side above a document, price tags in a 2×2 grid.
- **Share one code path for both formats.** Use a single script with a `VERT` flag and per-scene layout objects. Before refactoring, save reference frames and pixel-diff after, so the approved version provably doesn't change.
- **Platform safe zones:** keep all text and key action clear of the top 15%, bottom 25% and right 15%.
- **The safe zone is not centred, but content must be.** The safe area's middle is x = 459–480, left of the frame's centre, and a layout centred there looked "off-centre" to the client. Fix: design inside the safe box, then show the content scaled by K (about 0.86) about the frame's centre line, so it spans x 180–900, symmetric about 540 and still clear of the right 15%.
  - Keep backgrounds, full-frame flashes, the covering rubber stamp and the logo in screen space.
  - Widen world-space backgrounds (water, piers) so they still reach the frame edges after scaling.
- **Long content scrolls inside a window.** An email taller than the safe area scrolls inside a framed viewport that ends at the safe line. In the reveal, where the viewport opens to the full frame, the lower part sinks into a solid ink "deep water" overlay, so no text ever sits in the bottom 25%.
- **Check it visually.** Render an overlay pass with a query flag (`--query safe=1`) into a separate `_check` folder, so debug frames never end up in the final video.
- **Stamps auto-fit.** Scale each stamp to the maximum safe width, accounting for its rotated bounding box. Long ones like "DON'T CLICK." otherwise overflow.
- **Avoid a squashed snapshot.** When a landscape snapshot of a portrait frame goes into a square Polaroid, crop a region instead of squashing the whole frame.
- **Captions** sit at the top of the safe area (y about 320–540). Scene content starts below about y 560.

## 6. Canvas and render-pipeline traps

- **Serve over http.** From `file://`, the canvas becomes "tainted" by images and `toDataURL` fails.
- **Render path:** puppeteer-core with the preinstalled Chromium, calling `window.__frame(i)` to get a PNG data URL for each frame, then ffmpeg (libx264, CRF 16, yuv420p, 24 fps). Throughput is about 2–4 frames per second at 1080×1920.
- **Everything is a pure function of `t`:** seeded RNG, no `Date` or `Math.random`, and no state carried between frames. That's what makes `--only` spot renders match the full render.
- **Background helpers that reset the transform break any scene you translate.** `paperBg` and `printFinish` draw in screen space via `resetT`. A camera rise that draws scene A translated and scene B above it will paint over itself. Draw each scene whole into an offscreen layer, then slide the layers. The same applies to zoom-through windows: draw the inner scene into a layer with the same content transform, and grow the window in screen space.
- **Pair every save with a restore.** Unbalanced `save`/`restore` around a clip silently shifts every later draw; wrap one-off screen-space draws in a helper.
- **The contact-sheet grid assumes landscape tiles.** Use a portrait tiler for 9:16 frames. Review sheets at 0.5 s intervals, plus full-size crops of every scene change.
- **Delivery limits.** The chat upload limit is 30 MB. Keep the CRF-16 master in the repo and send a CRF 20–22 preview (about 25 MB for 45 s). Make sure `.gitignore` excludes frame folders, intermediate WAVs and `_check` renders. Check which `.gitignore` you're editing (repo root vs project folder).
- **Name clashes in score scripts.** Scripts composed from a shared header can collide: a chord table named `ROOT` overwrote the sample-folder path. Use distinct names.

## 7. Story and explainer craft

- **Four parts that worked for a scam explainer:** bait, trap, theft, fix. Each gets 3–5 bars.
  - The villain's prop can carry the metaphor: a fishing rod and hook for phishing.
  - Each stolen item is a labelled card the viewer reads as it's yanked away: LOGIN & PASSWORD, MEDICARE NUMBER, NAME & ADDRESS, CARD NUMBER.
- **Captions carry the story with the sound off.** They are the narration: short, ALL CAPS, a few words each.
- **End on the protection line, held for two bars.** For example "DON'T CLICK. / GO TO THE APP / YOURSELF.", then the rubber stamp, then the logo.
- **Show "looks real" on screen.** A fake SECURE badge and a copied header, with the host's magnifier exposing the garbled address.
- **Let the host's first appearance feel like a turn.** Here the scammer was knocked out by a logo sticker slam, and the key moved from minor to major.
- **Evidence continuity pays off.** The client asked for the SCAM snapshot to be pinned next to the CAUGHT snapshot: things caught earlier should reappear on the evidence wall.

## 8. Audio for voiceover

- **A bed needs a different arrangement, not just less volume.**
  - Remove melodic lines in the voice range (roughly 300–3500 Hz): trumpets, clarinet, viola eighths.
  - Carry impacts with kick, timpani and bass instead of brass stabs.
  - Soften the snare and tambourine.
  - Keep high glockenspiel accents sparse.
  - Apply a gentle EQ dip around 2.2 kHz (-5 dB) and 450 Hz (-2.5 dB) on the music only.

  Verify it: the speech-band share of energy dropped from 20% to 11%.
- **Mix levels:**
  - Put the mix at about -23 LUFS, so a voice recorded at about -16 LUFS rides on top without ducking.
  - Deliver music and foley stems made with the same fixed gain, so they sum to the mix.
  - Include a timed VO script (about 100 words for 42 s), leaving the logo's last 2 s clear.
  - Tell the client the video will sound quiet on its own.

## 9. Working with this client

- They review closely, frame by frame and beat by beat. Expect notes on:
  - sync ("there's an extra beat")
  - legibility ("text bleeding off cards", "a bit see-through")
  - consistency ("everything paced the same")
  - centring
- Screenshots of problems arrive with the notes. Fix exactly what's named, and fix the same bug class wherever else it occurs (all stamps, not just SCAM). Say so when you do.
- Deliver each round with:
  - a preview mp4
  - a short list of what changed and how it was verified (stillness, logo fidelity, sync, loudness, safe zone)
  - anything you couldn't check, such as the fact that you can measure audio but not listen to it

## 10. Reusable pieces in this repo

| file | what it is |
|---|---|
| `core.js`, `kit.js` | Canvas core from the hand-drawn-canvas-animation skill (rng, easing, dotScreen, layers, fitText, wordStamp, paper) |
| `printkit.js` | Screen-print kit: inks and registration, `ink`/`key`/`block`/`dotsIn`/`inkText`, opaque `stampLand`, ransom letters, the Jeff puppet, magnifier, Polaroid, pushpin, yarn, `loadPrintKit()` |
| `casefile.js` | The case-file intro, 16:9 and 9:16 from one script (`VERT`) |
| `mychart.js` | The 9:16 explainer: captions, safe-zone content transform, scammer puppet, fishing line and hook, zoom-through, camera rise |
| `render.mjs` | `--html`, `--only`, `--grid`, `--all`, `--query` |
| `tools/cut_casefile_jeff.py`, `tools/cut_scammer.py` | Cut reference art into puppet parts with pivots |
| `score_casefile.py`, `score_mychart.py`, `tools/vo_bed.sh` | Sample-based scores on the bar grid; VO bed and stems |

## Fake officer explainer
- In a push between scenes, draw each scene's caption inside its own layer (the old caption frozen, the new one landing). A caption drawn on top of both layers lands on the old scene's content for the 0.15 s before the downbeat.
- A slam-in logo must clear the captions at its largest landing scale, not just at rest (720 x 502 at y 880, landing from 1.15x).
- At 24 fps an eighth-note hit falls between two frames (7.5 frames), about 21 ms from either. Put synced hits on beats (15 frames), and check with `tools/sync_check.py`, which also reports the mp4's container offset.
- Puppet pieces that come off (a cap, a badge) need hidden fills under them, not only under joints: here a head dome tiled from the costume's own black, and the coat copied from just below the badge.
- **Approved background for close-ups: textured cream** (`creamBg` / `makeCream` in `officer.js`). Use it behind phones, documents and any card-heavy close-up; the blue dotted background stays for character scenes. The recipe:
  - flat palette cream `#efe6d2`
  - about 60k fine grain specks
  - about 900 faint paper fibres
  - soft light mottling, where each blotch fades to its own colour at alpha 0
  - no dots, no vignette, nothing moving

  Rejected: black-on-cream dots (hypnotic), a scrapbook page with torn scraps and tape, and the plain `PAPER_TEX` stock (reads grey and cloudy, about 25 levels darker than cream).
- Canvas radial gradients blend unpremultiplied: fading `rgba(255,252,240,.16)` to `rgba(0,0,0,0)` leaves grey halos. Fade to the same colour at alpha 0.

## Appending an approved clip untouched
- Render the new part with the clip's own x264 settings, then join with the concat demuxer and `-c copy`. Verify with `framemd5`: the clip's decoded frames must match the original bit for bit.
- To hand off seamlessly into a loop, end the new part on the loop's own last frames and last bar of audio. The cut then becomes the loop's own wrap.
- AAC overshoots transients by about 1.5 dB, so put a soft ceiling around -4 dBFS on composed material before muxing.
