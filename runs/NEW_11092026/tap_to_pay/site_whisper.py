"""Whisper the news-site copies of clips whose YouTube uploads are bot-walled.
Uses rossen_harvest.vertical_transcribe's download_audio + transcribe_audio.
Usage: python3 site_whisper.py <key>=<url> ...   -> appends to site_transcripts.json"""
import json, sys, subprocess
from pathlib import Path
from rossen_harvest.vertical_transcribe import download_audio, _get_model
import numpy as np
def transcribe_audio(wav, model_size="base.en"):
    # faster-whisper's own decoder trips on this PyAV build; decode with ffmpeg to 16k mono float32
    raw = subprocess.run(["ffmpeg","-v","error","-i",str(wav),"-f","f32le","-ac","1","-ar","16000","-"],capture_output=True).stdout
    audio = np.frombuffer(raw, np.float32)
    segs, _ = _get_model(model_size).transcribe(audio, beam_size=5, vad_filter=False)
    class C: pass
    out=[]
    for sg in segs:
        c=C(); c.start=round(sg.start,2); c.end=round(sg.end,2); c.text=sg.text.strip(); out.append(c)
    return out
out = Path(__file__).with_name("site_transcripts.json")
data = json.loads(out.read_text()) if out.exists() else {}
for arg in sys.argv[1:]:
    key, url = arg.split("=", 1)
    if key in data: continue
    wav = Path(__file__).with_name("site_audio") / f"{key}.wav"
    if not wav.exists():
        src = wav.with_suffix(".src.mp4")
        subprocess.run(["yt-dlp","-q","-f","worst/best","-o",str(src),url],timeout=600)
        subprocess.run(["ffmpeg","-v","error","-y","-i",str(src),"-vn","-ac","1","-ar","16000",str(wav)])
        if src.exists(): src.unlink()
    if not wav.exists():
        print("download failed", key); continue
    dur = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(wav)],capture_output=True,text=True).stdout.strip()
    cues = transcribe_audio(wav, model_size="base.en")
    data[key] = {"url": url, "duration": dur, "cues": [{"start": c.start, "end": c.end, "text": c.text} for c in cues]}
    out.write_text(json.dumps(data, indent=1))
    print("ok", key, dur, len(cues))
