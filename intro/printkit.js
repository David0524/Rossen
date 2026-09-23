'use strict';
/* Screen-print "case file" kit shared by the Rossen films: inks sampled from the official logo, halftone tints with
   misregistration, black keylines, solid stamps, ransom letters, the jointed Jeff puppet, and case-file props.
   Load after core.js and kit.js; the film calls setFormat() first, then awaits loadPrintKit(). */
// ---- inks (blue and yellow sampled from the official logo)
const BLUE = '#0858C0', BLK = '#1d1b1f', YEL = '#F8D000', CREAM = '#efe6d2', CHIP = '#f8f2e4';
const REG = { [BLUE]: [4, -3], [YEL]: [-4, 3], [BLK]: [0, 0], [CHIP]: [0, 0], [CREAM]: [0, 0] };   // misregistration per ink
const ANG = { [BLUE]: .26, [YEL]: 0, [BLK]: .78 };
let PAPER_TEX = null, SPECK = null;
const SLAM = .14;   // landings start this early so they finish ON the beat

// ================= screen-print kit =================
function rough(pts, seed, amp = 2.2, step = 16, close = true) { const r = rng(seed); return densify(pts, step, close).map(([x, y]) => [x + (r() - .5) * amp, y + (r() - .5) * amp]); }
// flat ink: solid, or a halftone tint (density 0..1). Colour inks print a few px off register.
function ink(c, pts, col, seed, o = {}) {
  const P = polyPath(rough(pts, seed, o.amp ?? 2.2)), [dx, dy] = o.reg === false ? [0, 0] : (REG[col] || [0, 0]);
  c.save(); c.translate(dx, dy);
  if (o.tint == null || o.tint >= 1) { c.fillStyle = col; c.fill(P); }
  else dotScreen(c, P, bbox(pts), { cell: o.cell ?? 10, color: col, density: o.tint, angle: ANG[col] ?? .4, jitter: .04, seed });
  c.restore(); return P;
}
function key(c, pts, w, seed, close = true, col = BLK) {   // black keyline, solid with a rough edge
  const q = rough(pts, seed, 2.4, 12, close); c.save(); c.strokeStyle = col; c.lineWidth = w; c.lineJoin = 'round'; c.lineCap = 'round';
  c.beginPath(); q.forEach(([x, y], i) => i ? c.lineTo(x, y) : c.moveTo(x, y)); if (close) c.closePath(); c.stroke(); c.restore();
}
function block(c, pts, col, seed, o = {}) { ink(c, pts, col, seed, o); if (o.key !== false) key(c, pts, o.kw ?? 6, seed + 7, true); }
function dotsIn(c, pts, col, density, seed, cell = 10) { ink(c, pts, col, seed, { tint: density, cell }); }
const rect = (x, y, w, h) => [[x, y], [x + w, y], [x + w, y + h], [x, y + h]];
function inkText(c, s, x, y, size, family, col, maxW, align = 'center', rot = 0) {   // text printed in one ink, off register like the rest
  const [dx, dy] = REG[col] || [0, 0]; c.save(); c.translate(x + dx, y + dy); c.rotate(rot); fitText(c, s, 0, 0, size, family, col, maxW, align); c.restore();
}
function paperBg(c) { c.save(); resetT(c); c.drawImage(PAPER_TEX, 0, 0, W, H); c.restore(); }
function printFinish(c) { c.save(); resetT(c); c.drawImage(SPECK, 0, 0, W, H); c.restore(); }   // ink never covers fully: paper specks through every solid
function stampImg(word, col = BLUE, size = 150) { return wordStamp(word, { color: col, style: 'fill', size, seed: word.length * 7 }); }
function stampLand(c, img, x, y, rot, sc, t, tl) {   // solid ink: nothing underneath shows through
  if (t < tl - .12) return;
  const a = seg(t, tl - .12, tl), s = t < tl ? lerp(1.55, 1, easeIn(a)) : t < tl + .12 ? 1 + .04 * Math.exp(-(t - tl) * 30) * Math.cos((t - tl) * 60) : 1;
  c.save(); c.translate(x, y); c.rotate(rot); c.scale(sc * s, sc * s);
  c.save(); c.filter = 'brightness(0)'; c.globalAlpha = .55; c.drawImage(img, -img.width / 2 + 12, -img.height / 2 + 14); c.restore();
  c.drawImage(img, -img.width / 2, -img.height / 2); c.restore();
  if (t >= tl && t < tl + .3) { const r = rng(Math.round(x + y)); c.save(); c.fillStyle = BLUE; c.globalAlpha = .8 * (1 - seg(t, tl + .15, tl + .3));
    for (let k = 0; k < 11; k++) { const ang = r() * TAU, d = (img.width * sc * .5) * (.75 + r() * .45), s2 = 2 + r() * 5; c.beginPath(); c.arc(x + Math.cos(ang) * d, y + Math.sin(ang) * d * .45, s2, 0, TAU); c.fill(); }
    c.restore(); }
}
function shake(t, hits) { let x = 0, y = 0; for (const [ti, a] of hits) if (t >= ti && t < ti + .14) { const r = rng(Math.round(t * 991)), d = 1 - (t - ti) / .14; x += (r() - .5) * a * 2 * d; y += (r() - .5) * a * 2 * d; } return [x, y]; }
const land = (t, t0) => seg(t, t0 - SLAM, t0);   // 0..1, reaching 1 exactly on t0

// ransom-note letters: each on its own cut paper chip, mixed fonts and inks
const RANSOM_STYLES = [
  { bg: BLK, fg: CHIP, font: 'Stamp' }, { bg: YEL, fg: BLK, font: '"DejaVu Serif"' }, { bg: CHIP, fg: BLUE, font: 'Stamp' },
  { bg: BLUE, fg: CHIP, font: '"Liberation Sans"' }, { bg: CHIP, fg: BLK, font: '"DejaVu Serif"' }, { bg: YEL, fg: BLUE, font: 'Marker' },
];
function ransomLetter(c, ch, x, y, size, k, rot) {
  const S = RANSOM_STYLES[k % RANSOM_STYLES.length], w = size * .92, h = size * 1.12, r = rng(40 + k);
  const pts = [[-w / 2 + r() * 8, -h / 2 + r() * 6], [w / 2 - r() * 6, -h / 2 + r() * 8], [w / 2 - r() * 8, h / 2 - r() * 6], [-w / 2 + r() * 6, h / 2 - r() * 8]];
  c.save(); c.translate(x, y); c.rotate(rot);
  c.save(); c.globalAlpha = .25; c.translate(8, 10); c.fillStyle = BLK; c.fill(polyPath(pts)); c.restore();
  ink(c, pts, S.bg, 60 + k, { amp: 1.4 }); c.font = `bold ${size * .82}px ${S.font}`;
  const [dx, dy] = REG[S.fg] || [0, 0]; c.fillStyle = S.fg; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(ch, dx, dy + size * .04);
  c.restore();
}

// ================= Jeff: jointed paper-cutout puppet cut from the reference =================
let JP = null;   // parts meta
const FEET = [850, 895];   // reference point between his shoes
// pose: { head, armL, armR, legL, legR (radians), bob, tilt, prop: 'glass'|'thumb'|'point' }
function jeff(c, x, y, s, p = {}) {
  const base = c.getTransform();
  c.save(); c.translate(x, y); c.rotate(p.tilt || 0); c.scale(s * (p.sx || 1), s * (p.sy || 1)); c.translate(-FEET[0], -FEET[1] - (p.bob || 0));
  const part = (k, a = 0) => { const m = JP.parts[k], [px, py] = m.pivot; c.save(); c.translate(px, py); c.rotate(a); c.translate(-px, -py); c.drawImage(IMG['j_' + k], m.x, m.y); c.restore(); };
  // paper split-pin at a joint
  const pin = (k) => { const [px, py] = JP.parts[k].pivot; c.fillStyle = YEL; c.beginPath(); c.arc(px, py, 9, 0, TAU); c.fill(); c.strokeStyle = BLK; c.lineWidth = 3; c.stroke(); };
  part('legL', p.legL || 0); part('legR', p.legR || 0);
  part('torso'); part('armR', p.armR || 0); pin('armR');
  part('armL', p.armL || 0);
  part('head', p.head || 0);
  // hand position (free arm) for props: fist centre in the reference is ~(1045, 738)
  const M = base.inverse().multiply(c.getTransform()), [px, py] = JP.parts.armR.pivot, a = p.armR || 0;
  const hx = px + Math.cos(a) * (1045 - px) - Math.sin(a) * (738 - py), hy = py + Math.sin(a) * (1045 - px) + Math.cos(a) * (738 - py);
  const handW = M.transformPoint(new DOMPoint(hx, hy)), shW = M.transformPoint(new DOMPoint(px, py));
  c.restore();
  const hand = [handW.x, handW.y], d0 = [hand[0] - shW.x, hand[1] - shW.y], dl = Math.hypot(...d0), u = [d0[0] / dl, d0[1] / dl], fr = 36 * s;
  if (p.prop === 'thumb') { const tn = Math.hypot(u[0] * .35, 1), td = [u[0] * .35 / tn, -1 / tn]; const b0 = [hand[0] + td[0] * fr * .45, hand[1] + td[1] * fr * .45]; skinCapsule(c, b0, [b0[0] + td[0] * fr * 1.05, b0[1] + td[1] * fr * 1.05], fr * .38, 71); }
  if (p.prop === 'point') { const b0 = [hand[0] + u[0] * fr * .55, hand[1] + u[1] * fr * .55]; skinCapsule(c, b0, [b0[0] + u[0] * fr * 1.35, b0[1] + u[1] * fr * 1.35], fr * .32, 72); }
  return { hand, u };
}
// a finger or thumb printed like the reference's hands: orange stock, red halftone, red off-register shadow, no keyline
function skinCapsule(c, a, b, r, seed) {
  const pts = capsulePts(a, b, r, 8), P = polyPath(pts);
  c.save(); c.translate(r * .28, r * .22); c.globalAlpha = .75; c.fillStyle = '#e2553b'; c.fill(P); c.restore();
  c.fillStyle = '#f4a46d'; c.fill(P);
  dotScreen(c, P, bbox(pts), { cell: Math.max(4, r * .42), color: '#dc4f37', density: .42, angle: .78, seed });
}

// ================= props =================
function magnifier(c, cx, cy, R, fromHand, inner) {   // ring (black), handle (yellow), optional contents
  if (fromHand) { const a = Math.atan2(cy - fromHand[1], cx - fromHand[0]), e = [cx - Math.cos(a) * R, cy - Math.sin(a) * R];
    c.save(); c.strokeStyle = BLK; c.lineCap = 'round'; c.lineWidth = 34; c.beginPath(); c.moveTo(fromHand[0], fromHand[1]); c.lineTo(e[0], e[1]); c.stroke();
    c.strokeStyle = YEL; c.lineWidth = 22; c.beginPath(); c.moveTo(fromHand[0], fromHand[1]); c.lineTo(e[0] + Math.cos(a) * -10, e[1] + Math.sin(a) * -10); c.stroke(); c.restore(); }
  if (inner) { c.save(); c.beginPath(); c.arc(cx, cy, R, 0, TAU); c.clip(); inner(); c.restore(); }
  else { c.save(); c.fillStyle = alpha(CHIP, .25); c.beginPath(); c.arc(cx, cy, R, 0, TAU); c.fill(); c.restore(); }
  c.save(); c.strokeStyle = BLK; c.lineWidth = Math.max(14, R * .12); c.beginPath(); c.arc(cx, cy, R, 0, TAU); c.stroke();
  c.strokeStyle = CHIP; c.lineWidth = Math.max(5, R * .04); c.lineCap = 'round'; c.beginPath(); c.arc(cx, cy, R * .78, Math.PI * 1.1, Math.PI * 1.4); c.stroke(); c.restore();
}
function polaroid(c, x, y, w, h, rot, seed, drawPic) {
  c.save(); c.translate(x, y); c.rotate(rot);
  c.save(); c.globalAlpha = .28; c.fillStyle = BLK; c.fillRect(-w / 2 + 10, -h / 2 + 12, w, h); c.restore();
  block(c, rect(-w / 2, -h / 2, w, h), CHIP, seed, { kw: 5 });
  const pw = w - 36, ph = h - 90; c.save(); c.beginPath(); c.rect(-pw / 2, -h / 2 + 18, pw, ph); c.clip(); c.translate(0, -h / 2 + 18 + ph / 2); drawPic(pw, ph); c.restore();
  key(c, rect(-pw / 2, -h / 2 + 18, pw, ph), 4, seed + 3);
  c.restore();
}
function pushpin(c, x, y) { c.save(); c.fillStyle = BLUE; c.beginPath(); c.arc(x, y, 15, 0, TAU); c.fill(); c.strokeStyle = BLK; c.lineWidth = 4; c.stroke(); c.fillStyle = alpha(CHIP, .8); c.beginPath(); c.arc(x - 5, y - 5, 4.5, 0, TAU); c.fill(); c.restore(); }
function string(c, a, b, sag = 40, u = 1) {
  const m = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + sag], pts = [];
  for (let i = 0; i <= 30 * u; i++) { const q = i / 30; pts.push([(1 - q) ** 2 * a[0] + 2 * (1 - q) * q * m[0] + q * q * b[0], (1 - q) ** 2 * a[1] + 2 * (1 - q) * q * m[1] + q * q * b[1]]); }
  if (pts.length < 2) return; c.save(); c.lineCap = 'round'; c.strokeStyle = BLK; c.lineWidth = 8; c.beginPath(); pts.forEach(([x, y], i) => i ? c.lineTo(x, y) : c.moveTo(x, y)); c.stroke();
  c.strokeStyle = YEL; c.lineWidth = 4.5; c.stroke(); c.restore();
}
function phoneIcon(c, s) { block(c, rect(-40 * s, -70 * s, 80 * s, 140 * s), BLK, 81, { kw: 4 }); ink(c, rect(-32 * s, -56 * s, 64 * s, 104 * s), CHIP, 82, { reg: false }); ink(c, rect(-32 * s, -56 * s, 64 * s, 22 * s), BLUE, 83); }
function lensIcon(c, s) { block(c, ellPts(0, 0, 62 * s, 62 * s, 0, 30), BLK, 84, { kw: 4 }); ink(c, ellPts(0, 0, 40 * s, 40 * s, 0, 26), BLUE, 85); ink(c, ellPts(-12 * s, -12 * s, 10 * s, 10 * s, 0, 14), CHIP, 86, { reg: false }); }
function tagIcon(c, s) { block(c, [[-70 * s, -30 * s], [40 * s, -30 * s], [70 * s, 0], [40 * s, 30 * s], [-70 * s, 30 * s]], YEL, 87, { kw: 4 }); inkText(c, '$9', -10 * s, 2 * s, 44 * s, 'Stamp', BLK, 90 * s); }
function docIcon(c, s) { block(c, rect(-48 * s, -64 * s, 96 * s, 128 * s), CHIP, 88, { kw: 4 }); for (let k = 0; k < 5; k++) ink(c, rect(-34 * s, (-44 + k * 20) * s, (k % 2 ? 50 : 68) * s, 9 * s), BLK, 89 + k, { reg: false }); }

// the con man, screen-printed: fedora, bandit mask, curly mustache, blue coat, yellow scarf
function conman(c, x, y, s, o = {}) {
  const { mood = 0, look = 0, t = 0 } = o;
  c.save(); c.translate(x, y); c.scale(s, s); if (mood) c.translate(Math.sin(t * 80) * 2.5, 0);
  block(c, ellPts(0, -52, 40, 40, 0, 36), BLUE, 901, { kw: 4 });
  block(c, [[-30, -86], [-8, -76], [-22, -58]], BLUE, 902, { kw: 3 }); block(c, [[30, -86], [8, -76], [22, -58]], BLUE, 903, { kw: 3 });
  block(c, ellPts(0, -100, 26, 25, 0, 30), CHIP, 904, { kw: 4 }); dotsIn(c, ellPts(0, -100, 26, 25, 0, 30), YEL, .35, 905, 7);
  block(c, rect(-22, -84, 44, 10), YEL, 906, { kw: 3 });
  block(c, rect(-28, -112, 56, 16), BLK, 907, { kw: 2 });
  for (const ex of [-11, 11]) { ink(c, ellPts(ex, -104, mood ? 7.5 : 6.5, mood ? 7.5 : 4.8, 0, 16), CHIP, 908 + ex, { reg: false }); c.fillStyle = BLK; c.beginPath(); c.arc(ex + look * 3, -104, mood ? 2.4 : 2.8, 0, TAU); c.fill(); }
  c.save(); c.strokeStyle = BLK; c.lineWidth = 4.5; c.lineCap = 'round'; c.beginPath(); c.moveTo(0, -90); c.quadraticCurveTo(-9, -95, -16, -89); c.quadraticCurveTo(-20, -84, -15, -82); c.moveTo(0, -90); c.quadraticCurveTo(9, -95, 16, -89); c.quadraticCurveTo(20, -84, 15, -82); c.stroke();
  if (mood) { c.fillStyle = BLK; c.beginPath(); c.ellipse(0, -80, 5, 6, 0, 0, TAU); c.fill(); } c.restore();
  block(c, ellPts(0, -120, 40, 8, 0, 24), BLK, 910, { kw: 2 }); block(c, [[-22, -120], [-19, -142], [-4, -138], [0, -144], [4, -138], [19, -142], [22, -120]], BLK, 911, { kw: 2 });
  ink(c, rect(-22, -128, 44, 7), YEL, 912);
  if (mood) { key(c, [[-34, -58], [-52, -90]], 9, 913, false, BLUE); key(c, [[34, -58], [54, -92]], 9, 914, false, BLUE); }
  c.restore();
}

// jeff parts, fonts, paper stock and the paper-speck finish (made at the current format)
async function loadPrintKit() {
  JP = await (await fetch('assets/casefile/jeff_parts.json')).json();
  await Promise.all(Object.keys(JP.parts).map(k => loadImg('j_' + k, `assets/casefile/jeff_${k}.png`)));
  await document.fonts.load('40px Stamp'); await document.fonts.load('40px Marker');
  PAPER_TEX = paperTexture(W, H, CREAM, 11);
  { const o = document.createElement('canvas'); o.width = W; o.height = H; const g = o.getContext('2d'), r = rng(12);   // paper specks through the ink
    for (let i = 0; i < 26000; i++) { g.globalAlpha = .15 + r() * .35; g.fillStyle = r() < .8 ? CHIP : '#d9ceb5'; const s = .8 + r() * 2.2; g.fillRect(r() * W, r() * H, s, s * (.6 + r() * .8)); }
    SPECK = o; }
}
