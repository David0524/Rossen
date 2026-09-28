'use strict';
/* Style demo (5 s, 2 bars at 96 BPM, D, 1080x1920, 24 fps): four lessons from REFERENCES.md tried on one shot.
   11  print marks as decoration: the scene is a printed panel on the sheet, with crop marks, registration targets and a
       colour bar instead of more dots.
   13  halftone dots as shading, locked to each puppet part: black dots on the side away from the light, blue dots as a rim
       light on the dark coat; the dot grid lives in the part's own coordinates, so it moves with the rig (no swimming).
   14  a real paper scan (ambientCG Paper002, CC0, a photographed paper) instead of generated specks: its fibres and flecks
       show through every ink, fixed in screen space.
   15  fewer inks per shot: bar 0 is printed in blue and black only (the disguise's yellow trim is reprinted blue); on bar 1
       the yellow plate runs, and the yellow is the warning: the badge, the caption and the colour bar's yellow patch.

   bar 0  0.0  the "deputy" on the phone, breathing; he puffs his chest on 3                "HE SAYS HE'S" / "A DEPUTY."
   bar 1  2.5  the yellow plate prints on 1 (badge, star, trim, the chip, the colour bar); the FAKE stamp lands on 2
               and he jolts; his cap pops up and a sweat drop appears on 3; he shrinks on 4        "THE BADGE" / "IS FAKE."
   A style test, not a deliverable: no intro title card or closing card. The logo bug is on throughout. */
const DUR = at(2), NFR = Math.round(FPS * DUR);
const CAPS = [[at(0), at(1) - SLAM, ["HE SAYS HE'S", BLK], ['A DEPUTY.', BLUE]], [at(1), DUR + 1, ['THE BADGE', BLK], ['IS FAKE.', YEL]]];
const YEL_ON = at(1) - SLAM;   // the yellow plate prints with the second card
const yelOn = t => t >= YEL_ON;
const capPop = (t, t0) => t < t0 ? lerp(1.05, 1, easeIn(land(t, t0))) : 1;
function chip(c, s, x, y, size, bg, fg, t, t0) {
  if (t < t0 - SLAM) return; c.font = `${size}px Stamp`; const w = Math.min(c.measureText(s).width, 740) + 60, h = size * 1.3, k = capPop(t, t0);
  c.save(); c.translate(x, y); c.scale(k, k);
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fillRect(-w / 2 + 8, -h / 2 + 10, w, h); c.restore();
  ink(c, rect(-w / 2, -h / 2, w, h), bg, 8100 + s.length, { amp: 3 }); inkText(c, s, 0, size * .06, size, 'Stamp', fg, 740); c.restore();
}
function captionsTop(c, t) {
  for (const cp of CAPS) { const [t0, t1] = cp; if (t < t0 - SLAM || t >= t1) continue;
    cp.slice(2).forEach(([s, bg], i) => chip(c, s, SCX, 372 + i * 116, 72, bg, bg === YEL ? BLK : CHIP, t, t0)); }
}
const breath = (t, ph = 0) => .012 * Math.sin(t * 2.2 + ph);
const spring = (t, t0, a, f = 18, d = 7) => t < t0 ? 0 : a * Math.exp(-(t - t0) * d) * Math.cos((t - t0) * f);

// ================= lesson 13: shaded parts (built once; the dots are in the part's own pixels) =================
const LIGHT = [-.6, -.8];   // towards the light: up and to the left
const PARTS = ['legL', 'legR', 'torso', 'badge', 'arm', 'head', 'cap'];
const SH = { two: {}, full: {} };   // two = the yellow reprinted blue (bar 0); full = the art's own inks (bar 1)
const rgbOf = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16));
function shadedPart(img, recolor) {
  const w = img.width, h = img.height, cv = document.createElement('canvas'); cv.width = w; cv.height = h; const g = cv.getContext('2d');
  g.drawImage(img, 0, 0); const id = g.getImageData(0, 0, w, h), px = id.data;
  if (recolor) { const [br, bg, bb] = rgbOf(BLUE); for (let i = 0; i < px.length; i += 4) { const r = px[i], gg = px[i + 1], b = px[i + 2];
    if (r > 140 && gg > 105 && b < 130 && r - b > 70) { const l = (r + gg) / 2 / 225; px[i] = br * l; px[i + 1] = bg * l; px[i + 2] = bb * l; } } g.putImageData(id, 0, 0); }
  const bl = document.createElement('canvas'); bl.width = w; bl.height = h; const bgc = bl.getContext('2d'); bgc.filter = 'blur(14px)'; bgc.drawImage(img, 0, 0);
  const A = bgc.getImageData(0, 0, w, h).data, P = g.getImageData(0, 0, w, h).data;
  const at4 = (x, y) => 4 * (Math.min(h - 1, Math.max(0, y)) * w + Math.min(w - 1, Math.max(0, x)));
  g.globalCompositeOperation = 'source-atop';
  const grid = (col, angle, cell, dens) => { const ca = Math.cos(angle), sa = Math.sin(angle), R = Math.hypot(w, h) / 2; g.fillStyle = col; g.beginPath();
    for (let v = -R; v <= R; v += cell) for (let u = -R; u <= R; u += cell) { const x = Math.round(w / 2 + ca * u - sa * v), y = Math.round(h / 2 + sa * u + ca * v);
      if (x < 0 || y < 0 || x >= w || y >= h || P[at4(x, y) + 3] < 128) continue; const d = dens(x, y); if (d <= .03) continue;
      const rad = cell * .62 * Math.sqrt(Math.min(d, 1)); g.moveTo(x + rad, y); g.arc(x, y, rad, 0, TAU); }
    g.fill(); };
  const form = (x, y) => { const k = 3, ax = A[at4(x + k, y) + 3] - A[at4(x - k, y) + 3], ay = A[at4(x, y + k) + 3] - A[at4(x, y - k) + 3], m = Math.hypot(ax, ay) + 1e-6;
    const nx = -ax / m, ny = -ay / m, rim = Math.min(1, m / 60), ndl = nx * LIGHT[0] + ny * LIGHT[1];
    const along = (x / w - .5) * -LIGHT[0] + (y / h - .5) * -LIGHT[1];   // across the whole part: darker away from the light
    const i = at4(x, y), lum = .3 * P[i] + .59 * P[i + 1] + .11 * P[i + 2]; return { rim, ndl, along, lum }; };
  grid(BLK, ANG[BLK], 11, (x, y) => { const f = form(x, y); if (f.lum < 55) return 0; return .5 * Math.max(0, f.along * 1.6 + .05) + .55 * f.rim * Math.max(0, -f.ndl); });
  grid(BLUE, ANG[BLUE], 11, (x, y) => { const f = form(x, y); if (f.lum > 75) return 0; return .75 * f.rim * Math.max(0, f.ndl); });   // rim light on the dark coat
  return cv;
}

// ================= the "deputy" (the officer puppet, assets/officer) =================
let OP = null;
const OFEET = [470, 1392], OS = .74;
function officer(c, t, p) {
  const set = yelOn(t) ? SH.full : SH.two, M = OP;
  c.save(); c.translate(...OFEET); c.rotate(p.tilt || 0); c.scale(OS * (p.sx || 1), OS * (1 + (p.breath || 0))); c.translate(-M.feet[0], -M.feet[1] - (p.bob || 0));
  const part = (k, a = 0, o = {}) => { const m = M.parts[k], [px, py] = m.pivot; c.save(); c.translate(px + (o.dx || 0), py + (o.dy || 0)); c.rotate(a + (o.rot || 0)); c.translate(-px, -py); c.drawImage(set[k], m.x, m.y); c.restore(); };
  part('legL', p.legL || 0); part('legR', p.legR || 0); part('torso'); part('badge');
  c.save(); const [hx, hy] = M.parts.head.pivot; c.translate(hx, hy); c.rotate(p.head || 0); c.translate(-hx, -hy);
  part('head'); if (p.sweat > 0) sweat(c, 846, 470, p.sweat); part('cap', 0, p.cap || {}); c.restore();
  part('arm', p.arm || 0);
  c.restore();
}
function sweat(c, x, y, k) {   // a paper-cutout sweat drop: cream stock, black keyline, blue dots on its shadow side
  c.save(); c.translate(x, y); c.scale(k, k); const pts = []; for (let i = 0; i <= 24; i++) { const a = -Math.PI / 2 + i / 24 * TAU, r = 30 * (1 - .75 * Math.max(0, -Math.sin(a)) ** 3);
    pts.push([Math.cos(a) * r * .82, 18 + Math.sin(a) * (i === 0 || i === 24 ? 52 : 34)]); }
  block(c, pts, CHIP, 7101, { kw: 5 }); dotsIn(c, pts.map(([px, py]) => [px + 8, py + 6]), BLUE, .45, 7102, 8); c.restore();
}
function officerPose(t) {
  const u3 = at(0, 3), puff = t < u3 - .15 ? 0 : t < u3 ? -.015 * seg(t, u3 - .15, u3) : t < at(1) ? .035 * (1 - Math.exp(-(t - u3) * 10)) : .035 * Math.exp(-(t - at(1)) * 6);   // anticipation, then the chest puff
  const jolt = spring(t, at(1, 2), .05), capT = at(1, 3), shrink = t < at(1, 4) ? 0 : easeOut(seg(t, at(1, 4), at(1, 4) + .3));
  const capUp = t < capT - .05 ? 0 : t < capT ? -40 * seg(t, capT - .05, capT) : -14 - 26 * Math.exp(-(t - capT) * 8) * Math.cos((t - capT) * 20);
  return {
    breath: breath(t), bob: 4 * Math.abs(Math.sin(t * Math.PI / BEAT)) * (t < at(1) ? 1 : .4),
    head: .035 * Math.sin(t * TAU / (2 * BEAT)) - (t >= capT ? .06 * (1 - Math.exp(-(t - capT) * 9)) : 0) + spring(t, at(1, 2) + .08, .06),   // the head trails the jolt
    arm: .03 * Math.sin(t * TAU / BEAT), sx: 1 + puff - .03 * shrink, tilt: -.6 * puff + jolt + .02 * shrink,
    cap: { dy: capUp, rot: t >= capT ? -.05 * Math.exp(-(t - capT) * 5) : 0 },
    sweat: t < capT ? 0 : Math.min(1, easeOutBack(seg(t, capT, capT + .25))),
  };
}
const refPt = ([x, y], p) => [OFEET[0] + (x - OP.feet[0]) * OS, OFEET[1] + (y - OP.feet[1] - (p.bob || 0)) * OS];

// ================= lesson 11: the printed panel and its marks =================
const PANEL = { x: 80, y: 600, w: 800, h: 830 }, FLOOR = 1340;
function panel(c) {
  const { x, y, w, h } = PANEL;
  ink(c, rect(x, y, w, FLOOR - y), CHIP, 7201, { reg: false });
  dotScreen(c, polyPath(rect(x, y, w, FLOOR - y)), [x, y, w, FLOOR - y], { cell: 18, color: BLUE, density: (px, py) => .1 + .28 * Math.min(1, Math.hypot(px - OFEET[0], py - 980) / 560), angle: ANG[BLUE], seed: 7202 });
  ink(c, rect(x, FLOOR, w, y + h - FLOOR), CHIP, 7203, { reg: false });   // flat drawn floor
  key(c, [[x, FLOOR], [x + w, FLOOR]], 6, 7204, false);
  key(c, rect(x, y, w, h), 5, 7205);
}
function cropMarks(c) {
  const { x, y, w, h } = PANEL, g = 22, L = 56; c.save(); c.strokeStyle = BLK; c.lineWidth = 3; c.beginPath();
  for (const [cx, cy, sx, sy] of [[x, y, -1, -1], [x + w, y, 1, -1], [x, y + h, -1, 1], [x + w, y + h, 1, 1]]) {
    c.moveTo(cx + sx * g, cy); c.lineTo(cx + sx * (g + L), cy); c.moveTo(cx, cy + sy * g); c.lineTo(cx, cy + sy * (g + L)); }
  for (const mx of [x + w / 2]) { c.moveTo(mx, y - g); c.lineTo(mx, y - g - 30); c.moveTo(mx, y + h + g); c.lineTo(mx, y + h + g + 30); }   // centre ticks
  c.stroke(); c.restore();
}
function regTarget(c, x, y, t) {   // one target per ink, each printed with its own plate's offset: the misregistration shows
  const inks = yelOn(t) ? [BLUE, YEL, BLK] : [BLUE, BLK];
  for (const col of inks) { const [dx, dy] = REG[col] || [0, 0]; c.save(); c.translate(x + dx, y + dy); c.strokeStyle = col; c.lineWidth = 3;
    c.beginPath(); c.arc(0, 0, 18, 0, TAU); c.moveTo(-30, 0); c.lineTo(30, 0); c.moveTo(0, -30); c.lineTo(0, 30); c.stroke(); c.restore(); }
}
function colourBar(c, t) {   // the printer's colour bar under the panel: each ink solid and at 50 %
  const x0 = PANEL.x, y = PANEL.y + PANEL.h + 44, s = 50, gap = 12;
  const sw = [[BLUE, 1], [BLUE, .5], [BLK, 1], [BLK, .5], [YEL, 1], [YEL, .5]];
  sw.forEach(([col, d], k) => { const x = x0 + k * (s + gap), P = rect(x, y, s, s);
    if (col === YEL && !yelOn(t)) { c.save(); c.strokeStyle = BLK; c.globalAlpha = .35; c.lineWidth = 2; c.setLineDash([5, 5]); c.strokeRect(x, y, s, s); c.restore(); return; }   // this plate hasn't run yet
    if (d === 1) ink(c, P, col, 7300 + k); else dotsIn(c, P, col, d, 7300 + k, 8); });
}

// ================= the FAKE stamp (the one prop label) =================
const STAMP_T = at(1, 2);
function fakeStamp(c, t, p) {   // a yellow label in the yellow plate, black type, slapped on under the badge
  if (t < STAMP_T - SLAM) return; const [x, y] = refPt([730, 880], p), k = capPop(t, STAMP_T), size = 84;
  c.save(); c.translate(x, y); c.rotate(-.08); c.scale(k, k); c.font = `${size}px Stamp`; const w = c.measureText('FAKE').width + 56, h = size * 1.3;
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fillRect(-w / 2 + 8, -h / 2 + 10, w, h); c.restore();
  block(c, rect(-w / 2, -h / 2, w, h), YEL, 7501, { kw: 6 }); inkText(c, 'FAKE', 0, size * .06, size, 'Stamp', BLK, w); c.restore();
}

// ================= lesson 14: the real paper =================
function paperFinish(c) {   // the scan's fibres and flecks through every ink (overlay), and the paper's own light fibres where the ink skipped
  c.save(); resetT(c); c.globalCompositeOperation = 'overlay'; c.drawImage(IMG.grain, 0, 0, W, H); c.globalCompositeOperation = 'source-over'; c.drawImage(IMG.tooth, 0, 0, W, H); c.restore();
}

// ================= assembly =================
function drawScene(c, t) {
  screenSpace(c, () => { c.fillStyle = CREAM; c.fillRect(0, 0, W, H); });   // flat cream stock: the texture comes from the scan
  contentT(c);
  panel(c); cropMarks(c); regTarget(c, PANEL.x - 44, PANEL.y + PANEL.h / 2, t); regTarget(c, PANEL.x + PANEL.w + 44, PANEL.y + PANEL.h / 2, t); colourBar(c, t);
  const p = officerPose(t);
  c.save(); c.globalAlpha = 1; dotsIn(c, ellPts(OFEET[0] + 10, FLOOR + 22, 230 * (p.sx || 1), 26, 0, 30), BLK, .4, 7401, 9); c.restore();   // the shadow under him, in dots
  officer(c, t, p); fakeStamp(c, t, p);
  paperFinish(c);
  contentT(c); captionsTop(c, t);
  logoBug(c, 1);
  if (SHOW_SAFE) safeOverlay(c);
}

// ================= runtime =================
const CV = document.getElementById('c'); CV.width = OUT_W; CV.height = OUT_H; const CTX = CV.getContext('2d');
function frame(i) { const t = Math.min(i / FPS, DUR - 1e-6); FILM_T = t; resetT(CTX); CTX.globalAlpha = 1; drawScene(CTX, t); resetT(CTX); }
window.__NFR = NFR; window.__FPS = FPS; window.__frame = i => { frame(i); return CV.toDataURL('image/png'); };
window.__caps = () => CAPS.map(([t0, t1, ...s]) => ({ t0, t1, s: s.map(x => x[0]) }));
(async () => {
  await loadPrintKit(); await loadVertKit();
  await Promise.all([loadImg('grain', 'assets/demo/paper_grain.png'), loadImg('tooth', 'assets/demo/ink_tooth.png')]);
  OP = await (await fetch('assets/officer/officer_parts.json')).json();
  await Promise.all(PARTS.map(k => loadImg('officer_' + k, `assets/officer/officer_${k}.png`)));
  for (const k of PARTS) { SH.two[k] = shadedPart(IMG['officer_' + k], true); SH.full[k] = shadedPart(IMG['officer_' + k], false); }
  frame(+(Q.get('frame') || 0));
  window.__ready = true;
})().catch(e => { console.error(e); window.__error = String(e); });
