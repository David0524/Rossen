#!/usr/bin/env python3
"""build_bible_house.py — render a bible draft (the markdown check_bible.py reads)
in the team's current layout (Matt Raub's rewrite, bible-rewrite-nancy-mary.docx;
Ghost Tapping page conventions):

  - one paragraph per line, NO blank paragraphs between lines, 10pt after each
  - every section starts on a new page; its first line is the opener, 18pt bold
    (each **HEADER** line and each —---- separator starts a new section)
  - spoken lines 14pt regular black; production cues 14pt bold red FF0000
  - Arial, US Letter, 1.25" left/right and 1" top/bottom margins, single spacing
  - [text](url) -> blue underlined hyperlink; inline **bold** kept

Usage: python3 tools/build_bible_house.py draft.md "10_07 LIVE BIBLE.docx" [--html out.html]
"""
import re, sys, html as H
from docx import Document
from docx.enum.text import WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, Inches, RGBColor

RED, BLACK = RGBColor(0xFF, 0, 0), RGBColor(0, 0, 0)
LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
SEP = re.compile(r"^[—\-_]{4,}$")
CARD = re.compile(r"CREATE FULL SCREEN GRAPHIC|TAKE FULLSCREEN")


def plain(s):
    return re.sub(r"\*+", "", s).strip()


def classify(lines):
    """-> list of (kind, text, newpage). kind: opener | body | cue | card"""
    out, newpage, card = [], False, False
    for raw in lines:
        s = raw.strip()
        if not s:
            continue
        p = plain(s)
        if SEP.match(p):
            newpage = True
            continue
        is_cue = p.startswith("((") or p.upper().startswith("OUT:")
        caps = re.sub(r"Mc", "MC", p)
        is_head = (s.startswith("**") and s.endswith("**") and not p.startswith("-")
                   and not is_cue and caps == caps.upper())
        if is_cue and CARD.search(p.upper()):
            card = True
        elif is_cue or p.startswith("-") or is_head:
            card = False
        if is_head:
            out.append(("opener", "-" + p, bool(out)))
            newpage = False
            continue
        if is_cue:
            kind = "cue"
        elif card:
            kind = "card"
        else:
            kind = "body"
        if newpage and out:
            kind = "opener" if kind == "body" else kind
        out.append((kind, s if kind != "cue" else p, newpage and bool(out)))
        newpage = False
    return out


def run(par, text, size, bold, color):
    r = par.add_run(text)
    r.font.name, r.font.size, r.font.bold, r.font.color.rgb = "Arial", Pt(size), bold, color
    rpr = r._element.get_or_add_rPr()
    f = rpr.find(qn("w:rFonts"))
    if f is None:
        f = OxmlElement("w:rFonts")
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        f.set(qn(a), "Arial")
    rpr.append(f)


def link(par, text, url, size):
    r_id = par.part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True)
    h = OxmlElement("w:hyperlink"); h.set(qn("r:id"), r_id)
    r = OxmlElement("w:r"); rpr = OxmlElement("w:rPr")
    for tag, val in (("w:color", "1155CC"), ("w:u", "single"), ("w:sz", str(size * 2))):
        e = OxmlElement(tag); e.set(qn("w:val"), val); rpr.append(e)
    f = OxmlElement("w:rFonts")
    for a in ("w:ascii", "w:hAnsi", "w:cs"):
        f.set(qn(a), "Arial")
    rpr.append(f); r.append(rpr)
    t = OxmlElement("w:t"); t.text = text; t.set(qn("xml:space"), "preserve"); r.append(t)
    h.append(r); par._p.append(h)


STYLE = {"opener": (18, True, BLACK), "body": (14, False, BLACK),
         "cue": (14, True, RED), "card": (14, False, RED)}


def build_docx(items, out):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Inches(8.5), Inches(11)
    sec.left_margin = sec.right_margin = Inches(1.25)
    sec.top_margin = sec.bottom_margin = Inches(1)
    doc.styles["Normal"].font.name = "Arial"
    for kind, text, newpage in items:
        if newpage:
            doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
        par = doc.add_paragraph()
        par.paragraph_format.space_before = Pt(0)
        par.paragraph_format.space_after = Pt(10)
        size, bold, color = STYLE[kind]
        for chunk in re.split(r"(\[[^\]]+\]\([^)]+\))", text):
            if not chunk:
                continue
            m = LINK.fullmatch(chunk)
            if m:
                link(par, m.group(1), m.group(2), size)
                continue
            for i, seg in enumerate(re.split(r"\*\*", chunk)):
                if seg:
                    run(par, seg, size, bold or i % 2 == 1, color)
    doc.save(out)


def build_html(items, out):
    css = {"opener": "font-size:18pt;font-weight:bold", "body": "font-size:14pt",
           "cue": "font-size:14pt;font-weight:bold;color:#FF0000", "card": "font-size:14pt;color:#FF0000"}
    rows = ['<html><head><meta charset="utf-8"></head><body style="font-family:Arial">']
    for kind, text, newpage in items:
        t = H.escape(text, quote=False)
        t = LINK.sub(r'<a href="\2" style="color:#1155CC">\1</a>', t)
        t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
        pb = "page-break-before:always;" if newpage else ""
        rows.append(f'<p style="{pb}margin:0 0 10pt 0;{css[kind]}">{t}</p>')
    rows.append("</body></html>")
    open(out, "w").write("\n".join(rows))


if __name__ == "__main__":
    src, out = sys.argv[1], sys.argv[2]
    items = classify(open(src, encoding="utf-8").read().split("\n"))
    build_docx(items, out)
    if "--html" in sys.argv:
        build_html(items, sys.argv[sys.argv.index("--html") + 1])
    print(f"wrote {out}: {len(items)} paragraphs, {sum(1 for i in items if i[2])} page breaks")
