#!/usr/bin/env python3
"""Validate a grader pass-one shortlist or pass-two picks file.

  python3 check_grades.py one shortlist.json
  python3 check_grades.py two picks.json

Checks (from rossen-clip-grader/SKILL.md):
  pass one  * <= 5 candidates per beat, each with score, source_type, reason,
              cannot_determine; source_mix reported; diversity floor recorded
  pass two  * exactly one flagged url (or an explicit null with a reason)
            * every proposed segment carries a verbatim outcue and in/out
            * scores 0-100, dimension scores 0-10
"""
from __future__ import annotations
import argparse, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "rossen-pipeline" / "scripts"))
from _common import Report, load

SOURCE_TYPES = {"affiliate", "network", "creator_long", "creator_short",
                "first_person", "raw_footage"}
TC = re.compile(r"^\d{1,2}:\d{2}(?::\d{2})?$|^\d{1,3}$|^(start|end)$", re.I)

def check_one(rows, r):
    for row in rows:
        bid = row.get("beat_id", "<no beat_id>")
        if row.get("pass") != 1:
            r.error(bid, f"pass is {row.get('pass')!r}, expected 1")
        cands = row.get("candidates")
        if cands is None:
            r.error(bid, "no 'candidates' list"); continue
        if len(cands) > 5:
            r.error(bid, f"{len(cands)} candidates — pass one narrows to 5")
        if len(cands) < 5 and not row.get("short_of_five_reason"):
            r.warn(bid, f"{len(cands)} candidates and no short_of_five_reason. The diversity "
                        "floor promotes, it never invents — say why you shipped short.")
        if "source_mix" not in row:
            r.error(bid, "no source_mix — pass one must report the shortlist distribution")
        if "diversity_floor_applied" not in row:
            r.error(bid, "no diversity_floor_applied flag")
        for c in cands:
            u = c.get("url", "<no url>")
            for f in ("url", "score", "source_type", "reason", "cannot_determine"):
                if f not in c: r.error(bid, f"candidate[{u}] missing '{f}'")
            if c.get("source_type") not in SOURCE_TYPES:
                r.error(bid, f"candidate[{u}] source_type {c.get('source_type')!r} not in "
                             f"{sorted(SOURCE_TYPES)}")
            s = c.get("score")
            if not isinstance(s, (int, float)) or not 0 <= s <= 100:
                r.error(bid, f"candidate[{u}] score {s!r} out of 0-100")

def check_two(rows, r):
    for row in rows:
        bid = row.get("beat_id", "<no beat_id>")
        if row.get("pass") != 2:
            r.error(bid, f"pass is {row.get('pass')!r}, expected 2")
        flagged = row.get("flagged", "__missing__")
        if flagged == "__missing__":
            r.error(bid, "no 'flagged' key — must be a url or an explicit null")
        ranked = row.get("ranked") or []
        if flagged is None:
            if not row.get("flagged_reason"):
                r.error(bid, "flagged null without a reason")
            if not row.get("better_query"):
                r.error(bid, "flagged null without the query that would find better")
            r.note(f"{bid}: flagged null — {row.get('flagged_reason','')[:90]}")
        else:
            urls = [e.get("url") for e in ranked]
            if flagged not in urls:
                r.error(bid, "flagged url does not appear in ranked[]")
            for e in ranked:
                if e.get("url") != flagged: continue
                if e.get("score", 0) < 55:
                    r.error(bid, f"flagged clip scores {e.get('score')} — nothing clearing 55 "
                                 "must return flagged: null instead")
                if not e.get("segments"):
                    r.error(bid, "flagged clip has no segments")
                for seg in e.get("segments") or []:
                    if not seg.get("outcue"):
                        r.error(bid, "segment with no outcue — every segment needs a verbatim "
                                     "phrase found in the transcript")
                    for k in ("in", "out"):
                        v = str(seg.get(k, ""))
                        if not TC.match(v):
                            r.error(bid, f"segment {k}={v!r} is not a timecode")
        for e in ranked:
            u = e.get("url", "<no url>")
            for dim in ("tone", "authenticity", "quality", "fit"):
                v = e.get(dim)
                if v is None: r.error(bid, f"ranked[{u}] missing dimension '{dim}'")
                elif not 0 <= v <= 10: r.error(bid, f"ranked[{u}] {dim}={v} out of 0-10")
            if e.get("source_type") not in SOURCE_TYPES:
                r.error(bid, f"ranked[{u}] source_type {e.get('source_type')!r} invalid")

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("which", choices=["one", "two"]); ap.add_argument("file")
    a = ap.parse_args()
    rows = load(a.file)
    r = Report(f"check_grades pass {a.which}")
    r.note(f"{len(rows)} beat record(s) in {a.file}")
    (check_one if a.which == "one" else check_two)(rows, r)
    return r.finish()

if __name__ == "__main__":
    raise SystemExit(main())
