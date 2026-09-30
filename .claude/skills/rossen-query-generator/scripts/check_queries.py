#!/usr/bin/env python3
"""check_queries.py — validate a generated query record against the output contract.

Usage:
    python3 scripts/check_queries.py queries.json
    python3 scripts/check_queries.py queries.json --json

Exists because this skill's product is a machine-consumed contract: the pipeline's
search backends read `queries` by register name, and the clip grader reads the
orientation-crossing tag. A malformed record does not error — the affected search
leg just silently returns less, and nobody finds out until a beat comes back empty.

Checks the five register keys, per-register string counts, the `#shorts`
suffix-ownership rule, orientation filtering in both directions, and the
`platform_map` / `shorts_search` blocks.

Exit: 0 clean, 1 contract violation, 2 unreadable.
"""

import argparse
import json
import re
import sys

REGISTERS = ["anchor", "news", "victim", "platform", "shorts"]

# per-register bands, reconciled with the worked example (~10-15 strings/beat)
BANDS = {
    "anchor": (0, 3),      # 0 is legitimate — not every beat has a dated anchor
    "news": (2, 5),
    "victim": (0, 3),      # measured 0 on horizontal/YouTube; see eval.md
    "platform": (2, 4),
    "shorts": (2, 5),
}
PER_BEAT_MAX = 18

# roles → allowed platforms, from the per-role weighting table
ROLE_PLATFORMS = {
    "victim_interview": {"youtube", "shorts", "news_web"},
    "confrontation_bust": {"youtube", "shorts", "tiktok"},
    "evidence": {"tiktok", "shorts", "facebook", "reddit"},
    "explainer_demo/creator_short": {"shorts", "tiktok", "instagram"},
    "explainer_demo/creator_long": {"youtube"},
    "authority_report": {"youtube", "news_web"},
    "debunk": {"youtube", "news_web"},
    "first_person_rant": {"shorts", "tiktok", "instagram"},
}
VERTICAL_ONLY = {"tiktok", "instagram", "facebook"}


def check(rec):
    errs, warns = [], []
    bid = rec.get("beat_id", "<no beat_id>")
    role = rec.get("clip_role")
    orient = rec.get("orientation")

    for f in ("beat_id", "clip_role", "orientation", "queries"):
        if f not in rec:
            errs.append(f"{bid}: missing top-level `{f}`")
    q = rec.get("queries")
    if not isinstance(q, dict):
        return [f"{bid}: `queries` must be an object keyed by register"], []

    # ---- five registers, not four
    for reg in REGISTERS:
        if reg not in q:
            sev = errs if reg in ("news", "platform", "shorts") else warns
            sev.append(
                f"{bid}: no `{reg}` register key."
                + (" The pipeline's ShortsBackend reads `shorts` by name — a "
                   "record without it starves the only vertical surface with a "
                   "reachable search index."
                   if reg == "shorts" else
                   " Emit the key with an empty list and a reason rather than "
                   "omitting it, so a deliberate skip is distinguishable from a "
                   "generation miss."))

    total = 0
    for reg, strings in q.items():
        if reg not in REGISTERS:
            warns.append(f"{bid}: unknown register `{reg}`")
            continue
        if not isinstance(strings, list):
            errs.append(f"{bid}.{reg}: must be a list of strings")
            continue
        total += len(strings)
        lo, hi = BANDS[reg]
        if not lo <= len(strings) <= hi:
            errs.append(f"{bid}.{reg}: {len(strings)} strings, band is {lo}-{hi}")
        for s in strings:
            if not isinstance(s, str) or not s.strip():
                errs.append(f"{bid}.{reg}: empty or non-string query")
                continue
            wc = len(s.split())
            if reg == "shorts":
                if re.search(r"#shorts\b", s, re.I):
                    errs.append(
                        f"{bid}.shorts: {s!r} bakes in `#shorts`. The harvest "
                        f"step appends the suffix — baking it in double-appends "
                        f"it and eats query length. Topical hashtags "
                        f"(`#scamalert`) belong in the string; `#shorts` does "
                        f"not.")
                if wc > 7:
                    warns.append(f"{bid}.shorts: {s!r} is {wc} words; the "
                                 f"dialect is 3-5 plus a hashtag or two.")
            if reg == "platform" and wc > 6:
                warns.append(f"{bid}.platform: {s!r} is {wc} words; TikTok "
                             f"search degrades badly past four or five.")
            if reg == "news" and re.search(r"\b(I|my|me)\b", s):
                warns.append(f"{bid}.news: {s!r} reads first person; news "
                             f"register is third-person headline syntax.")

    if total > PER_BEAT_MAX:
        errs.append(f"{bid}: {total} strings for this beat, ceiling is "
                    f"{PER_BEAT_MAX}. At 10-12 beats an episode this is the "
                    f"difference between a 2-minute and a 10-minute search stage.")

    # ---- anchor should reuse the beat's prebuilt news_anchor when present
    na = rec.get("news_anchor")
    if na:
        anchors = [a.lower() for a in q.get("anchor", [])]
        if not any(na.lower() in a or a in na.lower() for a in anchors):
            warns.append(
                f"{bid}: beat record carries news_anchor={na!r} but no anchor "
                f"query reuses it. That string is prebuilt upstream — make it "
                f"anchor query #1 rather than regenerating around it.")

    # ---- orientation is a hard filter in both directions
    pmap = rec.get("platform_map", {})
    if orient == "horizontal":
        for p in set(pmap) & VERTICAL_ONLY:
            errs.append(f"{bid}: horizontal beat maps to `{p}`. Orientation is "
                        f"producer-authored and predicted platform correctly in "
                        f"26 of 26 observed cases.")
    elif orient == "vertical":
        if "youtube" in pmap:
            errs.append(f"{bid}: vertical beat maps to `youtube` long-form. "
                        f"Shorts is the exception, not YouTube long-form.")
    if "shorts" not in pmap:
        warns.append(f"{bid}: `shorts` missing from platform_map. Shorts runs on "
                     f"every orientation.")

    # ---- role/platform agreement
    if role in ROLE_PLATFORMS:
        stray = set(pmap) - ROLE_PLATFORMS[role] - {"shorts"}
        if stray:
            warns.append(f"{bid}: platform_map has {sorted(stray)} not in the "
                         f"weighting table's row for `{role}`.")

    # ---- shorts_search block
    ss = rec.get("shorts_search", {})
    if q.get("shorts"):
        if ss.get("suffix") != "#shorts":
            errs.append(f"{bid}: shorts_search.suffix must be '#shorts' — it is "
                        f"what the harvest step appends.")
        if "duration" not in str(ss.get("match_filter", "")):
            errs.append(f"{bid}: shorts_search.match_filter must set a duration "
                        f"ceiling; without it the #shorts token alone leaks "
                        f"long-form uploads.")
        if "surfaced_for" in ss:
            errs.append(
                f"{bid}: `surfaced_for` does not belong in shorts_search. It is "
                f"a per-candidate tag the harvester applies to each Shorts "
                f"result returned for a horizontal beat, because the grader "
                f"reads it per candidate. Use "
                f"shorts_search.cross_orientation: true instead.")
        if orient == "horizontal" and not ss.get("cross_orientation"):
            warns.append(f"{bid}: horizontal beat with Shorts queries should set "
                         f"shorts_search.cross_orientation: true so the "
                         f"harvester tags candidates for the grader.")
    return errs, warns


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    try:
        data = json.load(open(a.path, encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"could not read {a.path}: {exc}", file=sys.stderr)
        sys.exit(2)

    records = data if isinstance(data, list) else [data]
    all_e, all_w = [], []
    for rec in records:
        e, w = check(rec)
        all_e += e
        all_w += w

    if a.json:
        print(json.dumps({"errors": all_e, "warnings": all_w}, indent=1))
    else:
        print(f"\nQUERY CONTRACT — {a.path}  ({len(records)} beat record(s))")
        print("=" * 70)
        for e in all_e:
            print(f"  x {e}")
        for w in all_w:
            print(f"  ! {w}")
        if not all_e and not all_w:
            print("  contract clean.")
        print(f"\n  {len(all_e)} violation(s), {len(all_w)} warning(s)\n")
    sys.exit(1 if all_e else 0)


if __name__ == "__main__":
    main()
