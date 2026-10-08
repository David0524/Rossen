#!/usr/bin/env python3
"""check_bible.py — mechanical compliance check for a Rossen Reports bible draft.

Usage:
    python3 scripts/check_bible.py draft.md                # Wednesday (default)
    python3 scripts/check_bible.py draft.md --day friday
    python3 scripts/check_bible.py draft.md --json
    python3 scripts/check_bible.py draft.md --stories 2 --stage final

--stories N  confirmed story count (default 2: A + small B). Length, clip and
             tease bands scale with it.
--stage      draft (XXX markers, blank OUT:) or final (numbered markers,
             transcribed outcue on OUT:).

Checks the numeric and structural contract stated in SKILL.md and
measurements.md. ERRORs are pipeline-breaking or hard-contract violations and
must be fixed. WARNs are calibration drift — read each one and decide.

Thresholds derive from the aired corpus; see measurements.md for provenance.
Exit codes: 0 = no errors, 1 = errors present, 2 = could not read the file.
"""

import argparse
import json
import re
import statistics
import sys

# ---------------------------------------------------------------- thresholds
T = {
    "bullet_mean": (9.5, 13.5),          # corpus mean 11.6
    "pct_le5w_max": 20.0,                # corpus 8-14%
    "pct_gt20w_max": 12.0,
    "excl_rate": (0.08, 0.20),           # aired documents 0.114-0.150
    "runway_min": 6,                     # 6-10 dash lines above a marker
    "runway_exceptions": 1,              # aired lead story has one short runway
    "first_person": (1, 3),
    "open_decisions": (2, 3),
    # Wednesday bands are per story and scale with --stories. Derived from the
    # four-story per-block rows in measurements.md; provisional until aired
    # A + B bibles are measured. Clips follow Matt's ~2 outside clips/segment.
    "wed_story": {"a_words": (600, 850), "later_words": (230, 520),
                  "tease_base": (50, 100), "tease_per": (60, 80),
                  "clips_per": 2},
    "fri": {"clips": (0, 4), "words": (600, 1100), "tease_words": (120, 300)},
    # call-in F2: no measured corpus yet, so bands are disabled
    "callin": {"clips": (0, 99), "words": (0, 99999), "tease_words": (0, 9999)},
}

BANNED = [
    "FOLKS", "CONSUMERS", "HOWEVER", "REPORTEDLY",
    "UTILIZE", "INDIVIDUALS", "FURTHERMORE", "MOREOVER", "IN CONCLUSION",
    "THE BOTTOM LINE", "HERE'S THE THING", "PURCHASE",
    # producer kit (Sept 2026): words Jeff doesn't say, per the voice profile
    "OUTRAGEOUS", "TOTALLY AMAZING", "INCREDIBLE DISCOUNTS", "FUNCTIONALLY",
    "DISCREPANCIES", "FLUCTUATIONS", "ADDITIONALLY", "UNACCEPTABLE",
    "WE WILL DEMONSTRATE", "JUST WATCH", "TAKE A LOOK", "HAVE A LOOK",
]

# Softer: he rarely says these; usually a "you" or "right now" fix. WARN only.
SOFT = ["CUSTOMERS", "SHOPPERS", "LISTENERS", "RECENTLY", "CURRENTLY"]

# Legal words: off-voice, but sometimes required (arrested-not-convicted, a
# source that says "alleged"). WARN, never ERROR — the legal note wins.
LEGAL = ["ALLEGED", "ALLEGEDLY"]

HEADER_VERBS = (r"IS|ARE|WAS|WERE|BE|BEEN|GOT|GET|GETS|DID|DO|DOES|HAS|HAVE|HAD|"
    r"WILL|WOULD|CAN|COULD|WANT|WANTS|SAYS|SAY|SAID|TOOK|TAKE|TAKES|TAKING|MADE|"
    r"MAKE|MAKES|WATCH|WAIT|THINK|LOOK|SEE|SAW|COME|COMES|CAME|COMING|HAPPEN|"
    r"HAPPENS|HAPPENED|HAPPENING|STEAL|STEALS|STOLE|STEALING|DRAIN|DRAINS|FOUND|"
    r"FIND|FINDS|PAY|PAYS|PAID|KNOW|KNOWS|KNEW|BOUGHT|BUY|BUYING|LOST|LOSE|LOSES|"
    r"LOSING|CUT|CUTS|CUTTING|DOING|WORK|WORKS|WORKED|GIVE|GIVES|GAVE|PUT|PUTS|GO|"
    r"GOES|GOING|WENT|TRY|TRIES|TRYING|TELL|TELLS|TOLD|KEEP|KEEPS|MOVE|MOVES|"
    r"START|STARTS|STARTED|SHOW|SHOWS|SHOWED|HIT|HITS|NEED|NEEDS|BELIEVE|HEAR|"
    r"LISTEN|SPOT|PROTECT|CALL|CALLS|CALLED|SEND|SENDS|SENT|SELL|SELLS|SOLD|"
    r"TARGET|TARGETS|EXPLODING|HUG|HUGS|GRAB|GRABS|SPY|SPYING|TRACK|TRACKING|"
    r"BECOME|BECOMES|LEFT|LEAVE|USE|USES|USING|TRICK|TRICKS|SCAM|SCAMS|SCAMMED|"
    r"IT'S|HE'S|SHE'S|THEY'RE|YOU'RE|WE'RE|HERE'S|THAT'S|WHAT'S|THERE'S|WHO'S|"
    r"ISN'T|AREN'T|DON'T|DOESN'T|WON'T|CAN'T")

ESCALATORS = ["BUT", "EVEN", "NOW", "WORSE", "THINK THAT", "SHOCKING", "MOST",
              "NEXT", "WAIT", "GUESS", "NEVER", "EXPLODING", "FINALLY"]

CLIP_STRICT = {
    "draft": re.compile(r"^\(\(\(PLAY CLIP XXX (HORIZONTAL|VERTICAL)( BROLL)?\)\)\)$"),
    "final": re.compile(r"^\(\(\(PLAY CLIP (\d+) (HORIZONTAL|VERTICAL)( BROLL)?\)\)\)$"),
}
SOURCE_LINE = re.compile(r"^\(\(\(\[[^\]]+\]\(https?://")
URLISH = re.compile(r"https?://|www\.|\b\d{1,2}:\d{2}\b|CLIP CONTEXT", re.I)
CLIP_LOOSE = re.compile(r"\(+\s*PLAY CLIP")
CUE_ANY = re.compile(r"\(\(+[^)]")
PROTECTION_HEADER = "HERE'S HOW TO PROTECT YOURSELF"


# ---------------------------------------------------------------- promises & tells
# Ryan (producer notes on the 10/14 bible, Oct 8 2026): a promise made in the
# tease ("THE ONE MOVE", "THE 5-SECOND HABIT") has to be paid off BY NAME in the
# body, and viewers get a takeaway after each case, not only at the end.
PROMISE_NOUNS = (r"PIECE OF PAPER|QUESTION|HABIT|MOVE|TRICK|THING|WORD|PHRASE|"
                 r"SETTING|CALL|STEP|RULE|MISTAKE|SIGN|BUTTON|NUMBER|TELL")
PROMISE_RE = re.compile(
    r"\b((?:ONE|\d+|ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE|TEN)"
    r"(?:[- ](?:SECOND|MINUTE|WORD|STEP))?\s+(?:[A-Z']+\s+){0,2}?(?:"
    + PROMISE_NOUNS + r"))\b")
NUMWORDS = {"1": "ONE", "2": "TWO", "3": "THREE", "4": "FOUR", "5": "FIVE",
            "6": "SIX", "7": "SEVEN", "8": "EIGHT", "9": "NINE", "10": "TEN"}
# a takeaway the viewer can use: a labeled tell, a red flag, or the list itself
TAKEAWAY_RE = re.compile(r"\bTHE TELL\b|\bTHE RED FLAG\b|HERE'?S HOW TO PROTECT|"
                         r"^-?\s*NUMBER ONE\b")


def norm_phrase(s):
    s = re.sub(r"\*+", "", s).upper().replace("\u2019", "'")
    s = re.sub(r"\b(\d+)\b", lambda m: NUMWORDS.get(m.group(1), m.group(1)), s)
    s = re.sub(r"[^A-Z0-9' ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def tease_promises(tease_lines):
    """Promise phrases in the tease, e.g. 'ONE MOVE', 'FIVE SECOND HABIT'."""
    out = []
    for l in tease_lines:
        for m in PROMISE_RE.finditer(norm_phrase(l)):
            p = m.group(1)
            if p not in out:
                out.append(p)
    return out


def unpaid_promises(tease_lines, body_lines):
    body = " " + norm_phrase(" \n ".join(body_lines)) + " "
    return [p for p in tease_promises(tease_lines) if f" {p} " not in body]


def takeaway_gaps(body_lines, clip_re, limit=3):
    """Runs of `limit`+ sound clips with no takeaway line between them.
    Expert cue lines do not count: the tell is Jeff's, not the guest's."""
    gaps, run, start = [], 0, None
    for i, l in enumerate(body_lines):
        s = re.sub(r"\*+", "", l).replace("\u2019", "'").strip().upper()
        if clip_re.search(s):
            if "BROLL" in s:
                continue
            if run == 0:
                start = i
            run += 1
            if run == limit:
                gaps.append(start)
        elif (not s.startswith(("(", "OUT:")) and not s.rstrip("!").endswith("?")
              and TAKEAWAY_RE.search(s)):
            run = 0
    return gaps


def strip_md(s):
    return re.sub(r"\*+", "", s).replace("\u2019", "'").strip()


def words(s):
    return len(re.findall(r"[A-Za-z0-9$%'.\-]+", s))


class Report:
    def __init__(self):
        self.errors = []
        self.warns = []
        self.stats = {}

    def err(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warns.append(msg)


def check(path, day="wednesday", stories=2, stage="draft"):
    r = Report()
    try:
        with open(path, encoding="utf-8") as fh:
            raw = fh.read()
    except OSError as exc:
        print(f"could not read {path}: {exc}", file=sys.stderr)
        sys.exit(2)

    lines = [l.rstrip() for l in raw.split("\n")]
    if day == "callin":
        band = T["callin"]
    elif day.startswith("w"):
        w = T["wed_story"]
        n = max(1, stories)
        band = {
            "clips": (max(1, n - 1), w["clips_per"] * n + 2),
            "words": (w["a_words"][0] + w["later_words"][0] * (n - 1),
                      w["a_words"][1] + w["later_words"][1] * (n - 1)),
            "tease_words": (w["tease_base"][0] + w["tease_per"][0] * n,
                            w["tease_base"][1] + w["tease_per"][1] * n),
        }
    else:
        band = T["fri"]
    r.stats["stage"] = stage
    r.stats["stories"] = stories

    # ---------------------------------------------------- tease boundary
    boundary = None
    for i, l in enumerate(lines):
        u = strip_md(l).upper().lstrip("- ")
        if u.startswith("HIT LIKE AND SUBSCRIBE") or u.startswith("JOIN THE CHAT"):
            boundary = i
            break
    if boundary is None:
        r.err("no tease boundary: needs HIT LIKE AND SUBSCRIBE / JOIN THE CHAT "
              "to close the tease block. The pipeline drops everything above it, "
              "so without it the whole tease is parsed as body.")
        boundary = 0
    tease, body = lines[:boundary], lines[boundary:]
    r.stats["tease_boundary_line"] = boundary

    # ---------------------------------------------------- clip markers
    clips = []
    for i, l in enumerate(lines):
        s = strip_md(l)
        if CLIP_LOOSE.search(s.upper()):
            clips.append(i)
            if not CLIP_STRICT[stage].match(s.upper()):
                form = ("(((PLAY CLIP XXX HORIZONTAL)))" if stage == "draft"
                        else "(((PLAY CLIP 1 HORIZONTAL))), numbered")
                r.err(f"line {i+1}: malformed {stage.upper()} clip marker {s!r} — "
                      f"must be exactly {form}, three parens each side, "
                      f"orientation present, optional ' BROLL' before the close.")
    r.stats["clip_beats"] = len(clips)
    if stage == "final":
        nums = []
        for i in clips:
            m = CLIP_STRICT["final"].match(strip_md(lines[i]).upper())
            if m:
                nums.append(int(m.group(1)))
        if nums and nums != list(range(1, len(nums) + 1)):
            r.err(f"FINAL clip numbers run {nums}; must be 1..{len(nums)} in "
                  f"document order, no gaps or repeats.")

    for i in clips:
        nxt = [x for x in lines[i + 1:i + 6] if strip_md(x)][:2]
        is_broll = "BROLL" in strip_md(lines[i]).upper()
        if not nxt or not strip_md(nxt[0]).upper().startswith("OUT:"):
            r.err(f"line {i+1}: clip marker has no OUT: line beneath it.")
            continue
        filled = strip_md(nxt[0]).upper().replace(" ", "") != "OUT:"
        # FINAL carries one red source line under OUT: (producer, 10/14):
        # ((([Outlet](URL) · in - out (OUTCUE) · BUTT · ...)))
        src = (strip_md(nxt[1]) if len(nxt) > 1
               and SOURCE_LINE.match(strip_md(nxt[1])) else None)
        if stage == "draft" and filled:
            r.err(f"line {i+1}: OUT: line is filled ({strip_md(nxt[0])!r}) in a "
                  f"DRAFT. Leave it blank, or check with --stage final.")
        if stage == "final" and not filled and not is_broll:
            if src and not re.search(r"\b\d{1,2}:\d{2}\b", src):
                r.warn(f"line {i+1}: blank OUT: on a MANUAL clip (link, no "
                       f"timecodes). Fill it once someone pulls the clip.")
            else:
                r.err(f"line {i+1}: FINAL clip has a blank OUT:. Carry the "
                      f"transcribed outcue from the outline.")
        if stage == "final" and not src:
            r.warn(f"line {i+1}: FINAL clip has no red source line under OUT:. "
                   f"Copy the outline's Videos row: ((([Outlet](URL) · in - out "
                   f"(OUTCUE))))")
        if len(nxt) > 1 and URLISH.search(strip_md(nxt[1])) and not (
                stage == "final" and src):
            r.err(f"line {i+1}: URL, timecode or clip-context text under the "
                  f"marker ({strip_md(nxt[1])[:60]!r}). In a DRAFT it belongs in "
                  f"the source log; in a FINAL only the one red source line "
                  f"goes here.")

    for l in tease:
        if CLIP_LOOSE.search(strip_md(l).upper()):
            r.err(f"PLAY CLIP marker inside the tease block: {strip_md(l)!r}. "
                  f"Produces an unresolvable duplicate beat.")
    for i, l in enumerate(lines):
        if re.search(r"TEASE\s*(//|-)\s*(SPONSOR|CHAPTER)", strip_md(l).upper()):
            for j in range(i + 1, min(i + 8, len(lines))):
                if CLIP_LOOSE.search(strip_md(lines[j]).upper()):
                    r.err(f"line {j+1}: PLAY CLIP marker inside a sponsor "
                          f"tease block.")

    lo, hi = band["clips"]
    if not lo <= len(clips) <= hi:
        r.warn(f"{len(clips)} clip beats; {day} bands at {lo}-{hi}. If the "
               f"supplied material genuinely does not carry more, flag the "
               f"deficit as a producer cue rather than inventing footage.")

    # ---------------------------------------------------- runways
    runways = []
    for i in clips:
        n, j = 0, i - 1
        while j >= 0:
            s = strip_md(lines[j])
            if not s:
                j -= 1
                continue
            if re.match(r"^-\s*\S", s):
                n += 1
                j -= 1
            elif s.upper() == s and not CUE_ANY.search(s):
                n += 1          # a bare all-caps line counts toward the runway
                break
            else:
                break
        runways.append(n)
    r.stats["runway_depths"] = runways
    short = [(clips[k] + 1, n) for k, n in enumerate(runways) if n < T["runway_min"]]
    if len(short) > T["runway_exceptions"]:
        for ln, n in short:
            r.err(f"line {ln}: runway is {n} lines, needs {T['runway_min']}-10. "
                  f"The setup names the person and plants the question the "
                  f"clip answers.")
    elif short:
        r.warn(f"line {short[0][0]}: short runway ({short[0][1]} lines). One is "
               f"within aired tolerance; a second is not.")

    # ---------------------------------------------------- lead-in repetition
    leadins = []
    for i in clips:
        prev = [strip_md(x) for x in lines[:i] if strip_md(x)]
        if prev:
            leadins.append(re.sub(r"^-\s*", "", prev[-1]).upper().rstrip(".!? "))
    counts = {}
    for l in leadins:
        counts[l] = counts.get(l, 0) + 1
    for phrase, n in counts.items():
        if n > 2:
            r.err(f"lead-in {phrase!r} used {n} times; cap is 2. An "
                  f"interchangeable setup does no work.")
        elif n == 2 and "WHAT WE KNOW RIGHT NOW" not in phrase:
            r.warn(f"lead-in {phrase!r} used twice — check both earn it.")

    # ---------------------------------------------------- bullets / syntax
    bullets = [re.sub(r"^-\s*", "", strip_md(l)) for l in body
               if re.match(r"^-\s*\S", strip_md(l)) and not CUE_ANY.search(strip_md(l))]
    wc = [words(b) for b in bullets]
    r.stats["body_bullets"] = len(bullets)
    if wc:
        mean = round(statistics.mean(wc), 1)
        r.stats["bullet_mean_words"] = mean
        r.stats["bullet_median_words"] = statistics.median(wc)
        pct5 = round(100 * sum(1 for w in wc if w <= 5) / len(wc), 1)
        pct20 = round(100 * sum(1 for w in wc if w > 20) / len(wc), 1)
        r.stats["pct_bullets_le5w"] = pct5
        r.stats["pct_bullets_gt20w"] = pct20
        blo, bhi = T["bullet_mean"]
        if mean < blo:
            r.err(f"bullet mean {mean} words, corpus is 11.6 (band {blo}-{bhi}). "
                  f"Over-fragmenting — reads punchy, delivers nothing.")
        elif mean > bhi:
            r.err(f"bullet mean {mean} words, corpus is 11.6 (band {blo}-{bhi}). "
                  f"Lines are being written to be read, not said.")
        if pct5 > T["pct_le5w_max"]:
            r.warn(f"{pct5}% of bullets are 5 words or shorter; corpus 8-14%.")
        if pct20 > T["pct_gt20w_max"]:
            r.warn(f"{pct20}% of bullets run over 20 words. Look for appositive "
                   f"inventories — split them, one idea per line.")

    spoken = [strip_md(l) for l in body if strip_md(l)
              and not CUE_ANY.search(strip_md(l))
              and not strip_md(l).upper().startswith("OUT:")]
    sw = sum(words(s) for s in spoken)
    tw = sum(words(strip_md(l)) for l in tease)
    r.stats["body_spoken_words"] = sw
    r.stats["tease_words"] = tw
    lo, hi = band["words"]
    if not lo <= sw <= hi:
        r.warn(f"{sw} spoken body words; {day} bands at {lo}-{hi}.")
    lo, hi = band["tease_words"]
    if tw and not lo <= tw <= hi:
        r.warn(f"tease block is {tw} words; bands at {lo}-{hi}.")

    # ---------------------------------------------------- prosody
    excl = sum(1 for s in spoken if "!" in s)
    rate = round(excl / max(len(spoken), 1), 3)
    r.stats["excl_line_rate"] = rate
    elo, ehi = T["excl_rate"]
    if rate < elo:
        r.err(f"exclamation-line rate {rate}; aired documents run {elo}-{ehi}. "
              f"The draft is flat — it gives Jeff no direction about where to "
              f"push. Mark intensity, do not add words.")
    elif rate > ehi:
        r.warn(f"exclamation-line rate {rate} is above the aired range "
               f"({elo}-{ehi}) — everything shouting is the same as nothing.")

    r.stats["triple_q"] = len(re.findall(r"\?\?\?", raw))
    if r.stats["triple_q"] == 0 and clips:
        r.warn("no ??? anywhere. Aired documents carry 0-2, usually on the "
               "question that hands off to a clip. Optional, but check whether "
               "a handoff wants one.")
    bold = len(re.findall(r"\*\*[^*\n]{2,70}\*\*", raw))
    r.stats["inline_bold_runs"] = bold
    if clips and bold < 3 * max(1, len(clips) // 4):
        r.warn(f"only {bold} bold runs. Aired stories mark several words per "
               f"story to hit.")

    # ---------------------------------------------------- register
    U = raw.upper()
    legal = {w: len(re.findall(r"\b" + re.escape(w) + r"\b", U))
             for w in LEGAL if re.search(r"\b" + re.escape(w) + r"\b", U)}
    for w, n in legal.items():
        r.warn(f"{w!r} x{n}: off-voice, but keep it where a legal note requires "
               f"it (arrested, not convicted; a source that says alleged). "
               f"Otherwise hedge by attribution: POLICE SAY.")
    hits = {w: len(re.findall(r"\b" + re.escape(w) + r"\b", U))
            for w in BANNED if re.search(r"\b" + re.escape(w) + r"\b", U)}
    r.stats["banned_words"] = hits
    for w, n in hits.items():
        r.err(f"banned register: {w!r} x{n}. He essentially never says it; "
              f"see the negative-space table in measurements.md.")
    soft = {w: len(re.findall(r"\b" + re.escape(w) + r"\b", U))
            for w in SOFT if re.search(r"\b" + re.escape(w) + r"\b", U)}
    for w, n in soft.items():
        r.warn(f"{w!r} x{n}: Jeff says 'you' / 'viewers' / 'right now'. Check "
               f"each use.")

    # ---------------------------------------------------- clip in / clip out
    # Producer kit: every clip goes in on a cue plus a verdict and comes out
    # on a one-line button. BUTT between segments of one source is exempt.
    CUE = re.compile(r"\b(WATCH THIS|CHECK THIS OUT|ROLL CLIP|WATCH CLIP|LISTEN|"
                     r"HERE YOU CAN SEE|WATCH WHAT|WATCH HIM|WATCH HER|"
                     r"HERE'S HOW IT HAPPENED|THIS IS (CRAZY|NUTS|SICK|INSANE|WILD))")
    no_cue, no_button = [], []
    for i in clips:
        above = [strip_md(x) for x in lines[max(0, i - 3):i] if strip_md(x)]
        if not any(CUE.search(x.upper()) for x in above):
            no_cue.append(i + 1)
        nxt_raw = ""
        for x in lines[i + 1:i + 8]:
            t = strip_md(x)
            if not t or t.upper().startswith("OUT:"):
                continue
            nxt_raw = x.strip()
            break
        nxt = strip_md(nxt_raw).upper()
        is_header = nxt_raw.startswith("**") and nxt == nxt.upper() and not nxt.startswith("-")
        if nxt.startswith("BUTT"):
            continue
        if not nxt or CLIP_LOOSE.search(nxt) or (is_header and not nxt.startswith("-")):
            no_button.append(i + 1)
    if no_cue:
        r.warn(f"{len(no_cue)} clip(s) with no cue + verdict in the last lines of "
               f"the runway ('WATCH THIS. THIS IS CRAZY.'), lines {no_cue[:6]}.")
    if no_button:
        r.warn(f"{len(no_button)} clip(s) not followed by a one-line button "
               f"(clip-to-clip or clip-to-header), lines {no_button[:6]}.")

    # ---------------------------------------------------- headers
    heads = []
    for l in body:
        if l.strip().startswith("**") and not CUE_ANY.search(l):
            s = strip_md(l)
            if (s and s.upper() == s and not s.startswith("-")
                    and not s.upper().startswith("OUT:") and words(s) <= 16):
                heads.append(s)
    mid = [h for h in heads if PROTECTION_HEADER not in h.upper()
           and "ALWAYS LOOKING FOR WAYS" not in h.upper()]
    r.stats["mid_story_headers"] = mid
    flat = [h for h in mid
            if not (h.endswith("!") or h.endswith("?")
                    or any(h.upper().startswith(e) or f" {e}" in h.upper()
                           for e in ESCALATORS))]
    if mid and len(flat) > len(mid) // 2:
        r.warn(f"{len(flat)} of {len(mid)} mid-story headers carry no "
               f"escalation marker — check they are sayable turns and not "
               f"article subheads: {flat[:3]}")
    for h in mid:
        if not re.search(r"(?<![A-Z'])(" + HEADER_VERBS + r")(?![A-Z'])", h.upper()):
            r.warn(f"header {h!r} has no verb — a noun phrase is almost always "
                   f"a label. Rewrite it as a line Jeff can say.")

    # ---------------------------------------------------- graphics
    g = len(re.findall(r"CREATE FULL SCREEN GRAPHIC", U))
    fs = len(re.findall(r"TAKE FULLSCREEN", U))
    r.stats["fullscreen_graphics"] = g
    r.stats["take_fullscreen"] = fs
    if g > 2:
        r.warn(f"{g} graphic cards. Threat stories run 0-1; only a list-shaped "
               f"story (what-to-buy, price limits, a click path) earns 3-4, and "
               f"the aired precedent for that is 06/22 story 4. Confirm this is "
               f"that case.")

    # ---------------------------------------------------- first person
    fp = [s for s in spoken
          if re.search(r"(^|[^A-Z])I('M|'VE|'D|'LL)?([^A-Z]|$)", s)
          and not re.search(r'"', s)]
    r.stats["first_person_lines"] = fp
    lo, hi = T["first_person"]
    if len(fp) > hi:
        r.warn(f"{len(fp)} first-person lines; cap is {hi}. Check none is "
               f"editorial opinion, and that nothing about Jeff's life, habits "
               f"or accounts was invented.")

    # ---------------------------------------------------- open decisions
    od = len([l for l in lines
              if re.match(r"^\**\(\(\((DECIDE|JEFF|PRODUCER)", strip_md(l).upper())])
    r.stats["open_decisions"] = od
    lo, hi = T["open_decisions"]
    if od < lo:
        r.warn(f"{od} open decisions; carry {lo}-{hi}. A draft that answers "
               f"every question quietly makes calls that belong to Jeff or the "
               f"producer.")

    # ---------------------------------------------------- producer cuts (10/14)
    # Learned from the 10/14 bible as the producer sent it. WARN only: the
    # producer makes the rare exception.
    OUTLETS = re.compile(
        r"\b(CBS|NBC|ABC|FOX|CNN|MSNBC|PBS|NPR|INSIDE EDITION|GOOD MORNING "
        r"AMERICA|TODAY SHOW|DATELINE|20/20|60 MINUTES|NEW YORK POST|NY POST|"
        r"USA TODAY|WASHINGTON POST|NEW YORK TIMES|WALL STREET JOURNAL|"
        r"ASSOCIATED PRESS|REUTERS|INVESTIGATETV|ABC\d+|[KW][A-Z]{2,3} NEWS|[KW][A-Z]{3} ?\d+|"
        r"[KW][A-Z]{2,3}'S (REPORTING|STORY|INVESTIGATION))\b")
    outlet_hits = [s for s in spoken if OUTLETS.search(s.upper())
                   and not s.upper().startswith("(")]
    r.stats["outlet_mentions"] = len(outlet_hits)
    if outlet_hits:
        r.warn(f"{len(outlet_hits)} spoken line(s) name a news outlet. No outlet "
               f"names on air except the rare one the producer chooses: say "
               f"'THIS REPORTER', 'REPORTERS', 'THE NEWS', or attribute to the "
               f"police, court or agency. {outlet_hits[:3]}")
    fam = [s for s in spoken if re.search(
        r"\b(YOUR (AGING |ELDERLY )?PARENTS?|YOUR MOM AND DAD|A PARENT WITH|"
        r"YOUR GRANDPARENTS?)\b", s.upper())]
    if fam:
        r.warn(f"{len(fam)} line(s) address the viewer as someone's grown child "
               f"({fam[:2]}). The audience is 55+: say 'YOUR FAMILY' or 'LOVED "
               f"ONES'.")
    if any(re.match(r"^-?\s*WELCOME TO ROSSEN REPORTS", strip_md(l).upper())
           for l in tease):
        r.warn("the slate is written in. Jeff says it himself: open the "
               "document on the command hook.")
    t_heads = {strip_md(l).upper().rstrip("!. ") for l in tease
               if l.strip().startswith("**") and strip_md(l)
               and not set(strip_md(l)) <= set("—-")}
    reused = [h for h in heads if h.upper().rstrip("!. ") in t_heads]
    if reused:
        r.warn(f"body header repeats the tease headline: {reused[:2]}. Open "
               f"each story on a new line that puts the viewer in the moment.")

    # ---------------------------------------------------- Ryan's retention rules (10/9)
    # references/examples/ryan-notes-2026-10-09.md. WARN only.
    EXCLUDE = re.compile(
        r"(YOU'RE NOT LOSING|DOESN'T APPLY TO YOU|DOES NOT APPLY TO YOU|"
        r"YOU'RE (FINE|SAFE|IN THE CLEAR|OFF THE HOOK)\b|NOTHING TO WORRY ABOUT|"
        r"YOU CAN RELAX|IF YOU HAVE ONE\b.*LISTEN UP|THIS ISN'T ABOUT YOU|"
        r"YOU'RE NOT AFFECTED)")
    excl = [s for s in spoken if EXCLUDE.search(s.upper())]
    if excl:
        r.warn(f"{len(excl)} line(s) may hand viewers a reason to leave "
               f"({excl[:2]}). Keep the fact, flip the conclusion: say why they "
               f"should stay (Ryan note 2).")
    LABEL = re.compile(
        r"^-?\s*(SCAM NUMBER (ONE|TWO|THREE|FOUR|FIVE|\d)\b|HERE ARE THE "
        r"(TWO|THREE|FOUR|FIVE|\d+) |.*\bSCARIEST (ONE |SCAM )?OF (THEM )?ALL)")
    labels = [s for s in spoken if LABEL.search(s.upper())]
    if labels:
        r.warn(f"{len(labels)} segment opener(s) read as labels ({labels[:2]}). "
               f"Open on the hook: the moment the viewer meets it and why it's "
               f"worse than the last one (Ryan note 4).")
    for i, l in enumerate(lines):
        if "QR" in l.upper() and l.strip().startswith(("(", "**(")):
            before = " ".join(strip_md(x).upper() for x in lines[max(0, i - 8):i])
            if not re.search(r"\b(OURS|OUR CODE|WE PUT|WE'RE PUTTING|THIS ONE IS "
                             r"OURS|YOU'RE WATCHING US)\b", before):
                r.warn(f"QR cue at line {i + 1} has no trust line before it. "
                       f"After telling viewers not to trust codes, say this one "
                       f"is ours and they watched us put it up (Ryan note 9).")
            break
    GENERIC = re.compile(r"\b(STICK AROUND|STAY WITH US|DON'T GO ANYWHERE|"
                         r"MUCH MORE|COMING UP|STAY TUNED)\b")
    for i, l in enumerate(lines):
        if "BUT FIRST, A QUICK WORD" in strip_md(l).upper():
            prev = [strip_md(x) for x in lines[max(0, i - 8):i]
                    if strip_md(x) and not strip_md(x).startswith("(")][-3:]
            txt = " ".join(prev).upper()
            if not prev or GENERIC.search(txt) or words(txt) < 8:
                r.warn(f"the tease before the sponsor at line {i + 1} doesn't "
                       f"name what's ahead. Name two or three specific payoffs "
                       f"(Ryan note 7): {prev[-1:] }")
    # an action line is a command: the verb opens a sentence
    ACTION = re.compile(r"(^-?\s*|[.!?…]\s+)(CALL|REPORT|HANG UP|CHECK|LOOK (AT|FOR|UP)|"
                        r"DON'T|NEVER|OPEN|ASK|FREEZE|DISPUTE|TYPE|SKIP|DELETE|"
                        r"BLOCK|SIGN UP|WATCH THE|SNAP|READ|NUMBER (ONE|TWO|THREE))\b")
    for i, l in enumerate(lines):
        if "BUT FIRST, A QUICK WORD" not in strip_md(l).upper():
            continue
        j = max((k for k in range(i) if strip_md(lines[k]).upper().startswith("OUT:")),
                default=None)
        if j is None:
            continue
        TEASE_LINE = re.compile(r"(\?$|RIGHT AFTER THIS|WHEN WE COME BACK|"
                                r"^-?\s*NEXT\b|COMING UP|AFTER THE BREAK|JOINS ME)")
        seg = [strip_md(x) for x in lines[j + 1:i]
               if strip_md(x) and not CUE_ANY.search(strip_md(x))
               and not TEASE_LINE.search(strip_md(x).upper().rstrip("!. "))]
        if seg and not any(ACTION.search(x.upper()) for x in seg):
            r.warn(f"the segment before the sponsor at line {i + 1} ends with no "
                   f"'what to do' line after its last clip. Resolve it before the "
                   f"bridge: the tell plus one action (Ryan note 6).")
    end_i = next((i for i, l in enumerate(lines)
                  if strip_md(l).upper().lstrip("- ").startswith("END OF SHOW")),
                 len(lines))
    # Friday: the close ends the content half, before the deals handoff
    tail = " ".join(strip_md(x).upper() for x in
                    (body if day.startswith("f") else lines[max(0, end_i - 14):end_i]))
    if not re.search(r"\b(SEND THIS|SHARE THIS|SEE YOU NEXT TIME)\b", tail):
        r.warn("no written close before END OF SHOW. Three short beats: send "
               "this to someone it protects, the next video, see you next time "
               "(Ryan note 11).")
    if day.startswith("f"):
        early = [strip_md(x).upper() for x in body[:max(40, len(body) // 3)]]
        if not any("ON SCREEN" in x and "?" in x for x in early):
            r.warn("no on-screen chat question after JOIN THE CHAT. Add one "
                   "specific question as a red cue (Ryan note 11).")

    # ---------------------------------------------------- protection headers
    if PROTECTION_HEADER.replace("'", "") not in U.replace("'", ""):
        r.warn("no HERE'S HOW TO PROTECT YOURSELF section found.")

    # ---------------------------------------------------- tease promises
    promised = tease_promises(tease)
    r.stats["tease_promises"] = promised
    for p in unpaid_promises(tease, body):
        r.err(f"the tease promises {p!r} but the body never names it. Pay it "
              f"off by name where it lands (-HERE'S THE {p} I PROMISED: ...), "
              f"or cut it from the tease.")

    # ---------------------------------------------------- takeaways per case
    gaps = takeaway_gaps(body, CLIP_LOOSE)
    r.stats["takeaway_gaps"] = len(gaps)
    for g in gaps:
        r.warn(f"line {boundary + g + 1}: three sound clips run with no takeaway "
               f"between them. Each victim case ends with a one-line tell "
               f"(-HERE'S THE TELL: ...) before the next case starts.")

    # ---------------------------------------------------- aphorism candidates
    aph = []
    for s in spoken:
        if s.startswith("-") or s.startswith("**"):
            body_txt = re.sub(r"^-\s*", "", s)
        else:
            body_txt = s
        # ellipses are breath marks, not sentence ends — collapse them first
        flat_txt = re.sub(r"\.\.\.+|\u2026", " ", body_txt)
        sents = [x for x in re.split(r"(?<=[.!?])\s+", flat_txt.strip()) if x]
        bt = body_txt.upper()
        # cue + verdict, numbered tips, repeated killer numbers and
        # on-screen callouts are house patterns, not built aphorisms
        if (re.match(r"^(WATCH THIS|CHECK THIS OUT|ROLL CLIP|NUMBER (ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN))", bt)
                or "THERE IT IS ON THE SCREEN" in bt or "BIG DEAL" in bt):
            continue
        if len(sents) >= 2 and words(body_txt) <= 16 and all(words(x) <= 8 for x in sents):
            aph.append(body_txt)
    r.stats["aphorism_candidates"] = aph
    if aph:
        r.warn(f"{len(aph)} possible constructed aphorism(s) — read each one. "
               f"Would it still do its job if Jeff said it a different way? "
               f"If no, cut it: {aph[:3]}")

    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--day", default="wednesday",
                    choices=["wednesday", "friday", "callin"])
    ap.add_argument("--stories", type=int, default=2,
                    help="confirmed story count (Wednesday bands scale with it)")
    ap.add_argument("--stage", default="draft", choices=["draft", "final"])
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    r = check(a.path, a.day, a.stories, a.stage)

    if a.json:
        print(json.dumps({"errors": r.errors, "warnings": r.warns,
                          "stats": r.stats}, indent=1, ensure_ascii=False))
    else:
        print(f"\n{a.path}  ({a.day})")
        print("=" * 68)
        for k, v in r.stats.items():
            if k not in ("mid_story_headers", "first_person_lines",
                         "aphorism_candidates", "banned_words"):
                print(f"  {k:24} {v}")
        print()
        if r.errors:
            print(f"ERRORS ({len(r.errors)}) — must fix:")
            for e in r.errors:
                print(f"  x {e}")
            print()
        if r.warns:
            print(f"WARNINGS ({len(r.warns)}) — read and decide:")
            for w in r.warns:
                print(f"  ! {w}")
            print()
        if not r.errors and not r.warns:
            print("clean.\n")
        elif not r.errors:
            print("no errors.\n")

    sys.exit(1 if r.errors else 0)


if __name__ == "__main__":
    main()
