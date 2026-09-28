"""Cut the screen-print Jeff reference into paper-cutout puppet parts (head, torso, arms, legs) with pivots.
The pixels are the reference's own; only the cut lines are new."""
import numpy as np, json
from PIL import Image, ImageDraw
src = Image.open('assets/casefile/jeff_ref.webp').convert('RGB'); A = np.array(src).astype(np.float32)
H, W, _ = A.shape
bg = np.median(np.concatenate([A[:40, :40].reshape(-1, 3), A[:40, -40:].reshape(-1, 3), A[-40:, :40].reshape(-1, 3)]), 0)
dist = np.sqrt(((A - bg) ** 2).sum(2))
fg = dist > 34
def dil(m, r):
    o = m.copy()
    for _ in range(r):
        n = o.copy(); n[1:] |= o[:-1]; n[:-1] |= o[1:]; n[:, 1:] |= o[:, :-1]; n[:, :-1] |= o[:, 1:]; o = n
    return o
def ero(m, r): return ~dil(~m, r)
# outside = flood from border through non-foreground; everything else is Jeff (fills holes like eye highlights)
wall = dil(fg, 2); out = np.zeros_like(fg); out[0, :] = out[-1, :] = out[:, 0] = out[:, -1] = True; out &= ~wall
while True:
    n = dil(out, 1) & ~wall
    if (n == out).all(): break
    out = n
jeff = ~dil(out, 2)
jeff = ero(dil(jeff, 1), 1)
def poly_mask(pts):
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).polygon([tuple(p) for p in pts], fill=255); return np.array(m) > 0
P = {
  'head':  [(600, 20), (1060, 20), (1060, 462), (990, 470), (700, 470), (695, 402), (600, 398)],
  'armL':  [(530, 398), (695, 398), (712, 500), (722, 560), (700, 690), (620, 700), (530, 690)],   # mic arm (screen left)
  'armR':  [(1004, 470), (1080, 470), (1140, 690), (1100, 790), (1000, 790), (1008, 600)],       # free arm (screen right)
  'legL':  [(640, 748), (848, 748), (848, 920), (640, 920)],
  'legR':  [(848, 748), (1060, 748), (1060, 920), (848, 920)],
}
masks = {k: poly_mask(v) & jeff for k, v in P.items()}
used = np.zeros_like(jeff)
for k in ('head', 'armL', 'armR', 'legL', 'legR'): masks[k] &= ~used; used |= masks[k]
masks['torso'] = jeff & ~used
# a hidden copy of the chin and jaw on the torso, under the head: at rest the head covers it exactly; when the head
# tilts it fills the slit that would otherwise open along the cut and let the background show through
yy = np.arange(H)[:, None] + np.zeros((1, W), int)
masks['torso'] |= masks['head'] & (yy >= 380)   # the jaw and chin only, below the cheeks
PIV = {'head': (842, 468), 'armL': (706, 520), 'armR': (1012, 512), 'legL': (752, 752), 'legR': (948, 752), 'torso': (850, 745)}
meta = {'ref': [W, H], 'parts': {}}
for k, m in masks.items():
    ys, xs = np.nonzero(m); x0, y0, x1, y1 = xs.min() - 2, ys.min() - 2, xs.max() + 3, ys.max() + 3
    rgba = np.zeros((y1 - y0, x1 - x0, 4), np.uint8); rgba[..., :3] = A[y0:y1, x0:x1]; rgba[..., 3] = m[y0:y1, x0:x1] * 255
    Image.fromarray(rgba).save(f'assets/casefile/jeff_{k}.png')
    meta['parts'][k] = {'x': int(x0), 'y': int(y0), 'w': int(x1 - x0), 'h': int(y1 - y0), 'pivot': PIV[k]}
json.dump(meta, open('assets/casefile/jeff_parts.json', 'w'), indent=1)
# preview: parts tinted on grey
pv = np.full((H, W, 3), 90, np.uint8); cols = {'head': (255, 120, 120), 'torso': (120, 255, 120), 'armL': (120, 120, 255), 'armR': (255, 255, 120), 'legL': (255, 120, 255), 'legR': (120, 255, 255)}
for k, m in masks.items(): pv[m] = (A[m] * .5 + np.array(cols[k]) * .5).astype(np.uint8)
Image.fromarray(pv).crop((500, 20, 1160, 920)).save('/tmp/claude-0/-home-user-Rossen/3fdd0da9-e341-56c5-b3c5-1d0ea82e103b/scratchpad/parts.png')
print({k: int(m.sum()) for k, m in masks.items()})
