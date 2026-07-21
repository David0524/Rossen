---
name: rossen-query-generator
description: Generate multi-register search queries for a Rossen Reports clip beat so the right footage surfaces in the top thirty results on YouTube, TikTok, Facebook, Instagram, and Reddit. Use immediately after beat extraction, or whenever the user has beat text or a script line and needs search terms, is asking why a clip is not surfacing, wants a clip pull list, or asks anything like "how would I find footage for this." Optimizes for recall, not precision.
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

## Per-role weighting

| Role | Lead register | Also run | Platforms |
|---|---|---|---|
| `victim_interview` | news | victim | youtube, news_web |
| `confrontation_bust` | platform | news | youtube, tiktok |
| `evidence` | platform | victim | tiktok, facebook, reddit |
| `explainer_demo/creator_short` | platform | victim | tiktok, instagram |
| `explainer_demo/creator_long` | news | anchor | youtube |
| `authority_report` | anchor | news | youtube, news_web |
| `debunk` | anchor | news | youtube, news_web |
| `first_person_rant` | victim | platform | tiktok, instagram |

Orientation from the beat record is a hard filter. Horizontal beats do not get TikTok queries. Vertical beats do not get YouTube long-form queries.

## Platform syntax differences

**YouTube.** Tolerates long natural-language strings. Affiliates title predictably and index well, so news register plus role noun works: `retired police officer scammed PayPal`. This is the single highest-yield platform for the show and should get the most queries.

**TikTok.** Short. Three to five words. Hashtags help, full sentences hurt. `#scamalert paypal`, `fake bill marketplace`. Search is caption-driven, so lead with the object and the emotion, not the mechanism.

**Facebook and Instagram.** Weakest search. Lean on hashtags and creator handles. Expect low yield and do not spend query budget here.

**Reddit.** Good for evidence and screen recordings. Subreddit-scoped works well: `site:reddit.com scam text screenshot`.

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
    "platform": ["#paypalscam cop", "retired cop scammed"]
  },
  "platform_map": {
    "youtube": ["anchor", "news", "victim"],
    "news_web": ["anchor", "news"]
  }
}
```

## Glossary

`reference/glossary.md` maps editorial terms to platform-native terms. It drifts. Every time a post-mortem shows a clip that aired but did not surface, check whether a missing glossary entry explains it, and add the entry.

## Evaluation

The only metric: does the clip that actually aired appear in the top thirty results for at least one generated query. Track per register so weighting can be tuned from data rather than assumption. Report which register hit, not just whether one did.
