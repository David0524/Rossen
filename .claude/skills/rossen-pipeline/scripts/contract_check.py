#!/usr/bin/env python3
"""Enforce the no-reduction rule at a stage boundary.

    python3 contract_check.py beats beats.json
    python3 contract_check.py picks picks.json

Every field dropped at a boundary looked unused at that boundary and was
load-bearing two steps later. This is the check that catches a reduced stage
file -- which is exactly what a resumed run leaves behind unnoticed, because
the file exists and parses fine.

  beats  = the extractor's record passed through, plus `queries`
  picks  = the grader's pass-two object passed through, plus `platform`, `title`
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _contract import (  # noqa: E402
    EXTRACTOR_KEYS, GRADER_PASS2_KEYS, PIPELINE_ADDED_KEYS, Report, load,
)


def check_beats(rows: list[dict], r: Report) -> None:
    for b in rows:
        bid = b.get("beat_id", "<no beat_id>")
        missing = [k for k in EXTRACTOR_KEYS if k not in b]
        if missing:
            r.error(bid, f"extractor record reduced -- dropped {missing}")
        if "queries" not in b:
            r.error(bid, "missing `queries` -- step 2 did not merge into the record")
    r.note(f"beats contract: extractor record ({len(EXTRACTOR_KEYS)} keys) + queries, "
           f"{len(rows)} rows")


def check_picks(rows: list[dict], r: Report) -> None:
    required = GRADER_PASS2_KEYS + PIPELINE_ADDED_KEYS
    for p in rows:
        bid = p.get("beat_id", "<no beat_id>")
        missing = [k for k in required if k not in p]
        if missing:
            r.error(bid, f"pass-two object reduced -- dropped {missing}")

        # A pick with nothing flagged still has to carry the grader's reasoning
        # forward, or the episode report becomes unbuildable.
        if p.get("flagged") in (None, "") and not (p.get("no_pick_reason") or "").strip():
            r.error(bid, "flagged is null but no_pick_reason is missing -- an empty beat must "
                         "say why and what query would find better")

        if p.get("pass") != 2:
            r.error(bid, f"pass is {p.get('pass')!r}, expected 2")

        ranked = p.get("ranked")
        if not isinstance(ranked, list):
            r.error(bid, "`ranked` is not a list")
        elif p.get("flagged") and not ranked:
            r.error(bid, "flagged a clip but `ranked` is empty -- the winner's scores "
                         "and reasoning did not survive the boundary")

        if not isinstance(p.get("source_mix"), dict):
            r.error(bid, "`source_mix` missing or not an object")
        if not isinstance(p.get("cannot_determine"), list):
            r.error(bid, "`cannot_determine` missing or not a list")

        # `platform` and `title` are what the Bible doc renders at the PLAY CLIP
        # marker; a pick without them cannot be written into the doc.
        if p.get("flagged"):
            if not (p.get("platform") or "").strip():
                r.error(bid, "flagged pick has no `platform`")
            if not (p.get("title") or "").strip():
                r.error(bid, "flagged pick has no `title` -- the doc renders it as link text")
    r.note(f"picks contract: pass-two object ({len(GRADER_PASS2_KEYS)} keys) + "
           f"{PIPELINE_ADDED_KEYS}, {len(rows)} rows")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["beats", "picks"])
    ap.add_argument("path")
    args = ap.parse_args()

    rows = load(args.path)
    r = Report(f"contract_check {args.stage}")
    (check_beats if args.stage == "beats" else check_picks)(rows, r)
    return r.finish()


if __name__ == "__main__":
    raise SystemExit(main())
