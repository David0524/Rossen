#!/usr/bin/env python3
"""Validate an extractor beats file against the beat-extractor contract.

    python3 check_beats.py beats.json --day wednesday

Checks the record shape the extractor promises, the orientation hard filter,
and the Checkpoint 1 sanity rules (beat-count band, priority spread). Exits
nonzero if any ERROR fired.

Scope, stated plainly: this validates *structure and distribution*. It cannot
tell you a beat is editorially wrong -- that a visual_spec describes the wrong
shot, or that a sourcability value was asserted without a search actually
having been run. A clean run here is not evidence the beats are right.
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "rossen-pipeline" / "scripts"))
from _contract import (  # noqa: E402
    DAY_BANDS, EXTRACTOR_KEYS, ORIENTATIONS, ROLES, SOURCABILITY,
    SOURCE_NATIVE, Report, load,
)

# rossen-query-generator SKILL.md: orientation is a hard filter on TikTok,
# Instagram and Facebook. A horizontal beat carrying these has leaked.
VERTICAL_ONLY_PLATFORMS = {"tiktok", "instagram"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("beats")
    ap.add_argument("--day", default=None,
                    help="show day; enforces the Checkpoint 1 beat-count band")
    args = ap.parse_args()

    beats = load(args.beats)
    r = Report("check_beats")

    seen: set[str] = set()
    for b in beats:
        bid = b.get("beat_id", "<no beat_id>")

        for k in EXTRACTOR_KEYS:
            if k not in b:
                r.error(bid, f"missing required extractor key `{k}`")

        if bid in seen:
            r.error(bid, "duplicate beat_id")
        seen.add(bid)

        orient = b.get("orientation")
        if orient not in ORIENTATIONS:
            r.error(bid, f"orientation {orient!r} not in {sorted(ORIENTATIONS)}")

        role = b.get("clip_role")
        if role not in ROLES:
            r.error(bid, f"clip_role {role!r} not a documented role")
        if role == "other" and not b.get("role_note"):
            r.error(bid, "clip_role `other` requires a role_note describing the fit")

        pri = b.get("priority")
        if pri not in (1, 2, 3):
            r.error(bid, f"priority {pri!r} must be 1, 2 or 3")

        es = b.get("expected_segments")
        if not isinstance(es, int) or es < 1:
            r.error(bid, f"expected_segments {es!r} must be an int >= 1")

        sc = b.get("sourcability")
        if sc not in SOURCABILITY:
            r.error(bid, f"sourcability {sc!r} not in {sorted(SOURCABILITY)}")
        if sc in {"none", "commentary_only", "throttled"} and not b.get("sourcability_note"):
            r.error(bid, f"sourcability `{sc}` requires a sourcability_note saying what was searched")

        sn = b.get("source_native")
        if sn not in SOURCE_NATIVE:
            r.error(bid, f"source_native {sn!r} not in {sorted(SOURCE_NATIVE)}")

        plats = set(b.get("platforms") or [])
        if not plats:
            r.error(bid, "platforms is empty")
        if orient == "horizontal" and (leak := plats & VERTICAL_ONLY_PLATFORMS):
            r.error(bid, f"horizontal beat carries vertical-only platforms {sorted(leak)} "
                         "-- orientation is a hard filter, not a hint")

        if not (b.get("script_text") or "").strip():
            r.error(bid, "script_text is empty -- the beat carries no searchable context")
        if not (b.get("visual_spec") or "").strip():
            r.error(bid, "visual_spec is empty")

        # An outcue exemption is legitimate (picture-only b-roll) but must be
        # justified in the record rather than assumed downstream.
        if b.get("outcue_required") is False and not b.get("outcue_exemption_reason"):
            r.error(bid, "outcue_required:false requires an outcue_exemption_reason")

        if sc in {"none", "commentary_only"}:
            r.warn(bid, f"sourcability `{sc}` -- surface this in the Checkpoint 1 table")
        if sc == "throttled":
            r.warn(bid, "sourcability `throttled` -- network condition, do not swap the case on it")

    # ---- Checkpoint 1 distribution rules
    n = len(beats)
    if args.day:
        day = args.day.strip().lower()
        if day not in DAY_BANDS:
            r.error("--day", f"{args.day!r} not one of {sorted(DAY_BANDS)}")
        else:
            lo, hi = DAY_BANDS[day]
            if not (lo <= n <= hi):
                r.error("beat count", f"{n} beats outside the {day} band {lo}-{hi} "
                                      "-- re-read the traps section (cold open / mid-show tease)")
            else:
                r.note(f"beat count {n} in the {day} band {lo}-{hi}")

    if n > 16:
        r.error("beat count", f"{n} beats -- above 16 you are extracting teases, not beats")

    if n:
        pri = Counter(b.get("priority") for b in beats)
        share = pri[1] / n
        r.note(f"priority spread {dict(sorted((k, v) for k, v in pri.items() if k is not None))} "
               f"-- priority 1 is {share:.0%} of beats")
        if share > 0.5:
            r.warn("priority spread",
                   f"{pri[1]}/{n} ({share:.0%}) are priority 1 -- graded by consequence this "
                   "should sit near a third; a high share usually means grading by setup length, "
                   "which makes the transcript budget arbitrary")
        roles = Counter(b.get("clip_role") for b in beats)
        r.note("roles " + " · ".join(f"{k} {v}" for k, v in roles.most_common()))
        orients = Counter(b.get("orientation") for b in beats)
        r.note("orientation " + " · ".join(f"{k} {v}" for k, v in orients.most_common()))

    return r.finish()


if __name__ == "__main__":
    raise SystemExit(main())
