#!/bin/sh
# "STILL LIVE" weekend deals roundup: both platform versions, straight from deals/deals.json.
#   edit deals/deals.json (the price-check time, prices, names, codes), then run:  sh tools/build_deals.sh
# Renders the Facebook and Instagram versions (only the CTA differs), scores once (the timing is shared), sets loudness,
# muxes, and makes a CRF 21 preview of each. Output: out/rossen-deals-still-live-<platform>/rossen-deals-still-live-<platform>.mp4
# Then builds the Story frames (tools/build_stories.sh): out/rossen-deals-stories/story_<n>_<name>.mp4 / .png
set -e
cd "$(dirname "$0")/.."
if grep -q '{{time}}' deals/deals.json; then echo "WARNING: deals.json still has the {{time}} placeholder for the price check"; fi
S=out/rossen-deals-still-live
python3 score_deals.py > /dev/null
ffmpeg -v error -y -i $S/score.wav -af "loudnorm=I=-16:TP=-2:LRA=11,aresample=48000,alimiter=limit=0.7:level=false" $S/score_norm.wav
for P in facebook instagram; do
  O=out/rossen-deals-still-live-$P
  node render.mjs --html rossen-deals-still-live-$P.html --all > /dev/null
  ffmpeg -v error -y -i $O/video.mp4 -i $S/score_norm.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart $O/rossen-deals-still-live-$P.mp4
  ffmpeg -v error -y -i $O/video.mp4 -an -c:v libx264 -crf 21 -preset slow -pix_fmt yuv420p $O/pv.mp4
  ffmpeg -v error -y -i $O/pv.mp4 -i $O/rossen-deals-still-live-$P.mp4 -map 0:v -map 1:a -c copy -movflags +faststart $O/preview_crf21.mp4 && rm $O/pv.mp4
  rm -rf $O/frames
  echo built $O/rossen-deals-still-live-$P.mp4 $O/preview_crf21.mp4
done
sh tools/build_stories.sh
