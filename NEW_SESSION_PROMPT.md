# Paste-ready kickoff prompts

Copy one of these into a fresh Claude Code chat. They exist because a cold
session re-derives the same context every time and gets the same few things
wrong — the branch, `pandoc`, `PYTHONPATH`, and whether the network paths
actually answer.

---

## A. Running the pipeline on a new script

> Repo: David0524/Rossen, branch `claude/rossen-pipeline-script-hcflp6` — check
> this branch out, **not** the default branch. It has the current skills, the
> harvest package, and `harvest/requirements.txt`.
>
> Read `HANDOFF.md` first, then `.claude/skills/rossen-pipeline/SKILL.md`, and run
> the full pipeline on [ATTACH SCRIPT .docx].
>
> Work autonomously — don't ask permission for anything reversible.
>
> Run the Preflight block in the skill doc as written, **including the network
> probes**. Confirm what's actually available before proceeding; don't assume
> anything carries over from a prior chat. Note that `pandoc` is not installed —
> use the zipfile fallback in the beat-extractor skill.
>
> Stop for me twice:
> 1. After beats and queries, before search.
> 2. Before any repair proposal touches the script itself.
>
> Hard rules:
> - Every segment needs an outcue found verbatim in the transcript, verified with
>   `Transcript.find()` — never by eye, never invented. If no transcript is
>   reachable, ship the pick with no outcue and flag it unverified.
> - If nothing clears the bar for a beat, flag it empty. An honest gap beats a bad
>   pick.
> - Diagnose before repairing — zero candidates for a beat is a query problem, not
>   a search problem. Say which queries you ran before calling a case unsourceable.
> - Orientation is a hard filter, not a hint. The one exception is a Short
>   surfaced against a horizontal beat, which gets scored with the framing
>   question flagged for me.
> - A `BUTT` marker means both segments come from the **same source**. Prefer one
>   source cut twice.
> - There is no automated download-and-cut stage in this codebase. Step 7 is a
>   hand-written manifest. Don't claim clips were pulled or cut.
> - YouTube media bytes (audio included) and TikTok are blocked in this
>   environment. Captions work but throttle easily — probe once, never loop
>   player clients, and retry through `fetch_many` after a wait before concluding
>   anything is blocked.
>
> When you're done: write `report.md` to the run directory, append every beat to
> `.claude/skills/rossen-beat-extractor/reference/beat_yield.md` (that exact path
> — not a bare `reference/beat_yield.md`), and build the filled Bible `.docx` per
> Step 8 with blue hyperlinks at PLAY CLIP markers and red for empty, weak,
> swapped, show-produced, or no-timecode beats. Commit and push to the branch
> above.

---

## B. Writing a new script

> Repo: David0524/Rossen, branch `claude/rossen-pipeline-script-hcflp6`.
>
> Read `HANDOFF.md`, then `.claude/skills/rossen-script-writer/SKILL.md`, and
> write the Bible for [DATE / show type].
>
> Before you write clip beats, read
> `.claude/skills/rossen-beat-extractor/reference/beat_yield.md`. It records what
> past beats actually yielded. The standing finding: **vertical `evidence` beats
> have yielded nothing in 4 of 4 attempts.** Write toward footage that exists —
> if a beat can only be satisfied by a screen recording of a specific web page,
> mark it show-produced in the script rather than sending it to the clip pipeline.
>
> Stories/topics: [PASTE]

---

## C. Picking up mid-run or resuming

> Repo: David0524/Rossen, branch `claude/rossen-pipeline-script-hcflp6`.
>
> Read `HANDOFF.md`, then the newest `runs/*/report.md` to see where the last run
> ended. Every stage writes a file and `harvest.db` caches searches and captions
> for two weeks, so resume at the first stage whose output file is missing. Don't
> delete `harvest.db` unless I ask for a genuinely cold run.
>
> Run the Preflight network probes first regardless — the last session's
> conclusions about what was reachable may not hold.

---

## D. Working on the skills or the harvest package

> Repo: David0524/Rossen, branch `claude/rossen-pipeline-script-hcflp6`.
>
> Read `HANDOFF.md` §7 before editing any skill. The repo is canonical and my
> Claude account is a deployment target — the account copies have drifted behind
> before and lost their `reference/` folders entirely, which fails silently
> because a skill pointing at a missing file just proceeds uncalibrated.
>
> After changing a skill, rebuild the bundles (`dist/skills/README.md` has the
> script) so I can re-upload.
>
> Tests are plain scripts, not pytest — run
> `for t in harvest/tests/*.py; do python3 "$t"; done`. Don't use pytest: it
> collects zero tests and dies on the module-level `sys.exit`, so a green pytest
> run would mean nothing ran. 128 currently pass; keep them passing and add
> coverage for anything new.
>
> Task: [PASTE]

---

## What to change in these prompts over time

The hard rules are durable. The **environment facts are not** — "YouTube media is
blocked," "captions throttle," "TikTok is IP-blocked" were all measured on
2026-07-24 on one egress IP. If a session finds different, that session is right
and this file is wrong. Update it rather than arguing with a live probe.

The branch name will also go stale once this work merges. Check
`git branch -r` rather than trusting the name above.
