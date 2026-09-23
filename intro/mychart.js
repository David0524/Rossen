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
// format, clock, safe zone and shared helpers: vertkit.js
const DUR = at(17) + 2, NFR = Math.round(FPS * DUR);

// the caption band: short ALL-CAPS lines on black paper chips, top of the safe zone, one set per downbeat
const CAPS = [
  [at(0), 'GOT THIS EMAIL?'], [at(1), 'A FREE KIT?', 'NEW RESULTS?'], [at(2), 'HURRY!', 'ACT NOW!'], [at(3), null],
  [at(4), 'THE LINK OPENS', 'A FAKE SITE'], [at(5), 'IT LOOKS REAL.', "IT'S NOT."], [at(6), 'IT ASKS FOR', 'YOUR INFO'],
  [at(7), 'THEN THEY', 'REEL IT ALL IN'], [at(9), null],
  [at(10), "HERE'S HOW", 'TO STAY SAFE'], [at(11), "DON'T CLICK", 'THE LINK'], [at(12), 'OPEN THE MYCHART', 'APP YOURSELF'],
  [at(13), 'OR TYPE IN YOUR', "PROVIDER'S WEBSITE"], [at(14), 'CHECK IF THE', 'MESSAGE IS REAL'], [at(15), null],
];

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
  const VP = [lerp(80, -400, up), lerp(560, -400, up), lerp(800, W + 800, up), lerp(870, H + 800, up)];
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
  if (deep > 0) { dotScreen(c, polyPath(rect(-400, 1290, W + 800, 160)), [-400, 1290, W + 800, 160], { cell: 16, color: BLUE, density: (x, y) => deep * clamp01((y - 1290) / 150), angle: ANG[BLUE], seed: 3620 });
    c.save(); c.globalAlpha = deep; ink(c, rect(-400, 1440, W + 800, 1000), BLUE, 3621, { amp: 5 }); c.restore(); }
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
    const J = jeff(c, 230, lerp(3000, 1840, jin), .7, { armR: lerp(0, -2.2, raise), head: -.06 * raise });
    if (raise > 0) { const target = [BR.x + 470, BR.y + 50 + dr], R = lerp(40, 120, raise), cx = lerp(J.hand[0] + 120, target[0], raise), cy = lerp(J.hand[1] - 160, target[1], raise);
      magnifier(c, cx, cy, R, J.hand, raise > .6 ? () => { c.translate(cx, cy); c.scale(1.9, 1.9); c.translate(-cx, -cy + dr); urlBar(c); } : null); }
  }
  if (t >= at(5, 3) - SLAM && t < at(6)) stampFit(c, 'FAKE!', BLK, 170, 520, 900, -.1, 1, t, at(5, 3));
}

// ================= the loot, reeled in on the pier =================
function scenePier(c, t, o = {}) {
  if (o.fixBg) fixBg(c); else { bgDots(c, BLUE, .12, .45); water(c, 1300, 1000, 3701, -400, W + 400); }
  const knock = o.knock ?? 0;   // bar 10: the logo slams and knocks him off
  if (!o.noPier) pier(c, -400, 470, 1250);
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
  contentT(g1); sceneSite(g1, t); contentT(g2); scenePier(g2, t);
  c.save(); resetT(c); c.drawImage(L1, 0, off, W, H); c.drawImage(L2, 0, off - H, W, H); c.restore();
}

// ================= the fix =================
function fixBg(c) { bgDots(c, BLUE, .06, .3); }
function scene10(c, t) {   // HERE'S HOW TO STAY SAFE
  const k = easeIn(seg(t, at(10), at(10) + .55)), fall = easeIn(seg(t, at(10), at(10) + .9));
  scenePier(c, t, { knock: k, fall, fixBg: t >= at(10), noPier: t >= at(10) });
  const [sx, sy] = shake(t, [[at(10), 18]]);
  if (t >= at(10) && t < at(10) + .3) { c.save(); c.globalAlpha = 1 - seg(t, at(10), at(10) + .3); resetT(c); c.fillStyle = CHIP; c.fillRect(0, 0, W, H); c.restore(); }
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
  const d = seg(t, at(16, 4), at(17)); if (d > 0) screenSpace(c, () => rubberStamp(c, easeIn(d)));
}
function sceneSignoff(c, t) {
  paperBg(c);
  // the official logo: exact file, no texture, no recolour, no distortion; centred on the frame, inside the safe zone; held still
  const im = IMG.logo, [bx, by, bw, bh] = IMG.logoBox, lw = 720, lh = bh * lw / bw;
  c.drawImage(im, bx, by, bw, bh, CX - lw / 2, SCY - lh / 2, lw, lh);
  const lift = seg(t, at(17), at(17) + .3);
  if (lift < 1) { c.save(); c.translate(0, -(H + 320) * easeIn(lift)); rubberStampFlat(c); c.restore(); }
}

// ================= assembly =================
function drawScene(c, t) {
  contentT(c);
  if (t < at(4)) sceneBait(c, t);
  else if (t < at(4) + .45) zoomThrough(c, t, at(4), at(4) + .45, buttonRect(), g => sceneBait(g, at(4) - 1e-3), g => sceneSite(g, t));
  else if (t < at(9)) sceneSite(c, t);
  else if (t < at(10)) sceneRise(c, t);
  else if (t < at(11) - SLAM) scene10(c, t);
  else if (t < at(14)) sceneFix(c, t);
  else if (t < at(14) + .45) zoomThrough(c, t, at(14), at(14) + .45, [PB.x, PB.y + 130, PB.w, PB.h - 130], g => sceneFix(g, at(14) - 1e-3), g => sceneInbox(g, t));
  else if (t < at(15)) sceneInbox(c, t);
  else if (t < at(17)) sceneLine(c, t);
  else { resetT(c); sceneSignoff(c, t); return; }   // screen space; no print finish over the official logo
  captions(c, t);
  printFinish(c);
  if (SHOW_SAFE) { c.save(); resetT(c); c.strokeStyle = '#ff00ff'; c.lineWidth = 4; c.strokeRect(CX - 360, 381, 720, 968); c.globalAlpha = .15; c.fillStyle = '#ff00ff'; c.fillRect(0, 0, W, 288); c.fillRect(0, 1440, W, 480); c.fillRect(918, 0, 162, H); c.restore(); }
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
