# The tease timeline

All times are on the loop's grid: **96 BPM, 4/4, key D** (`score_loop.py`). One beat = 0.625 s, one bar = 2.5 s, 24 fps
(a beat is 15 frames, a bar 60). `at(bar, beat)` in `vertkit.js` is film time (bar 0-based, beat 1-based). Video time = film
time + the intro pickup.

## The bar map (the approved Wednesday layout: 12 bars + a 3-beat pickup = 31.875 s, then the loop ×2 = 41.875 s)

| bars | what | notes |
|---|---|---|
| pickup (−3 beats, 1.875 s) | intro title card | logo + title + day/time, still from frame 0; exits by fade + dive/dissolve (≤ 0.5 s) ending as bar 0's card lands |
| 0–2 | story 1 (3 bars) | the hook object on screen from bar 0's first frame; bar 0 carries the first card |
| 3–5 | story 2 (3 bars) | equal bars per story |
| 6–8 | story 3 (3 bars) | bar 8 beat 3 = the musical stop (a button hit on A), beat 4 = silence, picture frozen |
| 9–10 | the promise (2 bars) | Jeff; a 6-word promise card needs 2 bars to be read twice |
| 11 | handoff | the loop's own page: its pieces land on beats 1–4 (masks), full loop frames from beat 4 + 0.1 s |
| then | loop ×2 | appended by stream copy |

Two stories → 3 bars each is still right; four stories → 2 bars each only if every card is 4 words or fewer. Tease length
target 25–30 s (the brief's range), total with the loop ×2 about 35–42 s. Pick the length the story needs; whole bars only.

## Timing constants (from the approved build)

| thing | value |
|---|---|
| landing lead (`SLAM`) | 0.14 s: anything that lands starts moving 0.14 s early and arrives exactly on the beat |
| card landing | from 1.05× to 1× over `SLAM`, then still (`capPop`); both lines of a two-line card land together |
| card on screen | from its land to the next card's land − `SLAM`, or to the start of a transition |
| read-twice rule | still time ≥ 2 × words ÷ 5 s (300 wpm) |
| simple transition (push, zoom into a rect) | 0.34–0.36 s, ending at the next downbeat − `SLAM` |
| signature transition (smoke billow, stage-flat swing) | ≤ 0.52 s, ending at the next downbeat − `SLAM`, never two in a row |
| cut | on a card's land − `SLAM` (the cut and the card land together) |
| intro | 3 beats; card still until beat 3 (1.25 s), words fade over 0.22 s, dissolve over the last beat |
| handoff | loop frames 60–119 under bar 11; pieces on beats 1, 2, 3, 3, 4, 4 (logo, LIVE TODAY, time card + day, LIVE ON row + Jeff) |

## Card rules (check each one on the contact sheet)

- 72 px Bowlby One SC (`Stamp`), cream on black for line 1, cream on blue for line 2; two lines at most; ≤ 16 characters a line.
- `fitText` must not squeeze a line below 85 % of its natural width; measure with PIL and the font file before building.
- Card band: content y ≈ 330–540 (screen 330–600). Scene content starts below content y ≈ 560.
- No prop label lands on a card's downbeat: move it to beat 2 (the site's name, the ticket total).
- At most a card plus one prop label on screen.

## Sound on the grid

- Composed bars in D; each story gets its own mood (sneaky pizzicato/clarinet; slick muted trumpet/glock/xylophone; tense
  spiccato/horns; confident D major brass for Jeff). Change the cue at each act.
- The last composed bar before the promise stops on A (the loop's dominant) on beat 3; beat 4 is gated to silence.
- The loop's own cue (decoded from the delivered loop file) plays under the last two tease bars, so the join is sample-exact;
  the composed layer fades to zero 0.1 s before the join.
- Every synced hit goes in `hits.json` (video time); the verify pass measures them on the final mp4.
