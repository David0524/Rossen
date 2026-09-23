'use strict';
/* Rossen Reports: "SCAM OR LEGIT?" quiz. 58.75 s, 1080x1920 (9:16), 24 fps, one shot. Case-file screen-print look
   (printkit.js, the approved blue/black/cream/yellow inks) with the vertical kit (vertkit.js). 96 BPM, one idea per bar.
   Each round is 7 bars: SHOW (1; the phone slides in on beat 1), PAUSE with a countdown (2), REVEAL: the verdict on
   beat 1 and a flag every two beats (2), TAKEAWAY (2).

   bars 0-6    round 1  SCAM   unpaid toll text        flags PAY TODAY, SMALL FEE, LINK
   bars 7-13   round 2  LEGIT  verification code       reasons YOU ASKED FOR IT, NO LINK, NO REQUEST
   bars 14-20  round 3  SCAM   fraud alert, reply Y/N  flags URGENT, REPLY YES OR NO
   bars 21-22  the last phone slides out; HOW MANY DID YOU GET RIGHT?, the answers, COMMENT YOUR SCORE: 0, 1, 2 OR 3?
   bar 23      the rubber stamp lands on beat 1; the official logo, untouched, still from 57.65 to 58.75
   The phone never moves while there is something to read.
*/
const DUR = at(23, 3), NFR = Math.round(FPS * DUR);
const CAPS = [];   // this film draws its own top band
const END_B = 21, STAMP_T = at(23);

// ================= the rounds =================
const LINK = 'htp://tol1-pay.zz/b1ll?7x';   // obviously garbled, not a real address
const ROUNDS = [
  { b: 0, scam: true, from: 'Toll Notice',
    lines: ['Your vehicle has an', 'unpaid toll balance of', '$6.99. Pay today to', 'avoid late fees:', LINK],
    marks: [{ l: 2, s: 'Pay today', tag: 'PAY TODAY' }, { l: 2, s: '$6.99', tag: 'SMALL FEE' }, { l: 4, s: LINK, tag: 'LINK' }],
    take: ["DON'T CLICK.", 'CHECK YOUR TOLL', 'ACCOUNT YOURSELF.'] },
  { b: 7, scam: false, from: 'Text Message',
    lines: ['Your verification code', "is 482913. Don't share", 'this code with anyone.', ''],
    marks: [{ l: 1, s: '482913', tag: 'YOU ASKED FOR IT' }, { l: 3, s: null, tag: 'NO LINK' }, { l: 2, s: 'this code with anyone.', tag: 'NO REQUEST' }],
    take: ['NEVER READ A CODE', 'TO ANYONE WHO CALLS.'] },
  { b: 14, scam: true, from: 'Account Alert',
    lines: ['FRAUD ALERT: $750', 'payment attempt.', 'Was this you?', 'Reply YES or NO.'],
    marks: [{ l: 0, s: 'FRAUD ALERT:', tag: 'URGENT' }, { l: 3, s: 'Reply YES or NO.', tag: 'REPLY YES OR NO' }],
    take: ["DON'T REPLY.", 'CALL THE NUMBER', 'ON YOUR CARD.'] },
];
const R_SHOW = 0, R_PAUSE = 1, R_REVEAL = 3, R_TAKE = 5;   // bar offsets inside a round

// ================= the phone =================
const PH = { x: 100, y: 640, w: 760, h: 600 };
const BUB = { x: PH.x + 30, y: PH.y + 176, w: PH.w - 60, pad: 30, pitch: 68, size: 54 };
const FONT = '"Liberation Sans"';
function lineFit(c, s) { c.font = `${BUB.size}px ${FONT}`; const w = c.measureText(s).width, maxW = BUB.w - 2 * BUB.pad; return w > maxW ? Math.floor(BUB.size * maxW / w) : BUB.size; }
const lineY = k => BUB.y + BUB.pad + 30 + k * BUB.pitch;
function phone(c, R, t) {
  const { x, y, w, h } = PH;
  shadowRect(c, x, y, w, h); block(c, rrPts(x, y, w, h, 60, 6), BLK, 6001, { kw: 6 });
  block(c, rrPts(x + 18, y + 48, w - 36, h - 72, 20, 4), CHIP, 6002, { kw: 3 });
  inkText(c, '9:41', x + 60, y + 26, 24, FONT, CHIP, 80, 'left');
  block(c, ellPts(x + w / 2, y + 86, 30, 30, 0, 24), R.scam ? BLUE : BLK, 6003, { kw: 4 }); inkText(c, R.from[0], x + w / 2, y + 89, 36, 'Stamp', CHIP, 40);
  inkText(c, R.from, x + w / 2, y + 138, 36, FONT, BLK, w - 120);
  ink(c, rect(x + 18, y + 162, w - 36, 3), BLK, 6004, { reg: false });
  const bh = BUB.pad * 2 + R.lines.length * BUB.pitch - 12;
  block(c, rrPts(BUB.x, BUB.y, BUB.w, bh, 30, 5), '#ffffff', 6005, { kw: 4, reg: false });
  highlights(c, R, t);   // under the text, so a mark never crosses a letter
  R.lines.forEach((s, k) => { if (!s) return; const link = s === LINK, sz = lineFit(c, s);
    inkText(c, s, BUB.x + BUB.pad, lineY(k), sz, FONT, link ? BLUE : BLK, BUB.w - 2 * BUB.pad, 'left');
    if (link) { c.font = `${sz}px ${FONT}`; ink(c, rect(BUB.x + BUB.pad, lineY(k) + sz * .52, c.measureText(s).width, 3), BLUE, 6006, { reg: false }); } });
}
// where a marked phrase sits in the bubble (the same font maths as the text itself)
function markBox(c, R, m) {
  const s = R.lines[m.l], y = lineY(m.l);
  if (!m.s) return { x: BUB.x + BUB.w * .5, y, w: 190, h: 46 };   // an empty spot: nothing to circle, the absence is the point
  const sz = lineFit(c, s); c.font = `${sz}px ${FONT}`; const i = s.indexOf(m.s), x0 = c.measureText(s.slice(0, i)).width, x1 = x0 + c.measureText(m.s).width;
  return { x: BUB.x + BUB.pad + (x0 + x1) / 2, y, w: x1 - x0, h: sz };
}
function markT(R, i) { return at(R.b + R_REVEAL) + (i + 1) * 2 * BEAT; }   // beat 3, then beats 1 and 3 of the next bar
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
  c.setLineDash([12, 10]); c.strokeStyle = BLUE; c.lineWidth = 6; c.strokeRect(box.x - box.w / 2 - 130, box.y - 30, box.w + 70, 62); c.setLineDash([]); c.restore();
  if (u > .4) check(c, box.x + 100, box.y + 4, .52, 1, 0);
}

// ================= the top band: title, stamp, takeaway =================
function chip(c, s, x, y, size, bg, fg, t, t0, rot = 0) {
  if (t < t0 - SLAM) return; c.font = `${size}px Stamp`; const w = Math.min(c.measureText(s).width, 780) + 60, h = size * 1.3, k = pop(t, t0);
  c.save(); c.translate(x, y); c.rotate(rot); c.scale(k, k);
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fillRect(-w / 2 + 8, -h / 2 + 10, w, h); c.restore();
  ink(c, rect(-w / 2, -h / 2, w, h), bg, 6100 + s.length, { amp: 3 }); inkText(c, s, 0, size * .06, size, 'Stamp', fg, 780); c.restore();
}
// the scorecard: one card per round. Future rounds show their number, the current round is highlighted, and an answered
// round flips to its answer on the reveal, so the viewer can keep score as they play
function scorecard(c, t, cur, y = 350, big = 1.22, t0 = -1) {
  const W0 = [170 * big, 240 * big], gap = 18 * big, ws = ROUNDS.map((_, i) => i === cur ? W0[1] : W0[0]), tot = ws.reduce((a, v) => a + v, 0) + gap * 2;
  let x = SCX - tot / 2;
  ROUNDS.forEach((R, i) => { const w = ws[i], h = 66 * big, tr = at(R.b + R_REVEAL), done = t >= tr - .02, cx = x + w / 2; x += w + gap;
    const tl = t0 >= 0 ? t0 + i * S16 : -1; if (tl >= 0 && t < tl - SLAM) return;
    const flip = done && t < tr + .2 ? Math.abs(Math.cos(seg(t, tr, tr + .2) * Math.PI)) : 1, k = tl >= 0 ? pop(t, tl) : 1;
    c.save(); c.translate(cx, y); c.scale(flip * k, k);
    const bg = done ? (R.scam ? BLK : BLUE) : i === cur ? YEL : CHIP, fg = done ? CHIP : BLK;
    c.save(); c.globalAlpha = .28; c.fillStyle = BLK; c.fillRect(-w / 2 + 7, -h / 2 + 8, w, h); c.restore();
    block(c, rect(-w / 2, -h / 2, w, h), bg, 6500 + i, { kw: 4 });
    inkText(c, done && !(t < tr + .1) ? (R.scam ? 'SCAM' : 'LEGIT') : i === cur ? `ROUND ${i + 1}` : String(i + 1), 0, 4 * big, 38 * big, 'Stamp', fg, w - 24 * big);
    c.restore(); });
}
// the answer pads: [SCAM] OR [LEGIT?]. They take turns pulsing through the countdown, lock on its last beat, and on the
// reveal the right one lights up and takes the stamp while the wrong one dims under an X
const PAD = { y: 482, w: 330, h: 124, x: [SCX - 225, SCX + 225] };
function pads(c, t, R, rn) {
  const b = R.b, tp = at(b + R_PAUSE), tl = at(b + R_PAUSE + 1, 4), tr = at(b + R_REVEAL), shown = rn === 0 ? -1 : at(b, 2);   // after the slide
  if (t < shown - SLAM) return;
  ['SCAM', 'LEGIT?'].forEach((lab, i) => {
    const right = (i === 0) === R.scam, beat = Math.floor((t - tp) / BEAT), pulse = t >= tp && t < tl && beat % 2 === i ? 1 + .07 * Math.exp(-((t - tp) % BEAT) * 6) : 1;
    let bg = i === 0 ? BLK : BLUE, fg = CHIP, k = pop(t, shown + i * S16) * pulse, dy = 0, lock = t >= tl - .02 && t < tr;
    if (t >= tr - .02) { if (right) { bg = YEL; fg = BLK; k *= 1.1 + .1 * Math.exp(-(t - tr) * 8); } else { bg = '#cfc8b8'; fg = '#8a8478'; dy = 10 * easeOut(seg(t, tr, tr + .2)); } }
    c.save(); c.translate(PAD.x[i], PAD.y + dy); c.scale(k, k); c.rotate(i ? .02 : -.02);
    c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fillRect(-PAD.w / 2 + 9, -PAD.h / 2 + 11, PAD.w, PAD.h); c.restore();
    block(c, rrPts(-PAD.w / 2, -PAD.h / 2, PAD.w, PAD.h, 26, 5), bg, 6600 + i, { kw: lock ? 12 : 6 });
    if (lock) key(c, rrPts(-PAD.w / 2 - 8, -PAD.h / 2 - 8, PAD.w + 16, PAD.h + 16, 30, 5), 6, 6610 + i, true, YEL);
    inkText(c, lab, 0, 8, 88, 'Stamp', fg, PAD.w - 40); c.restore();
    if (t >= tr - SLAM && !right) xMark(c, PAD.x[i], PAD.y + dy, .62, t, tr);
  });
  if (t < tr) chip(c, 'OR', SCX, PAD.y, 44, CHIP, BLK, t, shown, 0);
  if (t >= tr - SLAM) { const i = R.scam ? 0 : 1; stampFit(c, R.scam ? 'SCAM!' : 'LEGIT!', R.scam ? BLK : BLUE, 200, PAD.x[i], PAD.y, R.scam ? -.05 : .04, 1, t, tr, 318, 1.3); }   // inside the lit pad, its yellow edge showing
}
function topBand(c, t, R, rn) {
  const b = R.b;
  if (t < at(b + R_TAKE) - SLAM) { scorecard(c, t, rn); pads(c, t, R, rn); }
  else R.take.forEach((s, i) => chip(c, s, SCX, 356 + i * 104 + (t > at(b + R_TAKE, 2) ? 3 * Math.sin((t - at(b + R_TAKE)) * TAU / (2 * BEAT) + i) : 0), 70, R.scam ? BLK : BLUE, CHIP, t, at(b + R_TAKE) + i * E8, i % 2 ? .012 : -.012));
}
// ================= the bottom band: countdown, then the labelled flags =================
function countdown(c, t, R) {
  const t0 = at(R.b + R_PAUSE), t1 = at(R.b + R_REVEAL), tl = at(R.b + R_PAUSE + 1, 4); if (t < t0 - SLAM || t >= t1) return;
  if (t >= tl - SLAM) { stampFit(c, 'LOCK IT IN!', BLK, 130, SCX, 1335, -.04, .9, t, tl, 760, 1.3); return; }   // the last beat
  const u = clamp01((t - t0) / (t1 - t0)), n = Math.max(1, 8 - Math.floor((t - t0) / BEAT)), last = n <= 3;
  const x = 790, y = 1330, r = 88, k = pop(t, t0) * (last ? 1 + .08 * Math.max(0, Math.cos((t - t0) * TAU / BEAT)) : 1);
  c.save(); c.translate(x, y); c.scale(k, k);
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.beginPath(); c.arc(8, 10, r, 0, TAU); c.fill(); c.restore();
  block(c, ellPts(0, 0, r, r, 0, 40), CHIP, 6201, { kw: 6 });
  c.fillStyle = last ? YEL : BLUE; c.beginPath(); c.moveTo(0, 0); c.arc(0, 0, r - 12, -Math.PI / 2, -Math.PI / 2 + TAU * (1 - u)); c.closePath(); c.fill();
  block(c, ellPts(0, 0, r * .56, r * .56, 0, 30), BLK, 6202, { kw: 0, key: false });
  inkText(c, String(n), 0, 6, 78, 'Stamp', CHIP, 84); c.restore();
}
function flagRows(c, R) {   // lay the tags out in rows no wider than the safe width
  const rows = [[]]; let w = 0; c.font = '52px Stamp';
  R.marks.forEach((m, i) => { const tw = c.measureText(m.tag).width + 56; if (w + tw > 840 && rows[rows.length - 1].length) { rows.push([]); w = 0; } rows[rows.length - 1].push({ i, tw }); w += tw + 16; });
  const pos = []; rows.forEach((row, ri) => { const tot = row.reduce((a, q) => a + q.tw, 0) + 16 * (row.length - 1); let x = SCX - tot / 2;
    row.forEach(q => { pos[q.i] = [x + q.tw / 2, 1298 + ri * 90]; x += q.tw + 16; }); });
  return pos;
}
function flags(c, t, R) {
  const t0 = at(R.b + R_REVEAL); if (t < t0) return;
  const pos = flagRows(c, R), col = R.scam ? YEL : BLUE;
  R.marks.forEach((m, i) => { const ti = markT(R, i), u = easeOut(seg(t, ti - SLAM, ti + .1)); const box = markBox(c, R, m);
    if (!m.s) noLinkMark(c, box, u);
    chip(c, m.tag, pos[i][0], pos[i][1], 52, R.scam ? BLK : BLUE, CHIP, t, ti, (i % 2 ? .02 : -.02)); });
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
  jeff(c, 120, lerp(3000, 1850, a), .58, { armR, prop, head, bob });
}
function villain(c, t, R, X) {   // only in scam reveals: caught in the spotlight, then yanked off stage
  if (!R.scam) return; const t0 = at(R.b + R_REVEAL), t1 = at(R.b + R_TAKE); if (t < t0 - SLAM || t > t1 + .6) return;
  const out = easeOut(land(t, t0)), yank = easeIn(seg(t, t1, t1 + .45)), x = X + 790 + 500 * yank, y = lerp(1150, 880, out) - 650 * yank;
  const glow = t >= t0 ? 1 : 0;
  if (glow && yank < 1) { c.save(); c.globalAlpha = .9 * (1 - yank) ** 2; dotScreen(c, polyPath(ellPts(X + 790, 690, 125, 125, 0, 40)), [X + 665, 565, 250, 250], { cell: 10, color: YEL, density: .55, angle: 0, seed: 6401 }); c.restore(); }
  scammer(c, x, y, .5, { sx: -1, head: t >= t0 ? .12 * Math.sin((t - t0) * 40) * Math.exp(-(t - t0) * 3) : 0, tilt: -.5 * yank });
  return { x, y, yank };
}
function crook(c, t, R, v) {   // the vaudeville hook
  if (!R.scam || !v) return; const t1 = at(R.b + R_TAKE), a = easeOut(seg(t, t1 - .25, t1)), yank = easeIn(seg(t, t1, t1 + .45)); if (a <= 0 || yank >= 1) return;
  const hx = v.x + 10, hy = v.y - 230, bx = lerp(1250, hx + 60, a) + 500 * yank;
  c.save(); c.lineCap = 'round';
  for (const [w, cl] of [[30, BLK], [18, YEL]]) { c.strokeStyle = cl; c.lineWidth = w; c.beginPath(); c.moveTo(bx + 500, hy + 500); c.lineTo(bx + 40, hy + 30); c.arc(bx, hy, 44, .6, Math.PI * 1.25, true); c.stroke(); }
  c.restore();
}

// ================= scenes =================
function stage(c, t, rn, X) {   // one round's phone, marks and villain, offset horizontally by X
  const R = ROUNDS[rn];
  c.save(); c.translate(X, 0); phone(c, R, t); flags(c, t, R); c.restore();
  // the villain pops up in front of the phone's top-right corner, clipped to the header so he never covers the message
  c.save(); c.beginPath(); c.rect(X + 640, 560, 300, PH.y + 162 - 560); c.clip(); const v = villain(c, t, R, X); c.restore();
  crook(c, t, R, v);
}
function roundAt(t) { for (let i = ROUNDS.length - 1; i >= 0; i--) if (t >= at(ROUNDS[i].b) - .01) return i; return 0; }
function sceneRounds(c, t) {
  bgDots(c, BLUE, .08, .45);
  const rn = roundAt(t), R = ROUNDS[rn];
  // the slide to the next round: the last beat of the takeaway bar
  host(c, t, rn);   // behind the labels, so he never covers a tag
  if (rn > 0 && t < at(R.b, 2)) {   // beat 1 of a new round: the last phone slides out as the new one slides in
    const u = easeIO(seg(t, at(R.b), at(R.b, 2)));
    stage(c, t, rn - 1, -1250 * u); stage(c, t, rn, 1250 * (1 - u)); scorecard(c, t, rn);
  } else { stage(c, t, rn, 0); topBand(c, t, R, rn); countdown(c, t, R); }
}
function sceneEnd(c, t) {   // bars 21-22
  bgDots(c, BLUE, .12, .55);
  const E = END_B, [sx, sy] = shake(t, [[at(E, 2), 14], [at(E, 3), 12]]), beatPulse = t > at(E + 1) ? 1 + .025 * Math.max(0, Math.cos((t - at(E + 1)) * TAU / BEAT)) : 1;
  if (t < at(E, 2)) { const u = easeIO(seg(t, at(E), at(E, 2)));   // round 3 slides out, the host with it
    c.save(); c.translate(-1250 * u, 0); host(c, t, ROUNDS.length - 1); c.restore(); stage(c, t, ROUNDS.length - 1, -1250 * u); }
  const th = easeOutBack(seg(t, at(E, 3), at(E, 3.5)));
  jeffUp(c, t, at(E, 2.5), SCX, { armR: lerp(0, -2.5, th), prop: th > .6 ? 'thumb' : null, head: t > at(E + 1) ? .05 * Math.sin((t - at(E + 1)) * TAU / (2 * BEAT)) : 0 }, .7);
  c.save(); c.translate(sx, sy);
  stampFit(c, 'HOW MANY DID', BLK, 140, SCX, 400, -.04, .95 * beatPulse, t, at(E, 2), 840, 1.25);
  stampFit(c, 'YOU GET RIGHT?', BLK, 140, SCX, 560, .03, .95 * beatPulse, t, at(E, 2.5), 840, 1.25);
  scorecard(c, t, -1, 722, 1.55, at(E, 3));   // the answers: SCAM, LEGIT, SCAM
  stampFit(c, 'COMMENT YOUR SCORE:', BLUE, 120, SCX, 885, -.03, 1 * beatPulse, t, at(E, 3.5), 840, 1.25);
  chip(c, '0, 1, 2 OR 3?', SCX, 1040, 92, BLK, CHIP, t, at(E, 3.5) + .01, .02);
  c.restore();
  const d = seg(t, at(E + 1, 3.5), STAMP_T); if (d > 0) screenSpace(c, () => rubberStamp(c, easeIn(d)));   // over a bar of END text first
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
  if (t < at(END_B)) sceneRounds(c, t);
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
