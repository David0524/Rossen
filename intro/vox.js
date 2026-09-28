'use strict';
/* Vox-inspired kit (see VOX_STUDY.md), on top of printkit.js and vertkit.js:
   - onTwos(t): the drawing clock for puppets and cut-out graphics. 12 drawings a second, anchored to the beat, so a new
     drawing lands exactly on every beat (a beat is 15 frames at 24 fps: drawings on frames 0, 2, ..., 14 of each beat).
     Text and the camera use the smooth clock t.
   - a 2.5D camera: layers at different depths, pushed in through a focus point.
   - evidence mark-up: highlighter (behind the words), a hand-drawn circle, a pointer line, and a marker held by Jeff. */

const onTwos = t => { const b = Math.floor(t / BEAT + 1e-6) * BEAT; return b + Math.floor((t - b) * FPS / 2 + 1e-6) * 2 / FPS; };

// cam: { x, y, z } = the focus point (content coords) and zoom. A layer at depth d moves and scales by d of the camera move:
// d = 1 is the evidence plane, d < 1 sits behind it (moves less), d > 1 sits in front (moves more).
function camLayer(c, cam, d, fn) {
  const s = 1 + (cam.z - 1) * d, fx = SCX + (cam.x - SCX) * d, fy = SCY + (cam.y - SCY) * d;
  c.save(); c.translate(SCX, SCY); c.scale(s, s); c.translate(-fx, -fy); fn(); c.restore();
}
function camPoint(cam, d, x, y) { const s = 1 + (cam.z - 1) * d, fx = SCX + (cam.x - SCX) * d, fy = SCY + (cam.y - SCY) * d; return [SCX + (x - fx) * s, SCY + (y - fy) * s]; }

// a highlighter stroke: flat yellow ink with ragged ends, drawn BEHIND the words it marks. u 0..1 = how far it has swept.
function highlighter(c, x, y, w, h, u, seed) {
  if (u <= 0) return; const r = rng(seed), ww = w * Math.min(1, u);
  const P = [[x - 6, y + r() * 4], [x + ww, y + r() * 3], [x + ww + 6, y + h * .5], [x + ww, y + h - r() * 3], [x - 4, y + h - r() * 4], [x - 10, y + h * .5]];
  ink(c, P, YEL, seed, { amp: 3, reg: false });
}
// a hand-drawn circle (a marker loop that overshoots its start), u 0..1 = how much has been drawn
function circleMark(c, cx, cy, rx, ry, u, col = BLUE, w = 10, seed = 1) {
  if (u <= 0) return; const r = rng(seed), a0 = -2.3, span = TAU * 1.12 * Math.min(1, u), n = Math.max(2, Math.round(60 * Math.min(1, u)));
  c.save(); c.strokeStyle = col; c.lineWidth = w; c.lineCap = 'round'; c.lineJoin = 'round'; c.beginPath();
  for (let i = 0; i <= n; i++) { const a = a0 + span * i / n, k = 1 + .05 * Math.sin(a * 2 + seed) + .03 * (i / n); const x = cx + Math.cos(a) * rx * k, y = cy + Math.sin(a) * ry * k; i ? c.lineTo(x, y) : c.moveTo(x, y); }
  c.stroke(); c.restore();
}
function pointer(c, a, b, u, col = BLK, w = 6) {   // a pointer line with an arrowhead at b
  if (u <= 0) return; const x = lerp(a[0], b[0], Math.min(1, u)), y = lerp(a[1], b[1], Math.min(1, u)), ang = Math.atan2(b[1] - a[1], b[0] - a[0]);
  c.save(); c.strokeStyle = col; c.lineWidth = w; c.lineCap = 'round'; c.beginPath(); c.moveTo(a[0], a[1]); c.lineTo(x, y); c.stroke();
  if (u >= 1) { c.beginPath(); c.moveTo(b[0], b[1]); c.lineTo(b[0] - 26 * Math.cos(ang - .45), b[1] - 26 * Math.sin(ang - .45)); c.moveTo(b[0], b[1]); c.lineTo(b[0] - 26 * Math.cos(ang + .45), b[1] - 26 * Math.sin(ang + .45)); c.stroke(); }
  c.restore();
}
// a big marker held by Jeff: a keyed body from his hand to the tip (like the magnifier's handle), cap colour = ink colour
function markerProp(c, hand, tip, col) {
  const a = Math.atan2(tip[1] - hand[1], tip[0] - hand[0]), L = Math.hypot(tip[0] - hand[0], tip[1] - hand[1]);
  c.save(); c.translate(hand[0], hand[1]); c.rotate(a);
  block(c, rrPts(-20, -17, L - 30, 34, 14, 4), BLK, 7801, { kw: 0, key: false });
  block(c, rrPts(-14, -11, L - 42, 22, 10, 4), col === YEL ? YEL : CHIP, 7802, { kw: 0, key: false });
  block(c, [[L - 34, -15], [L - 8, -7], [L, 0], [L - 8, 7], [L - 34, 15]], col, 7803, { kw: 4 });
  c.restore();
}
