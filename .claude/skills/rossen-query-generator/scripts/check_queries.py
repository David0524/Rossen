#!/usr/bin/env python3
"""Validate the query block of a beats.json against the query-generator contract.

  python3 check_queries.py beats.json

Checks (from rossen-query-generator/SKILL.md):
  * five registers present and non-empty on every searchable beat
  * orientation is a hard filter: horizontal beats get no tiktok/instagram/facebook
  * shorts register runs on every orientation, and carries the shorts_search block
  * platform_map only names platforms the beat declares and registers that exist
  * anchor register is populated whenever the beat has a news_anchor
"""
from __future__ import annotations
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "rossen-pipeline" / "scripts"))
from _common import Report, load

REGISTERS = ["anchor", "news", "victim", "platform", "shorts"]
VERTICAL_ONLY = {"tiktok", "instagram", "facebook"}

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("beats")
    a = ap.parse_args()
    beats = load(a.beats)
    r = Report("check_queries")
    total = 0
    for b in beats:
        bid = b.get("beat_id", "<no beat_id>")
        if b.get("status") == "show_produced":
            r.note(f"{bid}: show-produced, no search lane — query checks skipped")
            continue
        q = b.get("queries") or {}
        plats = set(b.get("platforms") or [])
        for reg in REGISTERS:
            if reg not in q:
                r.error(bid, f"register '{reg}' missing")
            elif not q[reg]:
                r.error(bid, f"register '{reg}' is empty")
            else:
                total += len(q[reg])
        if b.get("news_anchor") and not q.get("anchor"):
            r.error(bid, "beat has a news_anchor but the anchor register is empty — "
                         "highest-hit-rate register for one query")
        if not q.get("shorts"):
            r.error(bid, "no shorts queries. Shorts run on every orientation.")
        if q.get("shorts") and not b.get("shorts_search"):
            r.error(bid, "shorts queries present but no shorts_search block "
                         "(needs suffix '#shorts' and match_filter 'duration < 60')")
        ss = b.get("shorts_search") or {}
        if ss:
            if ss.get("suffix") != "#shorts":
                r.error(bid, f"shorts_search.suffix is {ss.get('suffix')!r}, expected '#shorts'")
            if "duration" not in str(ss.get("match_filter", "")):
                r.error(bid, "shorts_search.match_filter must bound duration (< 60)")
        if b.get("orientation") == "vertical" and "youtube" in plats:
            if b.get("orientation_decision_pending"):
                r.warn(bid, "vertical beat routed to youtube long-form — allowed only because "
                            "orientation_decision_pending is set by a script DECIDE marker")
            else:
                r.error(bid, "vertical beat routed to youtube long-form — orientation is a hard filter")
        bad = plats & VERTICAL_ONLY
        if b.get("orientation") == "horizontal" and bad:
            if b.get("orientation_decision_pending"):
                r.warn(bid, f"horizontal beat routed to {sorted(bad)} — allowed only because "
                            "orientation_decision_pending is set by a script DECIDE marker")
            else:
                r.error(bid, f"horizontal beat routed to {sorted(bad)} — orientation is a hard "
                             "filter, producer-authored, 26/26 correct")
        pm = b.get("platform_map") or {}
        for plat, regs in pm.items():
            if plat not in plats:
                r.error(bid, f"platform_map names '{plat}' which is not in platforms")
            for reg in regs:
                if reg not in q:
                    r.error(bid, f"platform_map['{plat}'] names register '{reg}' with no queries")
        for plat in plats:
            if plat not in pm:
                r.warn(bid, f"platform '{plat}' declared but absent from platform_map")
    r.note(f"{total} query strings across {len(beats)} beats")
    return r.finish()

if __name__ == "__main__":
    raise SystemExit(main())
