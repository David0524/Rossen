# F1 07/31/2026 — THE AIRBNB & VRBO RENTAL SCAM

**Run:** `runs/F1_07312026` · branch `claude/gift-card-vertical-beat-test-glmu54`
**Status:** complete through Step 8, holding at Checkpoint 2 for one decision on b04.
**Degraded by a missing search key:** no. `BRAVE_API_KEY` was present; no `DEGRADED` line.

```
Source mix, 4 beats:  affiliate 3 · network 1
```

3 of 4 picks are affiliate (75%). See "cheap swaps" below.

**Yield: 3 PICK / 1 LOCATED / 0 EMPTY.**

## Beat table

| Beat | Role | Or. | Pick | Platform | Source type | Segment | Outcue |
|---|---|---|---|---|---|---|---|
| F1-b01 | victim_interview | H | Scripps DWYM (Matarese) — Gentry | news_web + YT twin | affiliate | 0:18–0:55 (39.5s cut) | "straight to voicemail" ✅ verified |
| F1-b02 | authority_report | H | **Same package** — Brasler | news_web + YT twin | affiliate | 0:59–1:19 (22.5s cut) | "not really part of this transaction" ✅ verified |
| F1-b03 | victim_interview | H | Inside Edition — Conti | youtube | network | 0:30–1:38 + 1:51–2:49 (2 cuts) | "up in the scam" / "coming up on surfing websites" ✅ verified |
| F1-b04 | victim_interview | H | CBS LA — Branch | youtube | affiliate | — MANUAL | not verifiable in this environment |

Four clips cut and on disk (`clips/`). One handed over as MANUAL CLIP with a
confirmed-correct source and **no invented timecode**.

## The three producer questions in the script — all answered

**1. The BUTT at line 129 — CONFIRMED, and verified at transcript level.**
The note asked whether Gentry and Brasler were one package. They are. One
Scripps "Don't Waste Your Money" piece by John Matarese carries Gentry at 0:18
and Brasler at 1:05, and Brasler delivers exactly the line the script sets up:

> "If you dig into their terms and conditions, they say basically we're not
> really part of this transaction."

against the script's *"THEY AREN'T ACTUALLY A PARTY TO YOUR TRANSACTION… THEY'RE
JUST A FORUM."* Same claim, same source. **One source, two segments, butted** —
so the BUTT stays and these are not two separate beats.

**2. Line 174, "WE HAVE NOT CONFIRMED VIDEO EXISTS" for Conti — it exists.**
Inside Edition, *"The Genius Way This Reporter Uncovered Airbnb Scammers"*, 8:15,
live and public (oEmbed 200). The fallback to a Jeff read over screenshots is
**not needed**.

**3. Line 108, "CONFIRM WHICH PLATFORM GENTRY BOOKED ON."** The package never
names the platform — it says "the rental site" and "one of the big rental sites"
throughout. The Scripps article headline covers "Airbnb, VRBO" generically.
**Leave the platform out of the setup lines**; the clip will not back a specific
one up.

## What I worked around

**YouTube is bot-walled in this environment.** Search worked (3,053 raw results),
but every *individual video page* returns "Sign in to confirm you're not a bot."
Consequences and what I did:

- **Step 5 returned 0/19 captions.** That is infrastructure, not "captions
  disabled," and treating 19 nulls as 19 demotes would have flagged nothing on
  all four beats for a reason that has nothing to do with the material.
- Tried every yt-dlp player client: `android_vr`, `web_safari`, `tv_embedded`,
  `ios` all bot-walled; `mweb` reached the page but subtitles need a PO token;
  `tv` returns DRM.
- **A 25-minute cooldown retry of the full shortlist also returned 0/19.** So the
  wall is persistent in this environment, not a transient rate-limit from the
  3,053-query search. Nothing further to try here; b03 and b04 are final as
  MANUAL CLIP.
- **The workaround that worked:** Scripps stations serve their video off Uplynk,
  and those streams are reachable. I pulled the manifest URL out of the WCPO
  article HTML, ffmpeg'd the audio, and transcribed locally with faster-whisper.
  That produced the verified transcript behind b01 and b02 and the media the
  clips were actually cut from.
- **b03 was later recovered.** Installing deno (the JS runtime yt-dlp asks for)
  changed the Facebook extraction: Inside Edition's own Facebook upload of the
  same package went from 0 formats to a downloadable `sd` render. It is
  494.24s against YouTube's 495s — the same cut — so the timecodes transfer to
  the YouTube link. Whispered locally, both outcues verified, both segments cut.
- **b04 is genuinely unreachable here.** CBS returns 406 to every header set and
  to yt-dlp's own CBSLocal extractor; there is no Facebook copy, and the Gray
  station that carried the story ran it as text only. Chromium is installed but
  cannot traverse the agent proxy (ERR_CONNECTION_RESET on every host,
  including example.com), so the browser route is closed too.

**Outcue discipline held.** A third candidate outcue for b02 — "we're just a
forum", which would have been the better on-air landing — was **rejected**
because Whisper truncated it to "We" and `Transcript.find()` could not verify it.
It is flagged in `picks.json` for an editor to confirm by ear rather than quoted
from memory.

**Whisper mis-renders "Zelle" as "sale"** throughout the b01/b02 transcript. A
transcription artifact, not an error in the clip — the audio says Zelle. Do not
quote the transcript file on air.

## Two CLI stages were missing and are now built

The pipeline skill documents both; neither existed (the CLI shipped with
`harvest`/`search`/`eval` only).

- **`captions`** (Step 5) — routes YouTube to the caption fetch and vertical
  platforms to Whisper, records nulls rather than dropping clips.
- **`clip`** (Step 7, new `clip.py`) — downloads each pick once, cuts padded
  segments, writes the manifest. Prefers an explicit `media_source` over the page
  URL, which is the only reason this run was cuttable. Keys the download on the
  media URL, not the beat id, so butt-cut beats fetch one file instead of two.

## Beats needing a human

- **b04 — no verified timecode.** The source is confirmed correct and alive. On a
  machine with normal YouTube access, `python3 -m rossen_harvest captions` then
  `clip` should finish it without changes.
- **b03 quality.** The only reachable copy was Facebook's at 640x360, below the
  720p floor. Re-pull from the YouTube original for air; the timecodes carry.
- **b02's 20-second segment** is short. Within the observed aired range
  (10s–161s) and it is the exact line Jeff sets up, but worth a look.

## Cheap swaps, if you want variety

3 of 4 picks are affiliate. The only genuine non-affiliate in the picks is b03
(network / Inside Edition). Runners-up that were a *different* source type:

- **b02** — BBB's "Victim of VRBO/HomeAway Rental Scam Tells Her Story"
  (`z1hKAyDG9ls`, first_person, 157s) was the diversity-floor promotion and the
  only first_person candidate that cleared the filters on any beat. It lost to
  the Scripps package on fit, not quality.
- **b04** — Pleasant Green's "A Scammer Has a Picture of My House?!"
  (`kU_Sw0F4qsI`, creator_long, 303s) was the floor promotion here.

**The diversity floor fired on all four beats and its promotion lost pass two
every time.** Per the grader skill, that pattern repeating is a signal the floor
is promoting filler rather than that variety is unavailable — worth watching
across the next runs rather than acting on from n=1.

## Beats with no clip

None. All four beats have a confirmed source; two are cut, two are manual.

## Clips that failed to download

None of the attempted ones. b03/b04 were never attempted because no reachable
media route exists here.
