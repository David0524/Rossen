"""Caption parsing tests. Uses a fixture shaped like real YouTube
auto-captions, including the rolling duplicate lines they emit."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rossen_harvest.transcripts import parse_vtt, Transcript, Cue, PAD_IN, PAD_OUT

ok = fail = 0
def check(label, cond):
    global ok, fail
    if cond: ok += 1; print(f"  PASS  {label}")
    else:    fail += 1; print(f"  FAIL  {label}")

# Real auto-caption shape: rolling duplicates, inline timing tags, entities.
VTT = """WEBVTT
Kind: captions
Language: en

00:00:00.120 --> 00:00:03.400
tonight a retired police officer says he

00:00:03.400 --> 00:00:06.900
tonight a retired police officer says he
lost nearly ten thousand dollars

00:00:06.900 --> 00:00:10.200
lost nearly ten thousand dollars
to a scam he never saw coming

00:00:34.000 --> 00:00:38.500
I spent <c>thirty</c> years putting criminals
away &amp; I still fell for it

00:00:38.500 --> 00:00:43.100
they sent me an invoice that looked
exactly like PayPal

00:01:18.000 --> 00:01:21.900
when I sent the money out that was it
it was gone
"""

print("\n-- vtt parsing --")
cues = parse_vtt(VTT)
check(f"cues parsed ({len(cues)})", len(cues) == 6)
check("rolling duplicates not doubled", cues[0].text == "tonight a retired police officer says he")
check("inline tags stripped", "<c>" not in cues[3].text)
check("entities unescaped", "&" in cues[3].text and "&amp;" not in cues[3].text)
check("start time float", abs(cues[0].start - 0.12) < 0.01)
check("timecode formatted", cues[3].timecode == "0:34")
check("last cue at 1:18", cues[-1].timecode == "1:18")

print("\n-- srt fallback --")
SRT = """1
00:00:05,000 --> 00:00:08,000
she took everything from us

2
00:00:08,000 --> 00:00:11,500
every dollar we had saved
"""
s = parse_vtt(SRT)
check("srt comma millis parsed", len(s) == 2 and s[0].timecode == "0:05")

print("\n-- transcript surface --")
t = Transcript("I3667lq1L2o", cues, "auto")
check("duration from last cue", abs(t.duration - 81.9) < 0.1)
check("full_text joins", "PayPal" in t.full_text())
p = t.as_prompt()
check("prompt is timestamped", p.startswith("[0:00]") and "[0:34]" in p)

print("\n-- outcue verification (the anchor) --")
hit = t.find("when I sent the money out")
check("exact phrase found", hit is not None and hit.timecode == "1:18")
check("case and punctuation ignored", t.find("When I sent the money OUT!") is not None)
check("phrase spanning two cues found", t.find("exactly like PayPal") is not None)
check("absent phrase returns None", t.find("this was never said on camera") is None)
check("empty phrase returns None", t.find("") is None)

print("\n-- padded segment output --")
a, b, outcue = t.segment(34.0, 43.1)
check(f"in padded early ({a})", a == "0:33")
check(f"out padded late ({b})", b == "0:44")
check("outcue is verbatim last line", "exactly like PayPal" in outcue)
check("pad constants sane", PAD_IN == 1.0 and PAD_OUT == 1.5)

a2, _, _ = t.segment(0.5, 3.0)
check("in point clamps at zero", a2 == "0:00")

print("\n-- degenerate input --")
check("empty string -> no cues", parse_vtt("") == [])
check("header only -> no cues", parse_vtt("WEBVTT\n\n") == [])
check("no captions -> empty transcript safe", Transcript("x", [], "none").duration == 0.0)

print(f"\n{'='*50}\n{ok} passed, {fail} failed\n{'='*50}")
sys.exit(1 if fail else 0)
