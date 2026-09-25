'use strict';
/* Rossen Reports explainer: the "unpaid toll" text scam. 44.5 s, 1080x1920 (9:16), 24 fps, one continuous film.
   House style (the case-file screen print, the approved palette, Jeff and the Scammer, 96 BPM, one idea per bar, the
   readability rules, the closing card), with a few techniques borrowed from Vox (VOX_STUDY.md), each used on purpose:
   - evidence mark-up: only on the phone, one mark per clue, a different mark for each clue
   - on twos (onTwos): puppets and cut-out graphics only; text and the camera stay smooth
   - a 2.5D camera: one slow push through the evidence (board behind, phone, Jeff in front)
   - one number: the FBI stat
   - three standout transitions, and nothing fancy anywhere else:
       [1] bar 6: the camera dives through the circled link into the fake page
       [2] bar 7: a fast pull-back (the motion trail peaks on the cut): the fake page shrinks to one pin on the map
       [3] bar 14: after a beat of silence, the strip unfolds, one panel per beat
   No real toll agency, state service, company, number or address anywhere.

   HOOK      bar 0-1   the text, pinned to the cream board, from frame 0      "WHY DID I GET / A TOLL BILL FOR A / ROAD I NEVER DROVE?"
                       (Jeff pops up on bar 1)
   EVIDENCE  bar 2     a highlighter behind the late fee                        "CLUE 1: URGENCY"
             bar 3     a circle around the garbled link                        "CLUE 2: THE LINK / NOT THE REAL SITE"
             bar 4     a pointer and an underline at $12.51                    "CLUE 3: THE TINY FEE / EASY TO JUST PAY"
             bar 5     a scribbled underline under the sender                  "CLUE 4: THE SENDER / A RANDOM NUMBER"
             bar 6     [1] the dive; the fake pay page                         "IT OPENS A / FAKE PAY PAGE"
   SCALE     bar 7     [2] the pull-back; pins pop across the map on eighths   "YOU'RE NOT ALONE."
             bar 8-9   the stat card lands and counts up, then holds           (the card is the only text)
   HOW       bar 10    the Scammer sends a spray of texts                      "SCAMMERS TEXT / IN BULK"
             bar 11    a few phones in a row get tapped                        "A FEW PEOPLE / TAP THE LINK"
             bar 12    a card slides into the fake page                        "THE FAKE PAGE / TAKES THEIR CARD"
             bar 13    the Scammer reels the cards in; the last beat is silent "AND THE SCAMMER / COLLECTS."
   FIX       bar 14-15 [3] the strip unfolds (1, 2, 3); Jeff; the stamp on 15:4   (the strip is the only text)
   END       bar 16    the closing card, still for its last 4.2 s
*/
const DUR = at(16) + 4.5, NFR = Math.round(FPS * DUR);
const SANS = '"Liberation Sans"', MONO = '"Liberation Mono"';
const PUSH = .3;

// ================= captions: level chips; they land from 1.05, then hold completely still =================
const CAPS = [
  [at(0), 'WHY DID I GET', 'A TOLL BILL FOR A', 'ROAD I NEVER DROVE?'],
  [at(2), 'CLUE 1: URGENCY'], [at(3), 'CLUE 2: THE LINK', 'NOT THE REAL SITE'], [at(4), 'CLUE 3: THE TINY FEE', 'EASY TO JUST PAY'],
  [at(5), 'CLUE 4: THE SENDER', 'A RANDOM NUMBER'], [at(6), 'IT OPENS A', 'FAKE PAY PAGE'], [at(7), "YOU'RE NOT ALONE."], [at(8), null],
  [at(10), 'SCAMMERS TEXT', 'IN BULK'], [at(11), 'A FEW PEOPLE', 'TAP THE LINK'], [at(12), 'THE FAKE PAGE', 'TAKES THEIR CARD'],
  [at(13), 'AND THE SCAMMER', 'COLLECTS.'], [at(14), null],
];
function capChip(c, s, x, y, size, bg, fg, t, t0) {
  if (t < t0 - SLAM && t0 > 0) return; c.font = `${size}px Stamp`; const w = Math.min(c.measureText(s).width, 720) + 60, h = size * 1.32;
  const k = t0 <= 0 || t >= t0 ? 1 : lerp(1.05, 1, easeOut(land(t, t0)));
  c.save(); c.translate(x, y); c.scale(k, k);
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fillRect(-w / 2 + 8, -h / 2 + 10, w, h); c.restore();
  c.fillStyle = bg; c.fillRect(-w / 2, -h / 2, w, h); fitText(c, s, 0, size * .06, size, 'Stamp', fg, 720); c.restore();
}
function captions(c, t) {
  let cur = null; for (const cp of CAPS) if (t >= cp[0] - SLAM) cur = cp;
  if (!cur || !cur[1]) return;
  const n = cur.length - 1, step = n > 2 ? 96 : 104;
  cur.slice(1).forEach((s, i) => capChip(c, s, SCX, 372 + i * step, 62, i ? BLUE : BLK, CHIP, t, cur[0] > 0 ? cur[0] + i * E8 : 0));
}

// ================= the evidence: the phone pinned to the board =================
const PH = { x: 200, y: 640, w: 560, h: 790 };
const MSG = 'TOLL SERVICES: Your vehicle has an outstanding toll balance of $12.51. Pay now to avoid a $50.00 late fee:';
const LINK = 'htps://t0ll-servlces.pay-qz.zz/k9?', SENDER = '+00 555-XXX-XXXX';
let LAYOUT = null;
function layoutMsg(c) {
  const size = 39, x0 = PH.x + 58, maxW = PH.w - 116, lh = 50; c.font = `${size}px ${SANS}`;
  const words = MSG.split(' '), lines = [], pos = []; let line = [], w = 0;
  for (const wd of words) { const ww = c.measureText(wd + ' ').width; if (w + ww > maxW && line.length) { lines.push(line); line = []; w = 0; } line.push([wd, w]); w += ww; }
  lines.push(line);
  const y0 = PH.y + 322;
  lines.forEach((ln, i) => ln.forEach(([wd, dx]) => pos.push({ wd, x: x0 + dx, y: y0 + i * lh, w: c.measureText(wd).width })));
  const linkY = y0 + lines.length * lh + 14;
  c.font = `32px ${SANS}`; const sw = c.measureText(SENDER).width;
  return { size, lh, pos, linkY, x0, maxW, bubble: [PH.x + 40, PH.y + 270, PH.w - 80, linkY - PH.y - 270 + 44], sender: { x: PH.x + PH.w / 2 - sw / 2, y: PH.y + 172, w: sw } };
}
function spanRects(from, to) {
  const L = LAYOUT, i0 = L.pos.findIndex(p => p.wd === from), i1 = L.pos.findIndex((p, i) => i >= i0 && p.wd === to);
  const rows = {}; for (let i = i0; i <= i1; i++) { const p = L.pos[i]; (rows[p.y] ||= []).push(p); }
  return Object.values(rows).map(ps => ({ x: ps[0].x - 6, y: ps[0].y - L.size * .82, w: ps[ps.length - 1].x + ps[ps.length - 1].w - ps[0].x + 12, h: L.size * 1.12 }));
}
const linkBox = () => { const L = LAYOUT; return { cx: L.x0 + L.maxW / 2, cy: L.linkY - 10, rx: L.maxW / 2 + 36, ry: 44 }; };
const feeWord = () => LAYOUT.pos.find(p => p.wd === '$12.51.');
const MARK = { fee: at(2, 2), link: at(3, 2), tiny: at(4, 2), sender: at(5, 2) };   // each mark draws from beat 2 to beat 3 (on twos)
const markU = (tt, k) => seg(tt, MARK[k], MARK[k] + BEAT);
function marks(c, tt) {   // on the evidence plane (the highlighter is drawn by phoneEvidence, behind the words)
  const lb = linkBox(); circleMark(c, lb.cx, lb.cy, lb.rx, lb.ry, markU(tt, 'link'), BLUE, 10, 3);
  const fw = feeWord(), tu = markU(tt, 'tiny');   // clue 3: a pointer in from the margin, then an underline
  if (tu > 0) { pointer(c, [PH.x - 40, fw.y + 80], [fw.x - 12, fw.y - 8], clamp01(tu * 1.6), BLK, 7);
    const uu = clamp01(tu * 1.6 - .6) / .4; if (uu > 0) { c.save(); c.strokeStyle = BLK; c.lineWidth = 6; c.lineCap = 'round'; c.beginPath(); c.moveTo(fw.x, fw.y + 10); c.lineTo(fw.x + (fw.w - 8) * clamp01(uu), fw.y + 12); c.stroke(); c.restore(); } }
  const S = LAYOUT.sender, su = markU(tt, 'sender');   // clue 4: a scribbled double underline under the sender
  if (su > 0) { c.save(); c.strokeStyle = BLUE; c.lineWidth = 7; c.lineCap = 'round'; c.beginPath();
    const n = 24, m = Math.round(n * su); for (let i = 0; i <= m; i++) { const q = i / n, x = q < .5 ? S.x - 10 + (S.w + 20) * q * 2 : S.x + S.w + 10 - (S.w + 20) * (q - .5) * 2, y = S.y + 16 + (q < .5 ? 0 : 12) + 2 * Math.sin(i * 1.7);
      i ? c.lineTo(x, y) : c.moveTo(x, y); } c.stroke(); c.restore(); }
}
function markerTip(tt) {   // where Jeff's marker is in bars 2-5 (null when he isn't marking)
  const b = Math.floor(tt / BAR + 1e-6), k = { 2: 'fee', 3: 'link', 4: 'tiny', 5: 'sender' }[b]; if (!k) return null;
  const u = markU(tt, k); let tip;
  if (k === 'fee') { const R = spanRects('Pay', 'fee:'), tot = R.reduce((q, r) => q + r.w, 0); let acc = 0; tip = [R[0].x, R[0].y + R[0].h / 2];
    for (const r of R) { if (u * tot <= acc + r.w) { tip = [r.x + Math.max(0, u * tot - acc), r.y + r.h / 2]; break; } acc += r.w; tip = [r.x + r.w, r.y + r.h / 2]; } }
  if (k === 'link') { const lb = linkBox(), a = -2.3 + TAU * 1.12 * u; tip = [lb.cx + Math.cos(a) * lb.rx, lb.cy + Math.sin(a) * lb.ry]; }
  if (k === 'tiny') { const fw = feeWord(), q = clamp01(u * 1.6); tip = q < 1 ? [lerp(PH.x - 40, fw.x - 12, q), lerp(fw.y + 80, fw.y - 8, q)] : [fw.x + (fw.w - 8) * clamp01((u * 1.6 - .6) / .4), fw.y + 12]; }
  if (k === 'sender') { const S = LAYOUT.sender; tip = u < .5 ? [S.x - 10 + (S.w + 20) * u * 2, S.y + 16] : [S.x + S.w + 10 - (S.w + 20) * (u - .5) * 2, S.y + 28]; }
  return { k, tip, col: { fee: YEL, link: BLUE, tiny: BLK, sender: BLUE }[k] };
}
function phoneEvidence(c, tt) {
  const { x, y, w, h } = PH;
  c.save(); c.globalAlpha = .28; c.fillStyle = BLK; c.fill(polyPath(rrPts(x + 16, y + 20, w, h, 54, 6))); c.restore();
  block(c, rrPts(x, y, w, h, 54, 6), BLK, 7001, { kw: 5 });
  block(c, rrPts(x + 20, y + 58, w - 40, h - 116, 20, 4), '#ffffff', 7002, { kw: 3, reg: false });
  c.fillStyle = '#ebe7df'; c.fillRect(x + 20, y + 58, w - 40, 150);
  c.fillStyle = BLK; c.beginPath(); c.arc(x + w / 2, y + 110, 30, 0, TAU); c.fill();
  inkText(c, SENDER, x + w / 2, y + 172, 32, SANS, BLK, w - 90);
  inkText(c, 'Text Message', x + w / 2, y + 236, 24, SANS, '#6d6a66', w - 90);
  const L = LAYOUT, [bx, by, bw, bh] = L.bubble;
  c.fillStyle = '#e4e1da'; c.fill(polyPath(rrPts(bx, by, bw, bh, 30, 6)));
  const hu = markU(tt, 'fee'); let acc = 0; const R = spanRects('Pay', 'fee:'), tot = R.reduce((s, r) => s + r.w, 0);
  R.forEach((r, i) => { const u = clamp01((hu * tot - acc) / r.w); highlighter(c, r.x, r.y, r.w, r.h, u, 7101 + i); acc += r.w; });
  c.font = `${L.size}px ${SANS}`; c.fillStyle = '#1b1b1b'; c.textAlign = 'left'; c.textBaseline = 'alphabetic';
  for (const p of L.pos) c.fillText(p.wd, p.x, p.y);
  c.fillStyle = '#1a55c8'; c.font = `${L.size - 5}px ${SANS}`; c.fillText(LINK, L.x0, L.linkY, L.maxW);
  c.fillRect(L.x0, L.linkY + 5, Math.min(L.maxW, c.measureText(LINK).width), 2.5);
  c.save(); c.translate(x + w / 2, y - 6); c.rotate(-.05); c.globalAlpha = .9; ink(c, rect(-90, -26, 180, 52), CREAM, 7201, { amp: 4, reg: false }); c.restore();
  pushpin(c, x + w - 36, y + 30);
}
function camEvidence(t) {   // one slow push (bars 0-5); then, into bar 6, the dive toward the link
  const u = easeIO(clamp01(t / at(6))), lb = linkBox();
  const cam = { x: 480, y: 845, z: lerp(1.0, 1.13, u) };
  const d = easeIn(seg(t, at(6) - .45, at(6) + .15)); cam.x = lerp(cam.x, lb.cx, d); cam.y = lerp(cam.y, lb.cy, d); cam.z = lerp(cam.z, 3.4, d);
  return cam;
}
function sceneEvidence(c, t) {
  creamBg(c);
  const tt = onTwos(t), cam = camEvidence(t);
  camLayer(c, cam, .35, () => { for (const [px, py] of [[110, 680], [860, 740], [880, 1360]]) pushpin(c, px, py); });
  camLayer(c, cam, 1, () => { phoneEvidence(c, tt); marks(c, tt); });
  camLayer(c, cam, 1.15, () => {   // Jeff pops up on bar 1, then marks one clue per bar (on twos)
    if (tt < at(1) - SLAM) return;
    const pop = easeOutBack(land(tt, at(1))), mk = markerTip(tt);
    let up = 0; if (mk) { const m0 = MARK[mk.k], inU = easeOut(seg(tt, m0 - BEAT * .6, m0)), outU = easeIn(seg(tt, m0 + BEAT * 1.1, m0 + BEAT * 1.7)); up = inU * (1 - outU); }
    const J = jeff(c, 150, lerp(2700, 1860, pop), .66, { armR: lerp(-.2, -1.95, up), prop: up < .3 ? 'point' : null, head: -.05 + .03 * Math.sin(tt * 2), bob: Math.abs(Math.sin(tt * Math.PI / BEAT)) * 3 });
    if (mk && up > .02) markerProp(c, J.hand, [lerp(J.hand[0] + 40, mk.tip[0], up), lerp(J.hand[1] - 40, mk.tip[1], up)], mk.col);
  });
}

// ================= the fake pay page =================
const FP = { x: 110, y: 620, w: 740, h: 800 };
function fakePage(c, t) {
  creamBg(c);
  const { x, y, w, h } = FP;
  c.save(); c.globalAlpha = .28; c.fillStyle = BLK; c.fillRect(x + 16, y + 20, w, h); c.restore();
  block(c, rrPts(x, y, w, h, 30, 6), '#ffffff', 7301, { kw: 6, reg: false });
  c.fillStyle = '#ebe7df'; c.fillRect(x + 6, y + 6, w - 12, 96);
  c.fillStyle = '#ffffff'; c.fill(polyPath(rrPts(x + 30, y + 24, w - 60, 60, 30, 6)));
  inkText(c, LINK.replace('/k9?', ''), x + 58, y + 56, 30, SANS, '#555', w - 110, 'left');
  c.fillStyle = BLUE; c.fillRect(x + 6, y + 102, w - 12, 110);
  inkText(c, 'Toll Services', x + 40, y + 160, 50, SANS, CHIP, w - 80, 'left');   // plain text only: no logo, no real agency
  inkText(c, 'Outstanding balance', x + 40, y + 268, 32, SANS, '#444', w - 80, 'left');
  inkText(c, '$12.51', x + 40, y + 332, 64, SANS, BLK, w - 80, 'left');
  const field = (label, fx, fy, fw) => { inkText(c, label, fx, fy, 28, SANS, '#444', fw, 'left'); c.strokeStyle = '#8b8883'; c.lineWidth = 3; c.strokeRect(fx, fy + 18, fw, 70); };
  field('Card number', x + 40, y + 420, w - 80); field('Expiration', x + 40, y + 540, 300); field('Security code', x + 380, y + 540, 320);
  if (Math.floor(t * 3) % 2) { c.fillStyle = BLK; c.fillRect(x + 56, y + 454, 4, 40); }   // the cursor, waiting
  c.fillStyle = YEL; c.fill(polyPath(rrPts(x + 40, y + 680, w - 80, 84, 42, 6))); inkText(c, 'Pay now', x + w / 2, y + 724, 40, SANS, BLK, 300);
}

// ================= the map and the stat =================
let US = null;
const PIN0 = [540, 1050];   // where the pull-back lands: the fake page becomes this pin
let PINS = [];
function inUS(x, y) { let ins = false; const P = US; for (let i = 0, j = P.length - 1; i < P.length; j = i++) { const [xi, yi] = P[i], [xj, yj] = P[j]; if ((yi > y) !== (yj > y) && x < (xj - xi) * (y - yi) / (yj - yi) + xi) ins = !ins; } return ins; }
function makePins() { const r = rng(4242); let n = 0;
  while (PINS.length < 15 && n++ < 5000) { const x = lerp(140, 830, r()), y = lerp(790, 1150, r()); if (inUS(x, y) && inUS(x, y - 50) && [PIN0, ...PINS].every(p => Math.hypot(p[0] - x, p[1] - y) > 95)) PINS.push([x, y]); } }
function mapPin(c, x, y, k) { if (k <= 0) return; c.save(); c.translate(x, y); c.scale(k, k);
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.beginPath(); c.ellipse(4, 4, 16, 6, 0, 0, TAU); c.fill(); c.restore();
  c.strokeStyle = BLK; c.lineWidth = 5; c.beginPath(); c.moveTo(0, 0); c.lineTo(0, -34); c.stroke();
  c.fillStyle = YEL; c.beginPath(); c.arc(0, -44, 16, 0, TAU); c.fill(); c.lineWidth = 4; c.stroke(); c.restore(); }
const PIN_T = k => at(7, 1.5) + k * E8 * .5;   // on sixteenths from beat 1.5 of bar 7 (the last lands on beat 4.5)
function sceneMap(c, t) {
  bgDots(c, BLUE, .08, .4);
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fill(polyPath(US.map(([x, y]) => [x + 10, y + 12]))); c.restore();
  block(c, US, CHIP, 7401, { kw: 6 });
  const tt = onTwos(t);
  mapPin(c, PIN0[0], PIN0[1], 1);
  PINS.forEach(([x, y], k) => { const t0 = PIN_T(k); if (tt < t0 - SLAM) return; mapPin(c, x, y, tt < t0 ? .6 + .4 * seg(tt, t0 - SLAM, t0) : 1 + .08 * Math.exp(-(tt - t0) * 10)); });
  if (t >= at(8) - SLAM) statCard(c, t);
}
function statCard(c, t) {   // level; lands from 1.05 on bar 8; the number counts up to its value on beat 2, then everything holds
  const k = t >= at(8) ? 1 : lerp(1.05, 1, easeOut(land(t, at(8)))), n = Math.round(60000 * easeOut(clamp01((t - at(8)) / BEAT)));
  const w = 720, h = 330, cx = SCX, cy = 1275;   // below the map (which ends at y 1168), so the pins stay in view
  c.save(); c.translate(cx, cy); c.scale(k, k);
  c.save(); c.globalAlpha = .35; c.fillStyle = BLK; c.fillRect(-w / 2 + 14, -h / 2 + 18, w, h); c.restore();
  c.fillStyle = BLK; c.fillRect(-w / 2, -h / 2, w, h);
  fitText(c, n.toLocaleString('en-US') + '+', 0, -62, 120, 'Stamp', YEL, w - 80);
  fitText(c, 'COMPLAINTS TO THE FBI', 0, 36, 46, 'Stamp', CHIP, w - 70);
  fitText(c, 'IN 2024', 0, 94, 46, 'Stamp', CHIP, w - 70);
  fitText(c, 'SOURCE: FBI', 0, 142, 28, SANS, CHIP, w - 70);
  c.restore();
}
function pullBack(c, t) {   // [2] at(7) - .2 .. at(7) + .15: the fake page shrinks fast to PIN0 while the map pulls back
  const u = easeIO(seg(t, at(7) - .2, at(7) + .15));
  const g1 = L1.getContext('2d'); contentT(g1); g1.globalAlpha = 1; fakePage(g1, at(7) - .2); contentT(g1); captions(g1, at(7) - .2 - 1e-3); printFinish(g1);
  const g2 = L2.getContext('2d'); contentT(g2); g2.globalAlpha = 1; sceneMap(g2, Math.max(t, at(7))); contentT(g2); captions(g2, Math.max(t, at(7) - SLAM)); printFinish(g2);
  const pin = [CX + (PIN0[0] - SCX) * K, SCY + (PIN0[1] - 44 - SCY) * K];   // PIN0's head, on screen
  screenSpace(c, () => {
    const zm = lerp(3.2, 1, u); c.save(); c.translate(pin[0], pin[1]); c.scale(zm, zm); c.translate(-pin[0], -pin[1]); c.drawImage(L2, 0, 0, W, H); c.restore();
    const trail = Math.sin(Math.PI * u);   // the page, shrinking into the pin, with a short motion trail that peaks on the cut
    for (let i = 4; i >= 0; i--) { const v = clamp01(u - i * .05 * trail), s = lerp(1, .02, v); if (v >= 1) continue;
      c.save(); c.globalAlpha = i ? .22 * trail : 1; c.translate(lerp(CX, pin[0], v), lerp(CY, pin[1], v)); c.scale(s, s); c.drawImage(L1, -W / 2, -H / 2, W, H); c.restore(); }
  });
}

// ================= how it works: a paper flow, one step per bar (on a tall board; the camera steps down) =================
const STEP_Y = [760, 1300, 1840, 2380];
function flowCam(t) { let y = STEP_Y[0]; for (let k = 1; k < 4; k++) y = lerp(y, STEP_Y[k], easeIO(seg(t, at(10 + k) - .3, at(10 + k) + .25))); return y; }
function smallPhone(c, x, y, s, lit, seed) { c.save(); c.translate(x, y); c.scale(s, s);
  block(c, rrPts(-50, -90, 100, 180, 16, 4), BLK, seed, { kw: 4 }); c.fillStyle = lit ? YEL : '#ffffff'; c.fillRect(-40, -72, 80, 144);
  c.fillStyle = '#d8d4cc'; c.fill(polyPath(rrPts(-32, -54, 64, 40, 10, 4))); c.restore(); }
function payCard(c, x, y, s, rot, seed) { c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s);
  block(c, rrPts(-90, -56, 180, 112, 12, 4), BLUE, seed, { kw: 4 }); c.fillStyle = YEL; c.fillRect(-66, -30, 36, 26);
  c.fillStyle = CHIP; for (let i = 0; i < 4; i++) c.fillRect(-66 + i * 36, 18, 26, 8); c.restore(); }
function bubble(c, x, y, s) { c.save(); c.translate(x, y); c.scale(s, s); block(c, rrPts(-44, -26, 88, 52, 16, 4), CHIP, 7501, { kw: 4 });
  block(c, [[-20, 22], [-4, 22], [-24, 40]], CHIP, 7502, { kw: 0, key: false }); c.fillStyle = BLK; for (let i = 0; i < 3; i++) c.fillRect(-26 + i * 20, -4, 12, 8); c.restore(); }
function sceneFlow(c, t) {
  bgDots(c, BLUE, .07, .35);
  const tt = onTwos(t), cy = flowCam(t);
  c.save(); c.beginPath(); c.rect(-400, 612, 1800, 1400); c.clip();   // below the captions: earlier steps slide away under this edge, never under the text
  c.translate(0, 1000 - cy);
  for (let k = 1; k < 4; k++) if (tt >= at(10 + k) - .35) pointer(c, [480, STEP_Y[k - 1] + 175], [480, STEP_Y[k] - 185], seg(tt, at(10 + k) - .1, at(10 + k) + .3), BLK, 8);
  // 1: the Scammer sends a spray of texts (bubbles on eighths)
  if (tt < at(11) + .3) {
  const tip = scammer(c, 250, STEP_Y[0] + 190, .55, { rod: -.2, head: .05 * Math.sin(tt * 6), bob: Math.abs(Math.sin(tt * Math.PI / BEAT)) * 4 });
  for (let i = 0; i < 7; i++) { const t0 = at(10, 1.5) + i * E8, u = easeOut(seg(tt, t0 - .3, t0)); if (u <= 0) continue; const a = -.9 + i * .3;
    bubble(c, lerp(tip[0], 580 + Math.cos(a) * 250, u), lerp(tip[1], STEP_Y[0] + 30 + Math.sin(a) * 120, u), .9); }
  }
  const shows = k => tt >= at(10 + k) - .35 && (k === 3 || tt < at(11 + k) + .3);   // each step shows only while the camera is on it: one step per bar
  // 2: a row of phones; two get tapped (beats 2 and 3)
  if (shows(1)) {
  const taps = { 1: at(11, 2), 4: at(11, 3) };
  for (let i = 0; i < 6; i++) { const x = 130 + i * 140, t0 = taps[i], lit = t0 !== undefined && tt >= t0; smallPhone(c, x, STEP_Y[1], .95, lit, 7600 + i); if (t0 !== undefined) tapRing(c, x, STEP_Y[1], tt, t0); }
  }
  // 3: the fake page takes a card (slides in from 1.5, lands on 3)
  if (shows(2)) {
  smallPhone(c, 540, STEP_Y[2], 1.6, false, 7700);
  const cu = easeIn(seg(tt, at(12, 2), at(12, 3))); if (tt >= at(12, 1.5)) payCard(c, lerp(200, 540, cu), STEP_Y[2] + lerp(40, 0, cu), lerp(1, .55, cu), lerp(-.2, 0, cu), 7710);
  }
  // 4: the Scammer reels the cards in (on 2, 3, 4)
  if (shows(3)) {
  const t4 = scammer(c, 700, STEP_Y[3] + 200, .6, { sx: -1, rod: -.3 + .1 * Math.sin(tt * 5), head: tt > at(13, 2) ? .08 * Math.sin(tt * 14) : 0, bob: Math.abs(Math.sin(tt * Math.PI / BEAT)) * 4 });
  for (let i = 0; i < 3; i++) { const t0 = at(13, 2 + i), u = easeIn(seg(tt, t0 - .35, t0)); if (tt < t0 - .35) continue;
    const hx = lerp(180 + i * 70, t4[0] - 20, u), hy = lerp(STEP_Y[3] - 120, t4[1] + 80 + i * 44, u); fishLine(c, t4, [hx, hy - 60], 10); payCard(c, hx, hy, .5, .2 - i * .2, 7720 + i); }
  }
  c.restore();
}

// ================= the fix: after a beat of silence, the strip unfolds =================
const STRIP = { x: 150, y: 620, w: 660, ph: 200 };
const PANELS = [["DON'T TAP", 'THE LINK.', BLK], ['CHECK YOUR TOLL', null, BLUE], ['ACCOUNT YOURSELF.', null, BLUE]];
const OPEN_T = [at(14), at(14, 2), at(14, 3)];   // the folded strip is pinned up on 1; panels 2 and 3 land on beats 2 and 3
function panelFace(c, k, x, y, w, h) { const [a, b, col] = PANELS[k];
  c.fillStyle = col; c.fillRect(x, y, w, h); key(c, rect(x, y, w, h), 5, 7800 + k);
  if (b) { fitText(c, a, x + w / 2, y + h * .34, 70, 'Stamp', CHIP, w - 70); fitText(c, b, x + w / 2, y + h * .72, 70, 'Stamp', CHIP, w - 70); }
  else fitText(c, a, x + w / 2, y + h / 2 + 4, 64, 'Stamp', CHIP, w - 60); }
function sceneFix(c, t) {
  creamBg(c);
  const tt = onTwos(t), { x, y, w, ph } = STRIP;
  const open = OPEN_T.map((t0, k) => k === 0 ? 1 : clamp01(seg(tt, t0 - SLAM * 2, t0)));
  const shown = 1 + (open[1] >= 1 ? 1 : 0) + (open[1] >= 1 && open[2] >= 1 ? 1 : 0);
  c.save(); c.globalAlpha = .25; c.fillStyle = BLK; c.fillRect(x + 12, y + 14, w, ph * shown); c.restore();
  const drop = t < OPEN_T[0] ? lerp(1.05, 1, easeOut(land(t, OPEN_T[0]))) : 1;   // the folded strip lands level
  const flip = (k, back) => { const u = open[k], hy = y + k * ph, sc = Math.cos(Math.PI * (1 - u));   // a panel flipping down about its top hinge
    if ((sc < 0) !== back) return; c.save(); c.translate(0, hy); c.scale(1, sc);
    if (sc > 0) panelFace(c, k, x, 0, w, ph); else { c.fillStyle = '#d9cdb2'; c.fillRect(x, 0, w, ph); key(c, rect(x, 0, w, ph), 5, 7810 + k); } c.restore(); };
  const active = k => (k === 1 || open[1] >= 1) && open[k] > 0 && open[k] < 1;
  for (let k = 1; k < 3; k++) if (active(k)) flip(k, true);   // still folded back: behind the panel above it
  c.save(); c.translate(x + w / 2, y); c.scale(drop, drop); c.translate(-(x + w / 2), -y); panelFace(c, 0, x, y, w, ph); c.restore();
  for (let k = 1; k < 3; k++) { if (k === 2 && open[1] < 1) break; if (open[k] >= 1) panelFace(c, k, x, y + k * ph, w, ph); else if (active(k)) flip(k, false); }
  pushpin(c, x + 30, y + 26); pushpin(c, x + w - 30, y + 26);
  const th = easeOutBack(seg(tt, at(15), at(15) + .35)), pop = easeOutBack(land(tt, at(14)));
  jeff(c, 180, lerp(2700, 1880, pop), .64, { armR: th > 0 ? lerp(-1.75, -2.5, th) : -1.75, prop: th > .6 ? 'thumb' : 'point', head: .04 * Math.sin(tt * 3), bob: Math.abs(Math.sin(tt * Math.PI / BEAT)) * 3 });
  const d = seg(t, at(15, 4), at(16)); if (d > 0) screenSpace(c, () => rubberStamp(c, easeIn(d)));
}
function sceneSignoff(c, t) {
  paperBg(c); liveEndCard(c);   // the closing card (vertkit.js): untouched logos, still
  const lift = seg(t, at(16), at(16) + .3);
  if (lift < 1) { c.save(); c.translate(0, -(H + 320) * easeIn(lift)); rubberStampFlat(c); c.restore(); }
}

// ================= assembly =================
function pushScenes(c, t, tb, A, B) {   // the plain transition: the camera drops from A to B on the downbeat
  const u = easeIO(seg(t, tb - PUSH / 2, tb + PUSH / 2)), g1 = L1.getContext('2d'), g2 = L2.getContext('2d');
  contentT(g1); g1.globalAlpha = 1; A(g1, t); contentT(g1); captions(g1, Math.min(t, tb - SLAM - 1e-3)); printFinish(g1);
  contentT(g2); g2.globalAlpha = 1; B(g2, t); contentT(g2); captions(g2, Math.max(t, tb - SLAM)); printFinish(g2);
  c.save(); resetT(c); c.drawImage(L1, 0, -u * H, W, H); c.drawImage(L2, 0, (1 - u) * H, W, H); c.restore();
}
function dive(c, t) {   // [1] at(6) - .3 .. at(6) + .15: the circle around the link opens into the fake page
  sceneEvidence(c, t); contentT(c); captions(c, Math.min(t, at(6) - SLAM - 1e-3)); printFinish(c);
  const u = easeIn(seg(t, at(6) - .3, at(6) + .15)), lb = linkBox(), cam = camEvidence(t), [px, py] = camPoint(cam, 1, lb.cx, lb.cy);
  const sx = CX + (px - SCX) * K, sy = SCY + (py - SCY) * K, r0 = lb.rx * cam.z * K, r = lerp(r0, Math.hypot(W, H), u), ry = r * lerp(lb.ry / lb.rx, 1, u);
  const g = L1.getContext('2d'); contentT(g); g.globalAlpha = 1; fakePage(g, t); contentT(g); printFinish(g);
  screenSpace(c, () => { c.save(); c.beginPath(); c.ellipse(sx, sy, r, ry, 0, 0, TAU); c.clip();
    const k = lerp(.45, 1, u); c.translate(sx, sy); c.scale(k, k); c.translate(-sx, -sy); c.drawImage(L1, 0, 0, W, H); c.restore();
    if (u < 1) { c.strokeStyle = BLUE; c.lineWidth = 10 * cam.z * K; c.beginPath(); c.ellipse(sx, sy, r, ry, 0, 0, TAU); c.stroke(); } });
}
function drawScene(c, t) {
  contentT(c);
  if (t >= at(16)) { resetT(c); sceneSignoff(c, t); return; }   // screen space; no print finish over the logos
  if (t < at(6) - .3) { sceneEvidence(c, t); contentT(c); captions(c, t); printFinish(c); }
  else if (t < at(6) + .15) { dive(c, t); if (t >= at(6) - SLAM) { contentT(c); captions(c, t); } }
  else if (t < at(7) - .2) { fakePage(c, t); contentT(c); captions(c, t); printFinish(c); }
  else if (t < at(7) + .15) pullBack(c, t);
  else if (t < at(10) - PUSH / 2) { sceneMap(c, t); contentT(c); captions(c, t); printFinish(c); }
  else if (t < at(10) + PUSH / 2) pushScenes(c, t, at(10), sceneMap, sceneFlow);
  else if (t < at(14)) { sceneFlow(c, t); contentT(c); captions(c, t); printFinish(c); }
  else { sceneFix(c, t); contentT(c); printFinish(c); }   // a clean cut after the silent beat
  if (SHOW_SAFE) safeOverlay(c);
}

// ================= runtime =================
const CV = document.getElementById('c'); CV.width = OUT_W; CV.height = OUT_H; const CTX = CV.getContext('2d');
function frame(i) { const t = Math.min(i / FPS, DUR - 1e-6); FILM_T = t; resetT(CTX); CTX.globalAlpha = 1; drawScene(CTX, t); resetT(CTX); }
window.__NFR = NFR; window.__FPS = FPS; window.__frame = i => { frame(i); return CV.toDataURL('image/png'); };
(async () => {
  await loadPrintKit(); await loadVertKit(); makeCream();
  US = (await (await fetch('assets/toll/us_outline.json')).json()).outline; makePins();
  LAYOUT = layoutMsg(CTX);
  frame(+(Q.get('frame') || 0));
  window.__ready = true;
})().catch(e => { console.error(e); window.__error = String(e); });
