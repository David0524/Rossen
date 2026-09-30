#!/usr/bin/env python3
"""Mechanical compliance check on a Step 2 pitch email (plain text).

    python3 check_pitch_email.py pitch_email.txt
    python3 check_pitch_email.py pitch_email.txt --one-sentence

Default mode is the house paragraph (1-5 sentences, ends on prior coverage).
--one-sentence enforces a single-sentence lead.

Catches structure slips: a story with no Coverage or Potential Packaging block,
a lead that runs long, coverage bullets with no date or URL, no competitor view
count, the wrong number of titles, markdown in a plain-text email, timecodes,
no prior-coverage statement, no recommendation. It cannot judge whether a claim
is true or a title is good. Those are yours.

Exit 1 on ERROR, 0 otherwise.
"""
import re
import sys

STORY = re.compile(r"^(\d+)\.\s+(.+)$", re.M)
FLAG = re.compile(r"^(One flag on|Flag on) #\d+", re.M)
URL = re.compile(r"https?://\S+")
MONTH = re.compile(
    r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2}\b"
    r"|\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\b|\b20\d{2}\b")
VIEWS = re.compile(r"\b\d[\d,.]*\s*[KM]?\s*views\b|\b\d[\d,.]*[KM]\b", re.I)
TIMECODE = re.compile(r"\b\d{1,2}:\d{2}(?::\d{2})?\s*[-–]\s*\d{1,2}:\d{2}")
SENT_END = re.compile(r"[.!?](?=[\"')\]]?\s+[A-Z])")
PRIOR = re.compile(r"never on our channel|never covered|we('ve)? (touched|covered|did|ran)|"
                   r"b story|c story|aired|nothing since|zero coverage|never touched|"
                   r"never done|we've never|first time", re.I)
RECO = re.compile(r"\b(my pick|my order|recommend|i'd (pick|go|lead)|we'd pick|pick is)\b", re.I)
BULLET = re.compile(r"^[-*]\s")

errors, warnings = [], []


def check(text, one_sentence):
    marks = list(STORY.finditer(text))
    if not marks:
        errors.append("No stories found. Expected lines like '1. HEADLINE IN CAPS'.")
        return
    nums = [int(m.group(1)) for m in marks]
    if nums != list(range(1, len(nums) + 1)):
        errors.append(f"Story numbers out of sequence: {nums}")
    if re.search(r"\*\*|^#+\s|^\|", text, re.M):
        errors.append("Markdown (bold, headers, or tables) in a plain-text email.")
    if TIMECODE.search(text):
        errors.append("Timecode found. The email never carries timecodes.")
    if not re.search(r"^Subject:", text, re.M):
        warnings.append("No 'Subject:' line (house: 'F2 Pitches for [tape date] ([air date] Air)').")
    if len(marks) < 4:
        warnings.append(f"{len(marks)} stories. For A-story pitches Jeff wants four or five options.")

    last_story_end = None
    flags_at = FLAG.search(text)
    for i, m in enumerate(marks):
        n, name = m.group(1), m.group(2).strip()
        tag = f"#{n}"
        nxt = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        body = text[m.end():nxt]
        if name != name.upper():
            errors.append(f"{tag}: headline must be all caps: '{name}'")
        cov = re.search(r"^Coverage:\s*$", body, re.M)
        pack = re.search(r"^Potential Packaging:\s*$", body, re.M)
        if not cov:
            errors.append(f"{tag}: no 'Coverage:' line.")
        if not pack:
            if re.search(r"^Titles:\s*$", body, re.M):
                errors.append(f"{tag}: header is 'Titles:'; use 'Potential Packaging:'.")
            else:
                errors.append(f"{tag}: no 'Potential Packaging:' line.")
        if not cov or not pack:
            continue

        lead = body[:cov.start()].strip()
        sentences = len(SENT_END.findall(lead)) + 1 if lead else 0
        if not lead:
            errors.append(f"{tag}: no pitch paragraph under the headline.")
        elif "\n\n" in lead:
            errors.append(f"{tag}: pitch must be one paragraph.")
        elif one_sentence and sentences > 1:
            errors.append(f"{tag}: lead runs past one sentence (--one-sentence mode).")
        elif sentences > 5:
            errors.append(f"{tag}: pitch paragraph is {sentences} sentences (house: three to five).")
        if lead and not one_sentence and not PRIOR.search(lead):
            warnings.append(f"{tag}: paragraph doesn't say whether we've covered it "
                            f"(end with 'Never on our channel.' or when we touched it).")

        cov_lines = [l for l in body[cov.end():pack.start()].splitlines() if l.strip()]
        if not 3 <= len(cov_lines) <= 5:
            warnings.append(f"{tag}: {len(cov_lines)} coverage bullets (house: three to five).")
        has_views = False
        for l in cov_lines:
            if not BULLET.match(l):
                errors.append(f"{tag}: coverage line not a bullet: '{l[:60]}'")
                continue
            if not URL.search(l):
                errors.append(f"{tag}: coverage bullet has no URL: '{l[:60]}'")
            pre = l.split("http")[0]
            if not MONTH.search(pre):
                warnings.append(f"{tag}: coverage bullet has no date: '{l[:60]}'")
            if VIEWS.search(pre):
                has_views = True
            if re.search(r"google\.\w+/search|bing\.com/search|youtube\.com/results", l):
                errors.append(f"{tag}: search-results URL is not a source: '{l[:60]}'")
        if cov_lines and not has_views:
            warnings.append(f"{tag}: no competitor video with a view count in Coverage.")

        # titles run to the first blank-line-separated non-bullet text
        tail = body[pack.end():]
        titles = []
        for l in tail.splitlines():
            if BULLET.match(l):
                titles.append(l)
            elif titles and l.strip():
                break
        if len(titles) != 3:
            errors.append(f"{tag}: {len(titles)} packaging titles (need exactly 3).")
        for t in titles:
            if not re.search(r"\b[A-Z]{3,}\b", t):
                warnings.append(f"{tag}: title has no caps punch word: '{t[2:62]}'")
            if re.search(r"\$\d", t):
                warnings.append(f"{tag}: dollar figure in title, confirm it's sourced: '{t[2:62]}'")
        last_story_end = m.end() + pack.end()

    closing = text[last_story_end:] if last_story_end else ""
    if not RECO.search(closing):
        warnings.append("No recommended order at the end ('My pick is #1 for the A...').")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        print(__doc__)
        sys.exit(2)
    check(open(args[0], encoding="utf-8").read(), "--one-sentence" in sys.argv)
    for e in errors:
        print("ERROR  ", e)
    for w in warnings:
        print("WARNING", w)
    if not errors and not warnings:
        print("OK")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
