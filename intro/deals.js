'use strict';
/* Rossen Reports: "STILL LIVE" weekend deals roundup. 1080x1920 (9:16), 24 fps, 96 BPM, one continuous film, 54.5 s.
   Everything on screen comes from deals/deals.json: the names, the prices (shown exactly as written there), the promo codes,
   the price-check date and time, the credit, the disclosure and the per-platform CTA. Percent off is calculated from the
   prices (whole cents, rounded to the nearest whole percent), never typed in. The platform comes from window.PLATFORM
   (set by the page) or ?platform=; only the CTA changes between the versions.
   Style: the case-file screen print on the approved textured cream board, the approved palette (printkit.js), the Jeff
   puppet, the screen-print logo sticker and the official logo on the closing card.

   The product photos are drawn from their files, uniformly scaled and level, never redrawn or altered, as prints pinned to
   the board with a clean cream border and a slight paper shadow. The paper-speck finish is applied BEFORE the prints and
   all type, so nothing textures the products or the letters. Nothing is drawn over a photo or over any text.

   OPEN      bar 0       "THESE DEALS ARE / STILL LIVE" from frame 0; photo 1 pins in on beat 3 (1.25 s); Jeff points
   DEAL k    3 bars each  bar 1: the photo pins in, the name lands     bar 2: the regular price
                         bar 3: the DEAL stamp slams onto the tag as the deal price lands (the regular price is struck
                                through at the same instant); beat 2: the percent-off sticker
             transitions: 1>2 push, 2>3 [signature] the whole board flips over like a price tag on its string,
                          3>4 push, 4>5 [signature] a shopping box drops in, pops open, and we dive in to the last deal
   NOTE      1 bar       the price check (cut in and out, so it is still and readable for the full bar)
   DISCLOSE  1 bar       the affiliate disclosure (cut in and out: still and readable for the full bar)
   CREDIT    1 bar       "DEALS FROM / DEALSEEK.COM"; Jeff pops up on beat 2
   CTA       1 bar       the platform CTA; Jeff's thumbs up on beat 2; the rubber stamp drops over the last .35 s
   END                   the closing card (liveEndCard), still for its last 4.2 s
*/
const SANS = '"Liberation Sans"';
const PUSH = .3, DB = 3;   // DB: bars per deal (every deal gets the same bars)
const PLATFORM = (window.PLATFORM || Q.get('platform') || 'facebook').toLowerCase();
let DJ = null, DEALS = [], N = 0, T_NOTE = 0, T_DISC = 0, T_CRED = 0, T_CTA = 0, T_END = 0, DUR = 1, NFR = 1;
const A_ = k => at(1 + DB * k), P_ = k => A_(k) + BAR, D_ = k => A_(k) + 2 * BAR;   // a deal's bars: photo, regular price, deal

// ================= data =================
function cents(s) {   // "169.90" -> 16990, exactly (no floating point)
  if (typeof s !== 'string' || !/^\d+\.\d\d$/.test(s)) throw new Error(`prices in deals.json must be strings like "39.90", got ${JSON.stringify(s)}`);
  const [a, b] = s.split('.'); return +a * 100 + +b;
}
function pctOff(d) { const r = cents(d.regular), p = cents(d.deal); return Math.round((r - p) * 100 / r); }
function checkData(j) {
  if (!Array.isArray(j.deals) || j.deals.length < 1) throw new Error('deals.json: no deals');
  for (const d of j.deals) { if (!d.name) throw new Error('deals.json: a deal has no name'); if (cents(d.deal) >= cents(d.regular)) throw new Error(`deals.json: ${d.name}: the deal price is not below the regular price`); if (!d.image) throw new Error(`deals.json: ${d.name}: no image`); }
  if (!j.cta || !j.cta[PLATFORM]) throw new Error(`deals.json: no CTA for platform "${PLATFORM}"`);
  if (!j.priceCheck || !j.priceCheck.date || !j.priceCheck.time) throw new Error('deals.json: priceCheck needs a date and a time');
}
const up = s => String(s).toUpperCase();

// ================= type: level chips that land gently (from 1.05, no overshoot), then hold completely still =================
const gentle = (t, t0) => t >= t0 ? 1 : lerp(1.05, 1, easeOut(land(t, t0)));
function lines2(c, s, size, maxW) {   // one line if it fits, else the most balanced two-line split
  c.font = `${size}px Stamp`; if (c.measureText(s).width <= maxW) return [s];
  const w = s.split(' '); let best = null;
  for (let i = 1; i < w.length; i++) { const a = w.slice(0, i).join(' '), b = w.slice(i).join(' '), m = Math.max(c.measureText(a).width, c.measureText(b).width); if (!best || m < best[0]) best = [m, [a, b]]; }
  return best ? best[1] : [s];
}
function wrap(c, s, size, maxW) { c.font = `${size}px Stamp`; const out = []; let cur = '';
  for (const wd of s.split(' ')) { const t2 = cur ? cur + ' ' + wd : wd; if (cur && c.measureText(t2).width > maxW) { out.push(cur); cur = wd; } else cur = t2; }
  out.push(cur); return out; }
function fitSize(c, ls, size, maxW) { c.font = `${size}px Stamp`; const m = Math.max(...ls.map(s => c.measureText(s).width)); return m > maxW ? Math.floor(size * maxW / m) : size; }
function chip(c, s, x, y, size, bg, fg, t, t0) {
  if (t < t0 - SLAM) return;
  c.font = `${size}px Stamp`; const w = c.measureText(s).width + 58, h = size * 1.34, k = gentle(t, t0);
  c.save(); c.translate(x, y); c.scale(k, k);
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fillRect(-w / 2 + 8, -h / 2 + 10, w, h); c.restore();
  c.fillStyle = bg; c.fillRect(-w / 2, -h / 2, w, h); text(c, s, 0, size * .06, `${size}px Stamp`, fg); c.restore();
}
function headChips(c, s, t, t0) {   // a two-line headline at the top of the board: black chip, then blue chip
  const ls = lines2(c, up(s), 62, 740), size = fitSize(c, ls, 62, 740);
  ls.forEach((l, i) => chip(c, l, SCX, 372 + i * 96, size, i ? BLUE : BLK, CHIP, t, t0));
}

// ================= the pinned photo prints =================
const PH = { x: 60, top: 530, box: 480, bd: 28 };   // left column; the sticker sits in the right column
function printRect(k) {
  const im = IMG['deal' + k], sc = Math.min(PH.box / im.width, PH.box / im.height), pw = im.width * sc, ph = im.height * sc;
  return { im, pw, ph, w: pw + 2 * PH.bd, h: ph + 2 * PH.bd, x: PH.x + (PH.box - pw) / 2, y: PH.top + (PH.box - ph) / 2 };
}
function photoPrint(c, k, t, t0) {   // drops onto the board and is pinned on t0; the photo itself is only ever scaled
  if (t < t0 - .25) return;
  const u = t >= t0 ? 1 : easeIn(seg(t, t0 - .25, t0)), s = lerp(1.1, 1, u), off = lerp(36, 12, u);
  const R = printRect(k), cx = R.x + R.w / 2, cy = R.y + R.h / 2;
  c.save(); c.translate(cx, cy); c.scale(s, s); c.translate(-cx, -cy);
  c.save(); c.shadowColor = 'rgba(29,27,31,0.30)'; c.shadowBlur = 20; c.shadowOffsetX = off * .6; c.shadowOffsetY = off; c.fillStyle = CHIP; c.fillRect(R.x, R.y, R.w, R.h); c.restore();
  c.imageSmoothingEnabled = true; c.imageSmoothingQuality = 'high'; c.drawImage(R.im, R.x + PH.bd, R.y + PH.bd, R.pw, R.ph);
  c.restore();
  if (u >= 1) pushpin(c, cx, R.y + 12);   // on the top border, clear of the photo
}

// ================= prices =================
const REGC = { x: 60, y: 1120, size: 54 };
function regChip(c, d, t, t0, struck) {   // "REG. $169.90": level, readable; struck through (not swept) the instant the deal lands
  if (t < t0 - SLAM) return;
  const lab = 'REG. ', pr = '$' + d.regular, size = REGC.size; c.font = `${size}px Stamp`;
  const wl = c.measureText(lab).width, wp = c.measureText(pr).width, w = wl + wp + 56, h = size * 1.36, k = gentle(t, t0);
  c.save(); c.translate(REGC.x, REGC.y); c.scale(k, k);
  c.save(); c.globalAlpha = .28; c.fillStyle = BLK; c.fillRect(8, -h / 2 + 10, w, h); c.restore();
  c.fillStyle = CHIP; c.fillRect(0, -h / 2, w, h); key(c, rect(0, -h / 2, w, h), 5, 8001);
  text(c, lab + pr, 28, size * .06, `${size}px Stamp`, BLK, 'left');
  if (struck) { c.fillStyle = BLUE; c.fillRect(28 + wl - 6, -1, wp + 12, 5); }   // thin, so every digit stays readable
  c.restore();
}
const TAG = { x: 60, y: 1188, w: 840, h: 206 };
const tagPts = (x, y, w, h) => [[x + 78, y], [x + w, y], [x + w, y + h], [x + 78, y + h], [x, y + h / 2]];
function priceTag(c, d, t, t0) {   // the yellow price tag with the deal price, pinned through its hole
  if (t < t0 - SLAM) return;
  const { x, y, w, h } = TAG, cx = x + w / 2, cy = y + h / 2, k = gentle(t, t0);
  c.save(); c.translate(cx, cy); c.scale(k, k); c.translate(-cx, -cy);
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fill(polyPath(tagPts(x + 10, y + 14, w, h))); c.restore();
  block(c, tagPts(x, y, w, h), YEL, 8101, { kw: 6 });
  c.fillStyle = CREAM; c.beginPath(); c.arc(x + 46, cy, 22, 0, TAU); c.fill(); c.strokeStyle = BLK; c.lineWidth = 4; c.stroke(); pushpin(c, x + 46, cy);
  const px0 = x + 340, pw = w - 360;
  if (d.code) { fitText(c, '$' + d.deal, px0 + pw / 2, cy - 22, 128, 'Stamp', BLK, pw); fitText(c, 'CODE: ' + up(d.code), px0 + pw / 2, cy + 66, 40, 'Stamp', BLK, pw); }
  else fitText(c, '$' + d.deal, px0 + pw / 2, cy + 8, 150, 'Stamp', BLK, pw);
  c.restore();
  dealStamp(c, x + 206, cy, t, t0);
}
function dealStamp(c, x, y, t, t0) {   // a clean, opaque rubber-stamp impression: solid ink, no texture in the letters
  if (t < t0 - SLAM) return;
  const s = t >= t0 ? 1 : lerp(1.45, 1, easeIn(land(t, t0))), w = 236, h = 116;
  c.save(); c.translate(x, y); c.rotate(-.07); c.scale(s, s);
  if (t < t0) { c.save(); c.globalAlpha = .25; c.fillStyle = BLK; c.fillRect(-w / 2 + 14, -h / 2 + 18, w, h); c.restore(); }
  c.fillStyle = CHIP; c.fill(polyPath(rrPts(-w / 2, -h / 2, w, h, 14, 4)));
  key(c, rrPts(-w / 2 + 5, -h / 2 + 5, w - 10, h - 10, 12, 4), 8, 8201, true, BLUE); key(c, rrPts(-w / 2 + 17, -h / 2 + 17, w - 34, h - 34, 8, 4), 3, 8202, true, BLUE);
  fitText(c, 'DEAL', 0, 6, 74, 'Stamp', BLUE, w - 60);
  c.restore();
}
const SK = { x: 772, y: 790, r: 124 };
function burstPts(x, y, r, n = 18) { const P = []; for (let i = 0; i < n * 2; i++) { const a = -Math.PI / 2 + i * Math.PI / n, rr = i % 2 ? r * .85 : r; P.push([x + Math.cos(a) * rr, y + Math.sin(a) * rr]); } return P; }
function sticker(c, d, t, t0) {   // percent off: a blue burst sticker with level type
  if (t < t0 - SLAM) return;
  const k = gentle(t, t0), { x, y, r } = SK;
  c.save(); c.translate(x, y); c.scale(k, k); c.translate(-x, -y);
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fill(polyPath(burstPts(x + 9, y + 12, r))); c.restore();
  block(c, burstPts(x, y, r), BLUE, 8301, { kw: 6 });
  fitText(c, pctOff(d) + '%', x, y - 18, 88, 'Stamp', CHIP, r * 1.5); fitText(c, 'OFF', x, y + 54, 50, 'Stamp', YEL, r * 1.2);
  c.restore();
}

// ================= scenes (each draws a whole frame in content coordinates) =================
function finish(c) { printFinish(c); contentT(c); }   // the paper specks: over the board and puppets only
function openJeff(c, t) {   // bar 0: Jeff stands in the right column pointing at the first deal, ducks out before bar 1
  const tt = onTwos(t), out = easeIn(seg(tt, at(1) - .45, at(1) - .1)); if (out >= 1) return;
  jeff(c, 770, lerp(1850, 2900, out), .6, { sx: -1, armR: -2.05, prop: 'point', head: -.06 + .03 * Math.sin(tt * 3), bob: Math.abs(Math.sin(tt * Math.PI / BEAT)) * 4 });
}
function dealScene(c, t, k, o = {}) {
  creamBg(c); contentT(c);
  if (k === 0) openJeff(c, t);
  finish(c);
  const d = DEALS[k];
  photoPrint(c, k, t, k === 0 ? at(0, 3) : A_(k));
  if (k === 0 && t < A_(0) - SLAM) { chip(c, 'THESE DEALS ARE', SCX, 372, 62, BLK, CHIP, t, 0); chip(c, up(DJ.title || 'STILL LIVE'), SCX, 478, 84, YEL, BLK, t, 0); }
  else headChips(c, d.name, t, A_(k));
  regChip(c, d, t, P_(k), t >= D_(k));
  if (!o.noTag) priceTag(c, d, t, D_(k));
  sticker(c, d, t, D_(k) + BEAT);
}
function paperNote(c, ls, cols, size, t, t0) {   // a plain pinned paper note, level, all type black or blue on cream chip
  const lh = size * 1.3, w = 800, h = ls.length * lh + 120, x = SCX - w / 2, y = SCY - h / 2 - 20, k = gentle(t, t0);
  c.save(); c.translate(SCX, y + h / 2); c.scale(k, k); c.translate(-SCX, -(y + h / 2));
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fillRect(x + 12, y + 16, w, h); c.restore();
  c.fillStyle = CHIP; c.fillRect(x, y, w, h); key(c, rect(x, y, w, h), 5, 8401);
  ls.forEach((l, i) => fitText(c, l, SCX, y + 60 + lh * (i + .5) + size * .06, size, 'Stamp', cols[i], w - 90));
  c.restore(); pushpin(c, x + 40, y + 30); pushpin(c, x + w - 40, y + 30);
}
function noteScene(c, t) {
  creamBg(c); contentT(c); finish(c);
  const pc = DJ.priceCheck, a = `PRICES AS OF ${up(pc.date)},`, b = `${up(pc.time)} ET.`, e = wrap(c, 'DEALS CAN END ANYTIME.', 66, 700);
  paperNote(c, [a, b, ...e], [BLK, BLK, ...e.map(() => BLUE)], 66, t, T_NOTE);
}
function discScene(c, t) {
  creamBg(c); contentT(c); finish(c);
  const s = up(DJ.disclosure), i = s.indexOf(':'), head = i > 0 ? s.slice(0, i + 1) : null, body = wrap(c, i > 0 ? s.slice(i + 1).trim() : s, 62, 700);
  paperNote(c, head ? [head, ...body] : body, head ? [BLUE, ...body.map(() => BLK)] : body.map(() => BLK), 62, t, T_DISC);
}
function ctaScene(c, t) {
  creamBg(c); contentT(c);
  const tt = onTwos(t), pop = easeOutBack(land(tt, T_CRED + BEAT)), th = easeOutBack(seg(tt, T_CTA + BEAT - SLAM, T_CTA + BEAT + .25));
  stickerLogo(c, 230, 1110, 300, -.05, 1);
  jeff(c, 640, lerp(2800, 1850, pop), .7, { armR: th > 0 ? lerp(0, -2.5, th) : 0, prop: th > .6 ? 'thumb' : null, head: .04 * Math.sin(tt * 3), bob: Math.abs(Math.sin(tt * Math.PI / BEAT)) * 4 });
  finish(c);
  headChips(c, DJ.credit, t, T_CRED);
  if (t >= T_CTA - SLAM) {   // the CTA: one big yellow card, level
    const ls = lines2(c, up(DJ.cta[PLATFORM]), 84, 700), size = fitSize(c, ls, 84, 700), h = ls.length * size * 1.28 + 70, w = 800, y = 610, k = gentle(t, T_CTA);
    c.save(); c.translate(SCX, y + h / 2); c.scale(k, k); c.translate(-SCX, -(y + h / 2));
    c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fillRect(SCX - w / 2 + 12, y + 16, w, h); c.restore();
    block(c, rect(SCX - w / 2, y, w, h), YEL, 8501, { kw: 6 });
    ls.forEach((l, i) => fitText(c, l, SCX, y + 35 + size * 1.28 * (i + .5) + size * .06, size, 'Stamp', BLK, w - 80));
    c.restore();
  }
  const dd = seg(t, T_END - .35, T_END); if (dd > 0) screenSpace(c, () => rubberStamp(c, easeIn(dd)));
}
function sceneSignoff(c, t) {
  paperBg(c); liveEndCard(c, ['youtube', 'instagram', 'facebook']);   // the closing card (vertkit.js), with Facebook added for this film: untouched logos, still
  const lift = seg(t, T_END, T_END + .3);
  if (lift < 1) { c.save(); c.translate(0, -(H + 320) * easeIn(lift)); rubberStampFlat(c); c.restore(); }
}

// ================= transitions =================
function toLayer(L, fn, t) { const g = L.getContext('2d'); contentT(g); g.globalAlpha = 1; fn(g, t); if (SHOW_SAFE) safeOverlay(g); return L; }
function pushH(c, t, tb, A, B) {   // the plain transition: the board slides left to the next deal
  const u = easeIO(seg(t, tb - PUSH / 2, tb + PUSH / 2)); toLayer(L1, A, t); toLayer(L2, B, t);
  screenSpace(c, () => { c.drawImage(L1, -u * W, 0, W, H); c.drawImage(L2, (1 - u) * W, 0, W, H); });
}
// [signature 1] the whole board hangs like a big price tag: it pulls back on its string, flips over, and the next deal is
// on the back. tb - .35 .. tb + .15; the back is fully turned on the downbeat.
const FLIP = [.35, .15];
function tagOutline(sc, fx) {   // the tag silhouette in screen space: the frame plus a head with a hole, above the frame
  const P = [[-W / 2, H / 2], [-W / 2, -H / 2], [-W / 2 + 230, -H / 2 - 210], [W / 2 - 230, -H / 2 - 210], [W / 2, -H / 2], [W / 2, H / 2]];
  return P.map(([x, y]) => [CX + x * sc * fx, CY + y * sc]);
}
function tagFlip(c, t, tb, A, B) {
  const u = seg(t, tb - FLIP[0], tb + FLIP[1]), sc = u < .3 ? lerp(1, .72, easeIO(u / .3)) : u > .7 ? lerp(.72, 1, easeIO((u - .7) / .3)) : .72;
  const v = clamp01((u - .3) / .4), fx = Math.cos(Math.PI * easeIO(v)), front = fx >= 0, af = Math.max(.012, Math.abs(fx));
  toLayer(L1, front ? A : B, front ? Math.min(t, tb - FLIP[0]) : Math.max(t, tb));
  screenSpace(c, () => {
    bgDots(c, BLUE, .22, .5);
    const hole = [CX, CY + (-H / 2 - 105) * sc];
    c.save(); c.strokeStyle = BLK; c.lineWidth = 8; c.beginPath(); c.moveTo(CX, -20); c.lineTo(hole[0], hole[1]); c.stroke(); c.strokeStyle = YEL; c.lineWidth = 4.5; c.stroke(); c.restore();
    const P = tagOutline(sc, af);
    c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fill(polyPath(P.map(([x, y]) => [x + 16, y + 20]))); c.restore();
    c.save(); c.fillStyle = CHIP; c.fill(polyPath(P)); c.clip(polyPath(P));
    c.translate(CX, CY); c.scale(sc * af, sc); c.drawImage(L1, -W / 2, -H / 2, W, H);
    c.restore();
    if (af < .999) { c.save(); c.globalAlpha = .28 * (1 - af); c.fillStyle = BLK; c.fill(polyPath(P)); c.restore(); }
    key(c, P, 6, 8601);
    c.save(); c.translate(hole[0], hole[1]); c.scale(af, 1); c.fillStyle = YEL; c.beginPath(); c.arc(0, 0, 40 * sc, 0, TAU); c.fill(); c.strokeStyle = BLK; c.lineWidth = 5; c.stroke();
    c.fillStyle = BLUE; c.beginPath(); c.arc(0, 0, 20 * sc, 0, TAU); c.fill(); c.stroke(); c.restore();
  });
}
// [signature 2] a shopping box drops onto the board, pops open, and we dive into it to the last deal.
const BOX = [.5, .12];   // tb - .5 .. tb + .12: lands on the "and" of beat 4, flaps open, the mouth grows to the frame
function boxFront(c, x0, y0, w, h, open) {   // front view; open 0..1 swings the two top flaps outward
  const d = 120, top = [[x0, y0], [x0 + w, y0], [x0 + w - 70, y0 - d], [x0 + 70, y0 - d]];
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fillRect(x0 + 16, y0 + 20, w, h); c.restore();
  block(c, top, open > 0 ? BLK : CREAM, 8701, { kw: 5 });
  block(c, rect(x0, y0, w, h), CREAM, 8702, { kw: 6 });
  ink(c, rect(x0 + w / 2 - 38, y0, 76, 120), YEL, 8703, { reg: false }); key(c, rect(x0 + w / 2 - 38, y0, 76, 120), 3, 8704);   // tape
  block(c, rrPts(x0 + w / 2 - 70, y0 + h - 130, 140, 34, 17, 4), BLK, 8705, { kw: 0, key: false });   // a hand hole
  if (open <= 0) { ink(c, rect(x0 + w / 2 - 38, y0 - d, 76, d), YEL, 8706, { reg: false }); return; }
  const th = lerp(0, 2.35, easeOutBack(open));
  for (const side of [-1, 1]) {   // each flap is hinged on a side edge of the top face
    const h0 = side < 0 ? [x0, y0] : [x0 + w, y0], h1 = side < 0 ? [x0 + 70, y0 - d] : [x0 + w - 70, y0 - d], L = w / 2 - 10;
    const dx = -side * Math.cos(th) * L, dy = -Math.sin(th) * L * .55;
    block(c, [h0, h1, [h1[0] + dx, h1[1] + dy], [h0[0] + dx, h0[1] + dy]], CREAM, 8710 + side, { kw: 5 });
  }
}
function boxPop(c, t, tb, A, B) {
  const tl = tb - E8, drop = easeIn(seg(t, tb - BOX[0], tl)), open = seg(t, tl, tb - .15), dive = easeIn(seg(t, tb - .15, tb + BOX[1]));
  const w = 560, h = 400, x0 = SCX - w / 2, y0 = lerp(-700, 820, drop);
  if (dive <= 0) { A(c, Math.min(t, tb - BOX[0])); contentT(c); boxFront(c, x0, y0, w, h, open); return; }
  A(c, tb - BOX[0]); contentT(c); boxFront(c, x0, y0, w, h, 1);
  toLayer(L1, B, Math.max(t, tb));
  const m = [CX + (x0 + 70 - SCX) * K, SCY + (y0 - 120 - SCY) * K, (w - 140) * K, 120 * K];   // the mouth, on screen
  const x = lerp(m[0], 0, dive), y = lerp(m[1], 0, dive), ww = lerp(m[2], W, dive), hh = lerp(m[3], H, dive), s = Math.max(ww / W, hh / H);
  screenSpace(c, () => { c.save(); c.beginPath(); c.rect(x, y, ww, hh); c.clip(); c.translate(x + ww / 2, y + hh / 2); c.scale(s, s); c.drawImage(L1, -W / 2, -H / 2, W, H); c.restore(); });
}

// ================= assembly =================
let SCN = [];
function buildTimeline() {
  N = DEALS.length;
  T_NOTE = at(1 + DB * N); T_DISC = T_NOTE + BAR; T_CRED = T_DISC + BAR; T_CTA = T_CRED + BAR; T_END = T_CTA + BAR;
  DUR = T_END + 4.5; NFR = Math.round(FPS * DUR);
  const flipTo = N >= 4 ? 2 : -1, boxTo = N >= 3 ? N - 1 : -1;
  SCN = DEALS.map((d, k) => ({ t0: k ? A_(k) : 0, fn: (g, t, o) => dealScene(g, t, k, o), tr: k === 0 ? null : k === flipTo ? 'flip' : k === boxTo ? 'box' : 'push' }));
  SCN.push({ t0: T_NOTE, fn: noteScene, tr: 'cut' }, { t0: T_DISC, fn: discScene, tr: 'cut' }, { t0: T_CRED, fn: ctaScene, tr: 'cut' });
}
const WIN = { push: [PUSH / 2, PUSH / 2], flip: FLIP, box: BOX, cut: [0, 0] };
function drawScene(c, t) {
  contentT(c);
  if (t >= T_END) { resetT(c); sceneSignoff(c, t); return; }   // screen space; no finish over the logos
  for (let i = 1; i < SCN.length; i++) {
    const S = SCN[i], [a, b] = WIN[S.tr]; if (!(t >= S.t0 - a && t < S.t0 + b)) continue;
    const A = SCN[i - 1].fn, B = S.fn;
    if (S.tr === 'push') pushH(c, t, S.t0, A, B);
    else if (S.tr === 'flip') tagFlip(c, t, S.t0, A, B);
    else if (S.tr === 'box') boxPop(c, t, S.t0, A, B);
    if (SHOW_SAFE && S.tr === 'box') safeOverlay(c);
    return;
  }
  let cur = SCN[0]; for (const S of SCN) if (t >= S.t0) cur = S;
  cur.fn(c, t);
  if (SHOW_SAFE) safeOverlay(c);
}

// ================= runtime (skipped when another film loads deals.js as a library: window.DEALS_LIB) =================
if (!window.DEALS_LIB) {
const CV = document.getElementById('c'); CV.width = OUT_W; CV.height = OUT_H; const CTX = CV.getContext('2d');
function frame(i) { const t = Math.min(i / FPS, DUR - 1e-6); FILM_T = t; resetT(CTX); CTX.globalAlpha = 1; drawScene(CTX, t); resetT(CTX); }
window.__FPS = FPS; window.__frame = i => { frame(i); return CV.toDataURL('image/png'); };
(async () => {
  await loadPrintKit(); await loadVertKit(); makeCream(); await loadImg('facebook_icon', 'assets/social/facebook_icon.png');
  DJ = await (await fetch('deals/deals.json', { cache: 'no-store' })).json(); checkData(DJ); DEALS = DJ.deals;
  await Promise.all(DEALS.map((d, k) => loadImg('deal' + k, d.image)));
  DEALS.forEach((d, k) => { if (!IMG['deal' + k] || !IMG['deal' + k].width) throw new Error('missing image: ' + d.image); });
  buildTimeline(); window.__NFR = NFR;
  window.__info = { platform: PLATFORM, dur: DUR, nfr: NFR, deals: DEALS.map((d, k) => ({ name: d.name, regular: '$' + d.regular, deal: '$' + d.deal, pct: pctOff(d), bars: [A_(k), P_(k), D_(k)].map(x => +(x / BAR).toFixed(3)) })),
    note: T_NOTE, disc: T_DISC, cred: T_CRED, cta: T_CTA, end: T_END };
  frame(+(Q.get('frame') || 0));
  window.__ready = true;
})().catch(e => { console.error(e); window.__error = String(e); });
}
