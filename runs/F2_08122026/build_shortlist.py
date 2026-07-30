import json
def c(url, st, score, dur, up, reason, cd, promoted=False, plat="youtube"):
    return {"url":url,"platform":plat,"source_type":st,"score":score,"duration":dur,
            "uploader":up,"reason":reason,"cannot_determine":cd,
            "diversity_floor_promoted":promoted}

SL=[]
def beat(bid, cands, mix, floor, short_reason=None, notes=None):
    o={"beat_id":bid,"pass":1,"candidates":cands,"source_mix":mix,
       "diversity_floor_applied":floor}
    if short_reason: o["short_of_five_reason"]=short_reason
    if notes: o["notes"]=notes
    SL.append(o)

# ---------------------------------------------------------------- b01/b02/b03
# One InvestigateTV+ package carries all three beats (script marks b02/b03 BUTT FROM B01).
IT_YT = "https://www.youtube.com/watch?v=LZoQ5aiVibA"
IT_WEB= "https://www.investigatetv.com/2026/01/23/ai-voice-cloning-scams-target-families-with-fake-kidnapping-calls/"
IT_WCAX="https://www.wcax.com/video/2026/01/21/investigatetv-how-ai-voice-cloning-scams-target-families-with-fake-kidnapping-calls/"

beat("F2c-b01",[
 c(IT_YT,"affiliate",90,442,"InvestigateTV",
   "Exact package the script cites (InvestigateTV+ 01-23-26), on a real channel with a back catalog. Title matches the beat verbatim.",
   ["whether Rachel's recorded call audio is actually played in-package or only described"]),
 c(IT_WEB,"affiliate",76,441,"InvestigateTV",
   "Same package on the originating site, dated 01-23-26 exactly as the script says. No caption track on a news_web page.",
   ["no captions on news_web — cannot verify an outcue from this copy"],plat="news_web"),
 c(IT_WCAX,"affiliate",64,1335,"WCAX",
   "Affiliate carriage of the full InvestigateTV+ weekend show; the segment is inside a 22-minute block.",
   ["where in the 22 minutes the Rachel segment sits"],plat="news_web"),
 c("https://www.youtube.com/watch?v=ruNDY0OBpg4","network",50,539,"CNN",
   "Different case (Arizona/DeStefano). Strong tape, wrong victim — kept only so pass two has a fallback if the exact package fails.",
   ["nothing metadata can settle; this is a fit rejection waiting to happen"]),
 c("https://www.youtube.com/watch?v=84gYLF2r2lo","affiliate",46,206,"KSDK News",
   "St. Louis County mom, AI kidnapping scam — right state, wrong person. Fallback only.",
   ["whether the KSDK mother is in fact Rachel under a different framing"]),
],{"affiliate":4,"network":1},False,
 notes="Diversity floor did NOT fire: 4 affiliate + 1 network is a monoculture by the rule, but no creator_short/first_person/raw_footage candidate cleared the hard filters for this specific case. Shipping five affiliates/network rather than reaching past a filter for filler.")

beat("F2c-b02",[
 c(IT_YT,"affiliate",84,442,"InvestigateTV",
   "The Dickherber voice-clone demo lives inside this same package. Script marks the beat BUTT FROM B01, so one source, two segments.",
   ["whether the demo is on camera with the reporter's reaction, or narrated over b-roll"]),
 c("https://www.investigatetv.com/2026/04/20/deepfake-scams-infiltrate-social-media-voice-cloning-becomes-easier/","affiliate",58,307,"InvestigateTV",
   "Later InvestigateTV deepfake/voice-cloning piece. Same unit, different demo — usable if the January demo is thin.",
   ["whether it contains an on-camera cloning demo at all"],plat="news_web"),
 c("https://www.investigatetv.com/2025/12/18/experts-issue-warning-about-ai-voice-clone-scams/","affiliate",54,124,"InvestigateTV",
   "Two-minute warning piece. Short for a demo but same franchise.",
   ["whether an actual demo occurs in 124s"],plat="news_web"),
 c("https://www.youtube.com/watch?v=y2vwV1XhLN8","affiliate",50,142,"KSDK News",
   "St. Louis affiliate on AI voice cloning — Dickherber's own market. Plausible she appears.",
   ["whether Dickherber is the expert in this one"]),
 c("https://www.youtube.com/watch?v=yxFMjTaiLOY","network",44,191,"Good Morning America",
   "GMA warning package. Network studio framing is weak for a demo beat.",
   ["whether any hands-on demo happens vs anchor narration"]),
],{"affiliate":4,"network":1},False,
 notes="Same monoculture note as b01. No creator_long clone-demo candidate survived the AI-slop filter — voice-cloning demos are a heavily slopped topic on YouTube.")

beat("F2c-b03",[
 c(IT_YT,"affiliate",86,442,"InvestigateTV",
   "Third segment off the same package: Rachel on law enforcement and the death threats. BUTT FROM B01.",
   ["whether the threats and the 'overseas cybercrime' line are both in the cut"]),
 c(IT_WEB,"affiliate",72,441,"InvestigateTV",
   "Originating-site copy of the same package.",
   ["no captions on news_web"],plat="news_web"),
 c(IT_WCAX,"affiliate",60,1335,"WCAX",
   "Full-show affiliate carriage.",
   ["segment position inside the 22-minute block"],plat="news_web"),
 c("https://www.youtube.com/watch?v=U7pT99zQAhc","affiliate",42,242,"ABC7 News Bay Area",
   "Scammer death threats to a California teen — right emotional beat, wrong case and wrong scam type.",
   ["nothing; this is a fit rejection"]),
 c("https://www.youtube.com/watch?v=Jes1WTv1ke0","affiliate",40,157,"WPXI-TV Pittsburgh",
   "Threatening messages in a phone scam targeting a local family. Wrong case.",
   ["whether any victim appears on camera"]),
],{"affiliate":5},True,
 notes="Diversity floor FIRED and could not promote: no non-affiliate candidate cleared the hard filters. Shipping five affiliates and saying so, per the 'it promotes, it never invents' limit.")

# ---------------------------------------------------------------- b04
beat("F2c-b04",[
 c("https://www.youtube.com/watch?v=qn9N9KQHY1s","affiliate",89,119,"ABC7",
   "The exact Del Mastro case on the originating affiliate (KGO/ABC7 SF), on YouTube with a caption track. Recovered by re-querying the beat after the first pass missed it.",
   ["whether Del Mastro is named on screen and whether the $5,400 figure is spoken"]),
 c("https://abc7news.com/post/bay-area-mom-thousands-scammers-use-ai-mimic-daughters-voice-fake-kidnapping-part-growing-trend/","affiliate",74,None,"ABC7 San Francisco",
   "The written/video post of the same story, 05-24-26. Prior run F2_07292026 located this exact URL.",
   ["no captions on news_web"],plat="news_web"),
 c("https://www.youtube.com/watch?v=xh_5ryQODZc","affiliate",52,106,"ABC 7 Chicago",
   "Different mom, same scam shape. Fallback only.",
   ["nothing; fit rejection"]),
 c("https://www.youtube.com/watch?v=FWrt7EMH8KI","affiliate",48,254,"Arizona's Family (3TV/CBS5)",
   "Scottsdale mom AI voice clone. Wrong case.",
   ["nothing; fit rejection"]),
 c("https://www.youtube.com/watch?v=qkFC6xgBQCI","affiliate",22,118,"DanRH Drum Channel",
   "REJECT ON FILTER: GMA interview with Del Mastro re-uploaded to an unrelated drum channel. Correct case, but it is an aggregator repost — clearance problem, and the original wins on upload date.",
   ["nothing; hard-filtered as a repost"]),
],{"affiliate":5},True,
 notes="Diversity floor FIRED, no eligible promotion. Note the fifth entry is retained as a documented hard-filter rejection, not a peer.")

# ---------------------------------------------------------------- b05
beat("F2c-b05",[
 c("https://www.youtube.com/watch?v=4vLlIbdwNhY","creator_long",85,317,"The Select Committee on China",
   "Erin West on the record about the scamdemic, 5 minutes, captioned, named lower-third. Right length for a one-minute pull.",
   ["whether the anxiety/action/money test is stated in this cut"]),
 c("https://www.youtube.com/watch?v=N0QwVkN0tDY","creator_long",70,1134,"Operation Shamrock",
   "Her own org's 2026 Blueprint talk. Nineteen minutes — the moment will be buried but it is definitely in there.",
   ["where the three-signal test sits in 19 minutes"]),
 c("https://www.youtube.com/watch?v=ngvdrDuaNRs","creator_short",62,75,"Chainalysis",
   "75-second cut of West on pig butchering. Tight, but likely off-topic from the voice-clone framing.",
   ["whether voice cloning is mentioned at all"]),
 c("https://www.youtube.com/watch?v=kh4ucNfKr9c","creator_long",48,3773,"Asset Reality",
   "63-minute podcast. Over the 20-minute ceiling; demoted hard per the duration rule.",
   ["nothing worth the transcript budget at this length"]),
 c("https://www.youtube.com/watch?v=Na9EvGe7hg8","creator_long",44,3534,"AARPMaine",
   "59-minute webinar. Same ceiling problem.",
   ["nothing"]),
],{"creator_long":4,"creator_short":1},False,
 notes="No affiliate candidate at all here — inverse of the usual mix. explainer_demo's natural source type IS creator_long per the grader's role table, so this scores at the top of the range rather than as a degraded affiliate.")

# ---------------------------------------------------------------- b06
beat("F2c-b06",[
 c("https://www.kmbc.com/article/olathe-police-warn-scam-child-abduction-money/70238283","affiliate",78,None,"KMBC 9 News",
   "The exact case: Olathe PD warning on the child-abduction ransom scam, dated 02-03-26 — matches the script's cited date precisely.",
   ["no captions on news_web; whether a police spokesperson appears on camera"],plat="news_web"),
 c("https://fox4kc.com/news/olathe-families-receive-kidnapping-ransom-call-police-warn-of-new-phone-scam/","affiliate",72,None,"FOX4KC",
   "Same case, same date, second Kansas City affiliate. Independent copy if KMBC's video is unusable.",
   ["no captions; whether it carries video or is text-only"],plat="news_web"),
 c("https://www.youtube.com/watch?v=BpFMz_qE-Eo","affiliate",40,134,"KSHB 41",
   "Olathe PD scam warning, but the department-impersonation scam, not the AI-voice kidnapping one. Wrong case.",
   ["nothing; fit rejection on case"]),
 c("https://www.youtube.com/watch?v=PIjb21ahu4w","affiliate",34,43,"KMBC 9",
   "Olathe PD utility phone scam. Wrong case and under the 25s-usable threshold for anything but evidence.",
   ["nothing"]),
 c("https://www.kctv5.com/2025/03/26/olathe-police-release-additional-information-suspicious-man-after-incident-arrest/","affiliate",28,188,"KCTV",
   "KCTV Olathe coverage, unrelated incident. Retained only because the script names KCTV as the source outlet.",
   ["whether KCTV has an unindexed 02-03-26 package"],plat="news_web"),
],{"affiliate":5},True,
 notes="Diversity floor FIRED, nothing to promote. ZERO YouTube candidates mention Olathe at all — the entire beat lives on news_web, matching the prior run's LOCATED verdict for the same department.")

# ---------------------------------------------------------------- b07 manual
beat("F2c-b07",[
 c("https://www.tiktok.com/@pearlmania500/video/7220912200855178538","creator_short",92,None,"@pearlmania500",
   "MANUAL LANE. The native post itself: 'Literally billions of unclaimed funds in every state. Go get your money' — the script's line, verbatim, from the creator it names. This is the pick; it is not graded against reposts.",
   ["view count and exact runtime are not exposed via search; no caption track on TikTok"],plat="tiktok"),
],{"creator_short":1},False,
 short_reason="Manual lane. source_native is tiktok and the script says 'have a look at the one that set it all off' — the artifact is a specific self-posted video, so there is no candidate set to rank. Searching for a repost to grade would be the wrong outcome, not a thorough one.")

# ---------------------------------------------------------------- b08
beat("F2c-b08",[
 c("https://www.youtube.com/watch?v=C2J_wnqMlIo","affiliate",91,144,"FOX 5 Washington DC",
   "The exact package the script names: \"Virginia's treasury flooded with unclaimed money requests, thanks to TikTok | FOX 5 DC\". 144s, captioned. Found by direct search; the harvest's YouTube leg missed it.",
   ["whether Bradley Earl is the official interviewed on camera"]),
 c("https://www.fox5dc.com/news/virginias-treasury-flooded-with-unclaimed-money-requests-heres-how-you-can-make-a-claim","affiliate",70,None,"FOX 5 DC",
   "Originating article for the same package. Dated 2023-04-25 — see the recency note in the report.",
   ["no captions on news_web"],plat="news_web"),
 c("https://www.youtube.com/watch?v=xk1bXTXbsbg","affiliate",56,237,"ABC 7 News - WJLA",
   "DC/Virginia unclaimed money package, $3.8 billion figure. Same region, no TikTok angle.",
   ["whether the TikTok-driven surge is mentioned"]),
 c("https://www.youtube.com/watch?v=-9usnea9ToE","affiliate",50,485,"WTKR News 3",
   "Virginia unclaimed-property accountability piece. Eight minutes, investigative rather than the spike story.",
   ["whether the claims surge is covered"]),
 c("https://www.tiktok.com/@deesale00/video/7324107480701717803","creator_short",44,None,"@deesale00",
   "DIVERSITY FLOOR PROMOTION. Creator telling followers to search the VA treasurer site — the demand side of the same story, and the only non-affiliate that cleared the filters.",
   ["runtime, audio quality, whether the person is on camera"],promoted=True,plat="tiktok"),
],{"affiliate":4,"creator_short":1},True,
 notes="Diversity floor fired and successfully promoted @deesale00 over a fifth affiliate. Note the promoted candidate scores 47 points below the top affiliate — it is not a peer.")

# ---------------------------------------------------------------- b09
beat("F2c-b09",[
 c("https://www.tiktok.com/@abc7chicago/video/7464824143582629150","creator_short",46,None,"@abc7chicago",
   "ABC7 Chicago's own vertical TikTok on Illinois unclaimed funds — the vertical cut the script's DECIDE marker asks about. But the caption is the Treasurer urging people to check, NOT the Udvance claim-denial story.",
   ["whether Udvance appears; whether this is a different story entirely"],plat="tiktok"),
 c("https://abc7chicago.com/post/illinois-treasurer-michael-frerichs-urges-residents-check-missing-money-unclaimed-cash/","affiliate",40,None,"ABC7 Chicago",
   "ABC7 Chicago on I-CASH, right outlet and right program, wrong story — promotional rather than the denial.",
   ["no captions; whether an I-Team denial package exists unindexed"],plat="news_web"),
 c("https://www.youtube.com/watch?v=WyPHkNcAYWM","affiliate",30,610,"FOX 32 Chicago",
   "Illinois Treasurer I-CASH auction. Same program, unrelated angle.",
   ["nothing; fit rejection"]),
 c("https://www.youtube.com/watch?v=zjX1K7Cv64M","affiliate",26,250,"Local 4 News WHBF",
   "ICash telethon. Wrong angle.",
   ["nothing"]),
 c("https://www.nbcchicago.com/news/local/what-is-i-cash-what-to-know-about-illinois-missing-money-program-and-how-to-search/3585214/","affiliate",24,None,"NBC Chicago",
   "Explainer on how to search I-CASH. No victim, no denial.",
   ["nothing"],plat="news_web"),
],{"affiliate":4,"creator_short":1},True,
 notes="Susan Udvance returns ZERO video coverage across the original harvest and a targeted re-query. Brave surfaces only her LinkedIn/ZoomInfo as a Chicago real-estate advisor, which corroborates the West Loop escrow detail but is not footage. Nothing here scores near 55 on fit — expect flagged: null.")

# ---------------------------------------------------------------- b10 (gated)
beat("F2c-b10",[
 c("https://www.youtube.com/watch?v=OxRedGsy-Ug","affiliate",68,1074,"CBS Boston",
   "'13 charged with scamming hundreds of grandparents' — full news conference, matches the script's DECIDE note on the count. 18 minutes, so the usable moment needs finding.",
   ["whether any AI-voice angle is mentioned, which is the script's stated doubt"]),
 c("https://www.youtube.com/watch?v=KzMxcmF5ng4","affiliate",64,141,"WJZ",
   "13 Canadians charged in the grandparent scam investigation. Tight 141s cut of the same count.",
   ["whether it is the same indictment as the DOJ one the script cites"]),
 c("https://www.youtube.com/watch?v=oF0Z-W4CUpI","affiliate",52,155,"KFOR Oklahoma's News 4",
   "Two arrested preying on elderly Oklahomans. Different case, same crime family.",
   ["nothing"]),
 c("https://www.youtube.com/watch?v=msFwnkXF-T0","affiliate",50,167,"WCAX-TV",
   "Cross-border Canadian arrests in a grandparent scam.",
   ["nothing"]),
 c("https://www.youtube.com/watch?v=7uB0tMldnlo","affiliate",42,111,"WFMY News 2",
   "Grandparent scam targeting seniors, warning rather than bust.",
   ["whether any arrest footage appears"]),
],{"affiliate":5},True,
 notes="Producer-gated beat. Diversity floor fired with nothing to promote. Sourcability is fine; the risk the script itself names is FIT — none of these is an AI-voice-cloning prosecution, because there isn't one on video.")

json.dump(SL, open("shortlist.json","w"), indent=1)
print(f"wrote {len(SL)} beat shortlists, {sum(len(b['candidates']) for b in SL)} candidates")
