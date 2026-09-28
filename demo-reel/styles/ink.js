'use strict';
/* STYLE: INK ON WARM PAPER (the careers chapter).
   Loose dip-pen linework in dark sepia-brown with a pressure-varied width, cross-hatched shadows, a pale warm-gray
   watercolor wash with pooled edges and granulation, and visible paper fibres. The only colour accents are brick red
   and, for the good posting only, a muted ink green. Motion is dry and deliberate. */
const INK = { paper: '#F5E9D2', sheet: '#FBF4E6', sepia: '#3A2718', sepiaMid: '#6E5139', fibre: '#C9B28C', wash: '#C8BBA8',
  red: '#B23A2E', redDeep: '#8A2A21', green: '#5C7A55', skin: '#ECD4B8', skinSh: '#D7B998', shirt: '#F7EFE0' };

// ---------------- marks ----------------
// pen: one dip-pen stroke along a polyline. Width swells and thins with pressure, tapers at both ends, and the line
// drifts a little off its path. Filled as a polygon, so it reads as ink rather than a canvas stroke.
function pen(c, pts, w, seed, o = {}) {
  const { col = INK.sepia, taper = [.12, .3], step = 2.4, drift = .8, press = .24, blot = 0 } = o;
  const r = rng(seed), P = resample(pts, step), N = P.length; if (N < 2) return;
  const ph = r() * TAU, f1 = .05 + r() * .05, ph2 = r() * TAU, L = [], R = [];
  for (let i = 0; i < N; i++) {
    const a = P[Math.max(0, i - 1)], b = P[Math.min(N - 1, i + 1)], dx = b[0] - a[0], dy = b[1] - a[1], d = Math.hypot(dx, dy) || 1, nx = -dy / d, ny = dx / d;
    const t = i / (N - 1); let k = 1;
    if (t < taper[0]) k = .3 + .7 * Math.sin(t / taper[0] * Math.PI / 2);
    if (t > 1 - taper[1]) k = Math.min(k, .1 + .9 * Math.sin((1 - t) / taper[1] * Math.PI / 2));
    const hw = Math.max(.3, w * .5 * k * (1 + press * Math.sin(ph + i * f1))), off = drift * Math.sin(ph2 + i * f1 * .7);
    L.push([P[i][0] + nx * (off + hw), P[i][1] + ny * (off + hw)]); R.push([P[i][0] + nx * (off - hw), P[i][1] + ny * (off - hw)]);
  }
  c.save(); c.fillStyle = col; c.beginPath(); L.forEach((q, i) => i ? c.lineTo(q[0], q[1]) : c.moveTo(q[0], q[1])); for (let i = N - 1; i >= 0; i--) c.lineTo(R[i][0], R[i][1]); c.closePath(); c.fill();
  if (blot) { c.beginPath(); c.arc(P[0][0], P[0][1], w * blot, 0, TAU); c.fill(); }
  c.restore();
}
// penLoop: a closed outline drawn loosely, as two overlapping strokes that don't quite meet
function penLoop(c, pts, w, seed, o = {}) {
  const r = rng(seed), N = pts.length, s0 = Math.floor(r() * N), split = Math.floor(N * (.5 + (r() - .5) * .2));
  const run = (a, len) => Array.from({ length: len }, (_, k) => pts[(a + k) % N]);
  pen(c, run(s0, split + 3), w, seed + 1, o); pen(c, run(s0 + split - 1, N - split + 4), w, seed + 2, o);
}
function bbox(pts) { let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9; for (const [x, y] of pts) { x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y); } return [x0, y0, x1 - x0, y1 - y0]; }
// hatching: pen strokes clipped to a shape; cross = a second layer at another angle for the deeper shadow
function inkHatch(c, pts, o = {}) { const { angle = .85, gap = 6.5, len = 16, al = .62, w = 1.25, seed = 1, cross = false } = o; const p = polyPath(pts), bb = bbox(pts);
  hatch(c, p, bb, { angle, gap, len, jitter: 5, color: INK.sepia, alpha: al, width: w, seed });
  if (cross) hatch(c, p, bb, { angle: angle - 1.25, gap: gap * 1.15, len, jitter: 5, color: INK.sepia, alpha: al * .8, width: w * .9, seed: seed + 9 }); }
// rough: wobble a closed contour with low-frequency noise (wash edges, torn fibres)
function rough(pts, amp, seed) { const r = rng(seed), ph = [r() * TAU, r() * TAU], N = pts.length; let cx = 0, cy = 0; pts.forEach(([x, y]) => { cx += x / N; cy += y / N; });
  return pts.map(([x, y], i) => { const a = i / N * TAU, k = amp * (Math.sin(a * 3 + ph[0]) * .6 + Math.sin(a * 7 + ph[1]) * .3 + (r() - .5) * .3), dx = x - cx, dy = y - cy, d = Math.hypot(dx, dy) || 1; return [x + dx / d * k, y + dy / d * k]; }); }
// wash: a watercolor fill, layered a little out of place, with a pooled darker edge and granulation
function wash(c, pts, col, al, seed) {
  const r = rng(seed), p = polyPath(pts); c.save(); c.fillStyle = col;
  c.globalAlpha = al; c.fill(p);
  for (let k = 0; k < 2; k++) { c.save(); c.translate((r() - .5) * 7, (r() - .5) * 7); c.globalAlpha = al * .3; c.fill(p); c.restore(); }
  c.globalAlpha = al * .7; c.strokeStyle = shade(col, .16); c.lineWidth = 2.4; c.lineJoin = 'round'; c.stroke(p);
  c.restore(); const bb = bbox(pts); grain(c, p, bb, bb[2] * bb[3] / 70, shade(col, .3), al * .45, seed + 3, 1.5);
}
// scrawl: a line of handwriting, as pen marks that read as text without being words
function scrawl(c, x0, x1, y, seed, o = {}) { const { w = 2.1, h = 7, col = INK.sepia } = o; const r = rng(seed); let x = x0;
  while (x < x1 - 8) { const wl = Math.min(x1 - x, 22 + r() * 46), pts = []; const n = Math.max(3, Math.round(wl / 5));
    for (let k = 0; k <= n; k++) pts.push([x + wl * k / n, y + (k % 2 ? -h : h * .35) * (.6 + r() * .6) + (r() - .5) * 2]);
    pen(c, smooth(pts, false, 3), w, (seed * 31 + x) | 0, { col, taper: [.1, .2], press: .3 }); x += wl + 9 + r() * 8; } }

// ---------------- the page ----------------
// warm paper: soft mottling, fibres, fine specks and a faint vignette (full frame, drawn once)
function inkPaper(L, seed = 7) {
  const g = L.getContext('2d'); resetT(g); const r = rng(seed);
  g.fillStyle = INK.paper; g.fillRect(0, 0, W, H);
  for (let i = 0; i < 80; i++) { const x = r() * W, y = r() * H, R = 90 + r() * 280, dark = r() < .55, col = dark ? '#D9C29B' : '#FFF7E4', gr = g.createRadialGradient(x, y, 0, x, y, R);
    gr.addColorStop(0, alpha(col, .1 + r() * .1)); gr.addColorStop(1, alpha(col, 0)); g.fillStyle = gr; g.fillRect(x - R, y - R, 2 * R, 2 * R); }
  g.lineCap = 'round';
  for (let i = 0; i < 3200; i++) { const x = r() * W, y = r() * H, l = 5 + r() * r() * 36, a = r() * TAU, bend = (r() - .5) * .9;
    g.strokeStyle = r() < .62 ? alpha(INK.fibre, .16 + r() * .24) : alpha('#FFFBF1', .35 + r() * .4); g.lineWidth = .5 + r() * .9;
    g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + Math.cos(a + bend) * l * .5, y + Math.sin(a + bend) * l * .5, x + Math.cos(a) * l, y + Math.sin(a) * l); g.stroke(); }
  grain(g, rectPath(0, 0, W, H), [0, 0, W, H], 4200, '#8E7552', .1, seed + 1, 1.4);
  const v = g.createRadialGradient(W / 2, H / 2, H * .3, W / 2, H / 2, H * .78); v.addColorStop(0, 'rgba(120,88,48,0)'); v.addColorStop(1, 'rgba(120,88,48,.15)'); g.fillStyle = v; g.fillRect(0, 0, W, H);
}
// sheetStock: a sheet of the same stock, lighter (a letter), with its own fibres
function sheetStock(g, w, h, seed) { const r = rng(seed); g.fillStyle = INK.sheet; g.fillRect(0, 0, w, h); g.lineCap = 'round';
  for (let i = 0; i < w * h / 260; i++) { const x = r() * w, y = r() * h, l = 4 + r() * r() * 24, a = r() * TAU; g.strokeStyle = alpha(INK.fibre, .1 + r() * .16); g.lineWidth = .5 + r() * .6;
    g.beginPath(); g.moveTo(x, y); g.lineTo(x + Math.cos(a) * l, y + Math.sin(a) * l); g.stroke(); }
  grain(g, rectPath(0, 0, w, h), [0, 0, w, h], w * h / 90, '#9A8260', .08, seed + 2, 1.3); }

// ---------------- YOU (the hand), in ink ----------------
function inkHand(c, p, part = 'back') {
  const G = HAND.geo(p.grip ?? 1), T = q => HAND.T(q, p), sw = 3.2 * (p.s || 1);
  const rightOf = sp => [...sp.map(([x, y]) => [x + 3, y]), ...sp.slice().reverse().map(([x, y]) => [x + 60, y])];
  const creases = (sp, seed) => [.42, .7].forEach((u, k) => { const i = Math.round(u * (sp.length - 1)), [x, y] = sp[i]; pen(c, T([[x - 9, y + 1], [x, y - 2], [x + 9, y + 1]]), sw * .5, seed + k, { taper: [.3, .4] }); });
  if (part === 'back') {
    const fa = T(G.forearm), h = G.forearm.length / 2;
    wash(c, fa, INK.skin, .96, 11); c.save(); c.clip(polyPath(fa)); inkHatch(c, T(G.shadeArm), { angle: 1.1, seed: 12, al: .5 }); c.restore();
    pen(c, T(G.forearm.slice(0, h)), sw, 13, { taper: [.05, .1] }); pen(c, T(G.forearm.slice(h)), sw, 14, { taper: [.1, .05] });
    G.fingers.forEach((f, i) => { const q = T(f); wash(c, q, INK.skin, .96, 20 + i); c.save(); c.clip(polyPath(q)); inkHatch(c, T(rightOf(G.fingerSpines[i])), { seed: 24 + i, al: .48, gap: 5.5 }); c.restore();
      penLoop(c, q, sw * .9, 30 + i); creases(G.fingerSpines[i], 60 + i * 3); });
    const bk = T(G.back); wash(c, bk, INK.skin, .98, 15); c.save(); c.clip(polyPath(bk)); inkHatch(c, T(G.shadeBack), { angle: 1.0, seed: 16, al: .5 }); inkHatch(c, T([[40, 90], [110, 90], [110, 200], [30, 200]]), { angle: 2.2, seed: 17, al: .4 }); c.restore();
    penLoop(c, bk, sw, 18); G.knuckles.forEach((k, i) => pen(c, T(k), sw * .75, 40 + i, { taper: [.35, .4] })); G.tendons.forEach((k, i) => pen(c, T(k), sw * .32, 45 + i, { col: INK.sepiaMid, taper: [.45, .5] }));
    const sl = T(G.sleeve), cf = T(G.cuff);
    c.fillStyle = INK.shirt; c.fill(polyPath(sl)); c.save(); c.clip(polyPath(sl)); inkHatch(c, T(G.shadeArm.map(([x, y]) => [x + 10, y])), { angle: 1.15, seed: 19, al: .55, cross: true }); c.restore();
    pen(c, [sl[0], sl[1]], sw * 1.1, 20); pen(c, [sl[3], sl[2]], sw * 1.1, 21);
    pen(c, T([HAND.al(330, 40), HAND.al(420, 58)]), sw * .55, 22, { col: INK.sepiaMid }); pen(c, T([HAND.al(360, -30), HAND.al(470, -20)]), sw * .5, 23, { col: INK.sepiaMid });
    c.fillStyle = INK.shirt; c.fill(polyPath(cf)); penLoop(c, cf, sw, 24); const [bx, by] = T([HAND.al(262, -46)])[0]; c.strokeStyle = INK.sepia; c.lineWidth = 2; c.beginPath(); c.arc(bx, by, 6 * (p.s || 1), 0, TAU); c.stroke();
  } else {
    const th = T(G.thumb); wash(c, th, INK.skin, 1, 50); c.save(); c.clip(polyPath(th)); inkHatch(c, T(G.thumbShade), { angle: .7, seed: 51, al: .45 }); c.restore();
    pen(c, T(G.thumbOpen), sw, 52, { taper: [.2, .25] }); const nl = T(G.nail); c.fillStyle = tint(INK.skin, .5); c.fill(polyPath(nl)); penLoop(c, nl, sw * .5, 53);
    const sp = G.thumbSpine, i = Math.round(sp.length * .55), [x, y] = sp[i]; pen(c, T([[x - 12, y + 4], [x - 2, y - 1], [x + 10, y + 3]]), sw * .5, 54, { taper: [.3, .4] });
  }
}

// ---------------- the offer letter, in ink (sheet units 520 x 680, three panels) ----------------
const SHEET = { w: 520, h: 680, ph: 680 / 3, grip: [420, 680] };   // grip: where the hand's origin sits (on the bottom edge)
function emblem(c, x, y, r0, seed) {   // a generic letterhead mark: a ring, a small star, two sprigs
  penLoop(c, ellPts(x, y, r0, r0, 0, 48), 2.6, seed); const st = []; for (let k = 0; k < 10; k++) { const a = -Math.PI / 2 + k * Math.PI / 5, rr = k % 2 ? r0 * .28 : r0 * .62; st.push([x + Math.cos(a) * rr, y + Math.sin(a) * rr]); }
  c.fillStyle = INK.sepia; c.fill(polyPath(st));
  for (const sgn of [-1, 1]) { const stem = [[x + sgn * (r0 + 8), y + 14], [x + sgn * (r0 + 40), y - 2], [x + sgn * (r0 + 62), y - 20]]; pen(c, smooth(stem, false, 6), 2.2, seed + (sgn > 0 ? 3 : 4));
    for (let k = 0; k < 3; k++) { const [lx, ly] = stem[0].map((v, j) => v + (stem[2][j] - v) * (k + 1) / 4); penLoop(c, ellPts(lx, ly - 7, 9, 4, -sgn * .6, 14), 1.6, seed + 10 + k + (sgn > 0 ? 5 : 0)); } }
}
function waxSeal(c, x, y, r0, seed) {
  const r = rng(seed), blob = rough(ellPts(x, y, r0, r0 * .96, 0, 40), r0 * .12, seed); c.fillStyle = INK.red; c.fill(polyPath(blob));
  for (let k = 0; k < 3; k++) { const a = r() * TAU, d = r0 * (.95 + r() * .1); c.beginPath(); c.arc(x + Math.cos(a) * d, y + Math.sin(a) * d, r0 * (.12 + r() * .1), 0, TAU); c.fill(); }
  c.strokeStyle = INK.redDeep; c.lineWidth = 3; c.beginPath(); c.arc(x, y, r0 * .7, 0, TAU); c.stroke(); c.lineWidth = 2;
  const st = []; for (let k = 0; k < 10; k++) { const a = -Math.PI / 2 + k * Math.PI / 5, rr = k % 2 ? r0 * .2 : r0 * .45; st.push([x + Math.cos(a) * rr, y + Math.sin(a) * rr]); } c.stroke(polyPath(st));
  c.fillStyle = alpha('#FFFFFF', .22); c.beginPath(); c.ellipse(x - r0 * .35, y - r0 * .42, r0 * .22, r0 * .1, -.6, 0, TAU); c.fill();
}
// front: letterhead, headline space, a red underline, body scrawl, signature. The headline is set separately (letterInkHeadline)
function letterFrontInk(g) { const { w, h, ph } = SHEET; sheetStock(g, w, h, 70);
  emblem(g, w / 2, 66, 26, 71); pen(g, [[70, 120], [450, 121]], 2.2, 72, { taper: [.05, .1] }); pen(g, [[70, 128], [450, 128]], 1.2, 73, { taper: [.05, .1] });
  scrawl(g, 70, 250, 166, 74, { w: 1.9, h: 6 }); scrawl(g, 70, 200, 192, 75, { w: 1.9, h: 6 }); scrawl(g, 330, 450, 166, 76, { w: 1.9, h: 6 });
  pen(g, smooth([[108, 430], [220, 437], [330, 433], [414, 426]], false, 6), 6.5, 77, { col: INK.red, press: .35, taper: [.08, .35] });
  for (let k = 0; k < 4; k++) scrawl(g, 70, [450, 440, 452, 300][k], 492 + k * 27, 80 + k, { w: 1.9, h: 6 });
  scrawl(g, 70, 170, 606, 86, { w: 1.9, h: 6 }); pen(g, smooth([[82, 648], [110, 616], [124, 640], [150, 606], [160, 650], [196, 624], [240, 640], [262, 628]], false, 5), 2.8, 87, { blot: .8 });
  for (const y of [ph, 2 * ph]) { g.save(); g.globalAlpha = .18; pen(g, [[6, y], [w - 6, y + 1]], 1.2, 88 + y | 0, { col: INK.sepiaMid }); g.restore(); }
  penLoop(g, rough([[0, 0], [w / 2, 0], [w, 0], [w, h / 2], [w, h], [w / 2, h], [0, h], [0, h / 2]].flatMap((q, i, a) => { const n = a[(i + 1) % a.length]; return [0, .25, .5, .75].map(t => [q[0] + (n[0] - q[0]) * t, q[1] + (n[1] - q[1]) * t]); }), 1.2, 89), 3, 90);
}
function letterInkHeadline(g) { g.save(); g.fillStyle = INK.sepia; g.textAlign = 'center'; g.textBaseline = 'alphabetic';
  const sz = Math.min(fitFont(g, 'YOU GOT', 900, 92, 'Playfair', 420), fitFont(g, 'THE JOB.', 900, 92, 'Playfair', 420)); g.font = `900 ${sz}px Playfair`;
  g.fillText('YOU GOT', SHEET.w / 2, 318); g.fillText('THE JOB.', SHEET.w / 2, 412); g.restore(); return sz; }
// backs, as seen once folded (each one panel, 520 x 226.7). Top: the outer flap, sealed. Bottom: the inside of the fold.
function letterBackTopInk(g) { const { w, ph } = SHEET; sheetStock(g, w, ph, 91);
  inkHatch(g, [[0, 0], [w, 0], [w, 26], [0, 22]], { angle: .2, gap: 5, len: 22, al: .4, seed: 92 });
  pen(g, [[18, 20], [w - 18, 20]], 1.4, 93); pen(g, [[w - 18, 20], [w - 18, ph - 18]], 1.4, 94); pen(g, [[w - 18, ph - 18], [18, ph - 18]], 1.4, 95); pen(g, [[18, ph - 18], [18, 20]], 1.4, 96);
  waxSeal(g, 104, ph / 2 + 4, 48, 97); scrawl(g, 200, 470, 82, 98, { w: 2.2, h: 7 }); scrawl(g, 200, 420, 116, 99, { w: 2.2, h: 7 }); scrawl(g, 200, 450, 150, 100, { w: 2.2, h: 7 });
  penLoop(g, [[0, 0], [w, 0], [w, ph], [0, ph]].flatMap((q, i, a) => { const n = a[(i + 1) % 4]; return [0, .5].map(t => [q[0] + (n[0] - q[0]) * t, q[1] + (n[1] - q[1]) * t]); }), 3, 101); }
function letterBackBotInk(g) { const { w, ph } = SHEET; sheetStock(g, w, ph, 102);
  inkHatch(g, [[0, ph - 30], [w, ph - 26], [w, ph], [0, ph]], { angle: .2, gap: 5, len: 22, al: .45, seed: 103, cross: true });
  g.save(); g.globalAlpha = .12; for (let k = 0; k < 4; k++) scrawl(g, 70, 440, 40 + k * 27, 104 + k, { w: 1.6, h: 5 }); g.restore();
  penLoop(g, [[0, 0], [w, 0], [w, ph], [0, ph]].flatMap((q, i, a) => { const n = a[(i + 1) % 4]; return [0, .5].map(t => [q[0] + (n[0] - q[0]) * t, q[1] + (n[1] - q[1]) * t]); }), 3, 108); }

// ---------------- the job postings (same sheet as the letter) and the stamps ----------------
function briefcase(c, x, y, seed) { const b = [[x - 34, y - 12], [x + 34, y - 12], [x + 34, y + 26], [x - 34, y + 26]];
  wash(c, b, INK.wash, .5, seed); penLoop(c, b.flatMap((q, i, a) => { const n = a[(i + 1) % 4]; return [0, .5].map(t => [q[0] + (n[0] - q[0]) * t, q[1] + (n[1] - q[1]) * t]); }), 2.6, seed + 1);
  pen(c, smooth([[x - 12, y - 12], [x - 12, y - 24], [x + 12, y - 24], [x + 12, y - 12]], false, 4), 2.4, seed + 2); pen(c, [[x - 34, y + 2], [x + 34, y + 2]], 1.6, seed + 3); }
// the posting's text block: sentence case, one size for every line (the longest line sets it)
function postingSize(g, groups) { g.save(); const lines = groups.flat(); let sz = 64; for (const l of lines) sz = Math.min(sz, fitFont(g, l, 700, 64, 'Playfair', 440)); g.restore(); return sz; }
function postingFaceInk(g, seed) { const { w, h } = SHEET; sheetStock(g, w, h, seed); briefcase(g, w / 2, 72, seed + 1);
  pen(g, [[70, 128], [450, 129]], 2.2, seed + 2, { taper: [.05, .1] }); pen(g, [[70, 136], [450, 136]], 1.2, seed + 3, { taper: [.05, .1] });
  penLoop(g, rough([[0, 0], [w / 2, 0], [w, 0], [w, h / 2], [w, h], [w / 2, h], [0, h], [0, h / 2]].flatMap((q, i, a) => { const n = a[(i + 1) % a.length]; return [0, .25, .5, .75].map(t => [q[0] + (n[0] - q[0]) * t, q[1] + (n[1] - q[1]) * t]); }), 1.2, seed + 4), 3, seed + 5); }
function postingText(g, groups, y0) { const sz = postingSize(g, groups); g.save(); g.fillStyle = INK.sepia; g.textAlign = 'center'; g.textBaseline = 'middle'; g.font = `700 ${sz}px Playfair`;
  let y = y0; groups.forEach((grp, k) => { grp.forEach(l => { g.fillText(l, SHEET.w / 2, y); y += sz * 1.2; }); y += sz * .45; }); g.restore(); return y; }
// a rubber stamp: a double border and the words, in one solid ink (fully opaque, no texture in the letters)
function stampInk(c, s, x, y, col, rot = -.1, k = 1) { c.save(); c.translate(x, y); c.rotate(rot); c.scale(k, k);
  const sz = fitFont(c, s, 900, 50, 'Playfair', 250), w = Math.max(230, c.measureText(s).width + 50), h = 84; c.fillStyle = INK.sheet; c.fillRect(-w / 2, -h / 2, w, h);
  c.strokeStyle = col; c.lineWidth = 5; c.strokeRect(-w / 2, -h / 2, w, h); c.lineWidth = 2; c.strokeRect(-w / 2 + 9, -h / 2 + 9, w - 18, h - 18);
  c.fillStyle = col; c.font = `900 ${sz}px Playfair`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(s, 0, 3); c.restore(); }
// the APPLY button, drawn in pen; pressed, it fills with ink and the word shows in the paper's colour
function applyButton(c, s, pressed, seed) { const x0 = 170, y0 = 592, w = 240, h = 66; const b = [[x0, y0], [x0 + w, y0], [x0 + w, y0 + h], [x0, y0 + h]];
  c.save(); if (pressed) { c.fillStyle = INK.sepia; c.fill(roundRectPath(x0, y0, w, h, 14)); } penLoop(c, smooth([[x0 + 14, y0], [x0 + w - 14, y0], [x0 + w, y0 + 14], [x0 + w, y0 + h - 14], [x0 + w - 14, y0 + h], [x0 + 14, y0 + h], [x0, y0 + h - 14], [x0, y0 + 14]], true, 3), 2.8, seed);
  c.fillStyle = pressed ? INK.sheet : INK.sepia; c.font = `900 ${fitFont(c, s, 900, 40, 'Playfair', 150)}px Playfair`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(s, x0 + 100, y0 + h / 2 + 2); c.restore(); }
// Raj's flag: a pen-drawn stick and a washed pennant that flutters a little
function inkFlag(c, x, y, len, col, t, seed) { pen(c, [[x, y], [x, y - len]], 4, seed, { taper: [.05, .2] });
  const f = []; for (let k = 0; k <= 8; k++) { const u = k / 8; f.push([x + u * 120, y - len + 6 + u * 24 + Math.sin(u * 5 + t * 9) * 5 * u]); } for (let k = 8; k >= 0; k--) { const u = k / 8; f.push([x + u * 120, y - len + 74 - u * 24 + Math.sin(u * 5 + t * 9) * 5 * u]); }
  c.fillStyle = col; c.fill(polyPath(f)); penLoop(c, f, 2.4, seed + 1); }
