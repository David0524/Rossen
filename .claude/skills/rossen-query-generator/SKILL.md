---
name: "rossen-query-generator"
description: Generate multi-register search queries for a Rossen Reports clip beat so the right footage surfaces in the top thirty results on YouTube, YouTube Shorts, TikTok, Facebook, Instagram, and Reddit. Use immediately after beat extraction, or whenever the user has beat text, an outline row, or a script line and needs search terms, is asking why a clip is not surfacing, wants a clip pull list, or asks anything like "how would I find footage for this." Optimizes for recall, not precision.
---

# Rossen Reports query generator

One beat in, a set of platform-tagged search strings out. A human picks the final
clip, so **optimize for recall**. Thirty scannable candidates beats four correct
ones. Never narrow a query to be precise.

## Bundled files

| File | Load when |
|---|---|
| `eval.md` | Tuning register weights, or deciding whether a register earns its budget. Measured results and the eval protocol. |
| `scripts/check_queries.py` | **Before handing off.** Validates the output contract. |
| `scripts/normalize_urls.py` | Before any eval run, on any calibration file. |

## The problem this solves

Beats arrive from the outline (via `rossen-beat-extractor`, outline mode) as part of
the outline w/ videos stage; `script_text` is the outline row plus the pre-bible's
specifics. The field keeps its name for the schema.

The beat text and the clip share almost no vocabulary. The beat says *romance scam
targeting seniors through Facebook Messenger*. The clip is a woman crying in her car
saying *my mom sent forty thousand dollars to a guy who said he was deployed
overseas*. Search the beat's words and you get PSAs. Search the victim's words and
you get the clip that works on air.

So: never search the beat's phrasing. Translate it into the register the footage
was actually titled and captioned in.

## Five registers

Generate all five per beat. **`shorts` is a first-class register, not a dialect** —
the pipeline's `ShortsBackend` reads it by name, so a record that omits the key
starves the only vertical surface with a reachable search index.

**Anchor register.** The literal proper nouns from the beat: company, dollar figure,
agency, state, regulatory action, product name. *Temu $232 million fine*. *Maryland
dynamic pricing ban*. On a dated-event beat this has the highest hit rate of the
five and it costs one query. **Always check for it first — and check the beat record
first.** The beat extractor emits a prebuilt `news_anchor` string; when it is
present that string is anchor query #1. Build around it, do not regenerate it.

**News register.** Affiliate and network headline syntax. Present tense, third
person, noun-heavy, no contractions. *Woman loses life savings*, *police warn of*,
*families targeted by*. **Do not add a city name.** Affiliates carry national wire
packages, so the affiliate that surfaces is usually nowhere near the event. Search
the story, not the location.

**Platform register.** Native slang and hashtags, aimed at TikTok. Romance scam is
catfish. Pig butchering is crypto scam or investment guy. Facebook Marketplace is
FBMP. Keep it short — TikTok search degrades badly past four or five words, where
YouTube tolerates a full sentence.

**Shorts register.** Shorter than TikTok, hashtag-heavy, emotion-forward. Three to
five words plus one or two topical hashtags, and the emotional payload goes in the
words, not the mechanism: `#scamalert she lost everything`, `grandma scammed
crying`, `mom fell for it #scam`. Lead with the feeling and the person. Do not
describe the fraud type — Shorts titles almost never do. A Shorts title is written
to stop a thumb, so it reads like a reaction, not a report.

**Never write `#shorts` into a query string.** The harvest step appends it (see
Platform syntax below). Baking it in double-appends the token and eats query length
that the dialect can't spare. Topical hashtags belong in the string; `#shorts` does
not.

**Victim register.** First person, emotional, ungrammatical, present tense, no
jargon. *I can't believe I fell for this*, *they took everything*, *my mom sent them
the money*. **Measured at zero on horizontal/YouTube beats, twice** — see the table
below and `eval.md`. Run it on vertical, where it is theorized to matter and remains
untested; treat it as optional on horizontal.

## How many strings

| Register | Strings per beat |
|---|---|
| anchor | 0–3 (0 is fine — not every beat has a dated anchor) |
| news | 2–5 |
| platform | 2–4 |
| shorts | 2–5 |
| victim | 0–3 (0 on horizontal is the default) |
| **Total** | **10–15, ceiling 18** |

**The ceiling is a real constraint, not a style note.** At 10–12 beats a Wednesday
episode, 15 strings a beat is ~150–180 queries and a ~2-minute search stage. At 40
strings a beat it is ~480 queries and the search stage stops fitting inside the
pipeline's budget. Spend the ceiling on the registers the role's row leads with.

Emit every one of the five keys, even when a register is deliberately empty — an
empty list with a reason is distinguishable from a generation miss; a missing key is
not.

## Per-role weighting

| Role | Lead register | Also run | Platforms |
|---|---|---|---|
| `victim_interview` | news | platform · *(victim: 0, optional)* | youtube, shorts, news_web |
| `confrontation_bust` | platform | news | youtube, shorts, tiktok |
| `evidence` | platform | victim | tiktok, shorts, facebook, reddit |
| `explainer_demo/creator_short` | platform | victim | shorts, tiktok, instagram |
| `explainer_demo/creator_long` | news | anchor | youtube |
| `authority_report` | anchor | news | youtube, news_web |
| `debunk` | anchor | news | youtube, news_web |
| `first_person_rant` | victim | platform | shorts, tiktok, instagram |

**The `victim: 0` annotation is measured, not cautious.** A recall@30 eval (n=8
horizontal/YouTube) found `victim` contributed zero — no hits at any rank, no unique
contribution — and an independent probe on a different index reproduced it.
`victim_interview` is the most common role in the calibration set (7 of 26) and its
platform row is horizontal/YouTube, so it is exactly the population that was
measured. Spend those strings on `platform`, which found every hit that surfaced at
all. `victim` stays unqualified on the vertical rows, where it has not been tested.

**Orientation is a hard filter in both directions.** Horizontal beats get no TikTok,
Instagram or Facebook queries. Vertical beats get no YouTube long-form queries.
Producer-authored, and it predicted the platform correctly in 26 of 26 observed
cases.

**Shorts is the sole exception and runs on every orientation.** A four-minute
affiliate package buries the raw victim moment at 1:30 under a reporter standup and
a b-roll walk-and-talk. A 45-second Short of the same woman crying about her
retirement is the moment with nothing on top of it. That is what goes on air. So
generate Shorts queries for every beat, both orientations.

When Shorts run against a **horizontal** beat, set `shorts_search.cross_orientation:
true`. The harvester then tags each returned Shorts candidate `orientation:
vertical, surfaced_for: horizontal`. **That tag is per-candidate and the harvester
applies it** — the clip grader reads it per candidate to know the producer's
orientation call is being deliberately crossed, and rules on framing rather than
silently failing it. Do not put `surfaced_for` in the beat's query record; there is
nothing there for the grader to read.

## Platform syntax differences

**YouTube.** Tolerates long natural-language strings. Affiliates title predictably
and index well, so news register plus role noun works: `retired police officer
scammed PayPal`. Highest-yield platform for the show; give it the most queries.

**YouTube Shorts.** Same index as YouTube, different title conventions and a hard
duration ceiling, so search it as its own surface rather than hoping Shorts fall out
of a long-form query. They do not — long-form queries are noun-heavy and Shorts
titles are not.

The harvest step runs each `shorts` string like this:

```bash
yt-dlp "ytsearch30:<query> #shorts" \
  --match-filter "duration < 60" \
  --flat-playlist --dump-json
```

Both halves are required and **both are the harvest step's job, not yours.** Without
the duration filter the `#shorts` token alone leaks long-form uploads that merely
mention Shorts in the description; without the suffix the filter leaves you
searching all of YouTube and discarding 90% of it. Emit plain strings under the
`shorts` key and let the harvester add the suffix and the filter.

Two operational notes. `--flat-playlist` sometimes returns null durations, in which
case the match filter silently passes everything — drop `--flat-playlist` for Shorts
runs if the returned set looks long-form. And a 60-second ceiling is the format
definition, not a quality signal; see the grader's triage rules.

**TikTok.** Short. Three to five words. Hashtags help, full sentences hurt.
`#scamalert paypal`, `fake bill marketplace`. Search is caption-driven, so lead with
the object and the emotion, not the mechanism. Distinct from the Shorts dialect:
TikTok tolerates the mechanism as the object, Shorts wants the person and the
feeling.

**Facebook and Instagram.** Weakest search. Lean on hashtags and creator handles.
Expect low yield and spend little of the ceiling here.

**Reddit.** Good for evidence and screen recordings. Subreddit-scoped works well:
`site:reddit.com scam text screenshot`.

**TikTok ships no captions.** yt-dlp returns no subtitle track for TikTok, period, so
a TikTok pick cannot get a verbatim outcue from the harvest step alone.
`rossen_harvest/vertical_transcribe.py` closes this — it downloads the clip and
transcribes locally with faster-whisper (CPU, no GPU), producing the same
`Transcript`/`Cue` shape `transcripts.py` does, so `.find()` and `.segment()` verify
a TikTok outcue exactly like a YouTube one. Run it in pass two, on the shortlist
only. If the dependency isn't installed, treat the TikTok pick as `sourcability:
high` but flag the outcue unverified rather than inventing one.

**Brave TikTok search yields mostly non-video pages.** A `site:tiktok.com` web search
returns browse/discover/profile pages far more often than real `/video/` or `/photo/`
permalinks — a measured sample put real videos at roughly **19%** of raw results.
`rossen_harvest/brave.py`'s platform detector filters for the literal `/video/` path
segment, so non-video pages fall through to `news_web` rather than being miscounted
as TikTok candidates. Expect raw TikTok yield per query to look sparse for this
reason; do not read it as the query missing.

## Confrontation vocabulary

This role has its own lexicon that shares nothing with the others: *caught on
camera*, *confronts*, *busted*, *exposed*, *called out*, *sting operation*,
*undercover*, *scammer gets caught*, *I confronted the*.

## Output

Five register keys, always. Then validate:

```bash
python3 scripts/check_queries.py queries.json
```

```json
{
  "beat_id": "05-06-b03",
  "clip_role": "victim_interview",
  "orientation": "horizontal",
  "news_anchor": "retired police officer PayPal scam $10,000",
  "queries": {
    "anchor": ["retired police officer PayPal scam $10,000"],
    "news": ["retired officer loses savings PayPal scam",
             "former police officer scammed out of thousands",
             "police officer falls for PayPal scam"],
    "platform": ["#paypalscam cop", "retired cop scammed", "cop paypal refund scam"],
    "shorts": ["#scamalert retired cop robbed",
               "cop lost his savings",
               "#paypalscam he cried",
               "30 years a cop then this #scam"],
    "victim": []
  },
  "queries_note": {
    "victim": "empty by rule — measured 0 on horizontal/YouTube, budget spent on platform"
  },
  "platform_map": {
    "youtube": ["anchor", "news", "platform"],
    "shorts": ["shorts"],
    "news_web": ["anchor", "news"]
  },
  "shorts_search": {
    "suffix": "#shorts",
    "match_filter": "duration < 60",
    "cross_orientation": true
  }
}
```

Eleven strings, inside the 10–15 band. `anchor` query #1 is the beat's prebuilt
`news_anchor` verbatim. No string carries `#shorts`. `victim` is present and empty
with its reason. `cross_orientation` is set because this is a horizontal beat with
Shorts queries, and the harvester will tag the candidates it returns.

## Glossary

`reference/glossary.md` maps editorial terms to platform-native terms. It drifts.
Every time a post-mortem shows a clip that aired but did not surface, check whether a
missing glossary entry explains it, and add the entry. One entry already came from a
recall miss on a station's "Investigates" franchise naming.

## Evaluation

Full protocol, measured results, data-quality warnings and the open vertical eval are
in `eval.md`. The short version:

**The only metric: does the clip that actually aired appear in the top thirty results
for at least one generated query.** Track per register — `any`, `best`, `unique` —
and report which register hit, not just whether one did.

**Before any eval run, repair URL casing.** Uppercased URLs corrupt case-sensitive
video IDs and silently drop rows. `aired_examples.md` currently carries this bug in
13 of its 26 URLs:

```bash
python3 scripts/normalize_urls.py reference/aired_examples.md
```

The corruption is lossy — flagged IDs need re-sourcing by title, and a corrupted row
is a data-quality drop, never an eval miss.
