# Studio notes: lessons adopted from the Opus 5.5 motion-design course

**Precedence:** the client's standing direction in `intro/SKILL_NOTES.md` §0 and the Vox study (`intro/VOX_STUDY.md`) come
first. Where the course disagrees, the client wins:
- **No camera drift under captions** ("text lands, then holds still ... no drifting camera under it"). A caption is up in
  almost every bar, so the course's "camera never dead" becomes: camera moves only at transitions, and the life comes from
  the puppets and props (breathing, overlap, anticipation), always at 24 fps.
- **Gentle landings for readable text**: from 1.05x at most, no wobble, still within 0.2 s; no other text moves while a
  caption lands. Snap-and-overshoot is for characters and props, not words.
- **Captions 70-76 px**, one idea per bar, at most a caption plus one prop label on screen.
- **Backgrounds**: textured cream for close-ups, lighter blue dots for character scenes, flat drawn pavement; one dotted
  field per scene at most. Yellow stays a small accent.
- **Always on ones: smooth 24 fps motion for everything.** On twos (the Vox study's 12 drawings a second for puppets) was tried on
  the Wednesday tease and rejected by the client as "very laggy". Don't use it.

Source: the "How to build a motion design studio with Opus 5.5" thread (Movez, Sep 27 2026) and the repos it links. What's here
is what applies to this repo's pipeline (Canvas 2D pages with a deterministic `__frame(i)`, puppeteer → PNG → ffmpeg, recorded
instruments and recorded foley, the case-file screen-print look). Things that don't apply are listed at the end, with why.

Installed: `.claude/skills/claude-animation/` (buildwithhanif/claude-animation-skill, MIT, commit 4ddb8c8). It's the same
architecture as ours (a pure `frame(ctx, t)`, node canvas, ffmpeg), plus character rigs, an acting and timing reference
(`references/motion.md`, `characters.md`, `traps.md`) and a sheet / strip / verify harness. Use its references when planning
motion; our own kit (`intro/core.js`, `printkit.js`, `vertkit.js`) stays the renderer for Rossen films.

## 1. The critique loop, before every full render

We already render contact sheets and a verify pass. Add the parts we skip:

- **Score before you fix.** After each sheet, score 1–10: hook in the first 2 s, readability at phone size, motion quality
  (no dead frames, nothing sliding without easing), variety (something new every 2–4 s), composition, brand accuracy, sound
  sync. Write the 3 worst problems with timestamps, fix those, re-sheet. Repeat until every score is 8+. Log it in the film's
  `review_log.md` so the next session sees what was tried.
- **Phone test**: `ffmpeg -i X.mp4 -vf "fps=1,scale=360:-1,tile=5x3" -frames:v 1 phone.png`. Read every card at 360 px wide.
- **Strip around fast actions**: `ffmpeg -ss T -i X.mp4 -vf "scale=320:-1,tile=12x1" -frames:v 1 strip.png` for 12 consecutive
  frames around every contact, pop, stamp and transition (catches pops, overlaps and one-frame glitches a per-beat sheet misses).
- **Determinism check**: render the same frame twice and compare hashes. State carried between frames breaks seeking silently.
- Look at the *encoded master*, not just the PNGs.

## 2. Motion that feels alive (the fix for "lifeless")

From `.claude/skills/claude-animation/references/motion.md` and the course's springs section:

- **Snap, then hold.** A change that happens in 1–2 frames and then holds reads as intentional; a 0.5 s ease reads as a slide
  transition. Put the ease on the settle, not the change.
- **Anticipation**: a small move the opposite way first (lean back before the tug, sink before the pop).
- **Overlap**: parts arrive at different times: body first, head and hands 2–3 frames later.
- **Holds need life**: breathing (±1.2 % in our films), a blink every ~3 s, a slow head drift. Our puppets currently hold stiff apart from a
  head sine; add breathing and overlap on every puppet call.
- **Loops never in phase**: every repeated thing gets its own phase offset.
- **Camera** (course advice; for Rossen films only where no card is up, i.e. in transitions): a slow push (+5–10 % over a shot) keeps a held shot from reading as a slide. Keep cards and logos out of the
  camera transform.
- **Scale**: at 1x, a small character on a 1920-tall frame reads as an icon. Stage characters big (the course's ~1.3x world
  zoom). This matches the notes on the Wednesday opening ("crowded", later fixed by letting the car run off the edge).
- **Every hit is several things on the same frame**: the contact, a flash or shake, a burst, a sound pair.
- **Springs for multi-target values**: when something changes target several times (a cursor, a lens moving prop to prop), sum
  one closed-form spring per change instead of restarting an ease. It stays a pure function of time.
- **Exposure**: always on ones (24 drawings/s). On twos was rejected by the client as laggy.

## 2b. From the two reference repos (JohnHeibel/ClaudeAnimationBase and PDoomVideo guides)

Read, not installed (they are film projects, not skills). The points that transfer:

- **Write the reads.** For each shot list what the viewer must understand, in order, each with a start and end time; two
  important reads never overlap ("when two things happen at once, the viewer sees only one"). Cause, then reaction.
  Review by counting frames per read: one that flashes by in a few frames is missed. Let the reads set the length.
- **Fast actions, slow meanings.** Quick motion is fine if anticipated, but its meaning gets a hold. One constant speed is flat.
- **Lead the eye** before each read: a character looks at it, the camera moves to it, or it lights up first.
- **Overlap, no twinning.** Code moves every part at once on the same curve; instead eyes lead, the body follows, arms, hats
  and props drag and settle last. Never both arms at the same angle or both characters blinking together.
- **Faces never snap.** A mood change is a squint (anticipation), the face swaps under it, a take sized to the emotion, then an
  overshoot settle. Our gasp head swaps in one frame: give it the squint and the take next time.
- **Push poses further than feels natural**; subtle reads as nothing. Block key poses as stills before in-betweens.
- **Characters big**: about 40 % of frame height in hero shots.
- **Props touch the hand**: compute the prop's point from the same pose and check it with a crop.
- **The camera is never dead** (course advice; overridden for Rossen films: no drift under a card, so this applies only to shots without one): every shot has a slow drift, push, pan or an on-beat shake. **Sets, not cards**: a chapter
  happens in one place and the camera moves through it.
- **Every seam gets a transition that belongs to the story**, including into the first shot. For the case-file look: a folder
  slamming shut, a stamp filling the frame, a zoom into a document. (Our briefs ask for one or two creative transitions and
  simple ones elsewhere; the rest should at least be cuts on action.)
- **Every shot needs an event**; set up a motif and pay it off (e.g. a scam meter or a growing stack of case files); let the
  ending rhyme with the opening.
- **Show it, don't write it.** A sign that repeats the story is the classic failure. Our ALL-CAPS cards are a client
  requirement (readable with the sound off), so keep them, but don't let a card restate exactly what the puppets act out;
  make the card add the stakes or the turn.
- **Seeded jitter trap**: one moving element consuming a different amount of randomness each frame shifts the random stream
  for everything drawn after it, so still things shimmer. Reseed per element with a stable key. (Our `ink`/`block` seed per
  call, which is the right pattern; keep it that way.)
- **Line width scales with camera zoom**: scale keylines down in close-ups or fine lines become blobs.
- **Subagent briefs**: one chapter per file, each agent edits only its own file, shared-file bugs are reported rather than
  edited, and the brief states the safe zones, the palette, a per-frame cost budget and the exact render-check commands.

## 3. Reference first

Naming a style beats describing one, and a reference beats both. Before a new film: extract frames from the reference
(Jeff's approved animation, or the loop and case-file films already approved), write a short `style_guide.md` (palette hex,
type, shot lengths, transition types, how text enters and exits, texture), then a shot list on the beat grid. Take the
grammar, never the content. The demo-reel pause ("so far from Jeff's animation") is the case for doing this every time.

## 4. Banned defaults (the tells of AI-made video)

Centered title on a gradient; everything fading in; corner labels and frame borders; glow on UI; generic particle bursts;
dead beats. Note: the new intro title card rule (CLAUDE.md) risks the first one. Keep the card on the case-file look, make it
land with a hit rather than a slide-in (it is already landed at frame 0, with the music's downbeat as the hit), give it one
moving element below it (the Wednesday card's little car), and exit with a fade + dissolve (the client asked for the fade).

## 5. Briefs and packaging

- The films that worked came from long director's briefs: logline, references, character bible, beat sheet with a payoff
  every 3–5 s, text rules, workflow gates (plan → stills → animatic → full pass → polish → audio → render), the critique loop,
  a deliverables list. Our tease briefs already follow most of this.
- For multi-scene films split across subagents, write an `ANIMATION_GUIDE.md` first so every subagent codes in the same style.
- Package a repeated pipeline as a skill so the next one is a sentence. Done: `.claude/skills/rossen-animation/` (V2), which
  covers every Rossen film type, with the tease pipeline as one chapter.

## Not adopted, and why

- **Synthesized music and SFX**: the Rossen briefs ask for warm, real instruments and recorded sound effects, so we keep the
  VSCO recordings and recorded CC0 foley, placed by their attack.
- **Remotion / HyperFrames skills**: a different stack (React / HTML+GSAP) from our canvas pages; not installed. Worth
  reconsidering only for a templated series with many data-driven variants.
- **Generate-then-trace with a video model**: needs a video API and would change the look; not in scope.
- **60 fps with 4-subframe motion blur**: our deliverables are 24 fps and match the approved loops; motion blur would soften
  the print texture. Consider it only for a fast camera move, on that move alone.
- **-14 LUFS**: the approved loops sit at -16 LUFS; changing loudness would break the sample-exact handoff into them.
