#!/usr/bin/env python3
"""Mechanical compliance check on a Guest Booking Sheet markdown source.

    python3 check_sheet.py sheet.md

Catches what reliably slips: a guest with no contact tier, a contact with no
provenance or retrieval date, a bookability rating with no reason, a missing
backup, a Tier C entry that names the individual instead of the intermediary,
a people-search site used as a source, a missing outreach log.

It cannot tell you whether the guest is right, whether the contact is current,
or whether the person will say yes. Those are yours.

Exit 1 on ERROR, 0 otherwise.
"""

import re
import sys

GUEST_H1 = re.compile(r"^#\s+(\d+)\.\s+(.+)$", re.M)
CONTACT = re.compile(r"\*\*Contact:\*\*")
VIA = re.compile(r"\bvia\b", re.I)
BOOKABILITY = re.compile(r"\*\*Bookability:\*\*\s*`?(STRONG|SOME|NONE FOUND)`?(.*)")
PREDICTIVE = re.compile(
    r"likely to (say yes|respond|agree)|probably will|good chance|"
    r"expect (a |them )?(yes|no)|should say yes|wants? the coverage",
    re.I,
)
SOURCE_LINE = re.compile(r"Source:.*?(\d{4}-\d{2}-\d{2})")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")

# People-search and data-broker domains. Not usable as a contact source.
BROKERS = re.compile(
    r"\b(spokeo|whitepages|beenverified|truepeoplesearch|fastpeoplesearch|"
    r"intelius|peoplefinders|radaris|instantcheckmate|truthfinder|zabasearch)\b",
    re.I,
)

REQUIRED_RUNS = [
    ("Name:", "name line"),
    ("Why them:", "why-them line"),
    ("Prior on camera:", "prior-on-camera line"),
    ("Contact:", "contact line"),
    ("Bookability:", "bookability rating"),
    ("Confirmed:", "confirmed run"),
]

# Runs that were cut from the guest page. Their content moved to back matter or
# was dropped; if one reappears the page is drifting back to the old form.
BANNED_RUNS = [
    ("The ask:", "the ask"),
    ("NEEDS VERIFICATION:", "needs-verification"),
    ("Risk flags:", "risk flags"),
    ("Backup:", "backup"),
]

errors, warnings = [], []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


# Sections that were cut from the document entirely.
BACK_MATTER = re.compile(
    r"^##\s+(SOURCES\s*&|OUTREACH LOG|OPEN QUESTIONS|CONTACT SOURCES)",
    re.M | re.I)
# A contact that is an index page rather than a way to reach a person.
WEAK_CONTACT = re.compile(
    r"team page|team index|staff (page|directory)|newsroom (page|index)|"
    r"route through .*(comms|communications)|via .*news ?desk|"
    r"press office\s*$|no individual profile",
    re.I,
)
COMPANY_H1 = re.compile(r"—\s*company\s*$", re.I)


def split_guests(md):
    """Return [(number, headline, body)] for each guest page.

    Back matter after the last guest belongs to the document, not to that
    guest — otherwise contacts in the outreach log get attributed to
    whoever happens to be last on the sheet.
    """
    marks = list(GUEST_H1.finditer(md))
    out = []
    for idx, m in enumerate(marks):
        end = marks[idx + 1].start() if idx + 1 < len(marks) else len(md)
        out.append((m.group(1), m.group(2).strip(), md[m.start():end]))
    return out


def check_contact_block(label, body):
    """A contact needs to be reachable, sourced, dated, and pitched."""
    if "NO CONTACT FOUND" in body:
        if not re.search(r"tried|searched|looked", body, re.I):
            warn(f"{label}: 'NO CONTACT FOUND' with no note on what was tried. "
                 f"Say what you searched so a human knows where to pick up.")
        return

    if not CONTACT.search(body):
        err(f"{label}: no contact line. Every guest carries **Contact:** or "
            f"'NO CONTACT FOUND'.")
        return

    # The contact block is the run plus its indented continuation lines.
    block = ""
    m = CONTACT.search(body)
    if m:
        after = body[m.start():].splitlines()
        kept = [after[0]]
        for line in after[1:]:
            if line.startswith(("  ", "\t")) or not line.strip():
                kept.append(line)
                if not line.strip() and len(kept) > 2:
                    break
            else:
                break
        block = "\n".join(kept)

    if not SOURCE_LINE.search(block):
        err(f"{label}: contact has no 'Source: ... YYYY-MM-DD' line. Contacts "
            f"rot — provenance and date are what make one trustable.")

    if "Pitch:" not in block:
        warn(f"{label}: contact has no 'Pitch:' line. One sentence on what they "
             f"get out of appearing is what the booker says on the call.")

    wc = WEAK_CONTACT.search(block)
    if wc:
        err(f"{label}: contact is an index, not a person ('{wc.group(0).strip()}'). "
            f"Find an email, a phone number, or a LinkedIn — or cut the guest.")

    if re.search(r"records search|people search|public records(?! request)",
                 block, re.I):
        err(f"{label}: contact sourced from a records or people search. Not a "
            f"booking path — route through someone who knows them.")

    if VIA.search(block) and not re.search(
            r"attorney|counsel|lawyer|law firm|advocacy|advocate|reporter|"
            r"journalist|news ?desk|news agency|syndicat|wire service|outlet|"
            r"group admin|moderator|guardian|liaison|publicist|press",
            block, re.I):
        warn(f"{label}: contact routes 'via' someone unnamed as a relationship. "
             f"Say who they are to the guest.")


def check(md):
    guests = split_guests(md)

    # --- document-level -----------------------------------------------------
    if not guests:
        err("No guest pages found. Expected H1s like '# 1. GUEST NAME — role'.")

    if not re.search(r"^##\s+GUESTS", md, re.M | re.I):
        err("No GUESTS section. Page one is the table.")

    bm = BACK_MATTER.search(md)
    if bm:
        err(f"Back-matter section found ('{bm.group(0).strip()}'). The sheet is "
            f"a list of people and how to reach them — it ends with the last "
            f"guest. Fact-checking belongs to rossen-bible-final-reviewer.")

    if re.search(r"NOT REVIEWED|cannot watch video|cannot watch or listen", md, re.I):
        err("Internal-document caveat found ('NOT REVIEWED' or similar). The "
            "reader knows. Link the appearance and move on.")

    if not re.search(r"^#\s+\d+\..*—\s*company\s*$", md, re.M | re.I):
        warn("No guest with role 'company'. Any story naming a company needs "
             "a right-of-reply contact. Skip only if no company is named.")

    if re.search(r"SLATE VERDICT|slate-level verdict|coverage assessment", md, re.I):
        err("Slate verdict found. The document never grades itself — page one "
            "is the table and nothing else.")

    if re.search(r"^##\s+ROSTER", md, re.M | re.I):
        err("Section is named ROSTER. It is GUESTS.")

    for m in BROKERS.finditer(md):
        err(f"People-search site used as a source ('{m.group(0)}'). These are "
            f"unreliable and not defensible if anyone asks where a contact came "
            f"from. Use published professional contact or an intermediary.")

    # --- per-guest ----------------------------------------------------------
    for num, headline, body in guests:
        label = f"Guest {num} ({headline[:44]})"

        if COMPANY_H1.search(headline):
            # A comment request, not a booking: name and contact only.
            for marker, what in [("Name:", "name line"),
                                 ("Contact:", "contact line")]:
                if marker not in body:
                    err(f"{label}: missing {what} (**{marker}**).")
            extra = [m for m, _ in REQUIRED_RUNS
                     if m not in ("Name:", "Contact:") and m in body]
            if extra:
                err(f"{label}: company entry carries {extra}. It gets a name "
                    f"and a contact and nothing else.")
            check_contact_block(label, body)
            continue

        for marker, what in REQUIRED_RUNS:
            if marker not in body:
                err(f"{label}: missing {what} (**{marker}**).")

        for marker, what in BANNED_RUNS:
            if marker in body:
                err(f"{label}: '{marker}' was cut from the guest page. Doubts "
                    f"and legal risk go in SOURCES & FLAGS; alternates come "
                    f"from asking the first person you call.")

        m = BOOKABILITY.search(body)
        if m:
            reason = m.group(2).strip(" —-–:")
            if len(reason) < 8:
                err(f"{label}: bookability '{m.group(1)}' with no appearance "
                    f"evidence. Say what the record shows — 'regular CNN and "
                    f"podcast appearances'.")
        elif "Bookability:" in body:
            err(f"{label}: bookability must be STRONG, SOME, or NONE FOUND — "
                f"appearance history, not a forecast.")

        pm = PREDICTIVE.search(body)
        if pm:
            err(f"{label}: predictive language ('{pm.group(0)}'). Bookability "
                f"is appearance history. Nobody can forecast a yes.")

        if re.search(r"`\w+`|\b\w+_\w+\b", headline):
            err(f"{label}: role is code-formatted or underscored in the "
                f"heading. Write plain words — 'victim', not '`victim_firsthand`'.")

        check_contact_block(label, body)

        for addr in EMAIL.findall(body):
            near = body[max(0, body.find(addr) - 300): body.find(addr) + 300]
            if not SOURCE_LINE.search(near):
                warn(f"{label}: email '{addr}' has no nearby dated Source line. "
                     f"If it wasn't found published, it doesn't go on the sheet.")


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2

    with open(sys.argv[1], encoding="utf-8") as fh:
        md = fh.read()

    check(md)

    for w in warnings:
        print(f"WARN   {w}")
    for e in errors:
        print(f"ERROR  {e}")

    if not errors and not warnings:
        print("Clean. Mechanical checks only — the guest, the contact, and the "
              "yes are still yours to judge.")
    else:
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
