"""YouTube search via yt-dlp. Metadata and thumbnails only, no video bytes.

`--flat-playlist --dump-json` against `ytsearch30:` returns title, channel,
duration, views, upload date, thumbnail and id without touching the media.
This is the highest-yield platform for the show, roughly 70% of what airs.

Every platform backend implements `search(query, limit) -> list[dict]` and
MUST return [] on failure rather than raising. A broken scraper degrades
the run, it does not kill it.
"""
from __future__ import annotations

import concurrent.futures as cf
import logging
import random
import time

from yt_dlp import YoutubeDL

from .cache import Cache
from .candidates import Candidate, from_ytdlp

log = logging.getLogger(__name__)

_YDL_OPTS = {
    "quiet": True,
    "no_warnings": True,
    "extract_flat": True,     # never resolve the video page
    "skip_download": True,
    "ignoreerrors": True,
    "socket_timeout": 30,
}

DEFAULT_LIMIT = 30
DEFAULT_CONCURRENCY = 5       # higher and YouTube starts throttling


class YouTubeBackend:
    platform = "youtube"

    def __init__(self, cache: Cache | None = None, limit: int = DEFAULT_LIMIT):
        self.cache = cache
        self.limit = limit

    def _search_key(self, query: str) -> str:
        return f"ytsearch{self.limit}:{query}"

    def search(self, query: str, limit: int | None = None) -> list[dict]:
        key = self._search_key(query)

        if self.cache:
            hit = self.cache.get_raw(key)
            if hit is not None:
                log.debug("cache hit: %s", query)
                return hit

        try:
            with YoutubeDL(_YDL_OPTS) as ydl:
                info = ydl.extract_info(key, download=False)
            entries = [e for e in (info or {}).get("entries", []) if e]
        except Exception as exc:                      # noqa: BLE001
            log.warning("youtube search failed for %r: %s", query, exc)
            return []

        if self.cache:
            self.cache.put_raw(key, entries)
        return entries


def harvest_beat(
    beat: dict,
    backend: YouTubeBackend,
    *,
    concurrency: int = DEFAULT_CONCURRENCY,
    jitter: tuple[float, float] = (0.2, 0.8),
) -> list[Candidate]:
    """Run every query for one beat and return normalized candidates.

    `beat` is the query-generator output: beat_id plus a `queries` dict
    of register -> list of query strings. Orientation is a hard filter
    upstream, so if this beat is vertical it should not reach here.
    """
    beat_id = beat["beat_id"]
    jobs: list[tuple[str, str]] = [
        (register, q)
        for register, queries in beat.get("queries", {}).items()
        for q in queries
    ]
    if not jobs:
        return []

    out: list[Candidate] = []

    def run(job: tuple[str, str]) -> list[Candidate]:
        register, query = job
        time.sleep(random.uniform(*jitter))
        entries = backend.search(query)
        cands = []
        for rank, entry in enumerate(entries, start=1):
            c = from_ytdlp(
                entry, beat_id=beat_id, query=query, register=register, rank=rank
            )
            if c:
                cands.append(c)
        return cands

    with cf.ThreadPoolExecutor(max_workers=concurrency) as pool:
        for result in pool.map(run, jobs):
            out.extend(result)

    log.info("beat %s: %d queries -> %d raw candidates", beat_id, len(jobs), len(out))
    return out
