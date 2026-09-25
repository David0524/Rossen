# What we can learn from Vox, and the plan for the next video

Vox's videos can't be watched from this environment, so this comes from written breakdowns of their technique, interviews with Joss Fong (a founding Vox video producer), and After Effects tutorials that recreate the look. The goal is not to copy Vox. It's to borrow the parts that make their videos clear and alive, and keep our approved case-file screen-print style, palette, Jeff and the rest.

## What Vox does

### 1. Story first: one question, answered like an essay
- Each video answers one focused question. The founding producer called the format an "animated opinion essay." There are no desks, and talking-head interviews are never the backbone.
- The voiceover is written plainly for the ear ("That's right." "Here is..."), because viewers are taking in a lot at once.
- The payoff is delayed on purpose. The black-hole video builds up how hard the photo was to take before showing it, so the reveal lands.
- The whole edit is built on the voiceover: the audio is laid down first, and every visual change is timed to a spoken emphasis or a peak in the sound.

**For us:** our shorts play with the sound off, so the captions are the voiceover. Write a caption-first script in which every caption triggers exactly one visual change. Frame each short as a question the viewer already has ("Why did I get a text about a toll I never drove?").

### 2. The look: flat colour, paper and evidence
- Flat shapes in a small palette (3–4 colours), bold colour against neutral paper, and heavy geometric type for headlines.
- Never pure white: paper grain, halftone, a light film grain, and a soft vignette.
- A collage of real-world evidence: cut-out photos with torn edges, tape, newspaper clippings, screenshots, maps and documents.
- Annotation is the signature move. A highlighter swipes across a key phrase, a circle is drawn around a detail, a callout line points to it, and the camera then pushes in on that detail.

**For us:** we already share the paper, halftone, flat inks and bold type. What we lack is the evidence layer. Our scenes are fully drawn scenes rather than documents being examined. Scam content is perfect for this: the text message, the fake site and the bank alert are the evidence, and Jeff is the investigator marking them up.

### 3. Motion: made by hand, not slick
- **Animating on twos.** The graphics move at 12 fps inside a 24 fps edit. The slight stutter reads as handmade, while perfectly smooth motion reads as corporate.
- **Step reveals.** Lower thirds and masks are revealed frame by frame in a jagged way, skipping frames, and the text appears a beat after its card.
- **Consistent easing** everywhere, with quick moves for energy and held frames for emphasis.
- **A background that "boils"**: textures swap 2–3 times a second behind static elements. This is subtle, but see the caution below.

**For us:** put the puppets and cut-out props on twos. That fits the paper-cutout look perfectly. Text keeps our readability rule: it lands, then holds still, with nothing boiling underneath it.

### 4. Camera: 2.5D depth
- Scenes are built as stacked layers at different depths (background paper, evidence, props, annotations), with a camera that pushes or drifts slowly through them. The parallax gives depth without 3D models.
- The "tracking transition": the camera pulls back fast with a short motion blur that peaks exactly on the cut, and then moves into the next scene.
- Map and zoom moves (Google Earth style) establish scale before the detail.

**For us:** we move scenes around as flat layers. A real camera over layered depth, with a slow continuous push under still captions, would add life without making the text harder to read.

### 5. Data made simple
- One big number or one simple chart per idea, building on screen (a bar grows, a counter ticks up), with nothing else on the screen.

**For us:** we almost never show a number. One sourced stat per explainer (from FTC or FBI data, verified at the time of the build) would add authority, which fits Jeff's investigative brand.

### 6. Music as structure
- The music changes about every 20 seconds, and each start or stop is an emotional cue. The music gives way to the voice, and reflective music carries a reveal.

**For us:** we already score by act. Add deliberate silence or a drop just before the reveal, and a clear change of cue at each act.

## What we keep, and what we don't take

**Keep:**
- the case-file screen-print look and the approved palette (logo blue, black, cream, yellow)
- Jeff and the Scammer puppets
- 96 BPM, one idea per bar, landings on the beat
- the readability rules: straight, still text
- the closing card

**Don't take:**
- real photos of people, or real brands
- chromatic aberration, light leaks and heavy grain, which would fight our clean inks
- a boiling background behind text (viewers already found the black dot background hypnotic)

## Plan for the next video: the "unpaid toll" text scam (9:16, about 45 s)

**The question:** "WHY DID I GET A TOLL BILL FOR A ROAD I NEVER DROVE?"

| Act | Bars | What happens |
|---|---|---|
| Hook | 0–1 | The text is already on screen in frame 0, as evidence pinned to the cream board: "UNPAID TOLL: $4.15. PAY TODAY TO AVOID FEES." The question caption lands on it. |
| The evidence | 2–5 | Jeff marks it up the Vox way, one mark per bar: highlighter over PAY TODAY (urgency), a circle around the link (a strange web address), a callout on the tiny fee ("small, so you don't think twice"), a highlight on the sender (a random number). The camera pushes in to each mark in turn. **[SIGNATURE 1]** On the link, the camera dives through the circle into the fake payment page. |
| The scale | 6–8 | **[SIGNATURE 2]** A pull-back to a flat map of the U.S. covered in pins: "THEY SEND IT TO EVERYONE." One sourced stat builds as a big number or a simple bar, to be verified from FTC or FBI data at build time. |
| The mechanism | 9–12 | A step-by-step flow built on the beats: millions of texts, then a few clicks, then the fake page, then the card number is stolen. The pieces are cut-out paper on twos, and the Scammer collects at the end. |
| The fix | 13–16 | The music drops for a beat, then turns confident. **[SIGNATURE 3]** Jeff unfolds a paper strip reading "DON'T TAP THE LINK. CHECK YOUR TOLL ACCOUNT YOURSELF." Then: go to the toll agency's site or app yourself, and report it (placeholders only, no real agency names). |
| End | 17–18 | The rubber stamp, then the closing card. |

**Technique checklist for the build:**
1. **Caption-first script.** One caption per bar, each paired with exactly one visual change.
2. **Evidence layer.** Documents and phones on the cream board, with tape and torn edges.
3. **Annotation kit, new in `vertkit.js`.** `highlighter()` sweeps a ragged yellow stroke behind the text (never over it); `circleMark()` draws itself on in a few steps; `callout()` draws a line to a straight label.
4. **2.5D camera, new.** A `cam` with depth layers, a slow push, and a tracking transition whose blur peaks on the cut.
5. **On twos.** Puppets and cut-outs move at 12 fps. Text and the camera stay at 24 fps so reading stays smooth.
6. **One data moment**, with its source written down in a `sources.txt` next to `audio_sources.txt`.
7. **Music cues** change at each act, with one deliberate silence before the fix.
8. **The existing rules still apply:** safe zone, opaque labels, nothing crossing text, sync within 10 ms, readability, and the closing card.

**Before the full build:** make a 5-second test of one evidence beat (the highlighter swipe, circle and push-in, with the puppet on twos) so the new techniques can be approved before they go into a whole video.

## Sources
- [PremiumBeat: 5 breakdowns on replicating the Vox motion-graphics look](https://www.premiumbeat.com/blog/replicating-vox-motion-graphic/)
- [DEmotion: Why your motion graphics never look like Vox](https://trydemotion.com/blog/motion-graphics-like-vox)
- [The Open Notebook: how a Vox video explains the first photo of a black hole](https://www.theopennotebook.com/2020/01/07/videogram-how-a-vox-video-explains-the-science-behind-the-first-photo-of-a-black-hole/)
- [Storybench: Joss Fong on reinventing science explainers](https://www.storybench.org/learning-for-a-living-howtowns-joss-fong-is-on-a-mission-to-reinvent-science-explainer-videos/)
- [Cliptude: the Vox animation format](https://www.cliptude.com/docs/vox-animation/)
- [Flatpack FX: Vox-style collage animation](https://www.flatpackfx.com/blog/create-vox-style-collage-animation-adobe-after-effects) and [the unfold paper effect](https://www.flatpackfx.com/blog/vox-style-unfold-paper-texture-effect-adobe-after-effects)
- YouTube tutorials (titles and descriptions only): [Vox-style 3D camera collage](https://www.youtube.com/watch?v=howss3CU5mI), [Created Daley's collage series](https://www.youtube.com/watch?v=AbFmCpfGmus)
