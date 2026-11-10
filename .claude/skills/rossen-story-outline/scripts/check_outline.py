#!/usr/bin/env python3
"""Mechanical check for a Rossen Outline w/ Videos (v3: the outline + Build Sheet).

Usage:
    python3 check_outline.py outline.md --stage beats     # after Phase 1
    python3 check_outline.py outline.md --stage videos    # after Phase 2
    python3 check_outline.py outline.md --stage videos --transcripts transcripts.json

v3 layout (producer, 11/10/2026): the front is the show in air order for the
room (headlines, talking points, clip blocks with soundbites, the break, the
protection steps, the close); the Build Sheet after a page break carries the
spine, the beats table, Jeff notes, fix sources and open calls. This
checker makes the two agree. Both layers are plain sentences with no machine
markers (producer, 11/10/2026): no ⚠️ or other emoji, no status words, no Status
column, no Gaps section; a clip that needs something carries a `No times yet:`,
`Legal:` or `Note:` line. An old table-format outline (v2: "| # | Beat | Who
| What happens | Clip |") is handed to check_outline_v2.py.

Stage defaults to whatever the header's "Stage:" says.
ERROR = fix before building. WARN = read it and decide. Exit 1 on any ERROR.
"""

import argparse
import datetime as dt
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_outline_v2 as v2  # noqa: E402  (helpers + legacy checker)

errors, warns = v2.errors, v2.warns          # window_scan reports into these
err, warn = errors.append, warns.append

BUILD = re.compile(r"^#\s+BUILD SHEET\b.*$", re.M)
TAG = re.compile(r"^`([A-Z]\d{1,2})\s*·\s*([^`]*)`\s*$", re.M)
HEAD2 = re.compile(r"^##\s+(.+?)\s*$", re.M)
CLIP_LINE = re.compile(
    r"^\s*(?:-\s*)?\*\*CLIP\s+(\d+)\s*\((HORIZONTAL|VERTICAL)(\s+BROLL)?\)\s*:\*\*\s*(.*)$", re.M)
CLIP_PH = re.compile(
    r"^\s*(?:-\s*)?\*\*CLIP\s+—\s*(HAVE|FIND)\s*·\s*(HORIZONTAL|VERTICAL)(\s+BROLL)?\s*:\*\*\s*(.*)$", re.M)
INOUT = re.compile(r"^\s*-\s*\*\*\s*\d{1,2}:\d{2}\s*[–-]\s*\d{1,2}:\d{2}.*\*\*\s*$")
SOUND = re.compile(r"^\s*-\s*\*Soundbite:", re.I)
NOTE = re.compile(r"^\s*-\s*(?:\*\*)?(No times yet|Legal|Note):", re.I)
BEAT_HEADER = ["beat", "clip", "who", "tag", "adds", "search specifics"]
BEAT_HEADER_OLD = ["beat", "clip", "who", "tag", "status", "adds", "search specifics"]
EMOJI = re.compile("[\u2600-\u27BF\U0001F300-\U0001FAFF\uFE0F]")
STATUS_WORD = re.compile(r"(?<![A-Za-z])(PICK|THROTTLED|UNVERIFIED|WEAK|CROP|EMPTY|MANUAL)(?![A-Za-z])|·\s*LEGAL\b")
SPINE = ["In one sentence", "Hold back", "Peg", "Climb", "Framing", "Open package",
         "Weight"]
TAGS = re.compile(r"^((HAVE|FIND)\s*·\s*(HORIZONTAL|VERTICAL)(\s+BROLL)?|DEMO|GUEST|JEFF|STILLS)$")
DATED = re.compile(
    r"\b(holidays?|holiday season|thanksgiving|christmas|hanukkah|new year'?s|"
    r"black friday|cyber monday|halloween|(this|last|next) (fall|autumn|winter|"
    r"spring|summer|season|week|weekend|month|year)|this time of year)\b", re.I)
TEASE_THIS = re.compile(r"^\s*-\s*(and |but |then |plus )?(this|these) (family|woman|man|"
                        r"couple|neighbor|homeowner|shopper|grandmother|veteran)\b", re.I)
OUTLET = re.compile(r"\b(CBS|NBC|ABC\d*|FOX\s?\d*|CNN|NPR|KTLA|KCAL|WBZ|WCVB|"
                    r"Inside Edition|Good Morning America|Dateline)\b")
AMP = re.compile(r"\b(now|but|even|worse|spreading|not just|bigger|closer|next|"
                 r"gets|another|already|again|faster|so who|wait)\b", re.I)


def split_front(md):
    m = BUILD.search(md)
    return (md[: m.start()], md[m.start():]) if m else (md, "")


def blocks(front):
    """Yield (headline, body) for each ## section of the front, in order."""
    heads = list(HEAD2.finditer(front))
    for i, h in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(front)
        yield h.group(1), front[h.end():end]


def check(md, stage, tx=None):
    body = re.sub(r"<!--.*?-->", "", md, flags=re.S)
    if re.search(r"^\|\s*#\s*\|\s*Beat\s*\|\s*Who\s*\|", body, re.M | re.I):
        print("(v2 table outline: using check_outline_v2)")
        return v2.check(md, stage, tx)

    if "(((" in body or re.search(r"\bOUT:", body):
        err("Bible markers found ((((…))) or OUT:). The outline never carries them.")
    for m in re.finditer(r"<[^>\n]{1,60}>", body):
        err(f"Unfilled template slot: {m.group(0)}")

    for i, line in enumerate(body.splitlines(), 1):
        if EMOJI.search(line):
            err(f"Line {i}: emoji or ⚠️ ('{line.strip()[:50]}'). The outline is plain sentences "
                f"(producer, 11/10): say what's needed in words.")
        elif not line.startswith("#") and not re.match(r"^\s*\d+\.\s+\*\*", line) \
                and STATUS_WORD.search(line):
            warn(f"Line {i}: status word '{STATUS_WORD.search(line).group(0)}' "
                 f"('{line.strip()[:50]}'). Pipeline status stays in the run folder; "
                 f"write a plain sentence (producer, 11/10).")

    front, sheet = split_front(body)
    if not sheet:
        err("No '# BUILD SHEET' after the close. v3 outlines carry it behind a page break.")
    elif "[[PAGE BREAK]]" not in front[-400:] + sheet[:50]:
        warn("Put [[PAGE BREAK]] right before '# BUILD SHEET' so the room can stop there.")

    # ---- header and page one ------------------------------------------------
    hm = re.search(r"Stage:\s*(beats|videos)", front[:800], re.I)
    declared = hm.group(1).lower() if hm else None
    if not declared:
        err("Header line has no 'Stage: beats' or 'Stage: videos'.")
    stage = stage or declared or "beats"
    if declared and declared != stage:
        err(f"Header says Stage: {declared}, checking as {stage}. Make them agree.")
    if not re.search(r"^#\s+\S", front, re.M):
        err("No title H1.")
    am = re.search(r"Airdate\s+[A-Za-z]{3}\s+([A-Za-z]{3})[a-z]*\s+(\d{1,2}),\s*(\d{4})", front[:800])
    aired = (dt.date(int(am.group(3)), v2.MONTHS[am.group(1).lower()], int(am.group(2)))
             if am and am.group(1).lower() in v2.MONTHS else None)
    if not aired:
        warn("Header line has no 'Airdate Wed Nov 11, 2026'; the six-month dating check is skipped.")
    for h in ("SUMMARY", "THE SHOW", "THE TEASE", "CLOSE"):
        if not re.search(rf"^##\s+{h}\b", front, re.M):
            err(f"Front has no '## {h}'.")
    show = re.search(r"^##\s+THE SHOW\b(.*?)(?=^##\s)", front, re.M | re.S)
    if show and not re.search(r"^\s*1\.\s", show.group(1), re.M):
        err("THE SHOW is a numbered list (one line per headline, break and close).")
    if show and "|" in show.group(1):
        warn("THE SHOW is a list, not a table (v3).")
    if re.search(r"^##\s+(DECISIONS|RUNNING ORDER)\b", front, re.M):
        warn("Decisions and the running-order table moved: Open calls go in the Build "
             "Sheet (and chat/OPEN.md); THE SHOW is a list.")

    # ---- front blocks -------------------------------------------------------
    front_beats, clip_nums, footage_front, legal_clips = [], [], {}, []
    prev_clip_seen = False
    for head, txt in blocks(front):
        if head.upper().startswith(("SUMMARY", "THE SHOW", "CLOSE")):
            continue
        if head.upper().startswith("THE TEASE"):
            tt = TAG.search(txt)
            if tt:
                front_beats.append(tt.group(1))
            pts = [l for l in txt.splitlines() if l.strip().startswith("-")]
            for l in pts:
                if TEASE_THIS.match(l):
                    warn(f"Tease: '{l.strip()[:60]}'. Jeff (11/11): 'You're going to "
                         f"see this family…', not 'This family…'.")
            continue
        tg = TAG.search(txt)
        if not tg:
            err(f"Block '{head[:50]}' has no beat tag line (`A2 · place · Mon YYYY`).")
            continue
        bid = tg.group(1)
        front_beats.append(bid)
        if head != head.upper():
            warn(f"{bid}: headline isn't in caps; it's the on-air header as written.")
        if re.match(r"^(AND |BUT )?IN [A-Z][A-Z ]+…", head):
            warn(f"{bid}: headline opens on a place ('{head[:40]}'). Subject first, impact on you.")
        pts = [l for l in txt.splitlines() if re.match(r"^-\s", l) and not
               re.match(r"^-\s*\*\*(Out|Red flag):", l)]
        for l in pts:
            t = l[1:].strip()
            if len(t.split()) > 25:
                warn(f"{bid}: talking point over 25 words: '{t[:50]}…'")
            if t.isupper() and len(t) > 20:
                warn(f"{bid}: talking point in caps; the outline is sentence case.")
            if DATED.search(t):
                warn(f"{bid}: '{DATED.search(t).group(0)}' dates the video. Jeff (11/11): "
                     f"evergreen; the date goes in a Jeff note.")
            if OUTLET.search(t):
                warn(f"{bid}: talking point names an outlet ('{OUTLET.search(t).group(0)}'). "
                     f"Jeff (11/11): no 'CBS shows this'; the clip line credits it.")
        for l in txt.splitlines():
            m = re.match(r"^-\s*\*\*(Out|Red flag):\*\*\s*(.*)", l)
            if m and DATED.search(m.group(2)):
                warn(f"{bid}: '{DATED.search(m.group(2)).group(0)}' in the {m.group(1)} line dates the video.")
        has_clip = False
        for m in CLIP_LINE.finditer(txt):
            has_clip = True
            n = int(m.group(1))
            clip_nums.append(n)
            footage_front.setdefault(bid, []).append(n)
            rest = txt[m.end():].splitlines()[1:6]
            inout = next((r for r in rest if INOUT.match(r)), None)
            notes = [NOTE.match(r).group(1).lower() for r in rest if NOTE.match(r)]
            no_times = "no times yet" in notes
            if "legal" in notes:
                legal_clips.append((bid, n))
            if not v2.LINK.search(m.group(4)):
                err(f"Clip {n}: no [Outlet — title](URL) link on the clip line.")
            if not inout and not no_times:
                err(f"Clip {n}: no bold in–out line under the clip (or a 'No times yet:' "
                    f"line saying why and how to get them).")
            if inout and no_times:
                err(f"Clip {n}: has an in–out line and 'No times yet:'. One or the other.")
            if not any(SOUND.match(r) for r in rest) and not no_times:
                err(f"Clip {n}: no *Soundbite:* line. The room judges the clip from it.")
            if re.search(r"\b(watched|confirmed on screen|we saw)\b", txt[m.start():m.start() + 600], re.I):
                err(f"Clip {n}: claims the footage was watched.")
            if tx is not None and inout:
                v2.window_scan(bid, n, m.group(4), inout, "PICK" + (" · LEGAL" if "legal" in notes else ""),
                               "", tx, bid)
        ph = list(CLIP_PH.finditer(txt))
        if ph:
            has_clip = True
            if stage == "videos":
                err(f"{bid}: clip placeholder left in at Stage: videos.")
            footage_front.setdefault(bid, [])
        if has_clip and prev_clip_seen and pts and not AMP.search(pts[0]):
            warn(f"{bid}: the block's first point doesn't move the story forward "
                 f"('{pts[0][1:].strip()[:50]}'). Jeff (11/11): amp up into every clip "
                 f"after the first ('And now it's spreading…').")
        if has_clip:
            prev_clip_seen = True
    if clip_nums and clip_nums != list(range(1, len(clip_nums) + 1)):
        err(f"Clips must run 1..N in air order; found {clip_nums}.")
    if not re.search(r"^/{6,}", front, re.M):
        warn("No //// break block in the front.")
    if not re.search(r"^##\s+HERE'S HOW TO PROTECT YOURSELF", front, re.M):
        warn("No '## HERE'S HOW TO PROTECT YOURSELF'.")

    if not sheet:
        return stage
    # ---- Build Sheet ----------------------------------------------------------
    for f in SPINE:
        if not re.search(rf"\*\*{re.escape(f)}:\*\*\s*\S", sheet):
            err(f"Build Sheet Spine has no '{f}:' line.")
    for h in ("Spine", "Beats", "Jeff should know", "The fix: sources", "Open calls"):
        if not re.search(rf"^##\s+{re.escape(h)}\b", sheet, re.M):
            err(f"Build Sheet has no '## {h}'.")
    if re.search(r"^##\s+Gaps\b", sheet, re.M):
        warn("Build Sheet has a '## Gaps' section. Gone since 11/10: dates and guarded facts "
             "go in Jeff should know; work still owed goes in Open calls.")
    rows, old = [], False
    for hdr, rs in v2.tables(sheet):
        if hdr[:len(BEAT_HEADER)] == BEAT_HEADER:
            rows += rs
        elif hdr[:len(BEAT_HEADER_OLD)] == BEAT_HEADER_OLD:
            old = True
            rows += [r[:4] + r[5:] for r in rs]
    if old:
        warn("Beats table has a Status column. Dropped 11/10 (producer): "
             "| Beat | Clip | Who | Tag | Adds | Search specifics |")
    if not rows:
        err("Build Sheet has no Beats table: | Beat | Clip | Who | Tag | Adds | Search specifics |")
        return stage
    jeff = sheet.split("## Jeff should know", 1)[-1].split("\n## ", 1)[0]
    opencalls = sheet.split("## Open calls", 1)[-1]
    for bid_, n_ in legal_clips:
        if not re.search(rf"\b{bid_}\b|clip\s*{n_}\b|legal", opencalls, re.I):
            warn(f"Clip {n_} has a Legal: line; put the call in Open calls too.")
    sheet_ids = [r[0] for r in rows]
    if sheet_ids != front_beats:
        missing = [b for b in front_beats if b not in sheet_ids]
        extra = [b for b in sheet_ids if b not in front_beats]
        if missing or extra:
            err(f"Front blocks and Beats rows disagree. In front only: {missing}; "
                f"in the Build Sheet only: {extra}. The front is the show; fix the sheet.")
        else:
            err(f"Beats rows are in a different order from the front: {sheet_ids} vs "
                f"{front_beats}. Reorder the sheet to match.")
    adds_seen = {}
    humans = 0
    stories = {}
    for r in rows:
        if len(r) < 6:
            err(f"Beats row {r[0]} has {len(r)} cells; it needs 6.")
            continue
        bid, clip, who, tag, adds, spec = r[:6]
        stories.setdefault(bid[0], []).append(bid)
        if not TAGS.match(tag):
            err(f"{bid}: tag '{tag}' isn't one of HAVE/FIND · ORIENTATION, DEMO, GUEST, JEFF, STILLS.")
        prob = v2.who_problem(re.sub(r"\(.*?\)|·\s*character", "", who))
        if prob:
            warn(f"{bid}: Who '{who[:50]}' is {prob}. Write the person, or the gap.")
        if v2.is_human(who):
            humans += 1
        footage = tag.startswith(("HAVE", "FIND"))
        if footage:
            dm = v2.WHO_DATE.search(who)
            if not dm:
                warn(f"{bid}: Who has no date in parentheses (Mon YYYY).")
            elif aired:
                mon = v2.MONTHS.get((dm.group(1) or "jan")[:3].lower(), 1)
                if (aired - dt.date(int(dm.group(2)), mon, 1)).days > 183 and \
                        not re.search(rf"^-\s*{bid}\b[^\n]*\b{dm.group(2)}\b", jeff, re.M):
                    warn(f"{bid}: case dated {dm.group(0)} is more than six months before the "
                         f"airdate. Start a Jeff should know line with its date "
                         f"('{bid}: <Month> {dm.group(2)}.'); the copy stays evergreen.")
            if not adds or adds == "—":
                warn(f"{bid}: no Adds (evidence, stakes or development). Jeff (11/04).")
            else:
                k = adds.split(":")[0].strip().lower() + ":" + adds.split(":", 1)[-1].strip().lower()
                if k in adds_seen:
                    warn(f"{bid}: adds the same as {adds_seen[k]} ('{adds}'). Cut one, or say what's new.")
                adds_seen[k] = bid
            if not spec or spec in ("—", "-"):
                warn(f"{bid}: no Search specifics; the pipeline searches on these (or write 'thin').")
            nums = [int(x) for x in re.findall(r"\d+", clip)]
            if stage == "videos" and nums != footage_front.get(bid, []):
                err(f"{bid}: Beats row says clip {clip}, the front block has "
                    f"{footage_front.get(bid) or 'none'}.")
        elif clip not in ("—", "-", ""):
            warn(f"{bid}: {tag} row carries clip {clip}.")
    for s_, ids in stories.items():
        lo, hi = (5, 10) if s_ == "A" else (2, 4)
        if not lo <= len(ids) <= hi:
            warn(f"Story {s_}: {len(ids)} beats (expected {lo}–{hi}).")
    if humans == 0:
        warn("No named human anywhere in Who. People, not policies.")
    fix = sheet.split("## The fix: sources", 1)[-1].split("\n## ", 1)[0]
    for line in fix.splitlines():
        t = line.strip()
        if t.startswith("- Step") and not re.search(r"\(.+\)|no source yet", t, re.I):
            warn(f"Fix source missing: '{t[:60]}'. End it with the issuing body's page, or "
                 f"say 'no source yet' and add an Open call.")
    if "do-nothing" not in fix.lower():
        warn("The fix: sources has no do-nothing test line.")
    return stage


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--stage", choices=["beats", "videos"])
    ap.add_argument("--transcripts", help="pipeline run's transcripts.json")
    a = ap.parse_args()
    tx = None
    if a.transcripts:
        with open(a.transcripts, encoding="utf-8") as fh:
            tx = json.load(fh)
    check(open(a.path, encoding="utf-8").read(), a.stage, tx)
    for e in errors:
        print(f"ERROR  {e}")
    for w in warns:
        print(f"WARN   {w}")
    if not errors and not warns:
        print("clean")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
