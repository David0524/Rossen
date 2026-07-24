"""Pass-one metadata triage: 2993 candidates → 5 per beat."""
import json, re, sys
from pathlib import Path
from collections import defaultdict

beats = {b["beat_id"]: b for b in json.loads(Path("beats.json").read_text())}
cands = json.loads(Path("candidates.json").read_text())

# --- source type tagging ---
AFFILIATE_PAT = re.compile(
    r"\b(KXAS|WFAA|ABC7|WCVB|WNBC|KNBC|KABC|KGO|WLS|KPRC|KHOU|WSVN|WPVI|"
    r"WPLG|KPIX|KTLA|WHDH|WBRC|WEWS|WKYC|WHIO|KFOR|KOCO|KOTV|News\s*\d|"
    r"FOX\s*\d|CBS\s*\d|NBC\s*\d|ABC\s*\d|Action\s*News|Eyewitness|"
    r"Local\s*\d+|WXYZ|WTVD|WSB|KMOV|WDAF|KCTV|KSHB|KSDK|WDIV|WXIA|"
    r"11Alive|12News|13News|WFLA|WFTS|WBNS|WLWT|WCPO|WOIO|WSYX|"
    r"WTHR|WISH|WRTV|WAVE|WHAS|WDRB|WLKY|FOX\s*News|CNN)\b",
    re.I
)
NETWORK_PAT = re.compile(
    r"\b(ABC News|NBC News|CBS News|CNBC|MSNBC|PBS|Reuters|AP|"
    r"Associated Press|NPR|Bloomberg|Today\.com|TODAY|Good Morning America|"
    r"CBS Mornings|Nightly News|CNN|BBC|FOX Business|Yahoo Finance)\b",
    re.I
)
CREATOR_PAT = re.compile(
    r"\b(explained|how to|tutorial|walkthrough|breakdown|review|analysis)\b", re.I
)
COMPILATION_PAT = re.compile(
    r"\b(top\s*\d+|compilation|#\d+|destroyed|montage|best of|worst of)\b", re.I
)

def tag_source(c):
    title = c.get("title") or ""
    uploader = c.get("uploader") or c.get("channel") or ""
    combined = f"{title} {uploader}"
    platform = c.get("platform", "youtube")

    if platform in ("news_web", "reddit"):
        if "reddit" in (c.get("url") or ""):
            return "reddit_post"
        return "news_web"

    if NETWORK_PAT.search(combined):
        return "network"
    if AFFILIATE_PAT.search(combined):
        return "affiliate"

    dur = c.get("duration") or 0
    if isinstance(dur, str):
        try: dur = float(dur)
        except: dur = 0

    if dur and dur < 65:
        return "creator_short"
    if CREATOR_PAT.search(title):
        return "creator_long"
    # Check for first-person indicators
    first_person = re.search(r"\b(my |I |me |got scammed|lost my|happened to me|can't believe)\b", title, re.I)
    if first_person:
        return "first_person"
    return "unknown"

# --- hard filters ---
def hard_filter(c, beat):
    title = (c.get("title") or "").lower()
    dur = c.get("duration")
    if isinstance(dur, str):
        try: dur = float(dur)
        except: dur = None

    role = beat["clip_role"]
    orientation = beat["orientation"]

    # Compilation / aggregator
    if COMPILATION_PAT.search(title):
        return "compilation"

    # Duration floor
    if dur is not None:
        if dur < 10:
            return "too_short"
        if role != "evidence" and dur < 25:
            return "too_short"
        # Duration ceiling
        if dur > 1200 and role != "explainer_demo/creator_long":
            return "too_long"

    # AI slop indicators
    if re.search(r"(AI voice|stock footage|generated)", title, re.I):
        return "ai_slop"

    return None

# --- scoring ---
NATURAL_SOURCE = {
    "victim_interview": {"affiliate", "first_person"},
    "confrontation_bust": {"first_person", "raw_footage", "creator_short"},
    "evidence": {"raw_footage", "first_person", "reddit_post"},
    "explainer_demo/creator_long": {"creator_long"},
    "explainer_demo/creator_short": {"creator_short", "first_person"},
    "first_person_rant": {"first_person", "creator_short"},
    "authority_report": {"network", "affiliate", "news_web"},
    "debunk": {"affiliate", "network", "creator_long"},
}

def score(c, beat):
    s = 50  # base
    role = beat["clip_role"]
    src = c.get("source_type", "unknown")
    title = (c.get("title") or "").lower()
    dur = c.get("duration")
    if isinstance(dur, str):
        try: dur = float(dur)
        except: dur = None

    # Source type fit
    natural = NATURAL_SOURCE.get(role, set())
    if src in natural:
        s += 20
    elif src in ("affiliate", "network", "news_web"):
        s += 10
    elif src == "unknown":
        s -= 15

    # Title relevance - check beat keywords
    beat_keywords = set()
    for word in re.findall(r'\w+', beat.get("segment_title", "").lower()):
        if len(word) > 3:
            beat_keywords.add(word)
    anchor_words = set()
    for word in re.findall(r'\w+', (beat.get("news_anchor") or "").lower()):
        if len(word) > 3:
            anchor_words.add(word)

    title_words = set(re.findall(r'\w+', title))
    keyword_hits = len(title_words & (beat_keywords | anchor_words))
    s += min(keyword_hits * 4, 20)

    # Duration fit
    if dur is not None and src != "creator_short":
        if 120 <= dur <= 360:
            s += 8
        elif 60 <= dur <= 600:
            s += 4
        elif dur > 600:
            s -= 5

    # View count tiebreak
    views = c.get("view_count") or c.get("views") or 0
    if isinstance(views, str):
        try: views = int(views)
        except: views = 0
    if views > 100000:
        s += 3
    elif views > 10000:
        s += 1

    # Platform bonus for matching beat expectation
    platform = c.get("platform", "youtube")
    if role == "authority_report" and platform == "news_web":
        s += 8
    if role == "evidence" and platform == "reddit":
        s += 5

    return max(0, min(100, s))

# --- main triage ---
by_beat = defaultdict(list)
for c in cands:
    by_beat[c["beat_id"]].append(c)

shortlist = []
triage_report = {}

for beat in beats.values():
    bid = beat["beat_id"]
    pool = by_beat.get(bid, [])

    # Tag source types
    for c in pool:
        c["source_type"] = tag_source(c)

    # Hard filter
    passed = []
    filtered_reasons = defaultdict(int)
    for c in pool:
        reason = hard_filter(c, beat)
        if reason:
            filtered_reasons[reason] += 1
        else:
            passed.append(c)

    # Score
    for c in passed:
        c["triage_score"] = score(c, beat)

    passed.sort(key=lambda x: -x["triage_score"])

    # Take top 5
    top5 = passed[:5]

    # Diversity floor
    source_types = [c["source_type"] for c in top5]
    mono = all(st in ("affiliate", "network", "news_web") for st in source_types)
    diversity_applied = False
    promoted = None

    if mono and len(top5) == 5:
        # Find highest-scoring non-affiliate/network
        for c in passed[5:]:
            if c["source_type"] not in ("affiliate", "network", "news_web"):
                promoted = c
                top5 = top5[:4] + [c]
                diversity_applied = True
                break

    mix = defaultdict(int)
    for c in top5:
        mix[c["source_type"]] += 1

    triage_report[bid] = {
        "total": len(pool),
        "passed_filter": len(passed),
        "filtered": dict(filtered_reasons),
        "source_mix": dict(mix),
        "diversity_floor": diversity_applied,
        "promoted": promoted["title"][:60] if promoted else None,
    }

    for c in top5:
        shortlist.append(c)

    # Print summary
    print(f"\n{bid} ({beat['clip_role']}, {beat['orientation']})")
    print(f"  {len(pool)} total -> {len(passed)} passed filters -> top 5")
    if filtered_reasons:
        print(f"  filtered: {dict(filtered_reasons)}")
    print(f"  source mix: {dict(mix)}")
    if diversity_applied:
        print(f"  DIVERSITY FLOOR: promoted {promoted['title'][:50]}")
    for i, c in enumerate(top5):
        dur = c.get("duration", "?")
        title = (c.get("title") or "")[:70]
        print(f"  {i+1}. [{c['triage_score']}] {c['source_type']:15} [{dur}s] {title}")

Path("shortlist.json").write_text(json.dumps(shortlist, indent=2, default=str))
Path("triage_report.json").write_text(json.dumps(triage_report, indent=2))
print(f"\nWrote shortlist.json ({len(shortlist)} candidates) and triage_report.json")
