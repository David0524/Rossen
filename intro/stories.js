'use strict';
/* Rossen Reports: "STILL LIVE" deals as Instagram / Facebook Story frames, 1080x1920, 24 fps. One slide per deal, then a
   "tune in" page. Everything comes from deals/deals.json, and the deal cards reuse the Reel's own drawing (deals.js, loaded
   as a library): the pinned photo print, the name chips, the struck regular price, the DEAL tag and the percent sticker.

   Each slide is a 5 s loop (8 beats at 96 BPM). The animation is deliberately minimal: the product photo and all type are
   completely still from frame 0 (so frame 0 is the finished still); only the arrow nudges toward the link-sticker outline
   on every beat and Jeff bobs, both on twos. Every motion repeats exactly every beat or every 5 s, so the slide loops cleanly.

   Stories layout (not the Reel's): the top 250 px (progress bar, profile) and the bottom 240 px (reply bar) stay clear of
   anything that matters; the sides keep 64 px. The deal card is the Reel's layout at full size (no K shrink).
     card        the Reel's deal layout, y 270-1340
     fine print  one small line under the tag: the affiliate disclosure
     link slot   a dashed outline where the link sticker goes (added in the app), with the arrow pointing into it
     Jeff        bottom right, pointing at the slot (deal slides) / thumbs up (last page) */
window.DEALS_LIB = true;
const SLIDE_S = 5, SLIDE_F = SLIDE_S * FPS;
const SAFE_ST = { x0: 64, x1: 1016, y0: 250, y1: 1680 };
const CARD_DX = 60, CARD_DY = -56;   // the Reel's content coordinates -> this slide
function cardT(g) { resetT(g); g.translate(CARD_DX, CARD_DY); }
const SLOT = { x: 110, y: 1452, w: 620, h: 140 };
const FINE_Y = 1374, FINE_SIZE = 22, FINE = `bold ${FINE_SIZE}px "Liberation Sans"`;

function finePrint(c, y = FINE_Y) {   // small and tucked away, but level and legible
  [up(DJ.disclosure)].forEach((s, i) => { c.font = FINE; const w = c.measureText(s).width, sz = w > 930 ? Math.floor(FINE_SIZE * 930 / w) : FINE_SIZE; text(c, s, CX, y + i * 30, `bold ${sz}px "Liberation Sans"`, BLK); });
}
function linkSlot(c) {   // the outline for the link sticker: dashed, empty inside, so the sticker sits in it
  const { x, y, w, h } = SLOT;
  c.save(); c.fillStyle = alpha(CHIP, .55); c.fill(polyPath(rrPts(x, y, w, h, h / 2, 8)));
  c.setLineDash([26, 16]); c.lineDashOffset = 0; c.strokeStyle = BLK; c.lineWidth = 6; c.lineJoin = 'round';
  c.stroke(polyPath(rrPts(x, y, w, h, h / 2, 8))); c.restore();
}
const beatU = t => { const tt = onTwos(t), ph = (tt % BEAT) / BEAT; return ph < .5 ? easeOut(ph * 2) : 1 - easeIO((ph - .5) * 2); };   // 0 -> 1 -> 0 each beat
function arrow(c, t) {   // a chunky yellow arrow, pointing left into the slot's right end, nudging in on every beat
  const tip = SLOT.x + SLOT.w + 30 - 16 * beatU(t), y = SLOT.y + 38;
  const P = [[tip, y], [tip + 64, y - 46], [tip + 64, y - 18], [tip + 190, y - 18], [tip + 190, y + 18], [tip + 64, y + 18], [tip + 64, y + 46]];
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fill(polyPath(P.map(([a, b]) => [a + 8, b + 10]))); c.restore();
  block(c, P, YEL, 9101, { kw: 6 });
}
function jeffStory(c, t, pose) {
  const tt = onTwos(t), bob = Math.abs(Math.sin(tt * Math.PI / BEAT)) * 4, head = .04 * Math.sin(tt * TAU / SLIDE_S);
  if (pose === 'point') jeff(c, 935, 2030, .56, { sx: -1, armR: -2.15, prop: 'point', head, bob });
  else jeff(c, CX, 2010, .7, { armR: -2.5, prop: 'thumb', head, bob });
}
function dealSlide(c, t, k) {
  creamBg(c);
  resetT(c); jeffStory(c, t, 'point');
  printFinish(c);   // the paper specks: board and puppet only; nothing below is textured
  const d = DEALS[k], L = 1e6;   // every card element fully landed: still from frame 0
  cardT(c); photoPrint(c, k, L, 0); headChips(c, d.name, L, 0); regChip(c, d, L, 0, true); priceTag(c, d, L, 0); sticker(c, d, L, 0);
  resetT(c); finePrint(c); linkSlot(c); arrow(c, t);
}
function endSlide(c, t) {
  creamBg(c);
  resetT(c); jeffStory(c, t, 'thumb');
  printFinish(c);
  const lg = IMG.logo, [bx, by, bw, bh] = IMG.logoBox, lw = 640, lh = bh * lw / bw, top = 290;   // the official logo, untouched
  c.drawImage(lg, bx, by, bw, bh, CX - lw / 2, top, lw, lh);
  const ls = DJ.storyEnd, y0 = top + lh + 110;
  ls.forEach((s, i) => fitText(c, up(s), CX, y0 + i * 100, 84, 'Stamp', i === 1 ? BLUE : BLK, 900));
  const y = y0 + ls.length * 100 + 40, ih = 64; c.font = '44px Stamp'; const tw = c.measureText('LIVE ON').width;
  const icons = DJ.storyPlatforms.map(k => { const im = IMG[k + '_icon']; return [im, im.width * ih / im.height]; });
  const total = tw + 26 + icons.reduce((q, [, iw]) => q + iw, 0) + 22 * (icons.length - 1); let x = CX - total / 2;
  text(c, 'LIVE ON', x, y + 3, '44px Stamp', BLK, 'left'); x += tw + 26;
  for (const [im, iw] of icons) { c.drawImage(im, x, y - ih / 2, iw, ih); x += iw + 22; }
  finePrint(c, y + 90);
}
function storySafe(c) { c.save(); resetT(c); c.globalAlpha = .18; c.fillStyle = '#ff00ff'; c.fillRect(0, 0, W, SAFE_ST.y0); c.fillRect(0, SAFE_ST.y1, W, H - SAFE_ST.y1);
  c.fillRect(0, 0, SAFE_ST.x0, H); c.fillRect(SAFE_ST.x1, 0, W - SAFE_ST.x1, H); c.restore(); }

// ================= runtime: all slides in one page, SLIDE_F frames each (the build splits them) =================
const CV = document.getElementById('c'); CV.width = OUT_W; CV.height = OUT_H; const CTX = CV.getContext('2d');
let NSLIDE = 1;
function frame(i) {
  const s = Math.min(NSLIDE - 1, Math.floor(i / SLIDE_F)), t = (i - s * SLIDE_F) / FPS; FILM_T = t;
  resetT(CTX); CTX.globalAlpha = 1;
  if (s < DEALS.length) dealSlide(CTX, t, s); else endSlide(CTX, t);
  if (SHOW_SAFE) storySafe(CTX); resetT(CTX);
}
window.__FPS = FPS; window.__frame = i => { frame(i); return CV.toDataURL('image/png'); };
(async () => {
  await loadPrintKit(); await loadVertKit(); makeCream(); await loadImg('facebook_icon', 'assets/social/facebook_icon.png');
  DJ = await (await fetch('deals/deals.json', { cache: 'no-store' })).json(); checkData(DJ); DEALS = DJ.deals;
  if (!Array.isArray(DJ.storyEnd) || !DJ.storyEnd.length) throw new Error('deals.json: storyEnd (the last page lines) missing');
  if (!Array.isArray(DJ.storyPlatforms)) throw new Error('deals.json: storyPlatforms missing');
  await Promise.all(DEALS.map((d, k) => loadImg('deal' + k, d.image)));
  DEALS.forEach((d, k) => { if (!IMG['deal' + k] || !IMG['deal' + k].width) throw new Error('missing image: ' + d.image); });
  NSLIDE = DEALS.length + 1; window.__NFR = NSLIDE * SLIDE_F;
  window.__info = { slides: NSLIDE, slideFrames: SLIDE_F, slot: SLOT };
  frame(+(Q.get('frame') || 0));
  window.__ready = true;
})().catch(e => { console.error(e); window.__error = String(e); });
