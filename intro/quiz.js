'use strict';
/* Rossen Reports: "SCAM OR LEGIT?" quiz. 42.5 s, 1080x1920 (9:16), 24 fps, one shot. Case-file screen-print look
   (printkit.js, the approved blue/black/cream/yellow inks) with the vertical kit (vertkit.js). 96 BPM, one idea per bar.
   Each round is 5 bars: SHOW (1), PAUSE with a countdown (2), REVEAL: stamp + flags (1), TAKEAWAY (1).

   bars 0-4    round 1  SCAM   unpaid toll text        flags PAY TODAY, SMALL FEE, LINK
   bars 5-9    round 2  LEGIT  verification code       reasons YOU ASKED FOR IT, NO LINK, NO REQUEST
   bars 10-14  round 3  SCAM   fraud alert, reply Y/N  flags URGENT, REPLY YES OR NO
   bar 15-16   HOW MANY DID YOU GET RIGHT? COMMENT YOUR SCORE.; the rubber stamp lands on bar 16 beat 3
   the official logo, untouched, still from 41.40 to 42.5
   The phone never moves while there is something to read; it slides between rounds on the last beat of each round.
*/
const DUR = at(17), NFR = Math.round(FPS * DUR);
const CAPS = [];   // this film draws its own top band
const STAMP_T = at(16, 3);

// ================= the rounds =================
const LINK = 'htp://tol1-pay.zz/b1ll?7x';   // obviously garbled, not a real address
const ROUNDS = [
  { b: 0, scam: true, from: 'Toll Notice',
    lines: ['Your vehicle has an', 'unpaid toll balance of', '$6.99. Pay today to', 'avoid late fees:', LINK],
    marks: [{ l: 2, s: 'Pay today', tag: 'PAY TODAY' }, { l: 2, s: '$6.99', tag: 'SMALL FEE' }, { l: 4, s: LINK, tag: 'LINK' }],
    take: ["DON'T CLICK.", 'CHECK YOUR TOLL', 'ACCOUNT YOURSELF.'] },
  { b: 5, scam: false, from: 'Text Message',
    lines: ['Your verification code', "is 482913. Don't share", 'this code with anyone.', ''],
    marks: [{ l: 1, s: '482913', tag: 'YOU ASKED FOR IT' }, { l: 3, s: null, tag: 'NO LINK' }, { l: 2, s: 'this code with anyone.', tag: 'NO REQUEST' }],
    take: ['NEVER READ A CODE', 'TO ANYONE WHO CALLS.'] },
  { b: 10, scam: true, from: 'Account Alert',
    lines: ['FRAUD ALERT: $750', 'payment attempt.', 'Was this you?', 'Reply YES or NO.'],
    marks: [{ l: 0, s: 'FRAUD ALERT:', tag: 'URGENT' }, { l: 3, s: 'Reply YES or NO.', tag: 'REPLY YES OR NO' }],
    take: ["DON'T REPLY.", 'CALL THE NUMBER', 'ON YOUR CARD.'] },
];
const R_SHOW = 0, R_PAUSE = 1, R_REVEAL = 3, R_TAKE = 4;   // bar offsets inside a round

// ================= the phone =================
const PH = { x: 170, y: 590, w: 620, h: 620 };
const BUB = { x: PH.x + 36, y: PH.y + 200, w: PH.w - 72, pad: 28, pitch: 58, size: 42 };
const FONT = '"Liberation Sans"';
function lineFit(c, s) { c.font = `${BUB.size}px ${FONT}`; const w = c.measureText(s).width, maxW = BUB.w - 2 * BUB.pad; return w > maxW ? Math.floor(BUB.size * maxW / w) : BUB.size; }
const lineY = k => BUB.y + BUB.pad + 24 + k * BUB.pitch;
function phone(c, R, t) {
  const { x, y, w, h } = PH;
  shadowRect(c, x, y, w, h); block(c, rrPts(x, y, w, h, 60, 6), BLK, 6001, { kw: 6 });
  block(c, rrPts(x + 18, y + 56, w - 36, h - 112, 20, 4), CHIP, 6002, { kw: 3 });
  inkText(c, '9:41', x + 60, y + 32, 26, FONT, CHIP, 80, 'left');
  block(c, ellPts(x + w / 2, y + 104, 28, 28, 0, 24), R.scam ? BLUE : BLK, 6003, { kw: 4 }); inkText(c, R.from[0], x + w / 2, y + 107, 34, 'Stamp', CHIP, 40);
  inkText(c, R.from, x + w / 2, y + 160, 30, FONT, BLK, w - 120);
  ink(c, rect(x + 18, y + 186, w - 36, 3), BLK, 6004, { reg: false });
  const bh = BUB.pad * 2 + R.lines.length * BUB.pitch - 10;
  block(c, rrPts(BUB.x, BUB.y, BUB.w, bh, 30, 5), '#ffffff', 6005, { kw: 4, reg: false });
  highlights(c, R, t);   // under the text, so a mark never crosses a letter
  R.lines.forEach((s, k) => { if (!s) return; const link = s === LINK, sz = lineFit(c, s);
    inkText(c, s, BUB.x + BUB.pad, lineY(k), sz, FONT, link ? BLUE : BLK, BUB.w - 2 * BUB.pad, 'left');
    if (link) { c.font = `${sz}px ${FONT}`; ink(c, rect(BUB.x + BUB.pad, lineY(k) + sz * .52, c.measureText(s).width, 3), BLUE, 6006, { reg: false }); } });
}
// where a marked phrase sits in the bubble (the same font maths as the text itself)
function markBox(c, R, m) {
  const s = R.lines[m.l], y = lineY(m.l);
  if (!m.s) return { x: BUB.x + BUB.w * .5, y, w: 150, h: 36 };   // an empty spot: nothing to circle, the absence is the point
  const sz = lineFit(c, s); c.font = `${sz}px ${FONT}`; const i = s.indexOf(m.s), x0 = c.measureText(s.slice(0, i)).width, x1 = x0 + c.measureText(m.s).width;
  return { x: BUB.x + BUB.pad + (x0 + x1) / 2, y, w: x1 - x0, h: sz };
}
function markT(R, i) { return at(R.b + R_REVEAL) + (i + 1) * BEAT; }
function highlights(c, R, t) {   // a marker swiped left to right behind each flagged phrase, on its beat
  R.marks.forEach((m, i) => { if (!m.s) return; const u = easeOut(seg(t, markT(R, i) - SLAM, markT(R, i) + .12)); if (u <= 0) return;
    const b = markBox(c, R, m), x0 = b.x - b.w / 2 - 10, w = (b.w + 20) * u, y0 = b.y - b.h * .62, h = b.h * 1.2;
    const P = [[x0, y0 + 3], [x0 + w, y0], [x0 + w, y0 + h - 2], [x0, y0 + h]];
    if (R.scam) ink(c, P, YEL, 6310 + i, { amp: 3, reg: false }); else ink(c, P, '#bcd2f0', 6310 + i, { amp: 3, reg: false }); });   // a pale tint of the logo blue, so the code stays crisp
}
function markerCircle(c, box, u, col, seed) {   // a hand-drawn marker ellipse, drawn on over u 0..1; never over the letters
  if (u <= 0) return; const rx = box.w / 2 + 20, ry = box.h / 2 + 12, r = rng(seed), a0 = -1.9 + r() * .3, n = 48;
  const pts = []; for (let i = 0; i <= n * u * 1.08; i++) { const a = a0 + i / n * TAU, j = 1 + .04 * Math.sin(i * .7 + seed); pts.push([box.x + Math.cos(a) * rx * j, box.y + 2 + Math.sin(a) * ry * j]); }
  if (pts.length < 2) return;
  for (const [w, cl] of [[14, BLK], [8, col]]) { c.save(); c.strokeStyle = cl; c.lineWidth = w; c.lineCap = 'round'; c.lineJoin = 'round'; c.beginPath(); pts.forEach(([x, y], i) => i ? c.lineTo(x, y) : c.moveTo(x, y)); c.stroke(); c.restore(); }
}
function noLinkMark(c, box, u) {   // round 2: where a link would be, a dashed empty slot with a check
  if (u <= 0) return; c.save(); c.globalAlpha = Math.min(1, u * 2);
  c.setLineDash([12, 10]); c.strokeStyle = BLUE; c.lineWidth = 6; c.strokeRect(box.x - box.w / 2 - 110, box.y - 24, box.w + 60, 50); c.setLineDash([]); c.restore();
  if (u > .4) check(c, box.x + 80, box.y + 4, .42, 1, 0);
}

// ================= the top band: title, stamp, takeaway =================
function chip(c, s, x, y, size, bg, fg, t, t0, rot = 0) {
  if (t < t0 - SLAM) return; c.font = `${size}px Stamp`; const w = Math.min(c.measureText(s).width, 800) + 60, h = size * 1.3, k = pop(t, t0);
  c.save(); c.translate(x, y); c.rotate(rot); c.scale(k, k);
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fillRect(-w / 2 + 8, -h / 2 + 10, w, h); c.restore();
  ink(c, rect(-w / 2, -h / 2, w, h), bg, 6100 + s.length, { amp: 3 }); inkText(c, s, 0, size * .06, size, 'Stamp', fg, 800); c.restore();
}
function topBand(c, t, R, rn) {
  const b = R.b, beatPulse = 1 + .03 * Math.max(0, Math.cos((t - at(b)) * TAU / BEAT));
  if (t < at(b + R_REVEAL) - SLAM) {
    chip(c, `ROUND ${rn + 1} OF 3`, SCX, 350, 46, BLUE, CHIP, t, rn === 0 ? -1 : at(b), -.02);
    c.save(); c.translate(SCX, 462); const pz = t > at(b + R_PAUSE) ? beatPulse : 1; c.scale(pz, pz); c.translate(-SCX, -462);
    chip(c, 'SCAM OR LEGIT?', SCX, 462, 82, BLK, CHIP, t, rn === 0 ? -1 : at(b) + E8, .015); c.restore();
  } else if (t < at(b + R_TAKE) - SLAM) {
    stampFit(c, R.scam ? 'SCAM!' : 'LEGIT!', R.scam ? BLK : BLUE, 190, SCX, 440, R.scam ? -.07 : .05, 1, t, at(b + R_REVEAL));
  } else R.take.forEach((s, i) => chip(c, s, SCX, 352 + i * 96, 60, R.scam ? BLK : BLUE, CHIP, t, at(b + R_TAKE) + i * E8, i % 2 ? .012 : -.012));
}
// ================= the bottom band: countdown, then the labelled flags =================
function countdown(c, t, R) {
  const t0 = at(R.b + R_PAUSE), t1 = at(R.b + R_REVEAL); if (t < t0 - SLAM || t >= t1) return;
  const u = clamp01((t - t0) / (t1 - t0)), n = Math.max(1, 8 - Math.floor((t - t0) / BEAT)), last = n <= 3;
  const x = 780, y = 1330, r = 74, k = pop(t, t0) * (last ? 1 + .08 * Math.max(0, Math.cos((t - t0) * TAU / BEAT)) : 1);
  c.save(); c.translate(x, y); c.scale(k, k);
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.beginPath(); c.arc(8, 10, r, 0, TAU); c.fill(); c.restore();
  block(c, ellPts(0, 0, r, r, 0, 40), CHIP, 6201, { kw: 6 });
  c.fillStyle = last ? YEL : BLUE; c.beginPath(); c.moveTo(0, 0); c.arc(0, 0, r - 12, -Math.PI / 2, -Math.PI / 2 + TAU * (1 - u)); c.closePath(); c.fill();
  block(c, ellPts(0, 0, r * .56, r * .56, 0, 30), BLK, 6202, { kw: 0, key: false });
  inkText(c, String(n), 0, 5, 64, 'Stamp', CHIP, 70); c.restore();
}
function flagRows(c, R) {   // lay the tags out in rows no wider than the safe width
  const rows = [[]]; let w = 0; c.font = '44px Stamp';
  R.marks.forEach((m, i) => { const tw = c.measureText(m.tag).width + 56; if (w + tw > 820 && rows[rows.length - 1].length) { rows.push([]); w = 0; } rows[rows.length - 1].push({ i, tw }); w += tw + 16; });
  const pos = []; rows.forEach((row, ri) => { const tot = row.reduce((a, q) => a + q.tw, 0) + 16 * (row.length - 1); let x = SCX - tot / 2;
    row.forEach(q => { pos[q.i] = [x + q.tw / 2, 1272 + ri * 96]; x += q.tw + 16; }); });
  return pos;
}
function flags(c, t, R) {
  const t0 = at(R.b + R_REVEAL); if (t < t0) return;
  const pos = flagRows(c, R), col = R.scam ? YEL : BLUE;
  R.marks.forEach((m, i) => { const ti = markT(R, i), u = easeOut(seg(t, ti - SLAM, ti + .1)); const box = markBox(c, R, m);
    if (!m.s) noLinkMark(c, box, u);
    chip(c, m.tag, pos[i][0], pos[i][1], 44, R.scam ? BLK : BLUE, CHIP, t, ti, (i % 2 ? .02 : -.02)); });
}

// ================= the host and the villain =================
function host(c, t, rn) {
  let armR = -1.05, prop = null, head = .08 * Math.sin((t - at(0)) * Math.PI / (2 * BEAT)), bob = Math.abs(Math.sin(t * Math.PI / BEAT)) * 5;
  if (rn >= 0) { const R = ROUNDS[rn], b = R.b;
    if (t < at(b + R_PAUSE)) { armR = -2.15; prop = 'point'; head = .05; }                          // "round n!"
    else if (t >= at(b + R_REVEAL)) { const u = easeOutBack(seg(t, at(b + R_REVEAL, 1.5), at(b + R_REVEAL, 1.9)));
      armR = lerp(-1.05, R.scam ? -1.9 : -2.5, u); prop = u > .6 ? (R.scam ? 'point' : 'thumb') : null; head = R.scam ? -.06 : .06; } }
  if (rn === 0 && t < at(0, 2) - SLAM) return;
  const a = rn === 0 ? easeOutBack(land(t, at(0, 2))) : 1;
  jeff(c, 130, lerp(2900, 1830, a), .5, { armR, prop, head, bob });
}
function villain(c, t, R, X) {   // only in scam reveals: caught in the spotlight, then yanked off stage
  if (!R.scam) return; const t0 = at(R.b + R_REVEAL), t1 = at(R.b + R_TAKE); if (t < t0 - SLAM || t > t1 + .6) return;
  const out = easeOut(land(t, t0)), yank = easeIn(seg(t, t1, t1 + .45)), x = X + lerp(690, 812, out) + 700 * yank, y = 950 - 160 * yank;
  const glow = t >= t0 ? 1 : 0;
  if (glow && yank < 1) { c.save(); c.globalAlpha = .9; dotScreen(c, polyPath(ellPts(X + 830, 700, 150, 150, 0, 40)), [X + 680, 550, 300, 300], { cell: 10, color: YEL, density: .55, angle: 0, seed: 6401 }); c.restore(); }
  scammer(c, x, y, .55, { sx: -1, head: t >= t0 ? .12 * Math.sin((t - t0) * 40) * Math.exp(-(t - t0) * 3) : 0, tilt: -.5 * yank });
  return { x, y, yank };
}
function crook(c, t, R, v) {   // the vaudeville hook
  if (!R.scam || !v) return; const t1 = at(R.b + R_TAKE), a = easeOut(seg(t, t1 - .25, t1)), yank = easeIn(seg(t, t1, t1 + .45)); if (a <= 0 || yank >= 1) return;
  const hx = v.x - 5, hy = v.y - 170, bx = lerp(1250, hx + 60, a) + 700 * yank;
  c.save(); c.lineCap = 'round';
  for (const [w, cl] of [[30, BLK], [18, YEL]]) { c.strokeStyle = cl; c.lineWidth = w; c.beginPath(); c.moveTo(bx + 500, hy + 500); c.lineTo(bx + 40, hy + 30); c.arc(bx, hy, 44, .6, Math.PI * 1.25, true); c.stroke(); }
  c.restore();
}

// ================= scenes =================
function stage(c, t, rn, X) {   // one round's phone, marks and villain, offset horizontally by X
  const R = ROUNDS[rn];
  const v = villain(c, t, R, X);
  c.save(); c.translate(X, 0); phone(c, R, t); flags(c, t, R); c.restore();
  crook(c, t, R, v);
}
function roundAt(t) { for (let i = ROUNDS.length - 1; i >= 0; i--) if (t >= at(ROUNDS[i].b) - .01) return i; return 0; }
function sceneRounds(c, t) {
  bgDots(c, BLUE, .08, .45);
  const rn = roundAt(t), R = ROUNDS[rn];
  // the slide to the next round: the last beat of the takeaway bar
  const sw = at(R.b + R_TAKE, 4), u = easeIO(seg(t, sw, sw + BEAT)), next = rn + 1 < ROUNDS.length;
  if (t < sw) { stage(c, t, rn, 0); topBand(c, t, R, rn); countdown(c, t, R); }
  else { stage(c, t, rn, -1150 * u); if (next) stage(c, at(ROUNDS[rn + 1].b), rn + 1, 1150 * (1 - u)); }
  host(c, t, rn);
}
function sceneEnd(c, t) {   // bars 15-16
  bgDots(c, BLUE, .12, .55);
  const [sx, sy] = shake(t, [[at(15), 14], [at(15, 2), 12]]), beatPulse = t > at(16) ? 1 + .025 * Math.max(0, Math.cos((t - at(16)) * TAU / BEAT)) : 1;
  const th = easeOutBack(seg(t, at(15, 2.5), at(15, 3)));
  jeffUp(c, t, at(15, 1.5), SCX, { armR: lerp(0, -2.5, th), prop: th > .6 ? 'thumb' : null, head: t > at(16) ? .05 * Math.sin((t - at(16)) * TAU / (2 * BEAT)) : 0 }, .7);
  c.save(); c.translate(sx, sy);
  stampFit(c, 'HOW MANY DID', BLK, 140, SCX, 420, -.04, .85 * beatPulse, t, at(15), 800, 1.25);
  stampFit(c, 'YOU GET RIGHT?', BLK, 140, SCX, 590, .03, .85 * beatPulse, t, at(15, 1.5), 800, 1.25);
  stampFit(c, 'COMMENT', BLUE, 150, SCX, 800, -.03, .9 * beatPulse, t, at(15, 2), 800, 1.25);
  stampFit(c, 'YOUR SCORE.', BLUE, 150, SCX, 975, .03, .9 * beatPulse, t, at(15, 2.5), 800, 1.25);
  c.restore();
  const d = seg(t, at(16, 2.5), STAMP_T); if (d > 0) screenSpace(c, () => rubberStamp(c, easeIn(d)));   // a full bar of END text first
}
function sceneSignoff(c, t) {
  paperBg(c);
  // the official logo: exact file, uniformly scaled, no texture or recolour, centred on the frame; held still
  const im = IMG.logo, [bx, by, bw, bh] = IMG.logoBox, lw = 720, lh = bh * lw / bw;
  c.drawImage(im, bx, by, bw, bh, CX - lw / 2, SCY - lh / 2, lw, lh);
  const lift = seg(t, STAMP_T, STAMP_T + .15);
  if (lift < 1) { c.save(); c.translate(0, -(H + 320) * easeIn(lift)); rubberStampFlat(c); c.restore(); }
}
function drawScene(c, t) {
  contentT(c);
  if (t < at(15)) sceneRounds(c, t);   // the last phone slides out on the final beat of round 3
  else if (t < STAMP_T) sceneEnd(c, t);
  else { resetT(c); sceneSignoff(c, t); return; }   // screen space; no print finish over the official logo
  printFinish(c);
  if (SHOW_SAFE) safeOverlay(c);
}

// ================= runtime =================
const CV = document.getElementById('c'); CV.width = OUT_W; CV.height = OUT_H; const CTX = CV.getContext('2d');
function frame(i) { const t = Math.min(i / FPS, DUR - 1e-6); FILM_T = t; resetT(CTX); CTX.globalAlpha = 1; drawScene(CTX, t); resetT(CTX); }
window.__NFR = NFR; window.__FPS = FPS; window.__frame = i => { frame(i); return CV.toDataURL('image/png'); };
(async () => {
  await loadPrintKit(); await loadVertKit();
  frame(+(Q.get('frame') || 0));
  window.__ready = true;
})().catch(e => { console.error(e); window.__error = String(e); });
