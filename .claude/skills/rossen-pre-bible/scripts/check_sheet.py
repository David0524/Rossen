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
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\uFE0F]")


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
    if EMOJI.search(md):
        err("Emoji found. The sheet uses no emoji: write CHECK, LEGAL and VIRAL CLIP as words.")

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

        # Template v3 (Oct 26, 2026): a Status line with the score replaces Slot/Confidence.
        if not re.search(r"\*\*Status:\*\*", body):
            err(f"{tag}: no '**Status:**' line (READY / NEEDS ... / RETURNING THEME / RE-PITCH).")
        if not re.search(r"\*\*Score:\*\*\s*\d+\s*/\s*14", body):
            err(f"{tag}: no '**Score:** N/14' with the seven numbers from quality-gate.md.")
        if not re.search(r"\*\*Track:\*\*\s*(SCAM|CONSUMER)", body):
            warn(f"{tag}: no '**Track:** SCAM' or '**Track:** CONSUMER' on the status line (quality-gate.md, two tracks).")
        if re.search(r"\*\*Track:\*\*\s*CONSUMER", body) and not re.search(r"Stakes\s*\d", body):
            warn(f"{tag}: consumer-track card should score Stakes, not Fear.")
        if not re.search(r"Lead test", body, re.I):
            warn(f"{tag}: no lead-test result on the status line.")
        if not re.search(r"\*\*Built on:\*\*", body):
            err(f"{tag}: no '**Built on:**' line under the packaging (the proven title it copies, with its numbers).")
        if not re.search(r"### COVERAGE CHECK", body):
            err(f"{tag}: no COVERAGE CHECK section (transcripts, Rossen Stories coverage table, Drive bibles).")

        if not re.search(r"POTENTIAL PACKAGING", body, re.I):
            err(f"{tag}: no POTENTIAL PACKAGING. The page leads with three titles.")
        elif len(re.findall(r"^- ", body.split("POTENTIAL PACKAGING", 1)[1].split("###", 1)[0], re.M)) != 3:
            warn(f"{tag}: POTENTIAL PACKAGING should list exactly three titles.")

        if not re.search(r"### CASES", body):
            err(f"{tag}: no CASES section. Cases go under the packaging, each dated and sourced.")

        if not re.search(r"THE PITCH|THE HOOK", body, re.I):
            warn(f"{tag}: no THE PITCH section.")

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
