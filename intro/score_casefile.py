"""Soundtrack for the Rossen Reports "case file" title sequence (rossen-casefile.html). Recorded samples only, no synthesis.

Music: an original 19.5 s cue sequenced from VSCO 2 Community Edition / VSCO 1 orchestral and drum samples (CC0).
Foley: Kenney CC0 packs. 96 BPM, one beat = 0.625 s = 15 frames, one bar per scene, one continuous groove.
Big hits only on the story beats: the folder thwack, LIVE, SCAM!, CAUGHT!, WARNING!, DEAL!, LIVE NOW, the sign-off.
Every sound effect is placed by its attack, on the frame where its picture lands.

usage: python3 score_casefile.py [samples_dir]  ->  out/rossen-casefile/score.wav
"""
import numpy as np, subprocess, wave, sys, os, re, glob, math
SR = 48000; DUR = 19.5
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

# ================= bar 1: the case file =================
roll_to(0.0, AT(0, 2), .35)                                                                      # builds from the first frame
hit(AT(0, 2), 'Dm', 1.0, .5); fx('impact/impactPlank_medium_000.ogg', AT(0, 2), .6); fx('rpg/bookPlace2.ogg', AT(0, 2), .45)   # folder thwacks down
for k, n in enumerate(('D5', 'F5', 'A5', 'D6')):                                                 # L-I-V-E, one chip per eighth
    tt = AT(0, 2.5 + k * .5); xyl(n, tt, .85); fx('casino/card-place-1.ogg', tt, .3); kick(tt, .55 if k < 3 else .8)
stab(AT(0, 4), 'Dm', .8); one(CRASH_MF, AT(0, 4), .3)
fx('rpg/bookFlip2.ogg', AT(0, 4.5), .6); swell_to(AT(1), .3)                                     # cover flips open

# ================= the groove, bars 2-7 =================
groove(4, 28)
bass({4: 'D2', 5: 'D2', 6: 'Bb1', 7: 'C2',  8: 'D2', 9: 'D2', 10: 'D2', 11: 'Eb2',  12: 'Bb1', 13: 'Bb1', 14: 'Eb2', 15: 'Eb2',
      16: 'D2', 17: 'D2', 18: 'A1', 19: 'A1',  20: 'D2', 21: 'D2', 22: 'D2', 23: 'A1',  24: 'G2', 25: 'G2', 26: 'A1', 27: 'A1'})
strings({4: ('D3', 'A3'), 5: ('F3', 'A3'), 6: ('D3', 'F3'), 7: ('E3', 'G3'),  8: ('D3', 'A3'), 9: ('D3', 'A3'), 10: ('F3', 'A3'), 11: ('Eb3', 'G3'),
         12: ('D3', 'F3'), 13: ('D3', 'F3'), 14: ('Eb3', 'G3'), 15: ('Eb3', 'Bb3'),  16: ('D3', 'F3'), 17: ('D3', 'A3'), 18: ('E3', 'A3'), 19: ('C#4', 'E4'),
         20: ('D3', 'F#3'), 21: ('F#3', 'A3'), 22: ('F#3', 'A3'), 23: ('E3', 'A3'),  24: ('G3', 'B3'), 25: ('G3', 'D4'), 26: ('A3', 'C#4'), 27: ('A3', 'E4')})

# ================= bar 2: the evidence board =================
downbeat(4)
for bb, n, d in [(4, 'D4', .28), (4.5, 'D4', .15), (5, 'F4', .28), (5.5, 'D4', .15), (6, 'A4', .55)]: tps(n, B(bb), .8, dur=d)   # the theme
fx('interface/pluck_001.ogg', AT(1, 2), .32)                                                     # Jeff pops up
fx('rpg/metalClick.ogg', AT(1, 3), .32, .2); stab(AT(1, 3), 'Bb', .5, bass=False)               # magnifier up
roll_to(AT(1, 4), AT(2), .32, TIMP_ROLL)                                                         # through the lens

# ================= bar 3: phishing =================
downbeat(8, .18); fx('interface/error_004.ogg', AT(2), .3)                                        # URGENT
for k, n in enumerate(('A3', 'G#3', 'G3', 'F3')): cla(n, AT(2, 2) + k * S16, .5, dur=.14)       # con man sneaks in with the hook
hit(AT(2, 3), 'Dm', 1.0, .55); fx('impact/impactPunch_heavy_001.ogg', AT(2, 3), .55)             # SCAM!
for k in range(3): tt = AT(2, 4) + k * S16 * 1.28; fx('interface/scratch_004.ogg', tt, .35, (-.3, 0, .3)[k]); snare(tt, .3)   # redaction marker strokes
roll_to(AT(2, 4.5), AT(3), .35)

# ================= bar 4: hidden camera =================
downbeat(12, .18); fx('interface/maximize_006.ogg', AT(3), .35); fx('interface/confirmation_002.ogg', AT(3) + .1, .14, .3)   # iris opens, REC
stab(AT(3, 2), 'Bb', .6); fx('impact/footstep_wood_001.ogg', AT(3, 2), .35, -.4)                # Jeff barges in
hit(AT(3, 3), 'Eb', 1.0, .55); fx('interface/switch_007.ogg', AT(3, 3), .5); fx('impact/impactPunch_heavy_002.ogg', AT(3, 3), .5)   # flash + CAUGHT!
fx('rpg/cloth4.ogg', AT(3, 4), .4); tomfill(AT(3, 4), AT(4), .45, S16); swell_to(AT(4), .3)    # the frame flies off as a Polaroid

# ================= bar 5: the warning =================
downbeat(16); fx('rpg/bookPlace1.ogg', AT(4), .4)                                               # the Polaroid lands, pinned
fx('interface/pluck_002.ogg', AT(4, 1.5), .28)                                                   # Jeff pops up
fx('rpg/cloth1.ogg', AT(4, 2), .4); glk('A5', AT(4, 2), .5); glk('C#6', AT(4, 2.25), .45)       # redaction bars peel back
hit(AT(4, 3), 'A', 1.0, .5); fx('impact/impactPunch_heavy_000.ogg', AT(4, 3), .5)               # WARNING!
fx('rpg/bookFlip2.ogg', AT(4, 4.5), .6)                                                          # page turn

# ================= bar 6: deals, D major =================
downbeat(20)
for k, n in enumerate(('D5', 'F#5', 'A5', 'D6')): tt = AT(5, 1 + k * .5); xyl(n, tt, .85); fx('casino/card-place-2.ogg', tt, .16, .4)   # tags on eighths
fx('interface/pluck_001.ogg', AT(5, 2), .28)                                                     # Jeff, thumbs up
hit(AT(5, 3), 'D', 1.0, .5); fx('impact/impactPunch_heavy_000.ogg', AT(5, 3), .5)               # DEAL!
for k, n in enumerate(('D6', 'F#6', 'A6')): glk(n, AT(5, 3.5) + k * E8, .45)
fx('rpg/bookClose.ogg', AT(5, 4) + .5, .5); fx('rpg/cloth2.ogg', AT(5, 4), .3)                  # the folder swings shut

# ================= bar 7: case closed =================
downbeat(24); stab(AT(6), 'G', .7); fx('rpg/bookPlace1.ogg', AT(6), .45)                         # the logo sticker slaps on
fx('interface/pluck_001.ogg', AT(6, 2), .28)
hit(AT(6, 3), 'A', .95, .45); fx('impact/impactPunch_heavy_001.ogg', AT(6, 3), .5)               # LIVE NOW
roll_to(AT(6, 4), AT(7), .4, TIMP_ROLL); swell_to(AT(7), .4); tomfill(AT(6, 4.5), AT(7), .45, S16)   # the big rubber stamp comes down

# ================= bar 8: the sign-off (17.5 s) =================
t = AT(7)
for n in ('D4', 'F#4', 'A4'): tpl(n, t, .95, dur=1.4, rel=.6)
for n in ('D2', 'F#2', 'A2'): hnl(n, t, .9, dur=1.4, rel=.6)
for n in ('D2', 'A1'): tbl(n, t, .85, dur=1.4, rel=.6)
cbp('D1', t, 1.0); cpz('D2', t, .9); timp(t, 1.0); kick(t, 1.0); one(CRASH, t, .6); glk('D6', t, .55)
fx('impact/impactPlank_medium_000.ogg', t, .5); fx('impact/impactSoft_heavy_000.ogg', t, .4)    # the stamp presses and lifts

# ---------------- master ----------------
fade = int(1.0 * SR); out[-fade:] *= np.linspace(1, 0, fade)[:, None] ** 2
out = np.tanh(out * 1.1) / 1.1
out *= (10 ** (-1 / 20)) / max(1e-6, np.abs(out).max())
od = 'out/rossen-casefile'; os.makedirs(od, exist_ok=True)
with wave.open(od + '/score.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(out, -1, 1) * 32767).astype('<i2').tobytes())
with open(od + '/samples_used.txt', 'w') as f: f.write('\n'.join(sorted(USED)) + '\n')
print(od + '/score.wav', DUR, 's,', len(USED), 'samples')
