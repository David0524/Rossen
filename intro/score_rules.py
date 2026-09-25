"""JEFF'S RULES series score (one script for every episode). Recorded samples only, no synthesis.

Reads rules/template.json and rules/epNN.json and builds the same timeline as rules.js. The recurring parts (title,
rule reveal, recap, end) always get the same sounds at the same beats; the rule reveal has a signature: a gavel,
timpani and low brass under each of the rule's two stamp strikes, with the high glock pair. Episode scenes get
chords per bar and cues from the episode data, played from a shared cue library (add a cue here, use it in any
episode). Voiceover-ready arrangement: no melodic lines in the voice range; drums, pizzicato bass and low horns carry
it, hits land in kick, timpani and bass. VSCO 2 CE / VSCO 1 (CC0) and Kenney (CC0).

usage: python3 score_rules.py rules/ep01   ->  out/rossen-rules-ep01/score.wav (+ samples_used.txt)
       HITS_ONLY=1 ...                     ->  score_hits.wav, the hits alone, for checking sync
"""
import numpy as np, subprocess, wave, sys, os, re, glob, math, json
SR = 48000
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audio')
EP_PATH = sys.argv[1] if len(sys.argv) > 1 else 'rules/ep01'
TPL = json.load(open('rules/template.json')); EP = json.load(open(EP_PATH + '.json'))
# the same timeline rules.js builds (the template's fixed bar counts + the episode's scenes)
SEGS = []
def _add(kind, bars, sid=None):
    b0 = SEGS[-1]['b0'] + SEGS[-1]['bars'] if SEGS else 0; SEGS.append({'kind': kind, 'bars': bars, 'b0': b0, 'id': sid or kind})
_add('title', TPL['bars']['title'])
for s in EP['scenes'][:EP['ruleAfter']]: _add('scene', s['bars'], s['id'])
_add('rule', TPL['bars']['rule'])
for s in EP['scenes'][EP['ruleAfter']:]: _add('scene', s['bars'], s['id'])
_add('recap', TPL['bars']['recap']); _add('end', TPL['bars']['end'])
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
PAD = {'Dm': ('D2', 'A2'), 'D': ('D2', 'A2'), 'Bb': ('Bb1', 'F2'), 'Gm': ('G1', 'D2'), 'G': ('G1', 'D2'), 'A': ('A1', 'E2'), 'Bm': ('B1', 'F#2'), 'Em': ('E2', 'B2'), 'C': ('C2', 'G2')}
SEG = {s['id']: s for s in SEGS}
def SA(seg, bar=1, beat=1): return AT(seg['b0'] + bar - 1, beat)
# template chords (fixed); episode chords from the data
TCH = {'title': ['D D G G', 'Bm Bm A A'], 'rule': ['G G A A', 'D D D D'], 'recap': ['G G A A', 'D D G A'], 'end': ['D D G A', 'D D D D', 'D D D D']}   # the third end bar sits under the closing card (nothing plays past the stamp)
rows = {}
for s in SEGS:
    ch = TCH.get(s['kind']) or next(x for x in EP['scenes'] if x['id'] == s['id']).get('chords') or ['D D G A'] * s['bars']
    for k in range(s['bars']): rows[s['b0'] + k] = ch[k]
STAMP = SA(SEG['end'], 2, 2)   # the rubber stamp lands on the official logo
if not HO:
    for bar in range(TOTAL_BARS): groove(BB(bar), min(BB(bar + 1), STAMP / BEAT), .55, .08)
    for bar, row in rows.items():
        for k, ch in enumerate(row.split()):
            bb = BB(bar, k + 1)
            if B(bb) >= STAMP: break
            r = CROOT[ch]; cpz(r, B(bb), .7, dur=.28); cpz(r, B(bb + .5), .6, dur=.28); cbp(r.replace('2', '1') if r[-1] == '2' else r.replace('1', '0'), B(bb), .4, dur=.3)
            if k % 2 == 0: [hnl(n, B(bb), .22, dur=BEAT * 2 - .1, rel=.25) for n in PAD[ch]]   # warm low horns, under the voice
def capsnd(t, two=True): xyl('D6', t, .3); fx('casino/card-place-1.ogg', t, .15); (two and (xyl('A6', t + E8, .28), fx('casino/card-place-2.ogg', t + E8, .13)))
def push(t): fx('casino/card-slide-3.ogg', t - .15, .3)                                  # the camera drop between segments
def stamp_hit(t, g=1.0, ch='D'): kick(t, .85 * g); timp(t, .8 * g); cbp(CH[ch][3], t, .9 * g); fx('impact/impactPunch_heavy_000.ogg', t, .45 * g)
def RULE_STRIKE(t, k):   # the signature: gavel + timpani + low brass + a high glock note (k = strike 0 or 1)
    fx('impact/impactWood_heavy_000.ogg', t, .7); fx('impact/impactPlank_medium_000.ogg', t, .45); kick(t, .9); timp(t, 1.0)
    for n in ('D2', 'A1') if k == 0 else ('D2', 'F#2'): tbl(n, t, .7, dur=.5, rel=.25)
    for n in ('D2', 'A2'): hnl(n, t, .6, dur=.55, rel=.25)
    cbp('D1', t, 1.0); glk(('A6', 'D6')[k], t, .5)

# ---------------- the recurring parts (identical in every episode) ----------------
s = SEG['title']
stamp_hit(0.0, .9); fx('impact/impactWood_heavy_000.ogg', 0.0, .5); glk('D6', 0.0, .4)          # JEFF'S RULES #n is already on screen
for i in range(len(EP['hook'])): t = SA(s, 1, 2) + i * E8; xyl(('D6', 'A6')[i], t, .35); fx('casino/card-place-1.ogg', t, .2); kick(t, .5)   # the hook
fx('interface/pluck_001.ogg', SA(s, 2), .3)                                                  # Jeff pops up
s = SEG['rule']
push(s['b0'] * 2.5); capsnd(SA(s), False)
fx('interface/pluck_002.ogg', SA(s, 1, 2), .3); roll_to(SA(s, 1, 2), SA(s, 1, 3), .35, TIMP_ROLL)   # Jeff steps in
RULE_STRIKE(SA(s, 1, 3), 0); RULE_STRIKE(SA(s, 2), 1)
s = SEG['recap']
push(s['b0'] * 2.5); capsnd(SA(s), False)
for k in range(2): t = SA(s, 1, 1 + k * .5); kick(t, .7); fx('impact/impactWood_heavy_000.ogg', t, .35)   # the rule again, a lighter touch
fx('interface/pluck_001.ogg', SA(s, 1, 1.5), .28)
for k in range(2): t = SA(s, 2, 1 + k * .5); stamp_hit(t, .6, 'G' if k == 0 else 'A'); xyl(('D6', 'A6')[k], t, .35)   # IT'S NOT RUDE. IT'S THE RULE.
s = SEG['end']
push(s['b0'] * 2.5)
stamp_hit(SA(s), 1.0); fx('rpg/bookPlace1.ogg', SA(s), .4)                                    # FOLLOW FOR
stamp_hit(SA(s, 1, 1.5), .9); glk('A6', SA(s, 1, 1.5), .4)                                   # RULE #n+1
fx('interface/pluck_002.ogg', SA(s, 1, 2), .28)
roll_to(SA(s, 2), STAMP, .45, TIMP_ROLL); tomfill(SA(s, 2, 1.25), STAMP, .45, S16 / 2)       # the rubber stamp comes down
for n in ('D2', 'F#2', 'A2'): hnl(n, STAMP, .9, dur=1.2, rel=.3)
for n in ('D2', 'A1'): tbl(n, STAMP, .85, dur=1.2, rel=.3)
cbp('D1', STAMP, 1.0); cpz('D2', STAMP, .9); timp(STAMP, 1.0); kick(STAMP, 1.0); one(CRASH, STAMP, .5); glk('D6', STAMP, .45)
fx('impact/impactPlank_medium_000.ogg', STAMP, .55); fx('impact/impactSoft_heavy_000.ogg', STAMP, .4)

# ---------------- episode scenes: the camera move, captions, cues ----------------
def ring(t):
    for j in range(8): glk(('D6', 'F#6')[j % 2], t + j * .05, .32)
    fx('interface/tick_002.ogg', t, .3)
def fxa(name, t, g=1.0, pan=0.0):
    x = load(K + name); e = np.convolve(np.abs(x).max(1), np.ones(96) / 96, 'same'); att = int(np.argmax(e >= .15 * e.max()))
    USED.add(K + name); put(x, t - att / SR, g, pan)
CUES = {
    'ring': ring,
    'pickup': lambda t: (fx('interface/click_001.ogg', t, .6), kick(t, .5)),
    'urgent': lambda t: (stamp_hit(t, 1.0, 'A'), fx('interface/error_004.ogg', t, .3)),
    'swap': lambda t: (fx('interface/scratch_004.ogg', t, .4), fx('casino/card-place-2.ogg', t, .3), kick(t, .7), one(RIM, t, .45, .1)),
    'fake': lambda t: (stamp_hit(t, 1.0, 'Bb'), fx('impact/impactPunch_heavy_002.ogg', t, .45)),
    'hangup': lambda t: (fx('interface/click_001.ogg', t, .6), fx('interface/close_001.ogg', t, .45), kick(t, .8), timp(t, .6)),
    'yank': lambda t: (fx('rpg/cloth3.ogg', t, .4), fx('impact/impactSoft_medium_000.ogg', t + .1, .35)),
    'cardup': lambda t: (fx('casino/card-slide-3.ogg', t - .1, .35), fx('rpg/bookPlace1.ogg', t + .15, .35)),
    'flip': lambda t: (fx('casino/card-fan-1.ogg', t, .4), kick(t, .7), one(RIM, t, .4, .1)),
    'dial': lambda t: [fx('interface/click_003.ogg', t + j * BEAT / 8, .3, (-.15, .15)[j % 2]) for j in range(len(EP.get('dialDigits', '18005550000')))],
    'call': lambda t: (fx('interface/click_001.ogg', t, .6), kick(t, .6), fx('interface/tick_002.ogg', t + E8, .35), fx('interface/tick_002.ogg', t + 2 * E8, .35)),
    'connect': lambda t: (stamp_hit(t, .8, 'G'), fx('interface/confirmation_002.ogg', t, .45)),
    'check': lambda t: (fx('interface/confirmation_001.ogg', t, .4), kick(t, .7), [glk(n, t + k * S16, .4) for k, n in enumerate(('D6', 'F#6', 'A6'))]),
    # episode 2 (fxa: samples that swell in are aligned by their first audible attack, not their half-peak point)
    'poof': lambda t: (fx('rpg/cloth3.ogg', t - .08, .45), fx('impact/impactSoft_medium_000.ogg', t, .45), kick(t, .6), glk('A6', t, .3)),   # a costume change
    'demand': lambda t: (stamp_hit(t, .9, 'A'), fx('interface/error_004.ogg', t, .25),                                         # the same demand, every time:
                         [tbs(n, t + E8 + k * E8, .5, dur=.2) for k, n in enumerate(('D3', 'C#3', 'C3'))]),                     # a low trombone "wah-wah-wah"
    'label': lambda t: (fx('casino/card-place-1.ogg', t, .3), kick(t, .6), one(RIM, t, .4, .1)),
    'digits': lambda t: (fx('interface/tick_002.ogg', t, .45), fxa('casino/card-place-2.ogg', t, .2), kick(t, .8), one(RIM, t, .45, .1)),
    'vanish': lambda t: (stamp_hit(t, 1.0, 'Bb'), fx('rpg/handleCoins.ogg', t + .02, .4), fx('casino/card-fan-1.ogg', t + .05, .35)),
    'highlight': lambda t: (fxa('interface/scratch_004.ogg', t, .4), kick(t, .55)),
    'rightaway': lambda t: (stamp_hit(t, 1.0, 'A'), fx('impact/impactPunch_heavy_001.ogg', t, .4)),
    'type': lambda t: [fx('interface/click_003.ogg', t + j * BEAT / 8, .32, (-.15, .15)[j % 2]) for j in range(len(EP.get('typeText', '')))],
}
for sc in EP['scenes']:
    s = SEG[sc['id']]; push(s['b0'] * 2.5)
    for cp in sc.get('caps', []): capsnd(SA(s, cp[0], cp[1]), len(cp) > 3)
for sid, bar, beat, cue in EP['cues']: CUES[cue](SA(SEG[sid], bar, beat))

# ---------------- under the closing card: a soft held D major, so the longer card never sits in silence ----------------
_t0 = STAMP + 1.2
if not HO:
    for n in ('D2', 'F#2', 'A2'): hnl(n, _t0, .3, dur=DUR - _t0 - .4, rel=1.0)
    cpz('D2', _t0, .3)

# ---------------- master ----------------
fade = int(.5 * SR); out[-fade:] *= np.linspace(1, 0, fade)[:, None] ** 2
out = np.tanh(out * 1.1) / 1.1
out *= (10 ** (-1 / 20)) / max(1e-6, np.abs(out).max())
od = 'out/rossen-rules-' + os.path.basename(EP_PATH); os.makedirs(od, exist_ok=True)
with wave.open(od + ('/score_hits.wav' if HO else '/score.wav'), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(out, -1, 1) * 32767).astype('<i2').tobytes())
if not HO:
    with open(od + '/samples_used.txt', 'w') as f: f.write('\n'.join(sorted(USED)) + '\n')
print(od, DUR, 's,', TOTAL_BARS, 'bars,', len(USED), 'samples;', ' | '.join(f"{s['id']} {s['b0']}+{s['bars']}" for s in SEGS))
