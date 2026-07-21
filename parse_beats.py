import re, sys, json, csv, os

URL_RE = re.compile(r'https?://[^\s\)\]\>"]+', re.I)
PLAY_RE = re.compile(r'\(*\s*PLAY\b.*?(HORIZONTAL|VERTICAL)?\s*\)*\s*$', re.I)
TC_RE = re.compile(r'^\**\s*:?(\d{1,2}:\d{2}|\d{1,2}:\d{2}:\d{2}|\d{2}|:\d{2}|00)\s*[-–]\s*(END OF CLIP|[\d:]+)\s*(\(([^)]*)\))?', re.I)
WHOLE_RE = re.compile(r'^\**\s*WHOLE CLIP\s*\**$', re.I)
BUTT_RE = re.compile(r'^\**\s*BUTT\s*\**$', re.I)
NOISE_RE = re.compile(r'^(TEASE|.*SPONSOR|.*CHAPTER|TAKE QR|JOIN THE CHAT|HIT LIKE|\s*[_\-–—]{3,}\s*|\s*#*\s*)$', re.I)

def clean(l):
    l = l.replace('\u200b','').strip()
    l = re.sub(r'\*+','',l)
    l = re.sub(r'^[\-\u2013\u2014\s]+','',l)
    return l.strip()

def platform_of(url):
    u = url.lower()
    for k,v in [('tiktok','tiktok'),('youtube','youtube'),('youtu.be','youtube'),
                ('facebook','facebook'),('instagram','instagram'),('reddit','reddit')]:
        if k in u: return v
    return 'web/news'

def parse(path, ep):
    raw = [l.rstrip() for l in open(path, encoding='utf-8')]
    lines = [clean(l) for l in raw]
    beats, i = [], 0
    # index of every PLAY marker
    plays = [n for n,l in enumerate(lines) if re.search(r'\bPLAY\b.*\bCLIP\b|\bPLAY\b.*\b(HORIZONTAL|VERTICAL)\b', l, re.I)]
    for bi, p in enumerate(plays):
        orient = 'vertical' if re.search(r'VERTICAL', lines[p], re.I) else 'horizontal'
        # setup text: walk backwards to previous play block end or section break
        start = plays[bi-1] if bi else 0
        setup = []
        for n in range(p-1, start, -1):
            l = lines[n]
            if not l: continue
            if URL_RE.search(l) or TC_RE.match(l) or WHOLE_RE.match(l) or BUTT_RE.match(l): break
            if NOISE_RE.match(l): continue
            setup.append(l)
            if len(setup) >= 12: break
        setup.reverse()
        # payload: walk forward collecting urls + timecodes until next play marker
        end = plays[bi+1] if bi+1 < len(plays) else len(lines)
        urls, segs = [], []
        for n in range(p+1, end):
            l = lines[n]
            if not l: continue
            for u in URL_RE.findall(l):
                if u not in urls: urls.append(u)
            if WHOLE_RE.match(l): segs.append({'in':'start','out':'end','outcue':None})
            m = TC_RE.match(l)
            if m: segs.append({'in':m.group(1),'out':m.group(2),'outcue':(m.group(4) or '').strip() or None})
            if l and not URL_RE.search(l) and not TC_RE.match(l) and not WHOLE_RE.match(l) \
               and not BUTT_RE.match(l) and len(l) > 25:
                break
        for u in urls:
            beats.append({
                'episode': ep,
                'beat_id': f'{ep}-b{bi+1:02d}',
                'orientation': orient,
                'setup_text': ' / '.join(setup[-8:]),
                'url': u,
                'platform': platform_of(u),
                'segments': segs if len(urls) == 1 else [],
                'n_segments': len(segs) if len(urls) == 1 else None,
            })
    return beats

all_beats = []
for f, ep in [('s1.txt','06-03'), ('s2.txt','06-17'), ('s3.txt','05-06')]:
    all_beats += parse(f, ep)

json.dump(all_beats, open('beats.json','w'), indent=2)
print(f'{len(all_beats)} clip rows across {len(set(b["beat_id"] for b in all_beats))} beats')
for b in all_beats:
    print(f'{b["beat_id"]:10} {b["orientation"]:10} {b["platform"]:10} {len(b["segments"])} seg  {b["url"][:60]}')
