# F2 08-05-2026 Pipeline Report

**Episode:** F2 TOP STORIES — WEDNESDAY, AUGUST 5
**Script:** Amazon refunds, recalled products, phishing texts, tax-free weekend
**Beats:** 11 extracted, 0 from cold open/tease
**Beats hint:** None found
**Run date:** 2026-07-24

## Source mix, 11 beats

```
affiliate 3 · creator_long 2 · creator_short 1 · first_person 1 · empty 3 · weak 1
```

3 of 11 beats are empty. 1 is a weak fit. The empties are all vertical evidence/rant beats whose natural content lives on TikTok, not YouTube. One (b07) is too recent for coverage to exist.

## Search coverage

- YouTube + Brave web/video
- Brave API key: set
- Serper: not set (not needed, Brave covers web search)
- 5167 raw candidates -> 2993 after dedupe across 11 beats
- Re-queried 4 beats (b02, b03, b05, b07) with revised queries
- YouTube downloads blocked by 403 in cloud environment — clips need local pull

## Beat table

| Beat | Role | Or. | Pick | Platform | Source | Dur | Outcue | Status |
|------|------|-----|------|----------|--------|-----|--------|--------|
| b01 | explainer_demo/creator_long | H | [DZ06YW82Qh8](https://www.youtube.com/watch?v=DZ06YW82Qh8) | youtube | creator_long | 283s | "my item didn't arrive as promised" | OK (2 segs) |
| b02 | evidence | V | — | — | — | — | — | EMPTY |
| b03 | victim_interview | H | [54tfKlslTA4](https://www.youtube.com/watch?v=54tfKlslTA4) | youtube | affiliate | 134s | "a 30% restocking fee" | WEAK |
| b04 | authority_report | H | [xY-s26O0hkE](https://www.youtube.com/watch?v=xY-s26O0hkE) | youtube | creator_long | 204s | "changes how Amazon runs its Prime program" | OK |
| b05 | first_person_rant | V | [mff8NrTcRw0](https://www.youtube.com/watch?v=mff8NrTcRw0) | youtube | creator_short | 64s | "the checks have to be cashed in within 60 days" | WEAK |
| b06 | authority_report | H | [ggDHtb-4GWQ](https://www.youtube.com/watch?v=ggDHtb-4GWQ) | youtube | affiliate | 154s | "hold online marketplaces accountable in the future" | OK |
| b07 | evidence | V | — | — | — | — | — | EMPTY |
| b08 | evidence | H | [iB-V407xMeE](https://www.youtube.com/watch?v=iB-V407xMeE) | youtube | first_person | 228s | "they're more likely to end up on your grilling surface" | OK (2 segs) |
| b09 | evidence | V | — | — | — | — | — | EMPTY |
| b10 | authority_report | H | [WZYjk1fX5hs](https://www.youtube.com/watch?v=WZYjk1fX5hs) | youtube | affiliate | 132s | "anything higher is suspicious" | OK |
| b11 | explainer_demo/creator_long | H | [erKRMlCUNkc](https://www.youtube.com/watch?v=erKRMlCUNkc) | youtube | affiliate | 128s | "like i said this is running the whole" | OK |

## Empty beats

**b02 (evidence, V):** Amazon phantom delivery — doorbell cam showing empty porch while app says delivered. This content is overwhelmingly TikTok/Reddit vertical clips and image posts. YouTube candidates were about buying doorbell cameras, not documenting phantom deliveries. Re-queried with doorbell-specific terms; still no usable video.

**b07 (evidence, V):** Lakkzoom immersion water heater fires. CPSC emergency action was July 22, 2026 — less than 2 weeks ago. No YouTube or social video of the actual fires yet. News_web results were CPSC press releases (text only). This will surface over the next week or two as local affiliates cover it.

**b09 (evidence, V):** Fake Amazon recall phishing text screenshot. r/Scams has multiple text-only posts confirming the scam exists, but no video. The content (phone screen recording of a scam text arriving) lives on TikTok. Fox news_web result may have video but isn't downloadable.

## Weak picks

**b03:** The Walmart third-party seller story (54tfKlslTA4) is the closest available. Couple orders table+chairs, gets only table, seller demands 30% restocking fee. Affiliate package, sympathetic victims on camera. But it's a Walmart story, not Amazon A-to-Z. The script says "LISTEN TO WHAT HAPPENED TO HER" and the clip has Amanda on camera, so the gender matches. A direct Amazon A-to-Z denial interview did not surface.

**b05:** The 64s settlement explainer (mff8NrTcRw0) covers the checks going out, max $51, PayPal/Venmo/check. But the beat wants someone showing their SMALL payout and reacting ("PEOPLE HAVE BEEN POSTING THEIR PAYOUTS ONLINE / SOME ARE UNDER A DOLLAR / THINK WHAT YOU WOULD DO"). That's TikTok reveal content — first-person reaction, not news explainer.

## What I had to work around

1. **Re-queried 4 beats** (b02, b03, b05, b07) after pass-one triage showed poor candidates. Revised queries focused on doorbell cam evidence, Amazon marketplace buyer complaints, settlement check reaction reveals, and Lakkzoom-specific fire footage. b03 improved slightly; the other three remained empty or weak.

2. **YouTube downloads blocked** (HTTP 403) in this cloud environment. Metadata and captions worked but video bytes are blocked by YouTube. All picks are logged with URLs and segment timecodes in `clips/manifest.json` for local download.

3. **2 Brave video queries failed** on b10 (connection reset). Still got 366 candidates from remaining queries.

4. **3 of 30 YouTube caption fetches returned null.** All three were on b01 where we had 3 other captioned candidates, so no impact.

## Monoculture check

No single source type holds 70%+ of the 8 filled picks. affiliate 3, creator_long 2, creator_short 1, first_person 1, plus the 3 empties. Mix is healthy.

## Degradation

- NOT degraded by missing search key (Brave API available)
- Degraded by missing TikTok/Instagram/Facebook direct search — 3 of 4 empty/weak beats are vertical content that lives on those platforms
- Degraded by YouTube download block in cloud environment — clips not cut
