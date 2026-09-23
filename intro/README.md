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
