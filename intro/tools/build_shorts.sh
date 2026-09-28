#!/bin/sh
# Rebuild every short that ends on the closing card (liveEndCard in vertkit.js): render, score, loudness, mux.
# usage: tools/build_shorts.sh [name ...]   (names: mychart quiz rules1 rules2 rules3 wwyd1 wwyd2 officer; default all)
set -e
cd "$(dirname "$0")/.."
build() {   # html  out-dir  score-command  loudnorm-I  limit
  O=out/$2
  node render.mjs --html $1 --all > /dev/null
  sh -c "$3" > /dev/null
  ffmpeg -v error -y -i $O/score.wav -af "loudnorm=I=$4:TP=-2:LRA=11,aresample=48000,alimiter=limit=$5:level=false" $O/score_norm.wav
  ffmpeg -v error -y -i $O/video.mp4 -i $O/score_norm.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest $O/$2.mp4
  echo built $O/$2.mp4
}
for n in ${@:-mychart quiz rules1 rules2 wwyd1 officer}; do case $n in
  mychart) build rossen-mychart-scam.html rossen-mychart-scam "python3 score_mychart.py && sh tools/vo_bed.sh" -16 0.7 ;;
  quiz)    build rossen-scam-or-legit.html rossen-scam-or-legit "python3 score_quiz.py" -15.2 0.63 ;;
  rules1)  build rossen-rules-ep01.html rossen-rules-ep01 "python3 score_rules.py rules/ep01" -16 0.7 ;;
  rules2)  build rossen-rules-ep02.html rossen-rules-ep02 "python3 score_rules.py rules/ep02" -16 0.7 ;;
  rules3)  build rossen-rules-ep03.html rossen-rules-ep03 "python3 score_rules.py rules/ep03" -16 0.7 ;;
  wwyd1)   build rossen-wwyd-ep01.html rossen-wwyd-ep01 "python3 score_wwyd.py wwyd/ep01" -16 0.7 ;;
  wwyd2)   build rossen-wwyd-ep02.html rossen-wwyd-ep02 "python3 score_wwyd.py wwyd/ep02" -16 0.7 ;;
  officer) build rossen-officer-scam.html rossen-officer-scam "python3 score_officer.py" -16 0.7 ;;
esac; done
