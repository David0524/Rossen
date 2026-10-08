# House .docx format

Load this at render time. The implementation of record is
`scripts/build_bible.py` — **run it rather than hand-building the document.**
Pandoc and plain markdown-to-docx conversion do not reproduce run-level colour,
and colour here is not styling.

**Red versus black is the whole point of the colour: black is what Jeff says, red
is a production instruction.** A cue rendered in black is a real defect — on a
live show he will read it aloud.

## Pipeline

```bash
python3 scripts/check_bible.py draft.md --day wednesday    # fix errors, repeat
python3 scripts/build_bible.py draft.md "HE SAID HE WAS TOM SELLECK - WED 10_14.docx"
python3 scripts/build_source_log.py sources.md "HE SAID HE WAS TOM SELLECK - WED 10_14 - SOURCE LOG.docx"
python3 scripts/verify_format.py "HE SAID HE WAS TOM SELLECK - WED 10_14.docx"
```

`build_bible.py` takes the same markdown draft `check_bible.py` reads, so one
artifact is validated and rendered. Requires `python-docx`:
`pip install python-docx --break-system-packages`.

Historical note: earlier guidance specified the `docx` npm library. The bundled
builder is Python instead — same output, no install step at render time, and it
matches the pattern of Anthropic's own document skills. If the house toolchain
must be Node, the classification table below is the spec to port.

## Format table

| Element | Format |
|---|---|
| Everything | Arial |
| Headers, story titles, mid-story beat headers, separators | 23pt bold black |
| Spoken body lines | 18pt regular black, bold only on emphasized words |
| All production cues — clip, `OUT:`, graphic, sponsor, screenshot, screen share | 18pt **bold red FF0000** |
| Graphic card list items | 18pt regular red |
| CTA lines | 18pt regular black |
| `END OF SHOW` | 18pt bold black |
| Hyperlinks | blue 1155CC, underlined, 18pt |

Page: US Letter, 1" margins all sides, line spacing 1.15.

Blank paragraph between distinct bullets and beats. **No** blank paragraph
between a clip cue and its `OUT:` line, or between a graphic-card cue and the
items on the card.

## How the builder classifies a line

Written down so a draft can be authored to render correctly the first time.

| Draft line | Renders as |
|---|---|
| `(((...)))` or `((...))` at line start | production cue |
| `OUT:` | production cue, no blank paragraph above it |
| `**ALL CAPS**` as the whole line | 23pt header |
| `—------` or `______` | 23pt separator |
| `HIT LIKE AND SUBSCRIBE`, `JOIN THE CHAT`, `BECOME A MEMBER` | CTA |
| `END OF SHOW` | 18pt bold black |
| all-caps line following a `CREATE FULL SCREEN GRAPHIC` or `TAKE FULLSCREEN` cue, until the next cue or dash bullet | graphic card item, red |
| anything else | spoken body |

Inline `**bold**` becomes a bold run in place. `[text](url)` becomes a blue
underlined hyperlink. Both work inside any body line.

## What verify_format.py checks

Every run is Arial; headers are 23pt bold black; body is 18pt; every cue is bold
`FF0000`; page is Letter with 1" margins; spacing is 1.15; no blank paragraph
sits between a clip cue and its `OUT:`; every clip cue has an `OUT:` beneath it.
It reports distinct defect classes rather than one line per run, so a systematic
error reads as one finding.

## Deliverables

Two files, both named for the A-story headline plus the air day and date
(` - DRAFT` before `.docx` on a draft bible):

```
HE SAID HE WAS TOM SELLECK - WED 10_14.docx
HE SAID HE WAS TOM SELLECK - WED 10_14 - SOURCE LOG.docx
```

**1. The bible.** No sources section and nothing under any clip marker but
`OUT:`. Citations may go inline as a hyperlink on the named source, matching how
aired bibles link a study or a resource URL. Keep any `UNCONFIRMED` flag short
and inside a red production cue.

**2. The companion source log**, built by `scripts/build_source_log.py` from a
markdown file with two pipe tables. The script errors on an empty source or
scope cell.

```
## CLAIMS
| Claim | Status | Source | Scope |
|---|---|---|---|
| Karen Whitaker, 79, Bermuda Dunes | CONFIRMED | https://www.nbcnews.com/... | Age and place per NBC; sheriff via Fox |
| Sheriff: no evidence scammers directly involved in deaths | CONFIRMED | https://www.foxnews.com/... | Copy never links scam to deaths; tease avoids the deaths |

## CLIPS
| Beat | Orientation | Role | Candidate URL | Timecode | Known from |
|---|---|---|---|---|---|
| b01 | HORIZONTAL | victim / case report | https://www.youtube.com/watch?v=n9agOyCc9Mk | — | title and description only, not watched |
```

Status is one of CONFIRMED, PARTIALLY CONFIRMED, UNVERIFIED, CONTRADICTED. Every
caution flag carried in from the pre-bible or outline gets a claims row whose
scope note says how the copy honours it. In FINAL, the Beat column carries the
clip number from the bible and Timecode carries in and out.

The chat reply stays short: stage, assumptions, anything declined, open
decisions, and the rows that need a human before air.
