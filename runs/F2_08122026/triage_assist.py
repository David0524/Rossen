"""Pass-one assist: narrow 5,725 candidates to a readable set per beat.
Heuristic only — it surfaces, it does not decide. The grade is made by hand
from the printed rows."""
import json, re, sys
from collections import Counter

C = json.load(open("candidates.json"))
BEATS = {b["beat_id"]: b for b in json.load(open("search_beats.json"))}

# Proper-noun / case terms per beat. Tier A = the exact case, tier B = topic.
TERMS = {
 "F2c-b01": (["investigatetv","investigate tv"], ["voice clon","cloned voice","ai voice","fake kidnap","virtual kidnap","wired money","daughter voice"]),
 "F2c-b02": (["dickherber","wentzville","investigatetv"], ["voice clon","clone his voice","cloned voice","ai voice","seconds of audio","demonstrat"]),
 "F2c-b03": (["investigatetv","investigate tv"], ["voice clon","ai voice","fake kidnap","threat","prosecut","cybercrime"]),
 "F2c-b04": (["del mastro","delmastro","martinez"], ["cartel","kidnap","ai voice","voice clon","daughter","20,000","five hour"]),
 "F2c-b05": (["erin west","shamrock","scamdemic"], ["prosecutor","pig butcher","scam call","warning signs"]),
 "F2c-b06": (["olathe"], ["police warn","kansas","kidnap","child","voice","scam warning"]),
 "F2c-b07": (["pearlman","pearlmania"], ["unclaimed","your money","every state","treasury"]),
 "F2c-b08": (["bradley earl","vamoneysearch","fox 5","fox5"], ["virginia","unclaimed","treasur","tiktok","claims"]),
 "F2c-b09": (["udvance","i-cash","icash","19,379","19379"], ["illinois","unclaimed","escrow","treasurer","claim denied","defunct"]),
 "F2c-b09H":(["udvance","i-cash","icash","19,379","19379"], ["illinois","unclaimed","escrow","treasurer","claim denied","defunct","i-team"]),
 "F2c-b10": (["grandparent scam","grandparent fraud"], ["indict","charged","doj","justice department","arrest","sentenc","seniors"]),
}

AFFIL = re.compile(r"\b(ab c|abc|cbs|nbc|fox|kxas|wfaa|kctv|kmbc|kshb|wgn|kgo|wls|witi|wpri|wcnc|wfla|katu|kprc|kare|wsb|wxyz|kdka|kiro|ktla|kron|wusa|wjla|whio|wnep|news ?\d|\d+ news|eyewitness|action news|abc ?\d|cbs ?\d|nbc ?\d|fox ?\d|i-team|investigates)\b", re.I)
NETWORK = re.compile(r"\b(abc news|nbc news|cbs news|cnn|reuters|associated press|\bap\b|today|good morning america|gma|nightline|inside edition|newsnation|scripps)\b", re.I)
SLOP = re.compile(r"\b(compilation|top \d+|scammers get|#\d+|reaction|explained|full movie|iqiyi|animation|drama|sub\b|episode|ep\d|storytime|asmr)\b", re.I)

def src_type(c):
    up = (c.get("uploader") or "") + " " + (c.get("title") or "")
    if NETWORK.search(up): return "network"
    if c.get("is_affiliate") or AFFIL.search(up): return "affiliate"
    if c["platform"] in ("tiktok","instagram"): return "creator_short"
    if (c.get("duration") or 0) and c["duration"] < 90: return "creator_short"
    return "creator_long"

def score(c, tierA, tierB):
    t = (c.get("title") or "").lower(); up=(c.get("uploader") or "").lower()
    blob = t + " " + up
    s = 0
    hitsA=[w for w in tierA if w in blob]; hitsB=[w for w in tierB if w in blob]
    s += 40*len(hitsA) + 7*len(hitsB)
    if not hitsA and not hitsB: return -1, [], []
    d = c.get("duration")
    if d:
        if 90 <= d <= 400: s += 12
        elif 400 < d <= 1200: s += 4
        elif d < 25: s -= 20
        elif d > 2400: s -= 25
    st = src_type(c)
    s += {"affiliate":14,"network":9,"creator_long":2,"creator_short":4}[st]
    if SLOP.search(blob): s -= 30
    if c.get("looks_like_compilation"): s -= 30
    return s, hitsA, hitsB

which = sys.argv[1] if len(sys.argv)>1 else None
byb = {}
for c in C: byb.setdefault(c["beat_id"], []).append(c)

for bid, rows in byb.items():
    if which and bid != which: continue
    tA,tB = TERMS[bid]
    scored=[]
    for c in rows:
        s,hA,hB = score(c,tA,tB)
        if s>0: scored.append((s,hA,c))
    scored.sort(key=lambda x:-x[0])
    b=BEATS[bid]
    print(f"\n{'='*100}\n{bid}  {b['clip_role']}  {b['orientation']}  | {len(rows)} cands, {len(scored)} topical")
    print(f"  platforms in pool: {Counter(c['platform'] for c in rows).most_common()}")
    for s,hA,c in scored[:int(sys.argv[2]) if len(sys.argv)>2 else 22]:
        print(f"  [{s:3}] {c['platform']:9} {src_type(c):13} {str(c.get('duration') or '?'):>5}s "
              f"{str(c.get('published') or '?')[:10]} {(c.get('uploader') or '?')[:26]:26} | {(c.get('title') or '')[:78]}")
        print(f"        {c['url'][:110]}  {'HIT:'+','.join(hA) if hA else ''}")
