"""Offline tests for the Brave backend. Normalization and routing only,
no network call."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rossen_harvest.brave import (
    detect_platform_and_id, from_brave, _parse_date, _parse_hms, _strip_tags,
)
from rossen_harvest.dedupe import dedupe
from rossen_harvest.candidates import Candidate, from_ytdlp

ok = fail = 0
def check(label, cond):
    global ok, fail
    if cond: ok += 1; print(f"  PASS  {label}")
    else:    fail += 1; print(f"  FAIL  {label}")

print("\n-- platform + id detection from url --")
cases = [
    ("https://www.youtube.com/watch?v=VlXGf6gz9BQ", "youtube", "VlXGf6gz9BQ"),
    ("https://youtu.be/5NwyEB0zZqs", "youtube", "5NwyEB0zZqs"),
    ("https://www.youtube.com/shorts/fTMUnn_LLgA", "youtube", "fTMUnn_LLgA"),
    ("https://www.tiktok.com/@user/video/7360012345678", "tiktok", "7360012345678"),
    ("https://www.instagram.com/reel/C9abcDEF/", "instagram", "C9abcDEF"),
    ("https://www.instagram.com/p/C9abcDEF/", "instagram", "C9abcDEF"),
    ("https://x.com/user/status/1790012345", "x", "1790012345"),
    ("https://twitter.com/user/status/1790012345", "x", "1790012345"),
    ("https://www.reddit.com/r/scams/comments/1abc2de/title/", "reddit", "1abc2de"),
]
for url, plat, vid in cases:
    p, i = detect_platform_and_id(url)
    check(f"{plat:9s} {url[:46]}", p == plat and i == vid)

# non-post URLs become stable news_web hashes
p1, i1 = detect_platform_and_id("https://www.today.com/video/eu-fines-temu")
p2, i2 = detect_platform_and_id("https://www.today.com/video/eu-fines-temu")
check("news_web platform for a plain article", p1 == "news_web")
check("news_web id is stable across calls", i1 == i2)
check("different url -> different news_web id",
      detect_platform_and_id("https://abcnews.com/x")[1] != i1)

print("\n-- duration + date parsing --")
check("M:SS -> seconds", _parse_hms("2:15") == 135)
check("H:MM:SS -> seconds", _parse_hms("1:02:03") == 3723)
check("garbage duration -> None", _parse_hms("live") is None)
check("None duration -> None", _parse_hms(None) is None)
check("ISO page_age parsed", _parse_date("2025-02-26T01:02:08").isoformat() == "2025-02-26")
check("human age parsed", _parse_date("February 26, 2025").isoformat() == "2025-02-26")
check("empty date -> None", _parse_date("") is None)
check("strip bold tags from title", _strip_tags("gold <strong>bar</strong> scam") == "gold bar scam")

print("\n-- from_brave normalization (web result shape) --")
web = {
    "url": "https://abcnews.com/US/gold-grifters/story?id=119147460",
    "title": "'Gold Grifters': Inside the growing scam - ABC News",
    "description": "exclusive phone interview",
    "page_age": "2025-02-26T01:02:08",
    "thumbnail": {"src": "https://imgs/small", "original": "https://i.abcnewsfe.com/big.jpg"},
    "profile": {"name": "ABC News", "long_name": "abcnews.com"},
}
c = from_brave(web, beat_id="b01", query="gold bar scam victim", register="news", rank=2)
check("web -> news_web platform", c.platform == "news_web")
check("uploader from profile.name", c.uploader == "ABC News")
check("widest thumbnail preferred (original)", c.thumbnail_url == "https://i.abcnewsfe.com/big.jpg")
check("published parsed from page_age", c.published.isoformat() == "2025-02-26")
check("register + rank retained", c.register == "news" and c.rank == 2)

print("\n-- from_brave normalization (video result shape) --")
video = {
    "url": "https://www.youtube.com/watch?v=VlXGf6gz9BQ",
    "title": "Don't let Grandma fall for this TikTok scam - YouTube",
    "age": "October 4, 2025",
    "thumbnail": {"src": "https://i.ytimg.com/vi/VlXGf6gz9BQ/mq.jpg"},
    "video": {"duration": "22:15", "creator": "bunni", "author": {"name": "bunni"}},
}
c = from_brave(video, beat_id="b02", query="grandma gold scam", register="platform", rank=1)
check("youtube URL from Brave tagged youtube", c.platform == "youtube")
check("native youtube id extracted", c.video_id == "VlXGf6gz9BQ")
check("duration from nested video.duration", c.duration == 1335)
check("uploader from video.creator", c.uploader == "bunni")

check("no url -> None", from_brave({"title": "x"}, beat_id="b", query="q", register="news") is None)

print("\n-- cross-backend dedupe: same youtube clip from yt-dlp and Brave --")
yt = from_ytdlp(
    {"id": "VlXGf6gz9BQ", "title": "Grandma TikTok scam", "channel": "bunni",
     "upload_date": "20251004"},
    beat_id="b02", query="grandma scam", register="news", rank=4,
)
br = from_brave(video, beat_id="b02", query="grandma gold scam", register="platform", rank=1)
kept = dedupe([yt, br])
check("same youtube video collapses to one across backends", len(kept) == 1)
check("both registers remembered on survivor", len(kept[0].also_found_by) == 2)

print(f"\n{'='*50}\n{ok} passed, {fail} failed\n{'='*50}")
sys.exit(1 if fail else 0)
