'use strict';
/* Wednesday live-show tease: a 1.9 s intro title card (a 3-beat pickup), then 30 s (12 bars at 96 BPM, D, the loop's tempo and key), 1080x1920 (9:16), 24 fps, one
   continuous film, then the approved 5 s LIVE TODAY loop (rossen-loop-wednesday, 5 PM ET) is appended untouched and plays twice (41.9 s).
   Times below are film time: the intro runs from -1.875 s, so video time = film time + 1.875 s.
   Case-file screen-print look (printkit.js), the approved palette (printkit.js: BLUE, BLK, YEL, CREAM, CHIP), the vertical
   safe-zone content transform (VERT_K 0.895, like the loop). Three car scams, teased, not explained; the red flags and the
   fixes are saved for the show. One short ALL-CAPS card per bar (the promise's card holds for its two bars). A card lands on
   its downbeat, sits level and dead still, and leaves before any transition starts: nothing moves across the words and no
   transition runs while one is up.

   INTRO      pickup -1.9  the title card: the official logo, 3 CAR SCAMS, LIVE WEDNESDAY · 5 PM ET, a little yellow car   (the title)
                           drives in and parks on beat 3; the words and logo fade and the driveway dissolves in, done as bar 0's card lands
   OIL SCAM   bar 0  0.0   the man's car, FOR SALE $10,000 in the windshield, from frame 0; the Scammer rises in on 3    "SELLING YOUR CAR?"
              bar 1  2.5   he fans cash in the man's face; the sidekick tiptoes in, the hood pops on 2, he pours on 3   "WHILE YOU'RE / DISTRACTED..."
              bar 2  5.0   a smoke puff on 1; the man's jaw drops on 2; the price flips to $0 on 3                  "YOUR CAR: / WORTHLESS"
                           (4) the engine smoke billows across the whole frame and clears onto a laptop
   FAKE DEALER bar 3 7.5   the website builds itself: the name on 1, the dream car on 2, five stars on 3, reviews and    "BUYING A CAR / ONLINE?"
                           PAY NOW on 4; (4&) the camera zooms into the screen
              bar 4  10.0  a hand taps PAY NOW on 1; PAID on 2; on 3 a corner of the page curls: it is a painted flat     "THE DEALERSHIP / ISN'T REAL"
                           (4&) the page swings away like a stage set and the camera pulls back onto an empty lot
              bar 5  12.5  the Scammer leans out from behind the flat on 1 and waves the cash; a dashed outline where     "THE CAR / DOESN'T EXIST"
                           the dream car should be; a tumbleweed on 3; (4&) the camera drops to a mailbox
   CLONED PLATE bar 6 15.0 the mailbox bursts on 1; tickets stack on the eighths; the total counts up to $3,000+ on 4    "$3,000 / IN TICKETS"
                           (4&) the camera zooms into the top ticket
              bar 7  17.5  the camera photo: a flash on 1; a car that is not his, with his plate ABC-0000, the Scammer    "IT'S NOT / YOUR CAR"
                           at the wheel; a marker circle round the plate on 3
              bar 8  20.0  the plate peels off the photo on 1-2 and flutters down on 3: a paper copy, taped on; 4 is      "SOMEONE COPIED / YOUR PLATE"
                           still and silent
   PROMISE    bars 9-10 22.5 cut with the card: Jeff rises with his magnifier on 9:1; it settles on the oil can on 9:3,    "WE'LL SHOW YOU / THE RED FLAGS."
                           the fake site on 10:1 and the paper plate on 10:3 (no flags and no fixes shown); (10:4&) the camera
                           drops to the loop
   HANDOFF    bar 11 27.5  the loop's own page; its pieces land on the beats in their exact places (logo on 1, LIVE TODAY on 2,
                           5 PM ET + WEDNESDAY on 3, LIVE ON YOUTUBE + Jeff on 4), and from 29.6 s it is the loop's own frames,
                           so the cut at 30.0 s is the loop's seamless wrap.
   Nothing here is real: a generic car, an invented dealership (TOTALLY REAL MOTORS), plate ABC-0000, no phone numbers or URLs.
*/
const B_JEFF = 9, B_HAND = 11;   // the promise gets two bars (9-10): long enough to read its card twice
const INTRO = 3 * BEAT;   // the intro title card: a 3-beat pickup (1.875 s) before bar 0; film time t runs from -INTRO
const DUR = at(12), NFR = Math.round(FPS * (INTRO + DUR));
const TR_INTRO = [-BEAT, -SLAM];   // after beat 3 the driveway dissolves in under the title card (0.49 s)
const INTRO_FADE = [-BEAT, -BEAT + .22];   // the title card's words and logo fade out, after 1.25 s dead still
const introA = t => 1 - easeIO(seg(t, ...INTRO_FADE));
const MONO = '"Liberation Mono"', PLATE_NO = 'ABC-0000', DEALER = 'TOTALLY REAL MOTORS';
// transitions: each runs between two cards, ending as the next card starts to land (never while a card is up)
const TR = {
  smoke: [at(2, 4) - .06, at(3) - SLAM], zoomSite: [at(4) - .36, at(4) - SLAM], swing: [at(5) - .52, at(5) - SLAM],
  toMail: [at(6) - .34, at(6) - SLAM], zoomTicket: [at(7) - .36, at(7) - SLAM], toLoop: [at(B_HAND) - .34, at(B_HAND) - SLAM],
};
const SMOKE_MID = (TR.smoke[0] + TR.smoke[1]) / 2 + .06;   // the frame is fully covered: the scene underneath changes here

// ================= captions =================
// [land time, time it leaves, line 1, line 2]; both lines land together, on the downbeat, and then hold dead still. All sit level.
const CAPS = [
  [at(0), at(1) - SLAM, 'SELLING YOUR CAR?'], [at(1), at(2) - SLAM, "WHILE YOU'RE", 'DISTRACTED...'], [at(2), TR.smoke[0], 'YOUR CAR:', 'WORTHLESS'],
  [at(3), TR.zoomSite[0], 'BUYING A CAR', 'ONLINE?'], [at(4), TR.swing[0], 'THE DEALERSHIP', "ISN'T REAL"], [at(5), TR.toMail[0], 'THE CAR', "DOESN'T EXIST"],
  [at(6), TR.zoomTicket[0], '$3,000', 'IN TICKETS'], [at(7), at(8) - SLAM, "IT'S NOT", 'YOUR CAR'], [at(8), at(B_JEFF) - SLAM, 'SOMEONE COPIED', 'YOUR PLATE'],
  [at(B_JEFF), TR.toLoop[0], "WE'LL SHOW YOU", 'THE RED FLAGS.'],
];
const capPop = (t, t0) => t < t0 ? lerp(1.05, 1, easeIn(land(t, t0))) : 1;   // scale only, level, from 1.05x: lands ON the beat and is still from that frame (SKILL_NOTES 0)
const gentle = capPop;   // the same landing for every readable prop label
function chip(c, s, x, y, size, bg, fg, t, t0, maxW = 740) {
  if (t < t0 - SLAM) return; c.font = `${size}px Stamp`; const w = Math.min(c.measureText(s).width, maxW) + 60, h = size * 1.3, k = capPop(t, t0);
  c.save(); c.translate(x, y); c.scale(k, k);
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fillRect(-w / 2 + 8, -h / 2 + 10, w, h); c.restore();
  ink(c, rect(-w / 2, -h / 2, w, h), bg, 8100 + s.length, { amp: 3 }); inkText(c, s, 0, size * .06, size, 'Stamp', fg, maxW); c.restore();
}
function captionsTop(c, t) {   // drawn after the print finish: solid ink, no texture inside the letters
  for (const cp of CAPS) { const [t0, t1] = cp; if (t < t0 - SLAM || t >= t1) continue;
    cp.slice(2).forEach((s, i) => chip(c, s, SCX, 372 + i * 116, 72, i ? BLUE : BLK, CHIP, t, t0)); }   // 72 px: the standing 70-76 px caption size
}
const capOn = t => CAPS.some(([t0, t1]) => t >= t0 - SLAM && t < t1);

// ================= small helpers =================
const sy = y => SCY + (y - SCY) * K;
function twos(t) {   // 12 drawings a second, but every beat frame (15 frames apart) is drawn exactly, so landings stay on the beat
  const f = Math.round(t * FPS), b = Math.floor(f / 15) * 15; if (f === b) return t;
  return Math.max(b, f - (((f % 2) + 2) % 2)) / FPS;
}
const breath = (t, ph = 0) => .012 * Math.sin(t * 2.2 + ph);   // a slow breath (±1.2 %), each character on its own phase
const lag = (t, t0, a = .14) => t < t0 ? 0 : -a * Math.exp(-(t - t0) * 7) * Math.sin((t - t0) * 17);   // overlap: a head that trails a landing, then settles   // content y -> screen y (backgrounds are drawn full-frame in screen space)
function ground(c, yC, o = {}) {   // pavement: flat paper, a black kerb line and a few drawn joints; no dots (the sky carries the texture)
  screenSpace(c, () => { const y = sy(yC); ink(c, rect(-20, y, W + 40, H - y + 20), CREAM, 5200, { reg: false });
    key(c, [[-20, y], [W + 20, y]], 6, 5202, false);
    if (o.kerb !== false) key(c, [[-20, y + 96], [W + 20, y + 96]], 4, 5203, false);                                     // the kerb edge of a sidewalk
    if (o.joints !== false) for (let k = 0; k < 6; k++) { const x = 40 + k * 200; key(c, [[x, y + 8], [x - 22, y + 90]], 3, 5204 + k, false); } });   // slab joints
}
function starPts(cx, cy, r, rot = 0) { const p = []; for (let k = 0; k < 10; k++) { const a = -Math.PI / 2 + rot + k * Math.PI / 5, rr = k % 2 ? r * .45 : r; p.push([cx + Math.cos(a) * rr, cy + Math.sin(a) * rr]); } return p; }
function shine(c, x, y, r, t, t0, seed = 1) {   // a four-point sparkle that pops in on t0 and twinkles
  if (t < t0 - SLAM) return; const k = pop(t, t0) * (1 + .12 * Math.sin((t - t0) * 9 + seed));
  c.save(); c.translate(x, y); c.scale(k, k); const P = [[0, -r], [r * .22, -r * .22], [r, 0], [r * .22, r * .22], [0, r], [-r * .22, r * .22], [-r, 0], [-r * .22, -r * .22]];
  block(c, P, YEL, 5300 + seed, { kw: 3 }); c.restore();
}
function tapRingC(c, x, y, t, t0, col = BLK) { const u = seg(t, t0, t0 + .4); if (u <= 0 || u >= 1) return; c.save(); c.globalAlpha = 1 - u; c.strokeStyle = col; c.lineWidth = 8; c.beginPath(); c.arc(x, y, 26 + 80 * easeOut(u), 0, TAU); c.stroke(); c.restore(); }
function wadOfCash(c, x, y, s, rot, fan) {   // a fanned wad of bills held at (x, y)
  c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s);
  for (let k = 0; k < 5; k++) { c.save(); c.rotate((k - 2) * .2 * fan); c.translate(0, -70);
    block(c, rect(-44, -70, 88, 140), YEL, 5401 + k, { kw: 4 }); ink(c, rect(-44, -12, 88, 24), BLUE, 5410 + k, { reg: false }); block(c, ellPts(0, 0, 18, 22, 0, 16), CHIP, 5420 + k, { kw: 3 });
    c.restore(); }
  c.restore();
}
function mitten(c, x, y, s, rot) { c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s); block(c, ellPts(0, 0, 42, 36, 0, 26), BLUE, 5431, { kw: 5 }); block(c, ellPts(-30, -20, 16, 13, -.6, 16), BLUE, 5432, { kw: 4 }); c.restore(); }

// ================= puppets =================
// the man (the car owner): the jointed puppet cut for the officer film (assets/officer/man_*); his gasp head is the same
// head with the smile repainted as an open "O" (tools/cut_sidekick.py)
let MANP = null, SKP = null;
function man(c, x, y, s, p = {}) {
  const M = MANP; c.save(); c.translate(x, y); c.rotate(p.tilt || 0); c.scale(s * (p.sx || 1), s * (1 + (p.breath || 0))); c.translate(-M.feet[0], -M.feet[1] - (p.bob || 0));
  const part = (k, a = 0, img = null, hs = null) => { const m = M.parts[k], [px, py] = m.pivot; c.save(); c.translate(px, py); c.rotate(a); if (hs) c.scale(hs[0], hs[1]); c.translate(-px, -py); c.drawImage(img || IMG['man_' + k], m.x, m.y); c.restore(); };
  part('legL', p.legL || 0); part('legR', p.legR || 0); part('torso'); part('head', p.head || 0, p.gasp ? IMG.man_gasp : null, p.headS); part('arm', p.arm || 0);
  c.restore();
}
// the Scammer's sidekick: cut from the user's drawing (assets/wedtease/sidekick_*). The oil can is its own piece, held in the
// hand: pose { head, arm (the hand, at the cuff), can (the can in the hand), legL, legR, bob, tilt, sx } -> the spout tip
function sidekick(c, x, y, s, p = {}) {
  const M = SKP, base = c.getTransform();
  c.save(); c.translate(x, y); c.rotate(p.tilt || 0); c.scale(s * (p.sx || 1), s * (1 + (p.breath || 0))); c.translate(-M.feet[0], -M.feet[1] - (p.bob || 0));
  const draw = k => { const m = M.parts[k]; c.drawImage(IMG['sk_' + k], m.x, m.y); };
  const pv = (k, a) => { const [px, py] = M.parts[k].pivot; c.translate(px, py); c.rotate(a); c.translate(-px, -py); };
  for (const k of ['legL', 'legR']) { c.save(); pv(k, p[k] || 0); draw(k); c.restore(); }
  draw('torso');
  c.save(); pv('arm', p.arm || 0); c.save(); pv('can', p.can || 0); draw('can');
  const q = base.inverse().multiply(c.getTransform()).transformPoint(new DOMPoint(...M.tip)); c.restore(); draw('arm'); c.restore();
  c.save(); pv('head', p.head || 0); draw('head'); c.restore();
  c.restore(); return [q.x, q.y];
}
// the Scammer (the explainer puppet, assets/explainer/scammer_*) without his fishing rod: the rod piece carries both his
// hands, so here his hands are blue mittens in his own ink, one on a sleeve that can reach, holding a fanned wad of bills.
// pose { head, legL, legR, bob, tilt, sx, hand: [x, y] in the caller's coordinates or null, cashRot, fan }
function scammerCash(c, x, y, s, p = {}) {
  const base = c.getTransform();
  c.save(); c.translate(x, y); c.rotate(p.tilt || 0); c.scale(s * (p.sx || 1), s * (1 + (p.breath || 0))); c.translate(-SP.feet[0], -SP.feet[1] - (p.bob || 0));
  const part = (k, a = 0) => { const m = SP.parts[k], [px, py] = m.pivot; c.save(); c.translate(px, py); c.rotate(a); c.translate(-px, -py); c.drawImage(IMG['s_' + k], m.x, m.y); c.restore(); };
  part('legL', p.legL || 0); part('legR', p.legR || 0); part('torso');
  mitten(c, 872, 676, 1.3, .3);   // the resting hand, where the reel was
  const toLocal = base.multiply(c.getTransform().inverse()), SH = [965, 580];   // shoulder of the reaching arm, in his reference
  let hand = p.hand ? (() => { const q = c.getTransform().inverse().multiply(base).transformPoint(new DOMPoint(...p.hand)); return [q.x, q.y]; })() : [1010, 640];
  c.save(); c.lineCap = 'round'; c.strokeStyle = BLK; c.lineWidth = 78; c.beginPath(); c.moveTo(...SH); c.lineTo(...hand); c.stroke(); c.strokeStyle = YEL; c.lineWidth = 8; c.globalAlpha = .9;
  c.beginPath(); c.moveTo(SH[0] + 30, SH[1]); c.lineTo(hand[0] + 30, hand[1]); c.stroke(); c.restore();   // the coat sleeve, with his yellow trim
  if (p.cash !== false) wadOfCash(c, hand[0], hand[1] - 10, 1.6, p.cashRot || 0, p.fan ?? 1);
  mitten(c, hand[0], hand[1], 1.5, p.cashRot || 0);
  part('head', p.head || 0);
  c.restore(); void toLocal;
}

// ================= props (generic, unbranded) =================
// a generic sedan in side view, facing left; (x, y) = the ground under its middle. o: { col, hood 0..1, sign: {price, droop, flip} }
const CAR_HOOD = [-175, -198], CAR_CAP = [-252, -206];
function sedan(c, x, y, s, o = {}) {
  const col = o.col || YEL, f = o.len || 1; c.save(); c.translate(x, y); c.scale(s * f, s);   // len < 1: a shorter car (round parts are drawn unsquashed)
  const round = (px, py, fn) => { c.save(); c.translate(px, py); c.scale(1 / f, 1); fn(); c.restore(); };
  c.save(); c.globalAlpha = .28; c.fillStyle = BLK; c.beginPath(); c.ellipse(0, -4, 330, 20, 0, 0, TAU); c.fill(); c.restore();
  block(c, [[-175, -196], [-95, -312], [148, -312], [238, -196]], col, 5501, { kw: 6 });
  ink(c, [[-152, -204], [-86, -292], [-14, -292], [-14, -204]], CHIP, 5502, { reg: false }); key(c, [[-152, -204], [-86, -292], [-14, -292], [-14, -204]], 4, 5503);
  ink(c, [[12, -204], [12, -292], [138, -292], [202, -204]], CHIP, 5504, { reg: false }); key(c, [[12, -204], [12, -292], [138, -292], [202, -204]], 4, 5505);
  if (o.shine) for (const [a, b] of [[-120, -226], [40, -226]]) ink(c, [[a, b], [a + 30, b - 50], [a + 46, b - 50], [a + 16, b]], '#ffffff', 5506 + a, { reg: false });
  if (o.hood > 0) { ink(c, rect(-316, -206, 146, 32), BLK, 5507, { reg: false }); block(c, rect(-296, -224, 96, 30), BLUE, 5508, { kw: 4 }); round(...CAR_CAP, () => block(c, ellPts(0, 0, 14, 10, 0, 14), CHIP, 5509, { kw: 3 })); }
  block(c, rrPts(-322, -200, 644, 142, 34), col, 5510, { kw: 6 });
  ink(c, rect(-320, -140, 640, 16), col === BLUE ? YEL : BLUE, 5511);
  key(c, [[-14, -196], [-14, -76]], 4, 5512, false); key(c, [[180, -196], [180, -84]], 4, 5513, false);
  for (const hx of [-70, 112]) block(c, rect(hx, -170, 44, 11), BLK, 5514 + hx, { kw: 0, key: false });
  round(-312, -168, () => block(c, ellPts(0, 0, 12, 18, 0, 14), CHIP, 5515, { kw: 3 })); block(c, rect(306, -172, 16, 28), BLK, 5516, { kw: 0, key: false });
  for (const [bx, bw] of [[-336, 74], [262, 74]]) block(c, rrPts(bx, -96, bw, 28, 12), BLK, 5517 + bx, { kw: 0, key: false });
  for (const wx of [-200, 205]) round(wx, -60, () => { block(c, ellPts(0, 0, 64, 64, 0, 36), BLK, 5520 + wx, { kw: 0, key: false }); block(c, ellPts(0, 0, 28, 28, 0, 20), CHIP, 5521 + wx, { kw: 4 }); });
  if (o.hood > 0) {   // the hood, hinged at the windshield, lifts at the front
    c.save(); c.translate(...CAR_HOOD); c.rotate(1.15 * easeOutBack(o.hood)); ink(c, [[4, 8], [-148, 10], [-148, 26], [4, 24]], BLK, 5529, { reg: false }); block(c, [[4, -8], [-150, -6], [-150, 12], [4, 12]], col, 5530, { kw: 5 }); c.restore();
  }
  if (o.sign) round(-40, -250, () => forSale(c, 0, 0, o.sign));
  c.restore();
}
function forSale(c, x, y, sg) {   // the FOR SALE card taped in the windshield; its price flips like a split-flap
  c.save(); c.translate(x, y); c.rotate(-.03 + (sg.droop || 0));
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fillRect(-86 + 6, -58 + 8, 172, 116); c.restore();
  block(c, rect(-86, -58, 172, 116), CHIP, 5601, { kw: 5 }); ink(c, rect(-86, -58, 172, 40), BLK, 5602, { reg: false });
  inkText(c, 'FOR SALE', 0, -36, 30, 'Stamp', CHIP, 150);
  const f = sg.flip ?? 1, old = sg.old || '$10,000', nu = sg.price || old;   // flip 0..1: the old price folds away, the new one unfolds
  const s = f < .5 ? 1 - f * 2 : (f - .5) * 2, txt = f < .5 ? old : nu;
  c.save(); c.translate(0, 22); c.scale(1, Math.max(.02, s)); inkText(c, txt, 0, 2, 42, 'Stamp', BLUE, 150); c.restore();
  for (const tx of [-80, 80]) { c.save(); c.translate(tx, -56); c.rotate(tx > 0 ? .5 : -.5); ink(c, rect(-18, -7, 36, 14), YEL, 5603 + tx, { reg: false }); c.restore(); }
  c.restore();
}
function puff(c, x, y, r, seed, a = 1) {   // a paper-cutout smoke cloud: cream stock, black keyline, a grey tint
  const q = rng(seed), P = []; const n = 9;
  for (let k = 0; k < n; k++) { const ang = k / n * TAU + q() * .3; P.push([x + Math.cos(ang) * r * (.7 + q() * .25), y + Math.sin(ang) * r * (.62 + q() * .2)]); }
  c.save(); c.globalAlpha = a;
  for (const [px, py] of P) block(c, ellPts(px, py, r * .42, r * .38, 0, 22), CHIP, seed + Math.round(px), { kw: 5 });
  block(c, ellPts(x, y, r * .78, r * .66, 0, 30), CHIP, seed + 1, { kw: 0, key: false }); dotsIn(c, ellPts(x, y + r * .2, r * .7, r * .4, 0, 26), BLK, .12, seed + 2, 10);
  c.restore();
}

// the fake dealership's website, drawn in its own 660 x 400 page coordinates. st: build state (each 0..1 or a time)
function site(c, t, st) {
  ink(c, rect(0, 0, 660, 400), CHIP, 5701, { reg: false });
  if (st.name && t >= at(3, 2) - SLAM) { const k = st.name(t); c.save(); c.translate(330, 32); c.scale(k, k); ink(c, rect(-330, -32, 660, 64), BLUE, 5702, { reg: false }); inkText(c, DEALER, 0, 3, 36, 'Stamp', CHIP, 600); c.restore(); }
  if (st.car) { const k = st.car(t); c.save(); c.translate(205, 200); c.scale(k, k); c.translate(-205, -200);
    dotsIn(c, rect(20, 84, 370, 232), YEL, .35, 5703, 10); key(c, rect(20, 84, 370, 232), 4, 5704);
    sedan(c, 205, 294, .5, { col: BLUE, shine: true }); c.restore();
    shine(c, 90, 130, 22, t, st.carT, 1); shine(c, 330, 150, 16, t, st.carT + S16, 2); shine(c, 300, 270, 14, t, st.carT + E8, 3); }
  (st.stars || []).forEach((t0, i) => { if (t < t0 - SLAM) return; const k = pop(t, t0); c.save(); c.translate(438 + i * 46, 110); c.scale(k, k); block(c, starPts(0, 0, 20), YEL, 5710 + i, { kw: 3 }); c.restore(); });
  if (st.reviews && t >= st.reviews - SLAM) [150, 224].forEach((by, i) => { const k = pop(t, st.reviews + i * S16); c.save(); c.translate(525, by + 30); c.scale(k, k); c.translate(-525, -(by + 30));
    block(c, rrPts(412, by, 226, 62, 14), '#ffffff', 5720 + i, { kw: 4, reg: false }); for (let j = 0; j < 5; j++) ink(c, starPts(430 + j * 20, by + 18, 8), YEL, 5725 + j, { reg: false });
    ink(c, rect(430, by + 34, 150, 8), BLK, 5730 + i, { reg: false }); ink(c, rect(430, by + 47, 110, 8), BLK, 5732 + i, { reg: false }); c.restore(); });
  if (st.pay && t >= st.pay - SLAM) { const k = gentle(t, st.pay), paid = st.paid && t >= st.paid - SLAM; c.save(); c.translate(525, 345); c.scale(k, k);
    block(c, rrPts(-113, -34, 226, 68, 20), paid ? BLUE : YEL, 5740, { kw: 5 }); inkText(c, paid ? 'PAID' : 'PAY NOW', paid ? -14 : 0, 3, 36, 'Stamp', paid ? CHIP : BLK, 190);
    if (paid) { c.save(); c.translate(70, 0); c.scale(.28 * gentle(t, st.paid), .28 * gentle(t, st.paid)); block(c, [[-90, -5], [-40, 45], [95, -95], [120, -65], [-40, 105], [-120, 25]], YEL, 5741, { kw: 10 }); c.restore(); }
    c.restore(); }
}
function laptop(c, x, y) {   // lid + screen frame + deck; the screen is 660 x 400 at (x - 330, y - 220)
  c.save(); c.translate(x, y);
  shadowRect(c, -360, -250, 720, 460); block(c, rrPts(-360, -250, 720, 470, 24), BLK, 5801, { kw: 5 });
  block(c, [[-400, 218], [400, 218], [446, 268], [-446, 268]], CHIP, 5802, { kw: 5 }); ink(c, rect(-90, 222, 180, 12), BLK, 5803, { reg: false });
  c.restore();
}
const LAP = [480, 960], SCR = [LAP[0] - 330, LAP[1] - 220, 660, 400];
const SITE_BUILD = { name: t => gentle(t, at(3, 2)), car: t => pop(t, at(3)), carT: at(3), stars: [0, 1, 2, 3, 4].map(k => at(3, 3) + k * S16 / 2), reviews: at(3, 4), pay: at(3, 4) + E8 };
const SITE_FULL = Object.assign({}, SITE_BUILD, { paid: at(4, 2) });

// ================= scenes =================
// OIL SCAM (bars 0-2): the driveway. The car faces left; the sidekick works at the hood, the Scammer faces the man.
const CAR = [800, 1340], CAR_LEN = .9, MAN = [150, 1352, .56], SCAM = [318, 1352, .56], SK = [578, 1352, .44];   // left to right: the man, the Scammer facing him, the car (hood at its left end; its tail runs off the right edge), the sidekick behind it
const MAN_FACE = [126, 988], OILK = 1.1, OILP = [480, 1352];   // the driveway is staged small, then shown 1.1x about the frame's centre line
const oilPt = ([x, y]) => [OILP[0] + (x - OILP[0]) * OILK, OILP[1] + (y - OILP[1]) * OILK];
function sceneOil(c, tRaw) {
  const t = twos(tRaw);   // the puppets and cut-outs, on twos
  bgDots(c, BLUE, .03, .18); ground(c, 1345);
  c.save(); c.translate(...OILP); c.scale(OILK, OILK); c.translate(-OILP[0], -OILP[1]);
  const puffT = at(2), [shx, shy] = shake(t, [[puffT, 16], [puffT + E8, 10], [puffT + BEAT, 8]]);
  const hood = seg(t, at(1, 2) - SLAM, at(1, 2) + .2);
  const flip = seg(t, at(2, 3) - SLAM, at(2, 3)), droop = .16 * easeOutBack(seg(t, at(2, 3), at(2, 3) + .3));
  // the sidekick sneaks in behind the car (bar 1, beats 1-2), leans over the engine and pours on 3; jumps back from the smoke on 2:1
  let tip = null, pour = 0;
  if (t >= at(1) - .3) {   // he pops up from behind the car on 1:1 (clipped at the car's sill, so nothing shows under it)
    const rise = easeOutBack(seg(t, at(1) - .3, at(1) + .05)), x = SK[0], step = 0, walk = 1;
    c.save(); c.beginPath(); c.rect(-2000, -2000, 5000, 2000 + CAR[1] - 20); c.clip();
    const lean = .12 * easeIO(seg(t, at(1, 2) + .1, at(1, 3) - .05)) * (1 - easeOut(seg(t, puffT - .05, puffT + .15)) * 1.6);
    pour = easeIO(seg(t, at(1, 3) - SLAM, at(1, 3))) * (1 - easeIO(seg(t, puffT - .05, puffT + .2)));
    const glee = t > puffT ? .06 * Math.sin((t - puffT) * 16) : 0;
    tip = sidekick(c, x, SK[1], SK[2], { tilt: lean, can: 1.9 * pour, arm: .2 * pour, head: glee + .04 * Math.sin(t * 3) + lag(t, at(1) + .05, .18), bob: -(1 - rise) * 640, breath: breath(t, 2) });
    c.restore();
  }
  c.save(); c.translate(shx, shy);   // the car stands in front of him: only his top half shows over it
  sedan(c, ...CAR, 1, { len: CAR_LEN, hood, sign: { price: '$0', flip, droop } });
  c.restore();
  {
    if (tip && pour > .6 && t < puffT) {   // the oil: a black stream from the spout into the engine, glugging on the eighths
      const cap = [CAR[0] + CAR_CAP[0] * CAR_LEN, CAR[1] + CAR_CAP[1]], g = 1 + .35 * Math.sin((t - at(1, 3)) * TAU / E8);
      c.save(); c.strokeStyle = BLK; c.lineCap = 'round'; c.lineWidth = 10 * g; c.beginPath(); c.moveTo(tip[0], tip[1]); c.quadraticCurveTo(tip[0] + 10, (tip[1] + cap[1]) / 2, cap[0], cap[1]); c.stroke(); c.restore();
      const n = Math.floor((t - at(1, 3)) / E8); for (let k = 0; k <= n; k++) { const u = seg(t, at(1, 3) + k * E8, at(1, 3) + k * E8 + .2); if (u > 0 && u < 1) block(c, ellPts(lerp(tip[0], cap[0], u), lerp(tip[1], cap[1], u), 11, 14, 0, 14), BLK, 5901 + k, { kw: 0, key: false }); }
    }
  }
  // the man: he turns to the buyer; follows the cash; his jaw drops on 2:2
  const gasp = t >= at(2, 2), jump = gasp ? 26 * Math.exp(-(t - at(2, 2)) * 6) * Math.abs(Math.cos((t - at(2, 2)) * 12)) : 0;
  const follow = t >= at(1) && t < at(2) ? .05 * Math.sin((t - at(1)) * TAU / E8 * .5) : 0;
  const GT = at(2, 2), squint = t >= GT - .1 && t < GT, take = t >= GT ? .12 * Math.exp(-(t - GT) * 9) * Math.cos((t - GT) * 22) : 0;   // anticipation, then a take that overshoots and settles
  const turn = easeOutBack(seg(t, at(0, 3) - .05, at(0, 3) + .25)) * .06;   // he turns to the buyer as he rises in, with a little overshoot
  man(c, MAN[0], MAN[1] - jump, MAN[2], { gasp: t >= GT, headS: squint ? [1.06, .9] : [1 - take * .5, 1 + take], head: turn + follow - (t >= GT ? .1 : 0) + .02 * Math.sin(t * 2.1), bob: Math.abs(Math.sin(t * Math.PI / (2 * BEAT))) * 3, breath: breath(t) });
  // the Scammer rises in on 0:3 holding up the cash; fans it in the man's face on the eighths of bar 1
  if (t >= at(0, 3) - SLAM) {
    const a = easeOutBack(land(t, at(0, 3))), yy = lerp(2300, SCAM[1], a), reach = easeOutBack(seg(t, at(1) - SLAM, at(1))) * (1 - easeIO(seg(t, puffT, puffT + .3)))   // the cash pulls back on the puff, so his face is clear for the jaw drop;
    const fanW = t >= at(1) && t < at(2) ? Math.sin((t - at(1)) * TAU / E8 * .5) : 0;
    const hand = [lerp(SCAM[0] - 70, MAN_FACE[0] + 70, reach) + 14 * fanW, lerp(SCAM[1] - 330, MAN_FACE[1] + 150, reach)];   // the wad fans up over his face
    const smug = t > puffT ? .05 * Math.sin((t - puffT) * 12) : .03 * Math.sin(t * 3);
    scammerCash(c, SCAM[0], yy, SCAM[2], { sx: -1, hand: [hand[0], hand[1] + (yy - SCAM[1])], cashRot: .25 * fanW + .2 * reach, fan: 1 + .25 * Math.abs(fanW), head: smug + lag(t, at(0, 3)), bob: Math.abs(Math.sin(t * Math.PI / BEAT)) * 4, breath: breath(t, 4) });
  }
  // the smoke puff on 2:1, then the engine keeps coughing on the beats
  const cap = [CAR[0] + CAR_CAP[0] * CAR_LEN + shx, CAR[1] + CAR_CAP[1] + shy];
  if (t >= puffT - SLAM) {
    const u = seg(t, puffT - SLAM, puffT + .5); puff(c, cap[0] - 150 * easeOut(u), cap[1] - 60 - 230 * easeOut(u), lerp(40, 150, easeOut(u)), 6001, t < puffT + 1.2 ? 1 : 1 - seg(t, puffT + 1.2, puffT + 1.6));
    for (let b = 1; b < 4; b++) { const tb = at(2, b + 1), v = seg(t, tb - .05, tb + .8); if (v <= 0 || v >= 1) continue; puff(c, cap[0] - 40 - 120 * v, cap[1] - 40 - 240 * v, lerp(30, 80, v), 6010 + b, 1 - v * v); }
  }
  c.restore();
}
function smokeWall(c, t) {   // the engine smoke billows across the whole frame (screen space), then clears
  const [t0, t1] = TR.smoke, uIn = easeIn(seg(t, t0, SMOKE_MID)), uOut = easeIn(seg(t, SMOKE_MID, t1));
  if (uIn <= 0 || uOut >= 1) return;
  screenSpace(c, () => { const [cx0, cy0] = oilPt([CAR[0] + CAR_CAP[0] * CAR_LEN, CAR[1] + CAR_CAP[1]]), ox = CX + (cx0 - SCX) * K, oy = sy(cy0), r = rng(6100);
    for (let k = 0; k < 26; k++) { const ang = r() * TAU, d = 250 + r() * 1100, tx = ox + Math.cos(ang) * d * .8, ty = oy + Math.sin(ang) * d * 1.1 - 200;
      const e = clamp01(uIn * 1.4 - k * .012), R = lerp(40, 520 + r() * 180, e) * (1 - uOut * (0.6 + .4 * r())), dx = uOut * (tx - ox) * .9 + uOut * 700 * Math.cos(ang), dy = uOut * (ty - oy) * .9 - uOut * 600;
      if (R <= 4) continue; puff(c, lerp(ox, tx, e) + dx, lerp(oy, ty, e) + dy, R, 6200 + k); } });
}

// FAKE DEALERSHIP (bars 3-5)
function sceneSiteBuild(c, t) {   // bar 3: the laptop; the site builds itself
  creamBg(c);   // close-ups on the approved textured cream
  laptop(c, ...LAP);
  c.save(); c.beginPath(); c.rect(...SCR); c.clip(); c.translate(SCR[0], SCR[1]); site(c, t, SITE_BUILD); c.restore();
  if (t < at(3, 4) + E8 + .2 && Math.floor(t * 8) % 2) { c.fillStyle = BLK; c.fillRect(SCR[0] + 620, SCR[1] + 360, 16, 26); }   // a blinking cursor while it builds
}
const PAGE = { x: 60, y: 620, w: 840, h: 553 }, PG_S = 840 / 660;   // bar 4: the page fills the width; a browser bar on top
const PAGE_L = layer(PAGE.w, PAGE.h);
function pageDraw(g, t) {   // into its own layer: browser bar (no address, no logo), the site, and the corner curl on 4:3
  g.save(); g.setTransform(S, 0, 0, S, 0, 0); g.clearRect(0, 0, PAGE.w, PAGE.h);
  block(g, rect(0, 0, PAGE.w, PAGE.h), BLK, 5810, { kw: 0, key: false });
  ink(g, rect(0, 0, PAGE.w, 44), BLK, 5811, { reg: false }); for (let k = 0; k < 3; k++) block(g, ellPts(26 + k * 30, 22, 9, 9, 0, 14), [YEL, CHIP, BLUE][k], 5812 + k, { kw: 0, key: false });
  block(g, rrPts(130, 10, 560, 24, 12), CHIP, 5815, { kw: 0, key: false, reg: false });
  g.save(); g.translate(0, 44); g.scale(PG_S, PG_S); site(g, t, SITE_FULL); g.restore();
  const curl = easeOutBack(seg(t, at(4, 3) - SLAM, at(4, 3) + .1)) * 110;   // the top-right corner folds down: plain board behind it
  if (curl > 1) { const x = PAGE.w, y = 44;
    ink(g, [[x - curl, y], [x, y], [x, y + curl]], BLK, 5820, { reg: false });
    block(g, [[x - curl, y], [x - curl, y + curl], [x, y + curl]], CHIP, 5821, { kw: 4, reg: false });
    for (let k = 1; k < 4; k++) key(g, [[x - curl + 8, y + curl * k / 4], [x - curl * (1 - k / 4) - 4, y + curl * k / 4]], 2, 5822 + k, false); }
  key(g, rect(3, 3, PAGE.w - 6, PAGE.h - 6), 6, 5830);
  g.restore();
}
function drawPage(c, t, a, sc, hx, hy) {   // the page on its left hinge at (hx, hy middle), swung by a (0 = flat to camera), scaled sc; far edge shortens
  pageDraw(PAGE_L.getContext('2d'), t);
  const N = 36, cw = Math.cos(a), taper = .28 * Math.sin(a);
  c.save(); c.globalAlpha = .28; c.fillStyle = BLK; c.beginPath(); c.moveTo(hx + 14, hy - PAGE.h * sc / 2 + 18); c.lineTo(hx + PAGE.w * sc * cw + 14, hy - PAGE.h * sc * (1 - taper) / 2 + 18); c.lineTo(hx + PAGE.w * sc * cw + 14, hy + PAGE.h * sc * (1 - taper) / 2 + 18); c.lineTo(hx + 14, hy + PAGE.h * sc / 2 + 18); c.fill(); c.restore();
  for (let i = 0; i < N; i++) { const u0 = i / N, f = 1 - taper * (u0 + .5 / N), sx0 = u0 * PAGE.w, sw = PAGE.w / N;
    c.drawImage(PAGE_L, sx0 * S, 0, sw * S + 1, PAGE.h * S, hx + sx0 * sc * cw, hy - PAGE.h * sc * f / 2, sw * sc * cw + .8, PAGE.h * sc * f); }
  if (a > .05) { c.save(); c.globalAlpha = .25 * Math.sin(a); c.fillStyle = BLK; c.beginPath(); c.moveTo(hx, hy - PAGE.h * sc / 2); c.lineTo(hx + PAGE.w * sc * cw, hy - PAGE.h * sc * (1 - taper) / 2); c.lineTo(hx + PAGE.w * sc * cw, hy + PAGE.h * sc * (1 - taper) / 2); c.lineTo(hx, hy + PAGE.h * sc / 2); c.fill(); c.restore(); }
}
const PAY_AT = [PAGE.x + 525 * PG_S, PAGE.y + 44 + 345 * PG_S];
function pointer(c, x, y, rot, s = 1) {   // the man's hand, pointing: his yellow skin, his blue sleeve; fingertip at (x, y)
  c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s);
  block(c, rect(-60, 150, 120, 260), BLUE, 5851, { kw: 6 }); block(c, rrPts(-64, 60, 128, 120, 40), YEL, 5852, { kw: 6 });
  block(c, rrPts(-20, 0, 40, 100, 20), YEL, 5853, { kw: 5 }); for (let k = 0; k < 3; k++) key(c, [[-40 + k * 26, 70], [-40 + k * 26, 100]], 3, 5854 + k, false);
  c.restore();
}
function sceneSite(c, t) {   // bar 4: the page; the tap on 1; PAID on 2; the corner curls on 3
  creamBg(c);
  const wob = t > at(4, 3) ? .012 * Math.exp(-(t - at(4, 3)) * 5) * Math.sin((t - at(4, 3)) * 22) : 0;
  c.save(); c.translate(PAGE.x, PAGE.y + PAGE.h); c.rotate(wob); c.translate(-PAGE.x, -(PAGE.y + PAGE.h)); drawPage(c, t, 0, 1, PAGE.x, PAGE.y + PAGE.h / 2); c.restore();
  const tap = at(4), inn = easeOut(seg(t, tap - .5, tap)), out = easeIn(seg(t, tap + .25, tap + .7)), press = t >= tap && t < tap + .12 ? 10 : 0;
  if (t > tap - .5 && out < 1) pointer(c, PAY_AT[0] + 10, lerp(1900, PAY_AT[1], inn) + press + 800 * out, -.18);
  tapRingC(c, ...PAY_AT, t, tap);
}
const FLAT = { a: 1.18, sc: .8, hx: 40, hy: 960 };   // where the page ends up: a painted flat standing in the lot
const GHOST = [650, 1390, .72];
function sceneLot(c, tRaw, withFlat = true) {
  const t = twos(tRaw);   // bar 5: the empty lot behind the flat; the Scammer waves from behind it
  bgDots(c, BLUE, .03, .18); ground(c, 1195, { joints: false });
  for (const [x0, x1] of [[330, 280], [940, 890]]) screenSpace(c, () => block(c, [[CX + (x0 - SCX) * K, sy(1205)], [CX + (x0 - SCX) * K + 22, sy(1205)], [CX + (x1 - SCX) * K + 30, H + 10], [CX + (x1 - SCX) * K, H + 10]], YEL, 6301 + x0, { kw: 0, key: false }));
  // where the dream car should be: a dashed outline, nothing inside
  c.save(); c.translate(GHOST[0], GHOST[1]); c.scale(GHOST[2], GHOST[2]); c.strokeStyle = BLK; c.lineWidth = 11; c.setLineDash([28, 18]); c.lineJoin = 'round';
  c.beginPath(); for (const [a, b] of [[-322, -60], [-322, -170], [-280, -200], [-175, -200], [-95, -312], [148, -312], [238, -200], [322, -190], [322, -60]]) c.lineTo(a, b); c.closePath(); c.stroke();
  for (const wx of [-200, 205]) { c.beginPath(); c.arc(wx, -60, 62, 0, TAU); c.stroke(); } c.restore();
  // the flat's brace and sandbag, behind it
  const fx = FLAT.hx + PAGE.w * FLAT.sc * Math.cos(FLAT.a), top = FLAT.hy - PAGE.h * FLAT.sc * (1 - .28 * Math.sin(FLAT.a)) / 2, bot = FLAT.hy + PAGE.h * FLAT.sc * (1 - .28 * Math.sin(FLAT.a)) / 2;
  block(c, [[fx - 16, top + 30], [fx + 4, top + 30], [fx + 150, bot + 8], [fx + 124, bot + 8]], BLK, 6310, { kw: 4 }); block(c, [[fx - 6, bot - 14], [fx - 6, bot + 4], [fx + 150, bot + 4], [fx + 150, bot - 14]], BLK, 6311, { kw: 4 });
  block(c, rrPts(fx + 96, bot - 24, 80, 38, 16), YEL, 6312, { kw: 4 });
  // the Scammer, behind the flat: leans out on 1, waves the cash on 2, 3, 4
  if (t >= at(5) - .3) { const out = easeOutBack(seg(t, at(5) - .1, at(5) + .25)), wave = Math.sin((t - at(5)) * TAU / BEAT);
    scammerCash(c, lerp(fx - 150, fx + 10, out), 1235, .8, { tilt: .14 * out, hand: [lerp(fx - 40, fx + 230, out) + 50 * wave, 840 + 24 * Math.abs(wave)], cashRot: .35 * wave, fan: 1.2, head: .05 * Math.sin(t * 5) + lag(t, at(5) + .25), breath: breath(t, 4) }); }
  // a tumbleweed rolls through the empty space on 3
  { const u = seg(t, at(5, 3) - .45, at(5, 4) + .2); if (u > 0 && u < 1) { const x = lerp(980, 340, u), y = 1380 - 70 * Math.abs(Math.sin(u * Math.PI * 3)); c.save(); c.translate(x, y); c.rotate(-u * 9);
    c.strokeStyle = BLK; c.lineWidth = 6; c.lineCap = 'round'; const r = rng(6320); for (let k = 0; k < 11; k++) { c.beginPath(); c.arc((r() - .5) * 30, (r() - .5) * 30, 26 + r() * 30, r() * TAU, r() * TAU + 2.6); c.stroke(); } c.restore(); } }
  if (withFlat) drawPage(c, t, FLAT.a, FLAT.sc, FLAT.hx, FLAT.hy);
}
function swing(c, t) {   // 4 -> 5: the page swings back on its left hinge like a stage flat; the camera pulls back onto the lot
  const u = easeIO(seg(t, ...TR.swing));
  sceneLot(c, t, false);
  const a = FLAT.a * u, sc = lerp(1, FLAT.sc, u), hx = lerp(PAGE.x, FLAT.hx, u), hy = lerp(PAGE.y + PAGE.h / 2, FLAT.hy, u);
  if (u < .35) { screenSpace(c, () => { c.save(); c.globalAlpha = 1 - u / .35; c.restore(); }); }
  drawPage(c, at(5) - .6, a, sc, hx, hy);
}

// CLONED PLATE (bars 6-8)
const BOX = [260, 1060], MOUTH = [BOX[0] + 170, BOX[1] + 10], STACK = [660, 1400];
const MAILK = 1.3, MAILP = [470, 1400], mailPt = ([x, y]) => [MAILP[0] + (x - MAILP[0]) * MAILK, MAILP[1] + (y - MAILP[1]) * MAILK];
const TICKET_T = [...Array(7).keys()].map(k => at(6) + k * E8);
const TOTALS = ['$900', '$1,800', '$3,000+'];   // on beats 2, 3, 4
function ticket(c, x, y, rot, s, seed) { c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s);
  c.save(); c.globalAlpha = .25; c.fillStyle = BLK; c.fillRect(-140 + 6, -80 + 8, 280, 160); c.restore();
  block(c, rect(-140, -80, 280, 160), CHIP, 6400 + seed, { kw: 4 }); ink(c, rect(-140, -80, 280, 30), BLK, 6401 + seed, { reg: false });
  ink(c, rect(-120, -34, 90, 70), BLK, 6402 + seed, { tint: .5, cell: 8 }); for (let k = 0; k < 3; k++) ink(c, rect(-16, -30 + k * 22, 130 - k * 26, 9), BLK, 6403 + seed + k, { reg: false });
  block(c, rect(40, 40, 80, 28), YEL, 6408 + seed, { kw: 3 }); c.restore(); }
const stackPos = k => [STACK[0] + ((k * 37) % 3 - 1) * 14, STACK[1] - 90 - k * 30, ((k * 53) % 5 - 2) * .04];
function mailbox(c, t) {
  block(c, rect(BOX[0] - 22, BOX[1] + 90, 44, 290), BLK, 6501, { kw: 4 });
  const P = [[-170, 100], [-170, -30], ...[...Array(13).keys()].map(k => { const a = Math.PI + k / 12 * Math.PI; return [Math.cos(a) * 170, -30 + Math.sin(a) * 100]; }), [170, 100]].map(([a, b]) => [BOX[0] + a, BOX[1] + b]);
  block(c, P, BLUE, 6502, { kw: 6 });
  const flag = easeOutBack(seg(t, at(6) - SLAM, at(6) + .1)); c.save(); c.translate(BOX[0] - 100, BOX[1] + 20); c.rotate(-Math.PI / 2 * flag);
  block(c, rect(-8, -8, 150, 18), YEL, 6503, { kw: 4 }); block(c, rect(110, -40, 40, 34), YEL, 6504, { kw: 4 }); c.restore();
  const door = easeOutBack(seg(t, at(6) - SLAM, at(6) + .08)); c.save(); c.translate(BOX[0] + 170, BOX[1] + 100); c.rotate(-1.9 * door * -1);
  block(c, [[-10, 0], [10, 0], [10, -200], [-10, -200]], BLUE, 6505, { kw: 5 }); c.restore();
  if (door > .2) ink(c, ellPts(MOUTH[0] - 4, MOUTH[1] + 10, 18, 80, 0, 24), BLK, 6506, { reg: false });
}
function sceneMail(c, tRaw) {   // bar 6
  const t = twos(tRaw);
  creamBg(c); ground(c, 1400);   // a close-up on the approved textured cream (and no yellow field: yellow stays a small accent)
  c.save(); c.translate(...MAILP); c.scale(MAILK, MAILK); c.translate(-MAILP[0], -MAILP[1]);
  mailbox(c, t);
  TICKET_T.forEach((t0, k) => { const [x, y, r] = stackPos(k), u = seg(t, t0 - .34, t0);
    if (u <= 0) return; const e = easeIn(u), px = lerp(MOUTH[0], x, e), py = lerp(MOUTH[1], y, e) - 110 * Math.sin(u * Math.PI);   // a low arc: never up into the total tag
    ticket(c, px, py, lerp(-.8 + k * .3, r, e), lerp(.5, 1, e), k * 10); });
  // the burst: loose tickets fly up out of the box on 1 and flutter away (behind nothing, clear of the card)
  for (let k = 0; k < 4; k++) { const u = seg(t, at(6) - .05, at(6) + .9); if (u <= 0 || u >= 1) continue; ticket(c, MOUTH[0] - (60 + k * 50) * easeOut(u), MOUTH[1] - 200 * Math.sin(u * 2.2) + 120 * u * k * .3, u * 4 * (k % 2 ? 1 : -1), .55, 100 + k * 10); }
  c.restore();
  // the running total, on a yellow tag that stays put
  const n = [2, 3, 4].filter(b => t >= at(6, b) - SLAM).length;
  if (n) { const b = n, k = gentle(t, at(6, b + 1)); c.save(); c.translate(700, 690); c.scale(k, k); c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fillRect(-150 + 8, -52 + 10, 300, 104); c.restore();
    block(c, [[-150, -52], [130, -52], [150, 0], [130, 52], [-150, 52]], YEL, 6510, { kw: 5 }); inkText(c, TOTALS[b - 1], -8, 5, 56, 'Stamp', BLK, 250); c.restore(); }
}
const topTicketRect = () => { const [x, y] = mailPt(stackPos(6)); return [x - 140 * MAILK, y - 80 * MAILK, 280 * MAILK, 160 * MAILK]; };
// the big ticket (bars 7-8): a camera photo of a car that is not his, his plate on it, the Scammer at the wheel
const TK = { x: 90, y: 560, w: 780, h: 850 }, PH = { x: 140, y: 690, w: 680, h: 480 };
const PLATE = { x: 480, y: 1084, w: 240, h: 120 };   // a plate's 2:1 proportions   // the plate on the photo (content coords)
function plateCard(c, x, y, s, rot, back = false, paper = false) {   // the plate: ABC-0000 on an embossed plate (no real state design);
  // it is a paper printout taped on: back = its blank back, paper = seen for what it is (cut edge, curl, tape)
  c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s);
  const w = PLATE.w, h = PLATE.h;
  if (paper) { c.save(); c.globalAlpha = .25; c.fillStyle = BLK; c.fillRect(-w / 2 + 8, -h / 2 + 10, w, h); c.restore(); }
  else if (!back) block(c, rrPts(-w / 2 - 9, -h / 2 - 9, w + 18, h + 18, 18), BLK, 6600, { kw: 0, key: false });   // the plate holder
  block(c, rrPts(-w / 2, -h / 2, w, h, 12), back ? CHIP : '#ffffff', 6601, { kw: 4, reg: false });
  if (!back) {
    key(c, rrPts(-w / 2 + 8, -h / 2 + 8, w - 16, h - 16, 8), 3, 6602);                                             // the stamped rim
    ink(c, rect(-w / 2 + 14, -h / 2 + 14, w - 28, 10), BLUE, 6603, { reg: false });                                // a plain band across the top (no words)
    ink(c, rect(-w / 2 + 14, h / 2 - 22, w - 28, 6), BLUE, 6604, { reg: false });
    for (const bx of [-62, 62]) { block(c, ellPts(bx, -h / 2 + 34, 7, 7, 0, 14), CHIP, 6605 + bx, { kw: 3, reg: false }); key(c, [[bx - 4, -h / 2 + 34], [bx + 4, -h / 2 + 34]], 2, 6606 + bx, false); }   // the two bolts
    block(c, rrPts(w / 2 - 50, -h / 2 + 30, 30, 22, 4), YEL, 6607, { kw: 2 });                                     // a registration sticker, blank
    c.save(); c.globalAlpha = .3; inkText(c, PLATE_NO, 3, 16, 60, 'Stamp', BLK, w - 44); c.restore(); inkText(c, PLATE_NO, 0, 12, 60, 'Stamp', BLK, w - 44);   // embossed characters
  } else for (let k = 0; k < 4; k++) ink(c, rect(-w / 2 + 16, -h / 2 + 20 + k * 20, w - 32 - (k % 2) * 50, 3), BLK, 6608 + k, { reg: false, tint: .6, cell: 4 });
  if (paper) { c.save(); c.strokeStyle = BLK; c.lineWidth = 3; c.setLineDash([10, 8]); c.strokeRect(-w / 2 - 6, -h / 2 - 6, w + 12, h + 12); c.restore();   // the scissor line of a printout
    block(c, [[w / 2 - 40, h / 2], [w / 2, h / 2 - 40], [w / 2, h / 2]], CHIP, 6612, { kw: 3 }); }                // a curled corner
  for (const [tx, ty, r] of [[-w / 2, -h / 2, -.6], [w / 2, -h / 2, .6]]) { c.save(); c.translate(tx, ty); c.rotate(r); ink(c, rect(-24, -9, 48, 18), YEL, 6610 + tx, { reg: false }); c.restore(); }
  c.restore();
}
function frontCar(c, x, y, s) {   // a generic car from the front, blue (his car is yellow), the Scammer at the wheel
  c.save(); c.translate(x, y); c.scale(s, s);
  block(c, [[-170, -150], [-120, -262], [120, -262], [170, -150]], BLUE, 6701, { kw: 6 });
  const WS = [[-148, -156], [-108, -244], [108, -244], [148, -156]]; ink(c, WS, CHIP, 6702, { reg: false });
  c.save(); c.clip(polyPath(WS)); const m = SP.parts.head, hs = .42; c.drawImage(IMG.s_head, -m.w * hs / 2 + 10, -250, m.w * hs, m.h * hs); dotsIn(c, WS, BLUE, .12, 6703, 8); c.restore(); key(c, WS, 5, 6704);
  block(c, rrPts(-260, -160, 520, 150, 36), BLUE, 6705, { kw: 6 });
  for (const hx of [-190, 190]) block(c, ellPts(hx, -110, 40, 26, 0, 20), CHIP, 6706 + hx, { kw: 4 });
  block(c, rrPts(-110, -126, 220, 40, 10), BLK, 6708, { kw: 0, key: false }); for (let k = 0; k < 5; k++) ink(c, rect(-96 + k * 42, -118, 24, 24), CHIP, 6709 + k, { reg: false, tint: .4, cell: 6 });
  block(c, rrPts(-270, -40, 540, 34, 14), BLK, 6715, { kw: 0, key: false });
  for (const wx of [-200, 200]) block(c, rrPts(wx - 40, -10, 80, 50, 12), BLK, 6716 + wx, { kw: 0, key: false });
  ink(c, rect(-104, -82, 208, 104), BLK, 6718, { reg: false });   // the plate's recess: bare once the paper comes off
  c.restore();
}
const PEEL = [at(8) - SLAM, at(8, 2) + .1], DROP = [at(8, 2) + .1, at(8, 3)], REST = [640, 1290, .1];
function sceneTicket(c, t) {   // bars 7-8
  creamBg(c);
  shadowRect(c, TK.x, TK.y, TK.w, TK.h); block(c, rect(TK.x, TK.y, TK.w, TK.h), CHIP, 6801, { kw: 6 }); ink(c, rect(TK.x, TK.y, TK.w, 90), BLK, 6802, { reg: false });
  c.save(); c.translate(TK.x + 70, TK.y + 45); block(c, rrPts(-36, -24, 72, 48, 8), YEL, 6803, { kw: 4 }); block(c, ellPts(0, 2, 15, 15, 0, 16), BLK, 6804, { kw: 0, key: false }); c.restore();   // a camera icon, no words
  for (let k = 0; k < 3; k++) ink(c, rect(TK.x + 150, TK.y + 24 + k * 16, 300 - k * 60, 8), CHIP, 6805 + k, { reg: false });
  c.save(); c.beginPath(); c.rect(PH.x, PH.y, PH.w, PH.h); c.clip();
  ink(c, rect(PH.x, PH.y, PH.w, PH.h), CHIP, 6810, { reg: false }); dotsIn(c, rect(PH.x, PH.y, PH.w, PH.h * .5), BLUE, .18, 6811, 10); dotsIn(c, rect(PH.x, PH.y + PH.h * .62, PH.w, PH.h * .4), BLK, .35, 6812, 10);
  const grin = t > at(7, 3) ? .02 * Math.sin((t - at(7, 3)) * 20) * Math.exp(-(t - at(7, 3)) * 2) : 0;
  c.save(); c.translate(480, 1120); c.rotate(grin); frontCar(c, 0, 0, 1.2); c.restore();
  c.restore(); key(c, rect(PH.x, PH.y, PH.w, PH.h), 8, 6813);
  for (let k = 0; k < 4; k++) ink(c, rect(TK.x + 60 + k * 40, TK.y + TK.h - 150, 24, 90), BLK, 6820 + k, { reg: false, tint: .7, cell: 6 });   // a barcode-ish block, no digits
  block(c, rect(TK.x + TK.w - 290, TK.y + TK.h - 150, 230, 90), YEL, 6825, { kw: 4 });
  // the marker circle round the plate on 7:3
  const mc = seg(t, at(7, 3) - SLAM, at(7, 3) + .25);
  if (mc > 0 && t < PEEL[1]) { c.save(); c.strokeStyle = YEL; c.lineWidth = 12; c.lineCap = 'round'; c.beginPath(); c.ellipse(PLATE.x, PLATE.y, 180, 98, -.05, -1.6, -1.6 + TAU * 1.05 * easeOut(mc)); c.stroke(); c.restore(); }
  // the plate: on the photo; peels off on its left edge (8:1-2), flutters down and lands face up (8:3)
  const pu = easeIO(seg(t, ...PEEL)), du = seg(t, ...DROP);
  if (du <= 0) { const f = Math.cos(pu * Math.PI * .9), lift = 1 + .15 * Math.sin(pu * Math.PI); c.save(); c.translate(PLATE.x - PLATE.w / 2, PLATE.y); c.scale(f * lift, lift); c.translate(PLATE.w / 2, 0); plateCard(c, 0, 0, 1, -.1 * pu, f < 0); c.restore(); }
  else { const e = easeOut(du), x = lerp(PLATE.x - PLATE.w / 2 - PLATE.w / 2 * .95, REST[0], e) + 40 * Math.sin(du * 8) * (1 - du), y = lerp(PLATE.y - 40, REST[1], easeIn(du)), f = Math.cos(lerp(Math.PI * .9, TAU, e));
    c.save(); c.translate(x, y); c.rotate(lerp(-.1, REST[2], e) + .3 * Math.sin(du * 7) * (1 - du)); c.scale(f * 1.1, 1.1); plateCard(c, 0, 0, 1, 0, f < 0, du > .6); c.restore(); }
}
function flashFull(c, t, t0) { const u = seg(t, t0, t0 + .3); if (u <= 0 || u >= 1) return; screenSpace(c, () => { c.save(); c.globalAlpha = .9 * (1 - u) ** 2; c.fillStyle = '#ffffff'; c.fillRect(0, 0, W, H); c.restore(); }); }

// THE PROMISE (bar 9): Jeff and his magnifier over the three props, on a case-file board. No flags, no fixes.
const BOARD = { x: 318, y: 680, w: 560, h: 400 }, PROPS = [[410, 885], [596, 885], [782, 885]];   // Jeff stands whole inside the safe zone below it
// the case board: one pinned photo per scam, a recap of what the viewer just saw
function picOil(pw, ph, c) { ink(c, rect(-pw / 2, -ph / 2, pw, ph), CHIP, 6920, { reg: false }); dotsIn(c, rect(-pw / 2, ph * .22, pw, ph), BLK, .3, 6921, 6);
  sedan(c, 8, ph * .3, .2, { len: CAR_LEN, hood: 1 }); puff(c, -32, -ph * .12, 30, 6922); }
function picSite(pw, ph, c) { ink(c, rect(-pw / 2, -ph / 2, pw, ph), BLK, 6923, { reg: false }); c.save(); c.translate(-pw / 2 + 4, -ph / 2 + 16); c.scale((pw - 8) / 660, (pw - 8) / 660); site(c, at(4) + 1, SITE_BUILD); c.restore(); }
function picPlate(pw, ph, c) { ink(c, rect(-pw / 2, -ph / 2, pw, ph), BLUE, 6924, { reg: false }); plateCard(c, 0, 4, .48, 0); }
const PICS = [picOil, picSite, picPlate];
function drawProps(c) { PROPS.forEach(([px, py], k) => { polaroid(c, px, py, 172, 212, [-.05, .03, -.03][k], 6930 + k * 5, (pw, ph) => PICS[k](pw, ph, c)); pushpin(c, px, py - 96); }); }
function sceneJeff(c, tRaw) {
  const t = twos(tRaw);
  bgDots(c, BLUE, .05, .3);
  shadowRect(c, BOARD.x, BOARD.y, BOARD.w, BOARD.h); block(c, rect(BOARD.x, BOARD.y, BOARD.w, BOARD.h), CHIP, 6910, { kw: 6 });
  drawProps(c);
  const t0 = at(B_JEFF), jin = easeOutBack(land(t, t0)), raise = easeOut(seg(t, t0 + .1, at(B_JEFF, 2)));
  const J = jeff(c, 190, lerp(2600, 1415, jin), .5, { armR: lerp(0, -2.05, raise), head: -.05 + .03 * Math.sin(t * 2) + lag(t, t0), bob: Math.abs(Math.sin(t * Math.PI / BEAT)) * 4, sy: 1 + breath(t, 1) });
  if (raise > 0) {   // the lens arrives on each prop on 2, 3, 4
    const ARR = [at(B_JEFF, 3), at(B_JEFF + 1, 1), at(B_JEFF + 1, 3)], MV = .35;   // the lens arrives on each prop on these beats
    const idx = t < ARR[1] - MV ? 0 : t < ARR[2] - MV ? 1 : 2;
    const from = PROPS[Math.max(0, idx - 1)], to = PROPS[idx], mv = idx === 0 ? 1 : easeIO(seg(t, ARR[idx] - MV, ARR[idx]));
    let [mx, my] = [lerp(from[0], to[0], mv), lerp(from[1], to[1], mv) - 20 * Math.sin(mv * Math.PI)];
    if (t < ARR[0]) { const u = easeIO(seg(t, at(B_JEFF, 2), ARR[0])); mx = lerp(J.hand[0] + 60, PROPS[0][0], u); my = lerp(J.hand[1] - 100, PROPS[0][1], u); }
    const R = lerp(40, 118, raise);
    magnifier(c, mx, my, R, J.hand, raise > .6 ? () => { c.translate(mx, my); c.scale(1.7, 1.7); c.translate(-mx, -my); block(c, rect(BOARD.x, BOARD.y, BOARD.w, BOARD.h), CHIP, 6910, { kw: 0, key: false }); drawProps(c); } : null);
  }
}

// HANDOFF (bar 10): the loop's own page. Its background is the loop's (same code, same seed); its pieces are cut from the
// delivered loop's own decoded frames with masks, land on the beats in their exact places, and from PIECE_T[5] + .1 the
// whole loop frame is shown, so the last tease frame is loop frame 119 and the next frame is the loop's own frame 0.
const LOOP_F0 = 60;
const PIECE_T = [at(B_HAND, 1), at(B_HAND, 2), at(B_HAND, 3), at(B_HAND, 3), at(B_HAND, 4), at(B_HAND, 4)];
let MASKS = null, PLATE_BG = null; const SCRATCH = layer();
const loopFrame = t => IMG['loop' + Math.min(119, Math.max(LOOP_F0, Math.round((t - at(B_HAND - 1)) * FPS)))];
function sceneHandoff(c, t) {
  screenSpace(c, () => {
    const full = t >= PIECE_T[5] + .1, im = loopFrame(t);
    if (full) { c.drawImage(im, 0, 0, W, H); return; }
    c.drawImage(PLATE_BG, 0, 0, W, H);
    MASKS.forEach((m, k) => {
      const t0 = PIECE_T[k]; if (t < t0 - SLAM) return;
      const g = SCRATCH.getContext('2d'); g.setTransform(1, 0, 0, 1, 0, 0); g.globalCompositeOperation = 'source-over'; g.clearRect(0, 0, SCRATCH.width, SCRATCH.height);
      g.drawImage(im, 0, 0, SCRATCH.width, SCRATCH.height); g.globalCompositeOperation = 'destination-in'; g.drawImage(m.cv, 0, 0, SCRATCH.width, SCRATCH.height); g.globalCompositeOperation = 'source-over';
      const [mx, my] = m.c; let k2 = 1, dy = 0;
      if (m.name === 'jeff') dy = (1 - easeOut(land(t, t0))) * 700;
      else k2 = t < t0 ? lerp(.8, 1, easeOut(land(t, t0))) : 1 + .02 * Math.exp(-(t - t0) * 12) * Math.cos((t - t0) * 30);
      c.save(); c.translate(mx, my + dy); c.scale(k2, k2); c.translate(-mx, -my); c.drawImage(SCRATCH, 0, 0, W, H); c.restore();
    });
  });
}
sceneHandoff.finish = false;

// INTRO (the 3-beat pickup): the title card. The official logo (drawn from its file, untouched, after the finish), the title,
// the show time, and a little yellow car that drives in underneath. Everything is on screen, level and still, from frame 0.
const INTRO_TITLE = '3 CAR SCAMS', INTRO_SUB = 'LIVE WEDNESDAY  ·  5 PM ET';
function sceneIntro(c, t) {
  bgDots(c, BLUE, .12, .55);
  const tt = twos(t), u = easeOut(seg(tt, -INTRO, -INTRO + 2 * BEAT)), park = -INTRO + 2 * BEAT;   // it parks on beat 3 and rocks on its springs
  const z = easeIn(seg(t, TR_INTRO[0], TR_INTRO[1])), zk = 1 + 1.8 * z;   // the exit: the camera dives into the little car (smooth, on ones)
  c.save(); c.translate(SCX, 1330); c.scale(zk, zk); c.translate(-SCX, -1330);
  const rock = tt > park ? .025 * Math.exp(-(tt - park) * 8) * Math.sin((tt - park) * 20) : 0;
  c.save(); c.translate(lerp(-420, SCX, u), 1392); c.rotate(rock); sedan(c, 0, 0, .5, { len: CAR_LEN }); c.restore();
  if (tt >= park) { const v = seg(tt, park, park + .5); if (v < 1) puff(c, SCX + 170 - 60 * v, 1370 - 50 * v, lerp(14, 34, v), 6050, 1 - v); }   // a little exhaust puff as it stops
  c.restore();
  const a = introA(t); if (a <= 0) return;
  c.save(); c.globalAlpha = a; chip(c, INTRO_TITLE, SCX, 905, 104, BLK, CHIP, t, -INTRO, 760); chip(c, INTRO_SUB, SCX, 1062, 46, YEL, BLK, t, -INTRO, 700); c.restore();
}
sceneIntro.overlay = (c, t) => { const a = introA(t); if (a <= 0) return;   // the official logo, screen space (it fades with the words)
  screenSpace(c, () => { const lg = IMG.logo, [bx, by, bw, bh] = IMG.logoBox, lw = 620, lh = bh * lw / bw; c.globalAlpha = a; c.drawImage(lg, bx, by, bw, bh, CX - lw / 2, 400, lw, lh); c.globalAlpha = 1; }); };
function dissolve(c, t, [t0, t1], A, B) {   // B fades in over A
  const u = easeIO(seg(t, t0, t1)); layerOf(L1, A, t); layerOf(L2, B, t);
  c.save(); resetT(c); c.drawImage(L1, 0, 0, W, H); c.globalAlpha = u; c.drawImage(L2, 0, 0, W, H); c.restore();
}

// ================= assembly =================
function layerOf(L, scene, t) { const g = L.getContext('2d'); contentT(g); g.globalAlpha = 1; scene(g, t); if (scene.finish !== false) printFinish(g); if (scene.overlay) { contentT(g); scene.overlay(g, t); } return L; }
function pushTo(c, t, [t0, t1], A, B, dir = 1) {   // the camera moves from A to B (B from below); no card is up
  const u = easeIO(seg(t, t0, t1)); layerOf(L1, A, t); layerOf(L2, B, t);
  c.save(); resetT(c); c.drawImage(L1, 0, -dir * u * H, W, H); c.drawImage(L2, 0, dir * (1 - u) * H, W, H); c.restore();
}
function zoomTo(c, t, [t0, t1], A, rect0, B) {
  zoomThrough(c, t, t0, t1, rect0, g => { A(g, t0 - 1e-3); }, g => B(g, t)); printFinish(c);
}
const inT = ([a, b], t) => t >= a && t < b;
function drawScene(c, t) {
  contentT(c);
  if (Q.has('plate')) { screenSpace(c, () => { bgDots(c, BLUE, .12, .55); printFinish(c); }); return; }
  if (t < TR_INTRO[0]) { sceneIntro(c, t); printFinish(c); sceneIntro.overlay(c, t); }
  else if (t < TR_INTRO[1]) dissolve(c, t, TR_INTRO, sceneIntro, sceneOil);
  else if (t < TR.smoke[0]) { sceneOil(c, t); printFinish(c); }
  else if (inT(TR.smoke, t)) { if (t < SMOKE_MID) sceneOil(c, t); else sceneSiteBuild(c, t); printFinish(c); contentT(c); smokeWall(c, t); }
  else if (t < TR.zoomSite[0]) { sceneSiteBuild(c, t); printFinish(c); }
  else if (inT(TR.zoomSite, t)) zoomTo(c, t, TR.zoomSite, sceneSiteBuild, SCR, sceneSite);
  else if (t < TR.swing[0]) { sceneSite(c, t); printFinish(c); }
  else if (inT(TR.swing, t)) { swing(c, t); printFinish(c); }
  else if (t < TR.toMail[0]) { sceneLot(c, t); printFinish(c); }
  else if (inT(TR.toMail, t)) pushTo(c, t, TR.toMail, sceneLot, sceneMail);
  else if (t < TR.zoomTicket[0]) { sceneMail(c, t); printFinish(c); }
  else if (inT(TR.zoomTicket, t)) zoomTo(c, t, TR.zoomTicket, sceneMail, topTicketRect(), sceneTicket);
  else if (t < at(B_JEFF) - SLAM) { sceneTicket(c, t); printFinish(c); flashFull(c, t, at(7)); }   // the cut: with the promise card, which lands on the downbeat
  else if (t < TR.toLoop[0]) { sceneJeff(c, t); printFinish(c); }
  else if (inT(TR.toLoop, t)) pushTo(c, t, TR.toLoop, sceneJeff, sceneHandoff);
  else sceneHandoff(c, t);
  contentT(c); captionsTop(c, t);
  if (SHOW_SAFE) safeOverlay(c);
}

// ================= runtime =================
const CV = document.getElementById('c'); CV.width = OUT_W; CV.height = OUT_H; const CTX = CV.getContext('2d');
function frame(i) { const t = Math.min(i / FPS - INTRO, DUR - 1e-6); FILM_T = t; resetT(CTX); CTX.globalAlpha = 1; drawScene(CTX, t); resetT(CTX); }
window.__NFR = NFR; window.__FPS = FPS; window.__frame = i => { frame(i); return CV.toDataURL('image/png'); };
window.__caps = () => CAPS.map(([t0, t1, ...s]) => ({ t0, t1, s })); window.__tr = () => TR;
(async () => {
  await loadPrintKit(); await loadVertKit(); makeCream();
  MANP = await (await fetch('assets/officer/man_parts.json')).json();
  await Promise.all([...Object.keys(MANP.parts).map(k => loadImg('man_' + k, `assets/officer/man_${k}.png`)), loadImg('man_gasp', 'assets/wedtease/man_head_gasp.png')]);
  SKP = await (await fetch('assets/wedtease/sidekick_parts.json')).json();
  await Promise.all(Object.keys(SKP.parts).map(k => loadImg('sk_' + k, `assets/wedtease/sidekick_${k}.png`)));
  if (!Q.has('plate')) {
    const pad = n => String(n).padStart(4, '0');
    await Promise.all([...Array(60).keys()].map(k => loadImg('loop' + (LOOP_F0 + k), `out/rossen-loop-wednesday/frames/${pad(LOOP_F0 + k)}.png`)));
    const M = await (await fetch('assets/wedtease/loop_masks.json')).json();
    MASKS = await Promise.all(M.pieces.map(async (p, k) => { await loadImg('mask' + k, `assets/wedtease/${p.file}`); const cv = document.createElement('canvas'); cv.width = OUT_W; cv.height = OUT_H; cv.getContext('2d').drawImage(IMG['mask' + k], 0, 0, OUT_W, OUT_H); return { cv, c: p.centre, name: p.name }; }));
  }
  PLATE_BG = document.createElement('canvas'); PLATE_BG.width = OUT_W; PLATE_BG.height = OUT_H; { const g = PLATE_BG.getContext('2d'); g.setTransform(OUT_W / W, 0, 0, OUT_H / H, 0, 0); bgDots(g, BLUE, .12, .55); printFinish(g); }
  frame(+(Q.get('frame') || 0));
  window.__ready = true;
})().catch(e => { console.error(e); window.__error = String(e); });
