#!/usr/bin/env python3
"""Update the clip pull sheet by editing the ORIGINAL docx, never regenerating it.

Same discipline as build_bible.py: every original paragraph, run, font, size,
colour and spacing value is preserved. Clips 7-12 are not touched at all — they
were already verified and are out of scope. Only the clip 1-6 STATUS lines are
rewritten, with resolved detail inserted beneath them.

House conventions matched exactly, read off clips 7-12:
  clip heading / IN-OUT / OUTCUE / STATUS   Arial bold, FF0000, sz 36
  URL                                        Arial, 1155CC, underlined, sz 36, hyperlinked
  spacing                                    line 276 auto; after 0 mid-block, 170 at block end
"""
import re
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

RUN = Path(__file__).resolve().parent
SRC = RUN / "pull_sheet.docx"
OUT = RUN / "WED_08_05_CLIP_PULL_SHEET_updated.docx"

RED, BLUE, GREEN, SZ = "FF0000", "1155CC", "0B6623", "36"
FONTS = ('<w:rFonts w:ascii="Arial" w:cs="Arial" w:eastAsia="Arial" w:hAnsi="Arial"/>')


def pr(after=0):
    return (f'<w:pPr><w:spacing w:after="{after}" w:line="276" '
            'w:lineRule="auto"/></w:pPr>')


def rpr(color, bold=True, underline=False):
    b = "<w:b/><w:bCs/>" if bold else ""
    u = '<w:u w:val="single"/>' if underline else ""
    return (f'<w:rPr>{FONTS}{b}<w:color w:val="{color}"/>'
            f'<w:sz w:val="{SZ}"/><w:szCs w:val="{SZ}"/>{u}</w:rPr>')


def para(text, color=RED, bold=True, after=0):
    return (f'<w:p>{pr(after)}<w:r>{rpr(color, bold)}'
            f'<w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>')


def link_para(url, rid, after=170):
    return (f'<w:p>{pr(after)}<w:hyperlink w:history="1" r:id="{rid}">'
            f'<w:r>{rpr(BLUE, bold=False, underline=True)}'
            f'<w:t xml:space="preserve">{escape(url)}</w:t></w:r>'
            '</w:hyperlink></w:p>')


# Replacement STATUS line + the block that follows it, per clip.
# `links` are (url) in order; they become hyperlinked paragraphs.
BLOCKS = {
1: dict(status="STATUS: EMPTY — NOTHING CLEARED THE BAR. NOTHING FLAGGED.",
        lines=["Top vertical candidate REJECTED on fit: @getlostwebsite TikTok is an Airbnb HOST",
               "defending his own indoor camera (“I have every right to monitor that space”).",
               "Right keywords, inverted story. Screen these two by hand — both verified vertical,",
               "both bot-walled from the harvest environment so no outcue could be confirmed:"],
        links=["https://www.youtube.com/watch?v=-csy3-_Qedc",
               "https://www.youtube.com/shorts/DqOM4hjj2gw"],
        tail=["CNN “Woman finds hidden camera in Airbnb” 42s · and a 56s how-to. NO TIMECODE — unverified."]),

2: dict(status="STATUS: LOCATED, NOT CUT. SOURCE CONFIRMED — NO TIMECODE.",
        lines=["Your leads were right. The Tegna sentencing package exists and its headline is the",
               "judge’s line. Every route blocked from the harvest environment (TEGNA 403, Nexstar 403,",
               "YouTube bot-walled). Should cut normally on a station machine."],
        links=["https://www.wtol.com/article/news/crime/hocking-hills-cabin-owner-sentenced-placing-hidden-cameras-bathrooms/512-33e0ec1e-a5f1-4c3c-9a4d-0ba0a0eb1c62"],
        tail=["YouTube twins: Lix_CaVtAHo (WKYC) · K86XQAs4LA0 (10TV, PRE-sentencing, wrong day).",
              "WARNING: Bradds’ victim statement is NOT in the 37s cutdown that was reachable.",
              "Confirm the full package actually contains it before building the beat."]),

3: dict(status="STATUS: PICK — CUT AND VERIFIED. BUTT WITH CLIP 6.",
        lines=["Your named lead. Marcus Hutchins / @malwaretech. Verified vertical 720x1280 from the",
               "decoded frame. Whisper transcript; TikTok ships no captions."],
        links=["https://www.tiktok.com/@malwaretech/video/7002804220126661893"],
        tail=["IN 0:32   OUT 1:27",
              "OUTCUE: “even a hole in the wall”   (verified @1:21.52)",
              "Covers two-way mirrors, the USB wall charger that is itself a camera, the pinhole with",
              "the blue reflection, and how small the lenses have got. Demo devices only — constraint clean."]),

4: dict(status="STATUS: DECISION REQUIRED — PULL SHEET CORRECTION.",
        lines=["David Wyzynajtys is in CNN’s WRITTEN July 2024 investigation. He is NOT in the 5:45",
               "video package. Pulled it, transcribed it in full: no Wyzynajtys, no Comfort, no Texas.",
               "The video IS reachable and DOES verify the script’s “35,000 customer support tickets”",
               "line at 1:48. But serving this beat from it means a different subject = script change."],
        links=["https://edition.cnn.com/2024/07/09/business/video/airbnb-hidden-cameras-investigation-digvid"],
        tail=["AVOID 1:11–1:40 and 3:42–3:53 — perpetrator admission re: recording during sex, and a",
              "victim describing intimate footage. Not recovered footage, so inside the letter of the",
              "rule, but past what the show airs. NO TIMECODE until the subject question is settled."]),

5: dict(status="STATUS: LOCATED, NOT CUT. SEE THE ORIENTATION WARNING.",
        lines=["Same Tegna package as clip 2. Content CONFIRMED by transcript: Yard in court (“I’m a",
               "good person who’s made a terrible mistake”), six to nine years, judge calls it",
               "“perverted” and “a renter’s worst nightmare”. Horizontal broadcast version is walled."],
        links=["https://www.wtol.com/article/news/crime/hocking-hills-cabin-owner-sentenced-placing-hidden-cameras-bathrooms/512-33e0ec1e-a5f1-4c3c-9a4d-0ba0a0eb1c62"],
        tail=["DO NOT USE the NewsBreak mirror that surfaced: it is a 720x1280 VERTICAL social cutdown",
              "with a burned-in WTOL 11 bug and burned-in captions. Wrong orientation for this beat and",
              "a competitor bug on screen.",
              "ALSO: frames sampled across that cutdown show Yard seated in orange scrubs — NO handcuff",
              "walk. Verify the walk-out shot exists before writing “WATCH HIM GO OUT IN HANDCUFFS”."]),

6: dict(status="STATUS: PICK — CUT AND VERIFIED. BUTT WITH CLIP 3, SAME SOURCE.",
        lines=["Same Hutchins TikTok as clip 3 — its first 30 seconds are this beat. Verified vertical",
               "720x1280 from the decoded frame."],
        links=["https://www.tiktok.com/@malwaretech/video/7002804220126661893"],
        tail=["IN 0:03   OUT 0:32",
              "OUTCUE: “see there’s a camera there”   (verified @0:29.24)",
              "Look where a creeper would look, shine a bright light, “it’s gonna give a bluish",
              "reflection”, test it on your own phone, then the mirrored clock reveal.",
              "ANSWERS THE OPEN BIBLE QUESTION: a usable real-room sweep exists, so the on-set",
              "flashlight demo is optional, not necessary. Jeff’s call."]),
}

HEADER = ("UPDATED 07/26 — clips 1-6 harvested. Clips 7-12 untouched. "
          "2 cut · 2 located · 1 decision · 1 empty.")


def main():
    zin = zipfile.ZipFile(SRC)
    doc = zin.read("word/document.xml").decode("utf-8")
    rels = zin.read("word/_rels/document.xml.rels").decode("utf-8")

    used = set(re.findall(r'Id="([^"]+)"', rels))
    new_rels, seq = [], 0

    def add_rel(url):
        nonlocal seq
        seq += 1
        rid = f"rIdnew{seq}"
        assert rid not in used, f"relationship id collision: {rid}"
        new_rels.append(
            f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/'
            f'officeDocument/2006/relationships/hyperlink" '
            f'Target="{escape(url, {chr(34): "&quot;"})}" TargetMode="External"/>')
        return rid

    # The six TO HARVEST status paragraphs, in document order = clips 1..6.
    pat = re.compile(r"<w:p>(?:(?!</w:p>).)*?STATUS: TO HARVEST(?:(?!</w:p>).)*?</w:p>", re.S)
    hits = list(pat.finditer(doc))
    if len(hits) != 6:
        raise SystemExit(f"expected 6 TO HARVEST lines, found {len(hits)}")

    built = []
    for n in range(1, 7):
        b = BLOCKS[n]
        xml = para(b["status"], RED, after=0)
        for ln in b["lines"]:
            xml += para(ln, GREEN, bold=False, after=0)
        for u in b["links"]:
            xml += link_para(u, add_rel(u), after=0)
        for i, ln in enumerate(b["tail"]):
            last = (i == len(b["tail"]) - 1)
            red_line = ln.startswith(("IN ", "OUTCUE:")) or ln.startswith(("WARNING", "DO NOT", "ALSO", "AVOID"))
            xml += para(ln, RED if red_line else GREEN, bold=red_line,
                        after=170 if last else 0)
        built.append(xml)

    for n in range(6, 0, -1):
        m = hits[n - 1]
        doc = doc[:m.start()] + built[n - 1] + doc[m.end():]

    # Header note directly after the document title.
    tmark = doc.find("CLIP PULL SHEET")
    if tmark > 0:
        end = doc.find("</w:p>", tmark) + 6
        doc = doc[:end] + para(HEADER, GREEN, bold=True, after=170) + doc[end:]

    rels = rels.replace("</Relationships>", "".join(new_rels) + "</Relationships>")

    with zipfile.ZipFile(SRC) as zs, zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zo:
        for item in zs.infolist():
            data = zs.read(item.filename)
            if item.filename == "word/document.xml":
                data = doc.encode("utf-8")
            elif item.filename == "word/_rels/document.xml.rels":
                data = rels.encode("utf-8")
            zo.writestr(item, data)

    print(f"wrote {OUT} ({OUT.stat().st_size} bytes, {seq} new hyperlinks)")


if __name__ == "__main__":
    main()
