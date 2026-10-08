# 10/14 V3 clip verification (10/8)

rossen-pipeline Checkpoint 0 + Steps 5–6 only (no search).

## Checkpoint 0
- Deps: rossen_harvest OK, yt-dlp 2026.08.19, faster-whisper OK, ffmpeg OK, Brave key HTTP 200.
- YouTube search OK. YouTube captions BOT-WALLED. YouTube media BLOCKED.
- Spaced retry (5 min, normal fetch_many path): Inside Edition still walled; media still blocked. One mweb attempt: page loads (title, 147 s, 9/30), no caption tracks.
- Clips 1–3 verified against captions cached by the 10/7 run (real rung-1 fetch, `transcripts.json`).
- WMBF (Arc Publishing) metadata and media reachable → Whisper (rung 2). TikTok refused at page request → rung 3.

## Per clip (V3 numbering)

| Clip | Source | Rung | Bible | Verdict | Recommended |
|---|---|---|---|---|---|
| 1a | First Coast News 3iz8G25Taxg | 1 | 0:42–0:58 "DIDN'T TELL ANYBODY" | **In clips "What's" (~0:41.8); out lands mid "I didn't tell her. Didn't tell anybody" (0:56.6–0:59.9)** | **0:39–1:00**. In on daughter: "Um, she didn't want to tell anybody." Out "DIDN'T TELL ANYBODY", before "Taylor bought" |
| 1b | same | 1 | 2:10–2:21 "WHAT WAS HAPPENING" | **In lands on sentence tail "...of dollars"; out ~1 s early (phrase ends ~2:22)** | **2:09–2:22**. In "Sure enough, they cost thousands of dollars. But Taylor claims…" |
| 2a | KOIN 6 VaEws6itP08 | 1 | 0:32–0:48 "BH28 SKINCARE CONSULTANTS" | **In lands on tail word "charges"; out at 0:48 catches "and that"** | **0:28–0:47**. In "So this store owner is now facing criminal charges. Like many women, Donna…" |
| 2b | same | 1 | 2:22–3:11 "BANK TELLER CALLED POLICE" | **In lands mid-sentence ("…into her nearby bank")**; out matches | **2:20–3:11**. In "Court records say he asked her to go into her nearby bank…" |
| 3a | WSMV Short 3EzgKCWb83Q | 1 | 0:39–1:11 "DEAD FOR 3 DAYS" | Matches. In is a clean speaker change; 2–5 s earlier lands mid-sentence | Keep 0:39–1:11 |
| 3b | same | 1 | 1:43–2:22 "THIS IS MY DAD'S HOUSE" | **In lands on VO tail "…confrontation"; out may clip "house" (~2:22.5)** | **1:44–2:23**. In "Where is all of my father's things?" |
| 4 | WMBF arrest pkg 9/30 / WMBF 8/27 | 2 | bodycam, "LOOK INTO IT" | **NOT FOUND.** Arrest pkg is a 34 s anchor reader (site metadata says 5:38; the actual media is 34 s): mugshot, POA doc, house. 8/27 page is 6 s of Nora's phone video ("Oh my god! Everything is gone!" + an f-bomb). No bodycam, no neighbor, no "senior services" | Needs a manual pull. Inside Edition is the untested candidate |
| 5 | Inside Edition -a000I1ww7c | 3 | walkout with sound? | **UNVERIFIED**: captions + media blocked | Keep WMBF jail b-roll |
| 5 | WMBF jail release 9/29 | 2 | 0:00–0:14 BROLL | Confirmed: media is 14.9 s, no speech; frames show Smalls walking to a silver SUV outside the detention center | Keep 0:00–0:14 BROLL |
| 6 | CBS Miami | – | – | Not in this request; not checked (news-site, still unverified) | – |
| 7 | TikTok @amandabainum457 | 3 | "YOU SAW WHAT IT RUNG UP AT" | **UNVERIFIED**: TikTok refused page request | Pull manually and confirm |
| 8 | TikTok @james_wrigg | 3 | in/out blank | **UNVERIFIED**: TikTok refused page request | Set in/out manually |

## Editorial flags from transcripts
- Clip 3b already plays police arriving (1:55 VO: "when Conway police arrived, officers saw the deed… treated her and her partner as the ones trespassing") and Nora: "they put me and my partner in handcuffs immediately." The bible's next lines ("SHE WAS THE ONE IN HANDCUFFS" / "THEN THE POLICE SHOWED UP" / "THE CAREGIVER SHOWED POLICE THE DEED") repeat it. Option: out at **1:55 "I GOT A DEED"** and let Jeff tell the police beat.
- The clip says "trespassing"; the bible says "booked on burglary" (WMBF). Viewers hear both.
- With no bodycam, clip 4's setup ("THE OFFICERS' BODY CAMERAS WERE ROLLING… A NEIGHBOR WALKED UP") has nothing to pay off.
