"""Cut the fake-officer explainer's characters into paper-cutout puppet parts with pivots. The pixels are the
references' own; only the cut lines are new.
  officer (the Scammer in disguise): cap and badge as separate pieces (the disguise falls apart), head, torso,
      the phone arm (hand + handset + sleeve, pivoting at the elbow), two legs
  man (the target): head, torso, phone arm, two legs
As in the other cutters, the torso carries a hidden copy of the chin under the head and of the sleeve at the elbow,
so a tilt never opens a see-through slit. The officer also gets hidden fills: coat under the badge (copied from the
coat just below it) and a head dome under the cap (the mask's own black), so either piece can come off."""
import numpy as np, json
from PIL import Image, ImageDraw
SCR = '/tmp/claude-0/-home-user-Rossen/3fdd0da9-e341-56c5-b3c5-1d0ea82e103b/scratchpad/'
CFG = {
  'officer': dict(
    cap=[(270, 0), (1000, 0), (1000, 356), (880, 362), (824, 408), (800, 416), (700, 447), (600, 474), (500, 493), (430, 510), (405, 520), (398, 536), (360, 536), (270, 440)],
    head=[(330, 380), (815, 380), (815, 600), (800, 590), (760, 612), (700, 632), (650, 642), (600, 628), (560, 606), (470, 582), (372, 562), (330, 560)],
    arm=[(810, 432), (880, 432), (905, 485), (945, 520), (940, 575), (990, 690), (965, 725), (935, 785), (872, 792), (850, 772), (848, 640), (828, 622), (808, 618)],
    badge=[(800, 700), (848, 752), (835, 830), (740, 830), (732, 752)],
    legs_y=1040, split_x=640, chin_y=560, side_x=770,
    piv=dict(cap=(610, 440), head=(630, 640), arm=(895, 770), badge=(792, 728), legL=(520, 1040), legR=(760, 1040), torso=(650, 1125)), feet=(650, 1125)),
  'man': dict(
    head=[(630, 50), (935, 50), (935, 300), (908, 330), (872, 346), (800, 354), (748, 346), (700, 322), (630, 322)],
    arm=[(918, 316), (1040, 316), (1040, 470), (1012, 548), (940, 556), (916, 470)],
    legs_y=622, split_x=830, chin_y=290,
    piv=dict(head=(805, 350), arm=(975, 535), legL=(765, 624), legR=(885, 624), torso=(830, 862)), feet=(830, 862)),
}
def dil(m, r):
    o = m.copy()
    for _ in range(r):
        n = o.copy(); n[1:] |= o[:-1]; n[:-1] |= o[1:]; n[:, 1:] |= o[:, :-1]; n[:, :-1] |= o[:, 1:]; o = n
    return o
def ero(m, r): return ~dil(~m, r)
for name, C in CFG.items():
    A = np.array(Image.open(f'assets/officer/{name}_ref.webp').convert('RGB')).astype(np.float32); H, W, _ = A.shape
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
    cap = poly(C['cap']) & body if 'cap' in C else np.zeros_like(body)
    head = poly(C['head']) & body & ~cap
    arm = poly(C['arm']) & body & ~head & ~cap
    badge = np.zeros_like(body)
    if 'badge' in C:   # the star: its yellow ink and orange rim inside the badge outline
        yel = (A[..., 0] > 190) & (A[..., 1] > 120) & (A[..., 2] < 140)
        badge = dil(yel & poly(C['badge']), 3) & poly(C['badge']) & body & ~arm
    legs = body & (yy >= C['legs_y']) & ~arm
    legL = legs & (xx < C['split_x']); legR = legs & (xx >= C['split_x'])
    torso = body & ~head & ~arm & ~legL & ~legR & ~cap & ~badge
    torso |= head & (yy >= C['chin_y'])   # the hidden chin
    if 'side_x' in C: torso |= head & (((xx >= C['side_x']) & (yy >= 440)) | ((xx < 460) & (yy >= 510)))   # and the cheeks behind the handset and the collar tip
    ex, ey = C['piv']['arm']; torso |= arm & ((xx - ex) ** 2 + (yy - ey) ** 2 < 70 ** 2)   # a hidden copy of the sleeve at the elbow
    RGB = {k: A.copy() for k in ('torso', 'head')}
    if badge.any():   # the coat under the badge: the same coat, 115 px lower
        fill = dil(badge, 2) & poly(C['badge']); ys, xs = np.nonzero(fill); RGB['torso'][ys, xs] = A[ys + 115, xs]; torso |= fill
    if cap.any():     # the head dome under the cap: the mask's own black, tiled, with an orange rim
        cx, cy, rx, ry = 618, 500, 205, 128
        e = ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2
        dome = (e < 1) & (yy < 520) & ~head
        tile = A[900:1000, 675:725]; ys, xs = np.nonzero(dome); ty, tx = (ys - 300) % 200, (xs - 400) % 100   # the black trousers, mirror-tiled
        ty = np.where(ty >= 100, 199 - ty, ty); tx = np.where(tx >= 50, 99 - tx, tx); RGB['head'][ys, xs] = tile[ty, tx]
        rim = dome & (e > .93); RGB['head'][rim] = np.array([236, 150, 52], np.float32)
        head |= dome
    masks = {'legL': legL, 'legR': legR, 'torso': torso, 'badge': badge, 'arm': arm, 'head': head, 'cap': cap}
    masks = {k: m for k, m in masks.items() if m.any()}
    meta = {'ref': [W, H], 'feet': list(C['feet']), 'parts': {}}
    for k, m in masks.items():
        ys, xs = np.nonzero(m); x0, y0, x1, y1 = max(0, xs.min() - 2), max(0, ys.min() - 2), min(W, xs.max() + 3), min(H, ys.max() + 3)
        src = RGB.get(k, A); rgba = np.zeros((y1 - y0, x1 - x0, 4), np.uint8); rgba[..., :3] = src[y0:y1, x0:x1]; rgba[..., 3] = m[y0:y1, x0:x1] * 255
        Image.fromarray(rgba).save(f'assets/officer/{name}_{k}.png')
        meta['parts'][k] = {'x': int(x0), 'y': int(y0), 'w': int(x1 - x0), 'h': int(y1 - y0), 'pivot': list(C['piv'][k])}
    json.dump(meta, open(f'assets/officer/{name}_parts.json', 'w'), indent=1)
    pv = np.full((H, W, 3), 90, np.uint8); cols = {'head': (255, 120, 120), 'torso': (120, 255, 120), 'arm': (255, 255, 120), 'legL': (255, 120, 255), 'legR': (120, 255, 255), 'cap': (120, 120, 255), 'badge': (255, 255, 255)}
    for k in ('torso', 'legL', 'legR', 'badge', 'head', 'cap', 'arm'):
        if k in masks: pv[masks[k]] = (A[masks[k]] * .5 + np.array(cols[k]) * .5).astype(np.uint8)
    Image.fromarray(pv).save(f'{SCR}{name}_parts.png')
    print(name, {k: int(m.sum()) for k, m in masks.items()})
