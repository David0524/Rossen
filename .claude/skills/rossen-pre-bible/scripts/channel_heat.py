#!/usr/bin/env python3
"""Heat-first scan: what is exploding RIGHT NOW on channels that share our audience.

Pulls recent uploads from audience-matched creators and news channels, keeps the
last N days, filters to consumer-threat titles, and ranks by views. Run this FIRST
every week, before theme searches. The top rows are the first candidate pool.

Usage:
  python3 scripts/channel_heat.py                 # default channel list, last 75 days
  python3 scripts/channel_heat.py --days 45 --top 40
  python3 scripts/channel_heat.py --add SomeHandle AnotherHandle
Set YTDLP_ARGS for extra yt-dlp flags (e.g. "--no-check-certificates").
Views and ages are YouTube's rounded/approximate figures; confirm before citing.
"""
import argparse, datetime, json, os, re, shlex, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

# Audience-matched creators first (their hits are the strongest signal), then news.
CHANNELS = ["EpicRealEstate", "HolySchmidt", "BoydClewis", "850ClubCredit", "ScamsAndFrauds",
            "PleasantGreen", "Payetteforward", "TrevorNace", "ThioJoe", "LawByMike", "AARP",
            "InsideEdition", "TODAY", "NBCNews", "CBSNews", "ABCNews", "CNBC", "WSJ",
            "ABC7", "ABC7NY", "NBCLA", "CBSNewYork", "FOX5Atlanta", "WSBTV", "WPLGLocal10",
            "WFTV", "WCVB", "9News", "KARE11", "FOX2StLouis"]
THREAT = re.compile(r"scam|fraud|steal|stole|drain|hack|spy|track|warning|warn|alert|thie|fake|trap|"
                    r"don.t|never|stop|police|arrest|lost|victim|danger|setting|turn off|check your|"
                    r"your bank|your phone|your card|your car|your home|homeowner|seniors|retire|paid off", re.I)

def ytdlp():
    return shutil.which("yt-dlp") or os.path.join(os.path.dirname(__file__), ".venv", "bin", "yt-dlp")

def pull(h, n):
    cmd = [ytdlp(), "--flat-playlist", "--playlist-end", str(n), "-J", "--extractor-args",
           "youtubetab:approximate_date"] + shlex.split(os.environ.get("YTDLP_ARGS", "")) + \
          [f"https://www.youtube.com/@{h}/videos"]
    try:
        d = json.loads(subprocess.run(cmd, capture_output=True, text=True, timeout=180).stdout or "{}")
        return h, d.get("channel") or h, d.get("entries") or []
    except Exception:
        return h, h, []

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--days", type=int, default=75)
    ap.add_argument("--top", type=int, default=50)
    ap.add_argument("--per-channel", type=int, default=120)
    ap.add_argument("--add", nargs="*", default=[])
    ap.add_argument("--all-titles", action="store_true", help="skip the threat-word filter")
    a = ap.parse_args()
    now = datetime.datetime.now(datetime.timezone.utc)
    rows, empty = [], []
    with ThreadPoolExecutor(6) as ex:
        for h, name, ents in ex.map(lambda h: pull(h, a.per_channel), CHANNELS + a.add):
            if not ents:
                empty.append(h)
            for e in ents:
                ts, title = e.get("timestamp"), e.get("title") or ""
                if not ts or (e.get("duration") or 0) < 60:
                    continue
                age = (now - datetime.datetime.fromtimestamp(ts, datetime.timezone.utc)).days
                if age <= a.days and (a.all_titles or THREAT.search(title)):
                    rows.append((e.get("view_count") or 0, age, name, e.get("id"), title))
    rows.sort(reverse=True)
    print(f"=== Heat scan: last {a.days} days, {len(rows)} threat-titled uploads")
    for v, age, name, vid, t in rows[: a.top]:
        flag = "HEAT " if v >= 500_000 else ("LOCAL" if v >= 200_000 else "     ")
        print(f"{flag} {v:>10,} | ~{age:>3}d | {name[:22]:22} | {vid} | {t[:95]}")
    if empty:
        print(f"\n(no data from: {', '.join(empty)} — handle may be wrong)")
    print("\nRead it for TOPICS that several channels are hitting at once. Ignore politics and crime-of-the-day.")

if __name__ == "__main__":
    main()
