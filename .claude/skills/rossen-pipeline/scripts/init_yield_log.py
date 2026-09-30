#!/usr/bin/env python3
"""init_yield_log.py — create the beat yield log with its schema header if absent.

Usage:
    python3 scripts/init_yield_log.py            # default path, inside the skill
    python3 scripts/init_yield_log.py --path <p>
    python3 scripts/init_yield_log.py --check     # report only, create nothing

Step 9 tells you to append to the yield log and to read the schema from the log's
own header rather than inventing columns. That is only possible if the log exists
with a header. It has shipped absent, which makes Step 9 unexecutable and invites
exactly the failure Step 9 warns about: a bare relative path resolving to a second
file at the repo root, the two drifting into incompatible schemas.

This script writes the canonical header once, at the canonical path, and refuses
to touch a log that already exists.
"""

import argparse
import os
import sys

DEFAULT = os.path.join("skills", "rossen-beat-extractor", "reference",
                       "beat_yield.md")

HEADER = """# Beat yield log

Append-only. One row per beat, every run — not just the failures. Written by
`rossen-pipeline` Step 9.

**This file lives inside the beat-extractor skill on purpose.** It is what
travels when the skill is deployed to an account; a copy at the repo root does
not. Always write the full path. A bare relative path has already resolved to a
second file at the repo root and the two drifted into incompatible schemas with
zero overlapping episodes before anyone noticed.

## Outcome vocabulary

Use these values only. If you need a new one, add it to this table in the same
commit so the next run inherits it instead of coining a synonym.

| Outcome | Meaning |
|---|---|
| `PICK` | A clip was found, graded, and its outcue verified against a transcript. |
| `WEAK` | A clip was flagged but scored low or carried flags; a human should re-check. |
| `MANUAL` | The right footage exists but off a captioned surface — link handed over, no timecode invented. |
| `SWAP` | The producer approved a different case or victim than the script named. |
| `SHOW-PRODUCED` | Correctly identified as un-sourceable before search ran; the show will shoot it. **Not a failure — never log as `EMPTY`.** |
| `EMPTY` | Searched and nothing usable came back. |
| `THROTTLED` | A shortlist exists but transcript verification was blocked (bot wall, rate limit). Not empty — re-run Step 5. |
| `CORRECTED` | A prior run's row for this beat was wrong; this row supersedes it. |

## Columns

| Column | Notes |
|---|---|
| `episode` | e.g. `07-24` |
| `beat_id` | e.g. `07-24-b03` |
| `show_day` | `WED` or `FRI` — yields differ sharply by day |
| `clip_role` | from the beat record |
| `orientation` | `horizontal` \\| `vertical` |
| `source_native` | `tiktok` \\| `instagram` \\| `x` \\| `none` |
| `sourcability` | scan verdict at Checkpoint 1 |
| `outcome` | from the vocabulary above |
| `source_type` | of the pick, if any |
| `transcript_rung` | 1 captions, 2 whisper, 3 unverified |
| `note` | what happened, in a clause |

## Rows

| episode | beat_id | show_day | clip_role | orientation | source_native | sourcability | outcome | source_type | transcript_rung | note |
|---|---|---|---|---|---|---|---|---|---|---|

## Cross-run observations

Things that only become visible across runs. Append here, dated.

### Structural dead ends

Beat shapes that repeatedly cannot be sourced. This is the most useful section in
the file — it tells the script writer to stop writing beats that cannot be
sourced, which is cheaper than sourcing them well.

- Vertical `evidence`: 0-for-4 across two episodes.

### Process bugs found, and what fixed them

Enough detail that a future run recognizes the symptom. Two of the three most
costly errors in this pipeline's history were diagnosis errors, not search
failures: orientation inferred from duration, and rate-limiting read as a hard IP
block.

### Sourcability-scan calibration

Predictions the scan got right or wrong, so its accuracy is measurable rather
than assumed.
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", default=DEFAULT)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    exists = os.path.exists(a.path)
    if a.check:
        print(f"{'present' if exists else 'ABSENT'}: {a.path}")
        sys.exit(0 if exists else 1)

    if exists:
        print(f"already present, leaving untouched: {a.path}")
        sys.exit(0)

    os.makedirs(os.path.dirname(a.path) or ".", exist_ok=True)
    with open(a.path, "w", encoding="utf-8") as fh:
        fh.write(HEADER)
    print(f"created {a.path} with the canonical header.\n"
          f"Append rows beneath the '## Rows' table. Never create a second copy "
          f"at the repo root.")


if __name__ == "__main__":
    main()
