"""Fake officer / jury-duty warrant explainer score (officer.js). Composed in code on the 96 BPM grid, played by recorded
instrument samples (VSCO 2 CE and its VSCO 1 drums, CC0); physical sound effects are recorded Kenney samples (CC0).
Mood: tense and official during the call (D minor, a snare march, timpani, held low horns, spiccato violins);
building through IT GETS CRAZIER (layers added bar by bar: kick, sixteenth violins, tambourine, a brass stab on each
new demand climbing in pitch, a swell into the slam); confident from the logo slam when Jeff enters (D major, horns and
trumpets, a steady groove). Tempo never changes: the escalation is in the content.

usage: python3 score_officer.py            ->  out/rossen-officer-scam/score.wav, samples_used.txt, audio_sources.txt, hits.json
       HITS_ONLY=1 python3 score_officer.py ->  score_hits.wav (the synced hits alone, for the sync check)
"""
import numpy as np, subprocess, wave, sys, os, re, glob, math, json
SR = 48000
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audio')
DUR = 20 * 2.5 + 2
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
STAMP = AT(20)   # the rubber stamp lands; the official logo is revealed

# ---------------- the chords, one row per bar ----------------
ROWS = {0: 'Dm Dm Bb A', 1: 'Dm Dm Gm A', 2: 'Dm Dm Bb A', 3: 'Gm Gm A A', 4: 'Dm Dm Bb A',       # the call: tense, official
        5: 'Dm Dm Bb Bb', 6: 'Gm Gm A A', 7: 'Dm Dm Bb C', 8: 'Eb Eb F A', 9: 'Dm Bb C A',          # it gets crazier
        10: 'D D G A', 11: 'D D G A', 12: 'G G A A', 13: 'D D G A', 14: 'D D G A', 15: 'G G D D',      # Jeff: confident
        16: 'D D G A', 17: 'G G A A', 18: 'D D G A', 19: 'D D G A'}
def mood(bar): return 'call' if bar <= 4 else 'build' if bar <= 9 else 'jeff'
if not HO:
    for bar, row in ROWS.items():
        md = mood(bar)
        for k, ch in enumerate(row.split()):
            bb = BB(bar, k + 1)
            if B(bb) >= STAMP - BEAT: break
            r = CROOT[ch]; lo = r.replace('2', '1') if r[-1] == '2' else r.replace('1', '0')
            cbp(lo, B(bb), .45 if md == 'call' else .4, dur=.3)
            if md == 'call':
                cpz(r, B(bb), .55, dur=.3)
                for j in range(2): vsp(TONES[ch][j % 2], B(bb + j * .5), .26, dur=.12)                   # spiccato eighths, held back
                if k in (1, 3): snare(B(bb), .3)                                                          # the march: snare on 2 and 4
                if k == 3: [one(SNR2, B(bb + .5 + q * .125), .16 + .05 * q, .05) for q in range(4)]      # a ruff into the next bar
            elif md == 'build':
                lvl = bar - 5                                                                             # one layer more every bar
                cpz(r, B(bb), .65, dur=.28); cpz(r, B(bb + .5), .55, dur=.28)
                n16 = 4 if lvl >= 2 else 2
                for j in range(n16): vsp(TONES[ch][j % 2 if lvl < 3 else j % 3], B(bb + j / n16), .26 + .03 * lvl, dur=.1)
                if lvl >= 1: vla(TONES[ch][2].replace('5', '4'), B(bb + .5), .3, dur=.2)
            else:
                cpz(r, B(bb), .7, dur=.28); cpz(r, B(bb + .5), .6, dur=.28)
                xyl(TONES[ch][k % 3], B(bb), .22, dur=.15)
            if k % 2 == 0:   # held low brass under each half bar
                inst = hnl if md != 'build' or bar < 8 else tbl
                for n in PAD[ch]: inst(n, B(bb), .22 if md == 'call' else .26, dur=BEAT * 2 - .08, rel=.25)
        # rhythm section per mood
        if md == 'call':
            timp(AT(bar), .45); kick(AT(bar), .5); kick(AT(bar, 3), .4)
        elif md == 'build':
            groove(BB(bar), BB(bar + 1), .45 + .06 * (bar - 5), .06 + .03 * (bar - 5))
            timp(AT(bar), .5 + .08 * (bar - 5))
        else:
            if B(BB(bar + 1)) <= STAMP - BEAT: groove(BB(bar), BB(bar + 1), .62, .13)
            else: groove(BB(bar), BB(bar, 4), .62, .13)
    swell_to(AT(10), .5); roll_to(AT(9, 3), AT(10), .4)                                                  # into the slam
    for n in ('D3', 'F#3', 'A3'): tpl(n, AT(10, 2), .2, dur=2.5 * 1.5, rel=.4)                          # Jeff's warm trumpets

# ---------------- sounds on the picture's beats ----------------
def ring(t):
    for j in range(8): glk(('D6', 'F6')[j % 2], t + j * .05, .32)
    fx('interface/tick_002.ogg', t, .3)
def capsnd(t): xyl('D6', t, .26); fx('casino/card-place-1.ogg', t, .14)
def popsnd(t, n='A5'): xyl(n, t, .42); fx('casino/card-place-2.ogg', t, .3); kick(t, .55); one(RIM, t, .35, .1); H(t, 'pop')
def stamp_hit(t, g=1.0, ch='D'): kick(t, .85 * g); timp(t, .8 * g); cbp(CH[ch][3], t, .9 * g); fx('impact/impactPunch_heavy_000.ogg', t, .45 * g); H(t, 'stamp')
def push(t): fx('casino/card-slide-3.ogg', t - .15, .28)
def fxa(name, t, g=1.0, pan=0.0):   # samples that swell in: align their first audible attack
    x = load(K + name); e = np.convolve(np.abs(x).max(1), np.ones(96) / 96, 'same'); att = int(np.argmax(e >= .15 * e.max()))
    USED.add(K + name); put(x, t - att / SR, g, pan)
CAP_T = [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (10, 2), (11, 2), (12, 2), (13, 2), (14, 1), (15, 2), (16, 2), (17, 1)]
for bar, n in CAP_T:
    for i in range(n):
        if bar == 0 and i == 0: continue   # frame 0 belongs to the ring
        capsnd(AT(bar) + i * E8)
for b in (5, 7, 11, 14, 15, 16, 17, 18): push(AT(b))

# HOOK: ringing in frame 0; he answers on the downbeat of bar 1; the warrant startles him
for t in (0.0, AT(0, 3)): ring(t); H(t, 'ring')
fx('interface/click_001.ogg', AT(1), .6); kick(AT(1), .7); timp(AT(1), .6); H(AT(1), 'answer')
fx('rpg/cloth2.ogg', AT(1, 3) - .05, .3); tbs('D2', AT(1, 3), .55, dur=.4); kick(AT(1, 3), .7); H(AT(1, 3), 'startle')
# WHY IT FEELS REAL: name, address; badge number, case number; the badge glints
for (bar, bt), n in zip([(2, 2), (2, 3), (3, 2), (3, 3)], ('A5', 'C6', 'A5', 'D6')): popsnd(AT(bar, bt), n)
glk('A6', AT(3, 2) - .1, .35); glk('E7', AT(3, 2) - .05, .25)
# the caller-ID swap: the sticker pops out of his phone, then is slapped on on beat 3; a sly clarinet
fx('interface/pluck_001.ogg', AT(4, 2) - .1, .45)
fx('rpg/bookPlace1.ogg', AT(4, 3), .5); kick(AT(4, 3), .85); one(RIM, AT(4, 3), .45, .1); timp(AT(4, 3), .5); H(AT(4, 3), 'slap')
for k, n in enumerate(('A3', 'Bb3', 'A3', 'F3')): cla(n, AT(4, 3.5) + k * S16, .45, dur=.12)
# IT GETS CRAZIER: the text buzzes twice, the tap, the dive
for t in (AT(5, 2), AT(5, 3)): fx('interface/toggle_001.ogg', t, .5); glk('A6', t, .3); kick(t, .5); H(t, 'buzz')
fx('interface/click_001.ogg', AT(5, 4), .6); kick(AT(5, 4), .6); H(AT(5, 4), 'tap')
fx('casino/card-slide-1.ogg', AT(6) - .1, .35)
fxa('interface/scratch_004.ogg', AT(6, 2), .28); kick(AT(6, 2), .9); timp(AT(6, 2), .45); one(RIM, AT(6, 2), .4, .1); H(AT(6, 2), 'highlight')
stamp_hit(AT(6, 3), .8, 'A')                                                                  # PAY NOW
# the demands: each new one a brass stab, a step higher
for k, (bar, bt) in enumerate([(7, 2), (7, 4), (8, 2), (8, 4)]):
    t = AT(bar, bt); fx('casino/chips-stack-%d.ogg' % (1 + k % 2), t, .45); kick(t, .75); one(RIM, t, .4, .1); H(t, 'demand')
    for n in (('D4', 'F4', 'A4'), ('Eb4', 'G4', 'Bb4'), ('F4', 'A4', 'C5'), ('G4', 'Bb4', 'D5'))[k]: tps(n, t, .55 + .08 * k, dur=.25)
    tbs(('D3', 'Eb3', 'F3', 'G3')[k], t, .6, dur=.25)
fx('casino/card-fan-1.ogg', AT(9) - .12, .45)                                                  # the list is swept away
stamp_hit(AT(9), 1.0, 'Dm'); fx('rpg/handleCoins.ogg', AT(9), .5); one(CRASH, AT(9), .35)       # BRING CASH.
fx('interface/drop_001.ogg', AT(9, 3), .5); kick(AT(9, 3), .7); timp(AT(9, 3), .6); H(AT(9, 3), 'pin')   # I'LL MEET YOU.
for k, n in enumerate(('A4', 'Bb4', 'C5', 'C#5')): tps(n, AT(9, 3.5) + k * S16, .5, dur=.12)
# THE TELLS: the logo slams, the "officer" is knocked off, Jeff pops up
stamp_hit(AT(10), 1.1, 'D'); one(CRASH, AT(10), .55); fx('impact/impactWood_heavy_000.ogg', AT(10), .5)
for n in ('D4', 'F#4', 'A4'): tps(n, AT(10), .85, dur=.45)
for n in ('D2', 'A2'): hns(n, AT(10), .9, dur=.5)
fx('rpg/cloth3.ogg', AT(10) + .05, .45)
fx('interface/pluck_002.ogg', AT(10, 2), .35); kick(AT(10, 2), .5); H(AT(10, 2), 'jeff')
for b in (11, 12, 13): fx('casino/card-slide-2.ogg', AT(b) - .2, .25)                          # the magnifier moves on
def lie(t, k):
    stamp_hit(t, 1.0, ('D', 'G', 'A')[k]); one(CRASH_MF, t, .25)
    for j, n in enumerate(('D5', 'A4') if k < 2 else ('D5', 'A4', 'D4')): tps(n, t + j * S16, .6, dur=.15)
for k, t in enumerate((AT(11, 3), AT(12, 3), AT(13, 3))): lie(t, k)
# the running gag: the cap slips (a sagging trombone), the badge drops and clatters, the cap flies off and lands
fx('rpg/cloth1.ogg', AT(11, 3) + .02, .45)
for k, n in enumerate(('A2', 'G#2', 'G2')): tbs(n, AT(11, 3.5) + k * S16, .45, dur=.14)
fx('interface/pluck_001.ogg', AT(12, 3) + .02, .35)
fx('impact/impactMetal_light_001.ogg', AT(12, 4), .55); kick(AT(12, 4), .5); H(AT(12, 4), 'badge lands')
fx('impact/impactMetal_light_002.ogg', AT(12, 4) + .14, .25)
fx('rpg/cloth4.ogg', AT(13, 3) + .03, .45)
for k, n in enumerate(('D5', 'F5', 'A5', 'D6')): xyl(n, AT(13, 3.25) + k * S16 / 2, .35, dur=.1)
fx('impact/impactSoft_heavy_000.ogg', AT(13, 4), .5); kick(AT(13, 4), .55); H(AT(13, 4), 'cap lands')
# THE FIX: hang up, look it up, call it, report it
fx('interface/click_001.ogg', AT(14, 3), .65); fx('interface/close_001.ogg', AT(14, 3), .5); kick(AT(14, 3), .8); timp(AT(14, 3), .6); H(AT(14, 3), 'hang up')
def typing(t0, t1, n, g=.2):
    for i in range(n): fx(('interface/click_002.ogg', 'interface/click_003.ogg')[i % 2], t0 + (i + 1) * (t1 - t0) / n - .02, g * (.8 + .2 * (i % 3)))
typing(AT(15) + .1, AT(15, 2.6), 16)
fx('interface/confirmation_001.ogg', AT(15, 3), .45); popsnd(AT(15, 3), 'D6')
for t in (AT(16, 1.5), AT(16, 2.5)): [glk(('D6', 'F#6')[j % 2], t + j * .05, .22) for j in range(6)]
fx('interface/pluck_002.ogg', AT(16, 2), .3)
fx('interface/confirmation_002.ogg', AT(16, 3), .45); kick(AT(16, 3), .7); one(RIM, AT(16, 3), .4, .1); H(AT(16, 3), 'check')
for k, n in enumerate(('D6', 'F#6', 'A6')): glk(n, AT(16, 3) + k * S16, .35)
typing(AT(17) + .1, AT(17, 1.9), 19)
popsnd(AT(17, 2), 'A5'); popsnd(AT(17, 3), 'D6')
# THE LINE and the sign-off
stamp_hit(AT(18), 1.0, 'D'); one(CRASH_MF, AT(18), .3); fx('rpg/bookPlace1.ogg', AT(18), .4)
fx('interface/pluck_002.ogg', AT(18, 2), .28)
stamp_hit(AT(18, 3), .95, 'G'); stamp_hit(AT(18, 4), .9, 'A')
roll_to(AT(19, 2), STAMP, .45, TIMP_ROLL); tomfill(AT(19, 4), STAMP, .45, S16 / 2)
if not HO:
    for n in ('D2', 'F#2', 'A2'): hnl(n, STAMP, .9, dur=1.4, rel=.4)
    for n in ('D2', 'A1'): tbl(n, STAMP, .85, dur=1.4, rel=.4)
cbp('D1', STAMP, 1.0); cpz('D2', STAMP, .9); timp(STAMP, 1.0); kick(STAMP, 1.0); one(CRASH, STAMP, .5); glk('D6', STAMP, .45); H(STAMP, 'rubber stamp')
fx('impact/impactPlank_medium_000.ogg', STAMP, .55); fx('impact/impactSoft_heavy_000.ogg', STAMP, .4)

# ---------------- master ----------------
fade = int(.8 * SR); out[-fade:] *= np.linspace(1, 0, fade)[:, None] ** 2
out = np.tanh(out * 1.1) / 1.1
out *= (10 ** (-1 / 20)) / max(1e-6, np.abs(out).max())
od = 'out/rossen-officer-scam'; os.makedirs(od, exist_ok=True)
with wave.open(od + ('/score_hits.wav' if HO else '/score.wav'), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(out, -1, 1) * 32767).astype('<i2').tobytes())
json.dump(sorted(set(HITS)), open(od + '/hits.json', 'w'))
if not HO:
    with open(od + '/samples_used.txt', 'w') as f: f.write('\n'.join(sorted(USED)) + '\n')
    PACK = {'interface': 'https://kenney.nl/assets/interface-sounds', 'impact': 'https://kenney.nl/assets/impact-sounds', 'rpg': 'https://kenney.nl/assets/rpg-audio',
            'casino': 'https://kenney.nl/assets/casino-audio', 'digital': 'https://kenney.nl/assets/digital-audio'}
    with open(od + '/audio_sources.txt', 'w') as f:
        f.write('Rossen Reports explainer: the fake officer / jury-duty warrant scam. Every recorded audio file in the mix, with its source and license.\n')
        f.write('All are CC0 1.0 (public domain dedication, commercial use allowed, no attribution required). None come from a music library that registers with Content ID.\n\n')
        for u in sorted(USED):
            if u.startswith('kenney/'): src = PACK[u.split('/')[1]] + '  (Kenney, kenney.nl)'
            else: src = 'https://github.com/sgossner/VSCO-2-CE  (Versilian Studios Chamber Orchestra 2 Community Edition' + (', VSCO 1 drums folder' if 'VSCO 1' in u else '') + ')'
            f.write(f'{u}\n    source: {src}\n    license: CC0 1.0\n')
        f.write('\nComposed (not recorded files): the whole score, written note by note in score_officer.py on the 96 BPM grid and played by the VSCO '
                'instrument recordings above: the snare march and ruffs of the call, the phone-ring trills (glockenspiel), the climbing brass stab on each '
                'new demand, the Scammer\'s clarinet sneak, the sagging trombone when the cap slips, the xylophone run when it flies off, the LIE stings, '
                'the ringback trills and the final chord. No synthesized tones are used anywhere; every sound effect is a recorded Kenney file.\n')
print(od, DUR, 's,', len(USED), 'samples,', len(set(HITS)), 'synced hits')
