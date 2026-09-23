'use strict';
/* Rossen Reports: "case file" title sequence. 19.5 s, 1920x1080, 24 fps, one continuous piece.
   Screen-print look: flat bold inks (logo blue, black, one yellow accent) on warm cream stock, halftone dot tints,
   misregistered colour layers, paper grain. 96 BPM: one beat = 0.625 s = 15 frames, one bar = 2.5 s, one scene per bar,
   a stamp on beat 3 of every scene. Every landing finishes ON its beat (things start falling SLAM seconds early).

   bar 1  0.0-2.5    CASE FILE   folder thwacks down on beat 2, ransom letters L-I-V-E on 2.5/3/3.5/4, cover flips open on 4.5
   bar 2  2.5-5.0    BOARD       camera pans the evidence board, Jeff pops up on 2, raises the magnifier on 3, lens on 4
   bar 3  5.0-7.5    PHISHING    "account locked" phone, con man dangles a hook on 2, SCAM! on 3, redaction marker on 4
   bar 4  7.5-10.0   HIDDEN CAM  lens iris opens on 1, Jeff barges in on 2, flash + CAUGHT! on 3, frame becomes a Polaroid on 4
   bar 5  10.0-12.5  WARNING     fine print; redaction bars peel back on 2, WARNING! on 3, page turn on 4.5
   bar 6  12.5-15.0  DEALS       tags land on eighths, Jeff thumbs up, DEAL! on 3, folder swings shut on 4
   bar 7  15.0-17.5  CASE CLOSED folder cover, screen-print logo slaps on 1, Jeff on 2, LIVE NOW on 3, rubber stamp on 4
   bar 8  17.5-19.5  SIGN-OFF    the official logo, untouched, revealed as the stamp lifts; still from 17.8
*/
const VERT = !!window.CASEFILE_VERTICAL;   // 9:16 build (rossen-casefile-vertical.html): same film, portrait layouts
setFormat(VERT ? { ar: '9:16', width: 1080 } : { ar: '16:9', width: 1920 });
const FPS = 24, DUR = 19.5, NFR = Math.round(FPS * DUR);
const BEAT = .625, BAR = 2.5;   // SLAM comes from printkit.js
const at = (bar, beat = 1) => bar * BAR + (beat - 1) * BEAT;   // bar 0-based, beat 1-based
const L1 = layer(), L2 = layer();
let FILM_T = 0;

// ================= bar 1: the case file =================
const FOLDER = VERT ? { x: 100, y: 173, w: 880, h: 1573 } : { x: 320, y: 180, w: 1280, h: 720 };   // inner page keeps the frame's aspect for the dive
const LET = VERT ? { size: 330 } : { x0: 300, sp: 230, y: 380, size: 250 };
const letPos = k => VERT ? [FOLDER.x + FOLDER.w / 2 + (k % 2 ? 175 : -175), FOLDER.y + (k < 2 ? 640 : 1050)] : [FOLDER.x + LET.x0 + k * LET.sp, FOLDER.y + LET.y];   // 9:16: LI / VE
function folderShape(x, y, w, h) { return [[x, y + 40], [x + 40, y], [x + 320, y], [x + 350, y + 40], [x + w, y + 40], [x + w, y + h], [x, y + h]]; }
function deskBg(c, t) { paperBg(c); dotsIn(c, rect(-50, -50, W + 100, H + 100), BLUE, .22, 1001, 14);
  for (let k = 0; k < 7; k++) { const r = rng(1010 + k); ink(c, rect(r() * W, r() * H, 180 + r() * 200, 8), BLK, 1011 + k, { reg: false }); } }
function sceneFile(c, t, coverFlip = 0) {
  deskBg(c, t);
  const [sx, sy] = shake(t, [[at(0, 2), 12], [at(0, 2.5), 5], [at(0, 3), 5], [at(0, 3.5), 5], [at(0, 4), 7]]);
  const drift = 1 + .03 * seg(t, 0, 2.2);
  c.save(); c.translate(sx, sy); c.translate(CX, CY); c.scale(drift, drift); c.rotate(-.015 * seg(t, 0, 2.2)); c.translate(-CX, -CY);
  // the folder slides in and thwacks down on beat 2
  const u = easeOut(land(t, at(0, 2)) ** .8), fx = lerp(1500, 0, u), fr = lerp(.35, 0, u);
  c.save(); c.translate(CX + fx, CY); c.rotate(fr); c.translate(-CX, -CY);
  const F = FOLDER;
  c.save(); c.globalAlpha = .3; c.translate(14, 18); c.fillStyle = BLK; c.fill(polyPath(folderShape(F.x, F.y, F.w, F.h))); c.restore();
  // inside pages (under the cover)
  block(c, folderShape(F.x, F.y, F.w, F.h), CHIP, 1020, { kw: 7 }); dotsIn(c, folderShape(F.x, F.y, F.w, F.h), YEL, .22, 1021, 11);
  if (coverFlip > 0) { const g = L2.getContext('2d'); resetT(g); sceneBoard(g, at(1)); c.save(); c.beginPath(); c.rect(F.x + 20, F.y + 60, F.w - 40, F.h - 80); c.clip(); c.drawImage(L2, F.x + 20, F.y + 60, F.w - 40, F.h - 80); c.restore(); }
  // the cover, flipping on its left spine
  const cos = Math.cos(coverFlip * Math.PI);
  c.save(); c.translate(F.x, 0); c.scale(cos, 1); c.translate(-F.x, 0);
  if (cos > 0 || coverFlip === 0) {
    block(c, folderShape(F.x, F.y + 6, F.w, F.h - 6), CHIP, 1022, { kw: 7 }); dotsIn(c, folderShape(F.x, F.y + 6, F.w, F.h - 6), YEL, .3, 1023, 11);
    block(c, rect(F.x + 60, F.y + 8, 250, 28), CHIP, 1024, { kw: 3 }); inkText(c, 'CASE FILE', F.x + 185, F.y + 23, 26, '"Liberation Mono"', BLK, 230);
    inkText(c, 'EVIDENCE  ·  DO NOT BEND', F.x + F.w - 60, F.y + F.h - 50, 30, '"Liberation Mono"', BLK, 600, 'right');
    // L-I-V-E in ransom letters, one per eighth from beat 2.5
    'LIVE'.split('').forEach((ch, k) => { const t0 = at(0, 2.5 + k * .5); if (t < t0 - SLAM) return; const q = land(t, t0), s = lerp(2.2, 1, easeIn(q));
      c.save(); c.translate(...letPos(k)); c.scale(s, s); ransomLetter(c, ch, 0, 0, LET.size, k * 2 + 1, [-.12, .08, -.05, .1][k]); c.restore(); });
  } else { block(c, folderShape(F.x, F.y + 6, F.w, F.h - 6), CHIP, 1025, { kw: 7 }); dotsIn(c, folderShape(F.x, F.y + 6, F.w, F.h - 6), YEL, .2, 1026, 11); }
  c.restore();
  c.restore(); c.restore();
}
// ================= bar 2: the evidence board =================
const BOARD_W = VERT ? W : 2700, BOARD_H = VERT ? 2700 : H;
const PINS = VERT ? [
  { x: 290, y: 560, rot: -.07, icon: phoneIcon, cap: 'THE TEXT' }, { x: 560, y: 1340, rot: .05, icon: phoneIcon, cap: 'THE SCAM' },
  { x: 800, y: 620, rot: -.04, icon: lensIcon, cap: 'HIDDEN CAM' }, { x: 820, y: 1960, rot: .06, icon: tagIcon, cap: 'THE DEAL' }, { x: 300, y: 2020, rot: .04, icon: docIcon, cap: 'FINE PRINT' },
] : [
  { x: 420, y: 330, rot: -.07, icon: phoneIcon, cap: 'THE TEXT' }, { x: 1180, y: 380, rot: .05, icon: phoneIcon, cap: 'THE SCAM' },
  { x: 1860, y: 300, rot: -.04, icon: lensIcon, cap: 'HIDDEN CAM' }, { x: 2380, y: 420, rot: .06, icon: tagIcon, cap: 'THE DEAL' }, { x: 820, y: 760, rot: .04, icon: docIcon, cap: 'FINE PRINT' },
];
function boardPan(t) { const u = lerp(0, VERT ? 720 : 760, easeIO(seg(t, at(1), at(1, 3)))); return VERT ? [0, u] : [u, 0]; }   // pan lands on the SCAM photo on beat 3 (down the board in 9:16)
function sceneBoard(c, t) {
  paperBg(c);
  const pan = boardPan(t);
  c.save(); c.translate(-pan[0], -pan[1]);
  // the board: blue tone, ledger lines, a headline strip
  dotsIn(c, rect(-60, -60, BOARD_W + 200, BOARD_H + 120), BLUE, .34, 1101, 12);
  if (VERT) { inkText(c, 'WHO IS RIPPING', CX, 160, 104, 'Stamp', BLK, 960); inkText(c, 'YOU OFF?', CX, 280, 104, 'Stamp', BLK, 960); }
  else inkText(c, 'WHO IS RIPPING YOU OFF?', 1180, 110, 88, 'Stamp', BLK, 1400);
  PINS.forEach((P, k) => polaroid(c, P.x, P.y, 330, 380, P.rot, 1110 + k, (pw, ph) => { ink(c, rect(-pw / 2, -ph / 2, pw, ph), CHIP, 1120 + k, { reg: false }); P.icon(c, 1.3); }));
  PINS.forEach((P, k) => inkText(c, P.cap, P.x, P.y + 150, 40, 'Marker', BLK, 280, 'center', P.rot));
  for (const [a, b] of [[0, 1], [1, 2], [2, 3], [1, 4]]) string(c, [PINS[a].x, PINS[a].y - 175], [PINS[b].x, PINS[b].y - 175], 60);
  PINS.forEach(P => pushpin(c, P.x, P.y - 175));
  c.restore();
  // Jeff pops up from the bottom on beat 2, raises the magnifier on beat 3
  const pu = easeOutBack(land(t, at(1, 2)) ** .9), jy = lerp(H + 1220, H + 5, pu);
  const raise = easeOut(seg(t, at(1, 3) - SLAM, at(1, 3)));
  const J = jeff(c, VERT ? 250 : 420, jy, VERT ? .8 : .72, { armR: lerp(0, -2.15, raise), head: .06 * raise, bob: Math.sin(t * 9) * 4 * (1 - raise) });
  return { J, raise };
}
function boardWithLens(c, t) {
  const { J, raise } = sceneBoard(c, t);
  if (raise <= 0) return;
  const pan = boardPan(t), target = [PINS[1].x - pan[0], PINS[1].y - 20 - pan[1]];
  const zoom = easeIn(seg(t, at(1, 4), at(2)));   // beat 4: through the lens
  const R = lerp(lerp(60, 170, raise), 1300, zoom * zoom), cx = lerp(J.hand[0] + 200, target[0], raise), cy = lerp(J.hand[1] - 200, target[1], raise);
  magnifier(c, lerp(cx, CX, zoom), lerp(cy, CY, zoom), R, zoom < .5 ? J.hand : null, raise > .6 ? () => {
    const g = L1.getContext('2d'); resetT(g); scenePhone(g, at(2)); const k = lerp(.35, 1, zoom); c.translate(lerp(cx, CX, zoom), lerp(cy, CY, zoom)); c.scale(k, k); c.drawImage(L1, -W / 2, -H / 2, W, H); } : null);
}
// ================= bar 3: phishing =================
const PHN = VERT ? { x: 540, y: 900, w: 620, h: 1040 } : { x: 960, y: 560, w: 560, h: 940 };
function scenePhone(c, t) {
  paperBg(c);
  // a halftone ramp of blue dots, bigger toward the edges
  dotScreen(c, polyPath(rect(0, 0, W, H)), [0, 0, W, H], { cell: 22, color: BLUE, density: (x, y) => .12 + .55 * Math.min(1, Math.hypot(x - CX, y - CY) / 1000), angle: .26, seed: 1201 });
  const [sx, sy] = shake(t, [[at(2, 3), 16]]);
  const breathe = 1 + .02 * Math.sin((t - at(2)) * Math.PI / BEAT);
  c.save(); c.translate(sx, sy); c.translate(PHN.x, PHN.y); c.scale(breathe, breathe); c.rotate(-.04);
  // con man sneaks up behind, dangles a hook on beat 2
  const up = easeOutBack(land(t, at(2, 2))) * (1 - easeIn(seg(t, at(2, 3.5) - .1, at(2, 3.5) + .1)));
  const panic = t >= at(2, 3);
  if (up > 0) conman(c, PHN.w / 2 + 20 - (1 - up) * 160, 40, 2.3, { mood: panic ? 1 : 0, look: Math.sin(t * 7) > 0 ? -1 : 1, t });
  const { w, h } = PHN;
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fill(polyPath(rrPts(-w / 2 + 16, -h / 2 + 22, w, h, 60, 6))); c.restore();
  block(c, rrPts(-w / 2, -h / 2, w, h, 60, 6), BLK, 1210, { kw: 6 });
  const sw = w - 52, sh = h - 150; block(c, rrPts(-sw / 2, -sh / 2, sw, sh, 20, 4), CHIP, 1211, { kw: 4 });
  ink(c, rect(-sw / 2, -sh / 2, sw, 90), BLUE, 1212); inkText(c, 'URGENT', 0, -sh / 2 + 47, 50, 'Stamp', CHIP, sw - 60);
  inkText(c, 'YOUR ACCOUNT', 0, -150, 58, 'Stamp', BLK, sw - 60); inkText(c, 'IS LOCKED', 0, -85, 58, 'Stamp', BLK, sw - 60);
  const pulse = 1 + .05 * Math.max(0, Math.sin((t - at(2)) * Math.PI * 2 / BEAT));
  c.save(); c.translate(0, 120); c.scale(pulse, pulse); block(c, rrPts(-190, -58, 380, 116, 40, 5), YEL, 1213, { kw: 5 }); inkText(c, 'VERIFY NOW', 0, 4, 54, 'Stamp', BLK, 330); c.restore();
  if (up > .3 && !panic) {   // the hook
    const hk = [-20, 60 + Math.sin(t * 9) * 12]; c.save(); c.strokeStyle = BLK; c.lineWidth = 3.5; c.beginPath(); c.moveTo(60, -320); c.lineTo(hk[0], hk[1] - 34); c.stroke();
    c.lineWidth = 8; c.lineCap = 'round'; c.beginPath(); c.moveTo(hk[0], hk[1] - 34); c.lineTo(hk[0], hk[1]); c.quadraticCurveTo(hk[0], hk[1] + 26, hk[0] - 22, hk[1] + 18); c.stroke(); c.restore();
    key(c, [[PHN.w / 2 + 50, -170], [60, -320]], 12, 1214, false);
  }
  c.restore();
  if (t >= at(2, 3) - SLAM) stampLand(c, stampImg('SCAM!', BLUE, 200), PHN.x + sx, PHN.y + 130 + sy, -.12, VERT ? .95 : 1, t, at(2, 3));
  // beat 4: a redaction marker blacks the frame out, three strokes
  for (let k = 0; k < 3; k++) { const a = seg(t, at(2, 4) + k * .2, at(2, 4) + k * .2 + .2); if (a <= 0) continue;
    const y0 = k * H / 3 - 20, sh = H / 3 + 40, pts = [[-40, y0], [-40 + (W + 80) * a, y0 + 10], [-40 + (W + 80) * a, y0 + sh], [-40, y0 + sh - 10]]; ink(c, pts, BLK, 1220 + k, { amp: 8 }); }
}
// ================= bar 4: hidden camera =================
function iris(c, open) {   // camera-lens aperture blades opening from the centre
  if (open >= 1) return; const n = 7, R = VERT ? 1700 : 1300, r = lerp(0, VERT ? 1300 : 1150, easeOut(open));
  c.save(); c.fillStyle = BLK;
  for (let k = 0; k < n; k++) { const a = k / n * TAU + open * .9; c.beginPath(); c.moveTo(CX + Math.cos(a) * r, CY + Math.sin(a) * r); c.lineTo(CX + Math.cos(a + 1.3) * R, CY + Math.sin(a + 1.3) * R); c.lineTo(CX + Math.cos(a + 2.4) * R, CY + Math.sin(a + 2.4) * R); c.lineTo(CX + Math.cos(a + TAU / n) * r, CY + Math.sin(a + TAU / n) * r); c.closePath(); c.fill();
    c.strokeStyle = alpha(CHIP, .35); c.lineWidth = 3; c.stroke(); }
  c.restore();
}
const CAUGHT_T = 7.5 + 1.25;   // bar 4 beat 3
const HL = VERT ? { wall: 1120, gx: -520, gy: 170, jx: 280, js: .9, cam: [540, 470, .85], snapY: 330 } : { wall: 800, gx: 0, gy: 0, jx: 470, js: .78, cam: [1100, 330, 1] };
function sceneHidden(c, t) {
  const tf = Math.min(t, CAUGHT_T);   // the flash freezes the action
  paperBg(c);
  dotsIn(c, rect(-40, -40, W + 80, HL.wall), BLUE, .42, 1301, 12);
  for (let x = 60; x < W; x += 120) ink(c, rect(x, -40, 26, HL.wall + 40), BLUE, 1302 + x, { tint: .75, cell: 8 });
  block(c, rect(-40, HL.wall - 20, W + 80, H - HL.wall + 60), CHIP, 1303, { kw: 6 }); dotsIn(c, rect(-40, HL.wall - 20, W + 80, H - HL.wall + 60), BLK, .12, 1304, 12);
  c.save(); c.translate(HL.gx, HL.gy);
  // the con man at his desk, counting cash
  const mood = tf >= at(3, 2) ? 1 : 0;
  conman(c, 1260, 700, 2.4, { mood, look: mood ? -1 : Math.sin(tf * 4), t: tf });
  for (let k = 0; k < 4; k++) { const ph = (tf * 1.6 + k * .25) % 1; c.save(); c.translate(1150 + k * 40, 600 - ph * 90); c.rotate(-.5 + ph); c.globalAlpha = 1 - ph; block(c, rect(-50, -24, 100, 48), YEL, 1310 + k, { kw: 3 }); inkText(c, '$', 0, 2, 34, 'Stamp', BLK, 60); c.restore(); }
  block(c, rect(880, 650, 700, 60), BLK, 1320, { kw: 4 }); block(c, rect(910, 710, 640, 250), BLK, 1321, { kw: 4 }); dotsIn(c, rect(930, 730, 600, 210), BLUE, .3, 1322, 10);
  for (let k = 0; k < 6; k++) block(c, rect(1400 + (k % 2) * 8, 630 - k * 12, 130, 22), YEL, 1330 + k, { kw: 3 });
  c.restore();
  // Jeff barges in on beat 2 and points
  const a = easeOutBack(land(tf, at(3, 2))), jx = lerp(-400, HL.jx, a), pointA = easeOut(seg(tf, at(3, 2), at(3, 2.5)));
  if (tf > at(3, 2) - SLAM) jeff(c, jx, H, HL.js, { armR: lerp(0, VERT ? -2.25 : -1.75, pointA), prop: pointA > .5 ? 'point' : null, tilt: .04 * (1 - a) });
  // viewfinder
  for (const [x, y, sx2, sy2] of [[70, 70, 1, 1], [W - 70, 70, -1, 1], [70, H - 70, 1, -1], [W - 70, H - 70, -1, -1]]) key(c, [[x, y + sy2 * 110], [x, y], [x + sx2 * 110, y]], 12, 1340 + x + y, false);
  const recY = VERT ? 232 : 132; if (Math.floor(tf * 3.2) % 2 === 0) { c.fillStyle = BLUE; c.beginPath(); c.arc(140, recY, 18, 0, TAU); c.fill(); }
  inkText(c, 'REC', 175, recY + 2, 52, 'Stamp', BLK, 200, 'left');
  block(c, rect(CX - 270, 70, 540, 90), BLK, 1350, { kw: 2 }); inkText(c, 'HIDDEN CAMERA', CX, 116, 50, 'Stamp', CHIP, 500);
  iris(c, seg(t, at(3), at(3, 1.5)));
  // beat 3: flash + CAUGHT!
  if (t >= CAUGHT_T - SLAM) stampLand(c, stampImg('CAUGHT!', BLUE, 170), HL.cam[0], HL.cam[1], -.08, HL.cam[2], t, CAUGHT_T);
  if (t >= CAUGHT_T && t < CAUGHT_T + .3) { c.save(); c.globalAlpha = 1 - seg(t, CAUGHT_T, CAUGHT_T + .3); c.fillStyle = CHIP; c.fillRect(0, 0, W, H); c.restore(); }
}
// ================= bar 5: the warning (fine print) =================
function sceneWarning(c, t) {
  paperBg(c); dotsIn(c, rect(-40, -40, W + 80, H + 80), BLUE, .2, 1401, 14);
  const [sx, sy] = shake(t, [[at(4, 3), 12]]);
  const push = 1 + .04 * seg(t, at(4), at(5));
  c.save(); c.translate(sx, sy); c.translate(...WS.push); c.scale(push, push); c.rotate(WS.rot); c.translate(-WS.push[0], -WS.push[1]);
  const D = WS.D;
  c.save(); c.globalAlpha = .28; c.fillStyle = BLK; c.fillRect(D.x + 14, D.y + 18, D.w, D.h); c.restore();
  block(c, rect(D.x, D.y, D.w, D.h), CHIP, 1402, { kw: 6 });
  inkText(c, 'TERMS OF SERVICE', D.x + D.w / 2, D.y + 70, 56, 'Stamp', BLK, D.w - 80);
  squiggleText(c, D.x + 60, D.y + 150, D.w - 120, 5, { seed: 1410, lineH: 30, color: BLK, width: 2.2 });
  // the hidden lines: redaction bars that peel back on beat 2
  const peel = easeOut(seg(t, at(4, 2) - SLAM, at(4, 2) + .1));
  [['WE SELL YOUR DATA', 360], ['HIDDEN FEE $19.99/MO', 520]].forEach(([s, y], k) => {
    block(c, rect(D.x + 50, D.y + y - 42, D.w - 100, 84), YEL, 1420 + k, { kw: 0, key: false });
    inkText(c, s, D.x + D.w / 2, D.y + y + 3, 60, 'Stamp', BLK, D.w - 140);
    const bw = (D.w - 90) * (1 - peel); if (bw > 2) ink(c, rect(D.x + 45 + (D.w - 90) - bw, D.y + y - 48, bw, 96), BLK, 1430 + k, { amp: 5 }); });
  squiggleText(c, D.x + 60, D.y + 640, D.w - 120, 7, { seed: 1411, lineH: 30, color: BLK, width: 2.2 });
  c.restore();
  // the caught Polaroid, pinned at top-left (it arrived from the hidden camera)
  pinnedEvidence(c, t, 1);
  // Jeff points at the fine print from the bottom right
  const a = easeOutBack(land(t, at(4, 1.5))), jy = lerp(H + 420, H + 5, a), pt = easeOut(seg(t, at(4, 1.5), at(4, 2)));
  jeff(c, WS.jeff[0], jy, WS.jeff[1], { armR: lerp(0, -2.6, pt), head: -.08, prop: pt > .5 ? 'point' : null });
  if (t >= at(4, 3) - SLAM) stampLand(c, stampImg('WARNING!', BLUE, 150), WS.stamp[0] + sx, WS.stamp[1] + sy, .07, WS.stamp[2], t, at(4, 3));
}
const SCAM_P = VERT ? [290, 330, .06] : [330, 290, .06], CAUGHT_P = VERT ? [790, 350, -.08] : [350, 770, -.08];   // the evidence wall beside (9:16: above) the fine print
const YARN = VERT ? [[SCAM_P[0], SCAM_P[1] - 190], [CAUGHT_P[0], CAUGHT_P[1] - 190], 70] : [[SCAM_P[0] + 60, SCAM_P[1] + 120], [CAUGHT_P[0], CAUGHT_P[1] - 190], 30];
const WS = VERT ? { D: { x: 110, y: 640, w: 860, h: 960 }, push: [540, 1120], rot: .02, jeff: [900, .64], stamp: [420, 1470, .72] }
                : { D: { x: 700, y: 110, w: 760, h: 900 }, push: [1050, 560], rot: .03, jeff: [1640, .7], stamp: [1120, 880, 1] };
function pinnedEvidence(c, t, caught) {
  if (caught) string(c, ...YARN);   // yarn runs behind the photos
  scamPolaroid(c, ...SCAM_P);
  if (caught) caughtPolaroid(c, CAUGHT_P[0], CAUGHT_P[1], 1, CAUGHT_P[2]);
  pushpin(c, SCAM_P[0], SCAM_P[1] - 190); if (caught) pushpin(c, CAUGHT_P[0], CAUGHT_P[1] - 190);
}
function scamPolaroid(c, x, y, rot) {   // the phone frame, SCAM! stamped, before the redaction marker
  if (!IMG.scamSnap) { const o = document.createElement('canvas'); o.width = W; o.height = H; const g = o.getContext('2d'); scenePhone(g, at(2, 3) + .35); drawPrint(g); IMG.scamSnap = o; }
  polaroid(c, x, y, 380, 380, rot, 1490, (pw, ph) => { const [sx0, sy0, cw] = VERT ? [0, 430, W] : [480, 150, 960]; c.drawImage(IMG.scamSnap, sx0, sy0, cw, cw * ph / pw, -pw / 2, -ph / 2, pw, ph); });
  inkText(c, 'SCAM', x, y + 150, 44, 'Marker', BLK, 300, 'center', rot);
}
function caughtPolaroid(c, x, y, s, rot) {
  const g = L2.getContext('2d'); resetT(g); sceneHidden(g, CAUGHT_T + .31); drawPrint(g);
  polaroid(c, x, y, 380 * s, 380 * s, rot, 1500, (pw, ph) => { if (VERT) c.drawImage(L2, 0, HL.snapY, W, W * ph / pw, -pw / 2, -ph / 2, pw, ph); else c.drawImage(L2, -pw / 2, -ph / 2, pw, ph); });
  inkText(c, 'CAUGHT', x - Math.sin(rot) * 0, y + 150 * s, 44 * s, 'Marker', BLK, 300 * s, 'center', rot);
}
// ================= bar 6: deals =================
const TAGS = VERT ? [
  { x: 300, y: 520, old: '$129', neu: '$59', t0: at(5, 1), rot: -.1 }, { x: 790, y: 510, old: '$80', neu: '$29', t0: at(5, 1.5), rot: .07 },
  { x: 290, y: 1010, old: '$250', neu: '$99', t0: at(5, 2), rot: -.06 }, { x: 800, y: 990, old: '$45', neu: '$15', t0: at(5, 2.5), rot: .09 },
] : [
  { x: 280, y: 560, old: '$129', neu: '$59', t0: at(5, 1), rot: -.1 }, { x: 600, y: 330, old: '$80', neu: '$29', t0: at(5, 1.5), rot: .07 },
  { x: 1360, y: 340, old: '$250', neu: '$99', t0: at(5, 2), rot: -.06 }, { x: 1680, y: 590, old: '$45', neu: '$15', t0: at(5, 2.5), rot: .09 },
];
function sceneDeals(c, t) {
  paperBg(c); dotsIn(c, rect(-40, H - 520, W + 80, 600), BLUE, .3, 1601, 13);
  const [sx, sy] = shake(t, [[at(5, 3), 12]]);
  c.save(); c.translate(sx, sy);
  const tagY = g => { const q = land(t, g.t0), sp = t > g.t0 ? Math.exp(-(t - g.t0) * 6) * Math.sin((t - g.t0) * 20) : 0; return [lerp(-300, g.y, easeIn(q)) + sp * 24, sp]; };
  TAGS.forEach(g => { if (t < g.t0 - SLAM) return; const [y] = tagY(g);   // hanging strings first, behind every tag
    c.save(); c.strokeStyle = BLK; c.lineWidth = 4; c.beginPath(); c.moveTo(g.x - 80, -20); c.lineTo(g.x - 150, y - 10); c.stroke(); c.restore(); });
  TAGS.forEach((g, k) => { if (t < g.t0 - SLAM) return; const [y, sp] = tagY(g), rot = g.rot + sp * .12;
    c.save(); c.translate(g.x, y); c.rotate(rot);
    block(c, [[-180, -90], [150, -90], [150, 90], [-180, 90], [-230, 0]], YEL, 1610 + k, { kw: 6 }); c.fillStyle = CHIP; c.beginPath(); c.arc(-185, 0, 14, 0, TAU); c.fill(); c.strokeStyle = BLK; c.lineWidth = 4; c.stroke();
    inkText(c, g.old, -10, -45, 56, '"DejaVu Serif"', BLK, 220);
    const st = seg(t, g.t0 + .05, g.t0 + .2); if (st > 0) { c.save(); c.strokeStyle = BLUE; c.lineWidth = 10; c.lineCap = 'round'; c.beginPath(); c.moveTo(-110, -38); c.lineTo(-110 + 200 * st, -54); c.stroke(); c.restore(); }
    const wr = easeOutBack(seg(t, g.t0 + .15, g.t0 + .3)); if (wr > 0) { c.save(); c.translate(-10, 38); c.scale(wr, wr); inkText(c, g.neu, 0, 0, 92, 'Stamp', BLUE, 240); c.restore(); }
    c.restore(); });
  const a = easeOutBack(land(t, at(5, 2))), jy = lerp(H + 520, H + 5, a), th = easeOutBack(seg(t, at(5, 2), at(5, 2.4)));
  if (t > at(5, 2) - SLAM) jeff(c, CX, jy, VERT ? .82 : .74, { armR: lerp(0, -2.5, th), prop: th > .6 ? 'thumb' : null, bob: -Math.abs(Math.sin((t - at(5)) * Math.PI / BEAT)) * 6 });
  c.restore();
  if (t >= at(5, 3) - SLAM) stampLand(c, stampImg('DEAL!', BLUE, 170), CX + sx, (VERT ? 245 : 150) + sy, -.06, 1, t, at(5, 3));
}
// ================= bar 7: case closed =================
function sceneClosed(c, t) {
  deskBg(c, t);
  const [sx, sy] = shake(t, [[at(6), 10], [at(6, 3), 12]]);
  const back = 1.08 - .08 * easeOut(seg(t, at(6), at(7)));
  c.save(); c.translate(sx, sy); c.translate(CX, CY); c.scale(back, back); c.rotate(.012); c.translate(-CX, -CY);
  const F = FOLDER;
  c.save(); c.globalAlpha = .3; c.translate(14, 18); c.fillStyle = BLK; c.fill(polyPath(folderShape(F.x, F.y, F.w, F.h))); c.restore();
  block(c, folderShape(F.x, F.y, F.w, F.h), CHIP, 1701, { kw: 7 }); dotsIn(c, folderShape(F.x, F.y, F.w, F.h), YEL, .3, 1702, 11);
  block(c, rect(F.x + 60, F.y + 8, 250, 28), CHIP, 1703, { kw: 3 }); inkText(c, 'CASE FILE', F.x + 185, F.y + 23, 26, '"Liberation Mono"', BLK, 230);
  // the screen-print logo, slapped on like a sticker (used exactly as supplied)
  const im = IMG.sp, [bx, by, bw, bh] = IMG.spBox, lw = VERT ? 900 : 820, lh = bh * lw / bw, q = land(t, at(6)), s = lerp(1.6, 1, easeIn(q));
  c.save(); c.translate(VERT ? 540 : 900, VERT ? 700 : 560); c.scale(s, s); c.rotate(-.03); c.drawImage(im, bx, by, bw, bh, -lw / 2, -lh / 2, lw, lh); c.restore();
  c.restore();
  const a = easeOutBack(land(t, at(6, 2))), jy = lerp(H + 520, H + 5, a), th = easeOutBack(seg(t, at(6, 2), at(6, 2.4)));
  if (t > at(6, 2) - SLAM) jeff(c, VERT ? 800 : 1640, jy, VERT ? .72 : .66, { armR: lerp(0, -2.5, th), prop: th > .6 ? 'thumb' : null, head: -.05 });
  if (t >= at(6, 3) - SLAM) stampLand(c, stampImg('LIVE NOW', BLUE, 140), (VERT ? 500 : 1390) + sx, (VERT ? 1160 : 250) + sy, VERT ? .06 : .1, VERT ? .9 : 1, t, at(6, 3));
  // beat 4: a giant rubber stamp comes down, fills the frame on the downbeat of bar 8
  const d = seg(t, at(6, 4), at(7));
  if (d > 0) rubberStamp(c, easeIn(d));
}
const STAMP_FACE = VERT ? [480, 830] : [820, 470];   // half-size; at 1.25x it covers the frame
function rubberStamp(c, u) {   // u: 0 = high above, 1 = pressed flat (covers the frame)
  const s = lerp(.35, 1.25, u), y = lerp(VERT ? -900 : -500, CY, u), [hw, hh] = STAMP_FACE;
  c.save(); c.translate(CX, y); c.scale(s, s);
  c.save(); c.globalAlpha = .35 * u; c.fillStyle = BLK; c.fillRect(-hw - 80, -hh - 50, 2 * hw + 160, 2 * hh + 100); c.restore();
  block(c, rect(-hw, -hh, 2 * hw, 2 * hh), BLUE, 1801, { kw: 10 });
  block(c, rect(-300, -hh - 150, 600, 160), BLK, 1802, { kw: 6 }); block(c, rect(-120, -hh - 430, 240, 300), YEL, 1803, { kw: 6 });
  c.restore();
}
// ================= bar 8: sign-off =================
function sceneSignoff(c, t) {
  paperBg(c);
  // the official logo: exact file, no texture, no recolour, no distortion; held still
  const im = IMG.logo, [bx, by, bw, bh] = IMG.logoBox, lw = VERT ? 900 : 1000, lh = bh * lw / bw;
  c.drawImage(im, bx, by, bw, bh, CX - lw / 2, CY - lh / 2, lw, lh);
  const lift = seg(t, at(7), at(7) + .3);   // the stamp lifts away, revealing it
  if (lift < 1) { c.save(); c.globalAlpha = 1; const u = easeIn(lift); c.translate(0, -(H + 320) * u); rubberStampFlat(c); c.restore(); }
}
function rubberStampFlat(c) { const [hw, hh] = STAMP_FACE; c.save(); c.translate(CX, CY); c.scale(1.25, 1.25); block(c, rect(-hw, -hh, 2 * hw, 2 * hh), BLUE, 1801, { kw: 10 }); c.restore(); }

// ================= assembly =================
function drawPrint(c) { printFinish(c); }
function drawAt(g, fn, t) { resetT(g); g.globalAlpha = 1; fn(g, t); }
function drawScene(c, t) {
  resetT(c);
  if (t < at(0, 4.5)) { sceneFile(c, t); return drawPrint(c); }
  if (t < at(1)) { const u = easeIO(seg(t, at(0, 4.5), at(1))), F = FOLDER;   // cover flips open while the camera dives into the page
    const k = lerp(1, W / (F.w - 40), u), ox = F.x + 20 + (F.w - 40) / 2, oy = F.y + 60 + (F.h - 80) / 2;
    c.save(); c.translate(CX, CY); c.scale(k, k); c.translate(-lerp(CX, ox, u), -lerp(CY, oy, u)); sceneFile(c, t, Math.min(1, u * 1.6)); c.restore(); return drawPrint(c); }
  if (t < at(2)) { boardWithLens(c, t); return drawPrint(c); }
  if (t < at(3)) { scenePhone(c, t); return drawPrint(c); }
  if (t < at(3, 4)) { sceneHidden(c, t); return drawPrint(c); }
  if (t < at(4)) {   // the frozen frame becomes a Polaroid and flies to the corner of the next page
    const u = easeIO(seg(t, at(3, 4), at(4)));
    sceneWarningBg(c, t); pinnedEvidence(c, t, 0);
    const x = lerp(CX, CAUGHT_P[0], u), y = lerp(CY, CAUGHT_P[1], u), s = lerp(2.6, 1, u), rot = lerp(0, CAUGHT_P[2], u) + Math.sin(u * Math.PI) * .25;
    caughtPolaroid(c, x, y, s, rot); return drawPrint(c);
  }
  if (t < at(4, 4.5)) { sceneWarning(c, t); return drawPrint(c); }
  if (t < at(5)) { drawAt(L1.getContext('2d'), sceneWarning, t); drawAt(L2.getContext('2d'), sceneDeals, t); pageTurn(c, L1, L2, easeIn(seg(t, at(4, 4.5), at(5) - .01))); return drawPrint(c); }
  if (t < at(5, 4)) { sceneDeals(c, t); return drawPrint(c); }
  if (t < at(6)) { const u = easeIn(seg(t, at(5, 4), at(6)));   // the folder cover swings shut over the deals
    sceneDeals(c, t); c.save(); c.translate(0, 0); c.scale(u, 1); block(c, rect(0, -20, W + 40, H + 40), CHIP, 1901, { kw: 10 }); dotsIn(c, rect(0, -20, W + 40, H + 40), YEL, .3, 1902, 11); c.restore(); return drawPrint(c); }
  if (t < at(7)) { sceneClosed(c, t); return drawPrint(c); }
  return sceneSignoff(c, t);   // no print finish over the official logo
}
function sceneWarningBg(c, t) { paperBg(c); dotsIn(c, rect(-40, -40, W + 80, H + 80), BLUE, .2, 1401, 14); }
function pageTurn(c, front, back, p) {
  const d = [-.78, -.62], n0 = Math.hypot(...d); d[0] /= n0; d[1] /= n0;
  const s = p * 2500, q = [W + d[0] * s, H + d[1] * s], frame = [[0, 0], [W, 0], [W, H], [0, H]], n = [-d[0], -d[1]];
  blit(c, back);
  const keep = clipHalf(frame, q, [-n[0], -n[1]]); if (keep.length > 2) { c.save(); c.clip(polyPath(keep)); blit(c, front); c.restore(); }
  const lifted = clipHalf(frame, q, n);
  if (lifted.length > 2) { const refl = lifted.map(([x, y]) => { const v = (x - q[0]) * n[0] + (y - q[1]) * n[1]; return [x - 2 * v * n[0], y - 2 * v * n[1]]; });
    const flap = clipHalf(refl, q, [-n[0], -n[1]]); if (flap.length > 2) { c.save(); c.globalAlpha = .25; c.fillStyle = BLK; c.fill(polyPath(flap.map(([x, y]) => [x + 18, y + 22]))); c.restore(); block(c, flap, CHIP, 1950, { kw: 6 }); dotsIn(c, flap, BLUE, .15, 1951, 12); } }
}

// ================= runtime =================
const CV = document.getElementById('c'); CV.width = OUT_W; CV.height = OUT_H; const CTX = CV.getContext('2d');
function frame(i) { const t = Math.min(i / FPS, DUR - 1e-6); FILM_T = t; resetT(CTX); CTX.globalAlpha = 1; drawScene(CTX, t); resetT(CTX); }
window.__NFR = NFR; window.__FPS = FPS; window.__frame = i => { frame(i); return CV.toDataURL('image/png'); };
(async () => {
  await loadPrintKit();
  await Promise.all([loadImg('logo', 'assets/official_logo.png'), loadImg('sp', 'assets/casefile/logo_screenprint.webp')]);
  IMG.logoBox = alphaBox(IMG.logo); IMG.spBox = alphaBox(IMG.sp);
  const q = new URLSearchParams(location.search); frame(+(q.get('frame') || 0));
  window.__ready = true;
})().catch(e => { console.error(e); window.__error = String(e); });
