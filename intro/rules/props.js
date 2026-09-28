'use strict';
/* JEFF'S RULES shared props: the phone (incoming call, on a call, buttons), ringing, and the Scammer lurking on
   the line. Moved out of episode 1 so every episode can use them; load after rules.js and before rules/epNN.js. */
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
