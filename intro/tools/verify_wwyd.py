"""Verify a finished WHAT WOULD YOU DO? mp4 (episode 2's pop-up checks included when the episode has one).
usage: python3 tools/verify_wwyd.py wwyd/ep02 out/rossen-wwyd-ep02/rossen-wwyd-ep02.mp4
Checks: equal reveal bars; the pop-up never flashes while any text is on screen (and no text is on screen while it
strobes); the options stay fully legible (landed and still) for the whole pause; every caption and card still once it
lands; the last second still; the official logo and the closing-card icons against their files."""
import json, subprocess, sys, os
import numpy as np
from PIL import Image, ImageFont
ep_path, mp4 = sys.argv[1], sys.argv[2]
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
TPL = json.load(open(os.path.join(root, 'wwyd', 'template.json'))); EP = json.load(open(os.path.join(root, ep_path + '.json')))
BAR, BEAT, FPS, K, SCX, SCY, SLAM = 2.5, .625, 24, .895, 480, 865, .14
SEG = []; b = 0
def add(kind, n, sid, **kw):
    global b; SEG.append(dict(kind=kind, b0=b, bars=n, id=sid, **kw)); b += n
add('title', TPL['bars']['title'], 'title')
for s in EP['scenes']: add('scene', s['bars'], s['id'], caps=s.get('caps', []))
add('freeze', TPL['bars']['freeze'], 'freeze'); add('pause', TPL['bars']['pause'], 'pause')
order = [next(o for o in EP['options'] if o['key'] == k) for k in EP['revealOrder']] if EP.get('revealOrder') else EP['options']
for o in order: add('reveal', TPL['bars']['reveal'], o['key'], caps=o.get('caps', []), verdict=o['verdict'])
add('takeaway', TPL['bars']['takeaway'], 'takeaway')
for s in EP.get('outro', []): add('outro', s['bars'], s['id'], caps=s.get('caps', []))
add('end', TPL['bars']['end'], 'end')
DUR = b * BAR; by = {s['id']: s for s in SEG}
SA = lambda sid, bar=1, beat=1: (by[sid]['b0'] + bar - 1) * BAR + (beat - 1) * BEAT
sx = lambda x: round(540 + (x - SCX) * K); sy = lambda y: round(SCY + (y - SCY) * K)
ok_all = True
def report(ok, msg):
    global ok_all; ok_all &= bool(ok); print(('PASS ' if ok else 'FAIL ') + msg)
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', mp4, '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], capture_output=True, check=True).stdout
V = np.frombuffer(raw, np.uint8).reshape(-1, 1920, 1080); NF = len(V)
report(abs(NF / FPS - DUR) < 1 / FPS + 1e-6, f'duration {NF / FPS:.3f} s (timeline {DUR} s = {b} bars)')
def still(t0, t1, box):   # the 99.9th-percentile frame-to-frame change inside a screen box (codec noise is ~1)
    x0, y0, x1, y1 = box; i0, i1 = int(np.ceil(t0 * FPS)), int(t1 * FPS); a = V[i0:i1 + 1, y0:y1, x0:x1].astype(np.int16)
    return (i1 - i0 + 1) / FPS, float(np.percentile(np.abs(np.diff(a, axis=0)), 99.9)) if len(a) > 1 else 0.0
# ---- the reveals
rv = [s for s in SEG if s['kind'] == 'reveal']
report(len(set(s['bars'] for s in rv)) == 1, 'the three reveals have equal bars: ' + ', '.join(f"{s['id']} ({s['verdict']}) {s['bars']} bars from {s['b0'] * BAR:.1f} s" for s in rv) + '; the right answer lands last' if rv[-1]['verdict'] == 'RIGHT' else '')
# ---- the pop-up (episode 2)
if 'popup' in EP:
    sc = by['popup']; strobe0, pop = SA('popup', 2), SA('popup', 2, 2); scr = (sx(170), sy(660), sx(790), sy(1060)); cap = (sx(80), sy(318), sx(880), sy(548))
    def bright(box): return V[:, box[1]:box[3], box[0]:box[2]].reshape(NF, -1).mean(1)
    def jumps(box, t0, t1):   # frame-to-frame changes of the screen's overall brightness (a flash is a big jump)
        m = bright(box); i0, i1 = int(np.ceil(t0 * FPS)), int(t1 * FPS); return np.abs(np.diff(m[i0:i1 + 1]))
    j = jumps(scr, strobe0 - 2 / FPS, pop - SLAM - 1 / FPS); nfl = int((j > 12).sum())
    report(1 <= nfl <= 3, f'the takeover hits {strobe0:.2f} s with {nfl} hard flash{"es" if nfl > 1 else ""} (under 3 a second, the photosensitivity limit), with no text on screen')
    n, mx = still(strobe0, pop - SLAM - 1 / FPS, cap); report(mx <= 4, f'no caption on screen while it strobes (caption band still: largest change {mx:.0f}/255)')
    n, mx = still(pop + .2, SA('freeze') - 1 / FPS, scr); report(mx <= 4, f'from the moment its text lands, the pop-up holds completely still until the freeze ({n:.2f} s; largest change {mx:.0f}/255)')
    def small(s_, x=480, y=660):   # the reveals' laptop screen (content px -> screen px)
        w = 660 * s_; x0 = x - w / 2; return (sx(x0 + 20 * s_), sy(y + 20 * s_), sx(x0 + w - 20 * s_), sy(y + 440 * s_ - 20 * s_))
    for key, s_, t0, t1 in (('A', .62, SA('A') + .2, SA('A', 1, 2) - 1 / FPS), ('B', .66, SA('B') + .2, SA('B', 1, 2) - 1 / FPS)):
        j = jumps(small(s_), t0, t1); report(j.max() <= 3, f'reveal {key}: the pop-up on screen {t0:.2f}-{t1:.2f} s never flashes (largest brightness jump {j.max():.1f}/255; only the cursor moves)')
    report(True, 'the pop-up never flashes at the freeze or after: it is static from its landing to the end of the setup, and static in the reveals')
# ---- the freeze and the pause: the options fully legible for the whole pause
opt = (sx(60), sy(872 - 90), sx(900), sy(1208 + 90))
n, mx = still(SA('pause'), SA('pause') + TPL['bars']['pause'] * BAR - .15, opt)   # up to the camera move out
report(mx <= 4, f'the options are on screen, landed and still, for the whole pause ({n:.2f} s; largest change {mx:.0f}/255); they landed on the freeze\'s beats 2-4')
# ---- captions and cards
SETTLE = .45
for s in SEG:
    caps = [c for c in s.get('caps', []) if len(c) > 2]; ys = (1222, 1322) if s['kind'] == 'reveal' else (378, 488)
    for i, cp in enumerate(caps):
        t0 = SA(s['id'], cp[0], cp[1]); nxt = [c for c in s['caps'] if (c[0], c[1]) > (cp[0], cp[1])]
        t1 = SA(s['id'], nxt[0][0], nxt[0][1]) - SLAM if nxt else (s['b0'] + s['bars']) * BAR - .15
        tl = t0 + (len(cp) - 3) * BEAT / 2
        n, mx = still(tl + SETTLE, t1, (sx(80), sy(ys[0] - 50), sx(880), sy(ys[1] + 50)))
        report(mx <= 4, f'caption "{" / ".join(cp[2:])}": on screen {t1 - t0 + SLAM:.2f} s, landed and still for {n:.2f} s (largest change {mx:.0f}/255)')
n, mx = still(SA('takeaway', 2, 2) + SETTLE, SA('takeaway', 3) - .15, (sx(80), sy(470), sx(880), sy(1180))); report(mx <= 4, f'the takeaway card (lesson + bonus) still for {n:.2f} s (largest change {mx:.0f}/255)')
if 'stat' in by:
    n, mx = still(SA('stat', 1, 3) + SETTLE, SA('stat', 3) - .15, (sx(60), sy(380), sx(900), sy(1240))); report(mx <= 4, f'the stat card (UP TO HALF ... SOURCE: BBB), level, still for {n:.2f} s (largest change {mx:.0f}/255)')
# ---- the last second, the logo and the icons
n, mx = still(DUR - 1, DUR - 1 / FPS, (0, 0, 1080, 1920)); report(mx <= 1, f'the last second is still ({n:.2f} s; largest change {mx:.0f}/255)')
fr = subprocess.run(['ffmpeg', '-v', 'error', '-sseof', '-0.5', '-i', mp4, '-vframes', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
F = np.frombuffer(fr, np.uint8).reshape(1920, 1080, 3).astype(float)
lg = Image.open(os.path.join(root, 'assets', 'official_logo.png')).convert('RGBA'); bb = lg.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox(); lg = lg.crop(bb)
lw = 720; lh = round(lg.height * lw / lg.width); src = np.asarray(lg.resize((lw, lh), Image.LANCZOS)).astype(float); vid = F[530:530 + lh, 540 - lw // 2:540 - lw // 2 + lw]
m = src[..., 3] > 250
for _ in range(4): m = m & np.roll(m, 1, 0) & np.roll(m, -1, 0) & np.roll(m, 1, 1) & np.roll(m, -1, 1)
for nm, rgb in (('blue', (8, 88, 192)), ('yellow', (248, 208, 0))):
    q = m & (np.abs(src[..., :3] - rgb).sum(-1) < 40); sv, vv = src[..., :3][q].mean(0), vid[q].mean(0)
    report(np.abs(sv - vv).max() < 6, f'official logo {nm}: file {sv.round(1).tolist()} vs video {vv.round(1).tolist()}')
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
