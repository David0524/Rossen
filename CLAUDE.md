# Rossen Reports workflow — standing instructions

## Delivery (producer rule, updated 10/6/2026)

**Do not push files to Google Drive** (too token-intensive). This replaces the 9/29 auto-push rule.
Deliver each stage's file in chat (SendUserFile) and commit it to the run folder (`runs/<RUN_ID>/`).
Only touch Drive if the producer asks for it in that conversation.

| Stage | Skill | Deliverable |
|---|---|---|
| 1. Pre-bible | rossen-pre-bible | The pitch sheet .docx |
| 2. Pre-bible email | rossen-pre-bible | In chat, ready to paste |
| 3. Outline w/ videos | rossen-story-outline + rossen-pipeline | The outline .docx, at Stage: videos |
| 4. Bible | rossen-script-writer | `<MM_DD> LIVE BIBLE.docx` |
| 5. Bible review | rossen-bible-final-reviewer | Review, annotated bible, source log (.docx) |

Reference if Drive is requested: `!Shows` folder id `1uwPmH5sTUldGiUkgILvmr2vu6Opavr5H`; show folders are named
`M/D -- <SHOW TITLE IN CAPS>`; never overwrite a file a person uploaded.

## Bible layout (producer, 9/30/2026)
- House format = rossen-script-writer's `build_bible.py` / `docx-format.md`: Arial, **1.15 line spacing**, a **blank line
  between every line** (sentence/phrase/cue), 18pt spoken lines, 23pt bold headers, cues bold red. Not 14pt; not tight.
- Build the .docx with `build_bible.py`. If a Google Doc is ever requested, generate it from the .docx with
  `tools/bible_docx_to_html.py`; never hand-write it separately.

## Team (producer note, 9/30/2026)
- Amanda Scherker is no longer with Rossen (the 9/30 skills update removed her from the skills). Bibles are
  written with rossen-script-writer from the approved outline w/ videos. Don't address, copy or credit her.
- Call-in shows: "a producer calls and books" callers. Ask the producer who that is before assuming.

## Audience and standing editorial notes
- Audience is 55+. Nothing kids-focused.
- Friday is Amazon/deals; deals guest Trey Donovan unless told otherwise.
