---
name: rossen-query-generator
description: Generate multi-register search queries for a Rossen Reports clip beat so the right footage surfaces in the top thirty results on YouTube, YouTube Shorts, TikTok, Facebook, Instagram, and Reddit. Use immediately after beat extraction, or whenever the user has beat text or a script line and needs search terms, is asking why a clip is not surfacing, wants a clip pull list, or asks anything like "how would I find footage for this." Optimizes for recall, not precision.
---

# Rossen Reports query generator

One beat in, a set of platform-tagged search strings out. A human picks the final clip, so **optimize for recall**. Thirty scannable candidates beats four correct ones. Never narrow a query to be precise.

## The problem this solves

The script and the clip share almost no vocabulary. The script says *romance scam targeting seniors through Facebook Messenger*. The clip is a woman crying in her car saying *my mom sent forty thousand dollars to a guy who said he was deployed overseas*. Search the script's words and you get PSAs. Search the victim's words and you get the clip that works on air.

So: never search the script's phrasing. Translate it into the register the footage was actually titled and captioned in.

## Four registers

Generate all four per beat. Six to ten strings each. Weight by role using the table further down.

**News register.** Affiliate and network headline syntax. Present tense, third person, noun-heavy, no contractions. *Woman loses life savings*, *police warn of*, *families targeted by*, *what to know about*. **Do not add a city name.** Affiliates carry national wire packages, so the affiliate that surfaces is usually nowhere near the event. Search the story, not the location.

**Victim register.** First person, emotional, ungrammatical, present tense, no jargon. *I can't believe I fell for this*, *they took everything*, *my mom sent them the money*. Works on TikTok, and also surfaces affiliate packages, because affiliates routinely title with the victim's own quote.

**Platform register.** Native slang and hashtags. Romance scam is catfish. Pig butchering is crypto scam or investment guy. Facebook Marketplace is FBMP. Keep queries short here; TikTok search degrades badly past four or five words, where YouTube tolerates a full sentence.

**Anchor register.** The literal proper nouns from the beat: company, dollar figure, agency, state, regulatory action, product name. *Temu $232 million fine*. *Maryland dynamic pricing ban*. *Meta 10% revenue scams*. When the beat has a dated news anchor this register has the highest hit rate of the four and it costs one query. Always check for it first.

### The platform register has two dialects

Platform register splits by destination. TikTok-flavored and Shorts-flavored strings are not interchangeable and both get generated whenever the platform register runs.

**Shorts dialect.** Shorter than TikTok, hashtag-heavy, emotion-forward. Three to five words plus one or two hashtags, and the emotional payload goes in the words, not the mechanism. `#scamalert she lost everything`, `#shorts grandma scammed crying`, `mom fell for it #scam`. Lead with the feeling and the person. Do not describe the fraud type — Shorts titles almost never do. A Shorts title is written to stop a thumb, so it reads like a reaction, not a report.

## Per-role weighting

| Role | Lead register | Also run | Platforms |
|---|---|---|---|
| `victim_interview` | news | victim | youtube, shorts, news_web |
| `confrontation_bust` | platform | news | youtube, shorts, tiktok |
| `evidence` | platform | victim | tiktok, shorts, facebook, reddit |
| `explainer_demo/creator_short` | platform | victim | shorts, tiktok, instagram |
| `explainer_demo/creator_long` | news | anchor | youtube |
| `authority_report` | anchor | news | youtube, news_web |
| `debunk` | anchor | news | youtube, news_web |
| `first_person_rant` | victim | platform | shorts, tiktok, instagram |

Orientation from the beat record is a hard filter on **TikTok, Instagram and Facebook**. Horizontal beats do not get TikTok queries. Vertical beats do not get YouTube long-form queries.

**Measured, not assumed, for the `victim` and `also run` cells below.** A recall@30 eval on horizontal/YouTube beats (n=8 testable) found the `victim` register contributed **zero** — no hits at any rank, no unique contribution — while `platform` found every hit that surfaced at all. See "Measured evaluation results" further down before trusting `victim` as a horizontal/YouTube register; it is unproven there and untested on vertical, which is where it was theorized to matter.

**Shorts are the exception, and run on every orientation.** A four-minute affiliate package buries the raw victim moment at 1:30 under a reporter standup and a b-roll walk-and-talk. A 45-second Short of the same woman crying about her retirement is the moment with nothing on top of it. That is what goes on air. So generate Shorts queries for every vertical beat, every beat where the platform register runs, and every horizontal beat as well.

Tag Shorts candidates surfaced against a horizontal beat as `orientation: vertical, surfaced_for: horizontal` so the grader knows the producer's orientation call is being deliberately crossed and can rule on framing rather than silently failing it.

## Platform syntax differences

**YouTube.** Tolerates long natural-language strings. Affiliates title predictably and index well, so news register plus role noun works: `retired police officer scammed PayPal`. This is the single highest-yield platform for the show and should get the most queries.

**YouTube Shorts.** Same index as YouTube, different title conventions and a hard duration ceiling, so it is worth searching as its own platform rather than hoping Shorts fall out of a long-form query. They do not — long-form queries are noun-heavy and Shorts titles are not.

Emit Shorts queries as explicit search strings so the harvest step can run them directly:

```bash
yt-dlp "ytsearch30:<query> #shorts" \
  --match-filter "duration < 60" \
  --flat-playlist --dump-json
```

Every Shorts query string carries the `#shorts` suffix and every Shorts query runs under `--match-filter "duration < 60"`. Without the filter the `#shorts` token alone leaks long-form uploads that merely mention Shorts in the description; without the suffix the duration filter leaves you searching all of YouTube and discarding 90% of it.

Two operational notes. `--flat-playlist` sometimes returns null durations, in which case the match filter silently passes everything — drop `--flat-playlist` for Shorts runs if the returned set looks long-form. And a 60-second ceiling is the format definition, not a quality signal; see the grader's triage rules.

Write them into the output as ordinary query strings under a `shorts` register. The suffix and the filter are the harvest step's job to apply, not something to bake into every string by hand.

**TikTok.** Short. Three to five words. Hashtags help, full sentences hurt. `#scamalert paypal`, `fake bill marketplace`. Search is caption-driven, so lead with the object and the emotion, not the mechanism. Distinct from the Shorts dialect: TikTok tolerates the mechanism as the object, Shorts wants the person and the feeling.

**Facebook and Instagram.** Weakest search. Lean on hashtags and creator handles. Expect low yield and do not spend query budget here.

**Reddit.** Good for evidence and screen recordings. Subreddit-scoped works well: `site:reddit.com scam text screenshot`.

**TikTok ships no captions.** yt-dlp returns no subtitle track for TikTok, period. A TikTok pick cannot get a verbatim outcue from the harvest step alone — it needs a transcription pass (Whisper or equivalent) between grading and the outcue check. If that pass isn't wired into the pipeline you're running, treat any TikTok pick as `sourcability: high` but flag the outcue as unverified rather than inventing one.

**Brave TikTok search yields mostly non-video pages.** A `site:tiktok.com` web search returns TikTok's browse/discover/profile pages far more often than actual `/video/` or `/photo/` permalinks — a measured sample put real videos at roughly 19% of raw results. `rossen_harvest/brave.py`'s platform detector already filters for the literal `/video/` path segment, so non-video TikTok pages fall through to `news_web` rather than being miscounted as TikTok candidates — but expect the raw TikTok yield per query to look sparse for this reason, and don't read it as the query missing.

## Confrontation vocabulary

This role has its own lexicon that shares nothing with the others and it is worth its own list: *caught on camera*, *confronts*, *busted*, *exposed*, *called out*, *sting operation*, *undercover*, *scammer gets caught*, *I confronted the*.

## Output

```json
{
  "beat_id": "05-06-b03",
  "clip_role": "victim_interview",
  "orientation": "horizontal",
  "queries": {
    "anchor": ["retired police officer PayPal scam $10,000"],
    "news": ["retired officer loses savings PayPal scam",
             "former police officer scammed out of thousands",
             "police officer falls for PayPal scam"],
    "victim": ["I was a cop and I got scammed",
               "he spent his career busting criminals then got scammed"],
    "platform": ["#paypalscam cop", "retired cop scammed"],
    "shorts": ["#scamalert retired cop robbed",
               "cop lost his savings #shorts",
               "#paypalscam he cried",
               "30 years a cop then this #scam"]
  },
  "platform_map": {
    "youtube": ["anchor", "news", "victim"],
    "shorts": ["shorts", "victim"],
    "news_web": ["anchor", "news"]
  },
  "shorts_search": {
    "suffix": "#shorts",
    "match_filter": "duration < 60",
    "surfaced_for": "horizontal"
  }
}
```

## Glossary

`reference/glossary.md` maps editorial terms to platform-native terms. It drifts. Every time a post-mortem shows a clip that aired but did not surface, check whether a missing glossary entry explains it, and add the entry.

## Measured evaluation results

The per-role weighting table above is largely inferred from the aired-examples calibration set. One real recall@30 run against `rossen_eval_worksheet.csv` has since measured it, horizontal/YouTube beats only (n=9 rows, 8 testable after a data-quality bug in the worksheet — see below):

**recall@30 = 0.889.** Above the 70% "build on it" threshold. When a query hits, it ranks well: median best-rank 1, max 3.

| register | any (found it) | best (found it first) | unique (only register that found it) |
|---|---|---|---|
| platform | 8 | 2 | **1** |
| news | 6 | 4 | 0 |
| anchor | 5 | 2 | 0 |
| victim | **0** | 0 | 0 |

Read this carefully — it is one small sample, not a settled result:

- **`platform` is the workhorse register on horizontal/YouTube beats.** It found every hit that surfaced at all. This is consistent with the current table's lead-register assignments for most roles, and is the strongest evidence yet that `platform` deserves its query budget even on YouTube, not just TikTok/Shorts.
- **`victim` found nothing on horizontal/YouTube beats in this sample.** That does not mean drop it — `victim` was theorized to matter most on vertical platforms (TikTok, first-person content), which this eval did not test. Treat `victim`'s place in the `victim_interview` and `evidence` rows above as unproven-not-disproven until a vertical-specific eval runs.
- **`news` and `anchor` have wide coverage (any) but zero unique contribution** in this sample — every hit they found, `platform` also found. Their value here looks like it's in *rank quality* (news found the best rank 4 of 8 times) and in dated-event beats specifically (anchor's natural strength), not in reach.
- **The one miss** was a beat whose aired clip was titled in investigative-journalism house style (a station's "Investigates" franchise brand) rather than plain news-headline syntax — see the glossary entry this added.

**Data-quality note, if you re-run this eval:** roughly half the YouTube URLs in `rossen_eval_worksheet.csv` were found fully uppercased in one copy of the worksheet, which corrupts case-sensitive video IDs and silently drops rows from the eval. Verify URL casing before trusting a low recall number — it may be a worksheet bug, not a query failure.

## Evaluation

The only metric: does the clip that actually aired appear in the top thirty results for at least one generated query. Track per register so weighting can be tuned from data rather than assumption. Report which register hit, not just whether one did.
