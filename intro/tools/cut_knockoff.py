"""Cut JEFF'S RULES #3's knockoff seller (the Scammer in his trench coat of knockoffs) into paper-cutout puppet parts.
The pixels are the reference's own; only the cut lines are new.
  head   the fedora, mask and face (pivots at the neck)
  centre the lapels and shirt between the coat flaps (fixed to the body), with a hidden copy of the chin under the head
  flapL / flapR  the two open coat flaps with the knockoffs pinned inside; each swings about its hinge on the centre
         strip (drawn with a horizontal squash), so the coat opens and closes
  handL / handR  the gloved hands, separate so they stay the right shape and ride the flaps' outer edges
  legL / legR
usage: python3 tools/cut_knockoff.py   (reads assets/rules/ep03/knock_ref.webp, writes knock_*.png + knock_parts.json)"""
import numpy as np, json
from PIL import Image, ImageDraw
D = 'assets/rules/ep03/'
A = np.array(Image.open(D + 'knock_ref.webp').convert('RGB')).astype(np.float32); H, W, _ = A.shape
def dil(m, r):
    o = m.copy()
    for _ in range(r):
        n = o.copy(); n[1:] |= o[:-1]; n[:-1] |= o[1:]; n[:, 1:] |= o[:, :-1]; n[:, :-1] |= o[:, 1:]; o = n
    return o
def ero(m, r): return ~dil(~m, r)
bg = np.median(np.concatenate([A[:40, :40].reshape(-1, 3), A[:40, -40:].reshape(-1, 3), A[-40:, :40].reshape(-1, 3)]), 0)
fg = np.sqrt(((A - bg) ** 2).sum(2)) > 34
wall = dil(fg, 2); out = np.zeros_like(fg); out[0, :] = out[-1, :] = out[:, 0] = out[:, -1] = True; out &= ~wall
while True:   # the paper background: flood-filled from the edges up to the ink
    n = dil(out, 1) & ~wall
    if (n == out).all(): break
    out = n
body = ero(dil(~dil(out, 2), 1), 1)
def poly(pts):
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).polygon([tuple(map(float, p)) for p in pts], fill=255); return np.array(m) > 0
yy = np.arange(H)[:, None] + np.zeros((1, W), int); xx = np.arange(W)[None, :] + np.zeros((H, 1), int)
body &= poly([(495, 105), (1175, 105), (1175, 860), (495, 860)])   # the figure only (the paper's edges carry grain)
HL, HR, HEM, NECK = 800, 870, 776, (835, 445)   # the flap hinges (x), the coat hem (y), the neck pivot
head = poly([(560, 110), (1070, 110), (1070, 300), (1010, 330), (960, 400), (930, 440), (880, 452), (800, 455), (760, 440), (720, 405), (560, 330)]) & body
glove = dil((A[..., 2] > 150) & (A[..., 0] < 110) & (A[..., 2] - A[..., 1] > 50), 3)   # the blue gloves only, not the coat edge they grip
handL = poly([(505, 425), (600, 425), (600, 520), (505, 520)]) & body & glove
handR = poly([(1068, 425), (1160, 425), (1160, 515), (1068, 515)]) & body & glove
coat = body & (yy < HEM) & ~head
flapL = coat & (xx < HL) & ~handL
flapR = coat & (xx > HR) & ~handR
centre = coat & (xx >= HL) & (xx <= HR)
centre |= head & (yy >= 400) & (xx > 740) & (xx < 940)   # the hidden chin: a head tilt never opens a slit at the neck
legs = body & (yy >= HEM)
legL = legs & (xx < 835); legR = legs & (xx >= 835)
parts = dict(head=head, centre=centre, flapL=flapL, flapR=flapR, handL=handL, handR=handR, legL=legL, legR=legR)
piv = dict(head=NECK, centre=(835, 845), flapL=(HL, 580), flapR=(HR, 580), handL=(552, 470), handR=(1112, 465), legL=(735, HEM), legR=(935, HEM))
meta = {'ref': [W, H], 'feet': [835, 845], 'hinge': [HL, HR], 'hem': HEM, 'parts': {}}
for k, m in parts.items():
    ys, xs = np.nonzero(m); x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    rgba = np.dstack([A.astype(np.uint8), (m * 255).astype(np.uint8)])[y0:y1, x0:x1]
    Image.fromarray(rgba).save(f'{D}knock_{k}.png')
    meta['parts'][k] = {'x': int(x0), 'y': int(y0), 'w': int(x1 - x0), 'h': int(y1 - y0), 'pivot': list(piv[k])}
json.dump(meta, open(D + 'knock_parts.json', 'w'), indent=1)
chk = Image.new('RGB', (W, H), (255, 255, 255)); cols = [(255, 80, 80), (80, 200, 80), (80, 80, 255), (230, 170, 0), (200, 0, 200), (0, 180, 180), (120, 60, 0), (90, 90, 90)]
arr = np.array(chk)
for (k, m), col in zip(parts.items(), cols): arr[m] = col
Image.fromarray(arr).save('/tmp/claude-0/-home-user-Rossen/3fdd0da9-e341-56c5-b3c5-1d0ea82e103b/scratchpad/knock_parts.png')
print({k: meta['parts'][k] for k in meta['parts']})
