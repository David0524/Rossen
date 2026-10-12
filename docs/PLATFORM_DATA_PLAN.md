# Platform data plan (handoff, 10/12/2026; revised after review the same day)

Status: **waiting on data.** The data request (`docs/Rossen Audience Data Request.docx`) has **not been
sent yet** (producer, 10/12), so it can still be trimmed per this plan before it goes out. Nothing below is built yet. No skill changes until the
producer approves (standing rule). Producer answers (10/12) are near the end.

## The problem we're solving

The skills catch mistakes one specialist at a time, late. This week's misses, by missing expertise:

| Missing expertise | What slipped (week of 10/5) |
|---|---|
| Showrunner / retention (Ryan) | 10 of his 11 notes on the 10/9 F1: no why-now chain, label openers, a segment cut to an ad on fear, a "reason to leave" line. Reviewer caught 1 of 11. |
| Editor (producer) | Outlet names, victim surnames and towns, payoff given away in the tease, slate written in. Fixed by hand on 10/14. |
| Reporter | Setup written for an unconfirmed bodycam (doesn't exist); 2025 cases read as new; Wrigg's state; clip in-points mid-sentence. |
| Standards | Guest questions pointing at an open case; credential stretch. |
| Jeff | Tease promises not paid off by name; title said "free sample" but she paid for a $25 facial. |
| Show state | A cut story kept from a stale outline; a graphic cue with no content; "we reached out to Walmart" with no request sent. |
| **YouTube / Facebook optimizer** | **Titles are drafted from `titles.md` at the pitch stage, but nothing checks them against performance, nothing checks that the open pays off the title and thumbnail, and nothing looks at the first 30 seconds or Facebook framing.** |

## What we decided

- **Rejected: "The Desk"** (seven persona "seats" reviewing at every handoff). Personas don't add
  intelligence, it would cost several reviewer runs per show (~95K tokens each), and it adds noise
  the producer learns to skim. What actually caught problems was specific evidence (Ryan's notes,
  the producer's edits, transcripts, the checker).
- **Proposed instead (not yet approved, not yet built):**
  1. **Misses log.** One line per correction from the producer, Ryan, Matt or Jeff: what, which stage
     should have caught it, and whether a rule or the checker could. Once a miss type appears twice it
     becomes a check. Open question for the producer: they say "log this", or Claude logs every
     correction it sees.
  2. **"Do we actually have it, and is it true?" check at the outline stage.** Most misses started there.
  3. **Repeated misses become mechanical checks** in `check_bible.py` / `check_outline.py`, not judgment.
  4. **Packaging, built only with the data below**; without it it's generic advice. It has two touch
     points, because packaging starts at the pitch (Jeff picks A stories "for packaging") and the open
     is written in the bible: (a) at the pitch, score the three title options in the email's
     `Potential Packaging` against the findings; (b) after the bible, final title and thumbnail text,
     a check that the first 30–60 seconds pay off the click, and a Facebook angle if Facebook turns
     out to carry its own cut. Whether that's a new skill or a reference file plus checks in the
     existing skills is decided after the findings. **No "Shorts moment"**: Shorts stopped in June
     2026 and Matt treats that as settled (`producer-kit/channel-facts.md`).
  5. **Read the show's state first:** every session reads `runs/<RUN_ID>/OPEN.md` and the latest
     outline/bible before touching anything.
- **Sequencing:** 1, 2, 3 and 5 don't need platform data. Put them to the producer for approval now
  instead of holding them until the data lands. Only 4 waits.

## What we already have (don't wait for it, don't re-request it)

| Have | Where | What it covers |
|---|---|---|
| **Timestamped transcripts of every live show, Mar 18 – Sep 29** (55 lives, ~39 min average) | `rossen-pre-bible/references/transcripts/<video id>.txt` | What was actually said, at the second, on the same timeline as the YouTube retention curve. **This is the segment map.** |
| Upload list: date, type, video id, length, current title | `rossen-pre-bible/references/channel-uploads.txt` | Every upload Mar 18 – Sep 29 |
| Current thumbnails | `https://i.ytimg.com/vi/<id>/maxresdefault.jpg` (reachable from here, checked 10/12) | The thumbnail running now, not earlier versions |
| Matt's back-catalog teardown (Aug 27, 501 videos) | Summary in `producer-kit/channel-facts.md` and `titles.md`; the source sheet is Matt's | Baselines: CTR by year, new vs returning CTR (4.26% vs 6.05%), traffic mix, runtime bands, day-of-week medians, topic medians |
| Bibles | 26 in `rossen-pre-bible/references/bibles/` (May 1 – Jul 24); 7/29, 10/7, 10/9, 10/14 in `runs/` | Aug 5 – Sep 25 (16 lives) are only in Drive |
| Ryan's retention rules | `rossen-script-writer/SKILL.md` "Retention: Ryan's structure rules"; `references/examples/ryan-notes-2026-10-09.md` | Untested claims the data can confirm or retire |

So we can **draft the episode map and the segment map ourselves** (air date, slot, video id, title,
stories, guest, sponsor reads, deals handoff, segment start times from the transcript) and ask the
team only to correct them and add the Facebook URLs. That removes the two most expensive MUST items
from their plate. The draft can be built before the data arrives.

Join on **air date**, not the bible's file date: F2 bibles are named for the tape date
(`06_22 ... AIRDATE 07_01`, `F2 07_10 BIBLE - AIRDATE 07_15`).

## The data (requested; see the .docx for the full list)

Minimum set: YouTube per-video export (last 30 episodes); retention screenshots for the 10 best and
10 worst; segment timestamps for those 20; their titles and thumbnails; Facebook per-video export.
Full set adds traffic sources and search terms, demographics, device type (TV viewing changes how we
write graphics), live concurrents and chat, Shorts, comments, and Facebook retention and distribution.

What still has to come from the team: the YouTube and Facebook exports, the retention curves, title
or thumbnail changes after publish, what actually goes on Facebook, and corrections to our draft maps.

**The key join is transcript ↔ retention**, on the same video timeline: that traces a dip to what Jeff
was saying when viewers left. The bible join comes second and answers a different question: was the
problem in what we wrote, or in how it was delivered (Jeff rewrites his lines on paper)?

**Precision is about 20–25 seconds, not a line.** The API returns retention in 100 steps of video
length (`elapsedVideoTimeRatio`), so one step is ~23 seconds of a 39-minute show; screenshots are
coarser. That resolves segments and transitions (first clip, guest, sponsor read, deals handoff),
not single lines. The first 30 seconds need Studio's "Key moments → Intro" figure (exact % at 0:30),
so keep those screenshots even with API access.

**Live vs replay:** check whether the retention curve for a live show counts live viewers or only
replay views (a vendor doc says replay only; unconfirmed). If replay only, the concurrent-viewer graph
is the live audience's retention signal, and the two audiences differ: live is the habit audience,
replay picks up browse and suggested viewers. Analyze them separately.

**Ask for the API, not screenshots.** Screenshots for 20–30 episodes are hours of team time and give
coarse curves. A one-time read-only authorization by the channel owner (`yt-analytics.readonly`)
returns the full curve and relative retention for every video, and makes the weekly refresh free.
Facebook: Business Suite Insights export; Meta renames metrics often.

**Which episodes:** not "10 best and 10 worst". Worst-by-views mostly tells us about packaging and
topic, not structure, and extremes exaggerate patterns. Use every live show that has a transcript and
a curve (all 55 with the API). If screenshots are the only route, pick ~20 spread across slots
(Wednesday, Friday deals, F2, call-in) and across the view range.

## Hypotheses, written before we look

Test the rules we already follow before adding new ones. Each gets confirmed, refined or retired.

| Claim (source) | Test |
|---|---|
| Useful info throughout holds viewers (Ryan, Oct 8: "Our best-performing live shows typically provide useful info throughout") | Tips/tells per segment from the transcript vs that segment's drop |
| Real loss first beats near-miss first (Ryan, Oct 8) | Retention through case 1 by which case led |
| A "reason to leave" line early costs viewers (Ryan's 10/9 F1 notes) | Drop in the step after such a line vs the episode's own slope |
| Cutting to the ad on an unresolved fear loses people (Ryan's 10/9 F1 notes) | Drop across sponsor reads, by what preceded them |
| Tease promises paid off by name hold the back half (Ryan, Oct 8) | Retention from the midpoint to the end, by payoff |
| Title patterns (`titles.md`): `DON'T…` commands, a dollar figure, `THIS`, `ALERT` labels | CTR and 7-day views vs the slot's median |
| Everyday money wins (kit): debit, tap to pay, tipping, the mailbox | Topic medians, scam lives only |
| New viewers click less, so packaging is the lever for them (`channel-facts.md`) | CTR by traffic source and new vs returning |
| Typical drop at the first clip, the guest, the sponsor read, the deals handoff | Segment-level drops, all lives |

## When the data arrives

1. **Ingest.** Raw files go in `data/platform/<YYYY-MM-DD>/` (YouTube/, Facebook/, records/). Keep
   them raw, with two exceptions before anything is committed: **drop revenue columns** (estimated
   revenue, RPM, CPM; the kit leaves revenue out on purpose, "ask Matt") and **drop commenter and
   chat usernames** (keep the text). Read each retention screenshot once and digitize it to a CSV;
   work from the CSV after that. Do the analysis in scripts, not by reading CSVs into the chat.
2. **Build one table per episode** from our draft episode map: metrics, the transcript segment
   map and, where we have it, the bible.
3. **Normalize before comparing.** Median long-form views roughly quadrupled from January to August,
   so raw views mostly measure when a video went up: compare each episode to the median of its
   neighbors (e.g. the 8 lives around it) and use first-7-day numbers where we have them. Compare
   within slot: Friday is the deals show and Friday medians run far below Wednesday's
   (`channel-facts.md`), so "scam vs deals" is confounded with the day. CTR depends on traffic mix and
   falls as impressions widen; compare it by traffic source. Retitled videos carry blended CTR; split
   or drop them.
4. **Segment drops within the episode.** Measure each segment's drop against that episode's own
   slope. Every show then serves as its own control, and 55 lives give hundreds of segment
   observations instead of 55 data points.
5. **Answer the questions:**
   - **Click:** which title and thumbnail patterns beat the slot's median CTR (numbers in titles, named
     brands, "DO NOT…" commands, faces vs objects). Note Target bombs.
   - **Open:** retention at 30s / 60s by open type (command hook, victim + dollar figure, question),
     and whether the open pays off the title and thumbnail.
   - **Mid-show:** the hypotheses above.
   - **Topics:** views and average view duration by scam category vs the release calendar.
   - **Facebook vs YouTube:** first find out what goes on Facebook (full live simulcast, crosspost,
     a different cut, clips). Compare the two only where it's the same video; YouTube transcript
     timings don't apply to a different cut.
6. **Write findings as evidence** in `docs/PLATFORM_FINDINGS.md`: the number, n, median and range, and
   two or three episode examples. **Call a finding stable only if it holds in both halves of the
   period** (Mar–Jun and Jul–Oct) with at least ~8 episodes on each side; everything else is
   provisional. Views vary 10x between shows, so five episodes prove little.
7. **Turn stable findings into rules** with the producer's approval, in a new dated reference (e.g.
   `references/audience-findings.md`), not in Matt's producer-kit files, which stay his words.
8. **Then design the packaging pass** from those findings.

## Close the loop (weekly, after the one-time pull)

- **Packaging log** per run (`runs/<RUN_ID>/PACKAGING.md`): the title and thumbnail options offered,
  the ones that ran, any retitle with its date, and the 7-day CTR, views and 30s retention filled in
  the following week. Each show becomes a test of the findings.
- **Weekly refresh:** the last two weeks' per-video rows and the new episodes' curves. Free with API
  access; otherwise two screenshots a week.
- **New transcripts** for each aired show (they stop at Sep 29), so the segment map stays current.

## Already known

From `producer-kit/jeff-and-ryan-rules.md`, `channel-facts.md` and `titles.md`: 62% of views are from
viewers 55+; 65+ is 37% of views and 52% of watch time; 70% returning viewers (82% of watch time).
Top shows: debit cards (2.5M), tap to pay (1.2M), tipping (1.1M), the mailbox (1.0M); live median
about 180K. Target "bombs" with the audience. The Flock camera show flopped (viewers like those
cameras). Wednesday is the best day; Friday medians are far lower. Suggested traffic watches longest;
search is ~3%; external is 1.4% despite ~1.1M followers elsewhere. The gender split conflicts between
two sources; check Studio before citing either.

## Producer answers (10/12)

1. Proposals 1, 2, 3, 5: **wait for now.**
2. Misses log, when built: **Claude logs every correction it sees.**
3. API access: **pending tomorrow's meeting (10/13).**
4. **Drop the Shorts moment.**
5. **Yes, pull the Aug 5 – Sep 25 bibles from Drive** (read-only).
6. Follow-up note: not needed; the request hasn't gone out, so revise the request itself.

## What we can do before any internal access

This container: YouTube watch pages and yt-dlp are bot-walled (checked 10/12); thumbnails
(`i.ytimg.com`) and oEmbed work.
- Revise the request .docx before it's sent.
- Draft the episode map and transcript segment map (55 lives).
- Pull and convert the Aug 5 – Sep 25 bibles.
- Download current thumbnails and tag them (face, object, words on screen); tag every title with the
  `titles.md` patterns and a topic category.
- Code each transcript for the hypotheses (open type, tips per segment, reason-to-leave lines, tease
  payoffs, sponsor and deals positions), so the data only needs joining.
- Write the ingest and analysis scripts against the expected export columns.

A browser on public pages (Chrome extension / Cowork):
- Public views, likes and comment counts for every live: a provisional outcome measure.
- The public "Most replayed" graph on each watch page. It shows replay intensity, not retention;
  label it that way.
- Public comments on the strongest and weakest shows.
- The Facebook page: what goes there (full live, crosspost, clips) and public view counts.
