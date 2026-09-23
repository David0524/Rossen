'use strict';
/* Rossen Reports explainer: the fake MyChart email scam. 44.5 s, 1080x1920 (9:16), 24 fps, one continuous shot.
   Case-file screen-print look (printkit.js). 96 BPM: one beat = 0.625 s, one bar = 2.5 s, one idea per bar, a caption
   on each downbeat. Every landing finishes ON its beat. Text and key action stay inside the platform safe zone:
   clear of the top 15%, the bottom 25% and the right 15% (x 60-900, y 300-1430).

   BAIT   bar 0  0.0   the email is already on screen: MyChart header, NEW TEST RESULTS      "GOT THIS EMAIL?"
          bar 1  2.5   scroll down: FREE MEDICARE HEALTH KIT                                 "A FREE KIT? NEW RESULTS?"
          bar 2  5.0   scroll down: the countdown ticks on every beat, CLICK HERE pulses     "HURRY! ACT NOW!"
          bar 3  7.5   rising reveal: the email hangs on a hook, the scammer is fishing      stamp IT'S BAIT! on 3, dive to the button on 4
   TRAP   bar 4  10.0  click, zoom through the button into a fake site                       "THE LINK OPENS A FAKE SITE"
          bar 5  12.5  Jeff's magnifier over the garbled address, FAKE! on 3                 "IT LOOKS REAL. IT'S NOT."
          bar 6  15.0  the form drops in on eighths: login, Medicare number, name, card      "IT ASKS FOR YOUR INFO"
   THEFT  bar 7  17.5  the hook snags the cards one by one (beats 2 and 4)                  "THEN THEY REEL IT ALL IN"
          bar 8  20.0  ... the last two cards
          bar 9  22.5  camera rises to the pier: the scammer reels the loot in, STOLEN! on 3
   FIX    bar 10 25.0  the screen-print logo slams down and knocks him off; Jeff pops up     "HERE'S HOW TO STAY SAFE"
          bar 11 27.5  the email drops back in; Jeff points; a big X lands on the link on 3  "DON'T CLICK THE LINK"
          bar 12 30.0  a phone rises; Jeff taps the MyChart app tile on 3                    "OPEN THE MYCHART APP YOURSELF"
          bar 13 32.5  a browser bar slides in; YOUR PROVIDER'S SITE types itself            "OR TYPE IN YOUR PROVIDER'S WEBSITE"
          bar 14 35.0  zoom into the real inbox; the magnifier checks it, CHECKED! on 3      "CHECK IF THE MESSAGE IS REAL"
          bar 15 37.5  DON'T CLICK. on 1, GO TO THE APP YOURSELF. on 3, Jeff thumbs up
          bar 16 40.0  held; the rubber stamp comes down on 4
   END    bar 17 42.5  the official logo, untouched, revealed as the stamp lifts; still from 42.8
*/
setFormat({ ar: '9:16', width: 1080 });
const FPS = 24, BEAT = .625, BAR = 2.5, E8 = BEAT / 2, S16 = BEAT / 4;
const at = (bar, beat = 1) => bar * BAR + (beat - 1) * BEAT;   // bar 0-based, beat 1-based
const DUR = at(17) + 2, NFR = Math.round(FPS * DUR);
const SAFE = { x0: 60, x1: 900, y0: 300, y1: 1430 }, SCX = 480, SCY = 865;   // centre of the safe zone
const L1 = layer(), L2 = layer();
let SP = null, FILM_T = 0;
const Q = new URLSearchParams(location.search), SHOW_SAFE = Q.has('safe');

// ================= small kit =================
const clamp01 = v => Math.max(0, Math.min(1, v));
const pop = (t, t0) => t < t0 ? lerp(1.3, 1, easeIn(land(t, t0))) : 1 + .06 * Math.exp(-(t - t0) * 12) * Math.cos((t - t0) * 30);   // lands on t0, wobbles
function bgDots(c, col = BLUE, lo = .1, hi = .5, cell = 20) {
  paperBg(c); dotScreen(c, polyPath(rect(0, 0, W, H)), [0, 0, W, H], { cell, color: col, density: (x, y) => lo + (hi - lo) * Math.min(1, Math.hypot(x - SCX, y - SCY) / 1100), angle: ANG[col] ?? .3, seed: 3001 });
}
function shadowRect(c, x, y, w, h, a = .28) { c.save(); c.globalAlpha = a; c.fillStyle = BLK; c.fillRect(x + 14, y + 18, w, h); c.restore(); }
function pill(c, cx, cy, w, h, col, label, size, tcol = BLK, seed = 2101) { block(c, rrPts(cx - w / 2, cy - h / 2, w, h, h / 2, 5), col, seed, { kw: 6 }); inkText(c, label, cx, cy + 4, size, 'Stamp', tcol, w - 60); }
// the caption band: short ALL-CAPS lines on black paper chips, top of the safe zone, one set per downbeat
const CAPS = [
  [at(0), 'GOT THIS EMAIL?'], [at(1), 'A FREE KIT?', 'NEW RESULTS?'], [at(2), 'HURRY!', 'ACT NOW!'], [at(3), null],
  [at(4), 'THE LINK OPENS', 'A FAKE SITE'], [at(5), 'IT LOOKS REAL.', "IT'S NOT."], [at(6), 'IT ASKS FOR', 'YOUR INFO'],
  [at(7), 'THEN THEY', 'REEL IT ALL IN'], [at(9), null],
  [at(10), "HERE'S HOW", 'TO STAY SAFE'], [at(11), "DON'T CLICK", 'THE LINK'], [at(12), 'OPEN THE MYCHART', 'APP YOURSELF'],
  [at(13), 'OR TYPE IN YOUR', "PROVIDER'S WEBSITE"], [at(14), 'CHECK IF THE', 'MESSAGE IS REAL'], [at(15), null],
];
function captions(c, t) {
  let cur = null; for (const cp of CAPS) if (t >= cp[0] - SLAM) cur = cp;
  if (!cur || !cur[1]) return;
  cur.slice(1).forEach((s, i) => {
    const t0 = cur[0] + i * E8; if (t < t0 - SLAM) return;
    const size = 76; c.font = `${size}px Stamp`; const tw = Math.min(c.measureText(s).width, 780), w = tw + 64, h = 108, y = 372 + i * 122, sc = pop(t, t0), rot = i % 2 ? .012 : -.012;
    c.save(); c.translate(SCX, y); c.rotate(rot); c.scale(sc, sc);
    c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fillRect(-w / 2 + 9, -h / 2 + 11, w, h); c.restore();
    ink(c, rect(-w / 2, -h / 2, w, h), BLK, 3100 + i, { amp: 3 }); inkText(c, s, 0, 5, size, 'Stamp', CHIP, 780);
    c.restore();
  });
}
function stampFit(c, word, col, size, x, y, rot, sc, t, t0, maxW = 800) {   // a stamp scaled down if it would leave the safe zone
  const im = stampImg(word, col, size), k = Math.min(sc, maxW / (im.width * Math.abs(Math.cos(rot)) + im.height * Math.abs(Math.sin(rot))));
  stampLand(c, im, x, y, rot, k, t, t0);
}
function xMark(c, x, y, s, t, t0) {   // a big black X slapped over something
  if (t < t0 - SLAM) return; const k = pop(t, t0) * s;
  c.save(); c.translate(x, y); c.scale(k, k);
  for (const r of [.72, -.72]) { c.save(); c.rotate(r); block(c, rrPts(-190, -34, 380, 68, 30, 4), BLK, 3200 + (r > 0 ? 1 : 2), { kw: 0, key: false }); c.restore(); }
  for (const r of [.72, -.72]) { c.save(); c.rotate(r); key(c, rrPts(-190, -34, 380, 68, 30, 4), 5, 3210 + (r > 0 ? 1 : 2), true, YEL); c.restore(); }
  c.restore();
}
function cursorArrow(c, x, y, s = 1) {   // a plain pointer arrow
  const P = [[0, 0], [0, 70], [18, 54], [32, 86], [46, 80], [32, 48], [56, 48]].map(([a, b]) => [x + a * s, y + b * s]);
  block(c, P, CHIP, 3301, { kw: 6 });
}
function tapRing(c, x, y, t, t0) { const u = seg(t, t0, t0 + .4); if (u <= 0 || u >= 1) return; c.save(); c.globalAlpha = 1 - u; c.strokeStyle = BLK; c.lineWidth = 8; c.beginPath(); c.arc(x, y, 30 + 90 * easeOut(u), 0, TAU); c.stroke(); c.restore(); }
function check(c, x, y, s, t, t0) {   // a yellow check mark, keyed black
  if (t < t0 - SLAM) return; const k = pop(t, t0) * s; c.save(); c.translate(x, y); c.scale(k, k);
  const P = [[-90, -5], [-40, 45], [95, -95], [120, -65], [-40, 105], [-120, 25]]; block(c, P, YEL, 3401, { kw: 8 }); c.restore();
}

// ================= the scammer puppet (cut from the reference) =================
// pose: { head, rod (radians, around the reel), legL, legR, bob, tilt, sx } -> returns the rod tip in the caller's coordinates
function scammer(c, x, y, s, p = {}) {
  const base = c.getTransform();
  c.save(); c.translate(x, y); c.rotate(p.tilt || 0); c.scale(s * (p.sx || 1), s); c.translate(-SP.feet[0], -SP.feet[1] - (p.bob || 0));
  const part = (k, a = 0) => { const m = SP.parts[k], [px, py] = m.pivot; c.save(); c.translate(px, py); c.rotate(a); c.translate(-px, -py); c.drawImage(IMG['s_' + k], m.x, m.y); c.restore(); };
  part('legL', p.legL || 0); part('legR', p.legR || 0); part('torso'); part('rod', p.rod || 0); part('head', p.head || 0);
  const M = base.inverse().multiply(c.getTransform()), [px, py] = SP.parts.rod.pivot, a = p.rod || 0, [tx, ty] = SP.tip;
  const q = M.transformPoint(new DOMPoint(px + Math.cos(a) * (tx - px) - Math.sin(a) * (ty - py), py + Math.sin(a) * (tx - px) + Math.cos(a) * (ty - py)));
  c.restore(); return [q.x, q.y];
}
function fishLine(c, a, b, sag = 20, w = 3.5) { c.save(); c.strokeStyle = BLK; c.lineWidth = w; c.lineCap = 'round'; c.beginPath(); c.moveTo(a[0], a[1]); c.quadraticCurveTo((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + sag, b[0], b[1]); c.stroke(); c.restore(); }
function hook(c, x, y, s = 1) {   // eye at (x, y); returns the point things hang from
  c.save(); c.translate(x, y); c.scale(s, s); c.strokeStyle = BLK; c.lineCap = 'round'; c.lineJoin = 'round';
  c.lineWidth = 7; c.beginPath(); c.arc(0, 0, 9, 0, TAU); c.stroke();
  c.lineWidth = 9; c.beginPath(); c.moveTo(0, 9); c.lineTo(0, 70); c.quadraticCurveTo(0, 100, -26, 96); c.quadraticCurveTo(-44, 90, -40, 66); c.stroke();
  c.lineWidth = 6; c.beginPath(); c.moveTo(-40, 66); c.lineTo(-30, 76); c.stroke();
  c.restore(); return [x - 14 * s, y + 97 * s];
}
function pier(c, x0, x1, y) {   // a plank pier with two posts, over halftone water
  for (const px of [x0 + 60, x1 - 70]) block(c, rect(px, y + 30, 34, 260), BLK, 3500 + px, { kw: 3 });
  block(c, rect(x0, y, x1 - x0, 42), BLK, 3510, { kw: 3 }); for (let k = x0 + 90; k < x1; k += 110) ink(c, rect(k, y + 6, 4, 30), CHIP, 3520 + k, { reg: false });
}
function water(c, y0, h, seed = 3600, x0 = -60, x1 = W + 60) { dotsIn(c, rect(x0, y0, x1 - x0, h), BLUE, .55, seed, 14); for (let k = 0; k < 5; k++) { const yy = y0 + 30 + k * 90, r = rng(seed + k); ink(c, rect(r() * 500 - 100, yy, 240 + r() * 300, 7), CHIP, seed + 10 + k, { reg: false }); ink(c, rect(560 + r() * 300, yy + 40, 160 + r() * 200, 7), CHIP, seed + 20 + k, { reg: false }); } }

// ================= the fake email =================
const EW = 780, EH = 1420, EX = SCX - EW / 2;   // world placement: x 90..870, y 0..1420
function timerDigit(t) { return Math.max(3, 9 - Math.max(0, Math.floor((t - at(2)) / BEAT) + 1)); }
function giftBox(c, x, y, s) {
  c.save(); c.translate(x, y); c.scale(s, s);
  block(c, rect(-120, -40, 240, 150), BLUE, 2201, { kw: 6 }); block(c, rect(-138, -84, 276, 56), BLUE, 2202, { kw: 6 });
  ink(c, rect(-18, -84, 36, 194), CHIP, 2203, { reg: false }); key(c, rect(-18, -84, 36, 194), 4, 2204);
  block(c, [[0, -84], [-70, -150], [-86, -112]], CHIP, 2205, { kw: 5 }); block(c, [[0, -84], [70, -150], [86, -112]], CHIP, 2206, { kw: 5 });
  c.restore();
}
function emailCard(c, t) {
  shadowRect(c, 0, 0, EW, EH);
  block(c, rect(0, 0, EW, EH), CHIP, 2001, { kw: 6 });
  ink(c, rect(0, 0, EW, 124), BLUE, 2002); key(c, rect(0, 0, EW, 124), 6, 2003);
  inkText(c, 'MyChart', 44, 66, 58, '"Liberation Sans"', CHIP, 330, 'left');   // plain text only, no logo
  inkText(c, 'NEW MESSAGE', EW - 40, 68, 30, '"Liberation Mono"', CHIP, 300, 'right');
  const nb = pop(t, at(0, 2)); if (t > at(0, 2) - SLAM) { c.save(); c.translate(EW - 14, 8); c.scale(nb, nb); block(c, ellPts(0, 0, 34, 34, 0, 24), YEL, 2004, { kw: 5 }); inkText(c, '1', 0, 3, 44, 'Stamp', BLK, 40); c.restore(); }
  inkText(c, 'FROM: MyChart Supp0rt Teem', 44, 172, 30, '"Liberation Mono"', BLK, 700, 'left');
  inkText(c, 'NEW TEST', EW / 2, 272, 96, 'Stamp', BLK, 700); inkText(c, 'RESULTS READY', EW / 2, 376, 96, 'Stamp', BLK, 700);
  // the offer
  block(c, rect(40, 450, EW - 80, 460), YEL, 2010, { kw: 5 });
  const gp = t < at(1, 2) - SLAM ? 1 : pop(t, at(1, 2)) * (1 + .03 * Math.sin((t - at(1)) * TAU / BEAT));
  giftBox(c, EW / 2, 600, gp);
  inkText(c, 'FREE MEDICARE', EW / 2, 770, 80, 'Stamp', BLK, 660); inkText(c, 'HEALTH KIT!', EW / 2, 862, 80, 'Stamp', BLK, 660);
  // the countdown: one tick per beat from bar 2
  inkText(c, 'OFFER ENDS IN', EW / 2, 1002, 56, 'Stamp', BLK, 660);
  const d = timerDigit(t), flash = t > at(2) && Math.floor((t - at(2)) / E8) % 2 === 1;
  ['0', '0', ':', '0', String(d)].forEach((ch, k) => { const x = EW / 2 + (k - 2) * 118;
    if (ch === ':') { inkText(c, ':', x, 1106, 110, 'Stamp', BLK, 60); return; }
    const hot = k === 4 && flash; block(c, rect(x - 50, 1050, 100, 116), hot ? BLK : CHIP, 2020 + k, { kw: 5 }); inkText(c, ch, x, 1112, 96, '"Liberation Mono"', hot ? YEL : BLK, 90); });
  const bp = 1 + .05 * Math.max(0, Math.sin((t - at(2)) * TAU / BEAT));
  c.save(); c.translate(EW / 2, 1300); c.scale(bp, bp); pill(c, 0, 0, 560, 136, YEL, 'CLICK HERE', 86); c.restore();
}
// world of the bait: the email hangs on a hook from the scammer's line; he stands on a pier high above
const S_FEET = [150, -700], S_K = 1.15;
function baitCam(t) {   // {cy, z}: scrolls down the email, rises to reveal the line, dives into the button
  let cy = 295 + 12 * Math.sin(t * 2), z = 1 + .015 * Math.sin(t * 1.3);
  cy = lerp(cy, 560, easeOut(seg(t, at(1) - .35, at(1))));
  cy = lerp(cy, 1030, easeOut(seg(t, at(2) - .35, at(2))));
  const up = easeIO(seg(t, at(3), at(3, 2))); cy = lerp(cy, -521, up); z = lerp(z, .6, up);
  const dv = easeIn(seg(t, at(3, 4), at(4))); cy = lerp(cy, 1300, dv); z = lerp(z, 1.5, dv);
  return { cy, z };
}
function sceneBait(c, t) {
  bgDots(c, BLUE, .08, .42);
  const { cy, z } = baitCam(t), up = easeIO(seg(t, at(3), at(3, 2))), dv = easeIn(seg(t, at(3, 4), at(4)));
  // the email scrolls inside a window that ends at the safe line; the window opens out to the full frame for the reveal
  const VP = [lerp(80, -20, up), lerp(560, -20, up), lerp(800, W + 40, up), lerp(870, H + 40, up)];
  c.save(); c.beginPath(); c.rect(...VP); c.clip();
  c.save(); c.translate(SCX, SCY); c.scale(z, z); c.translate(-SCX, -cy);
  water(c, -600, 3000, 3601, -2400, 3400);
  pier(c, -1400, 380, S_FEET[1]);
  const glee = t > at(3, 3) ? Math.sin((t - at(3, 3)) * TAU / E8) * .06 : 0;
  const tip = scammer(c, S_FEET[0], S_FEET[1], S_K, { rod: -.05 + .04 * Math.sin(t * 3), head: glee, bob: Math.abs(Math.sin(t * Math.PI / BEAT)) * 6 });
  // the email swings a little on its hook
  const bounce = 55 * Math.exp(-t * 5) * Math.cos(t * 13), sw = .012 * Math.sin(t * 2.4);
  const eye = [SCX, -60 + bounce];
  fishLine(c, tip, eye, 30);
  c.save(); c.translate(SCX, bounce); c.rotate(sw); c.translate(-EW / 2, 0); emailCard(c, t); c.restore();
  hook(c, eye[0], eye[1], 1.3);
  c.restore();
  // deep water: below the safe line the hanging email sinks out of sight
  const deep = up * (1 - dv);
  if (deep > 0) { dotScreen(c, polyPath(rect(0, 1290, W, 160)), [0, 1290, W, 160], { cell: 16, color: BLUE, density: (x, y) => deep * clamp01((y - 1290) / 150), angle: ANG[BLUE], seed: 3620 });
    c.save(); c.globalAlpha = deep; ink(c, rect(-20, 1440, W + 40, H - 1400), BLUE, 3621, { amp: 5 }); c.restore(); }
  c.restore();
  if (up < 1) { c.save(); c.globalAlpha = 1 - up; key(c, rrPts(...VP, 26, 4), 10, 3630); c.restore(); }
  // the pointer arrives on beat 4 and clicks on the downbeat of bar 4
  if (t > at(3, 4) - .2) { const u = easeOut(seg(t, at(3, 4) - .2, at(4) - .05)); cursorArrow(c, lerp(900, 560, u), lerp(1500, 900, u), t > at(4) - .05 ? .85 : 1); }
  if (t >= at(3, 3) - SLAM && t < at(3, 4)) stampFit(c, "IT'S BAIT!", BLK, 150, SCX, 1010, -.08, .95, t, at(3, 3));
}
// the button's on-screen rect at the end of the dive (the zoom-through window)
function buttonRect() { const z = 1.5; return [SCX - 280 * z, SCY - 68 * z, 560 * z, 136 * z]; }

// ================= the fake site =================
const BR = { x: 70, y: 570, w: 820, h: 850 };
const URL_TXT = 'htp://myc-hart.l0gin-kit.zz/?!';   // obviously garbled: not a real address
const FIELDS = ['LOGIN & PASSWORD', 'MEDICARE NUMBER', 'NAME & ADDRESS', 'CARD NUMBER'];
const FIELD_T = [at(6, 1.5), at(6, 2), at(6, 2.5), at(6, 3)], SNAG_T = [at(7, 2), at(7, 4), at(8, 2), at(8, 4)];
const fieldY = k => 810 + k * 150;
function urlBar(c) {
  ink(c, rect(BR.x, BR.y, BR.w, 100), BLK, 2301);
  for (let k = 0; k < 3; k++) { c.fillStyle = [BLUE, YEL, CHIP][k]; c.beginPath(); c.arc(BR.x + 34 + k * 32, BR.y + 50, 10, 0, TAU); c.fill(); }
  block(c, rrPts(BR.x + 140, BR.y + 22, BR.w - 170, 56, 28, 4), CHIP, 2302, { kw: 3 });
  inkText(c, URL_TXT, BR.x + 170, BR.y + 52, 30, '"Liberation Mono"', BLK, BR.w - 220, 'left');
}
function fieldCard(c, k, t, x, y, rot = 0) {
  c.save(); c.translate(x, y); c.rotate(rot);
  shadowRect(c, -380, 0, 760, 130, .2);
  block(c, rect(-380, 0, 760, 130), CHIP, 2400 + k, { kw: 5 });
  inkText(c, FIELDS[k], -350, 36, 46, 'Stamp', BLK, 700, 'left');
  block(c, rect(-350, 66, 700, 48), '#ffffff', 2410 + k, { kw: 3, reg: false });
  const n = Math.max(0, Math.min(14, Math.floor((t - FIELD_T[k] - .1) / (S16 / 2))));
  inkText(c, '•'.repeat(n), -330, 92, 44, '"Liberation Mono"', BLK, 660, 'left');
  c.restore();
}
function sitePage(c, t, withBody = true) {
  shadowRect(c, BR.x, BR.y, BR.w, BR.h);
  block(c, rect(BR.x, BR.y, BR.w, BR.h), CHIP, 2300, { kw: 6 });
  urlBar(c);
  ink(c, rect(BR.x, BR.y + 100, BR.w, 96), BLUE, 2303);
  inkText(c, 'MyChart', BR.x + 36, BR.y + 150, 52, '"Liberation Sans"', CHIP, 300, 'left');   // plain text only
  inkText(c, 'SIGN IN', BR.x + BR.w - 36, BR.y + 152, 38, 'Stamp', CHIP, 240, 'right');
  if (!withBody) return;
  const out = easeIn(seg(t, at(6) - .1, at(6) + .2));   // the pitch slides away when the form arrives
  if (out < 1) { c.save(); c.globalAlpha = 1 - out; c.translate(0, -60 * out);
    inkText(c, 'SIGN IN TO GET', SCX, 900, 70, 'Stamp', BLK, 740); inkText(c, 'YOUR FREE KIT', SCX, 990, 70, 'Stamp', BLK, 740);
    block(c, rrPts(SCX - 160, 1070, 320, 70, 35, 4), YEL, 2310, { kw: 4 }); inkText(c, 'SECURE ✓', SCX, 1108, 40, 'Stamp', BLK, 280);
    pill(c, SCX, 1250, 440, 110, BLUE, 'SIGN IN', 60, CHIP, 2311);
    c.restore(); }
}
function sceneSite(c, t) {
  bgDots(c, BLK, .04, .2, 18);
  const dr = 8 * Math.sin((t - at(4)) * .8);   // the camera keeps drifting
  c.save(); c.translate(0, dr);
  sitePage(c, t);
  // the form: four cards on eighths, then the hook takes them one by one
  for (let k = 0; k < 4; k++) {
    if (t < FIELD_T[k] - SLAM) continue;
    const ts = SNAG_T[k], y0 = fieldY(k), dropY = lerp(-260, y0, easeIn(land(t, FIELD_T[k])));
    if (t < ts) { fieldCard(c, k, t, SCX, dropY); continue; }
    const u = seg(t, ts + .08, ts + .5), shake = t < ts + .08 ? Math.sin((t - ts) * 90) * 6 : 0;   // snag, then yank
    const y = lerp(y0, -500, easeIn(u)), rot = .25 * Math.sin(u * 5) * (k % 2 ? 1 : -1);
    fieldCard(c, k, t, SCX + shake, y, rot);
    if (u < 1) { const hp = [SCX + shake - 14, y - 96]; fishLine(c, [SCX + 40, -80], [hp[0] + 14, hp[1]], 0); hook(c, hp[0] + 14, hp[1], 1); }
  }
  // the hook coming down for the next card
  for (let k = 0; k < 4; k++) { const ts = SNAG_T[k], a = seg(t, ts - .55, ts); if (a <= 0 || a >= 1) continue;
    const y = lerp(-150, fieldY(k) - 96, easeOut(a)), x = SCX + 20 * Math.sin(t * 7); fishLine(c, [SCX + 40, -80], [x, y], 0); hook(c, x, y, 1); }
  c.restore();
  // Jeff checks the address with the magnifier (bar 5)
  const jin = easeOutBack(land(t, at(5))) * (1 - easeIn(seg(t, at(6), at(6) + .3)));
  if (jin > 0) {
    const raise = easeOut(seg(t, at(5, 2) - SLAM, at(5, 2)));
    const J = jeff(c, 230, lerp(2500, 1840, jin), .7, { armR: lerp(0, -2.2, raise), head: -.06 * raise });
    if (raise > 0) { const target = [BR.x + 470, BR.y + 50 + dr], R = lerp(40, 120, raise), cx = lerp(J.hand[0] + 120, target[0], raise), cy = lerp(J.hand[1] - 160, target[1], raise);
      magnifier(c, cx, cy, R, J.hand, raise > .6 ? () => { c.translate(cx, cy); c.scale(1.9, 1.9); c.translate(-cx, -cy + dr); urlBar(c); } : null); }
  }
  if (t >= at(5, 3) - SLAM && t < at(6)) stampFit(c, 'FAKE!', BLK, 170, 520, 900, -.1, 1, t, at(5, 3));
}

// ================= the loot, reeled in on the pier =================
function scenePier(c, t, o = {}) {
  if (o.fixBg) fixBg(c); else { bgDots(c, BLUE, .12, .45); water(c, 1300, 700, 3701); }
  const knock = o.knock ?? 0;   // bar 10: the logo slams and knocks him off
  if (!o.noPier) pier(c, -60, 470, 1250);
  const crank = t > at(9, 2.5) ? Math.sin((t - at(9, 2.5)) * TAU / E8) * .12 * Math.exp(-(t - at(9, 2.5)) * 1.5) : 0;
  const reel = -.1 - .22 * easeOut(seg(t, at(9, 2.5) - SLAM, at(9, 2.5))) + crank;
  const fx = 310 - knock * 800, fy = 1250 - knock * 600 + knock * knock * 300;
  const tip = scammer(c, fx, fy, .95, { rod: reel, head: .08 * Math.sin(t * 6), tilt: -knock * 2.2, bob: Math.abs(Math.sin(t * Math.PI / BEAT)) * 5 });
  // the loot: four cards hanging from the hook
  const fall = o.fall ?? 0, hp = [tip[0] + 20, tip[1] + 300 + fall * 900];
  if (fall < 1) {
    if (fall === 0) fishLine(c, tip, hp, 10);
    const hk = hook(c, hp[0], hp[1], .8);
    for (let k = 0; k < 4; k++) { const r = (k - 1.5) * .18 + .05 * Math.sin(t * 4 + k), dy = fall * (300 + k * 200);
      c.save(); c.translate(hk[0], hk[1] + dy); c.rotate(r); c.scale(.36, .36); fieldCard(c, k, 99, 0, 20); c.restore(); }
  }
  if (t >= at(9, 3) - SLAM && t < at(10)) stampFit(c, 'STOLEN!', BLK, 170, SCX, 480, -.07, .95, t, at(9, 3));
}
function sceneRise(c, t) {   // bar 9: the camera rises from the empty fake site to the pier (each drawn whole, then slid)
  const off = easeIO(seg(t, at(9), at(9, 2))) * H, g1 = L1.getContext('2d'), g2 = L2.getContext('2d');
  resetT(g1); sceneSite(g1, t); resetT(g2); scenePier(g2, t);
  c.save(); resetT(c); c.drawImage(L1, 0, off, W, H); c.drawImage(L2, 0, off - H, W, H); c.restore();
}

// ================= the fix =================
function fixBg(c) { bgDots(c, BLUE, .06, .3); }
function stickerLogo(c, x, y, lw, rot, s) { const im = IMG.sp, [bx, by, bw, bh] = IMG.spBox, lh = bh * lw / bw; c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s); c.drawImage(im, bx, by, bw, bh, -lw / 2, -lh / 2, lw, lh); c.restore(); }
function jeffUp(c, t, t0, x, p = {}, s = .72) { const a = easeOutBack(land(t, t0)); if (t < t0 - SLAM) return null; return jeff(c, x, lerp(2600, 1830, a), s, p); }
function scene10(c, t) {   // HERE'S HOW TO STAY SAFE
  const k = easeIn(seg(t, at(10), at(10) + .55)), fall = easeIn(seg(t, at(10), at(10) + .9));
  scenePier(c, t, { knock: k, fall, fixBg: t >= at(10), noPier: t >= at(10) });
  const [sx, sy] = shake(t, [[at(10), 18]]);
  if (t >= at(10) && t < at(10) + .3) { c.save(); c.globalAlpha = 1 - seg(t, at(10), at(10) + .3); c.fillStyle = CHIP; c.fillRect(0, 0, W, H); c.restore(); }
  stickerLogo(c, SCX + sx, 800 + sy, 720, -.03, lerp(1.9, 1, easeIn(land(t, at(10)))));
  const th = easeOutBack(seg(t, at(10, 2.5), at(10, 3)));
  jeffUp(c, t, at(10, 2), SCX, { armR: lerp(0, -2.5, th), prop: th > .6 ? 'thumb' : null });
}
function compactEmail(c, x, y) {   // the same fake email, short version
  shadowRect(c, x, y, EW, 520); block(c, rect(x, y, EW, 520), CHIP, 2501, { kw: 6 });
  ink(c, rect(x, y, EW, 110), BLUE, 2502); key(c, rect(x, y, EW, 110), 6, 2503);
  inkText(c, 'MyChart', x + 44, y + 58, 54, '"Liberation Sans"', CHIP, 330, 'left');
  inkText(c, 'FREE MEDICARE', x + EW / 2, y + 190, 74, 'Stamp', BLK, 700); inkText(c, 'HEALTH KIT!', x + EW / 2, y + 276, 74, 'Stamp', BLK, 700);
  pill(c, x + EW / 2, y + 410, 540, 130, YEL, 'CLICK HERE', 82);
}
const PH = { x: 330, y: 590, w: 460, h: 820 };
const TILE = { x0: PH.x + 44, y0: PH.y + 130, sz: 104, gap: 40 };
function phone(c, t, x, y) {
  c.save(); c.translate(x - PH.x, y - PH.y);
  shadowRect(c, PH.x, PH.y, PH.w, PH.h); block(c, rrPts(PH.x, PH.y, PH.w, PH.h, 56, 6), BLK, 2601, { kw: 6 });
  block(c, rrPts(PH.x + 22, PH.y + 60, PH.w - 44, PH.h - 120, 18, 4), CHIP, 2602, { kw: 3 });
  const tap = at(12, 3), press = t > tap && t < tap + .2 ? .9 : 1;
  for (let r = 0; r < 4; r++) for (let q = 0; q < 3; q++) {
    const tx = TILE.x0 + q * (TILE.sz + TILE.gap), ty = TILE.y0 + r * (TILE.sz + TILE.gap + 16), me = r === 1 && q === 1;
    c.save(); c.translate(tx + TILE.sz / 2, ty + TILE.sz / 2); if (me) c.scale(press, press);
    const col = me ? YEL : [BLUE, CHIP, BLK, BLUE, CHIP][(r * 3 + q) % 5];
    block(c, rrPts(-TILE.sz / 2, -TILE.sz / 2, TILE.sz, TILE.sz, 24, 4), col, 2610 + r * 3 + q, { kw: 4 });
    if (me) inkText(c, 'MyChart', 0, 4, 26, '"Liberation Sans"', BLK, TILE.sz - 12);   // plain text only
    else { c.fillStyle = col === CHIP ? BLUE : CHIP; c.globalAlpha = .9; if ((r + q) % 2) { c.beginPath(); c.arc(0, 0, 22, 0, TAU); c.fill(); } else c.fillRect(-20, -20, 40, 40); }
    c.restore();
  }
  const tcx = TILE.x0 + 1.5 * TILE.sz + TILE.gap, tcy = TILE.y0 + 1.5 * TILE.sz + TILE.gap + 16;
  tapRing(c, tcx, tcy, t, tap);
  const po = easeOutBack(seg(t, tap + .05, tap + .35));   // the tile pops out big
  if (po > 0) { c.save(); c.translate(lerp(tcx, PH.x + PH.w / 2, po), lerp(tcy, PH.y + 330, po)); c.scale(lerp(1, 2.9, po), lerp(1, 2.9, po)); c.rotate(-.04 * po);
    c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fillRect(-TILE.sz / 2 + 5, -TILE.sz / 2 + 6, TILE.sz, TILE.sz); c.restore();
    block(c, rrPts(-TILE.sz / 2, -TILE.sz / 2, TILE.sz, TILE.sz, 24, 4), YEL, 2690, { kw: 3 }); inkText(c, 'MyChart', 0, 4, 26, '"Liberation Sans"', BLK, TILE.sz - 12); c.restore(); }
  c.restore();
}
const PB = { x: 90, y: 620, w: 780, h: 560 };   // the real browser: an address bar you type yourself
function browser(c, t, x) {
  c.save(); c.translate(x - PB.x, 0);
  shadowRect(c, PB.x, PB.y, PB.w, PB.h); block(c, rect(PB.x, PB.y, PB.w, PB.h), CHIP, 2701, { kw: 6 });
  ink(c, rect(PB.x, PB.y, PB.w, 130), BLK, 2702);
  block(c, rrPts(PB.x + 30, PB.y + 30, PB.w - 60, 72, 36, 4), '#ffffff', 2703, { kw: 3, reg: false });
  const s = "YOUR PROVIDER'S SITE", n = Math.max(0, Math.min(s.length, Math.floor((t - at(13) - .12) / ((at(13, 3) - .3 - at(13)) / s.length))));
  inkText(c, s.slice(0, n) + (Math.floor(t * 4) % 2 ? '|' : ''), PB.x + 64, PB.y + 68, 40, '"Liberation Mono"', BLK, PB.w - 120, 'left');
  if (t >= at(13, 3) - SLAM) { const k = pop(t, at(13, 3)); c.save(); c.translate(PB.x + PB.w / 2, PB.y + 350); c.scale(k, k);
    inkText(c, 'YOUR PATIENT PORTAL', 0, -50, 58, 'Stamp', BLK, 700); pill(c, 0, 70, 380, 100, BLUE, 'SIGN IN', 54, CHIP, 2704); c.restore(); }
  c.restore();
}
const IB = { x: 90, y: 590, w: 780, h: 820 };
function inbox(c, t) {
  shadowRect(c, IB.x, IB.y, IB.w, IB.h); block(c, rect(IB.x, IB.y, IB.w, IB.h), CHIP, 2801, { kw: 6 });
  ink(c, rect(IB.x, IB.y, IB.w, 120), BLUE, 2802); inkText(c, 'MY MESSAGES', SCX, IB.y + 64, 62, 'Stamp', CHIP, 700);
  ['APPOINTMENT REMINDER', 'VISIT SUMMARY', 'BILLING QUESTION'].forEach((s, k) => { const y = IB.y + 170 + k * 150;
    block(c, rect(IB.x + 36, y, IB.w - 72, 120), '#ffffff', 2810 + k, { kw: 4, reg: false }); inkText(c, s, IB.x + 70, y + 62, 44, '"Liberation Sans"', BLK, IB.w - 140, 'left'); });
}
function sceneFix(c, t) {
  fixBg(c);
  // bar 11: the email drops back in; a big X on the link
  if (t < at(12) - .3) {
    const y = lerp(-700, 560, easeIn(land(t, at(11))));
    compactEmail(c, EX, y);
    xMark(c, SCX, y + 410, 1, t, at(11, 3));
    const pt = easeOut(seg(t, at(11, 2) - SLAM, at(11, 2)));
    jeff(c, SCX, 1830, .72, { armR: lerp(0, -2.35, pt), prop: pt > .5 ? 'point' : null });
    return;
  }
  // bars 12-13: the phone, then the browser; Jeff moves to the corner and points
  const jx = lerp(SCX, 190, easeIO(seg(t, at(12) - .3, at(12) + .2)));
  const out12 = easeIn(seg(t, at(12) - .3, at(12)));   // the email whips out left as the phone rises
  if (out12 < 1) { compactEmail(c, EX - 1200 * out12, 560); xMark(c, SCX - 1200 * out12, 970, 1, t, at(11, 3)); }
  const phY = lerp(2000, PH.y, easeOut(land(t, at(12)))), phX = PH.x - 1300 * easeIn(seg(t, at(13) - .3, at(13)));
  if (t < at(13)) phone(c, t, phX, phY);
  if (t >= at(13) - .3) browser(c, t, lerp(1200, PB.x, easeOut(seg(t, at(13) - .3, at(13)))));
  const pt = t < at(13) ? easeOut(seg(t, at(12, 3) - SLAM, at(12, 3))) : 1;
  jeff(c, jx, 1830, .66, { armR: lerp(0, -1.9, pt), prop: pt > .5 ? 'point' : null, head: .05 });
}
function sceneInbox(c, t) {   // bar 14
  fixBg(c); inbox(c, t);
  const sweep = seg(t, at(14, 1.5), at(14, 2.75));
  if (sweep > 0 && sweep < 1) { const y = IB.y + 230 + 300 * easeIO(sweep); magnifier(c, 260 + 360 * sweep, y, 90, null, null); }
  check(c, 760, 680, .9, t, at(14, 3));
  if (t >= at(14, 3) - SLAM) stampFit(c, 'CHECKED!', BLK, 150, SCX, 1000, -.06, .9, t, at(14, 3));
  const th = easeOutBack(seg(t, at(14, 3), at(14, 3.4)));
  jeff(c, 190, 1830, .66, { armR: lerp(-1.9, -2.5, th), prop: th > .6 ? 'thumb' : 'point', head: .05 });
}
function sceneLine(c, t) {   // bars 15-16: the protection line
  bgDots(c, BLUE, .1, .5);
  const [sx, sy] = shake(t, [[at(15), 14], [at(15, 3), 12]]);
  const beatPulse = t > at(16) ? 1 + .025 * Math.max(0, Math.cos((t - at(16)) * TAU / BEAT)) : 1;
  c.save(); c.translate(sx, sy);
  stampFit(c, "DON'T CLICK.", BLK, 150, SCX, 500, -.05, .82 * beatPulse, t, at(15));
  stampFit(c, 'GO TO THE APP', BLUE, 140, SCX, 730, .03, .78 * beatPulse, t, at(15, 3));
  stampFit(c, 'YOURSELF.', BLUE, 140, SCX, 900, -.03, .82 * beatPulse, t, at(15, 3.5));
  c.restore();
  const th = easeOutBack(seg(t, at(15, 2), at(15, 2.4))), nod = t > at(16) ? .05 * Math.sin((t - at(16)) * TAU / (2 * BEAT)) : 0;
  jeffUp(c, t, at(15, 2), SCX, { armR: lerp(0, -2.5, th), prop: th > .6 ? 'thumb' : null, head: nod }, .74);
  const d = seg(t, at(16, 4), at(17)); if (d > 0) rubberStamp(c, easeIn(d));
}
const STAMP_FACE = [480, 830];
function rubberStamp(c, u) {
  const s = lerp(.35, 1.25, u), y = lerp(-900, CY, u), [hw, hh] = STAMP_FACE;
  c.save(); c.translate(CX, y); c.scale(s, s);
  c.save(); c.globalAlpha = .35 * u; c.fillStyle = BLK; c.fillRect(-hw - 80, -hh - 50, 2 * hw + 160, 2 * hh + 100); c.restore();
  block(c, rect(-hw, -hh, 2 * hw, 2 * hh), BLUE, 1801, { kw: 10 });
  block(c, rect(-300, -hh - 150, 600, 160), BLK, 1802, { kw: 6 }); block(c, rect(-120, -hh - 430, 240, 300), YEL, 1803, { kw: 6 });
  c.restore();
}
function rubberStampFlat(c) { const [hw, hh] = STAMP_FACE; c.save(); c.translate(CX, CY); c.scale(1.25, 1.25); block(c, rect(-hw, -hh, 2 * hw, 2 * hh), BLUE, 1801, { kw: 10 }); c.restore(); }
function sceneSignoff(c, t) {
  paperBg(c);
  // the official logo: exact file, no texture, no recolour, no distortion; centred in the safe zone; held still
  const im = IMG.logo, [bx, by, bw, bh] = IMG.logoBox, lw = 780, lh = bh * lw / bw;
  c.drawImage(im, bx, by, bw, bh, SCX - lw / 2, SCY - lh / 2, lw, lh);
  const lift = seg(t, at(17), at(17) + .3);
  if (lift < 1) { c.save(); c.translate(0, -(H + 320) * easeIn(lift)); rubberStampFlat(c); c.restore(); }
}

// ================= assembly =================
function zoomThrough(c, t, t0, t1, rect0, under, inner) {   // a window grows from rect0 to the full frame; inner scene drawn through it
  const u = easeIO(seg(t, t0, t1)), [x0, y0, w0, h0] = rect0;
  const x = lerp(x0, 0, u), y = lerp(y0, 0, u), w = lerp(w0, W, u), h = lerp(h0, H, u), k = lerp(w0 / W, 1, u);
  under(c);
  const g = L1.getContext('2d'); resetT(g); g.globalAlpha = 1; inner(g);
  c.save(); c.beginPath(); c.rect(x, y, w, h); c.clip(); c.translate(x + w / 2, y + h / 2); c.scale(Math.max(k, w / W, h / H), Math.max(k, w / W, h / H)); c.drawImage(L1, -W / 2, -H / 2, W, H); c.restore();
  if (u < 1) key(c, rect(x, y, w, h), 8, 4001);
}
function drawScene(c, t) {
  resetT(c);
  if (t < at(4)) sceneBait(c, t);
  else if (t < at(4) + .45) zoomThrough(c, t, at(4), at(4) + .45, buttonRect(), g => sceneBait(g, at(4) - 1e-3), g => sceneSite(g, t));
  else if (t < at(9)) sceneSite(c, t);
  else if (t < at(10)) sceneRise(c, t);
  else if (t < at(11) - SLAM) scene10(c, t);
  else if (t < at(14)) sceneFix(c, t);
  else if (t < at(14) + .45) zoomThrough(c, t, at(14), at(14) + .45, [PB.x, PB.y + 130, PB.w, PB.h - 130], g => sceneFix(g, at(14) - 1e-3), g => sceneInbox(g, t));
  else if (t < at(15)) sceneInbox(c, t);
  else if (t < at(17)) sceneLine(c, t);
  else { sceneSignoff(c, t); return; }   // no print finish over the official logo
  captions(c, t);
  printFinish(c);
  if (SHOW_SAFE) { c.save(); c.strokeStyle = '#ff00ff'; c.lineWidth = 4; c.strokeRect(SAFE.x0, SAFE.y0, SAFE.x1 - SAFE.x0, SAFE.y1 - SAFE.y0); c.globalAlpha = .15; c.fillStyle = '#ff00ff'; c.fillRect(0, 0, W, 288); c.fillRect(0, 1440, W, 480); c.fillRect(918, 0, 162, H); c.restore(); }
}

// ================= runtime =================
const CV = document.getElementById('c'); CV.width = OUT_W; CV.height = OUT_H; const CTX = CV.getContext('2d');
function frame(i) { const t = Math.min(i / FPS, DUR - 1e-6); FILM_T = t; resetT(CTX); CTX.globalAlpha = 1; drawScene(CTX, t); resetT(CTX); }
window.__NFR = NFR; window.__FPS = FPS; window.__frame = i => { frame(i); return CV.toDataURL('image/png'); };
(async () => {
  await loadPrintKit();
  SP = await (await fetch('assets/explainer/scammer_parts.json')).json();
  await Promise.all([...Object.keys(SP.parts).map(k => loadImg('s_' + k, `assets/explainer/scammer_${k}.png`)), loadImg('logo', 'assets/official_logo.png'), loadImg('sp', 'assets/casefile/logo_screenprint.webp')]);
  IMG.logoBox = alphaBox(IMG.logo); IMG.spBox = alphaBox(IMG.sp);
  frame(+(Q.get('frame') || 0));
  window.__ready = true;
})().catch(e => { console.error(e); window.__error = String(e); });
