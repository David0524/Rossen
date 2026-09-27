import json
def c(url,st,score,dur,up,reason,cd,plat="youtube",promoted=False,flags=None):
    d={"url":url,"platform":plat,"source_type":st,"score":score,"duration":dur,"uploader":up,
       "reason":reason,"cannot_determine":cd,"diversity_floor_promoted":promoted}
    if flags: d["flags"]=flags
    return d
SL=[]
def beat(bid,cands,mix,floor,short=None,notes=None):
    o={"beat_id":bid,"pass":1,"candidates":cands,"source_mix":mix,"diversity_floor_applied":floor}
    if short: o["short_of_five_reason"]=short
    if notes: o["notes"]=notes
    SL.append(o)
Y="https://www.youtube.com/watch?v="
# ---------- A1 manual
beat("L07-A1",[c("https://www.tiktok.com/@user60342208753/video/7679448051202657566","first_person",92,None,"@user60342208753",
  "MANUAL LANE. The worker's own post. Handle matches the source log; ID decodes to 2026-08-29, the script's date. Surfaced independently by both the pre-scan and the harvest.",
  ["not watched; caption fragment reads '…#files #government #flock | dei target' — confirm it is the basket video"],plat="tiktok")],
  {"first_person":1},False,short="Manual lane: source_native tiktok. The native post is the pick; reposts (Rhett Walker xBjs7LKtMHc) and commentary (Taylor Lorenz Ho6Sg72mJtg) are not graded against it.")
# ---------- A2
beat("L07-A2",[
 c(Y+"jTKvp41lHZc","affiliate",86,142,"NBC Connecticut","License plate readers at Home Depot and Lowe's — the Connecticut story the source log was chasing, on a captioned affiliate. Added by hand: the pre-scan found it, the harvest did not.",["whether it shows the pole cameras clearly, per 'here you can see'"]),
 c("https://www.foxnews.com/tech/license-plate-cameras-home-depot-lowes-spark-privacy-fears.amp","network",78,144,"Fox News","The exact Fox News Connecticut report the source log cites (May 16, 2026). news_web, no caption track.",["no captions — outcue unverifiable from this copy"],plat="news_web"),
 c(Y+"-RaHh0LVS7Q","affiliate",70,121,"We Are Iowa Local 5","Home Depot and Lowe's installing plate readers. Second market, same story.",["footage of the actual cameras vs anchor read"]),
 c(Y+"lq3mZnI8tnY","affiliate",52,143,"KOMO News","Flock privacy safeguards amid backlash — right company, not the stores.",["whether stores are mentioned"]),
 c(Y+"NyS782HGrbY","creator_long",48,227,"ACLU","DIVERSITY FLOOR PROMOTION over a fifth affiliate/network. Police use of Flock data — the 'who can search it' angle. Advocacy source; 38 below the top pick, not a peer.",["whether stores are named"],promoted=True),
],{"affiliate":3,"network":1,"creator_long":1},True)
# ---------- A3
beat("L07-A3",[
 c("https://www.youtube.com/shorts/jqTpde_UWs4","creator_short",74,125,"Omni Talk Retail","Vertical Short — the only native-vertical Caper footage found. Commentary title ('strategy still isn't working'), so b-roll content is uncertain.",["whether the cart is on screen and rolling, vs a talking head"]),
 c(Y+"IO1wx3zBR6s","creator_long",72,124,"Instacart","Instacart's own launch video: clean, well-lit cart footage in an aisle — exactly the visual. But horizontal against a VERTICAL BROLL beat, and it's brand marketing.",["crop viability for vertical"],flags=["orientation crossed: horizontal source on a vertical beat — producer rules on crop"]),
 c(Y+"CU53EbSEVAA","affiliate",66,327,"FOX 5 New York","Affiliate package on Caper carts in a grocery store. Horizontal.",["crop viability"],flags=["orientation crossed"]),
 c(Y+"BuUPAtCEKMM","first_person",60,217,"Ankit","Shopper filming ShopRite Caper carts. Raw — could be the natural b-roll.",["orientation, stability"]),
 c(Y+"v2Ea_skSdE4","creator_short",54,26,"The Spoon","26s cart demo, 2023. Short enough to be pure b-roll.",["orientation; age of the cart model"]),
],{"creator_short":2,"creator_long":1,"affiliate":1,"first_person":1},False)
# ---------- A4 (no Jones video) — swap candidates graded so the room has them in hand
beat("L07-A4",[
 c(Y+"tmoQxq2P7Y4","network",62,181,"Inside Edition","A different woman accused after self-checkout (~891K views). Closest to the setup's emotional beat, but it is a CASE SWAP.",["date, which store, whether AI cameras are involved"],flags=["case swap — needs producer approval"]),
 c(Y+"hunFGy5waws","network",58,301,"FRANCE 24 English","Fact-check of claims about Walmart's in-store AI cameras. Explainer — matches the script's DECIDE fallback — but it may cut AGAINST the segment's framing.",["what it concludes about self-checkout specifically"],flags=["may contradict the show — read before using"]),
 c(Y+"JS2ezxljX_c","affiliate",50,52,"KHOU 11","'Walmart testing out artificial intelligence in stores' — short explainer. Likely old.",["date; whether it's self-checkout"]),
 c(Y+"kEN0nL8mtXw","network",48,146,"CBS News","Alabama woman awarded $2.1M after false shoplifting accusation at Walmart. A case swap, and a strong one, but not self-checkout AI.",["whether self-checkout is involved"],flags=["case swap — needs producer approval"]),
 c(Y+"IUpUy4UqZD4","network",40,203,"AP Archive","Walmart's 'AI factory' store — cameras in a store, raw AP. Old (2019).",["date"]),
],{"network":4,"affiliate":1},True,
 notes="No video of Brianna Jones exists in any reachable source (YouTube zero on three variants and a retry; Charlotte Observer, FOX8 and WAVY are text; FOX8 blocked a direct fetch). NAME COLLISION: a WCJB Facebook post about a Brianna Jones who was a Walmart manager in a fraud case is a DIFFERENT PERSON — do not pull it. Candidates below exist only to put the script's DECIDE options in front of the producer.")
# ---------- A5
beat("L07-A5",[
 c(Y+"osxr7xSxsGo","creator_long",88,1114,"More Perfect Union and Consumer Reports","The study itself, from the outlet that ran it (~4.76M views). creator_long is this role's natural source type.",["whether Eric Gardner is on camera; where the screenshots moment sits in 18 minutes"]),
 c(Y+"WpX5kp5Svtk","creator_long",80,175,"More Perfect Union","Three-minute MPU cut on the same findings (Dec 14, 2025). Tighter runway than the long version.",["whether Gardner presents it"]),
 c(Y+"_I6qF2d3uYc","creator_long",60,1764,"Consumer Reports","CR's own 'Talking Carts' long-form. 29 minutes — over the ceiling, demoted.",["everything; too long to scan in metadata"]),
 c(Y+"8V7Hl2jcWl8","affiliate",58,129,"WISH-TV","Affiliate read of the CR findings. No Gardner.",["whether any MPU footage is used"]),
 c(Y+"U5Rt7aPBDUE","network",52,152,"Good Morning America","Instacart responds — useful for the rebuttal line, not the setup.",["whether the D.C. eggs example is cited"]),
],{"creator_long":3,"affiliate":1,"network":1},False)
# ---------- B1 manual
beat("L07-B1",[c("https://www.tiktok.com/@kb.montalbano/video/7523672986004606238","first_person",88,None,"@kb.montalbano",
  "MANUAL LANE. 'Katelyn Montalbano's short video'. ID decodes to 2025-07-05 — days before that July's Prime Day, consistent with 'screenshotted before Prime Day'. Found by the pre-scan and again by the harvest.",
  ["not watched — confirm this is the cart post and not another from the account (@kb.montalbano, 'Katelyn | 4x Boy Mama')"],plat="tiktok")],
  {"first_person":1},False,short="Manual lane: source_native tiktok. No YouTube copy exists.")
# ---------- B2 manual
beat("L07-B2",[c("https://www.tiktok.com/@semyajnotsemaj","creator_short",70,None,"@semyajnotsemaj",
  "MANUAL LANE, PROFILE ONLY. The specific video could not be pinned by any search. Distractify (7/17/2024) gives the product (INIU wireless charger, 41% off at $15.98 vs an inflated $24.98), the tool (CamelCamelCamel) and the quote 'a 41 percent discount on a fake price'.",
  ["the permalink itself — scroll the profile to July 2024"],plat="tiktok")],
  {"creator_short":1},False,short="Manual lane: source_native tiktok, permalink not pinned. Other creators' Prime-Day-price-history TikToks surfaced (@chloesdealclub, @niickjackson) but the script names Jaymes, so they are not substitutes without a script change.")
json.dump(SL,open("shortlist.json","w"),indent=1); print("shortlist:",len(SL),"beats,",sum(len(b["candidates"]) for b in SL),"candidates")
