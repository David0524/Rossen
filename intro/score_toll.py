"""Score for the "unpaid toll" explainer (toll.js), 44.5 s. Composed in code on the 96 BPM grid and played by recorded
instrument samples (VSCO 2 CE and its VSCO 1 drums, CC0); physical sound effects are recorded Kenney samples (CC0).
The music changes at each act: HOOK (a sparse question: low horn, pizzicato, a ticking rim), EVIDENCE (a detective walk:
walking pizzicato bass, brushes, a clarinet answer after each mark), the DIVE and the fake page (held strings, a low pulse),
SCALE (timpani and horns open up; the stat lands on a brass chord), HOW IT WORKS (the groove drives), then one beat of
silence, and the FIX (warm D major: horns and trumpets), the stamp and the closing card.

usage: python3 score_toll.py             ->  out/rossen-toll-scam/score.wav, hits.json, samples_used.txt, audio_sources.txt
       HITS_ONLY=1 python3 score_toll.py  ->  score_hits.wav (the synced hits alone)
"""
import numpy as np, subprocess, wave, sys, os, re, glob, math, json
SR = 48000
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audio')
DUR = 16 * 2.5 + 4.5   # 16 bars, then the closing card
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
    if os.environ.get('PITCHED_ONLY'): return
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
def timp(t, g=1.0, dur=None):
    if os.environ.get('PITCHED_ONLY'): return
   # Timpani4 rings a little sharp of Eb; pulled down to D
    x = load(TIMP); USED.add(TIMP); ratio = 2 ** (-0.8 / 12); src = np.arange(int(len(x) / ratio)) * ratio
    y = np.stack([np.interp(src, np.arange(len(x)), x[:, c]) for c in (0, 1)], 1).astype(np.float32); put(y, t, g * .9, 0, dur, .3)
BD, CRASH, CRASH_MF, SWELL = P + 'BDrumNewhit_v6_rr1_Sum.wav', P + 'cymbal-crash1_ff_rr1.wav', P + 'cymbal-crash1_mf_rr1.wav', P + 'susCymb1-cresc-Short_v1.wav'
SN_ROLL, SN, TRI, CLAVE, TAMB = P + 'Snare2-rollNS_v5_rr1_Sum.wav', P + 'Snare2-HitNS_v3_rr1_Sum.wav', P + 'Triangle3-Hit_v2_rr1_Sum.wav', P + 'Claves1_Hit_v2_rr1_Sum.wav', P + 'Tamb1-Hit_v1_rr1_Sum.wav'
K = 'kenney/'
def fx(name, t, g=1.0, pan=0.0, dur=None):   # foley is placed so its ATTACK (first reach of half its peak) lands on t
    if os.environ.get('PITCHED_ONLY'): return
    x = load(K + name); env = np.abs(x).max(1); att = int(np.argmax(env >= .5 * env.max()))
    USED.add(K + name); put(x, t - att / SR, g, pan, dur)

BEAT = 0.625; E8, S16 = BEAT / 2, BEAT / 4
B = lambda b: b * BEAT   # beat -> seconds (beat 0 = first frame = first downbeat)
BAR = lambda n, b=0: B(4 * n + b)   # bar n (0-based), beat b
D1_ = V + 'VSCO 1 Percussion/drums/'
KICK, KICK2, SNR, SNR2, SNRF, RIM = D1_ + 'bass/bdrum_ff_1.wav', D1_ + 'bass/bdrum_f_1.wav', D1_ + 'snare/drum2/snare2_f_1.wav', D1_ + 'snare/drum2/snare2_mf_1.wav', D1_ + 'snare/drum2/snare2_ff_1.wav', D1_ + 'snare/drum2/snare2_rimshot_f_1.wav'
TOMH, TOML = D1_ + 'tenor/tenor_higher/tenorH_ff_1.wav', D1_ + 'tenor/tenor_lower/tenor_ff_1.wav'
TAMB2 = P + 'Tamb1-Hit_v2_rr1_Sum.wav'
_tuned = {}
def tuned(rel, t, g, semis, pan=0.0):   # drums pulled into the key (kick -> A, toms -> A and E)
    if os.environ.get('PITCHED_ONLY'): return
    if (rel, semis) not in _tuned:
        x = load(rel); ratio = 2 ** (semis / 12); src = np.arange(int(len(x) / ratio)) * ratio
        _tuned[(rel, semis)] = np.stack([np.interp(src, np.arange(len(x)), x[:, c]) for c in (0, 1)], 1).astype(np.float32)
    USED.add(rel); put(_tuned[(rel, semis)], t, g, pan)
def kick(t, g=.9): tuned(KICK if g > .6 else KICK2, t, g, 1.47 if g > .6 else 0)
def snare(t, g=.5): one(SNR if g > .35 else SNR2, t, g, .05)
def tamb(t0, t1, g=.16):
    k = 0; t = t0
    while t < t1 - 1e-6: one(TAMB if k % 2 == 0 else TAMB2, t, g * (1.0 if k % 2 else .7), .35); t += E8; k += 1
def swell_to(t, g=.4):
    if os.environ.get('PITCHED_ONLY'): return
    x = load(SWELL); USED.add(SWELL); pk = int(np.argmax(np.abs(x).max(1))); put(x[:pk], t - pk / SR, g, dur=pk / SR, rel=.02)
def roll_to(t0, t1, g=.45, rel=SN_ROLL):
    if os.environ.get('PITCHED_ONLY'): return
    x = load(rel); USED.add(rel); n = int((t1 - t0) * SR); put(x[:n] * np.linspace(.12, 1, n)[:, None] ** 1.5, t0, g)
def tomfill(t0, t1, g=.55, step=S16):
    k = 0; t = t0
    while t < t1 - 1e-6: hi = (k // 2) % 2 == 0; tuned(TOMH if hi else TOML, t, g * (.7 + .3 * k * step / (t1 - t0)), -.32 if hi else -.82, .1 * (1 if k % 2 else -1)); t += step; k += 1
CH = {   # chord voicings: trumpets / horns / trombones / contrabass root (library note names)
    'Dm': (['D4', 'F4', 'A3'], ['D2', 'A2'], ['D3', 'F2'], 'D1'), 'Bb': (['D4', 'F4', 'Bb3'], ['Bb1', 'F2'], ['Bb2', 'F2'], 'Bb0'),
    'C': (['E4', 'G4', 'C4'], ['C2', 'G2'], ['C3', 'G2'], 'C1'), 'Eb': (['Eb4', 'G3', 'Bb3'], ['Eb2', 'Bb2'], ['Eb3', 'G2'], 'Eb1'),
    'D': (['D4', 'F#4', 'A3'], ['D2', 'A2'], ['D3', 'F#2'], 'D1'), 'F': (['F4', 'A3', 'C4'], ['F2', 'C2'], ['F2', 'A2'], 'F1'),
    'G': (['G4', 'B3', 'D4'], ['G1', 'D2'], ['G2', 'B2'], 'G1'), 'A': (['A4', 'C#4', 'E4'], ['A1', 'E2'], ['A2', 'C#3'], 'A0'),
}
def stab(t, ch, g=1.0, dur=.32, bass=True):
    tp, hn, tb, root = CH[ch]
    for n in tp: tps(n, t, g, dur=dur)
    for n in hn: hns(n, t, g, dur=dur + .05)
    for n in tb: tbs(n, t, g * .9, dur=dur + .05)
    if bass: cbp(root, t, g)
def hit(t, ch, g=1.0, crash=.5):   # stab + kick + timpani + crash
    stab(t, ch, g); kick(t, g); timp(t, g * .9)
    if crash: one(CRASH, t, crash)
def ostinato(t0, t1, notes, inst, g=.5, step=E8, dur=.16):
    k = 0; t = t0
    while t < t1 - 1e-6: inst(notes[k % len(notes)], t, g, dur=dur); t += step; k += 1

def groove(b0, b1, g=.75, tamb_g=.15):   # kick on 1, the "and" of 2 and 3; snare on 2 and 4; tambourine eighths
    for bb in range(int(b0), int(b1)):
        pos = bb % 4
        if pos in (0, 2): kick(B(bb), g)
        if pos == 1: kick(B(bb + .5), g * .7)
        if pos in (1, 3): snare(B(bb), .45)
    tamb(B(b0), B(b1), tamb_g)
def bass(beats):   # eighth-note bass, one root per beat: {beat: note}
    for bb, n in beats.items(): cpz(n, B(bb), .7, dur=.28); cpz(n, B(bb + .5), .6, dur=.28); cbp(n.replace('2', '1').replace('A1', 'A0').replace('B1', 'B0'), B(bb), .35, dur=.3)
def strings(beats):   # viola eighths on chord tones: {beat: (lo, hi)}
    for bb, (lo, hi) in beats.items(): vla(lo, B(bb), .38, dur=.2); vla(hi, B(bb + .5), .34, dur=.2)
def downbeat(bb, g=.22): one(CRASH_MF, B(bb), g)   # scene changes: a light cymbal, no brass

AT = lambda bar, beat=1: bar * 2.5 + (beat - 1) * BEAT   # same clock as the picture (bar 0-based, beat 1-based)
BB = lambda bar, beat=1: bar * 4 + (beat - 1)            # the same point in beats from the start


HO = bool(os.environ.get('HITS_ONLY'))
if HO: groove = roll_to = tomfill = swell_to = tamb = lambda *a, **k: None
CH['Gm'] = (['D4', 'G4', 'Bb3'], ['G1', 'D2'], ['G2', 'Bb2'], 'G1')
CROOT = {'Dm': 'D2', 'D': 'D2', 'Bb': 'Bb1', 'Gm': 'G2', 'G': 'G2', 'A': 'A1', 'C': 'C2', 'Eb': 'Eb2', 'F': 'F2'}
TONES = {'Dm': ('D5', 'F5', 'A5'), 'D': ('D5', 'F#5', 'A5'), 'Bb': ('D5', 'F5', 'Bb5'), 'Gm': ('D5', 'G5', 'Bb5'), 'G': ('D5', 'G5', 'B5'),
         'A': ('C#5', 'E5', 'A5'), 'C': ('C5', 'E5', 'G5'), 'Eb': ('Eb5', 'G5', 'Bb5'), 'F': ('C5', 'F5', 'A5')}
PAD = {'Dm': ('D2', 'F2', 'A2'), 'Bb': ('Bb1', 'D2', 'F2'), 'Gm': ('G1', 'D2', 'Bb2'), 'A': ('A1', 'C#2', 'E2'), 'C': ('C2', 'E2', 'G2'),
       'Eb': ('Eb2', 'G2', 'Bb2'), 'D': ('D3', 'F#3', 'A3'), 'G': ('G2', 'B2', 'D3'), 'F': ('F2', 'A2', 'C3')}
HITS = []   # every synced hit: (time, what) -> hits.json, checked against the picture
def H(t, what): HITS.append((round(t, 4), what))
STAMP = AT(16)   # the rubber stamp lands; the closing card is revealed

SIL0, SIL1 = AT(13, 4), AT(14)   # the silent beat before the fix
CH['Bm'] = (['D4', 'F#4', 'B3'], ['B1', 'F#2'], ['B2', 'F#2'], 'B0')
CROOT['Bm'] = 'B1'; TONES['Bm'] = ('D5', 'F#5', 'B5'); PAD['Bm'] = ('B1', 'D2', 'F#2')
def capsnd(t): xyl('D6', t, .2); fx('casino/card-place-1.ogg', t, .12)
def stamp_hit(t, g=1.0, ch='D'): kick(t, .85 * g); timp(t, .8 * g); cbp(CH[ch][3], t, .9 * g); fx('impact/impactPunch_heavy_000.ogg', t, .45 * g); H(t, 'stamp')
def push(t): fx('casino/card-slide-3.ogg', t - .15, .26)
def fxa(name, t, g=1.0, pan=0.0):   # samples that swell in: align their first audible attack
    x = load(K + name); e = np.convolve(np.abs(x).max(1), np.ones(96) / 96, 'same'); att = int(np.argmax(e >= .15 * e.max()))
    USED.add(K + name); put(x, t - att / SR, g, pan)

# ---------------- the music, act by act ----------------
ROWS = {0: 'Dm Dm Bb A', 1: 'Dm Dm Bb A',                                    # hook: a question
        2: 'Dm Dm C C', 3: 'Bb Bb A A', 4: 'Dm Dm C C', 5: 'Bb Bb A A',       # evidence: the detective walk
        6: 'Gm Gm A A',                                                       # the fake page
        7: 'Dm Dm Bb Bb', 8: 'Gm Gm A A', 9: 'Dm Bb C A',                     # scale
        10: 'Dm Dm Bb C', 11: 'Dm Dm Bb C', 12: 'Gm Gm A A', 13: 'Dm Dm A A',  # how it works (the last beat is silent)
        14: 'D D G A', 15: 'D D G A'}                                         # the fix: warm D major
def act(bar): return 'hook' if bar <= 1 else 'evidence' if bar <= 5 else 'page' if bar == 6 else 'scale' if bar <= 9 else 'how' if bar <= 13 else 'fix'
if not HO:
    for bar, row in ROWS.items():
        a = act(bar)
        for k, ch in enumerate(row.split()):
            bb = BB(bar, k + 1); t = B(bb)
            if SIL0 - 1e-6 <= t < SIL1 or t >= STAMP - BEAT: continue
            r = CROOT[ch]; lo = r.replace('2', '1') if r[-1] == '2' else r.replace('1', '0')
            if a == 'hook':
                if k in (0, 2): cpz(r, t, .55, dur=.3); cbp(lo, t, .4, dur=.4)
                one(RIM, t, .12, .1)                                                          # the tick of a clock
                if k == 0: [hnl(n, t, .2, dur=BEAT * 4 - .1, rel=.3) for n in PAD[ch]]
            elif a == 'evidence':
                cbp(lo, t, .42, dur=.3); cpz(r, t, .55, dur=.26); cpz(TONES[ch][0].replace('5', '3'), t + E8, .4, dur=.2)   # a walking bass
                if k in (1, 3): one(SNR2, t, .14, .05)                                           # brushes on 2 and 4
                if k % 2 == 0: [hnl(n, t, .15, dur=BEAT * 2 - .1, rel=.25) for n in PAD[ch]]
            elif a == 'page':
                for j in range(4): vsp(TONES[ch][j % 2], t + j * S16, .22, dur=.1)               # held tension
                if k == 0: [hnl(n, t, .25, dur=2.5 - .1, rel=.3) for n in PAD[ch]]; cbp(lo, t, .5, dur=.6)
            elif a == 'scale':
                cbp(lo, t, .45, dur=.3); cpz(r, t, .6, dur=.28); cpz(r, t + E8, .5, dur=.28)
                for j in range(2): vsp(TONES[ch][j % 2], t + j * E8, .26, dur=.12)
                if k % 2 == 0: [hnl(n, t, .26, dur=BEAT * 2 - .1, rel=.3) for n in PAD[ch]]
            elif a == 'how':
                cbp(lo, t, .42, dur=.3); cpz(r, t, .62, dur=.26); cpz(r, t + E8, .52, dur=.26)
                for j in range(4): vsp(TONES[ch][j % 3], t + j * S16, .24, dur=.09)
            else:
                cbp(lo, t, .45, dur=.3); cpz(r, t, .65, dur=.28); cpz(r, t + E8, .55, dur=.28)
                xyl(TONES[ch][k % 3], t, .22, dur=.15)
                if k % 2 == 0: [hnl(n, t, .3, dur=BEAT * 2 - .1, rel=.3) for n in PAD[ch]]
        if a == 'evidence' or a == 'hook': timp(AT(bar), .35)
        if a == 'scale': timp(AT(bar), .55); kick(AT(bar), .6); kick(AT(bar, 3), .5)
        if a == 'how': groove(BB(bar), BB(bar, 4) if bar == 13 else BB(bar + 1), .5, .07)
        if a == 'fix': groove(BB(bar), min(BB(bar + 1), STAMP / BEAT - 1), .58, .1)
    for n in ('D3', 'F#3', 'A3'): tpl(n, AT(14, 1.02), .16, dur=2.5 * 1.8, rel=.5)          # warm trumpets under the fix
    swell_to(AT(7), .3); roll_to(AT(15, 4), STAMP, .4, TIMP_ROLL); tomfill(AT(15, 4.25), STAMP, .4, S16 / 2)

# ---------------- sounds on the picture's beats ----------------
for bar, n in [(0, 3), (2, 1), (3, 2), (4, 2), (5, 2), (6, 2), (7, 1), (10, 2), (11, 2), (12, 2), (13, 2)]:
    for i in range(n):
        if bar == 0: continue   # frame 0: the caption is already there
        capsnd(AT(bar) + i * E8)
# HOOK: the phone pings in frame 0; Jeff pops up on bar 1
fx('interface/glass_001.ogg', 0.0, .45); glk('A6', 0.0, .3); kick(0.0, .55); H(0.0, 'ping')
fx('interface/pluck_002.ogg', AT(1), .35); kick(AT(1), .5); H(AT(1), 'jeff')
# EVIDENCE: each mark starts on beat 2 (the pen touches down) and lands on beat 3, with a rising xylophone answer
for k, (bar, sfx, g) in enumerate([(2, 'interface/scratch_004.ogg', .3), (3, 'interface/scratch_002.ogg', .35), (4, 'interface/scratch_001.ogg', .35), (5, 'interface/scratch_002.ogg', .32)]):
    t2, t3 = AT(bar, 2), AT(bar, 3)
    (fxa if 'scratch_004' in sfx else fx)(sfx, t2 + (.02 if 'scratch_004' in sfx else 0), g); one(RIM, t2, .35, .1); kick(t2, .6); H(t2, 'pen down')
    xyl(('A5', 'C6', 'D6', 'E6')[k], t3, .45, dur=.2); one(CLAVE, t3, .3); H(t3, 'mark')
    for j, n in enumerate(('A3', 'Bb3', 'A3')): cla(n, AT(bar, 3.5) + j * S16, .38, dur=.12)   # the clarinet answer
# [1] the dive, and the fake page's waiting cursor
fx('casino/card-slide-5.ogg', AT(6) - .3, .3); swell_to(AT(6), .35); kick(AT(6), .8); one(CRASH_MF, AT(6), .25); H(AT(6), 'dive')
for b in (2, 3, 4): fx('interface/tick_001.ogg', AT(6, b), .25)
# [2] the pull-back; pins on sixteenths from 7:1.5; the stat lands on bar 8 and counts up to beat 2
fx('casino/card-slide-1.ogg', AT(7) - .2, .3); kick(AT(7), .85); timp(AT(7), .6); H(AT(7), 'pull-back')
for k in range(15): t = AT(7, 1.5) + k * E8 * .5; fx('casino/chip-lay-1.ogg', t, .22 + .01 * k, pan=-.4 + .055 * k); H(t, 'pin')
stamp_hit(AT(8), 1.0, 'Gm'); one(CRASH, AT(8), .35)
for n in ('D4', 'G4', 'Bb4'): tps(n, AT(8), .7, dur=.35)
for n in ('G1', 'D2'): hns(n, AT(8), .8, dur=.5)
for j in range(3): fx('interface/tick_002.ogg', AT(8) + j * S16, .15)                          # the counter
glk('D6', AT(8, 2), .35); H(AT(8, 2), 'count lands')
# HOW IT WORKS: texts fly out on eighths; two taps; the card slides and lands; three cards reeled in
push(AT(10))
for i in range(7): t = AT(10, 1.5) + i * E8; fx('interface/glass_002.ogg', t, .16); glk(('D6', 'F6', 'A6')[i % 3], t, .16); H(t, 'text')
for b in (2, 3): fx('interface/click_001.ogg', AT(11, b), .6); kick(AT(11, b), .5); H(AT(11, b), 'tap')
fx('casino/card-slide-2.ogg', AT(12, 2), .35); fx('casino/card-place-2.ogg', AT(12, 3), .5); kick(AT(12, 3), .7); one(RIM, AT(12, 3), .35, .1); H(AT(12, 3), 'card in')
for i, b in enumerate((2, 3, 4)):
    t = AT(13, b)
    if t < SIL0 - 1e-6: fx('rpg/handleCoins.ogg', t, .35); kick(t, .55); H(t, 'reel')
fx('rpg/handleCoins2.ogg', AT(13, 3.5), .3)
# FIX: the strip is pinned up on 1 and unfolds on 2 and 3; Jeff's thumbs up on bar 15
fx('rpg/bookPlace1.ogg', AT(14), .5); fx('impact/impactSoft_medium_000.ogg', AT(14), .4); kick(AT(14), .8); H(AT(14), 'strip')
for n in ('D2', 'A2'): hns(n, AT(14), .7, dur=.6)
for b in (2, 3): fx('rpg/bookFlip2.ogg', AT(14, b), .35); kick(AT(14, b), .75); H(AT(14, b), 'unfold')
fx('interface/confirmation_001.ogg', AT(15), .4); kick(AT(15), .55); H(AT(15), 'thumbs')
# END: the rubber stamp, the final chord, a soft held chord under the closing card
if not HO:
    for n in ('D2', 'F#2', 'A2'): hnl(n, STAMP, .9, dur=1.4, rel=.4)
    for n in ('D2', 'A1'): tbl(n, STAMP, .85, dur=1.4, rel=.4)
cbp('D1', STAMP, 1.0); cpz('D2', STAMP, .9); timp(STAMP, 1.0); kick(STAMP, 1.0); one(CRASH, STAMP, .5); glk('D6', STAMP, .45); H(STAMP, 'rubber stamp')
fx('impact/impactPlank_medium_000.ogg', STAMP, .55); fx('impact/impactSoft_heavy_000.ogg', STAMP, .4)
_t0 = STAMP + 1.2
if not HO:
    for n in ('D2', 'F#2', 'A2'): hnl(n, _t0, .3, dur=DUR - _t0 - .4, rel=1.0)
    cpz('D2', _t0, .3)

# ---------------- master ----------------
# the silent beat: everything (tails included) fades out in 25 ms before it and stays at zero until the fix
i0, i1, fz = int(SIL0 * SR), int(SIL1 * SR), int(.025 * SR)
out[i0 - fz:i0] *= np.linspace(1, 0, fz)[:, None]; out[i0:i1] = 0
fade = int(.8 * SR); out[-fade:] *= np.linspace(1, 0, fade)[:, None] ** 2
out = np.tanh(out * 1.1) / 1.1
out *= (10 ** (-1 / 20)) / max(1e-6, np.abs(out).max())
out[i0:i1] = 0
od = 'out/rossen-toll-scam'; os.makedirs(od, exist_ok=True)
with wave.open(od + ('/score_hits.wav' if HO else '/score.wav'), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(out, -1, 1) * 32767).astype('<i2').tobytes())
json.dump(sorted(set(HITS)), open(od + '/hits.json', 'w'))
if not HO:
    with open(od + '/samples_used.txt', 'w') as f: f.write('\n'.join(sorted(USED)) + '\n')
    PACK = {'interface': 'https://kenney.nl/assets/interface-sounds', 'impact': 'https://kenney.nl/assets/impact-sounds', 'rpg': 'https://kenney.nl/assets/rpg-audio',
            'casino': 'https://kenney.nl/assets/casino-audio', 'digital': 'https://kenney.nl/assets/digital-audio'}
    with open(od + '/audio_sources.txt', 'w') as f:
        f.write('Rossen Reports explainer: the "unpaid toll" text scam. Every recorded audio file in the mix, with its source and license.\n')
        f.write('All are CC0 1.0 (public domain dedication, commercial use allowed, no attribution required). None come from a music library that registers with Content ID.\n\n')
        for u in sorted(USED):
            if u.startswith('kenney/'): src = PACK[u.split('/')[1]] + '  (Kenney, kenney.nl)'
            else: src = 'https://github.com/sgossner/VSCO-2-CE  (Versilian Studios Chamber Orchestra 2 Community Edition' + (', VSCO 1 drums folder' if 'VSCO 1' in u else '') + ')'
            f.write(f'{u}\n    source: {src}\n    license: CC0 1.0\n')
        f.write('\nComposed (not recorded files): the whole score, written note by note in score_toll.py on the 96 BPM grid and played by the VSCO '
                'instrument recordings above: the hook\'s ticking rim and low horn, the evidence walk (pizzicato bass, brushes, the clarinet answer '
                'after each mark, the rising xylophone on each mark), the held tension of the fake page, the stat\'s brass chord, the groove of '
                '"how it works", the warm D-major fix and the final chord. The one beat of silence before the fix is true digital silence. '
                'No synthesized tones are used anywhere; every sound effect is a recorded Kenney file.\n')
    with open(od + '/sources.txt', 'w') as f:
        f.write('On-screen facts and data used in the "unpaid toll" explainer\n\n'
                '"60,000+ COMPLAINTS TO THE FBI IN 2024" (shown with "SOURCE: FBI"): the FBI Internet Crime Complaint Center (IC3) received more than '
                '60,000 complaints about unpaid-toll scam texts in 2024, as reported from FBI figures, e.g.\n'
                '    https://www.newsweek.com/fbi-warning-scam-smishing-texts-delete-phones-2043344\n'
                '    FBI IC3 public service announcement on road-toll smishing (April 2024): https://www.ic3.gov/PSA/2024/PSA240412\n\n'
                'Map outline: Natural Earth 1:110m admin-0 countries (public domain), https://www.naturalearthdata.com/ '
                '(via https://github.com/nvkelso/natural-earth-vector)\n')
print(od, DUR, 's,', len(USED), 'samples,', len(set(HITS)), 'synced hits')
