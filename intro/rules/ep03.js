'use strict';
/* JEFF'S RULES #3: CHECK THE SELLER. The episode's middle scenes (recurring parts: rules.js; phone: rules/props.js).
   setup (3 bars)  1: a huge deal on headphones on his phone; he taps BUY on 3
                   2: the box drops on 1, pops open on 2, and out come the lopsided fakes, labelled HEDPHONES, on 3
                   3: the listing is back on 1; on 2 a blue glove yanks it aside like a curtain [signature 1], and there
                      he is: the knockoff seller, who throws his coat open on 3 (the running gag) and flaps it on 4
   why   (2 bars)  1: one big storefront   2: Jeff yanks the cord, the shutter rolls up [signature 2] on a street of
                   little stalls: friendly sellers, and one shady one, who flashes his coat on 3
   how   (3 bars)  1: the product page, zoomed in; SOLD BY lights up on 2, SHIPPED BY on 3 (the page is the only text)
                   2: the ranking builds, one rung per beat: THE BRAND, THE STORE ITSELF, A SELLER YOU DON'T KNOW
                   3: it holds; the knockoff seller pops up below the risky end and flashes his coat
   Everything is generic: no store, marketplace or brand names or logos, and the knockoffs parody nothing real.
   Puppets: the everyday man from the jury-duty explainer (assets/officer/man_*), the knockoff seller cut from the
   episode's reference (assets/rules/ep03/knock_*, tools/cut_knockoff.py), Jeff (printkit.js). Puppets move on twos. */

// ================= puppets =================
const PUP = {};
window.EP_ASSETS = async () => {
  makeCream();   // the approved cream board, for the product-page close-up
  for (const [name, dir] of [['man', 'assets/officer/'], ['knock', 'assets/rules/ep03/']]) {
    PUP[name] = await (await fetch(`${dir}${name}_parts.json`)).json();
    await Promise.all(Object.keys(PUP[name].parts).map(k => loadImg(name + '_' + k, `${dir}${name}_${k}.png`)));
  }
};
const bobOf = (t, a = 4, per = BEAT) => Math.abs(Math.sin(t * Math.PI / per)) * a;
function manP(c, x, y, s, t, p = {}) {   // the shopper (the same puppet and pose set as the jury-duty explainer)
  const M = PUP.man, head = p.head ?? .03 * Math.sin(t * 2.1), bob = p.bob ?? bobOf(t, 3, 2 * BEAT);
  c.save(); c.translate(x, y); c.scale(s * (p.sx || 1), s); c.translate(-M.feet[0], -M.feet[1] - bob);
  const part = (k, a = 0) => { const m = M.parts[k], [px, py] = m.pivot; c.save(); c.translate(px, py); c.rotate(a); c.translate(-px, -py); c.drawImage(IMG['man_' + k], m.x, m.y); c.restore(); };
  part('legL'); part('legR'); part('torso'); part('head', head); part('arm', p.arm || 0); c.restore();
}
// the knockoff seller. open 0..1: the coat flaps swing about their hinges on the centre strip (0 = clutched shut)
function knock(c, x, y, s, t, p = {}) {
  const M = PUP.knock, [HL, HR] = M.hinge, open = p.open ?? 1, fs = lerp(.1, 1, open);
  const head = p.head ?? .05 * Math.sin(t * 3), bob = p.bob ?? bobOf(t, 4);
  c.save(); c.translate(x, y); c.rotate(p.tilt || 0); c.scale(s * (p.sx || 1), s); c.translate(-M.feet[0], -M.feet[1] - bob);
  const img = (k, dx = 0, dy = 0) => { const m = M.parts[k]; c.drawImage(IMG['knock_' + k], m.x + dx, m.y + dy); };
  const piv = (k, a, fn) => { const [px, py] = M.parts[k].pivot; c.save(); c.translate(px, py); c.rotate(a); c.translate(-px, -py); fn(); c.restore(); };
  piv('legL', p.legL || 0, () => img('legL')); piv('legR', p.legR || 0, () => img('legR'));
  block(c, [[712, 430], [958, 430], [990, M.hem], [682, M.hem]], BLK, 9601, { kw: 0, key: false }); key(c, [[712, 430], [958, 430], [990, M.hem], [682, M.hem]], 6, 9602, true, YEL);   // the coat's back, seen when it is clutched shut
  img('centre');
  for (const [k, hx, sd] of [['flapL', HL, -1], ['flapR', HR, 1]]) { c.save(); c.translate(hx, 0); c.scale(fs, 1); c.translate(-hx, 0); img(k); c.restore(); }
  for (const [k, hx] of [['handL', HL], ['handR', HR]]) { const m = M.parts[k], [px] = m.pivot; img(k, (hx + (px - hx) * fs) - px, 0); }   // each hand rides its flap's outer edge
  piv('head', head, () => img('head'));
  c.restore();
}
const flashOpen = (t, t0) => t < t0 - SLAM ? 0 : t < t0 ? easeIn(land(t, t0)) : 1 + .08 * Math.exp(-(t - t0) * 9) * Math.sin((t - t0) * 30);   // throws the coat open, landing on t0
const flapWiggle = (t, t0) => t < t0 ? 1 : 1 - .3 * Math.sin(Math.PI * clamp01((t - t0) / (E8))) ;   // a quick flap on t0

// ================= props =================
function headphones(c, x, y, s, fake = false) {   // generic headphones; the fakes are lopsided, with one cup too big
  c.save(); c.translate(x, y); c.scale(s, s); if (fake) c.rotate(-.12);
  c.save(); c.lineCap = 'round'; c.strokeStyle = BLK; c.lineWidth = 34; c.beginPath();
  if (fake) { c.moveTo(-118, 30); c.quadraticCurveTo(-60, -170, 128, -40); } else { c.moveTo(-120, 30); c.quadraticCurveTo(0, -210, 120, 30); }
  c.stroke(); c.strokeStyle = YEL; c.lineWidth = 14; c.stroke(); c.restore();
  const cup = (cx, cy, rx, ry, seed) => { block(c, ellPts(cx, cy, rx, ry, 0, 30), BLK, seed, { kw: 5 }); block(c, ellPts(cx + (cx < 0 ? 10 : -10), cy, rx * .62, ry * .7, 0, 26), YEL, seed + 1, { kw: 3 }); };
  if (fake) { cup(-122, 62, 50, 70, 9701); cup(140, 30, 78, 100, 9703); } else { cup(-120, 60, 58, 82, 9701); cup(120, 60, 58, 82, 9703); }
  c.restore();
}
function saleBurst(c, x, y, r, label, t, t0, seed = 9710) {   // the discount sticker: a yellow burst, level type
  if (t < t0 - SLAM) return; const k = t >= t0 ? 1 : lerp(1.05, 1, easeOut(land(t, t0))); const P = [];
  for (let i = 0; i < 32; i++) { const a = -Math.PI / 2 + i * Math.PI / 16, rr = i % 2 ? r * .84 : r; P.push([x + Math.cos(a) * rr, y + Math.sin(a) * rr]); }
  c.save(); c.translate(x, y); c.scale(k, k); c.translate(-x, -y);
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fill(polyPath(P.map(([a, b]) => [a + 8, b + 10]))); c.restore();
  block(c, P, YEL, seed, { kw: 6 }); const [a, b] = label.split(' ');
  fitText(c, a, x, y - r * .16, r * .58, 'Stamp', BLK, r * 1.4); fitText(c, b || '', x, y + r * .36, r * .36, 'Stamp', BLK, r * 1.2);
  c.restore();
}
const LIST = { x: 110, y: 600, w: 560, h: 800 };
function listingPhone(c, t, tBuy, dy = 0) {   // his phone, showing the deal: headphones, the sticker, BUY NOW
  const { x, y, w, h } = LIST; c.save(); c.translate(0, dy);
  shadowRect(c, x, y, w, h); block(c, rrPts(x, y, w, h, 60, 6), BLK, 9720, { kw: 6 });
  block(c, rrPts(x + 18, y + 48, w - 36, h - 72, 22, 4), CHIP, 9721, { kw: 3 });
  headphones(c, x + w / 2, y + 330, 1.25);
  saleBurst(c, x + w - 120, y + 170, 108, EP.discount, 1e9, 0);
  const pr = t >= tBuy && t < tBuy + .18 ? .94 : 1, bx = x + w / 2, by = y + h - 150;
  c.save(); c.translate(bx, by); c.scale(pr, pr); block(c, rrPts(-190, -55, 380, 110, 55, 6), BLUE, 9722, { kw: 6 }); fitText(c, 'BUY NOW', 0, 6, 60, 'Stamp', CHIP, 320); c.restore();
  const u = seg(t, tBuy, tBuy + .4); if (u > 0 && u < 1) { c.save(); c.globalAlpha = 1 - u; c.strokeStyle = BLK; c.lineWidth = 8;   // the tap: a ring pulsing OUTSIDE the button, never over its words
    c.beginPath(); c.ellipse(bx, by, 215 + 50 * easeOut(u), 80 + 40 * easeOut(u), 0, 0, TAU); c.stroke(); c.restore(); }
  c.restore();
}
function box(c, x, y, open, t) {   // a plain shipping box (front view), flaps popping open; tape in yellow
  const w = 440, h = 300, x0 = x - w / 2, y0 = y - h;
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fillRect(x0 + 16, y0 + 20, w, h); c.restore();
  if (open > 0) { const th = lerp(0, 2.2, easeOutBack(open));
    for (const sd of [-1, 1]) { const hx = sd < 0 ? x0 : x0 + w, L = w / 2 - 6, dx = -sd * Math.cos(th) * L, dy = -Math.sin(th) * L * .7;
      block(c, [[hx, y0], [hx + dx, y0 + dy], [hx + dx * .96 + sd * 8, y0 + dy - 26], [hx + sd * 8, y0 - 26]], CREAM, 9730 + sd, { kw: 5 }); }
    block(c, [[x0 + 8, y0 - 26], [x0 + w - 8, y0 - 26], [x0 + w, y0], [x0, y0]], BLK, 9733, { kw: 4 }); }
  else { block(c, [[x0, y0], [x0 + w, y0], [x0 + w - 8, y0 - 26], [x0 + 8, y0 - 26]], CREAM, 9734, { kw: 5 }); ink(c, rect(x - 34, y0 - 26, 68, 26), YEL, 9735, { reg: false }); }
  block(c, rect(x0, y0, w, h), CREAM, 9736, { kw: 6 });
  ink(c, rect(x - 34, y0, 68, 110), YEL, 9737, { reg: false }); key(c, rect(x - 34, y0, 68, 110), 3, 9738);
  for (let k = 0; k < 3; k++) ink(c, rect(x0 + 40, y0 + h - 90 + k * 22, 120 - k * 30, 9), BLK, 9740 + k, { reg: false });   // a shipping label's lines (no words)
}
function tag(c, x, y, s) {   // the fakes' label, hanging from a string: opaque, level
  c.save(); c.strokeStyle = BLK; c.lineWidth = 4; c.beginPath(); c.moveTo(x - 20, y - 60); c.lineTo(x, y - 24); c.stroke(); c.restore();
  const w = 290, h = 72; c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fillRect(x - w / 2 + 8, y - 24 + 10, w, h); c.restore();
  block(c, [[x - w / 2 + 26, y - 24], [x + w / 2, y - 24], [x + w / 2, y + 48], [x - w / 2 + 26, y + 48], [x - w / 2, y + 12]], CHIP, 9750, { kw: 5 });
  fitText(c, s, x + 12, y + 16, 46, 'Stamp', BLK, w - 60);
}
function listingCard(c) {   // the listing, full size: the same page as on his phone (for the curtain)
  const x = 110, y = 590, w = 740, h = 850;
  shadowRect(c, x, y, w, h); block(c, rect(x, y, w, h), CHIP, 9760, { kw: 6 }); ink(c, rect(x, y, w, 70), BLUE, 9761, { reg: false });
  for (let k = 0; k < 3; k++) block(c, ellPts(x + 42 + k * 34, y + 35, 10, 10, 0, 12), CHIP, 9762 + k, { kw: 0, key: false });
  headphones(c, x + w / 2 - 40, y + 400, 1.55); saleBurst(c, x + w - 140, y + 210, 118, EP.discount, 1e9, 0);
  block(c, rrPts(x + w / 2 - 210, y + h - 170, 420, 110, 55, 6), BLUE, 9765, { kw: 6 }); fitText(c, 'BUY NOW', x + w / 2, y + h - 114, 64, 'Stamp', CHIP, 340);
  return [x, y, w, h];
}

// ================= setup =================
SCENES.setup = (c, t, S) => {
  sceneBg(c);
  const tt = onTwos(t), b2 = S.at(2), b3 = S.at(3);
  if (t < b3) {
    const out = easeIn(seg(t, b2 - E8, b2));   // the phone drops away as the box drops in
    if (out < 1) listingPhone(c, t, S.at(1, 3), 900 * out);
    if (t >= b2 - E8) {
      const land_ = easeIn(seg(t, b2 - E8, b2)), bx = 390, by = lerp(-200, 1380, land_);
      const op = seg(t, S.at(2, 2) - SLAM, S.at(2, 2)); box(c, bx, by, op, t);
      const rise = easeOutBack(seg(tt, S.at(2, 3) - SLAM, S.at(2, 3) + .12));
      if (rise > 0) { headphones(c, bx, lerp(1180, 900, rise), 1.1, true); if (rise >= .98) tag(c, bx + 120, 1070, EP.fakeLabel); }
    }
    const confused = t >= S.at(2, 3) ? -.12 : 0;
    manP(c, 790, 1700, .55, tt, { head: confused + .03 * Math.sin(tt * 2.1) });
  } else {   // bar 3: the listing is back; a glove yanks it aside like a curtain; behind it, the knockoff seller
    const pull = easeIO(seg(t, S.at(3, 2) - SLAM, S.at(3, 2) + .4)), op = flashOpen(tt, S.at(3, 3)) * flapWiggle(tt, S.at(3, 4));
    knock(c, 480, 1470, .95, tt, { open: op });
    {   // the listing stays gathered at the side like a drawn curtain
      const [x, y, w, h] = [110, 590, 740, 850], sx = lerp(1, .07, pull);
      c.save(); c.translate(x, 0); c.scale(sx, 1); c.translate(-x, 0); listingCard(c);
      for (let k = 0; k < 9; k++) { c.save(); c.globalAlpha = .22 * pull; c.fillStyle = BLK; c.fillRect(x + (k + .5) * w / 9, y, w / 18, h); c.restore(); }   // the folds gather
      c.restore();
      if (t >= S.at(3, 2) - .3) { const hx = x + w * sx, m = PUP.knock.parts.handR; c.drawImage(IMG.knock_handR, hx - 30, y + h / 2 - 50, m.w * .9, m.h * .9); }   // his glove, at the pulled edge
    }
  }
};

// ================= why: a big site is really a street of sellers =================
const SHOP = { x: 120, y: 690, w: 720, h: 700 };
function stall(c, x, y, k, shady, tt, t, tFlash) {   // one little seller's stall
  const w = 210, h = 250, cols = shady ? [BLK, BLK] : [[BLUE, CHIP], [YEL, CHIP], [BLUE, YEL]][k % 3];
  block(c, rect(x - w / 2, y, w, h), shady ? '#3a3638' : CREAM, 9800 + k, { kw: 5 });
  for (let i = 0; i < 5; i++) ink(c, rect(x - w / 2 + i * w / 5, y - 8, w / 5, 46), i % 2 ? cols[1] : cols[0], 9810 + k * 7 + i, { reg: false });
  key(c, rect(x - w / 2, y - 8, w, 46), 4, 9830 + k);
  if (shady) knock(c, x, y + h + 10, .26, tt, { open: flashOpen(tt, tFlash), bob: 0 });
  else { block(c, ellPts(x, y + 120, 34, 34, 0, 22), YEL, 9840 + k, { kw: 4 });   // a friendly seller: a round face and a smile
    c.fillStyle = BLK; for (const dx of [-11, 11]) { c.beginPath(); c.arc(x + dx, y + 114, 4.5, 0, TAU); c.fill(); }
    c.save(); c.strokeStyle = BLK; c.lineWidth = 4; c.lineCap = 'round'; c.beginPath(); c.arc(x, y + 124, 13, .25, Math.PI - .25); c.stroke(); c.restore();
    block(c, rrPts(x - 44, y + 150, 88, 60, 20, 4), BLUE, 9850 + k, { kw: 4 }); }
  block(c, rect(x - w / 2 - 6, y + h - 60, w + 12, 60), shady ? BLK : BLUE, 9860 + k, { kw: 5 });   // the counter
  if (!shady) for (let i = 0; i < 3; i++) block(c, rrPts(x - 60 + i * 44, y + h - 90, 32, 30, 6, 3), [YEL, CHIP, YEL][i], 9870 + k * 3 + i, { kw: 3 });
}
SCENES.why = (c, t, S) => {
  sceneBg(c);
  const tt = onTwos(t), { x, y, w, h } = SHOP, roll = easeIn(seg(t, S.at(2) - SLAM, S.at(2, 1.8)));
  shadowRect(c, x, y, w, h); block(c, rect(x, y, w, h), CREAM, 9900, { kw: 6 });   // the building
  for (let i = 0; i < 8; i++) ink(c, rect(x + i * w / 8, y, w / 8, 70), i % 2 ? CHIP : BLUE, 9901 + i, { reg: false }); key(c, rect(x, y, w, 70), 5, 9910);   // the awning
  const sx = SCX, sy = y - 70;   // the sign: a shopping bag, no words
  block(c, rrPts(sx - 170, sy - 60, 340, 120, 20, 5), BLK, 9911, { kw: 5 });
  block(c, rect(sx - 38, sy - 26, 76, 66), YEL, 9912, { kw: 4 }); c.save(); c.strokeStyle = YEL; c.lineWidth = 8; c.beginPath(); c.arc(sx, sy - 26, 20, Math.PI, 0); c.stroke(); c.restore();
  const ix = x + 30, iy = y + 100, iw = w - 60, ih = h - 130;   // inside: the street of little stalls
  if (t >= S.at(2) - SLAM) { block(c, rect(ix, iy, iw, ih), BLK, 9913, { kw: 0, key: false });
    const P = [[ix + 120, iy + 30], [ix + 330, iy + 30], [ix + 540, iy + 30], [ix + 120, iy + 320], [ix + 330, iy + 320], [ix + 540, iy + 320]];
    P.forEach(([px, py], k) => { const pop_ = easeOutBack(seg(tt, S.at(2, 2) + k * S16 - SLAM, S.at(2, 2) + k * S16)); if (pop_ <= 0) return;
      c.save(); c.translate(px, py + 125); c.scale(pop_, pop_); c.translate(-px, -(py + 125)); stall(c, px, py, k, k === 4, tt, t, S.at(2, 3)); c.restore(); }); }
  const shutterH = ih * (1 - roll);   // the shutter rolls up into its drum
  if (shutterH > 1) { block(c, rect(ix, iy, iw, shutterH), '#d9cdb2', 9920, { kw: 5 }); for (let yy = iy + 30; yy < iy + shutterH - 10; yy += 34) ink(c, rect(ix + 8, yy, iw - 16, 6), '#bfae8c', 9921 + yy, { reg: false }); }
  block(c, rrPts(ix - 10, iy - 30, iw + 20, 42, 20, 4), BLK, 9930, { kw: 4 });   // the drum
  const cordY = iy + shutterH + 20, handY = lerp(1500, 1560, roll);   // the cord Jeff pulls
  c.save(); c.strokeStyle = BLK; c.lineWidth = 6; c.beginPath(); c.moveTo(ix + iw - 60, iy + shutterH); c.lineTo(ix + iw - 60, Math.max(cordY, t >= S.at(1, 4) ? handY - 40 : cordY + 120)); c.stroke(); c.restore();
  if (t >= S.at(1, 3) - SLAM) { const pop_ = easeOutBack(land(tt, S.at(1, 3))), pull = t >= S.at(2) - SLAM ? 1 : 0;
    jeff(c, 830, lerp(2600, 1880, pop_), .5, { sx: -1, armR: pull ? -2.2 : -2.9, prop: null, head: .04 * Math.sin(tt * 3), bob: bobOf(tt, 3) }); }
};

// ================= how: read the SOLD BY and SHIPPED BY lines, then the ranking =================
function productPage(c, t, S) {
  const x = 110, y = 600, w = 740, h = 760;
  shadowRect(c, x, y, w, h); block(c, rect(x, y, w, h), CHIP, 9950, { kw: 6 }); ink(c, rect(x, y, w, 70), BLUE, 9951, { reg: false });
  block(c, rect(x + 40, y + 110, 300, 250), '#ffffff', 9952, { kw: 3, reg: false }); headphones(c, x + 190, y + 250, .85);
  for (let k = 0; k < 3; k++) ink(c, rect(x + 380, y + 140 + k * 50, 300 - k * 70, 22), '#d6ccb6', 9953 + k, { reg: false });   // other page details, blank
  const rows = [['SOLD BY:', EP.seller, S.at(1, 2)], ['SHIPPED BY:', EP.seller, S.at(1, 3)]];
  rows.forEach(([lab, val, tl], i) => { const ry = y + 470 + i * 140;
    if (t >= tl) { block(c, rrPts(x + 30, ry - 55, w - 60, 110, 16, 4), YEL, 9960 + i, { kw: 5 }); }   // it lights up (no sweep across the words)
    fitText(c, `${lab} ${val}`, x + w / 2, ry + 6, 58, 'Stamp', BLK, w - 110); });
}
function ranking(c, t, S) {   // the three-rung ranking: level chips, one per beat
  const rows = EP.ranking, ys = [690, 900, 1130], cols = [[BLUE, CHIP], [BLK, CHIP], [YEL, BLK]];
  const x0 = 220, w = 660;
  if (t >= S.at(2) - SLAM) {   // the scale down the left side
    const k = t >= S.at(2) ? 1 : lerp(1.05, 1, easeOut(land(t, S.at(2))));
    c.save(); c.translate(150, 900); c.scale(k, k); c.translate(-150, -900);
    block(c, [[137, 640], [163, 640], [163, 1180], [190, 1180], [150, 1250], [110, 1180], [137, 1180]], BLK, 9970, { kw: 4 }); c.restore(); }
  rows.forEach((ls, i) => { const tl = S.at(2, 1 + i); if (t < tl - SLAM) return; const k = t >= tl ? 1 : lerp(1.05, 1, easeOut(land(t, tl))), y = ys[i], h = ls.length > 1 ? 170 : 120;
    c.save(); c.translate(x0 + w / 2, y); c.scale(k, k); c.translate(-(x0 + w / 2), -y);
    c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fillRect(x0 + 10, y - h / 2 + 12, w, h); c.restore();
    block(c, rect(x0, y - h / 2, w, h), cols[i][0], 9980 + i, { kw: 6 });
    block(c, ellPts(x0 + 70, y, 46, 46, 0, 30), CHIP, 9985 + i, { kw: 4 }); fitText(c, String(i + 1), x0 + 70, y + 6, 58, 'Stamp', BLK, 70);
    ls.forEach((s, j) => fitText(c, s, x0 + 120 + (w - 140) / 2, y + 6 + (j - (ls.length - 1) / 2) * 70, 62, 'Stamp', cols[i][1], w - 160));
    c.restore(); });
  const lab = (s, y, tl, bg, fg) => { if (t < tl - SLAM) return; const k = t >= tl ? 1 : lerp(1.05, 1, easeOut(land(t, tl))); c.save(); c.translate(150, y); c.scale(k, k);
    c.font = '40px Stamp'; const w2 = c.measureText(s).width + 32; block(c, rect(-w2 / 2, -30, w2, 60), bg, 9990 + y, { kw: 4 }); fitText(c, s, 0, 3, 40, 'Stamp', fg, 260); c.restore(); };
  lab('SAFEST', 596, S.at(2), BLUE, CHIP); lab('RISKIEST', 1296, S.at(2, 3), BLK, YEL);
}
SCENES.how = (c, t, S) => {
  const tt = onTwos(t);
  if (t < S.at(2)) {   // bar 1: zoomed in on the page (the zoom settles before anything is read)
    creamBg(c);
    const z = lerp(1, 1.12, easeOut(seg(t, S.at(1), S.at(1, 1.5)))), fx = 480, fy = 1140;
    c.save(); c.translate(fx, fy); c.scale(z, z); c.translate(-fx, -fy); productPage(c, t, S); c.restore();
    const pt = easeOutBack(seg(tt, S.at(1, 2) - SLAM, S.at(1, 2)));
    jeff(c, 150, lerp(2600, 1900, easeOutBack(land(tt, S.at(1)))), .52, { armR: lerp(-1.2, -2.3, pt), prop: pt > .5 ? 'point' : null, head: .04 * Math.sin(tt * 3), bob: bobOf(tt, 3) });
  } else {   // bars 2-3: the ranking; the knockoff seller pops up below the risky end
    sceneBg(c); ranking(c, t, S);
    if (t >= S.at(3) - SLAM) { const pop_ = easeOutBack(land(tt, S.at(3))); knock(c, 760, lerp(2400, 1880, pop_), .66, tt, { open: flashOpen(tt, S.at(3, 2)) }); }
  }
};
