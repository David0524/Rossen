"""Dedupe harvested candidates.

Two collisions matter and they are different problems.

1. The same video returned by several queries. Exact video_id match.
   Cheap. Keep one record, remember every query that found it, because
   which register surfaced a clip is the eval signal.

2. The same wire package re-hosted by dozens of Nexstar and Sinclair
   stations under near-identical titles. This is a WITHIN-YouTube
   collision, so cross-platform matching never catches it. Fuzzy title.
   Keep the earliest upload date: that is usually the originating
   station and it is what matters for clearance.
"""
from __future__ import annotations

import re
from difflib import SequenceMatcher

from .candidates import Candidate

# Boilerplate that varies between stations carrying the same wire package.
_STATION_NOISE = re.compile(
    r"\b(abc|nbc|cbs|fox|cw)\s?-?\s?\d{0,2}\b"
    r"|\b[kw][a-z]{2,3}(-tv)?\b"
    r"|\bnews\s?\d{1,2}\b"
    r"|\b(exclusive|breaking|watch|full (story|interview|segment)|raw video)\b"
    r"|\b(live|update|report)\b",
    re.I,
)
_PUNCT = re.compile(r"[^\w\s]")
_WS = re.compile(r"\s+")

TITLE_THRESHOLD = 0.86


def normalize_title(title: str) -> str:
    t = title.lower()
    t = _STATION_NOISE.sub(" ", t)
    t = _PUNCT.sub(" ", t)
    return _WS.sub(" ", t).strip()


def title_similarity(a: str, b: str) -> float:
    na, nb = normalize_title(a), normalize_title(b)
    if not na or not nb:
        return 0.0
    if na == nb:
        return 1.0
    return SequenceMatcher(None, na, nb).ratio()


def _sort_key(c: Candidate):
    """Preferred survivor: earliest upload, then affiliate, then most views."""
    from datetime import date as _d
    return (
        c.published or _d.max,          # earliest first, unknown last
        not c.is_affiliate,             # affiliates first
        -(c.views or 0),                # then most watched
    )


# Platforms that carry a fetchable caption or subtitle track. An outcue has to
# be quoted verbatim from a transcript, so a copy we can transcribe is worth
# strictly more than one we cannot, all else equal.
CAPTIONABLE_PLATFORMS = {"youtube"}


def _beats_incumbent(cand: Candidate, incumbent: Candidate) -> bool:
    """Should `cand` displace `incumbent` as the survivor of a title collision?

    The earliest-upload rule exists to keep the ORIGINATING station when a wire
    package is re-hosted across a dozen affiliates -- that is a within-YouTube
    clearance question. It is the wrong rule across platforms: an outlet's own
    website embed and its own YouTube upload of the same package are the same
    outlet, so clearance is a wash, but only the YouTube copy has captions.
    Preferring the website copy silently costs the beat its verifiable outcue
    and degrades it to a manual-lane LOCATED for no editorial gain.
    """
    cand_cap = cand.platform in CAPTIONABLE_PLATFORMS
    inc_cap = incumbent.platform in CAPTIONABLE_PLATFORMS
    if cand_cap != inc_cap:
        return cand_cap
    return _sort_key(cand) < _sort_key(incumbent)


def dedupe(candidates: list[Candidate]) -> list[Candidate]:
    """Collapse duplicates within one beat. Returns survivors only.

    Survivors carry `also_found_by`, the list of "register:query" strings
    that reached them. That list is what the eval reads.
    """
    # --- pass 1: exact video_id, per platform -------------------------
    by_id: dict[tuple[str, str], Candidate] = {}
    for c in candidates:
        key = (c.platform, c.video_id)
        tag = f"{c.register}:{c.query_that_found_it}"
        if key not in by_id:
            c.also_found_by = [tag]
            by_id[key] = c
            continue
        kept = by_id[key]
        if tag not in kept.also_found_by:
            kept.also_found_by.append(tag)
        # keep the best rank seen across queries
        if c.rank is not None and (kept.rank is None or c.rank < kept.rank):
            kept.rank = c.rank

    survivors = sorted(by_id.values(), key=_sort_key)

    # --- pass 2: fuzzy title, within and across platforms -------------
    kept: list[Candidate] = []
    for cand in survivors:
        idx = next(
            (i for i, k in enumerate(kept)
             if title_similarity(k.title, cand.title) >= TITLE_THRESHOLD),
            None,
        )
        if idx is None:
            kept.append(cand)
            continue

        incumbent = kept[idx]
        winner, loser = (
            (cand, incumbent) if _beats_incumbent(cand, incumbent)
            else (incumbent, cand)
        )
        loser.duplicate_of = winner.video_id
        winner.duplicate_of = None
        for tag in loser.also_found_by:
            if tag not in winner.also_found_by:
                winner.also_found_by.append(tag)
        if loser.rank is not None and (winner.rank is None or loser.rank < winner.rank):
            winner.rank = loser.rank
        kept[idx] = winner

    return kept


def dedupe_by_beat(candidates: list[Candidate]) -> list[Candidate]:
    """Dedupe within each beat independently.

    Deliberately NOT global. The same clip legitimately serves two beats
    in one episode, and collapsing across beats would hide that.
    """
    out: list[Candidate] = []
    beats = sorted({c.beat_id for c in candidates})
    for beat in beats:
        out.extend(dedupe([c for c in candidates if c.beat_id == beat]))
    return out
