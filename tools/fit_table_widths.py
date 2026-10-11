#!/usr/bin/env python3
"""Make the shortlist table in a pitch-sheet .docx as short as possible.

build_sheet.py sets per-cell widths but no table grid, so LibreOffice and Google
Docs render equal columns. This writes a fixed layout plus tblGrid, choosing the
widths by measurement: render page one with LibreOffice, read the table's height
from pdftotext -bbox (SHORTLIST heading to the next text after the table), and
shift 0.1" between column pairs while the table gets shorter.

Usage: python3 tools/fit_table_widths.py sheet.docx [w1,w2,...]   (optional start)
Needs soffice and pdftotext.
"""
import itertools, os, re, shutil, subprocess, sys, tempfile
from docx import Document
from docx.shared import Inches
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

TOTAL = 6.9  # text width on the sheet (8.5" page, 0.8" margins)


def apply(src, dst, ws):
    d = Document(src)
    t = d.tables[0]
    tbl = t._tbl
    for old in tbl.tblPr.findall(qn('w:tblLayout')):
        tbl.tblPr.remove(old)
    lay = OxmlElement('w:tblLayout'); lay.set(qn('w:type'), 'fixed'); tbl.tblPr.append(lay)
    for gc in list(tbl.tblGrid):
        tbl.tblGrid.remove(gc)
    for w in ws:
        gc = OxmlElement('w:gridCol'); gc.set(qn('w:w'), str(int(w * 1440))); tbl.tblGrid.append(gc)
    for r in t.rows:
        for c, w in zip(r.cells, ws):
            c.width = Inches(w)
    d.save(dst)


def height(src, ws, tmp):
    probe = os.path.join(tmp, 'probe.docx')
    apply(src, probe, ws)
    subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', tmp, probe],
                   capture_output=True)
    x = subprocess.run(['pdftotext', '-f', '1', '-l', '2', '-bbox', os.path.join(tmp, 'probe.pdf'), '-'],
                       capture_output=True, text=True).stdout
    pages = x.split('<page ')[1:]
    words = [(p, float(m.group(1)), m.group(2)) for p, pg in enumerate(pages)
             for m in re.finditer(r'yMax="([\d.]+)">([^<]*)<', pg)]
    top = next((y for p, y, w in words if w == 'SHORTLIST'), None)
    end = next((p * 1000 + y for p, y, w in words if w == 'SLATE'), None)
    return 9999 if top is None or end is None else end - top


def main():
    path = sys.argv[1]
    d = Document(path)
    n = len(d.tables[0].columns)
    if len(sys.argv) > 2:
        ws = [float(v) for v in sys.argv[2].split(',')]
    elif n == 6:
        ws = [0.30, 1.25, 2.60, 1.00, 0.85, 0.90]  # measured best for the 10/16+10/21 sheet
    else:
        ws = [TOTAL / n] * n
    mins = [0.3] + [0.6] * (n - 1)
    tmp = tempfile.mkdtemp()
    try:
        best = height(path, ws, tmp)
        improved = True
        while improved:
            improved = False
            for i, j in itertools.permutations(range(1, n), 2):
                c = ws[:]; c[i] -= 0.1; c[j] += 0.1
                if c[i] < mins[i]:
                    continue
                h = height(path, c, tmp)
                if h < best - 0.5:
                    ws, best, improved = c, h, True
        apply(path, path, ws)
        print('widths:', [round(w, 2) for w in ws], 'table height (pt):', round(best, 1))
    finally:
        shutil.rmtree(tmp)


if __name__ == '__main__':
    main()
