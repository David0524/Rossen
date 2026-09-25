'use strict';
/* Friday live-show tease: 30 s (12 bars at 96 BPM, D minor into D major), 1080x1920 (9:16), 24 fps, one continuous film,
   then the approved 5 s LIVE TODAY loop (rossen-loop-friday, 10 AM ET) is appended untouched and plays twice (40 s total). Case-file screen-print
   look (printkit.js), the approved palette, the vertical safe-zone content transform (VERT_K 0.895, like the loop).
   Tease the scams, don't explain them. Captions: one short ALL-CAPS card per bar, on screen for the whole bar.

   NEW PHONE  bar 0  0.0   a delivery box slams onto the doorstep in frame 0; flaps pop on 3; a new phone rises    "OPENING A / NEW PHONE?"
              bar 1  2.5   ACTIVATED on 1; on 3 it rings: CARRIER SUPPORT                                       "MINUTES LATER... / IT RINGS."
              bar 2  5.0   a fishing hook drops on 2 and yanks the phone up and away on 3                      "WITHIN THE HOUR, / IT'S GONE."
   PORT HACK  bar 3  7.5   the camera follows it up: the Scammer has it on his line; on 3 he pulls the phone     "PORT HACKING"
                           number out of it like a thread
              bar 4  10.0  the camera follows the thread right to a vault; it turns the lock; the door opens on 3 "YOUR NUMBER... / OPENS YOUR BANK"
              bar 5  12.5  cash streams out on eighths; the calendar tears DAY 1, DAY 4, WEEK 2, WEEK 3           "FOR DAYS. / EVEN WEEKS."
   THE FIX    bar 6  15.0  dive into the vault: a laptop typing; Jeff's magnifier on 2; a padlock slams on 3, a   "AN ETHICAL HACKER / SHOWS YOU HOW / TO STOP IT"
                           check on 4
   DEALS      bar 7  17.5  price tags swing in on 1, 2, 3; YOUR REQUESTS on 4                                    "PLUS: HOT DEALS / AND LIVE REQUESTS"
   AMAZON     bars 8-9 20.0 the official Amazon logo on a card; three code tickets slide out from behind it (8:2-4);   "WE FOUND HIDDEN / AMAZON PROMO CODES"
                           REVEALED LIVE stamps cover the codes (9:1-3); Jeff thumbs up on 9:4
   LIVE       bar 10 25.0  a plain video player with Jeff live inside; LIVE on 2; the ROSSEN REPORTS CHANNEL row   "LIVE ON YOUTUBE / ROSSEN REPORTS"
                           on 3; SEE YOU AT 10! on 4
   HANDOFF    bar 11 27.5  the camera drops onto the loop's own page; its pieces land on the beats in their exact
                           places (logo on 1, LIVE TODAY on 2, 10 AM ET + FRIDAY on 3, LIVE ON YOUTUBE + Jeff on 4), and from 29.5 s
                           it is the loop's own frames, so the cut at 30.0 s is the loop's seamless wrap.
*/
const B_LIVE = 10, B_HAND = 11;   // the LIVE ON YOUTUBE bar and the handoff bar
const DUR = at(12), NFR = Math.round(FPS * DUR);
const SANS = '"Liberation Sans"', MONO = '"Liberation Mono"', FAKE_NUM = '1-555-XXX-XXXX';
const PUSH = .3;

// ================= captions =================
const CAPS = [
  [at(0), 'OPENING A', 'NEW PHONE?'], [at(1), 'MINUTES LATER...', 'IT RINGS.'], [at(2), 'WITHIN THE HOUR,', "IT'S GONE."],
  [at(3), 'PORT HACKING'], [at(4), 'YOUR NUMBER...', 'OPENS YOUR BANK'], [at(5), 'FOR DAYS.', 'EVEN WEEKS.'],
  [at(6), 'AN ETHICAL HACKER', 'SHOWS YOU HOW', 'TO STOP IT'], [at(7), 'PLUS: HOT DEALS', 'AND LIVE REQUESTS'], [at(8), 'WE FOUND HIDDEN', 'AMAZON PROMO CODES'], [at(B_LIVE), 'LIVE ON YOUTUBE', 'ROSSEN REPORTS'], [at(B_HAND), null],
];
function chip(c, s, x, y, size, bg, fg, t, t0, rot = 0, maxW = 700, from = 1.1, font = 'Stamp') {
  if (t < t0 - SLAM) return; c.font = `${size}px ${font}`; const w = Math.min(c.measureText(s).width, maxW) + 60, h = size * 1.3, k = t < t0 ? lerp(from, 1, easeIn(land(t, t0))) : pop(t, t0);
  c.save(); c.translate(x, y); c.rotate(rot); c.scale(k, k);
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fillRect(-w / 2 + 8, -h / 2 + 10, w, h); c.restore();
  ink(c, rect(-w / 2, -h / 2, w, h), bg, 8100 + s.length, { amp: 3 }); inkText(c, s, 0, size * .06, size, font, fg, maxW); c.restore();
}
function captionsTop(c, t) {   // 760 px wide at most: +-418 even at the 1.1x landing
  let cur = null; for (const cp of CAPS) if (t >= cp[0] - SLAM) cur = cp;
  if (!cur || !cur[1]) return;
  cur.slice(1).forEach((s, i) => chip(c, s, SCX, 376 + i * 112, 66, i ? BLUE : BLK, CHIP, t, cur[0] + i * E8, i % 2 ? .012 : -.012));
}
function pushScenes(c, t, tb, A, B, dir = 1) {   // the camera moves from A to B, centred on the downbeat; dir 1 = drops (B from below), -1 = rises
  const u = easeIO(seg(t, tb - PUSH / 2, tb + PUSH / 2)), g1 = L1.getContext('2d'), g2 = L2.getContext('2d');
  contentT(g1); g1.globalAlpha = 1; A(g1, t); contentT(g1); captionsTop(g1, Math.min(t, tb - SLAM - 1e-3)); if (A.finish !== false) printFinish(g1); if (A.overlay) { contentT(g1); A.overlay(g1, t); }
  contentT(g2); g2.globalAlpha = 1; B(g2, t); contentT(g2); captionsTop(g2, Math.max(t, tb - SLAM)); if (B.finish !== false) printFinish(g2); if (B.overlay) { contentT(g2); B.overlay(g2, t); }
  c.save(); resetT(c); c.drawImage(L1, 0, -dir * u * H, W, H); c.drawImage(L2, 0, dir * (1 - u) * H, W, H); c.restore();
}

// ================= props (generic, unbranded) =================
function phone(c, x, y, s, rot, screen) {   // a plain black slab phone; screen(c) draws in local coords, screen area +-122 x +-232
  c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s);
  c.save(); c.globalAlpha = .28; c.fillStyle = BLK; c.fill(polyPath(rrPts(-140 + 14, -260 + 18, 280, 520, 44, 6))); c.restore();
  block(c, rrPts(-140, -260, 280, 520, 44, 6), BLK, 7001, { kw: 5 });
  block(c, rrPts(-122, -232, 244, 464, 22, 4), CHIP, 7002, { kw: 3, reg: false });
  c.fillStyle = BLK; c.fillRect(-30, -250, 60, 8);
  if (screen) { c.save(); c.beginPath(); c.rect(-122, -232, 244, 464); c.clip(); screen(c); c.restore(); }
  c.restore();
}
function box(c, x, y, s, open) {   // a plain shipping box: back flaps, body; open 0..1 swings the top flaps out
  c.save(); c.translate(x, y); c.scale(s, s);
  const fl = (side) => { const a = lerp(0, 2.3, easeOutBack(open)) * side; c.save(); c.translate(side * 230, -70); c.rotate(-a); block(c, rect(side > 0 ? -230 : 0, -40, 230, 40), YEL, 7011 + side, { kw: 5 }); c.restore(); };
  if (open > 0) { fl(-1); fl(1); }
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fillRect(-230 + 16, -70 + 20, 460, 250); c.restore();
  block(c, rect(-230, -70, 460, 250), YEL, 7010, { kw: 6 });
  ink(c, rect(-34, -70, 68, 250), BLUE, 7013); key(c, rect(-34, -70, 68, 250), 4, 7014);
  block(c, rect(60, 40, 130, 90), '#ffffff', 7015, { kw: 3, reg: false });
  for (let k = 0; k < 9; k++) { c.fillStyle = BLK; c.fillRect(76 + k * 11, 64, k % 3 ? 5 : 8, 44); }
  if (open <= 0) block(c, rect(-230, -78, 460, 16), YEL, 7016, { kw: 4 });
  c.restore();
}
function ringWaves(c, x, y, t, t0s, r0 = 170) { for (const t0 of t0s) { const u = seg(t, t0, t0 + .6); if (u <= 0 || u >= 1) continue;
  c.save(); c.globalAlpha = 1 - u; c.strokeStyle = YEL; c.lineWidth = 12; c.lineCap = 'round';
  for (const sd of [-1, 1]) for (let k = 0; k < 2; k++) { const r = r0 + k * 44 + 40 * u; c.beginPath(); c.arc(x, y, r, sd > 0 ? -.55 : Math.PI - .55, sd > 0 ? .55 : Math.PI + .55); c.stroke(); }
  c.restore(); } }
function dust(c, x, y, t, t0, w = 300) { const u = seg(t, t0, t0 + .45); if (u <= 0 || u >= 1) return; const r = rng(Math.round(x));
  c.save(); c.globalAlpha = .8 * (1 - u); for (let k = 0; k < 9; k++) { const sd = k % 2 ? 1 : -1, dx = sd * (w / 2 + 60 * easeOut(u) * (1 + r())), dy = -30 * easeOut(u) * r();
    block(c, ellPts(x + dx, y + dy, 16 + 14 * r(), 12 + 8 * r(), 0, 12), CHIP, 7100 + k, { kw: 3 }); } c.restore(); }
function padlock(c, x, y, s) { c.save(); c.translate(x, y); c.scale(s, s);
  c.save(); c.strokeStyle = BLK; c.lineWidth = 34; c.lineCap = 'round'; c.beginPath(); c.moveTo(-62, 0); c.lineTo(-62, -60); c.arc(0, -60, 62, Math.PI, 0); c.lineTo(62, 0); c.stroke();
  c.strokeStyle = CHIP; c.lineWidth = 12; c.beginPath(); c.moveTo(-62, -4); c.lineTo(-62, -60); c.arc(0, -60, 62, Math.PI, 0); c.lineTo(62, -4); c.stroke(); c.restore();
  block(c, rrPts(-110, -10, 220, 170, 24, 5), YEL, 7201, { kw: 7 }); block(c, ellPts(0, 55, 20, 20, 0, 16), BLK, 7202, { kw: 0, key: false }); block(c, rect(-9, 60, 18, 50), BLK, 7203, { kw: 0, key: false });
  c.restore(); }
function vault(c, x, y, t, open) {   // a plain round vault door on a wall panel (no bank, no logo)
  c.save(); c.translate(x, y);
  shadowRect(c, -330, -330, 660, 660); block(c, rect(-330, -330, 660, 660), BLK, 7301, { kw: 6 });
  // the inside: stacked cash
  ink(c, ellPts(0, 0, 270, 270, 0, 60), CHIP, 7302, { reg: false });
  for (let r = 0; r < 4; r++) for (let q = 0; q < 3; q++) { const bx = -150 + q * 100, by = -120 + r * 70; block(c, rect(bx, by, 88, 52), YEL, 7310 + r * 3 + q, { kw: 4 }); ink(c, rect(bx + 34, by, 20, 52), BLUE, 7330 + r * 3 + q, { reg: false }); }
  // the door swings open on its left hinge
  const a = easeOutBack(open), sx = Math.cos(a * 1.9);
  c.save(); c.translate(-270, 0); c.scale(sx, 1); c.translate(270, 0);
  block(c, ellPts(0, 0, 270, 270, 0, 60), sx >= 0 ? BLUE : BLK, 7303, { kw: 8 });
  if (sx >= 0) { block(c, ellPts(0, 0, 200, 200, 0, 50), BLUE, 7304, { kw: 5 });
    const rot = t * .3 + open * 3; c.save(); c.rotate(rot); c.strokeStyle = YEL; c.lineWidth = 22; c.lineCap = 'round';
    for (let k = 0; k < 3; k++) { c.save(); c.rotate(k * TAU / 3); c.beginPath(); c.moveTo(0, 0); c.lineTo(0, -150); c.stroke(); c.restore(); } c.restore();
    block(c, ellPts(0, 0, 44, 44, 0, 24), YEL, 7305, { kw: 5 }); block(c, ellPts(170, 0, 22, 22, 0, 18), BLK, 7306, { kw: 0, key: false }); block(c, rect(163, 0, 14, 40), BLK, 7307, { kw: 0, key: false }); }
  c.restore(); c.restore();
}
const KEYHOLE = [170, 10];   // relative to the vault centre, while the door is shut
function bill(c, x, y, rot, s = 1) { c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s); block(c, rect(-66, -32, 132, 64), YEL, 7401, { kw: 4 }); ink(c, rect(-12, -32, 24, 64), BLUE, 7402, { reg: false }); inkText(c, '$', -42, 3, 34, 'Stamp', BLK, 40); c.restore(); }
const PAGES = ['DAY 1', 'DAY 4', 'WEEK 2', 'WEEK 3'];
function calendar(c, x, y, t, b0) {   // a tear-off pad: a page flies off on each beat
  c.save(); c.translate(x, y);
  shadowRect(c, -130, -120, 260, 250); block(c, rect(-130, -120, 260, 250), CHIP, 7501, { kw: 5 }); ink(c, rect(-130, -120, 260, 60), BLK, 7502);
  for (const rx of [-70, 70]) block(c, ellPts(rx, -120, 12, 12, 0, 12), YEL, 7503 + rx, { kw: 3 });
  const n = Math.max(0, Math.min(PAGES.length - 1, Math.floor((t - b0 + SLAM) / BEAT)));
  inkText(c, PAGES[n], 0, 42, 64, 'Stamp', BLUE, 230);
  if (n > 0) { const u = seg(t, b0 + n * BEAT - SLAM, b0 + n * BEAT + .35); if (u < 1) { c.save(); c.translate(160 * u, -60 * u - 200 * u * u); c.rotate(.9 * u); c.globalAlpha = 1 - u;
    block(c, rect(-130, -60, 260, 190), CHIP, 7510, { kw: 4 }); inkText(c, PAGES[n - 1], 0, 42, 64, 'Stamp', BLUE, 230); c.restore(); } }
  c.restore();
}
function laptop(c, x, y, t, t0) {   // a plain laptop: the "code" is rows of bars, no readable text
  c.save(); c.translate(x, y);
  shadowRect(c, -330, -230, 660, 420); block(c, rrPts(-330, -230, 660, 420, 22, 5), BLK, 7601, { kw: 5 });
  block(c, rrPts(-300, -200, 600, 360, 10, 4), BLK, 7602, { kw: 3 });
  block(c, [[-390, 190], [390, 190], [430, 240], [-430, 240]], CHIP, 7603, { kw: 5 });
  const n = Math.max(0, Math.floor((t - t0) / E8)), r = rng(7610);
  for (let k = 0; k < Math.min(9, n + 2); k++) { const w = 120 + r() * 300, vis = k < n + 1 ? 1 : seg(t, t0 + (n) * E8, t0 + (n + 1) * E8);
    c.fillStyle = k % 3 === 2 ? BLUE : YEL; c.fillRect(-270 + (k % 4 === 1 ? 40 : 0), -170 + k * 36, w * vis, 16); }
  if (Math.floor(t * 4) % 2) { c.fillStyle = YEL; c.fillRect(-270, -170 + Math.min(9, n + 2) * 36, 22, 18); }
  c.restore();
}
function priceTag(c, x, y, rot, label, col, fg, w = 330) {   // hangs from (x, y) on a string
  c.save(); c.translate(x, y); c.rotate(rot);
  c.save(); c.strokeStyle = BLK; c.lineWidth = 4; c.beginPath(); c.moveTo(0, -120); c.lineTo(0, 0); c.stroke(); c.restore();
  const P = [[-w / 2, 20], [-w / 2 + 50, -20], [w / 2, -20], [w / 2, 110], [-w / 2 + 50, 110], [-w / 2, 70]];
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fill(polyPath(P.map(([a, b]) => [a + 10, b + 12]))); c.restore();
  block(c, P, col, 7700 + label.length, { kw: 6 }); block(c, ellPts(-w / 2 + 40, 45, 12, 12, 0, 12), CREAM, 7750, { kw: 3 });
  const L = label.split('\n');   // one or two lines, never squeezed hard
  if (L.length === 1) inkText(c, L[0], 30, 48, 52, 'Stamp', fg, w - 110); else L.forEach((s, i) => inkText(c, s, 30, 22 + i * 52, 46, 'Stamp', fg, w - 110));
  c.restore();
}
function chatBubble(c, x, y, rot, label) { c.save(); c.translate(x, y); c.rotate(rot);
  const P = [...rrPts(-170, -60, 340, 120, 30, 5)]; c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fillRect(-160, -48, 340, 120); c.restore();
  block(c, P, BLUE, 7801, { kw: 6 }); block(c, [[-100, 58], [-60, 58], [-110, 110]], BLUE, 7802, { kw: 5 }); ink(c, rect(-100, 50, 44, 12), BLUE, 7803, { reg: false });
  inkText(c, label, 0, 4, 44, 'Stamp', CHIP, 300); c.restore(); }

// ================= scenes =================
// NEW PHONE (bars 0-2): the doorstep, textured cream stock
const BOX = [480, 1230], PH0 = [480, 880], BOX_S = 1.25;
function phoneScreen(t) { return c => {
  if (t < at(1) - SLAM) { inkText(c, 'HELLO', 0, -20, 64, 'Stamp', BLUE, 220); inkText(c, 'SET UP YOUR PHONE', 0, 40, 20, SANS, BLK, 220); return; }
  if (t < at(1, 3) - SLAM) { check(c, 0, -40, .75, t, at(1)); inkText(c, 'ACTIVATED', 0, 110, 40, 'Stamp', BLK, 220); return; }
  ink(c, rect(-122, -232, 244, 90), BLUE, 7020); inkText(c, 'INCOMING CALL', 0, -186, 24, SANS, CHIP, 220);
  inkText(c, 'CARRIER', 0, -70, 46, 'Stamp', BLK, 220); inkText(c, 'SUPPORT', 0, -18, 46, 'Stamp', BLK, 220); inkText(c, FAKE_NUM, 0, 40, 22, MONO, BLK, 220);
  block(c, ellPts(-60, 160, 38, 38, 0, 24), BLK, 7021, { kw: 0, key: false }); block(c, ellPts(60, 160, 38, 38, 0, 24), YEL, 7022, { kw: 4 });
}; }
const RINGS = [at(1, 3), at(1, 4), at(2, 1)];
function sceneNewPhone(c, t) {
  creamBg(c);
  const [sx, sy] = shake(t, [[0, 18], [at(0, 3), 8]]);
  c.save(); c.translate(sx, sy);
  const open = seg(t, at(0, 3) - SLAM, at(0, 3) + .1);
  // the phone rises out of the box (hidden below the rim), then floats; it is hooked and yanked away in bar 2
  const rise = easeOut(seg(t, at(0, 4) - .1, at(1)));   // no overshoot: the phone never reaches the captions
  let px = PH0[0], py = lerp(BOX[1] + 60, PH0[1], rise) + (t > at(1) ? 8 * Math.sin((t - at(1)) * 3) : 0), prot = lerp(.1, -.03, rise), ps = lerp(.55, 1, rise);
  let jig = 0; for (const r of RINGS) if (t >= r && t < r + .4) jig += Math.sin((t - r) * 80) * .05 * (1 - (t - r) / .4);
  const hk = at(2, 2), yank = easeIn(seg(t, at(2, 3) - .05, at(2, 3) + .45));
  py -= 1500 * yank; prot += jig + 1.2 * yank;
  if (t >= at(0, 4) - .1) { c.save(); if (rise < 1) { c.beginPath(); c.rect(-2000, -2000, 5000, BOX[1] - 70 * BOX_S + 2000); c.clip(); } phone(c, px, py, ps, prot, phoneScreen(t)); c.restore(); }
  ringWaves(c, px, py, t, RINGS.filter(r => r < at(2, 3)));
  // the fishing line and hook come down for it
  if (t >= hk - .5) { const top = [px + 20, -300], dn = easeOut(seg(t, hk - .5, hk)), hy = lerp(-200, py - 280 * ps, dn); fishLine(c, top, [px, hy], 0); hook(c, px, hy, 1.4); }
  box(c, BOX[0], BOX[1], BOX_S, open);
  c.restore();
  dust(c, BOX[0], BOX[1] + 180 * BOX_S, t, 0, 460 * BOX_S);
}

// PORT HACKING (bars 3-5): the Scammer's side, one wide world; the camera pans right along the thread to the vault
const SC_AT = [250, 1430, 1.12], VAULT_AT = [1380, 930], PAN = 900;
function camPan(t) { return PAN * easeIO(seg(t, at(4) - .3, at(4) + .45)); }
const THREAD = '(555) XXX-XXXX';
function scenePort(c, t) {
  bgDots(c, BLUE, .1, .45);
  const cx = camPan(t);
  c.save(); c.translate(-cx, 0);
  const reel = -.25 + .05 * Math.sin(t * 3), glee = t > at(3, 3) ? .06 * Math.sin((t - at(3, 3)) * 14) : 0;
  const tip = scammer(c, ...SC_AT, { rod: reel, head: glee, bob: Math.abs(Math.sin(t * Math.PI / BEAT)) * 5 });
  // the stolen phone, hanging from his line, swings in from above as the camera arrives
  const arrive = easeOutBack(seg(t, at(3) - .2, at(3) + .35)), hang = [tip[0] + 40, tip[1] + 260 - (1 - arrive) * 700];
  fishLine(c, tip, [hang[0], hang[1] - 190], 12);
  const pp = [hang[0], hang[1]], sw = .08 * Math.sin(t * 2.6);
  phone(c, pp[0], pp[1], .5, sw, cc => { ink(cc, rect(-122, -232, 244, 464), BLK, 7030); inkText(cc, 'NO SERVICE', 0, 0, 34, 'Stamp', YEL, 220); });
  // the phone number, pulled out like a thread: one ransom-note chip per character, then the string runs to the vault
  const t0 = at(3, 3) - .1, t1 = at(4, 3), keyW = [VAULT_AT[0] + KEYHOLE[0], VAULT_AT[1] + KEYHOLE[1]];
  if (t >= t0) {
    const u = easeOut(seg(t, t0, t1)), start = [pp[0] + 60, pp[1] - 40], mid = [700, 700], end = keyW;
    const pt = s => { const a = 1 - s; return [a * a * start[0] + 2 * a * s * mid[0] + s * s * end[0], a * a * start[1] + 2 * a * s * mid[1] + s * s * end[1]]; };
    c.save(); c.strokeStyle = BLK; c.lineWidth = 5; c.lineCap = 'round'; c.beginPath(); for (let k = 0; k <= 40; k++) { const q = pt(u * k / 40); k ? c.lineTo(q[0], q[1]) : c.moveTo(q[0], q[1]); } c.stroke(); c.restore();
    const chars = [...THREAD];
    chars.forEach((ch, k) => { const s = (k + 1.5) / (chars.length + 2.5); if (s > u - .02) return; const q = pt(s); if (ch !== ' ') ransomLetter(c, ch, q[0], q[1] + 4, 80, k, .15 * Math.sin(k * 1.7 + t * 3)); });
  }
  // the vault opens on beat 3 of bar 4; cash streams out on eighths in bar 5; the calendar tears
  const open = seg(t, at(4, 3) - SLAM, at(4, 3) + .35);
  vault(c, ...VAULT_AT, t, open);
  if (t >= at(5) - SLAM) { for (let k = 0; k < 8; k++) { const tk = at(5) + k * E8, u = seg(t, tk - .1, tk + .9); if (u <= 0 || u >= 1) continue;
      bill(c, lerp(VAULT_AT[0] - 40, VAULT_AT[0] - 1100, easeIn(u)), VAULT_AT[1] - 60 + (k % 3 - 1) * 70 - 260 * Math.sin(u * Math.PI), u * 6 * (k % 2 ? 1 : -1), 1.1); }
    calendar(c, VAULT_AT[0] + 250, 740, t, at(5)); }
  c.restore();
}
function vaultRect() { const x = VAULT_AT[0] - PAN; return [x - 270, VAULT_AT[1] - 270, 540, 540]; }

// THE FIX (bars 6-7): a laptop, Jeff and the magnifier; then the phone gets its padlock
const LAP = [480, 900];   // below the three-line caption of bar 6 (its third chip ends at y 647)
function sceneFix(c, t) {   // bar 6: the laptop typing; Jeff's magnifier on 2; a padlock slams onto it on 3; a check on 4
  bgDots(c, BLUE, .06, .3);
  const [sx, sy] = shake(t, [[at(6, 3), 14]]);
  c.save(); c.translate(sx, sy); laptop(c, LAP[0], LAP[1], t, at(6)); c.restore();
  const jin = easeOutBack(land(t, at(6, 2))), raise = easeOut(seg(t, at(6, 2), at(6, 2) + .35)), lower = easeIn(seg(t, at(6, 3) - SLAM, at(6, 3))), up = raise * (1 - lower);
  const th = easeOutBack(seg(t, at(6, 3), at(6, 3) + .35));
  if (t >= at(6, 2) - SLAM) {
    const J = jeff(c, 176, lerp(3000, 1830, jin), .66, { armR: lerp(lerp(0, -2.2, up), -2.5, th), prop: th > .6 ? 'thumb' : null, head: -.05 + .03 * Math.sin(t * 2) });
    if (up > 0) { const cxm = lerp(J.hand[0] + 80, LAP[0] + 90, up), cym = lerp(J.hand[1] - 120, LAP[1] - 40, up) + 8 * Math.sin(t * 3);
      magnifier(c, cxm, cym, lerp(40, 120, up), J.hand, up > .6 ? () => { c.translate(cxm, cym); c.scale(1.8, 1.8); c.translate(-cxm, -cym); laptop(c, LAP[0], LAP[1], t, at(6)); } : null); }
  }
  if (t >= at(6, 3) - SLAM) { const k = t < at(6, 3) ? lerp(1.4, 1, easeIn(land(t, at(6, 3)))) : pop(t, at(6, 3)); padlock(c, LAP[0] + sx, LAP[1] + 40 + sy, 1.1 * k); }
  check(c, 740, 770, .7, t, at(6, 4));
}

// DEALS (bar 7): brighter; tags swing in on each beat
const TAGS = [['40% OFF', 265, 720, YEL, BLK, 320], ['PROMO\nCODE', 690, 700, BLUE, CHIP, 300], ['AMAZON\nDEALS', 262, 1000, CHIP, BLK, 300]], TAG_S = 1.2;   // AMAZON as plain text only
function sceneDeals(c, t) {
  bgDots(c, YEL, .14, .5);
  TAGS.forEach(([s, x, y, col, fg, w], k) => { const t0 = at(7, 1 + k); 
    if (t < t0 - SLAM) return; const kp = t < t0 ? lerp(.6, 1, easeOut(land(t, t0))) : pop(t, t0), swing = t > t0 ? .14 * Math.exp(-(t - t0) * 2.2) * Math.sin((t - t0) * 9) : 0;   // each tag pops in place: nothing travels past the captions
    c.save(); c.translate(x, y); c.scale(TAG_S * kp, TAG_S * kp); priceTag(c, 0, 0, swing + (k % 2 ? .05 : -.05), s, col, fg, w); c.restore(); });
  if (t >= at(7, 4) - SLAM) { const k = pop(t, at(7, 4)); c.save(); c.translate(690, 1010); c.scale(k * TAG_S, k * TAG_S); chatBubble(c, 0, 0, .04, 'YOUR REQUESTS'); c.restore(); }   // x 486-894: clear of the tags and the safe edge
  const th = easeOutBack(seg(t, at(7, 1.5), at(7, 2)));
  jeff(c, SCX, 1830, .7, { armR: lerp(0, -2.5, th), prop: th > .6 ? 'thumb' : null, head: .05 * Math.sin(t * 5), bob: Math.abs(Math.sin(t * Math.PI / BEAT)) * 6 });
}

// LIVE ON YOUTUBE (bar 8): a plain video player (no platform logo) with Jeff live inside; LIVE on 2; the channel row on 3;
// a chat bubble on 4. "YouTube" appears only as plain text in the caption.
// AMAZON PROMO CODES (bars 8-9), on the approved textured cream. The official Amazon logo (assets/tease/amazon_logo_official.png,
// supplied by the client) sits on a card, drawn exactly as supplied: uniform scale only, no recolour, and it is drawn AFTER the print
// finish so nothing covers it. Three code tickets slide out from behind the card (bottom slot first, so none passes another)
// on 8:2, 8:3, 8:4; a REVEALED LIVE stamp covers each code on 9:1, 9:2, 9:3; Jeff gives a thumbs up on 9:4. No real codes.
const AZ = { x: 160, y: 585, w: 640, h: 220 }, AZ_LW = 520;
const TICKETS = [['PROMO CODE', 1170, at(8, 2), at(9, 1)], ['SECRET CODE', 1030, at(8, 3), at(9, 2)], ['HIDDEN CODE', 890, at(8, 4), at(9, 3)]];
const azPop = t => t < at(8) ? 1 : 1 + .04 * Math.exp(-(t - at(8)) * 12) * Math.cos((t - at(8)) * 30);
function ticket(c, label, y, t, tStamp, k) {   // 720 x 130, centred; the label and the hidden code sit either side of the tear line
  c.save(); c.translate(SCX, y);
  c.save(); c.globalAlpha = .28; c.fillStyle = BLK; c.fillRect(-360 + 10, -65 + 12, 720, 130); c.restore();
  block(c, rect(-360, -65, 720, 130), CHIP, 9600 + k, { kw: 5 });
  c.save(); c.strokeStyle = BLK; c.lineWidth = 4; c.setLineDash([12, 10]); c.beginPath(); c.moveTo(-90, -58); c.lineTo(-90, 58); c.stroke(); c.restore();
  inkText(c, label, -225, 5, 44, 'Stamp', BLUE, 240);
  inkText(c, '? ? ? ? ?', 135, 7, 52, MONO, BLK, 400);
  if (t >= tStamp - SLAM) { const s2 = t < tStamp ? lerp(1.12, 1, easeIn(land(t, tStamp))) : pop(t, tStamp);   // lands inside the code area (at most 381 px wide): never over the label
    c.save(); c.translate(135, 0); c.rotate(-.04); c.scale(s2, s2);
    c.save(); c.globalAlpha = .45; c.fillStyle = BLK; c.fillRect(-170 + 7, -44 + 8, 340, 88); c.restore();
    block(c, rect(-170, -44, 340, 88), YEL, 9610 + k, { kw: 5 }); inkText(c, 'REVEALED LIVE', 0, 4, 42, 'Stamp', BLK, 310); c.restore(); }
  c.restore();
}
function sceneAmazon(c, t) {
  creamBg(c);
  TICKETS.forEach(([label, y, t0, ts], k) => { if (t < t0 - .4) return; const u = easeOut(seg(t, t0 - .4, t0));
    ticket(c, label, lerp(AZ.y + AZ.h / 2, y, u), t, ts, k); sparkle(c, 830, y - 62, 40, t, t0); });
  const k = azPop(t); c.save(); c.translate(SCX, AZ.y + AZ.h / 2); c.scale(k, k); c.translate(-SCX, -(AZ.y + AZ.h / 2));
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fillRect(AZ.x + 12, AZ.y + 16, AZ.w, AZ.h); c.restore();
  block(c, rrPts(AZ.x, AZ.y, AZ.w, AZ.h, 24, 5), '#ffffff', 9620, { kw: 6, reg: false }); c.restore();
  const th = easeOutBack(seg(t, at(9, 4) - SLAM, at(9, 4) + .2)), pt = easeOut(seg(t, at(8, 2) - SLAM, at(8, 2)));
  jeff(c, 150, 1860, .62, { armR: th > 0 ? lerp(-1.6, -2.5, th) : lerp(0, -1.6, pt), prop: th > .6 ? 'thumb' : pt > .5 ? 'point' : null, head: .04 * Math.sin(t * 4), bob: Math.abs(Math.sin(t * Math.PI / BEAT)) * 4 });
}
sceneAmazon.overlay = (c, t) => {   // the official logo: after the finish, never covered
  const im = IMG.amazon, lh = im.height * AZ_LW / im.width, k = azPop(t);
  c.save(); c.translate(SCX, AZ.y + AZ.h / 2); c.scale(k, k); c.drawImage(im, -AZ_LW / 2, -lh / 2 + 4, AZ_LW, lh); c.restore();
};

const PL = { x: 110, y: 600, w: 740, h: 416 };
const popUp = (t, t0) => t < t0 ? lerp(.8, 1, easeOut(land(t, t0))) : pop(t, t0);   // grows into place: never wider than its resting size (+6%)
function sceneLive(c, t) {
  bgDots(c, BLUE, .08, .4);
  const { x, y, w, h } = PL;
  shadowRect(c, x, y, w, h); block(c, rect(x, y, w, h), BLK, 7901, { kw: 6 });
  c.save(); c.beginPath(); c.rect(x + 14, y + 14, w - 28, h - 28); c.clip();
  ink(c, rect(x, y, w, h), CREAM, 7902, { reg: false }); dotsIn(c, rect(x, y, w, h), YEL, .35, 7903, 14);
  jeff(c, x + w / 2, y + h + 60, .46, { armR: -2.35 + .22 * Math.sin(t * TAU / BEAT), head: .05 * Math.sin(t * 3), bob: Math.abs(Math.sin(t * Math.PI / BEAT)) * 5 });
  c.restore();
  // the progress bar: at the live edge
  ink(c, rect(x + 30, y + h - 36, w - 60, 10), CHIP, 7904, { reg: false }); ink(c, rect(x + 30, y + h - 36, w - 60, 10), YEL, 7905, { reg: false });
  if (t >= at(B_LIVE, 2) - SLAM) { const k = popUp(t, at(B_LIVE, 2)); c.save(); c.translate(x + 110, y + 62); c.scale(k, k);
    block(c, rrPts(-80, -30, 160, 60, 12, 4), BLK, 7906, { kw: 3 }); block(c, ellPts(-46, 0, 12, 12, 0, 14), YEL, 7907, { kw: 0, key: false });
    inkText(c, 'LIVE', 16, 3, 38, 'Stamp', YEL, 90); c.restore(); }
  if (t >= at(B_LIVE, 3) - SLAM) { const k = popUp(t, at(B_LIVE, 3)); c.save(); c.translate(SCX, 1120); c.scale(k, k);
    c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fillRect(-370 + 10, -60 + 12, 740, 120); c.restore();
    block(c, rect(-370, -60, 740, 120), CHIP, 7908, { kw: 5 });
    stickerLogo(c, -285, 0, 130, -.04, 1);
    inkText(c, 'ROSSEN REPORTS', -200, -14, 50, 'Stamp', BLK, 540, 'left'); inkText(c, 'CHANNEL  ·  10 AM ET', -200, 36, 34, SANS, BLUE, 540, 'left');
    c.restore(); }
  if (t >= at(B_LIVE, 4) - SLAM) { const k = popUp(t, at(B_LIVE, 4)); c.save(); c.translate(SCX + 60, 1300); c.scale(k * 1.1, k * 1.1); chatBubble(c, 0, 0, -.03, 'SEE YOU AT 10!'); c.restore(); }
}

// HANDOFF (bar 11): the loop's own page. Its background is the loop's (same code, same seed); its pieces are cut from the
// loop's own frames with masks, land on the beats in their exact places, and from PIECE_T[5] + .1 the whole loop frame
// is shown, so the last tease frame is loop frame 119 and the next frame is the loop's own frame 0.
const LOOP_F0 = 60;   // loop frames 60-119 play under the handoff bar (loop time = t - at(B_HAND - 1))
const PIECE_T = [at(B_HAND, 1), at(B_HAND, 2), at(B_HAND, 3), at(B_HAND, 3), at(B_HAND, 4), at(B_HAND, 4)];   // logo, LIVE TODAY, the time card + FRIDAY, LIVE ON YOUTUBE + Jeff: each on a beat (and a whole frame)
let MASKS = null, PLATE = null; const SCRATCH = layer();   // its own scratch layer: L1/L2 carry the camera pushes
const loopFrame = t => IMG['loop' + Math.min(119, Math.max(LOOP_F0, Math.round((t - at(B_HAND - 1)) * FPS)))];
function sceneHandoff(c, t) {
  screenSpace(c, () => {
    const full = t >= PIECE_T[5] + .1, im = loopFrame(t);
    if (full) { c.drawImage(im, 0, 0, W, H); return; }
    c.drawImage(PLATE, 0, 0, W, H);   // the loop's background, finish included
    MASKS.forEach((m, k) => {
      const t0 = PIECE_T[k]; if (t < t0 - SLAM) return;
      const g = SCRATCH.getContext('2d'); g.setTransform(1, 0, 0, 1, 0, 0); g.globalCompositeOperation = 'source-over'; g.clearRect(0, 0, SCRATCH.width, SCRATCH.height);
      g.drawImage(im, 0, 0, SCRATCH.width, SCRATCH.height); g.globalCompositeOperation = 'destination-in'; g.drawImage(m.cv, 0, 0, SCRATCH.width, SCRATCH.height); g.globalCompositeOperation = 'source-over';
      const [mx, my] = m.c; let k2 = 1, dy = 0;
      if (m.name === 'jeff') dy = (1 - easeOut(land(t, t0))) * 700;   // Jeff rises from below, no overshoot: he never passes over FRIDAY
      else k2 = t < t0 ? lerp(.8, 1, easeOut(land(t, t0))) : 1 + .02 * Math.exp(-(t - t0) * 12) * Math.cos((t - t0) * 30);   // the rest pop in place, never bigger than the loop's own frame (+2%): nothing travels over another piece
      c.save(); c.translate(mx, my + dy); c.scale(k2, k2); c.translate(-mx, -my); c.drawImage(SCRATCH, 0, 0, W, H); c.restore();
    });
  });
}
sceneHandoff.finish = false;   // the loop's pixels already carry the print finish

// ================= assembly =================
function drawScene(c, t) {
  contentT(c);
  if (Q.has('plate')) { screenSpace(c, () => { bgDots(c, BLUE, .12, .55); printFinish(c); }); return; }
  if (t < at(3) - PUSH / 2) { sceneNewPhone(c, t); contentT(c); captionsTop(c, t); printFinish(c); }
  else if (t < at(3) + PUSH / 2) pushScenes(c, t, at(3), sceneNewPhone, scenePort, -1);   // the camera follows the phone up
  else if (t < at(6)) { scenePort(c, t); contentT(c); captionsTop(c, t); printFinish(c); }
  else if (t < at(6) + .45) { zoomThrough(c, t, at(6), at(6) + .45, vaultRect(), g => scenePort(g, at(6) - 1e-3), g => sceneFix(g, t));
    contentT(c); captionsTop(c, t); printFinish(c); }   // dive into the vault; the caption stays full size on top (never inside the zooming window)
  else if (t < at(7) - PUSH / 2) { sceneFix(c, t); contentT(c); captionsTop(c, t); printFinish(c); }
  else if (t < at(7) + PUSH / 2) pushScenes(c, t, at(7), sceneFix, sceneDeals);
  else if (t < at(8) - PUSH / 2) { sceneDeals(c, t); contentT(c); captionsTop(c, t); printFinish(c); }
  else if (t < at(8) + PUSH / 2) pushScenes(c, t, at(8), sceneDeals, sceneAmazon);
  else if (t < at(B_LIVE) - PUSH / 2) { sceneAmazon(c, t); contentT(c); captionsTop(c, t); printFinish(c); contentT(c); sceneAmazon.overlay(c, t); }
  else if (t < at(B_LIVE) + PUSH / 2) pushScenes(c, t, at(B_LIVE), sceneAmazon, sceneLive);
  else if (t < at(B_HAND) - PUSH / 2) { sceneLive(c, t); contentT(c); captionsTop(c, t); printFinish(c); }
  else if (t < at(B_HAND) + PUSH / 2) pushScenes(c, t, at(B_HAND), sceneLive, sceneHandoff);
  else sceneHandoff(c, t);
  if (SHOW_SAFE) safeOverlay(c);
}

// ================= runtime =================
const CV = document.getElementById('c'); CV.width = OUT_W; CV.height = OUT_H; const CTX = CV.getContext('2d');
function frame(i) { const t = Math.min(i / FPS, DUR - 1e-6); FILM_T = t; resetT(CTX); CTX.globalAlpha = 1; drawScene(CTX, t); resetT(CTX); }
window.__NFR = NFR; window.__FPS = FPS; window.__frame = i => { frame(i); return CV.toDataURL('image/png'); };
(async () => {
  await loadPrintKit(); await loadVertKit(); makeCream(); await loadImg('amazon', 'assets/tease/amazon_logo_official.png');
  const pad = n => String(n).padStart(4, '0');
  await Promise.all([...Array(60).keys()].map(k => loadImg('loop' + (LOOP_F0 + k), `out/rossen-loop-friday-youtube/frames/${pad(LOOP_F0 + k)}.png`)));
  if (!Q.has('plate')) { const M = await (await fetch('assets/tease/loop_masks.json')).json();
  MASKS = await Promise.all(M.pieces.map(async (p, k) => { await loadImg('mask' + k, `assets/tease/${p.file}`); const cv = document.createElement('canvas'); cv.width = OUT_W; cv.height = OUT_H; cv.getContext('2d').drawImage(IMG['mask' + k], 0, 0, OUT_W, OUT_H); return { cv, c: p.centre, name: p.name }; })); }
  PLATE = document.createElement('canvas'); PLATE.width = OUT_W; PLATE.height = OUT_H; { const g = PLATE.getContext('2d'); g.setTransform(OUT_W / W, 0, 0, OUT_H / H, 0, 0); bgDots(g, BLUE, .12, .55); printFinish(g); }
  frame(+(Q.get('frame') || 0));
  window.__ready = true;
})().catch(e => { console.error(e); window.__error = String(e); });
