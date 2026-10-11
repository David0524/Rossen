#!/usr/bin/env python3
"""build_bible.py — render a bible draft (markdown) to house-format .docx.

Usage:
    python3 scripts/build_bible.py draft.md "07_29 F2 BIBLE.docx"

Input is the same markdown file check_bible.py reads, so one artifact is both
validated and rendered. Formatting rules live in docx-format.md; this script is
the implementation of record. Do not hand-build the document or convert with
pandoc — neither reproduces run-level colour, and red-vs-black is production
semantics, not styling: black is what Jeff says, red is an instruction.

Line classification:
  (((...)))  or  ((...))     production cue   18pt bold red FF0000
  OUT:                       production cue   18pt bold red, no blank above it
  **ALL CAPS**  full line    header           23pt bold black
  —-----  or  ______         separator        23pt bold black
  HIT LIKE / JOIN THE CHAT   CTA              18pt regular black
  END OF SHOW                                 18pt bold black
  all-caps lines inside a graphic card         18pt regular red
  first line after an OUT:   re-entry line    23pt bold black
  [[PAGE BREAK]]             hard page break  between stories and cases
  everything else            spoken body      18pt regular black

A {{JEFF PLEASE NOTE: ...}} span anywhere in a line is removed from the text
and attached to that paragraph as a Word comment.

Inline **bold** becomes a bold run. [text](url) becomes a blue underlined link.
"""

import re
import sys

try:
    from docx import Document
    from docx.enum.text import WD_LINE_SPACING
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    from docx.shared import Pt, Inches, RGBColor
except ImportError:
    sys.exit("python-docx is required:  pip install python-docx "
             "--break-system-packages")

FONT = "Arial"
BLACK = RGBColor(0x00, 0x00, 0x00)
RED = RGBColor(0xFF, 0x00, 0x00)
LINK_BLUE = "1155CC"

CUE_OPEN = re.compile(r"^\(\(+")
SEPARATOR = re.compile(r"^[\u2014\-_=]{4,}$")
CTA = ("HIT LIKE AND SUBSCRIBE", "JOIN THE CHAT", "BECOME A MEMBER",
       "SEND IN YOUR LIVE REQUESTS")
CARD_OPENER = re.compile(r"CREATE FULL SCREEN GRAPHIC|TAKE FULLSCREEN")
LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
NOTE = re.compile(r"\{\{\s*(.*?)\s*\}\}")
PAGE_BREAK = re.compile(r"^\[\[\s*PAGE BREAK\s*\]\]$", re.I)
COMMENT_AUTHOR, COMMENT_INITIALS = "Claude", "C"


def strip_md(s):
    return re.sub(r"\*+", "", s).strip()


def set_font(run, size, bold, color):
    run.font.name = FONT
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), FONT)


def add_hyperlink(par, text, url):
    part = par.part
    r_id = part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True)
    link = OxmlElement("w:hyperlink")
    link.set(qn("r:id"), r_id)
    r = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    for tag, val in (("w:color", LINK_BLUE), ("w:u", "single")):
        el = OxmlElement(tag)
        el.set(qn("w:val"), val)
        rpr.append(el)
    fonts = OxmlElement("w:rFonts")
    for attr in ("w:ascii", "w:hAnsi", "w:cs"):
        fonts.set(qn(attr), FONT)
    rpr.append(fonts)
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), "36")            # half-points: 18pt
    rpr.append(sz)
    r.append(rpr)
    t = OxmlElement("w:t")
    t.text = text
    t.set(qn("xml:space"), "preserve")
    r.append(t)
    link.append(r)
    par._p.append(link)


def page_break(doc):
    from docx.enum.text import WD_BREAK
    par = doc.add_paragraph()
    par.add_run().add_break(WD_BREAK.PAGE)
    return par


def attach_notes(doc, par, notes):
    for note in notes:
        if not note.upper().startswith("JEFF PLEASE NOTE"):
            note = "JEFF PLEASE NOTE: " + note
        runs = [r for r in par.runs if r.text.strip()] or [par.add_run(" ")]
        doc.add_comment(runs, text=note, author=COMMENT_AUTHOR,
                        initials=COMMENT_INITIALS)


def emit(doc, text, size, bold, color, inline=True):
    """One paragraph. `inline` parses **bold** and [text](url) inside it."""
    par = doc.add_paragraph()
    pf = par.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.15
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)

    if not inline:
        set_font(par.add_run(strip_md(text)), size, bold, color)
        return par

    for chunk in re.split(r"(\[[^\]]+\]\([^)]+\))", text):
        if not chunk:
            continue
        m = LINK.fullmatch(chunk)
        if m:
            add_hyperlink(par, m.group(1), m.group(2))
            continue
        for i, seg in enumerate(re.split(r"\*\*", chunk)):
            if seg == "":
                continue
            set_font(par.add_run(seg), size, bold or (i % 2 == 1), color)
    return par


def build(src, out):
    with open(src, encoding="utf-8") as fh:
        lines = [l.rstrip() for l in fh.read().split("\n")]

    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Inches(8.5), Inches(11)
    for side in ("left", "right", "top", "bottom"):
        setattr(sec, f"{side}_margin", Inches(1))
    style = doc.styles["Normal"]
    style.font.name = FONT
    style.font.size = Pt(18)

    in_card = False
    prev_was_clip = False
    after_out = False
    first = True
    page_top = False

    for raw in lines:
        notes = NOTE.findall(raw)
        raw = NOTE.sub("", raw).rstrip()
        s = strip_md(raw)
        if PAGE_BREAK.match(s):
            if not first:
                page_break(doc)
                page_top = True
            continue
        if not s:
            continue

        upper = s.upper()
        is_cue = bool(CUE_OPEN.match(s))
        is_out = upper.startswith("OUT:")
        is_bullet = bool(re.match(r"^-\s*\S", s))

        # ---- graphic-card state
        if is_cue and CARD_OPENER.search(upper):
            in_card = True
        elif is_cue or is_bullet:
            in_card = False

        # ---- blank paragraph between elements
        blank = (not first and not page_top and not (prev_was_clip and is_out)
                 and not in_card)
        if blank:
            emit(doc, "", 18, False, BLACK, inline=False)
        page_top = False

        # ---- classify and emit
        if is_cue or is_out:
            par = emit(doc, s, 18, True, RED)
        elif after_out:
            # first line out of a clip: Jeff's re-entry point
            par = emit(doc, raw.strip(), 23, True, BLACK)
        elif SEPARATOR.match(s):
            par = emit(doc, s, 23, True, BLACK, inline=False)
        elif upper.replace("-", "").strip().startswith("END OF SHOW"):
            par = emit(doc, s, 18, True, BLACK, inline=False)
        elif any(upper.lstrip("- ").startswith(c) for c in CTA):
            par = emit(doc, s, 18, False, BLACK)
        elif in_card and not is_bullet:
            par = emit(doc, s, 18, False, RED)
        elif (raw.strip().startswith("**") and not is_bullet
              and s == upper and len(s.split()) <= 20):
            par = emit(doc, s, 23, True, BLACK)
        else:
            par = emit(doc, raw.strip(), 18, False, BLACK)

        attach_notes(doc, par, notes)
        if is_out:
            after_out = True
        elif not is_cue:
            after_out = False

        prev_was_clip = bool(re.search(r"PLAY CLIP", upper)) and is_cue
        first = False

    doc.save(out)
    print(f"wrote {out}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    build(sys.argv[1], sys.argv[2])
