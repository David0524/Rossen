#!/usr/bin/env bash
#
# crop_vertical.sh — trim a source clip to an outcue-anchored span and, when the
# source is a landscape file with a vertical video sitting inside the frame,
# crop it back to a clean full-screen 9:16.
#
# Built for Rossen vertical beats (first_person_rant, evidence, self-recorded).
# The self-recorded phone clip is native 9:16, but the only copies that surface
# are often 16:9 reposts with the vertical pillar-boxed in the center. This
# recovers the vertical.
#
# Two modes:
#
#   frame  — pull one still so you can SEE where the subject sits before cutting.
#            Always do this first on a landscape source; the center-crop assumes
#            the subject is centered, and reposts frequently offset him with a
#            headline panel.
#
#   cut    — trim [--start,--end] and write the deliverable. Pick one geometry:
#              --native      source is already 9:16; trim only, no reframe
#              --vertical    center-crop 16:9 -> 9:16 (auto geometry via ffprobe)
#              --crop W:H:X:Y explicit ffmpeg crop box, then scale to 1080x1920
#            If none is given, cut auto-detects: portrait -> native, landscape
#            -> vertical.
#
# Timecodes accept ffmpeg syntax: 0:00, 1:11, 71, 00:01:11.
#
# Examples:
#   cut/crop_vertical.sh frame -i gutman.mp4 -t 0:30
#   cut/crop_vertical.sh cut -i gutman.mp4 -s 0:00 -e 1:11 -o gutman_opt1.mp4 --vertical
#   cut/crop_vertical.sh cut -i gutman.mp4 -s 0:00 -e 1:11 -o gutman_opt1.mp4 --vertical --x 220
#   cut/crop_vertical.sh cut -i phone.mp4  -s 0:00 -e 1:11 -o gutman_opt1.mp4 --native
#
set -euo pipefail

die()  { printf 'crop_vertical: %s\n' "$*" >&2; exit 1; }
have() { command -v "$1" >/dev/null 2>&1; }

have ffmpeg  || die "ffmpeg not found (need ffmpeg on PATH)"
have ffprobe || die "ffprobe not found (ships with ffmpeg)"

usage() {
  sed -n '2,45p' "$0" | sed 's/^#\{0,1\} \{0,1\}//'
  exit "${1:-0}"
}

[ $# -ge 1 ] || usage 1
MODE=$1; shift

# ---- defaults ---------------------------------------------------------------
IN=""; OUT=""; START=""; END=""; FRAME_T="0:05"
GEOM="auto"          # auto | native | vertical | explicit crop box
CROP_BOX=""          # W:H:X:Y when GEOM=explicit
X_OVERRIDE=""        # nudge just the center-crop x offset
CRF=18
TARGET_W=1080; TARGET_H=1920   # delivery size for vertical

# ---- arg parse --------------------------------------------------------------
while [ $# -gt 0 ]; do
  case "$1" in
    -i|--input)   IN=$2; shift 2 ;;
    -o|--output)  OUT=$2; shift 2 ;;
    -s|--start)   START=$2; shift 2 ;;
    -e|--end)     END=$2; shift 2 ;;
    -t|--time)    FRAME_T=$2; shift 2 ;;   # frame mode: timestamp of the still
    --native)     GEOM="native"; shift ;;
    --vertical)   GEOM="vertical"; shift ;;
    --crop)       GEOM="explicit"; CROP_BOX=$2; shift 2 ;;
    --x)          X_OVERRIDE=$2; shift 2 ;;
    --crf)        CRF=$2; shift 2 ;;
    -h|--help)    usage 0 ;;
    *)            die "unknown arg: $1 (try --help)" ;;
  esac
done

[ -n "$IN" ] || die "need -i/--input"
[ -f "$IN" ] || die "input not found: $IN"

# probe source dimensions
read -r SRC_W SRC_H < <(ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height -of csv=p=0:s=x "$IN" | tr 'x' ' ')
[ -n "${SRC_W:-}" ] && [ -n "${SRC_H:-}" ] || die "could not read dimensions from $IN"

# ---- frame mode -------------------------------------------------------------
if [ "$MODE" = "frame" ]; then
  OUT=${OUT:-check_${FRAME_T//[:]/_}.png}
  ffmpeg -y -ss "$FRAME_T" -i "$IN" -frames:v 1 "$OUT" >/dev/null 2>&1 \
    || die "frame extract failed at $FRAME_T"
  printf 'wrote %s  (source %sx%s)\n' "$OUT" "$SRC_W" "$SRC_H"
  printf 'look: is the subject centered? if offset, pass --x <pixels> to cut.\n'
  exit 0
fi

[ "$MODE" = "cut" ] || die "mode must be 'frame' or 'cut' (got '$MODE')"
[ -n "$OUT" ]   || die "need -o/--output"
[ -n "$START" ] || die "need -s/--start"
[ -n "$END" ]   || die "need -e/--end"

# ---- resolve geometry -------------------------------------------------------
if [ "$GEOM" = "auto" ]; then
  if [ "$SRC_H" -ge "$SRC_W" ]; then GEOM="native"; else GEOM="vertical"; fi
  printf 'geometry: auto -> %s (source %sx%s)\n' "$GEOM" "$SRC_W" "$SRC_H"
fi

VF=""
case "$GEOM" in
  native)
    # already portrait: trim only, no reframe. Re-encode for frame-accurate cut.
    VF=""
    ;;
  vertical)
    # center-crop a 9:16 column out of the landscape frame, then scale to target.
    cw=$(( SRC_H * TARGET_W / TARGET_H ))     # width of a 9:16 column at full height
    [ "$cw" -le "$SRC_W" ] || die "computed crop width $cw exceeds source width $SRC_W"
    if [ -n "$X_OVERRIDE" ]; then cx=$X_OVERRIDE; else cx=$(( (SRC_W - cw) / 2 )); fi
    VF="crop=${cw}:${SRC_H}:${cx}:0,scale=${TARGET_W}:${TARGET_H}"
    printf 'geometry: crop=%s:%s:%s:0 then scale %sx%s\n' \
      "$cw" "$SRC_H" "$cx" "$TARGET_W" "$TARGET_H"
    ;;
  explicit)
    [ -n "$CROP_BOX" ] || die "--crop needs W:H:X:Y"
    VF="crop=${CROP_BOX},scale=${TARGET_W}:${TARGET_H}"
    printf 'geometry: crop=%s then scale %sx%s\n' "$CROP_BOX" "$TARGET_W" "$TARGET_H"
    ;;
esac

# ---- cut --------------------------------------------------------------------
# -ss/-to as inputs after -i => frame-accurate. Re-encode video; AAC audio.
if [ -z "$VF" ]; then
  ffmpeg -y -i "$IN" -ss "$START" -to "$END" \
    -c:v libx264 -crf "$CRF" -preset slow -pix_fmt yuv420p \
    -c:a aac -b:a 192k -movflags +faststart "$OUT"
else
  ffmpeg -y -i "$IN" -ss "$START" -to "$END" -vf "$VF" \
    -c:v libx264 -crf "$CRF" -preset slow -pix_fmt yuv420p \
    -c:a aac -b:a 192k -movflags +faststart "$OUT"
fi

printf '\ndone -> %s\n' "$OUT"
printf 'verify the outcue lands at the tail: open it and confirm the last words.\n'
