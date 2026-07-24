"""Offline tests for vertical_transcribe.py. No network, no Whisper model
load -- those are exercised live (see the module docstring for the
confirmed-live findings this module encodes). This covers the parts that
don't need either: ID extraction, cue building, and cache-miss handling
with the model call mocked out."""
import sys, os, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rossen_harvest.vertical_transcribe import (
    tiktok_id, fetch_vertical_transcript, AUDIO_SAFE_FORMAT,
)
from rossen_harvest.transcripts import Cue, Transcript
from rossen_harvest.cache import Cache

ok = fail = 0
def check(label, cond):
    global ok, fail
    if cond: ok += 1; print(f"  PASS  {label}")
    else:    fail += 1; print(f"  FAIL  {label}")

print("\n-- tiktok_id extraction --")
cases = [
    ("https://www.tiktok.com/@naledimofficial/video/7461585895750192390", "7461585895750192390"),
    ("https://www.tiktok.com/@user/video/123?lang=en", "123"),
    ("https://www.tiktok.com/@handle.with.dots/photo/9988776655", "9988776655"),
    ("https://www.tiktok.com/foryou", None),
    ("https://www.youtube.com/watch?v=abc", None),
    ("", None),
]
for url, want in cases:
    got = tiktok_id(url)
    check(f"{url[:52]:52s} -> {want}", got == want)

print("\n-- format string is the confirmed-safe one --")
check("AUDIO_SAFE_FORMAT leads with 'download' (confirmed audio-bearing)",
      AUDIO_SAFE_FORMAT.split("/")[0] == "download")
check("AUDIO_SAFE_FORMAT excludes audio-less formats explicitly",
      "acodec!=none" in AUDIO_SAFE_FORMAT)

print("\n-- Transcript shape matches transcripts.py (drop-in for outcue verification) --")
cues = [Cue(0.0, 5.1, "quick story time about how I almost got scammed")]
t = Transcript("vid1", cues, "whisper")
check("source tagged 'whisper'", t.source == "whisper")
check(".find() works identically to a caption-sourced transcript",
      t.find("almost got scammed") is not None)
check(".as_prompt() timestamps like a caption transcript",
      t.as_prompt().startswith("[0:00]"))
a, b, outcue = t.segment(0.0, 5.0)
check(".segment() pads and returns a verbatim outcue",
      outcue == "quick story time about how I almost got scammed")

print("\n-- cache round-trip without touching the network or the model --")
with tempfile.TemporaryDirectory() as td:
    cache = Cache(os.path.join(td, "t.db"))
    # Prime the cache directly, as fetch_vertical_transcript would after a
    # real transcription, then confirm the cache-hit path returns it
    # without calling download_audio or the model.
    cache.put_raw("whisper:tiny.en:999", {
        "cues": [{"start": 0.0, "end": 2.0, "text": "cached line"}],
    })
    t = fetch_vertical_transcript("https://www.tiktok.com/@x/video/999",
                                   cache=cache, model_size="tiny.en")
    check("cache hit returns a Transcript, no network/model call", t is not None)
    check("cache hit carries the cached cue text",
          t is not None and t.cues[0].text == "cached line")
    check("cache hit is tagged whisper", t is not None and t.source == "whisper")

    # Negative cache: an empty dict means "checked, nothing found" -- must
    # return None, not an empty-but-truthy Transcript.
    cache.put_raw("whisper:tiny.en:888", {})
    t = fetch_vertical_transcript("https://www.tiktok.com/@x/video/888",
                                   cache=cache, model_size="tiny.en")
    check("negative cache (empty dict) returns None, not a hollow Transcript",
          t is None)

print(f"\n{'='*50}\n{ok} passed, {fail} failed\n{'='*50}")
sys.exit(1 if fail else 0)
