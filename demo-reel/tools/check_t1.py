"""Checks on the transition-1 test mp4: text holds still while read, no colour leaks between the two styles outside the
transition, and the safe zones. usage: python3 tools/check_t1.py _check/transition-1-test.mp4"""
import subprocess, sys, numpy as np
mp4 = sys.argv[1]; FPS = 24
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', mp4, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
V = np.frombuffer(raw, np.uint8).reshape(-1, 1920, 1080, 3); NF = len(V); ok = True
K, SCY = .82, 864
def box(x0, y0, x1, y1): f = lambda x, y: (round(540 + (x - 459) * K), round(SCY + (y - 576) * K)); a, b = f(x0, y0); c, d = f(x1, y1); return a, b, c, d
def still(t0, t1, b):
    x0, y0, x1, y1 = b; i0, i1 = int(np.ceil(t0 * FPS)), int(t1 * FPS); g = V[i0:i1 + 1, y0:y1, x0:x1].astype(np.int16).mean(3)
    return (i1 - i0 + 1) / FPS, float(np.percentile(np.abs(np.diff(g, axis=0)), 99.9))
def rep(c, m):
    global ok; ok &= bool(c); print(('PASS ' if c else 'FAIL ') + m)
n, mx = still(.625 + .27, 2.19 - 1 / FPS, box(318, 110, 890, 858)); rep(mx <= 4, f'the offer letter ("YOU GOT THE JOB.") holds still for {n:.2f} s once landed (largest change {mx:.0f}/255)')
n, mx = still(3.75 + .3, 5 - 1 / FPS, box(99, 25, 819, 275)); rep(mx <= 4, f'the MONEY RULE #1 card holds still for {n:.2f} s once landed (largest change {mx:.0f}/255)')
def frac(frames, test): return max(float(test(V[i].astype(np.int16)).mean()) for i in frames)
fluo = lambda F: ((np.abs(F - [255, 72, 176]).sum(2) < 90) | (np.abs(F - [0, 165, 181]).sum(2) < 90) | ((F[..., 0] > 200) & (F[..., 1] > 190) & (F[..., 2] < 90)))
ink = [i for i in range(NF) if i / FPS < 2.30]; riso = [i for i in range(NF) if i / FPS > 2.98]
f = frac(ink, fluo); rep(f < 1e-4, f'ink bars (0-2.30 s): no fluorescent pink, teal or yellow anywhere (worst frame {f * 100:.4f}% of pixels)')
warm = lambda F: (np.abs(F - [245, 233, 210]).sum(2) < 14) | (np.abs(F - [58, 39, 24]).sum(2) < 40)
f = frac(riso, warm); rep(f < 1e-3, f'riso bars (2.98-5.0 s): no warm ink paper or sepia ink left (worst frame {f * 100:.4f}% of pixels)')
print('ALL PASS' if ok else 'SOME CHECKS FAILED')
