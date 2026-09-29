---
name: "rossen-clip-grader"
description: Score and rank harvested clip candidates against a Rossen Reports beat, then flag the one to air. Runs in two passes: a cheap metadata triage that narrows thirty candidates to a priority-sized shortlist, then a transcript-informed grade that picks the winner and proposes in and out points. Use this whenever candidates have been harvested for a beat and need ranking, whenever the user asks which clip to use, wants a shortlist, asks "is this clip any good," or is deciding what goes in the outline's Videos table. Also use when auditing why a clip was or was not picked.
---

# Rossen Reports clip grader

Candidates in, a ranked shortlist and one flagged pick out. You are making the call
that a producer used to make, so the standard is not "is this relevant" but "will
this play on air."

pre-bible → pre-bible email → **outline w/ videos** → bible → bible review

**This is the last search stage.** Your pass-two object becomes the outline's Videos
row for the beat — and from there, the bible's numbered clip marker, URL, in–out and
`OUT:` line. The bible writer copies it; nothing downstream re-grades it. Validate before handing off:

```bash
python3 scripts/check_grades.py one shortlist.json
python3 scripts/check_grades.py two picks.json
```

## Beats that should not reach you

Check these first and return immediately rather than grading.

| Beat record says | Do this |
|---|---|
| `source_native` is `tiktok`/`instagram`/`x` | **Manual lane.** A native post is already identified and that post *is* the pick. Hand over the permalink. Do not rank YouTube reposts against it — aggregator copies re-narrate over the subject's audio or are bot-walled from download, so neither is clean or clearable. |
| `sourcability: none` | Not a grading task. It is a swap, show-produced or drop decision, made at Checkpoint 1. |
| `sourcability: throttled` | The extractor's scan hit a rate limiter, so this is a network condition, not an absence of footage. Send it back for a re-scan; do not grade whatever came back. |

## Two passes

**Pass one, metadata triage.** Thirty candidates, no video downloaded. You have
title, channel, duration, view count, upload date, thumbnail URL. Score every
candidate, keep the top few. This pass is about elimination, not selection: you are
throwing out the obviously wrong, not identifying the winner.

**Pass two, transcript grade.** The survivors get downloaded and transcribed. Now
you have what is actually said and when. Re-rank, flag one, propose in and out
points with an outcue. This is where tone, quality and fit get decided, because none
of them are visible in metadata.

Never flag from pass one alone. Metadata will tell you a clip is plausible. It will
not tell you the victim is inaudible, the reporter buries the moment at 4:30, or the
whole package is a studio two-shot with no actual person in it.

### How many survivors — size it against `priority`

Pass two downloads and transcribes every candidate you pass it. It is the most
expensive step in the pipeline, and the beat record already tells you how much the
beat is worth.

| Beat `priority` | Shortlist |
|---|---|
| 1 — the segment's argument breaks without this clip | **5** |
| 2 — illustrates a point the copy already makes | **3** |
| 3 — texture; the segment reads fine if it never rolls | **2** |

Shipping fewer is legitimate when the diversity floor found nothing to promote — say
so in `shortlist_note`. Shipping more is not: it spends the transcript budget of a
priority-1 beat on a beat the show could drop.

## Pass one: metadata triage

### Hard filters — fail one and the candidate is out

No scoring, no exceptions.

- **Duration floor.** Source under 25 seconds cannot yield a usable segment for any
  role except `evidence`, where 10 seconds is fine.
- **Compilation and aggregator channels.** Titles like "Top 10 Scams", "Scam
  Compilation", "SCAMMERS GET DESTROYED #47". Re-uploads of other people's footage —
  a clearance problem and usually a quality problem.
- **AI slop.** Synthetic voiceover over stock footage, channel names that are
  generic keyword strings, upload cadence of many per day. Increasingly common on
  scam topics.
- **Obvious reposts.** Same title as an earlier upload from a credible source. Keep
  the original. Earliest upload date wins.

### Scoring modifiers — these adjust the score, they do not eliminate

Kept separate from the filters above on purpose. An earlier version listed these
alongside the hard filters under the heading "fail any of these and the candidate is
out," which was false for all three and made the real filters look negotiable.

- **Orientation mismatch — demote to the floor, with one documented exception.** A
  horizontal beat cannot take a vertical source; the producer typed it in the
  script. **Exception:** a Short carrying `surfaced_for: horizontal` from the query
  generator was crossed deliberately, because Shorts routinely hold the raw victim
  moment that a four-minute affiliate package buries at 1:30. Do not auto-fail it.
  Score it, and put the framing question in that candidate's `cannot_determine` so a
  human rules on pillarbox versus punch-in.
- **Duration ceiling by role.** 10 minutes is where the moment starts being buried
  and the score should reflect it. Past 20 minutes, demote to the floor unless the
  role is `explainer_demo/creator_long` — a 45-minute podcast is not a
  `victim_interview` candidate however well the title matches.
- **Shorts are exempt from duration scoring entirely.** Not a filter at all; see
  below.

### Scoring signals

**Source type.** Tag every candidate with exactly one, from the title, channel name
and channel history. This tag drives credibility scoring and gets carried through to
the output.

| Tag | What it looks like |
|---|---|
| `affiliate` | Local call letters — KXAS, WFAA, ABC7, News 4 |
| `network` | Network and wire — ABC News, NBC News, AP, Reuters |
| `creator_long` | Established fraud, consumer or finance channel, long-form, real back catalog |
| `creator_short` | Same kind of channel, Shorts or vertical output |
| `first_person` | Individual account, the person it happened to, no production apparatus |
| `raw_footage` | Doorbell, dashcam, security, screen recording, bystander phone video |

**Channel credibility is scored relative to the role, not on an absolute ladder.**
There is no tier that is best everywhere. Each role has a natural source type and
that type gets the top of the range; the others are scored against how well they
substitute, not against affiliates.

| Role | Natural source types | Weak for this role |
|---|---|---|
| `victim_interview` | affiliate, first_person | network studio-only |
| `confrontation_bust` | first_person, raw_footage, creator_short | network |
| `evidence` | raw_footage, first_person | affiliate, network |
| `explainer_demo/creator_long` | **creator_long** | affiliate, network |
| `explainer_demo/creator_short` | **creator_short**, first_person | affiliate, network |
| `first_person_rant` | **first_person**, creator_short | affiliate, network |
| `authority_report` | network, affiliate | first_person, raw_footage |
| `debunk` | affiliate, network, creator_long | raw_footage |

The three bolded cells are the correction. A well-produced creator video is not a
degraded affiliate package for those roles — it is the right source, and it should
score at the top of the range there. A channel like Holy Schmidt doing a careful
walkthrough of how a Social Security imposter call actually runs is exactly what
`explainer_demo` asks for, and no affiliate produces that. Stop reading "commentary"
as a demerit for roles whose whole point is a person explaining something on camera.

What still demotes a creator, in any role: no back catalog, generic keyword channel
name, engagement-farming title, reaction content with no original reporting, or a
channel whose upload cadence says content mill. Judge the work, not the fact that it
came from an individual.

Unknown channel, generic name, no history — heavy demote, unchanged, for every role.

**Title syntax fit.** Does the title read like the register that should have found
it? An affiliate headline for a victim interview. A first-person caption for a rant.
A title that is a keyword salad is a bad sign regardless of relevance.

**Duration fit against what actually airs.** Measured from three episodes, 24 aired
segments:

| Statistic | Value |
|---|---|
| Aired segment length, median | 67s |
| Interquartile range | 50s to 95s |
| Full observed range | 10s to 161s |
| Total airtime per beat, median | 88s |

So the show wants roughly a minute of usable material. A source needs to comfortably
contain that plus setup. For horizontal news packages, 2 to 6 minutes is the sweet
spot. Under 90 seconds is usually a headline read with no interview in it.

**Shorts do not get scored on duration.** The "under 90 seconds is a headline read"
rule is a fact about affiliate uploads and it does not transfer. A 45-second Short
is not a truncated package; it is a complete piece of content whose whole runtime is
the moment. Judge it on channel, title register and role fit alone, and never demote
a Short for being 30 to 60 seconds long — that is the format performing as designed.

The median aired segment is 67 seconds against a 60-second ceiling, so a strong
Short will usually be played closer to whole than trimmed. Treat near-total usable
runtime as a point in its favor, not as a sign there is no runway.

**Upload recency.** For `authority_report` and `debunk`, recency is close to
decisive; the beat exists because something happened this week. For
`victim_interview` and `evidence`, age is nearly irrelevant. A 2023 affiliate
package about an FBI imposter scam plays fine today.

**View count.** Weak signal, use as a tiebreak only. High views on TikTok correlate
with watchability. High views on YouTube often just mean an old upload. Never let
views override channel credibility.

### Diversity floor

Apply after scoring, before writing the shortlist.

**If every survivor is `affiliate`, drop the lowest and promote the highest-scoring
non-affiliate candidate that cleared the hard filters.** Any of `creator_long`,
`creator_short`, `first_person`, `raw_footage` qualifies. Same rule if the shortlist
is `affiliate` and `network` combined — wire and local are one monoculture, not two.

The affiliate lean is Jeff's preference and it is a good one; affiliates title
predictably, shoot clean audio and clear easily. But a shortlist of the same shape
means pass two gets to choose only between near-identical framings, and the raw
moment that actually plays — someone crying in a driveway, a screen recording of the
text thread — never reaches the transcript pass to compete.

Two limits on the floor. It promotes, it never invents: if no non-affiliate candidate
cleared the hard filters, ship one short and say why in `shortlist_note` rather than
reaching back past a filter for filler. And it is a floor, not a quota — if the
promoted candidate scores 30 or more points below the affiliate it displaced, say so
in its one-line reason so pass two does not treat the shortlist as peers.

### Pass one output

```json
{
  "beat_id": "05-06-b03",
  "orientation": "horizontal",
  "clip_role": "victim_interview",
  "priority": 1,
  "expected_segments": 1,
  "source_mix": {"affiliate": 4, "first_person": 1},
  "shortlist_note": "",
  "candidates": [
    {
      "url": "https://www.youtube.com/watch?v=I3667lq1L2o",
      "source_type": "affiliate",
      "score": 82,
      "reason": "ABC affiliate, headline register matches a victim interview, 3:40 runtime",
      "cannot_determine": ["whether the officer is audible", "whether he appears on camera or is only quoted"],
      "promoted_by_floor": false
    }
  ]
}
```

`beat_id`, `orientation`, `clip_role`, `priority` and `expected_segments` are
carried through from the beat record — pass two and the pipeline both need them, and
this is their only route forward.

`cannot_determine` is **per candidate** in pass one: it tells pass two what to look
for on that specific clip. In pass two it becomes a single beat-level list. The
shape changes deliberately between passes.

## Pass two: transcript grade

Now you have a word-level transcript with timestamps. Grade on four dimensions,
0–10 each.

### Tone

Does this sound like Rossen Reports? The show is consumer-protective, urgent,
plain-spoken, and sympathetic to the victim. It is never sneering at the person who
got scammed, never true-crime lurid, never jokey about someone's loss.

- **Good tone.** A person describing what happened in their own words, plainly, with
  feeling. A reporter who sounds like they care. A creator who is helpful rather
  than performing outrage.
- **Bad tone.** Scambaiting content that mocks the caller. Content that treats the
  victim as stupid. Wry irony. Anything with a laugh track energy.
- **Language.** Profanity is a flag, not a disqualifier. One aired clip carried an
  on-air warning about it. Note it in `flags` so the producer can decide, and prefer
  a clean alternative if one scores within a few points.

### Vibe and authenticity

Rossen plays raw over polished. A shaky vertical video of a family standing in a
burned garage beat any professionally produced safety segment about lithium
batteries.

- Prefer first-hand over second-hand. Someone who was there beats someone reporting
  on someone who was there.
- Prefer specific over general. "Forty thousand dollars" beats "a large sum."
- Prefer emotional register that is real over performed. Someone crying because they
  lost their savings, not someone doing a concerned-face intro.
- Studio-only packages with no field interview are weak for every role except
  `authority_report`.

### Quality

- **Audio is the gate.** Bad audio kills a clip in a way bad video does not.
  Inaudible victim, heavy wind, blown-out phone mic, loud background music under
  speech — all disqualifying even if the content is perfect. Score 3 or below and
  the veto below fires.
- **Faces.** Required for `victim_interview`, `first_person_rant`,
  `confrontation_bust`. Not required for `evidence` or `explainer_demo`. A
  silhouetted or back-to-camera victim is usable but demote it, because Jeff's
  setups routinely point at the person.
- **Watermarks and burned-in logos.** Another outlet's bug in the corner is a
  clearance and optics problem. Demote. A TikTok username watermark is normal and
  fine.
- **Resolution.** 720p is the floor for full-screen play.

### Fit to the beat

This is where most rejections should happen and it is the thing metadata cannot see.

Read the beat's `script_text` and ask whether this clip delivers the specific claim
Jeff just set up. If the setup says *this couple lost $850,000*, a clip about a
different couple losing $30,000 does not fit, however good it is. If the setup says
*watch what happens when he confronts the seller*, a clip where no confrontation
occurs is a miss even if the scam matches. Score 3 or below and the veto fires.

Check the `visual_spec` too. It describes what the producer expected to see.

## The score

**Weighted, not averaged, and three dimensions are gates.**

```
score = (fit×0.35 + quality×0.25 + authenticity×0.20 + tone×0.20) × 10

VETO: if tone, quality or fit is 3 or below, the score caps at 40
      regardless of the other three.
```

The weights follow the rules above: fit is where most rejections should happen,
audio is the gate, and authenticity is a strong preference rather than a gate — it
is the one dimension without a veto.

**Why the veto exists.** Under a plain average, a clip with an inaudible victim
(tone 10, authenticity 10, quality 2, fit 10) scores **80** — nearly double the
worked example's rejected candidate, and comfortably inside anything a reader would
call a strong pick. The prose calls that clip disqualifying. Without a veto the
rubric contradicts its own most forceful rules: a mismatched fit lands at 72, and
scambaiting that mocks the victim lands at 70. All three cap at 40 now.

### Decision thresholds

| Score | Meaning |
|---|---|
| **70+** | Flag it. |
| **55–69** | Flag it, but it is a weak pick — it must appear in the pipeline's human-re-check callout. |
| **below 55** | Do not flag. Return `flagged: null` with a `null_reason` and the query that would find something better. |

A bad flagged clip costs a producer more than an honest empty result, because they
will discover the problem in the edit bay instead of at the contact sheet.

### Runway

Jeff talks into the clip, so the clip must land quickly once it starts. Find the
moment, then look for a clean entry 2 to 5 seconds before it. If the usable moment
cannot be entered cleanly without 30 seconds of anchor setup, the clip is weaker
than its content suggests.

**Where the moment actually lives.** Measured from the same 24 aired segments:

| Orientation | Median first in-point | Range |
|---|---|---|
| horizontal (news packages) | 34s | 0s to 152s |
| vertical (TikTok, Facebook) | 0s | 0s to 14s |

Shorts behave like the vertical row and more so: the hook is at 0:00 because the
format punishes anything else, so expect an in-point at or near the top and do not
go hunting for a buried moment that is not there.

News packages open with an anchor toss and a reporter standup that always gets cut.
The usable material starts about half a minute in. Vertical social clips start at
the top, because the creator already front-loaded the hook. Use this as a prior when
scanning the transcript: on a horizontal candidate, do not conclude the clip is weak
because the first 30 seconds are generic.

## Pass two output

```json
{
  "beat_id": "05-06-b03",
  "pass": 2,
  "expected_segments": 1,
  "flagged": "https://www.youtube.com/watch?v=I3667lq1L2o",
  "source_mix": {"affiliate": 3, "first_person": 1, "creator_short": 1},
  "diversity_floor_applied": true,
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
      "flags": []
    }
  ],
  "rejected": [
    {"url": "...", "source_type": "network", "score": 41, "reason": "studio two-shot, no victim on camera"}
  ],
  "cannot_determine": ["whether the second half of the package repeats the same soundbite"]
}
```

That example is verified against the aired ground truth for beat 05-06-b03 —
URL, in and out points, and outcue all match what actually rolled. Note the
case-sensitive video ID: `I3667lq1L2o`. Some copies of `aired_examples.md` carry it
whole-string uppercased, which corrupts it; this record is correct.

Its score checks out under the formula: fit 9(.35) + quality 8(.25) + authenticity
9(.20) + tone 9(.20) = 8.75 → **88**.

`outcue` is required on every proposed segment and must be verbatim from the
transcript. It is the verification anchor: a correct out point is one where that
phrase appears in the transcript within about a second of the proposed timestamp.
Never invent it, never paraphrase it.

**Check `expected_segments` before you finish.** It comes from the outline row (or, in
script-mode back-fill, from counting `BUTT` markers), so it is the producer's own count of how many slices this beat
wants. Propose fewer and you ship the beat at a fraction of its intended length,
invisibly. Four of 24 aired beats were butt-cuts pulling 2 to 3 slices from one
source, so this is normal, not an edge case. If the beat expects 2 and you can only
find 1, say why in `cannot_determine` rather than silently shipping one.

**Do not do timecode arithmetic in your head.** Report the timestamps the transcript
gives you; the pipeline snaps them to scene boundaries at Step 6.5.

## Episode-level source mix

Per-beat tags are for the grader. The number the producer acts on is the mix across
the whole episode, so report it once at the end of pass two, before the per-beat
table:

```
Source mix, 10 beats:  affiliate 8 · first_person 1 · creator_long 1
```

Call it out in words when one type takes 70% or more of the picks — "8 of 10 picks
are affiliate" — and name the beats where the runner-up was a different source type,
so a producer who wants variety knows exactly which swaps are cheap. Do not
editorialize past that. A monoculture may be the right answer for a given episode;
the job here is to make it visible rather than to break it up on your own initiative.

Report the same line for beats where the diversity floor fired and the promoted
candidate did not survive pass two. That pattern repeating across episodes means the
floor is promoting filler and the hard filters upstream need a look, not that variety
is unavailable.

## When nothing is good enough

Say so. Return `flagged: null` with a `null_reason`, and say what query would find
something better. The threshold is 55 — see Decision thresholds above. Do not flag
the least-bad option to avoid an empty cell.

`reference/aired_examples.md` in the beat extractor skill holds 24 beats with the
clip that actually aired and its in and out points. Read it to calibrate.
