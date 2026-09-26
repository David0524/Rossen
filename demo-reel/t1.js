'use strict';
/* TRANSITION 1 look test (2 bars, 5.0 s): the last bar of the careers chapter and the first bar of personal finance.
   Your hand catches the offer letter ("YOU GOT THE JOB."), Raj nods. The letter lifts off, flies at the camera and folds
   itself in three (the folds snap shut on the downbeat and the eighth after it); mid-flight its sepia ink and hatching
   dissolve into riso grain and fluorescent ink, the wax seal becoming the paycheck's $ badge, while the whole page
   dissolves from ink to riso on the same downbeat as the music. The paycheck drops into your (now riso) hand, the
   MONEY RULE #1 card lands, Maya bounces in. */
const NB = 2, DUR = NB * BAR, NFR = Math.round(DUR * FPS);
const T_LAND = at(0, 2), T_NOD = at(0, 3), T_FLY = 2.19, T_F1 = at(1, 1), T_F2 = at(1, 1) + E8, T_CATCH = at(1, 2), T_TITLE = at(1, 3), T_MAYA = at(1, 4);
const SC = [2.30, 2.80], OB = [2.45, 2.98];   // the page dissolve (centred on the downbeat) and the prop's own, a little later
const FLUO = [RISO.pink, RISO.teal, RISO.yellow];
const CV = document.getElementById('c'); CV.width = OUT_W; CV.height = OUT_H; const c = CV.getContext('2d');
const INK_BG = layer(), RISO_BG = layer(), RISO_L = layer(), RP = platesFor(RISO_L);
const RES = 1.15, OBJ_F = makeDissolver(260, 340, 5151, [[5, 6, .55], [16, 20, .3]]), OBJ_B = makeDissolver(260, 114, 6161, [[5, 2, .55], [16, 7, .3]]);
const PS = 1.1, G0 = [780, 858];   // the prop's scale; where the hand holds it
const LETTER_AT = [G0[0] - (SHEET.grip[0] - SHEET.w / 2) * PS, G0[1] - (SHEET.grip[1] - SHEET.ph * 1.5) * PS], CHECK_AT = [LETTER_AT[0], LETTER_AT[1] + SHEET.ph * PS];
const RAJ = { x: 160, y: 1130, s: .6 }, MAYA = { x: 140, y: 1130, s: .56 }, CARD_Y = 150;
const FACE = {};

function face(w, h, draw) { const o = document.createElement('canvas'); o.width = Math.round(w * RES); o.height = Math.round(h * RES); const g = o.getContext('2d'); g.scale(RES, RES); draw(g); return o; }
function blankLike(o) { const b = document.createElement('canvas'); b.width = o.width; b.height = o.height; return b; }
function build() {
  inkPaper(INK_BG); { const g = INK_BG.getContext('2d'); designT(g);
    wash(g, rough(ellPts(470, 640, 450, 540, 0, 90), 26, 3), INK.wash, .34, 4);
    wash(g, rough(ellPts(RAJ.x + 4, RAJ.y + 6, 150, 20, 0, 40), 4, 5), INK.wash, .6, 6); inkHatch(g, ellPts(RAJ.x + 14, RAJ.y + 8, 140, 16, 0, 40), { angle: .15, gap: 5, len: 20, al: .5, seed: 7, cross: true });
    pen(g, smooth([[-60, RAJ.y + 4], [140, RAJ.y + 10], [330, RAJ.y + 6], [420, RAJ.y + 9]], false, 6), 2.6, 8, { taper: [.05, .5] }); }
  risoPaper(RISO_BG); { const g = RISO_BG.getContext('2d'), P = platesFor(RISO_BG);
    const band = [[-400, 1070], [1400, 1060], [1400, 2200], [-400, 2200]], dT = q => designT(q);
    rfill(P, 'teal', band, .24, dT); rfill(P, 'yellow', circPath(690, 600, 250), .85, dT); rfill(P, 'pink', circPath(690, 600, 250), .12, dT);
    for (const [x, y, r0, ink] of [[860, 380, 12, 'pink'], [60, 470, 9, 'teal'], [880, 960, 10, 'pink'], [420, 990, 7, 'teal'], [30, 820, 12, 'yellow'], [520, 350, 8, 'pink']]) rfill(P, ink, circPath(x, y, r0), 1, dT);
    risoPrint(g, P, { grainOff: [11, 23] }); }
  FACE.fInk = face(SHEET.w, SHEET.h, letterFrontInk); FACE.btInk = face(SHEET.w, SHEET.ph, letterBackTopInk); FACE.bbInk = face(SHEET.w, SHEET.ph, letterBackBotInk);
  FACE.fRiso = risoFace(SHEET.w, SHEET.h, RES, letterFrontRiso, 3); FACE.btRiso = risoFace(SHEET.w, SHEET.ph, RES, paycheckRiso, 4); FACE.bbRiso = risoFace(SHEET.w, SHEET.ph, RES, checkInsideRiso, 5);
  FACE.f = blankLike(FACE.fInk); FACE.bt = blankLike(FACE.btInk); FACE.bb = blankLike(FACE.bbInk);
}
function mixFace(dst, ink, riso, D, p, after) { const g = dst.getContext('2d'); g.setTransform(1, 0, 0, 1, 0, 0); g.globalCompositeOperation = 'source-over'; g.clearRect(0, 0, dst.width, dst.height);
  g.drawImage(ink, 0, 0); if (p > 0) D.draw(g, riso, p, .12, FLUO, [0, 0, dst.width, dst.height]); if (after) { g.save(); g.scale(RES, RES); after(g); g.restore(); } }

// ---------------- motion ----------------
function objState(t) {   // the prop: anchor = the middle panel's centre (design units), scale, turn, squash, the two folds
  const st = { x: LETTER_AT[0], y: LETTER_AT[1], s: 1, rot: 0, sx: 1, sy: 1, f1: 0, f2: 0 };
  if (t < T_FLY) { const a = seg(t, .06, T_LAND); st.y = lerp(-980, LETTER_AT[1], 1 - (1 - a) * (1 - a)); st.y += dip(t); st.s = PS; return st; }
  if (t < T_CATCH - SLAM) {
    const [x, y, s, rot] = kf(t, [[T_FLY, LETTER_AT[0], LETTER_AT[1], 1, 0], [2.30, LETTER_AT[0] - 4, LETTER_AT[1] - 44, 1.03, -.01], [2.58, 540, 420, 1.3, -.075], [2.78, 530, 450, 1.32, -.04], [T_CATCH - SLAM, CHECK_AT[0] - 6, CHECK_AT[1] - 46, 1.02, .025]]);
    Object.assign(st, { x, y, s, rot });
  } else { const a = seg(t, T_CATCH - SLAM, T_CATCH), e = a * a; Object.assign(st, { x: lerp(CHECK_AT[0] - 6, CHECK_AT[0], e), y: lerp(CHECK_AT[1] - 46, CHECK_AT[1], e), s: lerp(1.02, 1, e), rot: lerp(.025, 0, e) });
    const u = t - T_CATCH, q = ring(u, .075, 9, 26); st.sy = 1 - q; st.sx = 1 + q * .6; st.y += handDy(t) + SHEET.ph / 2 * q * PS; }
  st.s *= PS; st.f1 = Math.PI * easeIn(seg(t, T_F1 - SLAM, T_F1)) ** .7; st.f2 = Math.PI * easeIn(seg(t, T_F2 - SLAM, T_F2)) ** .7;
  return st;
}
const dip = t => t > T_LAND ? 8 * Math.sin(Math.PI * Math.min(1, (t - T_LAND) / .26)) : 0;   // the dry catch: one small give, no bounce
function handDy(t) { let y = dip(t);
  y += 170 * easeIO(seg(t, T_FLY, 2.46)) * (1 - easeOut(seg(t, 2.78, 2.98)));
  if (t > T_CATCH) y += 14 * Math.exp(-(t - T_CATCH) * 8) * Math.sin((t - T_CATCH) * 24);   // the riso catch bounces
  return y; }
function handPose(t) { const grip = t < T_FLY ? easeIO(seg(t, T_LAND - .08, T_LAND)) : t < T_CATCH - .1 ? 1 - easeIO(seg(t, T_FLY, T_FLY + .1)) : easeIO(seg(t, T_CATCH - .06, T_CATCH));
  return { x: G0[0], y: G0[1] + handDy(t), rot: -.1, s: PS, grip }; }
function objBottom(st) { const { ph } = SHEET; const rel = st.f1 < Math.PI / 2 ? ph * .5 + ph * Math.cos(st.f1) : ph * .5; return st.y + rel * st.s * st.sy; }
function thumbFront(t, st, hp) { if (st.s > 1.06 * PS) return false; const tip = HAND.T([HAND.geo(hp.grip).tip], hp)[0]; return objBottom(st) > tip[1] + 2; }
function rajPose(t) { const u = onTwos(t) - (T_NOD - SLAM); return { head: u > 0 && u < .55 ? .075 * Math.sin(Math.PI * Math.min(1, u / .55)) : 0 }; }
function mayaPose(t) { const a0 = T_MAYA - .42; if (t < a0) return null; const a = seg(t, a0, T_MAYA), u = t - T_MAYA;
  const x = lerp(-330, MAYA.x, 1 - (1 - a) ** 2), y = MAYA.y - 20 * 4 * a * (1 - a), air = t < T_MAYA ? Math.sin(Math.PI * a) : 0, q = ring(u, .12, 8, 20);
  return { x, y, sx: (1 - .06 * air) * (1 + q * .7), sy: (1 + .04 * air) * (1 - q), tilt: t < T_MAYA ? .14 * (1 - a) : 0, head: t > T_MAYA ? .05 * Math.sin(u * 9) * Math.exp(-u * 3) : 0 }; }
function cardPop(t) { const a = seg(t, T_TITLE - SLAM, T_TITLE); if (t < T_TITLE - SLAM) return 0; return t < T_TITLE ? lerp(.35, 1.07, easeOut(a)) : t < T_TITLE + .3 ? 1 + ring(t - T_TITLE, .07, 11, 22) * (1 - seg(t, T_TITLE + .2, T_TITLE + .3)) : 1; }   // lands, settles, then exactly still

// ---------------- the prop: three panels, folding ----------------
// A panel flips about its hinge toward the camera: its visible height is |cos f| of the panel, and its free edge
// widens a little as it comes closer. dir -1 draws up from the hinge (the source's bottom row at the hinge), +1 down.
function flip(c, img, sy0, hingeY, dir, f, po = 0) {
  const { w, ph } = SHEET, k = Math.abs(Math.cos(f)), n = 14, grow = .16 * Math.sin(f); if (k < .004) return;
  for (let i = 0; i < n; i++) { const v0 = i / n, v1 = (i + 1) / n, vm = (v0 + v1) / 2, ws = 1 + grow * vm, sy = dir > 0 ? sy0 + v0 * ph : sy0 + ph - v1 * ph;
    const dy = dir > 0 ? hingeY + v0 * ph * k : hingeY - v1 * ph * k; c.drawImage(img, 0, sy * RES, img.width, ph / n * RES, w / 2 - w * ws / 2, dy - .4, w * ws, ph * k / n + .8); }
  const a = Math.sin(f); if (a > .01) { const y0 = dir > 0 ? hingeY : hingeY - ph * k; c.save(); c.globalCompositeOperation = 'multiply';   // the turning panel darkens in its own world's ink
    c.fillStyle = alpha(INK.sepiaMid, .42 * a * (1 - po)); c.fillRect(-w * grow / 2, y0, w * (1 + grow), ph * k); c.fillStyle = alpha(RISO.teal, .45 * a * po); c.fillRect(-w * grow / 2, y0, w * (1 + grow), ph * k); c.restore(); }
}
function drawObject(c, st, ps, po) {
  const { w, ph } = SHEET, h1 = ph, h2 = 2 * ph;
  c.save(); designT(c); c.translate(st.x, st.y); c.rotate(st.rot); c.scale(st.s * st.sx, st.s * st.sy); c.translate(-w / 2, -ph * 1.5);
  const top = st.f2 < Math.PI / 2 ? h1 - ph * Math.abs(Math.cos(st.f2)) : h1, bot = st.f1 < Math.PI / 2 ? h2 + ph * Math.abs(Math.cos(st.f1)) : h2, lift = 1 + (st.s / PS - 1) * 6;
  if (ps < 1) { c.save(); c.globalAlpha = .17 * (1 - ps); c.fillStyle = INK.sepia; c.fillRect(8 * lift, top + 12 * lift, w, bot - top); c.restore(); }
  if (ps > 0) { c.save(); c.globalAlpha = ps; c.globalCompositeOperation = 'multiply'; c.fillStyle = alpha(RISO.teal, .38); c.fillRect(10 * lift, top + 13 * lift, w, bot - top); c.restore(); }
  c.drawImage(FACE.f, 0, h1 * RES, FACE.f.width, ph * RES, 0, h1, w, ph);
  if (st.f2 < Math.PI / 2) flip(c, FACE.f, 0, h1, -1, st.f2, po);
  if (st.f1 < Math.PI / 2) flip(c, FACE.f, h2, h2, +1, st.f1, po); else flip(c, FACE.bb, 0, h2, -1, st.f1, po);
  if (st.f2 >= Math.PI / 2) flip(c, FACE.bt, 0, h1, +1, st.f2, po);
  c.restore();
}

// ---------------- the two worlds ----------------
function inkScene(c, t, hp, thumbIn) { c.save(); resetT(c); c.drawImage(INK_BG, 0, 0, W, H); designT(c);
  puppet(c, 'raj', RAJ.x, RAJ.y, RAJ.s, rajPose(t)); inkHand(c, hp, 'back'); if (thumbIn) inkHand(c, hp, 'thumb'); c.restore(); }
function handSilhouette(hp, thumb) { const G = HAND.geo(hp.grip), T = q => HAND.T(q, hp), p = new Path2D(); for (const q of [G.forearm, G.sleeve, G.back, ...G.fingers, ...(thumb ? [G.thumb] : [])]) p.addPath(polyPath(T(q))); return p; }
function risoScene(t, hp, thumbIn) {
  const g = RISO_L.getContext('2d'); resetT(g); g.globalCompositeOperation = 'source-over'; g.globalAlpha = 1; g.drawImage(RISO_BG, 0, 0, W, H);
  designT(g); g.fillStyle = RISO.paper; g.fill(handSilhouette(hp, thumbIn));
  clearPlates(RP); const dT = q => designT(q);
  risoHand(RP, hp, 'back', dT); if (thumbIn) risoHand(RP, hp, 'thumb', dT);
  const mp = mayaPose(t); if (mp && t > T_MAYA - .06) { const k = t < T_MAYA ? 0 : 1; rfill(RP, 'teal', ellPts(MAYA.x + 10, MAYA.y + 6, 150 * k, 18, 0, 40), .5, dT); }
  const pop = cardPop(t); if (pop > 0) { const cw = 720, ch = 250, cx = DCX, cy = CARD_Y;
    const T2 = q => { designT(q); q.translate(cx, cy); q.scale(pop, pop); q.translate(-cx, -cy); };
    const fr = new Path2D(); fr.rect(cx - cw / 2, cy - ch / 2, cw, ch); fr.rect(cx - cw / 2 + 20, cy - ch / 2 + 20, cw - 40, ch - 40);
    { const q = plateCtx(RP, 'yellow', T2); q.save(); q.fillStyle = RISO.yellow; q.fill(fr, 'evenodd'); q.restore(); }
    const sh = new Path2D(); sh.rect(cx - cw / 2 + 18, cy - ch / 2 + 18, cw, ch); sh.rect(cx - cw / 2, cy - ch / 2, cw, ch);
    { const q = plateCtx(RP, 'pink', T2); q.save(); q.fillStyle = RISO.pink; q.fill(sh, 'evenodd'); q.restore(); } }
  risoPrint(g, RP, { grainOff: [0, 0] });
  if (mp) { designT(g); puppet(g, 'maya', mp.x, mp.y, MAYA.s, mp); }
  if (pop > 0) { designT(g); g.translate(DCX, CARD_Y); g.scale(pop, pop); g.translate(-DCX, -CARD_Y);
    const sz = Math.min(fitFont(g, 'MONEY RULE', 400, 96, 'ArchivoBlack', 620), 96); risoType(g, 'MONEY RULE', DCX, CARD_Y - 44, 400, sz, 'ArchivoBlack'); risoType(g, '#1', DCX, CARD_Y + 50, 400, sz, 'ArchivoBlack'); }
}
function risoThumb(c, hp) { c.save(); designT(c); c.fillStyle = RISO.paper; const G = HAND.geo(hp.grip); c.fill(polyPath(HAND.T(G.thumb, hp))); c.restore();
  clearPlates(RP); risoHand(RP, hp, 'thumb', q => designT(q)); risoPrint(c, RP, { grainOff: [0, 0] }); }

function frame(i) {
  const t = i / FPS, st = objState(t), hp = handPose(t), ps = easeIO(seg(t, SC[0], SC[1])), po = easeIO(seg(t, OB[0], OB[1])), front = thumbFront(t, st, hp);
  mixFace(FACE.f, FACE.fInk, FACE.fRiso, OBJ_F, po, letterInkHeadline);
  mixFace(FACE.bt, FACE.btInk, FACE.btRiso, OBJ_B, po); mixFace(FACE.bb, FACE.bbInk, FACE.bbRiso, OBJ_B, po);
  resetT(c); c.globalCompositeOperation = 'source-over'; c.globalAlpha = 1;
  if (ps < 1) inkScene(c, t, hp, !front);
  if (ps > 0) { risoScene(t, hp, !front); maskedDraw(c, RISO_L, ps, .09, FLUO); }
  drawObject(c, st, ps, po);
  if (front) { if (ps < .5) { c.save(); designT(c); inkHand(c, hp, 'thumb'); c.restore(); } else risoThumb(c, hp); }
  if (SHOW_SAFE) safeOverlay(c);
}

window.__NFR = NFR;
window.__frame = i => { frame(i); return CV.toDataURL('image/png'); };
(async () => {
  try { await Promise.all([document.fonts.load('900 60px Playfair'), document.fonts.load('400 60px ArchivoBlack')]); await Promise.all(['raj', 'maya'].map(loadPuppet));
    build(); frame(0); window.__ready = true;
    if (!Q.has('bare')) { let t0 = performance.now(); const tick = () => { frame(Math.floor((performance.now() - t0) / 1000 * FPS) % NFR); requestAnimationFrame(tick); }; tick(); }
  } catch (e) { window.__error = String(e.stack || e); console.error(e); }
})();
