# Building a new tease from the Wednesday build

Work in `intro/`. `<day>` is `wed` or `fri`; `<Day>` is `wednesday` or `friday`. The Wednesday files are the reference. Copy
them and change only what's listed here, so the proven parts (captions, handoff, joins, verify) stay identical.

## Files

| copy from | to | change |
|---|---|---|
| `rossen-tease-wednesday.html` | `rossen-tease-<Day>.html` | title, script name |
| `wed-tease.js` | `<day>-tease.js` | the header timeline comment, `CAPS`, `TR`, the scenes, `INTRO_TITLE`/`INTRO_SUB`, the loop frames path, the masks folder |
| `score_wed_tease.py` | `score_<day>_tease.py` | `ROWS` (chords per bar), the melodic lines, the foley block, `LOOP_MP4`, the output folder, the audio_sources header |
| `tools/build_wed_tease.sh` | `tools/build_<day>_tease.sh` | `O=`, `L=` (the loop file), the html and score names |
| `tools/verify_wed_tease.py` | `tools/verify_<day>_tease.py` | `LOOP`, `NT` (frames before the loop), `TR`, `CAPS`, `FLASH`, `SCAMS`, the intro title |
| `tools/make_wed_masks.py` | `tools/make_<day>_masks.py` | `LOOP` frames folder, the assets folder |
| `tools/cut_sidekick.py` | `tools/cut_<name>.py` | only when a new character is attached |

Assets for the film go in `assets/<day>tease/`; check renders go in `_check/<day>tease/` (the safe pass in `safe/`, critique
rounds in `review/`).

## What stays exactly as in the Wednesday film (don't rewrite)

- `chip()` / `capPop()` / `captionsTop()` (cards: 72 px, from 1.05×, level, drawn after `printFinish`), `CAPS` as
  `[land, leave, line1, line2]`.
- `pushTo`, `zoomTo`, `dissolve`, `layerOf` (each scene is drawn whole into its own layer, then moved: `paperBg`/`printFinish`
  reset the transform).
- `sceneHandoff` + `PIECE_T` + `loopFrame` + the mask loader.
- `frame(i)`: `t = i / FPS − INTRO`, and `drawScene` dispatching on `t` with a branch per scene and per transition window.
- The puppet functions `man`, `sidekick`, `scammerCash` (breathing via `p.breath`, a head scale via `p.headS`); Jeff via
  `jeff(c, x, y, s, { sy: 1 + breath(t) })`; `lag()` for heads that trail a landing; `twos = t => t` (keep on ones).
- `ground()` (flat drawn sidewalk), `creamBg()` for close-ups, `bgDots(c, BLUE, .03, .18)` for character scenes.

## Commands

```sh
cd intro
L="../final-videos/09 Live Today Loop - Wednesday 5 PM (9x16).mp4"   # Friday: 10 Live Today Loop - Friday 10 AM (9x16).mp4
md5sum "$L" out/rossen-loop-<Day>/rossen-loop-<Day>.mp4            # the delivered loop and the repo copy must match
ffprobe -v error -show_entries stream=width,height,r_frame_rate,nb_frames "$L"   # 1080x1920, 24/1, 120

# the loop's frames, decoded read-only (for the handoff bar and the masks)
rm -rf out/rossen-loop-<Day>/frames && mkdir -p out/rossen-loop-<Day>/frames
ffmpeg -v error -i "$L" -start_number 0 out/rossen-loop-<Day>/frames/%04d.png

# masks: the loop's bare background from the tease page, then the diff
node render.mjs --html rossen-tease-<Day>.html --query plate=1 --only 0
cp out/rossen-tease-<Day>_check/frames/0000.png assets/<day>tease/loop_plate.png
python3 tools/make_<day>_masks.py            # check the overlay: each band must hold one loop piece

# the critique loop (before any full render): one frame per beat, then a sheet
node render.mjs --html rossen-tease-<Day>.html --only $(python3 -c "print(','.join(['0','20','30','40']+[str(45+k*15+7) for k in range(48)]))")
# strips around fast actions: render 12-16 consecutive frames and tile them
# phone test (after a build): ffmpeg -i preview.mp4 -vf "fps=1,scale=360:-1,tile=8x4" -frames:v 1 phone.png

# the whole thing: render, score, join ×2, preview, sync, verify, safe pass
sh tools/build_<day>_tease.sh                 # SKIP_RENDER=1 reuses frames/video.mp4 after a score-only change
tail -1 out/rossen-tease-<Day>/verify.txt     # must be "0 failed"
```

A render of 1005 frames takes about 2.5 minutes; the full build about 5 minutes. After changing only a few frames, re-render
those with `--only`, re-encode `video.mp4` from the frames folder with the same x264 settings, then `SKIP_RENDER=1`.

## Traps this build already solved

- **Stream-copy join**: the tease must be encoded with the loop's own x264 settings (`render.mjs --all` does: libx264 CRF 16
  slow yuv420p 24 fps), or the concat won't join. The joined loop's first packet gains the loop's own SPS/PPS in-band; that's
  expected (verify checks every other NAL unit byte for byte).
- **Masks from decoded frames** need a diff threshold of 90 (codec noise on halftone edges reaches ~60).
- **The decoded AAC** of the loop has 640 samples of padding after 5.000 s: trim to `5 * SR`.
- **Render output collisions**: rendering a loop page writes into `out/rossen-loop-<Day>/frames`, the same folder the tease
  reads its decoded frames from. Re-decode after any loop render.
- **A comment pasted mid-line** can swallow the rest of a JS statement (the intro car vanished). Put comments at line ends.
- **Hits masked by the loop cue**: in the last two bars the measured onsets are the loop's own (8–16 ms "late" in the original
  loop file too). Check those hits in `sync_hits_only.txt` (the hits alone).
- **Audio positions** use film time + the intro offset (`T0` in the score, `OFF` in verify, `INTRO` in the film).
