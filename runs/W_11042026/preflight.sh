#!/bin/bash
# Phase 2 preflight for the Rossen pipeline. Run from the project root.
export PYTHONPATH="$(pwd)/harvest:$PYTHONPATH"
ok(){ echo "OK      $1"; }; bad(){ echo "MISSING $1"; }
python3 -c "import rossen_harvest" 2>/dev/null && ok "rossen_harvest" || bad "rossen_harvest (see SETUP_PHASE2.md step 1)"
python3 -c "import faster_whisper" 2>/dev/null && ok "faster-whisper" || bad "faster-whisper (pip install faster-whisper)"
which ffmpeg >/dev/null && ok "ffmpeg" || bad "ffmpeg"
[ -n "$BRAVE_API_KEY" ] && [ "$(curl -s -o /dev/null -w '%{http_code}' -H "X-Subscription-Token: $BRAVE_API_KEY" 'https://api.search.brave.com/res/v1/web/search?q=test')" = "200" ] && ok "Brave key" || bad "Brave key (set BRAVE_API_KEY, step 3)"
yt-dlp $YTDLP_ARGS --flat-playlist --dump-json "ytsearch1:scam" >/dev/null 2>&1 && ok "YouTube search" || bad "YouTube search"
yt-dlp $YTDLP_ARGS --skip-download --list-subs "https://www.youtube.com/watch?v=aircAruvnKk" 2>&1 | grep -q "not a bot" && bad "YouTube captions (step 4: cookies-from-browser)" || ok "YouTube captions"
yt-dlp $YTDLP_ARGS -f bestaudio -o /tmp/probe.%\(ext\)s --no-warnings "https://www.youtube.com/watch?v=aircAruvnKk" >/dev/null 2>&1 && ok "YouTube audio" || bad "YouTube audio (step 4)"
