#!/usr/bin/env python3
"""Fill the Bible doc by editing the ORIGINAL docx, not by rebuilding it.

The first attempt rebuilt the document from script.txt with docx-js. That
silently threw away the script's typography: the original is a teleprompter
document set in Arial at 18pt body / 23pt headers, and a rebuild came out in
the default theme font at 11pt, which is unreadable off a prompter.

So this does XML surgery instead. Every original paragraph, run, font, size,
colour and spacing value is left exactly as the writer set it; the only change
is new paragraphs inserted after each PLAY CLIP marker, styled to match the
surrounding script (Arial, sz 36 = 18pt, spacing line 276) and coloured blue
for links or amber for a manual-clip caveat.

Original conventions this matches:
  headers        Arial bold, colour 000000, sz 46
  body lines     Arial regular, colour 000000, sz 36
  markers/notes  Arial bold, colour FF0000, sz 36
  inserted clip  Arial, colour 1155CC (links) or B7791F (manual note), sz 36
"""
import re
import shutil
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

RUN = Path(__file__).resolve().parent
SRC = RUN / "script.docx"
OUT = RUN / "F1_AIRBNB_VRBO_07312026_BIBLE_updated.docx"

BLUE, AMBER, SZ = "1155CC", "B7791F", "36"
FONTS = ('<w:rFonts w:ascii="Arial" w:cs="Arial" w:eastAsia="Arial" '
         'w:hAnsi="Arial"/>')
SPACING = '<w:pPr><w:spacing w:line="276"/></w:pPr>'


def rpr(color, bold=False, underline=False):
    b = "<w:b/><w:bCs/>" if bold else '<w:b w:val="false"/><w:bCs w:val="false"/>'
    u = '<w:u w:val="single"/>' if underline else ""
    return (f'<w:rPr>{FONTS}{b}<w:color w:val="{color}"/>{u}'
            f'<w:sz w:val="{SZ}"/><w:szCs w:val="{SZ}"/></w:rPr>')


def run(text, color, bold=False, underline=False):
    return (f'<w:r>{rpr(color, bold, underline)}'
            f'<w:t xml:space="preserve">{escape(text)}</w:t></w:r>')


def para(*runs):
    return f"<w:p>{SPACING}{''.join(runs)}</w:p>"


def link_para(label, url, rid):
    return para(
        run(label, BLUE),
        f'<w:hyperlink r:id="{rid}">{run(url, BLUE, underline=True)}</w:hyperlink>',
    )


CLIPS = [
    dict(role="victim_interview / horizontal", kind="pick",
         src="Scripps 'Don't Waste Your Money' (John Matarese) — carried by WCPO 9",
         url="https://www.wcpo.com/money/consumer/dont-waste-your-money/fake-rental-listings-targeting-summer-travelers-on-airbnb-vrbo",
         alt="https://www.youtube.com/watch?v=uWnVyoPqOcw",
         tin="0:18", tout="0:55", outcue="straight to voicemail",
         note="BUTT segment 1 of 2 — same package as the next clip."),
    dict(role="authority_report / horizontal", kind="pick",
         src="Same Scripps package — Kevin Brasler, Consumers' Checkbook",
         url="https://www.wcpo.com/money/consumer/dont-waste-your-money/fake-rental-listings-targeting-summer-travelers-on-airbnb-vrbo",
         alt="https://www.youtube.com/watch?v=uWnVyoPqOcw",
         tin="0:59", tout="1:19", outcue="not really part of this transaction",
         note="BUTT segment 2 of 2. Producer question above is ANSWERED: Gentry and Brasler are one package, so this is one source, two segments."),
    dict(role="victim_interview / horizontal", kind="manual",
         src="Inside Edition — 'The Genius Way This Reporter Uncovered Airbnb Scammers'",
         url="https://www.youtube.com/watch?v=VfwRWgw_M3I",
         note="Conti on camera, 8:15. ANSWERS the producer question above: the video DOES exist, so the Jeff-read-over-screenshots fallback is not needed. No timecode — this environment could not reach YouTube captions or media to verify an outcue. Pull IN/OUT on a machine with normal YouTube access."),
    dict(role="victim_interview / horizontal", kind="manual",
         src="CBS Los Angeles — 'Exclusive: Family Discovers Home Listed On Airbnb Without Their Permission'",
         url="https://www.youtube.com/watch?v=WMofFj3FJDQ",
         note="Confirmed as the Jeff Branch case (Santa Monica Mountains, $450/night, 'modern masterpiece', pet sitter). Option A taken, beat stays HORIZONTAL, no case swap. No timecode — same reason as above."),
]


def build_block(c, rid_url, rid_alt):
    tag = "   (MANUAL CLIP — no verified timecode)" if c["kind"] == "manual" else ""
    out = [para(run("▶ CLIP — " + c["role"] + tag, BLUE, bold=True)),
           link_para("Source: " + c["src"] + "  —  ", c["url"], rid_url)]
    if c.get("alt"):
        out.append(link_para("Also on YouTube: ", c["alt"], rid_alt))
    if c["kind"] == "pick":
        out.append(para(run(
            f'IN {c["tin"]}   OUT {c["tout"]}   outcue: "{c["outcue"]}"',
            BLUE, bold=True)))
    if c.get("note"):
        out.append(para(run(c["note"], AMBER if c["kind"] == "manual" else BLUE)))
    return "".join(out)


def main():
    zin = zipfile.ZipFile(SRC)
    doc = zin.read("word/document.xml").decode("utf-8")
    rels = zin.read("word/_rels/document.xml.rels").decode("utf-8")

    # Allocate relationship ids that cannot collide. The script already
    # contains hyperlinks and some of its ids are non-numeric
    # ("rId6wzwyqzcxgderysuzxdnm"), so counting from the max number is not
    # safe. Use a distinct prefix and assert it is unused.
    used = set(re.findall(r'Id="([^"]+)"', rels))
    new_rels, rid_map, seq = [], [], 0
    for c in CLIPS:
        ids = {}
        for key in ("url", "alt"):
            if c.get(key):
                seq += 1
                rid = f"rIdclip{seq}"
                assert rid not in used, f"relationship id collision: {rid}"
                ids[key] = rid
                new_rels.append(
                    f'<Relationship Id="{rid}" '
                    'Type="http://schemas.openxmlformats.org/officeDocument/2006/'
                    f'relationships/hyperlink" Target="{escape(c[key], {chr(34): "&quot;"})}" '
                    'TargetMode="External"/>')
        rid_map.append(ids)

    # insert each block immediately after its PLAY CLIP marker paragraph
    marker = re.compile(r"<w:p>(?:(?!</w:p>).)*?PLAY CLIP(?:(?!</w:p>).)*?</w:p>", re.S)
    hits = list(marker.finditer(doc))
    if len(hits) != len(CLIPS):
        raise SystemExit(f"expected {len(CLIPS)} markers, found {len(hits)}")

    for c, ids, m in zip(reversed(CLIPS), reversed(rid_map), reversed(hits)):
        block = build_block(c, ids.get("url"), ids.get("alt"))
        doc = doc[:m.end()] + block + doc[m.end():]

    rels = rels.replace("</Relationships>", "".join(new_rels) + "</Relationships>")

    shutil.copy(SRC, OUT)
    with zipfile.ZipFile(SRC) as z_src, zipfile.ZipFile(
            OUT, "w", zipfile.ZIP_DEFLATED) as z_out:
        for item in z_src.infolist():
            data = z_src.read(item.filename)
            if item.filename == "word/document.xml":
                data = doc.encode("utf-8")
            elif item.filename == "word/_rels/document.xml.rels":
                data = rels.encode("utf-8")
            z_out.writestr(item, data)

    print(f"wrote {OUT} ({OUT.stat().st_size} bytes, {len(CLIPS)} clip blocks)")


if __name__ == "__main__":
    main()
