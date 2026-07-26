"""Step 7: download each pick once and cut its segments.

Documented in the pipeline skill as `python -m rossen_harvest clip` but
never implemented — the CLI shipped with harvest/search/eval only. This
closes that gap for horizontal beats. `cut/crop_vertical.sh` remains the
tool for reframing a vertical beat out of a landscape repost; this module
does not reframe, it trims.

A pick may carry an explicit `media_source` (an HLS manifest or a direct
mp4 pulled off the outlet's own page). That wins over `url`, because it is
the route that actually works when YouTube is bot-walled — which is how
the 07-31 run got its only cuttable source.

Timecodes are padded by the same PAD_IN/PAD_OUT the transcript layer uses,
so an editor trims rather than hunts for a clipped first syllable.
"""
from __future__ import annotations

import hashlib
import json
import logging
import subprocess
from pathlib import Path

from .transcripts import PAD_IN, PAD_OUT

log = logging.getLogger(__name__)


def parse_tc(tc: str | float | int) -> float:
    """'1:19' or '79' or '00:01:19.5' -> seconds."""
    if isinstance(tc, (int, float)):
        return float(tc)
    parts = str(tc).strip().split(":")
    try:
        vals = [float(p) for p in parts]
    except ValueError:
        raise ValueError(f"unparseable timecode: {tc!r}")
    sec = 0.0
    for v in vals:
        sec = sec * 60 + v
    return sec


def fmt_tc(sec: float) -> str:
    m, s = divmod(max(0.0, sec), 60)
    return f"{int(m)}:{s:05.2f}"


def _source_key(pick: dict) -> str:
    """Identify the underlying media, not the beat.

    Butt-cut beats share one source by definition — b01 and b02 of the
    07-31 run are two segments of the same Scripps package — so keying the
    download on beat_id fetched the same 36MB file twice. Key on the media
    URL instead and the second beat reuses the first beat's download.
    """
    raw = pick.get("media_source") or pick.get("flagged") or pick.get("url") or ""
    return hashlib.sha1(raw.encode()).hexdigest()[:12]


def resolve_source(pick: dict, outdir: Path) -> Path | None:
    """Get one local media file for a pick, downloading only once."""
    dest = outdir / f"src_{_source_key(pick)}.mp4"
    if dest.exists() and dest.stat().st_size > 0:
        log.info("%s: source already downloaded (%s)", pick["beat_id"], dest.name)
        return dest

    media = pick.get("media_source")
    if media:
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", media,
               "-c", "copy", "-bsf:a", "aac_adtstoasc", str(dest)]
        if subprocess.run(cmd).returncode == 0 and dest.exists():
            return dest
        # stream copy can fail on some HLS variants; re-encode as a fallback
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", media,
               "-c:v", "libx264", "-preset", "veryfast", "-c:a", "aac", str(dest)]
        if subprocess.run(cmd).returncode == 0 and dest.exists():
            return dest
        log.warning("%s: ffmpeg could not pull media_source", pick["beat_id"])

    url = pick.get("flagged") or pick.get("url")
    if url:
        cmd = ["yt-dlp", "-f", "bv*[height<=720]+ba/b[height<=720]/b",
               "--merge-output-format", "mp4", "-o", str(dest), url]
        if subprocess.run(cmd).returncode == 0 and dest.exists():
            return dest
        log.warning("%s: yt-dlp could not download %s", pick["beat_id"], url)

    return None


def cut_segment(src: Path, start: float, end: float, dest: Path) -> bool:
    dur = max(0.1, end - start)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{start:.3f}",
           "-i", str(src), "-t", f"{dur:.3f}",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
           "-c:a", "aac", str(dest)]
    return subprocess.run(cmd).returncode == 0 and dest.exists()


def run(picks: list[dict], outdir: Path) -> dict:
    outdir.mkdir(parents=True, exist_ok=True)
    manifest = {"clips": [], "failed": []}

    for pick in picks:
        bid = pick["beat_id"]
        segs = pick.get("segments") or []
        if not segs:
            manifest["failed"].append({"beat_id": bid, "reason": "no segments"})
            continue

        src = resolve_source(pick, outdir)
        if not src:
            manifest["failed"].append(
                {"beat_id": bid, "reason": "could not obtain media",
                 "url": pick.get("flagged")})
            log.warning("%s: no media, skipping", bid)
            continue

        for i, seg in enumerate(segs, 1):
            a = max(0.0, parse_tc(seg["in"]) - PAD_IN)
            b = parse_tc(seg["out"]) + PAD_OUT
            dest = outdir / f"{bid}_seg{i}.mp4"
            ok = cut_segment(src, a, b, dest)
            row = {
                "beat_id": bid, "segment": i, "file": dest.name,
                "in": fmt_tc(a), "out": fmt_tc(b),
                "in_unpadded": seg["in"], "out_unpadded": seg["out"],
                "outcue": seg.get("outcue"),
                "outcue_verified": seg.get("outcue_verified", False),
                "source": pick.get("flagged") or pick.get("url"),
                "butt_with": pick.get("butt_with"),
            }
            if ok:
                manifest["clips"].append(row)
                print(f"  {bid} seg{i}: {fmt_tc(a)}-{fmt_tc(b)} -> {dest.name}")
            else:
                row["reason"] = "ffmpeg cut failed"
                manifest["failed"].append(row)

    (outdir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    return manifest


def cmd_clip(args) -> int:
    picks = json.loads(Path(args.picks).read_text())
    if isinstance(picks, dict):
        picks = [picks]
    outdir = Path(args.outdir)
    m = run(picks, outdir)
    print(f"\n{len(m['clips'])} segments cut, {len(m['failed'])} failed")
    for f in m["failed"]:
        print(f"  FAILED {f.get('beat_id')}: {f.get('reason')}")
    unverified = [c for c in m["clips"] if not c["outcue_verified"]]
    if unverified:
        print(f"  WARNING: {len(unverified)} segments have an unverified outcue")
    print(f"wrote {outdir/'manifest.json'}")
    return 0
