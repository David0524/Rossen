"""Soundtrack for the Rossen Reports title sequence (rossen-title-sequence.html), built only from recorded samples.

Music: an original 20 s cue sequenced from VSCO 2 Community Edition orchestral samples plus the VSCO 1 drum kit (CC0):
drum groove (kick, snare, tenor toms, tambourine), driving spiccato strings, pizzicato bass, a brass news-theme fanfare,
timpani, cymbal swells, xylophone and glockenspiel. Foley: Kenney CC0 packs.
120 BPM from 0.00 s, one beat = 0.5 s = 12 frames, so the music and the picture share one grid.
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

B = lambda b: 0.5 * b   # beat -> seconds (beat 0 = first frame)
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
    while t < t1 - 1e-6: one(TAMB if k % 2 == 0 else TAMB2, t, g * (1.0 if k % 2 else .7), .35); t += .25; k += 1
def swell_to(t, g=.4):
    if os.environ.get('PITCHED_ONLY'): return
    x = load(SWELL); USED.add(SWELL); pk = int(np.argmax(np.abs(x).max(1))); put(x[:pk], t - pk / SR, g, dur=pk / SR, rel=.02)
def roll_to(t0, t1, g=.45, rel=SN_ROLL):
    if os.environ.get('PITCHED_ONLY'): return
    x = load(rel); USED.add(rel); n = int((t1 - t0) * SR); put(x[:n] * np.linspace(.12, 1, n)[:, None] ** 1.5, t0, g)
def tomfill(t0, t1, g=.55, step=.125):
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
def ostinato(t0, t1, notes, inst, g=.5, step=.25, dur=.18):
    k = 0; t = t0
    while t < t1 - 1e-6: inst(notes[k % len(notes)], t, g, dur=dur); t += step; k += 1

# ================= 0-2  countdown =================
for tt in (0.0, 0.5, 1.0):
    timp(tt, .85); tuned(TOMH, tt, .5, -.32); snare(tt, .35); fx('interface/click_002.ogg', tt, .35)
    cbp('D1', tt, .7)
roll_to(1.0, 1.5, .5)
for k, n in enumerate(['A3', 'C4', 'D4', 'E4']): vsp(n, 1.0 + k * .125, .45 + .08 * k, dur=.12)
hit(1.5, 'Dm', 1.0, .55); fx('impact/impactPunch_heavy_000.ogg', 1.5, .6); fx('impact/impactWood_heavy_000.ogg', 1.5, .4)
swell_to(2.0, .38)
for k, n in enumerate(['D4', 'E4', 'F4', 'G4', 'A4', 'Bb4', 'C5', 'D5']): vsp(n, 1.5 + k * .0625, .5 + .04 * k, dur=.07)

# ================= 2-5  street run: the groove kicks in =================
hit(2.0, 'Dm', .95, .5)
for tt in (2.0, 2.75, 3.0, 3.75, 4.0): kick(tt, .8)
for tt in (2.5, 3.5): snare(tt, .5)
tamb(2.0, 3.75)
ostinato(2.0, 3.0, ['D2'], cpz, .75, .25, .2); ostinato(3.0, 3.5, ['Bb1'], cpz, .75, .25, .2); ostinato(3.5, 4.0, ['C2'], cpz, .75, .25, .2)
ostinato(2.0, 4.0, ['D3', 'A3', 'F3', 'A3'], vla, .45, .25, .18)
fan = [(2.0, 'D4', .22), (2.25, 'D4', .12), (2.5, 'F4', .22), (2.75, 'D4', .12), (3.0, 'A4', .4), (3.5, 'G4', .2), (3.75, 'E4', .2)]
for tt, n, d in fan: tps(n, tt, .85, dur=d)
for tt, ch in ((3.0, 'Bb'), (3.5, 'C')): stab(tt, ch, .55, bass=False)
for k in range(11): fx(f'impact/footstep_concrete_00{k % 5}.ogg', 2.06 + k * .16, .18, -.2)
stab(3.8, 'Dm', .8); one(CRASH_MF, 3.8, .3); fx('impact/footstep_concrete_003.ogg', 3.8, .4); fx('rpg/cloth3.ogg', 3.8, .35)   # skid
ostinato(4.0, 4.5, ['D2'], cbp, .5, .25, .2); one(CLAVE, 4.25, .2)
fx('rpg/metalClick.ogg', 4.1, .3, .2); cla('A3', 4.2, .5, dur=.1); cla('D4', 4.33, .55, dur=.1)
roll_to(4.5, 5.0, .4, TIMP_ROLL); swell_to(5.0, .32)
for k, n in enumerate(['D4', 'F4', 'A4', 'D5']): vsp(n, 4.5 + k * .125, .5, dur=.12)

# ================= 5-8  phone: phishing =================
hit(5.0, 'Dm', .9, .45)
fx('interface/pluck_001.ogg', 5.1, .35); fx('interface/pluck_002.ogg', 5.3, .35)             # bubble + button pop in
for tt in (5.0, 5.5, 6.0): kick(tt, .7)
for tt in (5.25, 5.75, 6.25): one(RIM, tt, .25, .1)
ostinato(5.0, 6.5, ['D4', 'D4', 'Eb4', 'D4'], vpz, .55, .25)
ostinato(5.0, 6.5, ['D2'], cbp, .45, .5)
for k, n in enumerate(('A3', 'G#3', 'G3', 'F3')): cla(n, 5.7 + k * .125, .5, dur=.11)           # scammer sneaks up with the rod
fx('rpg/creak1.ogg', 5.95, .2, .3); fx('rpg/creak2.ogg', 6.25, .15, .3)
hit(6.5, 'Dm', 1.0, .6); fx('impact/impactPunch_heavy_001.ogg', 6.5, .6)                       # SCAM!
stab(6.75, 'Dm', .6); stab(7.0, 'Eb', .75)
for k in range(8): vsp('D4' if k % 2 == 0 else 'Eb4', 6.56 + k * .0625, .5, dur=.07)          # scammer panics
fx('interface/glitch_002.ogg', 7.25, .4); fx('interface/glitch_003.ogg', 7.37, .3)
roll_to(7.5, 8.0, .45); swell_to(8.0, .3)
for k, n in enumerate(['D4', 'F4', 'A4', 'D5']): vsp(n, 7.5 + k * .125, .5, dur=.12)

# ================= 8-11  hidden camera =================
kick(8.0, .9); stab(8.0, 'Dm', .7); one(CRASH_MF, 8.0, .3)
ostinato(8.0, 9.5, ['D2', 'D2', 'Eb2', 'D2'], cpz, .7, .25, .2)
for tt in (8.0, 8.5, 9.0): kick(tt, .7)
for tt in (8.25, 8.75, 9.25): one(CLAVE, tt, .25, .2)
fx('interface/confirmation_002.ogg', 8.05, .15, .3)                                            # REC blip
stab(8.75, 'Bb', .7); tuned(TOMH, 8.75, .5, -.32); fx('impact/footstep_wood_001.ogg', 8.75, .35, -.4)   # Jeff barges in
hit(9.5, 'Eb', 1.0, .6); fx('impact/impactPunch_heavy_002.ogg', 9.5, .6)                       # CAUGHT!
stab(9.75, 'Eb', .6)
for k, n in enumerate(['D5', 'C5', 'A4', 'G4', 'F4', 'E4', 'D4', 'C#4']): vpz(n, 9.85 + k * .0417, .75)   # he bolts
for k in range(4): fx(f'casino/card-slide-{k + 1}.ogg', 9.55 + k * .06, .2, .3)                # cash flies
kick(10.0, .7); snare(10.25, .4); ostinato(10.0, 10.5, ['D2'], cbp, .5, .25, .2)
fx('rpg/cloth4.ogg', 10.5, .45); tomfill(10.5, 11.0, .55); swell_to(11.0, .3)                   # whip pan

# ================= 11-14  deals: D major =================
hit(11.0, 'D', .95, .55)
for tt in (11.0, 11.75, 12.0, 12.75, 13.0): kick(tt, .8)
for tt in (11.5, 13.5): snare(tt, .5)
tamb(11.0, 13.6)
ostinato(11.0, 12.5, ['D2'], cpz, .75, .25, .2); ostinato(12.5, 13.0, ['D2'], cpz, .75, .25, .2)
ostinato(13.0, 13.5, ['G1'], cpz, .75, .25, .2); ostinato(13.5, 14.0, ['A1'], cpz, .75, .25, .2)
for tt, n in zip((11.0, 11.25, 11.5, 11.75), ('D5', 'F#5', 'A5', 'D6')): xyl(n, tt, .9); fx('casino/card-place-2.ogg', tt, .2, .4)
for tt in (11.2, 11.45, 11.7, 11.95): fx('interface/scratch_001.ogg', tt, .12, .3)             # marker strike-throughs
tps('A3', 12.0, .7, dur=.2); tps('D4', 12.25, .75, dur=.2)
hit(12.5, 'D', 1.0, .5); fx('impact/impactPunch_heavy_000.ogg', 12.5, .55)                     # DEAL!
glk('D6', 12.5, .6); glk('F#6', 12.62, .5); glk('A6', 12.75, .5)
stab(13.0, 'G', .6, bass=False); stab(13.5, 'A', .6, bass=False)
fx('rpg/bookFlip2.ogg', 13.65, .6); snare(13.65, .3)                                           # page turn

# ================= 14-17  montage: a hit on every card =================
for tt, ch in zip((14.0, 14.5, 15.0, 15.5), ('D', 'F', 'G', 'A')):
    hit(tt, ch, .9, .35 if tt > 14 else .5); fx('rpg/bookPlace1.ogg', tt, .45)
for tt, arp in ((14.0, ['D3', 'F#3', 'A3', 'F#3']), (14.5, ['F3', 'A3', 'C4', 'A3']), (15.0, ['G3', 'B3', 'D4', 'B3']), (15.5, ['A3', 'C#4', 'E4', 'C#4'])): ostinato(tt, tt + .5, arp, vla, .45, .125, .1)
for tt in (14.25, 14.75, 15.25): snare(tt, .3)
# hold on the four cards: groove on A while the captions read, then a fill into the logo
ostinato(16.0, 17.0, ['A1'], cpz, .7, .25, .2); ostinato(16.0, 17.0, ['A3', 'C#4', 'E4', 'C#4'], vla, .4, .125, .1)
for tt in (16.0, 16.5): kick(tt, .75)
snare(16.25, .4); tamb(16.0, 16.5)
roll_to(16.5, 17.0, .4); tomfill(16.75, 17.0, .45)

# ================= 17-20  logo =================
hit(17.0, 'D', .9, .45); fx('rpg/cloth2.ogg', 17.0, .35); fx('interface/pluck_001.ogg', 17.1, .3)
for tt, n in ((17.0, 'D4'), (17.25, 'F#4'), (17.5, 'A4')): tps(n, tt, .8, dur=.2)
kick(17.5, .7); tomfill(17.5, 18.0, .5); roll_to(17.5, 18.0, .35, TIMP_ROLL); swell_to(18.0, .4)
t = 18.0   # the payoff: full D major lands with the logo
for n in ('D4', 'F#4', 'A4'): tpl(n, t, .95, dur=1.6, rel=.6)
for n in ('D2', 'F#2', 'A2'): hnl(n, t, .9, dur=1.6, rel=.6)
for n in ('D2', 'A1'): tbl(n, t, .85, dur=1.6, rel=.6)
cbp('D1', t, 1.0); cpz('D2', t, .9); timp(t, 1.0); kick(t, 1.0); one(CRASH, t, .65); glk('D6', t, .6)
fx('impact/impactSoft_heavy_000.ogg', t, .45)
for k in range(2): fx(f'casino/card-fan-{k + 1}.ogg', 18.02 + k * .1, .25, (-.3, .3)[k])       # confetti
snare(18.5, .6); one(TRI, 18.5, .35); tps('D4', 18.5, .7, dur=.25); hns('D2', 18.5, .6, dur=.25)
fx('impact/impactPunch_heavy_001.ogg', 18.5, .5)                                               # LIVE stamp

# ---------------- master ----------------
fade = int(.8 * SR); out[-fade:] *= np.linspace(1, 0, fade)[:, None] ** 2
out = np.tanh(out * 1.1) / 1.1
out *= (10 ** (-1 / 20)) / max(1e-6, np.abs(out).max())
od = 'out/rossen-title-sequence'; os.makedirs(od, exist_ok=True)
with wave.open(od + '/score.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(out, -1, 1) * 32767).astype('<i2').tobytes())
with open(od + '/samples_used.txt', 'w') as f: f.write('\n'.join(sorted(USED)) + '\n')
print(od + '/score.wav', DUR, 's,', len(USED), 'samples')
