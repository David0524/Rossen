"""The demo reel's score and foley: one continuous 96 BPM groove whose instrumentation changes with each chapter and
builds a little, so travel lands as the payoff. Every cue is read from the film's own cue sheet (out/reel/timeline.json,
written by render.mjs), so picture and sound can't drift apart. Hits are placed by their audible attack (half-rise),
the way sync is measured.
  open          a slam (kick, timpani, low pizzicato), the page flip
  careers       dry and wry: walking contrabass pizzicato, claves on 2 and 4, violin plucks, a clarinet shrug
  finance       bright and bouncy: cello pizzicato octaves, violin pizzicato offbeat chords, xylophone, glockenspiel,
                tambourine, kick on 1 and 3
  productivity  calm and spacious: soft upright piano, a soft pizzicato pulse; pencil on paper
  travel        upbeat and driving: kick on every beat, snare on 2 and 4, tambourine eighths, driving pizzicato and
                spiccato strings, brass stabs, timpani
  lineup, end   the groove settles; horns and piano; the last chord rings out
The hard cut at the productivity downbeat cuts the audio too: nothing sounding before it carries past it.
Recorded samples only (no synthesis): VSCO 2 CE, Kenney, FreePats Upright Piano KW and OpenGameArt recordings, all CC0.
usage: python3 tools/score.py [out/reel]  ->  score.wav, hits.json, samples_used.txt, audio_sources.txt in that folder"""
import numpy as np, subprocess, wave, os, re, glob, math, json, sys, shutil
SR = 48000
HERE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
ROOT = os.path.join(HERE, 'audio'); LIB = os.path.normpath(os.path.join(HERE, '..', 'intro', 'audio'))   # LIB: where the generic CC0 libraries were first downloaded
OUT = os.path.join(HERE, sys.argv[1] if len(sys.argv) > 1 else 'out/reel')
TL = json.load(open(os.path.join(OUT, 'timeline.json'))); T = TL['T']; DUR = TL['dur']
BPM, BEAT = TL['bpm'], 60 / TL['bpm']; BAR = 4 * BEAT; E8, S16 = BEAT / 2, BEAT / 4
bt = lambda bar, beat=1: bar * BAR + (beat - 1) * BEAT
CUT = T['cut']   # the hard cut: sound stops here, and the next chapter starts here
out = np.zeros((int(SR * (DUR + 2)), 2), np.float32)
_cache, USED, HITS = {}, set(), []
def H(t, what): HITS.append((round(t, 4), what))
def path(rel):   # the reel's own copy of each file (copied from the library download on first use)
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p):
        src = os.path.join(LIB, rel); assert os.path.exists(src), rel; os.makedirs(os.path.dirname(p), exist_ok=True); shutil.copy2(src, p)
    return p
def load(rel):
    if rel not in _cache:
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path(rel), '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
        x = np.frombuffer(raw, np.float32).reshape(-1, 2).copy(); i0 = int(np.argmax(np.abs(x).max(1) > 0.003)); _cache[rel] = x[max(0, i0 - 48):]
    return _cache[rel]
def attack(x):   # seconds from the start of x to its audible attack: the half-rise of its main peak (as sync_check.py measures)
    e = np.abs(x).max(1); n = len(e) // 48 * 48; e = e[:n].reshape(-1, 48).max(1)[:400]; p = e.max(); return int(np.argmax(e >= .5 * p)) / 1000
def lead_trim(x, keep=.012):   # drop a quiet lead-in before the attack (with a short fade), so nothing is heard early
    a = attack(x); i = int(max(0, a - keep) * SR)
    if i <= 0: return x
    y = x[i:].copy(); f = min(len(y), int(.004 * SR)); y[:f] *= np.linspace(0, 1, f)[:, None]; return y
def put(x, t, gain=1.0, pan=0.0, dur=None, rel=0.08, sync=True, seg=None):
    if seg:   # an excerpt of a longer recording: (start s, length s)
        a, b = int(seg[0] * SR), int((seg[0] + seg[1]) * SR); x = x[a:b].copy(); f = min(len(x), int(.01 * SR)); x[:f] *= np.linspace(0, 1, f)[:, None]; x[-f:] *= np.linspace(1, 0, f)[:, None]
    if dur is not None:
        n = min(len(x), int((dur + rel) * SR)); x = x[:n].copy(); r = min(n, int(rel * SR)); x[n - r:] *= np.linspace(1, 0, r)[:, None]
    if sync: t -= attack(x)
    if t < CUT and t + len(x) / SR > CUT:   # the hard cut: nothing carries across it
        n = max(1, int((CUT - t) * SR)); x = x[:n].copy(); f = min(n, int(.004 * SR)); x[n - f:] *= np.linspace(1, 0, f)[:, None]
    lg, rg = math.cos((pan + 1) * math.pi / 4) * 1.414, math.sin((pan + 1) * math.pi / 4) * 1.414
    x = x * gain * np.array([min(1, lg), min(1, rg)], np.float32); i0 = int(round(t * SR))
    if i0 < 0: x = x[-i0:]; i0 = 0
    i1 = min(len(out), i0 + len(x)); out[i0:i1] += x[: i1 - i0]
NAMES = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}
def midi(n): m = re.match(r'([A-G][#b]?)(-?\d)', n); return NAMES[m.group(1)] + 12 * (int(m.group(2)) + 1)
class Inst:
    """pattern: a glob with the note name as the only varying token. Note names follow each library's own file names;
    the nearest sample is repitched (resampled), preferring to repitch down."""
    def __init__(self, pattern, pan=0.0, gain=1.0, lib=True):
        self.map = {}; pre, post = pattern.split('*'); base = LIB if lib else ROOT
        for f in glob.glob(os.path.join(base, pattern)):
            rel = os.path.relpath(f, base); tok = rel[len(pre):len(rel) - len(post)]
            if re.fullmatch(r'[A-G][#b]?-?\d', tok): self.map[midi(tok)] = rel
        assert self.map, pattern; self.pan, self.gain = pan, gain
    def __call__(self, note, t, vel=1.0, dur=None, rel=0.08, pan=None, sync=True):
        m = midi(note) if isinstance(note, str) else note; k = min(self.map, key=lambda s: (abs(s - m), s < m)); x = load(self.map[k]); USED.add(self.map[k])
        if k != m:
            ratio = 2 ** ((m - k) / 12); n = int(len(x) / ratio); src = np.arange(n) * ratio
            x = np.stack([np.interp(src, np.arange(len(x)), x[:, c]) for c in (0, 1)], 1).astype(np.float32)
        put(x, t, vel * self.gain, self.pan if pan is None else pan, dur, rel, sync)
def one(rel, t, gain=1.0, pan=0.0, dur=None, relz=0.08, sync=True, seg=None):
    USED.add(rel); x = load(rel); put(lead_trim(x) if sync and not seg else x, t, gain, pan, dur, relz, sync, seg)
def chord(inst, notes, t, vel=1.0, dur=None, spread=0.0, rel=.1):
    for k, n in enumerate(notes): inst(n, t + k * spread, vel, dur=dur, rel=rel)

V, KC, KR, KI, OG = 'vsco/', 'kenney/casino/', 'kenney/rpg/', 'kenney/impact/', 'opengameart/'
cbp = Inst(V + 'Strings/Solo Contrabass/Pizz/BKCtbss_Pizz_*_v1_rr1.wav', pan=.05, gain=1.1)
cpz = Inst(V + 'Strings/Cello Section/pizzT/pizzT_*_v2_RR1.wav', pan=.15, gain=1.0)
vpz = Inst(V + 'Strings/Violin Section/Pizz/VlnEns_Pizz_*_v2_rr1.wav', pan=-.3, gain=.6)
vsp = Inst(V + 'Strings/Violin Section/Spic/VlnEns_Spic_*_v2_rr1.wav', pan=-.35, gain=.42)
vla = Inst(V + 'Strings/Viola Section/spic/Violas_spic_*_v2_rr1.wav', pan=.3, gain=.4)
clar = Inst(V + 'Woodwinds/Clarinet/stac/DCClar_stac_*_v3_rr1_sum.wav', pan=.25, gain=.55)
tps = Inst(V + 'Brass/Trumpet/stac/Sum_SHTrumpet_stac_*_v3_rr1.wav', pan=-.15, gain=.5)
hns = Inst(V + 'Brass/F Horn/stac/MOHorn_stac_*_v2_rr1.wav', pan=.25, gain=.62)
hnl = Inst(V + 'Brass/F Horn/sus/MOHorn_sus_*_v1_1.wav', pan=.2, gain=.42)
tbs = Inst(V + 'Brass/Tenor Trombone/stac/tenortbn_stac_*_v3_rr1.wav', pan=.1, gain=.55)
tbl = Inst(V + 'Brass/Tenor Trombone/sus/tenortbn_sus_*_v2_1.wav', pan=.1, gain=.5)
xylo = Inst(V + 'Percussion/Xylo/Xylo_Medium_*_ff_01_far.wav', pan=-.1, gain=.42)
glock = Inst(V + 'Percussion/Glock/glock_medium_*.wav', pan=.2, gain=.26)
piano = Inst('freepats/UprightPianoKW/*vL.flac', pan=0, gain=.55, lib=False)
KICK, CLAVE, TAMB, TAMB2 = V + 'Percussion/BDrumNewhit_v6_rr1_Sum.wav', V + 'Percussion/Claves1_Hit_v2_rr1_Sum.wav', V + 'Percussion/Tamb1-Hit_v1_rr1_Sum.wav', V + 'Percussion/Tamb1-Hit_v2_rr1_Sum.wav'
SNARE, TIMP, CRASH, TRI = V + 'VSCO 1 Percussion/drums/snare/drum2/snare2_mf_1.wav', V + 'Percussion/Timpani/Timpani4_Hit_v4_rr1_Sum.wav', V + 'Percussion/cymbal-crash1_mf_rr1.wav', V + 'Percussion/Triangle3-Hit_v2_rr1_Sum.wav'
RIP, ZIP, PENCIL, TAPE = OG + 'luckius/paper_ripped_1.wav', OG + 'antumdeluge/zipper_1.wav', OG + 'antumdeluge/pencil_write.flac', OG + 'owlishmedia/stationery_07.wav'
def slap(t, g=1.0, pan=0.0, what=None):   # a sticker slapped down: a flat card slap over a soft body thump
    one(KC + 'card-place-2.ogg', t, .7 * g, pan); one(KI + 'impactSoft_medium_000.ogg', t, .45 * g, pan)
    if what: H(t, what)
def stamp(t, g=1.0, pan=0.0, what=None):   # a rubber stamp: a wooden thump and the paper under it
    one(KI + 'impactPlank_medium_000.ogg', t, .6 * g, pan); one(KC + 'card-place-3.ogg', t, .45 * g, pan)
    if what: H(t, what)

# ======================= OPEN (bar 0) =======================
one(KC + 'card-place-2.ogg', 0, 1.0); one(KICK, .03, .45, sync=False); one(TIMP, .06, .35, sync=False); cbp('F1', .02, .55, dur=.5, sync=False); chord(vpz, ['C4', 'F4', 'A4'], 0, .4, dur=.3); H(0, 'YOUR FIRST BIG WIN')
glock('C6', bt(0, 2), .5, dur=.6); one(CLAVE, bt(0, 2), .25, .3); one(CLAVE, bt(0, 4), .25, .3); cbp('C2', bt(0, 3), .8, dur=.4)
one(KR + 'bookFlip2.ogg', T['flip'][1], .7, .1); cbp('E1', T['flip'][1], .9, dur=.4); vpz('A3', T['flip'][1], .45, dur=.25); H(T['flip'][1], 'page flipped')

# ======================= CAREERS (bars 1-3): dry and wry =======================
walk = {1: ['D1', 'F1', 'A1', 'C2'], 2: ['A#0', 'D1', 'F1', 'A1'], 3: ['G1', 'A#1', 'A1', 'E1']}
for b, notes in walk.items():
    for k, n in enumerate(notes): cbp(n, bt(b, 1 + k), .95 if k else 1.05, dur=BEAT * .8, rel=.12)
    for k in (2, 4): one(CLAVE, bt(b, k), .3, .3)
chord(vpz, ['D4', 'F4', 'A4'], T['cTitle'], .55, dur=.3); one(KC + 'card-place-2.ogg', T['cTitle'], .55, .1); H(T['cTitle'], 'RED FLAG OR GREEN FLAG?')
clar('D4', bt(1, 3) + E8, .5, dur=.14); clar('A3', bt(1, 4), .45, dur=.16)
one(KC + 'card-place-1.ogg', T['aLand'], .7, .2); vpz('F4', T['aLand'], .5, dur=.25); H(T['aLand'], 'posting A lands')
one(KR + 'cloth1.ogg', T['redUp'] - .32, .3, -.3, sync=False, dur=.2); clar('A#3', T['redUp'], .7, dur=.18); clar('A3', T['redUp'] + E8, .55, dur=.2); H(T['redUp'], 'red flag up')
stamp(T['redStamp'], 1, .1, 'RED FLAG stamp'); cbp('A#0', T['redStamp'], .7, dur=.3)
one(KC + 'card-slide-1.ogg', T['aOut'][0], .45, -.2); H(T['aOut'][0], 'posting A flicked away')
one(KC + 'card-place-1.ogg', T['bLand'], .7, .2); vpz('D4', T['bLand'], .5, dur=.25); H(T['bLand'], 'posting B lands')
one(KR + 'cloth2.ogg', T['green'] - .32, .3, -.3, sync=False, dur=.2); stamp(T['green'], 1, .1, 'GREEN FLAG stamp'); chord(vpz, ['G4', 'B4', 'D5'], T['green'], .45, dur=.3)
one(KR + 'metalClick.ogg', T['apply'], .55, .25); vpz('D5', T['apply'], .4, dur=.2); H(T['apply'], 'APPLY pressed')
one(KC + 'card-fan-1.ogg', T['spin'][0], .3, .15, sync=False, dur=.16, relz=.04)
glock('C6', T['spin'][1], .55, dur=.6); chord(vpz, ['A3', 'C#4', 'E4'], T['spin'][1], .5, dur=.3); H(T['spin'][1], 'YOU GOT THE JOB.')
clar('A3', T['nod'], .75, dur=.16); clar('F3', T['nod'] + E8, .6, dur=.18); H(T['nod'], 'Raj nods')
one(KC + 'card-slide-2.ogg', T['fly'], .5, .1); H(T['fly'], 'letter lifts')
for k, n in enumerate(['C5', 'G5', 'C6', 'G5', 'C6', 'G6', 'C6', 'G6']): glock(n, T['sc'][0] + k * S16 * .8, .5 + k * .06, dur=.5, sync=False)   # the shimmer under the dissolve

# ======================= FINANCE (bars 4-6): bright and bouncy =======================
f1 = T['f1']
for b in (4, 5, 6):
    for k in (1, 3): one(KICK, bt(b, k), .8)
    for k in range(4): one(TAMB if k % 2 else TAMB2, bt(b, 1 + k) + E8, .28, -.35)
bass = {4: ['F1', 'F2', 'C2', 'F2', 'A1', 'C2', 'F1', 'A1'], 5: ['A#1', 'D2', 'F2', 'D2', 'C2', 'E2', 'G2', 'E2'], 6: ['F1', 'F2', 'C2', 'A1', 'C2', 'E2', 'G2', 'A#2']}
offb = {4: [['C4', 'F4', 'A4']] * 4, 5: [['D4', 'F4', 'A#4']] * 2 + [['E4', 'G4', 'C5']] * 2, 6: [['C4', 'F4', 'A4']] * 2 + [['E4', 'G4', 'A#4']] * 2}
for b in (4, 5, 6):
    for k, n in enumerate(bass[b]): cpz(n, bt(b) + k * E8, .85, dur=.22, rel=.1)
    for k, ch in enumerate(offb[b]): chord(vpz, ch, bt(b, 1 + k) + E8, .4, dur=.18)
one(KC + 'card-place-2.ogg', T['f1'], .7, -.1); H(T['f1'], 'fold 1 (downbeat)')
one(KC + 'card-place-3.ogg', T['f2'], .6, .1); H(T['f2'], 'fold 2')
one(KR + 'handleCoins2.ogg', T['catch_'], .55, .25); one(KC + 'card-place-1.ogg', T['catch_'], .55, .2); xylo('C6', T['catch_'], .8, dur=.5); H(T['catch_'], 'paycheck caught')
xylo('F5', T['fTitle'], .85, dur=.4); xylo('A5', T['fTitle'] + S16, .7, dur=.4, sync=False); xylo('C6', T['fTitle'] + 2 * S16, .75, dur=.6, sync=False); one(TAMB, T['fTitle'], .35, -.3); H(T['fTitle'], 'MONEY RULE #1')
for k, n in enumerate(['C4', 'E4', 'G4']): vpz(n, T['maya'] - .2 + k * .06, .35, dur=.12, sync=False)
one(KICK, T['maya'], .55); one(KI + 'footstep_wood_000.ogg', T['maya'], .5, -.3); xylo('G5', T['maya'], .6, dur=.3); xylo('C6', T['maya'] + E8, .6, dur=.6, sync=False); H(T['maya'], 'Maya lands')
one(KC + 'card-slide-3.ogg', T['swing'][0], .3, .2, sync=False)
one(RIP, T['tear'], .9, -.1); H(T['tear'], 'the paycheck tears')
one(KR + 'handleCoins2.ogg', T['chunkIn'], .6, -.35); glock('G6', T['chunkIn'], .6, dur=.5); H(T['chunkIn'], 'chunk into the piggy bank')
xylo('C6', T['fCap'], .8, dur=.5); xylo('F6', T['fCap'] + S16, .6, dur=.5, sync=False); H(T['fCap'], 'PAY YOURSELF FIRST.')
one(KC + 'card-place-3.ogg', T['drop'], .6, .2); one(KI + 'impactSoft_medium_000.ogg', T['drop'], .35, .2); H(T['drop'], 'the rest lands on the spend pile')
for k, tc in enumerate(T['coins']): one(KR + 'handleCoins2.ogg', tc, .45 + .05 * k, -.35); glock(['C5', 'G5', 'C6', 'G6'][k], tc, .5, dur=.4); H(tc, f'coin {k + 1} in')
xylo('A5', T['label'], .8, dur=.4); xylo('C6', T['label'] + S16, .7, dur=.6, sync=False); one(TAMB, T['label'], .35, -.3); chord(vpz, ['C4', 'F4', 'A4'], T['label'], .4, dur=.25); H(T['label'], 'TRIP FUND')

# ======================= PRODUCTIVITY (bars 7-9): calm, spacious, soft piano =======================
cut = CUT
chords = {7: ('F2', ['F3', 'A3', 'C4', 'E4']), 8: ('D2', ['F3', 'A3', 'C4', 'E4']), 9: ('A#1', ['D3', 'F3', 'A3', 'C4'])}
for b, (root, ch) in chords.items():
    piano(root, bt(b), .6, dur=2.2, rel=.4); chord(piano, ch, bt(b), .36, dur=2.2, rel=.4)
    arp = [ch[0], ch[2], ch[1], ch[3], ch[2], ch[0], ch[1], ch[2]]
    for k, n in enumerate(arp):
        if k: piano(n, bt(b) + k * E8, .13, dur=.45, rel=.3, sync=False)
    for k in (1, 3): cpz({'F2': 'F1', 'D2': 'D1', 'A#1': 'A#1'}[root], bt(b, k), .45, dur=.3)   # a soft pulse keeps the groove
H(cut, 'hard cut (downbeat)')
piano('E5', T['pTitle'], .6, dur=1.2, rel=.4); one(PENCIL, T['pTitle'] + .05, .5, .1, sync=False, seg=(.1, .4)); H(T['pTitle'], 'ONE HABIT')
H(T['pCap'], 'the two-minute rule')
one(PENCIL, T['listDraw'][0], .45, .15, sync=False, seg=(.0, .8))   # the list drawing itself
for k, tc in enumerate(T['checks']): one(PENCIL, tc - .13, .25, .2, sync=False, seg=(.55 + .1 * k, .07)); one(KC + 'card-place-3.ogg', tc, .22, .2, dur=.06); piano(['C5', 'D5', 'E5', 'F5', 'G5'][k], tc, .85, dur=.8, rel=.3); H(tc, f'check {k + 1}')
piano('A4', T['last'], .55, dur=1, rel=.4); piano('C5', T['last'] + E8, .5, dur=1.2, rel=.4, sync=False); H(T['last'], 'BOOK THE TRIP')
piano('D5', T['hNod'], .35, dur=.8, rel=.3); piano('C4', bt(9, 3), .3, dur=1, rel=.4); piano('G3', bt(9, 3), .3, dur=1, rel=.4, sync=False)
one(RIP, T['rip'], 1.0, -.2); H(T['rip'], 'Hana tears the page')
one(TAPE, T['peel'][0], .75, .1, sync=False)   # the page peels away like a sticker backing
for k, n in enumerate(['C5', 'G5', 'C6', 'G6']): glock(n, T['peel'][0] + k * .12, .25 + .05 * k, dur=.4, sync=False)   # a rising run as the page lifts

# ======================= TRAVEL (bars 10-12): upbeat, driving, the payoff =======================
for b in (10, 11, 12):
    for k in range(1, 5): one(KICK, bt(b, k), .85 if k in (1, 3) else .7)
    for k in (2, 4): one(SNARE, bt(b, k), .55, .05)
    for k in range(8): one(TAMB if k % 2 else TAMB2, bt(b) + k * E8, .3 if k % 2 else .2, -.35)
tbass = {10: ['F1', 'F1', 'F2', 'F1', 'C2', 'C2', 'A1', 'C2'], 11: ['A#1', 'A#1', 'D2', 'A#1', 'C2', 'C2', 'E2', 'C2'], 12: ['F1', 'F1', 'A1', 'C2', 'C2', 'E2', 'G2', 'E2']}
tstr = {10: ['C4', 'F4', 'A4', 'F4'], 11: ['D4', 'F4', 'C4', 'E4'], 12: ['C4', 'F4', 'E4', 'G4']}
for b in (10, 11, 12):
    for k, n in enumerate(tbass[b]): cpz(n, bt(b) + k * E8, .9, dur=.2, rel=.08)
    for k in range(8): vsp(tstr[b][k // 2], bt(b) + k * E8, .5 if k % 2 == 0 else .35, dur=.14, sync=k == 0)
one(CRASH, T['dPop'], .5, .1); one(TIMP, T['dPop'], .6); chord(hns, ['F2', 'A2'], T['dPop'], .7, dur=.3); chord(tps, ['A#3', 'F4'], T['dPop'], .55, dur=.25); H(T['dPop'], "Diego's world (downbeat)")
slap(T['vTitle'], 1, .1, 'PACK OR PASS?'); chord(tps, ['F4', 'A4'], T['vTitle'], .5, dur=.2)
one(KR + 'cloth3.ogg', T['handIn2'][0], .4, .3, sync=False)
slap(T['q'], 1, 0, 'the question lands'); chord(hns, ['A#1', 'D2'], T['q'], .55, dur=.3)
tbl('D2', T['uhoh'], .75, dur=.28, rel=.1); tbl('C#2', T['uhoh'] + .3, .7, dur=.45, rel=.2, sync=False); one(KC + 'card-place-3.ogg', T['uhoh'], .35, -.3); H(T['uhoh'], 'uh-oh')
slap(T['pass'], 1.3, .2, 'PASS'); one(TIMP, T['pass'], .45); chord(tps, ['G3', 'D4', 'A#3'], T['pass'], .6, dur=.2); chord(tbs, ['D3'], T['pass'], .5, dur=.2)
one(KR + 'cloth4.ogg', T['move'] - .2, .45, 0, sync=False); one(KI + 'impactSoft_medium_000.ogg', T['move'] + .17, .45, -.1); H(T['move'], 'into the carry-on')
slap(T['vCap'], 1, 0, 'SPARE BATTERIES GO IN YOUR CARRY-ON.'); chord(hns, ['F2', 'C2'], T['vCap'], .55, dur=.3); chord(tps, ['A4', 'F4'], T['vCap'], .45, dur=.2)
one(ZIP, T['zip'] - .16, .8, -.1, sync=False); one(KR + 'metalClick.ogg', T['zip'], .4, -.1); H(T['zip'], 'the bag zipped')
one(KI + 'footstep_wood_000.ogg', T['hop'], .5, -.3); xylo('C6', T['hop'], .6, dur=.4); chord(tps, ['F4', 'A4'], T['hop'], .45, dur=.2); H(T['hop'], 'Diego hops')

# ======================= LINEUP (bar 13) and END CARD (bars 14-15) =======================
for k in (1, 3): one(KICK, bt(13, k), .7)
for k in range(4): one(TAMB, bt(13, 1 + k) + E8, .22, -.35)
for k, n in enumerate(['A#1', 'D2', 'F2', 'D2', 'C2', 'E2', 'G2', 'E2']): cpz(n, bt(13) + k * E8, .75, dur=.2)
for k, ts in enumerate(T['slaps']): one(KC + ['card-place-1.ogg', 'card-place-2.ogg', 'card-place-3.ogg', 'card-place-2.ogg'][k], ts, .55, [-.3, -.1, .1, .3][k]); H(ts, f'sticker {k + 1}')
glock('G5', T['lCap'], .55, dur=.8); xylo('C6', T['lCap'], .6, dur=.6); chord(hnl, ['F2', 'A2'], T['lCap'], .5, dur=1.8, rel=.4); H(T['lCap'], 'ONE STORY. FOUR STYLES. YOUR CHARACTER.')
piano('F2', T['e1'], .7, dur=3, rel=.8); chord(piano, ['F3', 'A3', 'C4'], T['e1'], .45, dur=3, rel=.8); chord(hnl, ['F2', 'C2'], T['e1'], .45, dur=2.4, rel=.6); one(KICK, T['e1'], .5); H(T['e1'], 'end card')
glock('C6', T['e2'], .5, dur=.8); piano('A4', T['e2'], .4, dur=1, rel=.4); H(T['e2'], 'NEW EPISODES IN A DAY')
piano('C5', T['e3'], .45, dur=1.2, rel=.5); chord(piano, ['F3', 'A3', 'C4', 'F4'], T['e3'], .35, dur=2.5, rel=.8); H(T['e3'], 'name')
piano('F5', T['e4'], .4, dur=2.2, rel=.8); glock('C6', T['e4'], .35, dur=1.2); H(T['e4'], 'email')

# ======================= mix down =======================
x = out[:int(SR * DUR)].copy(); f = int(1.2 * SR); x[-f:] *= np.linspace(1, 0, f)[:, None] ** 1.5   # the last chord rings out under the still frame
x = x / max(1e-6, np.abs(x).max()) * .7
with wave.open(os.path.join(OUT, 'score_raw.wav'), 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1) * 32767).astype('<i2').tobytes())
# loudness: two passes, so the gain is one fixed value (linear), not a ramp; the limiter's lookahead is compensated
raw = os.path.join(OUT, 'score_raw.wav')
meas = subprocess.run(['ffmpeg', '-hide_banner', '-i', raw, '-af', 'loudnorm=I=-16:TP=-2:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
m = json.loads(meas[meas.rindex('{'):meas.rindex('}') + 1])
ln = f"loudnorm=I=-16:TP=-2:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', raw, '-af', ln + ',aresample=48000,alimiter=limit=0.7:level=false:latency=true', '-ar', '48000', os.path.join(OUT, 'score.wav')], check=True)
json.dump(sorted(set(HITS)), open(os.path.join(OUT, 'hits.json'), 'w'))
open(os.path.join(OUT, 'samples_used.txt'), 'w').write('\n'.join(sorted(USED)) + '\n')
SRC = [('vsco/', 'https://github.com/sgossner/VSCO-2-CE', 'Versilian Studios Chamber Orchestra 2 Community Edition', 'CC0 1.0'),
       ('kenney/casino/', 'https://kenney.nl/assets/casino-audio', 'Kenney, kenney.nl', 'CC0 1.0'), ('kenney/rpg/', 'https://kenney.nl/assets/rpg-audio', 'Kenney, kenney.nl', 'CC0 1.0'),
       ('kenney/impact/', 'https://kenney.nl/assets/impact-sounds', 'Kenney, kenney.nl', 'CC0 1.0'),
       ('freepats/UprightPianoKW/', 'https://freepats.zenvoid.org/Piano/acoustic-grand-piano.html', 'FreePats project, Upright Piano KW (a Kawai upright, recorded 2017), version 2022-02-21', 'CC0 1.0'),
       ('opengameart/luckius/', 'https://opengameart.org/content/various-paper-sound-effects', 'Luckius, "Various Paper Sound Effects" (file: Paper Ripped - 1.wav)', 'CC0 1.0'),
       ('opengameart/antumdeluge/zipper', 'https://opengameart.org/content/zipper', 'AntumDeluge, "Zipper" (a jacket zipper; file: zipper-1.wav)', 'CC0 1.0'),
       ('opengameart/antumdeluge/pencil', 'https://opengameart.org/content/pencil-sounds', 'AntumDeluge, "Pencil Sounds" (pencil_write by NachtmahrTV)', 'CC0 1.0'),
       ('opengameart/owlishmedia/', 'https://opengameart.org/content/202-more-sound-effects', 'OwlishMedia, "202 More Sound Effects" (Paper & Stationery, recorded at home)', 'CC0 1.0')]
with open(os.path.join(OUT, 'audio_sources.txt'), 'w') as fo:
    fo.write('YOUR FIRST BIG WIN (demo reel): every recorded audio file in the mix, with its source and license.\n'
             'All are CC0 1.0 (public domain dedication: commercial use allowed, no attribution required). None come from a music library that registers with Content ID.\n'
             'The reel keeps its own copy of every file in audio/, with the libraries\' own license files.\n\n')
    for u in sorted(USED):
        _, url, who, lic = next(v for v in SRC if u.startswith(v[0])); fo.write(f'{u}\n    source: {url}  ({who})\n    license: {lic}\n')
    fo.write('\nComposed (not recorded files): the whole score, written note by note in tools/score.py on the 96 BPM grid and played by the '
             'instrument recordings above, including the glockenspiel shimmer under the ink-to-riso dissolve, the coin-by-coin glockenspiel '
             'climb as the piggy bank fills, the rising piano notes on each check, the trombone "uh-oh" and the brass stabs. Two sound effects are '
             'layered from recordings rather than single files: the sticker slap (a Kenney card slap over a Kenney soft impact) and the rubber '
             'stamp (a Kenney wooden impact over a Kenney card placement). The pencil sounds are excerpts cut from one pencil-writing recording. '
             'No synthesized tones are used anywhere.\n')
print(len(USED), 'samples;', len(HITS), 'synced hits ->', OUT)
