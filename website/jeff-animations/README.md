# Cartoon Jeff on rossenreports.com

Four small animations of the cartoon Jeff for the live site. He is the same jointed paper-cutout puppet used in the social videos: the art comes from the approved case-file Jeff in `intro/assets/casefile/` on the `claude/gallant-fermi-t8urdw` branch. He's drawn live on a canvas from 6 cut-out parts, so the whole package is about 80 KB and stays sharp on retina screens.

Watch `preview-desktop.mp4` (21 s) to see all four.

| # | Where | What happens | Why it's there |
|---|---|---|---|
| 1 | The double rule between the hero and "This Week's Circular" | Jeff rides a zip-line trolley along the rule, left to right, waving the mic. Once per page view. | Leads the eye from the hero into the deals |
| 2 | "He's got the receipts" | After the receipt prints, Jeff pops up and circles **25+** with a giant pencil. He stays, and the circle stays. | Marks the receipt's punchline |
| 3 | Top of the closer, above "Clip this. Save all year." | A dashed coupon line. Jeff walks along it with giant scissors and cuts it, then stands at the end. | Acts out "clip this" |
| 4 | Every "You're in. Check your inbox!" | Jeff pops up beside the message with a thumbs up. | Confirms the signup |

The site's own motion rule ("every effect explains or confirms something") held for all four.

## Install (two lines, plus a folder)

1. Copy this folder's `jeff-puppet.js`, `jeff-puppet.css` and everything in `art/` into one folder at the site root named **`jeff/`**:
   ```
   jeff/jeff-puppet.js
   jeff/jeff-puppet.css
   jeff/jeff.json
   jeff/jeff-head.webp  jeff-torso.webp  jeff-armL.webp  jeff-armR.webp  jeff-legL.webp  jeff-legR.webp
   ```
2. In `index.html`, add the stylesheet after the Font Awesome `<link>` in `<head>`:
   ```html
   <link rel="stylesheet" href="jeff/jeff-puppet.css">
   ```
3. Add the script just before `</body>`, after the page's own script:
   ```html
   <script defer src="jeff/jeff-puppet.js" data-art="jeff/"></script>
   ```

You don't need to change any markup. The script finds `.circular`, `.receipts .tape .tot`, `.closer` and `.signup-done` itself, and it adds the coupon strip at the top of `.closer` on its own.

## Behaviour and safety

- **Reduced motion.** The script reads the site's existing `motion` class on `<html>`, which is only set when the visitor hasn't asked for reduced motion. Without it, the zip line is skipped and the other three are drawn in their final, still state.
- **Accessibility.** Every canvas is `aria-hidden` and `pointer-events: none`, so it never blocks a link, the form or text selection.
- **Failure.** If the script fails to load, the page is exactly as it is today. Each gag is wrapped on its own, so one error can't stop the others.
- **Timing.**
  - The receipt gag waits for the site's own receipt print (`.tape.armed.in`).
  - The zip line waits about 1.4 s after page load, so the hero's entrance plays first.
  - Nothing runs until its section scrolls into view.
- **Cost.**
  - The art is loaded lazily the first time a gag is about to play.
  - Each animation runs for 1.5–4 s, then stops. Nothing loops in the background.
- **Phones.** On a phone Jeff stands under the receipt and reaches up-right. The CSS adds 104 px of bottom padding to that section on screens up to 860 px wide, so he has room.
- **Print.** All of it is hidden when the page is printed.

## Switching gags off or tuning them

- Keep only some of the gags: `data-gags="receipt,cut,thumb"` on the script tag. The default is all four.
- Sizes are set per gag in `jeff-puppet.js` as `s` (CSS px per art unit): zip `.34` (`.25` on phones), receipt up to `.38`, scissors `.36` (`.26` on phones).
- Zip-line speed: `T` in `gagZip` (3.6 s desktop, 2.8 s phone).
- The pencil mark is graphite (`GRAPHITE`), not red. The site reserves red for prices and warnings.

## Next step (optional): make the scissors cut something real

Right now the scissors gag cuts a line that's drawn on a canvas, and nothing on the page changes. The upgrade below makes the cut piece actually come away from the page. Do this after the four gags above are live and approved.

**The idea.** When Jeff reaches the end of the line, the strip of navy page above the cut becomes a loose flap.
- It's pinned at the right end, where Jeff is standing.
- Its left end drops a few pixels and tips down.
- Behind it, a sliver of bare white paper shows through.
- The cut edge is hard and straight, like a guillotine trim. It is not torn or soft.

It should look like Jeff really clipped the page.

**The hook is already in `jeff-puppet.js`.** When the cut finishes, the script:
- adds the class `jeff-cut-done` to `.closer`;
- fires a bubbling `jeff:cut` event on it, with `detail = { still, lineY, strip }`.

`lineY` is the cut's height in px from the top of the strip. `still` is `true` when the visitor prefers reduced motion. In that case, show the end state with no movement.

**How to build it:**

1. **Structure.** Inside `.jeff-cut`, add a `div.jeff-flap` that covers the strip from the top down to the cut line. Its `height` is `lineY` px, read from the event detail or measured. Paint it with the same navy and halftone as `.closer`:
   ```css
   background-color: var(--navy-deep);
   background-image: var(--tex-halftone);
   ```
   It must line up with the section's background so it's invisible until it moves. Use `background-attachment` / `background-position` relative to `.closer` so the dots don't jump.
2. **The paper behind.** Give `.jeff-cut` a `::before` covering the same area in bare paper: `var(--thermal)` (`#FBFAF6`), or plain white.
   - Add a thin inner shadow along its top edge, for example `inset 0 6px 8px -6px rgba(0,0,0,.45)`, so it reads as a layer under the page.
   - Keep it hidden (under the flap) until the cut.
3. **The motion**, on `jeff:cut` and only when `!detail.still`:
   - Set `transform-origin: right bottom` on the flap.
   - Animate `transform: rotate(-2.2deg) translateY(5px)` over about 450 ms, with a small overshoot and settle, the way every stop in the films does. Something like `cubic-bezier(.3,1.5,.5,1)`, or a keyframe that goes to -2.6deg and back to -2.2deg.
   - The wedge of white that opens on the left is the "glimpse." At its widest it should be about 10–14 px on desktop and 8 px on phones. Never let it reach the "Clip this" headline.
4. **The edge.** The flap's bottom edge stays crisp, with no blur and no border-radius.
   - Add a 1 px light line on that edge so the cut catches the light: `box-shadow: 0 1px 0 rgba(244,239,227,.5)`.
   - Add a soft drop shadow under the flap onto the white, for example `filter: drop-shadow(0 3px 3px rgba(0,0,0,.35))`.
5. **Jeff stays put.** The Jeff canvas (`.jeff-stage` inside the strip) must sit above the flap and must not rotate with it: give it a higher `z-index` and keep it a sibling of the flap, not a child. He stands at the pinned end, so nothing he's touching moves.
6. **Optional beat.** After the flap settles, Jeff can glance down at the gap: tilt his head about 0.1 rad for half a second, then back to centre. Add it in `gagCut` as a short `play()` after `cutDone`. Do it only if it reads well; skip it if it feels busy.
7. **Reduced motion and print.**
   - When `detail.still` is true, apply the final transform with no transition.
   - In `@media print`, hide `.jeff-flap` and the `::before`.

**Check before shipping:**
- No layout shift: the flap is decoration, `aria-hidden`, and `pointer-events: none`.
- The email field and button in `.closer` still work.
- The white sliver never covers text.
- At phone width the gap stays small and the flap doesn't overflow the screen sideways (`overflow: hidden` on `.jeff-cut` if needed).

## Files

| File | What it is |
|---|---|
| `jeff-puppet.js` | The puppet rig, the props (pencil, scissors, zip trolley, thumb) and the four gags. Plain JS with no dependencies. |
| `jeff-puppet.css` | Canvas layering, the coupon strip, phone padding for the receipt gag, print rules |
| `art/jeff.json` | Part positions and joint pivots, in art units |
| `art/jeff-*.webp` | The six cut-out parts: about 52 KB in total, cut from `intro/assets/casefile/jeff_*.png` at 42 % |
| `preview-desktop.mp4` | Screen recording of all four on a copy of the live page |
| `HANDOFF_PROMPT.md` | What to paste to the Claude account that runs the site |
