# Prompt: amend the skills to fix vertical video sourcing

Paste everything below the rule into a session that has the repo checked out.
It is a directive to change the skills, not a spec — the diagnosis is settled,
the redesign is yours.

---

The vertical video path in this pipeline has failed on every episode it has been
run against. I want you to read the evidence, work out what the skills got wrong,
and amend them. Do not treat this as a request to add a note about vertical being
hard — the failure is structural and the fix will change how beats are extracted,
how queries are generated, and how candidates are graded.

## The record, measured from `runs/*/candidates.json` and the yield log

**Seven vertical beats have been attempted across three episodes. Zero were
satisfied cleanly by the automated pipeline on first pass.**

| Run | Beat | Role | What happened |
|---|---|---|---|
| 07-29 | F2b-b08 | evidence | EMPTY — no fake-IC3-page screen recording found |
| 07-29 | F2b-b11 | evidence | EMPTY — no scam-text screen recording found |
| 08-05 | b02 | evidence | EMPTY, then case-swapped to a horizontal package |
| 08-05 | b05 | first_person_rant | WEAK (got a news explainer, not a first-person reaction), then swapped and re-roled |
| 08-05 | b07 | evidence | EMPTY, then case-swapped to horizontal |
| 08-05 | b09 | evidence | Satisfied once by a **YouTube Short**. On a second run, triage shipped a **1920x1080 landscape** video against this vertical beat; the user caught it; it was hand-fixed with a bespoke `site:tiktok.com` Brave query |
| 08-07 | b03 | evidence | Assigned SHOW-PRODUCED before search |

**Native social yield across all three episodes: 8 candidates out of 7,549. That
is 0.11%.**

| Run | Total candidates | tiktok | instagram | facebook | x |
|---|---|---|---|---|---|
| 07-29 | 2,838 | 2 | 0 | 0 | 0 |
| 08-05 | 2,975 | 2 | 0 | 1 | 1 |
| 08-07 | 1,736 | 1 | 1 | 0 | 0 |

Three episodes of query generation aimed at TikTok, Instagram and Facebook
produced eight usable native candidates total. The queries were not the problem
in any obvious way — they were written to the platform register, kept short,
hashtag-led. The surface simply is not reachable by the tools wired in.

## What I think went wrong — verify this before acting on it

**1. Orientation was inferred instead of verified.** `triage.py` treated any
YouTube candidate under 75 seconds as vertical, on the theory that short YouTube
uploads are Shorts and Shorts are vertical. Plenty of ordinary 16:9 videos run
under a minute. This shipped a landscape clip against a vertical beat and it took
a human to catch. Duration is not orientation. Nothing in the pipeline ever
checked actual pixel dimensions before asserting a candidate satisfied a vertical
hard filter.

**2. Vertical beats were structurally excluded from the only vertical surface
that works.** `__main__.py` gated the YouTube backend on
`orientation != "vertical"`, so a vertical beat's `shorts` register ran *nowhere*
— despite the query-generator skill stating in plain text that Shorts run on
every orientation. Meanwhile the one clean vertical success in the whole record
(08-05 b09, first run) came from a YouTube Short. The pipeline had its best
vertical source switched off for exactly the beats that needed it. This is fixed
in code as of 2026-07-24, but **the fix has never been exercised against a live
vertical beat**, because 08-07's only vertical beat went show-produced. Confirming
it is part of your job.

**3. "Vertical" and "native social post" were treated as the same thing. They are
not.** Vertical is an aspect ratio. Native social is a platform and a rights
situation. A YouTube Short is vertical, searchable, captioned, and clearable. A
TikTok post is vertical, barely searchable, uncaptioned, and awkward to clear.
The skills use one word for both and route accordingly, which is why beats that
only ever needed a portrait frame were sent hunting for a TikTok permalink.

**4. Whisper was treated as the answer to the vertical caption gap, and it has
never once run successfully in this codebase.** It transcribes bytes something
else must fetch. Where media is blocked — as it is here for both YouTube and
TikTok — it has no input. Building it was reasonable; relying on it in the skill
text as though it closes the gap is not, because it only closes the gap when
media is reachable, and nothing checks that before promising it.

**5. Six of seven vertical beats were role `evidence`, and most were
screen-recordings of a web page or a text thread.** That is not footage anyone
else has a reason to have posted. The 08-07 run finally named this correctly and
routed it to production instead of search. That should have happened at
extraction on all six, not after three full harvests.

**6. The fallback has always been "swap to horizontal."** Three swaps on 08-05
alone. It works, and the producer approved each one, but it quietly costs the
show the raw handheld texture Rossen explicitly prefers — the skills themselves
say a shaky vertical video of a family in a burned garage beats any polished
package. A pipeline whose vertical answer is always "use a horizontal clip
instead" has given up on a stated editorial preference without ever saying so out
loud.

## What I want you to change

Work out the specifics yourself, but these are the outcomes I am asking for.

**Make orientation a verified property, never an inferred one.** Decide what
counts as proof, where the check belongs, and what a candidate looks like when
orientation is unknown rather than confirmed. A beat's hard filter should never be
satisfied by a guess, and "unknown" should be visible to the grader rather than
silently coerced to one value or the other.

**Separate the aspect-ratio question from the platform question** everywhere the
skills currently conflate them — beat extraction, query generation, routing, and
grading. A beat should be able to say "portrait frame required" independently of
"must be a native social post," because those have completely different
sourcing odds and the current vocabulary cannot express the difference.

**Promote Shorts to the primary vertical strategy and say why in the skill text.**
The evidence supports it: one clean vertical win, and it came from Shorts, versus
0.11% native social yield. Anything that presents Shorts as a secondary or
crossover surface is now contradicted by the data.

**Give vertical beats a realistic triage at extraction time.** Six of seven were
sent to a full harvest that could not possibly satisfy them. The sourcability scan
already predicted this correctly on 08-07 and saved the run. Generalize that: a
vertical beat should be classified before search into something like
Shorts-satisfiable, native-post-findable (a named person whose own post can be
located via press coverage), show-produced, or genuinely impossible — and only the
first two should consume harvest budget. Name the categories however you think is
right.

**Be honest in the skill text about what the tools can actually reach.** Anything
that promises a capability contingent on media access should say what happens when
media is blocked, and the pipeline should find that out by probing rather than by
failing at Step 5. Do not delete `vertical_transcribe.py` — it is correct code
that some environments can run. Fix what the skills claim about it.

**Say the editorial cost out loud.** When a vertical beat swaps to horizontal, the
report should note what texture was lost, so the producer is making that trade
knowingly and repeatedly rather than by default.

## Constraints

Do not weaken the hard rules to make vertical easier. Outcues still come from
transcripts, verbatim, or the segment ships flagged with no outcue. An honest
empty beat still beats a bad pick. A case swap is still the producer's call.

Amend the skills — `rossen-beat-extractor`, `rossen-query-generator`,
`rossen-clip-grader`, `rossen-pipeline` — rather than writing a new document about
vertical. If a change belongs in code (`harvest/rossen_harvest/`), make it there
and keep the 128 tests passing, adding coverage for anything new.

Record what you changed and why in
`.claude/skills/rossen-beat-extractor/reference/beat_yield.md`, so the next run
inherits the reasoning and not just the result.

Where the evidence above is thin — one clean Shorts win is one data point, not a
trend — say so in the skill text rather than overclaiming. The failure record is
solid; the remedy is a hypothesis until an episode tests it.
