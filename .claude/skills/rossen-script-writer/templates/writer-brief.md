# Writer brief (fill in the <> fields; send as the writer subagent's prompt)

Facts and moves only. Never paste example wording into this brief: it gets
copied almost word for word.

---

You are writing the teleprompter bible for Rossen Reports (host Jeff Rossen, a
consumer-protection show for a 55+ audience): <SHOW> <Day> <M/DD>, taped <date>.
<Story count and shape>. <Guest or "no guest">. <Number> sponsor break(s),
<sponsor>. Stage: <DRAFT or FINAL>. Every word of the bible is yours. I'm the
director and fact-checker. I'll send notes in rounds, and you'll make every edit
yourself.

## Read first, all of it

1. `<repo>/CLAUDE.md`.
2. The skill: `<skill dir>/SKILL.md`, and every file it marks "every draft",
   plus `references/clip-contract.md`, `running-orders.md` and `docx-format.md`.
3. Voice. Read these for how Jeff actually talks, not for rules:
   `references/producer-kit/rossen-voice.md` (all of it), and the aired livestream
   transcripts in the rossen-pre-bible skill's `references/transcripts/`:
   `Gh1ueu7ovlQ.txt`, `SjaMwcIQXyU.txt` and `<topic match>.txt`. Notice his
   reaction-first buttons, the repeated killer number, direct address, the
   objection he turns around, and short punches.
4. The approved outline: `<path>`. Its clips are locked.
5. The research packet: `<path>`. Use only the facts in it. Where it lists a trap,
   the copy must avoid it. Where it gives a corrected in or out point, use that one.

Do not open <other drafts or earlier bibles for this show>.

## Write the whole bible, in this order

<The show's shape, from the outline: title line; super tease (open package,
command hook, stacked stakes, the objection turned around, the proof and fix
promises, about 180 words at most); each story or stop with its IT GETS WORSE
turns, its own takeaway and a bridge; the sponsor break at a real story boundary
with a tease that names specific payoffs; the protection list; the written close;
END OF SHOW.> JEFF PLEASE NOTE comments where the skill calls for them, and two or
three red open decisions from the packet.

## Then

- Save as `<run>/bible/draft_v1.md`.
- Run `<skill dir>/scripts/check_bible.py <draft> --day <day> --stories <n> --stage <stage>`
  and clear every ERROR. <If one long story: it runs long against the per-story
  bands; note it, don't cut to fit.>
- Write the source log markdown (format in `build_source_log.py`'s docstring) at
  `<run>/bible/sources.md`.
- Don't build the .docx and don't run the review loop yet.
- Reply with the checker's error and warning counts and the warnings, your tease
  word count, and anything you couldn't confirm.
