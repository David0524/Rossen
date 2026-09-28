# Your First Big Win: demo reel

A 40-second vertical demo reel (1080x1920, 24 fps, 96 BPM, 16 bars) that shows creators what the service makes. One continuous story is told by four invented creators' series, each in its own fully committed visual style. The hero, "you", appears only as a hand and in captions.

This folder is self-contained and separate from the Rossen Reports work. It has its own palettes, textures, fonts, characters, sounds and output. It shares only generic tooling (the canvas core, the render script and the sync checker).

**Deliverables** (in `final/`):

- `Your First Big Win - demo reel (9x16).mp4`: the preview, CRF 21, about 10 MB.
- `... master.mp4`: the master, CRF 16.
- `verify (preview).txt`, `verify (master).txt` and `sync.txt`: the checks run on each file.
- `audio_sources.txt`: every recorded sound, with its source and license.

## The story

| Bars | Time | Chapter | Style | What happens |
|---|---|---|---|---|
| 0 | 0-2.5 s | Open | Plain paper | YOUR FIRST BIG WIN lands, then the page flips up to reveal chapter 1. |
| 1-3 | 2.5-10 s | Careers: RED FLAG OR GREEN FLAG? (Raj) | Ink on warm paper | The title card. Posting A lands in your hand, Raj raises his red flag and RED FLAG is stamped. Posting B gets GREEN FLAG. Your thumb presses APPLY, and the posting turns over: YOU GOT THE JOB. |
| (T1) | around 10.0 s | | | The letter flies at the camera and folds in three: the first fold snaps shut on the downbeat, the second half a beat later. The ink and hatching dissolve into riso grain, and the wax seal becomes the paycheck's $ badge. |
| 4-6 | 10-17.5 s | Personal finance: MONEY RULES (Maya) | Risograph | The paycheck lands in your hand, then MONEY RULE #1. Maya catches a chunk of the paycheck for her piggy bank before the rest reaches the spend pile: PAY YOURSELF FIRST. The piggy bank fills and gets a TRIP FUND label. |
| (T2) | 17.5 s exactly | | | A hard cut on the downbeat. The music changes at the same instant. |
| 7-9 | 17.5-25 s | Productivity: ONE HABIT (Hana) | Graphite minimalism | A sticky note: DAY 1 AT THE NEW JOB. Then ONE HABIT. The list draws itself in pencil, the two-minute rule appears, and you tick items off in blue until only BOOK THE TRIP is left. |
| (T3) | 24.4-25.0 s | | | Hana tears the page. It peels away like a sticker backing onto Diego's sticker world. |
| 10-12 | 25-32.5 s | Travel: PACK OR PASS? (Diego) | Sticker cartoon | POWER BANK IN YOUR CHECKED BAG? Diego pulls his uh-oh face, a PASS sticker lands, and the power bank goes into the carry-on. Then SPARE BATTERIES GO IN YOUR CARRY-ON., and you zip the bag. |
| 13 | 32.5-35 s | Lineup | Plain paper | The four hosts as four die-cut stickers: ONE STORY. FOUR STYLES. YOUR CHARACTER. |
| 14-15 | 35-40 s | End card | Plain paper | ANIMATED SERIES FOR CREATORS / NEW EPISODES IN A DAY / name / email. The last second is completely still. |

The four chapters get 3 bars each. All on-screen copy, including the end card's `{{YOUR NAME OR BUSINESS NAME}}` and `{{YOUR EMAIL}}`, lives in `reel.json`. To fill them in, edit that file and run `sh tools/build.sh`.

## The styles (`styles/`)

- **Ink** (`ink.js`): warm paper with fibres, mottling and a watercolor wash. Dip-pen strokes are filled polygons whose width varies with pressure. Cross-hatched shadows. The accents are brick red, plus a muted ink green on the good posting only. Type is Playfair Display.
- **Riso** (`riso.js`): three fluorescent ink plates (pink, teal, yellow). Each plate is punched with grain and speckle, then multiplied onto white paper out of register. Type is Archivo Black: pink over teal with a solid navy core, so letters have no texture inside.
- **Graphite** (`graphite.js`): pencil passes of varying weight, with the paper's tooth punched out of the pencil layer. Light shading, and sky blue as the only colour. Type is Inter.
- **Sticker** (`sticker.js`): thick black outlines, one-tone cel shading, and props die-cut with a white border and a soft shadow. Type is Fredoka.
- **Plain** (`plain.js`): the reel's own neutral frame for the open, the lineup and the end card. Type is Bricolage Grotesque.
- **The hand** (`lib/hand.js`): one set of hand geometry, drawn by every style, so "you" is recognisably the same hand in all four worlds.

## Characters

`ref/` holds the four reference drawings. `tools/cut_puppets.py` cuts them into jointed paper-cutout puppets in `assets/` (head, arms, torso and two legs, with hidden fills under the moving parts). It also makes Diego's alternate uh-oh head and the die-cut stickers used in the lineup.

## Sound

`tools/score.py` composes the score on the beat grid from the film's own cue sheet (`out/reel/timeline.json`), so picture and sound can't drift apart.

- **The groove:** one continuous 96 BPM groove whose instrumentation changes each chapter:
  - careers is dry, with walking bass and plucks;
  - finance is bouncy pizzicato with xylophone;
  - productivity is soft upright piano;
  - travel drives, with drums and brass;
  - the lineup and end card settle and ring out.
- **Foley:** paper, stamps, coins, a paper rip, a pencil, a tape peel, sticker slaps and a zipper. Each hit is placed by its audible attack.
- **Sources:** all recordings are CC0 (VSCO 2 CE, Kenney, the FreePats Upright Piano KW, and OpenGameArt recordings by Luckius, AntumDeluge and OwlishMedia). The reel keeps its own copies in `audio/`. `final/audio_sources.txt` logs every file with its source URL and license, and says what is composed.

## Build and check

```sh
sh tools/build.sh      # frames -> score -> master + preview -> sync + verification (about 6 minutes)
```

- `tools/verify.py` checks the decoded mp4. It covers:
  - length and bars;
  - equal chapter bars;
  - the hard cut landing on the downbeat;
  - every text card holding still while it is up;
  - no colour leaks between styles;
  - the safe zones;
  - flashing;
  - a completely still last second.
- `tools/sync_check.py` measures every hit's audio onset against its picture time.
- `node render.mjs --html reel.html --query safe=1 --only ...` renders the safe-zone overlay (`_check/safe/`).
- `t1.html` / `t1.js` and `_check/transition-1-test.mp4` are the approved 5-second look test for transition 1, kept for reference. The reel itself is `reel.html` / `film.js`.
