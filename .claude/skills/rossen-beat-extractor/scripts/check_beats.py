#!/usr/bin/env python3
"""check_beats.py — validate beat records against the contract three skills read.

Usage:
    python3 scripts/check_beats.py beats.json
    python3 scripts/check_beats.py beats.json --day friday
    python3 scripts/check_beats.py beats.json --json

This skill is upstream of everything, so a field defect here propagates to the
query generator, the search router and the grader. Two kinds of check:

  per-record — required fields, role vocabulary, orientation/platform agreement
  set-level  — the distribution checks that are invisible one beat at a time,
               above all `priority`, which has historically collapsed to a
               constant and silently made the downstream Whisper allocation
               arbitrary

Exit: 0 clean, 1 violation, 2 unreadable.
"""

import argparse
import json
import re
import sys
from collections import Counter

REQUIRED = [
    "beat_id", "episode", "segment_title", "script_text", "orientation",
    "clip_role", "news_anchor", "visual_spec", "platforms", "offsite_likely",
    "priority", "expected_segments", "sourcability", "source_native",
]

# Eight values across seven families. Must stay identical to the
# rossen-query-generator per-role weighting table — that is the one handoff in
# this system with no drift, and it is worth keeping that way.
ROLES = {
    "victim_interview", "confrontation_bust", "evidence",
    "explainer_demo/creator_short", "explainer_demo/creator_long",
    "authority_report", "debunk", "first_person_rant",
}
PLATFORMS = {"youtube", "shorts", "tiktok", "facebook", "instagram", "reddit",
             "news_web"}
VERTICAL_ONLY = {"tiktok", "instagram", "facebook"}
SOURCABILITY = {"high", "commentary_only", "none", "throttled", "unchecked"}
SOURCE_NATIVE = {"instagram", "x", "tiktok", "none"}

BAND = {"wednesday": (10, 12), "friday": (0, 5)}
PRIORITY_1_CEILING = 0.55      # see the calibration note in SKILL.md
SEARCH_ENGINE_SMELL = re.compile(
    r"footage (related to|of)|video (about|related)|clip (about|showing that)",
    re.I)


def check_record(b, i):
    errs, warns = [], []
    tag = b.get("beat_id") or f"index {i}"

    if "role" in b and "clip_role" not in b:
        errs.append(f"{tag}: field is named `role`. The contract field is "
                    f"`clip_role` — the query generator, the search router and "
                    f"the grader all read `clip_role`.")
    for f in REQUIRED:
        if f not in b:
            errs.append(f"{tag}: missing `{f}`")

    role = b.get("clip_role")
    if role and role not in ROLES:
        if role == "other" or role == "explainer_demo":
            errs.append(
                f"{tag}: clip_role={role!r} is not in the vocabulary. "
                + ("`other` has no weighting row downstream — assign the closest "
                   "of the eight values and put the mismatch in `role_note`."
                   if role == "other" else
                   "`explainer_demo` must be emitted split: "
                   "`explainer_demo/creator_short` or "
                   "`explainer_demo/creator_long`."))
        else:
            errs.append(f"{tag}: unknown clip_role {role!r}. Valid: "
                        f"{sorted(ROLES)}")

    orient = b.get("orientation")
    if orient not in {"horizontal", "vertical", None}:
        errs.append(f"{tag}: orientation {orient!r} must be horizontal or vertical")

    plats = b.get("platforms") or []
    if not isinstance(plats, list) or not plats:
        errs.append(f"{tag}: `platforms` must be a non-empty list")
    else:
        for p in plats:
            if p not in PLATFORMS:
                errs.append(f"{tag}: unknown platform {p!r}. Valid: "
                            f"{sorted(PLATFORMS)}")
        if orient == "horizontal":
            bad = set(plats) & VERTICAL_ONLY
            if bad:
                errs.append(f"{tag}: horizontal beat lists {sorted(bad)}. "
                            f"Orientation is producer-authored and held in every "
                            f"observed case; it is a hard filter both ways.")
        elif orient == "vertical" and "youtube" in plats:
            errs.append(f"{tag}: vertical beat lists `youtube` long-form. "
                        f"`shorts` is the exception, not `youtube`.")
        if "shorts" not in plats:
            warns.append(f"{tag}: no `shorts` platform. Shorts runs on every "
                         f"orientation — it is often where the raw moment lives "
                         f"without a reporter standup on top of it.")

    pr = b.get("priority")
    if pr not in {1, 2, 3, None}:
        errs.append(f"{tag}: priority {pr!r} must be 1, 2 or 3")

    es = b.get("expected_segments")
    if es is not None and (not isinstance(es, int) or es < 1):
        errs.append(f"{tag}: expected_segments must be an integer >= 1")

    sc = b.get("sourcability")
    if sc is not None and sc not in SOURCABILITY:
        errs.append(f"{tag}: sourcability {sc!r} not in {sorted(SOURCABILITY)}")
    if sc in {"none", "commentary_only", "throttled"} and \
            not (b.get("sourcability_note") or "").strip():
        errs.append(f"{tag}: sourcability={sc!r} needs a `sourcability_note` "
                    f"saying what was searched and what came back. A bare "
                    f"downgrade is not actionable at Checkpoint 1.")
    if sc == "throttled":
        warns.append(f"{tag}: sourcability=throttled — a network condition, not "
                     f"an absence of footage. Re-run this beat's scan before "
                     f"the producer rules on it; do not swap or drop on it.")

    sn = b.get("source_native")
    if sn is not None and sn not in SOURCE_NATIVE:
        errs.append(f"{tag}: source_native {sn!r} not in {sorted(SOURCE_NATIVE)}")
    if sn and sn != "none":
        if sc == "none":
            errs.append(
                f"{tag}: source_native={sn!r} but sourcability=none. A native "
                f"post existing is the opposite of un-sourceable — this beat is "
                f"un-*searchable*. Route it to the manual lane.")
        warns.append(f"{tag}: source_native={sn!r} — manual lane. Hand over the "
                     f"original permalink; do not search for a repost.")

    vs = b.get("visual_spec") or ""
    if SEARCH_ENGINE_SMELL.search(vs):
        warns.append(f"{tag}: visual_spec {vs!r} reads like a search string. "
                     f"Describe what a producer would see in the thumbnail.")
    if vs and len(vs.split()) < 4:
        warns.append(f"{tag}: visual_spec is {len(vs.split())} words — too thin "
                     f"to make a contact sheet scannable.")

    st = b.get("script_text") or ""
    if re.search(r"PLAY CLIP|\(\(\(", st):
        errs.append(f"{tag}: script_text contains a production marker. Collect "
                    f"the dash-bulleted setup lines only.")
    if st and not re.search(r"\$[\d,]|\d", st) and not b.get("news_anchor"):
        warns.append(f"{tag}: no figure in script_text and no news_anchor. The "
                     f"searchable specifics may not have been captured.")

    if b.get("beat_id") and not re.match(r"^\d{2}-\d{2}-([A-Z]\d{1,2}|b\d{2})$",
                                         b["beat_id"]):
        warns.append(f"{tag}: beat_id should look like `10-07-A5` (outline row) "
                     f"or `06-03-b03` (script-mode back-fill)")
    return errs, warns


def check_set(beats, day):
    errs, warns = [], []
    n = len(beats)
    lo, hi = BAND[day]
    if not lo <= n <= hi:
        warns.append(
            f"{n} beats extracted; {day} band is {lo}-{hi}. "
            + ("Above the band usually means the cold open or a mid-show tease "
               "was extracted — those restate segments in beat language and "
               "produce unresolvable duplicates."
               if n > hi else
               "Below the band is normal on Friday and suspicious on Wednesday."))

    prio = [b.get("priority") for b in beats if b.get("priority")]
    if len(prio) >= 5:
        share1 = prio.count(1) / len(prio)
        if share1 > PRIORITY_1_CEILING:
            errs.append(
                f"priority is degenerate: {prio.count(1)}/{len(prio)} beats "
                f"({round(100*share1)}%) are priority 1, ceiling is "
                f"{round(100*PRIORITY_1_CEILING)}%. Graded by consequence rather "
                f"than setup length, roughly a third of beats are priority 1. A "
                f"field that reads 1 for almost everything looks like signal and "
                f"carries none, and the pipeline allocates its transcript budget "
                f"from it.")
        if len(set(prio)) == 1:
            errs.append(f"every beat is priority {prio[0]} — the field is "
                        f"carrying no information at all.")

    roles = Counter(b.get("clip_role") for b in beats)
    if n >= 6 and len(roles) < 3:
        warns.append(f"only {len(roles)} distinct roles across {n} beats "
                     f"({dict(roles)}). Real episodes mix four or more.")

    ve = [b.get("beat_id") for b in beats
          if b.get("clip_role") == "evidence" and b.get("orientation") == "vertical"
          and b.get("sourcability") == "none"]
    if ve:
        warns.append(
            f"vertical `evidence` beats flagged sourcability=none: {ve}. The "
            f"yield log shows this shape failing in the *search* pipeline, but "
            f"two such beats aired from native TikTok. Check `source_native` "
            f"before writing this shape off — the finding is a routing signal, "
            f"not a suppression rule.")

    ids = [b.get("beat_id") for b in beats]
    dupes = [i for i, c in Counter(ids).items() if c > 1]
    if dupes:
        errs.append(f"duplicate beat_id(s): {dupes}")
    return errs, warns


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--day", default="wednesday", choices=["wednesday", "friday"])
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    try:
        data = json.load(open(a.path, encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"could not read {a.path}: {exc}", file=sys.stderr)
        sys.exit(2)

    beats = data if isinstance(data, list) else [data]
    errs, warns = [], []
    for i, b in enumerate(beats):
        e, w = check_record(b, i)
        errs += e
        warns += w
    e, w = check_set(beats, a.day)
    errs += e
    warns += w

    if a.json:
        print(json.dumps({"errors": errs, "warnings": warns}, indent=1))
    else:
        prio = Counter(b.get("priority") for b in beats)
        print(f"\nBEAT CONTRACT — {a.path}  ({len(beats)} beats, {a.day})")
        print("=" * 72)
        print(f"  priority spread {dict(sorted(prio.items(), key=lambda x: str(x[0])))}"
              f"   roles {len(set(b.get('clip_role') for b in beats))}\n")
        for x in errs:
            print(f"  x {x}")
        for x in warns:
            print(f"  ! {x}")
        if not errs and not warns:
            print("  contract clean.")
        print(f"\n  {len(errs)} violation(s), {len(warns)} warning(s)\n")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
