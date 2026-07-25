"""Offline tests for the Shorts gate and the pixel orientation check.

Network calls are stubbed. The fixtures are the real videos from the
2026-07-25 vertical smoke test, so the regression these guard against is
the one that actually shipped a landscape clip against a vertical beat.
"""
import io
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rossen_harvest import shorts
from rossen_harvest.__main__ import _gate_orientation, _with_shorts_web, _wants_shorts
from rossen_harvest.candidates import Candidate

ok = fail = 0


def check(label, cond):
    global ok, fail
    if cond:
        ok += 1
        print(f"  PASS  {label}")
    else:
        fail += 1
        print(f"  FAIL  {label}")


def jpeg(width, height):
    """Minimal JPEG with a SOF0 segment carrying the given dimensions."""
    return (
        b"\xff\xd8"
        + b"\xff\xe0" + struct.pack(">H", 16) + b"JFIF\x00" + b"\x00" * 9
        + b"\xff\xc0" + struct.pack(">H", 17) + b"\x08"
        + struct.pack(">H", height) + struct.pack(">H", width)
        + b"\x03" + b"\x00" * 9
        + b"\xff\xd9"
    )


print("\n-- the stale duration ceiling --")
check("Shorts ceiling raised to 3 minutes", shorts.SHORTS_MAX_DURATION == 180)
check("legacy 60s ceiling kept for reference",
      shorts.LEGACY_SHORTS_MAX_DURATION == 60)
check("119s CTV News Short is no longer filtered out",
      shorts.looks_like_short(119))
check("the old ceiling would have dropped it",
      119 > shorts.LEGACY_SHORTS_MAX_DURATION)
check("null duration passes the pre-filter (flat-playlist returns None)",
      shorts.looks_like_short(None))
check("a 20-minute upload is still ruled out", not shorts.looks_like_short(1200))

print("\n-- JPEG dimension parsing --")
check("portrait thumbnail parsed", shorts.jpeg_dimensions(jpeg(1080, 1920)) == (1080, 1920))
check("landscape thumbnail parsed", shorts.jpeg_dimensions(jpeg(1280, 720)) == (1280, 720))
check("540x960 parsed", shorts.jpeg_dimensions(jpeg(540, 960)) == (540, 960))
check("non-JPEG rejected", shorts.jpeg_dimensions(b"not a jpeg at all") is None)
check("truncated data rejected", shorts.jpeg_dimensions(b"\xff\xd8") is None)

print("\n-- orientation from explicit dimensions (no network) --")
check("1080x1920 is vertical",
      shorts.verify_orientation("x", width=1080, height=1920) == shorts.VERTICAL)
check("1920x1080 is landscape",
      shorts.verify_orientation("x", width=1920, height=1080) == shorts.LANDSCAPE)
check("540x960 is vertical",
      shorts.verify_orientation("x", width=540, height=960) == shorts.VERTICAL)
check("640x360 reel is landscape",
      shorts.verify_orientation("x", width=640, height=360) == shorts.LANDSCAPE)

print("\n-- orientation from the oar thumbnail --")
# ZVQPxS16At0 (CTV News Short) serves oardefault at 1080x1920.
shorts.oar_dimensions = lambda vid, timeout=15.0: {
    "ZVQPxS16At0": (1080, 1920),
    "_RTe-ddhxoY": (540, 960),
    "PNjdcz3eG9o": None,      # landscape — no oar variant exists
    "oI05QvICQo8": None,
}.get(vid)
shorts._probe_reachable = lambda timeout: True

check("CTV News Short verified vertical",
      shorts.verify_orientation("ZVQPxS16At0") == shorts.VERTICAL)
check("540x960 non-Short verified vertical",
      shorts.verify_orientation("_RTe-ddhxoY") == shorts.VERTICAL)
check("25s 1280x720 clip verified LANDSCAPE (the postmortem bug)",
      shorts.verify_orientation("PNjdcz3eG9o") == shorts.LANDSCAPE)
check("21s 1280x720 clip verified LANDSCAPE",
      shorts.verify_orientation("oI05QvICQo8") == shorts.LANDSCAPE)

print("\n-- a dead network reads as unknown, never as landscape --")
shorts._probe_reachable = lambda timeout: False
check("unreachable host gives unknown, not a guess",
      shorts.verify_orientation("PNjdcz3eG9o") == shorts.UNKNOWN)
shorts._probe_reachable = lambda timeout: True

print("\n-- site:youtube.com/shorts query construction --")
q = shorts.shorts_web_queries(["#scamalert check the gift card", "gift card already empty"])
check("prefix applied", q[0] == "site:youtube.com/shorts #scamalert check the gift card")
check("all strings converted", len(q) == 2)
check("blank strings dropped", shorts.shorts_web_queries(["", "  ", "x"]) ==
      ["site:youtube.com/shorts x"])

print("\n-- beat routing --")
vertical_beat = {
    "beat_id": "smoke-vertical-b01",
    "orientation": "vertical",
    "platforms": ["shorts", "tiktok", "instagram"],
    "queries": {"shorts": ["gift card already empty"],
                "platform": ["gift card scam sticker", "tampered gift card rack", "third"]},
}
check("vertical beat wants shorts", _wants_shorts(vertical_beat))
enriched = _with_shorts_web(vertical_beat)
check("shorts_web register added", "shorts_web" in enriched["queries"])
check("seeded from shorts plus two platform strings",
      len(enriched["queries"]["shorts_web"]) == 3)
check("original beat not mutated", "shorts_web" not in vertical_beat["queries"])
check("existing registers preserved", enriched["queries"]["shorts"] ==
      ["gift card already empty"])

plain = {"beat_id": "b", "orientation": "horizontal", "platforms": ["news_web"],
         "queries": {"news": ["x"]}}
check("non-shorts beat untouched", _with_shorts_web(plain) is plain)

print("\n-- the orientation gate end to end --")


def cand(vid, beat_id="smoke-vertical-b01", platform="youtube"):
    return Candidate(platform=platform, url=f"https://y/{vid}", video_id=vid,
                     title=vid, beat_id=beat_id, query_that_found_it="q",
                     register="shorts")


beats = [{"beat_id": "smoke-vertical-b01", "orientation": "vertical"},
         {"beat_id": "horiz-b02", "orientation": "horizontal"}]

shorts_map = {"ZVQPxS16At0": True, "PNjdcz3eG9o": False, "_RTe-ddhxoY": False}
import rossen_harvest.__main__ as m
m.verify_orientation = lambda vid, **kw: {
    "ZVQPxS16At0": shorts.VERTICAL,
    "_RTe-ddhxoY": shorts.VERTICAL,
    "PNjdcz3eG9o": shorts.LANDSCAPE,
}.get(vid, shorts.UNKNOWN)
m.is_short = lambda vid, **kw: shorts_map.get(vid)

pool = [cand("ZVQPxS16At0"), cand("PNjdcz3eG9o"), cand("_RTe-ddhxoY"),
        cand("mystery0001"), cand("horizonly01", beat_id="horiz-b02"),
        cand("tk1", platform="tiktok")]

gated = _gate_orientation(list(pool), beats, drop=False)
by_id = {c.video_id: c for c in gated}
check("nothing dropped without --drop-landscape", len(gated) == 6)
check("Short flagged vertical", by_id["ZVQPxS16At0"].orientation_verified == shorts.VERTICAL)
check("Short flagged as a Short", by_id["ZVQPxS16At0"].is_short is True)
check("landscape clip flagged landscape",
      by_id["PNjdcz3eG9o"].orientation_verified == shorts.LANDSCAPE)
check("vertical non-Short flagged is_short False",
      by_id["_RTe-ddhxoY"].is_short is False)
check("unverifiable candidate is unknown, not vertical",
      by_id["mystery0001"].orientation_verified == shorts.UNKNOWN)
check("horizontal beat's candidate untouched",
      by_id["horizonly01"].orientation_verified is None)
check("non-youtube candidate untouched (needs its own media probe)",
      by_id["tk1"].orientation_verified is None)

gated2 = _gate_orientation(list(pool), beats, drop=True)
ids2 = {c.video_id for c in gated2}
check("verified landscape dropped", "PNjdcz3eG9o" not in ids2)
check("verified vertical kept", "ZVQPxS16At0" in ids2)
check("UNKNOWN survives — a network wobble must not shrink the funnel",
      "mystery0001" in ids2)
check("other beats' candidates never dropped", "horizonly01" in ids2)

print("\n-- the brave cap must not starve a register --")
# Regression: shorts_web was added at the tail of the queries dict, and
# harvest_beat concatenated registers before truncating to `cap`. With the
# default cap of 8 the new register never ran a single query.
from rossen_harvest.youtube import harvest_beat


class _StubBackend:
    platform = "stub"

    def __init__(self):
        self.seen = []

    def search(self, query, limit=None):
        self.seen.append(query)
        return []


capped_beat = {
    "beat_id": "b",
    "queries": {
        "platform": ["p1", "p2", "p3", "p4", "p5", "p6"],
        "victim": ["v1", "v2", "v3", "v4", "v5"],
        "news": ["n1", "n2", "n3", "n4"],
        "anchor": ["a1", "a2"],
        "shorts_web": ["s1", "s2", "s3"],
    },
}
stub = _StubBackend()
harvest_beat(capped_beat, stub, registers=set(capped_beat["queries"]),
             cap=8, concurrency=1, jitter=(0, 0))
seen_regs = {r for q in stub.seen for r, qs in capped_beat["queries"].items() if q in qs}
check("cap respected", len(stub.seen) == 8)
check("shorts_web survives the cap (was starved by flat concatenation)",
      "shorts_web" in seen_regs)
check("every register represented under the cap", len(seen_regs) == 5)
check("round-robin takes each register's first string first",
      stub.seen[:5] == ["p1", "v1", "n1", "a1", "s1"])

uncapped = _StubBackend()
harvest_beat(capped_beat, uncapped, registers=set(capped_beat["queries"]),
             cap=None, concurrency=1, jitter=(0, 0))
check("no cap runs every query", len(uncapped.seen) == 20)
check("no query lost or duplicated", sorted(uncapped.seen) == sorted(
    q for qs in capped_beat["queries"].values() for q in qs))

print("\n-- candidate carries the new fields --")
row = cand("ZVQPxS16At0").to_row()
check("orientation_verified in row", "orientation_verified" in row)
check("is_short in row", "is_short" in row)
check("both default to None (unchecked, not passing)",
      row["orientation_verified"] is None and row["is_short"] is None)

print(f"\n{ok} passed, {fail} failed")
sys.exit(1 if fail else 0)
