import json, subprocess, time
CHECKS = [
 ("b01", 'mom stayed on phone two hours AI voice scam wired money Mexico'),
 ("b01", 'AI voice clone scam Missouri mom Walmart Walgreens'),
 ("b02", 'Ann Dickherber cybersecurity Wentzville'),
 ("b02", 'cybersecurity expert clones reporter voice on camera demo'),
 ("b03", 'AI kidnapping scam victim police did nothing death threats'),
 ("b06", 'Olathe police department scam warning'),
 ("b06", 'Olathe Kansas police AI voice scam KCTV'),
 ("b09", 'Susan Udvance'),
 ("b09", 'Illinois unclaimed property woman cannot claim money defunct companies ABC7'),
 ("b07", 'Pearlmania500 unclaimed money every state'),
]
out={}
for bid,q in CHECKS:
    cmd=["yt-dlp","--ignore-errors","--no-warnings","--flat-playlist",
         "--print","%(id)s | %(channel)s | %(duration)s | %(title)s",
         f"ytsearch5:{q}"]
    r=subprocess.run(cmd,capture_output=True,text=True,timeout=120)
    lines=[l for l in r.stdout.strip().split("\n") if l.strip()]
    out.setdefault(bid,[]).append({"query":q,"results":lines,"stderr":r.stderr.strip()[-300:]})
    print(f"### {bid} :: {q} -> {len(lines)}", flush=True)
    for l in lines: print("   ", l, flush=True)
    if not lines and r.stderr.strip(): print("   STDERR:", r.stderr.strip()[-300:], flush=True)
    time.sleep(6)
json.dump(out, open("sourcability_retry.json","w"), indent=1)
