# Beat yield log

Appended every pipeline run, every beat — not just failures. The point is to
learn which roles/orientations reliably yield an airable clip and which are
structural dead ends, so the bible can be written toward what sources exist.

Columns: run · beat · role · orientation · outcome · why / source
Outcomes: PICK (verified outcue) · LOCATED (case found, no caption-able source)
· SWAP (needs script change) · EMPTY (nothing cleared the bar)

## Run F2_07292026 (AI voice-clone / agency impersonation / back-to-school)

| Beat | Role | Or. | Outcome | Why / source |
|---|---|---|---|---|
| F2b-b01 | victim_interview | H | LOCATED | Del Mastro $5,400 case on ABC7 SF (news_web); no captioned YT twin |
| F2b-b02 | explainer_demo | H | PICK (swap) | FOX4 Dallas gMXuQ4MusPk 2:00-2:12 "it's my voice artificially generated" (Greg Bull/Noviello; script rewritten off Dickherber) |
| F2b-b03 | victim_interview | H | PICK (swap) | KATU sPIIFyPyKKE 1:37-2:30 "It's your child" (Tina/Hillsboro $2,500; reframed from raw-audio to recount) |
| F2b-b04 | authority_report | H | LOCATED | Olathe PD kids-voice case on KMBC/KCTV (news_web); no captioned YT twin |
| F2b-b05 | victim_interview | H | LOCATED | Schildhorn on FOX29/CNN (news_web); YouTube only AI-slop reposts |
| F2b-b06 | victim_interview | H | PICK | WFLA As4nS5aOVnw 0:38-1:02 "so she gave it to them" (Brightwell $15K, exact) |
| F2b-b07 | authority_report | H | EMPTY | IC3 alert I-072026-PSA (5 days old); only generic FBI-scam packages |
| F2b-b08 | evidence | V | EMPTY | No fake-IC3-site/deepfake-official screen recording (vertical evidence) |
| F2b-b09 | authority_report | H | PICK | WPRI rkZMNuoNfqA 1:25-1:48 "deposit money into a Bitcoin ATM" (fit: not agent/badge angle) |
| F2b-b10 | authority_report | H | PICK | WCNC JUbuCpPGX3g 0:27-0:55 "the S standing for secure" (fit: not IRS-CI specific) |
| F2b-b11 | evidence | V | EMPTY | No nurse/coach/tuition scam-text screen recording (vertical evidence) |
| F2b-b12 | explainer_demo | H | EMPTY | No Target Circle barcode-scan demo (KPRC hit = boarding-pass barcodes) |

**Yield:** 5 PICK (incl. 2 approved swaps) / 3 LOCATED / 4 EMPTY of 12.
**Pattern:** vertical `evidence` 0/2 (both empty) — worst category, again. Named
victims frequently source only to news_web (no captions) — LOCATED, not PICK.
`authority_report` on <2-week-old federal alerts (b07) too new for captioned video.
Brave news_web leg was decisive: b02/b01/b04/b05/b06 exact cases surfaced only there.

## Run F2_07292026_TOPSTORIES (utility impostor / bed rail recall / hidden cameras / FTC refunds)

Wednesday, 12 beats. Second, unrelated script in the same F2 07/29 slot — the
earlier F2_07292026 run is a different episode, not a prior attempt at this one.

| Beat | Role | Or. | Outcome | Why / source |
|---|---|---|---|---|
| F2t-b01 | victim_interview | H | PICK | ABC13 mwHYj6Pn8R8 butt-cut 0:55-1:47 + 2:03-2:33 "him in jail" (Marge Vlasak, exact, both halves in one package) |
| F2t-b02 | authority_report | H | PICK | WJLA i8ie5dvEge0 0:37-1:18 "Last year, a victim lost $18,500" (carries the Ellis never-come-inside soundbite) |
| F2t-b03 | authority_report | H | PICK | KPRC WxR6-ycJwaQ 1:20-1:43 ERCOT line (manual captions; caption garbles "does not send") |
| F2t-b04 | evidence | V | PICK (orientation ruling) | WXYZ e_Zo3DGvQ04 0:23-0:37 doorbell audio intact; horizontal carrier of vertical footage, needs crop ruling |
| F2t-b05 | confrontation_bust | H | PICK | NBC10 Y-Pvm6nJp3o 0:33-1:41 "I am glad you got these people" (64s, on the aired median) |
| F2t-b06 | explainer_demo | H | PICK (swap) | Local 4 WTdnsIZrXMs butt-cut; exact 2018 ABC13 package exists but news_web only |
| F2t-b07 | evidence (b-roll) | H | PICK (picture only) | Vive Health fGnZjq0Beq4 3:56-4:20 + 4:42-5:12; manufacturer's own install video, correct model line |
| F2t-b08 | authority_report | H | PICK (fit caveat) | Channel 3000 oJRrtg56X5s 0:02-0:23; covers the FEBRUARY recall, not the March 122,000/two-deaths one |
| F2t-b09 | authority_report | H | PICK | CityNews If_wgxWojR0 0:08-0:48; exact case but a reader, no soundbite anywhere in the market |
| F2t-b10 | victim_interview | H | PICK | WMTV fNxPpoMBK0M 0:47-1:25 "got on cameras" (Faust on camera, exact) |
| F2t-b11 | confrontation_bust | H | PICK (swap) | WKYC Lix_CaVtAHo butt-cut; defendant + victim's mother, no sheriff — cued line points at the wrong speaker |
| F2t-b12 | authority_report | H | EMPTY | No broadcast video of the Hopper FTC settlement on any captioned platform; result space is refund-tutorial slop |

**Yield:** 11 PICK (incl. 2 approved-pending swaps) / 0 LOCATED / 1 EMPTY of 12.
Best yield recorded in this log; the prior run was 5 PICK / 3 LOCATED / 4 EMPTY.

**Patterns.**
1. A dedupe defect, not sourcing, caused most of the previous run's LOCATED
   rows. Pass-2 fuzzy-title dedupe was platform-blind and preferred the earliest
   upload, so a station's caption-less website page beat its own captioned
   YouTube upload of the same package. Fixed in `dedupe.py` this run; re-running
   off cache recovered 18 captionable twins and turned b01/b02/b03/b10 from
   would-be LOCATED into PICK. Re-read old LOCATED rows with suspicion.
2. Sourcability at Checkpoint 1 was wrong on two beats in the pessimistic
   direction: b07 scanned as `none` and b08 as `commentary_only`, and the full
   multi-register search found usable footage for both. Two ad-hoc probe queries
   are not enough to declare a beat dead — the scan should run the generated
   anchor register, not improvised strings.
3. Over-specified proper nouns kill recall. "hidden cameras Verona Airbnb
   outlet" returned zero; the case-shaped "hidden cameras bathroom outlets
   Madison Airbnb rental" returned the exact package at rank 1. Same failure on
   b01. The producer's inline SEARCH REGISTER hints lost to generated queries
   for exactly this reason.
4. `authority_report` was the most common role (5 of 12) and yielded 5 PICKs,
   but three are readers with no soundbite (b08, b09, and b02's shorter
   carriers). Recall-era beats source reliably; they just do not source *voices*.
5. Vertical `evidence` still does not source natively — 0 for 1 again, same as
   the prior run's 0 for 2. Three runs of evidence now say the same thing: if a
   beat is typed VERTICAL and the artifact is police- or third-party-released,
   expect a horizontal carrier and plan the crop, rather than expecting a
   native vertical post.
6. One Short (Lix_CaVtAHo, 71s) won a horizontal beat, confirming the query
   generator's note that Shorts should run on every orientation.
