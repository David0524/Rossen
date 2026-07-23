"""CLI.

    python -m rossen_harvest harvest queries.json --out candidates.json
    python -m rossen_harvest eval queries.json rossen_eval_worksheet.csv

`queries.json` is the query generator's output: a list of beat objects,
each with beat_id, clip_role, orientation, and a `queries` dict of
register -> [query strings].

EVAL is Task 1. It answers the only metric that matters right now:
does the clip that actually aired appear in the top thirty results for
at least one generated query, and which register got it there.
"""
from __future__ import annotations

import argparse
import csv
import json
import logging
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

from .brave import BraveBackend, from_brave
from .cache import Cache
from .candidates import Candidate
from .dedupe import dedupe_by_beat
from .youtube import DEFAULT_CONCURRENCY, YouTubeBackend, harvest_beat

log = logging.getLogger("rossen_harvest")

# Beats needing coverage YouTube cannot give: network/affiliate video on the
# outlet's own site, and the vertical platforms whose search is otherwise
# closed. Brave is the leg that reaches these.
BRAVE_PLATFORMS = {"news_web", "tiktok", "instagram", "facebook", "x", "reddit"}

# Which registers each Brave endpoint runs.
#
# The WEB endpoint indexes ordinary pages, which is where a native TikTok,
# Instagram or X *post* actually lives, as well as network/affiliate video
# on the outlet's own site. So it runs the noun-heavy news/anchor strings
# AND the emotional victim/platform strings that name a specific social post.
#
# The VIDEO endpoint is YouTube-heavy — it reliably surfaces YouTube and
# Shorts but rarely a native TikTok/IG post — so it takes the short-form
# and confrontation registers to widen YouTube/Shorts discovery.
#
# The two overlap on victim/platform on purpose: a vertical beat should get
# both a shot at the native social post (web) and at YouTube coverage (video).
BRAVE_WEB_REGISTERS = {"anchor", "news", "victim", "platform"}
BRAVE_VIDEO_REGISTERS = {"platform", "shorts", "victim", "confrontation"}


def _beat_needs_brave(beat: dict) -> bool:
    plats = set(beat.get("platforms") or [])
    return beat.get("orientation") == "vertical" or bool(plats & BRAVE_PLATFORMS)

_YT_ID = re.compile(
    r"(?:v=|/shorts/|youtu\.be/|/embed/)([A-Za-z0-9_-]{11})"
)


def youtube_id(url: str) -> str | None:
    m = _YT_ID.search(url or "")
    return m.group(1) if m else None


# --------------------------------------------------------------------- harvest

def cmd_harvest(args) -> int:
    beats = json.loads(Path(args.queries).read_text())
    if isinstance(beats, dict):
        beats = [beats]

    cache = Cache(args.db)
    yt = YouTubeBackend(cache=cache, limit=args.limit)

    # Brave leg: web (network/affiliate sites) and video (social/short-form).
    brave_key = os.environ.get("BRAVE_API_KEY")
    use_brave = bool(brave_key) and not args.no_brave
    web = vid = None
    if use_brave:
        web = BraveBackend(brave_key, cache=cache, limit=args.brave_count, kind="web")
        vid = BraveBackend(brave_key, cache=cache, limit=args.brave_count, kind="video")

    needs_brave = [b for b in beats if _beat_needs_brave(b)]
    if needs_brave and not use_brave:
        why = "BRAVE_API_KEY is not set" if not brave_key else "Brave disabled with --no-brave"
        log.warning(
            "DEGRADED: %d of %d beats need web/social/vertical coverage but %s. "
            "Running YouTube-only — no TikTok, Instagram, X, Facebook, Reddit, "
            "off-YouTube network video, and no coverage at all for vertical beats.",
            len(needs_brave), len(beats), why,
        )

    all_cands: list[Candidate] = []
    for beat in beats:
        if beat.get("orientation") != "vertical":
            all_cands.extend(
                harvest_beat(beat, yt, concurrency=args.concurrency)
            )
        elif not use_brave:
            log.info("skipping %s: vertical and no Brave backend", beat["beat_id"])

        if use_brave and _beat_needs_brave(beat):
            all_cands.extend(harvest_beat(
                beat, web, normalize=from_brave, registers=BRAVE_WEB_REGISTERS,
                cap=args.brave_cap, concurrency=2, jitter=(0, 0),
            ))
            all_cands.extend(harvest_beat(
                beat, vid, normalize=from_brave, registers=BRAVE_VIDEO_REGISTERS,
                cap=args.brave_cap, concurrency=2, jitter=(0, 0),
            ))

    kept = dedupe_by_beat(all_cands)
    cache.save_candidates(kept)

    print(f"{len(all_cands)} raw -> {len(kept)} after dedupe "
          f"across {len({c.beat_id for c in kept})} beats "
          f"({'youtube + brave' if use_brave else 'youtube only'})")

    by_platform: dict[str, int] = defaultdict(int)
    for c in kept:
        by_platform[c.platform] += 1
    if by_platform:
        print("  by platform: " + " · ".join(
            f"{p} {n}" for p, n in sorted(by_platform.items(), key=lambda x: -x[1])))

    for beat_id in sorted({c.beat_id for c in kept}):
        n = sum(1 for c in kept if c.beat_id == beat_id)
        print(f"  {beat_id}: {n}")

    if args.out:
        Path(args.out).write_text(
            json.dumps([c.to_row() for c in kept], indent=2, default=str)
        )
        print(f"wrote {args.out}")
    return 0


# ------------------------------------------------------------------------ eval

def cmd_eval(args) -> int:
    beats = {b["beat_id"]: b for b in json.loads(Path(args.queries).read_text())}

    truth: dict[str, dict] = {}
    with open(args.worksheet, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            vid = youtube_id(row.get("url", ""))
            if vid:
                truth[row["beat_id"]] = {
                    "video_id": vid,
                    "url": row["url"],
                    "role": row.get("clip_role_CONFIRM") or "?",
                    "orientation": row.get("orientation", ""),
                }

    cache = Cache(args.db)
    backend = YouTubeBackend(cache=cache, limit=args.limit)

    results = []
    skipped = []

    for beat_id, target in truth.items():
        beat = beats.get(beat_id)
        if not beat:
            skipped.append((beat_id, "no queries generated"))
            continue

        cands = harvest_beat(beat, backend, concurrency=args.concurrency)

        hits = [c for c in cands if c.video_id == target["video_id"]]
        if hits:
            best = min(hits, key=lambda c: c.rank or 999)
            results.append({
                "beat_id": beat_id, "hit": True,
                "role": beat.get("clip_role", target["role"]),
                "register": best.register, "rank": best.rank,
                "query": best.query_that_found_it,
                "all_registers": sorted({h.register for h in hits}),
                "n_queries": sum(len(v) for v in beat.get("queries", {}).values()),
            })
        else:
            results.append({
                "beat_id": beat_id, "hit": False,
                "role": beat.get("clip_role", target["role"]),
                "register": None, "rank": None, "query": None,
                "all_registers": [],
                "n_queries": sum(len(v) for v in beat.get("queries", {}).values()),
                "url": target["url"],
            })

    _report(results, skipped)

    if args.out:
        Path(args.out).write_text(json.dumps(results, indent=2))
        print(f"\nwrote {args.out}")
    return 0


def _report(results: list[dict], skipped: list[tuple[str, str]]) -> None:
    if not results:
        print("no rows evaluated")
        return

    n = len(results)
    hits = [r for r in results if r["hit"]]
    print(f"\n{'='*60}\nRECALL @30: {len(hits)}/{n} = {len(hits)/n:.0%}\n{'='*60}")

    # by register: which one FIRST surfaced the clip, and which COULD have
    first = defaultdict(int)
    could = defaultdict(int)
    for r in hits:
        first[r["register"]] += 1
        for reg in r["all_registers"]:
            could[reg] += 1

    print("\nby register")
    print(f"  {'register':<12} {'best rank':>10} {'any rank':>10}")
    for reg in sorted(set(first) | set(could)):
        print(f"  {reg:<12} {first[reg]:>10} {could[reg]:>10}")

    # unique contribution: hits ONLY that register found
    print("\nunique contribution (removing this register loses the clip)")
    for reg in sorted(could):
        uniq = sum(1 for r in hits if r["all_registers"] == [reg])
        print(f"  {reg:<12} {uniq}")

    # by role
    by_role = defaultdict(lambda: [0, 0])
    for r in results:
        by_role[r["role"]][1] += 1
        if r["hit"]:
            by_role[r["role"]][0] += 1
    print("\nby clip role")
    for role, (h, t) in sorted(by_role.items()):
        print(f"  {role:<32} {h}/{t}")

    # rank distribution
    ranks = sorted(r["rank"] for r in hits if r["rank"])
    if ranks:
        top5 = sum(1 for x in ranks if x <= 5)
        top10 = sum(1 for x in ranks if x <= 10)
        print(f"\nrank of aired clip: median {ranks[len(ranks)//2]}, "
              f"top-5 {top5}/{len(ranks)}, top-10 {top10}/{len(ranks)}")

    misses = [r for r in results if not r["hit"]]
    if misses:
        print(f"\nMISSES ({len(misses)}) — these are the glossary's homework")
        for r in misses:
            print(f"  {r['beat_id']:<12} {r['role']:<28} {r.get('url','')}")

    if skipped:
        print(f"\nskipped ({len(skipped)})")
        for beat_id, why in skipped:
            print(f"  {beat_id}: {why}")

    print("\ninterpretation: >70% build the harvest on it. "
          "<50% fix the glossary first.")


# ------------------------------------------------------------------------ main

def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="rossen_harvest")
    p.add_argument("-v", "--verbose", action="store_true")
    p.add_argument("--db", default="harvest.db")
    p.add_argument("--limit", type=int, default=30)
    p.add_argument("--concurrency", type=int, default=DEFAULT_CONCURRENCY)
    sub = p.add_subparsers(dest="cmd", required=True)

    h = sub.add_parser("harvest", aliases=["search"],
                       help="run queries across YouTube + Brave, dedupe, store")
    h.add_argument("queries")
    h.add_argument("--out")
    h.add_argument("--no-brave", action="store_true",
                   help="YouTube only, skip the Brave web/social/vertical leg")
    h.add_argument("--brave-count", type=int, default=20,
                   help="results per Brave request (max 20)")
    h.add_argument("--brave-cap", type=int, default=8,
                   help="max queries per beat per Brave endpoint (protects quota)")
    h.set_defaults(func=cmd_harvest)

    e = sub.add_parser("eval", help="Task 1: measure recall@30")
    e.add_argument("queries")
    e.add_argument("worksheet")
    e.add_argument("--out")
    e.set_defaults(func=cmd_eval)

    args = p.parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(message)s",
    )
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
