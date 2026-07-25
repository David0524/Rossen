# Rossen skills — transfer bundles

Upload-ready `.zip` bundles of all five Rossen skills, built from
`.claude/skills/` in this repo. Rebuild them any time with:

```bash
python3 - <<'EOF'
import zipfile, pathlib
src = pathlib.Path(".claude/skills")
out = pathlib.Path("dist/skills"); out.mkdir(parents=True, exist_ok=True)
for skill in sorted(p for p in src.iterdir() if p.is_dir()):
    with zipfile.ZipFile(out / f"{skill.name}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(skill.rglob("*")):
            if f.is_file():
                z.write(f, str(f.relative_to(src)))
EOF
```

Each archive's root contains the skill folder, e.g.
`rossen-beat-extractor/SKILL.md` plus its `reference/` files — which is what
the Skills uploader expects.

## Why these exist

The five Rossen skills already live in the Claude account (they sync down into
a session, with account `skillId`s recorded in `~/.claude/skills/manifest.json`).
But as of 2026-07-24 the account copies had drifted **behind** the repo, and
they had lost their `reference/` folders entirely:

| Skill | Repo | Account | Gap |
|---|---|---|---|
| rossen-pipeline | 375 lines | 167 | Shorts routing, network preflight probes, transcript ladder, Step 5/7 corrections |
| rossen-beat-extractor | 168 | 104 | the sourcability scan |
| rossen-query-generator | 150 | 122 | measured recall@30 results, Shorts dialect |
| rossen-clip-grader | — | — | in sync |
| rossen-script-writer | 740 | 740 | was account-only; now committed here |

The missing `reference/` folders matter more than the line counts. Three skills
instruct the reader to read files that were not present in the account copies:

- `rossen-beat-extractor/reference/aired_examples.md` — 24 worked beats from
  three episodes, the calibration set. `rossen-clip-grader` and
  `rossen-pipeline` both point at it too.
- `rossen-query-generator/reference/glossary.md` — editorial term to
  platform-native term mapping.

A skill whose instructions reference a file that does not exist degrades
silently: the model proceeds uncalibrated rather than erroring.

## The repo is the source of truth

Treat `.claude/skills/` in this repo as canonical and the account as a
deployment target, not the reverse. The account has no version history, no
diff, and no way to tell which of two copies is newer. Every improvement in
this repo arrived with a commit message explaining the measurement behind it;
that context does not survive a copy-paste into a settings pane.

So: edit here, commit, rebuild bundles, re-upload. Never edit in the account
and expect it to come back.
