'use strict';
/* Rossen Reports: LIVE TODAY promo for "The DEVASTATING New Zelle Scam". 15 s, 1080x1920 (9:16), 24 fps, one shot.
   Case-file screen-print look (printkit.js, the approved blue/black/cream/yellow inks) and the vertical kit
   (vertkit.js: safe-zone content transform, captions, stamps, scammer puppet). 96 BPM, one idea per bar:

   bar 0  0.0   the fake fraud-alert text is on screen from frame 0                  "GOT THIS TEXT?"
   bar 1  2.5   a thumb creeps to reply YES, a hook dangles over send; DON'T REPLY! on 3, zoom through the screen on 4
   bar 2  5.0   the account drains on eighths while the scammer fishes cash out of a wallet; $0.00 on 3
                                                                                          "THIS TEXT CAN EMPTY YOUR ACCOUNT"
   bar 3  7.5   the phone drops back; Jeff's magnifier over YES shows the hook on 3   "WHAT HAPPENS IF YOU REPLY?"
                zoom through the lens on 4
   bar 4  10.0  LIVE TODAY on 1, 5PM ET on 1.5, WEDNESDAY on 2, Jeff thumbs up
   bar 5  12.5  held; the rubber stamp lands on 2.5 and lifts off the official logo, still from 13.69
*/
const DUR = at(6), NFR = Math.round(FPS * DUR);
const SHOW = Object.assign({ time: '5PM ET', day: 'WEDNESDAY' }, window.SHOW || {});   // a wrapper page can set another airtime
const CAPS = [
  [at(0), 'GOT THIS TEXT?'], [at(1), null], [at(2), 'THIS TEXT CAN', 'EMPTY YOUR ACCOUNT'], [at(3), 'WHAT HAPPENS', 'IF YOU REPLY?'], [at(4), null],
];
const STAMP_T = at(5, 2.5);   // the rubber stamp presses down; the logo is under it

// ================= the phone and the fake text (no bank name anywhere) =================
const PH = { x: 180, y: 560, w: 600, h: 860 };
const MSG = ['FRAUD ALERT:', '$750 PAYMENT', 'ATTEMPT.', 'WAS THIS YOU?', 'REPLY YES OR NO.'];
const SEND = [PH.x + PH.w - 58, PH.y + 756], FIELD = { x: PH.x + 30, y: PH.y + 725, w: PH.w - 130, h: 62 };
function phone(c, t, o = {}) {
  const { x, y, w, h } = PH;
  shadowRect(c, x, y, w, h); block(c, rrPts(x, y, w, h, 60, 6), BLK, 5001, { kw: 6 });
  block(c, rrPts(x + 18, y + 56, w - 36, h - 112, 20, 4), CHIP, 5002, { kw: 3 });
  inkText(c, '9:41', x + 60, y + 32, 26, '"Liberation Sans"', CHIP, 80, 'left');
  // the sender: a generic alert, no bank
  block(c, ellPts(x + w / 2, y + 108, 30, 30, 0, 24), BLUE, 5003, { kw: 4 }); inkText(c, '!', x + w / 2, y + 111, 40, 'Stamp', CHIP, 30);
  inkText(c, 'Account Alert', x + w / 2, y + 166, 30, '"Liberation Sans"', BLK, w - 120);
  ink(c, rect(x + 18, y + 196, w - 36, 3), BLK, 5004, { reg: false });
  // the bubble
  const bp = o.pulse ?? 1;
  c.save(); c.translate(x + 40, y + 226); c.scale(bp, bp);
  block(c, rrPts(0, 0, 460, 360, 30, 5), '#ffffff', 5005, { kw: 4, reg: false });
  MSG.forEach((s, k) => inkText(c, s, 28, 46 + k * 62 + (k > 2 ? 14 : 0), 46, '"Liberation Sans"', BLK, 410, 'left'));
  c.restore();
  // the reply bar: typed text and the send button
  block(c, rrPts(FIELD.x, FIELD.y, FIELD.w, FIELD.h, 31, 4), '#ffffff', 5006, { kw: 3, reg: false });
  const typed = o.typed ?? '';
  inkText(c, typed || 'Text Message', FIELD.x + 28, FIELD.y + 33, 34, '"Liberation Sans"', typed ? BLK : '#9a9488', FIELD.w - 50, 'left');
  block(c, ellPts(SEND[0], SEND[1], 31, 31, 0, 24), BLUE, 5007, { kw: 4 });
  c.save(); c.strokeStyle = CHIP; c.lineWidth = 7; c.lineCap = 'round'; c.lineJoin = 'round'; c.beginPath(); c.moveTo(SEND[0], SEND[1] + 14); c.lineTo(SEND[0], SEND[1] - 13); c.moveTo(SEND[0] - 11, SEND[1] - 2); c.lineTo(SEND[0], SEND[1] - 13); c.lineTo(SEND[0] + 11, SEND[1] - 2); c.stroke(); c.restore();
}
const screenRect = () => [PH.x + 18, PH.y + 56, PH.w - 36, PH.h - 112];
function thumb(c, tip, dir = [-.42, -.91], r = 50) {   // a thumb printed like Jeff's hands
  const base = [tip[0] - dir[0] * 190, tip[1] - dir[1] * 190], fist = [tip[0] - dir[0] * 250 + 40, tip[1] - dir[1] * 250 + 30], ang = Math.atan2(dir[1], dir[0]);
  c.save(); c.translate(fist[0] - dir[0] * 120, fist[1] - dir[1] * 120); c.rotate(ang + Math.PI / 2); block(c, rect(-95, 0, 190, 400), BLK, 5102, { kw: 5 }); ink(c, rect(-95, 0, 190, 26), CHIP, 5103, { reg: false }); c.restore();
  skinCapsule(c, [fist[0] - 30, fist[1] + 10], [fist[0] + 40, fist[1] + 40], r * 1.55, 5104);   // the fist
  skinCapsule(c, base, tip, r, 5101);
  const n = [tip[0] - dir[0] * r * .7, tip[1] - dir[1] * r * .7];
  c.save(); c.globalAlpha = .9; c.fillStyle = '#fbd3b0'; c.beginPath(); c.ellipse(n[0], n[1], r * .5, r * .62, Math.atan2(dir[1], dir[0]) + Math.PI / 2, 0, TAU); c.fill(); c.restore();
}
function typedAt(t) { const s = 'YES'; return s.slice(0, [at(1, 1.5), at(1, 1.75), at(1, 2)].filter(x => t >= x).length); }
function sceneText(c, t) {   // bars 0-1
  bgDots(c, BLUE, .1, .5);
  const settle = 60 * Math.exp(-t * 5) * Math.cos(t * 13), push = 1 + .03 * seg(t, 0, at(1, 3));
  const pulse = 1 + .035 * Math.exp(-Math.max(0, t - at(0, 3)) * 5) * (t > at(0, 3) - SLAM ? 1 : 0);
  const [sx, sy] = shake(t, [[at(1, 3), 16]]);
  c.save(); c.translate(sx, sy + settle); c.translate(SCX, 940); c.scale(push, push); c.translate(-SCX, -940);
  phone(c, t, { pulse, typed: typedAt(t) });
  // the hook comes down over the send button, dangles, and is yanked away when the stamp lands
  const dn = easeOut(seg(t, at(1) - .1, at(1, 1.5))), yank = easeIn(seg(t, at(1, 3), at(1, 3) + .3));
  if (dn > 0 && yank < 1) { const hx = SEND[0] + 6 * Math.sin(t * 5), hy = lerp(-200, SEND[1] - 150, dn) - 900 * yank;
    fishLine(c, [hx, -300], [hx, hy], 0); hook(c, hx, hy, .8); }
  // the thumb creeps toward send, hesitates, then snaps back on the stamp
  const creep = easeIO(seg(t, at(1), at(1, 2.75))), back = easeOut(seg(t, at(1, 3), at(1, 3.5)));
  if (creep > 0 && back < 1) { const tip = [lerp(960, SEND[0] + 16, creep) + 4 * Math.sin(t * 17) * creep, lerp(1700, SEND[1] + 20, creep)];
    thumb(c, [lerp(tip[0], 1050, back), lerp(tip[1], 2000, back)]); }
  c.restore();
}

// ================= the account drains =================
const BAL = [[at(2), '$4,280.00'], [at(2, 1.5), '$3,530.00'], [at(2, 2), '$2,780.00'], [at(2, 2.5), '$2,030.00'], [at(2, 3), '$0.00']];
const ACC = { x: 110, y: 580, w: 740, h: 330 };
function account(c, t) {
  const { x, y, w, h } = ACC;
  shadowRect(c, x, y, w, h); block(c, rect(x, y, w, h), CHIP, 5201, { kw: 6 });
  ink(c, rect(x, y, w, 80), BLUE, 5202); key(c, rect(x, y, w, 80), 6, 5203); inkText(c, 'MY ACCOUNT', x + w / 2, y + 44, 46, 'Stamp', CHIP, w - 80);
  inkText(c, 'BALANCE', x + w / 2, y + 118, 32, '"Liberation Sans"', BLK, 300);
  let k = 0; BAL.forEach(([t0], i) => { if (t >= t0 - .02) k = i; });
  const zero = k === BAL.length - 1, hot = zero && Math.floor((t - at(2, 3)) / E8) % 2 === 0;
  const sc = pop(t, BAL[k][0]);
  c.save(); c.translate(x + w / 2, y + 205); c.scale(sc, sc);
  if (zero) block(c, rect(-250, -70, 500, 140), hot ? BLK : YEL, 5204, { kw: 5 });
  inkText(c, BAL[k][1], 0, 6, 120, 'Stamp', zero ? (hot ? YEL : BLK) : BLK, 640); c.restore();
  if (k > 0) inkText(c, `Zelle payment  -$750  x${Math.min(k, 3)}` + (zero ? '  ...' : ''), x + w / 2, y + 292, 40, '"Liberation Sans"', BLK, w - 80);   // plain system font
}
function wallet(c, x, y, open, t) {
  shadowRect(c, x - 150, y - 90, 300, 190, .25);
  block(c, rrPts(x - 150, y - 90, 300, 190, 22, 5), BLK, 5301, { kw: 5 });
  const left = Math.max(0, 5 - [at(2, 1.5), at(2, 2), at(2, 2.5), at(2, 3)].filter(v => t >= v).length * 1.25);
  for (let k = 0; k < Math.ceil(left); k++) { c.save(); c.translate(x - 90 + k * 40, y - 96 - k * 3); c.rotate(-.1 + k * .05); block(c, rect(-42, -26, 110, 52), YEL, 5310 + k, { kw: 3 }); inkText(c, '$', 12, 2, 34, 'Stamp', BLK, 40); c.restore(); }
  c.save(); c.translate(x, y - 90); c.rotate(-.5 * open); block(c, rrPts(-150, -14, 300, 60, 18, 4), BLUE, 5320, { kw: 5 }); c.restore();
  block(c, ellPts(x + 110, y + 10, 18, 18, 0, 16), YEL, 5321, { kw: 3 });
}
function bill(c, x, y, rot, s = 1) { c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s); block(c, rect(-55, -28, 110, 56), YEL, 5401, { kw: 3 }); inkText(c, '$', 0, 3, 36, 'Stamp', BLK, 40); c.restore(); }
function sceneDrain(c, t) {   // bar 2
  bgDots(c, BLK, .04, .22, 18);
  const [sx, sy] = shake(t, [[at(2, 3), 16]]);
  c.save(); c.translate(sx, sy);
  account(c, t);
  const W0 = [330, 1250];
  wallet(c, W0[0], W0[1], 1, t);
  // the scammer on the right fishes the cash out, one yank per eighth
  const yk = [at(2, 1.5), at(2, 2), at(2, 2.5), at(2, 3)];
  let rod = -.05;
  yk.forEach(v => { const u = seg(t, v - .1, v + .18); rod -= .22 * Math.sin(u * Math.PI); });
  const tip = scammer(c, 700, 1430, .72, { sx: -1, rod, head: .07 * Math.sin(t * 7), bob: Math.abs(Math.sin(t * Math.PI / BEAT)) * 5 });
  const dip = yk.reduce((m, v) => Math.max(m, t < v ? easeOut(seg(t, v - .3, v - .1)) : 1 - easeOut(seg(t, v, v + .2))), 0);   // down into the wallet, yanked out on the eighth
  const hp = [lerp(tip[0], W0[0] + 20, .85), lerp(tip[1] + 60, W0[1] - 150, dip)];
  fishLine(c, tip, hp, 10); hook(c, hp[0], hp[1], .7);
  // the bills fly off: out of the wallet, over the hook, off the left edge (always below the account card)
  yk.forEach((v, i) => { for (let j = 0; j < 3; j++) { const u = seg(t, v + j * .05, v + .9 + j * .05); if (u <= 0 || u >= 1) continue;
    const bx = lerp(W0[0], -200, easeIn(u)), by = W0[1] - 120 - 190 * Math.sin(u * Math.PI) - j * 30; bill(c, bx, Math.max(by, 960), (u * 7 + j) * (j % 2 ? 1 : -1), .9); } });
  c.restore();
}

// ================= the tease: Jeff and the magnifier =================
const TS = .85, tp = ([x, y]) => [SCX + (x - SCX) * TS, 560 + (y - 560) * TS];   // bar 3 phone scale about its top
const phoneT = c => { c.translate(SCX, 560); c.scale(TS, TS); c.translate(-SCX, -560); };
const LENS0 = [FIELD.x + 75, FIELD.y + 31], LENS = tp(LENS0);
function lensInner(c, cx, cy, t) {   // YES, magnified, with the hook through it on beat 3
  c.translate(cx, cy); c.scale(1.8, 1.8); c.translate(-cx, -cy); c.translate(cx - LENS0[0], cy - LENS0[1]); phoneT(c); c.translate(LENS0[0] - cx, LENS0[1] - cy);
  block(c, rect(PH.x, PH.y + 640, PH.w, 170), CHIP, 5501, { kw: 0, key: false });
  block(c, rrPts(FIELD.x, FIELD.y, FIELD.w, FIELD.h, 31, 4), '#ffffff', 5006, { kw: 3, reg: false });
  inkText(c, 'YES', FIELD.x + 28, FIELD.y + 33, 34, '"Liberation Sans"', BLK, 200, 'left');
  if (t >= at(3, 3) - SLAM) { const k = pop(t, at(3, 3)); c.save(); c.translate(LENS0[0] + 38, LENS0[1] - 58); c.scale(k * .55, k * .55); hook(c, 0, 0, 1); c.restore(); }
}
function sceneTease(c, t, flat = false) {   // bar 3
  bgDots(c, BLUE, .1, .5);
  const drop = easeIn(land(t, at(3)));
  c.save(); c.translate(0, lerp(-1500, 0, drop)); phoneT(c);
  phone(c, t, { typed: 'YES' });
  c.restore();
  const J = jeffUp(c, t, at(3, 1.5), 150, { armR: lerp(0, -1.2, easeOut(seg(t, at(3, 2) - SLAM, at(3, 2)))), head: .05 }, .66);
  const raise = easeOut(seg(t, at(3, 2) - SLAM, at(3, 2)));
  if (!J || raise <= 0 || flat) return J;
  const cx = lerp(J.hand[0] + 80, LENS[0], raise), cy = lerp(J.hand[1] - 120, LENS[1], raise);
  magnifier(c, cx, cy, lerp(40, 118, raise), J.hand, raise > .6 ? () => lensInner(c, cx, cy, t) : null);
  return J;
}
function lensZoom(c, t) {   // bar 3 beat 4: through the lens into the LIVE TODAY card
  const u = easeIn(seg(t, at(3, 4), at(4)));
  const J = sceneTease(c, t, true), R = lerp(118, 1700, u * u), cx = lerp(LENS[0], SCX, u), cy = lerp(LENS[1], SCY, u);
  const g = L1.getContext('2d'); contentT(g); g.globalAlpha = 1; sceneLive(g, at(4));
  magnifier(c, cx, cy, R, u < .5 ? J.hand : null, () => { const p = c.getTransform().transformPoint(new DOMPoint(cx, cy)); resetT(c); const k = lerp(.35, 1, u);
    c.translate(p.x, p.y); c.scale(k, k); c.drawImage(L1, -CX, -SCY, W, H); });
}

// ================= LIVE TODAY 5PM ET =================
function sceneLive(c, t) {   // bars 4-5
  bgDots(c, BLUE, .12, .55);
  const [sx, sy] = shake(t, [[at(4), 16], [at(4, 1.5), 10]]);
  const beatPulse = t > at(5) ? 1 + .025 * Math.max(0, Math.cos((t - at(5)) * TAU / BEAT)) : 1;
  stickerLogo(c, SCX, 500, 560, -.03, lerp(1.6, 1, easeIn(land(t, at(4)))));
  const th = easeOutBack(seg(t, at(4, 2.5), at(4, 3)));
  jeffUp(c, t, at(4, 2), SCX, { armR: lerp(0, -2.5, th), prop: th > .6 ? 'thumb' : null, head: t > at(5) ? .05 * Math.sin((t - at(5)) * TAU / (2 * BEAT)) : 0 }, .72);
  c.save(); c.translate(sx, sy);
  stampFit(c, 'LIVE TODAY', BLK, 150, SCX, 790, -.04, .9 * beatPulse, t, at(4), 800, 1.25);
  stampFit(c, SHOW.time, BLUE, 170, SCX, 1012, .03, .95 * beatPulse, t, at(4, 1.5), 800, 1.18);
  if (t >= at(4, 2) - SLAM) { const k = pop(t, at(4, 2)); c.save(); c.translate(SCX, 1172); c.scale(k, k); c.rotate(-.015);
    c.font = '58px Stamp'; const w = c.measureText(SHOW.day).width + 60;
    c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fillRect(-w / 2 + 8, -44, w, 92); c.restore(); ink(c, rect(-w / 2, -48, w, 92), BLK, 5601, { amp: 3 }); inkText(c, SHOW.day, 0, 4, 58, 'Stamp', CHIP, 600); c.restore(); }
  c.restore();
  const d = seg(t, at(5, 1.5), STAMP_T); if (d > 0) screenSpace(c, () => rubberStamp(c, easeIn(d)));
}
function sceneSignoff(c, t) {
  paperBg(c);
  // the official logo: exact file, uniformly scaled, no texture or recolour, centred on the frame; held still
  const im = IMG.logo, [bx, by, bw, bh] = IMG.logoBox, lw = 720, lh = bh * lw / bw;
  c.drawImage(im, bx, by, bw, bh, CX - lw / 2, SCY - lh / 2, lw, lh);
  const lift = seg(t, STAMP_T, STAMP_T + .25);
  if (lift < 1) { c.save(); c.translate(0, -(H + 320) * easeIn(lift)); rubberStampFlat(c); c.restore(); }
}

// ================= assembly =================
function drawScene(c, t) {
  contentT(c);
  if (t < at(1, 4)) sceneText(c, t);
  else if (t < at(2)) zoomThrough(c, t, at(1, 4), at(2), screenRect(), g => sceneText(g, t), g => sceneDrain(g, t));
  else if (t < at(3) - SLAM) sceneDrain(c, t);
  else if (t < at(3, 4)) sceneTease(c, t);
  else if (t < at(4)) lensZoom(c, t);
  else if (t < STAMP_T) sceneLive(c, t);
  else { resetT(c); sceneSignoff(c, t); return; }   // screen space; no print finish over the official logo
  captions(c, t);
  // DON'T REPLY! rides on top through the zoom into the account
  if (t >= at(1, 3) - SLAM && t < at(2)) stampFit(c, "DON'T REPLY!", BLK, 160, SCX, 440, -.06, 1, t, at(1, 3));
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
