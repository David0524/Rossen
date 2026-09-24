"""WHAT WOULD YOU DO? series score (one script for every episode). Composed in code on the 96 BPM grid, played by recorded
instrument samples (VSCO 2 CE and its VSCO 1 drums, CC0); physical sound effects are recorded Kenney samples (CC0).

Reads wwyd/template.json and wwyd/epNN.json and builds the same timeline as wwyd.js. The recurring parts always get the
same music and sounds at the same beats: the title's question motif; the freeze (the music cuts out under a record
scratch and a camera shutter, the options land on beats 2, 3, 4); the pause (a ticking clock over a held low horn,
climbing on the last three beats); one sting per verdict (WRONG: a low buzzer and a sagging trombone; CLOSE: a composed
"almost" figure on xylophone and glock; RIGHT: a trumpet fanfare with a bright chime); takeaway; end.
Mood: tense during the call (Dm, pizzicato and spiccato strings, a sneaky clarinet), playful through the reveals
(xylophone and pizzicato bounce), warm when the Grandson answers (held horns in D major).

usage: python3 score_wwyd.py wwyd/ep01   ->  out/rossen-wwyd-ep01/score.wav, samples_used.txt, audio_sources.txt
       HITS_ONLY=1 ...                   ->  score_hits.wav (the hits alone, for sync checks)
"""
import numpy as np, subprocess, wave, sys, os, re, glob, math, json
SR = 48000
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audio')
EP_PATH = sys.argv[1] if len(sys.argv) > 1 else 'wwyd/ep01'
TPL = json.load(open('wwyd/template.json')); EP = json.load(open(EP_PATH + '.json'))
SEGS = []   # the same timeline wwyd.js builds
def _add(kind, bars, sid):
    b0 = SEGS[-1]['b0'] + SEGS[-1]['bars'] if SEGS else 0; SEGS.append({'kind': kind, 'bars': bars, 'b0': b0, 'id': sid})
_add('title', TPL['bars']['title'], 'title')
for s in EP['scenes']: _add('scene', s['bars'], s['id'])
_add('freeze', TPL['bars']['freeze'], 'freeze'); _add('pause', TPL['bars']['pause'], 'pause')
for o in EP['options']: _add('reveal', TPL['bars']['reveal'], o['key'])
_add('takeaway', TPL['bars']['takeaway'], 'takeaway'); _add('end', TPL['bars']['end'], 'end')
TOTAL_BARS = SEGS[-1]['b0'] + SEGS[-1]['bars']; DUR = TOTAL_BARS * 2.5
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
if HO: groove = roll_to = tomfill = swell_to = lambda *a, **k: None
CH['Gm'] = (['D4', 'G4', 'Bb3'], ['G1', 'D2'], ['G2', 'Bb2'], 'G1')
CROOT = {'Dm': 'D2', 'D': 'D2', 'Bb': 'Bb1', 'Gm': 'G2', 'G': 'G2', 'A': 'A1', 'Bm': 'B1', 'Em': 'E2', 'C': 'C2'}
TONES = {'Dm': ('D5', 'F5', 'A5'), 'D': ('D5', 'F#5', 'A5'), 'Bb': ('D5', 'F5', 'Bb5'), 'Gm': ('D5', 'G5', 'Bb5'), 'G': ('D5', 'G5', 'B5'), 'A': ('C#5', 'E5', 'A5')}
SEG = {s['id']: s for s in SEGS}
def SA(seg, bar=1, beat=1): return AT(seg['b0'] + bar - 1, beat)
REVEAL_CH = {'WRONG': ['Dm Dm Bb A', 'Dm Dm Bb A'], 'CLOSE': ['Bb Bb A A', 'Gm Gm A A'], 'RIGHT': ['D D G A', 'D D G D']}
TCH = {'title': ['Dm Dm Bb A', 'Dm Dm Bb A'], 'takeaway': ['G G A A', 'D D G A'], 'end': ['D D G A', 'D D D D']}
rows, mood = {}, {}
for s in SEGS:
    if s['kind'] in ('freeze', 'pause'): continue          # the music stops for the freeze and the pause
    if s['kind'] == 'reveal': ch = REVEAL_CH[next(o for o in EP['options'] if o['key'] == s['id'])['verdict']]; md = 'play'
    elif s['kind'] == 'scene': ch = next(x for x in EP['scenes'] if x['id'] == s['id'])['chords']; md = 'tense'
    else: ch = TCH[s['kind']]; md = 'tense' if s['kind'] == 'title' else 'warm'
    for k in range(s['bars']): rows[s['b0'] + k] = ch[k]; mood[s['b0'] + k] = md
STAMP = SA(SEG['end'], 2, 2)
if not HO:
    for bar, row in rows.items():
        groove(BB(bar), min(BB(bar + 1), STAMP / BEAT), .5 if mood[bar] == 'tense' else .6, .08 if mood[bar] == 'tense' else .12)
        for k, ch in enumerate(row.split()):
            bb = BB(bar, k + 1)
            if B(bb) >= STAMP: break
            r = CROOT[ch]; cpz(r, B(bb), .7, dur=.28); cpz(r, B(bb + .5), .6, dur=.28); cbp(r.replace('2', '1') if r[-1] == '2' else r.replace('1', '0'), B(bb), .4, dur=.3)
            if mood[bar] == 'tense':   # spiccato violins pulse, a sneaky clarinet answers
                for j in range(4): vsp(TONES[ch][j % 2], B(bb + j * .25), .3, dur=.1)
            elif mood[bar] == 'play':  # xylophone bounce on the chord tones
                xyl(TONES[ch][k % 3], B(bb), .3, dur=.15); xyl(TONES[ch][(k + 1) % 3], B(bb + .5), .26, dur=.15)
            else:
                if k % 2 == 0: [hnl(n, B(bb), .3, dur=BEAT * 2 - .1, rel=.25) for n in (('D3', 'F#3', 'A3') if ch == 'D' else ('G2', 'B2', 'D3') if ch == 'G' else ('A2', 'C#3', 'E3'))]
def capsnd(t, two=True): xyl('D6', t, .3); fx('casino/card-place-1.ogg', t, .15); (two and (xyl('A6', t + E8, .28), fx('casino/card-place-2.ogg', t + E8, .13)))
def push(t): fx('casino/card-slide-3.ogg', t - .15, .3)
def fxa(name, t, g=1.0, pan=0.0):   # samples that swell in: align their first audible attack
    x = load(K + name); e = np.convolve(np.abs(x).max(1), np.ones(96) / 96, 'same'); att = int(np.argmax(e >= .15 * e.max()))
    USED.add(K + name); put(x, t - att / SR, g, pan)
def stamp_hit(t, g=1.0, ch='D'): kick(t, .85 * g); timp(t, .8 * g); cbp(CH[ch][3], t, .9 * g); fx('impact/impactPunch_heavy_000.ogg', t, .45 * g)
def pushes():
    for s in SEGS[1:]:
        if s['kind'] not in ('freeze', 'pause'): push(s['b0'] * 2.5)

# ---------------- the recurring parts (identical in every episode) ----------------
s = SEG['title']
stamp_hit(0.0, 1.0, 'Dm'); fx('impact/impactWood_heavy_000.ogg', 0.0, .45)                   # WHAT WOULD YOU DO? on frame 0
for k, n in enumerate(('D5', 'F5', 'A5', 'G#5')): xyl(n, SA(s, 1, 2 + k * .5), .5, dur=.2)    # the question motif, left hanging
fx('casino/card-place-1.ogg', SA(s, 1, 2), .2)                                                # EPISODE n
s = SEG['freeze']; t = SA(s)
fxa('interface/scratch_004.ogg', t, .55); fx('interface/switch_007.ogg', t, .5); kick(t, .9); timp(t, .9); cbp('D1', t, .8); one(CRASH_MF, t, .25)   # FREEZE!
for i in range(3):
    tt = SA(s, 1, 2 + i); fx('casino/card-place-2.ogg', tt, .35); kick(tt, .6); one(RIM, tt, .4, .1); xyl(('A5', 'B5', 'C#6')[i], tt, .5)   # the options land
s = SEG['pause']
if not HO:
    for n in ('A1', 'E2'): hnl(n, SA(s), .35, dur=2 * 2.5 - .2, rel=.3)                         # held low horn under the clock
for k in range(8):
    tt = SA(s) + k * BEAT
    if not HO: fx('interface/tick_002.ogg', tt, .5); one(CLAVE, tt, .2); fx('interface/tick_001.ogg', tt + E8, .26)
    if k % 2 == 0 and not HO: kick(tt, .4)
    if k >= 5: xyl(('A5', 'B5', 'C#6')[k - 5], tt, .5); glk(('A5', 'B5', 'C#6')[k - 5], tt, .3)
roll_to(SA(s, 2, 4), SA(s, 2, 4) + BEAT, .35, TIMP_ROLL)
def sting(v, t):
    if v == 'WRONG':
        kick(t, .9); timp(t, .8); cbp('D1', t, .9); fx('digital/lowThreeTone.ogg', t, .3); fx('interface/error_004.ogg', t, .3)
        for k, n in enumerate(('C3', 'B2', 'Bb2', 'A2')): tbs(n, t + E8 + k * E8, .6, dur=.25 if k < 3 else .5)   # a sagging "wah-wah-wah-waaah"
    elif v == 'CLOSE':   # composed: "almost..." on xylophone and glock, a question that doesn't resolve
        kick(t, .8); timp(t, .6); cbp('Bb0', t, .8); one(CLAVE, t, .4)
        for k, n in enumerate(('A5', 'Bb5', 'A5', 'E5')): xyl(n, t + k * S16 * 1.5, .55, dur=.15)
        glk('E6', t + E8 * 2, .35); glk('D#6', t + E8 * 2.5, .3); fx('interface/pluck_002.ogg', t, .3)
    else:
        kick(t, 1.0); timp(t, .9); cbp('D1', t, 1.0); one(CRASH, t, .45); fx('interface/confirmation_002.ogg', t, .45); fx('digital/threeTone1.ogg', t, .25)
        for k, n in enumerate(('D4', 'F#4', 'A4', 'D5')): tps(n, t + k * S16, .8, dur=.2 if k < 3 else .5)
        for k, n in enumerate(('D6', 'F#6', 'A6')): glk(n, t + k * S16, .4)
for i, o in enumerate(EP['options']):
    s = SEG[o['key']]; sting(o['verdict'], SA(s))
    if i == 0: fx('interface/pluck_001.ogg', SA(s, 1, 1.5), .3)                                # Jeff steps in
    for cp in o.get('caps', []): capsnd(SA(s, cp[0], cp[1]))
    if o['verdict'] == 'RIGHT' and not HO:                                                      # warm: held horns in D when he answers
        for n in ('D3', 'F#3', 'A3'): hnl(n, SA(s, 2), .45, dur=2.5 - .1, rel=.4)
s = SEG['takeaway']
stamp_hit(SA(s), 1.0, 'G'); stamp_hit(SA(s, 1, 1.5), .9, 'A')
glk('A6', SA(s, 2), .45); fx('casino/card-place-1.ogg', SA(s, 2), .3); kick(SA(s, 2), .6)       # BONUS TIP
for k in range(2): t = SA(s, 2, 1.5) + k * E8; xyl(('D6', 'F#6')[k], t, .4); fx('casino/card-place-2.ogg', t, .2); kick(t, .5)
fx('interface/pluck_002.ogg', SA(s, 1, 2), .28)
s = SEG['end']
stamp_hit(SA(s), 1.0); fx('rpg/bookPlace1.ogg', SA(s), .4)
stamp_hit(SA(s, 1, 1.5), .9); glk('A6', SA(s, 1, 1.5), .4)
fx('interface/pluck_002.ogg', SA(s, 1, 2), .28)
roll_to(SA(s, 2), STAMP, .45, TIMP_ROLL); tomfill(SA(s, 2, 1.25), STAMP, .45, S16 / 2)
for n in ('D2', 'F#2', 'A2'): hnl(n, STAMP, .9, dur=1.2, rel=.3)
for n in ('D2', 'A1'): tbl(n, STAMP, .85, dur=1.2, rel=.3)
cbp('D1', STAMP, 1.0); cpz('D2', STAMP, .9); timp(STAMP, 1.0); kick(STAMP, 1.0); one(CRASH, STAMP, .5); glk('D6', STAMP, .45)
fx('impact/impactPlank_medium_000.ogg', STAMP, .55); fx('impact/impactSoft_heavy_000.ogg', STAMP, .4)
pushes()

# ---------------- episode: scene captions and cues ----------------
def ring(t):
    for j in range(8): glk(('D6', 'F#6')[j % 2], t + j * .05, .3)
    fx('interface/tick_002.ogg', t, .3)
CUES = {
    'ring': ring,
    'answer': lambda t: (fx('interface/click_001.ogg', t, .6), kick(t, .6)),
    'peek': lambda t: [cla(n, t + k * S16 / 2, .45, dur=.08) for k, n in enumerate(('A3', 'Bb3', 'A3', 'Bb3'))],
    'sneak': lambda t: [cla(n, t + k * S16, .5, dur=.14) for k, n in enumerate(('A3', 'G#3', 'G3', 'F3'))],
    'envelope': lambda t: (fx('rpg/cloth3.ogg', t - .1, .35), fx('rpg/bookPlace1.ogg', t, .4), kick(t, .7)),
    'cash': lambda t: (fx('rpg/handleCoins.ogg', t, .45), fx('casino/card-fan-1.ogg', t, .35), kick(t, .8), one(RIM, t, .45, .1)),
    'walkoff': lambda t: ([fx(f'impact/footstep_wood_00{k % 4}.ogg', t + k * E8, .35) for k in range(4)], [tbs(n, t + k * E8, .45, dur=.2) for k, n in enumerate(('D3', 'C#3', 'C3'))]),
    'highlight': lambda t: (fxa('interface/scratch_004.ogg', t, .4), kick(t, .6), one(RIM, t, .4, .1)),
    'play': lambda t: (fx('interface/click_001.ogg', t, .55), kick(t, .55)),
    'copied': lambda t: (stamp_hit(t, .8, 'A'), fx('interface/glitch_002.ogg', t, .3)),
    'hangup': lambda t: (fx('interface/click_001.ogg', t, .6), fx('interface/close_001.ogg', t, .45), kick(t, .7)),
    'call': lambda t: (fx('interface/click_001.ogg', t, .6), kick(t, .6), fx('interface/tick_002.ogg', t + E8, .35), fx('interface/tick_002.ogg', t + 2 * E8, .35)),
    'answerwarm': lambda t: (fx('interface/confirmation_001.ogg', t, .45), kick(t, .7), [glk(n, t + k * S16, .4) for k, n in enumerate(('D6', 'F#6', 'A6'))]),
    'collapse': lambda t: (fx('impact/impactSoft_heavy_000.ogg', t, .55), fx('rpg/cloth3.ogg', t + .05, .4), kick(t, .9), timp(t, .6), [tbs(n, t + .1 + k * S16, .55, dur=.12) for k, n in enumerate(('D3', 'C3', 'A2', 'F2', 'D2'))]),
}
for sc in EP['scenes']:
    s = SEG[sc['id']]
    for cp in sc.get('caps', []): capsnd(SA(s, cp[0], cp[1]), len(cp) > 3)
for sid, bar, beat, cue in EP['cues']: CUES[cue](SA(SEG[sid], bar, beat))

# ---------------- master ----------------
fade = int(.5 * SR); out[-fade:] *= np.linspace(1, 0, fade)[:, None] ** 2
out = np.tanh(out * 1.1) / 1.1
out *= (10 ** (-1 / 20)) / max(1e-6, np.abs(out).max())
od = 'out/rossen-wwyd-' + os.path.basename(EP_PATH); os.makedirs(od, exist_ok=True)
with wave.open(od + ('/score_hits.wav' if HO else '/score.wav'), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(out, -1, 1) * 32767).astype('<i2').tobytes())
if not HO:
    with open(od + '/samples_used.txt', 'w') as f: f.write('\n'.join(sorted(USED)) + '\n')
    PACK = {'interface': 'https://kenney.nl/assets/interface-sounds', 'impact': 'https://kenney.nl/assets/impact-sounds', 'rpg': 'https://kenney.nl/assets/rpg-audio',
            'casino': 'https://kenney.nl/assets/casino-audio', 'digital': 'https://kenney.nl/assets/digital-audio'}
    with open(od + '/audio_sources.txt', 'w') as f:
        f.write('WHAT WOULD YOU DO? #%d: every recorded audio file in the mix, with its source and license.\n' % EP['num'])
        f.write('All are CC0 1.0 (public domain dedication, commercial use allowed, no attribution required). None come from a music library that registers with Content ID.\n\n')
        for u in sorted(USED):
            if u.startswith('kenney/'): src = PACK[u.split('/')[1]] + '  (Kenney, kenney.nl)'
            else: src = 'https://github.com/sgossner/VSCO-2-CE  (Versilian Studios Chamber Orchestra 2 Community Edition' + (', VSCO 1 drums folder' if 'VSCO 1' in u else '') + ')'
            f.write(f'{u}\n    source: {src}\n    license: CC0 1.0\n')
        f.write('\nComposed (not recorded files): the whole score, written note by note in score_wwyd.py on the 96 BPM grid and played by the VSCO instrument recordings above. '
                'That includes the CLOSE sting ("almost...": xylophone A5 Bb5 A5 E5 plus glock E6 D#6), the WRONG trombone sag, the RIGHT fanfare, the title question motif, '
                'the phone-ring trills (glockenspiel) and the Scammer\'s clarinet sneaks. No synthesized tones are used anywhere.\n')
print(od, DUR, 's,', TOTAL_BARS, 'bars,', len(USED), 'samples;', ' | '.join(f"{s['id']} {s['b0']}+{s['bars']}" for s in SEGS))
