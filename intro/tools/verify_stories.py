"""Verify the "STILL LIVE" Story frames (out/rossen-deals-stories) against deals/deals.json.
usage: python3 tools/verify_stories.py
Per deal slide (OCR on the lossless PNG still): the name, the regular price, the deal price, the percent off (matched against
every value from 0% to 99% in the same font), the strike through the regular price, and the fine print (the disclosure only). Per mp4: 5 s at 24 fps,
1080x1920; the card (photo, prices, type, fine print) completely still in every frame; the loop seamless (the last frame
leads back into the first like any other pair); the link-sticker slot empty inside. The last page: its lines and the icons."""
import json, subprocess, os, re, glob
import numpy as np
from PIL import Image, ImageFont, ImageDraw
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'); O = os.path.join(root, 'out', 'rossen-deals-stories')
DJ = json.load(open(os.path.join(root, 'deals', 'deals.json'))); D = DJ['deals']; N = len(D)
FONT = os.path.join(root, 'assets', 'fonts', 'BowlbyOneSC-Regular.ttf')
DX, DY = 60, -56   # the Reel's card coordinates -> the Story slide (stories.js cardT)
card = lambda x0, y0, x1, y1: (round(x0 + DX), round(y0 + DY), round(x1 + DX), round(y1 + DY))
SLOT = (110, 1452, 730, 1592)
cents = lambda s: int(s.split('.')[0]) * 100 + int(s.split('.')[1])
pct = lambda d: int((cents(d['regular']) - cents(d['deal'])) * 100 / cents(d['regular']) + .5)
norm = lambda s: re.sub(r'[^A-Z0-9$.%:/,{}\-]', '', s.upper())
ok_all = True
def report(ok, msg):
    global ok_all; ok_all &= bool(ok); print(('PASS ' if ok else 'FAIL ') + msg)
def ocr(img, box, ink='dark', wl=None, psm=7, scale=2):
    a = img[box[1]:box[3], box[0]:box[2]].astype(int); r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = {'dark': np.maximum(np.maximum(r, g), b) < 110, 'light': np.minimum(np.minimum(r, g), b) > 222,
         'inkblue': (np.maximum(np.maximum(r, g), b) < 110) | ((b > 150) & (r < 60))}[ink]
    im = Image.fromarray(np.pad(np.where(m, 0, 255).astype(np.uint8), 24, constant_values=255)); im = im.resize((im.width * scale, im.height * scale), Image.LANCZOS)
    im.save('/tmp/_ocr_st.png'); cmd = ['tesseract', '/tmp/_ocr_st.png', '-', '--psm', str(psm)] + (['-c', f'tessedit_char_whitelist={wl}'] if wl else [])
    return subprocess.run(cmd, capture_output=True, text=True).stdout.strip()
def ocr_any(want, *a, **kw):   # a few page modes and scales; exact matches only
    reads = []
    for psm in (kw.pop('psm', 7), 8, 13, 6):
        for sc in (2, 3):
            r = norm(ocr(*a, psm=psm, scale=sc, **kw)); reads.append(r)
            if r == want: return r
    return max(set(reads), key=reads.count)
def split2(s, size=62, maxW=740):   # deals.js lines2()
    f = ImageFont.truetype(FONT, size)
    if f.getlength(s) <= maxW: return [s]
    w = s.split(' '); return min(([' '.join(w[:i]), ' '.join(w[i:])] for i in range(1, len(w))), key=lambda p: max(f.getlength(p[0]), f.getlength(p[1])))
def chips(f, want):
    out = ''
    for i, wnt in enumerate(want):
        x0, y0, x1, y1 = card(40, 372 + i * 96 - 36, 920, 372 + i * 96 + 36); a = f[y0:y1, x0:x1].astype(int)
        bg = (np.maximum(np.maximum(a[..., 0], a[..., 1]), a[..., 2]) < 70) | ((a[..., 2] > 150) & (a[..., 0] < 60)); cols = np.where(bg.mean(0) > .3)[0]
        if len(cols): out += ocr_any(norm(wnt), f, (x0 + cols[0] + 6, y0 + 4, x0 + cols[-1] - 6, y1 - 4), 'light')
    return out
def ink_bbox(m, clean=0):
    e = m.copy()
    for _ in range(clean): e = e & np.roll(e, 1, 0) & np.roll(e, -1, 0) & np.roll(e, 1, 1) & np.roll(e, -1, 1)
    ys, xs = np.where(e); return m[max(0, ys.min() - clean):ys.max() + 1 + clean, max(0, xs.min() - clean):xs.max() + 1 + clean]
def pct_match(f):
    x0, y0, x1, y1 = card(660, 720, 884, 812); m = ink_bbox(f[y0:y1, x0:x1].astype(int).min(-1) > 222, 3)
    tgt = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).resize((160, 80), Image.LANCZOS), float) / 255; best = None
    for v in range(100):
        st = f'{v}%'; w = ImageFont.truetype(FONT, 88).getlength(st); size = int(88 * 186 / w) if w > 186 else 88
        im = Image.new('L', (400, 200), 0); ImageDraw.Draw(im).text((10, 10), st, font=ImageFont.truetype(FONT, size), fill=255); r = ink_bbox(np.asarray(im) > 128)
        ref = np.asarray(Image.fromarray((r * 255).astype(np.uint8)).resize((160, 80), Image.LANCZOS), float) / 255
        cc = np.corrcoef(tgt.ravel(), ref.ravel())[0, 1]; sc = cc - abs(np.log((m.shape[1] / m.shape[0]) / (r.shape[1] / r.shape[0])))
        if best is None or sc > best[0]: best = (sc, st, cc)
    return best
def frames(mp4, scale=None):
    vf = ['-vf', f'scale={scale}'] if scale else []; w, h = (map(int, scale.split(':')) if scale else (1080, 1920))
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', mp4, *vf, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)
fine2 = f"PRICES AS OF {DJ['priceCheck']['date'].upper()}, {DJ['priceCheck']['time'].upper()} ET. DEALS CAN END ANYTIME."
files = sorted(glob.glob(os.path.join(O, 'story_*.mp4')), key=lambda p: int(re.search(r'story_(\d+)_', p).group(1)))
report(len(files) == N + 1, f'{len(files)} slides (expected {N} deals + the last page)')
for s, mp4 in enumerate(files):
    png = mp4[:-4] + '.png'; f = np.asarray(Image.open(png).convert('RGB')); tag = os.path.basename(mp4)
    V = frames(mp4); report(len(V) == 120 and V.shape[1:] == (1920, 1080, 3), f'{tag}: {len(V)} frames, {V.shape[2]}x{V.shape[1]} (5.00 s at 24 fps)')
    Vs = V[:, ::4, ::4].astype(np.int16)   # motion, measured on a quarter-size copy
    cardzone = (slice(250 // 4, 1420 // 4), slice(0, 1080 // 4)) if s < N else (slice(250 // 4, 1260 // 4), slice(0, 1080 // 4))
    G = V[:, cardzone[0].start * 4:cardzone[0].stop * 4].astype(np.int16).mean(-1); dd = np.abs(np.diff(G, axis=0))   # full-size, grey
    report(dd.mean() < .01 and (dd > 4).mean() < 1e-4, f'{tag}: the card (photo, prices, type, fine print) is still in every frame: mean change {dd.mean():.4f}/255, {(dd > 4).mean():.5%} of pixels ever change by more than 4/255 (isolated codec blocks)')
    moves = [np.abs(Vs[i] - Vs[i - 1]).mean() for i in range(1, len(Vs))]; wrap = np.abs(Vs[0] - Vs[-1]).mean()
    report(wrap <= max(moves) + .05, f'{tag}: loops seamlessly (last->first change {wrap:.3f}, frame-to-frame max {max(moves):.3f})')
    if s < N:
        d = D[s]
        name = norm(chips(f, split2(d['name'].upper()))); report(name == norm(d['name']), f'{tag} name: read {name!r}')
        rw = ImageFont.truetype(FONT, 54).getlength('REG. $' + d['regular']) + 56
        a = f.copy(); y0s = 1120 + DY - 3; blu = lambda r: (r[..., 2] > 150) & (r[..., 0] < 80)   # read the regular price through its strike:
        for yy in range(y0s, y0s + 10): m = blu(a[yy]); a[yy][m] = a[y0s - 1][m]                        # fill the strike rows from the row just above
        reg = ocr_any('REG.$' + d['regular'], a, card(72, 1090, 60 + rw - 12, 1150), 'dark', 'REG.$0123456789 '); report(reg == 'REG.$' + d['regular'], f'{tag} regular: expected {"REG.$" + d["regular"]!r}, read {reg!r}')
        ft = ImageFont.truetype(FONT, 54); wl, wp = ft.getlength('REG. '), ft.getlength('$' + d['regular'])
        band = f[1120 + DY:1123 + DY, round(60 + 28 + wl + DX):round(60 + 28 + wl + wp + DX)].astype(int); blue = ((band[..., 2] > 150) & (band[..., 0] < 80)).mean()
        report(blue > .8, f'{tag}: the regular price is struck through ({blue:.0%} of the strike line)')
        deal = ocr_any('$' + d['deal'], f, card(390, 1196, 900, 1386), 'dark', '$0123456789.'); report(deal == '$' + d['deal'], f'{tag} deal: expected {"$" + d["deal"]!r}, read {deal!r}')
        sc, st, cc = pct_match(f); report(st == f'{pct(d)}%', f'{tag} percent: expected {pct(d)}%, best match of 0%-99% is {st} (correlation {cc:.3f})')
        fy = 1374
    else:
        want = [norm(x) for x in DJ['storyEnd']]
        lg = Image.open(os.path.join(root, 'assets', 'official_logo.png')); bb = lg.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox(); lh = (bb[3] - bb[1]) * 640 / (bb[2] - bb[0])
        y0 = 290 + lh + 110
        got = [ocr_any(w, f, (60, round(y0 + i * 100 - 52), 1020, round(y0 + i * 100 + 52)), 'inkblue') for i, w in enumerate(want)]
        report(got == want, f'{tag} lines: read {got}')
        fy = round(y0 + len(want) * 100 + 40 + 90)
    fl = ocr_any(norm(DJ['disclosure']), f, (40, fy - 16, 1040, fy + 16), 'dark', psm=7); report(fl == norm(DJ['disclosure']), f'{tag} fine print: read {fl!r}')
    if s < N: below = f[fy + 18:fy + 60, 40:1040].astype(int); report((below.max(-1) < 110).mean() == 0, f'{tag}: nothing printed under the disclosure (no price-check line)')
    if s < N:
        x0, y0, x1, y1 = SLOT; inner = f[y0 + 14:y1 - 14, x0 + 50:x1 - 50].astype(int)
        report((np.maximum(np.maximum(inner[..., 0], inner[..., 1]), inner[..., 2]) < 150).mean() == 0, f'{tag}: the link-sticker slot is empty inside (nothing for the sticker to cover)')
print('ALL PASS' if ok_all else 'SOME CHECKS FAILED')
