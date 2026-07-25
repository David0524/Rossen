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
    backend,
    *,
    concurrency: int = DEFAULT_CONCURRENCY,
    jitter: tuple[float, float] = (0.2, 0.8),
    normalize=from_ytdlp,
    registers: set[str] | None = None,
    cap: int | None = None,
) -> list[Candidate]:
    """Run a beat's queries through one backend and return normalized candidates.

    `beat` is the query-generator output: beat_id plus a `queries` dict
    of register -> list of query strings.

    `normalize` turns one raw backend entry into a Candidate; it defaults
    to the YouTube shape but any backend passes its own (see `from_brave`).
    `registers` restricts which registers run, so a backend can take only
    the registers it is good at. `cap` truncates the job list, which
    matters for rate-limited APIs where every query costs quota.

    Orientation is a hard filter upstream for the YouTube backend: a
    vertical beat should not reach it. Brave has no such restriction.
    """
    beat_id = beat["beat_id"]
    by_register: dict[str, list[str]] = {
        register: list(queries)
        for register, queries in beat.get("queries", {}).items()
        if (registers is None or register in registers) and queries
    }

    # Round-robin across registers rather than concatenating them, because
    # `cap` truncates and a flat concatenation starves whatever sorts last.
    # That is not hypothetical: when `shorts_web` was added it landed at the
    # tail and a cap of 8 meant it never ran at all.
    jobs: list[tuple[str, str]] = []
    for i in range(max((len(v) for v in by_register.values()), default=0)):
        for register, queries in by_register.items():
            if i < len(queries):
                jobs.append((register, queries[i]))

    if cap is not None:
        jobs = jobs[:cap]
    if not jobs:
        return []

    out: list[Candidate] = []

    def run(job: tuple[str, str]) -> list[Candidate]:
        register, query = job
        if jitter != (0, 0):
            time.sleep(random.uniform(*jitter))
        entries = backend.search(query)
        cands = []
        for rank, entry in enumerate(entries, start=1):
            c = normalize(
                entry, beat_id=beat_id, query=query, register=register, rank=rank
            )
            if c:
                cands.append(c)
        return cands

    with cf.ThreadPoolExecutor(max_workers=concurrency) as pool:
        for result in pool.map(run, jobs):
            out.extend(result)

    log.info("beat %s: %d queries via %s -> %d raw candidates",
             beat_id, len(jobs), getattr(backend, "platform", "?"), len(out))
    return out
