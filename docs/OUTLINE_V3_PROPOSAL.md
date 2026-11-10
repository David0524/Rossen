# Outline v3: TJ's layout, our content

> **Adopted 11/10/2026** in `rossen-story-outline` as "one document, two readers": the front is TJ's show-order layout for the room (the producer's edits below included); everything Claude and the pipeline need moved to a Build Sheet behind a page break, keyed by beat id. The skill's SKILL.md and `references/example_v3_1111.md` are now the spec; this file is the history.

Proposal, 11/3/2026. Nothing in the skills changes until the producer approves (CLAUDE.md).
Worked example: `runs/W_11112026/Outline F2 11_11 -- v3 SAMPLE.docx` (source `outline_v3_sample.md`). It is our
11/11 outline (`outline.md`), with the same beats, clips and research, laid out the v3 way.

## The short version

TJ's outline reads like the show. Ours reads like a database. v3 keeps TJ's top-to-bottom, one-block-per-beat
layout, with each clip and its soundbite sitting where it plays. It keeps every field our skills depend on
(dates, status, hold back, climb, red flags, Jeff notes, sources), and puts each one where a person reads it:
a labeled line inside the beat it belongs to, not a separate table or section.

## What makes TJ's outline easy to review and change by hand

1. **It runs in show order, top to bottom.** Copy, then the clip, then copy. You never cross-reference a beat
   table against a Videos table by row number. Ours makes the reader hold "row 5" in their head across two
   tables and three sections.
2. **The section headers are the on-air headlines.** You see the show's shape in viewer language
   ("BURGLARS CAN BLACK OUT YOUR SECURITY CAMERA… FOR ABOUT 60 BUCKS"), not in labels ("Your camera goes dark").
   Our headlines sat in a separate "Headlines and bridges" list at the bottom.
3. **Each clip sits where it plays, with its soundbite.** The link, date and length come first, then the in–out
   points with outcues in bold, then the transcript in italics. A reviewer can judge the clip without opening it.
   Ours had a one-line "Shows" summary in a table on another page.
4. **Clips are numbered in air order (CLIP 1–9).** "Clip 3" means the same thing in the outline, the bible and
   the edit bay.
5. **The bullets are near-copy.** They're sayable sentences in sentence case. A producer can rewrite a line,
   and the bible writer barely has to translate it.
6. **No tables in the body.** Moving a beat is cut and paste of one block. Editing a table in Google Docs (merged
   cells, wrapped text, rows that won't move) is what makes ours hard to change by hand.
7. **The break is visible:** a `////` rule, the sponsor tease and the spot names, in place.
8. **The protection list is the payoff,** numbered steps with sub-bullets, and its clips embedded under the step
   they prove.
9. **Facts are linked where they're stated** (FCC, the U.S. Attorney) instead of in a source list.
10. **It's short.** Page one is a summary paragraph, then the show.

## What ours does that TJ's lost, and what it cost this week

| Our field | What it does | What happened without it (11/11) |
|---|---|---|
| **Who, with full name, place and date** | The room sees the real case; ⚠️ flags anything more than six months old so the bible dates it | Braintree (2024) went to air undated in TJ's copy, so it reads as current |
| **Clip status** (`PICK`, `WEAK`, `MANUAL`, `· UNVERIFIED`, `· LEGAL`) | Says which clips a transcript has verified and which windows carry legal risk | Clips 1 and 4 have no transcript in our run; nothing in TJ's outline says so |
| **Hold back** | Decides the payoff the tease and headers must not give away | TJ's header "…AND POLICE LEFT IT RIGHT THERE" gave away the trap; we rewrote it |
| **Peg / why-now, Climb, Framing** | The story's spine: why this week, what gets worse each beat, the phrase true of every case | TJ's order puts the success story third; Jeff's 11/04 note says show results early |
| **Red flags per case + the fix with sources** | Every claim in the protection list carries the issuing body | TJ's "the LA County sheriff says… Uber Eats bags" isn't in any source; we had to rewrite it |
| **Jeff should know** | Becomes the bible's JEFF PLEASE NOTE comments | TJ's has none; all 15 in the bible came from our outline and research |
| **Open package, Decisions before we write** | The room's open calls, before drafting | TJ's names no open package; we had to decide it after the bible was written |
| **Beat ids (`11-11-A5`) and fixed tags** | The clip pipeline, `check_outline.py` and the bible writer parse them | TJ's prose can't be checked or fed to the pipeline |

## The v3 layout

### Page one

```
# 11/11 WED — <WORKING TITLE IN CAPS>
Airdate · tapes · stories · guest · sponsor (breaks) · Stage: beats | videos

SUMMARY — three sentences, plain prose (TJ's paragraph, our "show in three sentences").

THE SPINE (per story; one line each)
  In one sentence: …
  Hold back: …
  Peg: … (why-now chain if news)
  Climb: …
  Framing: …
  Open package: CLIP n — what's on screen

RUNNING ORDER — a numbered list, not a table:
  1. Tease
  2. <headline> — clips 1–3
  3. //// Break: OmniWatch
  …

DECISIONS BEFORE WE WRITE — checkboxes: [ ] …
```

### The body: one block per beat, in show order

```
## <THE ON-AIR HEADLINE, IN CAPS>            ← becomes the bible header as written
A2 · They got caught · Braintree, MA family and neighbor (Jul 2024) ⚠️ date it on air
                                              ← the meta line: beat id · beat · Who (date) · flags

- Talking points, sentence case, one thought each, in the order Jeff hits them.
- The last bullet sets up the question the clip answers.

CLIP 1 (HORIZONTAL) · PICK — [Outlet — title](URL) · Jul 16, 2024 · 2:39
  0:30–1:00 ("REALLY, REALLY SHOCKING") // BUTT 1:21–1:32 ("CAMOUFLAGED INTO THE BUSHES")
  Soundbite: "…verbatim…" // "…verbatim…"
  Legal: …                                    ← only when the status carries · LEGAL

Out: the line Jeff comes back in on, and the next reason to stay.
Red flag: the takeaway after this case.       ← only after a victim case
Jeff should know: one line.                    ← zero or more, under the beat they guard
```

Before Phase 2, the clip block is a placeholder the pipeline fills:
`CLIP — FIND · VERTICAL: <the footage wanted, with the searchable specifics>`.

### Break

```
////////////////////
Next (tease): two or three named payoffs, as sentences to the viewer.
OMNIWATCH SPOT
////////////////////
```

### HERE'S HOW TO PROTECT YOURSELF

Numbered steps, in TJ's form: a bold command, then sub-bullets for the details, each fact ending with its
source in parentheses. Clips that prove a step sit under it as clip blocks. The tease's named promise is
labeled (`← the two-minute walk from the tease`), and the do-nothing test is the step's last bullet.

### Back page: Gaps and verification

Only the ⚠️ items that change the show's shape or need a person before taping. Everything a beat needs is
already inside that beat.

### Formatting (Google Docs friendly)

- Arial 11. H1 story title, H2 headlines (caps, bold). The meta line in small grey. Clip lines bold, soundbites
  italic grey, labels (`Out:`, `Red flag:`, `Jeff should know:`, `Legal:`) bold.
- No tables in the body; the running order is a list. Every URL is a live link.
- A page break before each story, never between beats, so one beat block never splits across tables.

## Why this stays easy for Claude

The structure moves from tables to **fixed line prefixes**, so nothing a script reads is lost:

| Script or skill | Reads today | Reads in v3 |
|---|---|---|
| `check_outline.py` | the beat and Videos tables | the meta line (`^[A-Z]\d+ · `), `CLIP n (ORIENTATION) · STATUS`, the in–out line, `Out:`, `Red flag:`, `Jeff should know:` |
| `rossen-beat-extractor` | Who + What happens + pre-bible | the meta line + the beat's talking points + the clip line's wanted footage |
| `rossen-pipeline` write-back | fills a Videos row per beat | replaces the beat's `CLIP — FIND…` placeholder with the clip block, soundbite from the transcript |
| `rossen-script-writer` | beat table → headers, Videos → markers | H2 → header as written; talking points → runway; clip block → numbered marker + red source line; `Out:` → re-entry line; `Red flag:` → takeaway; `Jeff should know:` → comment |

All of the checker's rules survive: one sentence per point, Who with a person and a date, ⚠️ dating, a status
on every clip, the transcript window scan, sources on fix steps, beats per story.

## What would change, once approved

1. `rossen-story-outline`: SKILL.md (layout sections), `templates/outline.md`, `check_outline.py` (parse the
   prefixes instead of tables) and `build_outline.py` (v3 styles, no body tables). Keep the v2 table reader in
   the checker for old outlines.
2. `rossen-pipeline` / `rossen-beat-extractor`: read beats from the meta lines; write clip blocks back with the
   soundbite.
3. `rossen-script-writer`: the handoff table above.
4. Before editing, diff each against the synced account copy (CLAUDE.md skill-sync rule), then send `.skill`
   packages.

## Questions for you

1. **Talking points or near-copy?** TJ's bullets are almost Jeff's lines ("Look how well they hid it. Watch
   this."). The sample writes them as sayable sentences in sentence case, which keeps them reviewable and lets
   the bible writer keep your edits. Fine, or do you want plainer notes?
2. **Soundbite length.** The sample quotes the full window, up to about 60 words a segment. Shorter (outcue plus
   one line)?
3. **Headlines in caps** in the outline (as they'll appear in the bible), or sentence case?

## Producer edits to the sample (11/3)

File: `runs/W_11112026/Outline F2 11_11 -- v3 SAMPLE (producer edits).docx`. What changed, and what it means for the spec:

1. **Breaks.** Running order: one break, labeled `GENERIC AD LEAD IN` instead of naming OmniWatch; Break 2 removed.
   Spec: the outline marks where the break goes and a generic lead-in; it doesn't name the sponsor or carry sponsor
   tease copy. (The body still shows two `OMNIWATCH SPOT` blocks; to confirm, one break and no sponsor name there either.)
2. **Decisions before we write: removed.** Spec: drop it from the outline. Open calls go to chat and `OPEN.md`.
3. **Protection list: replaced with TJ's version.** Plain, sayable steps in sentence case with sub-bullets; no source
   parentheticals; no demo block; no `Jeff should know` or do-nothing test inside the list; clips 8 and 9 in TJ's
   nested form (`CLIP n (ORIENTATION): link · date · length`, then a sub-bullet for the timecode and one for the
   SOUNDBITE), no status, and the setup line ends `Listen.`
   Spec: the fix section is written as the producer will read it. Sources, the do-nothing test and fix-step Jeff notes
   move to the back page, keyed by step number, so the bible writer and the source log still get them.

Open questions raised by the edits: whether TJ's nested clip format replaces the v3 clip block everywhere, or only
in the protection list; and whether clip status (`PICK`, `UNVERIFIED`, `LEGAL`) stays visible in the body or moves
to the back page.
