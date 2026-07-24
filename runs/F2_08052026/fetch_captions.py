"""Fetch captions for shortlisted YouTube candidates."""
import json, re, sys
sys.path.insert(0, "/home/user/Rossen/harvest")
from pathlib import Path
from rossen_harvest.transcripts import fetch_many, Transcript
from rossen_harvest.cache import Cache

shortlist = json.loads(Path("shortlist.json").read_text())

# Extract YouTube video IDs from shortlist
YT_ID = re.compile(r"(?:v=|/shorts/|youtu\.be/|/embed/)([A-Za-z0-9_-]{11})")

yt_candidates = []
for c in shortlist:
    url = c.get("url") or ""
    m = YT_ID.search(url)
    if m:
        c["video_id"] = m.group(1)
        yt_candidates.append(c)
    else:
        c["video_id"] = None

video_ids = [c["video_id"] for c in yt_candidates if c["video_id"]]
print(f"Fetching captions for {len(video_ids)} YouTube candidates...")

cache = Cache("harvest.db")
transcripts = fetch_many(video_ids, cache=cache, concurrency=4)

# Build output
output = {}
got = 0
null = 0
for vid, t in transcripts.items():
    if t:
        got += 1
        output[vid] = {
            "video_id": vid,
            "source": t.source,
            "duration": t.duration,
            "full_text": t.full_text()[:3000],
            "cues": [{"start": c.start, "end": c.end, "text": c.text, "timecode": c.timecode}
                     for c in t.cues],
            "prompt": t.as_prompt(),
        }
    else:
        null += 1
        output[vid] = None

Path("transcripts.json").write_text(json.dumps(output, indent=2, default=str))
print(f"Captions fetched: {got} success, {null} null")

# Report which candidates got captions
for c in shortlist:
    vid = c.get("video_id")
    has_caption = vid and vid in output and output[vid] is not None
    title = (c.get("title") or "")[:60]
    platform = c.get("platform", "?")
    status = "OK" if has_caption else ("N/A (non-YT)" if not vid else "NULL")
    print(f"  {c['beat_id']} [{platform:8}] {status:12} {title}")
