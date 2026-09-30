#!/usr/bin/env python3
"""contract_check.py — validate a stage file against the sibling skills' schemas.

Usage:
    python3 scripts/contract_check.py beats beats.json
    python3 scripts/contract_check.py picks picks.json
    python3 scripts/contract_check.py both beats.json picks.json

Exists because the three handoffs in this pipeline drift silently. A reduced
`beats.json` or `picks.json` does not error — it just quietly makes a later step
impossible, and the failure surfaces at Step 8 when the report cannot be built,
or in the edit bay when a butt-cut beat ships one segment.

Field sets below are transcribed from the siblings' own declared output schemas.
When a sibling changes its schema, change it here in the same commit.

Exit: 0 clean, 1 contract violation, 2 unreadable input.
"""

import json
import sys

# ---- rossen-beat-extractor, "## Output" + sourcability scan output
BEAT_REQUIRED = [
    "beat_id", "episode", "segment_title", "script_text", "orientation",
    "clip_role", "news_anchor", "visual_spec", "platforms", "offsite_likely",
    "priority", "expected_segments", "sourcability", "source_native",
]
BEAT_OPTIONAL = ["sourcability_note", "aired_url", "aired_platform", "segments"]

# ---- rossen-query-generator: four registers plus the Shorts dialect it emits
#      as explicit strings. Step 3's ShortsBackend consumes `shorts` by name.
REGISTERS_REQUIRED = ["news", "victim", "platform", "anchor", "shorts"]

# ---- rossen-clip-grader, "## Output" (pass two). picks.json is this object
#      passed through, plus platform/title added by the pipeline.
PICK_REQUIRED = [
    "beat_id", "flagged", "source_mix", "diversity_floor_applied", "ranked",
    "rejected", "cannot_determine", "platform",
]
RANKED_REQUIRED = [
    "url", "source_type", "score", "tone", "authenticity", "quality", "fit",
    "segments", "reasoning", "flags",
]
SEGMENT_REQUIRED = ["in", "out", "outcue"]

VALID_ORIENTATION = {"horizontal", "vertical"}
VALID_SOURCABILITY = {"high", "commentary_only", "none", "unchecked"}
VALID_SOURCE_NATIVE = {"instagram", "x", "tiktok", "none"}

# Step 8 requires these callouts; each needs these fields to exist.
STEP8_NEEDS = {
    "beats with no usable clip": ["flagged"],
    "weak picks a human should re-check": ["score", "flags", "reasoning"],
    "source type at 70%+ of picks": ["source_mix"],
    "beats where the runner-up was a different type": ["ranked"],
    "diversity-floor promotions that lost pass two":
        ["diversity_floor_applied", "ranked"],
}


def load(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"could not read {path}: {exc}", file=sys.stderr)
        sys.exit(2)


def check_beats(path):
    data = load(path)
    if not isinstance(data, list):
        return [f"{path}: expected a JSON array of beat objects"]
    errs, warns = [], []

    for i, b in enumerate(data):
        tag = b.get("beat_id", f"index {i}")
        for f in BEAT_REQUIRED:
            if f not in b:
                errs.append(
                    f"{tag}: missing `{f}`. The beat extractor emits it; "
                    f"dropping it here is how the field stops existing for the "
                    f"whole run.")
        if b.get("orientation") not in VALID_ORIENTATION | {None}:
            errs.append(f"{tag}: orientation {b['orientation']!r} not in "
                        f"{sorted(VALID_ORIENTATION)}")
        if "sourcability" in b and b["sourcability"] not in VALID_SOURCABILITY:
            errs.append(f"{tag}: sourcability {b['sourcability']!r} not in "
                        f"{sorted(VALID_SOURCABILITY)}")
        if "source_native" in b and b["source_native"] not in VALID_SOURCE_NATIVE:
            errs.append(f"{tag}: source_native {b['source_native']!r} not in "
                        f"{sorted(VALID_SOURCE_NATIVE)}")

        q = b.get("queries")
        if not isinstance(q, dict):
            errs.append(f"{tag}: missing or malformed `queries` dict")
        else:
            for reg in REGISTERS_REQUIRED:
                if reg not in q:
                    sev = errs if reg == "shorts" else warns
                    sev.append(
                        f"{tag}: no `{reg}` register."
                        + (" Step 3's ShortsBackend runs `shorts` and "
                           "`platform` only — without `shorts` it loses half "
                           "its input, and Shorts is the only vertical surface "
                           "with a reachable search index."
                           if reg == "shorts" else
                           " Generate it or state why it was skipped."))
            if b.get("orientation") == "horizontal" and q.get("victim"):
                warns.append(
                    f"{tag}: `victim` register on a horizontal beat. The query "
                    f"generator's recall@30 eval (n=8) found it contributed "
                    f"zero there. Spend it knowingly or drop it.")

        # routing sanity: a beat that cannot be searched should not be searched
        if b.get("source_native") not in (None, "none") and \
                b.get("sourcability") != "none":
            warns.append(
                f"{tag}: source_native={b.get('source_native')!r} means a native "
                f"post exists. Per the extractor that post *is* the pick — route "
                f"this beat to the manual lane at Checkpoint 1 rather than "
                f"searching for a repost.")

    return errs, warns


def check_picks(path):
    data = load(path)
    if not isinstance(data, list):
        return [f"{path}: expected a JSON array"], []
    errs, warns = [], []

    for i, p in enumerate(data):
        tag = p.get("beat_id", f"index {i}")
        for f in PICK_REQUIRED:
            if f not in p:
                errs.append(
                    f"{tag}: missing `{f}`. The clip grader emits it and Step 8 "
                    f"needs it — a reduced picks.json makes the report "
                    f"unbuildable.")
        ranked = p.get("ranked")
        if ranked is None:
            continue
        if not isinstance(ranked, list):
            errs.append(f"{tag}: `ranked` must be a list")
            continue
        if not ranked and p.get("flagged"):
            errs.append(f"{tag}: flagged a pick but `ranked` is empty")
        for j, r in enumerate(ranked):
            for f in RANKED_REQUIRED:
                if f not in r:
                    errs.append(f"{tag} ranked[{j}]: missing `{f}`")
            for k, seg in enumerate(r.get("segments") or []):
                for f in SEGMENT_REQUIRED:
                    if f not in seg:
                        errs.append(f"{tag} ranked[{j}].segments[{k}]: "
                                    f"missing `{f}`")
                if not (seg.get("outcue") or "").strip():
                    errs.append(
                        f"{tag} ranked[{j}].segments[{k}]: empty outcue. An "
                        f"unverified outcue never gets written — flag the beat "
                        f"unverified instead.")

    # Step 8 derivability
    present = set()
    for p in data:
        present |= set(p)
        for r in p.get("ranked") or []:
            present |= set(r)
    dead = []
    for callout, needs in STEP8_NEEDS.items():
        missing = [n for n in needs if n not in present]
        if missing:
            dead.append((callout, missing))
    for callout, missing in dead:
        errs.append(f"Step 8 callout '{callout}' is not derivable — no {missing} "
                    f"anywhere in the file.")
    return errs, warns


def emit(label, errs, warns):
    print(f"\n{label}")
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
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    mode = sys.argv[1]
    bad = 0
    if mode in ("beats", "both"):
        e, w = check_beats(sys.argv[2])
        bad += emit(f"BEATS CONTRACT — {sys.argv[2]}", e, w)
    if mode in ("picks", "both"):
        path = sys.argv[3] if mode == "both" else sys.argv[2]
        e, w = check_picks(path)
        bad += emit(f"PICKS CONTRACT — {path}", e, w)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
