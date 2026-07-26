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
import concurrent.futures as cf
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
from .shorts import (
    LANDSCAPE,
    UNKNOWN,
    VERTICAL,
    is_short,
    shorts_web_queries,
    verify_orientation,
)
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
#
# `shorts_web` is a synthetic register built by `_with_shorts_web` — the
# `site:youtube.com/shorts` forms of the Shorts strings. It runs on the web
# endpoint because it constrains on a URL path, which the video endpoint
# cannot express. See `shorts.shorts_web_queries` for why the `#shorts`
# suffix alone was not enough.
BRAVE_WEB_REGISTERS = {"anchor", "news", "victim", "platform", "shorts_web"}
BRAVE_VIDEO_REGISTERS = {"platform", "shorts", "victim", "confrontation"}


def _beat_needs_brave(beat: dict) -> bool:
    plats = set(beat.get("platforms") or [])
    return beat.get("orientation") == "vertical" or bool(plats & BRAVE_PLATFORMS)


def _wants_shorts(beat: dict) -> bool:
    return (
        "shorts" in (beat.get("platforms") or [])
        or beat.get("orientation") == "vertical"
        or bool(beat.get("queries", {}).get("shorts"))
    )


def _with_shorts_web(beat: dict) -> dict:
    """Add the `site:youtube.com/shorts` register, without mutating the beat.

    Seeded from the `shorts` strings and topped up from `platform`, since
    the Shorts dialect is deliberately short and a couple of noun-heavier
    strings widen the path-constrained search cheaply.
    """
    if not _wants_shorts(beat):
        return beat
    queries = beat.get("queries", {})
    seed = list(queries.get("shorts") or []) + list(queries.get("platform") or [])[:2]
    web = shorts_web_queries(seed)
    if not web:
        return beat
    out = dict(beat)
    out["queries"] = {**queries, "shorts_web": web}
    return out

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
                _with_shorts_web(beat), web, normalize=from_brave,
                registers=BRAVE_WEB_REGISTERS,
                cap=args.brave_cap, concurrency=2, jitter=(0, 0),
            ))
            all_cands.extend(harvest_beat(
                beat, vid, normalize=from_brave, registers=BRAVE_VIDEO_REGISTERS,
                cap=args.brave_cap, concurrency=2, jitter=(0, 0),
            ))

    kept = dedupe_by_beat(all_cands)

    if not args.no_verify_orientation:
        kept = _gate_orientation(
            kept, beats, drop=args.drop_landscape, concurrency=args.concurrency
        )

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


VERTICAL_PLATFORMS = {"tiktok", "instagram", "x", "facebook"}


def cmd_captions(args) -> int:
    """Step 5: fetch a transcript for every shortlisted clip.

    YouTube goes through `transcripts.fetch_many` (auto-captions via
    yt-dlp — metadata only, no media). The vertical platforms ship no
    caption track at all, so they route to `vertical_transcribe`, which
    downloads and runs faster-whisper locally. Both return the same
    `Transcript` shape, so pass two's `.find()` / `.segment()` outcue
    verification works identically either way.

    A clip whose transcript comes back None is recorded as null rather
    than dropped — the grader is required to demote it, not guess at
    what it said.
    """
    from .transcripts import fetch_many

    shortlist = json.loads(Path(args.shortlist).read_text())
    cache = Cache(args.db)

    yt_ids, vertical_urls, meta = [], [], {}
    for c in shortlist:
        platform = (c.get("platform") or "").lower()
        key = c.get("video_id") or c.get("url")
        meta[key] = c
        if platform in VERTICAL_PLATFORMS:
            vertical_urls.append(c["url"])
        elif c.get("video_id"):
            yt_ids.append(c["video_id"])
        else:
            log.warning("no video_id and not a vertical platform, skipping: %s",
                        c.get("url"))

    results: dict[str, object] = {}

    if yt_ids:
        for vid, t in fetch_many(sorted(set(yt_ids)), cache=cache,
                                 concurrency=args.concurrency).items():
            results[vid] = t

    if vertical_urls:
        if args.no_whisper:
            log.warning("%d vertical clips need Whisper but --no-whisper is set; "
                        "their outcues cannot be verified", len(vertical_urls))
            for u in vertical_urls:
                results[u] = None
        else:
            try:
                from .vertical_transcribe import fetch_many_vertical
                for url, t in fetch_many_vertical(
                    sorted(set(vertical_urls)), cache=cache,
                    model_size=args.whisper_model,
                ).items():
                    results[url] = t
            except ImportError as exc:
                log.warning("faster-whisper unavailable (%s) — %d vertical clips "
                            "get no transcript. Flag their outcues unverified "
                            "rather than inventing one.", exc, len(vertical_urls))
                for u in vertical_urls:
                    results[u] = None

    out = {}
    for key, t in results.items():
        c = meta.get(key, {})
        if t is None:
            out[key] = None
            continue
        out[key] = {
            "video_id": getattr(t, "video_id", key),
            "url": c.get("url"),
            "beat_id": c.get("beat_id"),
            "source": t.source,
            "duration": t.duration,
            "cues": [{"start": q.start, "end": q.end, "text": q.text} for q in t.cues],
            "prompt": t.as_prompt(),
        }

    got = sum(1 for v in out.values() if v)
    print(f"captions: {got}/{len(out)} clips have a transcript")
    missing = [k for k, v in out.items() if not v]
    if missing:
        print("  no transcript (demote, do not guess): " + ", ".join(missing))

    Path(args.out).write_text(json.dumps(out, indent=2, default=str))
    print(f"wrote {args.out}")
    return 0


def _gate_orientation(
    cands: list[Candidate],
    beats: list[dict],
    *,
    drop: bool = False,
    concurrency: int = DEFAULT_CONCURRENCY,
) -> list[Candidate]:
    """Verify orientation from pixels for candidates on vertical beats.

    This is the vertical postmortem fix. Previously a sub-75-second YouTube
    video could be asserted vertical on duration alone, and a 1920x1080
    landscape clip shipped against a vertical beat. Nothing here reads
    duration: orientation comes from `shorts.verify_orientation`, which
    reads pixels, and format from `shorts.is_short`, which reads whether
    the `/shorts/` URL resolves.

    Only YouTube candidates are checked. TikTok and Instagram permalinks
    need their own probe (both platforms serve landscape video into
    portrait slots — the smoke test found a 640x360 clip on a `/reel/`
    URL), but that costs a media fetch, so it belongs in the grader's
    shortlist pass, not here at 244-candidates-per-beat scale.

    "unknown" is never treated as a pass. With `drop`, only candidates
    positively verified landscape are removed; unverified ones survive
    flagged, because a network wobble must not silently shrink the funnel.
    """
    vertical_beats = {
        b["beat_id"] for b in beats if b.get("orientation") == VERTICAL
    }
    targets = [
        c for c in cands
        if c.beat_id in vertical_beats and c.platform == "youtube" and c.video_id
    ]
    if not targets:
        return cands

    def check(c: Candidate) -> None:
        c.orientation_verified = verify_orientation(c.video_id)
        c.is_short = is_short(c.video_id)

    with cf.ThreadPoolExecutor(max_workers=concurrency) as pool:
        list(pool.map(check, targets))

    counts = defaultdict(int)
    for c in targets:
        counts[c.orientation_verified or UNKNOWN] += 1
    n_short = sum(1 for c in targets if c.is_short)

    print(f"  orientation gate: {len(targets)} youtube candidates on vertical beats"
          f" — verified vertical {counts[VERTICAL]}"
          f" · landscape {counts[LANDSCAPE]}"
          f" · unknown {counts[UNKNOWN]} · served as Shorts {n_short}")

    if counts[UNKNOWN]:
        print(f"  WARNING: {counts[UNKNOWN]} candidates could not be verified. "
              "Unverified is not vertical — the grader must not treat them as passing.")

    if not drop:
        return cands

    landscape = {id(c) for c in targets if c.orientation_verified == LANDSCAPE}
    out = [c for c in cands if id(c) not in landscape]
    print(f"  dropped {len(cands) - len(out)} verified-landscape candidates "
          f"from vertical beats")
    return out


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
    h.add_argument("--no-verify-orientation", action="store_true",
                   help="skip the pixel-level orientation gate on vertical beats "
                        "(the gate is the vertical postmortem fix — only skip it "
                        "when working offline)")
    h.add_argument("--drop-landscape", action="store_true",
                   help="remove candidates verified landscape on a vertical beat, "
                        "rather than only flagging them. Never drops 'unknown'")
    h.set_defaults(func=cmd_harvest)

    cap = sub.add_parser("captions",
                         help="Step 5: fetch transcripts for a shortlist")
    cap.add_argument("shortlist")
    cap.add_argument("--out", default="transcripts.json")
    cap.add_argument("--no-whisper", action="store_true",
                     help="skip the Whisper pass on vertical clips; their "
                          "outcues will be unverifiable")
    cap.add_argument("--whisper-model", default="base.en")
    cap.set_defaults(func=cmd_captions)

    cl = sub.add_parser("clip", help="Step 7: download picks and cut segments")
    cl.add_argument("picks")
    cl.add_argument("--outdir", default="clips")
    cl.set_defaults(func=lambda a: __import__(
        "rossen_harvest.clip", fromlist=["cmd_clip"]).cmd_clip(a))

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
