'use strict';
/* "Unpaid toll" explainer. For now, the 5 s look test (?test=1): one evidence moment, 2 bars at 96 BPM.
   bar 0  the fake toll text is pinned to the cream board from frame 0; CLUE 1: THE LATE FEE. Jeff raises his highlighter on 2,
          sweeps "Pay now to avoid a $50.00 late fee" on 3 (lands on 3), holds on 4
   bar 1  CLUE 2: THE LINK. He swaps to the blue marker on 1, circles the garbled link on 2-3 (closes on 3), holds on 4
   Camera: one smooth push-in through the evidence plane (24 fps). Jeff and the marks: on twos (onTwos). Captions: level, land
   from 1.05, then hold completely still. No real toll agency, company, number or address. */
const TEST = Q.has('test');
const DUR = TEST ? at(2) : at(2), NFR = Math.round(FPS * DUR);
const SANS = '"Liberation Sans"', MONO = '"Liberation Mono"';

// ================= captions: level black chips, one set at a time =================
const CAPS = [[at(0), 'CLUE 1:', 'THE LATE FEE'], [at(1), 'CLUE 2:', 'THE LINK']];
function capChip(c, s, x, y, size, bg, fg, t, t0) {   // level; lands from 1.05 on t0, then holds perfectly still
  if (t < t0 - SLAM && t0 > 0) return; c.font = `${size}px Stamp`; const w = Math.min(c.measureText(s).width, 720) + 64, h = size * 1.32;
  const k = t0 <= 0 || t >= t0 ? 1 : lerp(1.05, 1, easeOut(land(t, t0)));
  c.save(); c.translate(x, y); c.scale(k, k);
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fillRect(-w / 2 + 8, -h / 2 + 10, w, h); c.restore();
  c.fillStyle = bg; c.fillRect(-w / 2, -h / 2, w, h); fitText(c, s, 0, size * .06, size, 'Stamp', fg, 720); c.restore();
}
function captions(c, t) {
  let cur = null; for (const cp of CAPS) if (t >= cp[0] - SLAM) cur = cp;
  if (!cur) return;
  cur.slice(1).forEach((s, i) => capChip(c, s, SCX, 376 + i * 112, 70, i ? BLUE : BLK, CHIP, t, cur[0] > 0 ? cur[0] + i * E8 : 0));   // frame 0: already landed
}

// ================= the evidence: a phone pinned to the board =================
const PH = { x: 200, y: 625, w: 560, h: 800 };
const MSG = 'TOLL SERVICES: Your vehicle has an outstanding toll balance of $12.51. Pay now to avoid a $50.00 late fee:';
const LINK = 'htps://t0ll-servlces.pay-qz.zz/k9?', SENDER = '+00 555-XXX-XXXX';
let LAYOUT = null;
function layoutMsg(c) {   // wraps the message into lines and records where each word sits (for the marks)
  const size = 39, x0 = PH.x + 58, maxW = PH.w - 116, lh = 50; c.font = `${size}px ${SANS}`;
  const words = MSG.split(' '), lines = [], pos = []; let line = [], w = 0;
  for (const wd of words) { const ww = c.measureText(wd + ' ').width; if (w + ww > maxW && line.length) { lines.push(line); line = []; w = 0; } line.push([wd, w]); w += ww; }
  lines.push(line);
  const y0 = PH.y + 322;
  lines.forEach((ln, i) => ln.forEach(([wd, dx]) => pos.push({ wd, x: x0 + dx, y: y0 + i * lh, w: c.measureText(wd).width })));
  const linkY = y0 + lines.length * lh + 14;
  return { size, lh, pos, linkY, x0, maxW, bubble: [PH.x + 40, PH.y + 270, PH.w - 80, linkY - PH.y - 270 + 44] };
}
function spanRects(from, to) {   // one rect per line for the words from..to (inclusive), for the highlighter
  const L = LAYOUT, i0 = L.pos.findIndex(p => p.wd === from), i1 = L.pos.findIndex((p, i) => i >= i0 && p.wd === to);
  const rows = {}; for (let i = i0; i <= i1; i++) { const p = L.pos[i]; (rows[p.y] ||= []).push(p); }
  return Object.values(rows).map(ps => ({ x: ps[0].x - 6, y: ps[0].y - L.size * .82, w: ps[ps.length - 1].x + ps[ps.length - 1].w - ps[0].x + 12, h: L.size * 1.12 }));
}
function phoneEvidence(c, tt) {   // tt: the on-twos clock, for the marks
  const { x, y, w, h } = PH;
  c.save(); c.globalAlpha = .28; c.fillStyle = BLK; c.fill(polyPath(rrPts(x + 16, y + 20, w, h, 54, 6))); c.restore();
  block(c, rrPts(x, y, w, h, 54, 6), BLK, 7001, { kw: 5 });
  block(c, rrPts(x + 20, y + 58, w - 40, h - 116, 20, 4), '#ffffff', 7002, { kw: 3, reg: false });
  // the conversation header: a random number
  c.fillStyle = '#ebe7df'; c.fillRect(x + 20, y + 58, w - 40, 150);
  c.fillStyle = BLK; c.beginPath(); c.arc(x + w / 2, y + 110, 30, 0, TAU); c.fill();
  inkText(c, SENDER, x + w / 2, y + 172, 32, SANS, BLK, w - 90);
  inkText(c, 'Text Message', x + w / 2, y + 236, 24, SANS, '#6d6a66', w - 90);
  // the message bubble
  const L = LAYOUT, [bx, by, bw, bh] = L.bubble;
  c.fillStyle = '#e4e1da'; c.fill(polyPath(rrPts(bx, by, bw, bh, 30, 6)));
  // clue 1: the late fee, highlighted behind the words (sweeps on 3 of bar 0)
  const hu = seg(tt, at(0, 2), at(0, 3)); let acc = 0; const R = spanRects('Pay', 'fee:'), tot = R.reduce((s, r) => s + r.w, 0);
  R.forEach((r, i) => { const u = clamp01((hu * tot - acc) / r.w); highlighter(c, r.x, r.y, r.w, r.h, u, 7101 + i); acc += r.w; });
  c.font = `${L.size}px ${SANS}`; c.fillStyle = '#1b1b1b'; c.textAlign = 'left'; c.textBaseline = 'alphabetic';
  for (const p of L.pos) c.fillText(p.wd, p.x, p.y);
  c.fillStyle = '#1a55c8'; c.font = `${L.size - 5}px ${SANS}`; c.fillText(LINK, L.x0, L.linkY, L.maxW);
  c.fillRect(L.x0, L.linkY + 5, Math.min(L.maxW, c.measureText(LINK).width), 2.5);
  // pinned: tape at the top, a pushpin
  c.save(); c.translate(x + w / 2, y - 6); c.rotate(-.05); c.globalAlpha = .9; ink(c, rect(-90, -26, 180, 52), CREAM, 7201, { amp: 4, reg: false }); c.restore();
  pushpin(c, x + w - 36, y + 30);
}
const linkBox = () => { const L = LAYOUT; return { cx: L.x0 + L.maxW / 2, cy: L.linkY - 10, rx: L.maxW / 2 + 36, ry: 44 }; };   // clear of the letters

// ================= the scene =================
function camAt(t) {   // one slow smooth push-in: from the whole phone to the link
  const u = Q.has('nocam') ? 0 : easeIO(clamp01(t / DUR));   // ?nocam=1 freezes the camera (to check the on-twos cadence)
  return { x: 480, y: 840, z: lerp(1.0, 1.14, u) };   // focus at y 840: the phone's top edge stays below the captions (>= y 580)
}
function scene(c, t) {
  creamBg(c);
  const tt = onTwos(t), cam = camAt(t);
  camLayer(c, cam, .35, () => {   // the board behind: a few pins and a string line, moving less than the evidence
    for (const [px, py] of [[110, 640], [860, 700], [880, 1330]]) pushpin(c, px, py);
  });
  camLayer(c, cam, 1, () => {
    phoneEvidence(c, tt);
    const lb = linkBox(), cu = seg(tt, at(1, 2), at(1, 3));
    circleMark(c, lb.cx, lb.cy, lb.rx, lb.ry, cu, BLUE, 10, 3);
  });
  // Jeff, in front (depth 1.15), on twos; his marker tip follows the mark being drawn
  camLayer(c, cam, 1.15, () => {
    const b1 = tt >= at(1) - 1e-6, b0 = b1 ? at(1) : at(0), m0 = b0 + BEAT, m1 = b0 + 2 * BEAT;   // marking: beat 2 -> 3
    const inU = easeOut(seg(tt, m0 - BEAT * .6, m0)), outU = easeIn(seg(tt, m1 + BEAT * .1, m1 + BEAT * .7)), up = inU * (1 - outU);
    let tip, hu = seg(tt, m0, m1);
    if (!b1) { const R = spanRects('Pay', 'fee:'), tot = R.reduce((q, r) => q + r.w, 0); let acc = 0; tip = [R[0].x, R[0].y + R[0].h / 2];
      for (const r of R) { if (hu * tot <= acc + r.w) { tip = [r.x + Math.max(0, hu * tot - acc), r.y + r.h / 2]; break; } acc += r.w; tip = [r.x + r.w, r.y + r.h / 2]; } }
    else { const lb = linkBox(), a = -2.3 + TAU * 1.12 * hu; tip = [lb.cx + Math.cos(a) * lb.rx, lb.cy + Math.sin(a) * lb.ry]; }
    const J = jeff(c, 150, 1860, .66, { armR: lerp(-.2, -1.95, up), prop: up < .3 ? 'point' : null, head: -.05 + .03 * Math.sin(tt * 2), bob: Math.abs(Math.sin(tt * Math.PI / BEAT)) * 3 });
    if (up > .02) markerProp(c, J.hand, [lerp(J.hand[0] + 40, tip[0], up), lerp(J.hand[1] - 40, tip[1], up)], b1 ? BLUE : YEL);
  });
}
function drawScene(c, t) { contentT(c); scene(c, t); contentT(c); captions(c, t); printFinish(c); if (SHOW_SAFE) safeOverlay(c); }

// ================= runtime =================
const CV = document.getElementById('c'); CV.width = OUT_W; CV.height = OUT_H; const CTX = CV.getContext('2d');
function frame(i) { const t = Math.min(i / FPS, DUR - 1e-6); FILM_T = t; resetT(CTX); CTX.globalAlpha = 1; drawScene(CTX, t); resetT(CTX); }
window.__NFR = NFR; window.__FPS = FPS; window.__frame = i => { frame(i); return CV.toDataURL('image/png'); };
(async () => {
  await loadPrintKit(); await loadVertKit(); makeCream();
  LAYOUT = layoutMsg(CTX);
  frame(+(Q.get('frame') || 0));
  window.__ready = true;
})().catch(e => { console.error(e); window.__error = String(e); });
