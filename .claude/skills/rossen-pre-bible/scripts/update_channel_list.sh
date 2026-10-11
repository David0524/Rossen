#!/bin/bash
# Lists every Rossen Reports upload since a date, newest first, with views.
# Usage:  bash scripts/update_channel_list.sh 20260918
# Output: prints rows you can paste at the top of references/channel-uploads.txt
#
# Why the odd flag: YouTube blocks yt-dlp's default client ("The page needs to be reloaded").
# The android client works.
YTDLP=$(command -v yt-dlp || echo "$(dirname "$0")/.venv/bin/yt-dlp")
SINCE="${1:-20260901}"
for TAB in videos streams; do
  TYPE=$([ "$TAB" = "videos" ] && echo VID || echo LIVE)
  "$YTDLP" --extractor-args "youtube:player_client=android" \
    --dateafter "$SINCE" --break-on-reject --lazy-playlist --skip-download --ignore-errors \
    --print "%(upload_date)s | $TYPE | %(id)s | %(duration_string)s | %(view_count)s views | %(title)s" \
    "https://www.youtube.com/@RossenReports/$TAB" 2>/dev/null
done | sort -r
