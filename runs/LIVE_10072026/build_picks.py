import json,sys
sys.path.insert(0,"/home/user/Rossen/harvest")
from rossen_harvest.transcripts import Transcript, Cue, PAD_IN
T=json.load(open("transcripts.json"))
def tr(v):
    r=[x for x in T.values() if x.get("video_id")==v and x["status"]=="ok"][0]
    return Transcript(v,[Cue(**c) for c in r["cues"]],r["source"])
def _s(t): s=t.strip(); return s.startswith(">>") or (bool(s) and s[0].isupper())
def seg(v,a,b):
    t=tr(v); idx=[i for i,c in enumerate(t.cues) if c.start<=a]
    if idx:
        i=idx[-1]; fl=a-6.0; j=i
        while j>0 and t.cues[j].start>=fl and not _s(t.cues[j].text): j-=1
        if t.cues[j].start>=fl and _s(t.cues[j].text): i=j
        a=max(0.0,t.cues[i].start)+PAD_IN
    i,o,oc=t.segment(a,b)
    assert oc and t.find(oc) is not None and not oc.strip().startswith(">>"),oc
    return {"in":i,"out":o,"outcue":oc}
SL={b["beat_id"]:b for b in json.load(open("shortlist.json"))}
def ranked_from_shortlist(bid,dims=(0,0,0,0)):
    out=[]
    for c in SL[bid]["candidates"]:
        out.append({"url":c["url"],"source_type":c["source_type"],"score":c["score"],"tone":dims[0],"authenticity":dims[1],
                    "quality":dims[2],"fit":dims[3],"segments":[],"reasoning":"Pass-one metadata only: "+c["reason"],
                    "flags":(c.get("flags") or [])+(["captions blocked by YouTube bot-check this run — not graded in pass two"] if c["platform"]=="youtube" else [])})
    return out
THROTTLE=("THROTTLED, not empty. Every caption fetch on this beat's YouTube shortlist hit YouTube's 'Sign in to confirm you're "
          "not a bot' wall — 72 bot-check errors across the run, still blocked after a 10-minute cooldown and a retry through "
          "the normal path. Without a transcript there is no verifiable outcue, so nothing is flagged. The blocked calls were not "
          "cached; re-running captions later re-fetches cleanly.")
RERUN="Re-run Step 5 (captions) for this beat after the YouTube block lifts — no query change needed; the shortlist is good."
P=[]
# A1 manual
P.append({"beat_id":"L07-A1","pass":2,"flagged":None,"status":"manual_clip","platform":"tiktok",
 "title":"Target worker's basket-tracker TikTok (Aug 29, 2026)","manual_url":"https://www.tiktok.com/@user60342208753/video/7679448051202657566",
 "flagged_reason":("MANUAL LANE — a real outcome, not a gap. source_native is tiktok: the worker's own post is the pick. Handle "
   "matches the source log, and the video ID decodes to 2026-08-29 13:40 UTC, the script's date. Not watched. TikTok ships no "
   "caption track and yt-dlp's TikTok extractor is failing this run, so the outcue is UNVERIFIED and no timecode is given."),
 "better_query":"n/a — permalink in hand. Pull the live view count on show day (script says 3.4M).",
 "source_mix":{"first_person":1},"diversity_floor_applied":False,
 "ranked":[{"url":"https://www.tiktok.com/@user60342208753/video/7679448051202657566","source_type":"first_person","score":92,
   "tone":9,"authenticity":10,"quality":7,"fit":10,"segments":[],"reasoning":"The originating post.",
   "flags":["outcue UNVERIFIED — no caption track, extractor failing"]}],
 "rejected":[{"url":"https://www.youtube.com/watch?v=xBjs7LKtMHc","source_type":"creator_short","score":20,"reason":"Rhett Walker repost of the worker's video — aggregator, not graded over the native post."}],
 "cannot_determine":["whether the caption fragment '…#files #government #flock | dei target' is this video's full caption"]})
# A2 throttled, with a manual fallback available now
P.append({"beat_id":"L07-A2","pass":2,"flagged":None,"status":"throttled","platform":"youtube",
 "title":"License plate readers now at Home Depot, Lowe's Home Improvement stores (NBC Connecticut) — pending captions",
 "manual_url":"https://www.foxnews.com/tech/license-plate-cameras-home-depot-lowes-spark-privacy-fears.amp",
 "flagged_reason":THROTTLE+(" FALLBACK AVAILABLE NOW: the Fox News Connecticut report the source log was chasing (May 16, 2026, "
   "144s) is on foxnews.com — a manual pull with no caption track, but the right story."),
 "better_query":RERUN,"source_mix":SL["L07-A2"]["source_mix"],"diversity_floor_applied":True,
 "ranked":ranked_from_shortlist("L07-A2",(8,8,8,8)),"rejected":[],"cannot_determine":["whether NBC CT shows the pole cameras on screen"]})
# A3 throttled
P.append({"beat_id":"L07-A3","pass":2,"flagged":None,"status":"throttled","platform":"youtube",
 "title":"Caper Cart b-roll — pending captions","flagged_reason":THROTTLE+(" For a b-roll beat the transcript matters less than the "
   "picture, so a producer can eyeball Instacart's own launch video (IO1wx3zBR6s) now — but it is horizontal against a VERTICAL "
   "BROLL marker and will need a crop ruling."),
 "better_query":RERUN,"source_mix":SL["L07-A3"]["source_mix"],"diversity_floor_applied":False,
 "ranked":ranked_from_shortlist("L07-A3",(8,7,8,8)),"rejected":[],"cannot_determine":["which candidates are natively vertical"]})
# A4 empty on the named case + swap proposal (checkpoint 2)
NURSE="https://www.youtube.com/watch?v=kEN0nL8mtXw"
s1=seg("kEN0nL8mtXw",1,40); s2=seg("kEN0nL8mtXw",54,61)
P.append({"beat_id":"L07-A4","pass":2,"flagged":None,"status":"awaiting_approval","platform":None,"title":None,
 "flagged_reason":("EMPTY on the named case — genuinely, not throttled. Brianna Jones has no video in any reachable source: "
   "YouTube returned nothing on three name variants (confirmed on retry while search was live), and the Charlotte Observer, FOX8 "
   "and WAVY coverage is text (two of the three block direct fetch, so embedded video cannot be ruled out entirely). NAME "
   "COLLISION: a WCJB post about a Brianna Jones who was a Walmart manager in a fraud case is a DIFFERENT PERSON. The script's own "
   "DECIDE line anticipates this. Any swap changes what the show says — proposal held for producer approval."),
 "better_query":"Ask FOX8/WAVY (Nexstar) whether their story has a video package with Jones on camera — that is the only route to the named case.",
 "swap_proposal":{"url":NURSE,"title":"Alabama woman falsely accused of shoplifting awarded $2.1 million in Walmart suit (CBS News / WKRG)",
   "person":"Lesley Nurse, Mims, Alabama","segments":[s1,s2],
   "why":("Self-checkout malfunction, stopped by asset protection, arrested and mugshotted over $48 of groceries, charge dropped when "
          "Walmart didn't show, then a $2.1M jury verdict. On camera, captioned, outcues verified. It fits 'think what you would do "
          "if this happened to you' better than any explainer, but it is a different woman, an older case (suit filed 2018), and "
          "involves no AI camera — the script's AI framing would need to come off this beat.")},
 "source_mix":SL["L07-A4"]["source_mix"],"diversity_floor_applied":True,
 "ranked":[{"url":NURSE,"source_type":"network","score":78,"tone":9,"authenticity":9,"quality":8,"fit":5,"segments":[s1,s2],
   "reasoning":"Best available swap. Fit scored 5 because it is not the named case — the swap is what makes it fit.",
   "flags":["case swap — requires producer approval","no AI camera involved; do not let the AI line sit over this clip"]}]
   +[x for x in ranked_from_shortlist("L07-A4",(8,7,8,4)) if x["url"]!=NURSE],
 "rejected":[{"url":"https://www.facebook.com/WCJB20/posts/walmart-fraud-brianna-jones-a-manager-at-a-local-walmart-loaded-11000-on","source_type":"affiliate","score":0,"reason":"NAME COLLISION — a different Brianna Jones (Walmart manager, fraud case). Never pull."}],
 "cannot_determine":["whether FRANCE 24's fact-check (hunFGy5waws) undercuts the segment's framing — it could not be read this run"]})
# A5 throttled
P.append({"beat_id":"L07-A5","pass":2,"flagged":None,"status":"throttled","platform":"youtube",
 "title":"We Had 400 People Shop For Groceries. What We Found Will Shock You. (More Perfect Union / Consumer Reports) — pending captions",
 "flagged_reason":THROTTLE+" The top candidate is the study's own video (~4.76M views); whether Eric Gardner is on camera is the thing the transcript would settle.",
 "better_query":RERUN,"source_mix":SL["L07-A5"]["source_mix"],"diversity_floor_applied":False,
 "ranked":ranked_from_shortlist("L07-A5",(9,9,8,9)),"rejected":[],"cannot_determine":["Eric Gardner on camera; timing of the screenshots moment"]})
# B1 manual
P.append({"beat_id":"L07-B1","pass":2,"flagged":None,"status":"manual_clip","platform":"tiktok",
 "title":"Katelyn Montalbano's short video (@kb.montalbano)","manual_url":"https://www.tiktok.com/@kb.montalbano/video/7523672986004606238",
 "flagged_reason":("MANUAL LANE. The creator's own post; ID decodes to 2025-07-05, days before the July 2025 Prime Day. Found by the "
   "pre-scan and independently by the harvest. Not watched — confirm it is the cart video. Outcue UNVERIFIED (no caption track)."),
 "better_query":"n/a — permalink in hand.","source_mix":{"first_person":1},"diversity_floor_applied":False,
 "ranked":[{"url":"https://www.tiktok.com/@kb.montalbano/video/7523672986004606238","source_type":"first_person","score":88,"tone":9,
   "authenticity":10,"quality":7,"fit":9,"segments":[],"reasoning":"The originating post.","flags":["outcue UNVERIFIED","2025 video — keep it off any 'this week' line"]}],
 "rejected":[],"cannot_determine":["that this is the cart post specifically"]})
# B2 manual, profile only
P.append({"beat_id":"L07-B2","pass":2,"flagged":None,"status":"manual_clip","platform":"tiktok",
 "title":"Jaymes (@semyajnotsemaj) — Prime Day fake-discount video, July 2024","manual_url":"https://www.tiktok.com/@semyajnotsemaj",
 "flagged_reason":("MANUAL LANE, PROFILE ONLY — the specific video could not be pinned by Brave (web + video) or the harvest. "
   "Distractify (7/17/2024) supplies the content: INIU wireless charger, 41% off at $15.98 against an inflated $24.98, found on "
   "CamelCamelCamel; quote 'a 41 percent discount on a fake price'. Scroll the profile to mid-July 2024."),
 "better_query":"Search TikTok in-app for @semyajnotsemaj, July 2024. Other creators' price-history TikToks exist (@chloesdealclub, @niickjackson) but the script names Jaymes.",
 "source_mix":{"creator_short":1},"diversity_floor_applied":False,
 "ranked":[{"url":"https://www.tiktok.com/@semyajnotsemaj","source_type":"creator_short","score":70,"tone":8,"authenticity":9,
   "quality":6,"fit":9,"segments":[],"reasoning":"Profile of the named creator; permalink unpinned.","flags":["permalink not found","2024 video"]}],
 "rejected":[],"cannot_determine":["the permalink"]})
json.dump(P,open("picks.json","w"),indent=1)
print("A4 swap segments:",s1,s2)
