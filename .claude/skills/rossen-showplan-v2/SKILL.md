---
name: "rossen-showplan-v2"
description: "ShowPlan V2 — stage 2 of the Rossen Reports v2 workflow (PreBible V2 → ShowPlan V2 → Bible V2 → Review V2). Builds the Show Plan: a shared Google Doc of bullets where producers plan, edit and fact-check the show together before the bible is written. Deep research, every clip found with a real link, every claim checked, then hands off to rossen-clips-v2 to download and timecode the clips. Afterward, handles producer edits and comments IN PLACE — never rebuilds the doc. Use whenever the user asks to build, update, or work through a show plan, says \"make the plan for Wednesday,\" approves stories from a pitch sheet, or leaves comments on a plan for Claude. Do NOT use for pitching stories (rossen-prebible-v2) or writing the bible (rossen-bible-v2)."
---

# ShowPlan V2

Stage 2 of 4. The Show Plan is where Kyle and David **plan, edit and check** the show
together. It is a Google Doc of bullets — easy to see, easy to edit — that becomes the
bible. It is not the bible: no teleprompter formatting, no Jeff-voice prose.

| File | Load when |
|---|---|
| `templates/wednesday.html` / `templates/friday.html` | Building a plan. Structure of record. |
| `references/plan-rules.md` | Every build. What each section must contain. |
| `scripts/gdocs.py` | Every Drive/Docs action: create, read, comments, in-place edits. |

## Where this runs

- **Claude Code on the Mac (full version).** Uses `scripts/gdocs.py` for everything,
  including in-place edits and comment replies. Clips V2 runs here too.
- **claude.ai chat (research and first build).** No `gdocs.py` (no Google login in the
  sandbox). Use the Google Drive connector instead: search for the show folder, create
  the plan by uploading the HTML as a Google Doc, and read it back with the connector's
  read tool. The connector **cannot edit a doc in place**, so in chat:
  - Build the plan once. Do not rebuild it after producers have opened it.
  - For later changes, read the doc and comments, then tell the user exactly which
    lines to change — or hand the edit to Claude Code.
  - Clips V2 can't run in chat (video sites are blocked); list the clip links and say
    the download/timecode step runs in Claude Code.

## Inputs

- The approved stories from the PreBible V2 sheet (in the show's Drive folder), or the
  user's list: "Keep Story A, Option 3 for B, keep C."
- Sponsors for that date (production calendar, if available).
- Clip links already found in PreBible V2 — they carry forward.

## Where it lives

Drive: `Show Plan Demo/<Weekday Mon D, YYYY>/Show Plan — <Weekday Mon D, YYYY>`.
Find-or-create the folder with `gdocs.py folder`, create the doc once with
`gdocs.py create`. **Create it once. Never create a second copy of the same plan.**

## Step 1 — research (thorough, and it takes time)

This is the deepest research pass on the approved stories. Expect it to take many
searches. For each story:

- **Verify every figure against its primary source** and record the link. A claim is
  ☑ only when you loaded the source and it says that. Otherwise ☐.
- **Find the people.** Threat stories are built from people in escalation order —
  who they are, what happened, the twist. Search named victims, plaintiffs,
  whistleblowers, creators, investigators. If none exist, say so in Open questions.
- **Find every clip.** Each video line needs a real URL. Paths in order of yield:
  press coverage that links the original post; local station video pages; the
  Internet Archive TV News Archive (search what was said on air); YouTube.
  "Not pulled yet," "find a clip," and empty links are not acceptable in a finished
  plan — either you found it, or the Open questions say exactly what couldn't be
  found and what you tried.
- **Fairness lines.** Every named company accused of something gets its response or
  denial on the same line, sourced.
- **Guests.** The reporter who covered it, or the investigator who did the work.

## Step 2 — build the doc

Follow the template and `references/plan-rules.md`:

- Run of show: headlines only, with the clip IDs under each.
- Tease: every story teased, strongest first, a hold-back last. Every tease figure
  must match a ☑ claim.
- Stories: Hook · How it works · People (with Turn + Video [ID] + [ID] IN/OUT) ·
  Stills & screen share · Claims · Graphics · Guest · Protect yourself · Open questions.
- Sponsor segues: one per booked sponsor, after Story 1 or Story 2 only, each
  bridging from the story before it.
- Good-news closer: never a scam; demo-shaped.
- Open questions (whole show): only things research genuinely couldn't settle.

Write HTML from the template, then `gdocs.py create`.

## Step 3 — hand off to Clips V2

Run `rossen-clips-v2` on the plan. It downloads every clip, transcribes it, picks in and
out points, checks still frames, uploads cuts to the show folder, and writes each
`[ID] IN/OUT: —` line in place. A clip that fails its check is replaced with another
found clip, and the plan line is updated in place.

The plan goes to the producers **after** Clips V2 has run.

## Step 4 — working the plan with the producers

Once producers are in the doc, the doc is theirs. Rules:

1. **Never rebuild, never re-create, never overwrite.** All changes are in place with
   `gdocs.py replace`, anchored on text that is unique (include the clip ID or the
   full line).
2. **Read before every edit.** `gdocs.py read` the current doc first; producers may
   have changed the line you're about to touch. If `replace` says NOT FOUND, re-read
   and anchor on what's there now.
3. **Comments are instructions.** `gdocs.py comments` lists open comments. For each:
   do the work, edit in place, then `gdocs.py reply --resolve` with one line saying
   what changed. If you can't do it, reply with why and leave it open.
4. **Their words win.** If a producer rewrote a line, don't restore yours.

## Handoff

When the producers say the plan is locked, `rossen-bible-v2` writes the bible from
the current doc.
