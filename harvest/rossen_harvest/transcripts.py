"""Captions without downloading video.

yt-dlp fetches auto-generated subtitles as a separate small file. This
replaces Whisper in the discovery path: no model download, no ffmpeg
dependency, no GPU, no per-clip transcode. Roughly a second per clip
instead of thirty.

What you give up: caption chunks are 1-3s granular rather than word
level, and auto-captions have no speaker separation, so a news package
reads as one undifferentiated stream. Pass two of the grader is judging
tone, authenticity, quality and fit, none of which need word precision.
Pad the resulting timecodes and let the editor nudge.

If a clip has captions disabled (5-10% of the time) this returns None
and the grader should demote rather than guess.
"""
from __future__ import annotations

import concurrent.futures as cf
import html
import io
import json
import logging
import re
import urllib.request
from dataclasses import dataclass

from yt_dlp import YoutubeDL

log = logging.getLogger(__name__)

# Pad applied when handing timecodes to the editor. Caption boundaries are
# coarse, so enter slightly early and leave slightly late; trimming down is
# cheap, discovering you clipped the first syllable is not.
PAD_IN = 1.0
PAD_OUT = 1.5

_TS = re.compile(
    r"(\d{2}):(\d{2}):(\d{2})[.,](\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2})[.,](\d{3})"
)
_TAG = re.compile(r"<[^>]+>")


@dataclass
class Cue:
    start: float
    end: float
    text: str

    @property
    def timecode(self) -> str:
        m, s = divmod(int(self.start), 60)
        return f"{m}:{s:02d}"


@dataclass
class Transcript:
    video_id: str
    cues: list[Cue]
    source: str                      # "auto" | "manual" | "none"

    @property
    def duration(self) -> float:
        return self.cues[-1].end if self.cues else 0.0

    def full_text(self) -> str:
        return " ".join(c.text for c in self.cues)

    def as_prompt(self, every: int = 1) -> str:
        """Timestamped transcript for the grader. One line per cue."""
        return "\n".join(
            f"[{c.timecode}] {c.text}" for c in self.cues[::every] if c.text
        )

    def find(self, phrase: str) -> Cue | None:
        """Locate a phrase. This is how an outcue gets verified."""
        norm = re.sub(r"[^\w\s]", "", phrase.lower()).strip()
        if not norm:
            return None
        for c in self.cues:
            if norm in re.sub(r"[^\w\s]", "", c.text.lower()):
                return c
        # fall back to a sliding window across cue boundaries
        words = norm.split()
        for i, c in enumerate(self.cues):
            window = " ".join(
                re.sub(r"[^\w\s]", "", x.text.lower())
                for x in self.cues[i : i + 4]
            )
            if norm in window:
                return c
        return None

    def segment(self, start: float, end: float) -> tuple[str, str, str]:
        """Padded in/out plus the verbatim outcue text at the out point."""
        a = max(0.0, start - PAD_IN)
        b = min(self.duration, end + PAD_OUT) if self.duration else end + PAD_OUT
        tail = [c for c in self.cues if c.start <= end]
        outcue = tail[-1].text if tail else ""
        return _fmt(a), _fmt(b), outcue


def _fmt(sec: float) -> str:
    m, s = divmod(int(sec), 60)
    return f"{m}:{s:02d}"


def parse_vtt(raw: str) -> list[Cue]:
    """Parse WebVTT or SRT. Auto-captions repeat lines for the rolling
    effect, so consecutive duplicates get collapsed."""
    cues: list[Cue] = []
    block_text: list[str] = []
    start = end = None

    def flush():
        nonlocal block_text, start, end
        if start is not None and block_text:
            text = _TAG.sub("", " ".join(block_text))
            text = html.unescape(re.sub(r"\s+", " ", text)).strip()
            if text and (not cues or cues[-1].text != text):
                cues.append(Cue(start, end, text))
        block_text = []

    for line in io.StringIO(raw):
        line = line.rstrip("\n")
        m = _TS.search(line)
        if m:
            flush()
            h1, m1, s1, ms1, h2, m2, s2, ms2 = (int(x) for x in m.groups())
            start = h1 * 3600 + m1 * 60 + s1 + ms1 / 1000
            end = h2 * 3600 + m2 * 60 + s2 + ms2 / 1000
            continue
        if not line.strip() or line.strip().isdigit() or line.startswith("WEBVTT"):
            if not line.strip():
                flush()
            continue
        if line.startswith(("Kind:", "Language:", "NOTE")):
            continue
        block_text.append(line.strip())
    flush()
    return cues


_SUB_OPTS = {
    "quiet": True,
    "no_warnings": True,
    "skip_download": True,
    "writesubtitles": True,
    "writeautomaticsub": True,
    "subtitleslangs": ["en", "en-US", "en-orig"],
    "socket_timeout": 30,
}


def fetch_transcript(video_id: str, *, cache=None) -> Transcript | None:
    """Metadata call only. No media bytes."""
    if cache is not None:
        hit = cache.get_raw(f"captions:{video_id}")
        if hit is not None:
            if not hit:
                return None
            return Transcript(video_id, [Cue(**c) for c in hit["cues"]], hit["source"])

    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        with YoutubeDL(_SUB_OPTS) as ydl:
            info = ydl.extract_info(url, download=False)
    except Exception as exc:                       # noqa: BLE001
        log.warning("caption lookup failed for %s: %s", video_id, exc)
        return None

    for key, source in (("subtitles", "manual"), ("automatic_captions", "auto")):
        tracks = (info or {}).get(key) or {}
        for lang in ("en", "en-US", "en-orig"):
            for fmt in tracks.get(lang, []):
                if fmt.get("ext") not in ("vtt", "srt"):
                    continue
                try:
                    with urllib.request.urlopen(fmt["url"], timeout=30) as r:
                        raw = r.read().decode("utf-8", "replace")
                except Exception as exc:           # noqa: BLE001
                    log.debug("caption download failed %s: %s", video_id, exc)
                    continue
                cues = parse_vtt(raw)
                if not cues:
                    continue
                t = Transcript(video_id, cues, source)
                if cache is not None:
                    cache.put_raw(f"captions:{video_id}", {
                        "source": source,
                        "cues": [{"start": c.start, "end": c.end, "text": c.text}
                                 for c in cues],
                    })
                return t

    log.info("no captions available for %s", video_id)
    if cache is not None:
        cache.put_raw(f"captions:{video_id}", {})
    return None


def fetch_many(video_ids: list[str], *, cache=None, concurrency: int = 6
               ) -> dict[str, Transcript | None]:
    out: dict[str, Transcript | None] = {}
    with cf.ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures = {pool.submit(fetch_transcript, v, cache=cache): v for v in video_ids}
        for fut in cf.as_completed(futures):
            vid = futures[fut]
            try:
                out[vid] = fut.result()
            except Exception:                      # noqa: BLE001
                out[vid] = None
    got = sum(1 for v in out.values() if v)
    log.info("captions: %d/%d clips", got, len(video_ids))
    return out
