'use strict';
/* STYLE: STICKER CARTOON (the travel chapter).
   Bold clean shapes, thick even black outlines, tangerine, electric blue and lime with simple one-tone cel shading,
   and a thick white die-cut border around every character and prop, with a subtle drop shadow. Snappy
   squash-and-stretch. Type: a rounded bold. Props are drawn once into their own canvas, die-cut (the border is the
   silhouette grown outward), and then moved around as stickers. */
const STK = { bg: '#E6E6E6', ink: '#141414', orange: '#FF7A1A', blue: '#1E6BFF', lime: '#8BD400', white: '#FFFFFF',
  orangeSh: '#D8600C', blueSh: '#1550D0', limeSh: '#6BA800', skin: '#EC9140', skinSh: '#C9712C', bgSh: '#D2D2D2' };
const OUTLINE = 6;

// a sticker: draw(g) paints the art (with its black outlines) into a canvas of w x h units at res px/unit. The white
// border is the art's silhouette grown by `border`; the shadow is that silhouette, offset and soft.
function makeSticker(w, h, draw, o = {}) {
  const { res = 1.2, border = 14, pad = 30 } = o, W0 = Math.ceil((w + 2 * pad) * res), H0 = Math.ceil((h + 2 * pad) * res);
  const art = document.createElement('canvas'); art.width = W0; art.height = H0; const g = art.getContext('2d'); g.scale(res, res); g.translate(pad, pad); draw(g);
  const sil = document.createElement('canvas'); sil.width = W0; sil.height = H0; const s = sil.getContext('2d');
  const n = 28, R = border * res; for (let k = 0; k < n; k++) { const a = k / n * TAU; s.drawImage(art, Math.cos(a) * R, Math.sin(a) * R); }
  for (let k = 0; k < n; k++) { const a = k / n * TAU; s.drawImage(art, Math.cos(a) * R * .5, Math.sin(a) * R * .5); }
  s.globalCompositeOperation = 'source-in'; s.fillStyle = '#fff'; s.fillRect(0, 0, W0, H0);
  const out = document.createElement('canvas'); out.width = W0; out.height = H0; const q = out.getContext('2d');
  q.drawImage(sil, 0, 0); q.drawImage(art, 0, 0);
  const sh = document.createElement('canvas'); sh.width = W0; sh.height = H0; const t = sh.getContext('2d'); t.filter = `blur(${3 * res}px)`; t.drawImage(sil, 0, 0); t.filter = 'none';
  t.globalCompositeOperation = 'source-in'; t.fillStyle = 'rgba(0,0,0,.2)'; t.fillRect(0, 0, W0, H0);
  return { img: out, shadow: sh, w, h, pad, res };
}
// place a sticker: (x, y) is where the art's (ax, ay) goes; sx/sy squash about that point
function putSticker(c, S, x, y, o = {}) { const { ax = S.w / 2, ay = S.h / 2, s = 1, sx = 1, sy = 1, rot = 0, lift = 1, al = 1 } = o;
  c.save(); c.globalAlpha = al; c.translate(x, y); c.rotate(rot); c.scale(s * sx, s * sy); const k = 1 / S.res, ox = -(ax + S.pad), oy = -(ay + S.pad);
  c.drawImage(S.shadow, ox + 5 * lift, oy + 8 * lift, S.img.width * k, S.img.height * k); c.drawImage(S.img, ox, oy, S.img.width * k, S.img.height * k); c.restore(); }
// a shape with a black outline and a one-tone cel shade (shade: a second path clipped inside, in the darker tone)
function stkShape(g, path, fill, shadeFill = null, shadePath = null, lw = OUTLINE) {
  g.fillStyle = fill; g.fill(path); if (shadeFill && shadePath) { g.save(); g.clip(path); g.fillStyle = shadeFill; g.fill(shadePath); g.restore(); }
  g.strokeStyle = STK.ink; g.lineWidth = lw; g.lineJoin = 'round'; g.lineCap = 'round'; g.stroke(path); }
function stkType(g, s, x, y, size, col = STK.ink, maxW = 9999, weight = 700) { return textAt(g, s, x, y, weight, size, 'Fredoka', col, maxW); }
// the world: a pale sticker sheet, a lime ground, a tangerine sun (full frame, drawn once)
function stkPaper(L) { const g = L.getContext('2d'); resetT(g); g.fillStyle = STK.bg; g.fillRect(0, 0, W, H);
  designT(g); const sun = circPath(640, 560, 118); g.fillStyle = STK.orange; g.fill(sun); g.save(); g.clip(sun); g.fillStyle = STK.orangeSh; g.fill(circPath(672, 592, 118)); g.restore(); g.strokeStyle = STK.ink; g.lineWidth = OUTLINE; g.stroke(sun);
  for (const [x, y, k] of [[250, 520, 1], [860, 460, .8]]) { const cl = new Path2D(); cl.arc(x, y, 34 * k, Math.PI, 0); cl.arc(x + 44 * k, y - 8 * k, 42 * k, Math.PI, 0); cl.arc(x + 90 * k, y, 30 * k, Math.PI, 0); cl.closePath(); stkShape(g, cl, STK.white, STK.bgSh, rectPath(x - 40, y - 12 * k, 200, 30)); }
  const gr = new Path2D(); gr.moveTo(-600, 1090); gr.bezierCurveTo(200, 1040, 700, 1060, 1500, 1080); gr.lineTo(1500, 2400); gr.lineTo(-600, 2400); gr.closePath();
  stkShape(g, gr, STK.lime, STK.limeSh, rectPath(-600, 1160, 2100, 1300)); }

// ---------------- YOU (the hand), as a sticker ----------------
// back (forearm, sleeve, palm, fingers) and the thumb are two stickers, so a prop can sit between them
function stkHandArt(part) { const G = HAND.geo(1), pts = q => polyPath(q);
  return g => { g.translate(120, 150);
    if (part === 'back') {
      stkShape(g, pts(G.forearm), STK.skin, STK.skinSh, pts(G.shadeArm)); G.fingers.forEach(f => stkShape(g, pts(f), STK.skin, STK.skinSh, pts([[30, -140], [80, -140], [80, 30], [30, 30]])));
      stkShape(g, pts(G.back), STK.skin, STK.skinSh, pts(G.shadeBack)); g.strokeStyle = STK.ink; g.lineWidth = 3.5; G.knuckles.forEach(k => { g.beginPath(); k.forEach((q, i) => i ? g.lineTo(...q) : g.moveTo(...q)); g.stroke(); });
      stkShape(g, pts(G.sleeve), STK.blue, STK.blueSh, pts(G.shadeArm.map(([x, y]) => [x + 10, y]))); stkShape(g, pts(G.cuff), STK.lime, STK.limeSh, pts([HAND.al(236, 20), HAND.al(290, 20), HAND.al(290, 80), HAND.al(236, 80)]));
    } else { const th = pts(G.thumb); g.fillStyle = STK.skin; g.fill(th); g.save(); g.clip(th); g.fillStyle = STK.skinSh; g.fill(pts(G.thumbShade)); g.restore();
      g.strokeStyle = STK.ink; g.lineWidth = OUTLINE; g.lineJoin = 'round'; g.lineCap = 'round'; g.beginPath(); G.thumbOpen.forEach((q, i) => i ? g.lineTo(...q) : g.moveTo(...q)); g.stroke();
      g.fillStyle = '#F6C08C'; g.fill(pts(G.nail)); g.lineWidth = 3; g.stroke(pts(G.nail)); } }; }
const STK_HAND = {};
function stkHandInit() { STK_HAND.back = makeSticker(760, 1120, stkHandArt('back'), { border: 12 }); STK_HAND.thumb = makeSticker(760, 1120, stkHandArt('thumb'), { border: 0 }); }
function stkHand(c, p, part = 'back') { const S = STK_HAND[part]; c.save(); c.translate(p.x, p.y); c.rotate(p.rot || 0); c.scale(p.s || 1, p.s || 1);
  const k = 1 / S.res; if (part === 'back') c.drawImage(S.shadow, -120 - S.pad + 5, -150 - S.pad + 8, S.img.width * k, S.img.height * k); c.drawImage(S.img, -120 - S.pad, -150 - S.pad, S.img.width * k, S.img.height * k); c.restore(); }
