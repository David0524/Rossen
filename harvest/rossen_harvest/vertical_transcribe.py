"""Whisper transcription for vertical platforms that ship no captions.

TikTok, Instagram Reels and native X video carry no subtitle track at all —
`transcripts.py`'s caption fetch always returns None for them. That is a real
gap, not a rounding error: without a transcript there is no way to verify an
outcue, and an unverified outcue is exactly the thing this pipeline refuses
to invent. This module closes it by downloading the clip and transcribing
the audio locally with faster-whisper (CTranslate2, CPU, no torch).

Produces the same `Transcript`/`Cue` shape as `transcripts.py`, so every
downstream consumer — `.find()` for outcue verification, `.segment()` for
padded in/out, `.as_prompt()` for the grader — works identically whether the
transcript came from YouTube captions or from Whisper. The only visible
difference is `Transcript.source == "whisper"`.

## What this costs that captions don't

- Downloads real media bytes. Captions-only (`transcripts.py`) never does.
- CPU transcription time, not a metadata call: roughly real-time-or-faster
  on the tiny/base models, i.e. a 60s clip takes single-digit seconds, not
  the ~1s a caption fetch takes. Budget for it — this is why it's a
  pass-two-only step, run on the handful of clips that survive triage, not
  every raw candidate.
- Word-level timing is approximate (Whisper's own segment boundaries), not
  platform-authored. Same padding discipline as captions applies.

## TikTok download gotchas, confirmed against a live clip

- **Do not let yt-dlp auto-pick TikTok's default format.** Several of
  TikTok's served variants (notably the H.265/`bytevc1` renditions) are
  video-only with no audio stream at all, despite top-level JSON metadata
  claiming `acodec: aac`. Request the `download` format id explicitly (the
  watermarked H.264 rendition) or fall back through an explicit format list
  that is confirmed to carry audio -- see `AUDIO_SAFE_FORMAT` below.
- **Do not enable `curl-cffi`/`--impersonate`** unless you have confirmed it
  actually improves reliability in your environment. In this sandbox it made
  things *worse* -- TikTok's TLS handshake reset immediately with `curl-cffi`
  installed, whereas plain yt-dlp (no impersonation target) resolved
  metadata and downloaded cleanly. yt-dlp's own impersonation warning is not
  itself a failure; only add the dependency if plain requests are actually
  being blocked.
- yt-dlp's built-in `-x --audio-format wav` postprocessor can fail
  (`unable to obtain file audio codec with ffprobe`) on some TikTok
  containers even when the download itself succeeds. This module downloads
  the muxed file and extracts audio with a direct `ffmpeg` call instead of
  relying on the postprocessor, which sidesteps that failure.
"""
from __future__ import annotations

import json
import logging
import re
import subprocess
import tempfile
from pathlib import Path

from .cache import Cache
from .transcripts import Cue, Transcript

log = logging.getLogger(__name__)

# Confirmed against a live download: the plain "download" format id is the
# watermarked H.264 rendition and reliably carries an AAC audio stream.
# Fall through to a couple of other formats known to be audio+video muxed,
# then to yt-dlp's own "best" as a last resort.
AUDIO_SAFE_FORMAT = "download/best[acodec!=none]/best"

_TIKTOK_URL = re.compile(
    r"tiktok\.com/@[^/]+/video/(\d+)|tiktok\.com/@[^/]+/photo/(\d+)"
)

# Every vertical surface this pipeline can reach, not just TikTok. Each entry
# maps a platform tag to the pattern that pulls its stable id out of a URL.
#
# Why this matters beyond tidiness: the id is the cache key. A URL that does
# not match any pattern falls back to caching on the raw URL string, so the
# same clip arriving with different tracking params (`?igsh=`, `?is_from_webapp`,
# a share-link suffix) caches two, three, four times and re-downloads and
# re-transcribes on every variant. Whisper is the expensive step in this
# pipeline; paying for it repeatedly on one clip is the exact cost the cache
# exists to prevent.
_VERTICAL_URL_PATTERNS = (
    ("tiktok",    _TIKTOK_URL),
    ("shorts",    re.compile(r"youtube\.com/shorts/([A-Za-z0-9_-]{11})")),
    ("instagram", re.compile(r"instagram\.com/(?:reel|reels|p|tv)/([A-Za-z0-9_-]+)")),
    ("x",         re.compile(r"(?:twitter|x)\.com/[^/]+/status/(\d+)")),
    ("facebook",  re.compile(r"facebook\.com/(?:reel/(\d+)|watch/?\?v=(\d+))")),
)


def tiktok_id(url: str) -> str | None:
    """TikTok-only id. Kept for the existing callers and tests that name it."""
    m = _TIKTOK_URL.search(url or "")
    if not m:
        return None
    return m.group(1) or m.group(2)


def vertical_id(url: str) -> tuple[str, str] | None:
    """`(platform, id)` for any supported vertical URL, else None.

    Prefer this over `tiktok_id` for anything cache-key shaped -- it covers
    Shorts, Reels, X and Facebook video as well, which `tiktok_id` silently
    returns None for.
    """
    for platform, pat in _VERTICAL_URL_PATTERNS:
        m = pat.search(url or "")
        if m:
            vid = next((g for g in m.groups() if g), None)
            if vid:
                return platform, vid
    return None


def _run(cmd: list[str], timeout: int) -> subprocess.CompletedProcess:
    """CLI subprocess, never in-process. See module docstring: this is not
    the macOS fork-crash workaround (that's an Apple/Network.framework bug
    this environment doesn't have) but the same pattern is still the right
    default for a step that shells out to yt-dlp/ffmpeg -- sequential,
    predictable failure, no thread-pool interaction with a subprocess-heavy
    library."""
    return subprocess.run(
        cmd, capture_output=True, text=True, timeout=timeout, check=False
    )


def download_audio(url: str, out_wav: Path, *, timeout: int = 120) -> bool:
    """Download a vertical clip and extract 16kHz mono audio to `out_wav`.

    Two subprocess calls, both CLI, both sequential: yt-dlp downloads the
    muxed file, ffmpeg extracts audio directly rather than trusting
    yt-dlp's postprocessor (see module docstring for why). Returns False on
    any failure; never raises, matching every other backend's contract.
    """
    with tempfile.TemporaryDirectory() as td:
        muxed = Path(td) / "src.%(ext)s"
        r = _run(
            [
                "yt-dlp", "-f", AUDIO_SAFE_FORMAT,
                "-o", str(muxed),
                "--no-warnings", "--quiet",
                url,
            ],
            timeout=timeout,
        )
        if r.returncode != 0:
            log.warning("vertical download failed for %s: %s", url, r.stderr[-500:])
            return False

        srcs = list(Path(td).glob("src.*"))
        if not srcs:
            log.warning("vertical download produced no file for %s", url)
            return False
        src = srcs[0]

        r = _run(
            [
                "ffmpeg", "-y", "-i", str(src),
                "-vn", "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le",
                str(out_wav),
            ],
            timeout=timeout,
        )
        if r.returncode != 0 or not out_wav.exists():
            log.warning("audio extraction failed for %s: %s", url, r.stderr[-500:])
            return False
        return True


_MODEL = None
_MODEL_SIZE = None


def _get_model(model_size: str):
    """Lazy singleton. Loading the model is the expensive part (~5s for
    tiny.en); do it once per process, not once per clip."""
    global _MODEL, _MODEL_SIZE
    if _MODEL is None or _MODEL_SIZE != model_size:
        from faster_whisper import WhisperModel
        _MODEL = WhisperModel(model_size, device="cpu", compute_type="int8")
        _MODEL_SIZE = model_size
    return _MODEL


def transcribe_audio(wav_path: Path, *, model_size: str = "base.en") -> list[Cue]:
    """Whisper transcription -> Cue list, same shape captions produce."""
    model = _get_model(model_size)
    segments, _info = model.transcribe(str(wav_path), beam_size=1)
    cues = []
    for seg in segments:
        text = seg.text.strip()
        if text:
            cues.append(Cue(seg.start, seg.end, text))
    return cues


def fetch_vertical_transcript(
    url: str,
    *,
    cache: Cache | None = None,
    model_size: str = "base.en",
    timeout: int = 120,
) -> Transcript | None:
    """Download + transcribe one vertical clip. Cached like any other
    query so re-grading the same shortlist never re-downloads or re-runs
    Whisper. Returns None on any failure -- never raises."""
    ident = vertical_id(url)
    vid = f"{ident[0]}:{ident[1]}" if ident else url
    cache_key = f"whisper:{model_size}:{vid}"

    if cache is not None:
        hit = cache.get_raw(cache_key)
        if hit is not None:
            if not hit:
                return None
            return Transcript(vid, [Cue(**c) for c in hit["cues"]], "whisper")

    with tempfile.TemporaryDirectory() as td:
        wav = Path(td) / "audio.wav"
        if not download_audio(url, wav, timeout=timeout):
            if cache is not None:
                cache.put_raw(cache_key, {})
            return None
        try:
            cues = transcribe_audio(wav, model_size=model_size)
        except Exception as exc:                       # noqa: BLE001
            log.warning("whisper transcription failed for %s: %s", url, exc)
            if cache is not None:
                cache.put_raw(cache_key, {})
            return None

    if not cues:
        if cache is not None:
            cache.put_raw(cache_key, {})
        return None

    if cache is not None:
        cache.put_raw(cache_key, {
            "cues": [{"start": c.start, "end": c.end, "text": c.text} for c in cues],
        })
    return Transcript(vid, cues, "whisper")


def fetch_many_vertical(
    urls: list[str],
    *,
    cache: Cache | None = None,
    model_size: str = "base.en",
) -> dict[str, Transcript | None]:
    """Sequential, deliberately. Whisper is CPU-bound and downloads share
    one egress path; there is no throughput win from threading this, and
    threading a subprocess-heavy step is exactly the pattern the macOS
    fork-crash gotcha warns against reintroducing on principle, even where
    this environment doesn't hit that specific bug."""
    out: dict[str, Transcript | None] = {}
    for url in urls:
        out[url] = fetch_vertical_transcript(url, cache=cache, model_size=model_size)
    got = sum(1 for v in out.values() if v)
    log.info("vertical transcripts: %d/%d clips", got, len(urls))
    return out
