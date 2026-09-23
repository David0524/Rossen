"""Soundtrack for the Rossen Reports title sequence (rossen-title-sequence.html), built only from recorded samples.

Music: an original 20 s cue sequenced from VSCO 2 Community Edition orchestral samples plus the VSCO 1 drum kit (CC0):
drum groove (kick, snare, tenor toms, tambourine), driving spiccato strings, pizzicato bass, a brass news-theme fanfare,
timpani, cymbal swells, xylophone and glockenspiel. Foley: Kenney CC0 packs.
144 BPM from 0.00 s: one beat = 5/12 s = 10 frames, one bar = 40 frames. The countdown and the run are one bar each,
every other scene is two bars, so every cut in the picture lands on a downbeat.
D minor for the scam half, D major from the deals on.

usage: python3 score_title.py [samples_dir]  ->  out/rossen-title-sequence/score.wav
"""
import numpy as np, subprocess, wave, sys, os, re, glob, math
SR = 48000; DUR = 20.0
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

BEAT = 5 / 12; E8, S16 = BEAT / 2, BEAT / 4
B = lambda b: b * BEAT   # beat -> seconds (beat 0 = first frame)
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

# Section map (beats): countdown 0-4 | run 4-8 | phone 8-16 | hidden cam 16-24 | deals 24-32 | cards 32-40 | logo 40-48
def groove(b0, b1, g=.8, tamb_g=.16):   # kick on 1 and the "and" of 2 and on 3, snare on 2 and 4, tambourine eighths
    for bb in range(int(b0), int(b1)):
        pos = bb % 4
        if pos in (0, 2): kick(B(bb), g)
        if pos == 1: kick(B(bb + .5), g * .75)
        if pos in (1, 3): snare(B(bb), .5)
    tamb(B(b0), B(b1), tamb_g)
def pulse_bass(b0, b1, notes, inst=cpz, g=.75):   # eighth-note bass, one note per beat
    for bb in range(int(b0), int(b1)):
        n = notes[(bb - int(b0)) % len(notes)]; inst(n, B(bb), g, dur=.16); inst(n, B(bb + .5), g * .85, dur=.16)

# ================= countdown (bar 0) =================
for bb in (0, 1, 2):
    tt = B(bb); timp(tt, .85); tuned(TOMH, tt, .5, -.32); snare(tt, .35); fx('interface/click_002.ogg', tt, .35); cbp('D1', tt, .7)
roll_to(B(2), B(3), .5)
for k, n in enumerate(['A3', 'C4', 'D4', 'E4']): vsp(n, B(2) + k * S16, .45 + .08 * k, dur=.1)
hit(B(3), 'Dm', 1.0, .55); fx('impact/impactPunch_heavy_000.ogg', B(3), .6); fx('impact/impactWood_heavy_000.ogg', B(3), .4)   # LIVE
swell_to(B(4), .38)
for k, n in enumerate(['D4', 'F4', 'A4', 'D5']): vsp(n, B(3) + k * S16, .5 + .06 * k, dur=.09)

# ================= the run (bar 1) =================
hit(B(4), 'Dm', .95, .5)
groove(4, 7)
pulse_bass(4, 6, ['D2']); pulse_bass(6, 7, ['Bb1']); pulse_bass(7, 8, ['C2'])
ostinato(B(4), B(8), ['D3', 'A3', 'F3', 'A3'], vla, .45, E8, .15)
for bb, n, d in [(4, 'D4', .2), (4.5, 'D4', .1), (5, 'F4', .2), (5.5, 'D4', .1), (6, 'A4', .35)]: tps(n, B(bb), .85, dur=d)
stab(B(6), 'Bb', .55, bass=False); stab(B(7), 'C', .55, bass=False)
for k in range(6): fx(f'impact/footstep_concrete_00{k % 5}.ogg', B(4) + .06 + k * .19, .18, -.2)
t_skid = 1 / 3 * 5 + 1.3 / 1.2       # skid in the picture (scene 3.3 -> film 2.75)
fx('impact/footstep_concrete_003.ogg', t_skid, .4); fx('rpg/cloth3.ogg', t_skid, .35); one(CRASH_MF, t_skid, .25)
fx('rpg/metalClick.ogg', 1 / 3 * 5 + 1.55 / 1.2, .3, .2)
roll_to(B(7), B(8), .35, TIMP_ROLL); swell_to(B(8), .3)

# ================= phone (bars 2-3) =================
hit(B(8), 'Dm', .9, .45)
fx('interface/pluck_001.ogg', B(8) + .11, .35); fx('interface/pluck_002.ogg', B(8) + .33, .35)   # bubble + button pop in
for bb in range(8, 12): kick(B(bb), .7); one(RIM, B(bb + .5), .25, .1)
ostinato(B(8), B(12), ['D4', 'D4', 'Eb4', 'D4'], vpz, .55, E8)
pulse_bass(8, 12, ['D2'], cbp, .45)
t_up = B(8) + .7 / .9                # scammer rises behind the phone
for k, n in enumerate(('A3', 'G#3', 'G3', 'F3')): cla(n, t_up + k * S16 * 1.2, .5, dur=.1)
fx('rpg/creak1.ogg', t_up + .28, .2, .3); fx('rpg/creak2.ogg', t_up + .6, .15, .3)
hit(B(12), 'Dm', 1.0, .6); fx('impact/impactPunch_heavy_001.ogg', B(12), .6)                   # SCAM!
for k in range(8): vsp('D4' if k % 2 == 0 else 'Eb4', B(12) + .06 + k * S16 / 2 * 1.6, .5, dur=.06)
stab(B(13), 'Dm', .6); stab(B(13.5), 'Eb', .75)
kick(B(13), .6); snare(B(13.5), .35)
fx('interface/glitch_002.ogg', B(14), .4); fx('interface/glitch_003.ogg', B(14) + .13, .3)
roll_to(B(14), B(16), .45); swell_to(B(16), .3)
for k, n in enumerate(['D4', 'F4', 'A4', 'D5']): vsp(n, B(15) + k * S16, .5, dur=.1)

# ================= hidden camera (bars 4-5) =================
kick(B(16), .9); stab(B(16), 'Dm', .7); one(CRASH_MF, B(16), .3)
for bb in range(16, 20): kick(B(bb), .7); one(CLAVE, B(bb + .5), .25, .2)
pulse_bass(16, 20, ['D2', 'D2', 'Eb2', 'D2'])
fx('interface/confirmation_002.ogg', B(16) + .05, .15, .3)                                     # REC blip
stab(B(18), 'Bb', .7); tuned(TOMH, B(18), .5, -.32); fx('impact/footstep_wood_001.ogg', B(18) - .05, .35, -.4)   # Jeff barges in
hit(B(20), 'Eb', 1.0, .6); fx('impact/impactPunch_heavy_002.ogg', B(20), .6)                   # CAUGHT!
stab(B(20.5), 'Eb', .6)
for k in range(4): fx(f'casino/card-slide-{k + 1}.ogg', B(20) + .06 + k * .06, .2, .3)          # cash flies
t_bolt = B(16) + 1.85 / .9                                                                     # he bolts
for k, n in enumerate(['D5', 'C5', 'A4', 'G4', 'F4', 'E4', 'D4', 'C#4']): vpz(n, t_bolt + k * .042, .75)
kick(B(21), .7); snare(B(21.5), .4); kick(B(22), .7); pulse_bass(21, 22.5, ['D2'], cbp, .5)
t_whip = B(16) + 2.5 / .9
fx('rpg/cloth4.ogg', t_whip, .45); tomfill(B(22.5), B(24), .5); swell_to(B(24), .3)            # whip pan

# ================= deals (bars 6-7), D major =================
hit(B(24), 'D', .95, .55)
groove(24, 31)
pulse_bass(24, 30, ['D2']); pulse_bass(30, 31, ['G1']); pulse_bass(31, 32, ['A1'])
for bb, n in zip((24, 25, 26, 27), ('D5', 'F#5', 'A5', 'D6')):                                  # a tag lands on every beat
    xyl(n, B(bb) + .17, .9); fx('casino/card-place-2.ogg', B(bb) + .17, .2, .4); fx('interface/scratch_001.ogg', B(bb) + .32, .12, .3)
fx('interface/pluck_001.ogg', B(24) + .4 / .9, .3)                                              # Jeff pops up
tps('A3', B(27), .7, dur=.18); tps('D4', B(27.5), .75, dur=.18)
hit(B(28), 'D', 1.0, .5); fx('impact/impactPunch_heavy_000.ogg', B(28), .55)                   # DEAL!
glk('D6', B(28), .6); glk('F#6', B(28.5), .5); glk('A6', B(29), .5)
stab(B(30), 'G', .6, bass=False); stab(B(31), 'A', .6, bass=False)
fx('rpg/bookFlip2.ogg', B(24) + 2.65 / .9, .6); snare(B(31), .3)                               # page turn

# ================= four cards (bars 8-9) =================
for bb, ch in zip((32, 33, 34, 35), ('D', 'F', 'G', 'A')):
    hit(B(bb), ch, .9, .35 if bb > 32 else .5); fx('rpg/bookPlace1.ogg', B(bb), .45)
for bb, arp in ((32, ['D3', 'F#3', 'A3', 'F#3']), (33, ['F3', 'A3', 'C4', 'A3']), (34, ['G3', 'B3', 'D4', 'B3']), (35, ['A3', 'C#4', 'E4', 'C#4'])):
    ostinato(B(bb), B(bb + 1), arp, vla, .45, S16, .09)
for bb in (32.5, 33.5, 34.5): snare(B(bb), .3)
# hold on the cards: a bar of groove on A while the captions read, fill into the logo
groove(36, 39, .75); pulse_bass(36, 40, ['A1'])
ostinato(B(36), B(40), ['A3', 'C#4', 'E4', 'C#4'], vla, .4, S16, .09)
roll_to(B(38), B(40), .4); tomfill(B(39), B(40), .45)

# ================= logo (bars 10-11) =================
hit(B(40), 'D', .9, .45); fx('rpg/cloth2.ogg', B(40), .35); fx('interface/pluck_001.ogg', B(40) + .1, .3)
for bb, n in ((40, 'D4'), (40.5, 'F#4'), (41, 'A4')): tps(n, B(bb), .8, dur=.18)
groove(41, 42, .7); pulse_bass(40, 43, ['D2'], cpz, .6)
fx('rpg/cloth1.ogg', 17.7, .3)                                                                 # the logo starts to fall
tomfill(B(43), B(44), .5); roll_to(B(42), B(44), .35, TIMP_ROLL); swell_to(B(44), .4)
t = B(44)   # the payoff: full D major lands with the logo on the downbeat of the last bar
for n in ('D4', 'F#4', 'A4'): tpl(n, t, .95, dur=1.4, rel=.6)
for n in ('D2', 'F#2', 'A2'): hnl(n, t, .9, dur=1.4, rel=.6)
for n in ('D2', 'A1'): tbl(n, t, .85, dur=1.4, rel=.6)
cbp('D1', t, 1.0); cpz('D2', t, .9); timp(t, 1.0); kick(t, 1.0); one(CRASH, t, .65); glk('D6', t, .6)
fx('impact/impactSoft_heavy_000.ogg', t, .45)
for k in range(2): fx(f'casino/card-fan-{k + 1}.ogg', t + .02 + k * .1, .25, (-.3, .3)[k])        # confetti
snare(B(45), .6); one(TRI, B(45), .35); tps('D4', B(45), .7, dur=.25); hns('D2', B(45), .6, dur=.25)
fx('impact/impactPunch_heavy_001.ogg', B(45), .5)                                              # LIVE stamp

# ---------------- master ----------------
fade = int(.8 * SR); out[-fade:] *= np.linspace(1, 0, fade)[:, None] ** 2
out = np.tanh(out * 1.1) / 1.1
out *= (10 ** (-1 / 20)) / max(1e-6, np.abs(out).max())
od = 'out/rossen-title-sequence'; os.makedirs(od, exist_ok=True)
with wave.open(od + '/score.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(out, -1, 1) * 32767).astype('<i2').tobytes())
with open(od + '/samples_used.txt', 'w') as f: f.write('\n'.join(sorted(USED)) + '\n')
print(od + '/score.wav', DUR, 's,', len(USED), 'samples')
