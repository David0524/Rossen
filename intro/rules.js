'use strict';
/* JEFF'S RULES: the series template. One data object per episode (rules/epNN.json) drives the whole film; the
   recurring parts (title card, rule reveal, recap card, end card) live here and look, time and sound identical in
   every episode. Their bar counts come from rules/template.json, which the score reads too. An episode supplies its
   middle scenes as draw functions in rules/epNN.js, registered by id in SCENES.

   timeline: TITLE | scenes before the rule | RULE | scenes after the rule | RECAP | END (+ the official logo)
   Every segment is a whole number of bars. Between segments the camera drops down to the next one (a vertical push
   centred on the downbeat). Captions come from the scene data: [bar, beat, line 1, line 2], landing on their beat.
*/
const EP_PATH = Q.get('ep') || window.EPISODE;
const SCENES = {};                 // SCENES[id] = (c, t, S) => {}; S.at(bar, beat) is time inside the scene, S.lt = t - start
let TPL = null, EP = null, TL = [], DUR = 0, NFR = 0, STAMP_T = 0;
const PUSH = .3;                   // the camera move between segments, centred on the downbeat

// ================= the timeline (the template enforces it) =================
function buildTimeline(tpl, ep) {
  const fail = m => { throw new Error(`JEFF'S RULES template: ${m}`); };
  if (!Array.isArray(ep.rule) || ep.rule.length !== tpl.ruleLines) fail(`the rule must be exactly ${tpl.ruleLines} lines`);
  if (!Array.isArray(ep.recap) || ep.recap.length !== 2) fail('the recap line must be 2 lines');
  if (!Array.isArray(ep.hook) || ep.hook.length < 1 || ep.hook.length > 2) fail('the hook must be 1 or 2 lines');
  if (!(ep.ruleAfter >= 0 && ep.ruleAfter <= ep.scenes.length)) fail('ruleAfter must point between scenes');
  ep.scenes.forEach(s => { if (!Number.isInteger(s.bars) || s.bars < 1 || s.bars > tpl.maxSceneBars) fail(`scene ${s.id} must be 1-${tpl.maxSceneBars} whole bars`);
    if (!SCENES[s.id]) fail(`no draw function for scene ${s.id}`); });
  const segs = [], add = (kind, bars, data = {}) => { const b0 = segs.length ? segs[segs.length - 1].b0 + segs[segs.length - 1].bars : 0; segs.push({ kind, bars, b0, ...data }); };
  add('title', tpl.bars.title, { caps: [] });
  ep.scenes.slice(0, ep.ruleAfter).forEach(s => add('scene', s.bars, s));
  add('rule', tpl.bars.rule, { caps: [] });
  ep.scenes.slice(ep.ruleAfter).forEach(s => add('scene', s.bars, s));
  add('recap', tpl.bars.recap, { caps: [] });
  add('end', tpl.bars.end, { caps: [] });
  segs.forEach(s => { s.t0 = at(s.b0); s.t1 = at(s.b0 + s.bars); s.at = (bar, beat = 1) => at(s.b0 + bar - 1, beat); });
  return segs;
}
const segAt = t => { for (let i = TL.length - 1; i >= 0; i--) if (t >= TL[i].t0 - PUSH / 2) return i; return 0; };

// ================= shared pieces =================
function chip(c, s, x, y, size, bg, fg, t, t0, rot = 0, maxW = 780) {
  if (t < t0 - SLAM) return; c.font = `${size}px Stamp`; const w = Math.min(c.measureText(s).width, maxW) + 60, h = size * 1.3, k = pop(t, t0);
  c.save(); c.translate(x, y); c.rotate(rot); c.scale(k, k);
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fillRect(-w / 2 + 8, -h / 2 + 10, w, h); c.restore();
  ink(c, rect(-w / 2, -h / 2, w, h), bg, 7100 + s.length, { amp: 3 }); inkText(c, s, 0, size * .06, size, 'Stamp', fg, maxW); c.restore();
}
const CAP_Y = [378, 488];
function sceneCaptions(c, t, S) {   // the current caption of a scene: from its beat until the next caption
  let cur = null; for (const cp of S.caps || []) if (t >= S.at(cp[0], cp[1]) - SLAM) cur = cp;
  if (!cur) return; const t0 = S.at(cur[0], cur[1]);
  cur.slice(2).forEach((s, i) => chip(c, s, SCX, CAP_Y[i], 74, BLK, CHIP, t, t0 + i * E8, i % 2 ? .012 : -.012));
}
function indexCard(c, y0, y1, num, seed = 7200) {   // the case-file index card every recurring part sits on
  shadowRect(c, 100, y0, 760, y1 - y0);
  block(c, [[100, y0], [130, y0 - 58], [400, y0 - 58], [430, y0], [860, y0], [860, y1], [100, y1]], CHIP, seed, { kw: 6 });
  ink(c, rect(100, y0 + 18, 760, 6), BLUE, seed + 1, { reg: false });
  inkText(c, `RULE #${num}`, 265, y0 - 26, 42, 'Stamp', BLK, 250);
}
function numBadge(c, x, y, num, s = 1) {
  c.save(); c.translate(x, y); c.scale(s, s); c.rotate(.08);
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.beginPath(); c.arc(8, 10, 92, 0, TAU); c.fill(); c.restore();
  block(c, ellPts(0, 0, 92, 92, 0, 44), YEL, 7300, { kw: 7 }); inkText(c, `#${num}`, 0, 8, 96, 'Stamp', BLK, 150); c.restore();
}
function burst(c, x, y, t, t0, r0 = 250) {   // yellow strike lines around a landing stamp (part of the rule signature)
  const u = seg(t, t0, t0 + .35); if (u <= 0 || u >= 1) return;
  c.save(); c.strokeStyle = YEL; c.lineCap = 'round'; c.globalAlpha = 1 - u;
  for (let k = 0; k < 12; k++) { const a = k / 12 * TAU + .13, r1 = r0 + 60 * easeOut(u), r2 = r1 + 60; c.lineWidth = 14; c.beginPath(); c.moveTo(x + Math.cos(a) * r1, y + Math.sin(a) * r1 * .5); c.lineTo(x + Math.cos(a) * r2, y + Math.sin(a) * r2 * .5); c.stroke(); }
  c.restore();
}

// ================= the recurring parts =================
function partTitle(c, t, S) {   // TITLE (2 bars): JEFF'S RULES #n and the hook, all on screen within the first second
  bgDots(c, BLUE, .12, .55);
  const breathe = 1 + .012 * Math.sin((t - S.t0) * Math.PI / BEAT);
  stampFit(c, "JEFF'S RULES", BLK, 150, SCX, 400, -.04, .95, t, S.t0 - 1, 840);
  c.save(); c.translate(SCX, 800); c.scale(breathe, breathe); c.translate(-SCX, -800);
  indexCard(c, 590, 1030, EP.num);
  EP.hook.forEach((s, i) => chip(c, s, SCX, 740 + i * 130 - (EP.hook.length - 1) * 0 , 84, i ? BLUE : BLK, CHIP, t, S.at(1, 2) + i * E8, i ? .015 : -.015));
  c.restore();
  numBadge(c, 790, 600, EP.num, t < S.t0 ? 1 : 1 + .04 * Math.max(0, Math.cos((t - S.t0) * TAU / BEAT)));
  jeffUp(c, t, S.at(2), SCX, { armR: -2.3, prop: 'point', head: .05 * Math.sin((t - S.t0) * TAU / (2 * BEAT)) }, .7);
}
function partRule(c, t, S) {   // RULE (2 bars): Jeff steps in, the rule stamps on in two strikes (the signature)
  bgDots(c, BLUE, .2, .62);
  chip(c, `JEFF'S RULE #${EP.num}`, SCX, 380, 70, BLK, CHIP, t, S.at(1), -.015);
  indexCard(c, 560, 1080, EP.num, 7210);
  const s1 = S.at(1, 3), s2 = S.at(2, 1);
  burst(c, SCX, 700, t, s1, 280); burst(c, SCX, 920, t, s2, 300);
  stampFit(c, EP.rule[0], BLK, 170, SCX, 700, -.04, 1, t, s1, 700, 1.4);
  stampFit(c, EP.rule[1], BLUE, 170, SCX, 920, .03, 1, t, s2, 700, 1.4);
  const a = easeOutBack(land(t, S.at(1, 2))), pt = easeOut(seg(t, S.at(1, 2), S.at(1, 2.5)));
  if (t >= S.at(1, 2) - SLAM) jeff(c, lerp(-300, 150, a), 1850, .6, { armR: lerp(-1, -2.4, pt), prop: pt > .5 ? 'point' : null, head: .05 });
}
function partRecap(c, t, S) {   // RECAP (2 bars): the rule again, then the line that makes it stick
  bgDots(c, BLUE, .08, .45);
  indexCard(c, 530, 1240, EP.num, 7220);   // tab top at 472, clear of the REMEMBER: chip (bottom 426)
  stampFit(c, EP.rule[0], BLK, 140, SCX, 670, -.04, .95, t, S.at(1), 680, 1.25);
  stampFit(c, EP.rule[1], BLUE, 140, SCX, 850, .03, .95, t, S.at(1, 1.5), 680, 1.25);
  EP.recap.forEach((s, i) => chip(c, s, SCX, 1030 + i * 110, 70, i ? BLUE : BLK, CHIP, t, S.at(2) + i * E8, i ? .015 : -.015, 640));   // never wider than the card
  chip(c, 'REMEMBER:', SCX, 380, 70, BLK, CHIP, t, S.at(1), -.015);
  const th = easeOutBack(seg(t, S.at(1, 2), S.at(1, 2.4)));
  jeffUp(c, t, S.at(1, 1.5), 140, { armR: lerp(0, -2.5, th), prop: th > .6 ? 'thumb' : null, head: .05 * Math.sin((t - S.t0) * TAU / (2 * BEAT)) }, .56);
}
function partEnd(c, t, S) {   // END (2 bars): FOLLOW FOR RULE #n+1, then the rubber stamp and the official logo
  bgDots(c, BLUE, .12, .55);
  stickerLogo(c, SCX, 420, 420, -.03, lerp(1.4, 1, easeIn(land(t, S.at(1)))));
  stampFit(c, 'FOLLOW FOR', BLK, 150, SCX, 660, -.04, .95, t, S.at(1), 840, 1.25);
  stampFit(c, `RULE #${EP.num + 1}`, BLUE, 190, SCX, 870, .03, 1, t, S.at(1, 1.5), 840, 1.25);
  const wv = Math.sin((t - S.at(1, 2)) * TAU / BEAT) * .25;
  jeffUp(c, t, S.at(1, 2), SCX, { armR: -2.4 + (t > S.at(1, 2.3) ? wv : 0), head: .04 * Math.sin((t - S.t0) * TAU / (2 * BEAT)) }, .66);
  const d = seg(t, S.at(2), STAMP_T); if (d > 0) screenSpace(c, () => rubberStamp(c, easeIn(d)));
}
SCENES.placeholder = (c, t, S) => {   // the template's stand-in scene (the RULE #2 dummy data uses it)
  bgDots(c, BLK, .04, .22, 18);
  c.save(); c.setLineDash([22, 16]); c.strokeStyle = BLK; c.lineWidth = 6; c.strokeRect(130, 620, 700, 700); c.restore();
};
function sceneBg(c) { bgDots(c, BLK, .04, .22, 18); }
function sceneSignoff(c, t) {
  paperBg(c);
  // the official logo: exact file, uniformly scaled, no texture or recolour, centred on the frame; held still
  const im = IMG.logo, [bx, by, bw, bh] = IMG.logoBox, lw = 720, lh = bh * lw / bw;
  c.drawImage(im, bx, by, bw, bh, CX - lw / 2, SCY - lh / 2, lw, lh);
  const lift = seg(t, STAMP_T, STAMP_T + .15);
  if (lift < 1) { c.save(); c.translate(0, -(H + 320) * easeIn(lift)); rubberStampFlat(c); c.restore(); }
}

// ================= assembly =================
const PARTS = { title: partTitle, rule: partRule, recap: partRecap, end: partEnd };
function drawSeg(c, t, S) {
  if (S.kind === 'scene') { const s = { ...S, lt: t - S.t0 }; SCENES[S.id](c, t, s); sceneCaptions(c, t, s); }
  else PARTS[S.kind](c, t, S);
}
function drawScene(c, t) {
  if (t >= STAMP_T) { resetT(c); sceneSignoff(c, t); return; }   // screen space; no print finish over the official logo
  const i = segAt(t), S = TL[i], u = i > 0 ? easeIO(seg(t, S.t0 - PUSH / 2, S.t0 + PUSH / 2)) : 1;
  if (u >= 1) { contentT(c); drawSeg(c, t, S); }
  else {   // the camera drops to the next segment: the old one rises out, the new one rises in
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
  TPL = await (await fetch('rules/template.json')).json();
  EP = await (await fetch(EP_PATH + '.json')).json();
  TL = buildTimeline(TPL, EP);
  const E = TL[TL.length - 1]; STAMP_T = E.at(2, 2); DUR = E.t1; NFR = Math.round(FPS * DUR); window.__NFR = NFR;
  window.__timeline = TL.map(s => ({ kind: s.kind, id: s.id || s.kind, b0: s.b0, bars: s.bars, t0: s.t0, t1: s.t1 }));
  frame(+(Q.get('frame') || 0));
  window.__ready = true;
})().catch(e => { console.error(e); window.__error = String(e); });
