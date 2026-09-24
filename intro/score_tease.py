"""Friday live-show tease score (friday-tease.js), 25 s, then the approved LIVE TODAY loop (rossen-loop-friday) follows.
Same tempo and key as the loop (96 BPM, D): bars 0-7 are composed here, played by recorded instrument samples (VSCO 2 CE
and its VSCO 1 drums, CC0); physical sound effects are recorded Kenney samples (CC0). Bars 8-9 carry the loop's own cue
(out/rossen-loop/loop_norm.wav, composed in score_loop.py), so the tease hands off with no bump: bar 7 ends on A, the chord
the loop ends on and whose tails ring into its first samples, and the cut at 25.0 s is the loop's own seamless wrap.
Mood: tense D minor through the scams (low strings, pizzicato, a ticking pulse, low brass), building layer by layer
through port hacking, lifting toward major when Jeff and the hacker come in, then the loop's bright D major on the deals.

usage: python3 score_tease.py            ->  out/rossen-tease-friday/tease_audio.wav (25 s), full_audio.wav (35 s: tease + the loop twice), hits.json,
                                            samples_used.txt, audio_sources.txt
       HITS_ONLY=1 python3 score_tease.py ->  score_hits.wav (the synced hits alone)
"""
import numpy as np, subprocess, wave, sys, os, re, glob, math, json
SR = 48000
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audio')
DUR = 10 * 2.5 + 2   # 25 s plus room for tails (cut at 25 s)
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
HITS = []
def H(t, what): HITS.append((round(t, 4), what))
END = AT(10); LOOP_IN = AT(8)   # the loop's cue takes over at bar 8

# ---------------- bars 0-7, composed ----------------
ROWS = {0: 'Dm Dm Bb A', 1: 'Dm Dm Bb A', 2: 'Gm Gm A A', 3: 'Dm Dm Bb C', 4: 'Bb Bb C A', 5: 'Dm Bb C A', 6: 'G G A A', 7: 'D D G A'}   # the fix lifts toward major; the deals are bright D major
if not HO:
    for bar, row in ROWS.items():
        for k, ch in enumerate(row.split()):
            bb = BB(bar, k + 1); r = CROOT[ch]; lo = r.replace('2', '1') if r[-1] == '2' else r.replace('1', '0')
            cbp(lo, B(bb), .42, dur=.3); cpz(r, B(bb), .6, dur=.28)
            if bar >= 3: cpz(r, B(bb + .5), .5, dur=.28)                                    # the bass doubles up for port hacking
            n = 2 if bar < 3 else 4                                                      # spiccato violins: eighths, then sixteenths
            if bar < 7:
              for j in range(n): vsp(TONES[ch][j % (2 if bar < 5 else 3)], B(bb + j / n), .24 + .02 * min(bar, 5), dur=.1)
            if k % 2 == 0: [ (hnl if bar < 6 else tpl)(nn, B(bb), .2 if bar < 6 else .13, dur=BEAT * 2 - .08, rel=.25) for nn in PAD[ch] ]
            if bar == 7: xyl(TONES[ch][k % 3], B(bb), .3, dur=.15); xyl(TONES[ch][(k + 1) % 3], B(bb + .5), .26, dur=.15)   # the deals bounce
        timp(AT(bar), .45 + .04 * bar)
        if bar < 3:   # the tick of the clock: rim on every beat, snare on 2 and 4
            for q in range(4): one(RIM, AT(bar, q + 1), .16, .1)
            snare(AT(bar, 2), .28); snare(AT(bar, 4), .28); kick(AT(bar), .5); kick(AT(bar, 3), .4)
        else:
            groove(BB(bar), BB(bar + 1), .5 + .03 * (bar - 3), .05 + .015 * (bar - 3) + (.05 if bar == 7 else 0))
    roll_to(AT(2, 3), AT(3), .3); swell_to(AT(6), .35)
    roll_to(AT(7, 3), LOOP_IN, .28)                                                      # into the LIVE bar

# ---------------- sounds on the picture's beats ----------------
def capsnd(t): xyl('D6', t, .24); fx('casino/card-place-1.ogg', t, .13)
def stamp_hit(t, g=1.0, ch='D'): kick(t, .85 * g); timp(t, .8 * g); cbp(CH[ch][3], t, .9 * g); fx('impact/impactPunch_heavy_000.ogg', t, .45 * g); H(t, 'stamp')
def push(t): fx('casino/card-slide-3.ogg', t - .15, .26)
def fxa(name, t, g=1.0, pan=0.0):
    x = load(K + name); e = np.convolve(np.abs(x).max(1), np.ones(96) / 96, 'same'); att = int(np.argmax(e >= .15 * e.max()))
    USED.add(K + name); put(x, t - att / SR, g, pan)
for bar, n in [(0, 2), (1, 2), (2, 2), (3, 1), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2)]:
    for i in range(n):
        if bar == 0 and i == 0: continue   # frame 0 belongs to the box
        capsnd(AT(bar) + i * E8)
# NEW PHONE: the box slams down in frame 0; flaps pop; the phone rises; ACTIVATED; it rings
fx('impact/impactWood_heavy_000.ogg', 0.0, .6); fx('impact/impactSoft_heavy_000.ogg', 0.0, .5); kick(0.0, 1.0); timp(0.0, .9); one(CRASH_MF, 0.0, .3)
for n in ('D2', 'A2'): hns(n, 0.0, .9, dur=.5)
tbs('D2', 0.0, .8, dur=.5); cbp('D1', 0.0, 1.0); H(0.0, 'box')
fx('casino/cards-pack-open-1.ogg', AT(0, 3), .55); kick(AT(0, 3), .6); one(RIM, AT(0, 3), .35, .1); H(AT(0, 3), 'flaps')
for k, n in enumerate(('D5', 'F5', 'A5', 'D6')): glk(n, AT(0, 4) - .1 + k * S16, .35)
fx('interface/confirmation_001.ogg', AT(1), .4); glk('A6', AT(1), .3); kick(AT(1), .55); H(AT(1), 'activated')
def ring(t):
    for j in range(8): glk(('D6', 'F6')[j % 2], t + j * .05, .32)
    fx('interface/tick_002.ogg', t, .3); kick(t, .45); H(t, 'ring')
for t in (AT(1, 3), AT(1, 4), AT(2)): ring(t)
fx('impact/impactMetal_light_001.ogg', AT(2, 2), .55); one(RIM, AT(2, 2), .4, .1); kick(AT(2, 2), .5); H(AT(2, 2), 'hook')
fx('rpg/cloth3.ogg', AT(2, 3), .3); kick(AT(2, 3), 1.0); one(RIM, AT(2, 3), .4, .1); H(AT(2, 3), 'yank')
for k, n in enumerate(('D3', 'F3', 'A3', 'D4')): tbs(n, AT(2, 3) + k * S16 / 2, .5, dur=.1)
# PORT HACKING: up to the Scammer; the number pulled out like a thread; along it to the vault; the door; the cash; the calendar
push(AT(3) + .15); fx('casino/card-slide-2.ogg', AT(3) + .1, .3)
fxa('interface/scratch_004.ogg', AT(3, 3) + .02, .16); kick(AT(3, 3), .95); one(RIM, AT(3, 3), .4, .1); H(AT(3, 3), 'thread')   # the scratch swells in just behind the kick
for k, n in enumerate(('A3', 'Bb3', 'A3', 'G#3', 'A3')): cla(n, AT(3, 3.5) + k * S16, .45, dur=.12)
fx('casino/card-slide-4.ogg', AT(4) - .2, .3)                                                    # the camera pans along the thread
fx('rpg/metalLatch.ogg', AT(4, 3), .6); fx('rpg/creak1.ogg', AT(4, 3) + .05, .4); stamp_hit(AT(4, 3), 1.0, 'A'); one(CRASH, AT(4, 3), .35)
fx('rpg/handleCoins.ogg', AT(5), .45); kick(AT(5), .7); H(AT(5), 'cash')
for k in range(1, 8): fx(('casino/card-fan-1.ogg', 'casino/card-fan-2.ogg')[k % 2], AT(5) + k * E8, .16)
for b in (2, 3, 4): fx('rpg/bookFlip2.ogg', AT(5, b), .4); one(RIM, AT(5, b), .3, .1); H(AT(5, b), 'page')
# THE FIX: dive into the vault; typing; Jeff; the padlock slams; the check
fx('casino/card-slide-5.ogg', AT(6) - .15, .18); kick(AT(6), .95); one(CRASH_MF, AT(6), .25); H(AT(6), 'dive')
for k in range(1, 5): fx(('interface/click_002.ogg', 'interface/click_003.ogg')[k % 2], AT(6) + k * E8, .18)
fx('interface/pluck_002.ogg', AT(6, 2), .35); kick(AT(6, 2), .55); H(AT(6, 2), 'jeff')
fx('rpg/metalClick.ogg', AT(6, 3), .6); stamp_hit(AT(6, 3), 1.0, 'A'); one(CRASH_MF, AT(6, 3), .3)
fx('interface/confirmation_002.ogg', AT(6, 4), .4); kick(AT(6, 4), .6); one(RIM, AT(6, 4), .35, .1); H(AT(6, 4), 'check')
for k, n in enumerate(('A5', 'C#6', 'E6')): glk(n, AT(6, 4) + k * S16, .32)
# DEALS: a tag on 1, 2, 3; the chat bubble on 4
push(AT(7))
for b in range(1, 5): t = AT(7, b); fx('casino/card-place-2.ogg', t, .32); glk(('D6', 'F#6', 'A6', 'D7')[b - 1], t, .24); kick(t, .5); H(t, 'tag')
# LIVE ON YOUTUBE (the loop's cue carries the music from here): LIVE on 2, the channel row on 3, the chat bubble on 4
FOLEY_END = END - .02
push(AT(8))
fx('interface/switch_007.ogg', AT(8, 2), .35); H(AT(8, 2), 'live')
fx('rpg/bookPlace1.ogg', AT(8, 3), .3); H(AT(8, 3), 'channel')
fx('casino/card-place-1.ogg', AT(8, 4), .3); fx('interface/pluck_001.ogg', AT(8, 4), .25); H(AT(8, 4), 'chat')
# HANDOFF: the loop's pieces on the beats of bar 9
push(AT(9))
for b in (1, 2, 3, 4): t = AT(9, b); fx('rpg/bookPlace1.ogg', t, .3 if b < 4 else .22); H(t, 'piece')

# ---------------- mix: composed bars + the loop's cue ----------------
n_end, n_in = int(END * SR), int(LOOP_IN * SR)
comp = out[:n_end].copy()
def read_wav(p):
    import wave as _w
    with _w.open(p) as w: return np.frombuffer(w.readframes(w.getnframes()), '<i2').reshape(-1, 2).astype(np.float32) / 32768
LOOP = read_wav('out/rossen-loop/loop_norm.wav'); assert abs(len(LOOP) - 5 * SR) < 2, len(LOOP)
# the composed part is levelled against the loop: its last bars sit at the loop's loudness
rms = lambda x: float(np.sqrt((x ** 2).mean() + 1e-12))
if not HO:
    target = rms(LOOP[: int(2.5 * SR)]); cur = rms(comp[int(AT(6) * SR): n_in])
    g = target / cur * 10 ** (-1.0 / 20)   # 1 dB under the loop, so the deals lift
    comp *= g
    lim = 10 ** (-4.0 / 20); comp = np.tanh(comp / lim) * lim    # soft ceiling at -4 dBFS: the AAC encode overshoots transients by about 1.5 dB
    fade = int(.006 * SR); body = comp.copy()
    # after bar 8 starts, only the composed tails of bar 7 and the foley remain; they must be silent by 25.0 s
    tail = np.ones(n_end, np.float32); t0 = int(FOLEY_END * SR) - int(.25 * SR); tail[t0:] = np.linspace(1, 0, n_end - t0) ** 2
    comp *= tail[:, None]
    duck = np.ones(n_end, np.float32); d0 = int((LOOP_IN - .04) * SR); d1 = int((LOOP_IN + .04) * SR); duck[d0:d1] = np.linspace(1, .6, d1 - d0); duck[d1:] = .6
    comp *= duck[:, None]   # the composed layer steps back as the loop's cue takes over, so the two downbeats don't stack
    lp = LOOP.copy(); lp[:fade] *= np.linspace(0, 1, fade)[:, None]                          # a 6 ms fade-in: the cue enters on its own downbeat
    comp[n_in:n_end] += lp[: n_end - n_in]
    print('levels: composed bars 6-7 %.1f dBFS rms, loop bar 1 %.1f dBFS rms, peak %.2f' % (20 * np.log10(rms(comp[int(AT(6) * SR):n_in])), 20 * np.log10(target), np.abs(comp).max()))
od = 'out/rossen-tease-friday'; os.makedirs(od, exist_ok=True)
def write(p, x):
    with wave.open(p, 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1) * 32767).astype('<i2').tobytes())
if HO: write(od + '/score_hits.wav', comp / max(1e-6, np.abs(comp).max()) * .9)
else:
    write(od + '/tease_audio.wav', comp)
    write(od + '/full_audio.wav', np.concatenate([comp, LOOP, LOOP]))   # the loop's audio, sample for sample, twice: its end wraps into its start
json.dump(sorted(set(HITS)), open(od + '/hits.json', 'w'))
if not HO:
    with open(od + '/samples_used.txt', 'w') as f: f.write('\n'.join(sorted(USED)) + '\n')
    PACK = {'interface': 'https://kenney.nl/assets/interface-sounds', 'impact': 'https://kenney.nl/assets/impact-sounds', 'rpg': 'https://kenney.nl/assets/rpg-audio',
            'casino': 'https://kenney.nl/assets/casino-audio', 'digital': 'https://kenney.nl/assets/digital-audio'}
    loop_used = [l.strip() for l in open('out/rossen-loop/samples_used.txt') if l.strip()]
    with open(od + '/audio_sources.txt', 'w') as f:
        f.write('Rossen Reports Friday live tease (25 s) + the LIVE TODAY loop played twice (10 s). Every recorded audio file in the mix, with its source and license.\n')
        f.write('All are CC0 1.0 (public domain dedication, commercial use allowed, no attribution required). None come from a music library that registers with Content ID.\n\n')
        for u in sorted(USED | set(loop_used)):
            if u.startswith('kenney/'): src = PACK[u.split('/')[1]] + '  (Kenney, kenney.nl)'
            else: src = 'https://github.com/sgossner/VSCO-2-CE  (Versilian Studios Chamber Orchestra 2 Community Edition' + (', VSCO 1 drums folder' if 'VSCO 1' in u else '') + ')'
            who = ('tease' if u in USED else '') + (' + ' if u in USED and u in loop_used else '') + ('loop cue' if u in loop_used else '')
            f.write(f'{u}\n    used in: {who}\n    source: {src}\n    license: CC0 1.0\n')
        f.write('\nComposed (not recorded files): the whole score. Bars 0-7 are written note by note in score_tease.py on the 96 BPM grid in D '
                '(the loop\'s tempo and key) and played by the VSCO recordings above: the ticking rim pulse and low brass of the new-phone scene, '
                'the glockenspiel phone rise and ring trills, the spiccato build, the Scammer\'s clarinet, the trombone yank, the xylophone bounce of the deals. Bars 8-9 and the appended loop are the LIVE TODAY loop cue, also composed in code (score_loop.py). '
                'No synthesized tones are used anywhere; every sound effect is a recorded Kenney file.\n')
print(od, len(set(HITS)), 'hits,', len(USED), 'samples')
