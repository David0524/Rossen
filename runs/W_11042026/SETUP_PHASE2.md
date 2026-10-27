# Phase 2 setup — run on your own computer in Claude Code

Why not in chat: YouTube blocks captions and audio downloads from cloud servers
("Sign in to confirm you're not a bot"). Every client yt-dlp offers and the
transcript API were tried from the chat sandbox on Oct 27, 2026; all blocked.
Your home or office connection is not blocked the same way.

## 1. Get the rossen_harvest package (the hard stop)

It is not in the skills, the Oct 12 skills backup or the workflow-update zip in
Drive. The likeliest home is Kyle's `rossen-clips-SHARE.zip` (22.9 MB, Drive,
July 23). Download it, unzip it, and put the `harvest/` folder in the project
root next to `runs/`. If it isn't in there, ask Kyle where `rossen_harvest`
lives.

## 2. Install (run every new session)

```bash
pip install -r harvest/requirements.txt      # yt-dlp, faster-whisper
pip install -U yt-dlp                         # YouTube changes often; stay current
export PYTHONPATH="$(pwd)/harvest"
python3 -c "import rossen_harvest, yt_dlp, faster_whisper; print('packages ok')"
which ffmpeg || brew install ffmpeg           # Mac; on Windows: winget install ffmpeg
```

## 3. Search key (TikTok, Instagram, Facebook, news-site video)

Without it the run is YouTube only, about 70% of normal coverage, and the four
TikTok beats in this show can't be checked.

1. Sign up at https://brave.com/search/api/ and create a key.
2. Add it to your shell profile, not to a document or chat:
   `export BRAVE_API_KEY="your-key"` in `~/.zshrc` (Mac) or `~/.bashrc`.
3. Open a new terminal.

## 4. If YouTube still says "not a bot" on your computer

Let yt-dlp borrow your logged-in browser session. Nothing to copy or share:

```bash
export YTDLP_ARGS="--cookies-from-browser chrome"   # or safari, firefox, edge
```

Use a browser where you're signed in to YouTube. Don't email or upload a cookies
file; it is a login.

## 5. Preflight

```bash
bash runs/2026-11-04_F2/preflight.sh
```

All six lines should say OK. Then in Claude Code:

> Use the rossen-story-outline skill, Phase 2 (rossen-pipeline), on
> runs/2026-11-04_F2/outline.md and the show plan in the same folder. Show: 11/4.
> Resume from Checkpoint 0.
