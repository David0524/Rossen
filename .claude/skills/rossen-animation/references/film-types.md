# Film types: what each one is, and its reference build

Lengths here exclude the intro title card's pickup (add about 1.9 s). Everything is in `intro/`, 96 BPM on the bar grid, the case-file screen-print look, 1080×1920 at 24 fps unless noted. Every
film opens on the intro title card (CLAUDE.md). New films end on `liveEndCard(c, ['youtube', 'instagram', 'facebook'])` unless
the type says otherwise. Start from the reference build of the same type: copy it under a new name, never edit an approved
film in place (series episodes share recurring parts that must stay frame-identical).

| type | reference | length | ends on | build | check |
|---|---|---|---|---|---|
| Live-show tease | `wed-tease.js` (+ `references/tease*.md`) | 25–30 s + loop ×2 | the LIVE TODAY loop ×2 | `tools/build_wed_tease.sh` pattern | `tools/verify_wed_tease.py` pattern |
| Scam explainer | `officer.js` (story, music mix), `toll.js` + `vox.js` (evidence mark-up), `mychart.js` + `score_mychart.py` + `tools/vo_bed.sh` (the narrated VO-bed pattern) | 44–55 s | closing card | `tools/build_shorts.sh officer` pattern; toll: manual steps in README | `tools/sync_check.py`, safe pass |
| LIVE TODAY promo | `livepromo.js` (Zelle) | 15 s | the live card, the rubber stamp, the official logo | score + loudnorm + mux (README) | sync, safe pass |
| Quiz (play-along) | `quiz.js` (Scam or Legit) | ~60 s | recap, COMMENT YOUR SCORE, closing card | `tools/build_shorts.sh quiz` | sync, safe pass |
| Series: JEFF'S RULES | `rules.js` + `rules/template.json` + `rules/epNN.json` + `rules/epNN.js` | ~42 s | closing card | `tools/build_shorts.sh rulesN` | `tools/verify_rules.py`, recurring parts vs ep01 |
| Series: WHAT WOULD YOU DO? | `wwyd.js` + `wwyd/template.json` + `wwyd/epNN.json` + `wwyd/epNN.js` | ~45–53 s | closing card | `tools/build_shorts.sh wwydN` | `tools/verify_wwyd.py` |
| Deals roundup + Stories | `deals.js`, `stories.js`, `deals/deals.json` | ~55 s; Stories 5 s loops | closing card (Reel); last page (Stories) | `tools/build_deals.sh` | `tools/verify_deals.py`, `tools/verify_stories.py` |
| LIVE TODAY loop | `liveloop.js` + `rossen-loop-<day>.html` (`window.SHOW`) | 5 s, seamless | itself | render `--all`, mux `out/rossen-loop/loop_norm.wav` | first frame follows the last; platforms row |
| Opener / title sequence | `casefile.js` (16:9 and 9:16, `VERT`), `rossen-title-sequence.html` | 15–20 s | the official logo | README "Opener" sections | still logo, safe pass (9:16) |

## Live-show tease
The full chapter is `references/tease.md` (with `tease-timeline.md`, `tease-build.md`). A tease teases: the show gives the
answers. Ends on the loop ×2, never on the closing card.

## Scam explainer
- **Shape**: bait · trap · theft · fix, 3–5 bars each (craft.md §7), one caption per bar, the host's first appearance as a turn
  (the key moves to major), the protection line held two bars, then the rubber stamp and the closing card.
- **Evidence** (VOX_STUDY.md): the scam's artifact (text, email, page) is the evidence on the board; Jeff marks it up one clue
  per bar, each with a different mark (highlighter under the words, a circle, a pointer, an underline); never over a letter.
  VOX_STUDY's "camera pushes in on each mark" and "slow push" happen only between captions (at the bar change, as the
  transition into the next mark), never while a caption is up; its on-twos advice is rejected.
- **One sourced number** at most, with `out/<film>/sources.txt`; verified at build time.
- **Two or three signature transitions** on story turns (the dive through the circled link, the pull-back to a map pin…).
- **Audio**: a music mix (-16 LUFS) by default. If Jeff will narrate, make a voiceover bed instead (craft.md §8: no melodic
  lines in the voice range, -23 LUFS, stems, a timed VO script). No current film combines narration with the title card and
  closing card: take the story structure from `officer.js`, the bed from `score_mychart.py` + `tools/vo_bed.sh` (MyChart itself
  predates both cards and ends on the bare logo), and add both cards.
- The toll explainer moved puppets on twos; that is now rejected (everything on ones).

## LIVE TODAY promo
Six bars: the hook object from frame 0, the danger, the loss, Jeff's magnifier on the tell, the LIVE TODAY card (logo, LIVE
TODAY, time, day, Jeff), the stamp lifting onto the still official logo. Brand names only as plain system-font text.

## Quiz
Each round: SHOW (1 bar) · PAUSE with an 8-beat countdown (2) · REVEAL (verdict on beat 1, a flag highlighted and labelled
every two beats) (2) · TAKEAWAY (2). The phone never moves while there's something to read. The title is the answer pads.

## Series episodes (JEFF'S RULES, WHAT WOULD YOU DO?)
- Only the data (`epNN.json`) and the episode's own scenes (`epNN.js`) are new. `buildTimeline()` enforces the template's
  bar counts; a new optional template field must be inert for earlier episodes (they must render and score bit-identically:
  re-render ep01 and compare).
- New puppets: an episode may load them via `window.EP_ASSETS`; cut them with a `tools/cut_*.py` like the others.
- An episode may set `endPlatforms` (use all three for new episodes).
- The intro title card rule applies to new episodes, but **no mechanism exists yet** in either series: `buildTimeline()` has
  fixed bar counts and the verify scripts don't know a pickup. The first new episode must add it: an optional `intro` field in
  `epNN.json` (absent in earlier episodes), drawn by the series script before TITLE with the timeline offset by the pickup (as
  `INTRO` in `wed-tease.js`), the score and hits shifted the same way (`T0`), and the verify script's times offset. Earlier
  episodes must still render and score bit-identically. Ask the user before building it, since it changes the recurring open.
- Bar counts: `rules/template.json` and `wwyd/template.json` are authoritative (END is 3 bars in both).
- **Recurring parts are approved as they are**, even where they predate the readability rules (the rules END's tilted
  FOLLOW FOR stamp landing from 1.25×): don't change them silently. New scenes follow craft.md §0; tell the user about the
  conflict and ask whether to modernize the recurring parts (which would change every episode that re-renders).
- `tools/build_shorts.sh` needs a case line added by hand for each new episode (and its default list updated).
- WWYD: options in the order WRONG · CLOSE · RIGHT; the right answer is revealed last (`revealOrder`).

## Deals roundup
Everything on screen comes from `deals/deals.json` (names, exact price strings, codes, the price-check time, disclosure,
credit, CTA per platform). Percent off is computed from whole cents. Product photos are drawn untouched and need a rights
check. Each deal gets three bars (photo + name; regular price; DEAL stamp + deal price + strike, sticker on beat 2). The fine
print holds still a full bar. Stories are 5 s loops with only the arrow and a small Jeff bob moving.

## LIVE TODAY loop
Every motion periodic in 5 s (2 bars), so the last frame flows into the first; the music is the same cue for every airtime
(`score_loop.py`, three cycles rendered, the middle one kept). `window.SHOW = { time, day, platforms }`. The time card always
keeps the approved 5PM card's size. The approved beat pulse (4.5–6 %) is the one place text pulses. Re-rendering a loop
invalidates every tease built on it: re-decode its frames, remake that tease's masks, rebuild the tease.

## Opener / title sequence
16:9 and 9:16 from one script (`VERT` flag, per-scene layouts; re-lay out, never crop). "The show is starting" must be clear by
second 3. The official logo ends it, untouched and still.
