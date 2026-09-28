'use strict';
/* WHAT WOULD YOU DO? #2: the fake virus pop-up. The episode's drawings (the recurring parts come from wwyd.js).
   tease     the laptop is already on the title card, on a calm page
   popup     (3 bars) 1: he's just browsing   2: the screen strobes (no text on screen), then on beat 2 the pop-up slams
             in and stops dead: from then on nothing flashes (one flash only, well under 3 a second)   3: the fake tech-support agent rises behind the laptop,
             headset on, rubbing his hands, visible to the viewer and not to the man. The last frame is the freeze-frame.
   reveal_A  THE TRAP (the CLOSE sting): the click installs fake "security" software, then a payment page; he rubs his hands
   reveal_C  WRONG: the number rings straight to his headset; then he's in the computer (a cursor that moves by itself)
             and the money flies to him
   reveal_B  RIGHT [signature]: the man clicks the pop-up's close box; the window collapses into it and sucks the agent
             in with it, headset last; the page is calm again
   stat      (outro, 2 bars) UP TO HALF OF TECH SUPPORT SCAMS START WITH A POP-UP, SOURCE: BBB, on a level card
   Everything is generic: no company, operating system or browser design, and the only number is 1-800-XXX-XXXX. The
   warning is drawn in the series palette (hazard yellow and black), not in any real warning's colours. Puppets move on twos. */
const twos = t => { const b = Math.floor(t / BEAT + 1e-6) * BEAT; return b + Math.floor((t - b) * FPS / 2 + 1e-6) * 2 / FPS; };
const bob = (t, a = 4, per = BEAT) => Math.abs(Math.sin(t * Math.PI / per)) * a;
const gentle = (t, t0) => t >= t0 ? 1 : lerp(1.05, 1, easeOut(land(t, t0)));

// ================= the fake tech-support agent (jointed; the headset is its own piece) =================
// p: { head, bob, rub 0..1 (hands together), sx, headset: {dx, dy, rot} (reference px), squash: [sx, sy] }
function tech(c, x, y, s, t, p = {}) {
  const M = PUP.tech, [fx, fy] = M.feet, sq = p.squash || [1, 1];
  c.save(); c.translate(x, y); c.rotate(p.tilt || 0); c.scale(s * (p.sx || 1) * sq[0], s * sq[1]); c.translate(-fx, -fy - (p.bob || 0));
  const img = (k, dx = 0, dy = 0) => { const m = M.parts[k]; c.drawImage(IMG['tech_' + k], m.x + dx, m.y + dy); };
  img('legL'); img('legR'); img('torso');
  const r = p.rub || 0, wig = r * 10 * Math.sin(t * 40);   // rubbing: the gloves come together and scrub
  img('handL', 38 * r + wig, -4 * r); img('handR', -40 * r - wig, 4 * r);
  const [hx, hy] = M.parts.head.pivot; c.save(); c.translate(hx, hy); c.rotate(p.head || 0); c.translate(-hx, -hy); img('head');
  const hs = p.headset || {}; c.save(); c.translate(hx + (hs.dx || 0), hy + (hs.dy || 0)); c.rotate(hs.rot || 0); c.translate(-hx, -hy); if (!hs.off) img('headset'); c.restore();
  c.restore(); c.restore();
}
function man(c, x, y, s, t, p = {}) { puppet(c, 'man', x, y, s, Object.assign({ head: .03 * Math.sin(t * 2.1), bob: bob(t, 3, 2 * BEAT) }, p)); }

// ================= the laptop, its pages, the pop-up =================
const LT = { x: 150, y: 640, w: 660, h: 440 };   // the screen at full size (content px)
function laptop(c, x, y, s, screen) {   // x: centre, y: top of the screen; screen(sx, sy, sw, sh) draws inside
  const w = LT.w * s, h = LT.h * s, x0 = x - w / 2;
  shadowRect(c, x0, y, w, h + 60 * s);
  block(c, rrPts(x0, y, w, h, 24 * s, 5), BLK, 9401, { kw: 5 });
  const ix = x0 + 20 * s, iy = y + 20 * s, iw = w - 40 * s, ih = h - 40 * s;
  c.save(); c.beginPath(); c.rect(ix, iy, iw, ih); c.clip(); c.fillStyle = CHIP; c.fillRect(ix, iy, iw, ih); screen(ix, iy, iw, ih); c.restore();
  block(c, [[x0 - 40 * s, y + h], [x0 + w + 40 * s, y + h], [x0 + w + 10 * s, y + h + 50 * s], [x0 - 10 * s, y + h + 50 * s]], BLUE, 9402, { kw: 5 });   // the keyboard deck
  ink(c, rect(x - 60 * s, y + h + 14 * s, 120 * s, 16 * s), BLK, 9403, { reg: false });   // the trackpad slot
  return { ix, iy, iw, ih };
}
function calmPage(c, ix, iy, iw, ih, scroll = 0) {   // a generic page: a header bar and blank blocks, no words
  c.fillStyle = BLUE; c.fillRect(ix, iy, iw, ih * .12);
  for (let k = 0; k < 6; k++) { const yy = iy + ih * .18 + k * ih * .2 - (scroll % (ih * .2)); if (yy > iy + ih) continue;
    c.fillStyle = '#e4dccb'; c.fillRect(ix + iw * .06, yy, iw * .32, ih * .15); c.fillStyle = '#d8cfbb'; c.fillRect(ix + iw * .42, yy + ih * .02, iw * .5, ih * .03); c.fillRect(ix + iw * .42, yy + ih * .08, iw * .38, ih * .03); }
}
function hazard(c, x, y, w, h, off = 0) {   // black and yellow hazard stripes
  c.save(); c.beginPath(); c.rect(x, y, w, h); c.clip(); c.fillStyle = YEL; c.fillRect(x, y, w, h); c.fillStyle = BLK;
  for (let k = -2; k < w / 40 + 2; k++) { const x1 = x + k * 40 + off; c.beginPath(); c.moveTo(x1, y + h); c.lineTo(x1 + 20, y + h); c.lineTo(x1 + 20 + h, y); c.lineTo(x1 + h, y); c.closePath(); c.fill(); }
  c.restore();
}
function warnSign(c, x, y, r) { block(c, [[x, y - r], [x + r * 1.1, y + r * .8], [x - r * 1.1, y + r * .8]], YEL, 9410, { kw: 5 }); fitText(c, '!', x, y + r * .25, r * 1.1, 'Stamp', BLK, r); }
function popupWin(c, ix, iy, iw, ih, k = 1, pressed = false) {   // the fake warning: opaque, level, every word static
  const x = ix + iw * .04, y = iy + ih * .05, w = iw * .92, h = ih * .9, cx = x + w / 2, cy = y + h / 2;
  c.save(); c.translate(cx, cy); c.scale(k, k); c.translate(-cx, -cy);
  c.save(); c.globalAlpha = .35; c.fillStyle = BLK; c.fillRect(x + 8, y + 10, w, h); c.restore();
  c.fillStyle = CHIP; c.fillRect(x, y, w, h); hazard(c, x, y, w, h * .1); c.strokeStyle = BLK; c.lineWidth = 5; c.strokeRect(x, y, w, h);
  const xb = closeBox(x, y, w, h); c.fillStyle = BLK; c.fillRect(xb.x - xb.r, xb.y - xb.r, xb.r * 2, xb.r * 2);
  c.save(); c.strokeStyle = YEL; c.lineWidth = 4; c.beginPath(); c.moveTo(xb.x - xb.r * .5, xb.y - xb.r * .5); c.lineTo(xb.x + xb.r * .5, xb.y + xb.r * .5); c.moveTo(xb.x + xb.r * .5, xb.y - xb.r * .5); c.lineTo(xb.x - xb.r * .5, xb.y + xb.r * .5); c.stroke(); c.restore();
  const P = EP.popup, s = w / 580;
  warnSign(c, x + 70 * s, y + h * .27, 38 * s);
  fitText(c, P[0], x + w / 2 + 40 * s, y + h * .27, 58 * s, 'Stamp', BLK, w - 170 * s);
  fitText(c, P[1], x + w / 2, y + h * .45, 34 * s, 'Stamp', BLK, w - 60 * s);
  fitText(c, P[2], x + w / 2, y + h * .57, 40 * s, 'Stamp', BLUE, w - 60 * s);
  fitText(c, P[3], x + w / 2, y + h * .68, 30 * s, 'Stamp', BLK, w - 60 * s);
  const bk = pressed ? .94 : 1, by = y + h * .85; c.save(); c.translate(x + w / 2, by); c.scale(bk, bk);
  block(c, rrPts(-170 * s, -30 * s, 340 * s, 60 * s, 30 * s, 5), BLK, 9420, { kw: 3 }); fitText(c, EP.popupButton, 0, 3 * s, 32 * s, 'Stamp', YEL, 300 * s); c.restore();
  c.restore();
  return { x, y, w, h, xb, btn: [x + w / 2, by] };
}
function closeBox(x, y, w, h) { return { x: x + w - h * .05 - 6, y: y + h * .05, r: h * .045 }; }
function cursor(c, x, y, s = .7) { cursorArrow(c, x, y, s); }
function twinkle(c, x, y, t, t0, r = 60) { const u = seg(t, t0, t0 + .4); if (u <= 0 || u >= 1) return; c.save(); c.globalAlpha = 1 - u; c.strokeStyle = YEL; c.lineWidth = 9; c.lineCap = 'round';
  for (let k = 0; k < 8; k++) { const a = k / 8 * TAU, r1 = r * .5 + r * u, r2 = r1 + 26; c.beginPath(); c.moveTo(x + Math.cos(a) * r1, y + Math.sin(a) * r1); c.lineTo(x + Math.cos(a) * r2, y + Math.sin(a) * r2); c.stroke(); } c.restore(); }

// ================= the title card and the setup =================
SCENES.tease = (c, t, S) => { laptop(c, SCX, 800, .72, (ix, iy, iw, ih) => calmPage(c, ix, iy, iw, ih, twos(t) * 20)); };
SCENES.popup = (c, t, S) => {
  sceneBg(c);
  const tt = twos(t), b2 = S.at(2), pop_ = S.at(2, 2), strobeEnd = pop_ - SLAM;
  const rise = easeOutBack(land(tt, S.at(3)));   // the agent rises behind the laptop on bar 3
  if (t >= S.at(3) - SLAM) tech(c, 700, lerp(1200, 900, rise), .62, tt, { sx: -1, head: .06 * Math.sin(tt * 4), bob: bob(tt, 3), rub: t >= S.at(3, 3) - SLAM ? .6 + .4 * Math.sin(tt * 8) : 0 });
  laptop(c, SCX, LT.y, 1, (ix, iy, iw, ih) => {
    calmPage(c, ix, iy, iw, ih, t < b2 ? twos(t) * 26 : twos(b2) * 26);
    if (t >= b2 && t < strobeEnd) { const off = (t - b2) * 260; c.fillStyle = BLK; c.fillRect(ix, iy, iw, ih); hazard(c, ix, iy, iw, ih * .18, off); hazard(c, ix, iy + ih * .82, iw, ih * .18, -off); }   // the takeover: one hard flash to black, hazard bands crawling (motion, not flicker; no text on screen)
    if (t >= strobeEnd) popupWin(c, ix, iy, iw, ih, t >= pop_ ? 1 : lerp(1.25, 1, easeIn(land(t, pop_))));   // it slams in and stops dead
  });
  const shock = t >= pop_ - SLAM ? easeOutBack(seg(tt, pop_ - SLAM, pop_ + .2)) : 0;
  man(c, 130, 1850, .74, tt, { head: -.14 * shock + .03 * Math.sin(tt * 2.1) + (t >= S.at(3) ? .05 * Math.sin(tt * 9) : 0), bob: bob(tt, 3, 2 * BEAT) + 20 * shock * (1 - seg(tt, pop_, pop_ + .4)) });
};

// ================= the reveals =================
const RV = { x: 480, y: 660, s: .62 };   // the small laptop in the reveals
SCENES.reveal_A = (c, t, S) => {   // THE TRAP: the fake scan installs fake software, then asks for money
  const tt = twos(t), click = S.at(1, 2), rub = t >= S.at(1, 3) - SLAM ? .6 + .4 * Math.sin(tt * 8) : 0;
  tech(c, 790, 1110, .46, tt, { sx: -1, head: .06 * Math.sin(tt * 4), bob: bob(tt, 3), rub });   // feet well above the lower captions
  const L = laptop(c, RV.x, RV.y, RV.s, (ix, iy, iw, ih) => {
    if (t < click + .15) { calmPage(c, ix, iy, iw, ih, 0); const P = popupWin(c, ix, iy, iw, ih, 1, t >= click && t < click + .15);
      const u = easeIO(seg(t, S.at(1, 1) + .1, click)); cursor(c, lerp(ix + iw * .85, P.btn[0] + 10, u), lerp(iy + ih * .95, P.btn[1] - 6, u), .6); }
    else if (t < S.at(2)) {   // the "download": a progress bar that fills, and a box being installed
      c.fillStyle = CHIP; c.fillRect(ix, iy, iw, ih); const u = clamp01((t - click - .15) / (S.at(2) - click - .3));
      block(c, [[ix + iw / 2 - 30, iy + ih * .2], [ix + iw / 2 + 30, iy + ih * .2], [ix + iw / 2 + 30, iy + ih * .38], [ix + iw / 2 + 60, iy + ih * .38], [ix + iw / 2, iy + ih * .5], [ix + iw / 2 - 60, iy + ih * .38], [ix + iw / 2 - 30, iy + ih * .38]], BLUE, 9450, { kw: 4 });
      c.fillStyle = BLK; c.fillRect(ix + iw * .15, iy + ih * .64, iw * .7, ih * .12); c.fillStyle = YEL; c.fillRect(ix + iw * .15 + 5, iy + ih * .64 + 5, (iw * .7 - 10) * u, ih * .12 - 10); }
    else {   // the payment page: a card and blank fields, and a big $
      c.fillStyle = CHIP; c.fillRect(ix, iy, iw, ih); hazard(c, ix, iy, iw, ih * .1);
      fitText(c, '$', ix + iw * .22, iy + ih * .52, ih * .5, 'Stamp', BLK, iw * .3);
      block(c, rrPts(ix + iw * .42, iy + ih * .22, iw * .46, ih * .3, 12, 4), BLUE, 9451, { kw: 4 }); c.fillStyle = YEL; c.fillRect(ix + iw * .47, iy + ih * .3, iw * .08, ih * .07);
      for (let k = 0; k < 2; k++) { c.strokeStyle = BLK; c.lineWidth = 4; c.strokeRect(ix + iw * .42, iy + ih * (.6 + k * .15), iw * .46, ih * .1); } }
  });
};
function bigPhone(c, x, y, s, t, t0) {   // his phone, dialing (no numbers on screen, just a handset)
  c.save(); c.translate(x, y); c.scale(s, s); shadowRect(c, -90, -160, 180, 320); block(c, rrPts(-90, -160, 180, 320, 26, 5), BLK, 9460, { kw: 5 });
  block(c, rrPts(-74, -130, 148, 250, 12, 4), CHIP, 9461, { kw: 3 }); block(c, ellPts(0, -10, 44, 44, 0, 28), BLUE, 9462, { kw: 4 });
  c.save(); c.strokeStyle = CHIP; c.lineWidth = 11; c.lineCap = 'round'; c.beginPath(); c.arc(0, -4, 20, Math.PI * 1.1, Math.PI * 1.9); c.stroke(); c.restore(); c.restore();
  for (let k = 0; k < 3; k++) { const u = ((t - t0) * 1.6 + k / 3) % 1; if (t < t0) break; c.save(); c.globalAlpha = (1 - u) * .8; c.strokeStyle = YEL; c.lineWidth = 8; c.beginPath(); c.arc(x + 100 * s, y - 60 * s, 30 + 60 * u, -.8, .8); c.stroke(); c.restore(); }
}
function cashBill(c, x, y, rot) { c.save(); c.translate(x, y); c.rotate(rot); block(c, rect(-60, -30, 120, 60), YEL, 9470, { kw: 4 }); block(c, ellPts(0, 0, 16, 16, 0, 16), BLUE, 9471, { kw: 3 }); c.restore(); }
SCENES.reveal_C = (c, t, S) => {   // WRONG: the number rings straight to his headset; then remote access, and the money
  const tt = twos(t), pick = S.at(1, 3);
  const glow = t >= pick ? 1 : 0;
  tech(c, 760, 1110, .5, tt, { sx: -1, head: .06 * Math.sin(tt * 4) + (glow ? .05 : 0), bob: bob(tt, 3), rub: t >= S.at(2, 3) ? .7 + .3 * Math.sin(tt * 8) : 0 });
  if (glow && t < S.at(2)) { const [mx, my] = [760 - 150, 1110 - 727 * .5 + 270 * .5]; for (let k = 0; k < 2; k++) { const u = ((t - pick) * 1.8 + k / 2) % 1; c.save(); c.globalAlpha = (1 - u) * .8; c.strokeStyle = YEL; c.lineWidth = 8; c.beginPath(); c.arc(mx, my, 20 + 50 * u, 0, TAU); c.stroke(); c.restore(); } }
  if (t < S.at(2)) {
    bigPhone(c, 280, 880, 1, tt, S.at(1, 2));
    if (t >= S.at(1, 2)) { const u = easeOut(seg(t, S.at(1, 2), pick)); c.save(); c.setLineDash([16, 14]); c.strokeStyle = BLK; c.lineWidth = 6; c.beginPath(); c.moveTo(390, 820); c.lineTo(lerp(390, 600, u), lerp(820, 860, u)); c.stroke(); c.restore(); }
  } else {   // bar 2: he's in the computer: the cursor moves by itself; then the money flies to him
    laptop(c, 370, RV.y, .56, (ix, iy, iw, ih) => { calmPage(c, ix, iy, iw, ih, 0);
      const a = (t - S.at(2)) * 3.2; const cx = ix + iw * (.5 + .3 * Math.cos(a)), cy = iy + ih * (.5 + .3 * Math.sin(a * 1.3));
      c.save(); c.setLineDash([8, 10]); c.strokeStyle = BLUE; c.lineWidth = 4; c.beginPath(); for (let k = 0; k < 18; k++) { const b = a - k * .08; const px = ix + iw * (.5 + .3 * Math.cos(b)), py = iy + ih * (.5 + .3 * Math.sin(b * 1.3)); k ? c.lineTo(px, py) : c.moveTo(px, py); } c.stroke(); c.restore();
      cursor(c, cx, cy, .55); });
    for (let k = 0; k < 3; k++) { const t0 = S.at(2, 3) + k * S16, u = easeIn(seg(t, t0 - .3, t0)); if (u <= 0) continue; cashBill(c, lerp(470, 700, u), lerp(800, 960 + k * 20, u) - 120 * Math.sin(u * Math.PI), -.3 + u * .6); }
  }
};
SCENES.reveal_B = (c, t, S) => {   // RIGHT: he closes it, and the window sucks the agent in with it
  const tt = twos(t), click = S.at(1, 2), done = S.at(1, 3), u = easeIn(seg(t, click, done));
  let P = null; const L = { x: RV.x, y: RV.y, s: .66 };
  const w = LT.w * L.s, x0 = L.x - w / 2, ix = x0 + 20 * L.s, iy = L.y + 20 * L.s, iw = w - 40 * L.s, ih = LT.h * L.s - 40 * L.s;
  const xb = closeBox(ix + iw * .04, iy + ih * .05, iw * .92, ih * .9);   // the close box, on the laptop screen
  if (t < done) {   // the agent behind the laptop: pulled in toward the close box, headset last
    const px = lerp(710, xb.x, u), py = lerp(1010, xb.y + 30, u), sc = lerp(.42, .02, u), sp = u * 5;
    tech(c, px, py, sc, tt, { sx: -1, tilt: sp, squash: [1 - .5 * u, 1 + .6 * u], head: .06 * Math.sin(tt * 4), headset: u > 0 ? { dx: -120 * u, dy: -260 * u, rot: -1.5 * u } : {}, bob: bob(tt, 3) });
  }
  laptop(c, L.x, L.y, L.s, (ix2, iy2, iw2, ih2) => {
    calmPage(c, ix2, iy2, iw2, ih2, 0);
    if (t < done) { const k = 1 - u; if (k > .01) { c.save(); c.translate(xb.x, xb.y); c.scale(k, k); c.translate(-xb.x, -xb.y); P = popupWin(c, ix2, iy2, iw2, ih2, 1); c.restore(); } }
    if (t < click + .2) { const m = easeIO(seg(t, S.at(1, 1) + .1, click)); cursor(c, lerp(ix2 + iw2 * .4, xb.x - 4, m), lerp(iy2 + ih2 * .8, xb.y - 4, m), .6); }
  });
  twinkle(c, xb.x, xb.y, t, done, 70); twinkle(c, L.x, L.y + 150, t, S.at(2), 110);
  if (t >= S.at(2) - SLAM) { const pop_ = easeOutBack(land(tt, S.at(2))); man(c, 800, lerp(2500, 1860, pop_), .56, tt, { sx: -1, head: .08 * Math.sin(tt * 3) }); }   // relieved
};

// ================= the stat (outro) =================
function levelCard(c, s, x, y, size, bg, fg, t, t0, maxW = 760) {   // level, lands gently, then holds completely still
  if (t < t0 - SLAM) return; c.font = `${size}px Stamp`; const w = Math.min(c.measureText(s).width, maxW) + 60, h = size * 1.34, k = gentle(t, t0);
  c.save(); c.translate(x, y); c.scale(k, k); c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fillRect(-w / 2 + 8, -h / 2 + 10, w, h); c.restore();
  c.fillStyle = bg; c.fillRect(-w / 2, -h / 2, w, h); fitText(c, s, 0, size * .06, size, 'Stamp', fg, maxW); c.restore();
}
SCENES.stat = (c, t, S) => {
  bgDots(c, BLUE, .1, .5);
  const st = EP.stat, t1 = S.at(1), t2 = S.at(1, 2), t3 = S.at(1, 3);
  levelCard(c, st.big, SCX, 470, 110, YEL, BLK, t, t1);
  if (t >= t1 - SLAM) { const k = gentle(t, t1), cx = SCX, cy = 740, r = 120; c.save(); c.translate(cx, cy); c.scale(k, k);   // half a pie
    c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.beginPath(); c.arc(8, 10, r, 0, TAU); c.fill(); c.restore();
    c.fillStyle = CHIP; c.beginPath(); c.arc(0, 0, r, 0, TAU); c.fill(); c.fillStyle = BLUE; c.beginPath(); c.moveTo(0, 0); c.arc(0, 0, r, -Math.PI / 2, Math.PI / 2); c.closePath(); c.fill();
    c.strokeStyle = BLK; c.lineWidth = 7; c.beginPath(); c.arc(0, 0, r, 0, TAU); c.stroke(); c.beginPath(); c.moveTo(0, -r); c.lineTo(0, r); c.stroke(); c.restore(); }
  st.lines.forEach((s, i) => levelCard(c, s, SCX, 960 + i * 104, 62, i ? BLUE : BLK, CHIP, t, t2));
  levelCard(c, st.source, SCX, 1190, 34, BLK, CHIP, t, t3, 400);
  const th = easeOutBack(seg(t, S.at(1, 2), S.at(1, 2.4)));
  jeff(c, 120, 1850, .5, { armR: lerp(-2.25, -2.5, th), prop: th > .6 ? 'thumb' : 'point', head: .05 * Math.sin((t - S.t0) * TAU / (2 * BEAT)) });
};
