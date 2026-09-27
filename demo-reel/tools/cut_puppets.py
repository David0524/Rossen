"""Cut the demo reel's four hosts into jointed paper-cutout puppets. The pixels are the references' own (ref/*); only the
cut lines are new. Each moving piece leaves a hidden fill behind it on the piece underneath, so a turn never opens a hole.
  raj    head, arm (clipboard, hand and forearm; pivots at the elbow), torso (with the hand in his pocket), two legs
  maya   head (bun and hoops), arm (piggy bank, hand and forearm; pivots at the elbow), torso (hand on hip), two legs
  hana   head (bun and the pencil in it), arm (the pencil hand; pivots at the wrist), arm2 (the notebook hand; pivots at the
         wrist), torso, two legs
  diego  head (the hat and its white sticker border), torso (both hands on the backpack straps), two legs, and a second
         head drawing, head_uhoh: the same head with the smile repainted as a worried "o" (his skin and outline colours)
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
  'hana': dict(
    head=[(300, 60), (620, 60), (620, 262), (582, 300), (548, 318), (508, 325), (470, 315), (445, 302), (405, 314), (335, 302), (316, 262)],
    arm=[(405, 418), (522, 418), (522, 528), (492, 560), (458, 574), (420, 572), (404, 542)],
    arm2=[(508, 450), (664, 446), (670, 522), (638, 600), (598, 616), (548, 614), (505, 594)],
    legs_y=760, split_x=548, chin=((462, 282, 560, 327)), fill_from=(330, 470, 360, 500),
    piv=dict(head=(510, 322), arm=(440, 568), arm2=(600, 606), legL=(470, 765), legR=(620, 765), torso=(548, 1455)), feet=(548, 1455)),
  'diego': dict(
    head=[(340, 80), (694, 80), (694, 262), (642, 332), (602, 380), (562, 402), (510, 404), (462, 388), (418, 352), (378, 332), (340, 300)],
    legs_y=1046, split_x=527, chin=((468, 360, 604, 405)), fill_from=None,
    piv=dict(head=(535, 396), legL=(450, 1050), legR=(610, 1050), torso=(525, 1482)), feet=(525, 1482),
    uhoh=dict(mouth=(510, 302, 590, 350), skin=(236, 145, 64), o=(552, 330, 13, 16))),
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
    arms = {}; taken = head.copy()
    for k in ('arm', 'arm2'):
        if k in C: arms[k] = poly(C[k]) & body & ~taken; taken |= arms[k]
    anyarm = np.zeros_like(body)
    for m in arms.values(): anyarm |= m
    legs = body & (yy >= C['legs_y']) & ~anyarm
    legL = legs & (xx < C['split_x']); legR = legs & (xx >= C['split_x'])
    torso = body & ~head & ~anyarm & ~legL & ~legR
    x0, y0, x1, y1 = C['chin']; torso |= head & (yy >= y0) & (xx >= x0) & (xx <= x1)   # the hidden chin
    RGB = {'torso': A.copy()}
    if arms:   # under each arm: the clothing's own colour, so a turn shows no hole
        hole = dil(anyarm, 2) & ero(dil(body, 6), 6) & ~head
        fx0, fy0, fx1, fy1 = C['fill_from']; col = np.median(A[fy0:fy1, fx0:fx1].reshape(-1, 3), 0)
        RGB['torso'][hole & ~torso] = col; torso |= hole
    parts = dict(legL=legL, legR=legR, torso=torso, **arms, head=head)
    meta = {'ref': [W, H], 'feet': list(C['feet']), 'parts': {}}
    os.makedirs(f'{ROOT}/assets', exist_ok=True); os.makedirs(CHECK, exist_ok=True)
    for k, m in parts.items():
        ys, xs = np.nonzero(m); a0, a1, b0, b1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
        src = RGB.get(k, A)
        Image.fromarray(np.dstack([src.astype(np.uint8), (m * 255).astype(np.uint8)])[b0:b1, a0:a1]).save(f'{ROOT}/assets/{name}_{k}.png')
        meta['parts'][k] = {'x': int(a0), 'y': int(b0), 'w': int(a1 - a0), 'h': int(b1 - b0), 'pivot': list(C['piv'][k])}
    if 'uhoh' in C:   # the worried face: the smile painted over in skin, a small open "o" drawn in his own outline style
        U = C['uhoh']; m = parts['head']; ys, xs = np.nonzero(m); a0, b0 = xs.min(), ys.min()
        im = Image.fromarray(np.dstack([A.astype(np.uint8), (m * 255).astype(np.uint8)])).convert('RGBA'); d = ImageDraw.Draw(im)
        x0, y0, x1, y1 = U['mouth']; d.ellipse((x0, y0, x1, y1), fill=tuple(U['skin']) + (255,))
        ox, oy, rx, ry = U['o']; d.ellipse((ox - rx - 4, oy - ry - 4, ox + rx + 4, oy + ry + 4), fill=(17, 17, 17, 255)); d.ellipse((ox - rx, oy - ry, ox + rx, oy + ry), fill=(150, 40, 30, 255))
        d.ellipse((ox - rx * .55, oy + ry * .15, ox + rx * .55, oy + ry * .85), fill=(214, 92, 72, 255))
        im.crop((a0, b0, xs.max() + 1, ys.max() + 1)).save(f'{ROOT}/assets/{name}_head_uhoh.png'); meta['alt'] = {'head_uhoh': 'head'}
    # the lineup sticker: the whole figure, die-cut with a white border (Diego's art already has its own)
    from PIL import ImageFilter   # a rounded dilation: blur the silhouette, keep everything the blur reaches
    cut = body if name == 'diego' else np.array(Image.fromarray((body * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(11))) > 14
    ys, xs = np.nonzero(cut); a0, a1, b0, b1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    rgb = A.copy(); rgb[cut & ~body] = 255
    Image.fromarray(np.dstack([rgb.astype(np.uint8), (cut * 255).astype(np.uint8)])[b0:b1, a0:a1]).save(f'{ROOT}/assets/{name}_sticker.png'); meta['sticker'] = [int(a0), int(b0), int(a1 - a0), int(b1 - b0)]
    json.dump(meta, open(f'{ROOT}/assets/{name}_parts.json', 'w'), indent=1)
    viz = np.full((H, W, 3), 255, np.uint8); cols = {'legL': (120, 60, 0), 'legR': (90, 90, 90), 'torso': (80, 80, 255), 'arm': (0, 180, 180), 'arm2': (200, 160, 0), 'head': (255, 80, 80)}
    for k, m in parts.items(): viz[m] = cols[k]
    Image.fromarray(np.concatenate([viz, A.astype(np.uint8)], 1)).resize((W, H // 2)).save(f'{CHECK}{name}_cut.png')
    print(name, {k: (v['x'], v['y'], v['w'], v['h']) for k, v in meta['parts'].items()})
