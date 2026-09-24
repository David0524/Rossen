"""Cut the WHAT WOULD YOU DO? characters (Grandma, the Grandson) into paper-cutout puppet parts with pivots:
head, torso, the phone arm (hand + phone + forearm, pivoting at the elbow), two legs. The pixels are the reference's own;
only the cut lines are new. Like the Jeff and Scammer cutters, the torso carries a hidden copy of the chin under the head
so a head tilt never opens a see-through slit."""
import numpy as np, json, sys
from PIL import Image, ImageDraw
CFG = {
  'grandma': dict(
    head=[(560, 60), (1060, 60), (1060, 390), (985, 392), (940, 405), (922, 440), (850, 447), (760, 447), (700, 432), (560, 432)],
    arm=[(924, 386), (1048, 386), (1050, 562), (992, 578), (934, 566), (922, 470)],
    legs_y=688, split_x=832, chin_y=400,
    piv=dict(head=(805, 445), arm=(975, 560), legL=(765, 690), legR=(905, 690), torso=(850, 866)), feet=(850, 866)),
  'grandson': dict(
    head=[(580, 30), (1060, 30), (1060, 306), (948, 314), (936, 352), (900, 362), (860, 376), (800, 384), (750, 372), (700, 336), (580, 336)],
    arm=[(906, 318), (1022, 318), (1022, 470), (1012, 562), (938, 572), (914, 470)],
    legs_y=650, split_x=832, chin_y=280,
    piv=dict(head=(805, 380), arm=(960, 560), legL=(765, 652), legR=(900, 652), torso=(840, 862)), feet=(840, 862)),
}
def dil(m, r):
    o = m.copy()
    for _ in range(r):
        n = o.copy(); n[1:] |= o[:-1]; n[:-1] |= o[1:]; n[:, 1:] |= o[:, :-1]; n[:, :-1] |= o[:, 1:]; o = n
    return o
def ero(m, r): return ~dil(~m, r)
for name, C in CFG.items():
    A = np.array(Image.open(f'assets/wwyd/{name}_ref.webp').convert('RGB')).astype(np.float32); H, W, _ = A.shape
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
    yy = np.arange(H)[:, None] + np.zeros((1, W), int); xx = np.arange(W)[None, :] + np.zeros((H, 1), int)
    head = poly(C['head']) & body
    arm = poly(C['arm']) & body & ~head
    legs = body & (yy >= C['legs_y']) & ~arm
    legL = legs & (xx < C['split_x']); legR = legs & (xx >= C['split_x'])
    torso = body & ~head & ~arm & ~legL & ~legR
    torso |= head & (yy >= C['chin_y'])   # the hidden chin
    ex, ey = C['piv']['arm']; torso |= arm & ((xx - ex) ** 2 + (yy - ey) ** 2 < 70 ** 2)   # a hidden copy of the sleeve at the elbow
    masks = {'legL': legL, 'legR': legR, 'torso': torso, 'arm': arm, 'head': head}
    meta = {'ref': [W, H], 'feet': list(C['feet']), 'parts': {}}
    for k, m in masks.items():
        ys, xs = np.nonzero(m); x0, y0, x1, y1 = max(0, xs.min() - 2), max(0, ys.min() - 2), min(W, xs.max() + 3), min(H, ys.max() + 3)
        rgba = np.zeros((y1 - y0, x1 - x0, 4), np.uint8); rgba[..., :3] = A[y0:y1, x0:x1]; rgba[..., 3] = m[y0:y1, x0:x1] * 255
        Image.fromarray(rgba).save(f'assets/wwyd/{name}_{k}.png')
        meta['parts'][k] = {'x': int(x0), 'y': int(y0), 'w': int(x1 - x0), 'h': int(y1 - y0), 'pivot': list(C['piv'][k])}
    json.dump(meta, open(f'assets/wwyd/{name}_parts.json', 'w'), indent=1)
    pv = np.full((H, W, 3), 90, np.uint8); cols = {'head': (255, 120, 120), 'torso': (120, 255, 120), 'arm': (255, 255, 120), 'legL': (255, 120, 255), 'legR': (120, 255, 255)}
    for k in ('torso', 'legL', 'legR', 'arm', 'head'): pv[masks[k]] = (A[masks[k]] * .5 + np.array(cols[k]) * .5).astype(np.uint8)
    Image.fromarray(pv).save(f'/tmp/claude-0/-home-user-Rossen/3fdd0da9-e341-56c5-b3c5-1d0ea82e103b/scratchpad/{name}_parts.png')
    print(name, {k: int(m.sum()) for k, m in masks.items()})
