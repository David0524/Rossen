#!/usr/bin/env python3
"""Step 6 — assemble picks.json with transcript-verified outcues.

Each proposed segment names an outcue PHRASE. We locate it in the cue
list with the same normalization Transcript.find() uses, then read the
real out-timecode off the matched cue — no timecode arithmetic, no
invented quotes. A segment whose outcue does not verify is rejected.
"""
import json, re

tr = json.load(open("transcripts.json"))

def fmt(s):
    m, sec = divmod(int(s), 60); return f"{m}:{sec:02d}"
def norm(x): return re.sub(r"[^\w\s]", "", x.lower()).strip()

def find_cue(url, phrase):
    """Return (start,end,matched_cue_text) for the cue where phrase lands."""
    cues = tr[url]["cues"]
    n = norm(phrase)
    for c in cues:
        if n in norm(c["text"]):
            return c["start"], c["end"], c["text"]
    # sliding window across up to 4 cues
    for i, c in enumerate(cues):
        win = " ".join(norm(cues[j]["text"]) for j in range(i, min(i+4, len(cues))))
        if n in win:
            # out point = end of the last cue that contributes to the match
            end = c["end"]
            for j in range(i, min(i+4, len(cues))):
                w = " ".join(norm(cues[k]["text"]) for k in range(i, j+1))
                end = cues[j]["end"]
                if n in w:
                    break
            return c["start"], end, " ".join(cues[j]["text"] for j in range(i, min(i+4, len(cues))))
    return None

# beat -> pick spec. segments = list of (in_timecode, outcue_phrase)
PICKS = {
 "08-05-b01": {"url":"https://www.youtube.com/watch?v=_8W0-cK5XTQ","platform":"youtube",
   "title":"DO THIS every time an Amazon package arrives late","uploader":"In the Black",
   "source_type":"creator_long","score":78,
   "segments":[("1:02","worth a shot though"),("2:34","10 credit easy")],
   "reasoning":"Creator walks through asking Amazon chat for a late-delivery credit and shows a $10 credit granted on screen. Matches 'WATCH HIM SHOW YOU HOW.' Not the exact guaranteed-delivery-fee path Jeff cites, but the same late-package-refund demo.",
   "flags":["fit is the general late-delivery credit, not specifically the guaranteed-delivery shipping-fee refund"]},
 "08-05-b03": {"url":"https://www.youtube.com/watch?v=IuxwwAdVGB8","platform":"youtube",
   "title":'Amazon buyers warn watch out for the "empty box" scam',"uploader":"WSPA 7News",
   "source_type":"affiliate","score":80,
   "segments":[("0:34","reimburse us")],
   "reasoning":"Named victim Becky Allen on camera: bought from a third-party seller, got the wrong item, went back and forth, never reimbursed. Matches the A-to-Z / third-party-denial setup and 'LISTEN TO WHAT HAPPENED TO HER.'",
   "flags":["not literally an A-to-Z claim denial; it is the adjacent third-party-seller no-refund case"]},
 "08-05-b04": {"url":"https://www.youtube.com/watch?v=zTgyswYFvsY","platform":"youtube",
   "title":"Amazon issuing checks to eligible Prime members","uploader":"ABC News",
   "source_type":"network","score":88,
   "segments":[("0:16","get a check in the mail")],
   "reasoning":"Network package on the payouts going out now: up to $51, PayPal/Venmo/check, eligibility window. Exactly the beat's 'HERE'S WHAT WE KNOW RIGHT NOW' on the $2.5B settlement.",
   "flags":[]},
 "08-05-b06": {"url":"https://www.youtube.com/watch?v=o_iCvhqaWiI","platform":"youtube",
   "title":"Consumer Reports: Amazon updates rules surrounding recalled items","uploader":"WKYC Channel 3",
   "source_type":"network","score":85,
   "segments":[("1:01","injury or death"),("1:57","products out of homes")],
   "reasoning":"Explains the CPSC unanimous ruling, the 400,000 defective units (CO detectors, kids' pajamas, hair dryers), Amazon's 'we're only an intermediary' argument and the government's rejection of it. Named consumer on camera. Covers the distributor-ruling beat squarely.",
   "flags":["Consumer Reports franchise piece; the airable core is 1:01-2:22, the tail drifts into a review-writing tangent"]},
 "08-05-b08": {"url":"https://www.youtube.com/watch?v=j7i0NTk3Qwk","platform":"youtube",
   "title":"Guilford Lake woman recovering after swallowing a grill brush bristle","uploader":"WKBN27",
   "source_type":"affiliate","score":86,
   "segments":[("0:01","off the market")],
   "reasoning":"Named victim (Sally Tina Meyer) with a one-inch wire bristle stuck in her throat for a month, doctors worried about infection, 'it should be off the market.' Recent, tight, matches 'HERE YOU CAN SEE WHAT HAPPENS.'",
   "flags":["victim is about a grill brush generally, not the specific Cuisinart/Conair recalled model; the injury is the point"]},
 "08-05-b09": {"url":"https://www.youtube.com/watch?v=LPF9ETVTrSw","platform":"youtube",
   "title":"Amazon Refund Text SCAM: Don't Click That Link!","uploader":"Ryan Mack",
   "source_type":"creator_short","score":80,
   "segments":[("0:00","Stay sharp")],
   "reasoning":"Vertical Short that shows the fake Amazon refund text on screen and walks through what happens when you tap the link. Matches the vertical evidence beat 'HERE YOU CAN SEE ONE OF THESE TEXTS LAND.' Near-whole play, format-native.",
   "flags":["creator explainer over the text, not a pure raw screen-record; strongest available vertical evidence"]},
 "08-05-b10": {"url":"https://www.youtube.com/watch?v=WZYjk1fX5hs","platform":"youtube",
   "title":"How to spot a class action settlement email scam","uploader":"News 19 WLTX",
   "source_type":"affiliate","score":84,
   "segments":[("0:04","just a few dollars")],
   "reasoning":"Verified-team walkthrough of a fake class-action settlement email and how to spot it (vague case details, unrealistic payout, urgency). Directly matches the fake-FTC-settlement-refund scam beat.",
   "flags":[]},
 "08-05-b11": {"url":"https://www.youtube.com/watch?v=erKRMlCUNkc","platform":"youtube",
   "title":"Ohio tax-free weekend: reporter shows savings at checkout","uploader":"WTOL 11",
   "source_type":"affiliate","score":84,
   "segments":[("0:23","cents on the dollar")],
   "reasoning":"Reporter live in-store rings up a real cart of school supplies and shoes and computes the savings at checkout ($38.98, no tax, ~8 cents on the dollar). On the traditional 3-day Ohio holiday, which matches the script's 'back to the traditional three days.' Exactly 'WATCH HIM SHOW YOU HOW MUCH THIS SAVES ON A REAL SCHOOL LIST.'",
   "flags":[]},
}

EMPTY = {
 "08-05-b02": "No clean vertical clip of the exact phenomenon (app says 'delivered', no truck ever came, doorbell proves it). Pool returned Reddit text threads and porch-THEFT clips (a person visibly stealing a package) — a different story. Native social gap, not a query failure.",
 "08-05-b05": "No first-person vertical reaction to a tiny payout ('some under a dollar'). Pool returned news-anchor settlement readouts and Reddit text. The reaction content lives on native TikTok/IG, which the Brave video endpoint does not surface. Native social gap, not a query failure.",
 "08-05-b07": "No footage of the actual recalled product (Lakkzoom immersion water heater). Pool returned generic water-heater-fire Reddit text and OTHER product recalls (Navien/Camplux tankless — wrong object). The product was recalled July 22, ~2 weeks pre-air, with no citizen or news video yet. Recency/availability gap, not a query failure.",
}

picks = []
problems = []
for bid, spec in PICKS.items():
    segs = []
    for in_tc, outcue in spec["segments"]:
        r = find_cue(spec["url"], outcue)
        if not r:
            problems.append(f"{bid}: OUTCUE NOT FOUND: {outcue!r}")
            continue
        start, end, matched = r
        segs.append({"in": in_tc, "out": fmt(end), "outcue": outcue,
                     "_verified_at": fmt(start), "_matched_cue": matched})
    picks.append({"beat_id": bid, "flagged": spec["url"], "platform": spec["platform"],
                  "title": spec["title"], "uploader": spec["uploader"],
                  "source_type": spec["source_type"], "score": spec["score"],
                  "segments": segs, "reasoning": spec["reasoning"], "flags": spec["flags"]})
for bid, reason in EMPTY.items():
    picks.append({"beat_id": bid, "flagged": None, "empty_reason": reason})

picks.sort(key=lambda p: p["beat_id"])
json.dump(picks, open("picks.json", "w"), indent=1)

print("OUTCUE VERIFICATION:")
for p in picks:
    if not p.get("flagged"):
        print(f"  {p['beat_id']}  EMPTY")
        continue
    for s in p["segments"]:
        print(f"  {p['beat_id']}  in {s['in']} -> out {s['out']}  outcue={s['outcue']!r}  (found at {s['_verified_at']})")
if problems:
    print("\nPROBLEMS:"); [print("  "+x) for x in problems]
else:
    print("\nAll outcues verified verbatim against transcripts.")
print(f"\npicks.json: {sum(1 for p in picks if p.get('flagged'))} flagged, {sum(1 for p in picks if not p.get('flagged'))} empty")
