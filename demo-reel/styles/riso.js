'use strict';
/* STYLE: RISOGRAPH (the personal-finance chapter).
   Three fluorescent inks only (hot pink, teal, sunny yellow) on white paper. Each ink is its own plate: shapes are drawn
   into the plate as coverage, the plate is punched with riso grain and speckle, then printed onto the paper with multiply
   a few pixels out of register. Overlaps mix like ink (pink over teal is purple to navy; teal over yellow is green;
   pink over yellow is orange). No outlines. Type is printed after the grain, pink over teal, so letters stay solid.
   Motion is bouncy. */
const RISO = { paper: '#FAF8F3', pink: '#FF48B0', teal: '#00A5B5', yellow: '#FFE800' };
const RISO_INKS = ['yellow', 'teal', 'pink'];
const RISO_MIS = { yellow: [1, -2], teal: [-3, 2], pink: [3, 1] };   // misregistration, output px

// the grain: an alpha field punched out of every plate (soft mottle + clumps + speckle), made once, larger than the frame
const RGRAIN = (() => {
  const w = 1160, h = 2000, o = document.createElement('canvas'); o.width = w; o.height = h; const g = o.getContext('2d'), d = g.createImageData(w, h), r = rng(777);
  const grid = (gw, gh) => { const G = new Float32Array((gw + 2) * (gh + 2)).map(() => r()); return (x, y) => { const gx = x / w * gw, gy = y / h * gh, i = gx | 0, j = gy | 0, fx = gx - i, fy = gy - j, sx = fx * fx * (3 - 2 * fx), sy = fy * fy * (3 - 2 * fy), q = (a, b) => G[b * (gw + 2) + a];
    return (q(i, j) * (1 - sx) + q(i + 1, j) * sx) * (1 - sy) + (q(i, j + 1) * (1 - sx) + q(i + 1, j + 1) * sx) * sy; }; };
  const big = grid(36, 62), mid = grid(190, 330);
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { const v = .5 * big(x, y) + .5 * mid(x, y), m = Math.max(0, Math.min(1, (v - .5) / .3)) * .42, u = r();
    const a = u < .075 ? .8 + r() * .2 : u < .2 ? .25 + r() * .2 : 0; d.data[(y * w + x) * 4 + 3] = Math.min(1, m + a) * 255; }
  g.putImageData(d, 0, 0); return o;
})();

// plates: one canvas per ink, the same pixel size as the target; draw into them with the target's transform
function makePlates(w, h) { const P = {}; for (const k of RISO_INKS) { const o = document.createElement('canvas'); o.width = w; o.height = h; P[k] = o; } return P; }
function platesFor(L) { return makePlates(L.width, L.height); }
function clearPlates(P) { for (const k of RISO_INKS) { const g = P[k].getContext('2d'); g.setTransform(1, 0, 0, 1, 0, 0); g.globalCompositeOperation = 'source-over'; g.globalAlpha = 1; g.clearRect(0, 0, P[k].width, P[k].height); } }
function plateCtx(P, ink, setT) { const g = P[ink].getContext('2d'); if (setT) setT(g); return g; }
// fill a shape into one plate at a coverage (0..1); knock = true removes ink instead (paper shows)
function rfill(P, ink, shape, cov = 1, setT = null, knock = false) {
  const g = plateCtx(P, ink, setT); g.save(); if (knock) g.globalCompositeOperation = 'destination-out'; g.fillStyle = knock ? '#000' : alpha(RISO[ink], cov);
  g.fill(shape instanceof Path2D ? shape : polyPath(shape)); g.restore(); }
function rstroke(P, ink, pts, w, cov = 1, setT = null) { const g = plateCtx(P, ink, setT); g.save(); g.strokeStyle = alpha(RISO[ink], cov); g.lineWidth = w; g.lineCap = 'round'; g.lineJoin = 'round';
  g.beginPath(); pts.forEach((q, i) => i ? g.lineTo(q[0], q[1]) : g.moveTo(q[0], q[1])); g.stroke(); g.restore(); }
// print: punch the grain out of each plate, then multiply it onto dst out of register. mis scales the offsets.
function risoPrint(dst, P, o = {}) { const { grainOff = [0, 0], mis = 1, rect = null } = o;
  const g = dst.getContext ? dst.getContext('2d') : dst;
  for (const k of RISO_INKS) { const p = P[k], pg = p.getContext('2d'), [gx, gy] = [grainOff[0] + (k === 'teal' ? 37 : k === 'pink' ? 71 : 0), grainOff[1] + (k === 'teal' ? 53 : k === 'pink' ? 19 : 0)];
    pg.save(); pg.setTransform(1, 0, 0, 1, 0, 0); pg.globalCompositeOperation = 'destination-out'; pg.drawImage(RGRAIN, -gx, -gy); pg.restore();
    g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.globalCompositeOperation = 'multiply'; const [dx, dy] = RISO_MIS[k]; g.drawImage(p, Math.round(dx * mis), Math.round(dy * mis)); g.restore(); }
}
// paper: warm white with a faint tooth (full frame, drawn once)
function risoPaper(L, seed = 9) { const g = L.getContext('2d'); resetT(g); g.fillStyle = RISO.paper; g.fillRect(0, 0, W, H);
  grain(g, rectPath(0, 0, W, H), [0, 0, W, H], 5000, '#B9B2A4', .12, seed, 1.2); grain(g, rectPath(0, 0, W, H), [0, 0, W, H], 900, '#FFFFFF', .7, seed + 1, 2); }
// type: pink printed over teal, both solid (after the grain), a hair out of register. The overlap is deep navy.
function risoType(c, s, x, y, weight, size, family, maxW = 9999, align = 'center', mis = 2.2) {
  const sz = fitFont(c, s, weight, size, family, maxW); c.save(); c.font = `${weight} ${sz}px ${family}`; c.textAlign = align; c.textBaseline = 'middle'; c.globalCompositeOperation = 'multiply';
  c.fillStyle = RISO.teal; c.fillText(s, x - mis, y + mis * .3); c.fillStyle = RISO.pink; c.fillText(s, x + mis, y - mis * .3); c.restore(); return sz; }

// ---------------- YOU (the hand), in riso: skin is yellow under pink; the sleeve teal, the cuff yellow ----------------
// Overlapping parts don't overprint: each part knocks out what's under it with a hairline paper gap, then prints.
function rknock(P, inks, shape, gap = 0, setT = null, gapLine = null) { const path = shape instanceof Path2D ? shape : polyPath(shape), gl = gapLine ? polyPath(gapLine, false) : path;
  for (const k of inks) { const g = plateCtx(P, k, setT); g.save(); g.globalCompositeOperation = 'destination-out'; g.fillStyle = '#000'; g.fill(path); if (gap) { g.strokeStyle = '#000'; g.lineWidth = gap; g.lineJoin = 'round'; g.lineCap = 'round'; g.stroke(gl); } g.restore(); } }
function risoHand(P, p, part = 'back', setT = null) {
  const G = HAND.geo(p.grip ?? 1), T = q => HAND.T(q, p), s = p.s || 1, ALL = RISO_INKS;
  const skin = (shape, shadeShape, gap = 4.5 * s, gapLine = null) => { rknock(P, ALL, shape, gap, setT, gapLine); rfill(P, 'yellow', shape, .6, setT); rfill(P, 'pink', shape, .42, setT);
    if (shadeShape) { const g = plateCtx(P, 'pink', setT); g.save(); g.clip(polyPath(shape)); g.fillStyle = alpha(RISO.pink, .3); g.fill(polyPath(shadeShape)); g.restore(); } };
  const rightOf = sp => [...sp.map(([x, y]) => [x + 3, y]), ...sp.slice().reverse().map(([x, y]) => [x + 60, y])];
  if (part === 'back') {
    skin(T(G.forearm), T(G.shadeArm), 0); G.fingers.forEach((f, i) => skin(T(f), T(rightOf(G.fingerSpines[i])))); skin(T(G.back), T(G.shadeBack));
    G.knuckles.forEach(k => rstroke(P, 'pink', T(k), 3.5 * s, .75, setT));
    G.fingerSpines.forEach(sp => [.42, .7].forEach(u => { const [x, y] = sp[Math.round(u * (sp.length - 1))]; rstroke(P, 'pink', T([[x - 8, y + 1], [x, y - 2], [x + 8, y + 1]]), 2.6 * s, .7, setT); }));
    rknock(P, ALL, T(G.sleeve), 0, setT); rfill(P, 'teal', T(G.sleeve), 1, setT);
    rknock(P, ALL, T(G.cuff), 0, setT); rfill(P, 'yellow', T(G.cuff), 1, setT);
    const [bx, by] = T([HAND.al(262, -46)])[0]; rfill(P, 'pink', circPath(bx, by, 8 * s), 1, setT);
  } else {
    skin(T(G.thumb), T(G.thumbShade), 4.5 * s, T(G.thumbOpen)); rknock(P, ['pink'], T(G.nail), 0, setT);
    const sp = G.thumbSpine, [x, y] = sp[Math.round(sp.length * .55)]; rstroke(P, 'pink', T([[x - 11, y + 4], [x - 2, y - 1], [x + 9, y + 3]]), 2.6 * s, .7, setT);
  }
}

// ---------------- the paycheck, in riso (panels of the letter sheet, 520 x 226.7 as seen) ----------------
// a small riso print of its own: paper, plates, grain, multiply. Faces are drawn once, at res px per unit.
function risoFace(w, h, res, draw, seed) {
  const o = document.createElement('canvas'); o.width = Math.round(w * res); o.height = Math.round(h * res); const g = o.getContext('2d');
  g.fillStyle = RISO.paper; g.fillRect(0, 0, o.width, o.height); g.save(); g.scale(res, res); grain(g, rectPath(0, 0, w, h), [0, 0, w, h], w * h / 40, '#B9B2A4', .12, seed, 1.1); g.restore();
  const P = makePlates(o.width, o.height), setT = q => q.setTransform(res, 0, 0, res, 0, 0); draw(P, setT);
  risoPrint(g, P, { grainOff: [seed * 13 % 300, seed * 29 % 600], mis: res * .9 }); return o;
}
function guilloche(P, w, h, setT, cov = .45) { for (let k = 0; k < 4; k++) { const pts = []; for (let x = 0; x <= w; x += 4) pts.push([x, h * (.2 + k * .2) + Math.sin(x / 26 + k * 1.3) * 10 + Math.sin(x / 9 + k) * 3]); rstroke(P, 'teal', pts, 2, cov, setT); } }
function paycheckRiso(P, setT) { const { w, ph } = SHEET;
  rfill(P, 'teal', [[0, 0], [w, 0], [w, ph], [0, ph]], .16, setT); guilloche(P, w, ph, setT, .35);
  const fr = new Path2D(); fr.rect(10, 10, w - 20, ph - 20); fr.rect(17, 17, w - 34, ph - 34); { const g = plateCtx(P, 'pink', setT); g.save(); g.fillStyle = RISO.pink; g.fill(fr, 'evenodd'); g.restore(); }
  rfill(P, 'pink', circPath(104, ph / 2 + 4, 60), 1, setT); rfill(P, 'teal', circPath(104, ph / 2 + 4, 60), 1, setT, true); rfill(P, 'yellow', circPath(104, ph / 2 + 4, 44), .9, setT);
  for (const ink of RISO_INKS) { const g = plateCtx(P, ink, setT); g.save(); g.globalCompositeOperation = 'destination-out'; g.font = '400 84px ArchivoBlack'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText('$', 104, ph / 2 + 8); g.restore(); }
  rfill(P, 'teal', [[200, 76], [470, 76], [470, 82], [200, 82]], 1, setT); rfill(P, 'teal', [[200, 112], [352, 112], [352, 118], [200, 118]], 1, setT);
  rfill(P, 'yellow', roundRectPath(372, 96, 98, 40, 8), 1, setT); rfill(P, 'teal', roundRectPath(372, 96, 98, 40, 8), 1, setT, true); rfill(P, 'pink', roundRectPath(380, 104, 82, 24, 5), .55, setT);
  const sig = smooth([[244, 182], [262, 158], [276, 176], [296, 152], [306, 184], [334, 166], [372, 176], [440, 170]], false, 6); rstroke(P, 'pink', sig, 3.4, 1, setT);
  for (let k = 0; k < 11; k++) rfill(P, 'teal', [[34 + k * 16, 190], [44 + k * 16, 190], [44 + k * 16, 202], [34 + k * 16, 202]], .9, setT);
}
function checkInsideRiso(P, setT) { const { w, ph } = SHEET; rfill(P, 'teal', [[0, 0], [w, 0], [w, ph], [0, ph]], .16, setT); guilloche(P, w, ph, setT, .3);
  rfill(P, 'pink', [[0, ph - 20], [w, ph - 20], [w, ph], [0, ph]], .35, setT); }
function letterFrontRiso(P, setT) { const { w, h, ph } = SHEET;
  rfill(P, 'pink', circPath(w / 2, 66, 26), 1, setT); rfill(P, 'yellow', circPath(w / 2 + 4, 62, 14), 1, setT);
  rfill(P, 'teal', [[70, 118], [450, 118], [450, 124], [70, 124]], 1, setT); rfill(P, 'pink', [[70, 128], [450, 128], [450, 131], [70, 131]], 1, setT);
  const bar = (x0, x1, y, ink = 'teal', cov = .75) => rfill(P, ink, roundRectPath(x0, y - 4, x1 - x0, 8, 4), cov, setT);
  bar(70, 250, 166); bar(70, 200, 192); bar(330, 450, 166);
  rfill(P, 'pink', roundRectPath(108, 424, 306, 10, 5), 1, setT);
  for (let k = 0; k < 4; k++) bar(70, [450, 440, 452, 300][k], 492 + k * 27);
  bar(70, 170, 606); rstroke(P, 'pink', smooth([[82, 648], [110, 616], [124, 640], [150, 606], [160, 650], [196, 624], [240, 640], [262, 628]], false, 5), 3.4, 1, setT);
  rfill(P, 'yellow', [[0, h - 16], [w, h - 16], [w, h], [0, h]], .8, setT);
}
