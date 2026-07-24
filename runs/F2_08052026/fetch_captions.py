#!/usr/bin/env python3
"""Step 5 — captions. YouTube caption fetch (metadata-cheap).

fetch_many takes BARE video IDs, not URLs (it prepends watch?v= itself);
a full URL double-prepends and silently returns None. Saves cue-level
transcripts (start,text) so pass-two outcue verification uses real
timestamps, not guesses.
"""
import json, re, sys
sys.path.insert(0, "/home/user/Rossen/harvest")
from rossen_harvest.transcripts import fetch_many
from rossen_harvest.cache import Cache

sl = json.load(open("shortlist.json"))
cache = Cache("harvest.db")
YT_ID = re.compile(r"(?:v=|/shorts/|youtu\.be/|/embed/)([A-Za-z0-9_-]{11})")

yt = []
for c in sl:
    if c["platform"] != "youtube":
        continue
    m = YT_ID.search(c["url"] or "")
    if m:
        yt.append((c["url"], m.group(1)))

ids = list({i for _, i in yt})
print(f"YouTube ids to fetch: {len(ids)}")
tr = fetch_many(ids, cache=cache)

out = {}
got = null = 0
for url, i in yt:
    t = tr.get(i)
    if t and t.cues and t.source != "none":
        out[url] = {
            "video_id": i, "source": t.source, "n_cues": len(t.cues),
            "duration": t.duration,
            "cues": [{"start": round(c.start, 2), "end": round(c.end, 2), "text": c.text} for c in t.cues],
        }
        got += 1
    else:
        out[url] = None
        null += 1

print(f"captions: {got} with text, {null} null/disabled")
json.dump(out, open("transcripts.json", "w"), indent=1)
print("wrote transcripts.json")
