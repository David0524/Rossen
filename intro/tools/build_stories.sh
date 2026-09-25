#!/bin/sh
# "STILL LIVE" Story frames from deals/deals.json: one 5 s looping mp4 and one PNG still per slide (each deal, then the
# "tune in" page). Output: out/rossen-deals-stories/story_<n>_<name>.mp4 / .png  (the still is the slide's first frame)
set -e
cd "$(dirname "$0")/.."
O=out/rossen-deals-stories
node render.mjs --html rossen-deals-stories.html > /dev/null
rm -f $O/story_*.mp4 $O/story_*.png
N=$(python3 -c "import json; print(len(json.load(open('deals/deals.json'))['deals']))")
for s in $(seq 0 $N); do
  if [ $s -lt $N ]; then name=$(python3 -c "import json,re; d=json.load(open('deals/deals.json'))['deals'][$s]; print(re.sub(r'[^a-z0-9]+','_',d['name'].lower()).strip('_'))"); else name=tune_in; fi
  f=$(printf "%s/story_%d_%s" $O $((s + 1)) $name); i0=$((s * 120))
  ffmpeg -v error -y -framerate 24 -start_number $i0 -i $O/frames/%04d.png -frames:v 120 -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -r 24 -movflags +faststart $f.mp4
  cp $O/frames/$(printf %04d $i0).png $f.png
  echo built $f.mp4 $f.png
done
rm -rf $O/frames
