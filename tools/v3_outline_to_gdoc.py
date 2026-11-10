"""v3 outline markdown -> HTML for a Google Doc upload: live links, nested clip bullets,
grey beat tags, red ⚠️ lines, a page break before the Build Sheet.
Usage: python3 tools/v3_outline_to_gdoc.py outline.md out.html   (then upload as text/html)
"""
import re, subprocess, sys, tempfile, os
src, out = sys.argv[1], sys.argv[2]
lines = open(src, encoding="utf-8").read().splitlines()
fixed = []
for l in lines:
    m = re.match(r"^( +)([-*]|\d+\.) (.*)$", l)
    if m:
        n = len(m.group(1)); lvl = 1 if n <= 3 else 2
        l = " " * (4 * lvl) + m.group(2) + " " + m.group(3)
    elif re.match(r"^\*\*CLIP\b", l):
        if fixed and fixed[-1].strip(): fixed.append("")
        l = "- " + l
    fixed.append(l)
tmp = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8")
tmp.write("\n".join(fixed)); tmp.close()
subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "md_to_gdoc_html.py"), tmp.name, out], check=True, stdout=subprocess.DEVNULL)
h = open(out, encoding="utf-8").read()
h = h.replace("<p>[[PAGE BREAK]]</p>", "")
h = re.sub(r"<p><code>(.*?)</code></p>", r'<p style="color:#777777;font-size:9pt">\1</p>', h)
h = re.sub(r"<li><em>(Soundbite:.*?)</em>", r'<li><em style="color:#555555">\1</em>', h, flags=re.S)
h = re.sub(r"<li>(⚠️.*?)</li>", r'<li style="color:#C0392B">\1</li>', h, flags=re.S)
open(out, "w", encoding="utf-8").write(h)
print(out, len(h), "links:", h.count("<a "))
