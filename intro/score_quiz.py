"""Soundtrack for the Rossen Reports "SCAM OR LEGIT?" quiz (rossen-scam-or-legit.html). Recorded samples only, no synthesis.

Music: an original 59 s cue sequenced from VSCO 2 Community Edition / VSCO 1 orchestral and drum samples (CC0), on the
same 96 BPM grid and instruments as the case-file videos. Foley: Kenney CC0 packs (Interface, Impact, RPG, Casino, and
two stings from Digital Audio for the right/wrong answer), placed by attack on the frame where its picture lands.
Each round: a fanfare on SHOW, a ticking clock under the 2-bar countdown, a buzzer or a chime on the reveal, one
marker swipe per flag, then the takeaway.

usage: python3 score_quiz.py [samples_dir]  ->  out/rossen-scam-or-legit/score.wav
"""
import numpy as np, subprocess, wave, sys, os, re, glob, math
SR = 48000; DUR = 61.5   # 23 bars, then the closing card
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


def fx_first(name, t, g=1.0, pan=0.0):   # foley that swells in (the marker squeak): align its FIRST audible attack
    x = load(K + name); e = np.convolve(np.abs(x).max(1), np.ones(96) / 96, 'same'); att = int(np.argmax(e >= .2 * e.max()))
    USED.add(K + name); put(x, t - att / SR, g, pan)
HO = bool(os.environ.get('HITS_ONLY'))   # verification stem: only the hits, no groove, rolls, fills or clock
if HO:
    groove = roll_to = tomfill = swell_to = lambda *a, **k: None
CH['Gm'] = (['D4', 'G4', 'Bb3'], ['G1', 'D2'], ['G2', 'Bb2'], 'G1')
CROOT = {'Dm': 'D2', 'D': 'D2', 'Bb': 'Bb1', 'Gm': 'G2', 'G': 'G2', 'A': 'A1', 'Bm': 'B1', 'Em': 'E2'}
VOX = {'Dm': ('D3', 'F3', 'A3'), 'D': ('D3', 'F#3', 'A3'), 'Bb': ('D3', 'F3', 'Bb3'), 'Gm': ('D3', 'G3', 'Bb3'), 'G': ('D3', 'G3', 'B3'),
       'A': ('C#3', 'E3', 'A3'), 'Bm': ('D3', 'F#3', 'B3'), 'Em': ('E3', 'G3', 'B3')}
ROUNDS = [(0, True, 3), (7, False, 3), (14, True, 2)]    # first bar, scam?, number of flags; 7 bars a round
END_B = 21; END = AT(23)                                 # the end card, and the rubber stamp landing on the official logo
chords = {}
for b, scam, n in ROUNDS:
    chords[b] = 'D D G A'; chords[b + 1] = 'Bm Bm G G'; chords[b + 2] = 'Em Em A A'
    chords[b + 3] = 'Dm Dm Bb A' if scam else 'D D G D'; chords[b + 4] = 'Bb Bb A A' if scam else 'G G A A'
    chords[b + 5] = 'G G A A'; chords[b + 6] = 'Bm Bm A A'
chords[END_B] = 'D D G A'; chords[END_B + 1] = 'D D A A'
QUIET = {b + k for b, _, _ in ROUNDS for k in (1, 2)}   # the groove steps back while the viewer thinks
for bar in range(END_B + 2 if not HO else 0):
    groove(BB(bar), BB(bar + 1), .5 if bar in QUIET else .7, .12)
for bar, row in (chords.items() if not HO else []):
    for k, ch in enumerate(row.split()):
        bb = BB(bar, k + 1)
        if B(bb) >= END: break
        r = CROOT[ch]; lo, mid, hi = VOX[ch]
        cpz(r, B(bb), .7, dur=.28); cpz(r, B(bb + .5), .6, dur=.28); cbp(r.replace('2', '1') if r[-1] == '2' else r.replace('1', '0'), B(bb), .38, dur=.3)
        vla(lo if k % 2 == 0 else mid, B(bb), .36, dur=.2); vla(hi, B(bb + .5), .32, dur=.2)
def capsnd(t, notes=('D5', 'A5')): xyl(notes[0], t, .45); fx('casino/card-place-1.ogg', t, .15); xyl(notes[1], t + E8, .4); fx('casino/card-place-2.ogg', t + E8, .13)

for ri, (b, scam, n) in enumerate(ROUNDS):
    # SHOW: round 1 is already on screen on frame 1; later rounds slide in over beat 1 and land on beat 2
    if ri == 0: hit(0.0, 'D', .9, .45); fx('interface/glass_001.ogg', 0.0, .5)
    else: fx('casino/card-slide-3.ogg', AT(b) + .05, .35); hit(AT(b, 2), 'D', .85, .4); fx('rpg/bookPlace1.ogg', AT(b, 2), .35); capsnd(AT(b, 2))
    for bb, nt, d in [(2.5, 'D4', .15), (3, 'F#4', .15), (3.5, 'A4', .15), (4, 'D5', .4)]: tps(nt, AT(b, bb), .75, dur=d)
    if ri == 0: fx('interface/pluck_001.ogg', AT(0, 2), .3)                                           # Jeff pops up
    # PAUSE: two bars of clock, the last three beats climb, LOCK IT IN! on the last
    for k in range(8 if not HO else 0):
        tt = AT(b + 1) + k * BEAT; fx('interface/tick_002.ogg', tt, .5); one(CLAVE, tt, .22); fx('interface/tick_001.ogg', tt + E8, .28)
        if 5 <= k < 7: xyl(('A5', 'B5')[k - 5], tt, .55); glk(('A5', 'B5')[k - 5], tt, .3)
    roll_to(AT(b + 2, 3), AT(b + 2, 4), .4)
    tl = AT(b + 2, 4); fx('rpg/metalLatch.ogg', tl, .55); stab(tl, 'A', .75); timp(tl, .6); roll_to(tl + .05, AT(b + 3), .3)   # LOCK IT IN!
    fx('casino/card-place-1.ogg', AT(b + 3) + .1, .3); glk('A6', AT(b + 3) + .1, .3)                                  # the scorecard flips
    # REVEAL: the verdict on beat 1, then one highlighter swipe every two beats
    t0 = AT(b + 3)
    if scam: hit(t0, 'Dm', 1.0, .3); fx('impact/impactPunch_heavy_001.ogg', t0, .55); fx('interface/error_004.ogg', t0, .35); fx('digital/lowThreeTone.ogg', t0, .22)
    else: hit(t0, 'D', 1.0, .3); fx('interface/confirmation_002.ogg', t0, .45); fx('digital/threeTone1.ogg', t0, .22); [glk(nt, t0 + k * S16, .45) for k, nt in enumerate(('D6', 'F#6', 'A6'))]
    if scam: fx('interface/switch_007.ogg', t0, .35); [cla(nt, t0 + .05 + k * S16 / 2, .45, dur=.08) for k, nt in enumerate(('A4', 'Bb4', 'A4', 'Bb4'))]   # caught in the spotlight
    for i in range(n):
        tt = t0 + (i + 1) * 2 * BEAT   # the same beats as markT() in quiz.js
        fx('interface/scratch_004.ogg', tt, .4, (-.2, .2)[i % 2]); fx('casino/card-place-2.ogg', tt, .25); kick(tt, .75); one(RIM, tt, .5, .1)   # each flag lands hard
        xyl(('F5', 'A5', 'D6')[i] if scam else ('F#5', 'A5', 'D6')[i], tt, .5)
    # TAKEAWAY (2 bars): the lines land; in scam rounds the vaudeville hook yanks him off
    t1 = AT(b + 5); stab(t1, 'G', .7); capsnd(t1, ('D5', 'G5')); kick(t1, .8); fx('impact/impactSoft_medium_000.ogg', t1, .4)   # every takeaway lands the same way
    if scam: fx('rpg/cloth3.ogg', t1 - .1, .4); [cla(nt, t1 + .05 + k * S16 / 2, .5, dur=.1) for k, nt in enumerate(('D5', 'A4', 'F4', 'D4'))]
    for bb, nt, d in [(1, 'A4', .28), (1.5, 'F#4', .15), (2, 'G4', .28), (3, 'A4', .55)]: tps(nt, AT(b + 6, bb), .6, dur=d)   # the second takeaway bar breathes
    swell_to(AT(b + 7), .3)                                                                           # into the next round
# END: the last phone slides out on beat 1, then HOW MANY DID YOU GET RIGHT? ... 0, 1, 2 OR 3?
E = END_B
fx('casino/card-slide-3.ogg', AT(E) + .05, .35)
hit(AT(E, 2), 'D', 1.0, .6); fx('impact/impactPunch_heavy_000.ogg', AT(E, 2), .5)
hit(AT(E, 2.5), 'D', .8, .3); fx('impact/impactPunch_heavy_001.ogg', AT(E, 2.5), .4)
hit(AT(E, 3), 'G', .9, .4); fx('impact/impactPunch_heavy_002.ogg', AT(E, 3), .45)
for i, nt in enumerate(('D5', 'A5', 'D6')): fx('casino/card-place-2.ogg', AT(E, 3) + i * S16, .3); xyl(nt, AT(E, 3) + i * S16, .45)   # the answers recap
hit(AT(E, 3.5), 'A', .9, .4); fx('impact/impactPunch_heavy_000.ogg', AT(E, 3.5), .45)
for bb, nt, d in [(1, 'D4', .15), (1.5, 'D4', .28), (2, 'F#4', .28), (3, 'A4', .5), (3.5, 'D5', .3)]: tps(nt, AT(E + 1, bb), .8, dur=d)
roll_to(AT(E + 1, 3), END, .45, TIMP_ROLL); tomfill(AT(E + 1, 3.5), END, .45, S16)                   # the rubber stamp comes down
t = END
for nt in ('D4', 'F#4', 'A4'): tpl(nt, t, .95, dur=1.2, rel=.3)
for nt in ('D2', 'F#2', 'A2'): hnl(nt, t, .9, dur=1.2, rel=.3)
for nt in ('D2', 'A1'): tbl(nt, t, .85, dur=1.2, rel=.3)
cbp('D1', t, 1.0); cpz('D2', t, .9); timp(t, 1.0); kick(t, 1.0); one(CRASH, t, .6); glk('D6', t, .55)
fx('impact/impactPlank_medium_000.ogg', t, .55); fx('impact/impactSoft_heavy_000.ogg', t, .4)

# ---------------- under the closing card: a soft held D major, so the longer card never sits in silence ----------------
_t0 = END + 1.2
if not HO:
    for n in ('D2', 'F#2', 'A2'): hnl(n, _t0, .3, dur=DUR - _t0 - .4, rel=1.0)
    cpz('D2', _t0, .3)

# ---------------- master ----------------
fade = int(.5 * SR); out[-fade:] *= np.linspace(1, 0, fade)[:, None] ** 2
out = np.tanh(out * 1.1) / 1.1
out *= (10 ** (-1 / 20)) / max(1e-6, np.abs(out).max())
od = 'out/rossen-scam-or-legit'; os.makedirs(od, exist_ok=True)
with wave.open(od + ('/score_hits.wav' if HO else '/score.wav'), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(out, -1, 1) * 32767).astype('<i2').tobytes())
if not HO:
  with open(od + '/samples_used.txt', 'w') as f: f.write('\n'.join(sorted(USED)) + '\n')
print(od + '/score.wav', DUR, 's,', len(USED), 'samples')
