'use strict';
/* TRANSITION 1 look test, v2 (the sampler order: finance, then careers). 2 bars, 5.0 s.
   Bar 0, the end of MONEY RULES: PAY YOURSELF FIRST. is up; on beat 4 the rest of the paycheck hops off the spend pile,
   flies at the camera and tumbles, so its plain riso back fills the frame by the downbeat.
   Downbeat: the full-frame paper dissolves from riso grain into warm ink paper, the music turns with it.
   Bar 1, the start of RED FLAG OR GREEN FLAG?: the paper pulls back and lands as Raj's job posting (beat 2); the series
   title card lands (the posting's text follows in the next bar of the full reel). */
const NB = 2, DUR = NB * BAR, NFR = Math.round(DUR * FPS);
const T = { hop: at(0, 2), capOut: [1.72, 1.86], lift: at(0, 4), cover: 2.44, fill: at(1), dz: [2.44, 2.76], land: at(1, 2), title: at(1, 2) + E8, titleOut: [4.72, 4.86] };
const FLUO = [RISO.pink, RISO.teal, RISO.yellow];
const CV = document.getElementById('c'); CV.width = OUT_W; CV.height = OUT_H; const c = CV.getContext('2d');
const INK_BG = layer(), RISO_BG = layer(), PAPER_R = layer(), POST_L = layer();
const MAYA = { x: 140, y: 1130, s: .56 }, RAJ = { x: 160, y: 1130, s: .6 }, CARD_Y = 130, TITLE_Y = 130;
const PRES = 2, FACE = {}; let COPY = null;
// where things sit on screen (px)
const toS = (x, y) => [540 + (x - DCX) * K, SCY_ + (y - DCY) * K];
const PILE = { c: toS(598, 832), s: .88 * K, rot: .16 };          // the paycheck's remains on the spend pile
const POST = { c: toS(604, 690), s: 1.1 * K };                      // the job posting, landed
const FULL_S = 3.1;                                                  // the posting's scale when it fills the frame
const TEAR = (() => { const r = rng(77), pts = []; for (let y = 0; y <= SHEET.ph + .1; y += 14) pts.push([184 + (r() - .5) * 18, y]); return pts; })();
const settle = (t, t0, amp, d = 12, f = 26, stop = .3) => t < t0 ? 0 : t < t0 + stop ? ring(t - t0, amp, d, f) * (1 - seg(t, t0 + stop * .7, t0 + stop)) : 0;

function build() {
  inkPaper(INK_BG); { const g = INK_BG.getContext('2d'); designT(g);
    wash(g, rough(ellPts(500, 660, 440, 520, 0, 90), 26, 3), INK.wash, .34, 4);
    wash(g, rough(ellPts(RAJ.x + 4, RAJ.y + 6, 150, 20, 0, 40), 4, 5), INK.wash, .6, 6); inkHatch(g, ellPts(RAJ.x + 14, RAJ.y + 8, 140, 16, 0, 40), { angle: .15, gap: 5, len: 20, al: .5, seed: 7, cross: true });
    pen(g, smooth([[-60, RAJ.y + 4], [140, RAJ.y + 10], [330, RAJ.y + 6], [420, RAJ.y + 9]], false, 6), 2.6, 8, { taper: [.05, .5] }); }
  risoPaper(RISO_BG); risoPaper(PAPER_R); { const g = RISO_BG.getContext('2d'), P = platesFor(RISO_BG), dT = q => designT(q);
    rfill(P, 'teal', [[-400, 1070], [1400, 1060], [1400, 2200], [-400, 2200]], .24, dT); rfill(P, 'yellow', circPath(690, 600, 250), .85, dT); rfill(P, 'pink', circPath(690, 600, 250), .12, dT);
    for (const [x, y, r0, ink] of [[860, 380, 12, 'pink'], [60, 470, 9, 'teal'], [880, 960, 10, 'pink'], [420, 990, 7, 'teal'], [30, 820, 12, 'yellow'], [520, 350, 8, 'pink']]) rfill(P, ink, circPath(x, y, r0), 1, dT);
    const bag = (x0, cx) => { const p = new Path2D(); p.arc(cx, x0, 30, Math.PI, 0); p.arc(cx, x0, 20, 0, Math.PI, true); p.closePath(); return p; };
    rfill(P, 'pink', roundRectPath(470, 930, 130, 150, 10), 1, dT); rfill(P, 'pink', bag(932, 535), 1, dT);
    rfill(P, 'teal', roundRectPath(590, 960, 120, 125, 10), 1, dT); rfill(P, 'teal', bag(962, 650), 1, dT);
    rfill(P, 'yellow', roundRectPath(560, 1020, 100, 70, 6), 1, dT); rfill(P, 'pink', roundRectPath(560, 1048, 100, 12, 2), .6, dT);
    rfill(P, 'teal', ellPts(MAYA.x + 10, MAYA.y + 6, 150, 18, 0, 40), .5, dT);
    risoPrint(g, P, { grainOff: [11, 23] }); }
  FACE.check = risoFace(SHEET.w, SHEET.ph, 1.6, paycheckRiso, 4);
  FACE.post = (() => { const o = document.createElement('canvas'); o.width = SHEET.w * PRES; o.height = SHEET.h * PRES; const g = o.getContext('2d'); g.scale(PRES, PRES); postingFaceInk(g, 110); return o; })();
  { const g = POST_L.getContext('2d'); resetT(g); g.drawImage(FACE.post, W / 2 - SHEET.w / 2 * FULL_S, H / 2 - SHEET.h / 2 * FULL_S, SHEET.w * FULL_S, SHEET.h * FULL_S); }
  const cc = COPY.careers; FACE.title = (() => { const o = document.createElement('canvas'); o.width = 760 * 1.2; o.height = 250 * 1.2; const g = o.getContext('2d'); g.scale(1.2, 1.2);
    sheetStock(g, 760, 250, 130); penLoop(g, [[6, 6], [380, 5], [754, 6], [755, 125], [754, 244], [380, 245], [6, 244], [5, 125]], 3, 131); pen(g, [[22, 22], [738, 22]], 1.4, 132); pen(g, [[22, 228], [738, 228]], 1.4, 133);
    g.fillStyle = INK.sepia; g.textAlign = 'center'; g.textBaseline = 'middle'; const sz = Math.min(fitFont(g, cc.series[0], 900, 88, 'Playfair', 660), fitFont(g, cc.series[1], 900, 88, 'Playfair', 660)); g.font = `900 ${sz}px Playfair`;
    g.fillText(cc.series[0], 380, 82); g.fillText(cc.series[1], 380, 172); return o; })();
}

// ---- the paycheck: on the pile, then hopping up, flying at the camera and tumbling so its plain back fills the frame
function checkState(t) {
  const [x0, y0] = PILE.c; if (t < T.lift - SLAM) return { cx: x0, cy: y0, s: PILE.s, rot: PILE.rot, a: 0 };
  const hop = t < 2.0 ? -60 * Math.sin(Math.PI * seg(t, T.lift - SLAM, 2.0)) : 0;
  const u = seg(t, 1.95, T.cover), e = easeIn(u), m = easeIO(seg(t, 1.95, 2.3));
  return { cx: lerp(x0, W / 2, m), cy: lerp(y0, H / 2, m) + hop, s: PILE.s * Math.pow(12.5 / PILE.s, e), rot: lerp(PILE.rot, 0, m), a: Math.PI * easeIO(seg(t, 2.06, 2.36)) };
}
function drawCheck(c, st) {
  const { w, ph } = SHEET, k = Math.cos(st.a), s = st.s, kk = Math.max(.02, Math.abs(k));
  const shape = new Path2D(); const P = [...TEAR, [w, ph], [w, 0]].map(([x, y]) => [(x - w / 2) * s, (y - ph / 2) * s * kk * Math.sign(k || 1)]);
  P.forEach((q, i) => i ? shape.lineTo(...q) : shape.moveTo(...q)); shape.closePath();
  c.save(); resetT(c); c.translate(st.cx, st.cy); c.rotate(st.rot);
  const lift = Math.min(1, (s / PILE.s - 1) / 3); if (s < 3) { c.save(); c.translate(8 + 20 * lift, 10 + 26 * lift); c.globalCompositeOperation = 'multiply'; c.fillStyle = alpha(RISO.teal, .38 * (1 - lift * .6)); c.fill(shape); c.restore(); }
  c.save(); c.clip(shape);
  if (k > 0) c.drawImage(FACE.check, -w / 2 * s, -ph / 2 * s * kk, w * s, ph * s * kk);
  else { c.save(); resetT(c); c.drawImage(PAPER_R, 0, 0, W, H); c.restore(); }   // the back: plain riso paper
  const sh = Math.sin(st.a); if (sh > .02) { c.globalCompositeOperation = 'multiply'; c.fillStyle = alpha(RISO.teal, .4 * sh); c.fillRect(-w * s, -ph * s, w * s * 2, ph * s * 2); }
  c.restore(); c.restore();
}
// ---- the job posting: from filling the frame down to its place on Raj's page
function postState(t) { const u = seg(t, T.dz[1], T.land), e = 1 - Math.pow(1 - u, 3), [x1, y1] = POST.c;
  const s = FULL_S * Math.pow(POST.s / FULL_S, e); return { cx: lerp(W / 2, x1, e), cy: lerp(H / 2, y1, e) + settle(t, T.land, 6, 14, 22, .26), s }; }
function drawPost(c, st) { const { w, h } = SHEET; c.save(); resetT(c); c.translate(st.cx, st.cy); c.scale(st.s, st.s);
  const sm = Math.min(1, Math.max(0, (1.6 - st.s) / .6)); if (sm > 0) { c.save(); c.globalAlpha = .17 * sm; c.fillStyle = INK.sepia; c.fillRect(-w / 2 + 8, -h / 2 + 12, w, h); c.restore(); }
  c.drawImage(FACE.post, -w / 2, -h / 2, w, h); c.restore(); }

// ---- the two worlds
function mayaPose(t) { const u = t - T.hop, q = ring(u, .1, 8, 20), air = t > T.hop - .3 && t < T.hop ? Math.sin(Math.PI * seg(t, T.hop - .3, T.hop)) : 0;
  return { sx: 1 + q * .7, sy: 1 - q + .04 * air, bob: 60 * air, head: .04 * Math.sin(t * 3), arm: .1 * Math.sin(Math.PI * seg(t, T.lift - .2, T.lift + .5)) }; }
function financeScene(c, t) { c.save(); resetT(c); c.drawImage(RISO_BG, 0, 0, W, H); designT(c); puppet(c, 'maya', MAYA.x, MAYA.y, MAYA.s, mayaPose(t));
  if (t < T.capOut[1]) { const fc = COPY.finance, k = 1 - easeIn(seg(t, T.capOut[0], T.capOut[1])); designT(c); c.translate(DCX, CARD_Y + 20); c.scale(k, k); c.translate(-DCX, -(CARD_Y + 20));
    const sz = Math.min(fitFont(c, fc.caption[0], 400, 104, 'ArchivoBlack', 800), 104); risoType(c, fc.caption[0], DCX, CARD_Y + 20 - 52, 400, sz, 'ArchivoBlack'); risoType(c, fc.caption[1], DCX, CARD_Y + 20 + 58, 400, sz, 'ArchivoBlack'); }
  c.restore(); }
function rajPose(t) { const u = onTwos(t) - (T.land + .1); return { head: u > 0 && u < .55 ? -.06 * Math.sin(Math.PI * u / .55) : 0 }; }
function careersScene(c, t) { c.save(); resetT(c); c.drawImage(INK_BG, 0, 0, W, H); designT(c); puppet(c, 'raj', RAJ.x, RAJ.y, RAJ.s, rajPose(t)); c.restore(); }
function titleCard(c, t) { if (t < T.title - SLAM || t >= T.titleOut[1]) return; const k = t < T.title ? seg(t, T.title - SLAM, T.title) : 1, a = Math.min(easeOut(k), 1 - seg(t, T.titleOut[0], T.titleOut[1]));
  const dy = (1 - easeOut(k)) * -60 + settle(t, T.title, 5, 12, 22, .26); c.save(); designT(c); c.globalAlpha = a; c.drawImage(FACE.title, DCX - 380, TITLE_Y - 125 + dy, 760, 250); c.restore(); }

function frame(i) {
  const t = i / FPS; resetT(c); c.globalCompositeOperation = 'source-over'; c.globalAlpha = 1;
  if (t < T.cover) { financeScene(c, t); drawCheck(c, checkState(t)); }
  else if (t < T.dz[1]) { c.save(); resetT(c); c.drawImage(PAPER_R, 0, 0, W, H); c.restore(); maskedDraw(c, POST_L, easeIO(seg(t, T.dz[0], T.dz[1])), .09, FLUO); }
  else { careersScene(c, t); drawPost(c, postState(t)); titleCard(c, t); }
  if (SHOW_SAFE) safeOverlay(c);
}
window.__NFR = NFR;
window.__frame = i => { frame(i); return CV.toDataURL('image/png'); };
(async () => {
  try { COPY = await (await fetch('reel.json')).json();
    await Promise.all(['900 60px Playfair', '700 60px Playfair', '400 60px ArchivoBlack'].map(f => document.fonts.load(f))); await Promise.all(['raj', 'maya'].map(loadPuppet));
    build(); window.__TL = { T, fps: FPS, dur: DUR }; frame(0); window.__ready = true;
    if (!Q.has('bare')) { const t0 = performance.now(); const tick = () => { frame(Math.floor((performance.now() - t0) / 1000 * FPS) % NFR); requestAnimationFrame(tick); }; tick(); }
  } catch (e) { window.__error = String(e.stack || e); console.error(e); }
})();
