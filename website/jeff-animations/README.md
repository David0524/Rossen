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

## Files

| File | What it is |
|---|---|
| `jeff-puppet.js` | The puppet rig, the props (pencil, scissors, zip trolley, thumb) and the four gags. Plain JS with no dependencies. |
| `jeff-puppet.css` | Canvas layering, the coupon strip, phone padding for the receipt gag, print rules |
| `art/jeff.json` | Part positions and joint pivots, in art units |
| `art/jeff-*.webp` | The six cut-out parts: about 52 KB in total, cut from `intro/assets/casefile/jeff_*.png` at 42 % |
| `preview-desktop.mp4` | Screen recording of all four on a copy of the live page |
| `HANDOFF_PROMPT.md` | What to paste to the Claude account that runs the site |
