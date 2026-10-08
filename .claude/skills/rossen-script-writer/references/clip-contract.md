# The clip contract — full detail

Load when placing clip beats or when `check_bible.py` names a marker problem.
SKILL.md carries the rules that govern every draft; this file carries the
tables, the variants and the aired precedents behind them.

- [Markers by stage](#markers-by-stage)
- [Silent B-roll](#silent-b-roll-jeff-talks-over)
- [Not clip beats](#not-clip-beats)
- [Butt cuts](#butt-cuts)
- [Orientation](#orientation-is-a-hard-constraint-not-a-formatting-detail)
- [The boundary marker](#the-boundary-marker)
- [Lead-in phrasing](#lead-in-phrasing-sets-the-clip-role)

## Markers by stage

DRAFT — clips not yet locked:

```
(((PLAY CLIP XXX HORIZONTAL)))
OUT:
```

FINAL — clips locked from the outline, numbered in air order, outcue filled
with the transcribed last words before we cut back:

```
(((PLAY CLIP 3 VERTICAL)))
OUT: (AND THAT'S WHEN SHE KNEW)

((([Outlet](URL) · 0:18 - 0:53 (AND THAT'S WHEN SHE KNEW))))
```

The red source line under a FINAL clip is the outline's Videos row: the outlet
linked to the clip, in - out with each segment's outcue, `BUTT` between
segments. Copy it from the outline; never retime it here. A MANUAL clip (no
transcript) keeps a blank `OUT:` and only the linked outlet. This is the form
the producer sent to Jeff on 10/14 (`references/examples/bible-sent-10-14.txt`).

Rules for both stages:

- On its own line, exactly three parens each side, orientation always present.
  Aired bibles contain two, four and five parens, a hyphen before the
  orientation, and one with no orientation at all. Those are typos; normalize.
- `OUT:` directly beneath, no blank line between.
- Nothing else under the marker except, in FINAL, that one red source line
  after a blank line. No clip-context block (Jeff removed it), no transcript, no
  description. The candidate URL, in/out timecodes, what the clip is known to
  show and verification notes also go in the companion source log, keyed by
  clip number (FINAL) or beat id (DRAFT). A DRAFT has nothing under `OUT:`.
- FINAL numbering runs 1, 2, 3… in document order with no gaps or repeats.
  BROLL beats are numbered in the same sequence.

## Silent B-roll Jeff talks over

Footage that runs mute while he narrates. It sources differently, so mark it
differently:

```
(((PLAY CLIP XXX VERTICAL BROLL)))
OUT:
```

The `BROLL` token tells the extractor to treat the beat as picture-only — no
outcue to find, no transcript to match. In FINAL, `OUT:` on a BROLL beat may stay
blank. Aired precedents, written inconsistently: `(((PLAY CLIP 6 BROLL
VERTICAL)))` on 06/22 and `(PLAY CLIP SHOP WITH POINTS 2 HORIZONTAL - BROLL JEFF
WILL TALK OVER)` on 06/26. Add `**(JEFF TALK OVER)**` above the marker when it
helps the control room.

## Not clip beats

Stills, art and screen work, all sourced separately. Never counted as clip beats:

```
(((TAKE ... SCREENSHOT)))
(((TAKE ... STILL)))
(((TAKE FULLSCREEN)))
(((CREATE FULL SCREEN GRAPHIC XXX)))
(((JEFF SCREEN SHARE)))
(((END SCREENSHARE)))
```

A segment built only from these is salvage, not a form to plan. If a story has
no findable footage, say so in the chat reply.

## Butt cuts

When one source will be cut into several segments, `BUTT` on its own line
between them. Roughly one beat in six.

## Orientation is a hard constraint, not a formatting detail

The pipeline will not search the other kind. Choose deliberately — and in
FINAL, match the orientation of the clip the outline actually picked.

| Footage | Orientation | Where it lives |
|---|---|---|
| Victim telling their story to a reporter | HORIZONTAL | YouTube, network, local affiliate |
| Someone venting to their phone camera | VERTICAL | TikTok, Reels, Facebook |
| Doorbell cam, security cam, screen recording of a scam text | VERTICAL | TikTok, Facebook, Reddit |
| Reporter or creator confronting a scammer | either | pick by where that footage actually lives |

## The boundary marker

The pipeline drops everything before the first `HIT LIKE AND SUBSCRIBE` or
`JOIN THE CHAT` line. That marker closes the tease block every time.

Never put a `PLAY CLIP` marker inside the tease block, or inside a
`TEASE // SPONSOR` block. The tease restates each story in beat language and
reads exactly like body copy; a marker in there produces an unresolvable
duplicate beat.

## Lead-in phrasing sets the clip role

The last line before the marker tells the extractor what kind of footage this
is. Treat the table as the *final* line of a runway whose line above it asks the
question — a role phrase alone is not a setup.

| Lead-in | Signals |
|---|---|
| LISTEN TO WHAT HAPPENED TO HIM / THINK WHAT YOU WOULD DO | victim interview (audio-led: LISTEN, not HEAR) |
| WATCH WHAT HAPPENS WHEN / HE SET UP A REAL STING / BUSTED HIM IN THE ACT | confrontation or bust |
| CHECK THIS OUT / HERE YOU CAN SEE | evidence footage |
| HERE'S WHAT WE KNOW RIGHT NOW | network or wire report — capped at two per bible |
| WATCH HIM SHOW YOU HOW / LET ME SHOW YOU | explainer, demo or screen share |

The team's cue-plus-verdict line (`WATCH THIS. THIS IS CRAZY.`) can follow or
replace the role phrase; the checker accepts either.
