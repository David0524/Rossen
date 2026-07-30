#!/usr/bin/env python3
"""Stage-boundary contract check. Catches a REDUCED stage file.

  python3 contract_check.py beats beats.json
  python3 contract_check.py picks picks.json

The failure this exists to prevent: a stage file that drops a field which looked
unused at that boundary and was load-bearing two steps later. beats.json is the
extractor's record passed through PLUS queries. picks.json is the grader's
pass-two object passed through PLUS platform and title.
"""
from __future__ import annotations
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import Report, load

BEATS_REQUIRED = ["beat_id", "episode", "segment_title", "script_text", "orientation",
                  "clip_role", "news_anchor", "visual_spec", "platforms", "offsite_likely",
                  "priority", "expected_segments", "sourcability", "sourcability_note",
                  "source_native", "queries", "platform_map"]
PICKS_REQUIRED = ["beat_id", "pass", "flagged", "source_mix", "diversity_floor_applied",
                  "ranked", "rejected", "cannot_determine", "platform", "title"]
RANKED_REQUIRED = ["url", "source_type", "score", "tone", "authenticity", "quality",
                   "fit", "segments", "reasoning", "flags"]

def check_beats(beats, r):
    for b in beats:
        bid = b.get("beat_id", "<no beat_id>")
        req = list(BEATS_REQUIRED)
        if b.get("status") == "show_produced":
            req = [f for f in req if f not in ("platform_map",)]
        for f in req:
            if f not in b:
                r.error(bid, f"REDUCED: field '{f}' dropped at the beats boundary")

def check_picks(picks, r):
    for p in picks:
        bid = p.get("beat_id", "<no beat_id>")
        for f in PICKS_REQUIRED:
            if f not in p:
                r.error(bid, f"REDUCED: field '{f}' dropped at the picks boundary")
        if p.get("pass") != 2:
            r.error(bid, f"pass is {p.get('pass')!r}; picks.json must carry the pass-two object")
        for entry in p.get("ranked") or []:
            u = entry.get("url", "<no url>")
            for f in RANKED_REQUIRED:
                if f not in entry:
                    r.error(bid, f"ranked[{u}]: REDUCED: field '{f}' dropped")
            for seg in entry.get("segments") or []:
                for f in ("in", "out", "outcue"):
                    if f not in seg:
                        r.error(bid, f"ranked[{u}]: segment missing '{f}'")
        if p.get("flagged") is None and not p.get("flagged_reason"):
            r.error(bid, "flagged is null but no flagged_reason given — an empty beat must "
                         "carry a reason and the query that would find better")
        if p.get("flagged") is None and not p.get("better_query"):
            r.error(bid, "flagged is null but no better_query given")

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["beats", "picks"]); ap.add_argument("file")
    a = ap.parse_args()
    rows = load(a.file)
    r = Report(f"contract_check {a.stage}")
    r.note(f"{len(rows)} record(s) in {a.file}")
    (check_beats if a.stage == "beats" else check_picks)(rows, r)
    return r.finish()

if __name__ == "__main__":
    raise SystemExit(main())
