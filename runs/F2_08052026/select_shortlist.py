#!/usr/bin/env python3
"""Hand-select the pass-one shortlist (<=5/beat) from the triaged pool.

Selection is by title substring so the choice is auditable. I picked
on-topic, orientation-correct candidates and applied the diversity floor
where a beat's survivors were a single source-type monoculture.
"""
import json, collections

T = json.load(open("triage_report.json"))  # top-14/beat, ranked

# For each beat: ordered list of title substrings identifying my picks.
# Case-insensitive substring match against candidate title.
PICKS = {
 "08-05-b01": [  # explainer_demo/creator_long — WEAK pool (how-to-refund content mills)
   "DO THIS every time a Amazon package arrives late",
   "They say Amazon shipped fake product and refuses refund",
   "Amazon refund requests for beginners",
   "How To Get A 100% Refund For An Amazon Missing Product",
   "Amazon Refunds: 3 Proven Methods",
 ],
 "08-05-b02": [  # evidence vertical — phantom delivery. Weak/likely EMPTY.
   "Fake delivery driver steals packages off porches",   # porch theft, closest video
   "Why Doesn’t My Amazon Driver ring my doorbell",
   "A fake delivery driver in a UPS vest was caught on a Ring",
 ],
 "08-05-b03": [  # victim_interview H — all-affiliate monoculture, floor can't find non-affiliate
   "Amazon faces lawsuit over refund policy",
   "Amazon buyers warn watch out for the \"empty box\" scam",
   "Charlotte man accused of $290K Amazon scam",
   "Beware of fake Amazon 3rd party sellers",
   "Amazon cranking out refunds for purchases made years ago",
 ],
 "08-05-b04": [  # authority_report — network monoculture; floor promotes an affiliate
   "Amazon issuing checks to eligible Prime members",       # ABC News
   "Who's eligible to get money from $2.5 billion Amazon settlement",  # GMA
   "Amazon tricked consumers into signing up for Prime",     # TODAY
   "FTC accuses Amazon of tricking consumers into enrolling in Prime", # CBS
   "Millions to receive Amazon refund after FTC settlement",  # KVUE affiliate <- diversity floor
 ],
 "08-05-b05": [  # first_person_rant vertical — WEAK, no true first-person reaction video
   "Amazon may owe you money! You may get a refund! Watch video",  # Jim Maisano short
   "Amazon Prime customers can file for refund in $2.5B settlement",  # CBS Chicago short
   "Amazon Prime settlement with FTC opens door for refunds",  # 9NEWS short
 ],
 "08-05-b06": [  # authority_report CPSC ruling — strong
   "Amazon responsible for hazardous 3rd-party products and recall",  # Fox Business
   "Amazon Held Accountable for Product Recalls",
   "Amazon sues Consumer Product Safety Commission over recall order",  # AP
   "Amazon is legally responsible for recalling dangerous products",   # CBS
   "Amazon is responsible for dangerous products sold on its site",    # NBC
 ],
 "08-05-b07": [  # evidence vertical Lakkzoom — GENUINE EMPTY (no product video). carry 1 to show pass2
   "Hot water heater caught on fire",   # reddit, generic wrong-product; illustrates gap
 ],
 "08-05-b08": [  # evidence H grill brush — strong, named victim available
   "woman recovering after swallowing a grill brush bris",   # WKBN27 named victim
   "Grill brush leads to injury",                            # LOCAL 12
   "What happens if you swallow a wire brush bristle",        # Jacksonville
   "Wire Grill Brushes Pose Risks In Food",                   # CBS New York
   "STOP Using Wire Grill Brushes They’re Dangerous",     # Papa Joe knows
 ],
 "08-05-b09": [  # evidence vertical fake recall text — strong (Shorts show the text)
   "Amazon Refund Text SCAM: Don’t Click That Link",     # Ryan Mack short
   "Text scam promises Amazon refund",                       # Iowa's News Now short
   "New Phishing Text, Amazon Safety Recall",                # reddit screenshot
   "A terrifying new Amazon subscription scam is exploding",  # facebook
   "Amazon recall scam via text",                            # reddit screenshot
 ],
 "08-05-b10": [  # authority_report settlement refund scam — good
   "How to spot a class action settlement email scam",       # News19 WLTX exact fit
   "Don’t fall for this 'Amazon' refund scam",           # FOX59
   "BBB warns of Amazon refund scam",                        # FOX23
   "Amazon refund text scam: FTC issues warning",            # USA Today
   "Amazon warns about refund scam",                         # 12 News
 ],
 "08-05-b11": [  # explainer_demo/creator_long tax-free — exclude luxury/duty-free hauls
   "Tax-free weekend hacks: What you need to know before you go",  # SA Live
   "Texas tax-free weekend: Surprising items you can buy",         # NBC DFW
   "Shoppers head to Open Newbury Street in Boston on Tax-Free",   # CBS Boston
   "How Does a Tax-Free Weekend Work",                            # County Office
   "Does California Have A Tax Free Weekend",                     # County Office
 ],
}

shortlist = []
for bid, subs in PICKS.items():
    pool = T[bid]
    for s in subs:
        hit = next((c for c in pool if s.lower() in (c.get("title") or "").lower()), None)
        if not hit:
            print(f"!! {bid}: no match for {s!r}")
            continue
        shortlist.append({
            "beat_id": bid,
            "url": hit["url"],
            "video_id": hit.get("video_id"),
            "title": hit.get("title"),
            "platform": hit["platform"],
            "uploader": hit.get("uploader"),
            "duration": hit.get("duration"),
            "source_type": hit["_st"],
            "cand_orientation": hit["_cand_or"],
            "register": hit.get("register"),
            "triage_score": hit["_score"],
        })

json.dump(shortlist, open("shortlist.json","w"), indent=1)
print(f"\nwrote shortlist.json: {len(shortlist)} entries across {len(set(c['beat_id'] for c in shortlist))} beats")
by = collections.Counter(c["beat_id"] for c in shortlist)
for bid in sorted(by): print(f"  {bid}: {by[bid]} | sources:", dict(collections.Counter(c["source_type"] for c in shortlist if c["beat_id"]==bid)))
yt = [c for c in shortlist if c["platform"]=="youtube"]
tk = [c for c in shortlist if c["platform"]=="tiktok"]
print(f"\nYouTube shortlist entries (get captions): {len(yt)}")
print(f"TikTok shortlist entries (get whisper): {len(tk)}")
