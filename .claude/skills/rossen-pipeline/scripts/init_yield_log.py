#!/usr/bin/env python3
"""Create the beat yield log if it does not exist.

    python3 init_yield_log.py --path .claude/skills/rossen-beat-extractor/reference/beat_yield.md

Idempotent: refuses to overwrite an existing log. Always pass the full path --
a bare relative path forks the log into a second file at the repo root.
"""
from __future__ import annotations

import argparse
from pathlib import Path

HEADER = """# Beat yield log

Appended every pipeline run, every beat — not just failures. The point is to
learn which roles/orientations reliably yield an airable clip and which are
structural dead ends, so the bible can be written toward what sources exist.

Columns: run · beat · role · orientation · outcome · why / source
Outcomes: PICK (verified outcue) · LOCATED (case found, no caption-able source)
· SWAP (needs script change) · SHOW-PRODUCED (removed from the clip pipeline,
the show shoots it) · EMPTY (nothing cleared the bar)

SHOW-PRODUCED is never EMPTY: a beat the show films itself is a production task
with a known owner, not a sourcing failure, and logging it as EMPTY corrupts the
per-role yield stats this file exists to produce.
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", required=True)
    args = ap.parse_args()

    p = Path(args.path)
    if p.exists():
        print(f"exists, leaving alone: {p}")
        return 0
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(HEADER)
    print(f"created {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
