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
`rossen-title-sequence.html` (drawing kit in `kit.js`) is one continuous piece at 120 BPM. One beat is 0.5 s, or 12 frames, and one bar is 2 s. The 3-2-1 is a three-beat pickup, so LIVE lands on the first downbeat. After that every scene is whole bars, with one two-beat drum fill into the final chord. The scenes are authored on their own clock; `SCENE_CLOCK` maps film time onto it piece by piece, and `score_title.py` mirrors that map so every sound lands on its picture event.

| film time | music | scene |
|---|---|---|
| 0–1.5 | 3-beat pickup | viewfinder countdown, 3-2-1 on the beats |
| 1.5–3.5 | bar 1 | LIVE stamp on the downbeat, holds and pulses, zoom into its dot on the last beat |
| 3.5–5.5 | bar 2 | the run (original 2 s choreography), magnifier at the lens |
| 5.5–9.5 | bars 3–4 | phone "YOU WON $1,000!", scammer phishing, SCAM! on the bar-4 downbeat (7.5) |
| 9.5–13.5 | bars 5–6 | hidden camera, Jeff barges in (10.5), CAUGHT! on the bar-6 downbeat (11.5), whip pan |
| 13.5–15.5 | bar 7 | a price tag on each eighth, re-priced live, DEAL! on beat 3 (14.5), page turn |
| 15.5–17.5 | bar 8 | four cards on eighths, then about 1¼ s to read them |
| 17.5–18.5 | 2-beat fill | cards blast, Jeff pops in, logo floats down |
| 18.5–20 | final chord | logo lands (18.5), LIVE stamp (18.75), still from 19.0 |

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
