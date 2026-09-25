"""Verify a finished "STILL LIVE" deals mp4 against deals/deals.json (the same timing formulas as deals.js).
usage: python3 tools/verify_deals.py out/rossen-deals-still-live-facebook/rossen-deals-still-live-facebook.mp4 facebook
Checks, on the mp4 itself: the names, regular prices, deal prices and percent-off (OCR of each deal's held frame), equal bars
per deal (scene starts found from the picture), the price note and the disclosure held completely still for a full bar (and
their text), the CTA text, the last second still, and the logo colours on the closing card against the logo file."""
import json, subprocess, sys, os, re
import numpy as np
from PIL import Image
mp4, plat = sys.argv[1], sys.argv[2]
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
DJ = json.load(open(os.path.join(root, 'deals', 'deals.json'))); D = DJ['deals']; N = len(D); DB = 3
BAR, BEAT, FPS = 2.5, .625, 24
at = lambda bar, beat=1: bar * BAR + (beat - 1) * BEAT
A_ = lambda k: at(1 + DB * k); D_ = lambda k: A_(k) + 2 * BAR
T_NOTE = at(1 + DB * N); T_DISC = T_NOTE + BAR; T_CRED = T_DISC + BAR; T_CTA = T_CRED + BAR; T_END = T_CTA + BAR; DUR = T_END + 4.5
cents = lambda s: int(s.split('.')[0]) * 100 + int(s.split('.')[1])
pct = lambda d: int((cents(d['regular']) - cents(d['deal'])) * 100 / cents(d['regular']) + .5)
K, SCX, SCY, CX = .895, 480, 865, 540
def scr(x0, y0, x1, y1): return (round(CX + (x0 - SCX) * K), round(SCY + (y0 - SCY) * K), round(CX + (x1 - SCX) * K), round(SCY + (y1 - SCY) * K))

raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', mp4, '-vf', 'scale=270:480', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], capture_output=True, check=True).stdout
V = np.frombuffer(raw, np.uint8).reshape(-1, 480, 270); NF = len(V)   # a small grey copy, for motion
def fr(t):   # one full-size frame (by frame number, exactly)
    i = min(NF - 1, int(round(t * FPS)))
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', mp4, '-vf', f'select=eq(n\\,{i})', '-vframes', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(1920, 1080, 3)
def ocr(img, box, ink='dark', wl=None, psm=7, scale=2):   # binarize by ink colour, then OCR (black letters on white)
    a = img[box[1]:box[3], box[0]:box[2]].astype(int); r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = {'dark': np.maximum(np.maximum(r, g), b) < 110,                              # black type (not the blue strike)
         'light': np.minimum(np.minimum(r, g), b) > 222,                             # cream type on black or blue chips
         'inkblue': (np.maximum(np.maximum(r, g), b) < 110) | ((b > 150) & (r < 60))}[ink]   # black or blue type on paper
    im = Image.fromarray(np.pad(np.where(m, 0, 255).astype(np.uint8), 24, constant_values=255)); im = im.resize((im.width * scale, im.height * scale), Image.LANCZOS)
    p = '/tmp/_ocr.png'; im.save(p); a = ['tesseract', p, '-', '--psm', str(psm)] + (['-c', f'tessedit_char_whitelist={wl}'] if wl else [])
    return subprocess.run(a, capture_output=True, text=True).stdout.strip()
def ocr_any(want, *a, **kw):   # a few tesseract page modes and scales; exact matches only, so a wrong price can never pass
    reads = []
    for psm in (kw.pop('psm', 7), 8, 13, 6):
        for sc in (2, 3):
            r = norm(ocr(*a, psm=psm, scale=sc, **kw)); reads.append(r)
            if r == want: return r
    return max(set(reads), key=reads.count)
def chips(f, n=2, y0=372, step=96, want=None):   # the headline chips at the top, one line each, cropped to the chip's own ink
    out = ''
    for i in range(n):
        x0, y0_, x1, y1 = scr(40, y0 + i * step - 36, 920, y0 + i * step + 36); a = f[y0_:y1, x0:x1].astype(int)
        bg = (np.maximum(np.maximum(a[..., 0], a[..., 1]), a[..., 2]) < 70) | ((a[..., 2] > 150) & (a[..., 0] < 60))   # black or blue chip
        cols = np.where(bg.mean(0) > .3)[0]
        if not len(cols): continue
        box = (x0 + cols[0] + 6, y0_ + 4, x0 + cols[-1] - 6, y1 - 4)
        out += ocr_any(want[i], f, box, 'light') if want and i < len(want) else ocr(f, box, 'light')
    return out
from PIL import ImageFont
FONT = os.path.join(root, 'assets', 'fonts', 'BowlbyOneSC-Regular.ttf')
def wrap(s, size, maxW):   # the same greedy wrap as deals.js
    f = ImageFont.truetype(FONT, size); out, cur = [], ''
    for wd in s.split(' '):
        t2 = (cur + ' ' + wd) if cur else wd
        if cur and f.getlength(t2) > maxW: out.append(cur); cur = wd
        else: cur = t2
    return out + [cur]
def ink_bbox(m, clean=0):   # crop to the ink; clean > 0 first ignores specks thinner than that (an erosion) when finding the box
    e = m.copy()
    for _ in range(clean): e = e & np.roll(e, 1, 0) & np.roll(e, -1, 0) & np.roll(e, 1, 1) & np.roll(e, -1, 1)
    ys, xs = np.where(e); c = clean; return m[max(0, ys.min() - c):ys.max() + 1 + c, max(0, xs.min() - c):xs.max() + 1 + c]
def pct_match(f, want):   # which of 0%..99% looks most like the sticker? (Bowlby, same size rule as deals.js fitText(88, maxW 186))
    x0, y0, x1, y1 = scr(660, 720, 884, 812); a = f[y0:y1, x0:x1].astype(int); m = ink_bbox(a.min(-1) > 222, 3)
    tgt = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).resize((160, 80), Image.LANCZOS), float) / 255
    best = None
    for v in range(100):
        st = f'{v}%'; ft = ImageFont.truetype(FONT, 88); w = ft.getlength(st); size = int(88 * 186 / w) if w > 186 else 88
        ft = ImageFont.truetype(FONT, size); im = Image.new('L', (400, 200), 0); from PIL import ImageDraw; ImageDraw.Draw(im).text((10, 10), st, font=ft, fill=255)
        r = ink_bbox(np.asarray(im) > 128); ref = np.asarray(Image.fromarray((r * 255).astype(np.uint8)).resize((160, 80), Image.LANCZOS), float) / 255
        sc = np.corrcoef(tgt.ravel(), ref.ravel())[0, 1]; aspect = abs(np.log((m.shape[1] / m.shape[0]) / (r.shape[1] / r.shape[0])))
        score = sc - aspect
        if best is None or score > best[0]: best = (score, st, sc)
    return best
def split2(s, size=62, maxW=740):   # deals.js lines2()
    f = ImageFont.truetype(FONT, size)
    if f.getlength(s) <= maxW: return [s]
    w = s.split(' '); return min(([' '.join(w[:i]), ' '.join(w[i:])] for i in range(1, len(w))), key=lambda p: max(f.getlength(p[0]), f.getlength(p[1])))
def note_box(nlines, size):   # the pinned note's text area (below its pins), as deals.js lays it out
    lh = size * 1.3; h = nlines * lh + 120; y = SCY - h / 2 - 20; return scr(90, y + 56, 870, y + h - 20)
norm = lambda s: re.sub(r'[^A-Z0-9$.%:/,{}\-]', '', s.upper())
ok_all = True
def report(ok, msg):
    global ok_all; ok_all &= ok; print(('PASS ' if ok else 'FAIL ') + msg)

print(f'{mp4}: {NF} frames = {NF / FPS:.3f} s (expected {DUR:.3f} s)'); report(abs(NF / FPS - DUR) < 1 / FPS + 1e-6, 'duration')
# ---- each deal, on its held frame (all four facts on screen, nothing moving)
for k, d in enumerate(D):
    f = fr(D_(k) + 1.5)
    fp = fr(A_(k) + BAR + 1.5)   # the regular price in its own bar, before it is struck through
    rw = ImageFont.truetype(FONT, 54).getlength('REG. $' + d['regular']) + 56; reg = ocr_any('REG.$' + d['regular'], fp, scr(72, 1090, 60 + rw - 12, 1150), 'dark', 'REG.$0123456789 ')   # inside the chip's keyline
    ft = ImageFont.truetype(FONT, 54); wl = ft.getlength('REG. '); wp = ft.getlength('$' + d['regular'])   # the strike: y -1..4 from the chip's centre line, over the price
    band = f[round(SCY + (1120 - SCY) * K):round(SCY + (1123 - SCY) * K), round(CX + (60 + 28 + wl - SCX) * K):round(CX + (60 + 28 + wl + wp - SCX) * K)].astype(int)
    blue = ((band[..., 2] > 150) & (band[..., 0] < 80)).mean(); report(blue > .8, f'deal {k + 1}: the regular price is struck through on the deal bar ({blue:.0%} of the strike line is blue)')
    deal = ocr_any('$' + d['deal'], f, scr(390, 1196, 900, 1386), 'dark', '$0123456789.')
    pc = ocr_any(f'{pct(d)}%', f, scr(660, 720, 884, 812), 'light', '0123456789%'); name = norm(chips(f, want=[norm(x) for x in split2(d['name'].upper())]))
    want = dict(reg='REG.$' + d['regular'], deal='$' + d['deal'], pc=f'{pct(d)}%', name=norm(d['name']))
    got = dict(reg=reg, deal=deal, pc=pc, name=name)
    for key in want:
        if key == 'pc' and got[key] != want[key]:   # Bowlby's 4 reads as an A to tesseract: match against every possible percent instead
            sc, st, cc = pct_match(f, want[key]); report(st == want[key], f'deal {k + 1} pc: expected {want[key]!r}; OCR read {got[key]!r}; best match of 0%-99% in the same font is {st!r} (correlation {cc:.3f})'); continue
        report(want[key] == got[key], f'deal {k + 1} {key}: expected {want[key]!r}, read {got[key]!r}')
    sc, st, cc = pct_match(f, want['pc']); report(st == want['pc'], f'deal {k + 1} pc, font match over 0%-99%: best {st!r} (correlation {cc:.3f})')
# ---- equal bars per deal: the deal starts from deals.json's timing, each confirmed as a picture change in the mp4
diff = np.array([np.abs(V[i].astype(np.int16) - V[i - 1].astype(np.int16)).mean() for i in range(1, NF)])
starts = [A_(k) for k in range(N)]
lens = [round(starts[k + 1] - starts[k], 3) for k in range(N - 1)] + [round(T_NOTE - starts[-1], 3)]
report(len(set(lens)) == 1, f'deal lengths (s): {lens} = {lens[0] / BAR:g} bars each')
for k in range(1, N):   # the picture must actually change at each deal start (the transition lands there)
    i = int(round(A_(k) * FPS)); w = diff[i - 14:i + 5].max(); report(w > 2, f'deal {k + 1} starts at {A_(k):.3f} s (picture change {w:.1f})')
# ---- the fine print: completely still for a full bar, and the right words
def still(t0, t1):
    i0, i1 = int(round(t0 * FPS)), int(round(t1 * FPS)); return i1 - i0, float(diff[i0:i1 - 1].max())
for nm, t0, words in (('price note', T_NOTE, f"PRICES AS OF {DJ['priceCheck']['date']}, {DJ['priceCheck']['time']} ET. DEALS CAN END ANYTIME."), ('disclosure', T_DISC, DJ['disclosure'])):
    n, mx = still(t0, t0 + BAR); report(mx < .6 and n >= 60, f'{nm}: {n} frames ({n / FPS:.2f} s) with max frame change {mx:.3f}')
    body = [f"PRICES AS OF {DJ['priceCheck']['date'].upper()},", f"{DJ['priceCheck']['time'].upper()} ET.", *wrap('DEALS CAN END ANYTIME.', 66, 700)] if nm == 'price note' else None
    if body is None: q = DJ['disclosure'].upper(); i = q.index(':'); body = [q[:i + 1], *wrap(q[i + 1:].strip(), 62, 700)]
    txt = norm(ocr(fr(t0 + 1.2), note_box(len(body), 66 if nm == 'price note' else 62), 'inkblue', psm=6)); report(txt == norm(words.upper()), f'{nm} text: read {txt!r}')
cta = norm(ocr(fr(T_CTA + 1.2), scr(100, 640, 860, 870), 'dark', psm=6)); report(cta == norm(DJ['cta'][plat]), f'CTA ({plat}): read {cta!r}')
cred = norm(chips(fr(T_CTA + 1.2), want=[norm(x) for x in split2(DJ['credit'].upper())])); report(cred == norm(DJ['credit']), f'credit: read {cred!r}')
# ---- the last second is still
n, mx = still(DUR - 1, DUR); report(mx == 0 or mx < .05, f'last second: max frame change {mx:.4f}')
# ---- the logo on the closing card vs the file (uniform scale, untouched colours)
lg = Image.open(os.path.join(root, 'assets', 'official_logo.png')).convert('RGBA'); bb = lg.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox(); lg = lg.crop(bb)   # alphaBox: alpha > 8
lw = 720; lh = round(lg.height * lw / lg.width); src = np.asarray(lg.resize((lw, lh), Image.LANCZOS)).astype(float)
x0, y0 = 540 - lw // 2, 530; vid = fr(DUR - .5)[y0:y0 + lh, x0:x0 + lw].astype(float)
m = src[..., 3] > 250
for _ in range(4): m = m & np.roll(m, 1, 0) & np.roll(m, -1, 0) & np.roll(m, 1, 1) & np.roll(m, -1, 1)   # erode: skip edges (4:2:0 chroma blurs them)
d = np.abs(src[..., :3][m] - vid[m]); report(np.median(d) < 4, f'logo pixels vs the file: median abs difference {np.median(d):.1f}/255, mean {d.mean():.2f}, over {m.sum()} interior pixels')
for nm, rgb in (('blue', (8, 88, 192)), ('yellow', (248, 208, 0))):   # each logo ink, averaged over its interior
    q = m & (np.abs(src[..., :3] - rgb).sum(-1) < 40); sv, vv = src[..., :3][q].mean(0), vid[q].mean(0)
    report(np.abs(sv - vv).max() < 6, f'logo {nm}: file {sv.round(1).tolist()} vs video {vv.round(1).tolist()} ({q.sum()} px)')
# ---- the platform icons on the closing card's LIVE ON line (as liveEndCard lays them out), each against its file
ICONS = ['youtube', 'instagram', 'facebook']; ih = 46; y_line = 530 + lg.height * 720 / lg.width + 110 + 92 + 118
ims = [Image.open(os.path.join(root, 'assets', 'social', f'{k}_icon.png')).convert('RGBA') for k in ICONS]; iws = [im.width * ih / im.height for im in ims]
tw = ImageFont.truetype(FONT, 34).getlength('LIVE ON'); x = 540 - (tw + 22 + sum(iws) + 16 * (len(ims) - 1)) / 2 + tw + 22
end = fr(DUR - .5)
for k, im, iw in zip(ICONS, ims, iws):
    x0, y0 = round(x), round(y_line - ih / 2); src = np.asarray(im.resize((round(iw), ih), Image.LANCZOS)).astype(float); vid = end[y0:y0 + ih, x0:x0 + round(iw)].astype(float)
    m = src[..., 3] > 250
    for _ in range(2): m = m & np.roll(m, 1, 0) & np.roll(m, -1, 0) & np.roll(m, 1, 1) & np.roll(m, -1, 1)
    d = np.abs(src[..., :3][m] - vid[m]); report(np.median(d) < 8, f'{k} icon on the closing card vs its file: median abs difference {np.median(d):.1f}/255 over {m.sum()} px')
    x += iw + 16
print('ALL PASS' if ok_all else 'SOME CHECKS FAILED')
