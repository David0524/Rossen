"""Cut the scammer reference into paper-cutout puppet parts (head, torso, rod with both hands, two boots) with pivots.
The pixels are the reference's own; only the cut lines are new. The fishing line and hook are left out so the film can
draw its own line (casting, snagging, reeling)."""
import numpy as np, json
from PIL import Image, ImageDraw
src = Image.open('assets/explainer/scammer_ref.png').convert('RGB'); A = np.array(src).astype(np.float32)
H, W, _ = A.shape
bg = np.median(np.concatenate([A[:40, :40].reshape(-1, 3), A[:40, -40:].reshape(-1, 3), A[-40:, :40].reshape(-1, 3)]), 0)
fg = np.sqrt(((A - bg) ** 2).sum(2)) > 34
def dil(m, r):
    o = m.copy()
    for _ in range(r):
        n = o.copy(); n[1:] |= o[:-1]; n[:-1] |= o[1:]; n[:, 1:] |= o[:, :-1]; n[:, :-1] |= o[:, 1:]; o = n
    return o
def ero(m, r): return ~dil(~m, r)
wall = dil(fg, 2); out = np.zeros_like(fg); out[0, :] = out[-1, :] = out[:, 0] = out[:, -1] = True; out &= ~wall
while True:
    n = dil(out, 1) & ~wall
    if (n == out).all(): break
    out = n
body = ero(dil(~dil(out, 2), 1), 1)
def poly(pts):
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).polygon([tuple(map(float, p)) for p in pts], fill=255); return np.array(m) > 0
def band(a, b, hw):
    a, b = np.array(a, float), np.array(b, float); d = (b - a) / np.linalg.norm(b - a); n = np.array([-d[1], d[0]]) * hw
    return poly([a + n, b + n, b - n, a - n])
line = poly([(1222, 246), (1280, 246), (1280, 500), (1275, 625), (1190, 625), (1190, 500), (1222, 500)])   # line + hook: drawn by the film
body &= ~line
# rod part: only the mittens, the reel and the rod itself, so the coat behind them stays on the torso
coat = poly([(588, 490), (760, 540), (900, 556), (975, 545), (1034, 630), (1032, 800), (588, 800)])
R, G, B = A[..., 0], A[..., 1], A[..., 2]
head_zone = poly([(535, 195), (1020, 195), (1020, 420), (975, 440), (968, 545), (600, 505), (535, 440)])   # hat + head, as below
hands = poly([(800, 612), (920, 612), (920, 560), (1022, 560), (1022, 748), (800, 748)])
mittens = dil((B > 140) & (R < 110) & (G < 170) & hands, 3)
yy, xx = np.mgrid[:H, :W]; reel = (xx - 905) ** 2 + (yy - 662) ** 2 < 33 ** 2
rod = (mittens | reel | (band((905, 664), (988, 538), 17) & coat) | (~coat & ~head_zone & poly([(940, 560), (1300, 560), (1300, 190), (940, 190)]))) & body
# the coat under the rod and hands: filled with a tile of plain coat from its left side (never seen unless the rod swings)
hole = (rod & coat) | (hands & coat & (A.sum(2) > 520))   # also the paper gaps between the mittens and the coat
tile = A[600:780, 606:694]
A2 = A.copy(); ys, xs = np.nonzero(hole); A2[ys, xs] = tile[(ys - 600) % 180, (xs - 606) % 88]
head = poly([(535, 195), (1020, 195), (1020, 420), (975, 440), (968, 545), (600, 505), (535, 440)]) & body & ~rod
legL = poly([(600, 792), (800, 792), (800, 860), (600, 860)]) & body & ~rod
legR = poly([(800, 792), (1000, 792), (1000, 860), (800, 860)]) & body & ~rod
torso = (body | hole) & ~head & ~legL & ~legR & ~(rod & ~coat)
masks = {'legL': legL, 'legR': legR, 'torso': torso, 'rod': rod, 'head': head}
PIV = {'head': (790, 545), 'rod': (905, 662), 'legL': (700, 792), 'legR': (900, 792), 'torso': (800, 835)}
meta = {'ref': [W, H], 'feet': [800, 835], 'tip': [1232, 230], 'parts': {}}
for k, m in masks.items():
    ys, xs = np.nonzero(m); x0, y0, x1, y1 = xs.min() - 2, ys.min() - 2, xs.max() + 3, ys.max() + 3
    src_px = A2 if k == 'torso' else A
    rgba = np.zeros((y1 - y0, x1 - x0, 4), np.uint8); rgba[..., :3] = src_px[y0:y1, x0:x1]; rgba[..., 3] = m[y0:y1, x0:x1] * 255
    Image.fromarray(rgba).save(f'assets/explainer/scammer_{k}.png')
    meta['parts'][k] = {'x': int(x0), 'y': int(y0), 'w': int(x1 - x0), 'h': int(y1 - y0), 'pivot': PIV[k]}
json.dump(meta, open('assets/explainer/scammer_parts.json', 'w'), indent=1)
pv = np.full((H, W, 3), 90, np.uint8); cols = {'head': (255, 120, 120), 'torso': (120, 255, 120), 'rod': (255, 255, 120), 'legL': (255, 120, 255), 'legR': (120, 255, 255)}
for k, m in masks.items(): pv[m] = (A[m] * .5 + np.array(cols[k]) * .5).astype(np.uint8)
Image.fromarray(pv).crop((520, 180, 1300, 880)).save('/tmp/claude-0/-home-user-Rossen/3fdd0da9-e341-56c5-b3c5-1d0ea82e103b/scratchpad/scam_parts.png')
print({k: int(m.sum()) for k, m in masks.items()}, 'line px left out:', int((line & ~dil(out, 2)).sum()))
