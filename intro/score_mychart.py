"""Soundtrack for the Rossen Reports MyChart-scam explainer (rossen-mychart-scam.html). Recorded samples only, no synthesis.

Music: an original 44.5 s cue sequenced from VSCO 2 Community Edition / VSCO 1 orchestral and drum samples (CC0), with the
same instruments and 96 BPM groove as the case-file intro. Foley: Kenney CC0 packs, each placed by its attack on the frame
where its picture lands. D minor while the scam plays out (bars 1-10), D major once Jeff shows the fix (bars 11-17).

Voiceover bed: Jeff narrates over this, so nothing melodic sits in the voice range. No trumpet or clarinet lines, no
viola eighths, no brass stabs on the hits (kick, timpani and bass instead); a softer snare and tambourine. Music and
foley are rendered to separate stems, with a gentle dip around 2 kHz on the music, and the mix sits at -23 LUFS so a
voice at about -16 LUFS rides clearly on top.

outputs (out/rossen-mychart-scam/): score_music.wav, score_sfx.wav, score.wav (their sum)

usage: python3 score_mychart.py [samples_dir]  ->  out/rossen-mychart-scam/score.wav
"""
import numpy as np, subprocess, wave, sys, os, re, glob, math
SR = 48000; DUR = 47.0   # 17 bars, then the closing card (4.5 s)
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


# ---------------- voiceover bed: two buses, and a pared-back arrangement ----------------
BUS = {'m': np.zeros_like(out), 'fx': np.zeros_like(out)}; CUR = ['m']
def put(x, t, gain=1.0, pan=0.0, dur=None, rel=0.08):   # as above, into the current bus
    if dur is not None:
        n = min(len(x), int((dur + rel) * SR)); x = x[:n].copy(); r = min(n, int(rel * SR)); x[n - r:] *= np.linspace(1, 0, r)[:, None]
    lg, rg = math.cos((pan + 1) * math.pi / 4) * 1.414, math.sin((pan + 1) * math.pi / 4) * 1.414
    x = x * gain * np.array([min(1, lg), min(1, rg)], np.float32); o = BUS[CUR[0]]
    i0 = int(round(t * SR))
    if i0 < 0: x = x[-i0:]; i0 = 0
    i1 = min(len(o), i0 + len(x))
    if i1 > i0: o[i0:i1] += x[: i1 - i0]
_fx = fx
def fx(name, t, g=1.0, pan=0.0, dur=None): CUR[0] = 'fx'; _fx(name, t, g, pan, dur); CUR[0] = 'm'
_none = lambda *a, **k: None
cla = tps = tbs = vla = _none                        # melodic lines out of the voice's way
_xyl = xyl; xyl = lambda n, t, v=1.0, **k: _xyl(n, t, v * .55, **k)
def snare(t, g=.5): one(SNR2, t, g * .55, .05)       # softer backbeat
def lowroot(ch): r = CH[ch][3]; return r
def stab(t, ch, g=1.0, dur=.32, bass=True):          # a hit felt in the low end, not heard as brass
    kick(t, .55 * g); cbp(lowroot(ch), t, .8 * g)
def hit(t, ch, g=1.0, crash=.5):
    kick(t, .8 * g); timp(t, .75 * g); cbp(lowroot(ch), t, .9 * g)
    if crash: one(CRASH_MF, t, crash * .6)

CHORDS = {   # one chord per beat, bar by bar (bar 0-based)
    0: 'Dm Dm Dm Dm', 1: 'Dm Dm Bb Bb', 2: 'Gm Gm A A', 3: 'Dm Dm Dm A', 4: 'Eb Eb Eb Eb', 5: 'Eb Eb Bb Bb', 6: 'Dm Dm C C',
    7: 'Dm Dm C C', 8: 'Bb Bb A A', 9: 'Dm Dm Dm A', 10: 'D D D D', 11: 'G G A A', 12: 'D D G G', 13: 'A A D D', 14: 'G G A A',
    15: 'D D G A', 16: 'D D A A'}
CROOT = {'Dm': 'D2', 'D': 'D2', 'Bb': 'Bb1', 'Gm': 'G2', 'G': 'G2', 'A': 'A1', 'Eb': 'Eb2', 'C': 'C2'}
VOX = {'Dm': ('D3', 'F3', 'A3'), 'D': ('D3', 'F#3', 'A3'), 'Bb': ('D3', 'F3', 'Bb3'), 'Gm': ('D3', 'G3', 'Bb3'), 'G': ('D3', 'G3', 'B3'),
       'A': ('C#3', 'E3', 'A3'), 'Eb': ('Eb3', 'G3', 'Bb3'), 'C': ('E3', 'G3', 'C4')}
CH['Gm'] = (['D4', 'G4', 'Bb3'], ['G1', 'D2'], ['G2', 'Bb2'], 'G1')

groove(0, BB(17), .6, .09)
for bar, row in CHORDS.items():
    for k, ch in enumerate(row.split()):
        bb = BB(bar, k + 1); r = CROOT[ch]; lo, mid, hi = VOX[ch]
        cpz(r, B(bb), .7, dur=.28); cpz(r, B(bb + .5), .6, dur=.28); cbp(r.replace('2', '1') if r[-1] == '2' else r.replace('1', '0'), B(bb), .35, dur=.3)
        vla(lo if k % 2 == 0 else mid, B(bb), .36, dur=.2); vla(hi, B(bb + .5), .32, dur=.2)
def capsnd(bar, two=True, notes=('D5', 'A5')):   # captions pop on the downbeat, second line an eighth later
    xyl(notes[0], AT(bar), .4)
    if two: xyl(notes[1], AT(bar) + E8, .36)
for bar in (4, 6, 7, 11, 12, 13, 14): downbeat(BB(bar), .16)

# ================= BAIT (bars 1-4) =================
stab(0.0, 'Dm', .65); one(CRASH_MF, 0.0, .3); capsnd(0, False)                                # the email is already there
fx('interface/glass_001.ogg', AT(0, 2), .45); glk('D6', AT(0, 2), .5)                          # 1 new message
for k, n in enumerate(('A3', 'Bb3', 'A3', 'F3')): cla(n, AT(0, 3) + k * E8, .45, dur=.2)       # a sneaky clarinet under the bait
fx('casino/card-slide-3.ogg', AT(1) - .25, .35); capsnd(1)                                     # scroll down
fx('interface/pluck_002.ogg', AT(1, 2), .35); glk('F5', AT(1, 2), .45); glk('A5', AT(1, 2.25), .45); glk('D6', AT(1, 2.5), .5)   # the gift pops
fx('casino/card-slide-3.ogg', AT(2) - .25, .35); capsnd(2, True, ('A5', 'C#6'))
for k in range(4): tt = AT(2, 1 + k); fx('interface/tick_002.ogg', tt, .55); one(CLAVE, tt, .35); fx('interface/tick_001.ogg', tt + E8, .3)   # the countdown
roll_to(AT(2, 3), AT(3), .3)
roll_to(AT(3), AT(3, 2), .45, TIMP_ROLL); swell_to(AT(3, 2), .35); fx('rpg/cloth3.ogg', AT(3), .35)  # the rising reveal
for k, n in enumerate(('A3', 'G#3', 'G3', 'F3')): cla(n, AT(3, 2) + k * S16, .55, dur=.14)     # there he is
hit(AT(3, 3), 'Dm', 1.0, .55); fx('impact/impactPunch_heavy_001.ogg', AT(3, 3), .55)           # IT'S BAIT!
fx('casino/card-slide-2.ogg', AT(3, 4), .35); swell_to(AT(4), .3)                              # dive to the button

# ================= TRAP (bars 5-7) =================
fx('interface/click_001.ogg', AT(4), .7); fx('interface/maximize_006.ogg', AT(4) + .05, .4); stab(AT(4), 'Eb', .7); capsnd(4)   # click, zoom through
fx('interface/pluck_001.ogg', AT(5), .32); capsnd(5)                                            # Jeff pops up
fx('rpg/metalClick.ogg', AT(5, 2), .35, .2); stab(AT(5, 2), 'Eb', .45, bass=False)             # magnifier on the address
fx('interface/glitch_002.ogg', AT(5, 2.5), .2)
hit(AT(5, 3), 'Bb', .95, .5); fx('impact/impactPunch_heavy_000.ogg', AT(5, 3), .5)             # FAKE!
capsnd(6)
for k, n in enumerate(('D5', 'F5', 'A5', 'D6')): tt = AT(6, 1.5 + k * .5); xyl(n, tt, .7); fx('casino/card-place-2.ogg', tt, .3, (-.2, .2)[k % 2])   # the form drops in
k = 0; tt = AT(6, 1.6)
while tt < AT(6, 4.5): fx('interface/click_003.ogg', tt, .16, .2); tt += S16; k += 1          # typing

# ================= THEFT (bars 8-10) =================
capsnd(7)
for bar in (7, 8): ostinato(AT(bar), AT(bar + 1), ['D4', 'F4', 'A4', 'F4', 'D4', 'E4', 'F4', 'E4'], vpz, .22)   # sneaky pizz
for k, ts in enumerate((AT(7, 2), AT(7, 4), AT(8, 2), AT(8, 4))):
    fx('rpg/cloth3.ogg', ts - .5, .22)                                                          # the hook drops
    fx('rpg/metalClick.ogg', ts, .5); fx('interface/drop_002.ogg', ts, .3); vpz(('D5', 'C5', 'Bb4', 'A4')[k], ts, .6, dur=.25)   # snag
    for j in range(8): fx('interface/tick_001.ogg', ts + .08 + j * S16 / 2, .3 - j * .02)      # reeled up: the ratchet
roll_to(AT(9), AT(9, 2), .4, TIMP_ROLL); swell_to(AT(9, 2), .35)                               # the camera rises to the pier
for j in range(12): fx('interface/tick_001.ogg', AT(9, 2.5) + j * S16 / 2, .32)                 # he cranks the reel
hit(AT(9, 3), 'Dm', 1.0, .6); fx('impact/impactPunch_heavy_002.ogg', AT(9, 3), .55)            # STOLEN!
for k, n in enumerate(('D3', 'C#3', 'C3', 'B2')): tbs(n, AT(9, 4) + k * S16, .6, dur=.14)      # a villain's snicker

# ================= FIX (bars 11-17), D major =================
hit(AT(10), 'D', 1.0, .6); fx('impact/impactPlank_medium_000.ogg', AT(10), .6); fx('rpg/bookPlace2.ogg', AT(10), .45); capsnd(10, True, ('D5', 'F#5'))   # the logo slams
fx('impact/impactSoft_medium_000.ogg', AT(10) + .05, .4)
for k, n in enumerate(('A4', 'F#4', 'D4', 'A3')): cla(n, AT(10) + .1 + k * S16 / 2, .5, dur=.1)   # he's knocked off
fx('casino/card-fan-1.ogg', AT(10) + .15, .3)                                                   # the loot flutters away
fx('interface/pluck_001.ogg', AT(10, 2), .3); glk('D6', AT(10, 3), .45)                         # Jeff, thumbs up
for k, n in enumerate(('D6', 'F#6', 'A6')): glk(n, AT(10, 3) + k * E8, .35)                      # a bright lift, above the voice
fx('rpg/bookPlace1.ogg', AT(11), .45); capsnd(11, True, ('D5', 'F#5'))                           # the email drops back in
fx('interface/pluck_002.ogg', AT(11, 2), .28)
hit(AT(11, 3), 'A', .95, .5); fx('impact/impactPunch_heavy_000.ogg', AT(11, 3), .5)             # X on the link
fx('casino/card-slide-3.ogg', AT(12) - .3, .35); fx('interface/open_001.ogg', AT(12), .35); capsnd(12, True, ('D5', 'A5'))   # the phone rises
fx('interface/click_001.ogg', AT(12, 3), .6); fx('interface/confirmation_001.ogg', AT(12, 3) + .05, .35); glk('A5', AT(12, 3), .4); glk('D6', AT(12, 3.25), .45)   # tap
fx('casino/card-slide-3.ogg', AT(13) - .3, .35); capsnd(13, True, ('A5', 'D6'))                   # the browser slides in
n = len("YOUR PROVIDER'S SITE"); step = (AT(13, 3) - .3 - AT(13)) / n
for j in range(n): fx('interface/click_003.ogg', AT(13) + .12 + j * step, .22, (-.15, .15)[j % 2])   # typed, letter by letter
fx('interface/confirmation_002.ogg', AT(13, 3), .4); stab(AT(13, 3), 'D', .6)                   # the real portal loads
fx('interface/maximize_002.ogg', AT(14), .4); capsnd(14, True, ('D5', 'F#5'))                     # into the inbox
fx('rpg/metalClick.ogg', AT(14, 1.5), .3)
hit(AT(14, 3), 'D', .95, .5); fx('impact/impactPunch_heavy_001.ogg', AT(14, 3), .45)            # CHECKED!
for k, n in enumerate(('D6', 'F#6', 'A6')): glk(n, AT(14, 3.5) + k * E8, .45)
hit(AT(15), 'D', 1.0, .6); fx('impact/impactPunch_heavy_002.ogg', AT(15), .55)                  # DON'T CLICK.
fx('interface/pluck_001.ogg', AT(15, 2), .3)
hit(AT(15, 3), 'G', .95, .45); fx('impact/impactPunch_heavy_000.ogg', AT(15, 3), .45)           # GO TO THE APP
hit(AT(15, 3.5), 'A', .95, .4); fx('impact/impactPunch_heavy_001.ogg', AT(15, 3.5), .45)        # YOURSELF.
for bb, n, d in [(1, 'D4', .28), (1.5, 'D4', .15), (2, 'F#4', .28), (2.5, 'D4', .15), (3, 'A4', .55)]: tps(n, AT(16, bb), .75, dur=d)
roll_to(AT(16, 4), AT(17), .4, TIMP_ROLL); swell_to(AT(17), .4); tomfill(AT(16, 4.5), AT(17), .45, S16)   # the rubber stamp comes down

# ================= the sign-off (42.5 s) =================
t = AT(17)
for n in ('D4', 'F#4', 'A4'): tpl(n, t, .95, dur=1.4, rel=.6)
for n in ('D2', 'F#2', 'A2'): hnl(n, t, .9, dur=1.4, rel=.6)
for n in ('D2', 'A1'): tbl(n, t, .85, dur=1.4, rel=.6)
cbp('D1', t, 1.0); cpz('D2', t, .9); timp(t, 1.0); kick(t, 1.0); one(CRASH, t, .6); glk('D6', t, .55)
fx('impact/impactPlank_medium_000.ogg', t, .5); fx('impact/impactSoft_heavy_000.ogg', t, .4)

# ---------------- under the closing card: a soft held D major, so the longer card never sits in silence ----------------
_t0 = AT(17) + 1.2
if True:
    for n in ('D2', 'F#2', 'A2'): hnl(n, _t0, .3, dur=DUR - _t0 - .4, rel=1.0)
    cpz('D2', _t0, .3)

# ---------------- master ----------------
FXG = .8   # foley a little under the music
mix = BUS['m'] + BUS['fx'] * FXG
fade = int(1.0 * SR); ramp = np.linspace(1, 0, fade)[:, None] ** 2
for x in (BUS['m'], BUS['fx'], mix): x[-fade:] *= ramp
peak = np.abs(np.tanh(mix * 1.1) / 1.1).max()
od = 'out/rossen-mychart-scam'; os.makedirs(od, exist_ok=True)
def wav(path, x):
    x = x * (10 ** (-1 / 20)) / max(1e-6, peak)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1) * 32767).astype('<i2').tobytes())
wav(od + '/score_music.wav', BUS['m']); wav(od + '/score_sfx.wav', BUS['fx'] * FXG); wav(od + '/score.wav', mix)   # stems sum to the mix
with open(od + '/samples_used.txt', 'w') as f: f.write('\n'.join(sorted(USED)) + '\n')
print(od + '/score.wav', DUR, 's,', len(USED), 'samples')
