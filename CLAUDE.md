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

## Team (producer note, 9/30/2026)
- **Amanda Scherker is no longer with Rossen.** The skills and producer-kit references still mention her
  (rossen-story-outline "Handing off to Amanda", amanda-assignment.md, "Amanda writes the bibles",
  "Amanda calls and books" on call-in shows, Jeff-brief credit lines). Ignore those: bibles are written
  with rossen-script-writer, straight from the approved outline w/ videos. Don't draft an Amanda
  assignment email or address/copy/credit her. If a task needs someone to book callers or guests, ask
  the producer who owns it now.

## Audience and standing editorial notes
- Audience is 55+. Nothing kids-focused.
- Friday is Amazon/deals; deals guest Trey Donovan unless told otherwise.
