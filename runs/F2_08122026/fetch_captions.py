import json, re, sys, time
sys.path.insert(0,"/home/user/Rossen/harvest")
from rossen_harvest.transcripts import fetch_transcript
from rossen_harvest.cache import Cache

YT=re.compile(r"(?:v=|/shorts/|youtu\.be/|/embed/)([A-Za-z0-9_-]{11})")
SL=json.load(open("shortlist.json"))
cache=Cache("harvest.db")
out={}
seen=set()
for b in SL:
    for c in b["candidates"]:
        m=YT.search(c["url"])
        if not m:
            out[c["url"]]={"status":"not_youtube","platform":c["platform"]}
            continue
        vid=m.group(1)
        if vid in seen: continue
        seen.add(vid)
        t=fetch_transcript(vid, cache=cache)
        if t is None:
            out[c["url"]]={"status":"null","video_id":vid}
            print(f"  NULL     {vid}  {c['uploader']}")
        else:
            out[c["url"]]={"status":"ok","video_id":vid,"source":t.source,
                           "duration":t.duration,"n_cues":len(t.cues),
                           "cues":[{"start":x.start,"end":x.end,"text":x.text} for x in t.cues]}
            print(f"  ok {t.source:6} {vid}  {len(t.cues):4} cues  {t.duration:6.0f}s  {c['uploader']}")
        time.sleep(1.5)
json.dump(out, open("transcripts.json","w"), indent=1)
print(f"\n{sum(1 for v in out.values() if v['status']=='ok')} ok / "
      f"{sum(1 for v in out.values() if v['status']=='null')} null / "
      f"{sum(1 for v in out.values() if v['status']=='not_youtube')} non-youtube")
