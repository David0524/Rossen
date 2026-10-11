# Pitch email — Step 2

The email that goes to Jeff and Ryan for a yes/no. Plain text, pasted straight
into a mail client. No markdown bold, no headers, no tables. This is the team's
house format (Matt Raub's template, producer kit, Sept 2026); Jeff reads the
headline and the titles first. A real one is in
`examples/pitch-email-2026-09-28-F2-A-options.md`. Read it before drafting.

## Shape

```
Subject: F2 Pitches for [tape date] ([air date] Air)

Jeff, Ryan,

[One or two lines: what these are for, and which show. Label F1 and F2 ideas
if both are in.]

1. HEADLINE IN CAPS THAT JEFF WILL UNDERSTAND

[The pitch paragraph. See below.]

Coverage:
- Source, date (what it shows, with the view count if it's a video): link
- Source, date (one detail): link
- Source, date (one detail): link

Potential Packaging:
- Title option one
- Title option two
- Title option three

2. NEXT HEADLINE
...

[Optional flag lines.]

[Recommended order and one sentence of why.]

[Sender's first name]
```

## The pitch paragraph

Two modes. Default to the paragraph; use the one-sentence mode when the user
asks for it or hands you an example written that way.

**Paragraph (default).** Three to five sentences: what the scam is, the single
best detail, the news peg with its date, why it's ours. Somewhere in it, the
viewer advice in one line (Ryan: "Jeff will just want to know what the advice to
viewers is"). **End with prior coverage**, in plain words: "Never on our
channel." / "We touched it as a B story in April; nothing since."

**One sentence.** Headline kept; the paragraph compressed to one sentence that
carries the scam, the peg and the date. Prior coverage then goes in a flag line.

Either way: no hype in the body. The hype lives in the titles. Every figure and
date in the paragraph must appear in a Coverage source below it. If the sexiest
part is an inference, it goes in a flag line, not the paragraph.

## Coverage

3–5 bullets, `- ` (or `* `). **At least one competitor video with its view count,
and at least one news or agency source from the last six weeks.** Put the one
detail each source is there for in a parenthetical before the colon.

Every link opened and every date confirmed. YouTube search results don't show
upload dates and a "trending" clip is often a year old: confirm with
`scripts/video_info.sh VIDEO_ID` where yt-dlp is available, otherwise from the
page itself. Never a constructed URL, never a search-results page. Say which
links you couldn't verify.

## Potential Packaging

Exactly three titles, in the channel's pattern (`producer-kit/titles.md`): two
halves joined by an em dash, 2–4 words in caps, `THIS` hiding the reveal, the
viewer in it. No victim or suspect names. A title can sell hard but cannot state
a fact the Coverage doesn't support; a dollar figure in a title needs a source.
Frame it as broadly as the cases (`STORE`, not `MALL`, unless every case was
in a mall), and build the dollar figure on a loss that happened, not a near-miss
(`COST HER`, not `ALMOST COST HER`, when you have both).

## How many stories

Four or five A options when pitching A stories (Jeff, Sept 28: "Kyle & David
need to provide more options each week. Not just a few."). A slate email for an
approved show can be shorter. Every A option must be a scam with a villain,
broad enough for the whole audience, and big enough to carry the show. Deals
stories go to Friday. See `producer-kit/jeff-and-ryan-rules.md`.

## Flag lines (optional)

Plain sentences, `Flag on #N:` / `One flag on #N:`, after the last story and
before the recommendation. Use them for: prior coverage when the one-sentence
mode leaves no room, an audience-frame note (the data skews younger than our
viewer), a load-bearing inference, a footage gap, an unsourced title figure, a
calendar collision. No flags, no flag lines.

## The close

Your recommended order and one sentence of why ("My pick is #1 for the A. It has
the most views behind it, it's our exact audience, and the NJ report gives us a
fresh peg."). Then the sender's name. Write in the sender's own voice; keep the
structure.

## What does not go in the email

Timecodes, outcues, confidence ratings, the verification block, open questions,
contract or business matters, caller names or numbers (caller IDs only).

## Before handing it over

Save as `pitch_email.txt` and run
`python3 scripts/check_pitch_email.py pitch_email.txt` (add `--one-sentence` in
that mode). Fix every ERROR. Paste in chat as a plain-text code block and stop.

## The WhatsApp version

For a fast gut check with Ryan before the email: `producer-kit/whatsapp-pitch.md`
and the example in `examples/whatsapp-pitch-2026-09-18.md`. One link per story,
lead with views, flag the weak one yourself, end with a one-line question.
