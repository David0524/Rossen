import json, subprocess, time, sys
CHECKS = [
 ("b01", 'Rachel Missouri AI voice cloning scam daughter'),
 ("b01", 'InvestigateTV AI voice clone mom wired money Mexico'),
 ("b02", 'Ann Dickherber voice cloning'),
 ("b03", 'Rachel Missouri voice clone death threats police'),
 ("b04", 'Deborah Del Mastro'),
 ("b05", 'Erin West Operation Shamrock scamdemic'),
 ("b06", 'Olathe Kansas police AI voice kidnapping scam'),
 ("b07", 'Alex Pearlman unclaimed money tiktok'),
 ("b08", 'Virginia treasury unclaimed property tiktok flood claims'),
 ("b09", 'Susan Udvance Illinois unclaimed property'),
 ("b10", 'DOJ grandparent scam indictment 13 charged'),
]
out={}
for i,(bid,q) in enumerate(CHECKS):
    cmd=["yt-dlp","--ignore-errors","--no-warnings","--flat-playlist",
         "--print","%(id)s | %(channel)s | %(duration)s | %(title)s",
         f"ytsearch5:{q}"]
    try:
        r=subprocess.run(cmd,capture_output=True,text=True,timeout=120)
        lines=[l for l in r.stdout.strip().split("\n") if l.strip()]
    except Exception as e:
        lines=[f"ERROR {e}"]
    out.setdefault(bid,[]).append({"query":q,"results":lines,"stderr":r.stderr.strip()[-200:] if 'r' in dir() else ""})
    print(f"### {bid} :: {q}  -> {len(lines)} hits", flush=True)
    for l in lines: print("   ", l, flush=True)
    time.sleep(4)
json.dump(out, open("sourcability_raw.json","w"), indent=1)
