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

# ---- Checkpoint 3 script edits ---------------------------------------------
# Approved by the producer ("complete the checkpoint items in the way you see
# fit"). Each entry rewrites the text of an existing paragraph IN PLACE, reusing
# that paragraph's own pPr and rPr, so font, size, spacing, colour and weight are
# untouched. Only the words change.
REPLACE = [
 # b02 — the cloned reporter is Lauren Trager, a woman. Named, and pronouns fixed.
 ("-A REPORTER ASKED HER TO PROVE HOW FAST A VOICE CAN BE STOLEN.",
  "-FIRST ALERT 4'S LAUREN TRAGER ASKED HER TO PROVE HOW FAST A VOICE CAN BE STOLEN."),
 ("-SO SHE TOOK A FEW SECONDS OF THAT REPORTER'S OWN VOICE.",
  "-SO SHE TOOK A FEW SECONDS OF LAUREN'S OWN VOICE."),
 ("-THEN SHE MADE HIS VOICE SAY WHATEVER SHE WANTED IT TO SAY.",
  "-THEN SHE MADE LAUREN'S VOICE SAY WHATEVER SHE WANTED IT TO SAY."),
 ("-WATCH HER SHOW YOU HOW FAST IT HAPPENS... AND WATCH HIS FACE.",
  "-WATCH HER SHOW YOU HOW FAST IT HAPPENS... AND WATCH LAUREN'S FACE."),
 # b04 — no source anywhere supports a $20,000 demand. Five hours and $5,400 do check out.
 ("-HE DEMANDED 20,000 DOLLARS. SHE FOLLOWED ORDERS FOR FIVE HOURS AND LOST OVER 5,000.",
  "-HE GAVE HER ORDERS AND SHE FOLLOWED THEM FOR FIVE HOURS... WIRING 5,400 DOLLARS TO MEXICO."),
 # b05 — Erin West never says either thing the script had her saying. Rewritten
 # onto her sworn testimony, which lands on the word the header promises.
 ("-ERIN WEST RUNS AN ORGANIZATION CALLED OPERATION SHAMROCK THAT FIGHTS THIS INDUSTRY.",
  "-ERIN WEST IS A FORMER PROSECUTOR WHO RUNS OPERATION SHAMROCK AND FIGHTS THIS INDUSTRY FULL TIME."),
 ("-SHE SAYS A FEW SECONDS OF YOUR VOICE PRODUCES SOMETHING THAT SOUNDS EXACTLY LIKE YOU.",
  "-SHE JUST TESTIFIED ABOUT ALL OF THIS IN FRONT OF CONGRESS."),
 ("-AND SHE GIVES YOU THE CLEANEST TEST OUT THERE FOR ANY SCAM CALL.",
  "-SHE SAYS THESE ARE NOT A PILE OF SEPARATE SCAMS. IT IS ONE GLOBAL CRIMINAL ECONOMY."),
 ("-ANXIETY... PLUS IMMEDIATE ACTION... PLUS MOVING MONEY.",
  "-AND SHE TOLD CONGRESS ABOUT VICTIMS WHO HAD TO BUILD THEIR OWN CASES, BECAUSE NOBODY ELSE WOULD."),
 ("-YOU GET ALL THREE AT ONCE, IT IS A SCAM. EVERY TIME!!",
  "-A PARALEGAL IN WISCONSIN TRACKED DOWN FOUR SUSPECTS HERSELF!!"),
 ("-LET HER EXPLAIN WHY SHE THINKS THIS ONLY GETS WORSE FROM HERE.",
  "-LISTEN TO THE QUESTION SHE SAYS THIS COUNTRY HAS TO ANSWER."),
 # b08 — the package is April 2023. Past-tense the framing, add the figure that is on tape.
 ("-VIRGINIA'S TREASURY SAID THE FLOOD OF CLAIMS WAS DIRECTLY BECAUSE OF TIKTOK.",
  "-WHEN THIS FIRST BLEW UP, VIRGINIA'S TREASURY SAID THE FLOOD OF CLAIMS CAME STRAIGHT FROM TIKTOK."),
 ("-VIRGINIA SAYS AN APPROVED CLAIM CAN PAY OUT IN ABOUT TEN DAYS.",
  "-THAT YEAR THEY PAID OUT A RECORD 46 MILLION DOLLARS ON 50,000 CLAIMS... DOUBLE THE YEAR BEFORE."),
 # b09 — DECIDE resolved: the I-Team package is horizontal.
 ("(((DECIDE VERTICAL OR HORIZONTAL - THE ABC7 CHICAGO TIKTOK CUT IS VERTICAL, THE ORIGINAL I-TEAM PACKAGE IS HORIZONTAL.)))",
  "(((RESOLVED - HORIZONTAL. THE ABC7 CHICAGO I-TEAM PACKAGE, JASON KNOWLES, 01-28-25. MANUAL PULL, NO CAPTIONS.)))"),
]

# Lines inserted after an existing paragraph, matching the body run style.
INSERT_AFTER = [
 # b08 — the ten-day payout is real and worth keeping; it just moved down.
 ("-THAT YEAR THEY PAID OUT A RECORD 46 MILLION DOLLARS ON 50,000 CLAIMS... DOUBLE THE YEAR BEFORE.",
  ["-AND VIRGINIA SAYS AN APPROVED CLAIM CAN PAY OUT IN ABOUT TEN DAYS."]),
 # The three-signal test, pulled off Erin West and given to Jeff as his own read.
 ("-ANYBODY WHO TELLS YOU TO STAY ON THE LINE AND TELL NOBODY IS RUNNING A SCAM!!",
  ["-AND LEARN THE THREE-PART TEST... ANXIETY... PLUS IMMEDIATE ACTION... PLUS MOVING MONEY.",
   "-YOU GET ALL THREE ON ONE CALL, IT IS A SCAM. EVERY TIME!!"]),
]

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
state = {"i": 0, "pending": None, "edits": 0, "ins": 0}

PPR_RE = re.compile(r"<w:pPr>.*?</w:pPr>", re.S)
RPR_RE = re.compile(r"<w:rPr>.*?</w:rPr>", re.S)

def retext(paragraph, text):
    """Rewrite a paragraph's words, reusing its OWN pPr and rPr verbatim so
    font, size, spacing, colour and weight are bit-for-bit unchanged."""
    ppr = (PPR_RE.search(paragraph) or [None]) and PPR_RE.search(paragraph)
    rpr = RPR_RE.search(paragraph)
    ppr = ppr.group(0) if ppr else PPR
    rpr = rpr.group(0) if rpr else rpr_body()
    return (f"<w:p>{ppr}<w:r>{rpr}"
            f'<w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>')

def rpr_body():
    return rpr("000000")

REPLACE_MAP = dict(REPLACE)
INSERT_MAP = dict(INSERT_AFTER)

# b10 is no longer gated — the DECIDE block is replaced by a real setup and a
# real PLAY CLIP marker, written off what the WJZ tape actually says.
B10_SETUP = [
 "SO DOES ANYBODY EVER GET CAUGHT? SOMETIMES, YES!!",
 "-NOBODY HAS BEEN PROSECUTED YET FOR CLONING A CHILD'S VOICE. NOT ONE CASE ANYWHERE.",
 "-BUT THE RINGS THAT MOVE THE MONEY? THOSE DO GET BUSTED.",
 "-THE F-B-I SPENT FIVE YEARS ON ONE OF THEM.",
 "-IT STARTED WITH PACKAGES GOING TO EMPTY HOUSES IN BALTIMORE.",
 "-THIRTEEN PEOPLE CHARGED. EIGHTY-FIVE VICTIMS. TWO AND A HALF MILLION DOLLARS.",
 "-AND ONE OF THOSE VICTIMS WAS HIT WITH A REPLICATED VOICE.",
 "-HERE IS WHAT THE AGENTS SAID WHEN THEY FINALLY CONNECTED IT ALL.",
]

def visit(m):
    p = m.group(0)
    txt = "".join(TEXT.findall(p)).strip()

    if txt in REPLACE_MAP:
        state["edits"] += 1
        p = retext(p, REPLACE_MAP[txt]); txt = REPLACE_MAP[txt]

    if txt.startswith("(((PLAY CLIP XXX"):
        state["pending"] = ORDER[state["i"]]; state["i"] += 1
        return p
    if txt == "OUT:" and state["pending"]:
        bid, state["pending"] = state["pending"], None
        return p + block(bid)                      # keep OUT:, append the fill
    if txt.startswith("(((DECIDE - DO WE ADD A BUST BEAT"):
        # Producer note answered: yes, add it, framed off the tape.
        out = [retext(p, "(((RESOLVED - BUST BEAT ADDED. NO A-I CLONING PROSECUTION EXISTS; "
                         "SETUP SAYS SO OUT LOUD AND RUNS THE MONEY-RING BUST INSTEAD.)))")]
        body_rpr = rpr("000000")
        head_rpr = rpr("000000", bold=True)
        for i, line in enumerate(B10_SETUP):
            out.append(f"<w:p>{PPR}<w:r>{head_rpr if i == 0 else body_rpr}"
                       f'<w:t xml:space="preserve">{escape(line)}</w:t></w:r></w:p>')
            out.append(f"<w:p>{PPR}<w:r>{body_rpr}</w:r></w:p>")
        marker_rpr = rpr("FF0000", bold=True)
        for lit in ("(((PLAY CLIP XXX HORIZONTAL)))", "OUT:"):
            out.append(f"<w:p>{PPR}<w:r>{marker_rpr}"
                       f'<w:t xml:space="preserve">{escape(lit)}</w:t></w:r></w:p>')
        out.append(block("F2c-b10"))
        return "".join(out)
    if txt.startswith("(((JEFF SCREEN SHARE"):
        return p + para(run(
            "F2C-B11 — SHOW-PRODUCED  ·  no clip to source. Jeff walks missingmoney.com live.",
            AMBER, bold=True))

    if txt in INSERT_MAP:
        state["ins"] += len(INSERT_MAP[txt])
        body_rpr = rpr("000000")
        extra = "".join(
            f"<w:p>{PPR}<w:r>{body_rpr}</w:r></w:p>"
            f"<w:p>{PPR}<w:r>{body_rpr}"
            f'<w:t xml:space="preserve">{escape(line)}</w:t></w:r></w:p>'
            for line in INSERT_MAP[txt])
        return p + extra
    return p

body = PARA.sub(visit, xml)
assert state["i"] == 9, f"expected 9 PLAY CLIP markers, filled {state['i']}"
assert state["edits"] == len(REPLACE), f"expected {len(REPLACE)} script edits, applied {state['edits']}"

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
      f"·  {len(RELS)} hyperlinks  ·  {state['edits']} script edits  ·  {state['ins']} lines inserted")
