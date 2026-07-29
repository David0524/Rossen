#!/usr/bin/env python3
"""Validate the `queries` block on a beats file against the query-generator contract.

    python3 check_queries.py beats.json

The load-bearing check is that all five registers are present and non-empty on
every beat. Four registers means the Shorts leg runs on half its input, and
Shorts is the only vertical surface with a reachable search index.

Scope: this validates register coverage and dialect discipline. It cannot tell
you a query will actually recall the clip -- only a recall@30 eval against a
worksheet of aired URLs can do that (`python3 -m rossen_harvest eval`).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "rossen-pipeline" / "scripts"))
from _contract import REGISTERS, Report, load  # noqa: E402

# rossen-query-generator SKILL.md, "Shorts dialect": three to five words plus
# one or two hashtags. Long noun-heavy strings are the long-form dialect and do
# not match how Shorts are titled.
SHORTS_MAX_WORDS = 9

# Same skill, "TikTok": search degrades badly past four or five words.
TIKTOK_MAX_WORDS = 6

# Same skill, "News register": do not add a city name -- affiliates carry
# national wire packages, so the affiliate that surfaces is usually nowhere
# near the event. Only flagged when the city is ALSO in the anchor register,
# which is where proper nouns legitimately belong.
def _words(s: str) -> int:
    return len([w for w in s.split() if w.strip()])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("beats")
    ap.add_argument("--min-per-register", type=int, default=1,
                    help="ERROR below this many strings per register (default 1)")
    args = ap.parse_args()

    beats = load(args.beats)
    r = Report("check_queries")
    total = 0

    for b in beats:
        bid = b.get("beat_id", "<no beat_id>")
        q = b.get("queries")
        if not isinstance(q, dict):
            r.error(bid, "missing or malformed `queries` dict")
            continue

        for reg in REGISTERS:
            if reg not in q:
                r.error(bid, f"missing register `{reg}` -- all five are required "
                             f"({', '.join(REGISTERS)})")
                continue
            strings = q[reg]
            if not isinstance(strings, list):
                r.error(bid, f"register `{reg}` is not a list")
                continue
            live = [s for s in strings if isinstance(s, str) and s.strip()]
            if len(live) < args.min_per_register:
                r.error(bid, f"register `{reg}` has {len(live)} usable string(s), "
                             f"need >= {args.min_per_register}")
            if len(live) != len(strings):
                r.error(bid, f"register `{reg}` contains empty or non-string entries")
            total += len(live)

        for extra in set(q) - set(REGISTERS):
            r.warn(bid, f"unrecognised register `{extra}` -- harvest routes by register "
                        "name and will not run it")

        # Shorts dialect discipline.
        for s in q.get("shorts", []) or []:
            if isinstance(s, str) and _words(s) > SHORTS_MAX_WORDS:
                r.warn(bid, f"shorts query is {_words(s)} words, reads as long-form "
                            f"dialect: {s!r}")

        # TikTok/vertical brevity, only where a vertical surface is in play.
        plats = set(b.get("platforms") or [])
        if plats & {"tiktok", "instagram"}:
            for s in q.get("platform", []) or []:
                if isinstance(s, str) and _words(s) > TIKTOK_MAX_WORDS:
                    r.warn(bid, f"platform query is {_words(s)} words on a beat routed to "
                                f"TikTok/IG, where search degrades past 5: {s!r}")

        # The anchor register is the highest-hit-rate register on dated-event
        # beats and costs one query, so a named news_anchor with no anchor
        # strings is a real miss.
        if (b.get("news_anchor") or "").strip() and not (q.get("anchor") or []):
            r.error(bid, "news_anchor is set but the `anchor` register is empty -- "
                         "that is the highest-hit-rate register on dated beats")

        pm = b.get("platform_map")
        if not isinstance(pm, dict) or not pm:
            r.error(bid, "missing `platform_map`")
        else:
            for surface, regs in pm.items():
                for reg in regs or []:
                    if reg not in q:
                        r.error(bid, f"platform_map[{surface}] references register "
                                     f"`{reg}` that is not in queries")

        # Shorts run on every orientation, so the search block must be present.
        ss = b.get("shorts_search")
        if not isinstance(ss, dict):
            r.error(bid, "missing `shorts_search` block")
        else:
            if not ss.get("suffix"):
                r.error(bid, "shorts_search.suffix missing -- without #shorts the duration "
                             "filter leaves you searching all of YouTube")
            if not ss.get("match_filter"):
                r.error(bid, "shorts_search.match_filter missing -- without it the #shorts "
                             "token alone leaks long-form uploads")

    r.note(f"{total} query strings across {len(beats)} beats")
    return r.finish()


if __name__ == "__main__":
    raise SystemExit(main())
