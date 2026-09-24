#!/bin/sh
# Friday tease + the approved LIVE TODAY loop, appended untouched and played twice (35 s).
#   1. render the 25 s tease (same x264 settings as the loop, so the streams join)
#   2. score it (the loop's cue carries bars 8-9; full_audio.wav = tease audio + the loop's own audio)
#   3. join the loop's video by stream copy (its packets are not re-encoded), mux the audio, make a CRF 21 preview
set -e
cd "$(dirname "$0")/.."
O=out/rossen-tease-friday
node render.mjs --html rossen-tease-friday.html --all > /dev/null
python3 score_tease.py
ffmpeg -v error -y -i out/rossen-loop-friday/rossen-loop-friday.mp4 -an -c:v copy $O/loop_v.mp4
printf "file 'video.mp4'\nfile 'loop_v.mp4'\nfile 'loop_v.mp4'\n" > $O/concat.txt
ffmpeg -v error -y -f concat -safe 0 -i $O/concat.txt -c copy $O/video_full.mp4
ffmpeg -v error -y -i $O/video_full.mp4 -i $O/full_audio.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest $O/rossen-tease-friday.mp4
ffmpeg -v error -y -i $O/video_full.mp4 -an -c:v libx264 -crf 21 -preset slow -pix_fmt yuv420p $O/pv.mp4
ffmpeg -v error -y -i $O/pv.mp4 -i $O/rossen-tease-friday.mp4 -map 0:v -map 1:a -c copy -movflags +faststart $O/preview_crf21.mp4 && rm $O/pv.mp4
echo built $O/rossen-tease-friday.mp4 $O/preview_crf21.mp4
