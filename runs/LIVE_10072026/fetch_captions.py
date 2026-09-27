import json,re,sys,time,sqlite3
sys.path.insert(0,"/home/user/Rossen/harvest")
from rossen_harvest.transcripts import fetch_transcript
from rossen_harvest.cache import Cache
YT=re.compile(r"(?:v=|/shorts/)([A-Za-z0-9_-]{11})")
SL=json.load(open("shortlist.json")); cache=Cache("harvest.db"); out={}; nulls=[]
def get(vid):
    t=fetch_transcript(vid,cache=cache)
    return t
for b in SL:
    for c in b["candidates"]:
        m=YT.search(c["url"])
        if not m: out[c["url"]]={"status":"not_youtube","platform":c["platform"]}; continue
        vid=m.group(1)
        if any(v.get("video_id")==vid for v in out.values()): continue
        t=get(vid)
        if t is None: nulls.append((c["url"],vid)); out[c["url"]]={"status":"null","video_id":vid}; print("NULL",vid,flush=True)
        else:
            out[c["url"]]={"status":"ok","video_id":vid,"source":t.source,"duration":t.duration,"n_cues":len(t.cues),
                           "cues":[{"start":x.start,"end":x.end,"text":x.text} for x in t.cues]}
            print(f"ok {t.source:6} {vid} {len(t.cues):4} cues {t.duration:6.0f}s",flush=True)
        time.sleep(3)
if nulls:
    print(f"retrying {len(nulls)} null(s) after 60s wait",flush=True); time.sleep(60)
    db=sqlite3.connect("harvest.db")
    for u,v in nulls: db.execute("DELETE FROM query_cache WHERE query=?",(f"captions:{v}",))
    db.commit(); db.close()
    for u,v in nulls:
        t=get(v)
        if t is None: out[u]={"status":"null","video_id":v,"retried":True}; print("STILL NULL",v,flush=True)
        else:
            out[u]={"status":"ok","video_id":v,"source":t.source,"duration":t.duration,"n_cues":len(t.cues),"retried":True,
                    "cues":[{"start":x.start,"end":x.end,"text":x.text} for x in t.cues]}
            print("RECOVERED",v,flush=True)
        time.sleep(15)
json.dump(out,open("transcripts.json","w"),indent=1)
print("DONE", sum(v["status"]=="ok" for v in out.values()),"ok /",sum(v["status"]=="null" for v in out.values()),"null /",sum(v["status"]=="not_youtube" for v in out.values()),"non-youtube",flush=True)
