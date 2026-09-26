"""Cut WHAT WOULD YOU DO? #2's fake tech-support agent (the Scammer in a headset) into paper-cutout puppet parts.
The pixels are the reference's own; only the cut lines are new.
  headset  the band, both earcups and the mic boom: a separate piece that rides on the head (and can fly off)
  head     the fedora, mask and face (pivots at the neck); under the left earcup it carries a hidden fill of face blue
  torso    coat, shirt, TECH GUY badge and belt, with hidden fills under the gloves (the coat, copied from just below)
  handL / handR  the gloves, separate so he can rub his hands together
  legL / legR
usage: python3 tools/cut_tech.py   (reads assets/wwyd/tech_ref.png, writes tech_*.png + tech_parts.json)"""
import numpy as np, json
from PIL import Image, ImageDraw
D = 'assets/wwyd/'
A = np.array(Image.open(D + 'tech_ref.png').convert('RGB')).astype(np.float32); H, W, _ = A.shape
def dil(m, r):
    o = m.copy()
    for _ in range(r):
        n = o.copy(); n[1:] |= o[:-1]; n[:-1] |= o[1:]; n[:, 1:] |= o[:, :-1]; n[:, :-1] |= o[:, 1:]; o = n
    return o
def ero(m, r): return ~dil(~m, r)
bg = np.median(np.concatenate([A[:40, :40].reshape(-1, 3), A[:40, -40:].reshape(-1, 3), A[-40:, :40].reshape(-1, 3)]), 0)
fg = np.sqrt(((A - bg) ** 2).sum(2)) > 34
wall = dil(fg, 2); out = np.zeros_like(fg); out[0, :] = out[-1, :] = out[:, 0] = out[:, -1] = True; out &= ~wall
while True:
    n = dil(out, 1) & ~wall
    if (n == out).all(): break
    out = n
body = ero(dil(~dil(out, 2), 1), 1)
def poly(pts):
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).polygon([tuple(map(float, p)) for p in pts], fill=255); return np.array(m) > 0
def line(pts, w):
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).line([tuple(map(float, p)) for p in pts], fill=255, width=w, joint='curve'); return np.array(m) > 0
body &= poly([(540, 95), (1110, 95), (1110, 870), (540, 870)])   # the figure only
yy = np.arange(H)[:, None] + np.zeros((1, W), int); xx = np.arange(W)[None, :] + np.zeros((H, 1), int)
NECK, LEGS_Y = (835, 468), 772
cupL = poly([(565, 275), (708, 275), (708, 452), (565, 452)])
band = line([(600, 290), (612, 220), (650, 160), (720, 122), (800, 108), (880, 114), (950, 150), (995, 215), (1005, 290), (995, 340)], 46)
cupR = poly([(950, 310), (1012, 310), (1012, 440), (950, 440)])
mic = line([(990, 360), (975, 405), (940, 425), (912, 428)], 30) | poly([(895, 402), (940, 402), (940, 450), (895, 450)])
hat_top = poly([(700, 125), (980, 125), (1060, 250), (660, 250)])   # where the band crosses the crown, the hat stays on top
headset = body & (cupL | cupR | mic | (band & ~(hat_top & (yy > 135))))
headset &= ~poly([(880, 455), (1000, 455), (1000, 520), (880, 520)])   # not the coat collar under the mic
head = body & poly([(560, 100), (1080, 100), (1080, 470), (560, 470)]) & ~headset & (yy < 480)
glove = dil((A[..., 2] > 150) & (A[..., 0] < 110) & (A[..., 2] - A[..., 1] > 50), 3)
handL = body & glove & poly([(680, 530), (800, 530), (800, 650), (680, 650)])
handR = body & glove & poly([(880, 530), (990, 530), (990, 650), (880, 650)])
legs = body & (yy >= LEGS_Y) & ~poly([(560, 760), (700, 760), (660, 830), (560, 830)]) & ~poly([(980, 740), (1100, 740), (1100, 830), (1010, 830)])
legL = legs & (xx < 835); legR = legs & (xx >= 835)
torso = body & ~head & ~headset & ~handL & ~handR & ~legL & ~legR
torso |= head & (yy >= 430) & (xx > 740) & (xx < 930)   # the hidden chin
RGB = {k: A.copy() for k in ('head', 'torso')}
fill = dil(cupL, 2) & poly([(600, 280), (720, 280), (720, 450), (600, 450)]) & ~headset   # under the left earcup: face blue (head)
face = A[(yy > 360) & (yy < 440) & (xx > 760) & (xx < 880) & (A[..., 2] > 150) & (A[..., 0] < 100)]
blue = np.median(face, 0) if len(face) else np.array([30, 90, 210.])
fz = dil(cupL & body, 1) & poly([(600, 280), (720, 280), (720, 452), (600, 452)]); RGB['head'][fz] = blue; head |= fz & ~(yy < 290)
for hm, dy in ((handL, 115), (handR, 120)):   # under each glove: the same coat, just below
    f = dil(hm, 3); ys, xs = np.nonzero(f); ok = ys + dy < H; RGB['torso'][ys[ok], xs[ok]] = A[ys[ok] + dy, xs[ok]]; torso |= f & body
parts = dict(headset=headset, head=head, torso=torso, handL=handL, handR=handR, legL=legL, legR=legR)
piv = dict(headset=NECK, head=NECK, torso=(835, 840), handL=(740, 590), handR=(935, 590), legL=(760, LEGS_Y), legR=(905, LEGS_Y))
meta = {'ref': [W, H], 'feet': [835, 840], 'parts': {}}
for k, m in parts.items():
    ys, xs = np.nonzero(m); x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    src = RGB.get(k, A)
    Image.fromarray(np.dstack([src.astype(np.uint8), (m * 255).astype(np.uint8)])[y0:y1, x0:x1]).save(f'{D}tech_{k}.png')
    meta['parts'][k] = {'x': int(x0), 'y': int(y0), 'w': int(x1 - x0), 'h': int(y1 - y0), 'pivot': list(piv[k])}
json.dump(meta, open(D + 'tech_parts.json', 'w'), indent=1)
arr = np.full((H, W, 3), 255, np.uint8); cols = [(255, 170, 0), (255, 80, 80), (80, 80, 255), (200, 0, 200), (0, 180, 180), (120, 60, 0), (90, 90, 90)]
for (k, m), col in zip(parts.items(), cols): arr[m] = col
Image.fromarray(arr[95:870, 540:1110]).save('/tmp/claude-0/-home-user-Rossen/3fdd0da9-e341-56c5-b3c5-1d0ea82e103b/scratchpad/tech_parts.png')
print({k: (v['x'], v['y'], v['w'], v['h']) for k, v in meta['parts'].items()})
