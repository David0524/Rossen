#!/bin/bash
# Ryan's rubric: what is overperforming on OTHER channels?
# Searches YouTube sorted by view count and prints the top results.
#
# Usage:
#   bash scripts/competitor_search.sh month "bitcoin atm scam" "squatter" "deed fraud"
#   bash scripts/competitor_search.sh year  "sweepstakes scam"
#
# First argument: month = uploaded this month, year = uploaded this year.
# Then one or more search phrases in quotes.
#
# Reading the output (views | video id | channel | length | title):
#   - Ignore entertainment, politics, scam-baiting creators, and non-US results. We want news stations and consumer channels.
#   - "year" results do not show the upload date. Confirm the date before you cite it:
#       bash scripts/video_info.sh VIDEO_ID
#   - A local news clip over 200K or a creator video over 500K is real heat for our lane.
YTDLP=$(command -v yt-dlp || echo "$(dirname "$0")/.venv/bin/yt-dlp")
WHEN="$1"; shift
[ "$WHEN" = "year" ] && SP="CAMSAggF" || SP="CAMSAggE"
for Q in "$@"; do
  echo "=== $Q ($WHEN, by views)"
  "$YTDLP" --flat-playlist --playlist-end 25 \
    --print "%(view_count)s | %(id)s | %(channel)s | %(duration_string)s | %(title)s" \
    "https://www.youtube.com/results?search_query=$(echo "$Q" | sed 's/ /+/g')&sp=$SP" 2>/dev/null \
    | grep -v "Rossen Reports" | sort -t'|' -k1,1nr | head -15 | cut -c1-170
  echo
done
