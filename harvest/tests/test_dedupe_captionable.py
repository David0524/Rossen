"""Regression: a title collision across platforms must not discard the only
copy with a caption track.

The bug this pins: `dedupe` pass 2 matches fuzzy titles across platforms, and
its survivor rule preferred the earliest upload date. An outlet's own website
embed of a package and its own YouTube upload of the same package collide on
title, so the website copy could win -- destroying the only transcribable copy.
Downstream that reads as "no captioned source exists for this beat," and the
beat degrades to a manual-lane LOCATED that a producer has to timecode by hand.

Observed live: b01/b10/b11 of the F2 07/29 TOP STORIES run each lost their exact
case this way while the correct YouTube video sat at rank 1 in the search cache.
"""
import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rossen_harvest.candidates import Candidate  # noqa: E402
from rossen_harvest.dedupe import dedupe  # noqa: E402

ok = fail = 0


def check(label, cond):
    global ok, fail
    if cond:
        ok += 1
        print(f"  PASS  {label}")
    else:
        fail += 1
        print(f"  FAIL  {label}")


def mk(platform, vid, title, published, uploader="ABC13 Houston", views=0, rank=1):
    return Candidate(
        platform=platform, url=f"https://example/{vid}", video_id=vid, title=title,
        beat_id="b01", query_that_found_it=f"q-{vid}", register="news",
        published=published, uploader=uploader, views=views, rank=rank,
        duration=212 if platform == "youtube" else None,
    )


TITLE = "Victim says restitution lags after fake utility worker theft"

print("\n-- captionable copy survives a cross-platform title collision --")

# The website copy is a day EARLIER, which under the old rule won outright.
web = mk("news_web", "uabc13page", f"Houston burglary victim says restitution lags "
                                   f"after fake utility worker theft", date(2025, 12, 1))
yt = mk("youtube", "mwHYj6Pn8R8", TITLE, date(2025, 12, 2))

for order in ([web, yt], [yt, web]):
    kept = dedupe(list(order))
    label = "web-first" if order[0] is web else "youtube-first"
    check(f"{label}: collapses to one", len(kept) == 1)
    check(f"{label}: survivor is the captionable youtube copy",
          kept and kept[0].platform == "youtube")
    check(f"{label}: survivor keeps the youtube id",
          kept and kept[0].video_id == "mwHYj6Pn8R8")
    check(f"{label}: survivor is not marked a duplicate",
          kept and kept[0].duplicate_of is None)
    check(f"{label}: both queries remembered on survivor",
          kept and len(kept[0].also_found_by) == 2)

print("\n-- within-YouTube wire dedupe still keeps the earliest station --")
# The originating-station rule must survive untouched when both copies are
# equally captionable; that is a clearance question, not a caption question.
early = mk("youtube", "early00000A", "Bed rail recall after two deaths",
           date(2026, 3, 26), uploader="KING 5")
late = mk("youtube", "late000000B", "Bed rail recall after two deaths",
          date(2026, 3, 28), uploader="KIRO 7")
kept = dedupe([late, early])
check("wire duplicates collapse to one", len(kept) == 1)
check("earliest upload survives", kept and kept[0].video_id == "early00000A")

print("\n-- neither captionable: earliest still wins --")
a = mk("news_web", "uweb000001", "Hopper to pay $35 million FTC settlement",
       date(2026, 7, 2), uploader="CNBC")
b = mk("news_web", "uweb000002", "Hopper to pay $35 million FTC settlement",
       date(2026, 7, 5), uploader="Yahoo")
kept = dedupe([b, a])
check("two uncaptionable copies collapse to one", len(kept) == 1)
check("earliest uncaptionable survives", kept and kept[0].video_id == "uweb000001")

print("\n-- distinct stories are not collapsed --")
kept = dedupe([
    mk("youtube", "story0001AA", "Calgary landlord charged with voyeurism", date(2026, 7, 11)),
    mk("youtube", "story0002BB", "Hopper to pay $35 million FTC settlement", date(2026, 7, 2)),
])
check("unrelated titles both survive", len(kept) == 2)

print(f"\n{'=' * 50}\n{ok} passed, {fail} failed\n{'=' * 50}")
sys.exit(1 if fail else 0)
