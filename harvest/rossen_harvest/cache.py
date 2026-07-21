"""SQLite cache.

The eval gets re-run many times while tuning registers and the glossary.
There is no reason to re-hit YouTube for a query already scored, and
yt-dlp will rate-limit if you do. Cache is keyed on the exact query
string plus the search prefix, with a TTL.

Also stores candidates, so a harvest run is resumable and the Airtable
push can be retried without re-searching.
"""
from __future__ import annotations

import json
import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path

from .candidates import Candidate, from_ytdlp

DEFAULT_TTL = 14 * 24 * 3600     # two weeks

SCHEMA = """
CREATE TABLE IF NOT EXISTS query_cache (
    query       TEXT PRIMARY KEY,
    fetched_at  REAL NOT NULL,
    raw_json    TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS candidates (
    beat_id     TEXT NOT NULL,
    platform    TEXT NOT NULL,
    video_id    TEXT NOT NULL,
    url         TEXT,
    title       TEXT,
    uploader    TEXT,
    duration    INTEGER,
    published   TEXT,
    views       INTEGER,
    thumbnail_url TEXT,
    register    TEXT,
    query_that_found_it TEXT,
    also_found_by TEXT,
    rank        INTEGER,
    PRIMARY KEY (beat_id, platform, video_id)
);
CREATE INDEX IF NOT EXISTS idx_cand_beat ON candidates(beat_id);
"""


class Cache:
    def __init__(self, path: str | Path = "harvest.db", ttl: int = DEFAULT_TTL):
        self.path = str(path)
        self.ttl = ttl
        with self._conn() as c:
            c.executescript(SCHEMA)

    @contextmanager
    def _conn(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    # ---- query cache -------------------------------------------------

    def get_raw(self, query: str) -> list[dict] | None:
        with self._conn() as c:
            row = c.execute(
                "SELECT fetched_at, raw_json FROM query_cache WHERE query = ?",
                (query,),
            ).fetchone()
        if row is None:
            return None
        if time.time() - row["fetched_at"] > self.ttl:
            return None
        return json.loads(row["raw_json"])

    def put_raw(self, query: str, entries: list[dict]) -> None:
        with self._conn() as c:
            c.execute(
                "INSERT OR REPLACE INTO query_cache (query, fetched_at, raw_json) "
                "VALUES (?, ?, ?)",
                (query, time.time(), json.dumps(entries)),
            )

    # ---- candidates --------------------------------------------------

    def save_candidates(self, candidates: list[Candidate]) -> int:
        rows = [
            (
                c.beat_id, c.platform, c.video_id, c.url, c.title, c.uploader,
                c.duration, c.published.isoformat() if c.published else None,
                c.views, c.thumbnail_url, c.register, c.query_that_found_it,
                "|".join(c.also_found_by), c.rank,
            )
            for c in candidates
        ]
        with self._conn() as conn:
            conn.executemany(
                "INSERT OR REPLACE INTO candidates VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                rows,
            )
        return len(rows)

    def load_candidates(self, beat_id: str | None = None) -> list[dict]:
        sql = "SELECT * FROM candidates"
        args: tuple = ()
        if beat_id:
            sql += " WHERE beat_id = ?"
            args = (beat_id,)
        with self._conn() as c:
            return [dict(r) for r in c.execute(sql, args).fetchall()]

    def stats(self) -> dict:
        with self._conn() as c:
            q = c.execute("SELECT COUNT(*) n FROM query_cache").fetchone()["n"]
            n = c.execute("SELECT COUNT(*) n FROM candidates").fetchone()["n"]
            b = c.execute("SELECT COUNT(DISTINCT beat_id) n FROM candidates").fetchone()["n"]
        return {"cached_queries": q, "candidates": n, "beats": b}
