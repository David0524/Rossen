#!/usr/bin/env python3
"""check_source_log.py — enforce the house SOURCE LOG format.

Usage:
    python3 scripts/check_source_log.py review.md

Reads a finished review, finds the SOURCE LOG table, and checks it against the
house format taken from the Airbnb/Vrbo review of Fri Jul 31:

  - `SOURCE LOG` heading, then one table, at the bottom of the document
  - header row exactly: CLAIM | CONFIDENCE | SCOPE | SOURCE
  - broken into ALL-CAPS group rows — the by-story / by-evidence-cluster
    breakdown. Group rows carry the name in CLAIM and leave the rest empty
  - no claim row before the first group row
  - the three standing groups present: CLIP SOURCES,
    PRODUCER QUESTIONS — ANSWERED, TEASE / BODY CONSISTENCY
  - no leftover skeleton placeholders or `(line N)` prefixes
  - every confidence value from the allowed set
  - every row carrying a figure has a non-empty SCOPE
  - SOURCE is a real URL, a back-reference ("Same.", "DOJ."), or an em dash —
    never a placeholder or an invented-looking citation

Exit codes: 0 = format clean, 1 = defects, 2 = no source log found.
"""

import re
import sys

HEADER_CELLS = ["CLAIM", "CONFIDENCE", "SCOPE", "SOURCE"]
ALLOWED_CONF = {"CONFIRMED", "PARTIALLY CONFIRMED", "UNVERIFIED",
                "CONTRADICTED", ""}
STANDING = ["CLIP SOURCES", "PRODUCER QUESTIONS", "TEASE / BODY CONSISTENCY"]
PLACEHOLDERS = re.compile(r"NAME THIS EVIDENCE CLUSTER|\(line \d+\)|TBD|XXX|"
                          r"\[source\]|LOREM", re.I)
FIGURE = re.compile(r"\$\s?[\d,]+|\d+(?:\.\d+)?\s?%|\b\d[\d,]*\s*"
                    r"(?:MILLION|BILLION|THOUSAND)\b|\b\d{4,}\b", re.I)
# house back-reference style, taken from the Airbnb log: "Same.",
# "Same Spotlight, footnote 1.", "DOJ.", "Brasler, in the Scripps package."
BACKREF = re.compile(r"^\s*(?:—\s*)?(same\b|ibid\b|as above\b|[A-Z]{2,8}\b|"
                     r"[A-Z][A-Za-z']+(?:\s+[a-z']+)*[,.]?\s)", re.I)
NAMED_PROV = re.compile(r"[A-Z][A-Za-z]{2,}")
URLISH = re.compile(r"https?://|\b[a-z0-9][a-z0-9-]*\.(?:gov|org|com|net)\b", re.I)


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def main(path):
    try:
        text = open(path, encoding="utf-8").read()
    except OSError as exc:
        print(f"could not read {path}: {exc}", file=sys.stderr)
        sys.exit(2)

    m = re.search(r"^#{1,4}\s*(?:\d+\.\s*)?SOURCE LOG\s*$", text, re.I | re.M)
    if not m:
        print("No `SOURCE LOG` heading found. The log is a required third "
              "artifact and belongs at the bottom of the review.",
              file=sys.stderr)
        sys.exit(2)

    tail = text[m.end():]
    rows = [l for l in tail.split("\n") if l.strip().startswith("|")]
    if not rows:
        print("SOURCE LOG heading present but no table beneath it.",
              file=sys.stderr)
        sys.exit(2)

    errs, warns = [], []

    # ---- header
    head = [c.upper() for c in cells(rows[0])]
    if head != HEADER_CELLS:
        errs.append(f"Header row is {head}, must be exactly {HEADER_CELLS}. "
                    f"Extra columns are fine only if these four lead, in order.")
    body = [r for r in rows[1:] if not re.fullmatch(r"\|[-: |]+\|", r.strip())]

    groups, claims, first_group_at = [], 0, None
    for i, r in enumerate(body):
        c = cells(r)
        if len(c) < 4:
            errs.append(f"row {i+1}: {len(c)} cells, need 4 — {r.strip()[:60]!r}")
            continue
        claim, conf, scope, src = c[0], c[1], c[2], c[3]
        bare = re.sub(r"\*+", "", claim).strip()
        is_group = bool(bare) and bare.upper() == bare and not conf and \
            not scope and not src and len(bare.split()) <= 10

        if is_group:
            groups.append(bare.upper())
            if first_group_at is None:
                first_group_at = i
            if not claim.strip().startswith("**"):
                warns.append(f"row {i+1}: group row {bare!r} should be bold so "
                             f"it reads as a break in the table.")
            continue

        claims += 1
        if first_group_at is None:
            errs.append(f"row {i+1}: claim row appears before any group row. "
                        f"Every claim sits under a named group — that is the "
                        f"by-story breakdown.")
        if PLACEHOLDERS.search(r):
            errs.append(f"row {i+1}: leftover skeleton placeholder — "
                        f"{PLACEHOLDERS.search(r).group(0)!r}")
        if conf.upper() not in ALLOWED_CONF:
            errs.append(f"row {i+1}: confidence {conf!r} not in "
                        f"{sorted(ALLOWED_CONF - {''})}. Leave it blank for "
                        f"non-fact-check issues rather than inventing a label.")
        if FIGURE.search(claim) and not scope:
            errs.append(f"row {i+1}: row carries a figure but SCOPE is empty. "
                        f"A figure without its scope cannot be audited and is "
                        f"how a fact-check introduces error — {bare[:50]!r}")
        if conf.upper() == "UNVERIFIED":
            # house style is an em dash, optionally followed by why. A URL here
            # contradicts the label.
            if URLISH.search(src):
                errs.append(f"row {i+1}: UNVERIFIED but SOURCE carries a URL — "
                            f"{src[:44]!r}. If a source was found the label is "
                            f"not UNVERIFIED.")
            elif not src:
                warns.append(f"row {i+1}: UNVERIFIED with an empty SOURCE. Use "
                             f"an em dash, and say why in the same cell.")
        elif conf.upper() in {"CONFIRMED", "PARTIALLY CONFIRMED",
                              "CONTRADICTED"}:
            if not src:
                errs.append(f"row {i+1}: {conf} with an empty SOURCE. A label "
                            f"without a pointer cannot be audited.")
            elif not (URLISH.search(src) or BACKREF.match(src)
                      or NAMED_PROV.search(src)):
                errs.append(f"row {i+1}: {conf} but SOURCE names nothing "
                            f"traceable — {src[:44]!r}.")
            elif not URLISH.search(src) and not BACKREF.match(src):
                warns.append(f"row {i+1}: {conf} with a named source but no URL "
                             f"and no back-reference — {src[:40]!r}. Fine for a "
                             f"video package; add a URL if one exists.")

    for want in STANDING:
        if not any(want.upper() in g for g in groups):
            errs.append(f"missing standing group {want!r}. All three appear in "
                        f"every log, empty if there is nothing to report.")

    if len(groups) < 2:
        warns.append(f"only {len(groups)} group row(s). The log is grouped by "
                     f"story or evidence cluster; a flat table loses the "
                     f"breakdown.")

    print(f"\n{path} — SOURCE LOG")
    print("=" * 66)
    print(f"  groups {len(groups)}   claim rows {claims}   "
          f"errors {len(errs)}   warnings {len(warns)}")
    if groups:
        print("\n  group order:")
        for g in groups:
            print(f"    · {g}")
    print()
    for e in errs:
        print(f"  x {e}")
    for w in warns:
        print(f"  ! {w}")
    if not errs and not warns:
        print("  format clean.")
    print()
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
