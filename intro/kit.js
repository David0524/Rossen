'use strict';
// Shared drawing kit for the Rossen films: crayon shapes, ink stamps, tags, bills, the scammer, Jeff's arm and the magnifier.
const INK = '#2b2622', RED = '#d63a31', PAPER = '#ece8dc';
const SKIN = '#e8a474', JACKET = '#3d3a38', SHIRT = '#b9c9de';
const IMG = {};
function loadImg(k, src) { return new Promise((res, rej) => { const im = new Image(); im.onload = () => { IMG[k] = im; res(); }; im.onerror = () => rej(new Error('missing ' + src)); im.src = src; }); }
function alphaBox(im) {   // trim transparent margins so the logo is centred on its ink, not its canvas
  const o = document.createElement('canvas'); o.width = im.width; o.height = im.height; const g = o.getContext('2d'); g.drawImage(im, 0, 0);
  const d = g.getImageData(0, 0, o.width, o.height).data; let x0 = o.width, y0 = o.height, x1 = 0, y1 = 0;
  for (let y = 0; y < o.height; y++) for (let x = 0; x < o.width; x++) if (d[(y * o.width + x) * 4 + 3] > 8) { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
  return x1 >= x0 ? [x0, y0, x1 - x0 + 1, y1 - y0 + 1] : [0, 0, im.width, im.height];
}

// ---------------- small helpers ----------------
const seg = (t, a, b) => clamp((t - a) / (b - a), 0, 1);
const easeOutBack = x => { const c1 = 1.9, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };
function rrPts(x, y, w, h, r, n = 6) {
  const p = [], cs = [[x + w - r, y + r, -Math.PI / 2], [x + w - r, y + h - r, 0], [x + r, y + h - r, Math.PI / 2], [x + r, y + r, Math.PI]];
  for (const [cx, cy, a0] of cs) for (let k = 0; k <= n; k++) { const a = a0 + k / n * Math.PI / 2; p.push([cx + Math.cos(a) * r, cy + Math.sin(a) * r]); }
  return p;
}
function densify(pts, step = 14, close = true) {
  const out = []; const n = pts.length;
  for (let i = 0; i < (close ? n : n - 1); i++) { const a = pts[i], b = pts[(i + 1) % n], L = Math.hypot(b[0] - a[0], b[1] - a[1]), m = Math.max(1, Math.ceil(L / step));
    for (let k = 0; k < m; k++) out.push([lerp(a[0], b[0], k / m), lerp(a[1], b[1], k / m)]); }
  if (!close) out.push(pts[n - 1]); return out;
}
function bbox(pts) { let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9; for (const [x, y] of pts) { x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y); } return [x0 - 4, y0 - 4, x1 - x0 + 8, y1 - y0 + 8]; }
// crayon-filled shape in the reference's coloured-pencil manner: flat fill, dense same-hue strokes, paper flecks, dark wobbly outline
// Matches the reference drawing's hand: waxy colored-pencil fill (two stroke layers + paper flecks) and a heavy, wobbly
// dark outline (about 1.5x the old weight), so drawn props sit next to the Jeff illustration without looking pasted in.
const OUTLINE_K = 1.5;
function shape(c, pts, fill, seed, o = {}) {
  const P = polyPath(pts), box = bbox(pts);
  c.fillStyle = fill; c.fill(P);
  hatch(c, P, box, { angle: o.angle ?? 1.05, gap: o.gap ?? 2.8, len: o.len ?? 17, jitter: 5, color: o.hc || shade(fill, .24), alpha: o.ha ?? .5, width: 1.4, seed });
  hatch(c, P, box, { angle: (o.angle ?? 1.05) - .45, gap: 5.5, len: 11, jitter: 5, color: tint(fill, .35), alpha: .28, width: 1.2, seed: seed + 5 });
  grain(c, P, box, Math.min(1600, box[2] * box[3] / (o.fleck ?? 26)), '#fbf7ee', o.fa ?? .5, seed + 3, 1.7);
  if (o.outline !== false) { const pp = densify(pts, 11, o.open ? false : true), lw = (o.lw ?? 5) * OUTLINE_K;
    crayon(c, pp, o.ink || '#26211d', lw, seed + 9, !o.open); crayon(c, pp, o.ink || '#26211d', lw * .45, seed + 19, !o.open); }
  return P;
}
function line(c, pts, w, seed, col = INK) { crayon(c, densify(pts, 10, false), col, w * 1.25, seed, false); }
function capsulePts(a, b, r, n = 10) {  // stadium around segment a-b
  const ang = Math.atan2(b[1] - a[1], b[0] - a[0]), p = [];
  for (let k = 0; k <= n; k++) { const t = ang - Math.PI / 2 + k / n * Math.PI; p.push([b[0] + Math.cos(t) * r, b[1] + Math.sin(t) * r]); }
  for (let k = 0; k <= n; k++) { const t = ang + Math.PI / 2 + k / n * Math.PI; p.push([a[0] + Math.cos(t) * r, a[1] + Math.sin(t) * r]); }
  return p;
}
function text(c, s, x, y, font, col, align = 'center') { c.font = font; c.textAlign = align; c.textBaseline = 'middle'; c.fillStyle = col; c.fillText(s, x, y); }

// ---------------- stamps (ink impressions), cached ----------------
const CACHE = {};
function inkTexture(g, w, h, seed, amount) {   // knock paper back through the ink: specks and dry drags
  const r = rng(seed); g.save(); g.globalCompositeOperation = 'destination-out';
  for (let i = 0; i < amount; i++) { g.globalAlpha = .25 + r() * .6; const s = .8 + r() * 2.6; g.fillRect(r() * w, r() * h, s, s * (.5 + r())); }
  g.lineCap = 'round'; for (let i = 0; i < amount / 60; i++) { g.globalAlpha = .18 + r() * .25; g.lineWidth = 1 + r() * 3; const x = r() * w, y = r() * h; g.beginPath(); g.moveTo(x, y); g.lineTo(x + 30 + r() * 90, y + (r() - .5) * 14); g.stroke(); }
  g.restore();
}
function liveBadge(w, h, dotOn = true) {
  const key = `live${w}x${h}${dotOn}`; if (CACHE[key]) return CACHE[key];
  const pad = 20, o = document.createElement('canvas'); o.width = w + pad * 2; o.height = h + pad * 2; const g = o.getContext('2d'); g.translate(pad, pad);
  const r = rng(w), pts = rrPts(0, 0, w, h, h * .22, 8).map(([x, y]) => [x + (r() - .5) * 2.4, y + (r() - .5) * 2.4]);
  g.fillStyle = RED; g.fill(polyPath(pts));
  const fs = h * .66; g.font = `${fs}px Stamp`; g.textAlign = 'left'; g.textBaseline = 'middle';
  const tw = g.measureText('LIVE').width, dotR = h * .15, gap = h * .2, total = dotR * 2 + gap + tw, x0 = (w - total) / 2;
  g.fillStyle = PAPER; g.fillText('LIVE', x0 + dotR * 2 + gap, h * .56);
  if (dotOn) { g.fillStyle = PAPER; g.beginPath(); g.arc(x0 + dotR, h * .5, dotR, 0, TAU); g.fill(); }
  else { g.globalCompositeOperation = 'destination-out'; g.lineWidth = Math.max(2, h * .035); g.beginPath(); g.arc(x0 + dotR, h * .5, dotR * .8, 0, TAU); g.stroke(); g.globalCompositeOperation = 'source-over'; }
  g.setTransform(1, 0, 0, 1, 0, 0); inkTexture(g, o.width, o.height, w + 7, w * h / 160);
  o.dot = [pad + x0 + dotR, pad + h * .5, dotR];
  return CACHE[key] = o;
}
function scamStamp() {
  if (CACHE.scam) return CACHE.scam;
  const w = 470, h = 170, pad = 24, o = document.createElement('canvas'); o.width = w + pad * 2; o.height = h + pad * 2; const g = o.getContext('2d'); g.translate(pad, pad);
  g.strokeStyle = RED; g.lineJoin = 'round'; const r = rng(5);
  const frame = (ins, lw) => { g.lineWidth = lw; g.beginPath(); rrPts(ins, ins, w - ins * 2, h - ins * 2, 14, 5).forEach(([x, y], k) => { x += (r() - .5) * 2; y += (r() - .5) * 2; k ? g.lineTo(x, y) : g.moveTo(x, y); }); g.closePath(); g.stroke(); };
  frame(4, 9); frame(18, 3.5);
  g.fillStyle = RED; g.font = '118px Stamp'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText('SCAM!', w / 2, h * .54);
  g.setTransform(1, 0, 0, 1, 0, 0); inkTexture(g, o.width, o.height, 77, 1500);
  return CACHE.scam = o;
}
// stamp animation: drops from above scale, lands at tLand, small squash after
function drawStamp(c, img, x, y, rot, scale, t, tLand, spat = .5) {
  const a = seg(t, tLand - .12, tLand); if (t < tLand - .12) return;
  const s = t < tLand ? lerp(1.55, 1, easeIn(a)) : t < tLand + .12 ? 1 + .04 * Math.exp(-(t - tLand) * 30) * Math.cos((t - tLand) * 60) : 1;
  c.save(); c.translate(x, y); c.rotate(rot); c.scale(scale * s, scale * s); c.globalAlpha = t < tLand ? .25 + .6 * a : .93;
  c.drawImage(img, -img.width / 2, -img.height / 2); c.restore();
  if (t >= tLand && t < tLand + spat) {   // ink spatter at impact
    const r = rng(Math.round(x + y)); c.save(); c.fillStyle = RED; c.globalAlpha = .75 * (1 - seg(t, tLand + spat * .5, tLand + spat));
    for (let k = 0; k < 11; k++) { const ang = r() * TAU, d = (img.width * scale * .5) * (.75 + r() * .45), s2 = 2 + r() * 5; c.beginPath(); c.arc(x + Math.cos(ang) * d, y + Math.sin(ang) * d * .45, s2, 0, TAU); c.fill(); }
    c.restore();
  }
}

// ---------------- price tags and bills, cached ----------------
function priceTag(oldP, newP, seed) {
  const key = 'tag' + seed; if (CACHE[key]) return CACHE[key];
  const w = 230, h = 132, pad = 14, o = document.createElement('canvas'); o.width = w + pad * 2; o.height = h + pad * 2; const g = o.getContext('2d'); g.translate(pad, pad);
  const pts = [[34, 0], [w, 0], [w, h], [34, h], [0, h * .72], [0, h * .28]];
  shape(g, pts, '#ecd39e', seed, { hc: '#c9a86a', ha: .35, lw: 4.5 });
  g.fillStyle = PAPER; g.beginPath(); g.arc(22, h / 2, 8, 0, TAU); g.fill(); g.strokeStyle = INK; g.lineWidth = 3; g.stroke();
  text(g, oldP, 132, 34, '38px Marker', '#4a3f38');
  g.strokeStyle = RED; g.lineWidth = 5; g.lineCap = 'round'; const tw = g.measureText(oldP).width; const r = rng(seed);
  g.beginPath(); g.moveTo(132 - tw / 2 - 8, 38 + r() * 4); g.lineTo(132 + tw / 2 + 8, 30 - r() * 4); g.stroke();
  g.beginPath(); g.moveTo(132 - tw / 2 - 6, 30); g.lineTo(132 + tw / 2 + 6, 40); g.stroke();
  text(g, newP, 134, 92, '62px Marker', RED);
  return CACHE[key] = o;
}
function bill() {
  if (CACHE.bill) return CACHE.bill;
  const w = 96, h = 46, pad = 8, o = document.createElement('canvas'); o.width = w + pad * 2; o.height = h + pad * 2; const g = o.getContext('2d'); g.translate(pad, pad);
  shape(g, rrPts(0, 0, w, h, 5, 3), '#9cc98a', 31, { hc: '#6f9f5f', lw: 3.2 });
  g.strokeStyle = '#4f7d44'; g.lineWidth = 2; g.strokeRect(7, 6, w - 14, h - 12);
  g.fillStyle = '#c7e3b8'; g.beginPath(); g.ellipse(w / 2, h / 2, 14, 15, 0, 0, TAU); g.fill(); g.stroke();
  text(g, '$', w / 2, h / 2 + 1, '24px Marker', '#3f6b36');
  return CACHE.bill = o;
}

// ---------------- props ----------------
// The villain: a little con man. Fedora with a red band, popped collar on a slate-blue trench coat, red scarf,
// curly mustache, bandit mask. ~125 px tall at s = 1, origin between the feet.
const COAT = '#56647b', COAT_D = '#3c4758', HAT = '#2f3440', SKIN2 = '#efc3a0';
function scammer(c, x, y, s, o = {}) {
  const { mood = 0, run = null, look = 0, t = 0, flip = 1 } = o;
  c.save(); c.translate(x, y); c.scale(s * flip, s);
  if (mood > .5) c.translate(Math.sin(t * 90) * 2.2, 0);
  const lp = run == null ? 0 : run;
  const leg = (dx, ph) => { const lift = run == null ? 0 : Math.max(0, Math.sin(ph)) * 10, fw = run == null ? 0 : Math.cos(ph) * 9;
    shape(c, capsulePts([dx, -24], [dx + fw, -6 - lift], 7, 6), '#343a47', 100 + dx, { lw: 3 });
    shape(c, ellPts(dx + fw + 6, -5 - lift, 13, 7, 0, 16), '#23262e', 102 + dx, { lw: 3 }); };
  leg(-13, lp); leg(13, lp + Math.PI);
  if (!o.noSack) {
    shape(c, ellPts(-42, -58, 25, 29, -.3, 26), '#c9a063', 110, { hc: '#9a7440', lw: 3.2 });
    line(c, [[-52, -85], [-42, -81], [-32, -87]], 3, 111); text(c, '$', -43, -54, '28px Marker', '#6b4a22');
  }
  // trench coat (egg), belt, lapels, buttons
  shape(c, ellPts(0, -50, 38, 38, 0, 40), COAT, 112, { hc: COAT_D, lw: 3.4 });
  c.save(); c.clip(ellPath(0, -50, 38, 38)); c.fillStyle = COAT_D; c.fillRect(-40, -46, 80, 8); c.restore();
  line(c, [[-4, -80], [-12, -50], [-2, -22]], 2.4, 121, '#26211d'); c.fillStyle = '#26211d'; for (const yy of [-58, -34]) { c.beginPath(); c.arc(6, yy, 2.6, 0, TAU); c.fill(); }
  // head
  shape(c, ellPts(0, -96, 25, 24, 0, 30), SKIN2, 113, { hc: '#d9a07a', lw: 3.2 });
  // popped collar + red scarf
  shape(c, [[-30, -86], [-10, -78], [-24, -60]], COAT, 114, { hc: COAT_D, lw: 3 });
  shape(c, [[30, -86], [10, -78], [24, -60]], COAT, 115, { hc: COAT_D, lw: 3 });
  shape(c, rrPts(-20, -80, 40, 10, 5, 2), '#c8503f', 116, { lw: 2.6 });
  shape(c, [[8, -72], [18, -72], [16, -52], [8, -54]], '#c8503f', 117, { lw: 2.4 });
  // bandit mask + eyes
  shape(c, rrPts(-26, -108, 52, 15, 7, 3), '#1f1c22', 118, { hc: '#111', lw: 2.4 });
  const ew = mood > .5 ? 7.5 : 6.2, eh = mood > .5 ? 7.5 : 4.6;
  for (const ex of [-11, 11]) { c.fillStyle = '#fbf7ee'; c.beginPath(); c.ellipse(ex, -100.5, ew, eh, 0, 0, TAU); c.fill();
    c.fillStyle = '#111'; c.beginPath(); c.arc(ex + look * 3, -100 + (mood > .5 ? 0 : .8), mood > .5 ? 2.3 : 2.6, 0, TAU); c.fill(); }
  // curly mustache
  c.save(); c.strokeStyle = '#2b2320'; c.lineWidth = 4; c.lineCap = 'round';
  c.beginPath(); c.moveTo(0, -87); c.quadraticCurveTo(-8, -91, -15, -86); c.quadraticCurveTo(-19, -82, -15, -80); c.stroke();
  c.beginPath(); c.moveTo(0, -87); c.quadraticCurveTo(8, -91, 15, -86); c.quadraticCurveTo(19, -82, 15, -80); c.stroke(); c.restore();
  if (mood > .5) { c.fillStyle = '#3a2226'; c.beginPath(); c.ellipse(0, -79, 5.5, 6.5, 0, 0, TAU); c.fill();
    c.fillStyle = '#9bd0f0'; for (const [dx, dy] of [[32, -104], [-34, -100]]) { c.beginPath(); c.moveTo(dx, dy - 10); c.quadraticCurveTo(dx + 6, dy, dx, dy + 4); c.quadraticCurveTo(dx - 6, dy, dx, dy - 10); c.fill(); } }
  else line(c, [[-5, -80], [2, -78], [8, -81]], 2.2, 122);
  // fedora with a red band
  shape(c, ellPts(0, -114, 36, 7, 0, 24), HAT, 123, { hc: '#1d2028', lw: 3 });
  shape(c, [[-20, -114], [-17, -134], [-4, -130], [0, -136], [4, -130], [17, -134], [20, -114]], HAT, 124, { hc: '#1d2028', lw: 3 });
  shape(c, rrPts(-20, -122, 40, 7, 2, 2), '#c8503f', 125, { lw: 2 });
  if (mood > .5) { line(c, [[-34, -58], [-50, -84]], 7, 126, COAT); line(c, [[34, -58], [52, -86]], 7, 127, COAT);
    shape(c, ellPts(-51, -88, 7, 7, 0, 12), SKIN2, 128, { lw: 2.4 }); shape(c, ellPts(53, -90, 7, 7, 0, 12), SKIN2, 129, { lw: 2.4 }); }
  c.restore();
}
// where the scammer is at time t (world, feet), and what he's doing
function ik(a, b, l1, l2, down = 1) {
  let dx = b[0] - a[0], dy = b[1] - a[1], d = Math.hypot(dx, dy); const dd = clamp(d, 1, l1 + l2 - .5);
  const ang = Math.atan2(dy, dx), cosA = clamp((l1 * l1 + dd * dd - l2 * l2) / (2 * l1 * dd), -1, 1), A = Math.acos(cosA);
  const e1 = [a[0] + Math.cos(ang + A) * l1, a[1] + Math.sin(ang + A) * l1], e2 = [a[0] + Math.cos(ang - A) * l1, a[1] + Math.sin(ang - A) * l1];
  const e = (e1[1] > e2[1]) === (down > 0) ? e1 : e2; const hx = e[0] + Math.cos(Math.atan2(b[1] - e[1], b[0] - e[0])) * l2, hy = e[1] + Math.sin(Math.atan2(b[1] - e[1], b[0] - e[0])) * l2;
  return [e, [hx, hy]];
}
function glassRing(c, L, R, seed) {
  c.save(); c.lineCap = 'round';
  c.strokeStyle = 'rgba(255,255,255,.75)'; c.lineWidth = 7; c.beginPath(); c.arc(L[0], L[1], R * .72, Math.PI * 1.08, Math.PI * 1.42); c.stroke();
  c.lineWidth = 4; c.beginPath(); c.arc(L[0], L[1], R * .72, Math.PI * 1.5, Math.PI * 1.58); c.stroke(); c.restore();
  const outer = ellPts(L[0], L[1], R + 12, R + 12, 0, 60), inner = ellPts(L[0], L[1], R, R, 0, 60);
  const ring = new Path2D(); ring.addPath(polyPath(outer)); ring.addPath(polyPath([...inner].reverse()));
  c.fillStyle = '#34302d'; c.fill(ring, 'evenodd');
  hatch(c, ring, [L[0] - R - 14, L[1] - R - 14, 2 * R + 28, 2 * R + 28], { gap: 3, len: 10, color: '#6f6b67', alpha: .5, seed });
  crayon(c, outer, INK, 4.5, seed + 1, true); crayon(c, inner, INK, 3.5, seed + 2, true);
}
function handleTo(c, from, L, R, seed) {   // grip at the hand, telescoping chrome shaft to the ring
  const ang = Math.atan2(L[1] - from[1], L[0] - from[0]), d = Math.hypot(L[0] - from[0], L[1] - from[1]) - R - 10;
  const at = u => [from[0] + Math.cos(ang) * u, from[1] + Math.sin(ang) * u];
  const segs = [[40, d, 5.5, '#c9ccd2'], [40, d * .66 + 40 * .34, 7.5, '#b4b8bf'], [-22, 40, 11, '#8a5a3c']];
  if (d > 60) { shape(c, capsulePts(at(40), at(d), 5.5, 6), '#c9ccd2', seed, { lw: 3.5, hc: '#9a9ea6' }); shape(c, capsulePts(at(40), at(40 + (d - 40) * .5), 7.5, 6), '#b4b8bf', seed + 1, { lw: 3.5, hc: '#8d9199' }); }
  shape(c, capsulePts(at(-24), at(44), 11, 8), '#8a5a3c', seed + 2, { lw: 4, hc: '#6b4128' });
  shape(c, capsulePts(at(40), at(46), 12, 4), '#d8b35a', seed + 3, { lw: 3 });
}
function speedLinesAt(c, x, y, ang, seed, a) {
  const r = rng(seed); c.save(); c.strokeStyle = INK; c.globalAlpha = .55 * a; c.lineWidth = 3; c.lineCap = 'round';
  for (let k = 0; k < 4; k++) { const o = (k - 1.5) * 28 + (r() - .5) * 10, L = 50 + r() * 40, px = x - Math.sin(ang) * o, py = y + Math.cos(ang) * o;
    c.beginPath(); c.moveTo(px, py); c.lineTo(px + Math.cos(ang) * L, py + Math.sin(ang) * L); c.stroke(); }
  c.restore();
}

// ---------------- scene assembly ----------------
function sparkle(c, x, y, u, seed) {
  const r = rng(seed); c.save(); c.strokeStyle = '#f2b84b'; c.lineWidth = 4; c.lineCap = 'round'; c.globalAlpha = 1 - u;
  for (let k = 0; k < 6; k++) { const a = k / 6 * TAU + r() * .3, d0 = 16 + u * 40, d1 = d0 + 18 * (1 - u) + 6; c.beginPath(); c.moveTo(x + Math.cos(a) * d0, y + Math.sin(a) * d0); c.lineTo(x + Math.cos(a) * d1, y + Math.sin(a) * d1); c.stroke(); }
  c.restore();
}
// logo: paper drop to centre, soft bounce, then perfectly still from 13.95

// ---------- additions for the title sequence ----------
// word stamp: 'fill' = solid ink block with the word knocked out, 'outline' = double frame + inked word
function wordStamp(word, o = {}) {
  const { color = RED, style = 'outline', size = 150, padX = 46, padY = 26, seed = 11 } = o;
  const key = `ws_${word}_${color}_${style}_${size}`; if (CACHE[key]) return CACHE[key];
  const m = document.createElement('canvas').getContext('2d'); m.font = `${size}px Stamp`; const tw = m.measureText(word).width;
  const w = Math.ceil(tw + padX * 2), h = Math.ceil(size * 1.12 + padY * 2), pad = 26, cv = document.createElement('canvas'); cv.width = w + pad * 2; cv.height = h + pad * 2;
  const g = cv.getContext('2d'); g.translate(pad, pad); const r = rng(seed);
  const rough = (ins, rr) => rrPts(ins, ins, w - ins * 2, h - ins * 2, rr, 5).map(([x, y]) => [x + (r() - .5) * 2.4, y + (r() - .5) * 2.4]);
  g.font = `${size}px Stamp`; g.textAlign = 'center'; g.textBaseline = 'middle';
  // solid, like a sticker slapped on: nothing underneath shows through the word
  if (style === 'fill') { g.fillStyle = color; g.fill(polyPath(rough(0, h * .2))); g.fillStyle = '#fbf8f0'; g.fillText(word, w / 2, h * .54); }
  else { g.fillStyle = '#fbf8f0'; g.fill(polyPath(rough(0, 18))); g.strokeStyle = color; g.lineJoin = 'round'; g.lineWidth = size * .075; g.stroke(polyPath(rough(size * .04, 16))); g.lineWidth = size * .03; g.stroke(polyPath(rough(size * .15, 10))); g.fillStyle = color; g.fillText(word, w / 2, h * .54); }
  g.setTransform(1, 0, 0, 1, 0, 0); inkTexture(g, cv.width, cv.height, seed + 5, cv.width * cv.height / 400);
  return CACHE[key] = cv;
}
// paper: warm stock with fibres and flecks, drawn once
function paperTexture(Wd, Hd, base = PAPER, seed = 3) {
  const o = document.createElement('canvas'); o.width = Wd; o.height = Hd; const g = o.getContext('2d'); g.fillStyle = base; g.fillRect(0, 0, Wd, Hd);
  const r = rng(seed);
  for (let i = 0; i < Wd * Hd / 90; i++) { g.globalAlpha = .05 + r() * .09; g.fillStyle = r() < .5 ? '#fffdf6' : '#b9b09e'; const s = .6 + r() * 1.8; g.fillRect(r() * Wd, r() * Hd, s, s); }
  g.lineCap = 'round'; for (let i = 0; i < 900; i++) { g.globalAlpha = .035 + r() * .05; g.strokeStyle = r() < .5 ? '#a89f8c' : '#fffaf0'; g.lineWidth = .6 + r(); const x = r() * Wd, y = r() * Hd, a = r() * TAU, L = 6 + r() * 26; g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + Math.cos(a) * L * .5 + (r() - .5) * 6, y + Math.sin(a) * L * .5 + (r() - .5) * 6, x + Math.cos(a) * L, y + Math.sin(a) * L); g.stroke(); }
  return o;
}
// Jeff: the reference drawing cut into body + two legs, placed at (x, gy) = between the feet, scale k.
const AX = 252, AY = 694, SHOULDER = [398, 468];
function drawArm(c, Sw, hand, k, seed = 500) {
  const l1 = 96 * k, l2 = 88 * k, [E, H] = ik(Sw, hand, l1, l2, 1), r = 29 * k;
  shape(c, capsulePts(Sw, E, r, 10), JACKET, seed, { hc: '#6f6b67', ha: .5, fleck: 30, fa: .5 });
  shape(c, capsulePts(E, H, r * .95, 10), JACKET, seed + 1, { hc: '#6f6b67', ha: .5, fleck: 30, fa: .5 });
  const ang = Math.atan2(H[1] - E[1], H[0] - E[0]), cuff = [H[0] - Math.cos(ang) * 6 * k, H[1] - Math.sin(ang) * 6 * k];
  shape(c, ellPts(cuff[0], cuff[1], 9 * k, r * .95, ang, 18), SHIRT, seed + 2, { lw: 3.5 });
  return { E, H, hc: [H[0] + Math.cos(ang) * 16 * k, H[1] + Math.sin(ang) * 16 * k], ang };
}
function drawHand(c, hc, mode, dir, k, seed = 520) {
  const f = k / .94;
  if (mode === 'thumb') shape(c, capsulePts([hc[0] - 4 * f, hc[1] - 6 * f], [hc[0] - 6 * f, hc[1] - 46 * f], 10.5 * f, 8), SKIN, seed + 1, { lw: 4, hc: '#c98457' });
  shape(c, rrPts(hc[0] - 24 * f, hc[1] - 21 * f, 48 * f, 44 * f, 17 * f, 4), SKIN, seed, { lw: 4.5, hc: '#c98457' });
  if (mode === 'point') { const b0 = [hc[0] + dir[0] * 10 * f, hc[1] + dir[1] * 10 * f], tip = [hc[0] + dir[0] * 64 * f, hc[1] + dir[1] * 64 * f]; shape(c, capsulePts(b0, tip, 10.5 * f, 8), SKIN, seed + 1, { lw: 4, hc: '#c98457' }); }
  else { c.strokeStyle = INK; c.lineWidth = 2.5; c.lineCap = 'round'; for (let q = 0; q < 2; q++) { c.beginPath(); c.moveTo(hc[0] + 6 * f, hc[1] - 8 * f + q * 12 * f); c.lineTo(hc[0] + 18 * f, hc[1] - 8 * f + q * 12 * f); c.stroke(); } }
}
// Shoes: the reference drawing stops at the trouser hems, so each leg gets a shoe (sprite px).
const FOOT = 24;   // shoe sole sits this far below the hem
const SHOES = [{ x0: 118, x1: 238, toe: -1, seed: 540 }, { x0: 276, x1: 384, toe: 1, seed: 545 }];
function shoe(c, S, lift) {
  const y0 = AY - 16 - lift, y1 = AY + FOOT - lift, m = (S.x0 + S.x1) / 2, w = S.x1 - S.x0, tx = S.toe * 14;
  const pts = [[S.x0 + 6 + (S.toe < 0 ? tx : 0), y1], [S.x1 - 6 + (S.toe > 0 ? tx : 0), y1], [S.x1 + (S.toe > 0 ? tx : 0), y1 - 14], [S.x1 - 6, y0 + 4], [S.x0 + 6, y0 + 4], [S.x0 + (S.toe < 0 ? tx : 0), y1 - 14]];
  shape(c, pts, '#4a3326', S.seed, { lw: 6, hc: '#2e1f17', ha: .5, fleck: 90, fa: .25 });
  c.save(); c.strokeStyle = 'rgba(255,240,220,.55)'; c.lineWidth = 5; c.lineCap = 'round'; c.beginPath(); c.moveTo(m + S.toe * w * .18 - 16, y0 + 12); c.lineTo(m + S.toe * w * .18 + 10, y0 + 10); c.stroke(); c.restore();
  crayon(c, [[S.x0 + 4 + (S.toe < 0 ? tx : 0), y1 - 5], [S.x1 - 4 + (S.toe > 0 ? tx : 0), y1 - 5]], '#1e1712', 3, S.seed + 4, false);
}
// body copy without the arm that hangs at his side (right of the jacket's inner crayon line), for poses with a raised arm
function bodyNoArm() {
  if (IMG.bodyNoArm) return IMG.bodyNoArm;
  const o = document.createElement('canvas'); o.width = IMG.body.width; o.height = IMG.body.height; const g = o.getContext('2d'); g.drawImage(IMG.body, 0, 0);
  g.globalCompositeOperation = 'destination-out'; g.beginPath(); g.moveTo(392, 470);
  for (let y = 470; y <= 622; y += 4) g.lineTo(388 + (y - 487) * 7 / 118 + 5, y);
  g.lineTo(470, 622); g.lineTo(470, 470); g.closePath(); g.fill();
  g.globalCompositeOperation = 'source-over';
  crayon(g, Array.from({ length: 40 }, (_, k) => { const y = 480 + k * 3.6; return [388 + (y - 487) * 7 / 118 + 3, y]; }), '#26211d', 7, 560, false);
  return IMG.bodyNoArm = o;
}
// p: {bob, tilt, sx, sy, lift:[l, r], hop}; armFn(Sw, rest) -> null | {mode, hand, dir}. (x, gy) = between the soles.
function drawJeff(c, x, gy, k, p = {}, armFn = null) {
  const { bob = 0, tilt = 0, sx = 1, sy = 1, lift = [0, 0], hop = 0 } = p;
  const base = c.getTransform();
  c.save(); c.translate(x, gy - hop); c.rotate(tilt); c.scale(k * sx, k * sy); c.translate(0, -FOOT);
  const M = base.inverse().multiply(c.getTransform());
  const Mb = M.translate(-AX, -AY - bob), sp = Mb.transformPoint(new DOMPoint(...SHOULDER)), rp = Mb.transformPoint(new DOMPoint(430, 640));
  const Sw = [sp.x, sp.y], A = armFn ? armFn(Sw, [rp.x, rp.y]) : null;
  c.drawImage(IMG.legL, -AX, -AY - lift[0]); c.drawImage(IMG.legR, -AX, -AY - lift[1]);
  c.save(); c.translate(-AX, -AY); shoe(c, SHOES[0], lift[0]); shoe(c, SHOES[1], lift[1]); c.restore();
  c.drawImage(A ? bodyNoArm() : IMG.body, -AX, -AY - bob);
  c.restore();
  if (!A) return armFn ? { Sw } : null;
  const arm = drawArm(c, Sw, A.hand, k);
  if (A.mode !== 'glass') drawHand(c, arm.hc, A.mode, A.dir, k);
  return { ...arm, mode: A.mode, Sw };
}
// half-plane polygon clip (Sutherland-Hodgman, one edge): keep points with dot(p - q, n) >= 0
function clipHalf(poly, q, n) {
  const out = [], side = p => (p[0] - q[0]) * n[0] + (p[1] - q[1]) * n[1];
  for (let i = 0; i < poly.length; i++) { const a = poly[i], b = poly[(i + 1) % poly.length], sa = side(a), sb = side(b);
    if (sa >= 0) out.push(a); if ((sa >= 0) !== (sb >= 0)) { const u = sa / (sa - sb); out.push([a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u]); } }
  return out;
}
// text that never runs past its box: shrinks the font until the measured width fits maxW
function fitText(c, s, x, y, size, family, col, maxW, align = 'center') {
  c.font = `${size}px ${family}`; const w = c.measureText(s).width; const sz = w > maxW ? Math.floor(size * maxW / w) : size;
  text(c, s, x, y, `${sz}px ${family}`, col, align); return sz;
}
