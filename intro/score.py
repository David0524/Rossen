"""Soundtrack for the Rossen Reports opener, built entirely from recorded samples (no synthesis).

Music: an original 15 s cue sequenced from VSCO 2 Community Edition orchestral samples (CC0):
pizzicato and spiccato strings, brass stabs and swells, timpani, snare, cymbals, glockenspiel, xylophone.
Foley: Kenney "Impact Sounds", "RPG Audio", "Interface Sounds", "Casino Audio" packs (CC0).
Notes are placed like a sampler: nearest recorded note, repitched by at most a couple of semitones.

120 BPM, one beat = 0.5 s, beat 0 = 0.30 s (the LIVE stamp). Key: D minor, turning to D major when the money comes back.
Hit points: 0.30 stamp | 7.30 SCAM! | 13.55 logo lands | 13.82 LIVE stamp + final chord.

usage: python3 score.py [samples_dir]  ->  out/score.wav
"""
import numpy as np, subprocess, wave, sys, os, re, glob, math
SR = 48000; DUR = 15.0
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audio')
out = np.zeros((int(SR * DUR), 2), np.float32)
_cache = {}
def load(rel):
    if rel not in _cache:
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', os.path.join(ROOT, rel), '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
        x = np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
        i0 = int(np.argmax(np.abs(x).max(1) > 0.003)); _cache[rel] = x[max(0, i0 - 48):]   # trim leading silence
    return _cache[rel]
USED = set()
def put(x, t, gain=1.0, pan=0.0, dur=None, rel=0.08):
    if dur is not None:
        n = min(len(x), int((dur + rel) * SR)); x = x[:n].copy(); r = min(n, int(rel * SR)); x[n - r:] *= np.linspace(1, 0, r)[:, None]
    lg, rg = math.cos((pan + 1) * math.pi / 4) * 1.414, math.sin((pan + 1) * math.pi / 4) * 1.414
    x = x * gain * np.array([min(1, lg), min(1, rg)], np.float32)
    i0 = int(round(t * SR))
    if i0 < 0: x = x[-i0:]; i0 = 0
    i1 = min(len(out), i0 + len(x))
    if i1 > i0: out[i0:i1] += x[: i1 - i0]

# ---------------- instruments ----------------
NAMES = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}
def midi(n): m = re.match(r'([A-G][#b]?)(-?\d)', n); return NAMES[m.group(1)] + 12 * (int(m.group(2)) + 1)
class Inst:
    """pattern: glob under ROOT with the note name as the only varying token, e.g. 'vsco/.../VlnEns_Pizz_*_v2_rr1.wav'.
    Note names follow the library's convention (one octave below concert pitch), used consistently for every instrument."""
    def __init__(self, pattern, pan=0.0, gain=1.0):
        self.map = {}; pre, post = pattern.split('*')
        for f in glob.glob(os.path.join(ROOT, pattern)):
            rel = os.path.relpath(f, ROOT); tok = rel[len(pre):len(rel) - len(post)]
            if re.fullmatch(r'[A-G][#b]?-?\d', tok): self.map[midi(tok)] = rel
        assert self.map, pattern
        self.pan, self.gain = pan, gain
    def __call__(self, note, t, vel=1.0, dur=None, rel=0.08, pan=None):
        m = midi(note) if isinstance(note, str) else note
        k = min(self.map, key=lambda s: (abs(s - m), s < m))   # nearest sample, prefer repitching down
        x = load(self.map[k]); USED.add(self.map[k])
        if k != m:   # sampler-style repitch: resample the recording
            ratio = 2 ** ((m - k) / 12); n = int(len(x) / ratio); src = np.arange(n) * ratio
            x = np.stack([np.interp(src, np.arange(len(x)), x[:, c]) for c in (0, 1)], 1).astype(np.float32)
        put(x, t, vel * self.gain, self.pan if pan is None else pan, dur, rel)
def one(rel, t, gain=1.0, pan=0.0, dur=None, relz=0.08):
    USED.add(rel); put(load(rel), t, gain, pan, dur, relz)

V = 'vsco/'
vpz = Inst(V + 'Strings/Violin Section/Pizz/VlnEns_Pizz_*_v2_rr1.wav', pan=-.35, gain=.75)
vsp = Inst(V + 'Strings/Violin Section/Spic/VlnEns_Spic_*_v2_rr1.wav', pan=-.3, gain=.55)
vla = Inst(V + 'Strings/Viola Section/spic/Violas_spic_*_v2_rr1.wav', pan=.2, gain=.55)
cpz = Inst(V + 'Strings/Cello Section/pizzT/pizzT_*_v2_RR1.wav', pan=.3, gain=.95)
cbp = Inst(V + 'Strings/Solo Contrabass/Pizz/BKCtbss_Pizz_*_v1_rr1.wav', pan=.05, gain=1.0)
tps = Inst(V + 'Brass/Trumpet/stac/Sum_SHTrumpet_stac_*_v3_rr1.wav', pan=-.15, gain=.6)
tpl = Inst(V + 'Brass/Trumpet/susvib/Sum_SHTrumpet_susvib_*_v2_rr1.wav', pan=-.15, gain=.5)
hns = Inst(V + 'Brass/F Horn/stac/MOHorn_stac_*_v2_rr1.wav', pan=.25, gain=.7)
hnl = Inst(V + 'Brass/F Horn/sus/MOHorn_sus_*_v1_1.wav', pan=.25, gain=.55)
tbs = Inst(V + 'Brass/Tenor Trombone/stac/tenortbn_stac_*_v3_rr1.wav', pan=.1, gain=.7)
tbl = Inst(V + 'Brass/Tenor Trombone/sus/tenortbn_sus_*_v2_1.wav', pan=.1, gain=.55)
cla = Inst(V + 'Woodwinds/Clarinet/stac/DCClar_stac_*_v3_rr1_sum.wav', pan=-.1, gain=.7)
glk = Inst(V + 'Percussion/Glock/glock_medium_*.wav', pan=.15, gain=.6)
xyl = Inst(V + 'Percussion/Xylo/Xylo_Medium_*_ff_01_far.wav', pan=-.1, gain=.5)
P = V + 'Percussion/'
TIMP, TIMP_ROLL = P + 'Timpani/Timpani4_Hit_v4_rr1_Sum.wav', P + 'Timpani/Rolls/Timpani4_Roll_v5_rr1_Sum.wav'
def timp(t, g=1.0, dur=None):   # Timpani4 rings a little sharp of Eb; pulled down to D
    x = load(TIMP); USED.add(TIMP); ratio = 2 ** (-0.8 / 12); src = np.arange(int(len(x) / ratio)) * ratio
    y = np.stack([np.interp(src, np.arange(len(x)), x[:, c]) for c in (0, 1)], 1).astype(np.float32); put(y, t, g * .9, 0, dur, .3)
BD, CRASH, CRASH_MF, SWELL = P + 'BDrumNewhit_v6_rr1_Sum.wav', P + 'cymbal-crash1_ff_rr1.wav', P + 'cymbal-crash1_mf_rr1.wav', P + 'susCymb1-cresc-Short_v1.wav'
SN_ROLL, SN, TRI, CLAVE, TAMB = P + 'Snare2-rollNS_v5_rr1_Sum.wav', P + 'Snare2-HitNS_v3_rr1_Sum.wav', P + 'Triangle3-Hit_v2_rr1_Sum.wav', P + 'Claves1_Hit_v2_rr1_Sum.wav', P + 'Tamb1-Hit_v1_rr1_Sum.wav'
K = 'kenney/'
def fx(name, t, g=1.0, pan=0.0, dur=None): one(K + name, t, g, pan, dur)

B = lambda b: 0.30 + 0.5 * b   # beat -> seconds

# ================= A. stamp + walk-in (0.30 - 2.8) =================
t = B(0)
for n in ('D4', 'A3'): tps(n, t, 1.0, dur=.35)
for n in ('D2', 'F2', 'A2'): hns(n, t, 1.0, dur=.4)
tbs('D3', t, .9, dur=.4); cbp('D1', t, 1.0); cpz('D2', t, .9)
timp(t, 1.0); one(BD, t, .9); one(CRASH_MF, t, .45)
fx('impact/impactPunch_heavy_000.ogg', .33, .55); fx('impact/impactWood_heavy_000.ogg', .33, .45)
# sneaky-cute walking theme: pizz bass on the beat, violin pizz tune, snare on 2 and 4, claves on the offbeats
walk_bass = [(1, 'D2'), (2, 'A1'), (3, 'D2'), (4, 'A1'), (5, 'D2')]
for b, n in walk_bass: cpz(n, B(b), .8); cbp(n.replace('2', '1').replace('A1', 'A0'), B(b), .45)
tune = [(1, 'D4'), (1.5, 'F4'), (2, 'A4'), (3, 'G4'), (3.5, 'F4'), (4, 'E4'), (4.5, 'C#4'), (5, 'D4')]
for b, n in tune: vpz(n, B(b), .85)
for b in (2, 4): one(SN, B(b), .22, .1)
for b in (1.5, 2.5, 3.5, 4.5): one(CLAVE, B(b), .12, -.2)
# footsteps (x from -300 to 380, stride 113 px, same curve as the picture)
for n in range(1, 7):
    e = 113 * n / 680; p = 1 - (1 - e) ** (1 / 1.7); fx(f'impact/footstep_wood_00{n % 5}.ogg', .45 + 2.15 * p, .28, -.3)

# ================= B. investigation (3.05 - 7.05) =================
# ticking viola ostinato with a creeping half-step, contrabass pulse, claves as a clock
osti = ['D3', 'D3', 'Eb3', 'D3']
for k in range(16):   # eighths from beat 5.5 to 13.5
    b = 5.5 + k * .5; vla(osti[k % 4], B(b), .85 + .35 * k / 15, dur=.22)
    if k >= 12: vsp(osti[k % 4].replace('3', '4'), B(b), .5 + .3 * (k - 12) / 3, dur=.2)
for b in range(6, 14): one(CLAVE, B(b), .24, .25); cbp('D1', B(b), .6 if b % 2 == 0 else .4, dur=.4)
fx('rpg/metalClick.ogg', 2.95, .35, .3)
for k, tt in enumerate((3.05, 3.15, 3.25)): fx('rpg/metalLatch.ogg', tt, .22, .3)      # telescoping handle
for k, n in enumerate(('A3', 'G#3', 'G3')): cla(n, 3.62 + k * .13, .75, dur=.12)        # scammer peeks: tip-toe clarinet
glk('D6', 4.98, .9); fx('interface/glass_002.ogg', 4.98, .18, .2)                     # hidden camera glint
vpz('D5', 6.02, .8); vpz('G#4', 6.15, .7); fx('interface/scratch_002.ogg', 6.02, .2)    # sticker peel
put(load(TIMP_ROLL)[: int(1.0 * SR)] * np.linspace(.1, 1, int(1.0 * SR))[:, None], 6.3, .55); USED.add(TIMP_ROLL)
x = load(SWELL); USED.add(SWELL); pk = int(np.argmax(np.abs(x).max(1))); put(x[:pk], 7.3 - pk / SR, .35, dur=pk / SR, rel=.02)                # cymbal swell ending on the hit
fx('rpg/cloth1.ogg', 6.85, .4, .2)                                                     # magnifier toss

# ================= C. SCAM! (7.30) and the getaway =================
def stab(t, root_notes, g):
    for n in root_notes['tp']: tps(n, t, g, dur=.3)
    for n in root_notes['hn']: hns(n, t, g, dur=.35)
    for n in root_notes['tb']: tbs(n, t, g, dur=.35)
Dm = {'tp': ['D4', 'F4', 'A3'], 'hn': ['D2', 'A2'], 'tb': ['D3', 'F2']}
Eb = {'tp': ['Eb4', 'G3', 'Bb3'], 'hn': ['Eb2', 'Bb2'], 'tb': ['Eb3', 'G2']}
stab(7.30, Dm, 1.0); cbp('D1', 7.30, 1.0); timp(7.30, 1.0); one(BD, 7.30, 1.0); one(CRASH, 7.30, .55)
stab(7.55, Dm, .7); one(SN, 7.55, .35)
stab(7.80, Eb, .95); cbp('Eb1', 7.80, .9); timp(7.80, .7)
fx('impact/impactPunch_heavy_001.ogg', 7.30, .6); fx('impact/impactSoft_medium_000.ogg', 7.05, .4, .2)
for k in range(8): vsp('D4' if k % 2 == 0 else 'Eb4', 7.8 + k * .0625 + .06, .55, dur=.07)   # panic trill
# the getaway: a scurrying pizz run down the D minor scale, snare taps, tiny footsteps
run = ['D5', 'C5', 'A4', 'G4', 'F4', 'E4', 'D4', 'C#4', 'A3', 'G3', 'F3', 'E3', 'D3']
for k, n in enumerate(run): vpz(n, 8.30 + k * .0833, .8 - .02 * k)
for b in (16, 17, 18): one(SN, B(b), .2)
for k in range(9): fx(f'impact/footstep_concrete_00{k % 5}.ogg', 8.32 + k * .115, .12, .4)

# ================= D. money comes home (9.3 - 11.05), D major =================
bills_home = sorted(8.36 + k * .11 + 1.15 + (k % 3) * .12 for k in range(6))
for k in range(6): fx(f'casino/card-slide-{k % 8 + 1}.ogg', 8.36 + k * .11, .22, .3)
for tt, n in zip(bills_home, ('D5', 'F#5', 'A5', 'D6', 'F#6', 'A6')): glk(n, tt, .8)
for b, n in ((18, 'D2'), (19, 'A1'), (20, 'D2'), (21, 'A1')): cpz(n, B(b), .85)
for b in (18.5, 19.5, 20.5):
    for n in ('F#4', 'A4'): vpz(n, B(b), .6)
for n in ('D4', 'F#4', 'A4', 'D5'): vpz(n, 10.64, .7)
one(TRI, 10.64, .35); fx('rpg/bookClose.ogg', 10.62, .35, -.2); fx('rpg/handleSmallLeather.ogg', 10.5, .25, -.2)

# ================= E. the deals (11.05 - 12.8) =================
fx('impact/impactPlank_medium_000.ogg', 11.04, .45, .5); one(BD, 11.04, .45); cbp('D1', 11.04, .8)
fx('casino/cards-pack-open-1.ogg', 11.18, .35, .5)
for tt, n in zip((11.34, 11.52, 11.70), ('A5', 'F#5', 'D5')): xyl(n, tt, .9); fx('casino/card-place-1.ogg', tt, .15, .5)   # prices drop
for b, n in ((22, 'A1'), (23, 'D2'), (24, 'A1')): cpz(n, B(b), .8); cbp('D1' if n == 'D2' else 'A0', B(b), .4)
for b in (22.5, 23.5, 24.5):
    for n in ('F#4', 'A4', 'D5'): vpz(n, B(b), .5)
for b in (22, 24): one(SN, B(b), .25); one(TAMB, B(b), .18, .3)

# ================= F. build and sign-off (12.8 - 15) =================
roll = load(SN_ROLL); USED.add(SN_ROLL); n = int(1.0 * SR); r = roll[:n] * np.linspace(.15, 1, n)[:, None]; put(r, 12.8, .45)
for k, nn in enumerate(['D4', 'E4', 'F#4', 'G4', 'A4', 'B4', 'C#5', 'D5']): vsp(nn, 12.8 + k * .125, .45 + .05 * k, dur=.12)
fx('rpg/cloth2.ogg', 12.88, .35, .3)
tps('A3', 13.55, .8, dur=.2); hns('A2', 13.55, .7, dur=.2); fx('impact/impactSoft_heavy_000.ogg', 13.55, .5)
t = 13.82   # the button: full D major, lands with the LIVE stamp
for n in ('D4', 'F#4', 'A4'): tpl(n, t, .9, dur=1.1, rel=.5)
for n in ('D2', 'F#2', 'A2'): hnl(n, t, .9, dur=1.1, rel=.5)
for n in ('D2', 'A1'): tbl(n, t, .85, dur=1.1, rel=.5)
cbp('D1', t, 1.0); cpz('D2', t, .9); vpz('D5', t, .7); vpz('A4', t, .6)
timp(t, 1.0); one(BD, t, 1.0); one(CRASH, t, .6); glk('D6', t, .7); one(TRI, t, .3)
fx('impact/impactPunch_heavy_002.ogg', t, .5)

# ---------------- master ----------------
fade = int(.35 * SR); out[-fade:] *= np.linspace(1, 0, fade)[:, None] ** 2
out = np.tanh(out * 1.1) / 1.1                      # gentle soft-clip on the peaks
out *= (10 ** (-1 / 20)) / max(1e-6, np.abs(out).max())
os.makedirs('out', exist_ok=True)
with wave.open('out/score.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(out, -1, 1) * 32767).astype('<i2').tobytes())
with open('out/samples_used.txt', 'w') as f: f.write('\n'.join(sorted(USED)) + '\n')
print('out/score.wav', DUR, 's,', len(USED), 'samples')
