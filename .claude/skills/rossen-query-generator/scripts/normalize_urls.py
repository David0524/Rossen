#!/usr/bin/env python3
"""normalize_urls.py — find and repair-where-possible the URL casing corruption
that silently drops rows from any recall eval.

Usage:
    python3 scripts/normalize_urls.py reference/aired_examples.md
    python3 scripts/normalize_urls.py file.csv --write        # edit in place
    python3 scripts/normalize_urls.py file.md --ids-only      # list broken IDs

**The corruption is lossy for video IDs and this script does not pretend
otherwise.** YouTube IDs and TikTok handles are case-sensitive; once
`I3667lq1L2o` has been uppercased to `I3667LQ1L2O` the original case is gone and
no amount of string manipulation recovers it. What this script does:

  - lowercases the parts that ARE safe: scheme, host, and path words on hosts
    whose paths are case-insensitive
  - leaves case-sensitive ID segments alone and reports them as UNRECOVERABLE,
    so they get re-sourced by hand instead of silently failing an eval
  - prints a count, because "roughly half" is the symptom to recognize

Re-source an unrecoverable YouTube ID by searching its title; the video is
usually still up and the aired-examples row carries enough context to find it.
"""

import argparse
import re
import sys

URL = re.compile(r"(?i)\bhttps?://[^\s`)\]<>\"']+")
# hosts whose path/query carries case-sensitive identifiers
CASE_SENSITIVE = {
    "youtube.com": r"[?&]v=([A-Za-z0-9_-]{6,})",
    "youtu.be": r"youtu\.be/([A-Za-z0-9_-]{6,})",
    "tiktok.com": r"@([A-Za-z0-9._]+)",
    "instagram.com": r"/(?:reels?|p)/([A-Za-z0-9_-]{6,})",
}


def looks_uppercased(url):
    """A URL whose scheme is uppercase was almost certainly whole-string upcased."""
    return url[:5].upper() == url[:5] and url[:4].upper() == "HTTP" \
        and url[:4] != "http"


def safe_lower(url):
    """Lowercase scheme + host, leave the rest untouched."""
    m = re.match(r"(?i)(https?://)([^/]+)(.*)", url)
    if not m:
        return url
    return m.group(1).lower() + m.group(2).lower() + m.group(3)


def sensitive_ids(url):
    out = []
    low = url.lower()
    for host, pat in CASE_SENSITIVE.items():
        if host in low:
            for m in re.finditer(pat, url, re.I):
                out.append((host, m.group(1)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--write", action="store_true",
                    help="apply the safe lowercasing in place")
    ap.add_argument("--ids-only", action="store_true")
    a = ap.parse_args()

    try:
        text = open(a.path, encoding="utf-8").read()
    except OSError as exc:
        print(f"could not read {a.path}: {exc}", file=sys.stderr)
        sys.exit(2)

    urls = URL.findall(text)
    broken = [u for u in urls if looks_uppercased(u)]
    unrecoverable, repaired = [], 0
    new_text = text

    for u in broken:
        ids = sensitive_ids(u)
        fixed = safe_lower(u)
        if fixed != u:
            new_text = new_text.replace(u, fixed)
            repaired += 1
        for host, ident in ids:
            if ident.upper() == ident and not ident.isdigit():
                unrecoverable.append((host, ident, fixed))

    if a.ids_only:
        for host, ident, u in unrecoverable:
            print(f"{host}\t{ident}\t{u}")
        sys.exit(1 if unrecoverable else 0)

    print(f"\n{a.path}")
    print("=" * 68)
    print(f"  URLs found                 {len(urls)}")
    print(f"  whole-string uppercased    {len(broken)}"
          + (f"  ({round(100*len(broken)/len(urls))}% — 'roughly half' is the "
             f"symptom)" if urls else ""))
    print(f"  scheme/host safely lowered {repaired}")
    print(f"  UNRECOVERABLE IDs          {len(unrecoverable)}\n")

    if unrecoverable:
        print("  These IDs are case-sensitive and their original case is gone.")
        print("  Re-source each by title; do not guess at casing, and do not")
        print("  count these rows as eval misses — they are data-quality drops.\n")
        for host, ident, u in unrecoverable:
            print(f"    {host:16} {ident}")
        print()

    if a.write and repaired:
        open(a.path, "w", encoding="utf-8").write(new_text)
        print(f"  wrote scheme/host lowercasing to {a.path}\n")
    elif repaired:
        print(f"  (dry run — pass --write to apply)\n")

    sys.exit(1 if unrecoverable else 0)


if __name__ == "__main__":
    main()
