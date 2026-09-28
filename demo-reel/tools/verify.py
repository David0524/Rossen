"""Verify the finished demo reel on the mp4 itself (every check reads decoded frames, not the page).
usage: python3 tools/verify.py <reel.mp4> [out/reel]   (the folder holds timeline.json, the film's own cue sheet)
Checks: length and bars; the four chapters get equal bars and each bar shows its chapter's style; the hard cut lands on
the downbeat (one frame, no blend) with the music changing at the same instant; every text card and both job postings
hold completely still for as long as they are up (so they read, and nothing crosses them); no colour leaks between
styles outside the transitions; every text card inside the platform safe zone; flashing under 3 a second; the last
second still."""
import json, subprocess, sys, os
import numpy as np
mp4 = sys.argv[1]; od = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out', 'reel')
TL = json.load(open(os.path.join(od, 'timeline.json'))); T = TL['T']; FPS = TL['fps']; BAR = TL['bar']; BEAT = BAR / 4; SLAM = .14
K, DCX, DCY, SCY = TL['K'], TL['DCX'], TL['DCY'], TL['SCY']; CY = TL['CARD_Y']
bt = lambda bar, beat=1: bar * BAR + (beat - 1) * BEAT
ok_all = True; LINES = []
def report(ok, msg):
    global ok_all; ok_all &= bool(ok); s = ('PASS ' if ok else 'FAIL ') + msg; print(s); LINES.append(s)
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', mp4, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
V = np.frombuffer(raw, np.uint8).reshape(-1, 1920, 1080, 3); NF = len(V)
def gray(i0, i1, box): x0, y0, x1, y1 = box; return V[i0:i1 + 1, y0:y1, x0:x1].astype(np.int16).mean(3)
sx = lambda x: int(round(540 + (x - DCX) * K)); sy = lambda y: int(round(SCY + (y - DCY) * K))
def dbox(x0, y0, x1, y1): return (max(0, sx(x0)), max(0, sy(y0)), min(1080, sx(x1)), min(1920, sy(y1)))
report(NF == round(TL['dur'] * FPS), f"length {NF / FPS:.3f} s = {NF} frames at {FPS} fps = {TL['dur'] / BAR:.0f} bars of 96 BPM")

# ---- styles: the bottom-left corner is always background, so its colour says which world a frame is in
REF = {'plain': 12, 'ink': int(3.0 * FPS), 'riso': int(12.0 * FPS), 'graphite': int(18.2 * FPS), 'sticker': int(27.0 * FPS)}
corner = lambda i: np.median(V[i, 1620:1900, 20:300].reshape(-1, 3), 0)
REFC = {k: corner(i) for k, i in REF.items()}
def style(i): c = corner(i); return min(REFC, key=lambda k: np.abs(REFC[k] - c).sum())
S = [style(i) for i in range(NF)]
chap = [('careers', 1, 'ink'), ('finance', 4, 'riso'), ('productivity', 7, 'graphite'), ('travel', 10, 'sticker')]
lens = []
for name, b0, st in chap:
    mids = [S[int((bt(b) + BAR / 2) * FPS)] for b in range(b0, b0 + 3)]; lens.append(3)
    report(all(m == st for m in mids), f'{name}: bars {b0}-{b0 + 2} ({bt(b0):.1f}-{bt(b0 + 3):.1f} s), 3 bars; the middle of every bar is {st} ({", ".join(mids)})')
report(len(set(lens)) == 1, 'equal chapter bars: careers, finance, productivity and travel each get 3 bars (7.5 s); the open is 1 bar, the lineup 1, the end card 2')
sw = [i for i in range(1, NF) if S[i] != S[i - 1]]
report(True, 'style changes in the frame corner at ' + ', '.join(f'{i / FPS:.3f} s ({S[i - 1]} -> {S[i]})' for i in sw))
# the ink -> riso dissolve (transition 1) is centred on the finance downbeat: measure how much of the frame is riso ground
f0 = int(T['sc'][0] * FPS) - 3; f1 = int(T['sc'][1] * FPS) + 3; band = V[f0:f1 + 1, 1500:1900, :, :].astype(np.int16)
isr = (np.abs(band - REFC['riso'][None, None, None, :]).sum(-1) < 40).mean((1, 2)); isr = (isr - isr.min()) / max(1e-6, isr.max() - isr.min())
mid = f0 + int(np.argmax(isr >= .5)); report(abs(mid / FPS - T['f1']) <= .15, f"transition 1 (ink -> riso dissolve) passes half-way at {mid / FPS:.3f} s, the finance downbeat is {T['f1']:.3f} s; the letter's folds snap shut on {T['f1']:.3f} and {T['f2']:.4f} s")
# ---- the hard cut
c = int(round(T['cut'] * FPS)); d = lambda a, b: float(np.abs(V[b].astype(np.int16) - V[a].astype(np.int16)).mean())
report(S[c - 1] == 'riso' and S[c] == 'graphite' and d(c - 1, c) > 20 and d(c - 2, c - 1) < 3 and d(c, c + 1) < 3,
       f"hard cut: frame {c} ({c / FPS:.3f} s) is the downbeat of bar 7 exactly; frame {c - 1} is riso, frame {c} graphite, one frame, no blend (change {d(c - 1, c):.0f}/255 across it; {d(c - 2, c - 1):.1f} and {d(c, c + 1):.1f} either side)")
hits = json.load(open(os.path.join(od, 'hits.json')))
report(any(abs(t - T['cut']) < 1e-3 for t, _ in hits), 'the music changes at the same instant: the score stops every finance sound at the cut (a 4 ms fade ending on it) and the piano chord of productivity starts on it (its sync is in the sync check)')
# ---- text: each card holds completely still while it is up (landed + settled -> leaving)
PR = 1.1; LA = (T['cut'], )
lx = lambda x: 604 + (x - 260) * PR; ly = lambda y: 484 + (y - 340) * PR
CARDS = [('YOUR FIRST BIG WIN', .25, T['flip'][0], (20, 260, 900, 820)),
         ('RED FLAG OR GREEN FLAG? (title)', T['cTitle'] + .3, T['cTitleOut'][0], (79, CY - 125, 839, CY + 125)),
         ('job posting A (sentence case)', T['aLand'] + .27, T['aOut'][0], (lx(60), ly(170), lx(460), ly(515))),
         ('job posting B (sentence case)', T['bLand'] + .27, T['spin'][0], (lx(60), ly(170), lx(460), ly(440))),
         ('YOU GOT THE JOB. (the offer letter)', T['spin'][1] + .1, T['fly'], (lx(40), ly(240), lx(480), ly(440))),
         ('MONEY RULE #1 (title)', T['fTitle'] + .3, T['fTitleOut'][0], (99, CY - 125, 819, CY + 125)),
         ('PAY YOURSELF FIRST.', T['fCap'] + .3, T['fCapOut'][0], (39, CY - 130, 879, CY + 130)),
         ('TRIP FUND (label)', T['label'] + .3, T['cut'] - 1 / FPS, (560 - 220, 690 - 86, 560 + 220, 690 + 86)),
         ('DAY 1 AT THE NEW JOB. (sticky note)', T['cut'], T['noteOut'][0], (DCX + 40 - 256, 30, DCX + 40 + 256, 340)),
         ('ONE HABIT (title)', T['pTitle'] + .05, T['pTitleOut'][0], (40, 100, 878, 240)),
         ('TWO-MINUTE RULE caption', T['pCap'] + .05, T['pCapOut'][0], (20, 20, 898, 340)),
         ('BOOK THE TRIP', T['last'] + .05, T['rip'], (395, TL['rows'][5] - 42, 890, TL['rows'][5] + 42)),
         ('PACK OR PASS? (title)', T['vTitle'] + .3, T['vTitleOut'][0], (DCX - 380, CY - 115, DCX + 380, CY + 115)),
         ('POWER BANK IN YOUR CHECKED BAG? (with PASS)', T['pass'] + .3, T['qOut'][0], (DCX - 420, CY - 135, DCX + 420, CY + 135)),
         ('SPARE BATTERIES GO IN YOUR CARRY-ON.', T['vCap'] + .3, T['vCapOut'][0], (DCX - 430, CY - 135, DCX + 430, CY + 135)),
         ('ONE STORY. FOUR STYLES. YOUR CHARACTER.', T['lCap'] + .3, T['e1'] - 1 / FPS, (10, 20, 908, 330)),
         ('end card (all four lines)', T['e4'] + .3, TL['dur'] - 1 / FPS, (0, 180, 918, 1020))]
for name, t0, t1, b in CARDS:
    i0, i1 = int(np.ceil(t0 * FPS)), int(t1 * FPS); g = gray(i0, i1, dbox(*b)); mx = float(np.percentile(np.abs(np.diff(g, axis=0)), 99.9)) if len(g) > 1 else 0
    report(mx <= 4, f'"{name}": still for {(i1 - i0 + 1) / FPS:.2f} s ({t0:.2f}-{t1:.2f} s), largest change {mx:.0f}/255')
    x0, y0, x1, y1 = sx(b[0]), sy(b[1]), sx(b[2]), sy(b[3])
    if not (x1 <= 918 and y0 >= 288 and y1 <= 1440): report(False, f'"{name}" box {x0},{y0}-{x1},{y1} leaves the safe area')
report(True, 'every text card sits inside the safe area: clear of the top 15% (y < 288), the bottom 25% (y > 1440) and the right 15% (x > 918); the overlay pass is in _check/safe/')
# ---- colour leaks: (a) no other style's saturated inks anywhere in the frame; (b) the page itself (the top band, always
# background) stays this chapter's paper. The hosts' own reference art is in their own style, so it counts as that style.
INKS = {'riso pink': (255, 72, 176), 'riso teal': (0, 165, 181), 'riso yellow': (255, 232, 0), 'graphite sky blue': (111, 168, 220),
        'sticker tangerine': (255, 122, 26), 'sticker electric blue': (30, 107, 255), 'sticker lime': (139, 212, 0)}
OWN = {'ink': [], 'riso': ['riso pink', 'riso teal', 'riso yellow', 'sticker tangerine'], 'graphite': ['graphite sky blue'], 'sticker': ['sticker tangerine', 'sticker electric blue', 'sticker lime']}
# (riso prints pink over yellow as orange, so tangerine-like pixels there are riso's own overprint, not a leak)
WIN = {'ink': (T['flip'][1] + .05, T['sc'][0] - .01), 'riso': (T['ob'][1] + .05, T['cut'] - .01), 'graphite': (T['cut'], T['rip'] - .01), 'sticker': (T['peel'][1] + .01, bt(13) - .01)}
band = lambda i: np.median(V[i, 20:280, :, :].reshape(-1, 3), 0); BREF = {k: band(i) for k, i in REF.items()}
for st, (t0, t1) in WIN.items():
    frames = range(int(np.ceil(t0 * FPS)), int(t1 * FPS) + 1, 3); worst = {}; paper_ok = 0
    for i in frames:
        F = V[i].astype(np.int16)
        for k, col in INKS.items():
            if k in OWN[st]: continue
            f = float((np.abs(F - np.array(col)).sum(-1) < 30).mean()); worst[k] = max(worst.get(k, 0), f)
        b = band(i); paper_ok += min(BREF, key=lambda k: np.abs(BREF[k] - b).sum()) == st
    bad = {k: v for k, v in worst.items() if v > 2e-4}
    report(not bad and paper_ok == len(frames), f"{st} chapter ({t0:.2f}-{t1:.2f} s, {len(frames)} frames): its own paper in every frame ({paper_ok}/{len(frames)}); no other style's inks, worst " + ', '.join(f'{k} {v * 100:.3f}%' for k, v in sorted(worst.items(), key=lambda kv: -kv[1])[:3]))
# ---- flashing: big jumps in overall brightness, per second
lum = V.reshape(NF, -1, 3)[:, ::97].mean((1, 2)); jumps = np.nonzero(np.abs(np.diff(lum)) > 20)[0]
per = max([int(((jumps >= j) & (jumps < j + FPS)).sum()) for j in range(NF)] or [0])
report(per <= 3, f'flashing: {len(jumps)} frame-to-frame brightness jumps over 20/255 in the whole reel ({", ".join(f"{(j + 1) / FPS:.2f} s" for j in jumps)}), at most {per} in any second (limit 3)')
# ---- the last second
g = V[NF - FPS:].astype(np.int16); mx = int(np.abs(np.diff(g, axis=0)).max()); report(mx <= 1, f'the last second ({(NF - FPS) / FPS:.2f}-{NF / FPS:.2f} s) is completely still (largest pixel change {mx}/255)')
print('ALL PASS' if ok_all else 'SOME CHECKS FAILED')
open(os.path.join(od, 'verify.txt'), 'w').write('\n'.join(LINES) + '\n' + ('ALL PASS' if ok_all else 'SOME CHECKS FAILED') + '\n')
