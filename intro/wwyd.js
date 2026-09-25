'use strict';
/* WHAT WOULD YOU DO?: the series template. One data object per episode (wwyd/epNN.json) drives the film; the recurring
   parts (title card, freeze-frame with options, pause countdown, the three answer reveals, takeaway, end card) live
   here and look, time and sound identical in every episode. Bar counts come from wwyd/template.json (read by the score
   too) and are enforced by buildTimeline(). An episode registers its drawings in SCENES:
     SCENES.tease(c, t, S)        the title card's picture (e.g. a phone already ringing)
     SCENES[sceneId](c, t, S)     each setup scene; the last frame of the last one is the freeze-frame
     SCENES['reveal_' + key]       what each answer leads to, drawn under the answer card
   S.at(bar, beat) is time inside the segment. Captions come from the data: [bar, beat, line 1, line 2].

   timeline: TITLE | setup scenes | FREEZE | PAUSE | REVEAL A | REVEAL B | REVEAL C | TAKEAWAY | END (+ the official logo)
*/
const EP_PATH = Q.get('ep') || window.EPISODE;
const SCENES = {};
let TPL = null, EP = null, TL = [], DUR = 0, NFR = 0, STAMP_T = 0, SNAP = null;
const PUSH = .3;                       // the camera drop between segments, centred on the downbeat
const NO_PUSH = { freeze: 1, pause: 1 };   // the freeze cuts in on the downbeat and the pause holds still

// ================= the timeline (the template enforces it) =================
function buildTimeline(tpl, ep) {
  const fail = m => { throw new Error(`WHAT WOULD YOU DO? template: ${m}`); };
  if (!Array.isArray(ep.options) || ep.options.length !== tpl.options) fail(`exactly ${tpl.options} options`);
  ep.options.forEach((o, i) => { if (o.verdict !== tpl.verdicts[i]) fail(`option ${o.key} must be ${tpl.verdicts[i]} (options run wrong, close, right)`);
    if (!Array.isArray(o.lines) || o.lines.length < 1 || o.lines.length > 2) fail(`option ${o.key} needs 1 or 2 lines`); });
  if (!ep.takeaway || ep.takeaway.length !== 2 || !ep.bonus || ep.bonus.length !== 2) fail('takeaway and bonus are 2 lines each');
  ep.scenes.forEach(s => { if (!Number.isInteger(s.bars) || s.bars < 1 || s.bars > tpl.maxSceneBars) fail(`scene ${s.id} must be 1-${tpl.maxSceneBars} whole bars`);
    if (!SCENES[s.id]) fail(`no draw function for scene ${s.id}`); });
  if (!SCENES.tease) fail('no title-card picture (SCENES.tease)');
  ep.options.forEach(o => { if (!SCENES['reveal_' + o.key]) fail(`no draw function for reveal_${o.key}`); });
  const segs = [], add = (kind, bars, data = {}) => { const b0 = segs.length ? segs[segs.length - 1].b0 + segs[segs.length - 1].bars : 0; segs.push({ kind, bars, b0, ...data }); };
  add('title', tpl.bars.title, { id: 'title' });
  ep.scenes.forEach(s => add('scene', s.bars, s));
  add('freeze', tpl.bars.freeze, { id: 'freeze' });
  add('pause', tpl.bars.pause, { id: 'pause' });
  ep.options.forEach((o, i) => add('reveal', tpl.bars.reveal, { id: o.key, opt: o, i, caps: o.caps }));
  add('takeaway', tpl.bars.takeaway, { id: 'takeaway' });
  add('end', tpl.bars.end, { id: 'end' });
  segs.forEach(s => { s.t0 = at(s.b0); s.t1 = at(s.b0 + s.bars); s.at = (bar, beat = 1) => at(s.b0 + bar - 1, beat); });
  return segs;
}
const segAt = t => { for (let i = TL.length - 1; i >= 0; i--) if (t >= TL[i].t0 - (NO_PUSH[TL[i].kind] ? 0 : PUSH / 2)) return i; return 0; };

// ================= puppets =================
const PUP = {};   // name -> parts meta (Grandma, the Grandson: head, torso, phone arm, two legs)
function puppet(c, name, x, y, s, p = {}) {
  const M = PUP[name];
  c.save(); c.translate(x, y); c.rotate(p.tilt || 0); c.scale(s * (p.sx || 1), s * (p.sy || 1)); c.translate(-M.feet[0], -M.feet[1] - (p.bob || 0));
  const part = (k, a = 0) => { const m = M.parts[k], [px, py] = m.pivot; c.save(); c.translate(px, py); c.rotate(a); c.translate(-px, -py); c.drawImage(IMG[name + '_' + k], m.x, m.y); c.restore(); };
  part('legL', p.legL || 0); part('legR', p.legR || 0); part('torso'); part('arm', p.arm || 0); part('head', p.head || 0);
  c.restore();
}
const SIL = layer();
function silhouette(c, col, alpha, draw) {   // anything drawn by draw(g), as one flat shape (the voice on the line)
  const g = SIL.getContext('2d'); g.setTransform(1, 0, 0, 1, 0, 0); g.globalCompositeOperation = 'source-over'; g.clearRect(0, 0, SIL.width, SIL.height);
  g.setTransform(c.getTransform()); draw(g);
  g.setTransform(1, 0, 0, 1, 0, 0); g.globalCompositeOperation = 'source-in'; g.fillStyle = col; g.fillRect(0, 0, SIL.width, SIL.height); g.globalCompositeOperation = 'source-over';
  c.save(); c.setTransform(1, 0, 0, 1, 0, 0); c.globalAlpha = alpha; c.drawImage(SIL, 0, 0); c.restore();
}

// ================= shared pieces =================
function chip(c, s, x, y, size, bg, fg, t, t0, rot = 0, maxW = 780, from = 1.3) {
  if (t < t0 - SLAM) return; c.font = `${size}px Stamp`; const w = Math.min(c.measureText(s).width, maxW) + 60, h = size * 1.3, k = t < t0 ? lerp(from, 1, easeIn(land(t, t0))) : pop(t, t0);
  c.save(); c.translate(x, y); c.rotate(rot); c.scale(k, k);
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fillRect(-w / 2 + 8, -h / 2 + 10, w, h); c.restore();
  ink(c, rect(-w / 2, -h / 2, w, h), bg, 8100 + s.length, { amp: 3 }); inkText(c, s, 0, size * .06, size, 'Stamp', fg, maxW); c.restore();
}
const CAP_Y = [378, 488], CAP_LOW = [1222, 1322];
function captions(c, t, S, ys = CAP_Y) {   // the current caption of a segment: from its beat until the next caption
  let cur = null; for (const cp of S.caps || []) if (t >= S.at(cp[0], cp[1]) - SLAM) cur = cp;
  if (!cur) return; const t0 = S.at(cur[0], cur[1]);
  cur.slice(2).forEach((s, i) => chip(c, s, SCX, ys[i], 66, BLK, CHIP, t, t0 + i * E8, i % 2 ? .012 : -.012, 730, 1.1));   // inside the safe width, tilt and landing included
}
function burst(c, x, y, t, t0, r0 = 220) {
  const u = seg(t, t0, t0 + .35); if (u <= 0 || u >= 1) return;
  c.save(); c.strokeStyle = YEL; c.lineCap = 'round'; c.globalAlpha = 1 - u;
  for (let k = 0; k < 12; k++) { const a = k / 12 * TAU + .13, r1 = r0 + 60 * easeOut(u), r2 = r1 + 60; c.lineWidth = 14; c.beginPath(); c.moveTo(x + Math.cos(a) * r1, y + Math.sin(a) * r1 * .5); c.lineTo(x + Math.cos(a) * r2, y + Math.sin(a) * r2 * .5); c.stroke(); }
  c.restore();
}
function sceneBg(c) { bgDots(c, BLK, .04, .22, 18); }
function flash(c, t, t0, d = .16) { const u = seg(t, t0, t0 + d); if (u <= 0 || u >= 1) return; screenSpace(c, () => { c.globalAlpha = 1 - u; c.fillStyle = CHIP; c.fillRect(0, 0, W, H); }); }

// the answer cards: letter badge + one or two lines, fully opaque
const OPT = { x: 70, w: 820, h: 150, y: [872, 1040, 1208] };
function optionCard(c, o, cx, cy, t, t0, state = 'normal', s = 1) {
  if (t < t0 - SLAM) return; const k = pop(t, t0) * s, { w, h } = OPT;
  const bg = { normal: CHIP, WRONG: '#d9d2c2', CLOSE: CHIP, RIGHT: YEL }[state], edge = state === 'RIGHT' ? 10 : 6;
  c.save(); c.translate(cx, cy); c.scale(k, k);
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fillRect(-w / 2 + 10, -h / 2 + 12, w, h); c.restore();
  block(c, rrPts(-w / 2, -h / 2, w, h, 26, 5), bg, 8200 + o.key.charCodeAt(0), { kw: edge });
  block(c, ellPts(-w / 2 + 70, 0, 46, 46, 0, 30), state === 'RIGHT' ? BLUE : BLK, 8210 + o.key.charCodeAt(0), { kw: 4 });
  inkText(c, o.key, -w / 2 + 70, 5, 62, 'Stamp', CHIP, 60);
  const ys = o.lines.length === 1 ? [4] : [-30, 36];
  o.lines.forEach((ln, i) => inkText(c, ln, -w / 2 + 140, ys[i], 52, 'Stamp', BLK, w - 170, 'left'));
  c.restore();
}
function countdown(c, t, t0, t1, x = 812, y = 496, r = 82) {
  if (t < t0 - SLAM || t >= t1) return;
  const u = clamp01((t - t0) / (t1 - t0)), n = Math.max(1, 8 - Math.floor((t - t0) / BEAT)), last = n <= 3;
  const k = pop(t, t0) * (last ? 1 + .08 * Math.max(0, Math.cos((t - t0) * TAU / BEAT)) : 1);
  c.save(); c.translate(x, y); c.scale(k, k);
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.beginPath(); c.arc(8, 10, r, 0, TAU); c.fill(); c.restore();
  block(c, ellPts(0, 0, r, r, 0, 40), CHIP, 8301, { kw: 6 });
  c.fillStyle = last ? YEL : BLUE; c.beginPath(); c.moveTo(0, 0); c.arc(0, 0, r - 12, -Math.PI / 2, -Math.PI / 2 + TAU * (1 - u)); c.closePath(); c.fill();
  block(c, ellPts(0, 0, r * .56, r * .56, 0, 30), BLK, 8302, { kw: 0, key: false });
  inkText(c, String(n), 0, 6, 70, 'Stamp', CHIP, 80); c.restore();
}
// the freeze-frame: the last frame of the setup, drawn once and kept
function snapshot() {
  if (SNAP) return SNAP; const S = TL.filter(s => s.kind === 'scene').pop();
  const o = document.createElement('canvas'); o.width = OUT_W; o.height = OUT_H; const g = o.getContext('2d'); contentT(g);
  SCENES[S.id](g, S.t1 - 1e-3, { ...S, lt: S.t1 - S.t0 - 1e-3 }); return SNAP = o;
}
const POL = { x: SCX - 10, y: 600, w: 560, h: 470, rot: -.03 };
function frozen(c, u) {   // u 0: the full frame, 1: shrunk into the Polaroid above the options
  const im = snapshot();
  if (u <= 0) { c.save(); resetT(c); c.drawImage(im, 0, 0, W, H); c.restore(); return; }
  const e = easeIO(u), w = lerp(W / K, POL.w, e), h = lerp(H / K, POL.h, e), x = lerp(SCX, POL.x, e), y = lerp(SCY, POL.y, e);
  polaroid(c, x, y, w, h, POL.rot * e, 8400, (pw, ph) => {   // the scene's middle band, where the action is
    const sw = W, sh = sw * ph / pw, sy = Math.min(H - sh, Math.max(0, 1000 - sh / 2));   // screen y ~1000: Grandma and the call
    c.drawImage(im, 0, sy, sw, sh, -pw / 2, -ph / 2, pw, ph); });
}

// ================= the recurring parts =================
function partTitle(c, t, S) {   // TITLE (2 bars): WHAT WOULD YOU DO? on frame 0; the episode's picture underneath
  bgDots(c, BLUE, .12, .55);
  SCENES.tease(c, t, S);
  stampFit(c, 'WHAT WOULD', BLK, 150, SCX, 390, -.04, .95, t, S.t0 - 1, 840);
  stampFit(c, 'YOU DO?', BLUE, 170, SCX, 560, .03, 1, t, S.t0 - 1, 840);
  chip(c, `EPISODE ${EP.num}`, SCX, 680, 40, YEL, BLK, t, S.at(1, 2), .02);
}
function optionsList(c, t, t0s) { EP.options.forEach((o, i) => optionCard(c, o, SCX, OPT.y[i], t, t0s[i])); }
function partFreeze(c, t, S) {   // FREEZE (1 bar): the action stops on the downbeat; three options on beats 2, 3, 4
  bgDots(c, BLK, .06, .3, 18);
  frozen(c, seg(t, S.at(1, 1.5), S.at(1, 2)));
  if (t < S.at(1, 2)) stampFit(c, 'FREEZE!', BLK, 170, SCX, 860, -.06, 1, t, S.t0, 700, 1.3);
  chip(c, 'WHAT WOULD YOU DO?', SCX, 370, 70, BLK, CHIP, t, S.at(1, 2), -.012);
  optionsList(c, t, [S.at(1, 2), S.at(1, 3), S.at(1, 4)]);
  flash(c, t, S.t0);
}
function partPause(c, t, S) {   // PAUSE (2 bars): the options hold still; COMMENT A, B, OR C and an 8-beat countdown
  bgDots(c, BLK, .06, .3, 18);
  frozen(c, 1);
  const pulse = 1 + .03 * Math.max(0, Math.cos((t - S.t0) * TAU / BEAT));
  c.save(); c.translate(SCX, 370); c.scale(pulse, pulse); c.translate(-SCX, -370); chip(c, 'COMMENT A, B, OR C', SCX, 370, 70, BLUE, CHIP, t, S.t0 - 1, -.012); c.restore();
  optionsList(c, t, [-1, -1, -1]);
  countdown(c, t, S.t0, S.t1);
}
const VERDICT = { WRONG: ['WRONG.', BLK, -.06], CLOSE: ['CLOSE, BUT...', BLK, .04], RIGHT: ['RIGHT!', BLUE, -.04] };
function partReveal(c, t, S) {   // REVEAL (2 bars each): the answer card, its verdict on the downbeat, what happens next
  sceneBg(c);
  const o = S.opt, [word, col, rot] = VERDICT[o.verdict];
  SCENES['reveal_' + o.key](c, t, S);
  optionCard(c, o, SCX, 372, t, S.t0 - 1, o.verdict, .92);
  if (o.verdict === 'RIGHT') burst(c, SCX, 540, t, S.t0, 230);
  stampFit(c, word, col, 150, SCX, 540, rot, .9, t, S.t0, 760, 1.35);
  captions(c, t, S, CAP_LOW);
  // Jeff walks through the answers: steps in on the first, points at each card, thumbs up on the right one
  const first = S.i === 0, th = easeOutBack(seg(t, S.at(1, 1.5), S.at(1, 1.9)));
  const pose = o.verdict === 'RIGHT' ? { armR: lerp(-2.2, -2.5, th), prop: th > .6 ? 'thumb' : 'point', head: .06 } : { armR: -2.25, prop: 'point', head: o.verdict === 'WRONG' ? -.06 : .03 };
  if (first) jeffUp(c, t, S.at(1, 1.5), 120, pose, .5); else jeff(c, 120, 1850, .5, pose);
}
function partTakeaway(c, t, S) {   // TAKEAWAY (2 bars): the lesson, then the bonus tip
  bgDots(c, BLUE, .1, .5);
  chip(c, 'THE LESSON:', SCX, 370, 66, BLK, CHIP, t, S.at(1), -.012);
  stampFit(c, EP.takeaway[0], BLK, 120, SCX, 560, -.04, .95, t, S.at(1), 820, 1.25);
  stampFit(c, EP.takeaway[1], BLUE, 130, SCX, 730, .03, .95, t, S.at(1, 1.5), 820, 1.25);
  chip(c, 'BONUS TIP:', SCX, 900, 58, YEL, BLK, t, S.at(2), .015);
  EP.bonus.forEach((s, i) => chip(c, s, SCX, 1020 + i * 104, 66, i ? BLUE : BLK, CHIP, t, S.at(2, 1.5) + i * E8, i ? .015 : -.015));
  const th = easeOutBack(seg(t, S.at(1, 2), S.at(1, 2.4)));
  jeff(c, 120, 1850, .5, { armR: lerp(-2.25, -2.5, th), prop: th > .6 ? 'thumb' : 'point', head: .05 * Math.sin((t - S.t0) * TAU / (2 * BEAT)) });
}
function partEnd(c, t, S) {   // END (2 bars): COMMENT IF YOU GOT IT RIGHT, then the rubber stamp and the official logo
  bgDots(c, BLUE, .12, .55);
  stickerLogo(c, SCX, 420, 420, -.03, lerp(1.4, 1, easeIn(land(t, S.at(1)))));
  stampFit(c, 'COMMENT IF YOU', BLK, 130, SCX, 660, -.04, .95, t, S.at(1), 840, 1.25);
  stampFit(c, 'GOT IT RIGHT!', BLUE, 160, SCX, 850, .03, 1, t, S.at(1, 1.5), 840, 1.25);
  const wv = Math.sin((t - S.at(1, 2)) * TAU / BEAT) * .25;
  jeffUp(c, t, S.at(1, 2), SCX, { armR: -2.4 + (t > S.at(1, 2.3) ? wv : 0), head: .04 * Math.sin((t - S.t0) * TAU / (2 * BEAT)) }, .66);
  const d = seg(t, S.at(2), STAMP_T); if (d > 0) screenSpace(c, () => rubberStamp(c, easeIn(d)));
}
function sceneSignoff(c, t) {
  paperBg(c);
  liveEndCard(c);   // the closing card (vertkit.js): the official logo, LIVE ON YOUTUBE + INSTAGRAM, WED 5 PM ET / FRI 10 AM ET; untouched, still
  const lift = seg(t, STAMP_T, STAMP_T + .15);
  if (lift < 1) { c.save(); c.translate(0, -(H + 320) * easeIn(lift)); rubberStampFlat(c); c.restore(); }
}

// ================= assembly =================
const PARTS = { title: partTitle, freeze: partFreeze, pause: partPause, reveal: partReveal, takeaway: partTakeaway, end: partEnd };
function drawSeg(c, t, S) {
  if (S.kind === 'scene') { SCENES[S.id](c, t, { ...S, lt: t - S.t0 }); captions(c, t, S); }
  else PARTS[S.kind](c, t, S);
}
function drawScene(c, t) {
  if (t >= STAMP_T) { resetT(c); sceneSignoff(c, t); return; }   // screen space; no print finish over the official logo
  const i = segAt(t), S = TL[i], u = i > 0 && !NO_PUSH[S.kind] ? easeIO(seg(t, S.t0 - PUSH / 2, S.t0 + PUSH / 2)) : 1;
  if (u >= 1) { contentT(c); drawSeg(c, t, S); }
  else {   // the camera drops to the next segment
    const P = TL[i - 1], g1 = L1.getContext('2d'), g2 = L2.getContext('2d');
    contentT(g1); drawSeg(g1, Math.min(t, P.t1 - 1e-3), P); contentT(g2); drawSeg(g2, Math.max(t, S.t0 - PUSH / 2), S);
    c.save(); resetT(c); c.drawImage(L1, 0, -H * u, W, H); c.drawImage(L2, 0, H * (1 - u), W, H); c.restore(); contentT(c);
  }
  printFinish(c);
  if (SHOW_SAFE) safeOverlay(c);
}

// ================= runtime =================
const CV = document.getElementById('c'); CV.width = OUT_W; CV.height = OUT_H; const CTX = CV.getContext('2d');
function frame(i) { const t = Math.min(i / FPS, DUR - 1e-6); FILM_T = t; resetT(CTX); CTX.globalAlpha = 1; drawScene(CTX, t); resetT(CTX); }
window.__FPS = FPS; window.__frame = i => { frame(i); return CV.toDataURL('image/png'); };
(async () => {
  await loadPrintKit(); await loadVertKit();
  TPL = await (await fetch('wwyd/template.json')).json();
  EP = await (await fetch(EP_PATH + '.json')).json();
  for (const name of EP.cast || []) { PUP[name] = await (await fetch(`assets/wwyd/${name}_parts.json`)).json();
    await Promise.all(Object.keys(PUP[name].parts).map(k => loadImg(name + '_' + k, `assets/wwyd/${name}_${k}.png`))); }
  TL = buildTimeline(TPL, EP);
  const E = TL[TL.length - 1]; STAMP_T = E.at(2, 2); DUR = E.t1; NFR = Math.round(FPS * DUR); window.__NFR = NFR;
  window.__timeline = TL.map(s => ({ kind: s.kind, id: s.id, b0: s.b0, bars: s.bars, t0: s.t0, t1: s.t1 }));
  frame(+(Q.get('frame') || 0));
  window.__ready = true;
})().catch(e => { console.error(e); window.__error = String(e); });
