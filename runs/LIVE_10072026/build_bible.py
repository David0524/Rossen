"""Fill the 10/07 LIVE bible IN PLACE. Never regenerates the document: rewritten
paragraphs keep their own pPr/rPr, inserted paragraphs copy the source's own
Arial / w:sz 36 / line=276 before=0 after=0. Only w:color and w:u are added."""
import json,re,zipfile
from pathlib import Path
from xml.sax.saxutils import escape
SRC=Path("script.docx"); DST=Path("10_07_LIVE_BIBLE_-_YOUR_STORE_IS_WATCHING_YOU_FILLED.docx")
BLUE,RED,AMBER="1155CC","C0392B","B7791F"
picks={p["beat_id"]:p for p in json.load(open("picks.json"))}
beats={b["beat_id"]:b for b in json.load(open("beats.json"))}
ORDER=["L07-A1","L07-A2","L07-A3","L07-A4","L07-A5","L07-B1","L07-B2"]

# ---- approved A4 swap: Brianna Jones -> Lesleigh Nurse (facts from the WKRG/CBS tape + CBS/NBC/WVTM coverage)
REPLACE={
 "-AI IS WATCHING YOUR HANDS AT SELF-CHECKOUT… AND ONE SHOPPER SAYS SHE ENDED UP SURROUNDED BY EMPLOYEES AND POLICE.":
 "-AI IS WATCHING YOUR HANDS AT SELF-CHECKOUT. AND ONE MOM WAS ARRESTED OVER 48 DOLLARS OF GROCERIES AFTER HER SCANNER MALFUNCTIONED… THEN A JURY AWARDED HER 2.1 MILLION DOLLARS.",
 "-BRIANNA JONES WAS SHOPPING AT A WALMART IN CHARLOTTE, NORTH CAROLINA BACK IN MARCH.":
 "-LESLEIGH NURSE WAS AT SELF-CHECKOUT AT THE WALMART IN SEMMES, ALABAMA… WITH HER HUSBAND AND THREE KIDS.",
 "-HER SELF-CHECKOUT REGISTER SHUT DOWN IN THE MIDDLE OF HER ORDER… A CONDIMENT WOULDN'T SCAN.":
 "-HER SCANNER KEPT MALFUNCTIONING… SHE EVEN GOT A WALMART WORKER TO HELP HER.",
 "-HER LAWSUIT SAYS A MANAGER TOLD HER THE MACHINE WAS SHUT OFF BECAUSE SHE WAS SCANNING TOO FAST.":
 "-SHE THOUGHT SHE HAD PAID FOR EVERYTHING… THEN AN ASSET PROTECTION MANAGER STOPPED HER AT THE DOOR.",
 "-SHE HAD HER RECEIPTS… SHE ASKED FOR HELP… AND THAT'S WHEN IT GOT SCARY.":
 "-SHE WAS CHARGED WITH STEALING 48 DOLLARS OF GROCERIES… ARRESTED… AND HER MUG SHOT WAS TAKEN.",
 "(((DECIDE CLIP - IF NO BRIANNA JONES INTERVIEW EXISTS, SWAP IN A NEWS EXPLAINER ON WALMART'S SELF-CHECKOUT CAMERAS)))":
 "(((RESOLVED - NO BRIANNA JONES VIDEO EXISTS. APPROVED SWAP TO LESLEIGH NURSE, SEMMES AL, WKRG VIA CBS NEWS. HER CASE DID NOT INVOLVE AN AI CAMERA - DO NOT SAY IT DID.)))",
 "-HER LAWSUIT SAYS SEVERAL EMPLOYEES AND A POLICE OFFICER SURROUNDED HER…":
 "-SHE SUED WALMART… AND A MOBILE COUNTY JURY AWARDED HER 2.1 MILLION DOLLARS!!",
 "-AND STORE WORKERS TOOK THE ITEMS SHE HAD PAID FOR!":
 "-A LAW PROFESSOR TESTIFIED IN HER CASE THAT OVER TWO YEARS, WALMART COLLECTED MORE THAN 300 MILLION DOLLARS FROM DEMAND LETTERS LIKE THE ONES SHE GOT.",
 "-WALMART HAS NOT PUBLICLY RESPONDED TO HER LAWSUIT IN COURT.":
 "-WALMART NEVER PRODUCED THE SELF-CHECKOUT VIDEO THAT WOULD HAVE SHOWN WHAT HAPPENED… AND IT SAID IT WOULD APPEAL.",
}
# bridge so the AI-camera lines don't sit directly over a case that involved no AI
INSERT_AFTER={
 "-AND AN ALERT GOES STRAIGHT TO AN EMPLOYEE'S HANDHELD.":
 ["-BUT THESE MACHINES DON'T ALWAYS WORK… AND WHEN THEY DON'T, IT CAN BE YOU WHO GETS BLAMED."],
}

PPR='<w:pPr><w:spacing w:lineRule="auto" w:line="276" w:before="0" w:after="0"/></w:pPr>'
FONTS='<w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial" w:eastAsia="Arial"/>'
B_ON='<w:b/>'; B_OFF='<w:b w:val="0"/>'; U_ON='<w:u w:val="single"/>'
def rpr(color,bold=False,u=False):
    b=B_ON if bold else B_OFF; uu=U_ON if u else ""
    return f'<w:rPr>{FONTS}{b}<w:color w:val="{color}"/>{uu}<w:sz w:val="36"/></w:rPr>'
def run(t,color,bold=False,u=False): return f'<w:r>{rpr(color,bold,u)}<w:t xml:space="preserve">{escape(t)}</w:t></w:r>'
def para(*r): return f"<w:p>{PPR}{''.join(r)}</w:p>"
RELS=[]
def link(url,text=None):
    rid=f"rIdClip{len(RELS)+1}"; RELS.append((rid,url))
    return f'<w:hyperlink r:id="{rid}">{run(text or url,BLUE,u=True)}</w:hyperlink>'

def block(bid):
    p,b=picks[bid],beats[bid]; tag=f"{bid} — {b['clip_role']} / {b['orientation']}"; out=[]
    st=p.get("status")
    if p.get("flagged"):
        r=next(x for x in p["ranked"] if x["url"]==p["flagged"])
        head=tag+("  ·  APPROVED SWAP" if st=="approved_swap" else "")
        out.append(para(run(head,BLUE,True)))
        out.append(para(run(p["title"]+"  —  ",BLUE),link(p["flagged"])))
        for s in r["segments"]:
            out.append(para(run(f"IN {s['in']} – OUT {s['out']}",BLUE,True),run(f"   OUTCUE: “{s['outcue']}”",BLUE)))
        for f in r.get("flags") or []: out.append(para(run("NOTE: "+f,AMBER)))
    elif st=="manual_clip":
        out.append(para(run(tag+"  ·  MANUAL CLIP — NO CAPTIONS",BLUE,True)))
        out.append(para(run(p["title"]+"  —  ",BLUE),link(p["manual_url"])))
        note=("OUTCUE UNVERIFIED — native TikTok post, no caption track. Not watched. Producer sets IN/OUT by eye. No timecode invented."
              if "tiktok.com/@" in p["manual_url"] and "/video/" in p["manual_url"] else
              "PERMALINK NOT PINNED — profile only. Scroll to the dated post. No timecode invented.")
        out.append(para(run(note,AMBER)))
    elif st=="throttled":
        top=p["ranked"][0]
        out.append(para(run(tag+"  ·  PENDING CAPTIONS — YOUTUBE BLOCKED THIS RUN",AMBER,True)))
        out.append(para(run("Top candidate:  ",AMBER),link(top["url"])))
        if p.get("manual_url"): out.append(para(run("Pull-now fallback (no captions):  ",AMBER),link(p["manual_url"])))
        out.append(para(run("Not flagged: no transcript means no verifiable outcue. Re-run captions to get IN/OUT. No timecode invented.",AMBER)))
    else:
        out.append(para(run(tag+"  ·  NO CLIP FOUND",RED,True)))
        out.append(para(run("no clip found — "+p.get("flagged_reason","")[:220],RED)))
    return "".join(out)

xml=zipfile.ZipFile(SRC).read("word/document.xml").decode()
PARA=re.compile(r"<w:p(?: [^>]*)?>.*?</w:p>",re.S); TEXT=re.compile(r"<w:t(?: [^>]*)?>(.*?)</w:t>",re.S)
PPR_RE=re.compile(r"<w:pPr>.*?</w:pPr>",re.S); RPR_RE=re.compile(r"<w:rPr>.*?</w:rPr>",re.S)
st={"i":0,"pending":None,"edits":0,"ins":0}
def retext(p,text):
    pp=PPR_RE.search(p); rp=RPR_RE.search(p)
    return f'<w:p>{pp.group(0) if pp else PPR}<w:r>{rp.group(0) if rp else rpr("000000")}<w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>'
def visit(m):
    p=m.group(0); import html; txt=html.unescape("".join(TEXT.findall(p))).strip()
    if txt in REPLACE: st["edits"]+=1; p=retext(p,REPLACE[txt]); txt=REPLACE[txt]
    if txt.startswith("(((PLAY CLIP XXX"): st["pending"]=ORDER[st["i"]]; st["i"]+=1; return p
    if txt=="OUT:" and st["pending"]: bid,st["pending"]=st["pending"],None; return p+block(bid)
    if txt in INSERT_AFTER:
        st["ins"]+=len(INSERT_AFTER[txt])
        return p+"".join(f'<w:p>{PPR}<w:r>{rpr("000000")}</w:r></w:p><w:p>{PPR}<w:r>{rpr("000000")}<w:t xml:space="preserve">{escape(l)}</w:t></w:r></w:p>' for l in INSERT_AFTER[txt])
    return p
body=PARA.sub(visit,xml)
assert st["i"]==7,st; assert st["edits"]==len(REPLACE),(st["edits"],len(REPLACE))
rels="".join(f'<Relationship Id="{r}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" Target="{escape(u,{chr(34):"&quot;"})}" TargetMode="External"/>' for r,u in RELS)
src=zipfile.ZipFile(SRC)
with zipfile.ZipFile(DST,"w",zipfile.ZIP_DEFLATED) as o:
    for it in src.infolist():
        d=src.read(it.filename)
        if it.filename=="word/document.xml": d=body.encode()
        elif it.filename=="word/_rels/document.xml.rels": d=d.decode().replace("</Relationships>",rels+"</Relationships>").encode()
        o.writestr(it,d)
print(f"wrote {DST} · {st['i']} markers · {st['edits']} script edits · {st['ins']} inserted · {len(RELS)} links")
