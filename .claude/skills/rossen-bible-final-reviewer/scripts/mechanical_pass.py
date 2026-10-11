#!/usr/bin/env python3
"""mechanical_pass.py — Step 0 of a bible review.

Does the decidable half of the checklist so the reviewer's attention goes to the
half that needs judgment. Emits findings already tagged BLOCKER / WARNING / NOTE
in the reviewer's own taxonomy, ready to drop into the summary tables, plus a
triage-ordered claim inventory so the fact-check budget is known before the first
search.

Usage:
    python3 scripts/mechanical_pass.py draft.md                  # pre-air draft
    python3 scripts/mechanical_pass.py draft.md --stage final    # manifest locked
    python3 scripts/mechanical_pass.py draft.md --json

--stage draft (default): clip cues without a source are a NOTE. Aired bibles
routinely carry unsourced cues at this stage; the clip pipeline sources them
downstream.
--stage final: the producer has said the clip manifest is locked, so a cue with
no source is a BLOCKER.

If `rossen-script-writer/scripts/check_bible.py` output is already available for
this draft, import its ERRORs instead of re-deriving the overlap; this script adds
the checks that one does not have (END OF SHOW, sponsor position, tease/body
figure drift, PII patterns, verbatim-quote length, claim inventory).
"""

import argparse
import json
import signal
import re
import sys

BANNED = ["FOLKS", "CONSUMERS", "HOWEVER", "ALLEGEDLY", "REPORTEDLY", "ALLEGED",
          "UTILIZE", "INDIVIDUALS", "FURTHERMORE", "MOREOVER", "IN CONCLUSION",
          "THE BOTTOM LINE", "HERE'S THE THING", "PURCHASE", "THE TELL",
          # producer kit (Sept 2026): words Jeff doesn't say
          "OUTRAGEOUS", "TOTALLY AMAZING", "INCREDIBLE DISCOUNTS", "FUNCTIONALLY",
          "DISCREPANCIES", "FLUCTUATIONS", "ADDITIONALLY", "UNACCEPTABLE",
          "WE WILL DEMONSTRATE", "JUST WATCH", "TAKE A LOOK", "HAVE A LOOK"]

CLIP = re.compile(r"\(+\s*PLAY CLIP\s+([A-Z0-9]+)([^)]*)\)+", re.I)
WELL_FORMED = re.compile(r"^\(\(\(PLAY CLIP (XXX|\d+) (HORIZONTAL|VERTICAL)"
                         r"( BROLL)?\)\)\)$", re.I)
PROTECT = re.compile(r"HOW TO PROTECT YOURSELF|KEY TAKEAWAYS|TAKEAWAYS|\bTIPS FOR\b|BEFORE YOU (THROW|TOSS|BUY|HAND)")
SPONSOR = re.compile(r"SPONSOR TEASE|PLAY (OMNIWATCH|CHAPTER )?SPONSOR", re.I)
MONEY = re.compile(r"\$\s?[\d,]+(?:\.\d+)?(?:\s*(?:MILLION|BILLION|THOUSAND))?"
                   r"|[\d,]+(?:\.\d+)?\s*(?:MILLION|BILLION|THOUSAND)\s+DOLLARS",
                   re.I)
PCT = re.compile(r"\d+(?:\.\d+)?\s?%|\d+\s*(?:TO|-)\s*\d+\s?%")
PHONE = re.compile(r"1?-?\s?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}")
URLISH = re.compile(r"\b[A-Z0-9][A-Z0-9-]*\.(?:GOV|ORG|COM|NET)(?:/\S*)?", re.I)
ASSET_HOST = re.compile(r"dropbox|googleusercontent|imgur|cdn\.|\.png|\.jpg|"
                        r"\.jpeg|\.gif|drive\.google", re.I)
QUOTED = re.compile(r"[\u201c\"]([^\u201d\"]{40,})[\u201d\"]")
ADDRESS = re.compile(r"\b\d{2,6}\s+[A-Z][A-Za-z]*\s+"
                     r"(STREET|ST|AVENUE|AVE|ROAD|RD|DRIVE|DR|LANE|LN|"
                     r"BOULEVARD|BLVD|COURT|CT|WAY|PLACE|PL)\b", re.I)
ACCT = re.compile(r"(ACCOUNT|CARD)\s+(ENDS?\s+IN|ENDING\s+IN|NUMBER\s+IS)\s*"
                  r"#?\s*(\d{3,})", re.I)
AGENCY = re.compile(r"\b(F-?B-?I|F-?T-?C|C-?F-?P-?B|D-?O-?T|D-?O-?J|FMCSA|"
                    r"IC3|MEDICARE|SOCIAL SECURITY|TREASURY|NHTSA|CPSC|"
                    r"HARVARD|LENDINGTREE|BBB)\b", re.I)
ATTRIB = re.compile(r"\b(SAYS|SAID|TOLD|ACCORDING TO|REPORTS?)\b", re.I)
DATEISH = re.compile(r"\b(19|20)\d{2}\b|\b(JANUARY|FEBRUARY|MARCH|APRIL|MAY|"
                     r"JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER)\b",
                     re.I)


# ---------------------------------------------------------------- promises & red flags
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
TAKEAWAY_RE = re.compile(r"RED FLAG|\bTHE TELL\b|HERE'?S HOW TO PROTECT|ONE MOVE I PROMISED|"
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
    Expert cue lines do not count: the red flag is Jeff's, not the guest's."""
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


NOTE_RE = re.compile(r"\{\{\s*(.*?)\s*\}\}")
PAGE_BREAK_RE = re.compile(r"^\s*\[\[\s*PAGE BREAK\s*\]\]\s*$", re.I)
FIGURE_RE = re.compile(r"\$\s?\d|\d+(,\d{3})*(\.\d+)?\s?(%|PERCENT\b)|\b\d[\d,.]*\s*"
                       r"(THOUSAND|MILLION|BILLION|DOLLARS?)\b|\b\d{2,}[\d,]*\b")
ONSCREEN_CUE = re.compile(r"PLAY CLIP|GRAPHIC|FULLSCREEN|SCREENSHOT|SCREEN SHARE|"
                          r"SHOW IMAGE|TAKE .*(IMAGE|PHOTO|SCREEN)")
STOP = set("A AN THE AND OR BUT TO OF IN ON AT FOR IS ARE WAS IT THIS THAT YOU YOUR "
           "WITH FROM BY AS BE IT'S THEY THEIR HE SHE HIS HER WE OUR ARE NOW JUST "
           "SO IF THEN THERE HERE'S WHAT WHO".split())
NAME_STOP = set("THANK THANKS AND YOU FOR SO THAT'S GREAT".split())
LONG_LINE_WORDS, NOTE_WORDS_MAX, DATA_RUN, ONSCREEN_WINDOW = 16, 45, 3, 3


def strip_md(s):
    """Spoken text only: JEFF PLEASE NOTE spans removed, [[PAGE BREAK]] empty."""
    if PAGE_BREAK_RE.match(s):
        return ""
    s = NOTE_RE.sub("", s)
    return re.sub(r"\*+", "", s).replace("\u2019", "'").strip()


def content_words(s):
    return {w for w in re.findall(r"[A-Z0-9']+", s.upper())
            if w not in STOP and len(w) > 2}


def oct2026_checks(raw_lines, lines, boundary, add):
    """David's notes, Oct 2026: page breaks between cases, the guest leaves by
    full name, short lines, no stat runs with nothing on screen, stories open on
    a hook rather than their title, the tease doesn't give the story away, and
    JEFF PLEASE NOTE comments are anchored and short."""
    cue = re.compile(r"\(\(+[^)]")
    clip = re.compile(r"\(+\s*PLAY CLIP", re.I)
    body_idx = range(boundary, len(lines))

    # page break between cases: a red flag followed by another sound clip
    pending = None
    for i in body_idx:
        if PAGE_BREAK_RE.match(raw_lines[i]):
            pending = None
            continue
        t = lines[i].upper()
        if not t:
            continue
        if "RED FLAG" in t and not t.startswith("("):
            pending = i
        elif clip.search(t) and "BROLL" not in t and pending is not None:
            add("WARNING", "format", f"line {pending+1}",
                "No [[PAGE BREAK]] before the next case. Every story and every "
                "case inside a story (A1, A2...) starts on a new page.")
            pending = None

    # guest leaves by full name
    for i, l in enumerate(lines):
        m = re.search(r"\(+\s*([A-Z][A-Z'\-]+)(\s+[A-Z][A-Z'\-]+)*\s+EXITS\s*\)+",
                      l.upper())
        if not m:
            continue
        prev = next((x.upper() for x in reversed(lines[:i]) if x and not cue.search(x)), "")
        mm = re.search(r"\b" + re.escape(m.group(1)) + r"\s+([A-Z][A-Z'\-]+)", prev)
        if not mm or mm.group(1) in NAME_STOP:
            add("WARNING", "production", f"line {i+1}",
                f"{m.group(1)} exits with no full name in the send-off. Write it "
                f"(-{m.group(1)} LASTNAME, THANK YOU.) in case Jeff blanks. "
                f"Call-in callers excepted.")

    # long lines
    long_ = [i for i in body_idx if lines[i] and not cue.search(lines[i])
             and not lines[i].upper().startswith("OUT:")
             and not re.match(r"^[A-Z]+:", lines[i])
             and len(re.sub(r"^-\s*", "", lines[i]).split()) > LONG_LINE_WORDS]
    if long_:
        add("WARNING", "voice", f"lines {[i+1 for i in long_[:6]]}",
            f"{len(long_)} spoken line(s) over {LONG_LINE_WORDS} words. The "
            f"bible is a reference for Jeff, not a script — split or cut.")

    # data with nothing on screen
    cues_on = [i for i, l in enumerate(lines) if cue.search(l) and ONSCREEN_CUE.search(l.upper())]
    run, dense = 0, []
    for i in body_idx:
        t = lines[i]
        if not t:
            continue
        if cue.search(t) or t.upper().startswith("OUT:"):
            run = 0
            continue
        figs = len(FIGURE_RE.findall(t.upper()))
        near = any(abs(i - c) <= ONSCREEN_WINDOW for c in cues_on)
        tip = bool(re.match(r"^-?\s*NUMBER (ONE|TWO|THREE|FOUR|FIVE)", t.upper()))
        if figs and not near and not tip:
            run += 1
            if figs >= 2 or run == DATA_RUN:
                dense.append(i + 1)
        else:
            run = 0
    if dense:
        add("WARNING", "voice", f"lines {dense[:6]}",
            "Stat-heavy copy with nothing on screen. Keep the one number that "
            "matters; move the rest to a graphic or a JEFF PLEASE NOTE comment.")

    # story opens by restating its header
    for i in body_idx:
        raw_l = raw_lines[i].strip()
        h = lines[i]
        if (not raw_l.startswith("**") or cue.search(h) or not h or h.startswith("-")
                or h.upper() != h or len(h.split()) > 16
                or "PROTECT YOURSELF" in h.upper()):
            continue
        hw = content_words(h)
        if len(hw) < 2:
            continue
        nxt = [x for x in lines[i + 1:i + 8] if x and not cue.search(x)][:2]
        for n in nxt:
            nw = content_words(n)
            if nw and len(hw & nw) / len(hw) >= 0.6:
                add("WARNING", "voice", f"line {i+1}",
                    f"Story opens by restating its header ({h[:40]!r} -> "
                    f"{n[:40]!r}). Lead with a hook, not a rewrite of the title.")
                break

    # tease gives the story away
    payoffs = [l for l in lines[boundary:]
               if "PROTECT YOURSELF" not in l.upper()
               and (re.search(r"RED FLAG", l.upper())
                    or re.match(r"^-?\s*NUMBER (ONE|TWO|THREE|FOUR|FIVE|SIX)\b", l.upper()))]
    for i in range(boundary):
        tw = content_words(lines[i])
        if len(tw) < 3:
            continue
        if any(content_words(p) and len(tw & content_words(p)) / len(tw) >= 0.6
               for p in payoffs):
            add("WARNING", "structure", f"line {i+1}",
                "The tease states a red flag or protection step the body pays "
                "off. Tease the question, not the answer — don't give the story "
                "away.")

    # JEFF PLEASE NOTE comments
    notes = [(i, n) for i, l in enumerate(raw_lines) for n in NOTE_RE.findall(l)]
    for i, n in notes:
        if not n.upper().startswith("JEFF PLEASE NOTE"):
            add("WARNING", "format", f"line {i+1}",
                "Comment must open with 'JEFF PLEASE NOTE:'.")
        if len(n.split()) > NOTE_WORDS_MAX:
            add("WARNING", "production", f"line {i+1}",
                f"JEFF PLEASE NOTE runs {len(n.split())} words; Jeff reads it "
                f"minutes before air. One or two sentences.")
        if not lines[i]:
            add("WARNING", "format", f"line {i+1}",
                "JEFF PLEASE NOTE sits on a line of its own; anchor it to the "
                "line it guards.")
    add("NOTE", "production", "document",
        f"{len(notes)} JEFF PLEASE NOTE comment(s). Judge whether any fact Jeff "
        f"must know (a nuance guarding a line, a number's limits, something "
        f"left out on purpose, who is speaking) is missing one.")


def analyze(path, stage="draft"):
    raw = open(path, encoding="utf-8").read()
    raw_lines = raw.split("\n")
    lines = [strip_md(l) for l in raw_lines]
    F = []                                    # findings

    def add(sev, dim, where, msg):
        F.append({"severity": sev, "dimension": dim, "where": where,
                  "issue": msg})

    # ---------------------------------------------------------- boundary / CTA
    boundary = None
    for i, l in enumerate(lines):
        u = l.upper().lstrip("- ")
        if u.startswith("HIT LIKE AND SUBSCRIBE") or u.startswith("JOIN THE CHAT"):
            boundary = i
            break
    if boundary is None:
        add("BLOCKER", "structure", "tease block",
            "No like/subscribe/join-chat CTA closing the tease block. The clip "
            "pipeline uses that line as its boundary marker, so without it the "
            "whole tease parses as body copy.")
        boundary = 0
    tease, body = lines[:boundary], lines[boundary:]

    if not re.search(r"-?\s*END OF SHOW", raw, re.I):
        add("WARNING", "structure", "document end",
            "No END OF SHOW marker.")

    # ---------------------------------------------------------- clip cues
    cues, numbered = [], []
    for i, l in enumerate(lines):
        if CLIP.search(l):
            cues.append((i, l))
            if not WELL_FORMED.match(l.upper()):
                add("WARNING", "format", f"line {i+1}",
                    f"Malformed clip cue {l!r}. Contract is exactly three "
                    f"parens each side and one orientation token. Aired bibles "
                    f"contain cues with two, four and five parens — those are "
                    f"typos in the corpus, not the contract, and the extractor "
                    f"parses on exact paren count.")
            m = CLIP.search(l)
            token = m.group(1).upper()
            if stage == "draft" and token.isdigit():
                numbered.append(i + 1)
            if stage == "final" and token == "XXX":
                add("WARNING", "format", f"line {i+1}",
                    "Cue still says XXX but the manifest is locked — numbers "
                    "should be filled in by now.")

    if numbered:
        add("NOTE", "format", f"{len(numbered)} cues",
            f"All {len(numbered)} clip cues are numbered rather than XXX. "
            f"rossen-script-writer leaves XXX literal until the show is timed, "
            f"so numbered cues mean either the show is timed or the draft did "
            f"not follow the placeholder convention. Confirm which — the two "
            f"skills must agree on this or the extractor gets fed the wrong "
            f"thing.")

    for i, l in enumerate(cues):
        idx = l[0]
        nxt = [x for x in lines[idx + 1:idx + 4] if x]
        if not nxt or not nxt[0].upper().startswith("OUT:"):
            add("WARNING", "format", f"line {idx+1}",
                "Clip cue has no OUT: line beneath it.")

    # source pointer near each cue: URL within 3 lines either side
    for idx, l in enumerate([c[0] for c in cues]):
        window = " ".join(lines[max(0, l - 2):l + 4])
        if not re.search(r"https?://", window):
            sev = "BLOCKER" if stage == "final" else "NOTE"
            add(sev, "clip source", f"line {l+1}",
                "No URL or source pointer on this cue. "
                + ("Manifest is locked, so this cue cannot be shot."
                   if stage == "final" else
                   "Normal at draft stage — aired bibles carry unsourced cues "
                   "and the clip pipeline sources them downstream. Listed so "
                   "the producer can confirm a manifest exists separately."))

    if cues:
        add("NOTE", "clip source", "all cues",
            f"{len(cues)} clip cues total. None can be visually confirmed — "
            f"this review works from titles, descriptions and transcripts only.")

    cue_lines = [c[0] for c in cues]

    # ---------------------------------------------------------- protection beats
    story_heads = [(i, l) for i, l in enumerate(body)
                   if l and l.upper() == l and len(l.split()) <= 12
                   and not CLIP.search(l) and not l.startswith("-")
                   and not l.upper().startswith("OUT:")]
    n_protect = len([l for l in body if PROTECT.search(l.upper())])
    n_sponsor_reads = len([l for l in body if SPONSOR.search(l)])
    if n_protect == 0:
        add("BLOCKER", "structure", "whole document",
            "No protection / takeaways beat anywhere. Every story in the aired "
            "corpus lands on one.")
    else:
        # per-story check: a run of clip cues with no protection beat after it
        # is a story that never lands its takeaways
        protect_lines = [i for i, l in enumerate(lines)
                         if PROTECT.search(l.upper())]
        trailing = [c for c in cue_lines if c > max(protect_lines)]
        if trailing:
            add("BLOCKER", "structure", f"after line {max(protect_lines)+1}",
                f"{len(trailing)} clip cue(s) appear after the last protection / "
                f"takeaways beat (cues at lines "
                f"{[c+1 for c in trailing][:6]}). That story runs its clips and "
                f"then ends without landing takeaways. Check each story "
                f"individually — a document-level count of protection beats "
                f"hides this.")

    # ---------------------------------------------------------- sponsor position
    sponsor_lines = [i for i, l in enumerate(lines) if SPONSOR.search(l)]
    blocks = []
    for i in sponsor_lines:
        if blocks and i - blocks[-1][-1] <= 6:
            blocks[-1].append(i)
        else:
            blocks.append([i])
    def is_header(t):
        return bool(t) and t.upper() == t and not t.startswith("-") \
            and not CLIP.search(t) and not t.upper().startswith("OUT:") \
            and not SPONSOR.search(t) and 2 <= len(t.split()) <= 14

    for blk in blocks:
        i = blk[0]
        before = [c for c in cue_lines if c < i]
        after = [c for c in cue_lines if c > i]
        if not (before and after):
            continue
        # a sponsor sits at a natural break if a section header or a takeaway/
        # protection beat separates it from the previous clip
        gap = lines[before[-1] + 1:i]
        at_break = any(is_header(t) for t in gap) or \
            PROTECT.search("\n".join(gap).upper())
        if not at_break:
            add("WARNING", "sponsor", f"line {i+1}",
                "Sponsor block interrupts a clip run — nothing but body copy "
                "between the previous clip and the sponsor, so there is no "
                "story boundary or takeaway beat here. House rule is one "
                "sponsor break at a story boundary.")
    if len(blocks) > 1:
        add("WARNING", "sponsor", "whole document",
            f"{len(blocks)} separate sponsor blocks at lines "
            f"{[b[0]+1 for b in blocks]}. Aired bibles carry one sponsor "
            f"break.")

    # ---------------------------------------------------------- register
    U = raw.upper()
    for w in BANNED:
        n = len(re.findall(r"\b" + re.escape(w) + r"\b", U))
        if n:
            add("WARNING", "voice", "whole document",
                f"Off-register word {w!r} x{n}. Near-absent from the aired "
                f"spoken corpus; see rossen-script-writer/measurements.md.")
    # Producer kit (Sept 2026): cue + verdict into a clip ("WATCH THIS. THIS IS
    # CRAZY.") is now written into bibles; "JUST WATCH" / "TAKE A LOOK" are not.

    # ---------------------------------------------------------- PII
    for i, l in enumerate(lines):
        if ADDRESS.search(l):
            add("BLOCKER", "privacy", f"line {i+1}",
                f"Looks like a street address: {ADDRESS.search(l).group(0)!r}. "
                f"Redact unless the source already made it public.")
        m = ACCT.search(l)
        if m:
            add("BLOCKER", "privacy", f"line {i+1}",
                f"Partial account/card number: {m.group(0)!r}. Redact.")

    # ---------------------------------------------------------- copyright
    for i, l in enumerate(lines):
        for m in QUOTED.finditer(l):
            wc = len(m.group(1).split())
            if wc >= 25:
                add("BLOCKER", "copyright", f"line {i+1}",
                    f"{wc}-word verbatim quoted block staged for air. "
                    f"Paraphrase it — long verbatim lifts are reproduction "
                    f"risk, and Jeff will not read a block quote as written "
                    f"anyway.")

    # ---------------------------------------------------------- tease/body drift
    def figs(chunk):
        out = {}
        for m in MONEY.finditer("\n".join(chunk)):
            key = re.sub(r"[^\d.]", "", m.group(0))[:6]
            out.setdefault(key, set()).add(m.group(0).strip())
        return out
    tf, bf = figs(tease), figs(body)
    for key in set(tf) & set(bf):
        variants = tf[key] | bf[key]
        if len({re.sub(r"\s+", "", v).upper() for v in variants}) > 1:
            add("BLOCKER", "consistency", "tease vs body",
                f"Figure stated differently in the tease and the body: "
                f"{sorted(variants)}. One of them will be wrong on air.")
    shared = sorted(set(tf) & set(bf))
    if shared:
        add("NOTE", "consistency", "tease vs body",
            f"{len(shared)} figure(s) appear in both tease and body. Re-check "
            f"after any correction lands — that is when drift gets introduced.")

    # ---------------------------------------------------------- tease promises
    for p in unpaid_promises(tease, body):
        add("WARNING", "consistency", "tease vs body",
            f"The tease promises {p!r} and the body never names it. Ryan's "
            f"rule (Oct 8, 2026): pay a tease promise off by name where it "
            f"lands ('HERE'S THE {p} I PROMISED'), or cut it from the tease.")

    # ---------------------------------------------------------- takeaways
    for g in takeaway_gaps(body, CLIP):
        add("WARNING", "structure", f"line {boundary + g + 1}",
            "Three sound clips run with no takeaway between them. Each victim "
            "case should end with a one-line red flag (HERE'S YOUR RED FLAG: ...), not "
            "wait for the guest or the closing list.")

    # ---------------------------------------------------------- Oct 2026 notes
    oct2026_checks(raw_lines, lines, boundary, add)

    # ---------------------------------------------------------- claim inventory
    inv = {"tier1_safety_contact": [], "tier2_entity_and_quote": [],
           "tier3_statistics": [], "tier4_background_dates": []}
    for i, l in enumerate(lines):
        if not l or CLIP.search(l):
            continue
        loc = f"line {i+1}"
        for m in PHONE.finditer(l):
            inv["tier1_safety_contact"].append([loc, m.group(0)])
        for m in URLISH.finditer(l):
            if not ASSET_HOST.search(m.group(0)):
                inv["tier1_safety_contact"].append([loc, m.group(0)])
        if AGENCY.search(l) or (ATTRIB.search(l) and re.search(r"[\u201c\"]", l)):
            inv["tier2_entity_and_quote"].append([loc, l[:88]])
        elif QUOTED.search(l):
            inv["tier2_entity_and_quote"].append([loc, l[:88]])
        for m in list(MONEY.finditer(l)) + list(PCT.finditer(l)):
            inv["tier3_statistics"].append([loc, m.group(0).strip()])
        if DATEISH.search(l) and not MONEY.search(l):
            inv["tier4_background_dates"].append([loc, l[:88]])

    total = sum(len(v) for v in inv.values())
    return {"stage": stage, "findings": F, "claim_inventory": inv,
            "claim_total": total, "clip_cues": len(cues),
            "protection_beats": n_protect}


SEV_ORDER = {"BLOCKER": 0, "WARNING": 1, "NOTE": 2}

LOG_HEADER = "| CLAIM | CONFIDENCE | SCOPE | SOURCE |"
LOG_RULE = "|---|---|---|---|"


UNNAMED = "<< NAME THIS EVIDENCE CLUSTER >>"
STANDING_GROUPS = ["CLIP SOURCES", "PRODUCER QUESTIONS — ANSWERED",
                   "TEASE / BODY CONSISTENCY"]


def emit_log_skeleton(path, r):
    """Emit the SOURCE LOG skeleton: fixed shape, claims in document order,
    standing groups at the bottom.

    Group *names* are deliberately left blank. Evidence clusters are an editorial
    call — "FTC DATA AND ALERTS", "ALLIE CONTI / VICE", "THE FEDERAL CASE" — and
    cannot be derived from the draft's headers, because protection beats appear
    mid-story and sponsor lead-ins look like story titles. The reviewer names
    them; check_source_log.py refuses a log with any placeholder left in it.
    """
    rows = []
    for tier in ("tier1_safety_contact", "tier2_entity_and_quote",
                 "tier3_statistics", "tier4_background_dates"):
        for loc, txt in r["claim_inventory"][tier]:
            n = int(re.sub(r"\D", "", loc) or 0)
            rows.append((n, txt.strip()))
    seen, ordered = set(), []
    for n, txt in sorted(rows):
        key = txt.upper()[:60]
        if key in seen:
            continue
        seen.add(key)
        ordered.append((n, txt))

    out = ["## SOURCE LOG", "", LOG_HEADER, LOG_RULE,
           f"| **{UNNAMED}** | | | |"]
    for n, txt in ordered:
        out.append(f"| (line {n}) {txt[:84]} |  |  |  |")
    for g in STANDING_GROUPS:
        out.append(f"| **{g}** | | | |")
    out.append("")
    out.append(f"<!-- {len(ordered)} claim rows. Split them into evidence "
               f"clusters and name each group in ALL CAPS, one group row per "
               f"cluster, following the story order of the bible. Strip the "
               f"(line N) prefixes once assigned. -->")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--stage", default="draft", choices=["draft", "final"])
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--emit-log-skeleton", action="store_true",
                    help="print a pre-grouped SOURCE LOG skeleton and exit")
    a = ap.parse_args()

    try:
        r = analyze(a.path, a.stage)
    except OSError as exc:
        print(f"could not read {a.path}: {exc}", file=sys.stderr)
        sys.exit(2)

    if a.emit_log_skeleton:
        print(emit_log_skeleton(a.path, r))
        sys.exit(0)

    if a.json:
        print(json.dumps(r, indent=1, ensure_ascii=False))
        sys.exit(0)

    F = sorted(r["findings"], key=lambda f: SEV_ORDER[f["severity"]])
    counts = {s: len([f for f in F if f["severity"] == s])
              for s in ("BLOCKER", "WARNING", "NOTE")}

    print(f"\nMECHANICAL PASS — {a.path}  (stage: {a.stage})")
    print("=" * 72)
    print(f"  clip cues {r['clip_cues']}   protection beats "
          f"{r['protection_beats']}   decidable findings "
          f"{counts['BLOCKER']}B / {counts['WARNING']}W / {counts['NOTE']}N\n")

    for f in F:
        print(f"  [{f['severity']}] {f['dimension']} — {f['where']}")
        print(f"      {f['issue']}\n")

    print("=" * 72)
    print(f"CLAIM INVENTORY — {r['claim_total']} checkable items, in triage order")
    print("=" * 72)
    labels = {
        "tier1_safety_contact": "TIER 1  phone numbers, URLs, agency contacts "
                                "— check every one, a wrong digit sends a "
                                "victim nowhere",
        "tier2_entity_and_quote": "TIER 2  named entities and attributed quotes "
                                  "— check every one, this is where defamation "
                                  "and fabrication live",
        "tier3_statistics": "TIER 3  dollar figures and percentages — check "
                            "every one, and pin each benchmark's scope and "
                            "period before calling anything CONTRADICTED",
        "tier4_background_dates": "TIER 4  dates and background framing — check "
                                  "if budget remains, else log as UNVERIFIED "
                                  "and say so",
    }
    for tier, label in labels.items():
        items = r["claim_inventory"][tier]
        print(f"\n{label}")
        print(f"  ({len(items)} items)")
        for loc, txt in items[:14]:
            print(f"    {loc:>10}  {txt}")
        if len(items) > 14:
            print(f"    … and {len(items)-14} more")

    print("\nAny Tier 3 or 4 item you did not fully search must appear in the "
          "source log as UNVERIFIED with a note saying the budget ran out — "
          "never as a silent omission.\n")

    sys.exit(1 if counts["BLOCKER"] else 0)


if __name__ == "__main__":
    try:
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (AttributeError, ValueError):
        pass
    main()
