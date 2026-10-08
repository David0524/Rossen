#!/usr/bin/env python3
"""Mechanical compliance check on a Pre-Bible Pitch Sheet markdown source.

    python3 check_sheet.py sheet.md

Catches what reliably slips: a missing verification block, a story with no slot-fit
line, invented timecodes, a confidence rating that isn't HIGH/MEDIUM/LOW, a viral
flag with no URL. It cannot judge whether the ranking is right or whether a claim
is true. Those are yours.

Exit 1 on ERROR, 0 otherwise.
"""

import re
import sys

STORY_H1 = re.compile(r"^#\s+(\d+)\.\s+(.+)$", re.M)
TIMECODE = re.compile(r"\b\d{1,2}:\d{2}(?::\d{2})?\s*[-–]\s*\d{1,2}:\d{2}")
CONFIDENCE = re.compile(r"\*\*Confidence:\s*(HIGH|MEDIUM|LOW)\*\*")

errors, warnings = [], []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def split_stories(md):
    """Return [(number, headline, body)] for each story page."""
    marks = list(STORY_H1.finditer(md))
    out = []
    for idx, m in enumerate(marks):
        end = marks[idx + 1].start() if idx + 1 < len(marks) else len(md)
        out.append((m.group(1), m.group(2).strip(), md[m.start():end]))
    return out


def check(md):
    stories = split_stories(md)

    # --- document-level -----------------------------------------------------
    if not stories:
        err("No story pages found. Expected H1s like '# 1. STORY HEADLINE'.")

    if not re.search(r"SHORTLIST", md, re.I):
        err("No shortlist section. Page one is the ranked table.")

    if not re.search(r"RESEARCH SOURCES\s*&\s*VERIFICATION FLAGS", md, re.I):
        err("No 'RESEARCH SOURCES & VERIFICATION FLAGS' block. Sources are not "
            "optional and must be segregated from the pitch pages.")

    if not re.search(r"OPEN QUESTIONS FOR THE MEETING", md, re.I):
        err("No 'OPEN QUESTIONS FOR THE MEETING'. The sheet exists to get "
            "decisions made in the room.")

    if not re.search(r"cannot watch video|not watched|did not watch", md, re.I):
        err("Missing the 'I cannot watch video' disclosure. It goes in READ THIS "
            "FIRST and beside every clip.")

    if not re.search(r"SLATE FIT", md, re.I):
        warn("No SLATE FIT verdict under the shortlist. Say whether this slate "
             "can actually fill the show.")

    # --- invented specificity ----------------------------------------------
    for m in TIMECODE.finditer(md):
        err(f"Timecode range '{m.group(0)}' — you cannot watch video, so you "
            f"cannot produce a timecode. Remove it.")

    if re.search(r"^\s*(\*\*)?OUT:", md, re.M):
        err("An 'OUT:' outcue appears. Outcues come from a human who watched the "
            "footage. They belong in the bible, not the pitch sheet.")

    # --- per story ----------------------------------------------------------
    for num, headline, body in stories:
        tag = f"Story {num} ({headline[:40]})"

        ratings = re.findall(r"\*\*Confidence:\s*([A-Za-z]+)", body)
        if not ratings:
            err(f"{tag}: no '**Confidence: HIGH|MEDIUM|LOW**' on the slot line.")
        for r in ratings:
            if r.upper() not in ("HIGH", "MEDIUM", "LOW"):
                err(f"{tag}: confidence '{r}' is not HIGH / MEDIUM / LOW.")

        if not re.search(r"\*\*Slot:\*\*", body):
            err(f"{tag}: no '**Slot:**' line.")

        if not re.search(r"SLOT FIT", body, re.I):
            err(f"{tag}: no SLOT FIT line. Every story is tested against the "
                f"day's shape.")

        if not re.search(r"WORKING TEASE", body, re.I):
            err(f"{tag}: no WORKING TEASE.")

        if not re.search(r"THE HOOK", body, re.I):
            warn(f"{tag}: no THE HOOK section.")

        if not re.search(r"FOOTAGE", body, re.I):
            err(f"{tag}: no FOOTAGE section. Say what exists and what doesn't — "
                f"'FOOTAGE — BE HONEST ABOUT THIS' when it's thin.")

        if not re.search(r"THE PAYOFF", body, re.I):
            err(f"{tag}: no THE PAYOFF. Every story carries protection steps.")

        if "🔥" in body and not re.search(r"https?://", body):
            err(f"{tag}: viral flag with no URL. A viral flag needs URL, "
                f"platform, view count, date observed, and upload date.")

        if "🔥" in body and not re.search(r"view", body, re.I):
            warn(f"{tag}: viral flag with no view count recorded.")

        words = len(re.findall(r"\w+", body))
        if words > 620:
            warn(f"{tag}: ~{words} words — likely to spill past one page. Cut "
                 f"before building, and check the rendered PDF.")

    # --- verification block --------------------------------------------------
    vblock = re.split(r"RESEARCH SOURCES\s*&\s*VERIFICATION FLAGS", md, flags=re.I)
    if len(vblock) > 1:
        tail = vblock[1]
        if "Confirmed" not in tail:
            err("Verification block has no '**Confirmed:**' runs. Confirmed and "
                "unconfirmed must be visually separated.")
        if not re.search(r"NEEDS VERIFICATION", tail, re.I):
            err("Verification block has no 'NEEDS VERIFICATION' runs. A slate "
                "with nothing to check has not been checked.")
        if not re.search(r"Sources?:", tail, re.I):
            err("Verification block lists no sources.")
        for num, headline, _ in stories:
            if not re.search(rf"STORY\s*{num}\b", tail, re.I):
                warn(f"Story {num} has no entry in the verification block.")

    return errors, warnings


def main():
    if len(sys.argv) < 2:
        print("usage: check_sheet.py sheet.md")
        return 2
    with open(sys.argv[1], encoding="utf-8") as fh:
        md = fh.read()

    errs, warns = check(md)

    for e in errs:
        print(f"ERROR   {e}")
    for w in warns:
        print(f"WARN    {w}")
    if not errs and not warns:
        print("clean — mechanical checks pass.")
    print(f"\n{len(errs)} error(s), {len(warns)} warning(s).")
    print("Mechanical only. Ranking quality and factual accuracy are not checked.")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
