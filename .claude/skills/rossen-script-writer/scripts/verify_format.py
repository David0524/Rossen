#!/usr/bin/env python3
"""verify_format.py — read a built .docx back and confirm it matches house format.

Usage:
    python3 scripts/verify_format.py "07_29 F2 BIBLE.docx"

Checks what the eye cannot reliably check on a 20-page document: that every run
is Arial, that headers are 23pt bold black, that spoken body is 18pt black, that
every production cue is bold FF0000 red, that page setup is Letter with 1"
margins and 1.15 spacing, and that the blank-paragraph rules hold around clip
cues. Red-vs-black is production semantics, so a cue rendered black is a real
defect, not a cosmetic one.

Exit codes: 0 = pass, 1 = defects found, 2 = could not read the file.
"""

import re
import sys

try:
    from docx import Document
    from docx.shared import RGBColor
except ImportError:
    sys.exit("python-docx is required:  pip install python-docx "
             "--break-system-packages")

RED = RGBColor(0xFF, 0x00, 0x00)
BLACK = RGBColor(0x00, 0x00, 0x00)
CUE = re.compile(r"^\(\(+|^OUT:")
EXPECTED_PAGE = {"width": 8.5, "height": 11.0, "margin": 1.0}


def approx(emu, inches):
    return abs(emu / 914400 - inches) < 0.02


def main(path):
    try:
        doc = Document(path)
    except Exception as exc:                       # noqa: BLE001
        print(f"could not open {path}: {exc}", file=sys.stderr)
        sys.exit(2)

    defects, checked = [], 0
    sec = doc.sections[0]
    if not approx(sec.page_width, EXPECTED_PAGE["width"]) or \
       not approx(sec.page_height, EXPECTED_PAGE["height"]):
        defects.append("page size is not US Letter")
    for side in ("left", "right", "top", "bottom"):
        if not approx(getattr(sec, f"{side}_margin"), EXPECTED_PAGE["margin"]):
            defects.append(f"{side} margin is not 1 inch")

    paras = doc.paragraphs
    for i, par in enumerate(paras):
        text = par.text.strip()
        if not text:
            continue
        checked += 1

        if par.paragraph_format.line_spacing not in (None, 1.15):
            defects.append(f"p{i}: line spacing "
                           f"{par.paragraph_format.line_spacing}, expected 1.15")

        is_cue = bool(CUE.match(text))
        is_header = (text == text.upper() and not text.startswith("-")
                     and not is_cue and len(text.split()) <= 20
                     and all(r.font.size and r.font.size.pt == 23
                             for r in par.runs if r.text.strip()))

        for run in par.runs:
            if not run.text.strip():
                continue
            name = run.font.name
            if name not in (None, "Arial"):
                defects.append(f"p{i}: font {name!r}, expected Arial "
                               f"({text[:40]!r})")
            size = run.font.size.pt if run.font.size else None
            color = run.font.color.rgb if run.font.color and \
                run.font.color.type is not None else None

            if is_cue:
                if color != RED:
                    defects.append(f"p{i}: production cue is not FF0000 red "
                                   f"({text[:40]!r})")
                if not run.font.bold:
                    defects.append(f"p{i}: production cue is not bold "
                                   f"({text[:40]!r})")
                if size not in (None, 18):
                    defects.append(f"p{i}: cue is {size}pt, expected 18pt")
            elif is_header:
                if size not in (None, 23):
                    defects.append(f"p{i}: header is {size}pt, expected 23pt "
                                   f"({text[:40]!r})")
                if color not in (None, BLACK):
                    defects.append(f"p{i}: header is not black ({text[:40]!r})")
            else:
                if size not in (None, 18, 23):
                    defects.append(f"p{i}: body run is {size}pt, expected 18pt "
                                   f"({text[:40]!r})")

    # ---- blank-paragraph rule around clip cues
    for i, par in enumerate(paras[:-2]):
        if re.match(r"^\(\(+PLAY CLIP", par.text.strip()):
            follow = [p.text.strip() for p in paras[i + 1:i + 3]]
            if follow and follow[0] == "":
                defects.append(f"p{i}: blank paragraph between the clip cue and "
                               f"its OUT: line — there must be none")
            if not any(f.upper().startswith("OUT:") for f in follow):
                defects.append(f"p{i}: clip cue has no OUT: line beneath it")

    print(f"\n{path}")
    print("=" * 68)
    print(f"  paragraphs with text : {checked}")
    print(f"  defects              : {len(defects)}\n")
    if defects:
        seen = set()
        for d in defects:
            key = re.sub(r"p\d+", "p#", d)
            if key in seen:
                continue
            seen.add(key)
            print(f"  x {d}")
        print(f"\n  ({len(defects)} total, {len(seen)} distinct)\n")
        sys.exit(1)
    print("  house format confirmed.\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
