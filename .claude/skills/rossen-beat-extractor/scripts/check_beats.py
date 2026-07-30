#!/usr/bin/env python3
"""Validate a beats.json against the beat-extractor contract.

  python3 check_beats.py beats.json --day wednesday

Checks (all sourced from rossen-beat-extractor/SKILL.md and the operator runbook):
  * beat count inside the show-day band            wednesday 10-12 · friday 0-5
  * priority graded by consequence, not setup length (~1/3 priority 1)
  * every beat carries the extractor's required fields
  * five register keys per beat: news victim platform anchor shorts
  * orientation / clip_role / sourcability drawn from the documented vocabularies
"""
from __future__ import annotations
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "rossen-pipeline" / "scripts"))
from _common import Report, load

BANDS = {"wednesday": (10, 12), "friday": (0, 5)}
REGISTERS = {"news", "victim", "platform", "anchor", "shorts"}
ROLES = {"victim_interview", "confrontation_bust", "evidence", "explainer_demo",
         "explainer_demo/creator_short", "explainer_demo/creator_long",
         "authority_report", "debunk", "first_person_rant", "other"}
ORIENTATIONS = {"horizontal", "vertical"}
SOURCABILITY = {"high", "commentary_only", "none", "unchecked", "throttled", "n/a"}
REQUIRED = ["beat_id", "episode", "segment_title", "script_text", "orientation",
            "clip_role", "news_anchor", "visual_spec", "platforms", "offsite_likely",
            "priority", "expected_segments", "sourcability", "sourcability_note"]

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("beats"); ap.add_argument("--day", required=True)
    a = ap.parse_args()
    day = a.day.strip().lower()
    if day not in BANDS:
        print(f"ERROR  --day must be one of {sorted(BANDS)}"); return 1
    beats = load(a.beats)
    r = Report(f"check_beats [{day}]")

    lo, hi = BANDS[day]
    searchable = [b for b in beats if b.get("status") != "show_produced"]
    r.note(f"{len(beats)} beat records, {len(searchable)} searchable "
           f"({len(beats) - len(searchable)} show-produced)")
    if not (lo <= len(beats) <= hi):
        (r.error if len(beats) > hi else r.warn)(
            "band", f"{len(beats)} beats outside the {day} band {lo}-{hi}. "
                    "Above band, re-read the traps section (cold open / mid-show tease).")

    p1 = [b for b in beats if b.get("priority") == 1]
    share = len(p1) / len(beats) if beats else 0
    r.note(f"priority 1: {len(p1)}/{len(beats)} ({share:.0%}); target ~33%")
    if share > 0.60:
        r.error("priority", f"{share:.0%} of beats are priority 1 — graded by setup length, "
                            "not consequence. The field is useless and the transcript budget "
                            "becomes arbitrary.")
    elif share > 0.45:
        r.warn("priority", f"{share:.0%} priority 1 is high; confirm each is a segment-killer.")

    seen = set()
    for b in beats:
        bid = b.get("beat_id", "<no beat_id>")
        if bid in seen: r.error(bid, "duplicate beat_id")
        seen.add(bid)
        for f in REQUIRED:
            if f not in b: r.error(bid, f"missing required field '{f}'")
        if b.get("orientation") not in ORIENTATIONS:
            r.error(bid, f"orientation {b.get('orientation')!r} not in {sorted(ORIENTATIONS)}")
        if b.get("clip_role") not in ROLES:
            r.error(bid, f"clip_role {b.get('clip_role')!r} not in the documented seven roles")
        if b.get("sourcability") not in SOURCABILITY:
            r.error(bid, f"sourcability {b.get('sourcability')!r} not in {sorted(SOURCABILITY)}")
        if b.get("priority") not in (1, 2, 3):
            r.error(bid, f"priority {b.get('priority')!r} must be 1, 2 or 3")
        q = b.get("queries")
        if not isinstance(q, dict):
            r.error(bid, "no queries dict — beats.json must carry step 1 and step 2 merged")
        else:
            missing = REGISTERS - set(q)
            if missing:
                r.error(bid, f"missing register key(s) {sorted(missing)}. Five keys are required; "
                             "four means the Shorts leg runs on half its input.")
        if b.get("sourcability") == "none" and b.get("priority") == 1:
            r.warn(bid, "priority 1 with sourcability 'none' — swap or drop before searching.")
    return r.finish()

if __name__ == "__main__":
    raise SystemExit(main())
