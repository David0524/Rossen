#!/usr/bin/env python3
"""Validate grader output against the clip-grader contract.

    python3 check_grades.py one shortlist.json
    python3 check_grades.py two  picks.json

Pass one: shortlist size, source_type tags, score range, the cannot_determine
note pass two depends on.

Pass two: the outcue rule. Every proposed segment needs a verbatim outcue and a
sane in/out. This checks the outcue is *present and non-trivial*; it cannot
check verbatimness without the transcript, so pass --transcripts to make that
check real.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "rossen-pipeline" / "scripts"))
from _contract import SOURCE_TYPES, Report, load, parse_tc  # noqa: E402

SHORTLIST_MAX = 5          # grader SKILL.md: narrow each beat to five
MIN_OUTCUE_WORDS = 3       # a one-word outcue is not a locatable anchor


def _norm(s: str) -> str:
    return " ".join("".join(c.lower() if c.isalnum() or c.isspace() else " "
                            for c in s).split())


def check_one(rows: list[dict], r: Report) -> None:
    by_beat: dict[str, list[dict]] = {}
    for c in rows:
        by_beat.setdefault(c.get("beat_id", "<no beat_id>"), []).append(c)

    for bid, cands in sorted(by_beat.items()):
        if len(cands) > SHORTLIST_MAX:
            r.error(bid, f"{len(cands)} shortlisted, ceiling is {SHORTLIST_MAX}")
        if len(cands) < SHORTLIST_MAX:
            r.warn(bid, f"{len(cands)} shortlisted (under {SHORTLIST_MAX}) -- say why in "
                        "the report; the diversity floor promotes, it never invents")

        for c in cands:
            url = c.get("url") or "<no url>"
            where = f"{bid} {url[:60]}"
            st = c.get("source_type")
            if st not in SOURCE_TYPES:
                r.error(where, f"source_type {st!r} not in {sorted(SOURCE_TYPES)}")
            sc = c.get("score")
            if not isinstance(sc, (int, float)) or not 0 <= sc <= 100:
                r.error(where, f"score {sc!r} must be a number 0-100")
            if not (c.get("reason") or "").strip():
                r.error(where, "missing one-line `reason`")
            if "cannot_determine" not in c:
                r.error(where, "missing `cannot_determine` -- this field tells pass two "
                               "what to look for and is not optional")

        mix = Counter(c.get("source_type") for c in cands)
        promoted = [c for c in cands if c.get("diversity_floor_promoted")]
        r.note(f"{bid} mix " + " · ".join(f"{k} {v}" for k, v in mix.most_common())
               + (f"  [floor promoted {len(promoted)}]" if promoted else ""))
        if cands and set(mix) <= {"affiliate", "network"} and not promoted:
            r.warn(bid, "shortlist is all affiliate/network with no diversity-floor "
                        "promotion -- wire and local are one monoculture, not two")


def check_two(rows: list[dict], r: Report, transcripts: dict | None) -> None:
    for p in rows:
        bid = p.get("beat_id", "<no beat_id>")
        flagged = p.get("flagged")

        if flagged in (None, ""):
            if not (p.get("no_pick_reason") or "").strip():
                r.error(bid, "flagged:null requires no_pick_reason")
            if not (p.get("suggested_query") or "").strip():
                r.error(bid, "flagged:null requires suggested_query -- the query that "
                             "would find better")
            r.note(f"{bid} flagged:null -- {str(p.get('no_pick_reason'))[:80]}")
            continue

        segs = p.get("segments")
        outcue_required = p.get("outcue_required", True)
        if not isinstance(segs, list) or not segs:
            r.error(bid, "flagged a clip but `segments` is empty")
            continue

        for i, s in enumerate(segs):
            where = f"{bid} seg{i}"
            tin, tout = s.get("in"), s.get("out")
            ain, aout = parse_tc(tin or ""), parse_tc(tout or "")
            if ain is None:
                r.error(where, f"`in` {tin!r} is not m:ss")
            if aout is None:
                r.error(where, f"`out` {tout!r} is not m:ss")
            if ain is not None and aout is not None:
                if aout <= ain:
                    r.error(where, f"out {tout} is not after in {tin}")
                elif aout - ain < 5:
                    r.warn(where, f"segment is {aout - ain:.0f}s -- below the 10s floor "
                                  "observed in any aired segment")

            oc = (s.get("outcue") or "").strip()
            if not outcue_required:
                if oc:
                    r.warn(where, "beat is marked outcue_required:false but carries an "
                                  "outcue -- picture-only b-roll takes no audio")
                continue
            if not oc:
                r.error(where, "missing `outcue` -- required verbatim on every segment")
                continue
            if len(oc.split()) < MIN_OUTCUE_WORDS:
                r.error(where, f"outcue {oc!r} is {len(oc.split())} word(s); too short to "
                               f"locate, need >= {MIN_OUTCUE_WORDS}")
            if s.get("outcue_verified") is False and not s.get("outcue_unverified_reason"):
                r.error(where, "outcue_verified:false requires outcue_unverified_reason "
                               "(it renders UNVERIFIED in the Bible doc)")

            if transcripts is not None:
                url = p.get("flagged")
                text = transcripts.get(url)
                if not text:
                    r.warn(where, "no transcript available for the flagged url, outcue "
                                  "verbatimness unchecked")
                elif _norm(oc) not in _norm(text):
                    r.error(where, f"outcue {oc!r} does NOT appear in the transcript -- "
                                   "the timecode is wrong. Never paraphrase an outcue.")

        n = len(segs)
        if n > 1:
            r.note(f"{bid} butt-cut, {n} segments from one source")

    return None


def _load_transcripts(path: str) -> dict[str, str]:
    """Flatten a transcripts.json into {url: full text} for outcue checking."""
    raw = json.loads(Path(path).read_text())
    items = raw.values() if isinstance(raw, dict) else raw
    out: dict[str, str] = {}
    for t in items:
        if not isinstance(t, dict):
            continue
        url = t.get("url") or t.get("id")
        if not url:
            continue
        if isinstance(t.get("text"), str):
            out[url] = t["text"]
        else:
            cues = t.get("cues") or t.get("segments") or []
            out[url] = " ".join(c.get("text", "") for c in cues if isinstance(c, dict))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("which", choices=["one", "two"])
    ap.add_argument("path")
    ap.add_argument("--transcripts", default=None,
                    help="transcripts.json; makes the outcue verbatim check real")
    args = ap.parse_args()

    rows = load(args.path)
    r = Report(f"check_grades pass {args.which}")
    if args.which == "one":
        check_one(rows, r)
    else:
        tr = _load_transcripts(args.transcripts) if args.transcripts else None
        if tr is None:
            r.warn("outcue", "no --transcripts given, so outcues are checked for shape "
                             "only, not verbatimness")
        check_two(rows, r, tr)
    return r.finish()


if __name__ == "__main__":
    raise SystemExit(main())
