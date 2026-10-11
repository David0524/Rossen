#!/usr/bin/env python3
"""check_grades.py — validate grader output for either pass.

Usage:
    python3 scripts/check_grades.py one shortlist.json
    python3 scripts/check_grades.py two picks.json
    python3 scripts/check_grades.py both shortlist.json picks.json

This is the terminal skill in the pipeline: its pass-two object becomes the Bible
doc, and nothing downstream can correct it. Checks the scoring formula and its
vetoes, the shortlist size against the beat's `priority`, proposed segments against
`expected_segments`, outcue presence, and manual-lane beats that should never have
reached grading at all.

Exit: 0 clean, 1 violation, 2 unreadable.
"""

import argparse
import json
import sys

SOURCE_TYPES = {"affiliate", "network", "creator_long", "creator_short",
                "first_person", "raw_footage"}
ROLES = {"victim_interview", "confrontation_bust", "evidence",
         "explainer_demo/creator_short", "explainer_demo/creator_long",
         "authority_report", "debunk", "first_person_rant"}

WEIGHTS = {"fit": 0.35, "quality": 0.25, "authenticity": 0.20, "tone": 0.20}
GATES = ("tone", "quality", "fit")     # authenticity is a preference, not a gate
GATE_FLOOR = 3
GATE_CAP = 40
FLAG_MIN = 55                          # below this, flagged must be null
WEAK_MAX = 69                          # 55-69 is a weak pick, human re-check
SHORTLIST_BY_PRIORITY = {1: 5, 2: 3, 3: 2}
SKIP_SOURCABILITY = {"none", "throttled"}


def refuse_if_routed_elsewhere(rec, bid):
    """A manual-lane or dead beat should never reach grading, in either pass."""
    sc, sn = rec.get("sourcability"), rec.get("source_native")
    if sn and sn != "none":
        return [f"{bid}: should not have been graded. source_native={sn!r} means "
                f"a native post is already identified — this is a manual-lane "
                f"beat. Hand the producer the permalink; do not rank reposts."]
    if sc in SKIP_SOURCABILITY:
        return [f"{bid}: should not have been graded. sourcability={sc!r} — "
                + ("re-run the extractor's scan; a throttle is a network "
                   "condition, not an absence of footage."
                   if sc == "throttled" else
                   "no findable footage, so this is a swap, show-produced or "
                   "drop decision, not a grading task.")]
    return []


def expected_score(r):
    subs = {k: r.get(k) for k in ("tone", "authenticity", "quality", "fit")}
    if any(v is None for v in subs.values()):
        return None
    if min(subs[g] for g in GATES) <= GATE_FLOOR:
        return GATE_CAP
    return round(sum(subs[k] * w for k, w in WEIGHTS.items()) * 10)


def check_one(records):
    errs, warns = [], []
    for rec in records:
        bid = rec.get("beat_id", "<no beat_id>")
        for f in ("beat_id", "orientation", "clip_role", "priority",
                  "expected_segments", "candidates", "source_mix"):
            if f not in rec:
                errs.append(f"{bid}: pass one missing `{f}`. The pipeline writes "
                            f"shortlist.json from this and pass two needs the "
                            f"beat fields carried through.")
        if rec.get("clip_role") and rec["clip_role"] not in ROLES:
            errs.append(f"{bid}: clip_role {rec['clip_role']!r} not in the "
                        f"canonical eight.")

        errs += refuse_if_routed_elsewhere(rec, bid)

        cands = rec.get("candidates") or []
        pr = rec.get("priority")
        want = SHORTLIST_BY_PRIORITY.get(pr)
        if want and len(cands) > want:
            errs.append(f"{bid}: {len(cands)} candidates shortlisted for a "
                        f"priority-{pr} beat; cap is {want}. Pass two downloads "
                        f"and transcribes every one of these — that is the most "
                        f"expensive step in the pipeline.")
        if want and len(cands) < want:
            note = (rec.get("shortlist_note") or "").strip()
            if not note:
                warns.append(f"{bid}: {len(cands)} candidates for a priority-{pr} "
                             f"beat (expected {want}). Legitimate when the "
                             f"diversity floor found nothing to promote — say so "
                             f"in `shortlist_note`.")

        for i, c in enumerate(cands):
            tag = f"{bid}.candidates[{i}]"
            for f in ("url", "source_type", "score", "reason",
                      "cannot_determine"):
                if f not in c:
                    errs.append(f"{tag}: missing `{f}`")
            st = c.get("source_type")
            if st and st not in SOURCE_TYPES:
                errs.append(f"{tag}: source_type {st!r} not in "
                            f"{sorted(SOURCE_TYPES)}")
            s = c.get("score")
            if s is not None and not 0 <= s <= 100:
                errs.append(f"{tag}: score {s} outside 0-100")
            if not isinstance(c.get("cannot_determine"), list):
                errs.append(f"{tag}: `cannot_determine` must be a list at "
                            f"candidate level in pass one — it tells pass two "
                            f"what to look for on this specific clip.")
            if c.get("promoted_by_floor") and c.get("score") is not None:
                peers = [x.get("score", 0) for x in cands
                         if not x.get("promoted_by_floor")]
                if peers and max(peers) - c["score"] >= 30:
                    if "below" not in (c.get("reason") or "").lower():
                        warns.append(
                            f"{tag}: promoted by the diversity floor and scoring "
                            f"{max(peers)-c['score']} points below the top peer. "
                            f"Say so in `reason` so pass two does not treat the "
                            f"shortlist as five peers.")

        mix = rec.get("source_mix") or {}
        if cands and mix and sum(mix.values()) != len(cands):
            errs.append(f"{bid}: source_mix sums to {sum(mix.values())} but there "
                        f"are {len(cands)} candidates.")
    return errs, warns


def check_two(records):
    errs, warns = [], []
    for rec in records:
        bid = rec.get("beat_id", "<no beat_id>")
        for f in ("beat_id", "pass", "flagged", "source_mix",
                  "diversity_floor_applied", "ranked", "rejected",
                  "cannot_determine"):
            if f not in rec:
                errs.append(f"{bid}: pass two missing `{f}`. The pipeline's "
                            f"episode report is built from these fields.")
        errs += refuse_if_routed_elsewhere(rec, bid)
        if not isinstance(rec.get("cannot_determine"), list):
            errs.append(f"{bid}: pass-two `cannot_determine` is a beat-level "
                        f"list. (Pass one carries it per candidate; the shape "
                        f"changes deliberately between passes.)")

        ranked = rec.get("ranked") or []
        for i, r in enumerate(ranked):
            tag = f"{bid}.ranked[{i}]"
            for f in ("url", "source_type", "score", "tone", "authenticity",
                      "quality", "fit", "segments", "reasoning", "flags"):
                if f not in r:
                    errs.append(f"{tag}: missing `{f}`")
            if r.get("source_type") and r["source_type"] not in SOURCE_TYPES:
                errs.append(f"{tag}: source_type {r['source_type']!r} unknown")

            for k in ("tone", "authenticity", "quality", "fit"):
                v = r.get(k)
                if v is not None and not 0 <= v <= 10:
                    errs.append(f"{tag}: {k}={v} outside 0-10")

            exp = expected_score(r)
            if exp is not None and r.get("score") is not None:
                if abs(r["score"] - exp) > 1:
                    gated = min(r[g] for g in GATES) <= GATE_FLOOR
                    errs.append(
                        f"{tag}: score {r['score']} but the rubric gives {exp}. "
                        + (f"A gate dimension is at {min(r[g] for g in GATES)} "
                           f"(<= {GATE_FLOOR}), so the total caps at {GATE_CAP} "
                           f"regardless of the other dimensions — audio, tone and "
                           f"fit are gates, not quarter-shares."
                           if gated else
                           f"Formula: fit .35 + quality .25 + authenticity .20 + "
                           f"tone .20, x10."))

            segs = r.get("segments") or []
            if not segs:
                errs.append(f"{tag}: no segments proposed")
            for j, s in enumerate(segs):
                for f in ("in", "out", "outcue"):
                    if f not in s:
                        errs.append(f"{tag}.segments[{j}]: missing `{f}`")
                if not (s.get("outcue") or "").strip():
                    errs.append(
                        f"{tag}.segments[{j}]: empty outcue. It is the "
                        f"verification anchor — the phrase must appear in the "
                        f"transcript within about a second of the out point. "
                        f"Never invent it, never paraphrase it.")

            es = rec.get("expected_segments")
            if es and i == 0 and len(segs) < es:
                errs.append(
                    f"{tag}: {len(segs)} segment(s) proposed but the beat record "
                    f"expects {es} (counted from BUTT markers in the script). A "
                    f"missed butt-cut ships the beat at a fraction of its "
                    f"intended length and is invisible in the output — either "
                    f"find the other slices or say why in `cannot_determine`.")

        fl = rec.get("flagged", "MISSING")
        urls = [r.get("url") for r in ranked]
        top = ranked[0].get("score") if ranked else None
        if fl not in (None, "MISSING"):
            if fl not in urls:
                errs.append(f"{bid}: flagged URL is not in `ranked`.")
            if top is not None and top < FLAG_MIN:
                errs.append(f"{bid}: flagged a pick scoring {top}, below the "
                            f"{FLAG_MIN} floor. Return flagged: null with a "
                            f"reason and the query that would find something "
                            f"better — a bad pick costs more than an honest gap.")
            elif top is not None and top <= WEAK_MAX:
                warns.append(f"{bid}: top score {top} is a weak pick "
                             f"({FLAG_MIN}-{WEAK_MAX}). Must appear in the "
                             f"pipeline's human-re-check callout.")
        elif fl is None:
            if not (rec.get("null_reason") or "").strip():
                errs.append(f"{bid}: flagged is null with no `null_reason`. Say "
                            f"what was wrong and what query would find better.")
            if top is not None and top >= FLAG_MIN:
                warns.append(f"{bid}: flagged null but the top candidate scores "
                             f"{top}. Explain why it was rejected anyway.")

        mix = rec.get("source_mix") or {}
        for k in mix:
            if k not in SOURCE_TYPES:
                errs.append(f"{bid}: source_mix key {k!r} unknown")
    return errs, warns


def run(label, fn, path):
    try:
        data = json.load(open(path, encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"could not read {path}: {exc}", file=sys.stderr)
        sys.exit(2)
    recs = data if isinstance(data, list) else [data]
    errs, warns = fn(recs)
    print(f"\n{label} — {path}  ({len(recs)} beat record(s))")
    print("=" * 70)
    for e in errs:
        print(f"  x {e}")
    for w in warns:
        print(f"  ! {w}")
    if not errs and not warns:
        print("  contract clean.")
    print(f"\n  {len(errs)} violation(s), {len(warns)} warning(s)\n")
    return len(errs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["one", "two", "both"])
    ap.add_argument("paths", nargs="+")
    a = ap.parse_args()
    bad = 0
    if a.mode in ("one", "both"):
        bad += run("PASS ONE", check_one, a.paths[0])
    if a.mode in ("two", "both"):
        bad += run("PASS TWO", check_two,
                   a.paths[1] if a.mode == "both" else a.paths[0])
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
