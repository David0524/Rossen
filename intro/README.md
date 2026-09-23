# Rossen Reports live-stream opener (15 s, 1920x1080, 24 fps)

`out/rossen-live-intro.mp4` is the finished opener: one continuous shot, H.264 plus AAC, at -16 LUFS.

## Rebuild
```bash
npm i                      # puppeteer-core only; uses the pre-installed Chromium
node render.mjs --all      # 360 frames -> out/video.mp4   (--grid 24 / --only 0,180 for spot checks)
python3 mix.py             # sample-based soundtrack -> out/score.wav (needs numpy)
ffmpeg -y -i out/score.wav -af loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000 out/score_norm.wav
ffmpeg -y -i out/video.mp4 -i out/score_norm.wav -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart out/rossen-live-intro.mp4
```

## Assets
- `assets/jeff_ref.png`: the cartoon Jeff reference. `tools/seg.py` and `tools/build_assets.py` cut Jeff out of it at full detail, so every frame uses the reference drawing itself. They write `jeff_body/legL/legR.png`, with the legs split off so he can walk, and `plate.png`, the same street with Jeff removed.
- `assets/logo_handdrawn.png`: the hand-drawn logo. It is used only as the mic flag, warped onto the flag inside the sprite.
- `assets/official_logo.png`: the final-beat logo. **This file is currently a stand-in copy of the hand-drawn logo, because no official PNG/SVG was on disk.** Replace it with the official file and re-run the steps above. It is drawn exactly as supplied: transparent margins are trimmed for centring, and it is scaled to fit a 720x400 box.
- Audio: slices of `/usr/lib/libreoffice/share/gallery/sounds/*.wav` placed on the beat timeline in `mix.py`. Nothing is synthesised.
- Fonts: Bowlby One SC and Patrick Hand (OFL), and Permanent Marker (Apache 2.0), from google/fonts. The licences are in `assets/fonts/`.
