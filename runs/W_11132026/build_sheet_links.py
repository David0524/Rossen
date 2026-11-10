#!/usr/bin/env python3
"""Run the skill's build_sheet.py with [label](url) rendered as real hyperlinks.

A run-local wrapper: it doesn't change the skill (skill edits need producer approval).
Usage: python3 build_sheet_links.py sheet.md -o out.docx
"""
import re
import sys

sys.path.insert(0, "/home/user/Rossen/.claude/skills/rossen-pre-bible/scripts")
import build_sheet  # noqa: E402
from docx.opc.constants import RELATIONSHIP_TYPE as RT  # noqa: E402
from docx.oxml import OxmlElement  # noqa: E402
from docx.oxml.ns import qn  # noqa: E402

LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
_orig = build_sheet.add_runs


def add_link(paragraph, text, url):
    r_id = paragraph.part.relate_to(url, RT.HYPERLINK, is_external=True)
    link = OxmlElement("w:hyperlink")
    link.set(qn("r:id"), r_id)
    run = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "1155CC")
    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "single")
    rpr.append(color)
    rpr.append(underline)
    run.append(rpr)
    t = OxmlElement("w:t")
    t.text = text
    t.set(qn("xml:space"), "preserve")
    run.append(t)
    link.append(run)
    paragraph._p.append(link)


def add_runs(paragraph, text):
    pos = 0
    for m in LINK.finditer(text):
        if m.start() > pos:
            _orig(paragraph, text[pos:m.start()])
        add_link(paragraph, m.group(1), m.group(2))
        pos = m.end()
    if pos < len(text):
        _orig(paragraph, text[pos:])


build_sheet.add_runs = add_runs

if __name__ == "__main__":
    build_sheet.main()
