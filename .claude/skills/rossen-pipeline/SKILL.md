---
name: rossen-pipeline
description: Run the full Rossen Reports clip pipeline on a show script — beat extraction, sourcability scan, query generation, search, grading, and pick output. Use this whenever a script is provided and the user wants the complete pipeline run end to end, or asks for clips to be sourced for a script. Orchestrates the beat-extractor, query-generator, and clip-grader skills in sequence with three user checkpoints and a feedback loop that catches unsourceable beats before wasting search effort.
---

# Rossen Reports clip pipeline

Script in, picks.json out. Three checkpoints where the producer reviews and redirects. A feedback loop between beats and sourcability prevents dead-end work.

## Prerequisites

Read these skills before starting. They contain the rules for each phase:

- `.claude/skills/rossen-beat-extractor/SKILL.md`
- `.claude/skills/rossen-query-generator/SKILL.md`
- `.claude/skills/rossen-clip-grader/SKILL.md`

Also read the calibration data:

- `.claude/skills/rossen-beat-extractor/reference/aired_examples.md`
- `.claude/skills/rossen-query-generator/reference/glossary.md`

## Phases

### Phase 1: Beat extraction

Follow the beat extractor skill. Convert the `.docx` to text, identify `PLAY CLIP` markers, assign roles and visual specs. Watch for the cold-open tease trap and mid-show teases.

### Phase 2: Sourcability scan

Run immediately after extraction, before showing anything to the user. For every beat that names a specific person, do a quick YouTube title search to check whether on-camera footage exists. See the "Sourcability scan" section in the beat extractor skill for the full protocol.

Tag every beat with `sourcability: high | commentary_only | none`. For beats with `none` or `commentary_only`, prepare swap suggestions: two or three alternative victims who cover the same scam type and DO have confirmed affiliate coverage on YouTube.

### Checkpoint 1: Beat table with sourcability

Show the user a table with columns: beat_id, role, orientation, one-line spec, **sourcability**, swap suggestions (if any).

If more than 16 beats: you are extracting teases. Re-read the traps section.

If any beat is `sourcability: none` or `commentary_only`: flag it prominently. The user decides whether to swap, mark as show-produced, or drop. **Do not proceed past this checkpoint with unsourceable beats still in the pipeline.** Either swap them, remove them, or get explicit user approval to proceed knowing they will likely come back empty.

Wait for user approval before continuing.

### Phase 3: Query generation

Follow the query generator skill. Generate four-register queries per beat. Apply per-role weighting and platform syntax differences.

**Shorts queries.** For every beat (not just vertical), generate 2-3 YouTube Shorts queries: short (3-5 words), hashtag-heavy, emotion-forward. YouTube Shorts often contain the raw victim moment that a 4-minute affiliate package buries at 1:30. Add `"shorts"` to the platform map for these queries. Use `--match-filter "duration<60"` when searching with yt-dlp.

### Phase 4: Search

Run queries via `yt-dlp` with `ytsearch30:` for YouTube, web search for news_web. For Shorts, use `ytsearch15:` with duration filter.

Collect metadata: title, channel, upload date, duration, view count, URL.

**Source-type tagging.** Tag every candidate as one of: `affiliate`, `network`, `creator_long`, `creator_short`, `first_person`, `raw_footage`, `shorts`. This tag flows through to grading and into the final picks so the producer can see the source mix.

### Checkpoint 2: Search results

Show per-platform candidate counts and source-type distribution per beat. Flag:

- Any beat with fewer than 10 candidates. Fix queries and re-run that beat alone.
- Any beat where all candidates are the same source type (e.g., all affiliate). Note it — the grader will enforce a diversity floor but the producer should know.
- Any beat where Shorts candidates exist but were not searched. Run the Shorts queries.

Wait for user approval before continuing.

### Phase 5: Grading

Follow the clip grader skill. Two passes: metadata triage (30 → 5), then transcript grade (5 → 1 pick with verbatim outcue).

**Diversity floor.** After pass 1, if all 5 survivors are the same source type (typically `affiliate`), replace the weakest survivor with the strongest candidate from a different source type. The goal is not to force non-affiliate picks, but to ensure the producer sees at least one alternative format in the shortlist. Tag the forced-in candidate so the producer knows why it is there.

**Shorts in pass 2.** Shorts candidates that survive pass 1 go through the same transcript grade as any other candidate. Do not penalize them for duration — 30-60 seconds is the format, not a flaw. A 45-second Short of a victim crying in their car can score higher than a 4-minute affiliate package where the victim appears for 12 seconds at 2:30.

### Checkpoint 3: Picks

Show picks.json before downloading anything. Every segment needs:

- A verbatim outcue verified against the transcript
- Source-type tag
- Flags for any fit, case-match, or mechanism concerns

Flag anything uncertain rather than picking. An empty beat costs less than a wrong clip discovered in the edit bay.

Wait for user approval before continuing.

### Phase 6: Download and cut

Download flagged clips. For each proposed segment, trim to the in/out span and, for vertical beats whose only source is a landscape repost, crop the pillar-boxed vertical back to full-screen 9:16.

Use `cut/crop_vertical.sh`. Always run its `frame` mode first on a landscape source to confirm where the subject sits before trusting the center-crop:

```
cut/crop_vertical.sh frame -i SRC.mp4 -t 0:30            # eyeball the layout
cut/crop_vertical.sh cut -i SRC.mp4 -s 0:00 -e 1:11 -o out.mp4 --vertical
```

`--native` when the source is already 9:16 (trim only), `--crop W:H:X:Y` or `--x <px>` when the subject is offset. Snap the out point to the verbatim outcue, not the raw seconds — copies are topped and tailed differently.

**Sourcing note.** Aggregator reposts (New York Post, and AI-narrator channels like "Glitz Gazette", "KnowKNEWZ") frequently carry the only findable copy but re-narrate over the audio or are DRM/bot-walled from download. The clean, clearable source is usually the subject's own social (Instagram) or the originating outlet. Flag this for the producer rather than shipping a repost's re-encode.

Deliver the final package: picks.json, cut clips, transcript files.

## The feedback loop

The pipeline is not strictly linear. At any checkpoint, information can flow backward:

- **Checkpoint 1 → Phase 1:** Sourcability scan reveals a named victim has no video. Go back to the script and swap.
- **Checkpoint 2 → Phase 3:** A beat returned too few candidates. Regenerate queries with different register emphasis or broader terms.
- **Checkpoint 3 → Phase 4:** The best candidate for a beat is a commentary video with no victim on camera. Search again with victim-register queries targeting the specific person.

The cost of a backward step is small (one search or one query regeneration). The cost of pushing forward with a bad beat is a wasted grading pass and a `flagged: null` at the end.

## Evaluation

Track per beat:

- Which register's query found the clip that was picked (anchor, news, victim, platform, shorts)
- Source type of the picked clip
- Whether the sourcability scan correctly predicted the outcome
- Whether a diversity-floor candidate was ultimately picked over an affiliate

This data tunes the weighting tables in the query generator and grader skills.
