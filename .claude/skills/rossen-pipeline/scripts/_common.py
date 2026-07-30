"""Shared helpers for the pipeline validators.

Authored 2026-07-30 during run F2_08052026. These scripts are referenced by the
pipeline operator's runbook but had never been committed; the contracts encoded
here are transcribed from the four SKILL.md files, not invented.
"""
from __future__ import annotations
import json, sys
from pathlib import Path

class Report:
    def __init__(self, name):
        self.name = name; self.errors = []; self.warns = []; self.notes = []
    def error(self, where, msg): self.errors.append(f"{where}: {msg}")
    def warn(self, where, msg): self.warns.append(f"{where}: {msg}")
    def note(self, msg): self.notes.append(msg)
    def finish(self) -> int:
        for n in self.notes: print(f"NOTE   {n}")
        for w in self.warns: print(f"WARN   {w}")
        for e in self.errors: print(f"ERROR  {e}")
        print(f"\n{self.name}: {len(self.errors)} error(s), {len(self.warns)} warning(s)")
        return 1 if self.errors else 0

def load(path) -> list:
    data = json.loads(Path(path).read_text())
    return data if isinstance(data, list) else [data]
