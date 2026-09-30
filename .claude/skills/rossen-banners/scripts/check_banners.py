#!/usr/bin/env python3
"""Mechanical checks for a Rossen Reports banner list.

Usage: python check_banners.py banners.txt   (or pipe the list on stdin)

One banner per line. Leading "-", "*", "•" and blank lines are ignored.
Catches mechanical misses only. It cannot judge clarity, stakes, or whether a
banner makes someone want to watch; that is the writer's job.
"""
import re
import sys

MAX_CHARS = 45          # Jeff's longest approved banner
MAX_WORDS = 8
TARGET_CHARS = 38       # typical approved length

STOCK = {
    "WELCOME TO ROSSEN REPORTS",
    "LIKE AND SUBSCRIBE",
    "JOIN THE CHAT",
    "CALL AND SHARE YOUR SCAM STORY!",
    "SCAM HOTLINE: 866-9-ROSSEN",
    "DEALSEEK.COM/ROSSEN",
    "🔥 AMAZON'S HOTTEST DEALS",
}

# Fixed guest labels: reused word for word. Key = name that triggers the check.
FIXED_LABELS = {
    "NADER": "NADER MARCOS, DEALSEEK CO-FOUNDER",
    "TREY": "TREY DONOVAN, DEALSEEK FOUNDER",
    "STICKLEY": "JIM STICKLEY | ETHICAL HACKER",
    "NOFZIGER": "AMY NOFZIGER | AARP FRAUD VICTIM SUPPORT",
}
DEALSEEK_HOSTS = {FIXED_LABELS["NADER"], FIXED_LABELS["TREY"]}
DEALSEEK_URL = "DEALSEEK.COM/ROSSEN"

EMOJI_RE = re.compile("[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F]")

WEAK = [
    "ON THE RISE", "BEWARE", "TARGETS", "AMID", "TERRIFYING", "INSANE",
    "SHOCKING", "HORRIFYING", "UNBELIEVABLE", "CRAZY", "MUST SEE",
    "YOU WON'T BELIEVE", "HERE'S HOW", "BEFORE IT HAPPENS", "WATCH THIS",
]

PLACEHOLDER = re.compile(
    r"XXX|\bTBD\b|\bTK\b|\?\?|\[|\]|\*|\bLABEL FOR\b|\bBANNERS?\b|EMOJI|"
    r"WHAT'S HIS|WHAT'S HER|\bINSERT\b|\bPLACEHOLDER\b", re.I)

K_SHORTHAND = re.compile(r"\$\d+(?:\.\d+)?\s?[KkMm]\b")

STATES = [
    "ALABAMA", "ALASKA", "ARIZONA", "ARKANSAS", "CALIFORNIA", "COLORADO",
    "CONNECTICUT", "DELAWARE", "FLORIDA", "GEORGIA", "HAWAII", "IDAHO",
    "ILLINOIS", "INDIANA", "IOWA", "KANSAS", "KENTUCKY", "LOUISIANA", "MAINE",
    "MARYLAND", "MASSACHUSETTS", "MICHIGAN", "MINNESOTA", "MISSISSIPPI",
    "MISSOURI", "MONTANA", "NEBRASKA", "NEVADA", "NEW HAMPSHIRE", "NEW JERSEY",
    "NEW MEXICO", "NEW YORK", "NORTH CAROLINA", "NORTH DAKOTA", "OHIO",
    "OKLAHOMA", "OREGON", "PENNSYLVANIA", "RHODE ISLAND", "SOUTH CAROLINA",
    "SOUTH DAKOTA", "TENNESSEE", "TEXAS", "UTAH", "VERMONT", "VIRGINIA",
    "WASHINGTON", "WEST VIRGINIA", "WISCONSIN", "WYOMING",
]
STATE_RE = re.compile(r"\b(" + "|".join(STATES) + r")\b")
CITY_STATE_RE = re.compile(r"\|\s*[A-Z .'-]+,\s*[A-Z .]+$")

STOPWORDS = {
    "THE", "A", "AN", "AND", "&", "OF", "TO", "YOUR", "YOU", "THIS", "IS",
    "IN", "ON", "FOR", "NOW", "RIGHT", "THEY", "IT", "CAN", "WITH", "|", ":",
    # show-wide words that appear in almost every banner
    "SCAM", "SCAMMER", "SCAMMED", "ROSSEN", "REPORT",
}


def norm(b):
    """Straighten curly quotes so fixed-text comparisons work."""
    return b.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"').strip()


def clean(line):
    return re.sub(r"^\s*[-*•—–]+\s*", "", line).strip()


def words(b):
    return [w for w in re.split(r"[\s|—–]+", b) if w and w not in {":", "|", "&"}]


def stem(w):
    w = re.sub(r"[^A-Z0-9$,]", "", w).rstrip(",")
    return w[:-1] if len(w) > 3 and w.endswith("S") else w


def content_words(b):
    out = set()
    for w in words(b.upper()):
        bare = re.sub(r"[^A-Z0-9$,]", "", w).rstrip(",")
        if bare and bare not in STOPWORDS:
            s = stem(w)
            if s and s not in STOPWORDS:
                out.add(s)
    return out


def main():
    src = open(sys.argv[1]).read() if len(sys.argv) > 1 else sys.stdin.read()
    raw = [l for l in src.splitlines() if clean(l)]
    banners = [norm(clean(l)) for l in raw]
    issues = []
    notes = []
    if any(re.match(r"^\s*[-*•—–]", l) for l in raw):
        notes.append("  deliver plain lines: no dashes or bullets in front of banners")

    def flag(i, msg):
        issues.append(f"  line {i + 1}: {msg}\n      {banners[i]}")

    if not banners:
        print("No banners found.")
        return 1

    if banners[0].upper() != "WELCOME TO ROSSEN REPORTS":
        issues.append("  list: first banner should be WELCOME TO ROSSEN REPORTS")
    joined = {b.upper() for b in banners}
    for s in ("LIKE AND SUBSCRIBE", "JOIN THE CHAT"):
        if s not in joined:
            notes.append(f"  no '{s}' (fine if the bible has none, e.g. a call-in show)")

    fixed = set(FIXED_LABELS.values())
    ups = [b.upper() for b in banners]
    tease_end = max([i for i, u in enumerate(ups) if u in ("LIKE AND SUBSCRIBE", "JOIN THE CHAT")] or [6]) + 2

    this_count = 0
    for i, b in enumerate(banners):
        up = b.upper()
        is_stock = up in STOCK or up in fixed
        # fixed labels must match exactly
        for key, label in FIXED_LABELS.items():
            if re.search(r"\b" + key + r"\b", up) and ("|" in up or "," in up or "DEALSEEK" in up) and up != label:
                flag(i, f"fixed label; use exactly: {label}")
        # emoji: only the fire emoji, only on the Amazon tease at the top
        emo = EMOJI_RE.findall(b)
        if emo:
            if any(e != "\U0001F525" for e in emo):
                flag(i, "emoji other than 🔥; no other emoji, ever")
            elif "AMAZON" not in up:
                flag(i, "🔥 goes only on the Amazon deals tease")
            elif i > tease_end:
                flag(i, "🔥 goes only in the tease at the top of the show")
        if b != up:
            flag(i, "not all caps")
        if is_stock:
            if re.search(r"\bTHIS\b", up):
                this_count += 1
            continue
        if len(b) > MAX_CHARS:
            flag(i, f"{len(b)} characters (ceiling {MAX_CHARS}, aim ~{TARGET_CHARS})")
        if len(words(b)) > MAX_WORDS:
            flag(i, f"{len(words(b))} words (ceiling {MAX_WORDS})")
        if PLACEHOLDER.search(b):
            flag(i, "placeholder or note-to-self, not finished copy")
        if K_SHORTHAND.search(b):
            flag(i, "dollar shorthand; write the full figure ($8,000 not $8K)")
        if STATE_RE.search(up) or CITY_STATE_RE.search(up):
            flag(i, "location; use stakes instead unless the place is the story")
        for w in WEAK:
            if re.search(r"\b" + re.escape(w) + r"\b", up):
                flag(i, f"weak or editorializing phrase: {w}")
        body = b.split("|")[0]
        if re.search(r"[—–;]| - ", body) or body.count(",") and not re.search(r"\d,\d", body):
            flag(i, "comma or dash: if it joins two ideas, split or pick one; if it's a list, use &")
        if "!" in b and not is_stock:
            flag(i, "exclamation point outside a stock line")
        if re.search(r"\bTHIS\b", up):
            this_count += 1

    for i, u in enumerate(ups):
        if u in DEALSEEK_HOSTS and (i + 1 >= len(ups) or ups[i + 1] != DEALSEEK_URL):
            flag(i, f"DealSeek host label must be followed right away by {DEALSEEK_URL}")
    if any(u in DEALSEEK_HOSTS for u in ups) and ups.count(DEALSEEK_URL) != 1:
        issues.append(f"  list: {DEALSEEK_URL} should appear exactly once, right after the DealSeek host label")
    if DEALSEEK_URL in ups:
        after = [u for u in ups[ups.index(DEALSEEK_URL) + 1:]]
        if after:
            notes.append(f"  {len(after)} banner(s) after {DEALSEEK_URL}: fine only if the DealSeek segment has ended")

    if this_count > 3:
        issues.append(f"  list: THIS used in {this_count} banners; keep it to 2-3 so it still lands")

    # Words in a quarter or more of the list are the show's subject (PHONE on a
    # phone-scam show, PRIME/DEAL on a Prime Day show), not a sign of repetition.
    from collections import Counter
    cw = [set() if (u in STOCK or u in fixed) else content_words(b) for u, b in zip(ups, banners)]
    df = Counter(w for s in cw for w in s)
    show_wide = {w for w, c in df.items() if c >= max(3, 0.25 * len(banners))}
    for i in range(len(banners)):
        for j in range(i + 1, len(banners)):
            a, b = cw[i] - show_wide, cw[j] - show_wide
            shared = a & b
            # A tease and its story's later banner are meant to share a subject;
            # only near-restatements count there.
            across_tease = i <= tease_end < j
            loose = len(shared) >= 2 and min(len(a), len(b)) <= 3 and not across_tease
            if len(shared) >= 3 or loose:
                issues.append(
                    f"  lines {i + 1} & {j + 1}: may say the same thing ({', '.join(sorted(shared))})\n"
                    f"      {banners[i]}\n      {banners[j]}")

    print(f"{len(banners)} banners checked.")
    if notes:
        print("Notes:")
        print("\n".join(notes))
    if issues:
        print(f"{len(issues)} flag(s):")
        print("\n".join(issues))
        return 1
    print("No mechanical issues. Now read it as a viewer who just tuned in.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
