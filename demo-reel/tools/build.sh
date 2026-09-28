#!/bin/sh
# Build the demo reel end to end: frames, score, master + preview, sync and verification reports.
# usage: sh tools/build.sh            (from demo-reel/; about 6 minutes)
set -e
cd "$(dirname "$0")/.."
NAME="Your First Big Win - demo reel (9x16)"
rm -rf out/reel/frames
node render.mjs --html reel.html --out out/reel                      # 960 PNG frames + timeline.json (the cue sheet)
python3 tools/score.py out/reel                                      # score.wav, hits.json, audio_sources.txt
mkdir -p final
# static frames must stay static in the file: no B-frames, no mb-tree, no psy-rd; the master also holds quality flat (qcomp 1)
ffmpeg -v error -y -framerate 24 -i out/reel/frames/%04d.png -i out/reel/score.wav -map 0:v -map 1:a -c:v libx264 -crf 16 -preset slow -pix_fmt yuv420p \
  -x264-params bframes=0:mbtree=0:psy-rd=0.0:qcomp=1.0 -r 24 -c:a aac -b:a 256k -shortest -movflags +faststart "final/$NAME master.mp4"
ffmpeg -v error -y -framerate 24 -i out/reel/frames/%04d.png -i out/reel/score.wav -map 0:v -map 1:a -c:v libx264 -crf 21 -preset slow -pix_fmt yuv420p \
  -x264-params bframes=0:mbtree=0:psy-rd=0.0 -r 24 -c:a aac -b:a 256k -shortest -movflags +faststart "final/$NAME.mp4"
python3 tools/sync_check.py "final/$NAME.mp4" out/reel/hits.json > final/sync.txt; tail -1 final/sync.txt
python3 tools/verify.py "final/$NAME master.mp4" out/reel > /dev/null; cp out/reel/verify.txt "final/verify (master).txt"
python3 tools/verify.py "final/$NAME.mp4" out/reel; cp out/reel/verify.txt "final/verify (preview).txt"
cp out/reel/audio_sources.txt out/reel/timeline.json out/reel/hits.json final/
ls -la final
