'use strict';
/* Vertical (9:16) kit shared by the Rossen shorts: format and 96 BPM clock, the platform safe zone and the centred
   content transform, captions (each film defines CAPS), stamps that fit the safe width, the scammer puppet with its
   line and hook, zoom-through windows, the rubber stamp. Load after core.js, kit.js and printkit.js. */
setFormat({ ar: '9:16', width: 1080 });
const FPS = 24, BEAT = .625, BAR = 2.5, E8 = BEAT / 2, S16 = BEAT / 4;
const at = (bar, beat = 1) => bar * BAR + (beat - 1) * BEAT;   // bar 0-based, beat 1-based

const SAFE = { x0: 60, x1: 900, y0: 300, y1: 1430 }, SCX = 480, SCY = 865;   // the layout is drawn around this centre...
// ...then shown centred on the frame: content is scaled by K about the frame's centre line, so x 60-900 lands on 180-900
// (symmetric about x 540 and still clear of the right 15%) and y 300-1430 on 381-1349. Backgrounds stay full-frame.
const K = 720 / 840;
function contentT(g) { resetT(g); g.translate(CX - SCX * K, SCY - SCY * K); g.scale(K, K); }
function screenSpace(c, fn) { c.save(); resetT(c); fn(); c.restore(); }
const L1 = layer(), L2 = layer();
let SP = null, FILM_T = 0;
const Q = new URLSearchParams(location.search), SHOW_SAFE = Q.has('safe');

// ================= small kit =================
const clamp01 = v => Math.max(0, Math.min(1, v));
const pop = (t, t0) => t < t0 ? lerp(1.3, 1, easeIn(land(t, t0))) : 1 + .06 * Math.exp(-(t - t0) * 12) * Math.cos((t - t0) * 30);   // lands on t0, wobbles
function bgDots(c, col = BLUE, lo = .1, hi = .5, cell = 20) {
  paperBg(c); c.save(); resetT(c); dotScreen(c, polyPath(rect(0, 0, W, H)), [0, 0, W, H], { cell, color: col, density: (x, y) => lo + (hi - lo) * Math.min(1, Math.hypot(x - SCX, y - SCY) / 1100), angle: ANG[col] ?? .3, seed: 3001 }); c.restore();
}
function shadowRect(c, x, y, w, h, a = .28) { c.save(); c.globalAlpha = a; c.fillStyle = BLK; c.fillRect(x + 14, y + 18, w, h); c.restore(); }
function pill(c, cx, cy, w, h, col, label, size, tcol = BLK, seed = 2101) { block(c, rrPts(cx - w / 2, cy - h / 2, w, h, h / 2, 5), col, seed, { kw: 6 }); inkText(c, label, cx, cy + 4, size, 'Stamp', tcol, w - 60); }

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
function stampFit(c, word, col, size, x, y, rot, sc, t, t0, maxW = 800, from = 1.55) {   // a stamp scaled down if it would leave the safe zone
  const im = stampImg(word, col, size), k = Math.min(sc, maxW / (im.width * Math.abs(Math.cos(rot)) + im.height * Math.abs(Math.sin(rot))));
  stampLand(c, im, x, y, rot, k, t, t0, from);
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

function stickerLogo(c, x, y, lw, rot, s) { const im = IMG.sp, [bx, by, bw, bh] = IMG.spBox, lh = bh * lw / bw; c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s); c.drawImage(im, bx, by, bw, bh, -lw / 2, -lh / 2, lw, lh); c.restore(); }
function jeffUp(c, t, t0, x, p = {}, s = .72) { const a = easeOutBack(land(t, t0)); if (t < t0 - SLAM) return null; return jeff(c, x, lerp(3000, 1830, a), s, p); }

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

function zoomThrough(c, t, t0, t1, rect0, under, inner) {   // a window grows from rect0 to the full frame; inner scene drawn through it
  under(c);   // in content coordinates; the window itself grows in screen space to the full frame
  const u = easeIO(seg(t, t0, t1)), x0 = CX + (rect0[0] - SCX) * K, y0 = SCY + (rect0[1] - SCY) * K, w0 = rect0[2] * K, h0 = rect0[3] * K;
  const x = lerp(x0, 0, u), y = lerp(y0, 0, u), w = lerp(w0, W, u), h = lerp(h0, H, u), k = lerp(w0 / W, 1, u);
  const g = L1.getContext('2d'); contentT(g); g.globalAlpha = 1; inner(g);
  c.save(); resetT(c); c.beginPath(); c.rect(x, y, w, h); c.clip(); c.translate(x + w / 2, y + h / 2); c.scale(Math.max(k, w / W, h / H), Math.max(k, w / W, h / H)); c.drawImage(L1, -W / 2, -H / 2, W, H); c.restore();
  if (u < 1) screenSpace(c, () => key(c, rect(x, y, w, h), 8, 4001));
}

// safe-zone overlay for ?safe=1 check renders (screen space)
function safeOverlay(c) { c.save(); resetT(c); c.strokeStyle = '#ff00ff'; c.lineWidth = 4; c.strokeRect(CX - 360, 381, 720, 968); c.globalAlpha = .15; c.fillStyle = '#ff00ff'; c.fillRect(0, 0, W, 288); c.fillRect(0, 1440, W, 480); c.fillRect(918, 0, 162, H); c.restore(); }
// the scammer's parts and both logos
async function loadVertKit() {
  SP = await (await fetch('assets/explainer/scammer_parts.json')).json();
  await Promise.all([...Object.keys(SP.parts).map(k => loadImg('s_' + k, `assets/explainer/scammer_${k}.png`)), loadImg('logo', 'assets/official_logo.png'), loadImg('sp', 'assets/casefile/logo_screenprint.webp')]);
  IMG.logoBox = alphaBox(IMG.logo); IMG.spBox = alphaBox(IMG.sp);
}
