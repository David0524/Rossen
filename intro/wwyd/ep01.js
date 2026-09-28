'use strict';
/* WHAT WOULD YOU DO? #1: the grandparent scam. The episode's drawings (the recurring parts come from wwyd.js).
   tease     Grandma's phone is already ringing on the title card: UNKNOWN NUMBER
   call      (3 bars) she answers; the caller is the Grandson's silhouette with the Scammer hiding behind it, visible to
             the viewer and not to her. The last frame of this scene is the freeze-frame.
   reveal_A  WRONG: the bail money flies into the Scammer's hands and he sneaks off with it
   reveal_B  CLOSE: he reads family details off a post, then copies the voice from a short clip
   reveal_C  RIGHT: she hangs up and calls her grandson's own number; he answers from home, fine; the fake silhouette
             collapses and the Scammer tumbles over
   Grandma is the hero and is never mocked; only the Scammer looks foolish. Every number is 1-555-XXX-XXXX style. */
const FAKE_NUM = '1-555-XXX-XXXX', SANS = '"Liberation Sans"', MONO = '"Liberation Mono"';
const GM = { head: [805, 445] };   // Grandma's reference points (from her parts file)

// ---------------- shared bits of this episode ----------------
function ringWaves(c, x, y, t, t0s) { for (const t0 of t0s) { const u = seg(t, t0, t0 + .6); if (u <= 0 || u >= 1) continue;
  c.save(); c.globalAlpha = 1 - u; c.strokeStyle = YEL; c.lineWidth = 11; c.lineCap = 'round';
  for (const sd of [-1, 1]) for (let k = 0; k < 2; k++) { const r = 50 + k * 40 + 36 * u; c.beginPath(); c.arc(x, y, r, sd > 0 ? -.8 : Math.PI - .8, sd > 0 ? .8 : Math.PI + .8); c.stroke(); }
  c.restore(); } }
function callerCard(c, x, y, w, h, lines, t, shake = 0) {   // a big caller-ID card
  c.save(); c.translate(shake, 0);
  shadowRect(c, x, y, w, h); block(c, rrPts(x, y, w, h, 30, 6), BLK, 9001, { kw: 6 }); block(c, rrPts(x + 16, y + 16, w - 32, h - 32, 20, 4), CHIP, 9002, { kw: 3 });
  lines.forEach(([s, size, font, col], i) => inkText(c, s, x + w / 2, y + 70 + i * 78, size, font, col, w - 70));
  c.restore();
}
function grandma(c, x, y, s, p = {}) { puppet(c, 'grandma', x, y, s, p); }
function grandson(c, x, y, s, p = {}) { puppet(c, 'grandson', x, y, s, p); }
// the voice on the line: the Grandson's shape, flat black, with the Scammer hiding behind it
function fakeVoice(c, x, y, s, t, o = {}) {
  const squash = o.squash || 0;
  if (o.peek !== undefined && o.peek > 0) {   // the Scammer, peeking out from behind the silhouette
    const px = x + 70 * s / .42 * o.peek + (o.fall || 0) * 300, py = y + (o.fall || 0) * 400;
    scammer(c, px, py, s * .86, { sx: -1, head: .08 * Math.sin(t * 5), tilt: (o.fall || 0) * 1.4, bob: Math.abs(Math.sin(t * Math.PI / BEAT)) * 4 });
  }
  if (squash >= 1) return;
  silhouette(c, BLK, .93, g => grandson(g, x, y, s, { head: .05 * Math.sin(t * 3), sy: 1 - squash }));
  if (squash < .4) { c.save(); c.globalAlpha = 1 - squash * 2.5; inkText(c, '?', x - 10 * s / .42, y - 630 * s * (1 - squash), 110 * s / .42, 'Stamp', CHIP, 120); c.restore(); }
}
function callBubble(c, t, B, tail, header, inner) {   // the call, as a speech bubble with a tail to Grandma's phone
  const { x, y, w, h } = B, P = [[x, y], [x + w, y], [x + w, y + h], [x + 150, y + h], tail, [x + 40, y + h - 60], [x, y + h - 60]];
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fill(polyPath(P.map(([a, b]) => [a + 12, b + 14]))); c.restore();
  block(c, P, CHIP, 9010, { kw: 7 });
  c.save(); c.beginPath(); c.rect(x + 12, y + 70, w - 24, h - 140); c.clip(); dotsIn(c, rect(x, y, w, h), BLUE, .18, 9011, 12); inner(); c.restore();
  ink(c, rect(x + 8, y + 8, w - 16, 62), BLK, 9012, { reg: false }); inkText(c, header, x + w / 2, y + 40, 38, 'Stamp', CHIP, w - 60);
}

// ================= the title card's picture =================
SCENES.tease = (c, t, S) => {
  const rings = [S.at(1, 1), S.at(1, 3), S.at(2, 1), S.at(2, 3)];
  let sx = 0; for (const r of rings) if (t >= r && t < r + .45) sx += Math.sin((t - r) * 90) * 8 * (1 - (t - r) / .45);
  grandma(c, 260, 1430, .66, { head: .06, bob: Math.abs(Math.sin(t * Math.PI / BEAT)) * 4 });
  callerCard(c, 470, 780, 410, 300, [['INCOMING CALL', 30, SANS, BLK], ['UNKNOWN', 64, 'Stamp', BLK], [FAKE_NUM, 38, MONO, BLK]], t, sx);
  ringWaves(c, 362, 1136, t, rings);   // around her phone, clear of the card
};

// ================= the call =================
const BUB = { x: 470, y: 590, w: 420, h: 510 };
SCENES.call = (c, t, S) => {
  sceneBg(c);
  const wob = S.lt > BAR ? .06 * Math.sin((t - S.t0) * 5) : 0, up = easeOut(seg(t, S.t0 - .1, S.t0 + .25));
  grandma(c, 230, 1430, .7, { arm: -.45 * up, head: -.06 + wob, bob: Math.abs(Math.sin(t * Math.PI / BEAT)) * 3 });
  const peek = easeOutBack(seg(t, S.at(1, 2) - SLAM, S.at(1, 2) + .2));
  const secs = Math.max(0, Math.floor((t - S.t0) * 1.6));
  callBubble(c, t, BUB, [352, 1085], `ON CALL  00:${String(secs).padStart(2, '0')}`, () => fakeVoice(c, 680, 1085, .42, t, { peek }));
};

// ================= the reveals =================
function envelope(c, x, y, rot, s = 1) { c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s);
  block(c, rect(-120, -75, 240, 150), YEL, 9100, { kw: 5 }); key(c, [[-120, -75], [0, 10], [120, -75]], 5, 9101, false);
  block(c, rrPts(-70, 20, 140, 44, 10, 3), BLK, 9102, { kw: 2 }); inkText(c, 'BAIL $$$', 0, 44, 30, 'Stamp', YEL, 130); c.restore(); }
function bill(c, x, y, rot) { c.save(); c.translate(x, y); c.rotate(rot); block(c, rect(-70, -34, 140, 68), YEL, 9110, { kw: 4 }); ink(c, rect(-14, -34, 28, 68), BLUE, 9111, { reg: false }); inkText(c, '$', -42, 3, 34, 'Stamp', BLK, 40); c.restore(); }
SCENES.reveal_A = (c, t, S) => {   // WRONG: the money is gone
  const land1 = S.at(1, 2), cash = S.at(1, 3), off = S.at(2, 3), go = easeIn(seg(t, off, off + .8));
  const sx = 690 + 520 * go, glee = t > cash ? .1 * Math.sin((t - cash) * 16) * Math.exp(-(t - cash) * 1.5) : 0;
  scammer(c, sx, 1150, .52, { sx: -1, head: glee, bob: Math.abs(Math.sin(t * Math.PI / E8)) * (t > cash ? 8 : 3), rod: -.15 });
  const u = easeIn(seg(t, land1 - .45, land1));
  if (t < cash) envelope(c, lerp(150, sx - 60, u), lerp(760, 930, u) - 120 * Math.sin(u * Math.PI), lerp(-.4, .2, u));
  else for (let k = 0; k < 6; k++) { const v = seg(t, cash + k * .04, cash + .45 + k * .04), a = k / 6 * TAU;   // it bursts into cash in his arms
    bill(c, sx - 60 + Math.cos(a) * 90 * easeOut(v), 930 + Math.sin(a) * 50 * easeOut(v) - 30 * k * (1 - go * .5), a + v); }
};
function post(c, x, y, w, h, t, hlT) {   // a generic social post: no platform, no names
  shadowRect(c, x, y, w, h); block(c, rrPts(x, y, w, h, 24, 5), CHIP, 9200, { kw: 6 });
  c.save(); c.beginPath(); c.arc(x + 70, y + 72, 46, 0, TAU); c.clip(); ink(c, rect(x + 20, y + 20, 100, 100), BLUE, 9201, { reg: false });
  const m = PUP.grandson.parts.head, im = IMG.grandson_head, sc = 110 / m.w; c.drawImage(im, x + 70 - m.w * sc / 2, y + 72 - m.h * sc / 2 + 6, m.w * sc, m.h * sc); c.restore();
  c.save(); c.strokeStyle = BLK; c.lineWidth = 5; c.beginPath(); c.arc(x + 70, y + 72, 46, 0, TAU); c.stroke(); c.restore();
  inkText(c, 'MY POST', x + 136, y + 60, 40, 'Stamp', BLK, w - 160, 'left'); inkText(c, 'PUBLIC  ·  2 DAYS AGO', x + 136, y + 102, 26, SANS, BLK, w - 160, 'left');
  const L = [['GOT MY FIRST CAR!', 0], ['LOVE YOU GRANDMA ♥', 1], ['#HOMETOWN #FAMILY', 2]];
  L.forEach(([s, k], i) => { const ly = y + 200 + i * 80, u = hlT[k] !== undefined ? easeOut(seg(t, hlT[k] - SLAM, hlT[k] + .1)) : 0;
    c.font = `40px Stamp`; const tw = Math.min(c.measureText(s).width, w - 70); if (u > 0) ink(c, rect(x + 30, ly - 30, (tw + 16) * u, 56), YEL, 9210 + i, { reg: false, amp: 3 });
    inkText(c, s, x + 38, ly, 40, 'Stamp', BLK, w - 70, 'left'); });
}
function clipCard(c, x, y, w, h, t, t0) {   // a short video clip with its sound wave
  shadowRect(c, x, y, w, h); block(c, rrPts(x, y, w, h, 24, 5), BLK, 9300, { kw: 6 });
  block(c, ellPts(x + 90, y + h / 2, 50, 50, 0, 30), YEL, 9301, { kw: 4 }); block(c, [[x + 76, y + h / 2 - 26], [x + 76, y + h / 2 + 26], [x + 112, y + h / 2]], BLK, 9302, { kw: 0, key: false });
  inkText(c, 'CLIP  0:03', x + 170, y + 50, 36, 'Stamp', CHIP, w - 200, 'left');
  for (let k = 0; k < 18; k++) { const a = t > t0 ? .35 + .65 * Math.abs(Math.sin(k * 1.7 + (t - t0) * 9)) : .3; const bh = 70 * a;
    c.fillStyle = CHIP; c.fillRect(x + 170 + k * 18, y + h / 2 + 25 - bh / 2, 10, bh); }
}
SCENES.reveal_B = (c, t, S) => {   // CLOSE: they can know the answers, and copy the voice
  const b2 = S.at(2), sw = easeIO(seg(t, b2 - .1, b2 + .3));
  const eye = [760, 1150];
  const mag = t < b2 ? { x: lerp(330, 280, Math.sin((t - S.t0) * 1.3) * .5 + .5), y: t < S.at(1, 3) ? 850 : 930 } : null;
  if (sw < 1) { c.save(); c.translate(-800 * sw, 0); post(c, 80, 660, 480, 460, t, [S.at(1, 2), S.at(1, 3)]); c.restore(); }
  if (sw > 0) { c.save(); c.translate(800 * (1 - sw), 0); clipCard(c, 80, 720, 480, 190, t, S.at(2, 2)); c.restore(); }
  const tip = scammer(c, eye[0], eye[1], .48, { sx: -1, head: .06 * Math.sin(t * 5), rod: -.3 });
  if (t >= S.at(2, 2)) for (let k = 0; k < 7; k++) { const u = ((t - S.at(2, 2)) * 1.6 + k / 7) % 1;   // the sound wave flows into his mouth
    c.save(); c.globalAlpha = Math.min(1, (1 - u) * 2); ink(c, rect(lerp(560, 700, u) - 6, 830 - 30 * Math.sin(k + u * 6) - 20, 12, 40 + 20 * Math.sin(k * 2 + t * 8)), BLUE, 9310 + k, { reg: false }); c.restore(); }
  chip(c, 'VOICE COPIED', 640, 690, 46, BLUE, CHIP, t, S.at(2, 3), .04, 360);
};
const HOME = { x: 540, y: 650, w: 350, h: 500 };
function homePanel(c, t) {   // the Grandson at home, relaxed
  const { x, y, w, h } = HOME;
  shadowRect(c, x, y, w, h); block(c, rrPts(x, y, w, h, 24, 5), CHIP, 9400, { kw: 6 }); dotsIn(c, rect(x, y, w, h), YEL, .2, 9401, 12);
  block(c, rect(x + 30, y + 60, 130, 120), BLUE, 9402, { kw: 4 }); key(c, [[x + 95, y + 60], [x + 95, y + 180]], 4, 9403, false); key(c, [[x + 30, y + 120], [x + 160, y + 120]], 4, 9404, false);
  block(c, [[x + 250, y + 90], [x + 320, y + 90], [x + 340, y + 150], [x + 230, y + 150]], YEL, 9405, { kw: 4 }); key(c, [[x + 285, y + 150], [x + 285, y + 330]], 6, 9406, false);
  ink(c, rect(x + 8, y + 8, w - 16, 50), BLK, 9407, { reg: false }); inkText(c, 'AT HOME', x + w / 2, y + 34, 32, 'Stamp', CHIP, w - 40);
  c.save(); c.beginPath(); c.rect(x + 8, y + 58, w - 16, h - 66); c.clip();
  grandson(c, x + w / 2 - 20, y + h - 12, .44, { arm: -.45, head: .06 + .04 * Math.sin((t) * 3), bob: Math.abs(Math.sin(t * Math.PI / (2 * BEAT))) * 4 });
  c.restore();
}
SCENES.reveal_C = (c, t, S) => {   // RIGHT: she hangs up and calls his real number; he's fine; the fake collapses
  const b2 = S.at(2), tap = S.at(1, 3), col = S.at(2, 3);
  if (t < b2) {
    grandma(c, 240, 1150, .55, { arm: 0, head: .04, bob: Math.abs(Math.sin(t * Math.PI / BEAT)) * 3 });
    const ended = t < S.at(1, 2.5), press = t >= tap && t < tap + .15 ? .95 : 1;
    if (ended) callerCard(c, 470, 680, 420, 330, [['CALL', 30, SANS, BLK], ['ENDED', 70, 'Stamp', BLK], ['UNKNOWN', 36, MONO, BLK]], t);
    else { callerCard(c, 470, 680, 420, 330, [['CONTACTS', 30, SANS, BLK], ['MY GRANDSON', 56, 'Stamp', BLK], [FAKE_NUM, 36, MONO, BLK]], t);
      c.save(); c.translate(680, 1070); c.scale(press, press); pill(c, 0, 0, 260, 90, BLUE, t < tap ? 'CALL' : 'CALLING...', 44, CHIP, 9500); c.restore(); tapRing(c, 680, 1070, t, tap); }
    return;
  }
  const sq = easeIn(seg(t, col, col + .35)), fall = easeIn(seg(t, col + .1, col + .8));
  fakeVoice(c, 400, 1150, .5, t, { peek: 1, squash: sq, fall });   // behind everyone
  if (sq > 0 && sq < 1) puff(c, 400, 900, t, col);
  grandma(c, 160, 1150, .5, { arm: -.45, head: .06 + .03 * Math.sin(t * 3), bob: Math.abs(Math.sin(t * Math.PI / BEAT)) * 4 });
  homePanel(c, t);
  if (t >= b2) for (let k = 0; k < 3; k++) { const u = ((t - b2) * 1.2 + k / 3) % 1; c.save(); c.globalAlpha = Math.sin(u * Math.PI); c.strokeStyle = BLUE; c.lineWidth = 7; c.lineCap = 'round';
    c.beginPath(); c.arc(lerp(330, 520, u), 860, 26, -1, 1); c.stroke(); c.restore(); }   // the call, warm and clear
};
function puff(c, x, y, t, t0) { const u = seg(t, t0 - .05, t0 + .35); if (u <= 0 || u >= 1) return; const r = rng(Math.round(t0 * 100));
  for (let k = 0; k < 10; k++) { const a = k / 10 * TAU + r(), d = 50 + 150 * easeOut(u), rr = (56 + r() * 30) * (1 - u * .7); block(c, ellPts(x + Math.cos(a) * d, y + Math.sin(a) * d * .7, rr, rr, 0, 20), CHIP, 9600 + k, { kw: 4 }); } }
