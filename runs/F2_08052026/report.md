# F2 08-05-2026 Pipeline Report

**Episode:** F2 TOP STORIES — WEDNESDAY, AUGUST 5
**Script:** Amazon refunds, recalled products, phishing texts, tax-free weekend
**Beats:** 11 extracted, 0 from cold open/tease
**Beats hint:** None found
**Run date:** 2026-07-24

## Source mix, 11 beats

```
affiliate 6 · creator_long 1 · creator_short 2 · empty 2
```

2 of 11 beats are empty. 1 is a weak fit. The empties are vertical evidence beats whose content lives on TikTok or is too recent to exist on video.

## Search coverage

- YouTube + Brave web/video
- Brave API key: set
- Serper: not set (not needed, Brave covers web search)
- 5167 raw candidates -> 2993 after dedupe across 11 beats
- Re-queried 4 beats (b02, b03, b05, b07) with revised queries
- YouTube downloads blocked by 403 in cloud environment — clips need local pull

## Beat table

| Beat | Role | Or. | Pick | Platform | Source | Score | Outcue | Status |
|------|------|-----|------|----------|--------|-------|--------|--------|
| b01 | explainer_demo/creator_long | H | [DZ06YW82Qh8](https://www.youtube.com/watch?v=DZ06YW82Qh8) | youtube | creator_long | 82 | "my item didn't arrive as promised" | OK (2 segs) |
| b02 | evidence | V | — | — | — | — | — | EMPTY |
| b03 | victim_interview | H | [23OPFKfjQ5I](https://www.youtube.com/watch?v=23OPFKfjQ5I) | youtube | affiliate | 84 | "a little bit of a slap in the face" | OK |
| b04 | authority_report | H | [ttBoYQjmaVc](https://www.youtube.com/watch?v=ttBoYQjmaVc) | youtube | affiliate | 87 | "a clear and conspicuous button..." | OK |
| b05 | first_person_rant | V | [mff8NrTcRw0](https://www.youtube.com/watch?v=mff8NrTcRw0) | youtube | creator_short | 68 | "the checks have to be cashed in within 60 days" | WEAK |
| b06 | authority_report | H | [ggDHtb-4GWQ](https://www.youtube.com/watch?v=ggDHtb-4GWQ) | youtube | affiliate | 88 | "hold online marketplaces accountable in the future" | OK |
| b07 | evidence | V | — | — | — | — | — | EMPTY |
| b08 | evidence | H | [ytkn-av0Dd8](https://www.youtube.com/watch?v=ytkn-av0Dd8) | youtube | affiliate | 86 | "after ingesting bristles hidden in food" | OK (2 segs) |
| b09 | evidence | V | [55hbVRTDICA](https://www.youtube.com/shorts/55hbVRTDICA) | youtube | creator_short | 80 | "they go on a shopping spree in your name in real time" | OK |
| b10 | authority_report | H | [g6n6rFw1MHk](https://www.youtube.com/watch?v=g6n6rFw1MHk) | youtube | affiliate | 82 | "it is going to be an automatic process" | OK |
| b11 | explainer_demo/creator_long | H | [erKRMlCUNkc](https://www.youtube.com/watch?v=erKRMlCUNkc) | youtube | affiliate | 90 | "like i said this is running the whole" | OK |

## Empty beats

**b02 (evidence, V):** Amazon phantom delivery — doorbell cam showing empty porch while app says delivered. This content is overwhelmingly TikTok/Reddit vertical clips and image posts. YouTube candidates were about buying doorbell cameras, not documenting phantom deliveries. Re-queried with doorbell-specific terms; still no usable video.

**b07 (evidence, V):** Lakkzoom immersion water heater fires. CPSC emergency action was July 22, 2026 — less than 2 weeks ago. No YouTube or social video of the actual fires yet. News_web results were CPSC press releases (text only). This will surface over the next week or two as local affiliates cover it.

## Weak picks

**b05:** The 64s settlement explainer (mff8NrTcRw0) covers the checks going out, max $51, PayPal/Venmo/check. But the beat wants someone showing their SMALL payout and reacting ("PEOPLE HAVE BEEN POSTING THEIR PAYOUTS ONLINE / SOME ARE UNDER A DOLLAR / THINK WHAT YOU WOULD DO"). That's TikTok reveal content — first-person reaction, not news explainer.

## Upgraded picks (pass two re-grade)

Five beats received significantly better picks on the second grading pass:

- **b03:** Walmart third-party seller story (54tfKlslTA4, score 72) → CBC Go Public Amazon fake graphics card investigation (23OPFKfjQ5I, score 84). Named victim Matthew Lago, $700 order, Amazon refused refund. Exact A-to-Z scenario.
- **b04:** Creator explainer (xY-s26O0hkE, score 78) → WHAS11/ABC affiliate package (ttBoYQjmaVc, score 87). Andrea Fujii's report with FTC chair quote, all key settlement facts.
- **b08:** Generic grill brush demo (iB-V407xMeE, score 85) → WDIV affiliate consumer investigation (ytkn-av0Dd8, score 86). Named victim Linda, bristle in throat required surgery, magnet test demonstration.
- **b09:** Previously EMPTY → YouTube Short covering exact Amazon recall text scam (55hbVRTDICA, score 80). FTC-flagged phishing setup, vertical orientation matches beat.
- **b10:** General settlement scam warning (WZYjk1fX5hs, score 75) → WBAY Amazon-specific settlement scam warning (g6n6rFw1MHk, score 82). Wisconsin Consumer Protection official on camera.

## Flags for producer

- **b03:** Script says "LISTEN TO WHAT HAPPENED TO HER" but victim is male (Matthew Lago). Gender mismatch needs script line swap.
- **b03:** CBC is a Canadian network — may need clearance check.
- **b09:** Clip is from Rossen Reports' own YouTube channel — confirm using own content as source clip.
- **b11:** Reporter is female, script says "WATCH HIM" — minor mismatch.

## What I had to work around

1. **Re-queried 4 beats** (b02, b03, b05, b07) after pass-one triage showed poor candidates. Revised queries focused on doorbell cam evidence, Amazon marketplace buyer complaints, settlement check reaction reveals, and Lakkzoom-specific fire footage. b03 improved significantly on second pass grading.

2. **YouTube downloads blocked** (HTTP 403) in this cloud environment. Metadata and captions worked but video bytes are blocked by YouTube. All picks are logged with URLs and segment timecodes in `clips/manifest.json` for local download.

3. **2 Brave video queries failed** on b10 (connection reset). Still got 366 candidates from remaining queries.

4. **3 of 30 YouTube caption fetches returned null.** All three were on b01 where we had 3 other captioned candidates, so no impact.

## Monoculture check

Affiliate holds 6 of 9 filled picks (67%), just under the 70% threshold. Runner-up type is creator_short at 2 picks (b05, b09). The affiliate-heavy mix reflects that the best case-specific, named-victim content for these beats came from local news investigations. The two creator_short picks are both vertical-orientation beats where affiliate packages are uncommon.

## Degradation

- NOT degraded by missing search key (Brave API available)
- Degraded by missing TikTok/Instagram/Facebook direct search — 2 empty beats and 1 weak beat are vertical content that lives on those platforms
- Degraded by YouTube download block in cloud environment — clips not cut
