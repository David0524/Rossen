# Handoff — 11/04 Wednesday (F2) outline w/ videos

Prepared Oct 27, 2026 from a claude.ai chat. Covers everything from the show plan
upload onward. Open this first, then `runs/2026-11-04_F2/`.

## Where things stand

| Phase | Status |
|---|---|
| Phase 1 — Beats | **Done.** `outline.md` (Stage: beats) and `11_04_OUTLINE_F2.docx` built and checked. |
| Phase 2 — Videos | **Not started.** Stopped at Checkpoint 0 (preflight). Must run in Claude Code on your own computer. |

## Inputs

- `Show_Plan___Wed_Oct_28__2026.docx` — the approved show plan (3 stories, OmniWatch after story 1).
- `jeff_approval.md` — written from your chat message: approved stories = the attached plan, no guest.
- Show: Wednesday, November 4, 2026. **The plan is headed "Wed Oct 28" — confirm the label.**

## Checkpoint 1 — beat table with lanes

Lanes: Search (find or verify), Manual (native TikTok post is the pick),
Show-produced (team shoots it), Drop. "—" = not a clip beat.

| Beat | Who | Clip | Lane |
|---|---|---|---|
| 11-04-A1 | You (the hook) | HAVE · VERTICAL BROLL, TikTok @financeunfolded (Oct 2021) | Manual |
| 11-04-A2 | Alex Pearlman (Apr 2023) | HAVE · VERTICAL, TikTok @pearlmania500 | Manual |
| 11-04-A3 | Barbara, 88, Bradenton FL (date unknown) | HAVE · HORIZONTAL, FOX 13 news page | Search |
| A4 | How it works | JEFF | — |
| 11-04-A5 | Susan Udvance, Illinois (~Oct 2025) | HAVE · HORIZONTAL, ABC7 Chicago (dbBueUfmuSI) | Search (verify) |
| 11-04-A6 | Eugene and Ann Breznock, CA (~Oct 2021) | HAVE · HORIZONTAL, CBS Sacramento (80djyAsS-YE) | Search (verify) |
| 11-04-A7 | Delaware man, unnamed (~Apr 2026) | HAVE · HORIZONTAL, CBS News California (1Grj5UvPLwo) | Search (verify) |
| A8 | California father and son, charged | STILLS (CA AG release) | — |
| 11-04-A9 | Find yours (missingmoney.com) | DEMO | Show-produced |
| 11-04-B1 | FTC and 20 states (Oct 27, 2026) | HAVE · HORIZONTAL, ABC News / GMA | Search |
| 11-04-B2 | Lori Hartline, Oklahoma (Mar 2024) | HAVE · VERTICAL, TikTok @moreperfectunion | Manual |
| 11-04-B3 | William Anderson, Butler County OH (Oct 2022) | HAVE · HORIZONTAL, LOCAL 12 news page | Search |
| 11-04-B4 | Lynda Swank, former DG employee (Nov 2022) | HAVE · HORIZONTAL, WHIO news page | Search |
| B5 | Still happening | JEFF | — |
| 11-04-C1 | Walmart's CEO on GMA (Oct 2026) | HAVE · HORIZONTAL, GMA (PQORnk7zuLc) | Search (verify) |
| 11-04-C2 | Paige, Sam's Club shopper (Oct 20, 2026) | HAVE · VERTICAL, TikTok @paigeanne80 | Manual |
| C3 | Costco perks | JEFF | — |

12 clip beats (top of the Wednesday 10–12 band): 4 manual, 7 search, 1 show-produced, 0 dropped.
Dates were read from TikTok post IDs and YouTube's approximate upload ages.

## Decisions the room owes (also on page one of the outline)

1. Plan labeled "Wed Oct 28" vs. show 11/4 — confirm.
2. **B repeat risk:** the 10/14 show ran a shelf-vs-register B naming Dollar General. The Oct 27 lawsuit is new; it's three weeks later.
3. **B tease gives away the hold-back** ("The shelf said $2.75. The register charged $5.") — same kind of line the producer cut on 10/14.
4. **C overlaps 8/7** ("10 Things Walmart Gives You FREE"). Keep C to the new Sam's Club bundle.
5. A has no news peg; most cases are 2021–2025 (each flagged "date it on air"). A runs 9 beats (the max).
6. A7's man is unnamed — get the name from the CBS clip.
7. A8 is a still — keep, or find a local package.
8. Story A is a "money you can claim" story, which the pre-bible marks off-list; Jeff approved it, and the scam half makes it fit.

Checker warnings left (all covered above): Barbara's date, the unnamed Delaware man,
B at 5 beats (2–4 expected), B1's Who is an institution.

The outline keeps the outline skill's ⚠️ markers (not CHECK) because
`check_outline.py` and the script writer look for that symbol.

## Checkpoint 0 — why Phase 2 stopped, and the fix

| Check | Result in chat sandbox | Fix (on your computer) |
|---|---|---|
| `rossen_harvest` package | Missing. Not in skills, the Oct 12 skills backup, or the workflow-update zip in Drive. | Most likely in Kyle's `rossen-clips-SHARE.zip` (22.9 MB, Drive, Jul 23). Unzip `harvest/` into the project root, or ask Kyle. |
| faster-whisper | Installed in the sandbox | `pip install -r harvest/requirements.txt` |
| Brave search key | Not set | brave.com/search/api; `export BRAVE_API_KEY=...` in your shell profile. Never in a doc or chat. |
| YouTube search | Works | — |
| YouTube captions | Bot-walled from the cloud sandbox (all yt-dlp clients and the transcript API tried) | Your connection usually works; else `export YTDLP_ARGS="--cookies-from-browser chrome"` |
| Audio downloads | Blocked from the sandbox | Same as captions |
| Prior runs for 11/4 | None (first run) | Nothing to fix |

Step-by-step: `runs/2026-11-04_F2/SETUP_PHASE2.md`. Check with `bash runs/2026-11-04_F2/preflight.sh` (seven lines, all OK).

## Next steps

1. Get `rossen_harvest` (Kyle's zip), set the Brave key, run preflight.
2. In Claude Code, from the folder holding `runs/` and `harvest/`:

> Use the rossen-story-outline skill, Phase 2 (rossen-pipeline), on
> runs/2026-11-04_F2/outline.md and the show plan in the same folder. Show: 11/4.
> Phase 1 is done and Checkpoint 1 is in HANDOFF.md. Resume at Checkpoint 0
> (preflight), then build beats.json (beat_id MM-DD-<story><row>; script_text =
> the row plus that beat's specifics from the show plan), and continue.
> Stop only on a priority-1 gap.

3. Settle the eight Decisions before the bible is written.

## What's in this zip

- `HANDOFF.md` — this file.
- `CHAT_LOG.md` — the chat from the show plan onward.
- `runs/2026-11-04_F2/` — show plan, jeff_approval.md, outline.md, 11_04_OUTLINE_F2.docx, SETUP_PHASE2.md, preflight.sh.
- `skills/` — copies of rossen-story-outline, rossen-pipeline, rossen-beat-extractor, rossen-query-generator, rossen-clip-grader, as used in this run (Oct 27, 2026). Use your installed copies if they're newer.
