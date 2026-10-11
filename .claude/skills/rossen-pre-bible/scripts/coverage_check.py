#!/usr/bin/env python3
"""
Has Rossen Reports already covered this? Searches every transcript, and every archived bible, for a topic.

Usage:
    python3 scripts/coverage_check.py "gold bar|bullion|courier"
    python3 scripts/coverage_check.py "squatter|fake lease" --context
    python3 scripts/coverage_check.py "deed|title theft" --min 2 --months 3

The first argument is a search pattern. Use | between synonyms. It is a regular expression, case-insensitive.
  --context   print the surrounding lines for the first few hits in each show, so you can tell a real segment from a passing mention
  --min N     only list shows with at least N matching lines (default 3). One or two hits is usually a passing mention or a deals-block product.
  --months N  flag shows newer than N months as RECENT (default 3). Our rule is no repeat inside three months.

How to read the result:
  10+ hits over several minutes = a real segment. Read it with --context before you pitch.
  3 to 9 hits = probably a B or C story or a long aside.
  Nothing = open, BUT check anything that aired after the newest transcript, and ask someone who was there.
  Watch for false matches (example: "tractor" matches "contractor", "letter" matches "newsletter").
"""
import os, re, sys, glob, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TX = os.path.join(ROOT, "references", "transcripts")
BIB = os.path.join(ROOT, "references", "bibles")   # aired bibles (May-Jul 2026), from the producer's Bible Archive

def main():
    args = sys.argv[1:]
    if not args or args[0].startswith("--"):
        print(__doc__); return
    pat = re.compile(args[0], re.I)
    context = "--context" in args
    min_hits = int(args[args.index("--min") + 1]) if "--min" in args else 3
    months = int(args[args.index("--months") + 1]) if "--months" in args else 3
    cutoff = (datetime.date.today() - datetime.timedelta(days=30.4 * months)).strftime("%Y%m%d")

    found = 0
    files = sorted(glob.glob(os.path.join(TX, "*.txt")), reverse=True) + sorted(glob.glob(os.path.join(BIB, "*.txt")), reverse=True)
    for f in files:
        lines = open(f, encoding="utf-8").read().split("\n")
        head = lines[0].lstrip("# ").strip()
        date = head[:8] if re.match(r"^\d{8}", head) else "????????"
        body = lines[1:]
        text = [re.sub(r"^\[\d\d:\d\d\] ", "", l) for l in body]
        is_bible = os.path.dirname(f) == BIB
        stamp = [("line %d" % (i + 2)) if is_bible else l[:7] for i, l in enumerate(body)]
        idx = [i for i, l in enumerate(text) if pat.search(l)]
        if len(idx) < min_hits:
            continue
        found += 1
        terms = sorted({m.group(0).lower() for l in text for m in pat.finditer(l)})[:8]
        flag = "RECENT" if date >= cutoff else "older "
        vid = os.path.basename(f)[:-4]
        print(f"{flag} {head[:90]}")
        print(f"       {len(idx)} hits, {stamp[idx[0]]} to {stamp[idx[-1]]}, matched: {terms}")
        print(f"       references/bibles/{vid}.txt" if is_bible else f"       https://www.youtube.com/watch?v={vid}")
        if context:
            shown = set(); n = 0
            for i in idx:
                if i in shown: continue
                a, b = max(0, i - 8), min(len(text), i + 9)
                shown.update(range(a, b)); n += 1
                print(f"       --- {stamp[i]}: " + " ".join(text[a:b])[:600])
                if n >= 3: break
        print()
    if not found:
        print("No show has", min_hits, "or more matching lines. Looks open.")
        print("Still check: (1) anything aired after the newest transcript, (2) the story board in references/producer-kit/ (a snapshot; ask for the live one), (3) shows before 2026-03-18 and the Mar 20-Apr 15 gap, which are not in the kit (bibles cover May-Jul only).")

if __name__ == "__main__":
    main()
