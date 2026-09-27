'use strict';
/* STYLE: GRAPHITE MINIMALISM (the productivity chapter).
   Soft pencil lines with varied weight, light graphite shading, bright white paper and lots of empty space. The only
   colour is soft sky blue. Pencil work is drawn into its own layer, then the paper's tooth is punched out of it so the
   graphite catches only the high points of the paper, and it is laid onto the page with multiply. The calmest motion in
   the reel: lines draw themselves on. Type: a clean light sans. */
const GRAPH = { paper: '#FDFDFB', lead: '#343434', lead2: '#6C6C6C', soft: '#A4A4A4', sky: '#6FA8DC' };

// the paper's tooth: a fine alpha field, punched out of the pencil layer (made once, larger than the frame)
const GTOOTH = (() => {
  const w = 1120, h = 1960, o = document.createElement('canvas'); o.width = w; o.height = h; const g = o.getContext('2d'), d = g.createImageData(w, h), r = rng(313);
  const G = new Float32Array(282 * 492).map(() => r()), vn = (x, y) => { const gx = x / 4, gy = y / 4, i = gx | 0, j = gy | 0, fx = gx - i, fy = gy - j, q = (a, b) => G[(b % 492) * 282 + (a % 282)];
    return (q(i, j) * (1 - fx) + q(i + 1, j) * fx) * (1 - fy) + (q(i, j + 1) * (1 - fx) + q(i + 1, j + 1) * fx) * fy; };
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { const v = .7 * vn(x, y) + .3 * r(); d.data[(y * w + x) * 4 + 3] = Math.max(0, Math.min(1, (v - .42) * 1.9)) * 170; }
  g.putImageData(d, 0, 0); return o;
})();
// the page: bright white, a whisper of tooth (full frame, drawn once)
function graphPaper(L, seed = 21) { const g = L.getContext('2d'); resetT(g); g.fillStyle = GRAPH.paper; g.fillRect(0, 0, W, H);
  grain(g, rectPath(0, 0, W, H), [0, 0, W, H], 2600, '#C9C9C6', .1, seed, 1.1); }
// pencil: several light passes along a path, each a little off the last, the weight swelling and fading with pressure.
// progress (0..1) draws only the first part of the line: lines draw themselves on.
function pencil(c, pts, w, seed, o = {}) {
  const { col = GRAPH.lead, passes = 3, al = .55, progress = 1, jit = .9, press = .45 } = o;
  let P = resample(pts, 3); if (progress < 1) { const n = Math.max(2, Math.round(P.length * progress)); if (progress <= 0) return; P = P.slice(0, n); }
  const r = rng(seed); c.save(); c.strokeStyle = col; c.lineCap = 'round'; c.lineJoin = 'round';
  for (let k = 0; k < passes; k++) { const ph = r() * TAU, dx = (r() - .5) * jit, dy = (r() - .5) * jit;
    for (let i = 1; i < P.length; i++) { const t = i / (P.length - 1), taper = Math.min(1, t * 6, (1 - t) * 5 + .15);
      c.globalAlpha = al * (.55 + .45 * taper) * (k ? .7 : 1); c.lineWidth = Math.max(.4, w * (1 - press / 2 + press * Math.sin(ph + i * .09) / 2) * (.5 + .5 * taper) * (k ? .7 : 1));
      c.beginPath(); c.moveTo(P[i - 1][0] + dx, P[i - 1][1] + dy); c.lineTo(P[i][0] + dx, P[i][1] + dy); c.stroke(); } }
  c.restore();
}
function pencilLoop(c, pts, w, seed, o = {}) { pencil(c, [...pts, pts[0], pts[1]], w, seed, o); }
// light graphite shading: fine parallel strokes plus a soft smudge, clipped to a shape
function graphShade(c, pts, o = {}) { const { angle = .75, gap = 5, al = .22, seed = 1, smudge = .08 } = o; const p = polyPath(pts), bb = bbox(pts);
  c.save(); c.fillStyle = alpha(GRAPH.soft, smudge); c.fill(p); c.restore();
  hatch(c, p, bb, { angle, gap, len: 26, jitter: 4, color: GRAPH.lead2, alpha: al, width: .9, seed }); }
// lay a pencil layer onto the page: punch the tooth out of it, then multiply it down
function graphLay(dst, L, o = {}) { const { tooth = .85, off = [0, 0] } = o; const g = L.getContext('2d');
  g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.globalCompositeOperation = 'destination-out'; g.globalAlpha = tooth; g.drawImage(GTOOTH, -off[0], -off[1]); g.restore();
  dst.save(); dst.setTransform(1, 0, 0, 1, 0, 0); dst.globalCompositeOperation = 'multiply'; dst.drawImage(L, 0, 0); dst.restore(); }
// type: a clean light sans in soft graphite, solid (type is laid after the tooth, so letters stay clean)
function graphType(c, s, x, y, weight, size, maxW = 9999, col = GRAPH.lead, align = 'center') { return textAt(c, s, x, y, weight, size, 'Inter', col, maxW, align); }
// the torn edge of a sheet: a ragged line with a few paper fibres pulled out of it
function tornLine(x0, x1, y, seed, amp = 7) { const r = rng(seed), pts = []; for (let x = x0; x <= x1 + .1; x += 7 + r() * 6) pts.push([x, y + (r() - .5) * amp * 2 + Math.sin(x / 23 + seed) * amp * .5]); return pts; }
function fibres(c, pts, seed, n = 26) { const r = rng(seed); c.save(); c.strokeStyle = alpha(GRAPH.soft, .6); c.lineWidth = .7;
  for (let k = 0; k < n; k++) { const [x, y] = pts[Math.floor(r() * pts.length)], a = -Math.PI / 2 + (r() - .5) * 1.4, l = 3 + r() * 9; c.beginPath(); c.moveTo(x, y); c.quadraticCurveTo(x + Math.cos(a) * l * .5 + (r() - .5) * 3, y + Math.sin(a) * l * .5, x + Math.cos(a) * l, y + Math.sin(a) * l); c.stroke(); } c.restore(); }

// ---------------- YOU (the hand), in pencil, holding a sky-blue pencil ----------------
const GPENCIL = { tail: [70, 70], tip: [-150, -168] };   // hand-local: the pencil runs from behind the palm to its tip
function graphHand(c, p, part = 'back') {
  const G = HAND.geo(p.grip ?? 1), T = q => HAND.T(q, p), s = p.s || 1, sw = 2.6 * s;
  if (part === 'back') {
    const fa = T(G.forearm), h = G.forearm.length / 2; c.save(); c.fillStyle = GRAPH.paper; c.fill(polyPath(fa)); c.restore(); graphShade(c, T(G.shadeArm), { seed: 61, al: .16 });
    pencil(c, T(G.forearm.slice(0, h)), sw, 62); pencil(c, T(G.forearm.slice(h)), sw, 63);
    G.fingers.forEach((f, i) => { const q = T(f); c.save(); c.fillStyle = GRAPH.paper; c.fill(polyPath(q)); c.restore(); pencilLoop(c, q, sw * .8, 64 + i); });
    const bk = T(G.back); c.save(); c.fillStyle = GRAPH.paper; c.fill(polyPath(bk)); c.clip(polyPath(bk)); graphShade(c, T(G.shadeBack), { seed: 70, al: .2 }); c.restore(); pencilLoop(c, bk, sw, 71);
    G.knuckles.forEach((k, i) => pencil(c, T(k), sw * .6, 72 + i, { al: .45 }));
    const sl = T(G.sleeve), cf = T(G.cuff); c.save(); c.fillStyle = GRAPH.paper; c.fill(polyPath(sl)); c.restore(); graphShade(c, T(G.shadeArm.map(([x, y]) => [x + 10, y])), { seed: 76, al: .2 });
    pencil(c, [sl[0], sl[1]], sw, 77); pencil(c, [sl[3], sl[2]], sw, 78); c.save(); c.fillStyle = GRAPH.paper; c.fill(polyPath(cf)); c.restore(); pencilLoop(c, cf, sw, 79);
  } else if (part === 'prop') {   // the pencil: sky blue body, a shaved wood cone, a graphite point
    const [a, b] = T([GPENCIL.tail, GPENCIL.tip]), ang = Math.atan2(b[1] - a[1], b[0] - a[0]), L = Math.hypot(b[0] - a[0], b[1] - a[1]), wv = 13 * s;
    c.save(); c.translate(a[0], a[1]); c.rotate(ang);
    c.fillStyle = GRAPH.sky; c.fillRect(0, -wv, L - 44 * s, wv * 2); c.fillStyle = alpha(GRAPH.lead, .12); c.fillRect(0, wv * .25, L - 44 * s, wv * .75);
    c.fillStyle = GRAPH.paper; c.beginPath(); c.moveTo(L - 44 * s, -wv); c.lineTo(L - 10 * s, -3.5 * s); c.lineTo(L - 10 * s, 3.5 * s); c.lineTo(L - 44 * s, wv); c.closePath(); c.fill();
    c.fillStyle = GRAPH.lead; c.beginPath(); c.moveTo(L - 12 * s, -4 * s); c.lineTo(L, 0); c.lineTo(L - 12 * s, 4 * s); c.closePath(); c.fill(); c.restore();
    const q = xform([[0, -wv], [L - 44 * s, -wv], [L - 10 * s, -3.5 * s], [L, 0], [L - 10 * s, 3.5 * s], [L - 44 * s, wv], [0, wv]], a[0], a[1], ang); pencilLoop(c, q, sw * .8, 80);
  } else {
    const th = T(G.thumb); c.save(); c.fillStyle = GRAPH.paper; c.fill(polyPath(th)); c.clip(polyPath(th)); graphShade(c, T(G.thumbShade), { seed: 81, al: .2 }); c.restore();
    pencil(c, T(G.thumbOpen), sw, 82); pencilLoop(c, T(G.nail), sw * .5, 83, { al: .4 });
  }
}
const graphTip = p => HAND.T([GPENCIL.tip], p)[0];   // where the pencil point is on the page
