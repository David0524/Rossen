# F2 07/29/2026 — TOP STORIES — clip pipeline run report

**Show day:** WEDNESDAY. **Beats:** 12 (Wednesday band 10–12). **Picks:** 11 flagged, 1 empty.
**Run directory:** `runs/F2_07292026_TOPSTORIES/`
**Primary deliverable:** `F2_TOP_STORIES_07292026_BIBLE_FILLED.docx`

This is a *different episode* from the existing `runs/F2_07292026/` (AI voice-clone /
FBI impersonation / back-to-school), which occupies the same 07/29 F2 slot. Those
artifacts were not resumed — resuming them would have graded the wrong show.

There is no cut stage. Clips were located, verified against transcript, and logged
as timecodes. Nothing was downloaded or cut.

---

## Source mix

```
Source mix, 11 picks:  affiliate 10 · creator_long 1
```

**affiliate holds 10 of 11 picks (91%)** — well past the 70% line. That is Jeff's
lean and it is defensible here: every one of these stories is a local-news case,
and affiliates title predictably and clear cleanly. But it means pass two mostly
chose between near-identical framings.

**The cheap swaps** — beats where the runner-up was a different source type:

| Beat | Flagged (affiliate) | Runner-up, different type | Gap |
|---|---|---|---|
| b09 | CityNews, 53s, reader | Punjabi Link Media, 183s, `creator_long` | 4 pts |
| b02 | WJLA, 90s | PepcoTV's own channel, 63s, `creator_long` | 16 pts |

b09 is the real one: 4 points apart and the runner-up has three times the runtime
on the same case. Both runners-up were **bot-walled at the caption step**, so
neither could be graded on transcript — that, not quality, is why they lost.

## Diversity floor: 5 of 6 promotions lost in pass two

The floor fired on b02, b05, b07, b09, b10, b12. Only **b07's** promotion survived
— and it won outright (Vive Health's own install video, the single best answer on
the board for that beat). The other five were promoted and then rejected:

- b05 → a Reddit text thread, 58 points below what it displaced
- b10 → a CBC story about a *British Columbia* Airbnb, wrong case entirely
- b12 → a Hopper complaint video predating the settlement
- b02, b09 → legitimate candidates, killed by the caption bot-wall

Per the grader skill, that pattern repeating means the floor is reaching past
usable material into filler, and **the hard filters upstream need a look** — not
that variety is unavailable. Three of the five promotions were off-case entirely,
which a case-identity filter would have caught before the floor ever ran.

---

## Beat table

| Beat | Role | Or. | Pri | Source | IN–OUT | Outcue |
|---|---|---|---|---|---|---|
| b01 | victim_interview | H | 1 | ABC13 Houston | 0:55–1:47 **+** 2:03–2:33 | "in jewelry, cash, and family heirlooms" / "I think they need to pick him up and put him in jail" |
| b02 | authority_report | H | 2 | WJLA | 0:37–1:18 | "Last year, a victim lost $18,500" |
| b03 | authority_report | H | 2 | KPRC 2 | 1:20–1:43 | "which says it does not and contractors to private homes" |
| b04 | evidence | **V** | 1 | WXYZ Detroit | 0:23–0:37 | "dead and his wife tied up and terrorized" |
| b05 | confrontation_bust | H | 2 | NBC10 Philadelphia | 0:33–1:41 | "I am glad you got these people" |
| b06 | explainer_demo | H | 1 | Local 4 Detroit | 0:45–1:01 **+** 2:13–2:28 | "these have a hidden camera" / "let me inside no questions asked" |
| b07 | evidence (b-roll) | H | 2 | Vive Health | 3:56–4:20 **+** 4:42–5:12 | *picture only, no outcue* |
| b08 | authority_report | H | 2 | Channel 3000 | 0:02–0:23 | "the bed rails are attached to the bed" |
| b09 | authority_report | H | 2 | CityNews Calgary | 0:08–0:48 | "He has a court date set for August 7th" |
| b10 | victim_interview | H | 1 | WMTV Madison | 0:47–1:25 | "there could have been anything that they got on cameras" |
| b11 | confrontation_bust | H | 2 | WKYC (Short) | 0:20–0:35 **+** 0:54–1:10 | "I knew it was wrong, but the novelty quickly wore off" / "We will never forget what he did to us" |
| b12 | authority_report | H | 3 | — | — | **FLAGGED NULL** |

Every outcue was located verbatim in its transcript and the out-point *derived
from where the phrase ends*, so quote and timecode cannot disagree. In-points are
snapped 2–5s early on a sentence boundary. Four beats are butt-cuts (b01, b06,
b07, b11). No outcue is UNVERIFIED — `faster-whisper` was installed, but in the
end no pick needed it, because b04's YouTube carrier had a caption track.

## The one gap

**b12 (Hopper FTC settlement) — `flagged: null`.** No broadcast video exists on any
captioned platform. The YouTube result space is almost entirely "how to get a
refund from Hopper" affiliate-marketing tutorials plus FTC-robotics-competition
noise; the one on-topic upload is a generic keyword channel that reads as AI slop
and fails the hard filters. Credible sources are text only (TechCrunch, the FTC
release). Priority 3, and **the script already carries the right answer as its own
fallback** — fullscreen the release and let Jeff read it. Nothing cleared 55, so
nothing was flagged.

Suggested query if you want another pass: search the CNBC and Yahoo Finance video
desks directly for the 07/02 consumer-settlement hit. A business-desk VO-SOT is
the realistic get, not an affiliate package.

## Manual lane (no invented timecodes)

No beat had `source_native` set — nobody in this script filmed themselves, so
there are no native social permalinks to hand over. Four beats carry a caption-less
web source as an **ALSO** entry in the doc, linked but with no timecode:

- **b06** — ABC13's actual 2018 "WOULD YOU FALL FOR IT?" package, the one the script
  was written to. Scored 88 in pass one, highest on the beat. `abc13.com/…/3505105/`
- **b08** — the KTVB/Tegna wire cut carrying the two deaths and the 122,000 figure
  the flagged clip lacks.
- **b11** — WBNS 10TV's 158s cut, which may carry the sheriff soundbite the flagged
  71s version doesn't.
- **b12** — the FTC release.

---

## Needs your ruling before air (Checkpoint 3 — these touch the script)

**1. b06 — script swap.** The flagged clip is structurally exactly this beat: Local 4's
"Help Me Hank" in a hard hat with a hidden camera in the safety goggles, teamed with
Ferndale police, at real doorsteps, and the payoff line *"that was the only man who
said no, every other guy I approached opened the door, let me inside, no questions
asked."* But it is Detroit, not Houston. Changing to it means rewriting: the
CenterPoint partnership, **Tia Alexander** who asked for ID, homeowners waving him
toward the **backyard gate** (here they let him inside the house), and *"watch how
fast he drives off the second somebody asks"* — which does not happen in this
package. Alternative: keep the script and run the ABC13 original as a manual pull.

**2. b11 — script swap.** The script cues *"WATCH WHAT THE SHERIFF'S OFFICE SAID WHEN
THE SENTENCE CAME DOWN."* No sheriff or prosecutor speaks in any available cut. The
speakers are the defendant Jason Yard (*"I knew it was wrong, but the novelty quickly
wore off"*) and the mother of a three-year-old guest (*"We will never forget what he
did to us"*). The mother is by far the stronger moment. The setup line needs to point
at her instead.

**3. b04 — orientation ruling.** You typed VERTICAL. Every available copy of the
sheriff-released doorbell footage is embedded in a horizontal affiliate package. Kept
as vertical per the hard filter and routed Brave-only; the flagged WXYZ clip carries
the doorbell view with raw audio intact at 0:26. Needs a punch-in/crop call —
`cut/crop_vertical.sh` is in the repo.

**4. b10 — name check.** The auto-caption renders the bachelorette-weekend guest as
**"Janice Faust"**; the script says **SHANISE FAUST**. Auto-captions mangle names
routinely so this proves nothing either way, but the script says the name out loud.

**5. b09 — two script corrections.** CityNews says **one** count of break and enter and
voyeurism; the script says *FIVE COUNTS OF VOYEURISM AND ONE COUNT OF BREAK AND
ENTER*. Also a fact the script doesn't have: police say Park may be a landlord in
**Vancouver and Toronto** as well, targeting Korean women.

**6. b01 — one figure.** The transcript says the safe held *"more than $200,000"* in
jewelry, cash and heirlooms. The script says *HUNDREDS OF THOUSANDS OF DOLLARS IN CASH
AND JEWELRY*. Police-reported totals often exceed the safe's contents, so this may be
fine — but the clip says $200K.

**7. b08 — fit caveat.** The flagged clip covers the **February** recall, not March's
122,000-unit action. Tells: *"no injuries have been reported"*, "thousands" not
122,000, missing hazard labels, sold *"August 2023 through December of last year"*. It
fits the script's February paragraph but **cannot carry the two deaths**.

**8. b07 — clearance/optics.** The b-roll is Vive Health's own marketing video for the
product being recalled. Free and exactly on-spec (correct model line — LVA2009SLV
COMPACT BED RAIL is first on your recall graphic), but airing the manufacturer's
promo footage over a story about two deaths in that product is your call.

---

## What I fixed without asking

**A real defect in `rossen_harvest/dedupe.py`.** Pass-2 fuzzy-title dedupe matched
across platforms and its survivor rule preferred the earliest upload date. So when a
station's own website page and its own YouTube upload of the *same package* collided
on title, the website copy could win — discarding the only copy with a caption track.
Since an outcue must be quoted verbatim from a transcript, that silently degrades a
beat to a manual-lane LOCATED for no editorial gain (same outlet, so clearance is a
wash).

This was costing this run four beats. `mwHYj6Pn8R8` (b01's exact case), `fNxPpoMBK0M`
(b10's), `i8ie5dvEge0` (b02's) and `WxR6-ycJwaQ` (b03's) were all sitting at **rank 1
in the search cache** and all absent from `candidates.json`. Fixed so a captionable
copy wins a cross-platform collision; the earliest-upload rule is untouched where it
belongs (within-YouTube wire duplicates still keep the originating station).
Re-running off cache recovered 18 captionable twins. 15-assertion regression test
added covering both arrival orders, the wire case, the neither-captionable case, and
non-collision. All 105 pre-existing harvest tests still pass.

**This almost certainly means the previous run's LOCATED rows were wrong too** —
b01/b04/b05 there were all recorded as "exact case on news_web, no captioned YouTube
twin," which is precisely the signature of this bug.

**Caption bot-wall, retried not laundered.** Four caption fetches returned null with
*"Sign in to confirm you're not a bot"* — a rate limit, not captions-disabled. b04's
top pick was one of them. Cleared the negative cache entries and retried spaced;
**b04 recovered** (79 cues). The other three (b02's PepcoTV, b09's Punjabi Link, b11's
LOCAL12) stayed walled and were demoted — recorded as bot-walled, not as
caption-less, because those are different facts.

**Query misses re-queried, not written off.** Six sourcability probes returned zero.
Re-probing looser showed five were query misses, not absences: over-specified proper
nouns were the cause. `"hidden cameras Verona Airbnb outlet"` → zero;
`"hidden cameras bathroom outlets Madison Airbnb rental"` → the exact package at rank
1. Zeros interleaved with hits, which ruled out a limiter. Every zero was retried once
before being recorded.

---

## Answering the sidecar question

**There is no `beats_hint.json`.** Nothing by that name exists on the filesystem. But
the script carries the same information inline as `(((CLIP CONTEXT)))` blocks with
`SEARCH REGISTER` strings, so those were merged at Step 2 as `hint_source:
inline_clip_context` and kept separately in `hint_queries` so they could be scored.

**The hints lost, 4–11.** A hint string surfaced the winning pick on 4 of 11 beats
(b03, b05, b07, b09). Generated queries surfaced all 11. Two failure modes:

1. **Over-specification.** b10's hint `hidden cameras Verona Airbnb outlet` returns
   zero — the city and state narrow it past the affiliate's own headline syntax. Same
   on b01.
2. **Stale premises.** b05's hints were built on *"NO BROADCAST VIDEO FOUND YET —
   PRINT SOURCE ONLY."* That is false: NBC10 and 6abc both have it on YouTube. b07's
   context said *"NO CANDIDATE FOUND"*; Vive's own video is the best b-roll on the
   board. b11's hint had a truncated Spectrum News URL when WKYC and WBNS both cover
   the sentencing.

The sourcability scan corrected the producer's own research on **six** beats: b01,
b02, b05, b09, b11 gained captioned YouTube sources the hints didn't list, and b07
went from "no candidate found" to a strong pick.

**Register yield across the 11 winning picks** (a beat can be found by several):

| register | found the pick |
|---|---|
| news | 9 |
| anchor | 8 |
| platform | 7 |
| shorts | 5 |
| **victim** | **0** |

`victim` contributed **nothing**, on 11 beats, 10 of them horizontal — an independent
second confirmation of the query generator's measured recall@30 result (n=8). Two
samples now say the same thing. It is still untested on vertical, and this run had
only one vertical beat, so the skill's "unproven-not-disproven" framing still holds —
but the horizontal case is looking settled.

One Short (`Lix_CaVtAHo`, 71s) won a **horizontal** beat, which is the query
generator's "run Shorts on every orientation" rule paying off.

---

## Validators

All four ran and all cleared to zero ERRORs.

| Validator | Result |
|---|---|
| `check_beats beats.json --day wednesday` | 0 errors, 4 warnings |
| `check_queries beats.json` | 0 errors, 0 warnings — 197 strings, 5 registers × 12 beats |
| `contract_check beats beats.json` | 0 errors |
| `check_grades one shortlist.json` | 0 errors, 11 warnings |
| `check_grades two picks.json --transcripts` | **0 errors, 0 warnings** |
| `contract_check picks picks.json` | 0 errors |

**The validators did not exist in this repo.** All five paths named in the run
contract were absent, along with `dependencies.md` and `schemas.md`. They were written
this run, each check citing the SKILL.md line it derives from, with `_contract.py`
holding shared vocabulary so the four cannot drift apart. Each script's docstring
states what it *cannot* check. Caveat worth keeping in view: these were authored in
the same session as the output they validate, so they cannot catch a contract that
was misunderstood in both places at once.

Warnings, all expected and all explained above: the 4 `check_beats` warnings are the
b06/b07/b08/b12 sourcability flags from Checkpoint 1 (two of which the full search
then overturned); the 11 `check_grades one` warnings are short shortlists on beats
where the case space is genuinely thin, plus all-affiliate shortlists where no
non-affiliate candidate cleared the hard filters.

`check_grades two` was run **with** `--transcripts`, so its outcue check was a real
verbatim re-verification against the caption data rather than a shape check — an
independent confirmation of what the pick builder asserted.

## Stale documentation found in `rossen-pipeline/SKILL.md`

- Step 3 documents `rossen_harvest search`; the real subcommand is `harvest`.
- Step 5 documents `rossen_harvest captions shortlist.json --out transcripts.json`.
  **There is no `captions` subcommand** — only `harvest` and `eval`. Used
  `transcripts.fetch_many()` directly.
- Step 7 documents a download-and-cut stage and Step 8 references clips that failed
  to download. There is no cut stage.
- Step 2 says "four registers"; the query generator specifies five and the Shorts leg
  needs the fifth.

## Counts

```
search      7,225 raw -> 5,685 after dedupe, 12 beats, youtube + brave (no DEGRADED line)
            by platform: youtube 4,648 · news_web 979 · reddit 49 · x 6 · instagram 3
            zero beats returned zero candidates
shortlist   52 rows / 12 beats (2-5 per beat)
transcripts 33 of 36 youtube shortlist entries; 3 bot-walled, 0 genuinely caption-less
picks       11 flagged, 1 null; 15 segments; 4 butt-cuts
```
