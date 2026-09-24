'use strict';
/* Rossen Reports explainer: the fake officer / jury-duty warrant scam. 52 s, 1080x1920 (9:16), 24 fps, one continuous
   film. Case-file screen-print look (printkit.js), the approved palette, the MyChart explainer's grammar: 96 BPM, one
   bar = 2.5 s, one idea per bar, a caption on each downbeat, every landing finishes ON its beat (SLAM early start).
   Text and key action stay inside the platform safe zone (VERT_K 0.895: content x 60-900, y 300-1430).
   Puppets: the Scammer in his fake-officer disguise (cap and badge are separate pieces) and the everyday man, cut by
   tools/cut_officer.py; Jeff from printkit.js. No real courts, counties, agencies, officers, badges, seals or numbers.

   HOOK    bar 0  0.0   his phone is ringing in frame 0: SHERIFF'S OFFICE                   "YOU MISSED / JURY DUTY."
           bar 1  2.5   he answers; the "officer" slides in on the other end              "THERE'S A WARRANT / FOR YOUR ARREST."
   REAL    bar 2  5.0   his name and address pop out of the call (beats 2, 3)              "HE KNOWS YOUR / NAME AND ADDRESS"
           bar 3  7.5   a badge number and a case number (beats 2, 3)                      "HE GIVES A BADGE / AND CASE NUMBER"
           bar 4  10.0  the real caller ID (UNKNOWN NUMBER); a SHERIFF'S OFFICE sticker     "EVEN CALLER ID / CAN BE FAKED"
                        pops out of the Scammer's phone and is slapped over it on 3
   CRAZIER bar 5  12.5  a text arrives on 2 (buzzes on 2 and 3): ACTIVE WARRANT; tap on 4, dive in     "THEN A TEXT / WITH A WARRANT"
           bar 6  15.0  the fake warrant: his name, AMOUNT DUE: $1,700, nonsense fine print "PAY $1,700 / OR BE ARRESTED"
           bar 7  17.5  the demands stack up: GIFT CARDS (2), PAYMENT APP (4)              "IT GETS / CRAZIER."
           bar 8  20.0  CRYPTO (2), WIRE TRANSFER (4)                                      "PAY RIGHT NOW / OR ELSE!"
           bar 9  22.5  the list is swept away: a cash bag (1), a meet-up pin (3)          "BRING CASH. / I'LL MEET YOU."
   TELLS   bar 10 25.0  the screen-print logo slams down and knocks him off; Jeff pops up  "HERE'S HOW / TO SPOT IT"
           bar 11 27.5  the magnifier on the cap: LIE #1 on 3, the cap slips over his eyes "COURTS NEVER / CALL FOR PAYMENT"
           bar 12 30.0  the magnifier on the badge: LIE #2 on 3, it drops off (lands on 4) "WARRANTS NEVER / COME BY TEXT"
           bar 13 32.5  the magnifier on his face: LIE #3 on 3, the cap flies off (lands 4) "NEVER GIVE YOUR / SSN OR BIRTHDATE"
   FIX     bar 14 35.0  his phone: the END button, tapped on 3: CALL ENDED                 "HANG UP."
           bar 15 37.5  a search types YOUR LOCAL COURT; the court's own listing on 3      "LOOK UP THE / COURT'S NUMBER"
           bar 16 40.0  he calls that number; Jeff thumbs up, a check on 3                  "CALL THE COURT / YOURSELF"
           bar 17 42.5  an address bar types ReportFraud.ftc.gov (big on 2); REPORT IT on 3            "REPORT IT AT"
   LINE    bar 18 45.0  HANG UP. on 1, CALL THE COURT on 3, YOURSELF. on 4, Jeff thumbs up
           bar 19 47.5  held; the rubber stamp comes down on 4
   END     bar 20 50.0  the official logo, untouched, revealed as the stamp lifts; still from 50.3
*/
const DUR = at(20) + 2, NFR = Math.round(FPS * DUR);
const SANS = '"Liberation Sans"', MONO = '"Liberation Mono"', FAKE_NUM = '1-555-XXX-XXXX', URL_REAL = 'ReportFraud.ftc.gov';
const PUSH = .3;   // the camera drop between scenes, centred on the downbeat

// ================= captions: black paper chips at the top of the safe zone, one set per downbeat =================
const CAPS = [
  [at(0), 'YOU MISSED', 'JURY DUTY.'], [at(1), "THERE'S A WARRANT", 'FOR YOUR ARREST.'], [at(2), 'HE KNOWS YOUR', 'NAME AND ADDRESS'],
  [at(3), 'HE GIVES A BADGE', 'AND CASE NUMBER'], [at(4), 'EVEN CALLER ID', 'CAN BE FAKED'], [at(5), 'THEN A TEXT', 'WITH A WARRANT'],
  [at(6), 'PAY $1,700', 'OR BE ARRESTED'], [at(7), 'IT GETS', 'CRAZIER.'], [at(8), 'PAY RIGHT NOW', 'OR ELSE!'], [at(9), 'BRING CASH.', "I'LL MEET YOU."],
  [at(10), "HERE'S HOW", 'TO SPOT IT'], [at(11), 'COURTS NEVER', 'CALL FOR PAYMENT'], [at(12), 'WARRANTS NEVER', 'COME BY TEXT'],
  [at(13), 'NEVER GIVE YOUR', 'SSN OR BIRTHDATE'], [at(14), 'HANG UP.'], [at(15), 'LOOK UP THE', "COURT'S NUMBER"], [at(16), 'CALL THE COURT', 'YOURSELF'],
  [at(17), 'REPORT IT AT'], [at(18), null],
];
function chip(c, s, x, y, size, bg, fg, t, t0, rot = 0, maxW = 730, from = 1.1, font = 'Stamp') {   // a paper chip; landing included, it stays inside maxW + 60
  if (t < t0 - SLAM) return; c.font = `${size}px ${font}`; const w = Math.min(c.measureText(s).width, maxW) + 60, h = size * 1.3, k = t < t0 ? lerp(from, 1, easeIn(land(t, t0))) : pop(t, t0);
  c.save(); c.translate(x, y); c.rotate(rot); c.scale(k, k);
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fillRect(-w / 2 + 8, -h / 2 + 10, w, h); c.restore();
  ink(c, rect(-w / 2, -h / 2, w, h), bg, 8100 + s.length, { amp: 3 }); inkText(c, s, 0, size * .06, size, font, fg, maxW); c.restore();
}
function captionsTop(c, t) {
  let cur = null; for (const cp of CAPS) if (t >= cp[0] - SLAM) cur = cp;
  if (!cur || !cur[1]) return;
  cur.slice(1).forEach((s, i) => chip(c, s, SCX, 376 + i * 112, 66, BLK, CHIP, t, cur[0] + i * E8, i % 2 ? .012 : -.012, 700));   // 760 wide at most: +-418 even at the 1.1x landing
}

// ================= puppets =================
const PUP = {};
// pose: { head, arm, legL, legR, bob, tilt, sx, cap: {dx, dy, rot}, badge: {dx, dy, rot, flip} } (offsets in reference pixels)
function puppet(c, name, x, y, s, p = {}) {
  const M = PUP[name];
  c.save(); c.translate(x, y); c.rotate(p.tilt || 0); c.scale(s * (p.sx || 1), s); c.translate(-M.feet[0], -M.feet[1] - (p.bob || 0));
  const part = (k, a = 0, o = null) => { const m = M.parts[k]; if (!m) return; const [px, py] = m.pivot; c.save(); c.translate(px, py);
    if (o) { c.translate(o.dx || 0, o.dy || 0); c.rotate(o.rot || 0); if (o.flip !== undefined) c.scale(Math.cos(o.flip), 1); } c.rotate(a); c.translate(-px, -py);
    const back = o && o.flip !== undefined && Math.cos(o.flip) < 0; c.drawImage(back ? IMG[name + '_' + k + '_back'] : IMG[name + '_' + k], m.x, m.y); c.restore(); };
  part('legL', p.legL || 0); part('legR', p.legR || 0); part('torso');
  if (name === 'officer') part('badge', 0, p.badge || {});
  if (name === 'officer') { c.save(); const [hx, hy] = M.parts.head.pivot; c.translate(hx, hy); c.rotate(p.head || 0); c.translate(-hx, -hy); part('head'); part('cap', 0, p.cap || {}); c.restore(); }
  else part('head', p.head || 0);
  part('arm', p.arm || 0);
  c.restore();
}
const bobOf = (t, a = 4, per = BEAT) => Math.abs(Math.sin(t * Math.PI / per)) * a;
function man(c, x, y, s, t, p = {}) { puppet(c, 'man', x, y, s, Object.assign({ head: .03 * Math.sin(t * 2.1), bob: bobOf(t, 3, 2 * BEAT) }, p)); }
// the disguise falls apart, one piece per lie (all offsets in the officer's reference pixels)
const LIE = [at(11, 3), at(12, 3), at(13, 3)];
function disguise(t) {
  const cap = { dx: 0, dy: 0, rot: 0 }, badge = { dx: 0, dy: 0, rot: 0 };
  const s1 = easeOutBack(seg(t, LIE[0] - .05, LIE[0] + .2));   // lie 1: the cap slips down over his eyes
  cap.dx = -12 * s1; cap.dy = 52 * s1; cap.rot = .28 * s1;
  if (t >= LIE[1] - SLAM) {   // lie 2: the badge pops off and drops to the floor (lands on beat 4), face down: cardboard and tape
    const u = seg(t, LIE[1], LIE[1] + BEAT), pop0 = easeOut(seg(t, LIE[1] - SLAM, LIE[1]));
    badge.dx = 30 * pop0 + 120 * u; badge.dy = -30 * pop0 + 400 * (u * u) + 30 * pop0 * u; badge.rot = 2.2 * u; badge.flip = Math.PI * Math.min(1, u * 1.2);
    if (t > LIE[1] + BEAT) { const v = t - LIE[1] - BEAT; badge.dy -= 26 * Math.abs(Math.sin(v * 14)) * Math.exp(-v * 7); }
  }
  if (t >= LIE[2] - SLAM) {   // lie 3: the cap flies off, spins and lands on the floor beside him on beat 4
    const u = seg(t, LIE[2] - SLAM, LIE[2] + BEAT), e = u;
    cap.dx = lerp(-12, 90, e); cap.dy = lerp(52, 740, e) - 520 * Math.sin(Math.min(1, e) * Math.PI) * .9; cap.rot = lerp(.2, 3.3, easeOut(e));
    if (t > LIE[2] + BEAT) { const v = t - LIE[2] - BEAT; cap.dy -= 20 * Math.abs(Math.sin(v * 13)) * Math.exp(-v * 7); }
  }
  return { cap, badge };
}
function officer(c, x, y, s, t, p = {}) {
  const d = disguise(t);
  puppet(c, 'officer', x, y, s, Object.assign({ head: .035 * Math.sin(t * TAU / (2 * BEAT)), arm: .03 * Math.sin(t * TAU / BEAT), bob: bobOf(t, 4), cap: d.cap, badge: d.badge }, p));
}
const O_PHONE = [845, 500];   // the officer's handset in his reference
function refPt(name, pt, x, y, s, bob = 0) { const M = PUP[name]; return [x + (pt[0] - M.feet[0]) * s, y + (pt[1] - M.feet[1] - bob) * s]; }

// ================= shared bits =================
function ringWaves(c, x, y, t, t0s) { for (const t0 of t0s) { const u = seg(t, t0, t0 + .6); if (u <= 0 || u >= 1) continue;
  c.save(); c.globalAlpha = 1 - u; c.strokeStyle = YEL; c.lineWidth = 11; c.lineCap = 'round';
  for (const sd of [-1, 1]) for (let k = 0; k < 2; k++) { const r = 44 + k * 38 + 34 * u; c.beginPath(); c.arc(x, y, r, sd > 0 ? -.8 : Math.PI - .8, sd > 0 ? .8 : Math.PI + .8); c.stroke(); }
  c.restore(); } }
function card(c, R, bg = CHIP, seed = 9001) { const { x, y, w, h } = R; shadowRect(c, x, y, w, h); block(c, rrPts(x, y, w, h, 28, 6), BLK, seed, { kw: 6 }); block(c, rrPts(x + 14, y + 14, w - 28, h - 28, 18, 4), bg, seed + 1, { kw: 3 }); }
const lerpR = (a, b, u) => ({ x: lerp(a.x, b.x, u), y: lerp(a.y, b.y, u), w: lerp(a.w, b.w, u), h: lerp(a.h, b.h, u) });
function sceneBg(c, col = BLUE, lo = .07, hi = .38) { bgDots(c, col, lo, hi); }
// the close-ups (the text, the warrant) sit on textured cream stock: the paper, soft mottling and faint fibres, no dots.
// Static, made once at load in screen space.
let CREAM_TEX = null;
function makeCream() {
  const o = document.createElement('canvas'); o.width = OUT_W; o.height = OUT_H; const g = o.getContext('2d'); g.setTransform(OUT_W / W, 0, 0, OUT_H / H, 0, 0);
  g.fillStyle = CREAM; g.fillRect(0, 0, W, H); const r = rng(9801);   // the palette cream
  for (let i = 0; i < 60000; i++) { g.fillStyle = r() < .55 ? 'rgba(170,150,110,0.10)' : 'rgba(255,253,245,0.35)'; const z = .8 + r() * 1.6; g.fillRect(r() * W, r() * H, z, z); }   // fine grain
  for (let i = 0; i < 70; i++) { const x = r() * W, y = r() * H, rad = 120 + r() * 320, gr = g.createRadialGradient(x, y, 0, x, y, rad);   // mottling
    const dark = r() < .35, rgb = dark ? '190,170,125' : '255,252,240'; gr.addColorStop(0, `rgba(${rgb},${dark ? .05 : .16})`); gr.addColorStop(1, `rgba(${rgb},0)`); g.fillStyle = gr; g.fillRect(x - rad, y - rad, 2 * rad, 2 * rad); }   // each blotch fades to its own colour: a fade to transparent black turns grey
  g.lineCap = 'round';
  for (let i = 0; i < 900; i++) { const x = r() * W, y = r() * H, a = r() * TAU, l = 6 + r() * 26, bend = (r() - .5) * 10;   // paper fibres
    g.strokeStyle = r() < .6 ? 'rgba(150,125,85,0.14)' : 'rgba(255,255,250,0.45)'; g.lineWidth = .8 + r() * .9;
    g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + Math.cos(a) * l / 2 - Math.sin(a) * bend, y + Math.sin(a) * l / 2 + Math.cos(a) * bend, x + Math.cos(a) * l, y + Math.sin(a) * l); g.stroke(); }
  CREAM_TEX = o;
}
function creamBg(c) { c.save(); resetT(c); c.drawImage(CREAM_TEX, 0, 0, W, H); c.restore(); }
function handset(c, x, y, s, col = BLK) {   // a phone-handset glyph
  c.save(); c.translate(x, y); c.scale(s, s); c.rotate(-.6);
  block(c, [[-60, -26], [-30, -26], [-24, -8], [24, -8], [30, -26], [60, -26], [64, 6], [40, 22], [28, 8], [-28, 8], [-40, 22], [-64, 6]], col, 9901, { kw: 0, key: false }); c.restore();
}
function sparkle(c, x, y, r, t, t0) { const u = seg(t, t0, t0 + .45); if (u <= 0 || u >= 1) return; const k = Math.sin(u * Math.PI) * r;
  c.save(); c.translate(x, y); c.rotate(u * 1.2); c.fillStyle = YEL; c.strokeStyle = BLK; c.lineWidth = 4;
  c.beginPath(); for (let i = 0; i < 8; i++) { const a = i / 8 * TAU, rr = i % 2 ? k * .28 : k; c.lineTo(Math.cos(a) * rr, Math.sin(a) * rr); } c.closePath(); c.fill(); c.stroke(); c.restore(); }
function pushScenes(c, t, tb, A, B) {   // the camera drops from scene A to scene B, centred on the downbeat tb
  const u = easeIO(seg(t, tb - PUSH / 2, tb + PUSH / 2)), g1 = L1.getContext('2d'), g2 = L2.getContext('2d');
  // each scene carries its own caption, so the new caption never lands on the old scene's content
  contentT(g1); g1.globalAlpha = 1; A(g1, t); contentT(g1); captionsTop(g1, Math.min(t, tb - SLAM - 1e-3));
  contentT(g2); g2.globalAlpha = 1; B(g2, t); contentT(g2); captionsTop(g2, Math.max(t, tb - SLAM));
  c.save(); resetT(c); c.drawImage(L1, 0, -u * H, W, H); c.drawImage(L2, 0, (1 - u) * H, W, H); c.restore();
}

// ================= HOOK + WHY IT FEELS REAL: the call (bars 0-4) =================
const MAN_AT = [250, 1430, .66], OFF_AT = [728, 1430, .48];
const RING_T = [-.05, at(0, 3), at(1) - .02];
const CARD_BIG = { x: 90, y: 590, w: 780, h: 300 }, STRIP = { x: 90, y: 566, w: 780, h: 84 }, CARD_SWAP = { x: 80, y: 590, w: 520, h: 330 };
const LABEL = { x: 110, y: 690, w: 480, h: 150 };   // the caller-ID label slot on the bar-4 card
function manPhonePt(t) { return refPt('man', [975, 380], ...MAN_AT, bobOf(t, 3, 2 * BEAT)); }
function sceneCall(c, t) {
  sceneBg(c);
  const ans = at(1), inO = easeOut(land(t, ans)), out4 = 0;
  // the officer slides in on the other end of the line when he answers
  const ox = lerp(1300, OFF_AT[0], inO);
  if (inO > 0) {
    const ph = refPt('officer', O_PHONE, ox, OFF_AT[1], OFF_AT[2]), mp = manPhonePt(t);
    // the line between the two phones, arcing over their heads
    c.save(); c.strokeStyle = BLK; c.lineWidth = 7; c.setLineDash([18, 14]); c.lineDashOffset = -t * 90; c.beginPath(); c.moveTo(mp[0] + 20, mp[1] - 40); c.quadraticCurveTo(470, 760, ph[0] - 30, ph[1] - 40); c.stroke(); c.restore();
    const glee = t > at(4, 3) ? .09 * Math.sin((t - at(4, 3)) * 16) * Math.exp(-(t - at(4, 3)) * 2) : 0;
    officer(c, ox, OFF_AT[1], OFF_AT[2], t, { head: .035 * Math.sin(t * TAU / (2 * BEAT)) + glee });
    sparkle(c, refPt('officer', [790, 760], ox, OFF_AT[1], OFF_AT[2])[0] + 30, refPt('officer', [790, 760], ox, OFF_AT[1], OFF_AT[2])[1] - 30, 46, t, at(3, 2) - .1);   // the badge glints
  }
  // the man: the phone jiggles while it rings, then he listens; startled on the warrant
  let jig = 0; for (const r of RING_T) if (t >= r && t < r + .45) jig += Math.sin((t - r) * 70) * .05 * (1 - (t - r) / .45);
  const startle = easeOutBack(seg(t, at(1, 3) - SLAM, at(1, 3) + .15)) * (1 - easeIO(seg(t, at(2, 3), at(3))));
  man(c, ...MAN_AT, t, { arm: jig, head: .03 * Math.sin(t * 2.1) - .08 * startle, bob: bobOf(t, 3, 2 * BEAT) + 14 * startle });
  if (t < ans + .3) { const mp = manPhonePt(t); ringWaves(c, mp[0], mp[1] - 30, t, RING_T); }
  // the caller-ID card: big while it rings, a strip while they talk, back for the swap in bar 4
  const toStrip = easeIO(seg(t, ans, ans + .3)), toSwap = easeIO(land(t, at(4)));
  let sx = 0; for (const r of RING_T) if (t >= r && t < r + .45 && t < ans) sx += Math.sin((t - r) * 90) * 8 * (1 - (t - r) / .45);
  if (toSwap <= 0) {
    const R = lerpR(CARD_BIG, STRIP, toStrip);
    c.save(); c.translate(sx, 0); card(c, R);
    if (toStrip < .5) { c.save(); c.globalAlpha = 1 - toStrip * 2;
      inkText(c, 'INCOMING CALL', R.x + R.w / 2, R.y + 66, 38, SANS, BLK, R.w - 80);
      inkText(c, "SHERIFF'S OFFICE", R.x + R.w / 2, R.y + 152, 70, 'Stamp', BLK, R.w - 70);
      inkText(c, FAKE_NUM, R.x + R.w / 2, R.y + 232, 40, MONO, BLK, R.w - 80); c.restore(); }
    else { c.save(); c.globalAlpha = (toStrip - .5) * 2; const secs = Math.max(0, Math.floor((t - ans) * 1.6));
      inkText(c, `ON CALL 00:${String(secs).padStart(2, '0')}`, R.x + 34, R.y + R.h / 2 + 2, 28, MONO, BLK, 260, 'left');
      inkText(c, "SHERIFF'S OFFICE", R.x + R.w - 36, R.y + R.h / 2 + 4, 44, 'Stamp', BLK, 460, 'right'); c.restore(); }
    c.restore();
  } else {   // bar 4: the real caller ID, and the swap
    const R = lerpR(STRIP, CARD_SWAP, toSwap); card(c, R);
    if (toSwap > .6) { c.save(); c.globalAlpha = (toSwap - .6) / .4;
      inkText(c, 'REAL CALLER ID', R.x + R.w / 2, R.y + 58, 32, SANS, BLK, R.w - 80);
      block(c, rect(LABEL.x, LABEL.y, LABEL.w, LABEL.h), '#ffffff', 9020, { kw: 4, reg: false });
      inkText(c, 'UNKNOWN', LABEL.x + LABEL.w / 2, LABEL.y + 50, 58, 'Stamp', BLK, LABEL.w - 50);
      inkText(c, 'NUMBER', LABEL.x + LABEL.w / 2, LABEL.y + 110, 58, 'Stamp', BLK, LABEL.w - 50);
      inkText(c, FAKE_NUM, R.x + R.w / 2, R.y + R.h - 50, 36, MONO, BLK, R.w - 80); c.restore(); }
    swapSticker(c, t);
  }
  // bars 2-3: what he knows and what he "gives": each pops out of the call on its beat
  if (t >= at(2) - SLAM && t < at(4) - SLAM) {
    const b3 = t >= at(3) - SLAM;
    const L = b3 ? [['BADGE #000-00', at(3, 2), BLK, CHIP], ['CASE NO. 00-0000', at(3, 3), BLUE, CHIP]] : [['JOHN DOE', at(2, 2), BLUE, CHIP], ['123 ANY STREET', at(2, 3), BLK, CHIP]];
    L.forEach(([s, t0, bg, fg], i) => chip(c, s, SCX + (i ? 30 : -30), 722 + i * 104, 56, bg, fg, t, t0, i ? .02 : -.025, 640, 1.3));
  }
}
function swapSticker(c, t) {   // the fake label pops out of the Scammer's phone, rises beside the card, then slides into the slot on beat 3
  const t0 = at(4, 2) - .1, t1 = at(4, 3); if (t < t0) return;
  const ph = refPt('officer', O_PHONE, ...OFF_AT), up = easeOut(seg(t, t0, t0 + .3)), inn = easeIn(land(t, t1));
  const px = lerp(ph[0], 770, up), py = lerp(ph[1] - 40, LABEL.y + LABEL.h / 2, up);
  const x = lerp(px, LABEL.x + LABEL.w / 2, inn), y = py, s = lerp(lerp(.2, .36, up), 1, inn), rot = lerp(lerp(1.4, .2, up), -.02, inn);
  c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s);
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fillRect(-LABEL.w / 2 + 8, -LABEL.h / 2 + 10, LABEL.w, LABEL.h); c.restore();
  block(c, rect(-LABEL.w / 2, -LABEL.h / 2, LABEL.w, LABEL.h), YEL, 9030, { kw: 5 });
  inkText(c, "SHERIFF'S", 0, -26, 60, 'Stamp', BLK, LABEL.w - 50); inkText(c, 'OFFICE', 0, 36, 60, 'Stamp', BLK, LABEL.w - 50);
  if (t > t1) { const pk = .5 + .5 * Math.sin((t - t1) * 5); c.fillStyle = CHIP; c.globalAlpha = .9; c.beginPath(); c.moveTo(LABEL.w / 2, -LABEL.h / 2); c.lineTo(LABEL.w / 2 - 40 - 8 * pk, -LABEL.h / 2); c.lineTo(LABEL.w / 2, -LABEL.h / 2 + 40 + 8 * pk); c.fill(); }   // a corner curls: it's a sticker
  c.restore();
}

// ================= IT GETS CRAZIER =================
const PH = { x: 230, y: 596, w: 500, h: 830 }, BUBBLE = { x: 262, y: 780, w: 436, h: 300 };
const TAP = [BUBBLE.x + BUBBLE.w / 2 + 146, BUBBLE.y + BUBBLE.h - 22];   // the pill's right end: the pointer never covers its label
function textPhone(c, t) {   // bar 5: a text arrives
  creamBg(c);
  const buzz = [at(5, 2), at(5, 3)]; let sx = 0; for (const b of buzz) if (t >= b && t < b + .2) sx += Math.sin((t - b) * 110) * 7 * (1 - (t - b) / .2);
  c.save(); c.translate(sx, 0);
  shadowRect(c, PH.x, PH.y, PH.w, PH.h); block(c, rrPts(PH.x, PH.y, PH.w, PH.h, 56, 6), BLK, 9101, { kw: 6 });
  block(c, rrPts(PH.x + 22, PH.y + 60, PH.w - 44, PH.h - 120, 18, 4), CHIP, 9102, { kw: 3 });
  ink(c, rect(PH.x + 22, PH.y + 60, PH.w - 44, 84), BLUE, 9103); inkText(c, 'MESSAGES', PH.x + PH.w / 2, PH.y + 104, 40, 'Stamp', CHIP, PH.w - 90);
  tapRing(c, TAP[0], TAP[1], t, at(5, 4));   // behind the bubble: the ring never crosses its text
  const k = pop(t, at(5, 2));
  if (t >= at(5, 2) - SLAM) { const { x, y, w, h } = BUBBLE; c.save(); c.translate(x + w / 2, y + h / 2); c.scale(k, k); c.translate(-x - w / 2, -y - h / 2);
    block(c, [...rrPts(x, y, w, h, 30, 5)], '#ffffff', 9110, { kw: 5, reg: false });
    inkText(c, 'OFFICIAL NOTICE:', x + w / 2, y + 62, 40, 'Stamp', BLK, w - 50);
    inkText(c, 'ACTIVE WARRANT', x + w / 2, y + 128, 40, 'Stamp', BLUE, w - 50);
    inkText(c, 'IN YOUR NAME.', x + w / 2, y + 186, 34, SANS, BLK, w - 50);
    pill(c, x + w / 2, y + h - 52, 300, 70, YEL, 'TAP TO VIEW', 34, BLK, 9111); c.restore(); }
  c.restore();
  if (t > at(5, 4) - .25) { const u = easeOut(seg(t, at(5, 4) - .25, at(5, 4))); cursorArrow(c, lerp(760, TAP[0], u), lerp(1380, TAP[1], u), t > at(5, 4) ? .88 : 1); }
}
const DOC = { x: 90, y: 590, w: 780, h: 830 };
const FINE = ['PURSUANT TO SUBSECTION 00(Z) OF THE WHEREAS', 'ACT, THE PARTY HEREINAFTER SHALL REMIT', 'FORTHWITH OR BE DEEMED IN CONTEMPT OF THE', 'HEREUNTO AFOREMENTIONED NOTWITHSTANDING,', 'ET CETERA, ET CETERA, AND SO ON AND SO ON.'];
function warrant(c, t) {   // bar 6: the fake warrant
  creamBg(c);
  const { x, y, w, h } = DOC;
  shadowRect(c, x, y, w, h); block(c, rect(x, y, w, h), CHIP, 9201, { kw: 6 });
  ink(c, rect(x, y, w, 120), BLK, 9202); inkText(c, 'WARRANT FOR ARREST', x + w / 2, y + 64, 58, 'Stamp', CHIP, w - 60);
  inkText(c, 'NAME: JOHN DOE', x + 40, y + 196, 50, 'Stamp', BLK, w - 80, 'left');
  inkText(c, 'CASE NO. 00-0000', x + 40, y + 262, 32, MONO, BLK, w - 80, 'left');
  const hl = easeOut(seg(t, at(6, 2) - SLAM, at(6, 2)));
  if (hl > 0) ink(c, rect(x + 26, y + 312, (w - 52) * hl, 104), YEL, 9203, { amp: 3 });
  key(c, rect(x + 26, y + 312, w - 52, 104), 5, 9204);
  inkText(c, 'AMOUNT DUE: $1,700', x + w / 2, y + 368, 58, 'Stamp', BLK, w - 100);
  FINE.forEach((s, i) => inkText(c, s, x + 40, y + 470 + i * 42, 24, MONO, BLK, w - 80, 'left'));
  if (t >= at(6, 3) - SLAM) { const k = pop(t, at(6, 3)); c.save(); c.translate(x + w / 2, y + h - 96); c.scale(k, k); pill(c, 0, 0, 440, 110, BLUE, 'PAY NOW', 60, CHIP, 9205); c.restore(); }
}
// the demands stack up on the left while he gets more and more excited
const ITEMS = [['GIFT CARDS', at(7, 2)], ['PAYMENT APP', at(7, 4)], ['CRYPTO', at(8, 2)], ['WIRE TRANSFER', at(8, 4)]];
const DEM_AT = [724, 1424, .5];
function itemIcon(c, k) {
  if (k === 0) { block(c, rrPts(-38, -26, 76, 52, 8, 3), YEL, 9300, { kw: 4 }); ink(c, rect(-8, -26, 16, 52), BLUE, 9301, { reg: false }); ink(c, rect(-38, -6, 76, 12), BLUE, 9302, { reg: false }); }
  if (k === 1) { block(c, rrPts(-24, -40, 48, 80, 10, 3), BLK, 9303, { kw: 3 }); ink(c, rect(-17, -30, 34, 56), CHIP, 9304, { reg: false }); block(c, [[-10, -2], [6, -2], [6, -12], [18, 4], [6, 20], [6, 10], [-10, 10]], BLUE, 9305, { kw: 0, key: false }); }
  if (k === 2) { block(c, ellPts(0, 0, 40, 40, 0, 30), YEL, 9306, { kw: 4 }); block(c, ellPts(0, 0, 22, 22, 0, 6), BLUE, 9307, { kw: 3 }); }
  if (k === 3) { for (const [dy, dir] of [[-14, 1], [14, -1]]) block(c, [[-36 * dir, dy - 6], [14 * dir, dy - 6], [14 * dir, dy - 16], [38 * dir, dy], [14 * dir, dy + 16], [14 * dir, dy + 6], [-36 * dir, dy + 6]], BLUE, 9308 + dir, { kw: 3 }); }
}
function itemCard(c, k, x, y, t, t0, rot) {
  if (t < t0 - SLAM) return; const s = pop(t, t0);
  c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s);
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fillRect(-212, -44, 440, 100); c.restore();
  block(c, rect(-220, -52, 440, 100), CHIP, 9320 + k, { kw: 5 });
  c.save(); c.translate(-160, 0); itemIcon(c, k); c.restore();
  inkText(c, ITEMS[k][0], 40, 4, 42, 'Stamp', BLK, 300);
  c.restore();
}
function cashBag(c, x, y, s) { c.save(); c.translate(x, y); c.scale(s, s);
  block(c, [[-40, -120], [40, -120], [26, -86], [110, 10], [96, 110], [-96, 110], [-110, 10], [-26, -86]], YEL, 9340, { kw: 7 });
  block(c, rect(-44, -104, 88, 22), BLK, 9341, { kw: 0, key: false }); inkText(c, '$', 0, 20, 130, 'Stamp', BLK, 120); c.restore(); }
function mapPin(c, x, y, s) { c.save(); c.translate(x, y); c.scale(s, s);
  const P = []; for (let i = 0; i <= 30; i++) { const a = Math.PI * .8 + i / 30 * Math.PI * 1.4; P.push([Math.cos(a) * 70, -110 + Math.sin(a) * 70]); } P.push([0, 0]);
  block(c, P, BLUE, 9350, { kw: 6 }); block(c, ellPts(0, -112, 28, 28, 0, 20), CHIP, 9351, { kw: 4 });
  c.save(); c.globalAlpha = .35; c.fillStyle = BLK; c.beginPath(); c.ellipse(0, 6, 60, 14, 0, 0, TAU); c.fill(); c.restore(); c.restore(); }
function demands(c, t, o = {}) {
  sceneBg(c, BLUE, .08, .42);
  const knock = o.knock || 0, lvl = t < at(8) ? 1 : t < at(9) ? 1.6 : 2.4;   // he gets more excited with every demand
  const glee = .05 * lvl * Math.sin(t * TAU / (lvl > 2 ? E8 : BEAT));
  officer(c, DEM_AT[0] + knock * 900, DEM_AT[1] - knock * 300, DEM_AT[2], t, { head: glee, bob: bobOf(t, 4 * lvl, lvl > 2 ? E8 : BEAT), tilt: knock * 1.6 });
  // the list; swept off to the left on the downbeat of bar 9
  const sweep = easeIn(seg(t, at(9) - SLAM, at(9) + .15));
  if (sweep < 1) ITEMS.forEach(([s, t0], k) => { c.save(); c.translate(318 - sweep * (1100 + k * 120), 652 + k * 128); c.scale(1.12, 1.12); itemCard(c, k, 0, 0, t, t0, (k % 2 ? .02 : -.02) - sweep * .4); c.restore(); });
  if (!o.noCash && t >= at(9) - SLAM) { cashBag(c, 290, 840, pop(t, at(9)) * 1.05);
    if (t >= at(9, 3) - SLAM) { const k = pop(t, at(9, 3)); c.save(); c.setLineDash([14, 14]); c.strokeStyle = BLK; c.lineWidth = 6; c.beginPath(); c.moveTo(340, 980); c.quadraticCurveTo(360, 1100, 250 + 20, 1210); c.stroke(); c.restore(); mapPin(c, 270, 1300, .9 * k); } }
}

// ================= THE TELLS =================
function fixBg(c) { bgDots(c, BLUE, .06, .3); }
function scene10(c, t) {   // the screen-print logo slams down and knocks him off; Jeff pops up
  const k = easeIn(seg(t, at(10), at(10) + .55));
  fixBg(c);
  demands_officerOnly(c, t, k);
  const [sx, sy] = shake(t, [[at(10), 18]]);
  if (t < at(10) + .3) { c.save(); c.globalAlpha = 1 - seg(t, at(10), at(10) + .3); resetT(c); c.fillStyle = CHIP; c.fillRect(0, 0, W, H); c.restore(); }
  stickerLogo(c, SCX + sx, LOGO_Y + sy, 720, -.03, 1);
  const th = easeOutBack(seg(t, at(10, 2.5), at(10, 3)));
  jeffUp(c, t, at(10, 2), SCX, { armR: lerp(0, -2.5, th), prop: th > .6 ? 'thumb' : null });
}
function demands_officerOnly(c, t, knock) { officer(c, DEM_AT[0] + knock * 900, DEM_AT[1] - knock * 500, DEM_AT[2], t, { tilt: knock * 2 }); }
const LOGO_Y = 880;   // 720 x 502: at its 1.15x landing size it still clears the captions and the safe width
function logoIn(c, t) {   // the landing itself (the logo slams from 1.15x)
  const [sx, sy] = shake(t, [[at(10), 18]]); stickerLogo(c, SCX + sx, LOGO_Y + sy, 720, -.03, lerp(1.15, 1, easeIn(land(t, at(10)))));
}
const TEL_AT = [676, 1424, .55];
const LENS_ON = [[600, 300], [792, 760], [640, 540]];   // cap, badge, face (the officer's reference)
function tellsOfficer(c, t) { officer(c, ...TEL_AT, t, { head: .03 * Math.sin(t * TAU / (2 * BEAT)) - (t > LIE[2] ? .06 : 0) }); }
function tells(c, t) {
  fixBg(c);
  tellsOfficer(c, t);
  const bar = t < at(12) ? 0 : t < at(13) ? 1 : 2, b0 = at(11 + bar);
  // Jeff's magnifier moves to the next piece of the disguise on each downbeat
  const tgt = k => refPt('officer', LENS_ON[k], ...TEL_AT), prev = tgt(Math.max(0, bar - 1)), cur = tgt(bar);
  const mv = bar === 0 ? easeOutBack(seg(t, at(11) - .2, at(11) + .2)) : easeIO(seg(t, b0 - .25, b0 + .1));
  const start = bar === 0 ? [360, 1300] : prev, cx = lerp(start[0], cur[0], mv), cy = lerp(start[1], cur[1], mv) + 6 * Math.sin(t * 3);
  const J = jeff(c, 176, 1830, .66, { armR: -2.25, head: -.05 + .03 * Math.sin(t * 2), bob: bobOf(t, 3, 2 * BEAT) });
  const R = 104 + (bar === 2 ? 20 : 0);
  magnifier(c, cx, cy, R, J.hand, () => { c.translate(cx, cy); c.scale(1.7, 1.7); c.translate(-cx, -cy); fixBg(c); tellsOfficer(c, t); });
  // LIE #1, #2, #3 on beat 3
  if (t >= LIE[bar] - SLAM) stampFit(c, `LIE #${bar + 1}`, BLK, 150, 470, 700, bar % 2 ? .06 : -.07, .9, t, LIE[bar], 640, 1.3);   // 640 x 1.3 < 840: inside the safe width while it lands
}

// ================= THE FIX =================
const HP = { x: 180, y: 600, w: 600, h: 820 };
function hangup(c, t) {   // bar 14
  fixBg(c);
  const tap = at(14, 3), ended = t >= tap;
  shadowRect(c, HP.x, HP.y, HP.w, HP.h); block(c, rrPts(HP.x, HP.y, HP.w, HP.h, 60, 6), BLK, 9401, { kw: 6 });
  block(c, rrPts(HP.x + 24, HP.y + 60, HP.w - 48, HP.h - 120, 20, 4), CHIP, 9402, { kw: 3 });
  const cx = HP.x + HP.w / 2, secs = Math.min(59, 42 + Math.floor((t - at(14)) * 1.6));
  if (!ended) inkText(c, `ON CALL 01:${String(secs).padStart(2, '0')}`, cx, HP.y + 140, 36, MONO, BLK, HP.w - 100);
  else chip(c, 'CALL ENDED', cx, HP.y + 142, 50, BLUE, CHIP, t, tap, -.02, HP.w - 150, 1.2);
  inkText(c, "SHERIFF'S OFFICE", cx, HP.y + 250, 48, 'Stamp', BLK, HP.w - 100);
  inkText(c, FAKE_NUM, cx, HP.y + 320, 34, MONO, BLK, HP.w - 100);
  const press = t > tap && t < tap + .2 ? .9 : 1, by = HP.y + HP.h - 230;
  c.save(); c.translate(cx, by); c.scale(press, press); block(c, ellPts(0, 0, 100, 100, 0, 40), ended ? BLK : YEL, 9403, { kw: 6 }); handset(c, 4, 6, 1, ended ? YEL : BLK); c.restore();
  inkText(c, 'END', cx, by + 150, 40, 'Stamp', BLK, 200);
  tapRing(c, cx, by, t, tap);
  if (t > tap - .35 && t < tap + .5) { const u = easeOut(seg(t, tap - .35, tap)); cursorArrow(c, lerp(840, cx - 10, u), lerp(1500, by - 10, u), t > tap ? .88 : 1); }
}
const PB = { x: 90, y: 600, w: 780, h: 600 };
function browserFrame(c, text, seed = 9500) {
  shadowRect(c, PB.x, PB.y, PB.w, PB.h); block(c, rect(PB.x, PB.y, PB.w, PB.h), CHIP, seed, { kw: 6 });
  ink(c, rect(PB.x, PB.y, PB.w, 130), BLK, seed + 1);
  block(c, rrPts(PB.x + 30, PB.y + 30, PB.w - 60, 72, 36, 4), '#ffffff', seed + 2, { kw: 3, reg: false });
  inkText(c, text, PB.x + 64, PB.y + 68, 40, MONO, BLK, PB.w - 120, 'left');
}
const typed = (t, s, t0, t1) => s.slice(0, Math.max(0, Math.min(s.length, Math.floor((t - t0) / ((t1 - t0) / s.length)))));
const caret = t => (Math.floor(t * 4) % 2 ? '|' : '');
function lookup(c, t) {   // bar 15: search for the court yourself
  fixBg(c);
  const s = 'YOUR LOCAL COURT', txt = typed(t, s, at(15) + .1, at(15, 2.6));
  browserFrame(c, txt + (txt.length < s.length ? caret(t) : ''));
  c.save(); c.globalAlpha = .9; c.fillStyle = BLK; c.beginPath(); c.arc(PB.x + PB.w - 78, PB.y + 66, 16, 0, TAU); c.lineWidth = 6; c.strokeStyle = BLK; c.stroke(); c.beginPath(); c.moveTo(PB.x + PB.w - 66, PB.y + 78); c.lineTo(PB.x + PB.w - 54, PB.y + 90); c.stroke(); c.restore();
  if (t >= at(15, 3) - SLAM) { const k = pop(t, at(15, 3)); c.save(); c.translate(PB.x + PB.w / 2, PB.y + 350); c.scale(k, k);
    block(c, rect(-340, -150, 680, 300), '#ffffff', 9510, { kw: 5, reg: false });
    inkText(c, 'CLERK OF COURT', 0, -86, 58, 'Stamp', BLUE, 620); inkText(c, 'THE COURT\'S OWN WEBSITE', 0, -22, 30, SANS, BLK, 620);
    block(c, rrPts(-270, 30, 540, 90, 45, 4), YEL, 9511, { kw: 4 }); handset(c, -210, 76, .5); inkText(c, FAKE_NUM, 30, 78, 38, MONO, BLK, 420); c.restore(); }
  const pt = easeOut(seg(t, at(15, 3) - SLAM, at(15, 3)));
  jeff(c, 176, 1830, .66, { armR: lerp(0, -1.9, pt), prop: pt > .5 ? 'point' : null, head: .05 });
}
function callCourt(c, t) {   // bar 16: he calls that number himself
  fixBg(c);
  const R = { x: 90, y: 600, w: 780, h: 250 }; card(c, R);
  inkText(c, 'CALLING...', R.x + R.w / 2, R.y + 70, 36, SANS, BLK, R.w - 80);
  inkText(c, 'CLERK OF COURT', R.x + R.w / 2, R.y + 142, 62, 'Stamp', BLUE, R.w - 80);
  inkText(c, 'THE NUMBER YOU LOOKED UP', R.x + R.w / 2, R.y + 200, 28, MONO, BLK, R.w - 80);
  const mp = manPhonePt(t); ringWaves(c, mp[0], mp[1] - 30, t, [at(16, 1.5), at(16, 2.5)]);
  man(c, ...MAN_AT, t, { head: .05 + .03 * Math.sin(t * 2.4) });
  check(c, 470, 1010, .9, t, at(16, 3));
  const th = easeOutBack(seg(t, at(16, 2), at(16, 2.4)));
  jeff(c, 690, 1830, .62, { armR: lerp(0, -2.5, th), prop: th > .6 ? 'thumb' : null, head: -.04 });
}
function report(c, t) {   // bar 17: report it
  fixBg(c);
  const txt = typed(t, URL_REAL, at(17) + .1, at(17, 1.9));
  shadowRect(c, PB.x, PB.y, PB.w, PB.h); block(c, rect(PB.x, PB.y, PB.w, PB.h), CHIP, 9601, { kw: 6 });
  ink(c, rect(PB.x, PB.y, PB.w, 150), BLK, 9602);
  block(c, rrPts(PB.x + 26, PB.y + 30, PB.w - 52, 90, 45, 4), '#ffffff', 9603, { kw: 3, reg: false });
  inkText(c, txt + (txt.length < URL_REAL.length ? caret(t) : ''), PB.x + 58, PB.y + 77, 48, SANS, BLK, PB.w - 110, 'left');
  // the typed address, big and exact, once it's complete
  if (t >= at(17, 2) - SLAM) { const k = pop(t, at(17, 2)); c.save(); c.translate(SCX, PB.y + 290); c.scale(k, k); inkText(c, URL_REAL, 0, 0, 70, SANS, BLUE, 580); c.restore(); }   // 580 x 1.3 still fits inside the page
  if (t >= at(17, 3) - SLAM) { const k = pop(t, at(17, 3)); c.save(); c.translate(SCX, PB.y + 460); c.scale(k, k); pill(c, 0, 0, 420, 120, YEL, 'REPORT IT', 62, BLK, 9604); c.restore(); }
  const pt = easeOut(seg(t, at(17, 3) - SLAM, at(17, 3)));
  jeff(c, 176, 1830, .66, { armR: lerp(0, -1.9, pt), prop: pt > .5 ? 'point' : null, head: .05 });
}
function sceneLine(c, t) {   // bars 18-19: the protection line
  bgDots(c, BLUE, .1, .5);
  const [sx, sy] = shake(t, [[at(18), 14], [at(18, 3), 12]]);
  const beatPulse = t > at(19) ? 1 + .025 * Math.max(0, Math.cos((t - at(19)) * TAU / BEAT)) : 1;
  c.save(); c.translate(sx, sy);
  stampFit(c, 'HANG UP.', BLK, 160, SCX, 520, -.05, .9 * beatPulse, t, at(18), 700, 1.2);   // 700 x 1.2 = 840: inside the safe width while landing
  stampFit(c, 'CALL THE COURT', BLUE, 130, SCX, 750, .03, .8 * beatPulse, t, at(18, 3), 700, 1.2);
  stampFit(c, 'YOURSELF.', BLUE, 140, SCX, 930, -.03, .82 * beatPulse, t, at(18, 4), 700, 1.2);
  c.restore();
  const th = easeOutBack(seg(t, at(18, 2), at(18, 2.4))), nod = t > at(19) ? .05 * Math.sin((t - at(19)) * TAU / (2 * BEAT)) : 0;
  jeffUp(c, t, at(18, 2), SCX, { armR: lerp(0, -2.5, th), prop: th > .6 ? 'thumb' : null, head: nod }, .74);
  const d = seg(t, at(19, 4), at(20)); if (d > 0) screenSpace(c, () => rubberStamp(c, easeIn(d)));
}
function sceneSignoff(c, t) {
  paperBg(c);
  // the official logo: exact file, no texture, no recolour, no distortion; centred on the frame, inside the safe zone; held still
  const im = IMG.logo, [bx, by, bw, bh] = IMG.logoBox, lw = 720, lh = bh * lw / bw;
  c.drawImage(im, bx, by, bw, bh, CX - lw / 2, SCY - lh / 2, lw, lh);
  const lift = seg(t, at(20), at(20) + .3);
  if (lift < 1) { c.save(); c.translate(0, -(H + 320) * easeIn(lift)); rubberStampFlat(c); c.restore(); }
}

// ================= assembly =================
const SCENES = [   // [first bar, draw]; a push between consecutive scenes unless noted
  [0, sceneCall], [5, textPhone], [6, warrant], [7, demands], [10, scene10], [11, tells], [14, hangup], [15, lookup], [16, callCourt], [17, report], [18, sceneLine],
];
const CUT_IN = { 6: 'zoom', 10: 'slam' };   // bar 6 dives through the TAP TO VIEW bubble; bar 10 is the logo slam
function sceneAt(t) { let k = 0; for (let i = 0; i < SCENES.length; i++) if (t >= at(SCENES[i][0])) k = i; return k; }
function drawScene(c, t) {
  contentT(c);
  if (t >= at(20)) { resetT(c); sceneSignoff(c, t); return; }   // screen space; no print finish over the official logo
  const k = sceneAt(t), [b0, fn] = SCENES[k], nxt = SCENES[k + 1];
  const tb = at(b0), pb = nxt ? at(nxt[0]) : Infinity;
  if (CUT_IN[b0] === 'zoom' && t < tb + .45) zoomThrough(c, t, tb, tb + .45, [BUBBLE.x, BUBBLE.y, BUBBLE.w, BUBBLE.h], g => textPhone(g, tb - 1e-3), g => warrant(g, t));
  else if (nxt && !CUT_IN[nxt[0]] && t >= pb - PUSH / 2) pushScenes(c, t, pb, fn, nxt[1]);
  else if (!CUT_IN[b0] && k > 0 && t < tb + PUSH / 2) pushScenes(c, t, tb, SCENES[k - 1][1], fn);
  else { fn(c, t); if (b0 === 7 && t >= at(10) - SLAM) logoIn(c, t); contentT(c); captionsTop(c, t); }   // the logo lands over the end of bar 9
  contentT(c);
  printFinish(c);
  if (SHOW_SAFE) safeOverlay(c);
}

// ================= runtime =================
const CV = document.getElementById('c'); CV.width = OUT_W; CV.height = OUT_H; const CTX = CV.getContext('2d');
function frame(i) { const t = Math.min(i / FPS, DUR - 1e-6); FILM_T = t; resetT(CTX); CTX.globalAlpha = 1; drawScene(CTX, t); resetT(CTX); }
window.__NFR = NFR; window.__FPS = FPS; window.__frame = i => { frame(i); return CV.toDataURL('image/png'); };
(async () => {
  await loadPrintKit(); await loadVertKit();
  for (const name of ['officer', 'man']) {
    PUP[name] = await (await fetch(`assets/officer/${name}_parts.json`)).json();
    await Promise.all(Object.keys(PUP[name].parts).map(k => loadImg(name + '_' + k, `assets/officer/${name}_${k}.png`)));
  }
  { const im = IMG.officer_badge, o = document.createElement('canvas'); o.width = im.width; o.height = im.height; const g = o.getContext('2d');   // the badge's back: plain card stock and a strip of tape
    g.drawImage(im, 0, 0); g.globalCompositeOperation = 'source-in'; g.fillStyle = CHIP; g.fillRect(0, 0, o.width, o.height);
    g.globalCompositeOperation = 'source-atop'; g.fillStyle = YEL; g.globalAlpha = .9; g.save(); g.translate(o.width / 2, o.height / 2); g.rotate(-.5); g.fillRect(-o.width, -9, o.width * 2, 18); g.restore();
    IMG.officer_badge_back = o; }
  makeCream();
  frame(+(Q.get('frame') || 0));
  window.__ready = true;
})().catch(e => { console.error(e); window.__error = String(e); });
