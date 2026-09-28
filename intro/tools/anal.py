import numpy as np, subprocess, glob, os
for f in sorted(glob.glob('/usr/lib/libreoffice/share/gallery/sounds/*.wav')):
    raw=subprocess.run(['ffmpeg','-v','error','-i',f,'-ac','1','-ar','22050','-f','f32le','-'],capture_output=True).stdout
    x=np.frombuffer(raw,np.float32); hop=1102
    env=[np.sqrt(np.mean(x[i:i+hop]**2)+1e-12) for i in range(0,len(x)-hop,hop)]
    env=np.array(env); db=20*np.log10(env/env.max()+1e-9)
    # centroid
    S=np.abs(np.fft.rfft(x[:min(len(x),22050*2)]*np.hanning(min(len(x),22050*2)))); fr=np.fft.rfftfreq(min(len(x),22050*2),1/22050)
    cen=(S*fr).sum()/S.sum()
    ons=[round(i*hop/22050,2) for i in range(1,len(env)) if env[i]>env[i-1]*2.2 and db[i]>-20]
    print(f"{os.path.basename(f):14s} peak={x.max():.2f} rms={env.mean():.3f} cen={cen:6.0f}Hz env(50ms dB)=",' '.join(str(int(v)) for v in db[:60:2]),'ons',ons[:12])
