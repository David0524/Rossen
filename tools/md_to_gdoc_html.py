#!/usr/bin/env python3
"""md_to_gdoc_html.py — turn a pre-bible or outline markdown source into HTML for a
Drive upload (Drive converts it to a native Google Doc), with every URL clickable.

Bare URLs, bare domain paths (cbsnews.com/...), and 11-character YouTube IDs that
appear elsewhere in the run as known clips become links. Story pages (`# N.` /
`# A.` and later H1s) start on a new page, like the .docx builders.

Usage: python3 tools/md_to_gdoc_html.py source.md out.html [known_ids.txt]
"""
import re, sys, html
import markdown

src, out = sys.argv[1], sys.argv[2]
ids = set()
if len(sys.argv) > 3:
    ids = set(re.findall(r"^([\w-]{11}) \|", open(sys.argv[3]).read(), re.M))
md = open(src, encoding="utf-8").read()

BARE_URL = re.compile(r"(?<![(\[<\"])(https?://[^\s)<>·]+[^\s)<>·.,;:])")
BARE_DOM = re.compile(r"(?<![\w/.:\[(-])((?:www\.)?[a-z0-9-]+(?:\.[a-z0-9-]+)*\.(?:com|org|gov|net|tv|us|ca)/[^\s)<>·]*[^\s)<>·.,;:])")
EXTRA_IDS = {"K-0vvz2MhsE", "hLl9btk1VxU", "LuNTbekmqnM", "Q8pGuskjZOc", "kEQircxHdHQ", "BH41BcnKo6w",
             "uRyHcqNnv1M", "kA7SCWe9Ook", "qC_wDqLoEnc", "OkpeBgQWHxA", "QvSKevBaHCQ", "K7dMmEAh4lM"}
ids |= EXTRA_IDS

def link_line(line):
    # protect existing markdown links
    keep = []
    def stash(m):
        keep.append(m.group(0)); return f"\x00{len(keep)-1}\x00"
    line = re.sub(r"\[[^\]]+\]\([^)]+\)", stash, line)
    line = BARE_URL.sub(lambda m: stash(re.match(".*", f"[{m.group(1)}]({m.group(1)})")), line)
    line = BARE_DOM.sub(lambda m: stash(re.match(".*", f"[{m.group(1)}](https://{m.group(1)})")), line)
    def yid(m):
        v = m.group(0)
        return stash(re.match(".*", f"[{v}](https://www.youtube.com/watch?v={v})")) if v in ids else v
    line = re.sub(r"(?<![\w-])[\w-]{11}(?![\w-])", yid, line)
    return re.sub(r"\x00(\d+)\x00", lambda m: keep[int(m.group(1))], line)

lines = [link_line(l) if not l.startswith("|---") else l for l in md.splitlines()]
# markdown needs a blank line before a list, and hard breaks inside a blockquote
fixed = []
for l in lines:
    if l.startswith("- ") and fixed and fixed[-1].strip() and not fixed[-1].startswith(("- ", "  ")):
        fixed.append("")
    if l.startswith(">") and l.strip() != ">":
        l = l + "  "
    fixed.append(l)
lines = fixed
body = markdown.markdown("\n".join(lines), extensions=["tables", "sane_lists"])

# page breaks before every H1 after the first
first = [True]
def h1(m):
    if first[0]:
        first[0] = False
        return m.group(0)
    return '<p style="page-break-before:always"></p>' + m.group(0)
body = re.sub(r"<h1>", h1, body)
body = body.replace("<table>", '<table border="1" style="border-collapse:collapse">')
body = body.replace("<blockquote>", '<blockquote style="background:#FCE4CC;border-left:4px solid #E8710A;padding:6px">')
body = body.replace("<a href=", '<a style="color:#1155CC;text-decoration:underline" href=')
open(out, "w", encoding="utf-8").write(
    '<html><head><meta charset="utf-8"></head><body style="font-family:Arial;font-size:11pt">'
    + body + "</body></html>")
print(out, len(body), "links:", body.count("<a "))
