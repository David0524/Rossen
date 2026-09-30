# Guest Sheet — document format

## Document order

1. `# GUEST SHEET — [STORY], [AIRDATE]` — document title, one H1
2. `## GUESTS` — the table, page one
3. `# 1. NAME — role` … one H1 per guest, each forcing a page break

That is the whole document. There is no sources block, no outreach log, and no
open-questions section.

Guest pages are detected as H1s beginning with a digit.

**No slate verdict, coverage summary, or self-assessment anywhere in the
document.** Page one is the table and nothing else.

## The guest table

Five columns, in this order:

```
| # | Name | Role | Contact | Prior on camera |
```

- `#` — booking priority. Narrow column, just the number.
- `Name` — the name and nothing else. "Isabelle Chapman." No affiliation here.
- `Role` — the role with its affiliation, which is what makes it readable:
  "CNN reporter", "Fox News reporter", "ex-Secret Service", "trial attorney",
  "company". Plain words, no underscores, no backticks.
- `Contact` — the actual email, phone, or LinkedIn. Not a team page.
- `Prior on camera` — outlet and year, or `None found`

There is no story column. The sheet is built after the show is written, so the
story is already known.

## The guest page

Use `templates/guest_page.md`. One page per guest, hard ceiling — and these pages
are short, so a full page should be rare.

Six runs, in order, and nothing else:

- `**Name:**`
- `**Why them:**` — one sentence
- `**Prior on camera:**` — link it, no caveats about not having watched it
- `**Contact:**` — with indented `Source:` and `Pitch:` continuation lines
- `**Bookability:**`
- `**Confirmed:**`

No ask line, no needs-verification run, no risk-flag run, no backup.

**A `company` entry is the exception** — name and contact only, nothing else. It
is a comment request, not a booking.

## Authoring convention: one run, one line

The renderer treats every line as its own paragraph. **Do not hard-wrap a run
across lines** — write each run on a single long line and let Word wrap it.

The exception is the contact block, where indented continuation lines are
deliberate. Indent them two spaces.

## Build procedure

```bash
python3 scripts/build_sheet.py sheet.md -o "Guest_Sheet_[AIRDATE].docx"
python3 scripts/check_sheet.py sheet.md
soffice --headless --convert-to pdf "Guest_Sheet_[AIRDATE].docx"
```

Then look at the pages. python-docx cannot report where a page actually broke.
