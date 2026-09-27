'use strict';
/* THE REEL'S OWN FRAME (the open, the lineup and the end card): plain paper, one neutral bold, near-black, level type.
   It belongs to none of the four styles, so each style reads as its own world against it. */
const PLAIN = { paper: '#EFEDE8', ink: '#171717', ink2: '#5E5C58' };
function plainPaper(L, seed = 31) { const g = L.getContext('2d'); resetT(g); g.fillStyle = PLAIN.paper; g.fillRect(0, 0, W, H);
  grain(g, rectPath(0, 0, W, H), [0, 0, W, H], 3000, '#A9A59C', .09, seed, 1.2); grain(g, rectPath(0, 0, W, H), [0, 0, W, H], 800, '#FFFFFF', .5, seed + 1, 1.8);
  const v = g.createRadialGradient(W / 2, H / 2, H * .35, W / 2, H / 2, H * .8); v.addColorStop(0, 'rgba(60,55,45,0)'); v.addColorStop(1, 'rgba(60,55,45,.08)'); g.fillStyle = v; g.fillRect(0, 0, W, H); }
// type: solid near-black; a cut-paper lift (a soft offset shadow) under the big lines only
function plainType(c, s, x, y, size, maxW = 9999, o = {}) { const { col = PLAIN.ink, lift = 0 } = o; const sz = fitFont(c, s, 800, size, 'Bricolage', maxW);
  if (lift) { c.save(); c.filter = `blur(${lift * .7}px)`; textAt(c, s, x + lift * .5, y + lift, 800, sz, 'Bricolage', 'rgba(40,34,24,.2)'); c.restore(); }
  return textAt(c, s, x, y, 800, sz, 'Bricolage', col); }
