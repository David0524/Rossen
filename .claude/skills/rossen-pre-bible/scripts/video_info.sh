#!/bin/bash
# Upload date, views, channel, title, and the start of the description for any YouTube video.
# Usage:  bash scripts/video_info.sh VIDEO_ID [VIDEO_ID ...]
# Always run this before citing a competitor video. Search results don't show dates, and
# a "trending" clip is often a year old.
YTDLP=$(command -v yt-dlp || echo "$(dirname "$0")/.venv/bin/yt-dlp")
for V in "$@"; do
  "$YTDLP" --extractor-args "youtube:player_client=android" --skip-download \
    --print "%(upload_date)s | %(view_count)s views | %(duration_string)s | %(channel)s | %(title)s
    %(description).300s" "https://www.youtube.com/watch?v=$V" 2>/dev/null
  echo
done
