# Rossen Reports live-stream openers (15 s, 1920x1080, 24 fps)

There are two films:
- `out/rossen-live-intro.mp4`: the story-style opener (table, scammer, deals).
- `out/rossen-title-sequence/rossen-title-sequence.mp4`: the title sequence, cut to a 120 BPM cue (see below).

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

## Opener 2: title sequence (20 s)
`rossen-title-sequence.html` (drawing kit in `kit.js`) is one continuous piece at 120 BPM. One beat is 0.5 s, or 12 frames, so every cut and stamp lands on the music. Each scene after the countdown gets 3 s.

| time | scene | transition out |
|---|---|---|
| 0–2 | pencil viewfinder, film-leader countdown 3-2-1, LIVE stamp at 1.5 | zoom into the LIVE dot, which opens as an iris |
| 2–5 | parallax street, Jeff running, skid at 3.8, magnifier shoved at the camera | zoom through the lens |
| 5–8 | giant phone "YOU WON $1,000!", scammer phishing for CLAIM NOW, SCAM! at 6.5 | phone tips to landscape, glitches to a feed, push into the screen |
| 8–10.5 | hidden-camera feed; Jeff barges in at 8.75, CAUGHT! at 9.5, scammer bolts | whip pan (10.5–11) |
| 11–13.65 | price tags drop on the eighths and get re-priced live, Jeff thumbs up, DEAL! at 12.5 | page turn |
| 14–17 | four cards on the beats (SCAMS EXPOSED / HIDDEN CAMERA / WARNINGS / REAL DEALS), then a hold to read them | cards blast outward |
| 17–20 | Jeff pops in, official logo paper-drops at 18.0 with confetti from behind it, LIVE stamp at 18.5, still from 19.0 | none |

Jeff: `kit.js` gives him shoes (the reference drawing stops at the trouser hems). Whenever a raised arm is drawn, it also switches to a copy of the body with the side-hanging arm cut away, so he never has two arms on one side. Stamps are solid, so nothing behind them shows through the lettering.

```bash
node render.mjs --html rossen-title-sequence.html --all      # -> out/rossen-title-sequence/video.mp4
python3 score_title.py                                      # -> out/rossen-title-sequence/score.wav
O=out/rossen-title-sequence
ffmpeg -y -i $O/score.wav -af "loudnorm=I=-16:TP=-2:LRA=11,aresample=48000,alimiter=limit=0.79:level=false" $O/score_norm.wav
ffmpeg -y -i $O/video.mp4 -i $O/score_norm.wav -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart $O/rossen-title-sequence.mp4
```
The score is a VSCO 2 CE orchestra (strings, brass fanfare and stabs, timpani, glock, xylophone) over the VSCO 1 drum kit, with the kick and toms retuned into the key, plus Kenney foley. `PITCHED_ONLY=1 python3 score_title.py` renders the pitched parts alone, for a tuning check.
