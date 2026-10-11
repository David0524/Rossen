# Revising an existing bible

Load when a marked-up bible comes back, or for any voice or length pass on an existing draft.

A marked-up bible coming back is as common as a new one. Do not regenerate the
document — **edit in place.** A rewrite loses the producer's accepted lines and
silently reverses decisions already made.

0. **Rewriting a whole bible** (not a targeted note): keep the formatting, the
   order, every fact, every cue, every guest line and the guests' timing.
   Rewrite Jeff's lines only. Truncate interviews so Jeff narrates the setup and
   the guest speaks at the three or four moments that need their voice. Flag
   factual problems as notes; never fix them silently.
1. **Read the whole bible first**, then locate what the note actually targets: a
   story, a beat, a header run, a length band, or the voice across the document.
2. **Change only that.** If a note says story 3 is long, cut story 3 — do not
   re-pitch story 2 or re-order the show.
3. **Watch the coupled constraints.** Cutting a story changes the clip count and
   the page total; cutting clips changes story 1's share of them; re-ordering
   stories moves the sponsor boundary. Re-check the tease block against any story
   that changed, since the tease restates each one.
4. **Preserve open decisions** that are still open. Close one only if the note
   closes it.
5. **Run `check_bible.py` on the revised file** and report what moved.
6. **Say what you changed and what you left**, briefly, in the chat reply. If a
   note cannot be followed without breaking a hard contract — the tease boundary,
   the marker format, a length band — say that instead of quietly splitting the
   difference.

For a voice or length pass across the whole document, work story by story and
re-run the checker after each, so a fix in one story does not push another out of
band.


## Promoting a DRAFT to FINAL

When the outline's clips are locked, convert in place: number every clip marker
in document order, fill each `OUT:` with the transcribed outcue from the
outline, confirm each orientation matches the clip picked, move the candidate
URL and timecodes into the source log under that clip number, and re-run
`check_bible.py --stage final`. Do not rewrite copy during the promotion except
where a setup line no longer matches what the locked clip shows.
