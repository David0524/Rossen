"""Masks for the Friday tease's last bar: the LIVE TODAY loop's pieces (logo, LIVE TODAY, the time card, FRIDAY, Jeff),
cut from the loop's own frames. A piece is every pixel where the loop frame differs from its bare background (the tease
page's ?plate=1 render, same code and seed), taken over loop frames 102-119 (the signal ring has faded there), cleaned of
isolated specks, grown 30 px to cover the beat pulses and Jeff's wave, split into bands, and feathered.
usage: node render.mjs --html rossen-tease-friday.html --query plate=1 --only 0 ; cp out/rossen-tease-friday_check/frames/0000.png assets/tease/loop_plate.png ; python3 tools/make_tease_masks.py"""
import numpy as np, json
from PIL import Image, ImageFilter
P = np.array(Image.open('assets/tease/loop_plate.png').convert('RGB')).astype(int)
U = np.zeros(P.shape[:2], bool)
for i in range(102, 120):
    f = np.array(Image.open(f'out/rossen-loop-friday/frames/{i:04d}.png').convert('RGB')).astype(int); U |= np.abs(f - P).sum(2) > 30
img = lambda m: Image.fromarray((m * 255).astype(np.uint8))
dens = np.array(img(U).filter(ImageFilter.BoxBlur(10))).astype(int) > 60
body = np.array(img(dens).filter(ImageFilter.MaxFilter(61))) > 0
ys = np.arange(U.shape[0])[:, None] + np.zeros((1, U.shape[1]), int)
BANDS = [('logo', 0, 700), ('live', 700, 886), ('card', 886, 1104), ('day', 1104, 1210), ('jeff', 1210, 1920)]
out = {'pieces': []}
for name, y0, y1 in BANDS:
    m = body & (ys >= y0) & (ys < y1)
    a = np.array(img(m).filter(ImageFilter.GaussianBlur(3)))
    rgba = np.zeros(m.shape + (4,), np.uint8); rgba[..., 3] = a
    Image.fromarray(rgba).save(f'assets/tease/loop_mask_{name}.png')
    yy, xx = np.nonzero(m); out['pieces'].append({'name': name, 'file': f'loop_mask_{name}.png', 'centre': [float(xx.mean()) * 1080 / 1080, float((yy.min() + yy.max()) / 2)]})
    print(name, 'px', int(m.sum()), 'bbox', xx.min(), yy.min(), xx.max(), yy.max())
json.dump(out, open('assets/tease/loop_masks.json', 'w'), indent=1)
