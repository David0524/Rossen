# Rossen Reports workflow — standing instructions

## Delivery (producer rule, updated 10/6/2026)

**Do not push files to Google Drive** (too token-intensive). This replaces the 9/29 auto-push rule.
Deliver each stage's file in chat (SendUserFile) and commit it to the run folder (`runs/<RUN_ID>/`).
Only touch Drive if the producer asks for it in that conversation.
Exception (producer, 10/7/2026): when the producer has converted a deliverable to a native Google Doc (e.g. [10/14 Outline](https://docs.google.com/document/d/1i7bo92FPzVjVRTmipk9x0C3gseEWYinlJbC3ClbnhQ4/edit)) and asks for changes, edit that Doc in place with the Google Docs connector (guarded by revisionId) and keep the local file in sync. The Docs connector can't edit .docx files in Drive.

| Stage | Skill | Deliverable |
|---|---|---|
| 1. Pre-bible | rossen-pre-bible | The pitch sheet .docx: `Prebible F1 10/16` |
| 2. Pre-bible email | rossen-pre-bible | In chat, ready to paste |
| 3. Outline w/ videos | rossen-story-outline + rossen-pipeline | The outline .docx, at Stage: videos: `Outline F1 10/16` |
| 4. Bible | rossen-script-writer | `F1 Fri 10/16 -- <Working Title>` (+ ` -- DRAFT` on a draft) and `F1 Fri 10/16 -- <Working Title> -- SOURCE LOG` |
| 5. Bible review | rossen-bible-final-reviewer | Review, annotated bible, source log (.docx) |

**Standard titles (producer, 10/14/2026):** `Prebible F1 10/16`, `Outline F1 10/16`, `F1 Fri 10/16 -- <Working Title>` (F2 = the Wednesday show: `F2 Wed 10/21 -- …`). Drive/Doc names keep the slash; local file names write it as `_` (`Outline F1 10_16.docx`). A pre-bible covering two shows: `Prebible F1 10/16 + F2 10/21`.

Reference if Drive is requested: `!Shows` folder id `1uwPmH5sTUldGiUkgILvmr2vu6Opavr5H`; show folders are named
`M/D -- <SHOW TITLE IN CAPS>`; never overwrite a file a person uploaded.

## Bible layout (producer, 9/30/2026)
- House format = rossen-script-writer's `build_bible.py` / `docx-format.md`: Arial, **1.15 line spacing**, a **blank line
  between every line** (sentence/phrase/cue), 18pt spoken lines, 23pt bold headers, cues bold red. Not 14pt; not tight.
- Build the .docx with `build_bible.py` and the companion source log with `build_source_log.py`. Name both with the standard bible title (producer, 10/14/2026; replaces the 10/8 headline-first naming). FINAL clips keep the red source line under `OUT:` (as sent 10/14) and the source log also carries every link and timecode. If a Google Doc is ever requested, generate it from the .docx with
  `tools/bible_docx_to_html.py`; never hand-write it separately.

## Team (producer note, 9/30/2026)
- Amanda Scherker is no longer with Rossen (the 9/30 skills update removed her from the skills). Bibles are
  written with rossen-script-writer from the approved outline w/ videos. Don't address, copy or credit her.
- Matt Raub is no longer with Rossen; TJ Cooney replaced him as Head of Content (producer, 10/12/2026). Don't
  address or copy Matt. Producer-kit rulings attributed to Matt stand until TJ or the producer changes them.
  Skills updated 10/14 (producer): current-role references say TJ; Matt stays only where the skills record what he
  did (his teardown, the two-clips standard, past meetings, aired transcripts, sent examples).
- Call-in shows: "a producer calls and books" callers. Ask the producer who that is before assuming.

## Audience and standing editorial notes
- Audience is 55+. Nothing kids-focused.
- Friday is Amazon/deals; deals guest Trey Donovan unless told otherwise.

## Standing notes (carried from the week of 10/5/2026)

Producer rulings that hold every week:
- The bible is written from the outline's locked clips (FINAL): numbered markers, `OUT:` with the outcue,
  the red source line under it, plus the companion source log. DRAFT/`XXX` only when no clips exist yet.
- The reviewer stays strict. Lines the producer keeps over a reviewer flag are one-offs, not rules.
- No skill changes until the producer approves. Don't edit the producer's Docs unless asked.
- Target is fine, but never the title or the main story.
- F1: never pitch a story that knocks Amazon (settlements, refunds, Amazon traps). The deals block sends viewers to buy there (producer, 10/11/2026).
- Pitch bar (producer, 10/11): would a 55+ middle-America viewer stop scrolling, and why does it matter to them? A small payout or a narrow niche fails it.
- Sponsor breaks (producer, 10/28/2026): go into every sponsor with a smooth transition, not a tease of what's
  coming. Two or three lines that bridge from the story just told to the sponsor's product, ending on the
  sponsor's name (e.g. the father-and-son forgery → "you'd want to know if your information is out there" →
  OmniWatch). No "NEXT…" lines and no "BUT FIRST, A QUICK WORD" before a break. This overrides the
  script-writer skill's tease-then-break rule (Ryan note 7) until the skill is updated.
- Graphic requests: deliver a ChatGPT-ready image prompt in chat. Keep "police say" / accused framing on screen.

Workarounds:
- Drive, only when asked: .docx → `tools/bible_docx_to_html.py` → upload the HTML as a new Google Doc in the
  show folder. Edit native Docs in place (Docs connector, guarded by revisionId).
- YouTube captions and media get bot-walled from this container. Probe once, wait 5+ minutes, retry once
  through `fetch_many`. Use the run's cached `transcripts.json` before re-fetching. A 30-minute wait has
  cleared it before.
- News-site video (WMBF / Arc Publishing) is reachable. Run Whisper on it, but check real length with
  ffprobe: site metadata has been 10x wrong.
- TikTok refuses requests from here. TikTok clips are a manual pull; say so instead of retrying.

Skill sync:
- The account copies of the skills (synced read-only at `/root/.claude/skills/synced/…`) can drift from
  the repo. Before editing a skill, diff it against the synced copy. If both changed, three-way merge from
  the last shared commit, ask the producer about real contradictions, then send `.skill` packages to upload.

Each run's open items live in `runs/<RUN_ID>/OPEN.md`, not here.

Project in progress: audience data and a packaging skill — read `docs/PLATFORM_DATA_PLAN.md` when the
YouTube/Facebook data arrives or the producer asks about titles, thumbnails, retention or the misses log.
