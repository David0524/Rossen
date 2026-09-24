'use strict';
/* JEFF'S RULES #2: GIFT CARDS ARE FOR GIFTS. The episode's middle scenes (recurring parts: rules.js; phone and lurker:
   rules/props.js).
   disguises (3 bars)  one silly costume per bar, swapped in a puff on beat 1: government agent, tech support, "grandson".
                       Each claim is the caption; on beat 3 the same demand, every time: GO BUY GIFT CARDS. READ ME THE NUMBERS.
   cash      (2 bars)  gift card = cash, with FAST · HARD TO TRACE · NO TAKE-BACKS on beats 2, 3, 4; then the numbers
                       are read (1.5, 2, 2.5) and the balance is $0.00 on 3 as the cash flies to the Scammer
   whatnow   (3 bars)  hang up (tap on 3) · already paid: call the card company, RIGHT AWAY! on 3 · report it at FTC.GOV
   No company names or logos; every number on screen is 1-800-XXX-XXXX style. */

// ---------------- the Scammer in costume ----------------
// the same transform as scammer() in vertkit.js, so a costume sits exactly on the puppet (head pieces turn with the head)
function costume(c, x, y, s, p, kind) {
  const [fx, fy] = SP.feet, [hx, hy] = SP.parts.head.pivot;
  c.save(); c.translate(x, y); c.rotate(p.tilt || 0); c.scale(s * (p.sx || 1), s); c.translate(-fx, -fy - (p.bob || 0));
  COSTUME_BODY[kind](c);
  c.translate(hx, hy); c.rotate(p.head || 0); c.translate(-hx, -hy); COSTUME_HEAD[kind](c);
  c.restore();
}
function nameTag(c, x, y, label) { block(c, rect(x, y, 170, 96), CHIP, 9001 + label.length, { kw: 5 }); ink(c, rect(x, y, 170, 24), BLUE, 9010, { reg: false }); inkText(c, label, x + 85, y + 62, 38, 'Stamp', BLK, 150); }
function star(c, x, y, r) { const P = []; for (let k = 0; k < 10; k++) { const a = -Math.PI / 2 + k * Math.PI / 5, rr = k % 2 ? r * .45 : r; P.push([x + Math.cos(a) * rr, y + Math.sin(a) * rr]); } block(c, P, YEL, 9020, { kw: 4 }); }
const COSTUME_HEAD = {
  agent(c) {   // a peaked official cap with a star, and very serious sunglasses
    block(c, [[598, 338], [592, 236], [700, 192], [932, 198], [962, 322]], BLUE, 9101, { kw: 6 });
    block(c, [[596, 300], [960, 290], [964, 330], [598, 340]], YEL, 9102, { kw: 4 });
    block(c, [[552, 336], [992, 318], [1004, 366], [556, 384]], BLK, 9103, { kw: 3 });
    star(c, 780, 248, 34);
    for (const [gx, gy] of [[690, 402], [842, 385]]) block(c, rrPts(gx, gy, 112, 64, 18, 4), BLK, 9104 + gx, { kw: 4 });
    key(c, [[802, 428], [842, 416]], 8, 9106, false);
  },
  tech(c) {   // a headset over the hat and giant round glasses
    c.save(); c.lineCap = 'round'; c.strokeStyle = BLK; c.lineWidth = 30; c.beginPath(); c.moveTo(612, 420); c.quadraticCurveTo(790, 60, 992, 400); c.stroke();
    c.strokeStyle = YEL; c.lineWidth = 14; c.stroke(); c.restore();
    for (const [ex, ey] of [[608, 440], [994, 412]]) block(c, ellPts(ex, ey, 44, 52, 0, 28), BLUE, 9110 + ex, { kw: 5 });
    c.save(); c.lineCap = 'round'; c.strokeStyle = BLK; c.lineWidth = 12; c.beginPath(); c.moveTo(622, 478); c.quadraticCurveTo(660, 540, 760, 516); c.stroke(); c.restore();
    block(c, ellPts(770, 514, 20, 20, 0, 18), BLK, 9112, { kw: 0, key: false });
    for (const [gx, gy] of [[745, 440], [895, 420]]) { c.save(); c.strokeStyle = BLK; c.lineWidth = 22; c.beginPath(); c.arc(gx, gy, 50, 0, TAU); c.stroke(); c.strokeStyle = CHIP; c.lineWidth = 10; c.stroke(); c.restore(); }
    key(c, [[795, 432], [845, 426]], 10, 9113, false);
  },
  grandson(c) {   // a curly wig, a backwards cap, and a bandage: "I'm in trouble!"
    const r = rng(9120); block(c, ellPts(785, 292, 250, 118, 0, 40), YEL, 9121, { kw: 5 });
    for (let k = 0; k < 13; k++) { const a = Math.PI + k / 12 * Math.PI, cx = 785 + Math.cos(a) * 240, cy = 300 + Math.sin(a) * 112; block(c, ellPts(cx, cy, 42 + r() * 10, 42 + r() * 10, 0, 18), YEL, 9130 + k, { kw: 4 }); }
    for (const [cx, cy] of [[560, 380], [1012, 350]]) block(c, ellPts(cx, cy, 40, 48, 0, 18), YEL, 9150 + cx, { kw: 4 });
    block(c, ellPts(800, 210, 150, 78, 0, 30), BLUE, 9160, { kw: 5 }); block(c, [[655, 214], [560, 196], [556, 236], [660, 250]], BLK, 9161, { kw: 3 });
    c.save(); c.translate(900, 488); c.rotate(-.5); block(c, rrPts(-64, -22, 128, 44, 16, 4), CHIP, 9162, { kw: 4 }); c.fillStyle = BLK; for (const dx of [-12, 0, 12]) { c.beginPath(); c.arc(dx, 0, 3.5, 0, TAU); c.fill(); } c.restore();
  },
};
const COSTUME_BODY = { agent(c) { nameTag(c, 628, 590, 'AGENT'); }, tech(c) { nameTag(c, 628, 590, 'TECH'); }, grandson(c) { nameTag(c, 628, 640, 'GRANDSON'); block(c, [[700, 560], [790, 600], [700, 640]], BLUE, 9170, { kw: 4 }); block(c, [[880, 560], [790, 600], [880, 640]], BLUE, 9171, { kw: 4 }); block(c, ellPts(790, 600, 20, 20, 0, 16), YEL, 9172, { kw: 3 }); } };
function puff(c, x, y, t, t0) {   // the costume change: a cloud of paper dots
  const u = seg(t, t0 - .08, t0 + .3); if (u <= 0 || u >= 1) return; const r = rng(Math.round(t0 * 100));
  for (let k = 0; k < 11; k++) { const a = k / 11 * TAU + r(), d = 60 + 170 * easeOut(u), rr = (70 + r() * 40) * (1 - u * .7);
    block(c, ellPts(x + Math.cos(a) * d, y + Math.sin(a) * d * .7, rr, rr, 0, 20), CHIP, 9200 + k, { kw: 4 }); }
}
function speech(c, lines, t, t0, tailTo) {   // the demand bubble; identical every time it appears
  if (t < t0 - SLAM) return; const k = pop(t, t0), bx = 110, by = 590, bw = 740, bh = 250;
  c.save(); c.translate(SCX, by + bh / 2); c.scale(k, k); c.translate(-SCX, -(by + bh / 2));
  const P = [[bx, by], [bx + bw, by], [bx + bw, by + bh], [tailTo[0] + 70, by + bh], [tailTo[0], tailTo[1]], [tailTo[0] - 20, by + bh], [bx, by + bh]];
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fill(polyPath(P.map(([x, y]) => [x + 10, y + 12]))); c.restore();
  block(c, P, CHIP, 9300, { kw: 7 });
  inkText(c, lines[0], SCX, by + 82, 66, 'Stamp', BLK, bw - 70); inkText(c, lines[1], SCX, by + 172, 66, 'Stamp', BLUE, bw - 70);
  c.restore();
}

// ================= disguises =================
const KINDS = ['agent', 'tech', 'grandson'];
SCENES.disguises = (c, t, S) => {
  sceneBg(c);
  const bar = Math.min(3, Math.max(1, Math.floor(S.lt / BAR) + 1)), kind = KINDS[bar - 1];
  const x = SCX, y = 1450, s = .8, p = { head: .06 * Math.sin(t * 4), bob: Math.abs(Math.sin(t * Math.PI / BEAT)) * 6 };
  scammer(c, x, y, s, p); costume(c, x, y, s, p, kind);
  puff(c, x, y - s * 505, t, S.at(bar, 1));
  const tb = S.at(bar, 3);
  if (t >= tb - SLAM) speech(c, EP.demand, t, tb, [x - 40, y - s * 520]);
  if (t >= tb + E8) { const u = seg(t, tb + E8, tb + BEAT); for (let k = 0; k < 3; k++) {   // gift cards flutter up out of the demand
    if (k === 1) continue;   // one card each side of him, never over his tag
    const cx = k ? 810 : 150, cy = 1290 - 60 * Math.sin((u + k * .3) * Math.PI); c.save(); c.translate(cx, cy); c.rotate(-.2 + k * .2); c.scale(.36, .36); giftCard(c, 0, 0, false, t); c.restore(); } }
};

// ================= cash: a gift card is like cash, and once the numbers are read it's gone =================
function giftCard(c, cx, cy, back, t, reveal = 3) {
  const w = 700, h = 440;
  c.save(); c.translate(cx, cy);
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fillRect(-w / 2 + 12, -h / 2 + 16, w, h); c.restore();
  if (!back) {
    block(c, rrPts(-w / 2, -h / 2, w, h, 34, 6), YEL, 9400, { kw: 6 });
    ink(c, rect(-w / 2 + 170, -h / 2, 60, h), BLUE, 9401, { reg: false }); ink(c, rect(-w / 2, -30, w, 60), BLUE, 9402, { reg: false });
    block(c, [[-w / 2 + 200, 0], [-w / 2 + 110, -90], [-w / 2 + 90, -30]], BLUE, 9403, { kw: 4 }); block(c, [[-w / 2 + 200, 0], [-w / 2 + 290, -90], [-w / 2 + 310, -30]], BLUE, 9404, { kw: 4 });
    inkText(c, 'GIFT CARD', 90, -120, 76, 'Stamp', BLK, 400); inkText(c, '$500', 150, 140, 110, 'Stamp', BLK, 300);
  } else {
    block(c, rrPts(-w / 2, -h / 2, w, h, 34, 6), CHIP, 9410, { kw: 6 });
    ink(c, rect(-w / 2, -h / 2 + 40, w, 70), BLK, 9411, { reg: false });
    inkText(c, 'PIN', -w / 2 + 50, -40, 44, 'Stamp', BLK, 120, 'left');
    for (let k = 0; k < 3; k++) { const gx = -w / 2 + 70 + k * 200, gy = 30;
      inkText(c, 'XXXX', gx + 80, gy + 36, 58, MONO, BLK, 180);
      if (k >= reveal) block(c, rrPts(gx, gy, 170, 72, 12, 3), '#cfc8b8', 9420 + k, { kw: 3 }); }
    inkText(c, 'CARD SERVICES  ' + NUM, 0, 170, 36, MONO, BLK, w - 80);
  }
  c.restore();
}
function cashStack(c, x, y, n = 4) { for (let k = 0; k < n; k++) { c.save(); c.translate(x + (k % 2) * 8, y - k * 22); block(c, rect(-150, -40, 300, 80), YEL, 9500 + k, { kw: 4 }); ink(c, rect(-30, -40, 60, 80), BLUE, 9510 + k, { reg: false }); inkText(c, '$', -100, 4, 46, 'Stamp', BLK, 50); inkText(c, '$', 100, 4, 46, 'Stamp', BLK, 50); c.restore(); } }
function bill(c, x, y, rot) { c.save(); c.translate(x, y); c.rotate(rot); c.scale(.55, .55); block(c, rect(-150, -40, 300, 80), YEL, 9520, { kw: 5 }); inkText(c, '$', 0, 4, 60, 'Stamp', BLK, 60); c.restore(); }
SCENES.cash = (c, t, S) => {
  sceneBg(c);
  const b2 = S.at(2), mv = easeIO(seg(t, b2 - .05, b2 + .35)), zeroT = S.at(2, 3);
  // bar 1: GIFT CARD = CASH, three labels on beats 2, 3, 4
  const cardS = lerp(.52, .86, mv), cardX = lerp(260, SCX, mv), cardY = lerp(800, 760, mv);
  const revealed = [S.at(2, 1.5), S.at(2, 2), S.at(2, 2.5)].filter(v => t >= v).length;
  c.save(); c.translate(cardX, cardY); c.scale(cardS * Math.max(.02, Math.abs(Math.cos(Math.PI * clamp01((t - b2 + .1) / .3)))), cardS);
  giftCard(c, 0, 0, t >= b2 + .05, t, revealed); c.restore();
  if (mv < 1) { c.save(); c.globalAlpha = 1 - mv; inkText(c, '=', 480, 812, 150, 'Stamp', BLK, 120); c.restore(); cashStack(c, lerp(700, 700, mv), 850); }
  [['FAST', SCX, 1060, 2], ['HARD TO TRACE', SCX, 1165, 3], ['NO TAKE-BACKS', SCX, 1270, 4]].forEach(([s, x, y, bt]) => { if (t < b2 - .05) chip(c, s, x, y, 58, BLK, CHIP, t, S.at(1, bt), bt % 2 ? .02 : -.02); });
  // bar 2: the balance, and the money flying to the Scammer on 3
  if (t >= b2) {
    const zero = t >= zeroT - .02, k = zero ? pop(t, zeroT) : 1;
    c.save(); c.translate(SCX - 120, 1080); c.scale(k, k); block(c, rect(-230, -58, 460, 116), zero ? BLK : CHIP, 9600, { kw: 5 });
    inkText(c, zero ? 'BALANCE $0.00' : 'BALANCE $500', 0, 6, 56, 'Stamp', zero ? YEL : BLK, 420); c.restore();
    for (let j = 0; j < 7; j++) { const u = seg(t, zeroT + j * .05, zeroT + .7 + j * .05); if (u <= 0 || u >= 1) continue;
      bill(c, lerp(200, 800, easeIn(u)), 1340 - 80 * Math.sin(u * Math.PI) - j * 8, u * 6 + j); }   // below the balance
    scammer(c, 820, 1470, .5, { sx: -1, head: zero ? .12 * Math.sin((t - zeroT) * 30) * Math.exp(-(t - zeroT) * 3) : .05 * Math.sin(t * 4), rod: -.2 });
  }
};

// ================= what now: hang up, call the card company, report it =================
function browser(c, t, typeT, tapT) {
  const x = 110, y = 610, w = 740, h = 600;
  shadowRect(c, x, y, w, h); block(c, rect(x, y, w, h), CHIP, 9700, { kw: 6 }); ink(c, rect(x, y, w, 120), BLK, 9701);
  block(c, rrPts(x + 30, y + 26, w - 60, 70, 35, 4), '#ffffff', 9702, { kw: 3, reg: false });
  const s = EP.typeText, n = Math.max(0, Math.min(s.length, Math.floor((t - typeT) / (BEAT / 8)) + 1));
  inkText(c, (t >= typeT ? s.slice(0, n) : '') + (Math.floor(t * 4) % 2 ? '|' : ''), x + 70, y + 62, 46, MONO, BLK, w - 140, 'left');
  inkText(c, 'REPORT FRAUD', x + w / 2, y + 250, 70, 'Stamp', BLK, w - 80);
  const press = t >= tapT && t < tapT + .15 ? .92 : 1; c.save(); c.translate(x + w / 2, y + 420); c.scale(press, press); pill(c, 0, 0, 420, 120, BLUE, 'START', 64, CHIP, 9703); c.restore();
  tapRing(c, x + w / 2, y + 420, t, tapT);
}
SCENES.whatnow = (c, t, S) => {
  sceneBg(c);
  const b1 = S.at(1), tap = S.at(1, 3), b2 = S.at(2), b3 = S.at(3), cx = PH.x + PH.w / 2;
  if (t < b2 + .3) {   // bar 1: the call, and Jeff hangs up on 3
    const out = easeIn(seg(t, b2 - .05, b2 + .3));
    lurker(c, t, b1 - 1, seg(t, S.at(1, 3.5), S.at(1, 4.5)));
    c.save(); c.translate(0, 900 * out); phoneBody(c);
    if (t < tap) { screenInCall(c, t, b1 - 6, 'UNKNOWN', 'ON CALL'); callButton(c, cx, PH.y + 640, BLK, true); }
    else { avatar(c, PH.y + 180, BLK, 'X'); inkText(c, 'CALL ENDED', cx, PH.y + 350, 64, 'Stamp', BLK, 480); }
    c.restore(); if (t < b2) tapRing(c, cx, PH.y + 640, t, tap);
  }
  if (t >= b2 - .05 && t < b3 + .3) {   // bar 2: the back of the card: call the card company, RIGHT AWAY! on 3
    const up = easeOut(seg(t, b2 - .05, b2 + .3)), out = easeIn(seg(t, b3 - .05, b3 + .3)), hl = easeOut(seg(t, S.at(2, 2), S.at(2, 2) + .2));
    c.save(); c.translate(SCX - 1100 * out, lerp(1900, 850, up));
    giftCard(c, 0, 0, true, t, 0);
    if (hl > 0) { ink(c, rect(-320, 136, 640 * hl, 66), YEL, 9710, { reg: false, amp: 3 }); inkText(c, 'CARD SERVICES  ' + NUM, 0, 170, 36, MONO, BLK, 620); }
    c.restore();
    if (t >= S.at(2, 3) - SLAM && t < b3) stampFit(c, 'RIGHT AWAY!', BLK, 140, SCX, 1200, -.05, .9, t, S.at(2, 3), 600);
  }
  if (t >= b3 - .05) {   // bar 3: report it: FTC.GOV typed, START tapped on 3, a check on 4
    const up = easeOut(seg(t, b3 - .05, b3 + .3)); c.save(); c.translate(0, 1300 * (1 - up)); browser(c, t, S.at(3, 1.5), S.at(3, 3)); c.restore();
    check(c, 760, 1060, .7, t, S.at(3, 4));
  }
  const th = easeOutBack(seg(t, S.at(3, 4), S.at(3, 4.4)));
  jeffUp(c, t, S.at(1, 1.5), 120, t >= S.at(3, 4) ? { armR: lerp(-2.2, -2.5, th), prop: th > .6 ? 'thumb' : 'point', head: .06 } : { armR: -2.2, prop: 'point', head: .05 }, .56);
};
