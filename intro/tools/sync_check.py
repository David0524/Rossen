"""Hit sync check: for every synced hit in hits.json, find the audio onset nearest its picture time and report the offset.
Onset = half-rise on a 1 ms peak envelope, above the level just before the hit (so a ringing tail is not an onset).
usage: python3 tools/sync_check.py <audio: wav or mp4> <hits.json> [--offset-ref score.wav]
With --offset-ref, the audio is first cross-correlated against that wav to report the container's fixed offset."""
import numpy as np, subprocess, json, sys
def pcm(f, sr=48000):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-map', '0:a:0', '-ac', '1', '-ar', str(sr), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32)
a = pcm(sys.argv[1]); hits = json.load(open(sys.argv[2]))
if '--offset-ref' in sys.argv:
    r = pcm(sys.argv[sys.argv.index('--offset-ref') + 1]); n = min(len(a), len(r), 48000 * 20)
    A = np.fft.rfft(a[:n], 2 * n); R = np.fft.rfft(r[:n], 2 * n); cc = np.fft.irfft(A * np.conj(R)); lag = int(np.argmax(np.abs(np.r_[cc[-2000:], cc[:2000]]))) - 2000
    print(f'container offset vs {sys.argv[sys.argv.index("--offset-ref") + 1]}: {lag / 48:.2f} ms')
e = np.abs(a[: len(a) // 48 * 48]).reshape(-1, 48).max(1)   # 1 ms envelope
worst = 0
for t, what in hits:
    i0 = int(round(t * 1000)); lo, hi = max(0, i0 - 40), min(len(e), i0 + 60)
    pre = float(np.median(e[max(0, i0 - 150): max(1, i0 - 60)])) if i0 > 60 else 0.0
    p = float(e[lo:hi].max()); thr = pre + .5 * (p - pre); on = lo + int(np.argmax(e[lo:hi] >= thr))
    d = on - i0; worst = max(worst, abs(d))
    print(f'{t:7.3f}s  {what:13s} onset {on / 1000:7.3f}s  offset {d:+4d} ms' + ('   <-- over 10 ms' if abs(d) > 10 else ''))
print(f'{len(hits)} hits, worst offset {worst} ms')
