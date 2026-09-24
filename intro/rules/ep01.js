'use strict';
/* JEFF'S RULES #1: HANG UP. CALL BACK. The episode's middle scenes (the recurring parts come from rules.js).
   setup (2 bars)  the phone rings, caller ID "YOUR BANK"; answered, the Scammer is on the line; URGENT on 3
   why   (2 bars)  the Scammer swaps the caller-ID name tag on beats 2, 3, 4; FAKE! on bar 2 beat 3
   how   (4 bars)  hang up (tap on 3, he is yanked off) · flip the card (on 3) · dial the number on the back · connected
   No real bank or company names, no real numbers: every number on screen is 1-800-XXX-XXXX style. */
const NUM = '1-800-XXX-XXXX';
const PH = { x: 150, y: 600, w: 560, h: 790 };
const MONO = '"Liberation Mono"', SANS = '"Liberation Sans"';

// ---------------- the phone ----------------
function handset(c, x, y, s, rot = 0, col = CHIP) {   // a phone-handset glyph
  c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s); c.strokeStyle = col; c.lineCap = 'round'; c.lineWidth = 13;
  c.beginPath(); c.arc(0, 8, 26, Math.PI * 1.1, Math.PI * 1.9); c.stroke();
  c.fillStyle = col; for (const sx of [-1, 1]) { c.beginPath(); c.ellipse(sx * 26, 12, 11, 8, sx * .5, 0, TAU); c.fill(); }
  c.restore();
}
function callButton(c, x, y, col, down, press = 1) {
  c.save(); c.translate(x, y); c.scale(press, press);
  block(c, ellPts(0, 0, 62, 62, 0, 36), col, 8001 + (down ? 1 : 0), { kw: 5 }); handset(c, 0, -4, 1, down ? Math.PI : 0); c.restore();
}
function phoneBody(c) {
  const { x, y, w, h } = PH;
  shadowRect(c, x, y, w, h); block(c, rrPts(x, y, w, h, 60, 6), BLK, 8010, { kw: 6 });
  block(c, rrPts(x + 18, y + 48, w - 36, h - 72, 22, 4), CHIP, 8011, { kw: 3 });
  inkText(c, '9:41', x + 60, y + 26, 24, SANS, CHIP, 80, 'left');
}
function avatar(c, y, col = BLUE, glyph = '?') { block(c, ellPts(PH.x + PH.w / 2, y, 70, 70, 0, 40), col, 8020, { kw: 5 }); inkText(c, glyph, PH.x + PH.w / 2, y + 8, 80, 'Stamp', CHIP, 90); }
function screenIncoming(c, t, t0) {
  const cx = PH.x + PH.w / 2; avatar(c, PH.y + 180);
  inkText(c, 'INCOMING CALL', cx, PH.y + 290, 34, SANS, BLK, 440);
  inkText(c, 'YOUR BANK', cx, PH.y + 370, 72, 'Stamp', BLK, 480);
  inkText(c, NUM, cx, PH.y + 450, 44, MONO, BLK, 480);
  const pulse = 1 + .08 * Math.max(0, Math.sin((t - t0) * TAU / BEAT));
  callButton(c, PH.x + 140, PH.y + 640, BLK, true); callButton(c, PH.x + PH.w - 140, PH.y + 640, BLUE, false, pulse);
}
function screenInCall(c, t, tStart, name = 'YOUR BANK', sub = null) {
  const cx = PH.x + PH.w / 2; avatar(c, PH.y + 180);
  inkText(c, name, cx, PH.y + 330, 72, 'Stamp', BLK, 480);
  const secs = Math.max(0, Math.floor((t - tStart) * 1.6)); inkText(c, sub || `00:${String(secs).padStart(2, '0')}`, cx, PH.y + 405, 42, MONO, BLK, 480);
  // sound waves off the avatar
  for (let k = 0; k < 3; k++) { const u = ((t - tStart) * 1.6 + k / 3) % 1; c.save(); c.globalAlpha = (1 - u) * .8; c.strokeStyle = BLUE; c.lineWidth = 6;
    for (const sd of [-1, 1]) { c.beginPath(); c.arc(cx, PH.y + 180, 90 + 50 * u, sd > 0 ? -.5 : Math.PI - .5, sd > 0 ? .5 : Math.PI + .5); c.stroke(); } c.restore(); }
}
function ringShake(t, t0s) { let x = 0; for (const t0 of t0s) if (t >= t0 && t < t0 + .5) x += Math.sin((t - t0) * 90) * 9 * (1 - (t - t0) / .5); return x; }
function ringWaves(c, t, t0s) { for (const t0 of t0s) { const u = seg(t, t0, t0 + .6); if (u <= 0 || u >= 1) continue;
  c.save(); c.globalAlpha = 1 - u; c.strokeStyle = YEL; c.lineWidth = 12; c.lineCap = 'round';
  for (const sd of [-1, 1]) for (let k = 0; k < 2; k++) { const r = 60 + k * 45 + 40 * u; c.beginPath(); c.arc(PH.x + PH.w / 2 + sd * (PH.w / 2 + 10), PH.y + 110, r, sd > 0 ? -.9 : Math.PI - .4, sd > 0 ? .4 : Math.PI + .9); c.stroke(); }
  c.restore(); } }

// ---------------- the villain on the line ----------------
function lurker(c, t, t0, out = 0) {   // the Scammer peeks from behind the phone's right edge, head below the captions
  const a = easeOutBack(land(t, t0)); if (t < t0 - SLAM) return;
  const x = 790 + 500 * easeIn(out), y = lerp(1500, 1160, a) - 700 * easeIn(out);
  scammer(c, x, y, .62, { sx: -1, head: .07 * Math.sin(t * 5), tilt: -.6 * easeIn(out), bob: Math.abs(Math.sin(t * Math.PI / BEAT)) * 4 });
}

// ================= setup =================
SCENES.setup = (c, t, S) => {
  sceneBg(c);
  const rings = [S.at(1, 1), S.at(1, 3)], picked = S.at(2, 1);
  const sx = t < picked ? ringShake(t, rings) : 0;
  lurker(c, t, picked);   // behind the phone
  c.save(); c.translate(sx, 0); phoneBody(c);
  if (t < picked) screenIncoming(c, t, S.t0); else screenInCall(c, t, picked);
  c.restore();
  if (t < picked) ringWaves(c, t, rings); else tapRing(c, PH.x + PH.w - 140, PH.y + 640, t, picked);
  if (t >= S.at(2, 3) - SLAM) stampFit(c, 'URGENT!', BLK, 150, PH.x + PH.w / 2, PH.y + 560, -.06, .9, t, S.at(2, 3), 520);
};

// ================= why: caller ID can be faked =================
const TAGS = [['YOUR BANK', NUM], ['GOVT OFFICE', '1-202-XXX-XXXX'], ['TECH SUPPORT', '1-888-XXX-XXXX'], ['YOUR BANK', NUM]];
const CID = { x: 110, y: 600, w: 740, h: 470 };
function tagCard(c, x, y, name, rot, seed) {
  c.save(); c.translate(x, y); c.rotate(rot);
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fillRect(-300 + 8, -70 + 10, 600, 140); c.restore();
  block(c, rrPts(-300, -70, 600, 140, 24, 5), YEL, seed, { kw: 6 });
  c.fillStyle = BLK; c.beginPath(); c.arc(-262, 0, 12, 0, TAU); c.fill();   // the sticker's pin hole
  inkText(c, name, 14, 8, 80, 'Stamp', BLK, 500); c.restore();
}
SCENES.why = (c, t, S) => {
  sceneBg(c);
  const swaps = [S.at(1, 2), S.at(1, 3), S.at(1, 4)]; let k = 0; swaps.forEach(ts => { if (t >= ts) k++; });
  const { x, y, w, h } = CID;
  shadowRect(c, x, y, w, h); block(c, rrPts(x, y, w, h, 34, 6), BLK, 8100, { kw: 6 }); block(c, rrPts(x + 20, y + 20, w - 40, h - 40, 24, 4), CHIP, 8101, { kw: 3 });
  inkText(c, 'CALLER ID', x + w / 2, y + 76, 40, SANS, BLK, 400);
  const tc = [x + w / 2, y + 220];
  tagCard(c, tc[0], tc[1], TAGS[k][0], k % 2 ? .02 : -.02, 8110 + k);
  inkText(c, TAGS[k][1], x + w / 2, y + 380, 50, MONO, BLK, 600);
  // the Scammer below, fishing the old tag off and slapping on the next one
  let rod = -.25; swaps.forEach(ts => { rod -= .3 * Math.sin(Math.PI * seg(t, ts - .15, ts + .2)); });   // he flicks the rod on each swap
  scammer(c, 700, 1480, .6, { sx: -1, rod, head: .08 * Math.sin(t * 6), bob: Math.abs(Math.sin(t * Math.PI / BEAT)) * 4 });
  swaps.forEach((ts, i) => { const u = seg(t, ts, ts + .4); if (u <= 0 || u >= 1) return;   // the old tag is flicked off sideways, level with itself
    tagCard(c, lerp(tc[0], 1250, easeIn(u)), tc[1] + 30 * u, TAGS[i][0], u * .6, 8120 + i); });
  if (t >= S.at(2, 3) - SLAM) stampFit(c, 'FAKE!', BLK, 170, 300, 1250, -.08, .9, t, S.at(2, 3), 420);
};

// ================= how: hang up, flip the card, call the number on the back =================
function bankCard(c, cx, cy, flip, t) {   // flip 0..1: front, edge-on at .5, back
  const sx = Math.abs(Math.cos(flip * Math.PI)), back = flip > .5, w = 700, h = 440;
  c.save(); c.translate(cx, cy); c.scale(Math.max(.02, sx), 1);
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fillRect(-w / 2 + 12, -h / 2 + 16, w, h); c.restore();
  if (!back) {
    block(c, rrPts(-w / 2, -h / 2, w, h, 34, 6), BLUE, 8200, { kw: 6 });
    inkText(c, 'YOUR BANK', -w / 2 + 50, -h / 2 + 80, 56, 'Stamp', CHIP, 420, 'left');
    block(c, rrPts(-w / 2 + 50, -40, 110, 84, 14, 4), YEL, 8201, { kw: 4 });
    inkText(c, 'XXXX XXXX XXXX 0000', 0, 120, 44, MONO, CHIP, w - 80);
  } else {
    block(c, rrPts(-w / 2, -h / 2, w, h, 34, 6), CHIP, 8210, { kw: 6 });
    ink(c, rect(-w / 2, -h / 2 + 50, w, 80), BLK, 8211, { reg: false });
    inkText(c, 'CUSTOMER SERVICE', 0, 20, 44, 'Stamp', BLK, w - 80);
    const hl = easeOut(seg(t, CARD_HL, CARD_HL + .2));
    if (hl > 0) ink(c, rect(-280, 70, 560 * hl, 84), YEL, 8212, { reg: false, amp: 3 });   // highlighter under the number
    inkText(c, NUM, 0, 114, 62, MONO, BLK, w - 80);
  }
  c.restore();
}
let CARD_HL = 0;
function screenDial(c, t, t0, pressed) {   // the dialer: digits typed on 32nds, then call
  const cx = PH.x + PH.w / 2, digits = NUM.replace(/-/g, ''), step = BEAT / 8;
  let n = Math.max(0, Math.min(digits.length, Math.floor((t - t0) / step) + 1)); if (t < t0) n = 0;
  let shown = '', d = 0; for (const ch of NUM) { if (ch === '-') { if (d > 0 && d < n) shown += '-'; continue; } if (d < n) shown += ch; d++; }
  inkText(c, shown || ' ', cx, PH.y + 150, 54, MONO, BLK, 500);
  const keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '#'];
  keys.forEach((kk, i) => { const kx = cx + ((i % 3) - 1) * 130, ky = PH.y + 250 + Math.floor(i / 3) * 95, hot = n > 0 && n <= digits.length && digits[n - 1] === kk && t - t0 < digits.length * step;
    block(c, ellPts(kx, ky, 40, 40, 0, 26), hot ? YEL : '#ffffff', 8300 + i, { kw: 3, reg: false }); inkText(c, kk, kx, ky + 4, 38, 'Stamp', BLK, 60); });
  callButton(c, cx, PH.y + 670, BLUE, false, pressed ? .9 : 1);
}
SCENES.how = (c, t, S) => {
  sceneBg(c);
  const b1 = S.at(1), tap = S.at(1, 3), b2 = S.at(2), flipT = S.at(2, 3), b3 = S.at(3), dialT = S.at(3, 1.5), callT = S.at(3, 3), b4 = S.at(4);
  CARD_HL = S.at(2, 4);
  const cx = PH.x + PH.w / 2;
  // bar 1: still on the call; Jeff taps hang-up on 3 and the Scammer is yanked off
  if (t < b2 + .3) {
    const out = easeIn(seg(t, b2 - .05, b2 + .3));   // the phone drops out as the card rises
    lurker(c, t, b1 - 1, seg(t, S.at(1, 3.5), S.at(1, 4.5)));
    c.save(); c.translate(0, 900 * out); phoneBody(c);
    if (t < tap) { screenInCall(c, t, b1 - 6); callButton(c, cx, PH.y + 640, BLK, true); }
    else { avatar(c, PH.y + 180, BLK, 'X'); inkText(c, 'CALL ENDED', cx, PH.y + 350, 64, 'Stamp', BLK, 480); inkText(c, 'YOUR BANK', cx, PH.y + 425, 40, SANS, BLK, 480); }
    c.restore(); if (t < b2) tapRing(c, cx, PH.y + 640, t, tap);
  }
  // bar 2: the card rises, flips on 3; the number on the back gets highlighted on 4
  if (t >= b2 - .05 && t < b3 + .3) {
    const up = easeOut(seg(t, b2 - .05, b2 + .3)), out = easeIn(seg(t, b3 - .05, b3 + .3));
    bankCard(c, SCX - 1100 * out, lerp(1900, 860, up), clamp01((t - flipT + .15) / .3), t);
  }
  // bars 3-4: the dialer rises; digits on 32nds from 1.5, call on 3; bar 4: connected, with a check
  if (t >= b3 - .05) {
    const up = easeOut(seg(t, b3 - .05, b3 + .3));
    c.save(); c.translate(0, 1300 * (1 - up)); phoneBody(c);
    if (t < callT) screenDial(c, t, dialT, false);
    else if (t < b4) { screenInCall(c, t, callT, 'CALLING...', NUM); }
    else { screenInCall(c, t, b4, 'YOUR BANK', 'YOU DIALED IT'); }
    c.restore();
    if (t >= callT && t < b4) tapRing(c, cx, PH.y + 670, t, callT);
    check(c, PH.x + PH.w - 80, PH.y + 520, .75, t, S.at(4, 2));
  }
  // Jeff: points at hang-up in bar 1, at the card in bar 2, thumbs up in bar 4
  const th = easeOutBack(seg(t, S.at(4, 2), S.at(4, 2.4)));
  jeffUp(c, t, S.at(1, 1.5), 120, t >= b4 ? { armR: lerp(-2.2, -2.5, th), prop: th > .6 ? 'thumb' : 'point', head: .06 } : { armR: -2.2, prop: 'point', head: .05 }, .56);
};
