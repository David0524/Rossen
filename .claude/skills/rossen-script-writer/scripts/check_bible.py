#!/usr/bin/env python3
"""check_bible.py — mechanical compliance check for a Rossen Reports bible draft.

Usage:
    python3 scripts/check_bible.py draft.md                # Wednesday (default)
    python3 scripts/check_bible.py draft.md --day friday
    python3 scripts/check_bible.py draft.md --json

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
    "wed": {"clips": (10, 12), "words": (1700, 2300), "tease_words": (210, 340)},
    "fri": {"clips": (0, 4), "words": (600, 1100), "tease_words": (120, 300)},
}

BANNED = [
    "FOLKS", "CONSUMERS", "HOWEVER", "ALLEGEDLY", "REPORTEDLY", "ALLEGED",
    "UTILIZE", "INDIVIDUALS", "FURTHERMORE", "MOREOVER", "IN CONCLUSION",
    "THE BOTTOM LINE", "HERE'S THE THING", "PURCHASE",
]

ESCALATORS = ["BUT", "EVEN", "NOW", "WORSE", "THINK THAT", "SHOCKING", "MOST",
              "NEXT", "WAIT", "GUESS", "NEVER", "EXPLODING", "FINALLY"]

CLIP_STRICT = re.compile(r"^\(\(\(PLAY CLIP XXX (HORIZONTAL|VERTICAL)"
                         r"( BROLL)?\)\)\)$")
CLIP_LOOSE = re.compile(r"\(+\s*PLAY CLIP")
CUE_ANY = re.compile(r"\(\(+[^)]")
PROTECTION_HEADER = "HERE'S HOW TO PROTECT YOURSELF"


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


def check(path, day="wednesday"):
    r = Report()
    try:
        with open(path, encoding="utf-8") as fh:
            raw = fh.read()
    except OSError as exc:
        print(f"could not read {path}: {exc}", file=sys.stderr)
        sys.exit(2)

    lines = [l.rstrip() for l in raw.split("\n")]
    band = T["wed"] if day.startswith("w") else T["fri"]

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
            if not CLIP_STRICT.match(s.upper()):
                r.err(f"line {i+1}: malformed clip marker {s!r} — must be "
                      f"exactly (((PLAY CLIP XXX HORIZONTAL))) or "
                      f"(((PLAY CLIP XXX VERTICAL))), three parens each side, "
                      f"XXX literal, optional ' BROLL' before the close.")
    r.stats["clip_beats"] = len(clips)

    for i in clips:
        nxt = [x for x in lines[i + 1:i + 4] if strip_md(x)]
        if not nxt or not strip_md(nxt[0]).upper().startswith("OUT:"):
            r.err(f"line {i+1}: clip marker has no OUT: line beneath it.")
        elif strip_md(nxt[0]).upper().replace(" ", "") != "OUT:":
            r.err(f"line {i+1}: OUT: line is pre-filled ({strip_md(nxt[0])!r}). "
                  f"Leave it blank — the pipeline fills it.")

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
                  f"The setup lines are the only thing the pipeline reads to "
                  f"decide what footage to find.")
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
    hits = {w: len(re.findall(r"\b" + re.escape(w) + r"\b", U))
            for w in BANNED if re.search(r"\b" + re.escape(w) + r"\b", U)}
    r.stats["banned_words"] = hits
    for w, n in hits.items():
        r.err(f"banned register: {w!r} x{n}. He essentially never says it; "
              f"see the negative-space table in measurements.md.")
    if re.search(r"\bWATCH THIS\b", U):
        r.err("'WATCH THIS' is Jeff's live handoff, spoken the instant before a "
              "clip rolls. Never write it.")

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
        if not re.search(r"\b(IS|ARE|WAS|WERE|GOT|GETS|DID|DOES|HAS|HAVE|WILL|"
                         r"CAN|WANT|SAYS|SAID|TOOK|TAKES|MADE|MAKES|WATCH|WAIT|"
                         r"THINK|LOOK|SEE|COMES|CAME|HAPPEN|HAPPENED|STEAL|"
                         r"STEALING|DRAIN|FOUND|FIND|PAY|PAID|KNOW|BOUGHT|"
                         r"BUYING|LOST|LOSES|CUT|CUTTING|DOING)\b", h.upper()):
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
               f"the aired precedent for that is the 06/22 what-not-to-buy "
               f"segment. Confirm this is that case.")

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

    # ---------------------------------------------------- protection headers
    if PROTECTION_HEADER.replace("'", "") not in U.replace("'", ""):
        r.warn("no HERE'S HOW TO PROTECT YOURSELF section found.")

    # ---------------------------------------------------- aphorism candidates
    aph = []
    for s in spoken:
        if s.startswith("-") or s.startswith("**"):
            body_txt = re.sub(r"^-\s*", "", s)
        else:
            body_txt = s
        sents = [x for x in re.split(r"(?<=[.!?])\s+", body_txt) if x]
        if len(sents) >= 2 and words(body_txt) <= 16:
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
                    choices=["wednesday", "friday"])
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    r = check(a.path, a.day)

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
