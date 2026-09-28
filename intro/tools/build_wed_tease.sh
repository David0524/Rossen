#!/bin/sh
# Wednesday tease + the approved Wednesday 5 PM LIVE TODAY loop, appended untouched and played twice (40 s). Every tease ends on its loop x2.
#   0. decode the delivered loop's frames (read-only) for the handoff bar and its masks
#   1. render the 30 s tease (same x264 settings as the loop, so the streams join)
#   2. score it (the loop's own cue carries bars 10-11; full_audio.wav = tease audio + the loop's own audio, twice)
#   3. join the loop's video by stream copy (its packets are not re-encoded), mux the audio, make a CRF 21 preview
set -e
cd "$(dirname "$0")/.."
O=out/rossen-tease-wednesday; L="../final-videos/09 Live Today Loop - Wednesday 5 PM (9x16).mp4"
mkdir -p out/rossen-loop-wednesday/frames
[ -f out/rossen-loop-wednesday/frames/0119.png ] || ffmpeg -v error -y -i "$L" -start_number 0 out/rossen-loop-wednesday/frames/%04d.png
[ -n "$SKIP_RENDER" ] || node render.mjs --html rossen-tease-wednesday.html --all > /dev/null
python3 score_wed_tease.py
ffmpeg -v error -y -i "$L" -an -c:v copy $O/loop_v.mp4
printf "file 'video.mp4'\nfile 'loop_v.mp4'\nfile 'loop_v.mp4'\n" > $O/concat.txt
ffmpeg -v error -y -f concat -safe 0 -i $O/concat.txt -c copy $O/video_full.mp4
ffmpeg -v error -y -i $O/video_full.mp4 -i $O/full_audio.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart $O/rossen-tease-wednesday.mp4
ffmpeg -v error -y -i $O/video_full.mp4 -an -c:v libx264 -crf 21 -preset slow -pix_fmt yuv420p $O/pv.mp4
ffmpeg -v error -y -i $O/pv.mp4 -i $O/rossen-tease-wednesday.mp4 -map 0:v -map 1:a -c copy -movflags +faststart $O/preview_crf21.mp4 && rm $O/pv.mp4
echo built $O/rossen-tease-wednesday.mp4 $O/preview_crf21.mp4
python3 tools/sync_check.py $O/rossen-tease-wednesday.mp4 $O/hits.json > $O/sync.txt
python3 tools/verify_wed_tease.py $O/rossen-tease-wednesday.mp4 $O/preview_crf21.mp4 > $O/verify.txt || true
tail -1 $O/sync.txt; tail -1 $O/verify.txt
HITS_ONLY=1 python3 score_wed_tease.py > /dev/null && python3 tools/sync_check.py $O/score_hits.wav $O/hits.json > $O/sync_hits_only.txt && tail -1 $O/sync_hits_only.txt
# the safe-zone overlay pass: one frame per beat, rendered with ?safe=1, and a contact sheet
L=$(python3 -c "print(','.join(str(k * 15 + 7) for k in range(48)))")
node render.mjs --html rossen-tease-wednesday.html --query safe=1 --only $L > /dev/null
mkdir -p _check/wedtease/safe && rm -f _check/wedtease/safe/*.jpg
for i in $(echo $L | tr , ' '); do f=$(printf %04d $i); python3 -c "from PIL import Image; Image.open('out/rossen-tease-wednesday_check/frames/$f.png').convert('RGB').save('_check/wedtease/safe/$f.jpg', quality=80)"; done
python3 -c "
from PIL import Image, ImageDraw; import glob
fs = sorted(f for f in glob.glob('_check/wedtease/safe/*.jpg') if 'sheet' not in f); cols, w, h = 8, 216, 384
S = Image.new('RGB', (cols * w, ((len(fs) + cols - 1) // cols) * (h + 20)), (20, 20, 20)); d = ImageDraw.Draw(S)
for k, f in enumerate(fs): x, y = (k % cols) * w, (k // cols) * (h + 20); S.paste(Image.open(f).convert('RGB').resize((w, h)), (x, y + 20)); d.text((x + 4, y + 4), '%.2fs' % (int(f[-8:-4]) / 24), fill=(255, 255, 255))
S.save('_check/wedtease/safe/safe_sheet.jpg', quality=85)"
