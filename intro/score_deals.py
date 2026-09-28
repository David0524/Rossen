"""Score for the "STILL LIVE" weekend deals roundup (deals.js). Its length and every hit come from deals/deals.json, with the
same timing formulas as the picture. Composed in code on the 96 BPM grid and played by recorded instrument samples (VSCO 2 CE
and its VSCO 1 drums, CC0); the foley is recorded Kenney samples (CC0). A bright, warm G-major shopping groove (pizzicato bass,
offbeat strings, xylophone and glockenspiel, horn pads, brushes-free drum kit), dropping to a held pad and a soft clock for the
fine print, then back for the credit and the CTA, the stamp and the closing card.

usage: python3 score_deals.py             ->  out/rossen-deals-still-live/score.wav, hits.json, samples_used.txt, audio_sources.txt
       HITS_ONLY=1 python3 score_deals.py  ->  score_hits.wav (the synced hits alone)
"""
import numpy as np, subprocess, wave, sys, os, re, glob, math, json
SR = 48000
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audio')
DJ = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'deals', 'deals.json')))
N, DB = len(DJ['deals']), 3   # deals, bars per deal (as in deals.js)
DUR = (1 + DB * N + 4) * 2.5 + 4.5   # open, the deals, note, disclosure, credit, CTA; then the closing card
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

CH['Em'] = (['E4', 'G4', 'B3'], ['E2', 'B2'], ['E3', 'G2'], 'E1')
CROOT['Em'] = 'E2'; TONES['Em'] = ('E5', 'G5', 'B5'); PAD['Em'] = ('E2', 'G2', 'B2')
def capsnd(t): xyl('D6', t, .2); fx('casino/card-place-1.ogg', t, .12)
def stamp_hit(t, g=1.0, ch='G'): kick(t, .85 * g); timp(t, .8 * g); cbp(CH[ch][3], t, .9 * g); fx('impact/impactPunch_heavy_000.ogg', t, .45 * g); H(t, 'stamp')
def push(t): fx('casino/card-slide-3.ogg', t - .15, .26)
def fxa(name, t, g=1.0, pan=0.0):   # samples that swell in: align their first audible attack
    x = load(K + name); e = np.convolve(np.abs(x).max(1), np.ones(96) / 96, 'same'); att = int(np.argmax(e >= .15 * e.max()))
    USED.add(K + name); put(x, t - att / SR, g, pan)

# ---------------- the timeline (the same formulas as deals.js) ----------------
A_ = lambda k: AT(1 + DB * k); P_ = lambda k: A_(k) + 2.5; D_ = lambda k: A_(k) + 5.0
T_NOTE = AT(1 + DB * N); T_DISC = T_NOTE + 2.5; T_CRED = T_DISC + 2.5; T_CTA = T_CRED + 2.5; STAMP = T_CTA + 2.5
FLIP_TO = 2 if N >= 4 else -1; BOX_TO = N - 1 if N >= 3 else -1
def pin(t, g=1.0): fx('casino/card-place-3.ogg', t, .45 * g); fx('rpg/metalClick.ogg', t, .28 * g); kick(t, .55 * g); H(t, 'photo pinned')
def kaching(t):   # the cash register, built from recorded parts: the drawer latch on the hit, then the bell and the coins a 16th later
    fx('rpg/metalLatch.ogg', t, .32); fx('impact/impactTin_medium_000.ogg', t, .18)
    one(TRI, t + S16, .55, .15); glk('B6', t + S16, .42); glk('G6', t + S16, .3); fx('casino/chips-collide-1.ogg', t + S16, .3, .2); fx('casino/chips-collide-3.ogg', t + S16 * 2, .22, -.2)

# ---------------- the music: bright G major, a bouncy weekend-shopping groove ----------------
ROWS = {0: 'G G C D'}
for k in range(N): ROWS[1 + DB * k] = 'G G Em Em'; ROWS[2 + DB * k] = 'C C D D'; ROWS[3 + DB * k] = 'G G C D'
b0 = 1 + DB * N; ROWS[b0] = 'C C G G'; ROWS[b0 + 1] = 'Em Em D D'; ROWS[b0 + 2] = 'C C D D'; ROWS[b0 + 3] = 'G G C D'
def act(bar): return 'open' if bar == 0 else 'deal' if bar < b0 else 'fine' if bar < b0 + 2 else 'close'
MEL = {'G': ('D5', 'G5', 'B5', 'G5'), 'Em': ('E5', 'G5', 'B5', 'G5'), 'C': ('E5', 'G5', 'C6', 'G5'), 'D': ('F#5', 'A5', 'D6', 'A5')}
if not HO:
    for bar, row in ROWS.items():
        a = act(bar)
        for k, ch in enumerate(row.split()):
            t = AT(bar, k + 1)
            if t >= STAMP - BEAT: continue
            r = CROOT[ch]; lo = r.replace('2', '1') if r[-1] == '2' else r.replace('1', '0')
            if a in ('open', 'deal', 'close'):
                cbp(lo, t, .42, dur=.3); cpz(r, t, .62, dur=.26); cpz(TONES[ch][1].replace('5', '3'), t + E8, .48, dur=.22)   # a bouncing bass
                vla(TONES[ch][0].replace('5', '4'), t + E8, .3, dur=.16); vla(TONES[ch][1].replace('5', '4'), t + E8 + S16, .22, dur=.12)   # offbeat strings
                if k % 2 == 0: [hnl(n, t, .2, dur=BEAT * 2 - .1, rel=.3) for n in PAD[ch]]
                if a == 'deal' and (bar - 1) % DB == 0:   # the xylophone hook, answering each new product
                    for j in range(2): xyl(MEL[ch][(2 * k + j) % 4], t + j * E8, .2, dur=.14)
            else:   # the fine print: the groove drops out, a held pad and a soft clock
                if k in (0, 2): cpz(r, t, .5, dur=.4); cbp(lo, t, .35, dur=.5)
                if k == 0: [hnl(n, t, .24, dur=BEAT * 4 - .1, rel=.3) for n in PAD[ch]]
                if k: fx('interface/tick_001.ogg', t, .16)
        if a in ('open', 'deal'): groove(BB(bar), BB(bar + 1), .5, .1)
        if a == 'close': groove(BB(bar), min(BB(bar + 1), STAMP / BEAT - 1), .56, .12)
    roll_to(STAMP - BEAT, STAMP, .4, TIMP_ROLL); tomfill(STAMP - BEAT * .75, STAMP, .4, S16 / 2)

# ---------------- sounds on the picture's beats ----------------
# OPEN: the title is there in frame 0; the first photo is pinned on beat 3
kick(0.0, .55); one(CLAVE, 0.0, .4); fx('casino/card-place-2.ogg', 0.0, .3); glk('G6', 0.0, .35); one(CRASH_MF, 0.0, .2); H(0.0, 'open')
pin(AT(0, 3))
for k in range(N):
    A, P, D = A_(k), P_(k), D_(k)
    if k == FLIP_TO:   # [signature 1] the board pulls back on its string, flips over, lands on the downbeat
        fx('casino/card-fan-1.ogg', A - .35, .3); fx('rpg/bookFlip2.ogg', A - .1, .42); fx('rpg/cloth2.ogg', A - .1, .2)
        fx('casino/card-place-2.ogg', A, .45); kick(A, .75); one(CRASH_MF, A, .2); H(A, 'flip lands')
    elif k == BOX_TO:   # [signature 2] the box drops in, lands on the "and" of 4, pops open, and we dive in
        tl = A - E8
        fx('casino/card-slide-1.ogg', A - .5, .28); fx('impact/impactSoft_heavy_000.ogg', tl, .5); fx('impact/impactWood_heavy_000.ogg', tl, .3); kick(tl, .7); H(tl, 'box lands')
        fxa('casino/cards-pack-open-1.ogg', tl + .03, .45); swell_to(A, .28)
        kick(A, .8); one(CRASH_MF, A, .25); fx('casino/card-place-3.ogg', A, .35); H(A, 'dive')
    else:
        if k: push(A)
        if k: pin(A)
    capsnd(A)
    fx('casino/card-place-1.ogg', P, .4); xyl('D6', P, .3); kick(P, .5); H(P, 'regular price')                     # the regular price
    stamp_hit(D, .9, 'G'); kaching(D); stab(D, 'G', .75, dur=.28, bass=False); H(D, 'DEAL stamp')                 # the stamp and the deal price
    fx('interface/pluck_002.ogg', D + BEAT, .35); kick(D + BEAT, .45); H(D + BEAT, 'sticker')                       # the percent-off sticker
    for j, n in enumerate(('G6', 'B6', 'D7')): glk(n, D + BEAT + j * S16, .22)
# the fine print: each note is pinned up on its downbeat (a cut)
for t, what, snd in ((T_NOTE, 'price note', 'rpg/bookPlace1.ogg'), (T_DISC, 'disclosure', 'rpg/bookPlace2.ogg')):
    fx(snd, t, .45); fx('rpg/metalClick.ogg', t, .25); kick(t, .6); one(CRASH_MF, t, .12); H(t, what)
# CREDIT and CTA: the credit lands, Jeff pops up on beat 2; the CTA lands on the next bar; his thumbs up on beat 2
capsnd(T_CRED); fx('casino/card-place-2.ogg', T_CRED, .45); kick(T_CRED, .7); one(CRASH_MF, T_CRED, .22); H(T_CRED, 'credit')
fx('interface/pluck_002.ogg', T_CRED + BEAT, .35); kick(T_CRED + BEAT, .5); H(T_CRED + BEAT, 'Jeff pops up')
kick(T_CTA, .8); stab(T_CTA, 'G', .8, dur=.3); fx('casino/card-place-2.ogg', T_CTA, .4); H(T_CTA, 'CTA')
fx('interface/confirmation_001.ogg', T_CTA + BEAT, .38); kick(T_CTA + BEAT, .5); H(T_CTA + BEAT, 'thumbs up')
# END: the rubber stamp, the final chord, a soft held chord under the closing card
if not HO:
    for n in ('G1', 'B1', 'D2'): hnl(n, STAMP, .85, dur=1.4, rel=.4)
    for n in ('G2', 'D2'): tbl(n, STAMP, .8, dur=1.4, rel=.4)
cbp('G0', STAMP, 1.0); cpz('G2', STAMP, .9); timp(STAMP, .9); kick(STAMP, 1.0); one(CRASH, STAMP, .45); glk('G6', STAMP, .45); H(STAMP, 'rubber stamp')
fx('impact/impactPlank_medium_000.ogg', STAMP, .55); fx('impact/impactSoft_heavy_000.ogg', STAMP, .4)
_t0 = STAMP + 1.2
if not HO:
    for n in ('G1', 'B1', 'D2'): hnl(n, _t0, .28, dur=DUR - _t0 - .4, rel=1.0)
    cpz('G2', _t0, .3)

# ---------------- master ----------------
fade = int(.8 * SR); out[-fade:] *= np.linspace(1, 0, fade)[:, None] ** 2
out = np.tanh(out * 1.1) / 1.1
out *= (10 ** (-1 / 20)) / max(1e-6, np.abs(out).max())
od = 'out/rossen-deals-still-live'; os.makedirs(od, exist_ok=True)
with wave.open(od + ('/score_hits.wav' if HO else '/score.wav'), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(out, -1, 1) * 32767).astype('<i2').tobytes())
json.dump(sorted(set(HITS)), open(od + '/hits.json', 'w'))
if not HO:
    with open(od + '/samples_used.txt', 'w') as f: f.write('\n'.join(sorted(USED)) + '\n')
    PACK = {'interface': 'https://kenney.nl/assets/interface-sounds', 'impact': 'https://kenney.nl/assets/impact-sounds', 'rpg': 'https://kenney.nl/assets/rpg-audio',
            'casino': 'https://kenney.nl/assets/casino-audio', 'digital': 'https://kenney.nl/assets/digital-audio'}
    with open(od + '/audio_sources.txt', 'w') as f:
        f.write('Rossen Reports: "STILL LIVE" weekend deals roundup (both platform versions share this soundtrack). Every recorded audio file in the mix, with its source and license.\n')
        f.write('All are CC0 1.0 (public domain dedication, commercial use allowed, no attribution required). None come from a library that registers with Content ID.\n\n')
        for u in sorted(USED):
            if u.startswith('kenney/'): src = PACK[u.split('/')[1]] + '  (Kenney, kenney.nl)'
            else: src = 'https://github.com/sgossner/VSCO-2-CE  (Versilian Studios Chamber Orchestra 2 Community Edition' + (', VSCO 1 drums folder' if 'VSCO 1' in u else '') + ')'
            f.write(f'{u}\n    source: {src}\n    license: CC0 1.0\n')
        f.write('\nComposed (not recorded files): the whole score, written note by note in score_deals.py on the 96 BPM grid and played by the VSCO '
                'instrument recordings above: the bouncing pizzicato bass and offbeat strings, the xylophone hook on each new product, the warm horn '
                'pads, the drum groove, the soft clock under the fine print, the glockenspiel run on each percent-off sticker, and the final G-major chord. '
                'The cash-register "ka-ching" is also composed: it is not a recording of a register, but is built from recorded CC0 parts, a '
                'Kenney metal latch and tin tap for the drawer, then a VSCO triangle, two glockenspiel notes and Kenney coin sounds a 16th note later. '
                'Every other effect (paper, pins, stamps, the price tags, the box, the flip) is a recorded Kenney file. No synthesized tones are used.\n')
print(od, DUR, 's,', len(USED), 'samples,', len(set(HITS)), 'synced hits')
