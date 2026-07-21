"""Candidate: the one shape every platform normalizes into."""
from __future__ import annotations

import re
from dataclasses import dataclass, field, asdict
from datetime import date, datetime
from typing import Any


# Channels whose uploads are re-hosts of other people's footage. Clearance
# problem and usually a quality problem. Matched case-insensitively as substrings.
COMPILATION_MARKERS = (
    "compilation", "top 10", "top ten", "best of", "#shorts compilation",
    "scammers get", "scammer gets destroyed", "funniest", "try not to",
)

# Rough affiliate call-letter pattern: KXAS, WFAA, ABC7, NBC 5, FOX13, News 4
AFFILIATE_RE = re.compile(
    r"\b([KW][A-Z]{2,3})\b|\b(ABC|NBC|CBS|FOX)\s?-?\s?\d{1,2}\b|\bNews\s?\d{1,2}\b",
    re.I,
)


@dataclass
class Candidate:
    """One harvested clip. Metadata only, no video bytes."""

    platform: str
    url: str
    video_id: str
    title: str
    beat_id: str
    query_that_found_it: str
    register: str

    thumbnail_url: str | None = None
    duration: int | None = None          # seconds
    published: date | None = None
    views: int | None = None
    uploader: str | None = None
    uploader_id: str | None = None

    # Populated by dedupe, not by the fetcher.
    rank: int | None = None              # position in the result page
    duplicate_of: str | None = None      # video_id of the kept record
    also_found_by: list[str] = field(default_factory=list)

    # ---- derived signals the grader reads -------------------------------

    @property
    def is_affiliate(self) -> bool:
        return bool(self.uploader and AFFILIATE_RE.search(self.uploader))

    @property
    def looks_like_compilation(self) -> bool:
        hay = f"{self.title} {self.uploader or ''}".lower()
        return any(m in hay for m in COMPILATION_MARKERS)

    def to_row(self) -> dict[str, Any]:
        d = asdict(self)
        d["published"] = self.published.isoformat() if self.published else None
        d["also_found_by"] = "|".join(self.also_found_by)
        d["is_affiliate"] = self.is_affiliate
        d["looks_like_compilation"] = self.looks_like_compilation
        return d


def _parse_upload_date(raw: Any) -> date | None:
    """yt-dlp gives YYYYMMDD, or a unix timestamp, or nothing."""
    if not raw:
        return None
    s = str(raw)
    if s.isdigit() and len(s) == 8:
        try:
            return datetime.strptime(s, "%Y%m%d").date()
        except ValueError:
            return None
    if s.isdigit():                      # timestamp
        try:
            return datetime.fromtimestamp(int(s)).date()
        except (ValueError, OSError):
            return None
    return None


def _best_thumbnail(entry: dict) -> str | None:
    """Flat-playlist entries carry a thumbnails list, sometimes a bare url."""
    if entry.get("thumbnail"):
        return entry["thumbnail"]
    thumbs = entry.get("thumbnails") or []
    if not thumbs:
        vid = entry.get("id")
        return f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg" if vid else None
    # widest wins; Airtable renders the attachment so bigger is better
    best = max(thumbs, key=lambda t: (t.get("width") or 0, t.get("height") or 0))
    return best.get("url")


def from_ytdlp(
    entry: dict,
    *,
    beat_id: str,
    query: str,
    register: str,
    rank: int | None = None,
) -> Candidate | None:
    """Normalize one `--flat-playlist --dump-json` entry.

    Returns None for entries with no usable id, which yt-dlp emits for
    playlists and the occasional dead result.
    """
    vid = entry.get("id")
    if not vid:
        return None

    url = entry.get("url") or entry.get("webpage_url") or f"https://www.youtube.com/watch?v={vid}"

    duration = entry.get("duration")
    if duration is not None:
        try:
            duration = int(float(duration))
        except (TypeError, ValueError):
            duration = None

    views = entry.get("view_count")
    if views is not None:
        try:
            views = int(views)
        except (TypeError, ValueError):
            views = None

    return Candidate(
        platform="youtube",
        url=url,
        video_id=vid,
        title=(entry.get("title") or "").strip(),
        beat_id=beat_id,
        query_that_found_it=query,
        register=register,
        thumbnail_url=_best_thumbnail(entry),
        duration=duration,
        published=_parse_upload_date(entry.get("upload_date") or entry.get("timestamp")),
        views=views,
        uploader=(entry.get("uploader") or entry.get("channel") or "").strip() or None,
        uploader_id=entry.get("channel_id") or entry.get("uploader_id"),
        rank=rank,
    )
