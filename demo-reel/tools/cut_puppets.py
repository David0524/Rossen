"""Cut the demo reel's four hosts into jointed paper-cutout puppets. The pixels are the references' own (ref/*); only the
cut lines are new. Each moving piece leaves a hidden fill behind it on the piece underneath, so a turn never opens a hole.
  raj    head, arm (clipboard, hand and forearm; pivots at the elbow), torso (with the hand in his pocket), two legs
  maya   head (bun and hoops), arm (piggy bank, hand and forearm; pivots at the elbow), torso (hand on hip), two legs
usage: python3 tools/cut_puppets.py [name ...]   ->  assets/<name>_<part>.png + assets/<name>_parts.json"""
import numpy as np, json, sys, os
from PIL import Image, ImageDraw
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
CHECK = os.path.join(ROOT, '_check', 'cuts') + '/'   # a visual check of each cut (not committed)
CFG = {
  'raj': dict(
    head=[(355, 75), (605, 75), (605, 318), (565, 340), (520, 352), (470, 348), (425, 330), (380, 300), (355, 250)],
    arm=[(283, 446), (432, 438), (480, 520), (480, 702), (360, 714), (272, 708), (258, 650), (272, 560)],
    legs_y=762, split_x=505, chin=((425, 290, 575, 352)), fill_from=(400, 380, 460, 420),
    piv=dict(head=(495, 346), arm=(300, 690), legL=(445, 765), legR=(565, 765), torso=(495, 1470)), feet=(495, 1470)),
  'maya': dict(
    head=[(290, 70), (660, 70), (660, 425), (610, 452), (545, 474), (478, 472), (420, 448), (372, 420), (290, 345)],
    arm=[(585, 568), (772, 566), (842, 598), (848, 722), (804, 784), (640, 796), (582, 762)],
    legs_y=900, split_x=540, chin=((430, 420, 610, 476)), fill_from=(470, 800, 520, 850),
    piv=dict(head=(505, 470), arm=(805, 662), legL=(440, 902), legR=(640, 902), torso=(540, 1455)), feet=(540, 1455)),
}
def dil(m, r):
    o = m.copy()
    for _ in range(r):
        n = o.copy(); n[1:] |= o[:-1]; n[:-1] |= o[1:]; n[:, 1:] |= o[:, :-1]; n[:, :-1] |= o[:, 1:]; o = n
    return o
def ero(m, r): return ~dil(~m, r)
for name in (sys.argv[1:] or list(CFG)):
    C = CFG[name]; A = np.array(Image.open(f'{ROOT}/ref/{name}_ref.webp').convert('RGB')).astype(np.float32); H, W, _ = A.shape
    bg = np.median(np.concatenate([A[:40, :40].reshape(-1, 3), A[:40, -40:].reshape(-1, 3), A[-40:, :40].reshape(-1, 3), A[-40:, -40:].reshape(-1, 3)]), 0)
    fg = np.sqrt(((A - bg) ** 2).sum(2)) > 30
    wall = dil(fg, 2); out = np.zeros_like(fg); out[0, :] = out[-1, :] = out[:, 0] = out[:, -1] = True; out &= ~wall
    while True:   # the paper: flood-filled from the edges up to the ink
        n = dil(out, 1) & ~wall
        if (n == out).all(): break
        out = n
    body = ero(dil(~dil(out, 2), 1), 1)
    lab = np.zeros((H, W), bool)   # keep the figure's own blob only (drop paper specks)
    ys, xs = np.nonzero(body); cy, cx = int(np.median(ys)), int(np.median(xs))
    from collections import deque
    q = deque([(cy, cx)]); lab[cy, cx] = True
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            yy_, xx_ = y + dy, x + dx
            if 0 <= yy_ < H and 0 <= xx_ < W and body[yy_, xx_] and not lab[yy_, xx_]: lab[yy_, xx_] = True; q.append((yy_, xx_))
    body = lab
    def poly(pts):
        m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).polygon([tuple(map(float, p)) for p in pts], fill=255); return np.array(m) > 0
    yy = np.arange(H)[:, None] + np.zeros((1, W), int); xx = np.arange(W)[None, :] + np.zeros((H, 1), int)
    head = poly(C['head']) & body
    arm = poly(C['arm']) & body & ~head
    legs = body & (yy >= C['legs_y']) & ~arm
    legL = legs & (xx < C['split_x']); legR = legs & (xx >= C['split_x'])
    torso = body & ~head & ~arm & ~legL & ~legR
    x0, y0, x1, y1 = C['chin']; torso |= head & (yy >= y0) & (xx >= x0) & (xx <= x1)   # the hidden chin
    RGB = {'torso': A.copy()}
    hole = dil(arm, 2) & ero(dil(body, 6), 6) & ~head   # under the arm: the clothing's own colour, so a turn shows no hole
    fx0, fy0, fx1, fy1 = C['fill_from']; col = np.median(A[fy0:fy1, fx0:fx1].reshape(-1, 3), 0)
    RGB['torso'][hole & ~torso] = col; torso |= hole
    parts = dict(legL=legL, legR=legR, torso=torso, arm=arm, head=head)
    meta = {'ref': [W, H], 'feet': list(C['feet']), 'parts': {}}
    os.makedirs(f'{ROOT}/assets', exist_ok=True); os.makedirs(CHECK, exist_ok=True)
    for k, m in parts.items():
        ys, xs = np.nonzero(m); a0, a1, b0, b1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
        src = RGB.get(k, A)
        Image.fromarray(np.dstack([src.astype(np.uint8), (m * 255).astype(np.uint8)])[b0:b1, a0:a1]).save(f'{ROOT}/assets/{name}_{k}.png')
        meta['parts'][k] = {'x': int(a0), 'y': int(b0), 'w': int(a1 - a0), 'h': int(b1 - b0), 'pivot': list(C['piv'][k])}
    json.dump(meta, open(f'{ROOT}/assets/{name}_parts.json', 'w'), indent=1)
    viz = np.full((H, W, 3), 255, np.uint8); cols = {'legL': (120, 60, 0), 'legR': (90, 90, 90), 'torso': (80, 80, 255), 'arm': (0, 180, 180), 'head': (255, 80, 80)}
    for k, m in parts.items(): viz[m] = cols[k]
    Image.fromarray(np.concatenate([viz, A.astype(np.uint8)], 1)).resize((W, H // 2)).save(f'{CHECK}{name}_cut.png')
    print(name, {k: (v['x'], v['y'], v['w'], v['h']) for k, v in meta['parts'].items()})
