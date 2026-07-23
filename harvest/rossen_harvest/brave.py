"""Brave Search backend. Web and video search via the Brave Search API.

Covers everything yt-dlp cannot reach on its own:

- **news_web** — network and affiliate video that lives on the outlet's
  own site rather than YouTube. The Temu fine clip aired off `today.com`;
  `authority_report` beats routinely resolve here.
- **vertical platforms** — TikTok, Instagram, X, Facebook, Reddit. Their
  search is closed to anonymous scraping, but their public post pages are
  indexed, and Brave returns them. This is the only search coverage
  vertical beats get; the YouTube backend skips them entirely.

Metadata only — url, title, description, thumbnail, age, and (for video
results) duration and creator. Never the media.

Requires `BRAVE_API_KEY` in the environment. Same contract as every
backend: `search(query, limit) -> list[dict]`, and it returns `[]` on any
failure rather than raising. A rate-limit or a network blip degrades the
run, it does not kill it.

Stdlib only, to match the rest of the package. No `requests`.
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import ssl
import threading
import time
from datetime import date, datetime
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

from .candidates import Candidate

log = logging.getLogger(__name__)

WEB_ENDPOINT = "https://api.search.brave.com/res/v1/web/search"
VIDEO_ENDPOINT = "https://api.search.brave.com/res/v1/videos/search"

DEFAULT_COUNT = 20            # Brave web/video hard-cap per request
FREE_TIER_INTERVAL = 1.1     # Brave free plan allows ~1 request/second

# The proxy CA in this environment, if present. Added to the default trust
# store so the API call verifies through the agent proxy without disabling
# TLS. Absent elsewhere, in which case the system store is used unchanged.
_CA_BUNDLE = "/root/.ccr/ca-bundle.crt"


def _ssl_context() -> ssl.SSLContext:
    ctx = ssl.create_default_context()
    bundle = os.environ.get("SSL_CERT_FILE") or _CA_BUNDLE
    if bundle and os.path.exists(bundle):
        try:
            ctx.load_verify_locations(bundle)
        except Exception:                                 # noqa: BLE001
            pass
    return ctx


_SSL = _ssl_context()

# Serialize API calls and space them out. Brave's free tier rate-limits at
# roughly one request per second; a thread pool would trip it instantly.
_rate_lock = threading.Lock()
_last_call = [0.0]


def _throttle(interval: float) -> None:
    with _rate_lock:
        wait = interval - (time.monotonic() - _last_call[0])
        if wait > 0:
            time.sleep(wait)
        _last_call[0] = time.monotonic()


# --------------------------------------------------------------------- backend

class BraveBackend:
    platform = "brave"

    def __init__(
        self,
        api_key: str,
        cache=None,
        limit: int = DEFAULT_COUNT,
        kind: str = "web",
        min_interval: float = FREE_TIER_INTERVAL,
    ):
        if kind not in ("web", "video"):
            raise ValueError("kind must be 'web' or 'video'")
        self.api_key = api_key
        self.cache = cache
        self.limit = min(limit, DEFAULT_COUNT)
        self.kind = kind
        self.endpoint = WEB_ENDPOINT if kind == "web" else VIDEO_ENDPOINT
        self.min_interval = min_interval

    def _search_key(self, query: str) -> str:
        return f"brave:{self.kind}:{self.limit}:{query}"

    def search(self, query: str, limit: int | None = None) -> list[dict]:
        key = self._search_key(query)

        if self.cache:
            hit = self.cache.get_raw(key)
            if hit is not None:
                log.debug("cache hit: %s", query)
                return hit

        try:
            entries = self._call(query)
        except Exception as exc:                          # noqa: BLE001
            log.warning("brave %s search failed for %r: %s", self.kind, query, exc)
            return []

        if self.cache:
            self.cache.put_raw(key, entries)
        return entries

    def _call(self, query: str) -> list[dict]:
        url = f"{self.endpoint}?{urlencode({'q': query, 'count': self.limit})}"
        req = Request(url, headers={
            "Accept": "application/json",
            "X-Subscription-Token": self.api_key,
        })

        for attempt in (1, 2):
            _throttle(self.min_interval)
            try:
                with urlopen(req, timeout=30, context=_SSL) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                break
            except HTTPError as exc:
                if exc.code == 429 and attempt == 1:      # rate limited, back off once
                    log.debug("brave 429, backing off")
                    time.sleep(2.0)
                    continue
                raise
            except URLError:
                raise
        else:
            return []

        if self.kind == "web":
            return (data.get("web") or {}).get("results", []) or []
        return data.get("results", []) or []


# ---------------------------------------------------------------- normalization

# Ordered: the first host pattern that matches wins, and it also names the
# platform so the grader and dedupe treat a Brave-found YouTube URL exactly
# like a yt-dlp one and collapse the two.
_ID_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("youtube", re.compile(r"(?:youtube\.com/(?:watch\?v=|shorts/|embed/)|youtu\.be/)([A-Za-z0-9_-]{11})")),
    ("tiktok", re.compile(r"tiktok\.com/[^/]+/video/(\d+)")),
    ("instagram", re.compile(r"instagram\.com/(?:reel|reels|p|tv)/([A-Za-z0-9_-]+)")),
    ("x", re.compile(r"(?:twitter|x)\.com/[^/]+/status/(\d+)")),
    ("facebook", re.compile(r"facebook\.com/(?:watch/?\?v=|reel/|[^/]+/videos/)(\d+)")),
    ("reddit", re.compile(r"reddit\.com/r/[^/]+/comments/([A-Za-z0-9]+)")),
]

_TAG_RE = re.compile(r"<[^>]+>")


def detect_platform_and_id(url: str) -> tuple[str, str]:
    """Name the destination platform and a stable id for one result URL.

    A post-bearing URL on a known platform yields that platform's native
    id, so the same clip found by two backends dedupes. Anything else is
    `news_web` with a hash of the URL, which is stable enough to dedupe a
    repeated web result across queries.
    """
    for platform, rx in _ID_PATTERNS:
        m = rx.search(url or "")
        if m:
            return platform, m.group(1)
    digest = hashlib.sha1((url or "").encode("utf-8")).hexdigest()[:15]
    return "news_web", f"u{digest}"


def _host(url: str) -> str:
    netloc = urlparse(url or "").netloc.lower()
    return netloc[4:] if netloc.startswith("www.") else netloc


def _strip_tags(text: str) -> str:
    return _TAG_RE.sub("", text or "").strip()


def _parse_date(raw) -> date | None:
    """Brave gives `page_age` as ISO, or `age` as 'February 26, 2025'."""
    if not raw:
        return None
    s = str(raw)
    try:
        return date.fromisoformat(s[:10])
    except ValueError:
        pass
    for fmt in ("%B %d, %Y", "%b %d, %Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def _parse_hms(raw) -> int | None:
    """Video duration comes as 'M:SS' or 'H:MM:SS'."""
    if not raw or not isinstance(raw, str) or ":" not in raw:
        return None
    parts = raw.split(":")
    try:
        nums = [int(p) for p in parts]
    except ValueError:
        return None
    secs = 0
    for n in nums:
        secs = secs * 60 + n
    return secs


def _coerce_int(raw) -> int | None:
    if raw is None:
        return None
    try:
        return int(raw)
    except (TypeError, ValueError):
        return None


def from_brave(
    entry: dict,
    *,
    beat_id: str,
    query: str,
    register: str,
    rank: int | None = None,
) -> Candidate | None:
    """Normalize one Brave web or video result into a Candidate.

    Same signature as `from_ytdlp`, so `harvest_beat` drives either.
    """
    url = entry.get("url")
    if not url:
        return None

    platform, vid = detect_platform_and_id(url)
    video = entry.get("video") or {}
    profile = entry.get("profile") or {}
    thumb = entry.get("thumbnail") or {}
    author = (video.get("author") or {}) if isinstance(video, dict) else {}

    uploader = (
        video.get("creator")
        or author.get("name")
        or profile.get("name")
        or profile.get("long_name")
        or _host(url)
        or None
    )

    return Candidate(
        platform=platform,
        url=url,
        video_id=vid,
        title=_strip_tags(entry.get("title") or ""),
        beat_id=beat_id,
        query_that_found_it=query,
        register=register,
        thumbnail_url=(thumb.get("original") or thumb.get("src")),
        duration=_parse_hms(video.get("duration")),
        published=_parse_date(entry.get("page_age") or entry.get("age")),
        views=_coerce_int(entry.get("views") or video.get("views")),
        uploader=uploader,
        uploader_id=None,
        rank=rank,
    )
