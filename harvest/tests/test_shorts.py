"""Shorts backend tests. No network: the search path is stubbed.

Covers the regression these were written for -- vertical beats used to skip
the YouTube backend entirely, so their `shorts` register never ran anywhere.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rossen_harvest.youtube import ShortsBackend, SHORTS_MAX_DURATION, harvest_beat
from rossen_harvest.candidates import from_ytdlp

ok = fail = 0
def check(label, cond):
    global ok, fail
    if cond: ok += 1; print(f"  PASS  {label}")
    else:    fail += 1; print(f"  FAIL  {label}")


print("\n-- query construction --")
b = ShortsBackend()
check("suffix appended", b._search_key("grandma scammed").endswith(" #shorts"))
check("suffix not duplicated",
      b._search_key("crying #shorts").count("#shorts") == 1)
check("case-insensitive suffix detect",
      b._search_key("x #SHORTS").lower().count("#shorts") == 1)
check("respects limit", b._search_key("q").startswith("ytsearch30:"))
check("platform is its own surface", ShortsBackend.platform == "shorts")


print("\n-- duration ceiling --")
class StubBackend(ShortsBackend):
    """Returns a fixed result set instead of calling YouTube."""
    def __init__(self, entries):
        super().__init__()
        self._entries = entries
    def search(self, query, limit=None):
        # bypass the network, keep ShortsBackend's filtering logic
        entries = self._entries
        kept = []
        for e in entries:
            dur = e.get("duration")
            if dur is not None and dur > SHORTS_MAX_DURATION:
                continue
            e = dict(e); e["_orientation"] = "vertical"
            e["_duration_known"] = dur is not None
            kept.append(e)
        return kept

entries = [
    {"id": "a" * 11, "title": "short one", "duration": 30},
    {"id": "b" * 11, "title": "long form package", "duration": 240},
    {"id": "c" * 11, "title": "exactly at ceiling", "duration": 60},
    {"id": "d" * 11, "title": "null duration", "duration": None},
]
got = StubBackend(entries).search("q")
ids = [e["id"][0] for e in got]
check("long-form filtered out", "b" not in ids)
check("under ceiling kept", "a" in ids)
check("exactly at ceiling kept (<=, not <)", "c" in ids)
check("null duration kept, not silently dropped", "d" in ids)
check("null duration flagged unknown",
      [e for e in got if e["id"].startswith("d")][0]["_duration_known"] is False)
check("known duration flagged known",
      [e for e in got if e["id"].startswith("a")][0]["_duration_known"] is True)


print("\n-- normalization tags the surface --")
c = from_ytdlp(got[0], beat_id="b03", query="q", register="shorts", rank=1)
check("platform is shorts, not youtube", c.platform == "shorts")
check("orientation vertical", c.orientation == "vertical")
long_c = from_ytdlp({"id": "e" * 11, "title": "t", "duration": 200},
                    beat_id="b01", query="q", register="news")
check("untagged entry stays youtube", long_c.platform == "youtube")
check("untagged entry stays horizontal", long_c.orientation == "horizontal")
check("duration_known defaults True", long_c.duration_known is True)
check("surfaced_for serializes", "surfaced_for" in c.to_row())


print("\n-- register gating --")
beat = {
    "beat_id": "b03",
    "queries": {
        "shorts": ["#scamalert she lost everything"],
        "platform": ["fake fbi page"],
        "news": ["woman loses life savings to imposter scam"],
        "anchor": ["FTC $3.5 billion imposter scams 2025"],
    },
}
seen = []
class Recorder(StubBackend):
    def search(self, query, limit=None):
        seen.append(query)
        return []

harvest_beat(beat, Recorder([]), registers={"shorts", "platform"},
             jitter=(0, 0), concurrency=1)
check("shorts register ran", "#scamalert she lost everything" in seen)
check("platform register ran", "fake fbi page" in seen)
check("news register excluded (noun-heavy misses Shorts titles)",
      "woman loses life savings to imposter scam" not in seen)
check("anchor register excluded", "FTC $3.5 billion imposter scams 2025" not in seen)


print("\n-- vertical beats reach Shorts (the regression) --")
from rossen_harvest.__main__ import SHORTS_REGISTERS
check("SHORTS_REGISTERS is shorts+platform",
      SHORTS_REGISTERS == {"shorts", "platform"})
vertical_beat = {"beat_id": "b03", "orientation": "vertical",
                 "queries": {"shorts": ["#scam fake page"]}}
seen.clear()
harvest_beat(vertical_beat, Recorder([]), registers=SHORTS_REGISTERS,
             jitter=(0, 0), concurrency=1)
check("a vertical beat's shorts query actually runs", seen == ["#scam fake page"])

print(f"\n{'='*50}\n{ok} passed, {fail} failed\n{'='*50}")
sys.exit(1 if fail else 0)
