'use strict';
/* Demo reel shared kit (on top of lib/core.js, the generic canvas core). Nothing here belongs to any client brand.
   - format: 1080x1920 (9:16), 24 fps, 96 BPM (a beat is 0.625 s, a bar 2.5 s); landings start 0.14 s early
   - the safe box: platform buttons and captions cover the top 15%, the bottom 25% and the right 15% of the frame, so
     key action and text live in a 918 x 1152 design box (screen x 0-918, y 288-1440). The box is not centred on the
     frame, so it is drawn in design units and scaled down by K about the frame's centre line (x 540), which centres it
     on the frame and keeps it inside the safe area. Backgrounds and full-frame transitions stay full-frame.
   - puppets: jointed paper cut-outs from assets/<name>_parts.json
   - the grain dissolve used by the style-changing transitions */
setFormat({ ar: '9:16', width: 1080 });
const FPS = 24, BPM = 96, BEAT = 60 / BPM, BAR = 4 * BEAT, E8 = BEAT / 2, S16 = BEAT / 4, SLAM = .14;
const at = (bar, beat = 1) => bar * BAR + (beat - 1) * BEAT;   // bar 0-based, beat 1-based
const DW = 918, DH = 1152, K = .82, DCX = DW / 2, DCY = DH / 2, SCY_ = 864;   // the design box and its scale
function designT(c) { resetT(c); c.translate(540 - DCX * K, SCY_ - DCY * K); c.scale(K, K); }
const toScreen = (x, y) => [540 + (x - DCX) * K, SCY_ + (y - DCY) * K];
const Q = new URLSearchParams(location.search), SHOW_SAFE = Q.has('safe');
function safeOverlay(c) { c.save(); resetT(c); c.fillStyle = 'rgba(255,0,255,.16)'; c.fillRect(0, 0, W, 288); c.fillRect(0, 1440, W, H - 1440); c.fillRect(918, 288, W - 918, 1152);
  const [x0, y0] = toScreen(0, 0), [x1, y1] = toScreen(DW, DH); c.strokeStyle = '#ff00ff'; c.lineWidth = 4; c.strokeRect(x0, y0, x1 - x0, y1 - y0); c.restore(); }

// ---------------- small helpers ----------------
const clamp01 = v => Math.max(0, Math.min(1, v));
const seg = (t, a, b) => clamp01((t - a) / (b - a));
const land = (t, t0) => seg(t, t0 - SLAM, t0);
const easeOutBack = (x, s = 1.7) => 1 + (s + 1) * Math.pow(x - 1, 3) + s * Math.pow(x - 1, 2);
const onTwos = t => { const b = Math.floor(t / BEAT + 1e-6) * BEAT; return b + Math.floor((t - b) * FPS / 2 + 1e-6) * 2 / FPS; };   // a new drawing on every beat
const IMG = {};
function loadImg(k, src) { return new Promise((res, rej) => { const im = new Image(); im.onload = () => { IMG[k] = im; res(im); }; im.onerror = () => rej(new Error('missing ' + src)); im.src = src; }); }
function fitFont(c, s, weight, size, family, maxW) { c.font = `${weight} ${size}px ${family}`; const w = c.measureText(s).width; return w > maxW ? Math.floor(size * maxW / w) : size; }
function textAt(c, s, x, y, weight, size, family, col, maxW = 9999, align = 'center') {   // solid, level type
  const sz = fitFont(c, s, weight, size, family, maxW); c.font = `${weight} ${sz}px ${family}`; c.textAlign = align; c.textBaseline = 'middle'; c.fillStyle = col; c.fillText(s, x, y); return sz;
}

// ---------------- puppets ----------------
const PUP = {};
async function loadPuppet(name) { PUP[name] = await (await fetch(`assets/${name}_parts.json`)).json(); const M = PUP[name];
  await Promise.all([...Object.keys(M.parts), ...Object.keys(M.alt || {})].map(k => loadImg(name + '_' + k, `assets/${name}_${k}.png`))); }
// pose: { head, arm, arm2, legL, legR (radians), bob (ref px), tilt, sx, sy (squash), headImg (an alternate head drawing),
//        armUnder(c) (drawn in the arm's own frame, under it: a prop in the hand), armScale }
function puppet(c, name, x, y, s, p = {}) {
  const M = PUP[name]; c.save(); c.translate(x, y); c.rotate(p.tilt || 0); c.scale(s * (p.sx || 1), s * (p.sy || 1)); c.translate(-M.feet[0], -M.feet[1] - (p.bob || 0));
  const part = (k, a = 0, img = k, under = null, ks = 1) => { const m = M.parts[k]; if (!m) return; const [px, py] = m.pivot; c.save(); c.translate(px, py); c.rotate(a); c.scale(ks, ks); c.translate(-px, -py);
    if (under) under(c); c.drawImage(IMG[name + '_' + img], m.x, m.y); c.restore(); };
  if (p.armBehind) { const m = M.parts.arm, [px, py] = m.pivot; c.save(); c.translate(px, py); c.rotate(p.arm || 0); c.translate(-px, -py); p.armBehind(c); c.restore(); }   // a prop held behind the body
  part('legL', p.legL || 0); part('legR', p.legR || 0); part('torso'); part('head', p.head || 0, p.headImg || 'head'); part('arm', p.arm || 0, 'arm', p.armUnder, p.armScale || 1); part('arm2', p.arm2 || 0);
  c.restore();
}
function refPoint(name, pt, x, y, s, p = {}) {   // a point of the reference drawing, where it lands on the page (no rotation)
  const M = PUP[name]; return [x + (pt[0] - M.feet[0]) * s * (p.sx || 1), y + (pt[1] - M.feet[1] - (p.bob || 0)) * s * (p.sy || 1)];
}

// ---------------- the grain dissolve (one style becomes another) ----------------
// A fixed noise field (coarse blotches plus fine grain). For progress p, pixels whose noise is below p have switched
// to the new style; a thin band at the switching edge is printed as speckle in the new style's inks. One dissolver
// covers the frame (screen space); a prop that changes style while it moves gets its own, in the prop's space.
// octaves: [[grid w, grid h, weight], ...] of smooth value noise; fine: the weight of per-pixel grain on top
function makeDissolver(w, h, seed, octaves = [[9, 16, .55], [30, 54, .3]], fine = .15) {
  const N = new Float32Array(w * h), mask = document.createElement('canvas'), fringe = document.createElement('canvas');
  mask.width = fringe.width = w; mask.height = fringe.height = h;
  const r = rng(seed), oct = octaves.map(([gw, gh, k]) => { const G = new Float32Array((gw + 2) * (gh + 2)).map(() => r()); return (x, y) => { const gx = x / w * gw, gy = y / h * gh, i = Math.floor(gx), j = Math.floor(gy), fx = gx - i, fy = gy - j, sx = fx * fx * (3 - 2 * fx), sy = fy * fy * (3 - 2 * fy);
    const g = (a, b) => G[b * (gw + 2) + a]; return k * ((g(i, j) * (1 - sx) + g(i + 1, j) * sx) * (1 - sy) + (g(i, j + 1) * (1 - sx) + g(i + 1, j + 1) * sx) * sy); }; });
  let lo = 1e9, hi = -1e9;
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { let v = fine * r(); for (const o of oct) v += o(x, y); N[y * w + x] = v; lo = Math.min(lo, v); hi = Math.max(hi, v); }
  for (let i = 0; i < N.length; i++) N[i] = (N[i] - lo) / (hi - lo);   // spread to 0..1 so p runs the whole field
  let key = null;
  const D = { mask, fringe, w, h,
    set(p, band = .09, fringeCols = null) {   // mask alpha = switched; fringe = speckle at the edge
      const k = p + '|' + band + '|' + fringeCols; if (k === key) return D; key = k;
      const m = mask.getContext('2d'), f = fringe.getContext('2d'), md = m.createImageData(w, h), fd = f.createImageData(w, h);
      const q = p * (1 + 2 * band) - band, cols = fringeCols && fringeCols.map(parseColor);
      for (let i = 0; i < N.length; i++) { const n = N[i], a = clamp01((q - n) / band + .5); md.data[i * 4 + 3] = a * 255;
        if (cols && Math.abs(q - n) < band * .35) { const kk = (i * 2654435761 >>> 0) % cols.length, [R, Gc, B] = cols[kk]; fd.data[i * 4] = R; fd.data[i * 4 + 1] = Gc; fd.data[i * 4 + 2] = B; fd.data[i * 4 + 3] = 255; } }
      m.putImageData(md, 0, 0); f.putImageData(fd, 0, 0); return D; },
    // src (any size) masked by the field, drawn into dst's rect (dx, dy, dw, dh) in dst's current transform
    draw(dst, src, p, band = .09, fringeCols = null, rect = null, tmp = null) {
      if (p <= 0) return; const [dx, dy, dw, dh] = rect || [0, 0, W, H];
      if (p >= 1) { dst.drawImage(src, dx, dy, dw, dh); return; }
      D.set(p, band, fringeCols);
      const T = tmp || _mixTmp(src.width, src.height), g = T.getContext('2d'); g.setTransform(1, 0, 0, 1, 0, 0); g.globalCompositeOperation = 'source-over'; g.clearRect(0, 0, T.width, T.height);
      g.drawImage(src, 0, 0, T.width, T.height); g.globalCompositeOperation = 'destination-in'; g.imageSmoothingEnabled = true; g.drawImage(mask, 0, 0, T.width, T.height); g.globalCompositeOperation = 'source-over';
      if (fringeCols) { g.imageSmoothingEnabled = false; g.drawImage(fringe, 0, 0, T.width, T.height); }
      dst.drawImage(T, dx, dy, dw, dh); } };
  return D;
}
const _mixT = {}; function _mixTmp(w, h) { const k = w + 'x' + h; if (!_mixT[k]) { const o = document.createElement('canvas'); o.width = w; o.height = h; _mixT[k] = o; } return _mixT[k]; }
const SCENE_DZ = makeDissolver(540, 960, 424242);
function maskedDraw(c, src, p, band = .09, fringeCols = null) {   // a full-frame layer over c, where the frame has switched
  c.save(); resetT(c); SCENE_DZ.draw(c, src, p, band, fringeCols); c.restore();
}
function clearLayer(L) { const g = L.getContext('2d'); g.setTransform(1, 0, 0, 1, 0, 0); g.globalCompositeOperation = 'source-over'; g.globalAlpha = 1; g.clearRect(0, 0, L.width, L.height); return g; }

// ---------------- curves ----------------
// Catmull-Rom through control points -> a dense polyline (for fills and for pen strokes)
function smooth(pts, closed = false, n = 8) {
  const P = pts.length, out = [], g = i => closed ? pts[(i + P) % P] : pts[Math.max(0, Math.min(P - 1, i))];
  const segs = closed ? P : P - 1;
  for (let i = 0; i < segs; i++) { const p0 = g(i - 1), p1 = g(i), p2 = g(i + 1), p3 = g(i + 2);
    for (let k = 0; k < n; k++) { const t = k / n, t2 = t * t, t3 = t2 * t;
      out.push([0, 1].map(j => .5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3))); } }
  if (!closed) out.push(pts[P - 1].slice());
  return out;
}
function resample(pts, step) {   // evenly spaced points along a polyline
  const out = [pts[0].slice()]; let carry = 0;
  for (let i = 1; i < pts.length; i++) { const [ax, ay] = pts[i - 1], [bx, by] = pts[i], L = Math.hypot(bx - ax, by - ay); let d = step - carry;
    while (d <= L) { out.push([ax + (bx - ax) * d / L, ay + (by - ay) * d / L]); d += step; } carry = L - (d - step); }
  const last = pts[pts.length - 1]; if (Math.hypot(last[0] - out[out.length - 1][0], last[1] - out[out.length - 1][1]) > step * .3) out.push(last.slice());
  return out;
}
const xform = (pts, x, y, rot = 0, s = 1) => { const c = Math.cos(rot), n = Math.sin(rot); return pts.map(([u, v]) => [x + (u * c - v * n) * s, y + (u * n + v * c) * s]); };
const capsule = (a, b, w, n = 10) => { const dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy), ang = Math.atan2(dy, dx), r = w / 2, pts = [];
  for (let k = 0; k <= n; k++) { const t = -Math.PI / 2 + Math.PI * k / n; pts.push([b[0] + Math.cos(ang + t) * r, b[1] + Math.sin(ang + t) * r]); }
  for (let k = 0; k <= n; k++) { const t = Math.PI / 2 + Math.PI * k / n; pts.push([a[0] + Math.cos(ang + t) * r * .96, a[1] + Math.sin(ang + t) * r * .96]); }
  return pts; };
// kf: keyframes [[t, v1, v2, ...], ...] -> the values at t, a smooth curve through them (Catmull-Rom), held at the ends
function kf(t, KF) {
  const n = KF.length; if (t <= KF[0][0]) return KF[0].slice(1); if (t >= KF[n - 1][0]) return KF[n - 1].slice(1);
  let i = 0; while (t > KF[i + 1][0]) i++;
  const p0 = KF[Math.max(0, i - 1)], p1 = KF[i], p2 = KF[i + 1], p3 = KF[Math.min(n - 1, i + 2)], dt = p2[0] - p1[0], u = (t - p1[0]) / dt;
  const h00 = 2 * u ** 3 - 3 * u * u + 1, h10 = u ** 3 - 2 * u * u + u, h01 = -2 * u ** 3 + 3 * u * u, h11 = u ** 3 - u * u;
  return p1.slice(1).map((_, j) => { const m1 = i > 0 ? (p2[j + 1] - p0[j + 1]) / (p2[0] - p0[0]) * dt : 0, m2 = i + 2 < n ? (p3[j + 1] - p1[j + 1]) / (p3[0] - p1[0]) * dt : 0;
    return h00 * p1[j + 1] + h10 * m1 + h01 * p2[j + 1] + h11 * m2; });
}
const ring = (u, amp, decay, freq) => u <= 0 ? 0 : amp * Math.exp(-u * decay) * Math.cos(u * freq);   // a damped bounce after a contact
// where a point of the reference drawing on the arm part lands on the page, the arm turned by its pose angle
function armPoint(name, pt, x, y, s, p = {}, part = 'arm') { const M = PUP[name], [px, py] = M.parts[part].pivot, a = p[part] || 0, k = p.armScale || 1;
  const dx = (pt[0] - px) * k, dy = (pt[1] - py) * k, q = [px + dx * Math.cos(a) - dy * Math.sin(a), py + dx * Math.sin(a) + dy * Math.cos(a)]; return refPoint(name, q, x, y, s, p); }
