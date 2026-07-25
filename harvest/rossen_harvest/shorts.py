"""YouTube Shorts: format gate and pixel-level orientation verification.

Two defects surfaced by the 2026-07-25 vertical smoke test, both fixed here.

**1. The duration ceiling was stale.** The pipeline gated Shorts on
`duration < 60`, which was YouTube's limit until October 2024. It is now
three minutes. The best YouTube candidate for the gift-card beat — CTV News
`ZVQPxS16At0`, genuinely served at `/shorts/`, 119 seconds — was silently
dropped by that filter. `SHORTS_MAX_DURATION` is now 180, and duration is
demoted to a cheap pre-filter: the authoritative test is whether the
`/shorts/` URL actually resolves (`is_short`).

**2. Duration is not an orientation signal.** This is the vertical
postmortem bug. A sub-75-second YouTube video was asserted vertical by
duration alone and a 1920x1080 landscape clip shipped against a vertical
beat. The smoke test reproduced it four ways — a 25s clip at 1280x720, a
21s clip at 1280x720, a 58s Instagram *Reel* at 640x360 (which defeats
duration *and* platform-name inference at once), and a 540x960 vertical
that is not a Short at all. Across nine Shorts-dialect queries, *every*
sub-60s YouTube result was landscape: local-news packages dominate that
duration band and they are uniformly 16:9. Duration is not a weak proxy
for orientation on this material, it is anti-correlated.

So orientation is read from pixels, never inferred. `verify_orientation`
uses the original-aspect-ratio thumbnail, which YouTube publishes at
`oardefault.jpg` / `oar2.jpg` for any source that is not 16:9. A landscape
video has no `oar` variant at all, so a 404 is itself the answer. This
works when media bytes are unavailable — in the smoke-test environment
YouTube video was bot-walled and DRM-blocked while thumbnails served fine.
Verified in both directions against yt-dlp's format table: `_RTe-ddhxoY`
reads 540x960 by both methods, and landscape `PNjdcz3eG9o` 404s on `oar`
while yt-dlp reports 1280x720.

Everything here fails soft. A network problem returns "unknown", never a
guess, and never an exception into the harvest loop.
"""
from __future__ import annotations

import logging
import urllib.error
import urllib.request

log = logging.getLogger(__name__)

# YouTube raised the Shorts ceiling from 60s to 3 minutes in October 2024.
SHORTS_MAX_DURATION = 180
LEGACY_SHORTS_MAX_DURATION = 60      # what the pipeline used to gate on

_UA = "Mozilla/5.0 (compatible; rossen-harvest/1.0)"
_OAR_VARIANTS = ("oardefault", "oar2")

VERTICAL = "vertical"
LANDSCAPE = "landscape"
UNKNOWN = "unknown"


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Keep the 3xx instead of following it — the redirect *is* the signal."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def is_short(video_id: str, *, timeout: float = 15.0) -> bool | None:
    """Is this video served as a Short?

    `GET /shorts/<id>` returns 200 for a real Short. For an ordinary upload
    YouTube 3xx-redirects to `/watch?v=<id>`. That redirect is the whole
    test, and it is the only reliable one: duration cannot distinguish a
    119-second Short from a 119-second regular upload.

    Returns None when the network call fails, so callers can tell "not a
    Short" apart from "could not check".
    """
    url = f"https://www.youtube.com/shorts/{video_id}"
    opener = urllib.request.build_opener(_NoRedirect)
    req = urllib.request.Request(url, headers={"User-Agent": _UA})
    try:
        with opener.open(req, timeout=timeout) as r:
            return r.status == 200
    except urllib.error.HTTPError as e:
        if 300 <= e.code < 400:
            return False          # redirected to /watch — a normal upload
        if e.code == 404:
            return False
        log.debug("is_short(%s): HTTP %s", video_id, e.code)
        return None
    except Exception as exc:                          # noqa: BLE001
        log.debug("is_short(%s) failed: %s", video_id, exc)
        return None


def jpeg_dimensions(data: bytes) -> tuple[int, int] | None:
    """Width and height from JPEG SOF markers. Stdlib only, no ffprobe.

    ffprobe would also work but is not guaranteed present, and this reads
    a few dozen bytes of header rather than shelling out per candidate.
    """
    if len(data) < 4 or data[0:2] != b"\xff\xd8":
        return None
    i, n = 2, len(data)
    while i < n - 9:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        # SOF0-SOF15, excluding DHT (c4), JPG (c8) and DAC (cc)
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            height = int.from_bytes(data[i + 5:i + 7], "big")
            width = int.from_bytes(data[i + 7:i + 9], "big")
            return (width, height) if width and height else None
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        seglen = int.from_bytes(data[i + 2:i + 4], "big")
        if seglen < 2:
            return None
        i += 2 + seglen
    return None


def oar_dimensions(video_id: str, *, timeout: float = 15.0) -> tuple[int, int] | None:
    """Pixel dimensions from the original-aspect-ratio thumbnail.

    Returns None when no `oar` variant exists, which for YouTube means the
    source is plain 16:9 — see `verify_orientation`, which reads that as
    landscape rather than as a failure.
    """
    for variant in _OAR_VARIANTS:
        url = f"https://i.ytimg.com/vi/{video_id}/{variant}.jpg"
        req = urllib.request.Request(url, headers={"User-Agent": _UA})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                if r.status != 200:
                    continue
                dims = jpeg_dimensions(r.read())
                if dims:
                    return dims
        except urllib.error.HTTPError as e:
            if e.code == 404:
                continue
            log.debug("oar_dimensions(%s/%s): HTTP %s", video_id, variant, e.code)
        except Exception as exc:                      # noqa: BLE001
            log.debug("oar_dimensions(%s/%s) failed: %s", video_id, variant, exc)
    return None


def _probe_reachable(timeout: float) -> bool:
    """Did the thumbnail host answer at all? Distinguishes 'no oar variant'
    from 'the network is down', so a dead network never reads as landscape."""
    req = urllib.request.Request(
        "https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg",
        headers={"User-Agent": _UA},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status == 200
    except Exception:                                 # noqa: BLE001
        return False


def verify_orientation(
    video_id: str,
    *,
    width: int | None = None,
    height: int | None = None,
    timeout: float = 15.0,
) -> str:
    """Read orientation from pixels. Never from duration, never from platform.

    Pass `width`/`height` when yt-dlp already resolved a video format — that
    is the most direct read and costs no request. Otherwise fall back to the
    original-aspect-ratio thumbnail.

    Returns "vertical", "landscape", or "unknown". Callers must treat
    "unknown" as unverified, not as a pass.
    """
    if width and height:
        return VERTICAL if height > width else LANDSCAPE

    dims = oar_dimensions(video_id, timeout=timeout)
    if dims:
        w, h = dims
        return VERTICAL if h > w else LANDSCAPE

    # No oar variant. That means 16:9 — but only if we can reach the host.
    return LANDSCAPE if _probe_reachable(timeout) else UNKNOWN


def shorts_web_queries(queries: list[str]) -> list[str]:
    """`site:youtube.com/shorts` forms, for the Brave web endpoint.

    The `#shorts` suffix convention underperformed badly in the smoke test.
    Suffixed `ytsearch` queries returned almost entirely landscape
    local-news packages plus off-topic craft videos ("how to remove sticker
    residue"), because the token matches descriptions rather than format.
    Every on-topic Short for that beat was found instead by a
    `site:youtube.com/shorts` web search, which constrains on the URL path
    and so cannot return a non-Short.

    Both strategies now run. This is the recall leg the suffix was failing
    to provide; it is not a replacement, and which one earns its budget is
    a question for the eval, not for assumption.
    """
    return [f"site:youtube.com/shorts {q}".strip() for q in queries if q and q.strip()]


def looks_like_short(duration: int | None) -> bool:
    """Cheap pre-filter only. True when duration cannot rule a Short out.

    None passes: `--flat-playlist` frequently returns null durations, and
    silently dropping those is how real Shorts go missing. Confirm with
    `is_short` before relying on the answer.
    """
    return duration is None or duration <= SHORTS_MAX_DURATION
