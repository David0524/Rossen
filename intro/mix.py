"""Build the soundtrack from sample files on disk (LibreOffice gallery sounds). No synthesis:
every sound is a slice of a recorded sample placed on the film's beat timeline, with gain, fades and a gentle low-pass."""
import numpy as np, subprocess, wave
SR = 48000; DUR = 15.0; SND = '/usr/lib/libreoffice/share/gallery/sounds/'
def load(n):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', SND + n + '.wav', '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
S = {n: load(n) for n in 'untie explos kongas apert2 laser glasses top drama falling sparcle kling pluck applause'.split()}
out = np.zeros((int(SR * DUR), 2), np.float32)
def lowpass(x, hz):
    a = np.exp(-2 * np.pi * hz / SR); y = np.empty_like(x); acc = np.zeros(2, np.float32)
    for i in range(len(x)): acc = (1 - a) * x[i] + a * acc; y[i] = acc
    return y
def place(t, name, a=0.0, b=None, gain=1.0, fin=0.004, fout=0.03, lp=None):
    x = S[name]; x = x[int(a * SR): int(b * SR) if b else len(x)].copy()
    if lp: x = lowpass(x, lp)
    n = len(x); env = np.ones(n, np.float32)
    fi, fo = max(1, int(fin * SR)), max(1, int(fout * SR))
    env[:fi] = np.linspace(0, 1, fi); env[-fo:] *= np.linspace(1, 0, fo)
    x *= env[:, None] * gain
    i0 = int(t * SR); i1 = min(len(out), i0 + n); out[i0:i1] += x[: i1 - i0]
# --- music bed: the pentatonic melody in untie.wav, looped three times under the action
# the phrase is dense for ~3.3 s then rings out, so each repeat starts over the previous one's tail
for t0 in (0.55, 3.9, 7.25, 10.6):
    place(t0, 'untie', gain=0.34, fout=0.9)
bed_end = int(13.4 * SR); fade = int(0.5 * SR); out[bed_end - fade: bed_end] *= np.linspace(1, 0, fade)[:, None]; out[bed_end:] = 0
# --- stamps
thunk = lambda t, g: (place(t, 'explos', 0, .38, gain=g, fout=.28, lp=650), place(t, 'kongas', .88, 1.05, gain=g * .55, fout=.05))
thunk(0.33, 0.95)
# --- footsteps on each foot contact of the walk-in (x from -300 to 380, stride 113 px)
for n in range(1, 7):
    e = 113 * n / 680; p = 1 - (1 - e) ** (1 / 1.7); t = .45 + 2.15 * p
    place(t - .01, 'kongas', *((.48, .70) if n % 2 else (.88, 1.05)), gain=0.33, fout=.06)
# --- investigation
place(2.92, 'apert2', 0, 1.0, gain=0.32, fin=.05, fout=.4)          # glass comes out, handle telescopes
place(3.62, 'laser', gain=0.22, fout=.05)                            # scammer peeks
place(4.98, 'glasses', 0, .7, gain=0.28, fout=.3)                    # hidden camera glint
place(6.02, 'top', 0, .35, gain=0.22, fout=.15)                      # sticker peel
place(6.82, 'apert2', 0, .8, gain=0.30, fin=.03, fout=.35)           # toss
place(7.05, 'top', 0, .45, gain=0.32, fout=.2)                       # scammer pops out
thunk(7.30, 1.25)                                                    # SCAM!
place(7.32, 'drama', 0, 1.9, gain=0.42, fout=.6)
place(8.28, 'falling', 0, 1.5, gain=0.34, fout=.4)                   # he bolts
for k in range(9): place(8.32 + k * .115, 'kongas', .48, .62, gain=0.16, fout=.04)
place(8.9, 'sparcle', 0, 2.0, gain=0.28, fout=.6)                    # money flutters home
place(10.64, 'kling', 0, 1.1, gain=0.32, fout=.5)                    # wallet snaps shut
# --- deals
place(11.04, 'pluck', 0, .6, gain=0.55, fout=.3); place(11.04, 'kongas', .88, 1.05, gain=.3, fout=.05)
place(11.18, 'top', 0, .4, gain=0.28, fout=.15)
for t in (11.34, 11.52, 11.70): place(t, 'kling', 0, .38, gain=0.22, fout=.2)
# --- sign-off
place(12.88, 'apert2', 0, .9, gain=0.30, fin=.03, fout=.4)
place(13.28, 'sparcle', 0, 1.1, gain=0.22, fout=.5)
place(13.55, 'pluck', 0, .7, gain=0.6, fout=.35); place(13.55, 'explos', 0, .25, gain=.4, fout=.2, lp=380)
thunk(13.82, 0.8)
place(13.62, 'applause', 0, 1.38, gain=0.2, fin=.25, fout=.9)
# master: peak to -1 dBFS, 30 ms tail fade
out[-int(.03 * SR):] *= np.linspace(1, 0, int(.03 * SR))[:, None]
out *= (10 ** (-1 / 20)) / max(1e-6, np.abs(out).max())
pcm = (np.clip(out, -1, 1) * 32767).astype('<i2')
with wave.open('out/score.wav', 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('out/score.wav', len(out) / SR, 's')
