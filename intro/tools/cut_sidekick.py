"""Cut the Scammer's sidekick (assets/wedtease/sidekick_ref.webp, the user's own character drawing) into a jointed
paper-cutout puppet. The pixels are the reference's own; only the cut lines are new. Each moving piece leaves a hidden
fill behind it on the piece underneath, so a turn never opens a hole.
  head   cap, mask and grin (pivots at the top of his long neck)
  torso  neck, jacket (his left arm stays hidden behind his back) and the pants' waist
  arm    his right hand (pivots at the sleeve cuff)
  can    the oil can, a separate piece drawn behind the hand; the part the fingers hide is filled with the can's own yellow
  legL / legR
Also cuts the man's (assets/officer/man_head.png) jaw drop: man_head_gasp.png, the same head with the smile repainted as
an open "O" in his own skin and outline colours.
usage: python3 tools/cut_sidekick.py  ->  assets/wedtease/sidekick_<part>.png + sidekick_parts.json (+ man_head_gasp.png)"""
import numpy as np, json, os
from collections import deque
from PIL import Image, ImageDraw
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
OUT = f'{ROOT}/assets/wedtease'
CHECK = f'{ROOT}/_check/wedtease/'
HEAD = [(360, 80), (730, 80), (730, 285), (648, 300), (618, 345), (580, 362), (550, 350), (548, 326), (505, 318), (472, 322), (430, 305), (360, 270)]
HAND = [(626, 758), (650, 750), (684, 768), (688, 800), (676, 836), (628, 838), (616, 810)]
CAN = [(670, 738), (679, 710), (692, 705), (701, 710), (735, 652), (747, 658), (713, 719), (718, 728), (713, 756), (683, 820), (660, 820), (647, 768)]
LEGS_Y, SPLIT = 885, lambda y: 500 + (y - LEGS_Y) * .03
PIV = dict(head=(527, 318), arm=(645, 762), can=(668, 790), legL=(452, 890), legR=(560, 890), torso=(540, 1455))
FEET = (540, 1455)
def dil(m, r):
    o = m.copy()
    for _ in range(r):
        n = o.copy(); n[1:] |= o[:-1]; n[:-1] |= o[1:]; n[:, 1:] |= o[:, :-1]; n[:, :-1] |= o[:, 1:]; o = n
    return o
def ero(m, r): return ~dil(~m, r)
A = np.array(Image.open(f'{OUT}/sidekick_ref.webp').convert('RGB')).astype(np.float32); H, W, _ = A.shape
bg = np.median(np.concatenate([A[:40, :40].reshape(-1, 3), A[:40, -40:].reshape(-1, 3), A[-40:, :40].reshape(-1, 3), A[-40:, -40:].reshape(-1, 3)]), 0)
fg = np.sqrt(((A - bg) ** 2).sum(2)) > 34
wall = dil(fg, 2); out = np.zeros_like(fg); out[0, :] = out[-1, :] = out[:, 0] = out[:, -1] = True; out &= ~wall
while True:
    n = dil(out, 1) & ~wall
    if (n == out).all(): break
    out = n
body = ero(dil(~dil(out, 2), 1), 1)
lab = np.zeros((H, W), bool); cy, cx = 600, 520; lab[cy, cx] = True; q = deque([(cy, cx)])
while q:
    y, x = q.popleft()
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        a, b = y + dy, x + dx
        if 0 <= a < H and 0 <= b < W and body[a, b] and not lab[a, b]: lab[a, b] = True; q.append((a, b))
body = lab
def poly(pts):
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).polygon([tuple(map(float, p)) for p in pts], fill=255); return np.array(m) > 0
yy = np.arange(H)[:, None] + np.zeros((1, W), int); xx = np.arange(W)[None, :] + np.zeros((H, 1), int)
blue = (A[..., 2] > A[..., 0] + 40) & (A[..., 2] > 110)
head = poly(HEAD) & body
handzone = poly(HAND) & body & dil(blue, 4)   # the hand's own blue and its outline, not the jacket hem
can = poly(CAN) & body & ~(handzone & blue) & ~head
hand = handzone & ~can
legs = body & (yy >= LEGS_Y) & ~hand & ~can
legL = legs & (xx < SPLIT(yy)); legR = legs & (xx >= SPLIT(yy))
torso = body & ~head & ~hand & ~can & ~legL & ~legR
RGB = {'torso': A.copy(), 'can': A.copy()}
neck = poly([(506, 270), (548, 270), (548, 345), (506, 345)]) & head   # the hidden neck top under the chin: the neck's own blue
RGB['torso'][neck] = np.median(A[390:430, 512:540].reshape(-1, 3), 0); torso |= neck
hole = dil(hand | can, 3) & poly([(606, 700), (668, 700), (664, 790), (650, 842), (606, 842)]) & ~torso   # behind the hand: the jacket's black
RGB['torso'][hole] = np.median(A[600:650, 560:600].reshape(-1, 3), 0); torso |= hole
cy0 = np.median(A[can & ~blue & (A[..., 0] > 180) & (A[..., 2] < 120)].reshape(-1, 3), 0)   # the part the fingers hide: the can's yellow
cfill = poly([(650, 768), (674, 758), (684, 814), (662, 818)]) & ~can; RGB['can'][cfill] = cy0; can |= cfill
parts = dict(legL=legL, legR=legR, torso=torso, can=can, arm=hand, head=head)
meta = {'ref': [W, H], 'feet': list(FEET), 'tip': [745, 658], 'parts': {}}
os.makedirs(CHECK, exist_ok=True)
for k, m in parts.items():
    ys, xs = np.nonzero(m); a0, a1, b0, b1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    Image.fromarray(np.dstack([RGB.get(k, A).astype(np.uint8), (m * 255).astype(np.uint8)])[b0:b1, a0:a1]).save(f'{OUT}/sidekick_{k}.png')
    meta['parts'][k] = {'x': int(a0), 'y': int(b0), 'w': int(a1 - a0), 'h': int(b1 - b0), 'pivot': list(PIV[k])}
json.dump(meta, open(f'{OUT}/sidekick_parts.json', 'w'), indent=1)
viz = np.full((H, W, 3), 255, np.uint8); cols = dict(legL=(120, 60, 0), legR=(90, 90, 90), torso=(80, 80, 255), can=(230, 170, 0), arm=(0, 180, 180), head=(255, 80, 80))
for k, m in parts.items(): viz[m] = cols[k]
Image.fromarray(np.concatenate([viz, A.astype(np.uint8)], 1)).resize((W, H // 2)).save(f'{CHECK}sidekick_cut.png')
print({k: (v['x'], v['y'], v['w'], v['h']) for k, v in meta['parts'].items()})

# the man's gasp: his smile covered with his own cheek halftone (copied from just below it), and an open "O" in his outline black
M = Image.open(f'{ROOT}/assets/officer/man_head.png').convert('RGBA'); a = np.array(M)
patch = a[236:256, 170:228].copy(); a[212:232, 170:228] = np.where(a[212:232, 170:228, 3:] > 0, patch, a[212:232, 170:228])
G = Image.fromarray(a); d = ImageDraw.Draw(G); ox, oy, rx, ry = 199, 228, 12, 16
d.ellipse((ox - rx - 4, oy - ry - 4, ox + rx + 4, oy + ry + 4), fill=(29, 27, 31, 255)); d.ellipse((ox - rx, oy - ry, ox + rx, oy + ry), fill=(58, 30, 30, 255))
d.ellipse((ox - rx * .6, oy + ry * .2, ox + rx * .6, oy + ry * .85), fill=(226, 118, 44, 255))
G.save(f'{OUT}/man_head_gasp.png')
b = Image.new('RGBA', (M.width * 2, M.height), (150, 150, 150, 255)); b.alpha_composite(M); b.alpha_composite(G, (M.width, 0)); b.save(f'{CHECK}man_gasp.png')
