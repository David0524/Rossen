# Review loop — W_11042026 (11/04 F2)

Reviewer: rossen-bible-final-reviewer, BLOCKER-only, background agent, 10/28/2026.

## Round 1 — 2 BLOCKERs, both fixed

1. **Delaware stock timing (CONTRADICTED).** The tease and the clip-5 button said the stock was worth 100K+ when it was sold. It sold for about $8,000 (2008) and was worth 100K+ when he tried to cash out (CBS clip 5 captions ~2:15–2:23; NPR Planet Money, Feb 2020).
   - Tease: "…FOR 8 THOUSAND DOLLARS… WHEN IT WAS WORTH MORE THAN 100 THOUSAND!!" → "…FOR 8 THOUSAND DOLLARS…" / "-BY THE TIME HE FOUND OUT, IT WAS WORTH MORE THAN 100 THOUSAND!!"
   - Button: "FOR STOCK WORTH MORE THAN 100 THOUSAND" → "BY THE TIME HE FOUND OUT, IT WAS WORTH MORE THAN 100 THOUSAND"
2. **Story C had no protection header after its clips (mechanical).** Added `**HERE'S HOW TO PROTECT YOURSELF**` above the takeaways after clip 11 (refund depends on billing; primary member only). Copy unchanged.

Also fixed (a timing error in the outline's own pick, raised as reviewer W6): clip 6's out moved 1:11 → 1:14. "we will" ends at 1:11; "defend this litigation vigorously" runs 1:11–1:14 (Whisper, abc_gma_dg). Mirrored in outline.md, picks.json, clips/manifest.json and SOURCE_LOG.md.

## Round 2

The changed lines were re-checked by the writer against clip 5's captions and the abc_gma_dg Whisper transcript, not by a second reviewer agent: consistent. `check_bible.py`: no errors.

## Still blocking

None.

## WARNINGs and NOTEs passed to the producer (not fixed)

- W1 "ALLEGEDLY" off-register (kept: the Delaware sale is an allegation).
- W2/W3 three sound clips with no takeaway between them (from line 71, from line 294).
- W4 six lines over 16 words. W5 figures with nothing on screen.
- W7 clip 5's slices start mid-sentence (2:09 "Brown's stadium", 2:56 "we're going to fix it"); its out may clip "unclaimed funds".
- W8 clip 4's third slice starts mid-sentence at 2:32.
- W9 the Delaware man can be named: Walter Schramm (Schramm v. Mayrack, D. Del. 1:22-cv-01443); sale was 2008, so not dated on air; no Delaware response line.
- W10 NY "LAST MONTH… SENT SECRET SHOPPERS": the release (Oct 15, 2026) dates the announcement, not the shopping.
- W11 "A FORMER EMPLOYEE IS HERE TO TELL YOU" sounds like an in-studio guest; she's in a 2022 clip.
- W12 Lori complained to the Oklahoma AG (per More Perfect Union and filings); she's also a named plaintiff (Hartline v. Dollar General, E.D. Okla.).
- W13 Costco Auto exclusions: oil changes and tires are confirmed excluded (also air bags, state inspections); update the JEFF note.
- N1 no clip visually confirmed. N2 Delaware figure in tease and body. N3 13 JEFF notes. N4 Barbara was 88 in Sept 2025. N5 the WHIO manager exchange is undated (report Nov 2022). N6 Lori's overcharges are from 2023 (video March 2024). N7 "lawmakers from both parties" is a federal bill (Liccardo, Lawler), not California. N8 "most members never use" has no source.
