"""(v2, sampler order) Score for the transition-1 look test (2 bars at 96 BPM, 5.0 s). One groove across the cut: the careers bar is dry and
wry (walking contrabass pizzicato, claves on 2 and 4, a clarinet shrug for Raj's nod); on the downbeat where the page
turns riso it opens up, bright and bouncy (cello pizzicato octaves, violin pizzicato offbeat chords, xylophone, glock,
tambourine and kick). Every hit is placed by its audible attack (half-rise), the way sync is measured.
Recorded samples only: VSCO 2 CE (CC0) and Kenney (CC0), copied into audio/ (the reel's own copies; see audio_sources.txt). The glock shimmer under the dissolve
is composed (arranged from the recorded glockenspiel notes), not a recording of a shimmer.
usage: python3 tools/score_t1b.py  ->  _check/t1b/score.wav, hits.json, samples_used.txt, audio_sources.txt"""
import numpy as np, subprocess, wave, os, re, glob, math, json
SR = 48000
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
ROOT = os.path.join(HERE, 'audio')
OUT = os.path.join(HERE, '_check', 't1b')
BPM, BEAT = 96, 60 / 96; BAR = 4 * BEAT; E8, S16 = BEAT / 2, BEAT / 4
at = lambda bar, beat=1: bar * BAR + (beat - 1) * BEAT
DUR = 2 * BAR
out = np.zeros((int(SR * (DUR + 1.5)), 2), np.float32)
_cache, USED, HITS = {}, set(), []
def H(t, what): HITS.append((round(t, 4), what))
def load(rel):
    if rel not in _cache:
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', os.path.join(ROOT, rel), '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
        x = np.frombuffer(raw, np.float32).reshape(-1, 2).copy(); i0 = int(np.argmax(np.abs(x).max(1) > 0.003)); _cache[rel] = x[max(0, i0 - 48):]
    return _cache[rel]
def attack(x):   # seconds from the start of x to its audible attack: the half-rise of its main peak (as sync_check.py measures)
    e = np.abs(x).max(1); n = len(e) // 48 * 48; e = e[:n].reshape(-1, 48).max(1)[:400]; p = e.max(); return int(np.argmax(e >= .5 * p)) / 1000
def lead_trim(x, keep=.012):   # drop a quiet lead-in before the attack (with a short fade), so nothing is heard early
    a = attack(x); i = int(max(0, a - keep) * SR)
    if i <= 0: return x
    y = x[i:].copy(); f = min(len(y), int(.004 * SR)); y[:f] *= np.linspace(0, 1, f)[:, None]; return y
def put(x, t, gain=1.0, pan=0.0, dur=None, rel=0.08, sync=True):
    if dur is not None:
        n = min(len(x), int((dur + rel) * SR)); x = x[:n].copy(); r = min(n, int(rel * SR)); x[n - r:] *= np.linspace(1, 0, r)[:, None]
    if sync: t -= attack(x)
    lg, rg = math.cos((pan + 1) * math.pi / 4) * 1.414, math.sin((pan + 1) * math.pi / 4) * 1.414
    x = x * gain * np.array([min(1, lg), min(1, rg)], np.float32); i0 = int(round(t * SR))
    if i0 < 0: x = x[-i0:]; i0 = 0
    i1 = min(len(out), i0 + len(x)); out[i0:i1] += x[: i1 - i0]
NAMES = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}
def midi(n): m = re.match(r'([A-G][#b]?)(-?\d)', n); return NAMES[m.group(1)] + 12 * (int(m.group(2)) + 1)
class Inst:
    """pattern: a glob under ROOT with the note name as the only varying token. Note names follow each library's own file
    names; the nearest sample is repitched (resampled), preferring to repitch down."""
    def __init__(self, pattern, pan=0.0, gain=1.0):
        self.map = {}; pre, post = pattern.split('*')
        for f in glob.glob(os.path.join(ROOT, pattern)):
            rel = os.path.relpath(f, ROOT); tok = rel[len(pre):len(rel) - len(post)]
            if re.fullmatch(r'[A-G][#b]?-?\d', tok): self.map[midi(tok)] = rel
        assert self.map, pattern; self.pan, self.gain = pan, gain
    def __call__(self, note, t, vel=1.0, dur=None, rel=0.08, pan=None):
        m = midi(note) if isinstance(note, str) else note; k = min(self.map, key=lambda s: (abs(s - m), s < m)); x = load(self.map[k]); USED.add(self.map[k])
        if k != m:
            ratio = 2 ** ((m - k) / 12); n = int(len(x) / ratio); src = np.arange(n) * ratio
            x = np.stack([np.interp(src, np.arange(len(x)), x[:, c]) for c in (0, 1)], 1).astype(np.float32)
        put(x, t, vel * self.gain, self.pan if pan is None else pan, dur, rel)
def one(rel, t, gain=1.0, pan=0.0, dur=None, relz=0.08, sync=True): USED.add(rel); put(lead_trim(load(rel)) if sync else load(rel), t, gain, pan, dur, relz, sync)

V, KC, KR, KI = 'vsco/', 'kenney/casino/', 'kenney/rpg/', 'kenney/impact/'
cbp = Inst(V + 'Strings/Solo Contrabass/Pizz/BKCtbss_Pizz_*_v1_rr1.wav', pan=.05, gain=1.1)
cpz = Inst(V + 'Strings/Cello Section/pizzT/pizzT_*_v2_RR1.wav', pan=.15, gain=1.0)
vpz = Inst(V + 'Strings/Violin Section/Pizz/VlnEns_Pizz_*_v2_rr1.wav', pan=-.3, gain=.62)
clar = Inst(V + 'Woodwinds/Clarinet/stac/DCClar_stac_*_v3_rr1_sum.wav', pan=.25, gain=.55)
xylo = Inst(V + 'Percussion/Xylo/Xylo_Medium_*_ff_01_far.wav', pan=-.1, gain=.42)
glock = Inst(V + 'Percussion/Glock/glock_medium_*.wav', pan=.2, gain=.26)
KICK, CLAVE, TAMB, TAMB2 = V + 'Percussion/BDrumNewhit_v6_rr1_Sum.wav', V + 'Percussion/Claves1_Hit_v2_rr1_Sum.wav', V + 'Percussion/Tamb1-Hit_v1_rr1_Sum.wav', V + 'Percussion/Tamb1-Hit_v2_rr1_Sum.wav'
T_LAND, T_NOD, T_FLY, T_F1, T_F2, T_CATCH, T_TITLE, T_MAYA = at(0, 2), at(0, 3), 2.19, at(1, 1), at(1, 1) + E8, at(1, 2), at(1, 3), at(1, 4)

T_HOP, T_LIFT, T_FILL, T_LAND, T_TITLE = at(0, 2), at(0, 4), at(1), at(1, 2), at(1, 2) + E8
# ---- bar 0, the end of MONEY RULES: bright and bouncy
for b in (1, 3): one(KICK, at(0, b), .75)
for k in range(4): one(TAMB if k % 2 else TAMB2, at(0, 1 + k) + E8, .28, pan=-.35)
for k, n in enumerate(['F1', 'F2', 'C2', 'F2', 'A1', 'C2', 'E1', 'G1']): cpz(n, at(0) + k * E8, .85, dur=.22, rel=.1)
for k in range(4): [vpz(n, at(0, 1 + k) + E8, .4, dur=.18) for n in ('C4', 'F4', 'A4')]
one(KI + 'footstep_wood_000.ogg', T_HOP, .45, pan=-.3); xylo('C6', T_HOP, .6, dur=.4); H(T_HOP, 'Maya hops')
one(KC + 'card-slide-2.ogg', T_LIFT, .55, pan=.1); xylo('G5', T_LIFT, .55, dur=.3); H(T_LIFT, 'paycheck lifts off')
one(KC + 'card-fan-1.ogg', 2.06, .3, pan=.1, dur=.2, relz=.05, sync=False)   # the tumble
for k, n in enumerate(['C5', 'G5', 'C6', 'G5', 'C6', 'G6', 'C6', 'G6']): glock(n, 2.44 + k * S16 * .8, .45 + k * .05, dur=.5)   # composed shimmer under the dissolve
# ---- bar 1, the start of RED FLAG OR GREEN FLAG?: dry and wry (the same groove, new instruments)
one(KR + 'bookFlip2.ogg', T_FILL, .7); cbp('D1', T_FILL, 1.05, dur=BEAT * .8, rel=.12); H(T_FILL, 'paper fills the frame (downbeat)')
for k, n in enumerate(['F1', 'A1', 'C2']): cbp(n, at(1, 2 + k), .95, dur=BEAT * .8, rel=.12)
for b in (2, 4): one(CLAVE, at(1, b), .3, pan=.3)
one(KC + 'card-place-1.ogg', T_LAND, .7, pan=.2); vpz('D4', T_LAND, .45, dur=.25); H(T_LAND, 'posting lands')
one(KC + 'card-place-2.ogg', T_TITLE, .55, pan=.1); [vpz(n, T_TITLE, .5, dur=.3) for n in ('D4', 'F4', 'A4')]; H(T_TITLE, 'RED FLAG OR GREEN FLAG?')
clar('A3', at(1, 4), .55, dur=.16); clar('F3', at(1, 4) + E8, .45, dur=.18)
cbp('D1', at(2), .7, dur=.5)
x = out[:int(SR * DUR)]; x = x / max(1e-6, np.abs(x).max()) * .7
os.makedirs(OUT, exist_ok=True)
with wave.open(os.path.join(OUT, 'score_raw.wav'), 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1) * 32767).astype('<i2').tobytes())
raw = os.path.join(OUT, 'score_raw.wav')   # loudness in two passes (one fixed gain, no ramp); the limiter's lookahead compensated
meas = subprocess.run(['ffmpeg', '-hide_banner', '-i', raw, '-af', 'loudnorm=I=-16:TP=-2:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
m = json.loads(meas[meas.rindex('{'):meas.rindex('}') + 1])
ln = f"loudnorm=I=-16:TP=-2:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', raw, '-af', ln + ',aresample=48000,alimiter=limit=0.7:level=false:latency=true', '-ar', '48000', os.path.join(OUT, 'score.wav')], check=True)
json.dump(sorted(set(HITS)), open(os.path.join(OUT, 'hits.json'), 'w'))
open(os.path.join(OUT, 'samples_used.txt'), 'w').write('\n'.join(sorted(USED)) + '\n')
SRC = {'vsco/': ('https://github.com/sgossner/VSCO-2-CE', 'Versilian Studios Chamber Orchestra 2 Community Edition'), 'kenney/casino/': ('https://kenney.nl/assets/casino-audio', 'Kenney, kenney.nl'),
       'kenney/rpg/': ('https://kenney.nl/assets/rpg-audio', 'Kenney, kenney.nl'), 'kenney/impact/': ('https://kenney.nl/assets/impact-sounds', 'Kenney, kenney.nl'), 'kenney/interface/': ('https://kenney.nl/assets/interface-sounds', 'Kenney, kenney.nl')}
with open(os.path.join(OUT, 'audio_sources.txt'), 'w') as f:
    f.write('TRANSITION 1 LOOK TEST (v2): every recorded audio file in the mix, with its source and license.\n'
            'All are CC0 1.0 (public domain dedication, commercial use allowed, no attribution required). None come from a music library that registers with Content ID.\n'
            'The reel keeps its own copies in audio/ (with the libraries\' license files).\n\n')
    for u in sorted(USED):
        url, who = next(v for k, v in SRC.items() if u.startswith(k)); f.write(f'{u}\n    source: {url}  ({who})\n    license: CC0 1.0\n')
    f.write('\nComposed (not recorded files): the whole score, written note by note in tools/score_t1b.py on the 96 BPM grid and played by the '
            'recordings above: the walking bass, the clarinet shrug, the pizzicato and xylophone parts, and the glockenspiel shimmer under the '
            'dissolve (eight recorded glock notes arranged as a rising sixteenth-note run). No synthesized tones are used anywhere.\n')
print(len(USED), 'samples;', len(HITS), 'synced hits ->', OUT)
