# Handoff schemas

The three files that cross a stage boundary. Load this when writing or reading
one. `scripts/contract_check.py` enforces everything here.

**The governing rule: a stage file is a superset of what the upstream skill
emits, never a reduction.** Every field this pipeline has ever dropped was
dropped because it looked unused at the boundary where it was dropped, and became
load-bearing two steps later. Dropping is silent — nothing errors, a later step
just becomes impossible.

- [beats.json](#beatsjson) — after Steps 1–2
- [shortlist.json](#shortlistjson) — after Step 4
- [picks.json](#picksjson) — after Step 6
- [clips/manifest.json](#clipsmanifestjson) — Step 7
- [What used to go wrong here](#what-used-to-go-wrong-here)

## beats.json

The beat extractor's record **passed through untouched**, plus `queries`.

```json
[{
  "beat_id": "07-24-b03",
  "episode": "07-24",
  "segment_title": "UNAUTHORIZED SUBSCRIPTIONS",
  "script_text": "SHE CANCELED HER AUDIBLE ACCOUNT / BUT THE CHARGES KEPT COMING…",
  "orientation": "vertical",
  "clip_role": "victim_interview",
  "news_anchor": "Audible cancelled subscription still charged",
  "visual_spec": "woman to camera describing cancelled Audible still billing her husband's card",
  "platforms": ["tiktok", "shorts"],
  "offsite_likely": false,
  "priority": 1,
  "expected_segments": 2,
  "sourcability": "high",
  "sourcability_note": "creator's own TikTok, two usable slices",
  "source_native": "tiktok",
  "queries": {
    "news":     ["audible cancelled still charged"],
    "victim":   ["I cancelled it last October"],
    "platform": ["audible wont cancel", "#audible scam"],
    "anchor":   ["Audible cancellation charge Amazon"],
    "shorts":   ["#scamalert charged after cancelling", "she cancelled and got billed"]
  }
}]
```

### Why each carried field matters downstream

| Field | Consumed by |
|---|---|
| `priority` | Checkpoint 1 triage, and which beats earn the expensive Whisper rung. A priority-1 gap stops the run; a priority-3 gap is a note. |
| `expected_segments` | Step 6. Counted from `BUTT` markers. Without it a butt-cut beat ships one segment and the omission is invisible. |
| `sourcability` + `source_native` | Checkpoint 1 routing. These decide whether a beat enters the search path at all. |
| `news_anchor` | A prebuilt anchor query. Feed it to the `anchor` register instead of regenerating it. |
| `episode`, `segment_title` | Step 9 yield-log rows, and the Step 8 report grouping. |
| `offsite_likely` | Step 3 Brave routing. |

### The five register keys

`news`, `victim`, `platform`, `anchor`, **`shorts`**.

The query generator describes "four registers" and then splits the platform
register into two dialects, instructing that Shorts strings be emitted as explicit
search strings. **Step 3's ShortsBackend consumes `shorts` by name.** A beats.json
carrying four keys silently halves the Shorts leg — and Shorts is the only vertical
surface with a reachable search index, so on a vertical-heavy episode that is the
whole run. `contract_check.py` errors on a missing `shorts` key.

`victim` on a horizontal beat is a known-cost query: the generator's recall@30 eval
(n=8, horizontal/YouTube) found it contributed **zero** — no hits at any rank.
Generate it if you want coverage insurance, but spend it knowingly. The checker
warns rather than errors.

## shortlist.json

Pass-one survivors, five per beat, as the clip grader's pass-one output: score,
`source_type`, one-line reason, and the explicit `cannot_determine` note. Carry
`beat_id`, `orientation`, `priority` and `expected_segments` through from the beat
so Step 5 can prioritise and Step 6 knows how many segments to look for.

## picks.json

**The clip grader's pass-two output object, passed through, plus `platform` and
`title` added by this pipeline.** Not a reduction of it.

```json
[{
  "beat_id": "07-24-b03",
  "pass": 2,
  "flagged": "https://www.tiktok.com/@lostalicat/video/7214501715771411754",
  "platform": "tiktok",
  "title": "I cancelled Audible in October and they're still charging us",
  "source_mix": {"first_person": 3, "creator_short": 2},
  "diversity_floor_applied": false,
  "ranked": [{
    "url": "https://www.tiktok.com/@lostalicat/video/7214501715771411754",
    "source_type": "first_person", "score": 84,
    "tone": 9, "authenticity": 9, "quality": 7, "fit": 8,
    "segments": [
      {"in": "0:19", "out": "0:57", "outcue": "allow them to do it"},
      {"in": "1:17", "out": "2:25", "outcue": "I get this email"}
    ],
    "reasoning": "Creator on camera, names the platform and the card, two clean slices.",
    "flags": []
  }],
  "rejected": [{"url": "…", "source_type": "creator_short", "score": 41,
                "reason": "no account detail on screen"}],
  "cannot_determine": ["whether the second slice repeats the first soundbite"],
  "transcript_rung": 2
}]
```

`flagged` is `null` when nothing was good enough. That is a real outcome — a bad
pick costs more than an honest gap, because it gets discovered in the edit bay.

### Step 8 cannot be written without these

Step 8 requires the report to call out weak picks, source-type monoculture,
runner-ups of a different type, and diversity-floor promotions that lost pass two.
Every one of those needs a field that lives in `ranked`, `source_mix`, or
`diversity_floor_applied`. A reduced `picks.json` of
`{beat_id, url, title, platform, segments}` makes **six of the seven required
callouts unbuildable**, and the failure surfaces only when someone tries to write
the report. `contract_check.py picks` checks derivability directly.

Every proposed segment needs a verbatim `outcue` present in the transcript near
the out point. Verify before writing. An empty or invented outcue is a contract
violation, not a rounding error — if you cannot verify it, flag the beat
unverified at rung 3 instead.

## clips/manifest.json

Hand-written in Step 7 from `picks.json` — one entry per beat with URL, platform,
`source_type`, and segments. There is no automated cut stage; see Step 7.

## What used to go wrong here

Kept because a future run will be tempted to re-reduce these files.

- **beats.json reduced to seven fields.** `priority`, `expected_segments`,
  `sourcability`, `source_native` and `news_anchor` were dropped at Step 2. Result:
  no priority weighting anywhere, butt-cuts inexpressible, and — worst — beats with
  a known native post went through full search, triage, captions and grading to
  arrive at an unverified gap that was predictable before search ran.
- **picks.json reduced to five fields.** Step 8's report became unbuildable from
  the file Step 6 produced.
- **Four register keys instead of five.** Shorts queries never reached the Shorts
  backend. This was once fixed at the backend level while the instruction
  continued to cause it.
