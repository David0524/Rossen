# Handoff — 10/14 register supercut for the 11/4 Dollar General B story

Written Oct 27, 2026 in a cloud Claude Code session that couldn't do this job. YouTube
blocks video downloads from the cloud container, and the file was too large to attach.
Run this in **Claude Code on your own computer**: the desktop app's Code tab, pointed at
a local folder.

## Paste this into the local session

> Read runs/W_11042026/SUPERCUT_HANDOFF.md and make the supercut. Download the 10/14
> video from our channel, transcribe the register segment, cut the bites listed there,
> and give me the MP4 plus the edit list. Stop and show me the cut list before you render.

## 1. Setup (one time)

```bash
git clone https://github.com/David0524/Rossen.git   # or `git pull` in an existing clone
cd Rossen
git checkout claude/handoff-query-eval-66k1ba       # the default branch
git pull
# Mac:
brew install ffmpeg yt-dlp
# Windows:
#   winget install Gyan.FFmpeg yt-dlp.yt-dlp
pip install faster-whisper
```

Check: `ffmpeg -version`, `yt-dlp --version`, `python3 -c "import faster_whisper"`.

## 2. Get the video

The source is the 10/14 Wednesday show, our own upload:
**NEVER Take a Free Sample at the Mall (Here's Why)**, Rossen Reports, 26:20.
https://www.youtube.com/watch?v=enqBc2rmTsk

```bash
mkdir -p runs/W_11042026/supercut && cd runs/W_11042026/supercut
yt-dlp -f "bv*[height<=1080]+ba/b" --merge-output-format mp4 -o "1014_full.%(ext)s" \
  "https://www.youtube.com/watch?v=enqBc2rmTsk"
```

If YouTube asks for sign-in at home, add `--cookies-from-browser chrome` (or safari or
firefox). Never put a cookies file in the repo or the chat. If the master file from the
editor is on this computer, use that instead and skip the download.

## 3. Find the segment and transcribe it

The register segment comes right **after the OmniWatch spot**, roughly the last third of the
show. It's headed "THE PRICE ON THE SHELF ISN'T ALWAYS WHAT YOU PAY" in the sent bible
(`runs/W_10142026/sent/sent.md`, about lines 280–345). Transcribe the whole show (or from
about 15:00 to the end) with word timestamps:

```python
from faster_whisper import WhisperModel
m = WhisperModel("small.en", device="cpu", compute_type="int8")
segs, _ = m.transcribe("1014_full.mp4", word_timestamps=True)
# write start/end/text per segment (and words) to supercut/transcript_1014.json
```

Jeff riffs off the page. **Cut on what he actually said** in the transcript, never on the
script's wording.

## 4. The bites (store-neutral only)

Find each of these in the transcript. Wording is from the sent bible, so expect small
differences on air.

| # | Bite (as written) | Why it's in |
|---|---|---|
| 1 | "YOU SEE THE SALE SIGN. YOU GRAB IT. YOU SCAN IT AT SELF-CHECKOUT." | The setup, no store named |
| 2 | "AND DO YOU ACTUALLY LOOK AT THE PRICE ON THE CHECKOUT SCREEN? MOST OF US DON'T." | The viewer's blind spot |
| 3 | "AND IT'S NOT JUST ONE STORE. LAST YEAR TARGET AND DOLLAR GENERAL STORES WERE FINED FOR RINGING UP MORE THAN THE SHELF." | **The money bite.** Jeff named Dollar General on 10/14 |
| 4 | "CHECK THE TAG AGAINST THE SCREEN. EVERY TIME." | The habit |
| 5 | Protect-yourself #1–#3: "WATCH THE SCREEN AS EACH ITEM SCANS…", "PRICE HIGHER THAN THE SIGN? ASK FOR THE SHELF PRICE BEFORE YOU PAY… SNAP A PHOTO OF THE SIGN", "CHECK YOUR RECEIPT BEFORE YOU LEAVE THE STORE" | Optional. Pick one or two; they repeat the 11/4 fix list |

**Leave out** everything that names or shows Walmart: Amanda's Chef Boyardee TikTok
(clip 8), the digital price tags, the $5.6 million settlement, James Wrigg's TikTok
(clip 9), and the "we reached out to Walmart" line. Also leave out the tease-block version
("THE SIGN SAID $1…"), which is a different read.

Target length: **20–40 seconds**. Bite 3 is the one that has to be there; 1 + 3 + 4 alone
works.

For each bite:
- In-point on the start of Jeff's sentence (a breath before is fine); out-point after his
  last word, not mid-word.
- **Look at the frames.** Pull a still from the start, middle and end of every bite
  (`ffmpeg -ss <t> -i 1014_full.mp4 -frames:v 1 bite1_mid.jpg`) and check for a Walmart
  logo, sign, lower-third or B-roll. If one is on screen, trim around it or drop the bite.
- Watch for graphics that name Walmart (the protect-yourself graphic should be generic,
  but check).

**Show David the cut list (bite, in, out, verbatim outcue, what's on screen) before
rendering.**

## 5. Render

Cut each bite, then join them with a short dip (about 6 frames to black, or a 0.2 s audio
crossfade). Keep the source resolution and frame rate.

```bash
# per bite (re-encode for frame-accurate cuts)
ffmpeg -ss <IN> -to <OUT> -i 1014_full.mp4 -c:v libx264 -crf 18 -preset medium \
  -c:a aac -b:a 192k -af "afade=t=in:d=0.08,afade=t=out:st=<DUR-0.12>:d=0.12" bite1.mp4
# join (all bites share codec settings)
printf "file 'bite1.mp4'\nfile 'bite3.mp4'\nfile 'bite4.mp4'\n" > list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy "F2 Wed 11_04 -- B supercut 10_14 register.mp4"
```

If the hard joins feel jumpy, use `xfade` / `acrossfade` instead (dip to black,
`duration=0.2`).

## 6. Deliver

- The MP4: `runs/W_11042026/supercut/F2 Wed 11_04 -- B supercut 10_14 register.mp4`.
  **Don't commit the video** (too big for git); just give David the path.
- `runs/W_11042026/supercut/CUT_LIST.md`: bite, source in–out in the 10/14 video,
  verbatim outcue, what's on screen. Also write a CMX3600 EDL (`supercut.edl`) so the
  editor can rebuild it in Premiere/Resolve from their master.
- Commit `CUT_LIST.md`, `supercut.edl` and `transcript_1014.json` on a new branch and push.

## 7. Where it goes in the 11/4 bible (for the script writer)

Story B, right after the lawsuit clip (B1, GMA) and before Lori (B2). Suggested toss:

> WE WARNED YOU ABOUT THIS THREE WEEKS AGO.
> (((PLAY SUPERCUT — 10/14 SHOW)))
> NOW THE FTC AND 20 STATES ARE SUING.

**Don't write "we're making a difference."** It implies our 10/14 story caused the FTC
suit, and that suit came out of a multi-year investigation. "We warned you" is true and
lands the same.

Note for the room: this softens the B repeat-risk Decision in the 11/4 outline (the 10/14
B covered the same shelf-vs-register issue). The supercut makes the repeat a callback.

## Where the 11/4 run stands (context)

- Outline w/ videos done: `runs/W_11042026/Outline F2 11_04.docx` (8 PICK verified, 4
  TikTok MANUAL). Open items in `runs/W_11042026/OPEN.md`.
- The local session can also do what the cloud can't: pull the 4 TikToks (A1, A2, B2, C2)
  and check the show plan's in/out points with Whisper. TikTok usually answers from a home
  connection.
