"""Fill the clip cues into the ORIGINAL script.docx.

Formatting rule: never regenerate the document. Every paragraph this script
inserts is built from the exact pPr/rPr the surrounding paragraphs already use
(Arial, w:sz 36, spacing line=276 before=0 after=0), so font, size and spacing
are byte-identical to the source. The only properties that differ are w:color
(blue for a located clip, red for a gap, amber for a caveat) and w:u on links,
which is what the deliverable asks for.
"""
import json, re, shutil, zipfile
from pathlib import Path
from xml.sax.saxutils import escape

SRC = Path("script.docx")
DST = Path("F2_TOP_STORIES_08122026_BIBLE_updated.docx")
BLUE, RED, AMBER = "1155CC", "C0392B", "B7791F"

picks = {p["beat_id"]: p for p in json.load(open("picks.json"))}
beats = {b["beat_id"]: b for b in json.load(open("beats.json"))}

# ---- paragraph/run templates lifted verbatim from the source document -------
PPR = ('<w:pPr><w:spacing w:lineRule="auto" w:line="276" w:before="0" '
       'w:after="0"/></w:pPr>')
FONTS = ('<w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial" '
         'w:eastAsia="Arial"/>')
SZ = '<w:sz w:val="36"/>'

def rpr(color, bold=False, underline=False):
    b = "<w:b/>" if bold else '<w:b w:val="0"/>'
    u = '<w:u w:val="single"/>' if underline else ""
    return f"<w:rPr>{FONTS}{b}<w:color w:val=\"{color}\"/>{u}{SZ}</w:rPr>"

def run(text, color, bold=False, underline=False):
    return (f"<w:r>{rpr(color, bold, underline)}"
            f'<w:t xml:space="preserve">{escape(text)}</w:t></w:r>')

def para(*runs):
    return f"<w:p>{PPR}{''.join(runs)}</w:p>"

RELS = []
def link(url, text, color=BLUE):
    rid = f"rIdClip{len(RELS)+1}"
    RELS.append((rid, url))
    return (f'<w:hyperlink r:id="{rid}">'
            f"{run(text, color, underline=True)}</w:hyperlink>")

# ---- the block inserted at each clip marker ---------------------------------
def block(bid):
    p, b = picks.get(bid), beats[bid]
    tag = f"{b['clip_role']} / {b['orientation']}"
    out = []
    if p and p.get("flagged"):
        r = next(x for x in p["ranked"] if x["url"] == p["flagged"])
        gated = p.get("status") == "producer_gated"
        head = f"{bid.upper()} — {tag}"
        if gated:
            head += "  ·  PRODUCER-GATED, DO NOT CUT UNTIL APPROVED"
        out.append(para(run(head, AMBER if gated else BLUE, bold=True)))
        out.append(para(run(p["title"] + "  —  ", BLUE), link(p["flagged"], p["flagged"])))
        for s in r["segments"]:
            out.append(para(run(f"IN {s['in']} – OUT {s['out']}", BLUE, bold=True),
                            run(f"   OUTCUE: “{s['outcue']}”", BLUE)))
        for f in r.get("flags") or []:
            out.append(para(run("NOTE: " + f, AMBER)))
    elif p and p.get("status") == "manual_clip":
        unver = bid == "F2c-b07"
        out.append(para(run(f"{bid.upper()} — {tag}  ·  MANUAL CLIP — no captions",
                            BLUE, bold=True)))
        out.append(para(run(p["title"] + "  —  ", BLUE),
                        link(p["manual_url"], p["manual_url"])))
        out.append(para(run(
            "OUTCUE UNVERIFIED — native TikTok post, no caption track. Producer sets IN/OUT by eye."
            if unver else
            "No caption track on this source. Producer sets IN/OUT by eye.", AMBER)))
    else:
        out.append(para(run(f"{bid.upper()} — {tag}  ·  NO CLIP FOUND", RED, bold=True)))
        why = ". ".join((p or {}).get("flagged_reason", "no reason recorded").split(". ")[:2]) + "."
        out.append(para(run("no clip found — " + why, RED)))
    return "".join(out)

# ---- surgical insertion into the original XML -------------------------------
xml = zipfile.ZipFile(SRC).read("word/document.xml").decode("utf-8")
PARA = re.compile(r"<w:p(?: [^>]*)?>.*?</w:p>", re.S)
TEXT = re.compile(r"<w:t(?: [^>]*)?>(.*?)</w:t>", re.S)

ORDER = [f"F2c-b0{i}" for i in range(1, 10)]
state = {"i": 0, "pending": None}

def visit(m):
    p = m.group(0)
    txt = "".join(TEXT.findall(p)).strip()
    if txt.startswith("(((PLAY CLIP XXX"):
        state["pending"] = ORDER[state["i"]]; state["i"] += 1
        return p
    if txt == "OUT:" and state["pending"]:
        bid, state["pending"] = state["pending"], None
        return p + block(bid)                      # keep OUT:, append the fill
    if txt.startswith("(((DECIDE - DO WE ADD A BUST BEAT"):
        return p + block("F2c-b10")
    if txt.startswith("(((JEFF SCREEN SHARE"):
        return p + para(run(
            "F2C-B11 — SHOW-PRODUCED  ·  no clip to source. Jeff walks missingmoney.com live.",
            AMBER, bold=True))
    return p

body = PARA.sub(visit, xml)
assert state["i"] == 9, f"expected 9 PLAY CLIP markers, filled {state['i']}"

# ---- repack, copying every other part through untouched ---------------------
rels_add = "".join(
    f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/'
    f'officeDocument/2006/relationships/hyperlink" Target="{escape(url, {chr(34): "&quot;"})}"'
    f' TargetMode="External"/>' for rid, url in RELS)

src = zipfile.ZipFile(SRC)
with zipfile.ZipFile(DST, "w", zipfile.ZIP_DEFLATED) as out:
    for item in src.infolist():
        data = src.read(item.filename)
        if item.filename == "word/document.xml":
            data = body.encode("utf-8")
        elif item.filename == "word/_rels/document.xml.rels":
            data = data.decode("utf-8").replace("</Relationships>",
                                                rels_add + "</Relationships>").encode("utf-8")
        out.writestr(item, data)

print(f"wrote {DST}  ·  {DST.stat().st_size} bytes  ·  {state['i']} clip markers filled  "
      f"·  {len(RELS)} hyperlinks")
