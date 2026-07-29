"""Shared contract vocabulary for the pipeline validators.

Single source of truth so four validators cannot drift apart. Every constant
here traces to a specific line in one of the four SKILL.md files; the comment
names which one. If a skill changes, change it here, not in a caller.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# rossen-beat-extractor SKILL.md, "Clip roles" -- seven roles plus the
# documented escape hatch for a beat that genuinely fits none of them.
ROLES = {
    "victim_interview", "confrontation_bust", "evidence", "explainer_demo",
    "authority_report", "debunk", "first_person_rant", "other",
}

# rossen-beat-extractor SKILL.md, marker table: orientation is producer-authored
# ground truth and only ever these two values.
ORIENTATIONS = {"horizontal", "vertical"}

# rossen-beat-extractor SKILL.md, "Sourcability scan" -> Output, plus the
# pipeline hard rule that a rate-limited search is recorded as `throttled`
# rather than as an absence of footage.
SOURCABILITY = {"high", "commentary_only", "none", "unchecked", "throttled"}

# rossen-beat-extractor SKILL.md, "Self-recorded beats".
SOURCE_NATIVE = {"instagram", "x", "tiktok", "none"}

# rossen-clip-grader SKILL.md, "Source type" table.
SOURCE_TYPES = {
    "affiliate", "network", "creator_long", "creator_short",
    "first_person", "raw_footage",
}

# rossen-query-generator SKILL.md: four named registers plus the `shorts`
# register the Shorts dialect section requires be emitted separately.
REGISTERS = ["news", "victim", "platform", "anchor", "shorts"]

# rossen-beat-extractor SKILL.md, "Output" -- the extractor's record. These are
# the keys the no-reduction rule protects across the step 1 -> step 2 boundary.
EXTRACTOR_KEYS = [
    "beat_id", "episode", "segment_title", "script_text", "orientation",
    "clip_role", "visual_spec", "platforms", "offsite_likely", "priority",
    "expected_segments", "sourcability", "sourcability_note", "source_native",
]

# rossen-clip-grader SKILL.md, "Output" -- the grader's pass-two object. These
# are the keys the no-reduction rule protects across the step 6 -> step 8
# boundary, plus the two fields the pipeline adds (`platform`, `title`).
GRADER_PASS2_KEYS = [
    "beat_id", "pass", "flagged", "source_mix", "diversity_floor_applied",
    "ranked", "rejected", "cannot_determine",
]
PIPELINE_ADDED_KEYS = ["platform", "title"]

# Checkpoint 1 beat-count bands, from the run contract.
DAY_BANDS = {"wednesday": (10, 12), "friday": (0, 5)}

TIMECODE = re.compile(r"^\d{1,2}:\d{2}(?:\.\d+)?$")


def parse_tc(s: str) -> float | None:
    """'1:07' -> 67.0. Returns None if unparseable."""
    if not isinstance(s, str) or not TIMECODE.match(s.strip()):
        return None
    mm, ss = s.strip().split(":")
    return int(mm) * 60 + float(ss)


class Report:
    """Collects findings. Exit status is driven by ERROR count only, so
    `clear every ERROR before the next stage` is mechanically checkable."""

    def __init__(self, name: str):
        self.name = name
        self.errors: list[str] = []
        self.warns: list[str] = []
        self.notes: list[str] = []

    def error(self, where: str, msg: str) -> None:
        self.errors.append(f"{where}: {msg}")

    def warn(self, where: str, msg: str) -> None:
        self.warns.append(f"{where}: {msg}")

    def note(self, msg: str) -> None:
        self.notes.append(msg)

    def finish(self) -> int:
        for m in self.notes:
            print(f"  note  {m}")
        for m in self.warns:
            print(f"  WARN  {m}")
        for m in self.errors:
            print(f"  ERROR {m}")
        print(f"{self.name}: {len(self.errors)} error(s), {len(self.warns)} warning(s)")
        return 1 if self.errors else 0


def load(path: str) -> list[dict]:
    data = json.loads(Path(path).read_text())
    if isinstance(data, dict):
        data = [data]
    if not isinstance(data, list):
        print(f"ERROR {path}: expected a JSON list of objects", file=sys.stderr)
        raise SystemExit(2)
    return data
