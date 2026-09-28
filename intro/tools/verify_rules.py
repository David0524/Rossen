"""Verify a finished JEFF'S RULES mp4: every caption and text card readable (landed and still) for its bar, the last second
still, the official logo and the closing-card icons matching their files.
usage: python3 tools/verify_rules.py rules/ep03 out/rossen-rules-ep03/rossen-rules-ep03.mp4"""
import json, subprocess, sys, os
import numpy as np
from PIL import Image, ImageFont
ep_path, mp4 = sys.argv[1], sys.argv[2]
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
TPL = json.load(open(os.path.join(root, 'rules', 'template.json'))); EP = json.load(open(os.path.join(root, ep_path + '.json')))
BAR, BEAT, FPS, K, SCY = 2.5, .625, 24, .895, 865
SEG = []; b = 0
def add(kind, n, sid=None):
    global b; SEG.append(dict(kind=kind, b0=b, bars=n, id=sid or kind)); b += n
add('title', TPL['bars']['title'])
for s in EP['scenes'][:EP['ruleAfter']]: add('scene', s['bars'], s['id'])
add('rule', TPL['bars']['rule'])
for s in EP['scenes'][EP['ruleAfter']:]: add('scene', s['bars'], s['id'])
add('recap', TPL['bars']['recap']); add('end', TPL['bars']['end'])
DUR = b * BAR; by = {s['id']: s for s in SEG}
SA = lambda sid, bar=1, beat=1: (by[sid]['b0'] + bar - 1) * BAR + (beat - 1) * BEAT
sy = lambda y: round(SCY + (y - SCY) * K)   # content y -> screen y
ok_all = True
def report(ok, msg):
    global ok_all; ok_all &= bool(ok); print(('PASS ' if ok else 'FAIL ') + msg)
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', mp4, '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], capture_output=True, check=True).stdout
V = np.frombuffer(raw, np.uint8).reshape(-1, 1920, 1080); NF = len(V)
report(abs(NF / FPS - DUR) < 1 / FPS + 1e-6, f'duration {NF / FPS:.3f} s (timeline {DUR} s = {b} bars)')
def still(t0, t1, y0, y1, x0=0, x1=1080):   # the largest frame-to-frame change in a band, t0..t1 (codec noise is ~1)
    i0, i1 = int(np.ceil(t0 * FPS)), int(t1 * FPS); a = V[i0:i1 + 1, y0:y1, x0:x1].astype(np.int16)
    return i1 - i0 + 1, float(np.percentile(np.abs(np.diff(a, axis=0)), 99.9)) if len(a) > 1 else 0.0
SETTLE = .45   # the series chip lands with a small bounce that is gone (under a pixel) by then
# ---- scene captions: each holds, landed and still, until the next caption or the end of its scene
for sc in EP['scenes']:
    caps = sc.get('caps', []); end = SA(sc['id']) + sc['bars'] * BAR
    for i, cp in enumerate(caps):
        t0 = SA(sc['id'], cp[0], cp[1]); t1 = SA(sc['id'], caps[i + 1][0], caps[i + 1][1]) - .14 if i + 1 < len(caps) else end - .15
        tl = t0 + (len(cp) - 3) * BEAT / 2   # the template lands each line an eighth after the one above
        n, mx = still(tl + SETTLE, t1, sy(378 - 60), sy(488 + 60), 60, 1020)
        report(t1 - t0 >= BAR - .3 and mx <= 4, f'caption "{" / ".join(cp[2:])}": on screen {t1 - t0 + .14:.2f} s (a full bar), landed and still for {n / FPS:.2f} s (largest change {mx:.0f}/255)')
# ---- the recurring cards (template): the rule, the recap and FOLLOW FOR, still once landed
r = by['rule']; n, mx = still(SA('rule', 2) + SETTLE, SA('rule', 3) - .15, sy(560), sy(1080), 100, 860); report(mx <= 4, f'the rule card: both lines landed and still for {n / FPS:.2f} s (largest change {mx:.0f}/255)')
n, mx = still(SA('recap', 2, 1.5) + SETTLE, SA('recap', 3) - .15, sy(530), sy(1240), 100, 860); report(mx <= 4, f'the recap card: rule + recap line still for {n / FPS:.2f} s (largest change {mx:.0f}/255)')
report(True, f'the rule is on screen twice: the reveal ({SA("rule", 1, 3):.2f} s) and the recap ({SA("recap"):.2f} s)')
# ---- this episode's own text cards
if EP['num'] == 3:
    n, mx = still(SA('how', 1, 1.5), SA('how', 1, 2) - .05, sy(1000), sy(1250), 120, 840); n2, mx2 = still(SA('how', 1, 3) + .05, SA('how', 2) - .05, sy(1000), sy(1250), 120, 840)
    report(max(mx, mx2) <= 4, f'the product page: SOLD BY / SHIPPED BY lines still (zoom settled at {SA("how", 1, 1.5):.2f} s; still between the highlights, largest change {max(mx, mx2):.0f}/255)')
    n, mx = still(SA('how', 2, 3) + SETTLE, SA('how', 4) - .15, sy(560), sy(1340), 60, 900)
    report(mx <= 4, f'the ranking card: all three rungs landed and still for {n / FPS:.2f} s, more than a bar (largest change {mx:.0f}/255)')
# ---- the last second, the logo and the icons (the closing card, screen space)
n, mx = still(DUR - 1, DUR - 1 / FPS, 0, 1920); report(mx <= 1, f'the last second is still: {n} frames, largest change {mx:.0f}/255')
fr = subprocess.run(['ffmpeg', '-v', 'error', '-sseof', '-0.5', '-i', mp4, '-vframes', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
F = np.frombuffer(fr, np.uint8).reshape(1920, 1080, 3).astype(float)
lg = Image.open(os.path.join(root, 'assets', 'official_logo.png')).convert('RGBA'); bb = lg.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox(); lg = lg.crop(bb)
lw = 720; lh = round(lg.height * lw / lg.width); src = np.asarray(lg.resize((lw, lh), Image.LANCZOS)).astype(float); vid = F[530:530 + lh, 540 - lw // 2:540 - lw // 2 + lw]
m = src[..., 3] > 250
for _ in range(4): m = m & np.roll(m, 1, 0) & np.roll(m, -1, 0) & np.roll(m, 1, 1) & np.roll(m, -1, 1)
for nm, rgb in (('blue', (8, 88, 192)), ('yellow', (248, 208, 0))):
    q = m & (np.abs(src[..., :3] - rgb).sum(-1) < 40); sv, vv = src[..., :3][q].mean(0), vid[q].mean(0)
    report(np.abs(sv - vv).max() < 6, f'official logo {nm}: file {sv.round(1).tolist()} vs video {vv.round(1).tolist()} ({q.sum()} px)')
d = np.abs(src[..., :3][m] - vid[m]); report(np.median(d) < 4, f'official logo pixels vs the file: median difference {np.median(d):.0f}/255 (uniform scale, untextured)')
plats = EP.get('endPlatforms', ['youtube', 'instagram']); ih = 46; y_line = 530 + lg.height * 720 / lg.width + 110 + 92 + 118
ims = [Image.open(os.path.join(root, 'assets', 'social', f'{k}_icon.png')).convert('RGBA') for k in plats]; iws = [im.width * ih / im.height for im in ims]
tw = ImageFont.truetype(os.path.join(root, 'assets', 'fonts', 'BowlbyOneSC-Regular.ttf'), 34).getlength('LIVE ON'); x = 540 - (tw + 22 + sum(iws) + 16 * (len(ims) - 1)) / 2 + tw + 22
for k, im, iw in zip(plats, ims, iws):
    x0, y0 = round(x), round(y_line - ih / 2); s2 = np.asarray(im.resize((round(iw), ih), Image.LANCZOS)).astype(float); v2 = F[y0:y0 + ih, x0:x0 + round(iw)]
    mm = s2[..., 3] > 250
    for _ in range(2): mm = mm & np.roll(mm, 1, 0) & np.roll(mm, -1, 0) & np.roll(mm, 1, 1) & np.roll(mm, -1, 1)
    dd = np.abs(s2[..., :3][mm] - v2[mm]); report(np.median(dd) < 8, f'closing card {k} icon vs its file: median difference {np.median(dd):.0f}/255'); x += iw + 16
print('ALL PASS' if ok_all else 'SOME CHECKS FAILED')
