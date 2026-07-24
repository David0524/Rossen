#!/usr/bin/env python3
"""Pass-one metadata triage for F2 08-07.

Hard filters, source_type tagging, then a beat-specific title-fit score.
This narrows ~590 candidates per beat to a reviewable field; the final 5
and the diversity floor are applied by hand on the printed shortlists.

Difference from the 08-05 triage: orientation is no longer *inferred* from
duration. The 08-05 script had to guess that a sub-60s YouTube upload was a
Short, which is false often enough that it shortlisted and flagged a 16:9
52-second video as vertical. The harvester now tags Shorts explicitly
(`platform == "shorts"`, set by ShortsBackend), so orientation is read, not
guessed.
"""
import json, re, collections, sys

RUN = "runs/F2_08072026"
C = json.load(open(f"{RUN}/candidates.json"))
BEATS = {b["beat_id"]: b for b in json.load(open(f"{RUN}/beats.json"))}

# --- source_type tagging -------------------------------------------------
NETWORK = re.compile(r"\b(abc news|nbc news|cbs news|cnbc|cnn|reuters|associated press|"
                     r"\bap\b|today|good morning america|gma|fox business|fox news|"
                     r"msnbc|bloomberg|wall street journal|wsj|60 minutes|"
                     r"washington post|nbc nightly|world news|inside edition)\b", re.I)
AFFIL_CALL = re.compile(r"\b([KW][A-Z]{2,4})\b")
AFFIL_WORDS = re.compile(r"\b(news ?\d{1,2}|channel ?\d{1,2}|abc ?\d|nbc ?\d|cbs ?\d|"
                         r"fox ?\d{1,2}|eyewitness news|action news|on your side|"
                         r"news center|first coast|live ?\d|first alert|\d{1,2} news|"
                         r"tampa bay \d+|wood tv|spectrum news)\b", re.I)
RAW_WORDS = re.compile(r"\b(doorbell|ring cam|security cam|surveillance|dash ?cam|"
                       r"screen recording|caught on camera|caught on cam|cctv|"
                       r"bodycam|body cam)\b", re.I)
LEO = re.compile(r"\b(sheriff|police department|county so|constable|"
                 r"police dept|sheriff's office)\b", re.I)


def source_type(x):
    up = x.get("uploader") or ""
    title = x.get("title") or ""
    plat = x["platform"]
    dur = x["duration"] if isinstance(x["duration"], (int, float)) else None
    if plat == "tiktok":
        return "creator_short"
    if plat == "shorts":
        # A Short from an affiliate/network account is still that outlet's
        # reporting, just cut for the format.
        if NETWORK.search(up) or AFFIL_CALL.search(up) or AFFIL_WORDS.search(up):
            return "affiliate"
        return "creator_short"
    if plat in ("facebook", "instagram"):
        return "first_person"
    if plat == "reddit":
        return "raw_footage"
    if plat == "news_web":
        return "network" if (NETWORK.search(up) or NETWORK.search(title)) else "affiliate"
    if NETWORK.search(up):
        return "network"
    if LEO.search(up):
        return "raw_footage"          # sheriff's office uploads = bodycam/surveillance
    if x.get("is_affiliate") or AFFIL_CALL.search(up) or AFFIL_WORDS.search(up):
        return "affiliate"
    if RAW_WORDS.search(title):
        return "raw_footage"
    if dur is not None and dur <= 75:
        return "creator_short"
    return "creator_long"


# --- hard filters --------------------------------------------------------
AI_SLOP = re.compile(r"\b(axiom lens|ai narrat|true crime daily recap|"
                     r"scam stories|crime & currency|retire informed)\b", re.I)
COMPILATION = re.compile(r"\b(compilation|top \d+|top ten|best of|funniest|"
                         r"try not to|scammers get|gets destroyed|"
                         r"rage|mega ?link|\bpart \d+\b)\b", re.I)
JUNK_LANG = re.compile(r"[一-鿿぀-ヿ가-힯]")


def hard_fail(x, beat):
    t = x.get("title") or ""
    up = x.get("uploader") or ""
    plat = x["platform"]
    dur = x["duration"] if isinstance(x["duration"], (int, float)) else None
    role = beat["clip_role"]

    if JUNK_LANG.search(t):
        return "non-english title"
    if COMPILATION.search(t) or x.get("looks_like_compilation"):
        return "compilation/aggregator"
    if AI_SLOP.search(up) or AI_SLOP.search(t):
        return "AI-narrator / repost channel"

    # Orientation. Shorts crossed against a horizontal beat are NOT auto-failed
    # (grader skill, hard-filters section) -- they are scored and the framing
    # question goes into cannot_determine for a human to rule on.
    # Duration rules do not apply to Shorts at all.
    if plat != "shorts":
        if dur is not None:
            if dur < 25 and role != "evidence":
                return "under 25s duration floor"
            if dur > 1200 and role != "explainer_demo/creator_long":
                return "over 20min, moment is buried"
    return None


# --- beat-specific title fit --------------------------------------------
TERMS = {
    "b01": {
        "core":  [r"\bscam", r"\bfraud", r"\bimposter|impostor|impersonat"],
        "strong": [r"\bfbi\b", r"\bftc\b", r"federal agent", r"courier",
                   r"\bsheriff|deputy|detective\b", r"gold bar", r"\bcash\b"],
        "bonus": [r"manatee", r"xin liu", r"bradenton", r"\$3\.5 ?million",
                  r"at (your|the) door", r"warn"],
    },
    "b02": {
        "core":  [r"\bscam", r"\bfraud"],
        "strong": [r"courier", r"\bsting\b", r"undercover", r"arrest|busted|nab",
                   r"\bdeputy|deputies|sheriff|police\b", r"caught"],
        "bonus": [r"gold (bar|coin)", r"collect", r"show(ed|s)? up",
                  r"elderly|senior|\d{2} year old", r"door", r"bodycam"],
    },
    "b04": {
        "core":  [r"romance scam|catfish|\bscam"],
        "strong": [r"victim", r"lost \$?[\d,]+|loses|lose", r"recovery|recover",
                   r"\bagain\b|twice|second time", r"romance"],
        "bonus": [r"468|\$468", r"long island|\bl\.?i\.?\b", r"facebook group",
                  r"support group", r"investigat"],
    },
}


def fit_score(x, beat_id):
    t = (x.get("title") or "").lower()
    g = TERMS[beat_id]
    s = 0
    if any(re.search(p, t) for p in g["core"]):
        s += 30
    s += 12 * sum(1 for p in g["strong"] if re.search(p, t))
    s += 18 * sum(1 for p in g["bonus"] if re.search(p, t))
    return s


ROLE_PREF = {
    "authority_report":   {"network": 20, "affiliate": 18, "raw_footage": 10,
                           "creator_long": 4, "creator_short": 4, "first_person": 0},
    "confrontation_bust": {"raw_footage": 20, "first_person": 18, "creator_short": 16,
                           "affiliate": 12, "creator_long": 8, "network": 4},
    "victim_interview":   {"affiliate": 20, "first_person": 18, "network": 10,
                           "creator_long": 6, "creator_short": 8, "raw_footage": 6},
}


def score(x, beat):
    st = source_type(x)
    s = fit_score(x, beat["beat_id"])
    s += ROLE_PREF[beat["clip_role"]].get(st, 0)

    dur = x["duration"] if isinstance(x["duration"], (int, float)) else None
    # Shorts are exempt from duration scoring entirely (grader skill).
    if x["platform"] != "shorts" and dur is not None:
        if 120 <= dur <= 360:
            s += 12
        elif 90 <= dur < 120 or 360 < dur <= 600:
            s += 6
        elif dur < 90:
            s -= 6
    if not x.get("uploader"):
        s -= 15
    return s, st


# --- run -----------------------------------------------------------------
out = {}
for bid, beat in BEATS.items():
    if beat.get("excluded_from_search"):
        continue
    rows = [x for x in C if x["beat_id"] == bid]
    kept, dropped = [], collections.Counter()
    seen = set()
    for x in rows:
        if x["video_id"] in seen:
            continue
        seen.add(x["video_id"])
        why = hard_fail(x, beat)
        if why:
            dropped[why] += 1
            continue
        sc, st = score(x, beat)
        x = dict(x)
        x["_score"], x["_source_type"] = sc, st
        kept.append(x)
    kept.sort(key=lambda r: -r["_score"])
    out[bid] = kept[:25]
    print(f"\n{'='*74}\n{bid}  {beat['clip_role']}  ({beat['orientation']})  "
          f"{len(rows)} raw -> {len(kept)} passed filters")
    print(f"  dropped: {dict(dropped)}")
    for r in kept[:18]:
        dur = r["duration"]
        d = f"{int(dur)}s" if isinstance(dur, (int, float)) else "?"
        sf = "*" if r["platform"] == "shorts" else " "
        print(f"  {r['_score']:4d} {sf}{r['_source_type']:14} {r['platform']:9} "
              f"{d:>6}  {(r.get('uploader') or '?')[:24]:24} {(r.get('title') or '')[:58]}")

json.dump(out, open(f"{RUN}/triage_report.json", "w"), indent=2)
print(f"\nwrote {RUN}/triage_report.json")
