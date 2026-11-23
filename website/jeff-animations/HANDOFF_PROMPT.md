Paste the text below to the Claude account that has the rossenreports.com code, and attach `jeff-animations.zip`.

---

Please add the cartoon-Jeff animations in the attached `jeff-animations.zip` to rossenreports.com. Everything you need is in its README.md. In short:

1. Unzip it, then copy the contents of its `jeff/` folder into a folder named `jeff/` at the site root: `jeff-puppet.js`, `jeff-puppet.css`, `jeff.json` and the six `jeff-*.webp` files.
2. In `index.html`, add `<link rel="stylesheet" href="jeff/jeff-puppet.css">` in `<head>`, right after the Font Awesome stylesheet.
3. Add `<script defer src="jeff/jeff-puppet.js" data-art="jeff/"></script>` right before `</body>`, after the page's own inline script.

Don't change any existing markup or styles. The script hooks into `.circular`, `.receipts .tape .tot`, `.closer` and `.signup-done` as they are on the live page today. If any of those class names have changed in the repo, tell me which ones before you adapt the script.

Before deploying, check a preview build:
- On desktop and on a phone-width window, Jeff should:
  - zip-line along the rule under the hero;
  - circle "25+" on the receipt after it prints;
  - cut the dashed line above "Clip this";
  - give a thumbs up after a test signup shows "You're in".
- Check that there are no console errors from `jeff-puppet.js`.
- With "reduce motion" turned on in the OS, the zip line shouldn't appear, and the other three should show still.

Deploy it as a normal Vercel deploy. Then send me the preview URL to approve before it goes to production.
