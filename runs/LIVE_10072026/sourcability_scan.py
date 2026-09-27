import subprocess,time,json
CHECKS=[
 ("A1","Target worker basket tracker TikTok"),
 ("A1","you are now being tracked at Target"),
 ("A2","Lowe's Home Depot license plate reader cameras Flock parking lot"),
 ("A3","Instacart Caper Cart"),
 ("A4","Brianna Jones Walmart self checkout lawsuit"),
 ("A4","Walmart self checkout AI camera missed scan"),
 ("A5","Eric Gardner More Perfect Union Instacart prices"),
 ("A5","Instacart price test Consumer Reports different prices same groceries"),
 ("B1","Katelyn Montalbano Prime Day cart"),
 ("B2","Prime Day fake discount price history camelcamelcamel"),
]
out={}
for bid,q in CHECKS:
    r=subprocess.run(["yt-dlp","--ignore-errors","--no-warnings","--flat-playlist",
      "--print","%(id)s | %(channel)s | %(view_count)s | %(duration)s | %(title)s",f"ytsearch6:{q}"],
      capture_output=True,text=True,timeout=150)
    lines=[l for l in r.stdout.strip().split("\n") if l.strip()]
    out.setdefault(bid,[]).append({"query":q,"results":lines,"stderr":r.stderr.strip()[-300:]})
    print(f"\n### {bid} :: {q} -> {len(lines)}")
    for l in lines: print("   ",l)
    if not lines: print("    STDERR:",r.stderr.strip()[-200:])
    time.sleep(5)
json.dump(out,open("sourcability_raw.json","w"),indent=1)
