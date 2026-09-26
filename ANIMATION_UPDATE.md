# Rossen Reports animation work: status update

This is a status update for anyone following along from outside this session. It is not a full handoff. It sits next to `HANDOFF.md`, which covers the separate clip-discovery system; that work is untouched.

In four working days (Sept 23–26) this repo gained an in-house animation pipeline for Jeff's social channels. There are 17 finished videos in `final-videos/`, a set of 7 Instagram/Facebook Story slides, and reusable series templates, so new episodes take hours rather than days.

---

## What exists now

### The look

The case-file screen print:
- flat inks sampled from the official logo (blue, black, cream, yellow; no red);
- paper-cutout puppets on paper stock;
- rubber stamps, pinned index cards and halftone dots.

Every film is 96 BPM. One idea lands per bar, and every landing hits the beat. The standing client direction (readable text, when to use creative transitions, the closing card) is written up in `intro/SKILL_NOTES.md` §0. New work is expected to follow it.

### Characters

The puppets are cut from reference art into jointed pieces that move:
- **Jeff**, on every video.
- **The Scammer**, with three new costume versions:
  - the fake officer;
  - a knockoff seller whose trench coat of fakes opens and closes;
  - a fake tech-support agent whose headset comes off.
- **An everyday man** (the recurring victim or shopper).
- **Grandma and the grandson** (What Would You Do? #1).

### Finished videos (`final-videos/`)

| # | Video | Notes |
|---|---|---|
| 01–02 | Case File intro (16:9 and 9:16) | The show opener |
| 03 | MyChart scam explainer | |
| 04 | LIVE TODAY promo (Zelle scam) | |
| 05 | Scam or Legit? quiz | |
| 06, 07, 16 | **Jeff's Rules** #1–#3 | Series template: Hang Up, Call Back · Gift Cards Are for Gifts · Check the Seller |
| 08, 17 | **What Would You Do?** #1–#2 | Series template: grandparent scam · fake virus pop-up |
| 09–10 | LIVE TODAY loops | Wednesday 5 PM, Friday 10 AM |
| 11 | Fake officer / jury-duty scam explainer | |
| 12 | Friday live tease + Amazon promo codes + loop ×2 | |
| 13 | Unpaid-toll text scam explainer | Borrows selectively from the Vox playbook: evidence mark-up, a 2.5D camera, one sourced stat |
| 14–15 | "Still Live" weekend deals roundup | Facebook and Instagram versions; only the CTA differs |

Also produced: 7 Story slides for the deals (a title, one slide per deal, and "Tune in next Friday"), each a 5-second perfect loop plus a PNG still, in `intro/out/rossen-deals-stories/`.

Every short ends on the same minimal closing card: the official logo, then WED 5 PM ET / FRI 10 AM ET, then LIVE ON YouTube · Instagram. The newest videos add Facebook to that line; older ones were deliberately left as they were.

### How it's built

Everything is code, and every frame is drawn from data:
- The films are HTML canvas pages rendered frame by frame to mp4 (`intro/render.mjs`).
- **Series templates:**
  - `rules.js` with `rules/template.json` (Jeff's Rules);
  - `wwyd.js` with `wwyd/template.json` (What Would You Do?).

  The recurring parts (title card, rule reveal, freeze and countdown, answer stings, end card) are fixed. An episode supplies only a data file and its middle scenes. New episodes are checked frame for frame against episode 1 to prove the recurring parts didn't drift.
- **Data-driven deals:** `intro/deals/deals.json` holds the names, exact price strings, codes and CTAs. Percent off is computed from the prices, never typed. Changing that one file and running one command rebuilds both Reels and all the Stories.
- **Music and sound:**
  - The scores are composed in code on the beat grid and played by recorded orchestral samples (VSCO 2 CE).
  - All sound effects are Kenney recordings.
  - Both libraries are CC0 (public domain dedication), so there's no Content ID exposure.
  - Each video logs its sources in `audio_sources.txt` and says which sounds are composed.
- **Verification on every final mp4:**
  - frame stillness while text is read;
  - audio–picture sync, measured in milliseconds against a log of every hit;
  - a safe-zone overlay pass;
  - the logo and platform icons checked against their files;
  - for the deals, OCR of every price, plus the percent sticker matched against all values from 0% to 99%.

  The results are saved as `verify.txt` / `sync.txt` next to each video.
- **Documentation:** `intro/README.md` has a section per film with its build command. `intro/SKILL_NOTES.md` holds the lessons learned, and `intro/VOX_STUDY.md` the research notes on the Vox style.

---

## Open items

1. **Deals price-check time.** `intro/deals/deals.json` still reads `"time": "{{time}}"`. Fill it in and run `cd intro && sh tools/build_deals.sh && python3 tools/verify_stories.py` (about 14 minutes). Only the Reel's price note uses it; the Stories no longer show it.
2. **Posting the Stories.** The link sticker is added in the app. Each deal slide has a dashed outline and an arrow showing where it goes. The slides are silent, so add music in the app if you want it.
3. **Rights check on one product photo.** The vibration-plate photo includes a model. It's the retailer's listing image, used untouched as requested, but confirm it's cleared.
4. **A series-wide style question (awaiting your decision).** The two series templates land captions with a small bounce and tilt that settles in about 0.4 s. That's looser than the gentler landing in the newer videos. Tightening it would change the earlier episodes too, so it's left as is until you decide.
5. **Known template sync quirk.** A few template sounds measure 16–21 ms late at the half-rise point (the scene-start caption tick and the Rules hook). They're identical in every episode, so they were kept. Everything episode-specific is within 10 ms.
6. **Performance numbers haven't been collected.** Views, watch time and comment rates on the "comment A/B/C" episodes haven't been pulled yet. They're the proof for item 7.
7. **Ownership and outreach.** Before offering this service to other creators, confirm with Jeff's side what is his (his puppet, logos and this specific look) and what is reusable (the pipeline and know-how). Also confirm he's comfortable with you working for others in his space. The plan is in `SELLING_THE_SERVICE.md`.
