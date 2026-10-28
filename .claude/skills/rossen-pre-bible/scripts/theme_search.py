#!/usr/bin/env python3
"""Theme-first search: run a theme's queries across time windows and merge the results.

Usage:
  python3 scripts/theme_search.py --list
  python3 scripts/theme_search.py --theme phishing                    # windows: year,any
  python3 scripts/theme_search.py --theme mail --windows month,year,any
  python3 scripts/theme_search.py --queries "patient portal scam" "fake hospital bill text"

Reads YouTube search sorted by view count. Read the output for CASES and HEAT inside a
theme, not as the story list. Upload dates shown are YouTube's approximate ages;
confirm a video's exact date with scripts/video_info.sh or its page before citing it.

Set YTDLP_ARGS for extra yt-dlp flags (e.g. YTDLP_ARGS="--no-check-certificates").
"""
import argparse, datetime, json, os, re, shlex, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
WINDOWS = {"week": "CAMSAggD", "month": "CAMSAggE", "year": "CAMSAggF", "any": "CAM%253D"}
RELEVANT = re.compile(r"scam|fraud|warn|steal|stole|theft|thie|fake|alert|hack|police|lost|victim|arrest|drain|con\b|crook|target|spy|track|record|camera|exposed|investigat", re.I)
SKIP_CHANNELS = {"rossen reports", "scammer payback", "kitboga", "penguinz0", "jim browning", "pleasant green"}

def ytdlp():
    return shutil.which("yt-dlp") or os.path.join(HERE, ".venv", "bin", "yt-dlp")

def search(query, window, n):
    url = "https://www.youtube.com/results?search_query=" + query.replace(" ", "+") + "&sp=" + WINDOWS[window]
    cmd = [ytdlp(), "--flat-playlist", "--playlist-end", str(n), "-J", "--extractor-args", "youtubetab:approximate_date"] + shlex.split(os.environ.get("YTDLP_ARGS", "")) + [url]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=120).stdout
        entries = (json.loads(out) or {}).get("entries") or []
    except Exception as e:
        print(f"  ! search failed: {query} ({window}): {e}", file=sys.stderr)
        return []
    rows = []
    for e in entries:
        if not e or not e.get("id"):
            continue
        rows.append({"id": e["id"], "title": e.get("title") or "", "channel": e.get("channel") or e.get("uploader") or "",
                     "views": e.get("view_count") or 0, "dur": e.get("duration") or 0, "ts": e.get("timestamp"), "window": window, "query": query})
    return rows

def norm(t):
    return re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()[:50]

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--theme", action="append", help="theme id from theme_queries.json (repeatable)")
    ap.add_argument("--queries", nargs="+", help="ad-hoc queries instead of / in addition to a theme")
    ap.add_argument("--windows", default="year,any", help="comma list of week,month,year,any (default year,any)")
    ap.add_argument("--per-query", type=int, default=20, help="results read per query and window")
    ap.add_argument("--top", type=int, default=25, help="rows printed per theme")
    ap.add_argument("--min-views", type=int, default=20000)
    ap.add_argument("--no-filter", action="store_true", help="keep titles without scam/threat words")
    ap.add_argument("--list", action="store_true", help="list themes and their queries")
    a = ap.parse_args()

    bank = json.load(open(os.path.join(HERE, "theme_queries.json")))
    if a.list:
        for k, v in bank.items():
            print(f"{k}: " + " | ".join(v))
        return
    jobs = {}
    for t in a.theme or []:
        if t not in bank:
            sys.exit(f"Unknown theme '{t}'. Run --list.")
        jobs[t] = bank[t]
    if a.queries:
        jobs["ad-hoc"] = a.queries
    if not jobs:
        sys.exit("Give --theme or --queries (or --list).")
    windows = [w.strip() for w in a.windows.split(",") if w.strip()]
    for w in windows:
        if w not in WINDOWS:
            sys.exit(f"Unknown window '{w}'. Use week, month, year, any.")

    for theme, queries in jobs.items():
        tasks = [(q, w) for q in queries for w in windows]
        with ThreadPoolExecutor(max_workers=4) as ex:
            results = list(ex.map(lambda qw: search(qw[0], qw[1], a.per_query), tasks))
        merged, seen_titles = {}, {}
        for rows in results:
            for r in rows:
                if r["channel"].lower() in SKIP_CHANNELS or r["views"] < a.min_views or (r["dur"] and r["dur"] < 60) \
                        or (not a.no_filter and not RELEVANT.search(r["title"])):
                    continue
                key = r["id"]
                nt = norm(r["title"])
                if nt in seen_titles and seen_titles[nt] != key:
                    key = seen_titles[nt]          # syndicated copy: keep one row, note it
                    merged[key]["copies"] += 1
                    continue
                seen_titles[nt] = key
                if key in merged:
                    m = merged[key]
                    m["windows"].add(r["window"]); m["queries"].add(r["query"])
                    m["views"] = max(m["views"], r["views"])
                else:
                    merged[key] = {**r, "windows": {r["window"]}, "queries": {r["query"]}, "copies": 0}
        rows = sorted(merged.values(), key=lambda r: r["views"], reverse=True)[: a.top]
        recent = sum(1 for r in merged.values() if r["windows"] & {"week", "month"})
        print(f"=== {theme}: {len(merged)} videos over {a.min_views:,} views ({recent} from this month or week) | windows: {','.join(windows)}")
        for r in rows:
            heat = "HEAT " if r["views"] >= 200_000 else "     "
            new = "NEW " if r["windows"] & {"week", "month"} else "    "
            cp = f" (+{r['copies']} similar)" if r["copies"] else ""
            when = datetime.datetime.fromtimestamp(r["ts"], datetime.timezone.utc).strftime("~%b %Y") if r.get("ts") else "   ?    "
            print(f"{heat}{new}{r['views']:>10,} | {when} | {r['id']} | {r['channel'][:26]:26} | {r['title'][:88]}{cp}")
        print("    HEAT = 200K+ (Ryan's local-news bar; creators need 500K). NEW = found in the month/week window.")
        print("    ~Mon YYYY is YouTube's approximate age (\"8 months ago\"). Confirm the exact date (scripts/video_info.sh or the page) before citing.\n")

if __name__ == "__main__":
    main()
