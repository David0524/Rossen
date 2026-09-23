"""Soundtrack for the Rossen Reports title sequence (rossen-title-sequence.html), built only from recorded samples.

Music: an original 19.5 s cue sequenced from VSCO 2 Community Edition orchestral samples plus the VSCO 1 drum kit (CC0):
drum groove (kick, snare, tenor toms, tambourine), driving spiccato strings, pizzicato bass, a brass news-theme fanfare,
timpani, cymbal swells, xylophone and glockenspiel. Foley: Kenney CC0 packs.
96 BPM: one beat = 0.625 s = 15 frames, one bar = 2.5 s. Eight bars, one per scene, every scene at the same pace:
countdown | run | phone | hidden cam | deals | cards | logo arrives | logo lands (17.5 s) and rings out.
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
def fx(name, t, g=1.0, pan=0.0, dur=None): one(K + name, t, g, pan, dur)

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

def groove(b0, b1, g=.8, tamb_g=.16):   # kick on 1, the "and" of 2 and 3; snare on 2 and 4; tambourine eighths
    for bb in range(int(b0), int(b1)):
        pos = bb % 4
        if pos in (0, 2): kick(B(bb), g)
        if pos == 1: kick(B(bb + .5), g * .75)
        if pos in (1, 3): snare(B(bb), .5)
    tamb(B(b0), B(b1), tamb_g)
def pulse_bass(b0, b1, notes, inst=cpz, g=.75):   # eighth-note bass, one note per beat
    for bb in range(int(b0), int(b1)):
        n = notes[(bb - int(b0)) % len(notes)]; inst(n, B(bb), g, dur=.25); inst(n, B(bb + .5), g * .85, dur=.25)

# ================= bar 1: countdown, 3-2-1-LIVE on the beats =================
for bb in (0, 1, 2):
    tt = B(bb); timp(tt, .8); tuned(TOMH, tt, .45, -.32); snare(tt, .3); fx('interface/click_002.ogg', tt, .35); cbp('D1', tt, .6)
roll_to(B(2), B(3), .45)
for k, n in enumerate(['A3', 'C4', 'D4', 'E4']): vsp(n, B(2) + k * S16, .4 + .08 * k, dur=.13)
hit(B(3), 'Dm', 1.0, .55); fx('impact/impactPunch_heavy_000.ogg', B(3), .6); fx('impact/impactWood_heavy_000.ogg', B(3), .4)   # LIVE
for k, n in enumerate(['D4', 'F4', 'A4', 'D5']): vsp(n, B(3.5) + k * S16 / 2, .5 + .06 * k, dur=.08)
swell_to(BAR(1), .35)

# ================= bar 2: the run =================
hit(BAR(1), 'Dm', .95, .5)
groove(4, 8)
pulse_bass(4, 6, ['D2']); pulse_bass(6, 7, ['Bb1']); pulse_bass(7, 8, ['C2'])
ostinato(BAR(1), BAR(2), ['D3', 'A3', 'F3', 'A3'], vla, .45, E8, .2)
for bb, n, d in [(4, 'D4', .26), (4.5, 'D4', .14), (5, 'F4', .26), (5.5, 'D4', .14), (6, 'A4', .5)]: tps(n, B(bb), .85, dur=d)
stab(B(6), 'Bb', .55, bass=False); stab(B(7), 'C', .55, bass=False)
for k in range(9): fx(f'impact/footstep_concrete_00{k % 5}.ogg', 2.56 + k * .17, .18, -.2)
fx('impact/footstep_concrete_003.ogg', 4.05, .4); fx('rpg/cloth3.ogg', 4.05, .35); one(CRASH_MF, 4.05, .25)   # skid
fx('rpg/metalClick.ogg', 4.35, .3, .2)
roll_to(B(7), BAR(2), .35, TIMP_ROLL); swell_to(BAR(2), .3)

# ================= bar 3: phone =================
hit(BAR(2), 'Dm', .9, .45)
fx('interface/pluck_001.ogg', 5.1, .35); fx('interface/pluck_002.ogg', 5.28, .35)               # bubble + button pop in
for bb in range(8, 10): kick(B(bb), .7); one(RIM, B(bb + .5), .25, .1)
ostinato(BAR(2), B(10), ['D4', 'D4', 'Eb4', 'D4'], vpz, .55, E8)
pulse_bass(8, 10, ['D2'], cbp, .45)
for k, n in enumerate(('A3', 'G#3', 'G3', 'F3')): cla(n, B(9) + k * S16, .5, dur=.14)           # scammer rises with the rod
fx('rpg/creak1.ogg', 5.9, .2, .3)
hit(B(10), 'Dm', 1.0, .6); fx('impact/impactPunch_heavy_001.ogg', B(10), .6)                    # SCAM! (beat 3)
for k in range(6): vsp('D4' if k % 2 == 0 else 'Eb4', B(10) + .06 + k * S16 / 2, .5, dur=.07)
stab(B(10.5), 'Dm', .55); stab(B(11), 'Eb', .75); kick(B(11), .6)                              # the phone tips
fx('interface/glitch_002.ogg', 7.0, .4); fx('interface/glitch_003.ogg', 7.1, .3)
roll_to(B(11), BAR(3), .45); swell_to(BAR(3), .3)
for k, n in enumerate(['D4', 'F4', 'A4', 'D5']): vsp(n, B(11.5) + k * S16 / 2, .5, dur=.08)

# ================= bar 4: hidden camera =================
kick(BAR(3), .9); stab(BAR(3), 'Dm', .7); one(CRASH_MF, BAR(3), .3)
for bb in range(12, 14): kick(B(bb), .7); one(CLAVE, B(bb + .5), .25, .2)
pulse_bass(12, 14, ['D2', 'D2'])
fx('interface/confirmation_002.ogg', BAR(3) + .05, .15, .3)                                    # REC blip
stab(B(13), 'Bb', .7); tuned(TOMH, B(13), .5, -.32); fx('impact/footstep_wood_001.ogg', 7.95, .35, -.4)   # Jeff barges in (beat 2)
hit(B(14), 'Eb', 1.0, .6); fx('impact/impactPunch_heavy_002.ogg', B(14), .6)                   # CAUGHT! (beat 3)
for k in range(4): fx(f'casino/card-slide-{k + 1}.ogg', 8.8 + k * .06, .2, .3)                 # cash flies
for k, n in enumerate(['D5', 'C5', 'A4', 'G4', 'F4', 'E4', 'D4', 'C#4']): vpz(n, 9.05 + k * .045, .75)   # he bolts
fx('rpg/cloth4.ogg', 9.5, .45); tomfill(9.5, BAR(4), .5, S16); swell_to(BAR(4), .3)           # whip pan

# ================= bar 5: deals, D major =================
hit(BAR(4), 'D', .95, .55)
groove(16, 20)
pulse_bass(16, 19, ['D2']); pulse_bass(19, 20, ['A1'])
for k, n in enumerate(('D5', 'F#5', 'A5', 'D6')):                                               # a tag lands on each eighth
    tl = BAR(4) + k * E8 + .16; xyl(n, tl, .9); fx('casino/card-place-2.ogg', tl, .2, .4); fx('interface/scratch_001.ogg', tl + .06, .12, .3)
fx('interface/pluck_001.ogg', 10.45, .3)                                                         # Jeff pops up
hit(B(18), 'D', 1.0, .5); fx('impact/impactPunch_heavy_000.ogg', B(18), .55)                   # DEAL! (beat 3)
glk('D6', B(18), .6); glk('F#6', B(18.5), .5); glk('A6', B(19), .5)
fx('rpg/bookFlip2.ogg', 12.1, .6); snare(12.1, .3)                                               # page turn

# ================= bar 6: four cards =================
for k, ch in enumerate(('D', 'F', 'G', 'A')):
    tt = BAR(5) + k * E8; stab(tt, ch, .8); kick(tt, .7 if k == 0 else .45); fx('rpg/bookPlace1.ogg', tt, .45)
    if k == 0: timp(tt, .8); one(CRASH_MF, tt, .35)
groove(22, 24, .7); pulse_bass(22, 24, ['A1'])
ostinato(B(22), BAR(6), ['A3', 'C#4', 'E4', 'C#4'], vla, .4, S16, .12)
roll_to(B(23), BAR(6), .4)

# ================= bar 7: the logo arrives =================
hit(BAR(6), 'D', .85, .4); fx('rpg/cloth2.ogg', BAR(6), .4)                                     # cards drift away
fx('interface/pluck_001.ogg', 15.25, .3)                                                         # Jeff pops in
groove(24, 27, .65, .12); pulse_bass(24, 27, ['D2'], cpz, .6)
for bb, n in ((25, 'D4'), (25.5, 'F#4'), (26, 'A4')): tps(n, B(bb), .75, dur=.24)
fx('rpg/cloth1.ogg', 15.9, .3)                                                                   # the logo starts to fall
tomfill(B(27), BAR(7), .5, S16); roll_to(B(26), BAR(7), .35, TIMP_ROLL); swell_to(BAR(7), .4)

# ================= bar 8: the payoff (17.5 s) =================
t = BAR(7)
for n in ('D4', 'F#4', 'A4'): tpl(n, t, .95, dur=1.3, rel=.6)
for n in ('D2', 'F#2', 'A2'): hnl(n, t, .9, dur=1.3, rel=.6)
for n in ('D2', 'A1'): tbl(n, t, .85, dur=1.3, rel=.6)
cbp('D1', t, 1.0); cpz('D2', t, .9); timp(t, 1.0); kick(t, 1.0); one(CRASH, t, .65); glk('D6', t, .6)
fx('impact/impactSoft_heavy_000.ogg', t, .45)
for k in range(2): fx(f'casino/card-fan-{k + 1}.ogg', t + .02 + k * .1, .25, (-.3, .3)[k])        # confetti
snare(B(29), .6); one(TRI, B(29), .35); tps('D4', B(29), .7, dur=.3); hns('D2', B(29), .6, dur=.3)
fx('impact/impactPunch_heavy_001.ogg', B(29), .5)                                               # LIVE stamp (beat 2)

# ---------------- master ----------------
fade = int(.8 * SR); out[-fade:] *= np.linspace(1, 0, fade)[:, None] ** 2
out = np.tanh(out * 1.1) / 1.1
out *= (10 ** (-1 / 20)) / max(1e-6, np.abs(out).max())
od = 'out/rossen-title-sequence'; os.makedirs(od, exist_ok=True)
with wave.open(od + '/score.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(out, -1, 1) * 32767).astype('<i2').tobytes())
with open(od + '/samples_used.txt', 'w') as f: f.write('\n'.join(sorted(USED)) + '\n')
print(od + '/score.wav', DUR, 's,', len(USED), 'samples')
