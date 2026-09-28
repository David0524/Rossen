import numpy as np, subprocess, sys
def load(f):
    raw=subprocess.run(['ffmpeg','-v','error','-i',f,'-ac','1','-ar','22050','-f','f32le','-'],capture_output=True).stdout
    return np.frombuffer(raw,np.float32)
names='untie romans theetone curve sparcle kling glasses top left pluck ok beam2 falling apert2 ups'.split()
for n in names:
    x=load(f'/usr/lib/libreoffice/share/gallery/sounds/{n}.wav'); N=2048; out=[]
    for i in range(0,len(x)-N,N):
        w=x[i:i+N]*np.hanning(N); S=np.abs(np.fft.rfft(w)); fr=np.fft.rfftfreq(N,1/22050)
        S[fr<60]=0; k=S.argmax(); e=np.sqrt((x[i:i+N]**2).mean())
        out.append(f"{fr[k]:.0f}{'' if e>0.03 else '.'}")
    print(n,' '.join(out[:40]))
