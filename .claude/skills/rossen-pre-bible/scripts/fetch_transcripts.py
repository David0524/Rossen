#!/usr/bin/env python3
"""
Download transcripts for Rossen Reports videos (or any YouTube video) into transcripts/rossen-reports/.

Usage:
    python3 scripts/fetch_transcripts.py VIDEO_ID [VIDEO_ID ...]
    python3 scripts/fetch_transcripts.py --missing     # every ID in coverage/channel-uploads.txt we don't have yet

Notes:
  - Skips the retail "Discontinuing / Items That WON'T LAST / Deals" videos when using --missing. They aren't scam shows.
  - YouTube rate-limits after about 50 requests ("IpBlocked"). Wait a few hours and rerun. It picks up where it left off.
"""
import os, re, sys, warnings
warnings.filterwarnings("ignore")
from youtube_transcript_api import YouTubeTranscriptApi

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "references", "transcripts")
LIST = os.path.join(ROOT, "references", "channel-uploads.txt")
RETAIL = re.compile(r"discontinuing|items that won.t last|deals you need|hidden deals|prices just|price gap|slashed prices|only sells these|just added|kirkland|who really makes", re.I)

def wanted_from_list():
    rows = []
    for line in open(LIST, encoding="utf-8"):
        if line.startswith("#") or "|" not in line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 5 or not re.match(r"^\d{8}$", parts[0]):
            continue
        date, vid, title = parts[0], parts[2], parts[-1]
        if RETAIL.search(title):
            continue
        if not os.path.exists(os.path.join(OUT, vid + ".txt")):
            rows.append((date, vid, title))
    return rows

def main():
    os.makedirs(OUT, exist_ok=True)
    args = sys.argv[1:]
    if not args:
        print(__doc__); return
    todo = wanted_from_list() if args == ["--missing"] else [("", v, "") for v in args]
    api = YouTubeTranscriptApi()
    ok = fail = 0
    for date, vid, title in todo:
        try:
            t = api.fetch(vid, languages=["en", "en-US"])
            with open(os.path.join(OUT, vid + ".txt"), "w", encoding="utf-8") as fh:
                fh.write(f"# {date} {title}\n")
                for s in t:
                    m, sec = divmod(int(s.start), 60)
                    fh.write(f"[{m:02d}:{sec:02d}] {s.text}\n")
            ok += 1; print("OK  ", vid, date, title[:60])
        except Exception as e:
            fail += 1; print("FAIL", vid, date, title[:60], "->", type(e).__name__)
    print(f"\nfetched {ok}, failed {fail}")

if __name__ == "__main__":
    main()
