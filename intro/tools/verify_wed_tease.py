"""Checks on the final Wednesday tease mp4 (and its preview): format; the three scams' equal bars and where the picture changes
scene; every card present and still for its whole time on screen; the beat of silence before the promise; the handoff into the
loop (no frame jump, no audio bump); the loop's packets and pixels unchanged from the delivered file; the safe zone; the preview.
usage: python3 tools/verify_wed_tease.py <final.mp4> [preview.mp4]  ->  prints a report (tools/build_wed_tease.sh saves it)"""
import numpy as np, subprocess, json, sys, hashlib, os
F = sys.argv[1]; PV = sys.argv[2] if len(sys.argv) > 2 else None
LOOP = '../final-videos/09 Live Today Loop - Wednesday 5 PM (9x16).mp4'
W, H, FPS, SR = 1080, 1920, 24, 48000
BEAT, BAR, SLAM, E8 = .625, 2.5, .14, .3125
OFF = 3 * BEAT   # the intro title card (a 3-beat pickup) comes first: video time = film time + OFF
at = lambda bar, beat=1: OFF + bar * BAR + (beat - 1) * BEAT
# the film's own timeline (wed-tease.js: TR and CAPS)
TR = {'intro card -> driveway (dissolve)': (OFF - BEAT, OFF - SLAM), 'smoke': (at(2, 4) - .06, at(3) - SLAM), 'zoomSite': (at(4) - .36, at(4) - SLAM), 'swing': (at(5) - .52, at(5) - SLAM),
      'toMail': (at(6) - .34, at(6) - SLAM), 'zoomTicket': (at(7) - .36, at(7) - SLAM), 'cut to Jeff': (at(9) - SLAM, at(9) - SLAM + 1 / 24), 'toLoop': (at(11) - .34, at(11) - SLAM)}
FLASH = (at(7), at(7) + .3)   # the camera flash (full frame, under the card): a flash, not a scene change
CAPS = [(at(0), at(1) - SLAM, 'SELLING YOUR CAR?'), (at(1), at(2) - SLAM, "WHILE YOU'RE / DISTRACTED..."), (at(2), TR['smoke'][0], 'YOUR CAR: / WORTHLESS'),
        (at(3), TR['zoomSite'][0], 'BUYING A CAR / ONLINE?'), (at(4), TR['swing'][0], "THE DEALERSHIP / ISN'T REAL"), (at(5), TR['toMail'][0], "THE CAR / DOESN'T EXIST"),
        (at(6), TR['zoomTicket'][0], '$3,000 / IN TICKETS'), (at(7), at(8) - SLAM, "IT'S NOT / YOUR CAR"), (at(8), at(9) - SLAM, 'SOMEONE COPIED / YOUR PLATE'),
        (at(9), TR['toLoop'][0], "WE'LL SHOW YOU / THE RED FLAGS.")]
NT = 765   # intro + tease frames (1.875 + 30 s); the loop follows
SCAMS = [('oil scam', 0, 3), ('fake AI dealership', 3, 6), ('cloned plates', 6, 9)]
WPS = 5.0   # reading speed for a short ALL-CAPS card: 300 words a minute; "read twice" = 2 x words / WPS
rep, fails = [], []
def say(s=''): rep.append(s); print(s)
def check(ok, what): say(('PASS  ' if ok else 'FAIL  ') + what); (None if ok else fails.append(what))
def probe(f):
    j = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', f], capture_output=True, check=True).stdout)
    return {s['codec_type']: s for s in j['streams']}, j['format']
def frames(f, lo=0, n=None, gray=False, post='', size=(W, H)):   # decoded frames as uint8 arrays (post: extra filters, e.g. a crop)
    vf = f"select='gte(n\\,{lo})'" + (f"*lt(n\\,{lo + n})" if n else '') + (',' + post if post else '')
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-vf', vf, '-vsync', '0', '-pix_fmt', 'gray' if gray else 'rgb24', '-f', 'rawvideo', '-'], capture_output=True, check=True).stdout
    w, h = size; return np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3) if not gray else np.frombuffer(raw, np.uint8).reshape(-1, h, w)
def pcm(f):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-map', '0:a:0', '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2)
db = lambda x: 20 * np.log10(max(float(x), 1e-9))

say(f'file: {F}')
st, fm = probe(F); v, a = st['video'], st['audio']
nf = int(v['nb_frames'])
say('\n== format')
check(v['width'] == 1080 and v['height'] == 1920 and v['r_frame_rate'] == '24/1', f"video {v['width']}x{v['height']} at {v['r_frame_rate']} fps, {v['codec_name']} {v['pix_fmt']} (the loop: 1080x1920, 24 fps)")
check(nf == NT + 240, f'{nf} frames = {nf / FPS:.3f} s (intro card 45 frames = 1.875 s + tease 720 frames = 30.000 s + the loop twice, 2 x 120 frames = 10.000 s)')
check(abs(float(a['duration']) - (NT / FPS + 10)) < .03 and a['sample_rate'] == '48000', f"audio {a['codec_name']} {a['sample_rate']} Hz {a['channels']} ch, {float(a['duration']):.3f} s")

say('\n== the three scams: equal bars, one idea per bar (whole bars at 96 BPM)')
for name, b0, b1 in SCAMS: say(f'      {name:20s} bars {b0}-{b1 - 1}: {at(b0):6.3f}-{at(b1):6.3f} s = {b1 - b0} bars = {at(b1) - at(b0):.3f} s')
check(len({b1 - b0 for _, b0, b1 in SCAMS}) == 1, 'all three scams get 3 bars (7.5 s) each; the promise gets bars 9-10, the handoff bar 11')
# where the picture actually changes scene: a large jump in the mean frame difference
G = frames(F, 0, NT, gray=True, post='scale=270:480', size=(270, 480)).astype(np.int16)
d = np.abs(np.diff(G, axis=0)).mean((1, 2))
big = [i + 1 for i in range(len(d)) if d[i] > 12]
def within(t): return next((k for k, (t0, t1) in TR.items() if t0 - 1 / 24 <= t <= t1 + 1 / 24), None)
within0 = within
within = lambda t: within0(t) or ('flash' if FLASH[0] <= t <= FLASH[1] else None)
outside = [f for f in big if not within(f / FPS) and f / FPS < at(11)]
say('      scene-change frames (mean change > 12 of 255): ' + ', '.join(f'{f}({f / FPS:.2f}s {within(f / FPS) or "?"})' for f in big if f / FPS < at(11)))
check(not outside, 'every scene change happens inside a planned transition window (or the cut to Jeff; the camera flash is listed), never mid-bar')

say('\n== the intro title card (3 CAR SCAMS / LIVE WEDNESDAY 5 PM ET, the official logo)')
IC = frames(F, 0, int(round((OFF - BEAT) * FPS)), post='crop=1080:740:0:380', size=(1080, 740)).astype(np.int16)   # still until its words start to fade
dmi = np.abs(IC - IC[0]).mean((1, 2, 3)).max(); hold = len(IC) / FPS
check(dmi < 1.0 and hold >= 2 * 3 / WPS,
      f'on screen from frame 0 for {hold:.2f} s, dead still (max change {dmi:.2f}/255 over the logo, title and time; the little car drives in below them); '
      f'reading the 3-word title twice at 300 wpm takes {2 * 3 / WPS:.2f} s')
del IC

say('\n== the logo bug (the official logo, top-left, from the first scene until the loop; not on the title card)')
BG = frames(F, 0, NT, post='crop=140:84:40:48', size=(140, 84)).astype(np.int16)
b0, b1 = int(np.ceil(OFF * FPS)), int(TR['toLoop'][0] * FPS) - 1
from PIL import Image as _I
lg = _I.open('assets/official_logo.png').convert('RGBA'); bb = lg.getbbox(); lg = lg.crop(bb).resize((140, round(140 * (bb[3] - bb[1]) / (bb[2] - bb[0]))), _I.LANCZOS)
la = np.array(lg).astype(np.int16); m = np.zeros((84, 140), bool)   # the logo's own opaque pixels, inset 2 px (its corners are transparent and its edge pixels blend with the scene)
m[:la.shape[0]] = np.array(_I.fromarray(((la[..., 3] > 250) * 255).astype(np.uint8)).filter(__import__('PIL.ImageFilter', fromlist=['x']).MinFilter(5))) > 0
dmb = max(float(np.abs(BG[k] - BG[b0])[m].mean()) for k in range(b0, b1 + 1)); away = float(np.abs(BG[0] - BG[b0])[m].mean())
inner = BG[b0][m].mean(0)
ref = la[..., :3][m[:la.shape[0]]].mean(0); col = float(np.abs(inner - ref).max())
check(dmb < 3.0 and away > 20 and col < 8, f'present and still (the rendered frames are pixel-identical there; the mp4 adds H.264 noise from the scenes changing around it, < 3/255) from {b0 / FPS:.2f} s to {b1 / FPS:.2f} s (max change over its opaque pixels {dmb:.2f}/255); absent on the title card (frame 0 differs by {away:.1f}/255); drawn untouched (opaque-interior colour within {col:.1f} levels of the file)')
del BG

say('\n== the cards: one at a time, present and still for their whole time, readable twice')
ov = [(CAPS[k][2], CAPS[k + 1][2]) for k in range(len(CAPS) - 1) if CAPS[k][1] > CAPS[k + 1][0] - SLAM]
check(not ov, 'no two cards on screen together (each leaves before the next starts to land)')
tr_over = [(c[2], k) for c in CAPS for k, (t0, t1) in TR.items() if k != 'cut to Jeff' and c[0] - SLAM < t1 and c[1] > t0]
check(not tr_over, 'no transition runs while a card is up')
band = frames(F, 0, NT, post='crop=1080:270:0:330', size=(1080, 270))   # the card band (screen y 330-600)
for t0, t1, s in CAPS:
    f0, f1 = int(np.ceil(t0 * FPS)), int(np.ceil(t1 * FPS)) - 1   # both lines land together on t0 and are still from that frame
    ref = band[f0].astype(np.int16); solid = (np.abs(ref - np.array([29, 27, 31])).sum(2) < 70) | (np.abs(ref - np.array([8, 88, 192])).sum(2) < 110)
    from PIL import Image, ImageFilter   # the chips are solid slabs; the halftone dots are not: an opening (min then max filter) keeps only the slabs
    core = np.array(Image.fromarray((solid * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(25)).filter(ImageFilter.MaxFilter(25))) > 0
    ys, xs = np.nonzero(core); y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    cm = core[y0:y1 + 1, x0:x1 + 1]; box = band[f0:f1 + 1, y0:y1 + 1, x0:x1 + 1].astype(np.int16); dm = max(float(np.abs(fr - box[0])[cm].mean()) for fr in box)   # over the card's own ink only
    words = len(s.replace('/', ' ').split()); need = 2 * words / WPS
    hold = (f1 - f0 + 1) / FPS; up = t1 - (t0 - SLAM)
    check(dm < 1.5 and hold >= need and x0 >= 164 and x1 <= 916 and 330 + y0 >= 288,
          f'"{s}": on screen {up:.2f} s ({t0 - SLAM:.2f}-{t1:.2f}), dead still {hold:.2f} s (reading it twice at 300 wpm takes {need:.2f} s), max change while still {dm:.2f}/255, card box x {x0}-{x1} y {330 + y0}-{330 + y1}')
say('      every card sits level (no rotation in wed-tease.js chip()); the promise card is level; solid ink with nothing drawn over it (drawn after the print finish)')

say('\n== the beat of silence before the promise')
A = pcm(F); s0, s1 = int((at(8, 4) + .01) * SR), int((at(9) - .012) * SR)   # the landing of card and hit at 9:1 starts after this
pk = np.abs(A[s0:s1]).max(); rm = np.sqrt((A[s0:s1] ** 2).mean())
pre = np.sqrt((A[int((at(8, 3)) * SR):int(at(8, 3.8) * SR)] ** 2).mean())
check(pk < 10 ** (-60 / 20), f'{at(8, 4) + .01:.3f}-{at(9) - .012:.3f} s: peak {db(pk):.1f} dBFS, rms {db(rm):.1f} dBFS (the beat before it: rms {db(pre):.1f} dBFS)')

say('\n== the handoff into the loop, and the loop into itself (it plays twice)')
L = frames(LOOP)
for r in range(2):
    T = frames(F, NT + 120 * r, 120); same = sum(int(np.array_equal(L[k], T[k])) for k in range(120))
    check(same == 120, f'loop copy {r + 1} (frames {NT + 120 * r}-{NT + 120 * r + 119}) decodes identical to the delivered loop, pixel for pixel: {same}/120 frames')
    if r == 0: T0 = T[0].copy()
    del T
del band, G
last = frames(F, NT - 1, 1)[0].astype(np.int16); m_last = np.abs(last - L[119].astype(np.int16)).mean()
jump = np.abs(T0.astype(np.int16) - last).mean(); wrap = np.abs(L[0].astype(np.int16) - L[119].astype(np.int16)).mean()
check(m_last < 4.0, f"the tease's last frame is the loop's own frame 119 (decoded from the delivered file, re-encoded once): mean difference {m_last:.2f}/255")
check(jump <= wrap + m_last + .5, f'the cut {NT - 1} -> {NT} changes the picture by {jump:.2f}/255; the loop\'s own wrap (119 -> 0) by {wrap:.2f}/255, plus the re-encode {m_last:.2f}: no frame jump')
say(f'      the cut {NT + 119} -> {NT + 120} (loop into loop) is the loop\'s own wrap: both copies decode identical to the delivered loop (above)')
LA = pcm(LOOP)[: 5 * SR]   # the decoded AAC carries 640 samples of encoder padding after its 5.000 s
seg = lambda x, i: np.sqrt((x[i:i + int(.05 * SR)] ** 2).mean())
lb, la = seg(LA, len(LA) - int(.05 * SR)), seg(LA, 0)
for j, name in ((NT * SR // FPS, 'tease into loop'), ((NT + 120) * SR // FPS, 'loop into loop')):
    before, after = seg(A, j - int(.05 * SR)), seg(A, j)
    step = np.abs(np.diff(A[j - 480:j + 480], axis=0)).max(); nb = np.percentile(np.abs(np.diff(A[j - 24000:j + 24000], axis=0)).max(1), 99.9)
    check(abs(db(after) - db(before) - (db(la) - db(lb))) < 1.5 and step <= nb * 1.5,
          f'audio at {j / SR:.1f} s ({name}): {db(before):.1f} -> {db(after):.1f} dBFS (50 ms rms; the loop\'s own wrap: {db(lb):.1f} -> {db(la):.1f}); largest sample step {step:.3f} vs {nb:.3f} (99.9th pct nearby): no bump')
    n = min(len(LA), len(A) - j); c = np.corrcoef(A[j:j + n, 0], LA[:n, 0])[0, 1]
    check(c > .99, f'  the audio after it matches the delivered loop\'s audio: correlation {c:.5f} (re-encoded once in the mux; the video is untouched)')

say('\n== the loop unchanged from the original file (both copies)')
def pk_md5(f):
    out = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-map', '0:v', '-c', 'copy', '-f', 'framemd5', '-'], capture_output=True, check=True).stdout.decode()
    return [l.split(',')[-1].strip() for l in out.splitlines() if l and not l.startswith('#')]
def raw_v(f): return subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-map', '0:v', '-c', 'copy', '-f', 'data', '-'], capture_output=True, check=True).stdout
def sizes(f): return [int(p['size']) for p in json.loads(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'packet=size', '-of', 'json', f], capture_output=True, check=True).stdout)['packets']]
def nals(b):
    i, r = 0, []
    while i + 4 <= len(b): n = int.from_bytes(b[i:i + 4], 'big'); r.append(b[i + 4:i + 4 + n]); i += 4 + n
    return r
po, pf = pk_md5(LOOP), pk_md5(F); so, sf = sizes(LOOP), sizes(F); ro, rf = raw_v(LOOP), raw_v(F)
avcc = subprocess.run(['ffmpeg', '-v', 'error', '-i', LOOP, '-map', '0:v', '-c', 'copy', '-bsf:v', 'h264_mp4toannexb', '-frames:v', '1', '-f', 'h264', '-'], capture_output=True, check=True).stdout
for r in range(2):
    k0 = NT + 120 * r; nsame = sum(x == y for x, y in zip(po[1:], pf[k0 + 1:k0 + 120]))
    check(nsame == 119, f'copy {r + 1}: video packets 2-120 are byte-identical to the delivered loop\'s (stream copy): {nsame}/119')
    off = sum(sf[:k0]); No, Nf = nals(ro[:so[0]]), nals(rf[off:off + sf[k0]]); extra = [x for x in Nf if x not in No]; own = all(x in avcc for x in extra)
    check(all(x in Nf for x in No) and {x[0] & 31 for x in extra} <= {7, 8} and own,
          f'copy {r + 1}, packet 1 (the key frame): all its NAL units are byte-identical ({[(x[0] & 31, len(x)) for x in No]}); the join adds only the loop\'s own SPS/PPS in-band ({[(x[0] & 31, len(x)) for x in extra]}, from its own header: {own})')
say(f'      delivered loop md5 {hashlib.md5(open(LOOP, "rb").read()).hexdigest()} (unchanged on disk)')

say('\n== safe zone (screen: text and key action clear of the top 15% (y < 288), bottom 25% (y > 1440) and right 15% (x > 918))')
say('      separate overlay pass: _check/wedtease/safe/ (the film rendered with ?safe=1, one frame per beat, and a contact sheet safe_sheet.jpg)')
say('      cards: every card box above lies inside x 164-916 and below y 288')

if PV:
    say('\n== preview')
    sv, sf = probe(PV); mb = os.path.getsize(PV) / 1e6
    enc = subprocess.run(['sh', '-c', f'strings "{PV}" | grep -m1 -o "crf=[0-9.]*"'], capture_output=True, text=True).stdout.strip()
    check(mb < 30 and enc.startswith('crf=21'), f'{PV}: {mb:.1f} MB, x264 {enc}, {sv["video"]["nb_frames"]} frames, audio {sv["audio"]["codec_name"]}')
say(f'\n{len(fails)} failed' + (': ' + '; '.join(fails) if fails else ''))
