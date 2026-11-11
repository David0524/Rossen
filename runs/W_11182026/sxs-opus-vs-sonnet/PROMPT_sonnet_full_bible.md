Experiment: write the full F2 Wed 11/18 bible with Sonnet doing all the writing and you directing it.

## Context

- **Setup first.** The test files live on branch `claude/nifty-darwin-xwzy6q`, not the default branch. Pull them in before anything else:

  ```bash
  git fetch origin claude/nifty-darwin-xwzy6q
  git checkout origin/claude/nifty-darwin-xwzy6q -- runs/W_11182026/sxs-opus-vs-sonnet
  ```

- This repo is the Rossen Reports workflow. Read `CLAUDE.md` first; it holds the standing producer rules.
- The approved outline is Kyle's outline for F2, airing Wed 11/18 and taping Fri 11/13. It's a one-story show, travel scams at every step of a trip, for a 55+ audience. File: `runs/W_11182026/sxs-opus-vs-sonnet/Outline F2 11_18 (Kyle).docx`. Convert it with `pandoc -t gfm` so the clip links survive.
- The clips are picked, timed and transcribed, so this is a FINAL-stage bible.
- The skill is `rossen-script-writer` (`.claude/skills/rossen-script-writer/SKILL.md`), plus the files it marks as required for every draft.
- An Opus bible for 11/18 was written separately, in another chat. Don't look for it or read it. This is a blind comparison.
- An earlier test in `runs/W_11182026/sxs-opus-vs-sonnet/` covers the tease and segment 1. Read its `README.md` for the lessons. Don't hand Sonnet that segment's text: the full bible starts fresh.

## Your role: director and fact-checker, not writer

- Spawn ONE Sonnet subagent (Agent tool, `model: "sonnet"`). Keep it alive across rounds with SendMessage, so it keeps its context.
- **Every word in the bible is Sonnet's.** You brief it, review its output, and send notes back. Sonnet makes every edit itself. You never edit the draft file.
- **Never give Sonnet example wording.** In the last test, Sonnet pasted a sample line from the brief almost word for word. Describe the move you want ("reaction first, then what the clip proved"; "repeat the killer number"). Don't write the line.

## Round 1: the full draft, with the voice brief from the start

Brief Sonnet to:

1. Read SKILL.md and every file it marks "every draft", plus `CLAUDE.md`.
2. Read for voice, not rules:
   - `.claude/skills/rossen-script-writer/references/producer-kit/rossen-voice.md`, all of it.
   - Jeff's aired livestream transcripts in `.claude/skills/rossen-pre-bible/references/transcripts/`: `jmUfTCWWDVM.txt` (his Google search scam segment, the closest match to this show), `Gh1ueu7ovlQ.txt` and `SjaMwcIQXyU.txt`.

   In the last test, this brief made the biggest difference to the voice.
3. Write the whole bible from the outline, in this order:
   - Title line.
   - Super tease: open package, command hook, stacked stakes, the objection turned around, the proof and fix promises.
   - All four stops: the Google numbers; the scammer who logged in and canceled her flight; the fake booking sites; the stolen suitcase and AirTag.
   - Each stop gets IT GETS WORSE turns, its own takeaway, and a bridge into the next.
   - The OmniWatch sponsor break, placed at a real story boundary, with a tease that names specific payoffs.
   - The closing payoff: Jeff's rule, three things to do and three never-dos.
   - The written close, then END OF SHOW.
4. Do the research it needs itself, from the outline's source links. Facts already confirmed in the last test:
   - The Points Guy's test: the "Primary US escalation line" was labeled for Swiss International Air Lines. Google's response: its anti-spam protections are "highly effective", and it removes scams once they're detected or reported.
   - Scam numbers sat on hacked pages at Rutgers, UC Merced and a federal health-IT (ONC) site, plus a spam page on Google.com. The Villages, Florida, and the City of Freeport, Texas hosted the files, but the article doesn't say they were hacked.
5. Run `scripts/check_bible.py <draft> --day wednesday --stories 1 --stage final` and clear every ERROR. A one-story umbrella show runs long against the per-story bands. That's expected; note it, don't cut to fit.
6. Build both deliverables with `build_bible.py` and `build_source_log.py`, then run `verify_format.py`.
7. Skip the skill's background review loop (`review-loop.md`). You are the reviewer.

## Rounds 2–3: your review

Read the draft against the outline and the sources. In the last test, Sonnet's misses were in facts and research, not voice. Check:

- **Unfinished research.** A company response left as an open decision when it can be found. An airline or detail left as "outline doesn't say".
- **Spoilers.** A runway or tease line that gives away what the clip reveals: an outcome, a refund, an arrest.
- **Source drift.** Every paraphrase of a clip against its transcript in the outline. Last time "never dealt with" became "never heard of".
- **Invented feelings or details** the source doesn't give. Second-person scenes are fine; made-up beats in them aren't.
- **Overclaims.** The Google demo is screen-recorded before a taped show, so nothing says "live" or "right now" about it. Refunds: the outline confirms the AmEx refund and the Frontier refund. The Delta family was only "promised" one.
- **Structure rules.** RED FLAG said about once a story. Every case ends on a takeaway. Every tease promise is paid off by name. The pre-sponsor tease names specifics. No outlet named outside its clip lead-in. Victims by first name or "this woman" / "this man", located by state. No unbooked guest named in black copy.
- **Lines from your own briefs.** Anything lifted from them gets rewritten.
- **Tease length.** The last tease ran 206 words against a 180 ceiling.

Send notes as problems plus the move to make, never replacement lines. Stop after round 3 even if small things remain, and list them.

## Known calls from the last test (carry these forward; flag any change)

- **Opening voicemail (outline Clip 1, ABC7).** The skill bans a clip marker in the tease, so it's a red OPEN PACKAGE cue there. Body clips are numbered 1..N from the first body clip, which shifts them one lower than the outline's numbering. Say so in the reply.
- **Jeff's Google demo (outline Clip 4).** A red screen-share / roll cue, not a numbered PLAY CLIP.
- **Alex Rivlin's Facebook video.** Orientation unknown. Marked HORIZONTAL until someone watches it; carry that as a red cue.
- **The "Decide In The Meeting" items.** Title, demo owner, AirTag link (Amazon or Apple), unbooked guest (Michelle Couch-Friedman of The Points Guy, or Amy Nofziger of AARP), the unwatched Instagram reel, and Jameel Reid's original video. These are the red open decisions. Carry two or three in the copy; list the rest in the reply.

## Deliverables

- Save to `runs/W_11182026/sonnet-bible/`:
  - `F2 Wed 11_18 -- <Working Title> -- SONNET.docx`
  - `F2 Wed 11_18 -- <Working Title> -- SONNET -- SOURCE LOG.docx`
  - Every draft round as `sonnet_draft_v1.md`, `sonnet_draft_v2.md` and so on.
  - `REVIEW_NOTES.md`, with your notes each round, verbatim.
- Send both .docx files in chat (SendUserFile). Commit and push to this session's branch. No Google Drive.
- Reply in chat, short:
  - Checker counts.
  - What you caught each round.
  - Anything still open.
  - Where Sonnet's voice was strongest and where it drifted.

  Put no model names in the commit message or the files beyond the "SONNET" label.
