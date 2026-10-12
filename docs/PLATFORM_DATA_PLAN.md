# Platform data plan (handoff, 10/12/2026)

Status: **waiting on data.** The producer sent the team `docs/Rossen Audience Data Request.docx`
(YouTube + Facebook + our own records). Nothing below is built yet. No skill changes until the
producer approves (standing rule).

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
| **YouTube / Facebook optimizer** | **Nothing checks titles, thumbnails, the first 30 seconds, Shorts or Facebook framing at all.** |

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
  4. **A packaging skill**, run once per show after the bible: title options, thumbnail text, the first
     30 seconds, the Shorts moment and a Facebook angle. **Build only with the data below**; without it
     it's generic advice.
  5. **Read the show's state first:** every session reads `runs/<RUN_ID>/OPEN.md` and the latest
     outline/bible before touching anything.

## The data (requested; see the .docx for the full list)

Minimum set: YouTube per-video export (last 30 episodes); retention screenshots for the 10 best and
10 worst; **segment timestamps** for those 20; their titles and thumbnails; Facebook per-video export.
Full set adds traffic sources and search terms, demographics, device type (TV viewing changes how we
write graphics), live concurrents and chat, Shorts, comments, and Facebook retention and distribution.

**The key join:** an episode map (air date, F1/F2, YouTube and Facebook URLs, bible file, stories,
guest, sponsor) plus **segment start times per episode**. That is what lets a retention dip be traced
to the exact bible line. Without it the numbers show where viewers leave, not why.

Retention curves: Studio shows them per video but doesn't bulk-export them, so screenshots to start.
The YouTube Analytics API returns full curves if the channel owner grants access once (worth it for
weekly use). Facebook: Business Suite Insights export; Meta renames metrics often.

## When the data arrives

1. Put raw files in `data/platform/<YYYY-MM-DD>/` (YouTube/, Facebook/, records/). Keep them raw.
2. Build one table per episode: metrics joined to the episode map and the bible (the 26 archived
   bibles are in `rossen-pre-bible/references/bibles/`; the release calendar and Topic Assignments
   sheets are in Drive).
3. Questions to answer first:
   - **Click:** which title and thumbnail patterns beat the channel median CTR (scam vs deals,
     numbers in titles, named brands, "DO NOT…" commands, faces vs objects). Note Target bombs.
   - **Open:** retention at 30s / 60s by open type (command hook, victim + dollar figure, question).
   - **Mid-show:** typical drop at the first clip, the guest, the sponsor read, the deals handoff.
   - **Topics:** views and average view duration by scam category vs the release calendar.
   - **Facebook vs YouTube:** does the same story hold differently on each.
4. Write findings as evidence (numbers, episode examples), then turn the stable ones into rules in
   the skills, with the producer's approval. Mark anything from fewer than ~5 episodes provisional.
5. Then design the packaging skill from those findings.

## Already known (from the producer kit, `rossen-pre-bible/references/producer-kit/jeff-and-ryan-rules.md`)

62% of views are from viewers 55+; 65+ is 37% of views and 52% of watch time; 70% returning viewers.
Top shows: debit cards (2.5M), tap to pay (1.2M), tipping (1.1M), the mailbox (1.0M). Target "bombs"
with the audience. The Flock camera show flopped (viewers like those cameras).
