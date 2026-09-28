"""Wednesday live-show tease score (wed-tease.js): a 1.875 s intro title card (a 3-beat pickup), 30 s of tease, then the Wednesday 5 PM LIVE TODAY loop (5 s) appended untouched and played twice.
Same tempo and key as the loop (96 BPM, D). Bars 0-8 are composed here, played by recorded instrument samples (VSCO 2 CE and its
VSCO 1 drums, CC0). Sound effects are recorded files (Kenney, BigSoundBank, OpenGameArt; all CC0), each placed by its audible attack.
Bar 8 lands on A on beat 3 and beat 4 is silent; Jeff steps in on bar 9 with a confident D major bar (brass, full groove) that ends on A,
the chord the loop ends on; on bar 10 the loop's own cue enters (its first half under the promise's second bar, its second half under the
handoff bar), so the cut at 30.0 s into the loop is the loop's own seamless wrap.
Mood: sneaky and comic for the oil scam, slick and too good for the fake dealership, tense for the tickets, confident for Jeff.

usage: python3 score_wed_tease.py            ->  out/rossen-tease-wednesday/tease_audio.wav (30 s), full_audio.wav (40 s: the tease + the loop twice), hits.json,
                                                samples_used.txt, audio_sources.txt
       HITS_ONLY=1 python3 score_wed_tease.py ->  score_hits.wav (the synced hits alone)
"""
import numpy as np, subprocess, wave, sys, os, re, glob, math, json
SR = 48000
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audio')
T0 = 3 * 0.625         # the intro title card: a 3-beat pickup before bar 0. Score times are film times (bar 0 = 0 s); the file starts at -T0
DUR = T0 + 12 * 2.5 + 2   # the intro + 30 s, plus room for tails
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
    i0 = int(round((t + T0) * SR))
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
CH['Bm'] = (['D4', 'F#4', 'B3'], ['B1', 'F#2'], ['B2', 'D3'], 'B0')
CROOT = {'Bm': 'B1', 'Dm': 'D2', 'D': 'D2', 'Bb': 'Bb1', 'Gm': 'G2', 'G': 'G2', 'A': 'A1', 'C': 'C2', 'Eb': 'Eb2', 'F': 'F2'}
TONES = {'Bm': ('D5', 'F#5', 'B5'), 'Dm': ('D5', 'F5', 'A5'), 'D': ('D5', 'F#5', 'A5'), 'Bb': ('D5', 'F5', 'Bb5'), 'Gm': ('D5', 'G5', 'Bb5'), 'G': ('D5', 'G5', 'B5'),
         'A': ('C#5', 'E5', 'A5'), 'C': ('C5', 'E5', 'G5'), 'Eb': ('Eb5', 'G5', 'Bb5'), 'F': ('C5', 'F5', 'A5')}
PAD = {'Bm': ('B1', 'D2', 'F#2'), 'Dm': ('D2', 'F2', 'A2'), 'Bb': ('Bb1', 'D2', 'F2'), 'Gm': ('G1', 'D2', 'Bb2'), 'A': ('A1', 'C#2', 'E2'), 'C': ('C2', 'E2', 'G2'),
       'Eb': ('Eb2', 'G2', 'Bb2'), 'D': ('D3', 'F#3', 'A3'), 'G': ('G2', 'B2', 'D3'), 'F': ('F2', 'A2', 'C3')}
HITS = []
def H(t, what): HITS.append((round(t + T0, 4), what))   # hits.json is in video time
B_JEFF, B_HAND = 9, 11
END = AT(12); LOOP_IN = AT(B_JEFF + 1)    # the loop's own cue takes over for the promise's second bar
SIL = (AT(8, 4), AT(B_JEFF))               # the beat of silence before the promise
SMOKE = (AT(2, 4) - .06, AT(3) - .14)      # the picture's transitions (wed-tease.js TR)
ZOOM1, SWING, TOMAIL, ZOOM2, TOLOOP = AT(4) - .36, AT(5) - .52, AT(6) - .34, AT(7) - .36, AT(B_HAND) - .34

def fxp(rel, t, g=1.0, pan=0.0, start=0.0, dur=None, frac=.5, fade=.06):
    """a recorded file (any pack under audio/), optionally one segment of it, placed so its ATTACK (first reach of frac of
    its peak) lands on t"""
    if os.environ.get('PITCHED_ONLY'): return
    x = load(rel); USED.add(rel); i0 = int(start * SR); x = x[i0: i0 + int(dur * SR) if dur else None].copy()
    f = min(len(x), int(fade * SR)); x[len(x) - f:] *= np.linspace(1, 0, f)[:, None]
    env = np.convolve(np.abs(x).max(1), np.ones(48) / 48, 'same'); att = int(np.argmax(env >= frac * env.max()))
    put(x, t - att / SR, g, pan)
BSB, OGA = 'bigsoundbank/joseph-sardin/', 'opengameart/'
KEYS = [(0.64, .16), (1.66, .16), (2.02, .16), (3.04, .16), (5.28, .16), (6.36, .16), (7.70, .14), (8.00, .14)]   # single keystrokes in the slow-keyboard take
def key_(t, k, g=.5): s0, d = KEYS[k % len(KEYS)]; fxp(BSB + 'bsb-1733_slow-keyboard.wav', t, g, .1 * (1 if k % 2 else -1), s0, d, .5, .03)
def whoosh(t_end, g=.35): fxp(BSB + 'bsb-1798_whoosh-10.wav', t_end - .25, g, frac=.9)   # peaks as the move lands
def capsnd(t): xyl('D6', t, .22); fx('casino/card-place-1.ogg', t, .12)

# ---------------- the score (bars 0-8), composed on the 96 BPM grid in D ----------------
# OIL SCAM (0-2): sneaky and comic, D minor: pizzicato bass walking on tiptoe, a staccato clarinet creeping, xylophone winks.
# FAKE DEALER (3-5): slick and too good, bright D major: glockenspiel and xylophone sparkle, a smooth muted-trumpet line, a
#   bouncy groove; the reveal (5) deflates to D minor with a sliding trombone.
# CLONED PLATE (6-8): tense: spiccato sixteenths, timpani, low horns, the snare builds; bar 8 lands on A on beat 3, then stops dead.
ROWS = {0: 'Dm Dm Gm A', 1: 'Dm Dm Gm A', 2: 'Bb Bb A A', 3: 'D D G A', 4: 'D Bm G A', 5: 'Dm Dm Bb A', 6: 'Dm Bb Dm Bb', 7: 'Gm Gm A A', 8: 'Dm Bb A -', 9: 'D D G A'}
if not HO:
    for bar, row in ROWS.items():
        for k, ch in enumerate(row.split()):
            if ch == '-': continue
            bb = BB(bar, k + 1); r = CROOT[ch]; lo = r.replace('2', '1') if r[-1] == '2' else r.replace('1', '0')
            cbp(lo, B(bb), .42, dur=.28)
            if bar < 3:   # tiptoe: bass on the beat, a short cello pluck on the "and"
                cpz(r, B(bb), .55, dur=.2); cpz(TONES[ch][0].replace('5', '3'), B(bb + .5), .38, dur=.14)
            elif bar < 5:   # the slick bounce: octave bass on eighths, xylophone and glock sparkle
                cpz(r, B(bb), .55, dur=.26); cpz(r, B(bb + .5), .45, dur=.2)
                xyl(TONES[ch][k % 3], B(bb), .28, dur=.14); xyl(TONES[ch][(k + 1) % 3], B(bb + .5), .24, dur=.14)
                if k % 2 == 0: [tpl(nn, B(bb), .1, dur=BEAT * 2 - .08, rel=.25) for nn in PAD[ch]]
            elif bar == 9:   # confident: Jeff. Octave bass eighths, horn and trumpet chords, a full groove
                cpz(r, B(bb), .62, dur=.26); cpz(r, B(bb + .5), .5, dur=.2)
                if k % 2 == 0: [hnl(nn, B(bb), .22, dur=BEAT * 2 - .08, rel=.2) for nn in PAD[ch]]
                xyl(TONES[ch][k % 3], B(bb), .22, dur=.14)
            elif bar == 5:   # deflated
                cpz(r, B(bb), .5, dur=.3)
                if k % 2 == 0: [hnl(nn, B(bb), .16, dur=BEAT * 2 - .08, rel=.25) for nn in PAD[ch]]
            else:   # tense: spiccato sixteenths, low horns, the bass doubling
                cpz(r, B(bb), .6, dur=.26); cpz(r, B(bb + .5), .5, dur=.2)
                for j in range(4): vsp(TONES[ch][j % 3], B(bb + j / 4), .22 + .02 * (bar - 6), dur=.09)
                if k % 2 == 0 and not (bar == 8 and k == 2): [hnl(nn, B(bb), .2, dur=BEAT * 2 - .08, rel=.2) for nn in PAD[ch]]
        timp(AT(bar), .42 + .03 * bar)
        if bar < 3:   # a soft tick-tock: rim on 2 and 4, a light kick on 1 and 3
            for q in (2, 4): one(RIM, AT(bar, q), .18, .1)
            kick(AT(bar), .45); kick(AT(bar, 3), .35)
        elif bar < 5: groove(BB(bar), BB(bar + 1), .5, .09)
        elif bar == 5: kick(AT(5), .6); snare(AT(5, 3), .3)
        elif bar == 9: groove(BB(9), BB(10), .62, .12)
        else:
            groove(BB(bar), BB(bar) + (3 if bar == 8 else 4), .5 + .04 * (bar - 6), .06)
    # the sneaky clarinet (bar 1, the sidekick at work) and its answer in bar 0
    for k, (n, d) in enumerate([('D4', 0), ('E4', .5), ('F4', 1), ('E4', 1.5), ('D4', 2), ('C#4', 2.5), ('D4', 3)]): cla(n, B(BB(1) + d), .5, dur=.12)
    for k, (n, d) in enumerate([('A3', 2), ('Bb3', 2.5), ('A3', 3), ('G#3', 3.25), ('A3', 3.5)]): cla(n, B(BB(0) + d), .42, dur=.1)
    # the slick muted-trumpet line over the website (bar 3-4)
    for n, d, l in [('F#4', 0, .5), ('A4', .5, .5), ('D5', 1, 1), ('B4', 2, .5), ('A4', 2.5, .5), ('G4', 3, .5), ('A4', 3.5, .5),
                    ('F#4', 4, .5), ('A4', 4.5, .5), ('B4', 5, 1), ('D5', 6, .5), ('C#5', 6.5, 1.3)]: tpl(n, B(BB(3) + d), .22, dur=l * BEAT - .05, rel=.12)
    # the reveal: a sliding trombone "wah-wah" down into bar 5
    for k, n in enumerate(('A2', 'G#2', 'G2', 'F#2')): tbl(n, AT(5) + k * E8, .5, dur=E8 * (2.4 if k == 3 else .95), rel=.15)
    roll_to(AT(8, 2), AT(8, 3), .3)   # the snare climbs into the stop on 8:3
    stab(AT(8, 3), 'A', .95, dur=.34); kick(AT(8, 3), .9); timp(AT(8, 3), .8); one(CRASH_MF, AT(8, 3), .2)
    # Jeff: a D major hit on 9:1 out of the silence, a rising trumpet call, and the bar ends on A into the loop's D
    hit(AT(9), 'D', 1.0, .4)
    for n, d, l in [('A4', 0, .5), ('D5', .5, .5), ('F#5', 1, 1), ('E5', 2, .5), ('F#5', 2.5, .5), ('A5', 3, 1.0)]: tpl(n, B(BB(9) + d), .3, dur=l * BEAT - .05, rel=.12)
    stab(AT(9, 4), 'A', .7, dur=.3); swell_to(AT(10), .25)

# ---------------- the intro (the pickup, -1.875 to 0) ----------------
# frame 0: the title card is there. A bright D major hit with a glockenspiel sparkle; the little car drives in (a soft tambourine
# shimmer) and parks on beat 3; then a two-note pizzicato pickup under the dissolve into bar 0's tiptoe.
IN0 = -T0
if not HO:
    hit(IN0, 'D', .85, .3)
    for k, n in enumerate(('D6', 'F#6', 'A6', 'D7')): glk(n, IN0 + k * S16, .3)
    for n in PAD['D']: hnl(n, IN0, .2, dur=2 * BEAT - .1, rel=.3)
    tamb(IN0 + E8, IN0 + 2 * BEAT, .1)
    cpz('A2', IN0 + 2 * BEAT, .5, dur=.2); cpz('C#3', IN0 + 2.5 * BEAT, .45, dur=.2)
fx('rpg/bookPlace1.ogg', IN0, .3); H(IN0, 'title card')
fx('impact/footstep_concrete_000.ogg', IN0 + 2 * BEAT, .25); one(RIM, IN0 + 2 * BEAT, .25, .1); H(IN0 + 2 * BEAT, 'car parks')
swell_to(-.02, .16)   # a soft cymbal swell under the dissolve into the driveway

# ---------------- sounds on the picture's beats (recorded; placed by their attack) ----------------
for bar in range(1, 10): capsnd(AT(bar))   # each card lands (both lines together); frame 0 belongs to the car door
# OIL SCAM
fxp(BSB + 'bsb-1526_car-door-4.wav', 0.0, .55, 0, 3.1, .7, .5); kick(0.0, .8); timp(0.0, .6); H(0.0, 'car door')
fx('casino/card-slide-3.ogg', AT(0, 3) - .1, .3); fx('rpg/cloth3.ogg', AT(0, 3), .3); kick(AT(0, 3), .6); one(RIM, AT(0, 3), .3, .1); H(AT(0, 3), 'scammer')
for n in ('D5', 'A5'): xyl(n, AT(0, 3), .3, dur=.15)
fx('interface/pluck_001.ogg', AT(1), .35); cla('A4', AT(1), .35, dur=.1); H(AT(1), 'sidekick')
for k in range(8): fx(('casino/card-fan-1.ogg', 'casino/card-fan-2.ogg')[k % 2], AT(1) + k * E8, .2 if k else .3, -.3)   # the cash fanning
fx('rpg/metalLatch.ogg', AT(1, 2), .55); fxp(BSB + 'bsb-0119_car-hood-closing.wav', AT(1, 2), .35); kick(AT(1, 2), .6); H(AT(1, 2), 'hood')
fxp(BSB + 'bsb-0117_glass-of-soda.wav', AT(1, 3), .6, .2, .75, 1.25, .5); H(AT(1, 3), 'pour')   # a can poured out: the oil
fxp(OGA + 'bart-steam-release-sounds/steam_hiss_marker1.wav', AT(2), .5, -.2, dur=1.2, frac=.4); fxp(BSB + 'bsb-0761_generator-attempts-to-start.wav', AT(2) + .02, .55, -.2, 3.02, 1.1)
kick(AT(2), 1.0); timp(AT(2), .9); one(CRASH_MF, AT(2), .25); H(AT(2), 'smoke')
for k, n in enumerate(('A5', 'F5', 'D5', 'A4')): xyl(n, AT(2, 2) + k * S16 / 2, .35, dur=.12)   # the jaw drop
fx('impact/impactSoft_medium_000.ogg', AT(2, 2), .3); H(AT(2, 2), 'jaw')
fx('impact/impactPunch_heavy_000.ogg', AT(2, 3), .45); fx('rpg/bookPlace1.ogg', AT(2, 3), .35); kick(AT(2, 3), .85); cbp('A0', AT(2, 3), .9); H(AT(2, 3), 'price')
fxp(BSB + 'bsb-1486_air-leak.wav', SMOKE[0], .35, 0, 1.0, .75, .3, .25); whoosh(SMOKE[1], .4)   # the smoke billows and clears
# FAKE DEALER: the site builds itself to the keystrokes
for k in range(16): key_(AT(3) + k * E8, k, .42 if k % 2 == 0 else .3)
for b, n in ((1, 'D6'), (2, 'F#6'), (4, 'A6')): glk(n, AT(3, b), .3); H(AT(3, b), 'site')
for k in range(5): glk(('D6', 'E6', 'F#6', 'A6', 'D7')[k], AT(3, 3) + k * S16 / 2, .28)
one(RIM, AT(3, 3), .32, .1); kick(AT(3, 3), .5); H(AT(3, 3), 'stars')
whoosh(AT(4) - .14, .3)
fx('interface/click_002.ogg', AT(4), .5); kick(AT(4), .7); H(AT(4), 'tap')
fx('interface/confirmation_001.ogg', AT(4, 2), .4); glk('A6', AT(4, 2), .25); H(AT(4, 2), 'paid')
fxp(BSB + 'bsb-3240_torn-paper-3.wav', AT(4, 3), .4); one(RIM, AT(4, 3), .3, .1); H(AT(4, 3), 'curl')
fx('rpg/creak1.ogg', SWING + .05, .45); whoosh(AT(5) - .14, .35); fx('impact/impactPlank_medium_000.ogg', AT(5) - .14, .3)   # the flat swings away
fx('interface/pluck_002.ogg', AT(5), .35); H(AT(5), 'scammer out')
for b in (2, 3, 4): fx('casino/card-fan-1.ogg', AT(5, b), .2)
fx('rpg/cloth1.ogg', AT(5, 3) - .3, .3); fx('rpg/cloth2.ogg', AT(5, 3) + .15, .25)   # the tumbleweed
# CLONED PLATE
fx('casino/card-slide-2.ogg', TOMAIL + .1, .3)
fxp(BSB + 'bsb-1527_metal-mailbox-1.wav', AT(6), .6, .1, .35, 1.0); fx('casino/cards-pack-open-1.ogg', AT(6) + .02, .4); kick(AT(6), .9); H(AT(6), 'mailbox')
for k in range(7): fx(('casino/card-place-2.ogg', 'casino/card-place-3.ogg')[k % 2], AT(6) + k * E8, .28, .2)
for b in (2, 3, 4): fx('casino/chips-stack-1.ogg', AT(6, b), .3, .25); H(AT(6, b), 'total')   # the total counts on 2, 3, 4
whoosh(AT(7) - .14, .3)
fxp(BSB + 'bsb-3022_old-camera-trigger.wav', AT(7), .6, 0, .3, 1.3); kick(AT(7), .8); one(CRASH_MF, AT(7), .2); H(AT(7), 'flash')
fx('interface/scratch_004.ogg', AT(7, 3), .2); one(RIM, AT(7, 3), .3, .1); H(AT(7, 3), 'marker')
fxp(BSB + 'bsb-0298_adhesive-tape-2.wav', AT(8), .45, 0, .1, .9, .3); one(RIM, AT(8), .32, .1); kick(AT(8), .55); H(AT(8), 'peel')
fx('casino/card-slide-1.ogg', AT(8, 2) + .1, .25); fx('rpg/bookPlace2.ogg', AT(8, 3), .35); H(AT(8, 3), 'plate lands')
# THE PROMISE: Jeff lands on 9:1 (the composed hit); the lens settles on the can 9:3, the site 10:1, the plate 10:3 (the loop's cue from bar 10)
fx('impact/impactSoft_heavy_000.ogg', AT(B_JEFF), .35); H(AT(B_JEFF), 'jeff')
for k, t in enumerate((AT(9, 3), AT(10), AT(10, 3))): fx('interface/glass_001.ogg', t, .25); one(RIM, t, .42, .1); glk(('A5', 'D6', 'F#6')[k], t, .3); H(t, 'lens')
fx('casino/card-slide-3.ogg', TOLOOP + .1, .26)
for b in (1, 2, 3, 4): fx('rpg/bookPlace1.ogg', AT(B_HAND, b), .3 if b < 4 else .22); one(RIM, AT(B_HAND, b), .4, .1); H(AT(B_HAND, b), 'piece')

# ---------------- mix: composed bars + the loop's own cue ----------------
S_ = lambda t: int(round((t + T0) * SR))   # film time -> sample index in the file
n_end, n_in = S_(END), S_(LOOP_IN)
comp = out[:n_end].copy()
LOOP_MP4 = '../final-videos/09 Live Today Loop - Wednesday 5 PM (9x16).mp4'   # the delivered loop's own audio, decoded (read-only)
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', LOOP_MP4, '-vn', '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
LOOP = np.frombuffer(raw, np.float32).reshape(-1, 2).copy(); assert abs(len(LOOP) - 5 * SR) < 1100, len(LOOP)
LOOP = np.pad(LOOP, ((0, max(0, 5 * SR - len(LOOP))), (0, 0)))[: 5 * SR]
rms = lambda x: float(np.sqrt((x ** 2).mean() + 1e-12))
if not HO:
    target = rms(LOOP[: int(2.5 * SR)]); cur = rms(comp[S_(AT(6)): S_(SIL[0])])
    comp *= target / cur * 10 ** (-1.0 / 20)
    lim = 10 ** (-4.0 / 20); comp = np.tanh(comp / lim) * lim
    gate = np.ones(n_end, np.float32); a0, a1 = S_(SIL[0]), S_(SIL[1]); f = int(.04 * SR)
    gate[a0 - f: a0] = np.linspace(1, 0, f); gate[a0: a1] = 0          # the silence: everything stops on 8:4
    gate[n_in:] = .6                                                   # under the loop's cue, only the picture's foley
    t0, t1 = S_(END - .45), S_(END - .1); gate[t0:t1] *= np.linspace(1, 0, t1 - t0) ** 2; gate[t1:] = 0   # silent before the join: it is the loop's own wrap
    comp *= gate[:, None]
    comp[n_in:n_end] += LOOP[: n_end - n_in]
    print('levels: bars 6-8 %.1f dBFS rms, bar 9 %.1f, loop %.1f dBFS rms, peak %.2f' % (20 * np.log10(rms(comp[S_(AT(6)):a0])), 20 * np.log10(rms(comp[a1:n_in])), 20 * np.log10(target), np.abs(comp).max()))
od = 'out/rossen-tease-wednesday'; os.makedirs(od, exist_ok=True)
def write(p, x):
    with wave.open(p, 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1) * 32767).astype('<i2').tobytes())
if HO: write(od + '/score_hits.wav', comp / max(1e-6, np.abs(comp).max()) * .9)
else:
    write(od + '/tease_audio.wav', comp)
    write(od + '/full_audio.wav', np.concatenate([comp, LOOP, LOOP]))   # the loop's own audio, sample for sample, twice: its end wraps into its start
json.dump(sorted(set(HITS)), open(od + '/hits.json', 'w'))
if not HO:
    with open(od + '/samples_used.txt', 'w') as f: f.write('\n'.join(sorted(USED)) + '\n')
    PACK = {'interface': 'https://kenney.nl/assets/interface-sounds', 'impact': 'https://kenney.nl/assets/impact-sounds', 'rpg': 'https://kenney.nl/assets/rpg-audio',
            'casino': 'https://kenney.nl/assets/casino-audio', 'digital': 'https://kenney.nl/assets/digital-audio'}
    BSB_ID = lambda u: re.search(r'bsb-(\d{4})', u).group(1)
    OGA_PAGE = {'spring-spring-various-sound-effects': 'https://opengameart.org/content/various-sound-effects-0  (spring-spring)',
                'bart-steam-release-sounds': 'https://opengameart.org/content/steam-release-sounds  (bart)'}
    notes = open('audio/wedtease_sources.txt').read()
    def page_of(u):
        if u.startswith('kenney/'): return PACK[u.split('/')[1]] + '  (Kenney, kenney.nl)', 'CC0 1.0'
        if u.startswith('vsco/'): return 'https://github.com/sgossner/VSCO-2-CE  (Versilian Studios Chamber Orchestra 2 Community Edition' + (', VSCO 1 drums folder' if 'VSCO 1' in u else '') + ')', 'CC0 1.0'
        row = next((l.split(' | ') for l in notes.splitlines() if l.startswith(u + ' |')), None)   # audio/wedtease_sources.txt: path | sound | page | file | author | license | length
        if u.startswith(BSB): return f'{row[2]}  (Joseph Sardin, BigSoundBank; file {row[3]})', 'CC0 1.0 (the page: "License CC0 (public domain): Free and royalty-free")'
        if u.startswith(OGA): return f'{row[2]}  ({row[4]}, OpenGameArt; file {row[3]})', 'CC0 1.0 (the page: "License(s): CC0")'
        return '?', '?'
    loop_used = [l.strip() for l in open('out/rossen-loop/samples_used.txt') if l.strip()]
    with open(od + '/audio_sources.txt', 'w') as f:
        f.write('Rossen Reports Wednesday live tease (1.9 s intro title card + 30 s, car scams) + the Wednesday 5 PM LIVE TODAY loop played twice (10 s). Every recorded audio file in the mix, with its source and license.\n')
        f.write('All are CC0 1.0 (public domain dedication, commercial use allowed, no attribution required). None come from a music library that registers with Content ID.\n\n')
        for u in sorted(USED | set(loop_used)):
            src, lic = page_of(u); who = ('tease' if u in USED else '') + (' + ' if u in USED and u in loop_used else '') + ('loop cue' if u in loop_used else '')
            f.write(f'{u}\n    used in: {who}\n    source: {src}\n    license: {lic}\n')
        f.write('\nComposed (not recorded files): the whole score. Bars 0-8 are written note by note in score_wed_tease.py on the 96 BPM grid in D '
                '(the loop\'s tempo and key) and played by the VSCO recordings above: the tiptoe pizzicato and creeping clarinet of the oil scam, the xylophone jaw drop, '
                'the slick muted trumpet, glockenspiel and xylophone of the fake dealership, the sliding trombone of the reveal, the spiccato and horns of the tickets, '
                'the intro title card\'s D major hit and pizzicato pickup, the stop on A and the beat of silence, Jeff\'s D major hit and trumpet call (bar 9). Bars 10-11 and the appended loop are the LIVE TODAY loop cue (composed in score_loop.py), taken from the delivered loop file itself. '
                'No synthesized tones are used anywhere, and no sound effect is composed: every effect is a recorded file listed above.\n')
print(od, len(set(HITS)), 'hits,', len(USED), 'samples')
