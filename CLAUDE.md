# Rossen Reports workflow — standing instructions

## Drive delivery (producer rule, 9/29/2026)

When each of the five stages is complete, push its deliverable to Google Drive **automatically**, without being asked:

**Folder:** `!Shows` (id `1uwPmH5sTUldGiUkgILvmr2vu6Opavr5H`, owner david@rossenmedia.com) → the show-date folder.
Show-date folders are named `M/D -- <SHOW TITLE IN CAPS>`, e.g. `10/7 -- YOUR STORE IS WATCHING YOU` (id `1043GPVDmiwWmnOTJGeg8Jg9TGPap05_5`),
`10/2 -- AMAZON PRIME DAY`. If the show's folder doesn't exist, create it under `!Shows` in that format.
Do not use Kyle's "Show Plan Demo" tree (`Wed Oct 7, 2026` etc.) unless told to.

| Stage | Skill | What goes to Drive |
|---|---|---|
| 1. Pre-bible | rossen-pre-bible | The pitch sheet (Google Doc) |
| 2. Pre-bible email | rossen-pre-bible, Step 3 | **Appended to the bottom of the pre-bible doc** — not a separate file |
| 3. Outline w/ videos | rossen-story-outline + rossen-pipeline | The outline (Google Doc), at Stage: videos |
| 4. Bible | rossen-script-writer | The bible |
| 5. Bible review | rossen-bible-final-reviewer | The review |

Notes:
- The Drive connector can't take a ~40 KB .docx in one call. Upload the stage's markdown rendered to HTML (`contentMimeType: text/html`),
  which Drive converts to a Google Doc with tables and links intact. Title: `M/D <Wed|Fri> <Stage name>`, e.g. `10/7 Wed Outline w Videos`.
- Never overwrite a file a person uploaded (e.g. `10/7 Wed Pre Bible Pitch V7`); add a new doc and say so.
- Say in chat which file was pushed and link it.

## Bible layout (producer, 9/30/2026)
- House format = rossen-script-writer's `build_bible.py` / `docx-format.md`: Arial, **1.15 line spacing**, a **blank line
  between every line** (sentence/phrase/cue), 18pt spoken lines, 23pt bold headers, cues bold red. Not 14pt; not tight.
- The Google Doc must match the .docx. Build the .docx with `build_bible.py`, then
  `python3 tools/bible_docx_to_html.py "<MM_DD> LIVE BIBLE.docx" out.html` and upload that HTML (it copies every
  paragraph, blank lines and sizes included). Put `p{margin:0;line-height:1.15}` in a `<style>` block to stay under
  the connector's size limit. Never hand-write the Drive HTML separately from the .docx.

## Team (producer note, 9/30/2026)
- Amanda Scherker is no longer with Rossen (the 9/30 skills update removed her from the skills). Bibles are
  written with rossen-script-writer from the approved outline w/ videos. Don't address, copy or credit her.
- Call-in shows: "a producer calls and books" callers. Ask the producer who that is before assuming.

## Audience and standing editorial notes
- Audience is 55+. Nothing kids-focused.
- Friday is Amazon/deals; deals guest Trey Donovan unless told otherwise.
