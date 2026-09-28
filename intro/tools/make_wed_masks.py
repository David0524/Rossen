"""Masks for the Wednesday tease's last bar: the LIVE TODAY loop's pieces (logo, LIVE TODAY, the time card, WEDNESDAY, LIVE ON YOUTUBE,
Jeff), cut from the delivered loop's own frames (decoded from final-videos/09, read-only; the loop itself is never re-rendered). A piece is every pixel where the loop frame differs from its bare background (the tease
page's ?plate=1 render, same code and seed), taken over loop frames 102-119 (the signal ring has faded there), cleaned of
isolated specks, grown 30 px to cover the beat pulses and Jeff's wave, split into bands, and feathered.
usage: ffmpeg -i "../final-videos/09 Live Today Loop - Wednesday 5 PM (9x16).mp4" -start_number 0 out/rossen-loop-wednesday/frames/%04d.png
       node render.mjs --html rossen-tease-wednesday.html --query plate=1 --only 0 ; cp out/rossen-tease-wednesday_check/frames/0000.png assets/wedtease/loop_plate.png
       python3 tools/make_wed_masks.py"""
import numpy as np, json
LOOP = 'out/rossen-loop-wednesday'   # the Wednesday 5 PM loop, decoded
from PIL import Image, ImageFilter
P = np.array(Image.open('assets/wedtease/loop_plate.png').convert('RGB')).astype(int)
U = np.zeros(P.shape[:2], bool)
for i in range(102, 120):
    f = np.array(Image.open(f'{LOOP}/frames/{i:04d}.png').convert('RGB')).astype(int); U |= np.abs(f - P).sum(2) > 90   # decoded frames: the halftone edges carry up to ~60 of codec noise
img = lambda m: Image.fromarray((m * 255).astype(np.uint8))
dens = np.array(img(U).filter(ImageFilter.BoxBlur(10))).astype(int) > 60
body = np.array(img(dens).filter(ImageFilter.MaxFilter(61))) > 0
ys = np.arange(U.shape[0])[:, None] + np.zeros((1, U.shape[1]), int)
BANDS = [('logo', 0, 700), ('live', 700, 886), ('card', 886, 1104), ('day', 1104, 1204), ('youtube', 1204, 1318), ('jeff', 1318, 1920)]
out = {'pieces': []}
for name, y0, y1 in BANDS:
    m = body & (ys >= y0) & (ys < y1)
    a = np.array(img(m).filter(ImageFilter.GaussianBlur(3)))
    rgba = np.zeros(m.shape + (4,), np.uint8); rgba[..., 3] = a
    Image.fromarray(rgba).save(f'assets/wedtease/loop_mask_{name}.png')
    yy, xx = np.nonzero(m); out['pieces'].append({'name': name, 'file': f'loop_mask_{name}.png', 'centre': [float(xx.mean()) * 1080 / 1080, float((yy.min() + yy.max()) / 2)]})
    print(name, 'px', int(m.sum()), 'bbox', xx.min(), yy.min(), xx.max(), yy.max())
json.dump(out, open('assets/wedtease/loop_masks.json', 'w'), indent=1)
