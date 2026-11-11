#!/usr/bin/env python3
"""fit_columns.py — column widths that make each table in a Google Doc as short as possible.

Standing rule (producer, 11/11/2026): every Google Doc we build gets its table
columns sized so the table is as short as possible.

Reads the pipe tables in a markdown source (the same file md_to_gdoc_html.py
uploads), measures every cell's text with Arial metrics (Liberation Sans), and
searches column widths that minimize the table's total rendered height
(sum over rows of the tallest cell) at a fixed total width. A column is never
narrower than its longest word, so words don't break.

Usage:
    python3 tools/fit_columns.py source.md [--width 468] [--pt 11] [--json]

Prints, per table, the widths in PT, and (with --json) a JSON list of widths
per table, in document order, ready for the Docs API:
    updateTableColumnProperties {tableStartLocation:{index:<table start>},
      columnIndices:[i], tableColumnProperties:{widthType:"FIXED_WIDTH",
      width:{magnitude:w, unit:"PT"}}, fields:"width,widthType"}
Find each table's start index with read_doc (body.content[].table, startIndex).

Defaults: an HTML upload becomes a US Letter Doc with 1-inch margins, so the
text width is 468pt; table text is 11pt Arial; Docs pads each cell 5pt a side.
"""
import argparse, itertools, json, re, sys
from PIL import ImageFont

REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
PAD = 10.0      # 5pt left + 5pt right
BORDER = 1.0
LINE = 1.15     # Docs line height multiple for normal text


def clean(cell):
    bold = cell.strip().startswith("**") and cell.strip().endswith("**")
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cell)          # links -> text
    t = re.sub(r"\*\*|__|(?<!\w)\*|\*(?!\w)|`", "", t)
    t = t.replace("\\|", "|").strip()
    return t, bold


def tables(md):
    out, cur = [], []
    for line in md.splitlines():
        s = line.strip()
        if s.startswith("|") and s.endswith("|"):
            cells = [c for c in re.split(r"(?<!\\)\|", s[1:-1])]
            if all(re.fullmatch(r"\s*:?-{2,}:?\s*", c) for c in cells):
                continue
            cur.append(cells)
        elif cur:
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    return out


class Meter:
    def __init__(self, pt):
        self.f = {False: ImageFont.truetype(REG, 100), True: ImageFont.truetype(BOLD, 100)}
        self.k = pt / 100.0
        self.cache = {}

    def w(self, s, bold):
        key = (s, bold)
        if key not in self.cache:
            self.cache[key] = self.f[bold].getlength(s) * self.k
        return self.cache[key]

    def lines(self, text, bold, width):
        avail = width - PAD
        n, cur = 0, ""
        for para in text.split("\n"):
            n += 1; cur = ""
            for word in para.split():
                trial = (cur + " " + word).strip()
                if self.w(trial, bold) <= avail:
                    cur = trial
                else:
                    n += 1 if cur else 0
                    ww = self.w(word, bold)
                    if ww > avail:              # a long token wraps by character
                        n += int(ww // avail)
                        cur = ""
                    else:
                        cur = word
        return max(n, 1)


def fit(rows, total, m, pt, header_bold=True):
    ncol = max(len(r) for r in rows)
    cells = []
    for ri, r in enumerate(rows):
        row = []
        for c in r + [""] * (ncol - len(r)):
            t, b = clean(c)
            row.append((t, b or (ri == 0 and header_bold)))
        cells.append(row)
    # Floors. The goal is the shortest table (producer, 11/11), so a long word may
    # break across lines when that makes the table shorter: the 11/25 outline came
    # out wrong when every column was held to its longest word ("HORIZONTAL",
    # "UNVERIFIED") and the text-heavy column got the leftovers. Only the header
    # word (and a 2-character id like "A2") is kept whole.
    mins = []
    for j in range(ncol):
        head = max((m.w(wd, cells[0][j][1]) for wd in cells[0][j][0].split()), default=0)
        mins.append(max(head, 14.0) + PAD + 1)
    if sum(mins) > total:
        k = total / sum(mins); mins = [x * k for x in mins]

    def height(ws):
        return sum(max(m.lines(t, b, w) for (t, b), w in zip(row, ws)) for row in cells)

    # start: proportional to each column's natural (unwrapped) width, floored at mins
    nat = [max(m.w(t, b) + PAD for row in cells for (t, b) in [row[j]]) for j in range(ncol)]
    spare = total - sum(mins)
    extra = [max(n - mn, 0) for n, mn in zip(nat, mins)]
    se = sum(extra) or 1
    ws = [mn + spare * e / se for mn, e in zip(mins, extra)]
    best = height(ws)
    for step in (24, 12, 6, 3, 1.5):
        improved = True
        while improved:
            improved = False
            for i, j in itertools.permutations(range(ncol), 2):
                c = ws[:]; c[i] -= step; c[j] += step
                if c[i] < mins[i]:
                    continue
                h = height(c)
                if h < best:
                    ws, best, improved = c, h, True
    return [round(w, 1) for w in ws], best, round(best * pt * LINE, 1)


def even_lines(rows, total, m):
    ncol = max(len(r) for r in rows)
    w = total / ncol
    return sum(max(m.lines(*clean(c), w) if True else 0 for c in r + [""] * (ncol - len(r))) for r in rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--width", type=float, default=468.0, help="text width in pt (Letter, 1in margins = 468)")
    ap.add_argument("--pt", type=float, default=11.0)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    md = open(a.source, encoding="utf-8").read()
    m = Meter(a.pt)
    res = []
    for n, rows in enumerate(tables(md)):
        ws, lines, h = fit(rows, a.width - BORDER, m, a.pt)
        res.append(ws)
        if not a.json:
            print(f"table {n + 1}: {len(rows)} rows x {len(ws)} cols · widths (pt) {ws} · "
                  f"{lines} lines tall (even columns: {even_lines(rows, a.width - BORDER, m)})")
    if a.json:
        print(json.dumps(res))


if __name__ == "__main__":
    sys.exit(main())
