"""Offline tests. Everything except the network call is covered."""
import sys, tempfile, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rossen_harvest.candidates import Candidate, from_ytdlp, _parse_upload_date
from rossen_harvest.dedupe import dedupe, dedupe_by_beat, title_similarity, normalize_title
from rossen_harvest.cache import Cache

ok = fail = 0
def check(label, cond):
    global ok, fail
    if cond: ok += 1; print(f"  PASS  {label}")
    else:    fail += 1; print(f"  FAIL  {label}")

print("\n-- normalization from yt-dlp shape --")
entry = {
    "id": "I3667lq1L2o",
    "title": "Retired police officer loses nearly $10,000 in PayPal scam",
    "duration": 184.0,
    "view_count": "45210",
    "upload_date": "20250428",
    "channel": "WFAA",
    "channel_id": "UCxyz",
    "thumbnails": [{"url": "http://a/small.jpg", "width": 120, "height": 90},
                   {"url": "http://a/big.jpg", "width": 1280, "height": 720}],
}
c = from_ytdlp(entry, beat_id="05-06-b03", query="retired officer scammed", register="news", rank=3)
check("video_id parsed", c.video_id == "I3667lq1L2o")
check("duration coerced to int", c.duration == 184)
check("views coerced to int", c.views == 45210)
check("upload_date parsed", c.published.isoformat() == "2025-04-28")
check("widest thumbnail chosen", c.thumbnail_url == "http://a/big.jpg")
check("affiliate detected (WFAA)", c.is_affiliate is True)
check("not flagged compilation", c.looks_like_compilation is False)
check("rank retained", c.rank == 3)

check("no id -> None", from_ytdlp({"title": "x"}, beat_id="b", query="q", register="news") is None)
check("thumbnail fallback built", from_ytdlp(
    {"id": "abc12345678", "title": "t"}, beat_id="b", query="q", register="news"
).thumbnail_url.endswith("abc12345678/hqdefault.jpg"))

print("\n-- compilation / slop detection --")
for t in ["Top 10 Scams of 2025", "SCAMMERS GET DESTROYED #47", "Best Of Scam Calls"]:
    check(f"rejects {t!r}", from_ytdlp(
        {"id": "x"*11, "title": t}, beat_id="b", query="q", register="news"
    ).looks_like_compilation)
check("keeps a real affiliate title", not from_ytdlp(
    {"id": "y"*11, "title": "Local woman loses life savings in romance scam"},
    beat_id="b", query="q", register="news").looks_like_compilation)

print("\n-- title similarity on real wire-package collisions --")
a = "Elderly couple loses $850,000 in FBI impersonation scam"
b = "ABC7 | Elderly couple loses $850,000 in FBI impersonation scam"
d = "WFAA-TV Exclusive: Elderly couple loses $850,000 in FBI impersonation scam"
e = "Woman loses $600,000 to fake federal agents"
check(f"station prefix collapses ({title_similarity(a,b):.2f})", title_similarity(a, b) >= 0.86)
check(f"call letters + boilerplate collapse ({title_similarity(a,d):.2f})", title_similarity(a, d) >= 0.86)
check(f"different story stays separate ({title_similarity(a,e):.2f})", title_similarity(a, e) < 0.86)

print("\n-- dedupe --")
from datetime import date
def mk(vid, title, reg, q, pub, views=0, up="Chan", rank=1, beat="b1"):
    return Candidate(platform="youtube", url=f"https://youtu.be/{vid}", video_id=vid,
                     title=title, beat_id=beat, query_that_found_it=q, register=reg,
                     published=pub, views=views, uploader=up, rank=rank)

same = [mk("aaa", a, "news", "q1", date(2025,1,5), rank=4),
        mk("aaa", a, "victim", "q2", date(2025,1,5), rank=9),
        mk("aaa", a, "anchor", "q3", date(2025,1,5), rank=2)]
kept = dedupe(same)
check("same id collapses to one", len(kept) == 1)
check("all three registers remembered", len(kept[0].also_found_by) == 3)
check("best rank kept", kept[0].rank == 2)

wire = [mk("bbb", a, "news", "q1", date(2025,3,10), up="ABC7"),
        mk("ccc", b, "news", "q2", date(2025,3,8),  up="WFAA"),
        mk("ddd", d, "news", "q3", date(2025,3,12), up="KXAS"),
        mk("eee", e, "news", "q4", date(2025,3,9),  up="NBC 5")]
kept = dedupe(wire)
check("wire package collapses to 2 stories", len(kept) == 2)
survivor = next(k for k in kept if title_similarity(k.title, a) > 0.8)
check("earliest upload survived (clearance)", survivor.published == date(2025,3,8))
check("merged registers onto survivor", len(survivor.also_found_by) >= 2)

cross = [mk("f", "same story", "news", "q", date(2025,1,1), beat="b1"),
         mk("g", "same story", "news", "q", date(2025,1,1), beat="b2")]
check("different beats not collapsed", len(dedupe_by_beat(cross)) == 2)

print("\n-- cache --")
with tempfile.TemporaryDirectory() as td:
    cache = Cache(os.path.join(td, "t.db"))
    check("cold miss", cache.get_raw("ytsearch30:x") is None)
    cache.put_raw("ytsearch30:x", [{"id": "1"}, {"id": "2"}])
    check("warm hit", len(cache.get_raw("ytsearch30:x")) == 2)
    cache.save_candidates(kept)
    check("candidates persisted", cache.stats()["candidates"] == len(kept))
    stale = Cache(os.path.join(td, "t.db"), ttl=-1)
    check("ttl expiry respected", stale.get_raw("ytsearch30:x") is None)

print("\n-- url id extraction --")
from rossen_harvest.__main__ import youtube_id
for u, want in [("https://www.youtube.com/watch?v=I3667lq1L2o", "I3667lq1L2o"),
                ("https://youtu.be/5NwyEB0zZqs", "5NwyEB0zZqs"),
                ("https://www.youtube.com/shorts/fTMUnn_LLgA", "fTMUnn_LLgA"),
                ("https://www.tiktok.com/@x/video/123", None),
                ("https://www.today.com/video/eu-fines-temu", None)]:
    check(f"{u[:45]:<45} -> {want}", youtube_id(u) == want)

print(f"\n{'='*50}\n{ok} passed, {fail} failed\n{'='*50}")
sys.exit(1 if fail else 0)
