---
name: rossen-clip-grader
description: Score and rank harvested clip candidates against a Rossen Reports beat, then flag the one to air. Runs in two passes: a cheap metadata triage that narrows thirty candidates to five, then a transcript-informed grade that picks the winner and proposes in and out points. Use this whenever candidates have been harvested for a beat and need ranking, whenever the user asks which clip to use, wants a shortlist, asks "is this clip any good," or is deciding what to send to the timecode extractor. Also use when auditing why a clip was or was not picked.
---

# Rossen Reports clip grader

Candidates in, a ranked shortlist and one flagged pick out. You are making the call that a producer used to make, so the standard is not "is this relevant" but "will this play on air."

## Two passes

**Pass one, metadata triage.** Thirty candidates, no video downloaded. You have title, channel, duration, view count, upload date, thumbnail URL. Score every candidate, keep the top five. This pass is about elimination, not selection: you are throwing out the obviously wrong, not identifying the winner.

**Pass two, transcript grade.** The five survivors get downloaded and transcribed. Now you have what is actually said and when. Re-rank, flag one, propose in and out points with an outcue. This is where tone, quality and fit get decided, because none of them are visible in metadata.

Never flag from pass one alone. Metadata will tell you a clip is plausible. It will not tell you the victim is inaudible, the reporter buries the moment at 4:30, or the whole package is a studio two-shot with no actual person in it.

## Pass one: metadata triage

### Hard filters, applied before scoring

Fail any of these and the candidate is out regardless of other merit.

- **Orientation mismatch.** A horizontal beat cannot take a vertical source. Non-negotiable, the producer typed it in the script.
- **Duration floor.** Source under 25 seconds cannot yield a usable segment for any role except `evidence`, where 10 seconds is fine.
- **Duration ceiling by role.** A 45 minute podcast episode is not a `victim_interview` candidate even if the title matches. Over 20 minutes, demote hard unless role is `explainer_demo/creator_long`.
- **Compilation and aggregator channels.** Titles like "Top 10 Scams", "Scam Compilation", "SCAMMERS GET DESTROYED #47". These are re-uploads of other people's footage, which is a clearance problem and usually a quality problem. Out.
- **AI slop.** Synthetic voiceover over stock footage, channel names that are generic keyword strings, upload cadence of many per day. Increasingly common on scam topics. Out.
- **Obvious reposts.** Same title as an earlier upload from a credible source. Keep the original, drop the repost. Earliest upload date wins.

### Scoring signals

**Channel credibility.** The single strongest metadata signal.
- Local affiliate call letters, KXAS, WFAA, ABC7, News 4 — highest tier for `victim_interview`, `confrontation_bust`, `debunk`
- Network and wire — highest tier for `authority_report`
- Established fraud-focused creators — highest for `explainer_demo/creator_long`
- Individual person accounts — right for `first_person_rant`, `evidence`, `creator_short`
- Unknown channel, generic name, no history — heavy demote

**Title syntax fit.** Does the title read like the register that should have found it? An affiliate headline for a victim interview. A first-person caption for a rant. A title that is a keyword salad is a bad sign regardless of relevance.

**Duration fit against what actually airs.** Measured from three episodes, 24 aired segments:

| Statistic | Value |
|---|---|
| Aired segment length, median | 67s |
| Interquartile range | 50s to 95s |
| Full observed range | 10s to 161s |
| Total airtime per beat, median | 88s |

So the show wants roughly a minute of usable material. A source needs to comfortably contain that plus setup. For horizontal news packages, 2 to 6 minutes is the sweet spot. Under 90 seconds is usually a headline read with no interview in it. Over 10 minutes and the moment is buried.

**Upload recency.** For `authority_report` and `debunk`, recency is close to decisive; the beat exists because something happened this week. For `victim_interview` and `evidence`, age is nearly irrelevant. A 2023 affiliate package about an FBI imposter scam plays fine today.

**View count.** Weak signal, use as a tiebreak only. High views on TikTok correlate with watchability. High views on YouTube often just mean an old upload. Never let views override channel credibility.

### Source-type tagging

Tag every candidate with one of: `affiliate`, `network`, `creator_long`, `creator_short`, `first_person`, `raw_footage`, `shorts`. This tag persists through pass two into the final picks so the producer can see the source mix at a glance. Assign based on channel and duration:

- `affiliate` — local station call letters (KXAS, ABC7, WFAA, CBS Texas, etc.)
- `network` — national outlet (ABC News, CBS News, NBC, CNN, Forbes, CNBC)
- `creator_long` — established individual channel, duration over 60s
- `creator_short` — individual channel, duration under 60s or YouTube Short
- `first_person` — the person in the video is the subject, not a commentator
- `raw_footage` — bodycam, doorbell cam, security cam, screen recording, no narration
- `shorts` — YouTube Short (duration under 60s, vertical, `#shorts` in title or metadata)

### Diversity floor

After scoring, if all 5 survivors are the same source type, replace the weakest survivor with the strongest candidate from a different source type. The goal is not to override the producer's preference for affiliates — it is to make sure they see at least one alternative and can make a conscious choice rather than a default one.

Tag any forced-in candidate with `diversity_floor: true` so the producer knows why it is in the shortlist.

When the beat role naturally fits a non-affiliate source type, this floor is unnecessary. `first_person_rant` should be first-person content. `evidence` should be raw footage. `explainer_demo/creator_short` should be a creator. Only force diversity when the natural role is being served by a monoculture.

### Pass one output

Five candidates, each with a score 0 to 100, a source type tag, a one-line reason, and an explicit note of what you cannot tell from metadata. That last field matters; it tells pass two what to look for.

## Pass two: transcript grade

Now you have a word-level transcript with timestamps. Grade on four dimensions.

### Tone

Does this sound like Rossen Reports? The show is consumer-protective, urgent, plain-spoken, and sympathetic to the victim. It is never sneering at the person who got scammed, never true-crime lurid, never jokey about someone's loss.

- **Good tone.** A person describing what happened in their own words, plainly, with feeling. A reporter who sounds like they care. A creator who is helpful rather than performing outrage.
- **Bad tone.** Scambaiting content that mocks the caller. Content that treats the victim as stupid. Wry irony. Anything with a laugh track energy.
- **Language.** Profanity is a flag, not a disqualifier. One aired clip carried an on-air warning about it. Note it in the output so the producer can decide, and prefer a clean alternative if one scores within a few points.

### Vibe and authenticity

Rossen plays raw over polished. A shaky vertical video of a family standing in a burned garage beat any professionally produced safety segment about lithium batteries.

- Prefer first-hand over second-hand. Someone who was there beats someone reporting on someone who was there.
- Prefer specific over general. "Forty thousand dollars" beats "a large sum."
- Prefer emotional register that is real over performed. Someone crying because they lost their savings, not someone doing a concerned-face intro.
- Studio-only packages with no field interview are weak for every role except `authority_report`.

### Quality

- **Audio is the gate.** Bad audio kills a clip in a way bad video does not. Inaudible victim, heavy wind, blown-out phone mic, loud background music under speech — all disqualifying even if the content is perfect.
- **Faces.** Required for `victim_interview`, `first_person_rant`, `confrontation_bust`. Not required for `evidence` or `explainer_demo`. A silhouetted or back-to-camera victim is usable but demote it, because Jeff's setups routinely point at the person.
- **Watermarks and burned-in logos.** Another outlet's bug in the corner is a clearance and optics problem. Demote. A TikTok username watermark is normal and fine.
- **Resolution.** 720p is the floor for full-screen play.

### Fit to the beat

This is where most rejections should happen and it is the thing metadata cannot see.

Read the beat's `script_text` and ask whether this clip delivers the specific claim Jeff just set up. If the setup says *this couple lost $850,000*, a clip about a different couple losing $30,000 does not fit, however good it is. If the setup says *watch what happens when he confronts the seller*, a clip where no confrontation occurs is a miss even if the scam matches.

Check the `visual_spec` too. It describes what the producer expected to see.

### Runway

Jeff talks into the clip, so the clip must land quickly once it starts. Find the moment, then look for a clean entry 2 to 5 seconds before it. If the usable moment cannot be entered cleanly without 30 seconds of anchor setup, the clip is weaker than its content suggests.

**Where the moment actually lives.** Measured from the same 24 aired segments:

| Orientation | Median first in-point | Range |
|---|---|---|
| horizontal (news packages) | 34s | 0s to 152s |
| vertical (TikTok, Facebook) | 0s | 0s to 14s |

News packages open with an anchor toss and a reporter standup that always gets cut. The usable material starts about half a minute in. Vertical social clips start at the top, because the creator already front-loaded the hook. Use this as a prior when scanning the transcript: on a horizontal candidate, do not conclude the clip is weak because the first 30 seconds are generic.

## Output

```json
{
  "beat_id": "05-06-b03",
  "pass": 2,
  "flagged": "https://www.youtube.com/watch?v=I3667lq1L2o",
  "ranked": [
    {
      "url": "https://www.youtube.com/watch?v=I3667lq1L2o",
      "source_type": "affiliate",
      "score": 88,
      "tone": 9,
      "authenticity": 9,
      "quality": 8,
      "fit": 9,
      "segments": [
        {"in": "0:21", "out": "1:20", "outcue": "when I sent the money out"}
      ],
      "reasoning": "Retired officer on camera at home, names the dollar figure, audible, affiliate package. Matches the setup line exactly.",
      "diversity_floor": false,
      "flags": []
    }
  ],
  "rejected": [
    {"url": "...", "source_type": "creator_long", "score": 41, "reason": "studio two-shot, no victim on camera"}
  ],
  "cannot_determine": ["whether the second half of the package repeats the same soundbite"]
}
```

`outcue` is required on every proposed segment and must be verbatim from the transcript. It is the verification anchor: a correct out point is one where that phrase appears in the transcript within about a second of the proposed timestamp. Never invent it, never paraphrase it.

Propose multiple segments when the best material is split. Four of 24 aired beats were butt-cuts pulling 2 to 3 slices from one source, so this is normal, not an edge case.

**Do not do timecode arithmetic in your head.** Report the timestamps the transcript gives you and let the pipeline snap them to scene boundaries.

## When nothing is good enough

Say so. Return `flagged: null` with a reason, and say what query would find something better. A bad flagged clip costs a producer more than an honest empty result, because they will discover the problem in the edit bay instead of at the contact sheet.

`reference/aired_examples.md` in the beat extractor skill holds 24 beats with the clip that actually aired and its in and out points. Read it to calibrate.
