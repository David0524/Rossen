#!/usr/bin/env python3
"""Mechanical check for a Rossen Outline w/ Videos markdown source.

Usage:
    python3 check_outline.py outline.md --stage beats     # after Phase 1
    python3 check_outline.py outline.md --stage videos    # after Phase 2

Stage defaults to whatever the header's **Stage:** says.
ERROR = fix before building. WARN = read it and decide. Exit 1 on any ERROR.
"""

import argparse
import re
import sys

STORY_H1 = re.compile(r"^#\s+([A-Z]|\d+)\.\s+(.*)$", re.M)
BEAT_HEADER = ["#", "beat", "who", "what happens", "clip"]
VIDEO_HEADER = ["#", "clip", "shows", "in–out", "status"]
FOOTAGE = re.compile(r"^(HAVE|FIND)\s*·\s*(HORIZONTAL|VERTICAL)(\s+BROLL)?\b")
OTHER_TAGS = ("DEMO", "GUEST", "JEFF", "STILLS")
STATUSES = ("PICK", "WEAK", "MANUAL", "SWAP", "THROTTLED", "EMPTY")
STATUS_RE = re.compile(r"^(%s)(\s*·\s*(UNVERIFIED|CROP))*$" % "|".join(STATUSES))
LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
TIMECODE = re.compile(r"\b\d{1,2}:\d{2}\b(?!\s*(am|pm))", re.I)
RANGE = re.compile(r"\d{1,2}:\d{2}\s*[–-]\s*\d{1,2}:\d{2}")

# --- Who column: is there a person in it? ----------------------------------
PLURAL_CATEGORY = re.compile(
    r"\b(shoppers|people|users|customers|victims|consumers|drivers|parents|"
    r"seniors|families|homeowners|renters|travelers|patients|workers|employees|"
    r"owners|viewers|fans|buyers|sellers|residents|members|fact-checkers|"
    r"experts|officials|carriers|companies|retailers|stores|banks)\b", re.I)
ROLE_NOUN = re.compile(
    r"\b(woman|man|mom|mother|dad|father|son|daughter|wife|husband|couple|"
    r"family|grandmother|grandfather|grandma|grandpa|teen|girl|boy|student|"
    r"worker|employee|shopper|customer|owner|creator|expert|hacker|officer|"
    r"detective|sheriff|trooper|reporter|nurse|doctor|lawyer|veteran|"
    r"retiree|driver|patient|whistleblower|founder|ceo|host|guest|victim|"
    r"homeowner|renter|traveler|professor|investigator|agent|senator|mayor)\b",
    re.I)
ORG_WORDS = re.compile(
    r"\b(Attorney General|AG|FBI|FTC|FCC|FDA|Department|Commission|Bureau|"
    r"Office|Agency|Inc|LLC|Corp|Company|Bank|Police|Court|Association|"
    r"University|Group|App|Cart|Statement|Policy|Settlement)\b")
NAME_PAIR = re.compile(r"\b[A-Z][a-z]+(?:[-'][A-Za-z]+)?\s+[A-Z][a-z]+")
NO_PERSON = re.compile(
    r"^(—|-|n/?a|none|tbd|unnamed|unknown|policy|the policy|settlement)\b", re.I)


def who_problem(who):
    """None if Who reads as a person; otherwise a short reason."""
    w = who.strip()
    if not w:
        return "blank"
    if re.match(r"you\b|the scammers?\b", w, re.I):
        return None
    if NO_PERSON.match(w):
        return "no person"
    if PLURAL_CATEGORY.search(w) and not ROLE_NOUN.search(w):
        return "a category, not a person"
    if ROLE_NOUN.search(w):
        return None
    if NAME_PAIR.search(ORG_WORDS.sub(" ", w)):
        return None
    if ORG_WORDS.search(w):
        return "an institution, not a person"
    if re.fullmatch(r"[A-Z][a-z]+", w):
        return "a first name with no identity — say who they are"
    return "a company or document, not a person"


def is_human(who):
    return who_problem(who) is None and not re.match(r"you\b|the scammers?\b",
                                                     who.strip(), re.I)


errors, warns = [], []
err, warn = errors.append, warns.append


def tables(block):
    """Yield (header, rows) for each pipe table in block."""
    cur = []
    for line in block.splitlines() + [""]:
        s = line.strip()
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                cur.append(cells)
        elif cur:
            yield [re.sub(r"\*", "", c).lower() for c in cur[0]], cur[1:]
            cur = []


def check(md, stage):
    body = re.sub(r"<!--.*?-->", "", md, flags=re.S)

    if "(((" in body or re.search(r"\bOUT:", body):
        err("Bible markers found ((((…))) or OUT:). The outline never carries them.")
    for m in re.finditer(r"<[^>\n]{1,60}>", body):
        err(f"Unfilled template slot: {m.group(0)}")

    first = STORY_H1.search(body)
    page_one = body[: first.start()] if first else body

    header = re.search(r"\*\*Stage:\*\*\s*(\w+)", page_one)
    declared = header.group(1).lower() if header else None
    if not declared:
        err("Header has no **Stage:** (beats or videos).")
    stage = stage or declared or "beats"
    if declared and declared != stage:
        err(f"Header says Stage: {declared}, checking as {stage}. Make them agree.")

    if not re.search(r"^#\s+\S", page_one, re.M):
        err("No title H1.")
    for h in ("**Airdate:**", "**Stories:**"):
        if h not in page_one:
            err(f"Header has no {h}")
    if "## RUNNING ORDER" not in page_one:
        err("Page one has no '## RUNNING ORDER'.")
    else:
        ro = page_one.split("## RUNNING ORDER", 1)[1].split("###", 1)[0]
        rows = [r for _, rs in tables(ro) for r in rs]
        if not rows:
            err("RUNNING ORDER has no table.")
        elif not any("omniwatch" in " ".join(r).lower() for r in rows):
            warn("No OmniWatch break in the running order.")
    for h in ("### The show in three sentences", "### The ride",
              "### Decisions before we write"):
        if h not in page_one:
            err(f"Page one missing '{h}'.")
    if TIMECODE.search(page_one):
        err("Timecode on page one. Timecodes live only in Videos tables.")

    starts = list(STORY_H1.finditer(body))
    if not starts:
        err("No story sections (# A. HEADLINE).")
    if "WEDNESDAY" in page_one.upper() and len(starts) > 2 \
            and not re.search(r"confirm", page_one, re.I):
        warn(f"Wednesday with {len(starts)} stories. Default is A + B. "
             "Say it was confirmed in the **Stories:** line.")

    decisions = page_one.split("### Decisions before we write", 1)[-1]

    for idx, m in enumerate(starts):
        label = f"Story {m.group(1)}"
        end = starts[idx + 1].start() if idx + 1 < len(starts) else len(body)
        block = body[m.start():end]
        for req in ("**In one sentence:**", "**Peg:**", "**Weight:**",
                    "### The fix", "### Gaps"):
            if req not in block:
                err(f"{label}: missing {req}")

        found = dict((tuple(h), rs) for h, rs in tables(block))
        beats = found.get(tuple(BEAT_HEADER))
        if beats is None:
            err(f"{label}: no beat table | # | Beat | Who | What happens | Clip |")
            continue

        lo, hi = (5, 9) if idx == 0 else (2, 4)
        if not lo <= len(beats) <= hi:
            warn(f"{label}: {len(beats)} beats (expected {lo}–{hi} for this slot).")

        footage, video, stills, humans = {}, 0, 0, 0
        for r in beats:
            if len(r) != 5:
                err(f"{label} beat {r[0] if r else '?'}: row needs 5 cells.")
                continue
            n, _, who, what, clip = r
            prob = who_problem(who)
            if prob == "blank":
                err(f"{label} beat {n}: Who is blank. Write the gap "
                    "(e.g. 'Unnamed — need a name').")
            elif prob:
                warn(f"{label} beat {n}: Who '{who}' is {prob}. "
                     "Name one, or flag it in Decisions.")
            elif is_human(who):
                humans += 1
            if len(what.split()) > 25:
                err(f"{label} beat {n}: 'What happens' is {len(what.split())} "
                    "words (max 25). Split the beat.")
            if TIMECODE.search(what):
                err(f"{label} beat {n}: timecode in the beat table.")
            tag0 = clip.split()[0].rstrip("—-:,") if clip else ""
            fm = FOOTAGE.match(clip)
            if fm:
                footage[n] = fm.group(2)
                video += 1
            elif tag0 in ("HAVE", "FIND"):
                err(f"{label} beat {n}: footage tag needs an orientation — "
                    "'HAVE · VERTICAL', 'FIND · HORIZONTAL'.")
            elif tag0 not in OTHER_TAGS:
                err(f"{label} beat {n}: Clip must start with HAVE · <ORIENTATION>, "
                    "FIND · <ORIENTATION>, DEMO, GUEST, JEFF or STILLS.")
            if tag0 == "STILLS":
                stills += 1
            caps = re.findall(r"[A-Za-z]{3,}", what)
            if caps and sum(w.isupper() for w in caps) / len(caps) > 0.6:
                warn(f"{label} beat {n}: reads in ALL CAPS. The outline is sentence case.")

        if stills and stills >= video:
            warn(f"{label}: {stills} STILLS beat(s) vs {video} video. The show wants video.")
        if humans == 0:
            warn(f"{label}: no named human anywhere in Who.")

        vids = found.get(tuple(VIDEO_HEADER))
        has_heading = "### Videos" in block
        if stage == "beats":
            if has_heading or vids is not None:
                err(f"{label}: Videos table present at Stage: beats. "
                    "Flip the header to videos, or remove it.")
            continue

        # ---- stage: videos
        if not footage:
            continue
        if vids is None:
            err(f"{label}: {len(footage)} footage beat(s) but no ### Videos table "
                "| # | Clip | Shows | In–Out | Status |.")
            continue
        seen = {}
        for r in vids:
            if len(r) != 5:
                err(f"{label} Videos row {r[0] if r else '?'}: needs 5 cells.")
                continue
            n, clip, shows, inout, status = r
            if n in seen:
                err(f"{label} Videos: beat {n} has two rows. One pick per beat.")
            seen[n] = status
            if n not in footage:
                err(f"{label} Videos: row {n} is not a HAVE/FIND beat.")
            st = status.upper().replace(" ", "")
            if not STATUS_RE.match(status.strip()):
                err(f"{label} Videos row {n}: status '{status}' — use "
                    f"{', '.join(STATUSES)}, optionally '· UNVERIFIED' / '· CROP'.")
                continue
            base = status.split("·")[0].strip()
            linked = LINK.search(clip)
            if base in ("PICK", "WEAK", "MANUAL", "SWAP", "THROTTLED") and not linked:
                err(f"{label} Videos row {n}: {base} needs a [title](URL) link.")
            if base in ("PICK", "WEAK", "SWAP") and "UNVERIFIED" not in st:
                if not (RANGE.search(inout) and '"' in inout) and \
                        "WHOLE CLIP" not in inout.upper():
                    err(f"{label} Videos row {n}: {base} without UNVERIFIED needs "
                        'in–out and a verbatim outcue: 0:17–0:51 "outcue".')
            if base in ("MANUAL", "THROTTLED", "EMPTY") or "UNVERIFIED" in st:
                if RANGE.search(inout) and "UNVERIFIED" in st:
                    err(f"{label} Videos row {n}: UNVERIFIED with a timecode. "
                        "No transcript, no timecode.")
            if base == "EMPTY" and len(shows.split()) < 3:
                err(f"{label} Videos row {n}: EMPTY needs a reason in Shows.")
            if base in ("EMPTY", "WEAK") or "CROP" in st:
                if not re.search(rf"\b{m.group(1)}\s*(beat\s*)?{n}\b|{m.group(1)}{n}\b",
                                 decisions):
                    warn(f"{label} Videos row {n}: {status} should be in Decisions "
                         f"(write '{m.group(1)} beat {n}').")
            if re.search(r"confirm(ed)? on screen|we watched|watched it", shows, re.I):
                err(f"{label} Videos row {n}: claims the footage was watched.")
        for n in footage:
            if n not in seen:
                err(f"{label}: footage beat {n} has no Videos row.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--stage", choices=["beats", "videos"])
    a = ap.parse_args()
    check(open(a.path, encoding="utf-8").read(), a.stage)
    for e in errors:
        print(f"ERROR  {e}")
    for w in warns:
        print(f"WARN   {w}")
    if not errors and not warns:
        print("clean")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
