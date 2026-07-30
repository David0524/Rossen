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
python3 scripts/build_bible.py draft.md "07_29 F2 BIBLE.docx"
python3 scripts/verify_format.py "07_29 F2 BIBLE.docx"
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

The `.docx` is the deliverable. Two things go **in the chat reply and never in
the document** — no reference bible contains either:

**1. The clip manifest.**

```
CLIP MANIFEST
b01  HORIZONTAL  victim interview     retired officer / PayPal invoice / $10,000
b02  VERTICAL    evidence             garage fire / lithium leaf blower
b03  HORIZONTAL  confrontation bust   police sting / gold courier / $700,000
```

**2. The source rundown**, separating what is confirmed from what needs a human
check, plus anything that could not be found.

Inside the document, citations go inline as hyperlinks on the named source,
matching how aired bibles link a study or a resource URL. Keep any `unconfirmed`
or `TBD` flags short and inline right at the relevant cue.
