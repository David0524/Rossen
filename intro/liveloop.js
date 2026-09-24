'use strict';
/* LIVE TODAY loops: the approved LIVE TODAY card as a seamless 5 s loop (2 bars at 96 BPM) for Reels and Stories.
   Same card as the promo's end frame, scaled up to fill the safe area. Every motion is periodic in the loop length,
   so the last frame flows straight back into the first. A page sets window.SHOW = { time, day } (default 5PM ET, WEDNESDAY), and optionally
   extra: a yellow chip under the day (e.g. 'LIVE ON YOUTUBE'); Jeff then stands a little lower. Without it the loop is unchanged.
   beat 1 and 3: LIVE TODAY and the time card pulse; beats 2 and 4: the day chip; once a bar: a signal ring behind the
   card; Jeff waves on every beat; the logo sticker rocks once per loop. */
const SHOW = Object.assign({ time: '5PM ET', day: 'WEDNESDAY' }, window.SHOW || {});
const DUR = at(2), NFR = Math.round(FPS * DUR);
const TAU_L = TAU / DUR;                                     // one full cycle per loop
const beatPh = t => ((t % BEAT) + BEAT) % BEAT / BEAT;       // 0..1 inside each beat
const kick = (t, every = 1, off = 0) => { const n = Math.floor(t / BEAT); return ((n - off) % every === 0) ? Math.pow(Math.max(0, Math.cos(beatPh(t) * Math.PI * .5)), 3) : 0; };   // 1 on the beat, 0 before the next one

// the airtime card is always the size of the approved 5PM ET card; a longer time gets a smaller font inside it
function timeCard() {
  const ref = stampImg('5PM ET', BLUE, 170);
  if (SHOW.time === '5PM ET') return ref;
  const H0 = 170 * 1.12 + 26 * 2, W0 = ref.width - 52, m = document.createElement('canvas').getContext('2d'); m.font = '170px Stamp';
  const tw = m.measureText(SHOW.time).width, maxTw = W0 - 2 * 34, size = tw > maxTw ? Math.floor(170 * maxTw / tw) : 170, tw2 = tw * size / 170;
  return wordStamp(SHOW.time, { color: BLUE, style: 'fill', size, padX: (W0 - tw2) / 2, padY: (H0 - size * 1.12) / 2, seed: SHOW.time.length * 7 });
}
function solidStamp(c, img, x, y, rot, sc) {   // a landed stamp (opaque, black drop shadow), no landing motion
  c.save(); c.translate(x, y); c.rotate(rot); c.scale(sc, sc);
  c.save(); c.filter = 'brightness(0)'; c.globalAlpha = .55; c.drawImage(img, -img.width / 2 + 12, -img.height / 2 + 14); c.restore();
  c.drawImage(img, -img.width / 2, -img.height / 2); c.restore();
}
const fitK = (img, rot, maxW) => maxW / (img.width * Math.abs(Math.cos(rot)) + img.height * Math.abs(Math.sin(rot)));
function ring(c, x, y, t) {   // a yellow signal ring once a bar, behind the card
  const u = ((t % BAR) + BAR) % BAR / BAR; if (u > .7) return; const e = u / .7;
  c.save(); c.globalAlpha = .9 * (1 - e); c.strokeStyle = YEL; c.lineWidth = 18; c.beginPath(); c.ellipse(x, y, 300 + 260 * e, 170 + 150 * e, 0, 0, TAU); c.stroke(); c.restore();
}
function scene(c, t) {
  bgDots(c, BLUE, .12, .55);
  ring(c, SCX, 900, t);
  // the logo sticker, rocking gently once per loop
  stickerLogo(c, SCX, 470, 610, -.03 + .025 * Math.sin(t * TAU_L), 1 + .015 * Math.sin(t * TAU_L * 2));
  // LIVE TODAY and the time card pulse on beats 1 and 3; the day chip on 2 and 4
  const p13 = kick(t, 2, 0), p24 = kick(t, 2, 1);
  const live = stampImg('LIVE TODAY', BLK, 150), card = timeCard();
  solidStamp(c, live, SCX, 800, -.04, fitK(live, -.04, 840) * (1 + .045 * p13));
  solidStamp(c, card, SCX, 1015, .03, fitK(stampImg('5PM ET', BLUE, 170), .03, 840) * (1 + .045 * p13));   // the 5PM card's size, for every airtime
  c.save(); c.translate(SCX, 1190); c.rotate(-.015); c.scale(1 + .06 * p24, 1 + .06 * p24);
  c.font = '72px Stamp'; const w = c.measureText(SHOW.day).width + 70;
  c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fillRect(-w / 2 + 9, -52, w, 108); c.restore(); ink(c, rect(-w / 2, -56, w, 108), BLK, 5601, { amp: 3 });
  inkText(c, SHOW.day, 0, 4, 72, 'Stamp', CHIP, 780); c.restore();
  if (SHOW.extra) {   // the extra chip pulses with the day chip, on 2 and 4
    c.save(); c.translate(SCX, 1310); c.rotate(.012); c.scale(1 + .06 * p24, 1 + .06 * p24);
    c.font = '64px Stamp'; const w2 = Math.min(c.measureText(SHOW.extra).width, 700) + 70;
    c.save(); c.globalAlpha = .3; c.fillStyle = BLK; c.fillRect(-w2 / 2 + 9, -46, w2, 96); c.restore(); block(c, rect(-w2 / 2, -50, w2, 96), YEL, 5602, { kw: 5 });
    inkText(c, SHOW.extra, 0, 4, 64, 'Stamp', BLK, 700); c.restore();
  }
  // Jeff waves on every beat
  const wave = Math.sin(t * TAU / BEAT) * .22;
  jeff(c, SCX, SHOW.extra ? 2050 : 1930, .78, { armR: -2.35 + wave, head: .05 * Math.sin(t * TAU_L * 2), bob: Math.abs(Math.sin(t * Math.PI / BEAT)) * 8 });
}
function drawScene(c, t) { contentT(c); scene(c, t); printFinish(c); if (SHOW_SAFE) safeOverlay(c); }

// ================= runtime =================
const CV = document.getElementById('c'); CV.width = OUT_W; CV.height = OUT_H; const CTX = CV.getContext('2d');
function frame(i) { const t = (i % NFR) / FPS; FILM_T = t; resetT(CTX); CTX.globalAlpha = 1; drawScene(CTX, t); resetT(CTX); }
window.__NFR = NFR; window.__FPS = FPS; window.__frame = i => { frame(i); return CV.toDataURL('image/png'); };
(async () => {
  await loadPrintKit(); await loadVertKit();
  frame(+(Q.get('frame') || 0));
  window.__ready = true;
})().catch(e => { console.error(e); window.__error = String(e); });
