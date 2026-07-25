# Beat yield log — MOVED

This is not the log. Do not append here.

The canonical log is:

```
.claude/skills/rossen-beat-extractor/reference/beat_yield.md
```

It lives inside the skill, beside `aired_examples.md`, so it travels with the
skill when the skill is deployed to a Claude account. A copy at this path does
not.

## Why this stub exists

This path used to hold a second, divergent copy of the log. It accumulated the
08-05 (×2) and 08-07 runs while the copy inside the skill sat frozen at
F2_07292026 — **zero episode overlap**, and two schemas that had drifted apart.
Both have been merged into the canonical file; nothing was dropped.

The cause was an ambiguous relative path: "append every beat to
`reference/beat_yield.md`" resolved here or there depending on the working
directory, and no skill documented which was meant. `rossen-pipeline` Step 9 now
names the full path explicitly. This stub stays so that anyone (or any model)
reaching for the old path gets redirected instead of silently starting a third
divergent copy.
