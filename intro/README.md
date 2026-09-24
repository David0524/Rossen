# Rossen Reports live-stream openers (15 s, 1920x1080, 24 fps)

There are two films:
- `out/rossen-live-intro.mp4`: the story-style opener (table, scammer, deals).
- `out/rossen-title-sequence/rossen-title-sequence.mp4`: the title sequence, cut to a 96 BPM cue (see below).

## Opener 1: story


`out/rossen-live-intro.mp4` is the finished opener: one continuous shot, H.264 plus AAC, at -16 LUFS.

## Rebuild
```bash
npm i                      # puppeteer-core only; uses the pre-installed Chromium
node render.mjs --all      # 360 frames -> out/video.mp4   (--grid 24 / --only 0,180 for spot checks)
python3 score.py           # sample-based soundtrack from audio/ -> out/score.wav (needs numpy)
ffmpeg -y -i out/score.wav -af "loudnorm=I=-16:TP=-2:LRA=11,aresample=48000,alimiter=limit=0.79:level=false" out/score_norm.wav
ffmpeg -y -i out/video.mp4 -i out/score_norm.wav -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart out/rossen-live-intro.mp4
```

## Assets
- `assets/jeff_ref.png`: the cartoon Jeff reference. `tools/seg.py` and `tools/build_assets.py` cut Jeff out of it at full detail, so every frame uses the reference drawing itself. They write `jeff_body/legL/legR.png`, with the legs split off so he can walk, and `plate.png`, the same street with Jeff removed.
- `assets/logo_handdrawn.png`: the hand-drawn logo. It is used only as the mic flag, warped onto the flag inside the sprite.
- `assets/official_logo.png`: the final-beat logo. This is the official file as supplied. It is drawn exactly as supplied: transparent margins are trimmed for centring, and it is scaled to fit a 720x400 box.
- Audio: nothing is synthesised. `score.py` sequences recorded samples like a sampler would (nearest recorded note, repitched by at most a couple of semitones):
  - Music: an original 15 s cue at 120 BPM in D minor, turning to D major. It uses pizzicato and spiccato strings, brass stabs and a final brass chord, timpani, snare, cymbals, glockenspiel and xylophone from **VSCO 2 Community Edition** (CC0). Hits land on the LIVE stamp (0.30 s), SCAM! (7.30 s), the logo landing (13.55 s) and the final LIVE stamp (13.82 s).
  - Foley: stamp thunks, footsteps, telescoping clicks, card flicks for the bills, leather for the wallet and cardboard for the box, all from **Kenney** Impact, RPG, Interface and Casino packs (CC0).
  - Only the samples used are bundled under `audio/`, with their licences. Both sources are public domain, so no credit line is required.
- Fonts: Bowlby One SC and Patrick Hand (OFL), and Permanent Marker (Apache 2.0), from google/fonts. The licences are in `assets/fonts/`.

## Opener 2: title sequence (18 s)
`rossen-title-sequence.html` (drawing kit in `kit.js`) is one continuous piece at 96 BPM. One beat is 0.625 s, or 15 frames, and one bar is 2.5 s. Every scene is one bar and plays at natural speed. Every landing (numbers, stamps, tags, cards, logo) finishes on its beat or eighth, at the same moment as its sound.

| bar | film time | scene | on the grid |
|---|---|---|---|
| 1 | 0–2.5 | countdown | 3 / 2 / 1 / LIVE on beats 1–4, zoom into the LIVE dot |
| 2 | 2.5–5.0 | the run | sprint on beats 1–2 (a footfall every 16th), skid on 3, magnifier on 3½, lens on 4 |
| 3 | 5.0–7.5 | phone | bubble on 1, button on 1½, scammer on 2, SCAM! on 3, phone tips on 4 |
| 4 | 7.5–10.0 | hidden camera | Jeff lands on 2, CAUGHT! on 3, scammer bolts on 3½, whip pan from 4 |
| 5 | 10.0–12.5 | deals | tags land on eighths 1–2½, Jeff up on 2, DEAL! on 3, page turn on 4½ |
| 6 | 12.5–15.0 | cards | one card per beat (mirrors the countdown); the logo starts falling on 4½ |
| 7 | 15.0–18.0 | logo | lands on the downbeat and blows the cards away, Jeff up on 2, LIVE on 3, still from 16.6, chord rings out |

The score (`score_title.py`) is arranged as one piece. After the countdown, a single groove and bass line run unbroken to the logo, with the chords moving bar by bar (Dm–Bb–C | Dm–Eb | D–Bb–Eb | D–A | D–F–G–A | D). Big orchestral hits are saved for the five story beats: LIVE, SCAM!, CAUGHT!, DEAL! and the logo. Scene changes get only a light cymbal.

**Style rules for the title sequence** (so later edits stay consistent):
- **One hand.** Every drawn prop goes through `shape()` in `kit.js`: waxy two-layer pencil fill, paper flecks, and a heavy wobbly outline at `OUTLINE_K` = 1.5×. That's what lets the props sit next to the Jeff illustration.
- **One palette.** Cream paper, the logo's yellow and blue, and the stamp red, plus ink and pencil grey (`BLUE`, `YEL`, `MRED`, `PALEBLUE`, `PINK`, `CREAM`). Money stays green.
- **One sunburst.** Only for the logo payoff. The phone sits on a wall of pinned clippings with redaction bars. The cards sit on a case-file page with photo corners, pushpins and red string.
- **The villain** is a small con man: fedora with a red band, popped collar on a slate-blue coat, red scarf, curly mustache and a bandit mask.
- **The official logo is never altered.** Its shadow is pencil hatching masked by the logo's silhouette.

All on-screen text is fitted to its box (`fitText` in `kit.js`), so nothing runs past a card, bubble or label.

Jeff: `kit.js` gives him shoes (the reference drawing stops at the trouser hems). Whenever a raised arm is drawn, it also switches to a copy of the body with the side-hanging arm cut away, so he never has two arms on one side. Stamps are solid, so nothing behind them shows through the lettering.

```bash
node render.mjs --html rossen-title-sequence.html --all      # -> out/rossen-title-sequence/video.mp4
python3 score_title.py                                      # -> out/rossen-title-sequence/score.wav
O=out/rossen-title-sequence
ffmpeg -y -i $O/score.wav -af "loudnorm=I=-16:TP=-2:LRA=11,aresample=48000,alimiter=limit=0.79:level=false" $O/score_norm.wav
ffmpeg -y -i $O/video.mp4 -i $O/score_norm.wav -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart $O/rossen-title-sequence.mp4
```
The score is a VSCO 2 CE orchestra (strings, brass fanfare and stabs, timpani, glock, xylophone) over the VSCO 1 drum kit, with the kick and toms retuned into the key, plus Kenney foley. `PITCHED_ONLY=1 python3 score_title.py` renders the pitched parts alone, for a tuning check.

## Opener 3: case file (19.5 s, screen print)
`rossen-casefile.html`: a "case file" title sequence in a screen-print look. It uses flat inks in the logo's blue (#0858C0), black and the logo's yellow (#F8D000) as the one accent, on warm cream stock, with halftone tints, misregistered colour layers and paper specks. 96 BPM: one bar (2.5 s) per scene, and a stamp on beat 3 of every scene.

| bar | time | scene | transition out |
|---|---|---|---|
| 1 | 0–2.5 | manila folder thwacks down (beat 2), ransom letters L-I-V-E on eighths | folder cover flips open |
| 2 | 2.5–5 | camera pans the evidence board, puppet Jeff pops up and raises the magnifier | zoom through the lens |
| 3 | 5–7.5 | "YOUR ACCOUNT IS LOCKED" phone, con man dangles a hook, SCAM! | redaction marker blacks out the screen |
| 4 | 7.5–10 | lens iris opens on the hidden camera, Jeff barges in, flash + CAUGHT! | the frozen frame becomes a Polaroid |
| 5 | 10–12.5 | terms of service: redaction bars peel back ("WE SELL YOUR DATA", "HIDDEN FEE"), WARNING! | page turn |
| 6 | 12.5–15 | price tags on eighths, Jeff thumbs up, DEAL! | folder swings shut |
| 7 | 15–17.5 | folder cover with the screen-print logo, LIVE NOW | giant rubber stamp |
| 8 | 17.5–19.5 | official logo, untouched, revealed as the stamp lifts; still for the last 1.7 s | none |

- **Jeff** is a jointed paper-cutout puppet cut from the reference art (`tools/cut_casefile_jeff.py`: head, torso, two arms, two legs, with pivots in `assets/casefile/jeff_parts.json`). Yellow split pins show at the shoulder joint. The pointing finger and thumb are printed like his reference hands.
- **Logos:** the screen-print logo appears as a sticker on the folder cover; the official logo is the final frame, drawn from the file with no texture or print finish over it.
- **Score:** `python3 score_casefile.py`, then the same loudnorm and mux steps as opener 2 (in `out/rossen-casefile/`).

### Vertical (9:16) version

`rossen-casefile-vertical.html` renders the same film at 1080x1920 for TikTok, Reels and Shorts. Both pages load one script, `casefile.js`; the vertical page sets `window.CASEFILE_VERTICAL = true` and each scene switches to a portrait layout (a tall folder with L-I / V-E, the board panning down instead of across, the SCAM and CAUGHT Polaroids side by side above the fine print, tags in a 2x2 grid). Timing is identical, so it uses the same score:

```
node render.mjs --html rossen-casefile-vertical.html --all
ffmpeg -y -i out/rossen-casefile-vertical/video.mp4 -i out/rossen-casefile/score_norm.wav -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart out/rossen-casefile-vertical/rossen-casefile-vertical.mp4
```

Stamps and text stay out of the platform UI zones (the top bar, and the bottom caption area below about y 1560).

## Explainer: the fake MyChart email scam (9:16)

`rossen-mychart-scam.html` (script `mychart.js`) is a 44.5 s vertical explainer at 1080x1920 for TikTok and Reels, in the same case-file screen-print look. The shared kit (inks, halftones, stamps, the Jeff puppet) now lives in `printkit.js`, loaded by both the intro and the explainer. One idea per 2.5 s bar at 96 BPM, a caption on each downbeat:

| bars | time | story | on screen |
|---|---|---|---|
| 1–4 | 0–10 | **bait**: the email is on screen from frame 1 and scrolls through NEW TEST RESULTS, FREE MEDICARE HEALTH KIT, a ticking countdown; the camera rises to show it hanging on the scammer's hook | GOT THIS EMAIL? · A FREE KIT? NEW RESULTS? · HURRY! ACT NOW! · IT'S BAIT! |
| 5–7 | 10–17.5 | **trap**: a click zooms through the button into a fake site with a garbled address; Jeff's magnifier; the form asks for everything | THE LINK OPENS A FAKE SITE · IT LOOKS REAL. IT'S NOT. · IT ASKS FOR YOUR INFO |
| 8–10 | 17.5–25 | **theft**: the hook yanks LOGIN & PASSWORD, MEDICARE NUMBER, NAME & ADDRESS, CARD NUMBER; the camera rises to the pier | THEN THEY REEL IT ALL IN · STOLEN! |
| 11–17 | 25–42.5 | **fix**: the logo sticker knocks him off; a big X on the link; the MyChart app tile; typing the provider's site yourself; the real inbox | HERE'S HOW TO STAY SAFE · DON'T CLICK THE LINK · OPEN THE MYCHART APP YOURSELF · OR TYPE IN YOUR PROVIDER'S WEBSITE · CHECK IF THE MESSAGE IS REAL · DON'T CLICK. GO TO THE APP YOURSELF. |
| 18 | 42.5–44.5 | official logo, untouched, centred in the safe zone; still for the last 1.7 s | |

- **Safe zone and centring:** the layout is drawn inside x 60–900, y 300–1430, then shown scaled to 86% about the frame's centre line, so everything is centred on the frame (x 180–900) and still clear of the top 15%, bottom 25% and right 15%. Backgrounds, the rubber stamp and the logo are drawn full-frame. The long email scrolls inside a window that ends at the safe line and sinks into deep water in the reveal. `node render.mjs --html rossen-mychart-scam.html --query safe=1 --only 0,200` renders frames with the zones overlaid (to `out/rossen-mychart-scam_check/`).
- **Brands:** "MyChart" and "Medicare" appear as plain text only; no logos are drawn or imitated. The fake address (`htp://myc-hart.l0gin-kit.zz/?!`) is garbled and not a real domain; the real-site step shows "YOUR PROVIDER'S SITE", not an address.
- **The scammer** is a jointed puppet cut from the supplied art by `tools/cut_scammer.py` (head, coat, rod with both hands pivoting at the reel, two boots). The coat under the hands is filled with its own texture so the rod can swing; the fishing line and hook are drawn by the film so it can cast, snag and reel.
- **Score (a voiceover bed):** `python3 score_mychart.py && sh tools/vo_bed.sh`, then mux `bed_mix.wav`. Built for Jeff to narrate over: no melodic lines in the voice range (no trumpet, clarinet or viola parts, and the hits are kick, timpani and bass rather than brass), a softer backbeat, a dip around 2 kHz on the music, and the mix at -23 LUFS so a voice at about -16 LUFS sits on top without ducking. The stems `bed_music.wav` and `bed_sfx.wav` add up to the mix. D minor while the scam plays out, D major once Jeff shows the fix; all samples CC0 (VSCO 2 CE, VSCO 1 drums, Kenney).
- **Voiceover script:** `out/rossen-mychart-scam/vo_script.txt`, about 100 words timed to the bars, matching the captions.

## Promo: LIVE TODAY, "The DEVASTATING New Zelle Scam" (9:16, 15 s)

`rossen-live-today.html` (script `livepromo.js`) is a 15 s vertical promo for TikTok, Reels and Shorts, in the approved case-file palette (logo blue, black, cream, yellow accent). The vertical helpers the explainer used (safe-zone content transform, captions, fitted stamps, the scammer puppet, line and hook, zoom-through, rubber stamp) now live in `vertkit.js`, shared by the explainer and the promo; the explainer renders unchanged. 96 BPM, six bars:

| bar | time | on screen |
|---|---|---|
| 1 | 0–2.5 | the fake fraud-alert text on a phone from frame 0 (no bank name) · GOT THIS TEXT? |
| 2 | 2.5–5 | a thumb creeps to send YES, a hook dangles over the send button · DON'T REPLY! on 3, zoom through the screen on 4 |
| 3 | 5–7.5 | the balance drains on eighths while the scammer fishes cash out of a wallet, $0.00 on 3 · THIS TEXT CAN EMPTY YOUR ACCOUNT |
| 4 | 7.5–10 | the phone drops back; Jeff's magnifier over YES shows the hook on 3 · WHAT HAPPENS IF YOU REPLY?; zoom through the lens |
| 5 | 10–12.5 | the screen-print logo, LIVE TODAY (1), 5PM ET (1.5), WEDNESDAY (2), Jeff thumbs up, the Rossen trumpet theme |
| 6 | 12.5–15 | held; the rubber stamp lands on 2.5 and lifts off the official logo, still for the last 1.3 s |

"Zelle" appears only as plain system-font text in the account's payment line. Score: `python3 score_live.py`, then loudnorm (I -16, TP -2) and `alimiter=limit=0.7` (the AAC encode overshoots a little), then mux. Multi-transient foley (coins, card fans) is aligned by its first audible transient (`fx_first`), not its loudest.

## Quiz: "SCAM OR LEGIT?" (9:16, 59 s)

`rossen-scam-or-legit.html` (script `quiz.js`) is a three-round play-along quiz for TikTok, Reels and Shorts in the approved case-file palette, built on `printkit.js` and `vertkit.js`. 96 BPM; every round is 7 bars: SHOW (1; the phone slides in on beat 1) · PAUSE with an 8-beat countdown (2) · REVEAL, where the verdict lands on beat 1 and a flag is highlighted and labelled every two beats (2) · TAKEAWAY (2). The phone never moves while there is something to read.

| bars | round | answer | marked | takeaway |
|---|---|---|---|---|
| 1–7 | unpaid toll text | SCAM | PAY TODAY · SMALL FEE · LINK | DON'T CLICK. CHECK YOUR TOLL ACCOUNT YOURSELF. |
| 8–14 | verification code | LEGIT | YOU ASKED FOR IT · NO LINK · NO REQUEST | NEVER READ A CODE TO ANYONE WHO CALLS. |
| 15–21 | fraud alert, reply Y/N | SCAM | URGENT · REPLY YES OR NO | DON'T REPLY. CALL THE NUMBER ON YOUR CARD. |
| 22–24 | HOW MANY DID YOU GET RIGHT?, the answers recap, COMMENT YOUR SCORE: 0, 1, 2 OR 3? (a full bar), then the official logo, still for the last 1.3 s | | | |

- Play-along mechanics: the title *is* the answer pads, [SCAM] OR [LEGIT?], which take turns pulsing through the countdown; the countdown's last beat is a LOCK IT IN! slam (latch sound) and the pads lock; on the reveal the right pad lights up and takes the stamp while the wrong one dims under an X. A three-card scorecard across the top (current round highlighted) flips each card to its answer as it is revealed, and the end card recaps SCAM · LEGIT · SCAM with COMMENT YOUR SCORE: 0, 1, 2 OR 3?
- Everything is sized up for phones: the quiz page sets `window.VERT_K = 0.895`, so content fills the safe width (x 164–916, still centred and clear of the right 15%), with message text at 48 px on screen. The other vertical films keep 0.857.
- Flags are marked with a highlighter swiped *under* the words (yellow for scam flags, a pale tint of the logo blue for safe reasons), so no mark ever crosses a letter; each labelled chip pops on the same beat as its highlight. The Scammer appears only in scam reveals: caught in a spotlight beside the phone, then yanked off by a vaudeville hook.
- Score: `python3 score_quiz.py`, then loudnorm (I -15.2, TP -2), `alimiter=limit=0.63`, mux. Two answer stings come from Kenney's Digital Audio pack (CC0, licence in `audio/kenney/digital/`). `HITS_ONLY=1 python3 score_quiz.py` writes `score_hits.wav` with the groove, rolls, fills and clock muted, for checking each hit's onset against its picture beat without neighbouring sounds.


### Puppet neck fix

Both cutters (`tools/cut_casefile_jeff.py`, `tools/cut_scammer.py`) add a hidden copy of the chin and jaw to the torso part, under the head. At rest the head covers it; when the head tilts it fills the slit that used to open along the cut and let the background show through. Measured at the largest tilt the films use: Jeff about 1,100 see-through pixels before, 0 after; the Scammer about 1,700 before, 0 after. Every film was re-rendered.

## Series: JEFF'S RULES (9:16)

A template for one-rule episodes. `rules.js` holds the recurring parts, and each episode is data plus its own middle scenes:

- `rules/template.json`: the fixed bar counts (title 2, rule 2, recap 2, end 2), a 2-line rule, scenes of 1–4 bars. It's read by both `rules.js` (picture) and `score_rules.py` (sound), and `buildTimeline()` throws if an episode breaks it.
- `rules/epNN.json`: the number, hook, rule, recap line, `ruleAfter` (how many scenes come before the rule reveal), scenes (id, bars, captions `[bar, beat, line1, line2]`, chords per bar) and sound cues `[scene, bar, beat, cue]`.
- `rules/epNN.js`: the draw functions for that episode's scene ids (`SCENES.id = (c, t, S) => …`, with `S.at(bar, beat)` for scene-relative time).
- The page sets `window.EPISODE = "rules/epNN"` and loads `rules.js` then `rules/epNN.js`. `?ep=rules/other` swaps the data.

Timeline: TITLE · scenes before the rule · RULE · scenes after · RECAP · END + official logo. Between segments the camera drops to the next one (a 0.3 s vertical push centred on the downbeat), with the same card-slide sound every time. The rule reveal's signature sound is a gavel + timpani + low brass + a high glock note under each of the rule's two stamp strikes (bar 1 beat 3, bar 2 beat 1).

Episode 1, `rossen-rules-ep01.html`, "HANG UP. CALL BACK.", 16 bars = 40 s: title (bars 1–2) · the phone rings, "YOUR BANK", the Scammer on the line, URGENT (3–4) · rule (5–6) · caller ID can be faked, he swaps the name tags (7–8) · hang up, flip your card, call the number on the back, now you know who you're talking to (9–12) · recap: IT'S NOT RUDE. IT'S THE RULE. (13–14) · FOLLOW FOR RULE #2, then the logo, still for the last 1.7 s (15–16). No bank or company names; every number is 1-800-XXX-XXXX style.

Score: `python3 score_rules.py rules/ep01`, then loudnorm (I -16, TP -2), `alimiter=limit=0.7`, mux. The arrangement is voiceover-ready: pizzicato bass, low horns and drums, with no melodic lines in the voice range. `HITS_ONLY=1` writes a hits-only stem for sync checks. Dummy data for a template check is in `rules/demo02.json` (render with `--query ep=rules/demo02`).

Episode 2, `rossen-rules-ep02.html`, "GIFT CARDS ARE FOR GIFTS.", 16 bars = 40 s. It's built from the same template with only new data (`rules/ep02.json`) and scenes (`rules/ep02.js`):
- title (bars 1–2)
- three disguises, one bar each, swapped in a puff on beat 1: a government agent (YOU OWE BACK TAXES!), tech support (YOUR COMPUTER IS INFECTED!) and a "grandson" (I'M IN TROUBLE! I NEED HELP!). Each one makes the same demand on beat 3, GO BUY GIFT CARDS. READ ME THE NUMBERS., with the same low-trombone sting (3–5)
- rule (6–7)
- a gift card is like cash (FAST · HARD TO TRACE · NO TAKE-BACKS), then the PIN is read and the balance hits $0.00 (8–9)
- hang up · already paid: call the card company, RIGHT AWAY! · report it at FTC.GOV (10–12)
- recap: NO REAL BILL IS PAID IN GIFT CARDS. (13–14)
- FOLLOW FOR RULE #3 and the logo (15–16)

The phone, ringing and lurking-Scammer helpers now live in `rules/props.js`, shared by all episodes. Episode 1 renders pixel-identically, and its score is byte-identical after the cue library grew.
