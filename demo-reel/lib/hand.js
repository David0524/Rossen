'use strict';
/* YOU: the hero is only ever a hand. One right hand, seen from the viewer's side, drawn by every style from the same
   geometry so it reads as the same hand in every world.
   Local units (about design units at s = 1): the origin sits on a held sheet's bottom edge. The sheet covers everything
   above y = 0, so the fingers (behind it) only show when the hand is empty; the knuckles, the back of the hand and the
   thumb (in front, its pad on the sheet) always show. The forearm leaves the frame to the lower right.
   pose: { x, y, rot, s, grip } with grip 0 (open, thumb out) .. 1 (the thumb closed on the sheet). */
// limb: a tapered, rounded shape along a centreline (fingers, the thumb). ws = widths along it (base .. tip).
function limb(ctrl, ws, n = 18) {
  const C = smooth(ctrl, false, 8), P = resample(C, Math.max(2, pathLength(C) / n)), N = P.length, L = [], R = [];
  for (let i = 0; i < N; i++) { const a = P[Math.max(0, i - 1)], b = P[Math.min(N - 1, i + 1)], dx = b[0] - a[0], dy = b[1] - a[1], d = Math.hypot(dx, dy) || 1, nx = -dy / d, ny = dx / d;
    const u = i / (N - 1) * (ws.length - 1), k = Math.min(ws.length - 2, Math.floor(u)), w = lerp(ws[k], ws[k + 1], u - k) / 2;
    L.push([P[i][0] + nx * w, P[i][1] + ny * w]); R.push([P[i][0] - nx * w, P[i][1] - ny * w]); }
  const e = P[N - 1], q = P[N - 2], ang = Math.atan2(e[1] - q[1], e[0] - q[0]), w = ws[ws.length - 1] / 2, cap = [];
  for (let k = 1; k < 10; k++) { const t = Math.PI / 2 - Math.PI * k / 10; cap.push([e[0] + Math.cos(ang + t) * w, e[1] + Math.sin(ang + t) * w]); }
  return { outline: [...L, ...cap, ...R.reverse()], spine: P };
}
const HAND = (() => {
  const d = [.36, .933], n = [.933, -.36], wc = [22, 166];
  const al = (u, hw) => [wc[0] + d[0] * u + n[0] * hw, wc[1] + d[1] * u + n[1] * hw];
  const back = smooth([[-60, 18], [-40, 8], [-21, 6], [-2, 5], [16, 8], [33, 14], [48, 22], [66, 52], [72, 104], [62, 158], [20, 176], [-22, 170], [-56, 144], [-72, 96], [-72, 52]], true, 5);
  const F = [[[-50, 18], [-55, -38], [-60, -92]], [[-18, 10], [-19, -52], [-21, -110]], [[15, 12], [18, -44], [22, -96]], [[45, 24], [52, -16], [59, -58]]];
  const FW = [[33, 31, 26], [34, 32, 27], [32, 30, 25], [28, 26, 21]];
  const fingers = F.map((f, i) => limb(f, FW[i]));
  const forearm = smooth([al(-8, 46), al(120, 54), al(330, 66), al(640, 66), al(640, -66), al(330, -62), al(120, -52), al(-8, -44)], false, 5);
  const cuff = [al(236, 72), al(290, 76), al(290, -76), al(236, -72)], sleeve = [al(236, 72), al(720, 92), al(720, -92), al(236, -72)];
  const TB = [-40, 132], TH = [[-40, 132], [-80, 78], [-68, 14], [-36, -30]], TW = [46, 42, 33, 29];   // the base sits inside the palm
  function geo(grip = 1) {
    const a = (1 - grip) * -.42, cs = Math.cos(a), sn = Math.sin(a), rot = ([x, y]) => { const vx = x - TB[0], vy = y - TB[1]; return [TB[0] + vx * cs - vy * sn, TB[1] + vx * sn + vy * cs]; };
    const th = limb(TH.map(rot), TW), sp = th.spine, e = sp[sp.length - 1], q = sp[sp.length - 5], ang = Math.atan2(e[1] - q[1], e[0] - q[0]);
    const nc = [e[0] - Math.cos(ang) * 12, e[1] - Math.sin(ang) * 12], nail = smooth(xform([[-9, -8], [5, -9], [10, 0], [5, 9], [-9, 8]], nc[0], nc[1], ang), true, 4);
    return { back, fingers: fingers.map(f => f.outline), fingerSpines: fingers.map(f => f.spine), forearm, cuff, sleeve, thumb: th.outline, thumbOpen: th.outline.slice(4, -10), thumbSpine: sp,   // thumbOpen: the outline without its base (it grows out of the palm)
      nail, tip: sp[sp.length - 1],
      knuckles: [[-54, 20, -40, 22], [-24, 12, -10, 13], [9, 14, 23, 17], [40, 26, 52, 30]].map(([a, b, c2, e2]) => [[a, b + 2], [(a + c2) / 2, b - 3], [c2, e2 + 2]]),
      tendons: [[[-44, 40], [-24, 132]], [[-14, 34], [-2, 136]], [[18, 38], [22, 134]], [[44, 46], [44, 124]]],
      shadeBack: [[26, -10], [110, -10], [110, 200], [18, 200]], shadeArm: [al(-10, 16), al(660, 30), al(660, 140), al(-10, 140)],
      thumbShade: [[-120, 40], [-40, 40], [-40, 200], [-120, 200]] };
  }
  const T = (pts, p) => xform(pts, p.x, p.y, p.rot || 0, p.s || 1);
  return { geo, T, al };
})();
