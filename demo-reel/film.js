'use strict';
/* YOUR FIRST BIG WIN: the demo reel. 16 bars at 96 BPM (40.0 s), 1080 x 1920.
   One story told by four creators' series, each in its own fully committed style, with the hero ("you") shown only
   as a hand and in captions. All on-screen copy is in reel.json.
     bar 0       OPEN          plain paper; YOUR FIRST BIG WIN lands; the page flips up to reveal chapter 1
     bars 1-3    CAREERS       ink on warm paper, Raj: RED FLAG OR GREEN FLAG? / posting A (red flag) / posting B
                               (green flag), your thumb presses APPLY, the posting turns over: YOU GOT THE JOB.
     (T1)                      the letter flies at the camera, folds in three on the downbeat and dissolves ink -> riso
     bars 4-6    FINANCE       risograph, Maya: MONEY RULE #1 / she catches a chunk of your paycheck for her piggy bank,
                               PAY YOURSELF FIRST. / the piggy fills, TRIP FUND
     (T2)                      a hard cut on the downbeat
     bars 7-9    PRODUCTIVITY  graphite, Hana: DAY 1 AT THE NEW JOB. / ONE HABIT / the list draws itself, the two-minute
                               rule, your blue checks / BOOK THE TRIP
     (T3)                      Hana tears the page; it peels away like a sticker backing onto Diego's sticker world
     bars 10-12  TRAVEL        sticker cartoon, Diego: PACK OR PASS? / POWER BANK IN YOUR CHECKED BAG? (uh-oh, PASS,
                               into the carry-on) / SPARE BATTERIES GO IN YOUR CARRY-ON., you zip the bag
     bar 13      LINEUP        the four hosts as four stickers on one page: ONE STORY. FOUR STYLES. YOUR CHARACTER.
     bars 14-15  END CARD      ANIMATED SERIES FOR CREATORS / NEW EPISODES IN A DAY / name / email; the last second still */
const NB = 16, DUR = NB * BAR, NFR = Math.round(DUR * FPS);
const SEC = { open: 0, careers: 1, finance: 4, productivity: 7, travel: 10, lineup: 13, end: 14 };
const A_ = (sec, bar = 1, beat = 1) => at(SEC[sec] + bar - 1, beat);
const FLUO = [RISO.pink, RISO.teal, RISO.yellow];
const T = {
  flip: [1.56, at(0, 4)],
  cTitle: A_('careers'), cTitleOut: [4.0, 4.14], handIn: [3.7, 4.12],
  aDrop: 4.14, aLand: A_('careers', 1, 4), redUp: A_('careers', 2), redStamp: A_('careers', 2, 2), aOut: [6.5, 6.64],
  bLand: A_('careers', 2, 4), green: A_('careers', 3), apply: A_('careers', 3, 2), spin: [8.26, A_('careers', 3, 2) + E8], nod: A_('careers', 3, 3),
  fly: A_('finance') - .31, f1: A_('finance'), f2: A_('finance') + E8, catch_: A_('finance', 1, 2),
  sc: [A_('finance') - .2, A_('finance') + .3], ob: [A_('finance') - .05, A_('finance') + .48],
  fTitle: A_('finance', 1, 3), fTitleOut: [12.34, 12.46], maya: A_('finance', 1, 4), swing: [A_('finance', 2), A_('finance', 2, 2) - .06],
  tear: A_('finance', 2, 2), chunkIn: A_('finance', 2, 2) + E8, fCap: A_('finance', 2, 3), fCapOut: [15.46, 15.6], drop: A_('finance', 2, 4),
  coins: [A_('finance', 3), A_('finance', 3) + E8, A_('finance', 3, 2), A_('finance', 3, 2) + E8], label: A_('finance', 3, 3),
  cut: A_('productivity'), noteOut: [18.84, 18.98], pTitle: A_('productivity', 1, 3) + E8, pTitleOut: [19.72, 19.86], pCap: A_('productivity', 2), pCapOut: [22.22, 22.36],
  listDraw: [A_('productivity', 2), A_('productivity', 2) + .9], checks: [20.9375, 21.25, 21.5625, 21.875, 22.1875], last: A_('productivity', 3), hNod: A_('productivity', 3, 2),
  reach: 24.16, rip: A_('productivity', 3, 4), peel: [24.46, A_('travel')],
  dPop: A_('travel'), vTitle: A_('travel', 1, 2), vTitleOut: [26.9, 27.02], handIn2: [26.95, 27.36], q: A_('travel', 2), uhoh: A_('travel', 2, 2), pass: A_('travel', 2, 3),
  move: A_('travel', 2, 4), qOut: [29.72, 29.86], vCap: A_('travel', 3), zip: A_('travel', 3, 3), hop: A_('travel', 3, 4), vCapOut: [32.34, 32.46],
  slaps: [0, 1, 2, 3].map(k => A_('lineup') + k * S16), lCap: A_('lineup', 1, 2),
  e1: A_('end'), e2: A_('end', 1, 3), e3: A_('end', 2), e4: A_('end', 2, 2),
};
let COPY = null;
const CV = document.getElementById('c'); CV.width = OUT_W; CV.height = OUT_H; const c = CV.getContext('2d');
const INK_BG = layer(), RISO_BG = layer(), GRAPH_BG = layer(), STK_BG = layer(), PLAIN_BG = layer();
const RISO_L = layer(), PAGE_L = layer(), PEN_L = layer(), OPEN_L = layer(), RP = platesFor(RISO_L);
const RES = 1.15, OBJ_F = makeDissolver(260, 340, 5151, [[5, 6, .55], [16, 20, .3]]), OBJ_B = makeDissolver(260, 114, 6161, [[5, 2, .55], [16, 7, .3]]);
const PS = 1.1, G0 = [780, 858], REL = [(SHEET.grip[0] - SHEET.w / 2) * PS, (SHEET.grip[1] - SHEET.ph * 1.5) * PS];
const LETTER_AT = [G0[0] - REL[0], G0[1] - REL[1]], CHECK_REL = [REL[0], REL[1] - SHEET.ph * PS], CHECK_AT = [G0[0] - CHECK_REL[0], G0[1] - CHECK_REL[1]];
const RAJ = { x: 160, y: 1130, s: .6 }, MAYA = { x: 140, y: 1130, s: .56 }, HANA = { x: 150, y: 1130, s: .5 }, DIEGO = { x: 150, y: 1130, s: .5 }, CARD_Y = 150;
const FACE = {}, STKS = {}, SWING = [800, 985];
const settle = (t, t0, amp = .06, d = 12, f = 26, stop = .3) => t < t0 ? 0 : t < t0 + stop ? ring(t - t0, amp, d, f) * (1 - seg(t, t0 + stop * .7, t0 + stop)) : 0;   // lands, rings, then exactly still
const pop = (t, t0, from = .35, over = 1.08) => t < t0 - SLAM ? 0 : t < t0 ? lerp(from, over, easeOut(seg(t, t0 - SLAM, t0))) : 1 + (over - 1) * settle(t, t0, 1, 11, 22, .3) / 1;

// ================= building (once) =================
function face(w, h, draw) { const o = document.createElement('canvas'); o.width = Math.round(w * RES); o.height = Math.round(h * RES); const g = o.getContext('2d'); g.scale(RES, RES); draw(g); return o; }
function blankLike(o) { const b = document.createElement('canvas'); b.width = o.width; b.height = o.height; return b; }
function stickerFromImage(im, k) { const w = im.width * k, h = im.height * k; return makeSticker(w, h, g => g.drawImage(im, 0, 0, w, h), { border: 0, res: 1 }); }
function build() {
  // ---- ink
  inkPaper(INK_BG); { const g = INK_BG.getContext('2d'); designT(g);
    wash(g, rough(ellPts(470, 640, 450, 540, 0, 90), 26, 3), INK.wash, .34, 4);
    wash(g, rough(ellPts(RAJ.x + 4, RAJ.y + 6, 150, 20, 0, 40), 4, 5), INK.wash, .6, 6); inkHatch(g, ellPts(RAJ.x + 14, RAJ.y + 8, 140, 16, 0, 40), { angle: .15, gap: 5, len: 20, al: .5, seed: 7, cross: true });
    pen(g, smooth([[-60, RAJ.y + 4], [140, RAJ.y + 10], [330, RAJ.y + 6], [420, RAJ.y + 9]], false, 6), 2.6, 8, { taper: [.05, .5] }); }
  const cc = COPY.careers;
  FACE.A = face(SHEET.w, SHEET.h, g => { postingFaceInk(g, 110); postingText(g, cc.postingA, 214); });
  FACE.B = face(SHEET.w, SHEET.h, g => { postingFaceInk(g, 120); postingText(g, cc.postingB, 214); });
  FACE.title = face(760, 250, g => { sheetStock(g, 760, 250, 130); penLoop(g, [[6, 6], [380, 5], [754, 6], [755, 125], [754, 244], [380, 245], [6, 244], [5, 125]], 3, 131); pen(g, [[22, 22], [738, 22]], 1.4, 132); pen(g, [[22, 228], [738, 228]], 1.4, 133);
    g.fillStyle = INK.sepia; g.textAlign = 'center'; g.textBaseline = 'middle'; const sz = Math.min(fitFont(g, cc.series[0], 900, 88, 'Playfair', 660), fitFont(g, cc.series[1], 900, 88, 'Playfair', 660)); g.font = `900 ${sz}px Playfair`;
    g.fillText(cc.series[0], 380, 82); g.fillText(cc.series[1], 380, 172); });
  FACE.fInk = face(SHEET.w, SHEET.h, letterFrontInk); FACE.btInk = face(SHEET.w, SHEET.ph, letterBackTopInk); FACE.bbInk = face(SHEET.w, SHEET.ph, letterBackBotInk);
  FACE.letter = face(SHEET.w, SHEET.h, g => { letterFrontInk(g); letterInkHeadline(g); });
  // ---- riso
  risoPaper(RISO_BG); { const g = RISO_BG.getContext('2d'), P = platesFor(RISO_BG), dT = q => designT(q);
    rfill(P, 'teal', [[-400, 1070], [1400, 1060], [1400, 2200], [-400, 2200]], .24, dT); rfill(P, 'yellow', circPath(690, 600, 250), .85, dT); rfill(P, 'pink', circPath(690, 600, 250), .12, dT);
    for (const [x, y, r0, ink] of [[860, 380, 12, 'pink'], [60, 470, 9, 'teal'], [880, 960, 10, 'pink'], [420, 990, 7, 'teal'], [30, 820, 12, 'yellow'], [520, 350, 8, 'pink']]) rfill(P, ink, circPath(x, y, r0), 1, dT);
    // the spend pile: two shopping bags and a box
    rfill(P, 'pink', roundRectPath(470, 930, 130, 150, 10), 1, dT); rknock(P, RISO_INKS, roundRectPath(500, 900, 70, 50, 26), 0, dT); rfill(P, 'pink', (() => { const p = new Path2D(); p.arc(535, 932, 30, Math.PI, 0); p.arc(535, 932, 20, 0, Math.PI, true); p.closePath(); return p; })(), 1, dT);
    rfill(P, 'teal', roundRectPath(590, 960, 120, 125, 10), 1, dT); rfill(P, 'teal', (() => { const p = new Path2D(); p.arc(650, 962, 28, Math.PI, 0); p.arc(650, 962, 19, 0, Math.PI, true); p.closePath(); return p; })(), 1, dT);
    rfill(P, 'yellow', roundRectPath(560, 1020, 100, 70, 6), 1, dT); rfill(P, 'pink', roundRectPath(560, 1048, 100, 12, 2), .6, dT);
    risoPrint(g, P, { grainOff: [11, 23] }); }
  FACE.fRiso = risoFace(SHEET.w, SHEET.h, RES, letterFrontRiso, 3); FACE.btRiso = risoFace(SHEET.w, SHEET.ph, RES, paycheckRiso, 4); FACE.bbRiso = risoFace(SHEET.w, SHEET.ph, RES, checkInsideRiso, 5);
  FACE.f = blankLike(FACE.fInk); FACE.bt = blankLike(FACE.btInk); FACE.bb = blankLike(FACE.bbInk);
  // ---- graphite: the page, and the torn-out to-do sheet on it
  graphPaper(GRAPH_BG); { const g = GRAPH_BG.getContext('2d'); designT(g); const top = tornLine(300, 880, 360, 41, 6);
    const sheet = [...top, [880, 1100], [300, 1100]]; g.save(); g.fillStyle = 'rgba(60,60,60,.06)'; g.translate(7, 9); g.fill(polyPath(sheet)); g.restore(); g.fillStyle = '#FFFFFF'; g.fill(polyPath(sheet));
    g.save(); g.clip(polyPath(sheet)); for (let k = 0; k < 7; k++) { g.fillStyle = alpha(GRAPH.sky, .38); g.fillRect(300, 478 + k * 95, 580, 2); } g.fillStyle = alpha(GRAPH.sky, .3); g.fillRect(338, 360, 2, 740); g.restore();
    const L = PEN_L, pg = clearLayer(L); designT(pg); pencil(pg, top, 1.6, 42, { al: .5 }); fibres(pg, top, 43); pencil(pg, [[880, 360], [880, 1100], [300, 1100], [300, 360]], 1.4, 44, { al: .4, passes: 2 }); graphLay(g, L); clearLayer(L); }
  // ---- sticker world
  stkPaper(STK_BG); stkHandInit(); buildStickers();
  // ---- plain
  plainPaper(PLAIN_BG);
  for (const n of ['raj', 'maya', 'hana', 'diego']) STKS['line_' + n] = stickerFromImage(IMG[n + '_sticker'], 660 / IMG[n + '_sticker'].height);
  STKS.diegoShadow = stickerFromImage(IMG.diego_sticker, 1);
}
function buildStickers() { const tv = COPY.travel;
  const card = (w, h, fill, lines, size, col) => makeSticker(w, h, g => { stkShape(g, roundRectPath(0, 0, w, h, 34), fill); const lh = size * 1.12, y0 = h / 2 - (lines.length - 1) * lh / 2;
    const sz = Math.min(...lines.map(l => fitFont(g, l, 700, size, 'Fredoka', w - 70))); lines.forEach((l, i) => stkType(g, l, w / 2, y0 + i * lh + 4, sz, col)); }, { border: 14 });
  STKS.title = card(700, 190, STK.orange, [tv.series], 96, STK.ink);
  STKS.q = card(800, 250, STK.white, tv.question, 76, STK.ink);
  STKS.cap = card(820, 250, STK.white, tv.caption, 76, STK.ink);
  STKS.pass = makeSticker(270, 124, g => { stkShape(g, roundRectPath(0, 0, 270, 124, 26), STK.blue, STK.blueSh, rectPath(0, 90, 270, 40)); stkType(g, tv.verdict, 135, 64, fitFont(g, tv.verdict, 700, 92, 'Fredoka', 220), STK.white); }, { border: 12 });
  STKS.suitLid = makeSticker(360, 270, g => { stkShape(g, roundRectPath(0, 20, 360, 250, 34), STK.orange, STK.orangeSh, rectPath(300, 20, 70, 260));
    stkShape(g, roundRectPath(24, 44, 312, 202, 20), STK.blue, STK.blueSh, rectPath(24, 44, 312, 34)); stkShape(g, roundRectPath(52, 130, 256, 94, 12), STK.lime, STK.limeSh, rectPath(52, 200, 256, 30));
    g.strokeStyle = STK.ink; g.lineWidth = 3; for (let x = 70; x < 300; x += 22) { g.beginPath(); g.moveTo(x, 136); g.lineTo(x, 218); g.stroke(); }
    const hd = new Path2D(); hd.moveTo(140, 22); hd.bezierCurveTo(140, -14, 220, -14, 220, 22); g.lineWidth = 14; g.strokeStyle = STK.ink; g.stroke(hd); g.lineWidth = 7; g.strokeStyle = STK.orange; g.stroke(hd); }, { border: 12 });
  STKS.suitBase = makeSticker(390, 170, g => { const tray = new Path2D(); tray.moveTo(18, 30); tray.lineTo(372, 30); tray.lineTo(390, 150); tray.lineTo(0, 150); tray.closePath();
    stkShape(g, roundRectPath(30, -34, 150, 70, 26), STK.lime, STK.limeSh, rectPath(30, 14, 150, 30)); stkShape(g, roundRectPath(170, -22, 190, 58, 14), STK.white, STK.bgSh, rectPath(170, 18, 190, 20));
    stkShape(g, tray, STK.orange, STK.orangeSh, rectPath(0, 112, 400, 40)); stkShape(g, roundRectPath(150, 60, 90, 22, 8), STK.orangeSh);
    for (const x of [44, 346]) stkShape(g, circPath(x, 160, 15), STK.ink); }, { border: 12 });
  const pack = open => g => { stkShape(g, roundRectPath(0, 20, 220, 260, 60), STK.blue, STK.blueSh, rectPath(160, 20, 70, 270)); stkShape(g, roundRectPath(34, 150, 152, 104, 24), STK.blueSh);
    g.strokeStyle = STK.ink; g.lineWidth = 4; g.beginPath(); g.moveTo(50, 184); g.lineTo(170, 184); g.stroke();
    g.lineWidth = 6; g.beginPath(); g.moveTo(80, 26); g.bezierCurveTo(80, -14, 140, -14, 140, 26); g.stroke();
    if (open) { const m = new Path2D(); m.moveTo(24, 66); m.quadraticCurveTo(110, 36, 196, 66); m.quadraticCurveTo(110, 100, 24, 66); stkShape(g, m, STK.ink); }
    else { g.lineWidth = 4; g.beginPath(); g.moveTo(24, 66); g.quadraticCurveTo(110, 52, 196, 66); g.stroke(); } };
  STKS.packOpen = makeSticker(220, 280, pack(true), { border: 12 }); STKS.packShut = makeSticker(220, 280, pack(false), { border: 12 });
  STKS.bank = makeSticker(96, 156, g => { stkShape(g, roundRectPath(0, 0, 96, 156, 18), STK.lime, STK.limeSh, rectPath(64, 0, 40, 160)); const b = [[56, 28], [26, 84], [48, 84], [38, 128], [72, 66], [50, 66], [60, 28]];
    g.fillStyle = STK.white; g.fill(polyPath(b)); g.strokeStyle = STK.ink; g.lineWidth = 3.5; g.stroke(polyPath(b)); stkShape(g, roundRectPath(34, -6, 28, 10, 3), STK.ink); }, { border: 10 });
  STKS.pull = makeSticker(26, 40, g => stkShape(g, roundRectPath(0, 0, 26, 40, 8), STK.lime, STK.limeSh, rectPath(16, 0, 12, 40), 4), { border: 6 });
  STKS.drop = makeSticker(46, 66, g => { const d = new Path2D(); d.moveTo(23, 0); d.bezierCurveTo(30, 18, 46, 32, 46, 44); d.arc(23, 44, 23, 0, Math.PI); d.bezierCurveTo(0, 32, 16, 18, 23, 0); stkShape(g, d, STK.blue, STK.blueSh, circPath(34, 50, 16), 4);
    g.fillStyle = STK.white; g.beginPath(); g.ellipse(15, 40, 5, 9, -.4, 0, TAU); g.fill(); }, { border: 8 });
}
function mixFace(dst, ink, riso, D, p, after) { const g = dst.getContext('2d'); g.setTransform(1, 0, 0, 1, 0, 0); g.globalCompositeOperation = 'source-over'; g.clearRect(0, 0, dst.width, dst.height);
  g.drawImage(ink, 0, 0); if (p > 0) D.draw(g, riso, p, .12, FLUO, [0, 0, dst.width, dst.height]); if (after) { g.save(); g.scale(RES, RES); after(g); g.restore(); } }

// ================= careers + finance: the prop in your hand =================
const dipAt = (t, t0, a = 8) => t > t0 && t < t0 + .26 ? a * Math.sin(Math.PI * (t - t0) / .26) : 0;
function handPoseCF(t) {   // your hand in careers and finance: where it is, how closed
  let x = G0[0], y = G0[1], grip = 0;
  y += 1350 * (1 - easeOut(seg(t, T.handIn[0], T.handIn[1])));
  if (t >= T.aLand - .08 && t < T.aOut[0]) grip = easeIO(seg(t, T.aLand - .08, T.aLand)); else if (t >= T.aOut[0] && t < T.bLand - .08) grip = 1 - easeIO(seg(t, T.aOut[0], T.aOut[0] + .06));
  else if (t >= T.bLand - .08 && t < T.fly) grip = easeIO(seg(t, T.bLand - .08, T.bLand)); else if (t >= T.fly && t < T.catch_ - .1) grip = 1 - easeIO(seg(t, T.fly, T.fly + .1));
  else if (t >= T.catch_ - .1 && t < T.drop - .15) grip = easeIO(seg(t, T.catch_ - .06, T.catch_)); else if (t >= T.drop - .15) grip = 1 - easeIO(seg(t, T.drop - .15, T.drop - .05));
  y += dipAt(t, T.aLand) + dipAt(t, T.bLand);
  y += 170 * easeIO(seg(t, T.fly, T.fly + .27)) * (1 - easeOut(seg(t, T.f1 + .28, T.f1 + .48)));
  if (t > T.catch_) y += 14 * Math.exp(-(t - T.catch_) * 8) * Math.sin((t - T.catch_) * 24);
  const mv = easeIO(seg(t, T.swing[0], T.swing[1])); x += (SWING[0] - G0[0]) * mv; y += (SWING[1] - G0[1]) * mv;   // toward the spend pile
  const out = easeIn(seg(t, T.drop + .05, T.drop + .55)); x += 320 * out; y += 1150 * out;
  return { x, y, rot: -.1, s: PS, grip };
}
function propCF(t, hp) {   // the prop: which card, where (anchor = the sheet's middle-panel centre), its folds and spin
  const st = { kind: null, x: LETTER_AT[0], y: LETTER_AT[1], s: PS, rot: 0, sx: 1, sy: 1, f1: 0, f2: 0 };
  const held = (rel = REL) => { st.x = hp.x - rel[0]; st.y = hp.y - rel[1]; };
  if (t < T.aDrop) return st;
  if (t < T.aOut[1]) { st.kind = 'A'; if (t < T.aLand) { const a = seg(t, T.aDrop, T.aLand); st.y = lerp(-1150, LETTER_AT[1], 1 - (1 - a) * (1 - a)); } else held();
    if (t > T.aOut[0]) { const a = easeIn(seg(t, T.aOut[0], T.aOut[1])); st.x = LETTER_AT[0] - 1250 * a; st.y = LETTER_AT[1] - 380 * a; st.rot = -.7 * a; } return st; }
  if (t < T.bLand - .235) return st;
  if (t < T.spin[0]) { st.kind = 'B'; if (t < T.bLand) { const a = seg(t, T.bLand - .235, T.bLand); st.y = lerp(-1150, LETTER_AT[1], 1 - (1 - a) * (1 - a)); } else held(); return st; }
  if (t < T.fly) { held(); if (t < T.spin[1]) { const e = easeIO(seg(t, T.spin[0], T.spin[1])); st.kind = e < .5 ? 'B' : 'letter'; st.spinK = Math.max(.02, Math.abs(Math.cos(Math.PI * e))); } else st.kind = 'letter'; return st; }
  // T1: the flight (as approved in the look test)
  st.kind = 'letter';
  if (t < T.catch_ - SLAM) { const [x, y, s, rot] = kf(t, [[T.fly, LETTER_AT[0], LETTER_AT[1], 1, 0], [T.f1 - .2, LETTER_AT[0] - 4, LETTER_AT[1] - 44, 1.03, -.01], [T.f1 + .08, 540, 420, 1.3, -.075], [T.f1 + .28, 530, 450, 1.32, -.04], [T.catch_ - SLAM, CHECK_AT[0] - 6, CHECK_AT[1] - 46, 1.02, .025]]);
    Object.assign(st, { x, y, s: s * PS, rot }); }
  else if (t < T.catch_) { const a = seg(t, T.catch_ - SLAM, T.catch_), e = a * a; Object.assign(st, { x: lerp(CHECK_AT[0] - 6, CHECK_AT[0], e), y: lerp(CHECK_AT[1] - 46, CHECK_AT[1], e), s: lerp(1.02, 1, e) * PS, rot: lerp(.025, 0, e) }); }
  else { held(CHECK_REL); const q = ring(t - T.catch_, .075, 9, 26); st.sy = 1 - q; st.sx = 1 + q * .6; st.y += SHEET.ph / 2 * q * PS; st.kind = 'check'; }
  st.f1 = Math.PI * easeIn(seg(t, T.f1 - SLAM, T.f1)) ** .7; st.f2 = Math.PI * easeIn(seg(t, T.f2 - SLAM, T.f2)) ** .7;
  if (t >= T.drop - .1) { const a = easeIn(seg(t, T.drop - .1, T.drop)); st.x = SWING[0] - CHECK_REL[0] - 26 * a; st.y = SWING[1] - CHECK_REL[1] - 28 * a; st.s = PS * (1 - .2 * a); st.rot = .16 * a; st.kind = 'check'; st.sx = st.sy = 1; st.onPile = true; }
  return st;
}
function objBottom(st) { const { ph } = SHEET; const rel = st.kind === 'check' ? ph * .5 : st.f1 < Math.PI / 2 ? ph * .5 + ph * Math.cos(st.f1) : ph * .5; return st.y + rel * st.s * st.sy; }
function thumbFront(st, hp) { if (!st.kind || st.s > 1.06 * PS || st.onPile) return false; const tip = HAND.T([HAND.geo(hp.grip).tip], hp)[0]; return objBottom(st) > tip[1] + 2; }
// a panel flipping about its hinge toward the camera (dir -1 draws up from the hinge, +1 down); shading in its own ink
function flip(c, img, sy0, hingeY, dir, f, po = 0) {
  const { w, ph } = SHEET, k = Math.abs(Math.cos(f)), n = 14, grow = .16 * Math.sin(f); if (k < .004) return;
  for (let i = 0; i < n; i++) { const v0 = i / n, v1 = (i + 1) / n, vm = (v0 + v1) / 2, ws = 1 + grow * vm, sy = dir > 0 ? sy0 + v0 * ph : sy0 + ph - v1 * ph;
    const dy = dir > 0 ? hingeY + v0 * ph * k : hingeY - v1 * ph * k; c.drawImage(img, 0, sy * RES, img.width, ph / n * RES, w / 2 - w * ws / 2, dy - .4, w * ws, ph * k / n + .8); }
  const a = Math.sin(f); if (a > .01) { const y0 = dir > 0 ? hingeY : hingeY - ph * k; c.save(); c.globalCompositeOperation = 'multiply';
    c.fillStyle = alpha(INK.sepiaMid, .42 * a * (1 - po)); c.fillRect(-w * grow / 2, y0, w * (1 + grow), ph * k); c.fillStyle = alpha(RISO.teal, .45 * a * po); c.fillRect(-w * grow / 2, y0, w * (1 + grow), ph * k); c.restore(); }
}
function stampK(t, t0) { return t < t0 - SLAM ? 0 : t < t0 ? lerp(1.12, 1, easeIn(seg(t, t0 - SLAM, t0))) : 1 + settle(t, t0, -.03, 16, 30, .22); }   // it thumps down from just above; even at its biggest it stays clear of the text
function propFrame(c, st) { c.translate(st.x, st.y); c.rotate(st.rot); c.scale(st.s * st.sx, st.s * st.sy); c.translate(-SHEET.w / 2, -SHEET.ph * 1.5); }
function drawCard(c, st, t) {   // posting A, posting B, the letter (unfolded), in ink
  const { w, h } = SHEET, cc = COPY.careers; c.save(); designT(c); propFrame(c, st);
  if (st.spinK !== undefined) { c.translate(SHEET.grip[0], 0); c.scale(st.spinK, 1); c.translate(-SHEET.grip[0], 0); }
  c.save(); c.globalAlpha = .17; c.fillStyle = INK.sepia; c.fillRect(8, 12, w, h); c.restore();
  c.drawImage(st.kind === 'A' ? FACE.A : st.kind === 'B' ? FACE.B : FACE.letter, 0, 0, w, h);
  if (st.kind === 'A') { const k = stampK(t, T.redStamp); if (k) stampInk(c, cc.red, 262, 600, INK.red, -.08, k * 1.45); }
  if (st.kind === 'B') { const k = stampK(t, T.green); if (k) stampInk(c, cc.green, 250, 514, INK.green, -.05, k * 1.15); applyButton(c, cc.apply, t >= T.apply - .02, 140); }
  c.restore();
}
function drawObject(c, st, ps, po) {   // the letter folding into the paycheck (T1), then the paycheck, then its torn pieces
  const { w, ph } = SHEET, h1 = ph, h2 = 2 * ph;
  c.save(); designT(c); propFrame(c, st);
  const top = st.f2 < Math.PI / 2 ? h1 - ph * Math.abs(Math.cos(st.f2)) : h1, bot = st.f1 < Math.PI / 2 ? h2 + ph * Math.abs(Math.cos(st.f1)) : h2, lift = 1 + (st.s / PS - 1) * 6;
  if (st.kind === 'check' && st.torn) { c.restore(); return; }
  if (ps < 1) { c.save(); c.globalAlpha = .17 * (1 - ps); c.fillStyle = INK.sepia; c.fillRect(8 * lift, top + 12 * lift, w, bot - top); c.restore(); }
  if (ps > 0) { c.save(); c.globalAlpha = ps; c.globalCompositeOperation = 'multiply'; c.fillStyle = alpha(RISO.teal, .38); c.fillRect(10 * lift, top + 13 * lift, w, bot - top); c.restore(); }
  if (st.kind === 'check' && st.f2 >= Math.PI) { c.drawImage(FACE.btRiso, 0, h1, w, ph); c.restore(); return; }
  c.drawImage(FACE.f, 0, h1 * RES, FACE.f.width, ph * RES, 0, h1, w, ph);
  if (st.f2 < Math.PI / 2) flip(c, FACE.f, 0, h1, -1, st.f2, po);
  if (st.f1 < Math.PI / 2) flip(c, FACE.f, h2, h2, +1, st.f1, po); else flip(c, FACE.bb, 0, h2, -1, st.f1, po);
  if (st.f2 >= Math.PI / 2) flip(c, FACE.bt, 0, h1, +1, st.f2, po);
  c.restore();
}
// the paycheck torn in two: Maya's chunk (the $ end) and the rest
const TEAR = (() => { const r = rng(77), pts = []; for (let y = 0; y <= SHEET.ph + .1; y += 14) pts.push([184 + (r() - .5) * 18, y]); return pts; })();
function checkPiece(c, which, x, y, s, rot, shadow = true) { const { w, ph } = SHEET; c.save(); designT(c); c.translate(x, y); c.rotate(rot); c.scale(s, s);
  const clip = which === 'chunk' ? [[0, 0], ...TEAR, [0, ph]] : [...TEAR, [w, ph], [w, 0]];
  if (shadow) { c.save(); c.translate(10, 12); c.globalCompositeOperation = 'multiply'; c.fillStyle = alpha(RISO.teal, .38); c.fill(polyPath(clip)); c.restore(); }
  c.save(); c.clip(polyPath(clip)); c.drawImage(FACE.btRiso, 0, 0, w, ph); c.restore(); c.restore(); }
function chunkState(t) { if (t < T.tear || t >= T.chunkIn) return null; const a = seg(t, T.tear, T.chunkIn), [sx, sy] = mayaSlot(t);
  const x0 = SWING[0] - CHECK_REL[0] - SHEET.w / 2 * PS, y0 = SWING[1] - CHECK_REL[1] - SHEET.ph / 2 * PS;   // the check's top-left when it tears, in design units
  return { x: lerp(x0, sx - 60, a), y: lerp(y0, sy - 60, a) - 160 * 4 * a * (1 - a), s: PS * lerp(1, .42, a), rot: lerp(0, -1.1, a) }; }

// ================= the scenes =================
function rajPose(t) { const u = onTwos(t) - (T.nod - SLAM), up = onTwos(t);
  const red = easeOut(seg(up, T.redUp - SLAM, T.redUp)) * (1 - easeIn(seg(up, T.aOut[0], T.aOut[1]))), green = easeOut(seg(up, T.green - SLAM, T.green)) * (1 - easeIn(seg(up, T.fly, T.fly + .15)));
  const flagUp = Math.max(red, green), col = green > 0 ? INK.green : INK.red;
  return { head: u > 0 && u < .55 ? .075 * Math.sin(Math.PI * Math.min(1, u / .55)) : 0, arm: -.12 * flagUp,
    armBehind: flagUp > .01 ? g => { g.save(); g.translate(352, 640 - 300 * flagUp); g.scale(1.6, 1.6); inkFlag(g, 0, 0, 230, col, up, 150); g.restore(); } : null }; }
function careersScene(c, t, hp, thumbIn) { c.save(); resetT(c); c.drawImage(INK_BG, 0, 0, W, H); designT(c);
  puppet(c, 'raj', RAJ.x, RAJ.y, RAJ.s, rajPose(t));
  const ta = t < T.cTitle - SLAM ? 0 : 1 - seg(t, T.cTitleOut[0], T.cTitleOut[1]);
  if (ta > 0 && t < T.cTitleOut[1]) { const k = t < T.cTitle ? seg(t, T.cTitle - SLAM, T.cTitle) : 1, dy = (1 - easeOut(k)) * -60 + (t >= T.cTitle ? dipAt(t, T.cTitle, 5) : 0);
    c.save(); c.globalAlpha = Math.min(ta, easeOut(k)); c.drawImage(FACE.title, DCX - 380, CARD_Y - 125 + dy, 760, 250); c.restore(); }
  inkHand(c, hp, 'back'); if (thumbIn) inkHand(c, hp, 'thumb'); c.restore(); }
function handSilhouette(hp, thumb) { const G = HAND.geo(hp.grip), Tq = q => HAND.T(q, hp), p = new Path2D(); for (const q of [G.forearm, G.sleeve, G.back, ...G.fingers, ...(thumb ? [G.thumb] : [])]) p.addPath(polyPath(Tq(q))); return p; }
function mayaPose(t) { const a0 = T.maya - .42; if (t < a0) return null; const a = seg(t, a0, T.maya), u = t - T.maya;
  const x = lerp(-330, MAYA.x, 1 - (1 - a) ** 2), y = MAYA.y - 20 * 4 * a * (1 - a), air = t < T.maya ? Math.sin(Math.PI * a) : 0, q = ring(u, .12, 8, 20);
  let arm = .3 * easeOutBack(seg(t, T.tear - .18, T.tear)) * (1 - easeIO(seg(t, T.chunkIn + .15, T.chunkIn + .45))), armScale = 1;
  T.coins.forEach((tc, i) => { arm += settle(t, tc, .09, 9, 24, .3); armScale += .03 * easeOut(seg(t, tc, tc + .1)); });
  arm += .18 * easeOutBack(seg(t, T.label - .2, T.label));
  return { x, y, sx: (1 - .06 * air) * (1 + q * .7), sy: (1 + .04 * air) * (1 - q), tilt: t < T.maya ? .14 * (1 - a) : 0, head: t > T.maya ? .05 * Math.sin(u * 9) * Math.exp(-u * 3) : 0, arm, armScale }; }
function mayaSlot(t) { const mp = mayaPose(t) || { x: MAYA.x, y: MAYA.y }; return toDesignSlot(mp); }
function toDesignSlot(mp) { return armPoint('maya', [720, 592], mp.x, mp.y, MAYA.s, mp); }
function coinState(t, tc) { if (t < tc - .3 || t >= tc) return null; const a = seg(t, tc - .3, tc), [sx, sy] = mayaSlot(t); return { x: lerp(-120, sx, a), y: lerp(430, sy, a) - 120 * 4 * a * (1 - a) }; }
function financeScene(t, hp, thumbIn) {
  const g = RISO_L.getContext('2d'), fc = COPY.finance; resetT(g); g.globalCompositeOperation = 'source-over'; g.globalAlpha = 1; g.drawImage(RISO_BG, 0, 0, W, H);
  designT(g); g.fillStyle = RISO.paper; g.fill(handSilhouette(hp, thumbIn));
  clearPlates(RP); const dT = q => designT(q);
  risoHand(RP, hp, 'back', dT); if (thumbIn) risoHand(RP, hp, 'thumb', dT);
  const mp = mayaPose(t); if (mp && t > T.maya - .06) { const k = t < T.maya ? 0 : 1; rfill(RP, 'teal', ellPts(MAYA.x + 10, MAYA.y + 6, 150 * k, 18, 0, 40), .5, dT); }
  for (const tc of T.coins) { const cs = coinState(t, tc); if (cs) { rfill(RP, 'yellow', circPath(cs.x, cs.y, 20), 1, dT); rfill(RP, 'pink', circPath(cs.x, cs.y, 20), .35, dT); rknock(P2(RP), ['yellow', 'pink'], circPath(cs.x, cs.y, 8), 0, dT); } }
  const cardK = t < T.fTitleOut[0] ? pop(t, T.fTitle) : 1 - easeIn(seg(t, T.fTitleOut[0], T.fTitleOut[1]));
  const cardT = q => { designT(q); q.translate(DCX, CARD_Y); q.scale(cardK, cardK); q.translate(-DCX, -CARD_Y); };
  if (cardK > 0 && t < T.fTitleOut[1]) { const cw = 720, ch = 250, cx = DCX, cy = CARD_Y; g.save(); cardT(g); g.fillStyle = RISO.paper; g.fillRect(cx - cw / 2, cy - ch / 2, cw, ch); g.restore(); designT(g);
    const fr = new Path2D(); fr.rect(cx - cw / 2, cy - ch / 2, cw, ch); fr.rect(cx - cw / 2 + 20, cy - ch / 2 + 20, cw - 40, ch - 40);
    { const q = plateCtx(RP, 'yellow', cardT); q.save(); q.fillStyle = RISO.yellow; q.fill(fr, 'evenodd'); q.restore(); }
    const sh = new Path2D(); sh.rect(cx - cw / 2 + 18, cy - ch / 2 + 18, cw, ch); sh.rect(cx - cw / 2, cy - ch / 2, cw, ch);
    { const q = plateCtx(RP, 'pink', cardT); q.save(); q.fillStyle = RISO.pink; q.fill(sh, 'evenodd'); q.restore(); } }
  const tagK = pop(t, T.label), tagAt = [560, 690];
  const tagT = q => { designT(q); q.translate(tagAt[0], tagAt[1]); q.scale(tagK * 1.45, tagK * 1.45); };
  if (tagK > 0) { { g.save(); tagT(g); g.fillStyle = RISO.paper; g.fill((() => { const p = new Path2D(); p.moveTo(-150, -34); p.lineTo(-120, -58); p.lineTo(150, -58); p.lineTo(150, 58); p.lineTo(-120, 58); p.lineTo(-150, 34); p.closePath(); return p; })()); g.restore(); designT(g); }
    const [sx, sy] = mayaSlot(t); { const q = plateCtx(RP, 'teal', dT); q.save(); q.strokeStyle = RISO.teal; q.lineWidth = 3; q.beginPath(); q.moveTo(sx + 30, sy + 40); q.quadraticCurveTo((sx + tagAt[0] - 200) / 2, tagAt[1] + 40, tagAt[0] - 217 * tagK, tagAt[1]); q.stroke(); q.restore(); }
    const tag = new Path2D(); tag.moveTo(-150, -34); tag.lineTo(-120, -58); tag.lineTo(150, -58); tag.lineTo(150, 58); tag.lineTo(-120, 58); tag.lineTo(-150, 34); tag.closePath();
    const inner = new Path2D(); inner.rect(-108, -40, 244, 80); const fr = new Path2D(); fr.addPath(tag); fr.addPath(inner);
    { const q = plateCtx(RP, 'yellow', tagT); q.save(); q.fillStyle = RISO.yellow; q.fill(fr, 'evenodd'); q.restore(); } rfill(RP, 'pink', circPath(-128, 0, 8), 1, tagT); }
  risoPrint(g, RP, { grainOff: [0, 0] });
  if (mp) { designT(g); puppet(g, 'maya', mp.x, mp.y, MAYA.s, mp); }
  if (cardK > 0 && t < T.fTitleOut[1]) { cardT(g); const sz = Math.min(fitFont(g, fc.series[0], 400, 96, 'ArchivoBlack', 620), 96); risoType(g, fc.series[0], DCX, CARD_Y - 44, 400, sz, 'ArchivoBlack'); risoType(g, fc.series[1], DCX, CARD_Y + 50, 400, sz, 'ArchivoBlack'); }
  const capA = t < T.fCap - SLAM ? 0 : t < T.fCapOut[0] ? pop(t, T.fCap) : 1 - easeIn(seg(t, T.fCapOut[0], T.fCapOut[1]));
  if (capA > 0 && t < T.fCapOut[1]) { designT(g); g.translate(DCX, CARD_Y); g.scale(capA, capA); g.translate(-DCX, -CARD_Y); const sz = Math.min(fitFont(g, fc.caption[0], 400, 104, 'ArchivoBlack', 800), 104);
    risoType(g, fc.caption[0], DCX, CARD_Y - 52, 400, sz, 'ArchivoBlack'); risoType(g, fc.caption[1], DCX, CARD_Y + 58, 400, sz, 'ArchivoBlack'); }
  if (tagK > 0) { tagT(g); risoType(g, fc.label, 14, 3, 400, 54, 'ArchivoBlack', 224, 'center', 1.6); }
}
const P2 = P => P;
function risoThumb(c, hp) { c.save(); designT(c); c.fillStyle = RISO.paper; const G = HAND.geo(hp.grip); c.fill(polyPath(HAND.T(G.thumb, hp))); c.restore();
  clearPlates(RP); risoHand(RP, hp, 'thumb', q => designT(q)); risoPrint(c, RP, { grainOff: [0, 0] }); }
function careersFinance(t) {
  const hp = handPoseCF(t), st = propCF(t, hp), ps = easeIO(seg(t, T.sc[0], T.sc[1])), po = easeIO(seg(t, T.ob[0], T.ob[1])), front = thumbFront(st, hp);
  if (st.kind === 'letter' || st.kind === 'check') { mixFace(FACE.f, FACE.fInk, FACE.fRiso, OBJ_F, po, letterInkHeadline); mixFace(FACE.bt, FACE.btInk, FACE.btRiso, OBJ_B, po); mixFace(FACE.bb, FACE.bbInk, FACE.bbRiso, OBJ_B, po); }
  resetT(c); c.globalCompositeOperation = 'source-over'; c.globalAlpha = 1;
  if (ps < 1) careersScene(c, t, hp, !front);
  if (ps > 0) { financeScene(t, hp, !front); maskedDraw(c, RISO_L, ps, .09, FLUO); }
  if (st.kind === 'A' || st.kind === 'B' || (st.kind === 'letter' && t < T.fly)) drawCard(c, st, t);
  else if (st.kind === 'letter' || st.kind === 'check') {
    if (t < T.tear) drawObject(c, st, ps, po);
    else { const x0 = st.x - SHEET.w / 2 * st.s, y0 = st.y - SHEET.ph / 2 * st.s; checkPiece(c, 'rest', x0, y0, st.s, st.rot); const ch = chunkState(t); if (ch) checkPiece(c, 'chunk', ch.x, ch.y, ch.s, ch.rot); }
  }
  if (front) { if (ps < .5) { c.save(); designT(c); inkHand(c, hp, 'thumb'); c.restore(); } else risoThumb(c, hp); }
}

// ---- productivity (graphite): drawn to its own page, which T3 tears and peels
const ROWS = [0, 1, 2, 3, 4, 5].map(i => ({ y: 450 + 95 * i, len: [330, 250, 380, 290, 340, 0][i] }));
const SCRIB = ROWS.map((r, i) => { const q = rng(500 + i), pts = []; for (let x = 410; x <= 410 + r.len; x += 9) pts.push([x, r.y + (Math.floor((x - 410) / 9) % 2 ? -8 : 5) * (.6 + q() * .5)]); return pts; });
const BOX = r => [[344, r.y - 22], [388, r.y - 22], [388, r.y + 22], [344, r.y + 22]];
const CHECKM = r => smooth([[350, r.y - 2], [362, r.y + 14], [394, r.y - 30]], false, 5);
function hanaPose(t) { const u = t - (T.hNod - SLAM), reach = easeOutBack(seg(t, T.reach, T.rip)) ;
  return { head: (u > 0 && u < .6 ? .06 * Math.sin(Math.PI * u / .6) : 0) + .015 * Math.sin(t * 1.3), arm: -.12 * easeIO(seg(t, T.pCap, T.pCap + .4)) * (1 - seg(t, T.pCap + 1.2, T.pCap + 1.8)) - 1.1 * reach, arm2: .02 * Math.sin(t * 1.1 + 1) }; }
function handPoseP(t) {   // your hand with the blue pencil: in, to each box, out of the way
  const tip = i => [362, ROWS[i].y], rest = [760, 1150], G = p => [p[0] + 166, p[1] + 152];
  let target = G(tip(0)), y0 = 0;
  const pts = [[T.listDraw[1] - .3, ...G(tip(0))]]; T.checks.forEach((tc, i) => { pts.push([tc - .1, ...G(tip(i))]); pts.push([tc + .02, ...G(tip(i))]); }); pts.push([T.checks[4] + .4, ...G(rest)]);
  const [x, y] = kf(t, pts); y0 = 700 * (1 - easeOut(seg(t, T.listDraw[1] - .7, T.listDraw[1] - .3)));
  return { x, y: y + y0, rot: -.1, s: 1, grip: 1 };
}
function productivity(g, t) {
  const pc = COPY.productivity; resetT(g); g.globalCompositeOperation = 'source-over'; g.globalAlpha = 1; g.drawImage(GRAPH_BG, 0, 0, W, H);
  designT(g); puppet(g, 'hana', HANA.x, HANA.y, HANA.s, hanaPose(t));
  const pl = PEN_L, pg = clearLayer(pl); designT(pg);
  ROWS.forEach((r, i) => { const t0 = T.listDraw[0] + i * .15, p = seg(t, t0, t0 + .13); if (p > 0) pencilLoop(pg, resample(BOX(r), 4), 2, 600 + i, { progress: p, al: .6 });
    const q = seg(t, t0 + .06, t0 + .15); if (q > 0 && r.len) pencil(pg, SCRIB[i], 2.2, 610 + i, { progress: q, al: .55, passes: 2 }); });
  if (t >= T.pTitle) { const p = seg(t, T.pTitle + .05, T.pTitle + .45); if (p > 0 && t < T.pTitleOut[1]) { pg.save(); pg.globalAlpha = 1 - seg(t, T.pTitleOut[0], T.pTitleOut[1]); pencil(pg, smooth([[250, 262], [459, 256], [668, 264]], false, 6), 5, 620, { col: GRAPH.sky, progress: p, al: .8 }); pg.restore(); } }
  graphLay(g, pl);
  // the blue checks, drawn on (in the pencil's colour)
  const cl = clearLayer(pl); designT(cl); T.checks.forEach((tc, i) => { const p = seg(t, tc - .12, tc); if (p > 0) pencil(cl, CHECKM(ROWS[i]), 5, 630 + i, { col: GRAPH.sky, progress: p, al: .9, passes: 2 }); }); graphLay(g, pl, { tooth: .5 });
  // your hand
  if (t > T.listDraw[1] - .7) { const hp = handPoseP(t); designT(g); graphHand(g, hp, 'back'); graphHand(g, hp, 'prop'); graphHand(g, hp, 'thumb'); }
  // type: the note, the title, the caption, the last item
  designT(g);
  if (t < T.noteOut[1]) { const a = 1 - seg(t, T.noteOut[0], T.noteOut[1]); g.save(); g.globalAlpha = a; g.translate(DCX + 40, 185); g.rotate(-.02); g.fillStyle = 'rgba(40,40,40,.08)'; g.fillRect(-250 + 7, -150 + 9, 500, 300);
    g.fillStyle = tint(GRAPH.sky, .35); g.fillRect(-250, -150, 500, 300); g.fillStyle = alpha(GRAPH.sky, .9); g.fillRect(-250, -150, 500, 34);
    const sz = Math.min(fitFont(g, pc.note[0], 400, 76, 'Inter', 430), fitFont(g, pc.note[1], 400, 76, 'Inter', 430)); graphType(g, pc.note[0], 0, -2, 400, sz); graphType(g, pc.note[1], 0, 16 + sz * 1.1, 400, sz); g.restore(); }
  if (t >= T.pTitle - SLAM && t < T.pTitleOut[1]) { const a = Math.min(seg(t, T.pTitle - SLAM, T.pTitle), 1 - seg(t, T.pTitleOut[0], T.pTitleOut[1])); g.save(); g.globalAlpha = a; graphType(g, pc.series, DCX, 180 + 6 * (1 - Math.min(1, seg(t, T.pTitle - SLAM, T.pTitle))), 300, 150, 820); g.restore(); }
  if (t >= T.pCap - SLAM && t < T.pCapOut[1]) { const a = Math.min(seg(t, T.pCap - SLAM, T.pCap), 1 - seg(t, T.pCapOut[0], T.pCapOut[1])); g.save(); g.globalAlpha = a;
    const sz = Math.min(...pc.caption.map(l => fitFont(g, l, 400, 70, 'Inter', 840))); pc.caption.forEach((l, i) => graphType(g, l, DCX, 80 + i * sz * 1.25, 400, sz)); g.restore(); }
  if (t >= T.last - SLAM) { g.save(); g.globalAlpha = seg(t, T.last - SLAM, T.last); graphType(g, pc.last, 410, ROWS[5].y + 2, 500, 66, 460, GRAPH.lead, 'left'); g.restore(); }
}
// T3: the page tears along its top and peels away like a sticker backing
const RIP = (() => { const r = rng(909), pts = []; for (let x = -20; x <= W + 20; x += 12 + r() * 10) pts.push([x, 26 + (r() - .5) * 22 + Math.sin(x / 40) * 6]); return pts; })();
function peelPage(c, t) {
  const drop = 14 * easeOut(seg(t, T.rip, T.rip + .1)), P = [...RIP.map(([x, y]) => [x, y + drop]), [W + 20, H + 20], [-20, H + 20]];
  const d = [W, H].map(v => v / Math.hypot(W, H)), full = Math.hypot(W, H) + 60, u = full * easeIn(seg(t, T.peel[0], T.peel[1])) ** .9;
  const half = (sgn) => { const p = new Path2D(), o = [d[0] * u, d[1] * u], n = [-d[1], d[0]], L = 5000; const a = [o[0] + n[0] * L, o[1] + n[1] * L], b = [o[0] - n[0] * L, o[1] - n[1] * L];
    p.moveTo(...a); p.lineTo(...b); p.lineTo(b[0] + sgn * d[0] * L, b[1] + sgn * d[1] * L); p.lineTo(a[0] + sgn * d[0] * L, a[1] + sgn * d[1] * L); p.closePath(); return p; };
  c.save(); resetT(c);
  c.save(); c.clip(half(+1)); c.save(); c.clip(polyPath(P)); c.drawImage(PAGE_L, 0, 0, W, H); c.restore();
  if (u > 0) { const g2 = c.createLinearGradient(d[0] * u, d[1] * u, d[0] * (u + 70), d[1] * (u + 70)); g2.addColorStop(0, 'rgba(30,30,30,.22)'); g2.addColorStop(1, 'rgba(30,30,30,0)'); c.fillStyle = g2; c.fill(polyPath(P)); }
  const R = P.map(([x, y]) => { const k = 2 * (u - (x * d[0] + y * d[1])); return [x + k * d[0], y + k * d[1]]; });
  if (u > 0) { c.save(); c.shadowColor = 'rgba(0,0,0,.25)'; c.shadowBlur = 18; c.shadowOffsetX = 8; c.shadowOffsetY = 10; const gb = c.createLinearGradient(d[0] * u, d[1] * u, d[0] * (u + 420), d[1] * (u + 420));
    gb.addColorStop(0, '#FFFFFF'); gb.addColorStop(.12, '#F4F4F2'); gb.addColorStop(.5, '#E9E9E6'); gb.addColorStop(1, '#DADAD6'); c.fillStyle = gb; c.fill(polyPath(R)); c.restore();
    c.strokeStyle = 'rgba(255,255,255,.9)'; c.lineWidth = 3; c.beginPath(); const o = [d[0] * (u + 6), d[1] * (u + 6)]; c.moveTo(o[0] - d[1] * 3000, o[1] + d[0] * 3000); c.lineTo(o[0] + d[1] * 3000, o[1] - d[0] * 3000); c.save(); c.clip(polyPath(R)); c.stroke(); c.restore(); }
  c.restore(); c.restore();
}

// ---- travel (stickers)
function diegoPose(t) { const q = ring(t - T.dPop, .08, 9, 22) + ring(t - T.hop, .08, 9, 22), air = t > T.hop - .3 && t < T.hop ? Math.sin(Math.PI * seg(t, T.hop - .3, T.hop)) : 0;
  const worry = t >= T.uhoh - .05 && t < T.qOut[1] - .2, w = worry ? easeOutBack(seg(t, T.uhoh - SLAM, T.uhoh)) : 0;
  return { sx: 1 + q * .6 + .03 * w, sy: 1 - q - .05 * w + .06 * air, tilt: -.06 * w, bob: 90 * air, head: -.08 * w + .02 * Math.sin(t * 3), headImg: worry ? 'head_uhoh' : 'head' }; }
function handPoseV(t) {
  const GA = [700, 740], GB = GB_, GC = [OPEN_[0] + 14, OPEN_[2] + 26], GD = [OPEN_[1] - 2, OPEN_[2] + 26];
  let [x, y] = kf(t, [[T.handIn2[0], GA[0] + 150, GA[1] + 760], [T.handIn2[1], ...GA], [T.move - .28, ...GA], [T.move, ...GB], [T.move + .5, ...GB], [T.zip - .45, ...GC], [T.zip - .15, ...GC], [T.zip, ...GD], [T.zip + .35, ...GD], [T.zip + .9, GD[0] + 200, GD[1] + 800]]);
  if (t > T.move - .28 && t < T.move) y -= 90 * Math.sin(Math.PI * seg(t, T.move - .28, T.move));
  const grip = t < T.move ? 1 : t < T.zip - .2 ? 1 - easeIO(seg(t, T.move, T.move + .08)) : easeIO(seg(t, T.zip - .2, T.zip - .15));
  return { x, y: y + settle(t, T.handIn2[1], 12, 10, 26, .3), rot: -.1, s: 1, grip };
}
function stkIn(t, t0, t1) { if (t < t0 - SLAM || (t1 && t >= t1[1])) return 0; if (t1 && t >= t1[0]) return 1 - easeIn(seg(t, t1[0], t1[1])); return t < t0 ? lerp(1.35, .96, easeIn(seg(t, t0 - SLAM, t0))) : 1 + settle(t, t0, -.04, 13, 28, .26); }
function travel(g, t) {
  resetT(g); g.globalCompositeOperation = 'source-over'; g.globalAlpha = 1; g.drawImage(STK_BG, 0, 0, W, H); designT(g);
  // Diego (his art is already a sticker; its shadow is his die-cut silhouette)
  const dp = diegoPose(t), M = PUP.diego, ks = DIEGO.s, sk = STKS.diegoShadow; g.save(); g.translate(DIEGO.x, DIEGO.y); g.rotate(dp.tilt || 0); g.scale(ks * dp.sx, ks * dp.sy); g.translate(-M.feet[0], -M.feet[1] - (dp.bob || 0));
  g.drawImage(sk.shadow, M.sticker[0] - sk.pad + 10, M.sticker[1] - sk.pad + 14, sk.shadow.width, sk.shadow.height); g.restore(); puppet(g, 'diego', DIEGO.x, DIEGO.y, ks, dp);
  if (t >= T.uhoh - SLAM && t < T.qOut[1] - .2) { const k = stkIn(t, T.uhoh); const [hx, hy] = refPoint('diego', [700, 180], DIEGO.x, DIEGO.y, ks, dp); putSticker(g, STKS.drop, hx + 6, hy + 8 * Math.sin(t * 8), { s: k }); }
  // the checked suitcase (open) and the carry-on
  putSticker(g, STKS.suitLid, 700, 985, { ax: 180, ay: 270, rot: -.04 }); putSticker(g, STKS.suitBase, 700, 1110, { ax: 195, ay: 165 });
  const hp = handPoseV(t), shut = t >= T.zip, zp = seg(t, T.zip - .15, T.zip), bankIn = t >= T.move;
  putSticker(g, shut ? STKS.packShut : STKS.packOpen, PACK[0], PACK[1], { ax: 110, ay: 280 });
  if (!shut && t >= T.zip - .15) { g.save(); const x = lerp(OPEN_[0], OPEN_[1], zp); g.beginPath(); g.moveTo(OPEN_[0], OPEN_[2]); g.quadraticCurveTo((OPEN_[0] + x) / 2, OPEN_[2] - 12, x, OPEN_[2]); g.strokeStyle = STK.ink; g.lineWidth = 7; g.stroke(); g.restore(); }
  // your hand, the power bank between its back and its thumb
  if (t >= T.handIn2[0] && t < T.zip + .9) {
    stkHand(g, hp, 'back');
    if (!bankIn) putSticker(g, STKS.bank, hp.x - 6, hp.y + 2, { ax: 48, ay: 156, rot: hp.rot });
    else if (t < T.move + .2) { const a = easeIn(seg(t, T.move, T.move + .18)); g.save(); g.beginPath(); g.rect(-400, -400, 1800, OPEN_[2] + 400); g.clip(); putSticker(g, STKS.bank, GB0(0) - 6, GB0(1) + 2 + 300 * a, { ax: 48, ay: 156 }); g.restore(); }
    if (t >= T.zip - .2 && t < T.zip) putSticker(g, STKS.pull, hp.x - 10, hp.y - 8, { ax: 13, ay: 34 });
    stkHand(g, hp, 'thumb');
  }
  if (t < T.zip - .2) putSticker(g, STKS.pull, OPEN_[0] + 4, OPEN_[2] + 26, { ax: 13, ay: 34 }); else if (t >= T.zip) putSticker(g, STKS.pull, OPEN_[1] - 6, OPEN_[2] + 26, { ax: 13, ay: 34 });
  // the cards
  const k1 = stkIn(t, T.vTitle, T.vTitleOut); if (k1 > 0) putSticker(g, STKS.title, DCX, CARD_Y, { s: k1 });
  const k2 = stkIn(t, T.q, T.qOut); if (k2 > 0) { putSticker(g, STKS.q, DCX, CARD_Y, { s: k2 }); const k3 = stkIn(t, T.pass, T.qOut); if (k3 > 0) { g.save(); g.translate(DCX, CARD_Y); g.scale(k2, k2); putSticker(g, STKS.pass, 236, 214, { s: k3, rot: -.08 }); g.restore(); } }
  const k4 = stkIn(t, T.vCap, T.vCapOut); if (k4 > 0) putSticker(g, STKS.cap, DCX, CARD_Y, { s: k4 });
}
const PACK = [410, 1110], OPEN_ = [PACK[0] - 86, PACK[0] + 86, PACK[1] - 214], GB_ = [PACK[0] + 10, PACK[1] - 330], GB0 = i => GB_[i];

// ---- the open, the lineup, the end card (the reel's own plain frame)
function openPage(g, t) { resetT(g); g.globalCompositeOperation = 'source-over'; g.drawImage(PLAIN_BG, 0, 0, W, H); designT(g);
  const k = 1 + settle(t, 0, .09, 12, 26, .22), o = COPY.open; g.save(); g.translate(DCX, 560); g.scale(k, k); g.translate(-DCX, -560);
  const s1 = plainType(g, o[0], DCX, 450, 176, 900, { lift: 11 }), s2 = fitFont(g, o[1], 800, 280, 'Bricolage', 900); plainType(g, o[1], DCX, 450 + s1 * .5 + s2 * .62, s2, 900, { lift: 16 }); g.restore(); }
function openFlip(c, t) {   // the page flips up about its top edge; its free edge comes toward the camera
  const th = Math.PI / 2 * easeIn(seg(t, T.flip[0], T.flip[1])), k = Math.cos(th), n = 32, grow = .32 * Math.sin(th); if (k < .003) return;
  c.save(); resetT(c); for (let i = 0; i < n; i++) { const v0 = i / n, v1 = (i + 1) / n, ws = 1 + grow * (v0 + v1) / 2; c.drawImage(OPEN_L, 0, v0 * OPEN_L.height, OPEN_L.width, OPEN_L.height / n, W / 2 - W * ws / 2, v0 * H * k - .5, W * ws, H * k / n + 1); }
  c.fillStyle = `rgba(20,18,14,${.35 * Math.sin(th)})`; c.fillRect(-W * grow / 2, 0, W * (1 + grow), H * k); c.restore(); }
function lineup(g, t) { resetT(g); g.drawImage(PLAIN_BG, 0, 0, W, H); designT(g);
  ['raj', 'maya', 'hana', 'diego'].forEach((n, i) => { const S = STKS['line_' + n], k = stkIn(t, T.slaps[i]); if (k > 0) putSticker(g, S, [132, 350, 572, 786][i], [1122, 1104, 1126, 1108][i], { ax: S.w / 2, ay: S.h, s: k, rot: [-.035, .03, -.02, .035][i] }); });
  if (t >= T.lCap - SLAM) { const k = pop(t, T.lCap, .6, 1.04), l = COPY.lineup; g.save(); g.translate(DCX, 175); g.scale(k, k); g.translate(-DCX, -175); const sz = Math.min(fitFont(g, l[0], 800, 96, 'Bricolage', 880), fitFont(g, l[1], 800, 96, 'Bricolage', 880));
    plainType(g, l[0], DCX, 110, sz, 880); plainType(g, l[1], DCX, 110 + sz * 1.15, sz, 880); g.restore(); } }
function endCard(g, t) { resetT(g); g.drawImage(PLAIN_BG, 0, 0, W, H); designT(g); const e = COPY.end;
  const line = (t0, fn) => { if (t < t0 - SLAM) return; const a = seg(t, t0 - SLAM, t0), dy = 18 * (1 - easeOut(a)); g.save(); g.globalAlpha = easeOut(a); g.translate(0, dy); fn(); g.restore(); };
  line(T.e1, () => { const sz = Math.min(fitFont(g, e.lines[0], 800, 118, 'Bricolage', 860), fitFont(g, e.lines[1], 800, 118, 'Bricolage', 860)); plainType(g, e.lines[0], DCX, 330, sz, 860, { lift: 8 }); plainType(g, e.lines[1], DCX, 330 + sz * 1.08, sz, 860, { lift: 8 }); });
  line(T.e2, () => { plainType(g, e.sub, DCX, 640, 64, 800, { col: PLAIN.ink2 }); g.fillStyle = PLAIN.ink; g.fillRect(DCX - 60, 730, 120, 5); });
  line(T.e3, () => plainType(g, e.name, DCX, 850, 88, 880));
  line(T.e4, () => plainType(g, e.email, DCX, 960, 70, 880, { col: PLAIN.ink2 })); }

// ================= the frame =================
function frame(i) {
  const t = i / FPS; resetT(c); c.globalCompositeOperation = 'source-over'; c.globalAlpha = 1;
  if (t < T.flip[0]) openPage(c, t);
  else if (t < T.flip[1]) { careersFinance(t); openPage(OPEN_L.getContext('2d'), 1.5); openFlip(c, t); }
  else if (t < T.cut) careersFinance(t);
  else if (t < T.rip) productivity(c, t);
  else if (t < T.peel[1]) { travel(c, t); productivity(PAGE_L.getContext('2d'), t); peelPage(c, t); }
  else if (t < A_('lineup')) travel(c, t);
  else if (t < A_('end')) lineup(c, t);
  else endCard(c, t);
  if (SHOW_SAFE) safeOverlay(c);
}
window.__NFR = NFR;
window.__frame = i => { frame(i); return CV.toDataURL('image/png'); };
(async () => {
  try {
    COPY = await (await fetch('reel.json')).json();
    await Promise.all([['900 60px Playfair'], ['700 60px Playfair'], ['400 60px ArchivoBlack'], ['300 60px Inter'], ['400 60px Inter'], ['600 60px Inter'], ['700 60px Fredoka'], ['800 60px Bricolage']].map(([f]) => document.fonts.load(f)));
    await Promise.all(['raj', 'maya', 'hana', 'diego'].map(loadPuppet));
    await Promise.all(['raj', 'maya', 'hana', 'diego'].map(n => loadImg(n + '_sticker', `assets/${n}_sticker.png`)));
    build();
    window.__TL = { bpm: BPM, bar: BAR, dur: DUR, nfr: NFR, fps: FPS, sections: SEC, T, K, DCX, DCY, SCY: SCY_, CARD_Y, rows: ROWS.map(r => r.y) };
    frame(0); window.__ready = true;
    if (!Q.has('bare')) { const t0 = performance.now(); const tick = () => { frame(Math.floor((performance.now() - t0) / 1000 * FPS) % NFR); requestAnimationFrame(tick); }; tick(); }
  } catch (e) { window.__error = String(e.stack || e); console.error(e); }
})();
