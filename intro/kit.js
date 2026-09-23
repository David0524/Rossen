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
function shape(c, pts, fill, seed, o = {}) {
  const P = polyPath(pts), box = bbox(pts);
  c.fillStyle = fill; c.fill(P);
  hatch(c, P, box, { angle: o.angle ?? 1.05, gap: o.gap ?? 3.4, len: o.len ?? 13, jitter: 4, color: o.hc || shade(fill, .22), alpha: o.ha ?? .45, width: 1.3, seed });
  grain(c, P, box, Math.min(900, box[2] * box[3] / (o.fleck ?? 55)), '#fbf7ee', o.fa ?? .45, seed + 3, 1.6);
  if (o.outline !== false) crayon(c, densify(pts, 12, o.open ? false : true), o.ink || INK, o.lw ?? 5, seed + 9, !o.open);
  return P;
}
function line(c, pts, w, seed, col = INK) { crayon(c, densify(pts, 10, false), col, w, seed, false); }
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
  g.globalCompositeOperation = 'destination-out';
  const fs = h * .66; g.font = `${fs}px Stamp`; g.textAlign = 'left'; g.textBaseline = 'middle';
  const tw = g.measureText('LIVE').width, dotR = h * .15, gap = h * .2, total = dotR * 2 + gap + tw, x0 = (w - total) / 2;
  g.fillText('LIVE', x0 + dotR * 2 + gap, h * .56);
  g.globalCompositeOperation = 'source-over';
  if (dotOn) { g.fillStyle = PAPER; g.beginPath(); g.arc(x0 + dotR, h * .5, dotR, 0, TAU); g.fill(); }
  else { g.globalCompositeOperation = 'destination-out'; g.lineWidth = Math.max(2, h * .035); g.beginPath(); g.arc(x0 + dotR, h * .5, dotR * .8, 0, TAU); g.stroke(); g.globalCompositeOperation = 'source-over'; }
  g.setTransform(1, 0, 0, 1, 0, 0); inkTexture(g, o.width, o.height, w + 7, w * h / 55);
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
function scammer(c, x, y, s, o = {}) {
  const { mood = 0, run = null, peek = 0, look = 0, t = 0, flip = 1 } = o;
  c.save(); c.translate(x, y); c.scale(s * flip, s);
  const shake = mood > .5 ? Math.sin(t * 90) * 2.2 : 0; c.translate(shake, 0);
  const lp = run == null ? 0 : run;
  // legs
  const leg = (dx, ph) => { const lift = run == null ? 0 : Math.max(0, Math.sin(ph)) * 10, fw = run == null ? 0 : Math.cos(ph) * 9;
    shape(c, capsulePts([dx, -26], [dx + fw, -6 - lift], 7, 6), '#3b3446', 100 + dx, { lw: 3.5 });
    shape(c, ellPts(dx + fw + 5, -5 - lift, 12, 7, 0, 16), '#26222c', 102 + dx, { lw: 3.5 }); };
  leg(-14, lp); leg(14, lp + Math.PI);
  // loot sack over the shoulder (behind body)
  if (!o.noSack) {
    shape(c, ellPts(-40, -64, 26, 30, -.3, 26), '#b58656', 110, { hc: '#8d6337', lw: 4 });
    line(c, [[-50, -92], [-40, -88], [-30, -94]], 3.5, 111);
    text(c, '$', -41, -60, '30px Marker', '#5b3a1e');
  }
  // body
  shape(c, ellPts(0, -54, 38, 44, 0, 40), '#6f5f8f', 112, { hc: '#554672' });
  // striped jumper band
  c.save(); c.clip(ellPath(0, -54, 38, 44)); c.fillStyle = 'rgba(40,34,48,.55)'; for (let k = 0; k < 3; k++) c.fillRect(-40, -46 + k * 14, 80, 6); c.restore();
  // beanie
  shape(c, [[-30, -86], [-24, -104], [0, -112], [24, -104], [30, -86]], '#2e2a33', 113, { hc: '#1c1a20', lw: 4 });
  shape(c, rrPts(-33, -90, 66, 10, 4, 2), '#46404f', 114, { lw: 3 });
  // bandit mask
  shape(c, rrPts(-34, -80, 68, 18, 8, 3), '#1f1c22', 115, { hc: '#111', lw: 3 });
  const ew = mood > .5 ? 9 : 7.5, eh = mood > .5 ? 9 : 5.5;
  for (const ex of [-13, 13]) { c.fillStyle = '#fbf7ee'; c.beginPath(); c.ellipse(ex, -71, ew, eh, 0, 0, TAU); c.fill();
    c.fillStyle = '#111'; c.beginPath(); c.arc(ex + look * 3.5, -71 + (mood > .5 ? 0 : 1), mood > .5 ? 2.6 : 3, 0, TAU); c.fill(); }
  // eyebrows / mouth
  if (mood > .5) {
    line(c, [[-22, -88], [-6, -84]], 3, 116); line(c, [[22, -88], [6, -84]], 3, 117);
    c.fillStyle = '#2a1f2a'; c.beginPath(); c.ellipse(0, -48, 9, 11, 0, 0, TAU); c.fill();
    c.fillStyle = '#9bd0f0'; for (const [dx, dy] of [[34, -92], [-38, -88]]) { c.beginPath(); c.moveTo(dx, dy - 10); c.quadraticCurveTo(dx + 6, dy, dx, dy + 4); c.quadraticCurveTo(dx - 6, dy, dx, dy - 10); c.fill(); }
  } else {
    line(c, [[-12, -50], [-2, -46], [12, -52]], 3, 118);   // sly smirk
  }
  // arms
  if (mood > .5) { line(c, [[-34, -60], [-50, -86]], 6, 119, '#554672'); line(c, [[34, -60], [52, -88]], 6, 120, '#554672'); }
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
  if (style === 'fill') { g.fillStyle = color; g.fill(polyPath(rough(0, h * .2))); g.globalCompositeOperation = 'destination-out'; g.fillText(word, w / 2, h * .54); g.globalCompositeOperation = 'source-over'; }
  else { g.strokeStyle = color; g.lineJoin = 'round'; g.lineWidth = size * .075; g.stroke(polyPath(rough(size * .04, 16))); g.lineWidth = size * .03; g.stroke(polyPath(rough(size * .15, 10))); g.fillStyle = color; g.fillText(word, w / 2, h * .54); }
  g.setTransform(1, 0, 0, 1, 0, 0); inkTexture(g, cv.width, cv.height, seed + 5, cv.width * cv.height / 45);
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
// p: {bob, tilt, sx, sy, lift:[l, r], hop}; armFn(Sw, rest) -> null | {mode, hand, dir}
function drawJeff(c, x, gy, k, p = {}, armFn = null) {
  const { bob = 0, tilt = 0, sx = 1, sy = 1, lift = [0, 0], hop = 0 } = p;
  const base = c.getTransform();
  c.save(); c.translate(x, gy - hop); c.rotate(tilt); c.scale(k * sx, k * sy);
  const M = base.inverse().multiply(c.getTransform());
  c.drawImage(IMG.legL, -AX, -AY - lift[0]); c.drawImage(IMG.legR, -AX, -AY - lift[1]); c.drawImage(IMG.body, -AX, -AY - bob);
  c.restore();
  if (!armFn) return null;
  const Mb = M.translate(-AX, -AY - bob), sp = Mb.transformPoint(new DOMPoint(...SHOULDER)), rp = Mb.transformPoint(new DOMPoint(430, 640));
  const Sw = [sp.x, sp.y], A = armFn(Sw, [rp.x, rp.y]); if (!A) return { Sw };
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
