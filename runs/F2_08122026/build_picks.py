import json, sys
sys.path.insert(0,"/home/user/Rossen/harvest")
from rossen_harvest.transcripts import Transcript, Cue

T=json.load(open("transcripts.json"))
def tr(vid):
    r=[v for v in T.values() if v.get("video_id")==vid][0]
    return Transcript(vid,[Cue(**c) for c in r["cues"]],r["source"])

from rossen_harvest.transcripts import PAD_IN
BACK = 6.0   # how far back to hunt for a sentence boundary ahead of the moment

def _starts_sentence(txt):
    s = txt.strip()
    if s.startswith(">>"):          # speaker change in auto-captions
        return True
    return bool(s) and s[0].isupper()

def seg(vid, a, b):
    """Return {in,out,outcue}.

    In-point: walk back from `a` to the nearest cue that actually begins a
    sentence or a speaker turn, then lead it by LEAD seconds so the clip does
    not start mid-clause. transcripts.PAD_IN adds a further second.
    Out-point: segment() supplies the outcue verbatim from the cue at/before
    the out point; find() then re-verifies the phrase is really in the tape.
    """
    t=tr(vid)
    idx=[i for i,c in enumerate(t.cues) if c.start<=a]
    if idx:
        i=idx[-1]
        floor=a-BACK                    # never hunt a boundary more than 6s back
        j=i
        while j>0 and t.cues[j].start>=floor and not _starts_sentence(t.cues[j].text):
            j-=1
        if t.cues[j].start>=floor and _starts_sentence(t.cues[j].text):
            i=j                         # a real sentence start inside the window
        # segment() subtracts PAD_IN, so offset by it to land the reported
        # in-point exactly on the boundary cue rather than inside the clause
        # before it.
        a=max(0.0, t.cues[i].start) + PAD_IN
    i,o,outcue=t.segment(a,b)
    assert outcue, f"{vid} {a}-{b}: empty outcue"
    assert t.find(outcue) is not None, f"{vid}: outcue not verifiable: {outcue!r}"
    assert not outcue.strip().startswith(">>"), (
        f"{vid} out={b}: outcue starts a new speaker turn, out point is late: {outcue!r}")
    return {"in":i,"out":o,"outcue":outcue}

IT="LZoQ5aiVibA"; IT_URL=f"https://www.youtube.com/watch?v={IT}"
P=[]

def rank(url, st, score, tone, auth, qual, fit, segs, reasoning, flags=None):
    return {"url":url,"source_type":st,"score":score,"tone":tone,"authenticity":auth,
            "quality":qual,"fit":fit,"segments":segs,"reasoning":reasoning,"flags":flags or []}

# ------------------------------------------------------------------ b01
P.append({"beat_id":"F2c-b01","pass":2,"flagged":IT_URL,
 "platform":"youtube","title":"AI voice cloning scams target families with fake kidnapping calls",
 "source_mix":{"affiliate":4,"network":1},"diversity_floor_applied":False,
 "ranked":[
  rank(IT_URL,"affiliate",91,9,10,8,10,
   [seg(IT,63,132), seg(IT,180,223)],
   "The exact package the script cites, and it delivers everything the setup promises: Rachel on camera, the caller-ID detail, and her own recording of the call played in full. 'I know my child's voice and it sounded exactly like my child's voice that I've heard every day of my life' at 1:35 is the moment. Second segment is her real-time realization and breakdown. Butt-cut from one source, exactly as the script marks it.",
   ["auto-captions render the expert's name as 'Dick Herbert' and Wentzville as 'Wville' — cosmetic, does not affect the outcues"]),
  rank("https://www.youtube.com/watch?v=ruNDY0OBpg4","network",44,8,7,9,2,[],
   "Strong CNN tape but it is the Arizona/DeStefano case, not Rachel. Fails fit outright.",[]),
  rank("https://www.youtube.com/watch?v=84gYLF2r2lo","affiliate",40,8,7,7,2,[],
   "KSDK, right metro, wrong mother. Fails fit.",[]),
 ],
 "rejected":[
  {"url":"https://www.investigatetv.com/2026/01/23/ai-voice-cloning-scams-target-families-with-fake-kidnapping-calls/","source_type":"affiliate","score":76,"reason":"Same package, but news_web carries no caption track — no verifiable outcue. Superseded by the YouTube copy."},
  {"url":"https://www.wcax.com/video/2026/01/21/investigatetv-how-ai-voice-cloning-scams-target-families-with-fake-kidnapping-calls/","source_type":"affiliate","score":64,"reason":"22-minute full-show carriage; the segment is buried and uncaptioned."},
  {"url":"https://www.youtube.com/watch?v=Jes1WTv1ke0","source_type":"affiliate","score":38,"reason":"Wrong case."},
 ],
 "cannot_determine":["whether the recorded call audio is cleared for rebroadcast — it is the victim's own recording aired by InvestigateTV, so clearance runs through Gray"]})

# ------------------------------------------------------------------ b02
P.append({"beat_id":"F2c-b02","pass":2,"flagged":IT_URL,
 "platform":"youtube","title":"AI voice cloning scams target families with fake kidnapping calls",
 "source_mix":{"affiliate":4,"network":1},"diversity_floor_applied":False,
 "ranked":[
  rank(IT_URL,"affiliate",87,9,9,8,10,
   [seg(IT,242,289)],
   "Ann Dickherber IS in the package the script already cites — she clones reporter Lauren Trager's voice on camera and the clone says 'I'd like to talk with you about your car's extended warranty', then Trager reacts: 'It is just very frightening how quick that happened.' That is the beat's 'watch her show you how fast it happens... and watch his face', delivered almost line for line. No swap needed after all.",
   ["the reporter is a woman (Lauren Trager); the script says 'watch HIS face' and 'that reporter's OWN voice... made HIS voice say' — pronouns need a one-word fix in the bible"]),
  rank("https://www.youtube.com/watch?v=y2vwV1XhLN8","affiliate",46,8,7,8,3,[],
   "KSDK AI voice-cloning explainer, no Dickherber and no hands-on demo.",[]),
  rank("https://www.youtube.com/watch?v=yxFMjTaiLOY","network",40,7,5,8,3,[],
   "GMA warning package, anchor-led, no demo.",[]),
 ],
 "rejected":[
  {"url":"https://www.investigatetv.com/2026/04/20/deepfake-scams-infiltrate-social-media-voice-cloning-becomes-easier/","source_type":"affiliate","score":52,"reason":"Different InvestigateTV piece; no captions, and the January package already contains the demo."},
  {"url":"https://www.investigatetv.com/2025/12/18/experts-issue-warning-about-ai-voice-clone-scams/","source_type":"affiliate","score":48,"reason":"124s warning piece, no demo, no captions."},
 ],
 "cannot_determine":["nothing material — the demo is fully audible in the transcript"]})

# ------------------------------------------------------------------ b03
P.append({"beat_id":"F2c-b03","pass":2,"flagged":IT_URL,
 "platform":"youtube","title":"AI voice cloning scams target families with fake kidnapping calls",
 "source_mix":{"affiliate":5},"diversity_floor_applied":True,
 "ranked":[
  rank(IT_URL,"affiliate",89,9,10,8,10,
   [seg(IT,312,340)],
   "Third butt off the same package. The reporter asks 'What have the authorities done for you?' and Rachel answers 'Zero. Nothing.' — which is precisely the script's 'hear what she says when she is asked what anybody actually did about it.' The overseas-cybercrime line and the death threats both land inside 30 seconds.",[]),
  rank("https://www.youtube.com/watch?v=U7pT99zQAhc","affiliate",36,8,8,7,2,[],
   "Death threats, but a Bay Area teen and a different scam. Fails fit.",[]),
 ],
 "rejected":[
  {"url":"https://www.investigatetv.com/2026/01/23/ai-voice-cloning-scams-target-families-with-fake-kidnapping-calls/","source_type":"affiliate","score":72,"reason":"No caption track on news_web."},
  {"url":"https://www.youtube.com/watch?v=Jes1WTv1ke0","source_type":"affiliate","score":34,"reason":"Wrong case."},
 ],
 "cannot_determine":["nothing material"]})

# ------------------------------------------------------------------ b04
AB="qn9N9KQHY1s"; AB_URL=f"https://www.youtube.com/watch?v={AB}"
P.append({"beat_id":"F2c-b04","pass":2,"flagged":AB_URL,
 "platform":"youtube","title":"Mom loses thousands after kidnap scammers use AI to mimic daughter's voice",
 "source_mix":{"network":1,"affiliate":4},"diversity_floor_applied":True,
 "ranked":[
  rank(AB_URL,"network",88,9,9,9,10,
   [seg(AB,11,62), seg(AB,81,107)],
   "The exact Del Mastro case, field package with her on camera. Every specific in Jeff's setup is spoken on tape: the daughter Sarah, the panic-attack voice saying 'I'm so sorry, Mom. I'm so scared', the $5,400 wired to Mexico, Sarah at work the whole time. Second segment is the Navy-veteran reflection, which is the 'think about what you would do' payoff. Tagged network because it is an ABC News correspondent piece (Aaron Katersky) carried by ABC7 — but it is a field package with the victim on camera, so the 'network studio-only is weak' demerit does not apply.",
   ["script says the demand was $20,000; the package says the caller demanded she wire $5,400. See the report — this is a script-accuracy item, not a clip problem"]),
  rank("https://www.youtube.com/watch?v=xh_5ryQODZc","affiliate",44,8,8,7,2,[],
   "ABC7 Chicago, different mother. Fails fit.",[]),
  rank("https://www.youtube.com/watch?v=FWrt7EMH8KI","affiliate",42,8,8,7,2,[],
   "Scottsdale mom. Fails fit.",[]),
 ],
 "rejected":[
  {"url":"https://abc7news.com/post/bay-area-mom-thousands-scammers-use-ai-mimic-daughters-voice-fake-kidnapping-part-growing-trend/","source_type":"affiliate","score":74,"reason":"Correct case on the originating affiliate site, but no caption track. Superseded by the captioned YouTube copy — this is the LOCATED-to-PICK upgrade the prior run could not make."},
  {"url":"https://www.youtube.com/watch?v=qkFC6xgBQCI","source_type":"affiliate","score":22,"reason":"HARD FILTER: correct case, but a GMA segment re-uploaded to an unrelated drum channel. Aggregator repost — clearance problem, and the original wins on date."},
 ],
 "cannot_determine":["whether ABC7's copy or the ABC News network master is the cleaner clearance path"]})

# ------------------------------------------------------------------ b05  EMPTY
P.append({"beat_id":"F2c-b05","pass":2,"flagged":None,
 "platform":None,"title":None,
 "flagged_reason":("Nothing cleared 55 on FIT. Five Erin West sources were graded, roughly 2.5 hours of "
   "transcript in total, and none of them contains what Jeff sets up. Her House Select Committee testimony "
   "says 'I call it the scamdemic' at 2:45 but never mentions voice cloning; the 19-minute Operation Shamrock "
   "talk, the 63-minute Asset Reality podcast and the 59-minute AARP webinar return zero hits for 'anxiety', "
   "'clone' or 'cloning'. The two specific claims in the script — that a few seconds of your voice produces "
   "something that sounds exactly like you, and the anxiety-plus-immediate-action-plus-moving-money test — "
   "are not attributable to her in any sourceable footage. NOTE: the first of those lines is spoken almost "
   "verbatim by an unnamed expert at 1:10 in the b04 ABC package. The beat is sourceable only by changing who "
   "says it, which is a script decision, not a search one."),
 "better_query":"\"Erin West\" \"anxiety\" \"urgency\" scam three signs interview  — and separately: site:operationshamrock.org video anxiety action money test",
 "source_mix":{"creator_long":4,"creator_short":1},"diversity_floor_applied":False,
 "ranked":[
  rank("https://www.youtube.com/watch?v=4vLlIbdwNhY","creator_long",48,9,9,8,2,[],
   "Genuinely powerful testimony — Chris, Don, Mary, the scamdemic framing, the Cambodia compounds. But it is about transnational scam infrastructure and law-enforcement failure, not voice cloning, and it does not contain the three-signal test. Fails fit for THIS beat.",[]),
  rank("https://www.youtube.com/watch?v=N0QwVkN0tDY","creator_long",34,8,8,7,1,[],
   "19-minute Blueprint talk. Zero hits for anxiety or cloning.",[]),
  rank("https://www.youtube.com/watch?v=ngvdrDuaNRs","creator_short",30,8,7,8,1,[],
   "75s Chainalysis cut on pig butchering. No voice-clone content at all.",[]),
  rank("https://www.youtube.com/watch?v=kh4ucNfKr9c","creator_long",22,8,8,6,1,[],
   "63-minute podcast, over the ceiling, and zero keyword hits across 1,815 cues.",[]),
  rank("https://www.youtube.com/watch?v=Na9EvGe7hg8","creator_long",20,8,7,6,1,[],
   "59-minute webinar, same result across 1,394 cues.",[]),
 ],
 "rejected":[],
 "cannot_determine":["whether Erin West has said this on camera somewhere not indexed by YouTube or Brave — an Operation Shamrock media-library item without a transcript is the most likely home"]})

# ------------------------------------------------------------------ b06  LOCATED / manual
P.append({"beat_id":"F2c-b06","pass":2,"flagged":None,
 "platform":"news_web","title":"Olathe police warn of scam claiming child abduction, demanding money",
 "status":"manual_clip",
 "manual_url":"https://www.kmbc.com/article/olathe-police-warn-scam-child-abduction-money/70238283",
 "flagged_reason":("LOCATED, not empty. The exact case exists and is dated 02-03-26, matching the script's "
   "cited date — KMBC 9 carries it, FOX4KC carries it independently. Neither is on captioned YouTube, and a "
   "targeted search returned ZERO YouTube candidates mentioning Olathe at all across 619 harvested candidates. "
   "No caption track means no verifiable outcue, so per the hard rule this gets a source link and no invented "
   "timecode. The prior run reached the same verdict on the same department."),
 "better_query":"There is no better query — this is a coverage boundary, not a query miss. The Kansas City affiliates publish this story to their own sites only. Pull it by hand from KMBC or FOX4KC.",
 "source_mix":{"affiliate":5},"diversity_floor_applied":True,
 "ranked":[
  rank("https://www.kmbc.com/article/olathe-police-warn-scam-child-abduction-money/70238283","affiliate",78,8,8,7,10,[],
   "Exact case, exact date. Manual pull — no captions on news_web.",["no caption track; outcue cannot be verified"]),
  rank("https://fox4kc.com/news/olathe-families-receive-kidnapping-ransom-call-police-warn-of-new-phone-scam/","affiliate",72,8,8,7,10,[],
   "Independent second copy of the same 02-03-26 case. Backup manual pull.",["no caption track"]),
  rank("https://www.youtube.com/watch?v=BpFMz_qE-Eo","affiliate",38,8,7,8,2,[],
   "Olathe PD, but the department-impersonation scam. Wrong case.",[]),
 ],
 "rejected":[
  {"url":"https://www.youtube.com/watch?v=PIjb21ahu4w","source_type":"affiliate","score":30,"reason":"Utility phone scam, wrong case, and captions genuinely unavailable after a retry."},
  {"url":"https://www.kctv5.com/2025/03/26/olathe-police-release-additional-information-suspicious-man-after-incident-arrest/","source_type":"affiliate","score":26,"reason":"Unrelated 2025 incident."},
 ],
 "cannot_determine":["whether KCTV — the outlet the script actually names — has an unindexed 02-03-26 package; only KMBC and FOX4KC surfaced"]})

# ------------------------------------------------------------------ b07  manual native
P.append({"beat_id":"F2c-b07","pass":2,"flagged":None,
 "platform":"tiktok","title":"Literally billions of unclaimed funds in every state. Go get your money",
 "status":"manual_clip",
 "manual_url":"https://www.tiktok.com/@pearlmania500/video/7220912200855178538",
 "flagged_reason":("MANUAL LANE, and this is a real outcome rather than a gap. source_native is tiktok: the "
   "script names Alex Pearlman and says 'have a look at the one that set it all off', so the artifact is his "
   "own post. Found it — @pearlmania500, captioned 'Literally billions of unclaimed funds in every state. Go "
   "get your money', which is the script's line verbatim. Per the skill, the native post is the pick and a "
   "YouTube repost is not graded. TikTok ships no caption track, and faster-whisper is not installed in this "
   "environment, so the outcue is left UNVERIFIED rather than invented."),
 "better_query":"n/a — the permalink is in hand.",
 "source_mix":{"creator_short":1},"diversity_floor_applied":False,
 "ranked":[
  rank("https://www.tiktok.com/@pearlmania500/video/7220912200855178538","creator_short",92,9,10,8,10,[],
   "The originating post itself, from the creator the script names, carrying the script's line in its caption.",
   ["no caption track (TikTok); faster-whisper not installed — outcue UNVERIFIED","runtime not exposed via search"]),
 ],
 "rejected":[],
 "cannot_determine":["exact runtime and whether the whole clip is usable — a producer should eyeball it before it is cut to length"]})

# ------------------------------------------------------------------ b08
FX="C2J_wnqMlIo"; FX_URL=f"https://www.youtube.com/watch?v={FX}"
P.append({"beat_id":"F2c-b08","pass":2,"flagged":FX_URL,
 "platform":"youtube","title":"Virginia's treasury flooded with unclaimed money requests, thanks to TikTok | FOX 5 DC",
 "source_mix":{"affiliate":4,"creator_short":1},"diversity_floor_applied":True,
 "ranked":[
  rank(FX_URL,"affiliate",86,8,8,8,9,
   [seg(FX,66,118)],
   "The exact package the script names, and Bradley Earl is on tape saying the fast-track numbers went 'into the triple digits for the first time' — the script's line, sourced. Also carries the record $46 million / 50,000 claims figure. 146s total, so the pull is clean.",
   ["package is dated 2023 and references 'all of 2022' — the TikTok stampede is an older story than the script implies. See the report."]),
  rank("https://www.youtube.com/watch?v=xk1bXTXbsbg","affiliate",54,8,7,8,5,[],
   "WJLA on DC/Virginia unclaimed money, $3.8 billion. Right region, no TikTok surge angle.",[]),
  rank("https://www.youtube.com/watch?v=-9usnea9ToE","affiliate",48,8,7,8,4,[],
   "WTKR accountability piece, 8 minutes, different thesis.",[]),
  rank("https://www.tiktok.com/@deesale00/video/7324107480701717803","creator_short",40,7,8,6,4,[],
   "Diversity-floor promotion. Demand-side creator clip, but it does not show the treasury being flooded, which is the beat. Promoted into the shortlist, lost in pass two.",
   ["no caption track"]),
 ],
 "rejected":[
  {"url":"https://www.fox5dc.com/news/virginias-treasury-flooded-with-unclaimed-money-requests-heres-how-you-can-make-a-claim","source_type":"affiliate","score":70,"reason":"Originating article for the same package; no captions. Superseded by the YouTube copy."},
 ],
 "cannot_determine":["whether FOX 5 has a more recent version of this story — the script's framing implies a current trend"]})

# ------------------------------------------------------------------ b09  EMPTY
P.append({"beat_id":"F2c-b09","pass":2,"flagged":None,
 "platform":None,"title":None,
 "flagged_reason":("Nothing cleared 55, on either orientation lane. Susan Udvance returns zero video coverage "
   "across 817 harvested candidates (216 vertical + 601 horizontal twin), a targeted re-query, and three "
   "direct yt-dlp searches. Brave surfaces only her LinkedIn and ZoomInfo as a Chicago real-estate advisor — "
   "which corroborates the West Loop escrow detail and tells us the case is real, but is not footage. The "
   "ABC7 Chicago I-Team package the script cites is not indexed anywhere reachable. Everything that did "
   "surface is I-CASH promotional coverage — right outlet, right program, opposite story. Per the rule, an "
   "empty beat costs less than a wrong clip: flagging nothing rather than airing a treasurer-urges-you-to-"
   "check package under a 'the state won't give her the money' setup."),
 "better_query":"\"Udvance\" site:abc7chicago.com  ·  ABC7 Chicago I-Team \"unclaimed property\" denied claim escrow West Loop  ·  Illinois treasurer I-CASH claim denied defunct corporation I-Team — and if none hit, ask ABC7 Chicago directly for the package; this looks like an indexing gap, not an absence.",
 "source_mix":{"affiliate":4,"creator_short":1},"diversity_floor_applied":True,
 "ranked":[
  rank("https://www.tiktok.com/@abc7chicago/video/7464824143582629150","creator_short",44,8,7,7,3,[],
   "The ABC7 Chicago vertical cut the script's DECIDE marker asks about — but its caption is the Treasurer urging residents to check for unclaimed funds, not the Udvance denial. Right outlet and right format, wrong story.",
   ["no caption track"]),
  rank("https://abc7chicago.com/post/illinois-treasurer-michael-frerichs-urges-residents-check-missing-money-unclaimed-cash/","affiliate",38,8,7,7,2,[],
   "Same problem in horizontal. Promotional, not investigative.",["no caption track"]),
  rank("https://www.youtube.com/watch?v=WyPHkNcAYWM","affiliate",28,7,6,8,1,[],
   "I-CASH auction with Bears pins. Unrelated angle.",[]),
  rank("https://www.youtube.com/watch?v=zjX1K7Cv64M","affiliate",24,7,6,7,1,[],"ICash telethon. Unrelated.",[]),
 ],
 "rejected":[],
 "cannot_determine":["whether the I-Team package exists and is simply not indexed — the strong prior is that it does, since the script's detail level (the exact $19,379, the West Loop deal, the two defunct co-signers) reads like someone watched it"]})

# ------------------------------------------------------------------ b10  gated
WJ="KzMxcmF5ng4"; WJ_URL=f"https://www.youtube.com/watch?v={WJ}"
P.append({"beat_id":"F2c-b10","pass":2,"flagged":WJ_URL,
 "platform":"youtube","title":"13 Canadians charged in 'grandparent scam' investigation case that started in Baltimore",
 "status":"producer_gated",
 "source_mix":{"affiliate":5},"diversity_floor_applied":True,
 "ranked":[
  rank(WJ_URL,"affiliate",71,8,8,8,7,
   [seg(WJ,62,98)],
   "Answers the script's DECIDE question with evidence. 'Canadian police charged 13 people this week' matches the count in the producer note, and unlike the alternatives this package ALSO touches the voice angle — at 1:38 it references a WJZ victim scammed out of $38,000 'using a replicated voice'. Still not an AI-cloning prosecution, so the script's own caveat stands; but if the producer wants a bust beat, this is the one that gets closest.",
   ["PRODUCER-GATED: no PLAY CLIP marker exists for this beat. Do not cut until approved.",
    "the indictment is a grandparent-scam ring, not an AI-voice prosecution — the script's stated doubt is correct"]),
  rank("https://www.youtube.com/watch?v=OxRedGsy-Ug","affiliate",58,8,8,7,5,[],
   "CBS Boston full news conference, same 13-charged case. Useful for the opposite reason: at 10:02 an official states outright 'we haven't seen any evidence of AI being used by this crew in this case' — which independently confirms the producer note. 18 minutes, so the moment is buried.",[]),
  rank("https://www.youtube.com/watch?v=msFwnkXF-T0","affiliate",46,8,7,8,4,[],
   "WCAX cross-border arrests, thinner.",[]),
  rank("https://www.youtube.com/watch?v=7uB0tMldnlo","affiliate",40,8,7,7,3,[],
   "WFMY warning piece, not a bust. Captions recovered on retry after a bot-check throttle.",[]),
 ],
 "rejected":[
  {"url":"https://www.youtube.com/watch?v=oF0Z-W4CUpI","source_type":"affiliate","score":36,"reason":"Different case; captions genuinely unavailable after retry."},
 ],
 "cannot_determine":["whether the DOJ September 2025 indictment the script names is the same action as this Canadian charging decision"]})

json.dump(P, open("picks.json","w"), indent=1)
print(f"wrote {len(P)} picks")
for p in P:
    f=p["flagged"]
    segs=sum(len(r["segments"]) for r in p["ranked"])
    print(f"  {p['beat_id']}: {'FLAGGED' if f else (p.get('status') or 'EMPTY'):13} {segs} segment(s)")
