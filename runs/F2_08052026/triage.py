#!/usr/bin/env python3
"""Pass-one metadata triage for F2 08-05.

Applies hard filters, tags source_type, scores title-fit against
beat-specific term groups, and emits the top candidates per beat for
human review. Selection of the final 5 + diversity floor is done by hand
on the printed shortlists — this only narrows the field and surfaces the
metadata a human can't eyeball across 3000 rows.
"""
import json, re, collections

C = json.load(open("candidates.json"))
BEATS = {b["beat_id"]: b for b in json.load(open("beats.json"))}

# --- source_type tagging -------------------------------------------------
NETWORK = re.compile(r"\b(abc news|nbc news|cbs news|cnbc|cnn|reuters|associated press|"
                     r"\bap\b|today|good morning america|gma|fox business|fox news|"
                     r"msnbc|bloomberg|wall street journal|wsj|"
                     r"washington post|nbc nightly|world news)\b", re.I)
AFFIL_CALL = re.compile(r"\b([KW][A-Z]{2,4})\b")  # KHOU, WFAA, WDIV, etc.
AFFIL_WORDS = re.compile(r"\b(news ?\d{1,2}|channel ?\d{1,2}|abc ?\d|nbc ?\d|cbs ?\d|"
                         r"fox ?\d{1,2}|eyewitness news|action news|on your side|"
                         r"7 on your side|news center|first coast|live ?\d|"
                         r"first alert|\d{1,2} news)\b", re.I)
RAW_WORDS = re.compile(r"\b(doorbell|ring cam|security cam|surveillance|dash ?cam|"
                       r"screen recording|caught on camera|caught on cam|cctv)\b", re.I)

def source_type(x):
    up = (x.get("uploader") or "")
    title = (x.get("title") or "")
    plat = x["platform"]
    dur = x["duration"] if isinstance(x["duration"], (int, float)) else None
    if plat == "tiktok":
        return "creator_short"
    if plat in ("facebook", "instagram"):
        return "first_person"
    if plat == "reddit":
        return "raw_footage"
    if plat == "news_web":
        if NETWORK.search(up) or NETWORK.search(title):
            return "network"
        return "affiliate"  # most news_web is local affiliate coverage
    # youtube
    if NETWORK.search(up):
        return "network"
    if x.get("is_affiliate") or AFFIL_CALL.search(up) or AFFIL_WORDS.search(up):
        return "affiliate"
    if RAW_WORDS.search(title):
        return "raw_footage"
    if dur is not None and dur <= 75:
        return "creator_short"   # Shorts / vertical
    return "creator_long"

# --- orientation gate ----------------------------------------------------
def orientation_of(x):
    plat = x["platform"]
    dur = x["duration"] if isinstance(x["duration"], (int, float)) else None
    if plat in ("tiktok", "instagram", "facebook", "reddit"):
        return "vertical"
    if plat == "news_web":
        return "horizontal"  # affiliate article/embedded package
    if dur is not None and dur <= 60:
        return "shorts"       # vertical, Shorts-exempt
    return "horizontal"

# --- beat-specific fit terms --------------------------------------------
FIT = {
 "08-05-b01": {"core":[r"amazon"], "groups":[r"refund|owes|money back|late|delivery|guarantee|a.?to.?z|credit|shipping"]},
 "08-05-b02": {"core":[r"amazon|package|delivery|delivered"], "groups":[r"delivered|marked delivered", r"never|not received|missing|stolen|no package|didn.?t (arrive|come)|empty", r"doorbell|porch|camera|caught"]},
 "08-05-b03": {"core":[r"amazon"], "groups":[r"refund|a.?to.?z|claim|denied|refuse|seller|third.?party|scam|dispute|money back"]},
 "08-05-b04": {"core":[r"amazon|ftc|prime"], "groups":[r"settlement|ftc|federal trade|2\.5 ?billion|class action|refund|\$51|\b51\b|payout|prime"]},
 "08-05-b05": {"core":[r"amazon|prime|settlement"], "groups":[r"settlement|refund|check|payout|prime", r"cent|dollar|penn|small|tiny|got|paid|how much|amount"]},
 "08-05-b06": {"core":[r"amazon"], "groups":[r"cpsc|consumer product safety|distributor|recall|400,?000|dangerous|hazard|safety|failed to notify"]},
 "08-05-b07": {"core":[r"immersion|lakkzoom|water heater|bucket heater|heater rod|heating rod|heating element"], "groups":[r"fire|recall|caught|burn|ignite|explode|hazard|melt"]},
 "08-05-b08": {"core":[r"grill brush|bristle|cuisinart|wire brush"], "groups":[r"recall|bristle|food|swallow|wire|danger|throat|hospital|injur"]},
 "08-05-b09": {"core":[r"amazon"], "groups":[r"text|sms|message", r"scam|phishing|fake|fraud", r"recall|refund|inspection"]},
 "08-05-b10": {"core":[r"amazon|ftc|settlement"], "groups":[r"settlement|refund|ftc|prime", r"scam|fake|warning|phish|fraud|paypal|imposter"]},
 "08-05-b11": {"core":[r"tax.?free|sales tax holiday|tax holiday|no sales tax"], "groups":[r"back to school|weekend|shopping|save|saving|states|school supplies|haul|2024|2025|2026"]},
}

def fit_score(x, bid):
    t = (x.get("title") or "").lower()
    spec = FIT[bid]
    core_ok = any(re.search(p, t) for p in spec["core"])
    if not core_ok:
        return 0, False
    g = sum(1 for grp in spec["groups"] if re.search(grp, t))
    return g, True

ROLE_CRED = {
 "victim_interview":        {"affiliate":10,"first_person":9,"creator_long":6,"network":5,"creator_short":6,"raw_footage":5},
 "authority_report":        {"network":10,"affiliate":9,"creator_long":6,"first_person":3,"creator_short":4,"raw_footage":2},
 "evidence":               {"raw_footage":10,"first_person":9,"creator_short":8,"affiliate":6,"network":5,"creator_long":6},
 "explainer_demo/creator_long":{"creator_long":10,"affiliate":6,"network":6,"creator_short":6,"first_person":6,"raw_footage":3},
 "first_person_rant":      {"first_person":10,"creator_short":9,"affiliate":4,"network":3,"creator_long":6,"raw_footage":6},
}
def role_cred(role, st): return ROLE_CRED.get(role, {}).get(st, 5)

def dur_fit(x, role):
    dur = x["duration"] if isinstance(x["duration"], (int, float)) else None
    if dur is None: return 0
    if role in ("evidence","first_person_rant") or dur <= 60: return 0
    if role == "explainer_demo/creator_long":
        return 3 if 60 <= dur <= 1800 else -3
    if 90 <= dur <= 360: return 4
    if 60 <= dur < 90:  return 1
    if 360 < dur <= 600: return 1
    if dur > 1200: return -6
    return 0

results = collections.defaultdict(list)
dropped = collections.Counter()

for x in C:
    bid = x["beat_id"]; beat = BEATS[bid]
    role = beat["clip_role"]; beat_or = beat["orientation"]
    st = source_type(x); cand_or = orientation_of(x)
    if x.get("looks_like_compilation"):
        dropped["compilation"] += 1; continue
    fit_g, core_ok = fit_score(x, bid)
    if not core_ok:
        dropped["offtopic"] += 1; continue
    if beat_or == "horizontal":
        if cand_or == "vertical" and x["platform"] in ("tiktok","instagram","facebook","reddit"):
            dropped["orient_h_reject_vertical"] += 1; continue
    else:
        if cand_or == "horizontal" and x["platform"] == "youtube":
            dropped["orient_v_reject_horiz_yt"] += 1; continue
    dur = x["duration"] if isinstance(x["duration"], (int, float)) else None
    if dur is not None and dur < 25 and role != "evidence":
        dropped["too_short"] += 1; continue
    score = role_cred(role, st)*6 + fit_g*10 + dur_fit(x, role)
    x2 = dict(x); x2["_st"]=st; x2["_cand_or"]=cand_or; x2["_fit"]=fit_g; x2["_score"]=score
    results[bid].append(x2)

def norm(t): return re.sub(r"[^a-z0-9 ]","",(t or "").lower()).strip()
for bid in results:
    seen={}; uniq=[]
    for x in sorted(results[bid], key=lambda r:-r["_score"]):
        k=(norm(x["title"])[:60], x["_st"])
        if k in seen: continue
        seen[k]=1; uniq.append(x)
    results[bid]=uniq

print("DROPPED:", dict(dropped)); print()
out={}
for bid in sorted(results):
    rk=sorted(results[bid], key=lambda r:-r["_score"]); out[bid]=rk[:14]
    beat=BEATS[bid]
    print(f"\n===== {bid}  {beat['clip_role']}  [{beat['orientation']}]  ({len(rk)} survived) =====")
    print("  top-14 source mix:", dict(collections.Counter(x["_st"] for x in rk[:14])))
    for i,x in enumerate(rk[:14]):
        dur=x["duration"] if isinstance(x["duration"],(int,float)) else "?"
        print(f"  {i+1:>2}. [{x['_score']:>3}] {x['_st']:<13} {x['_cand_or']:<10} d={str(dur):<5} fit={x['_fit']} "
              f"{x['platform']:<8} {(x.get('uploader') or '')[:24]:<24} | {(x.get('title') or '')[:66]}")
json.dump({k:[{kk:vv for kk,vv in x.items() if not kk.startswith('thumbnail')} for x in v] for k,v in out.items()},
          open("triage_report.json","w"), indent=1, default=str)
print("\nwrote triage_report.json")
