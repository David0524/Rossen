import numpy as np
from PIL import Image
im=np.array(Image.open('../assets/jeff_ref.png').convert('RGB')).astype(np.float32)
x0,x1,y0,y1=250,720,190,884
sub=im[y0:y1,x0:x1]; lum=sub@[.299,.587,.114]
mx=sub.max(2); mn=sub.min(2); sat=(mx-mn)/(mx+1)
def dil(m,r):
    o=m.copy()
    for _ in range(r):
        n=o.copy(); n[1:]|=o[:-1]; n[:-1]|=o[1:]; n[:,1:]|=o[:,:-1]; n[:,:-1]|=o[:,1:]; o=n
    return o
def flood(seedmask,passable):
    out=seedmask&passable
    while True:
        n=dil(out,1)&passable
        if (n==out).all(): return out
        out=n
dark=lum<110
walls=dil(dark,2)
passable=~walls & (((sat<0.2)&(lum>135))|(lum>215))
b=np.zeros(dark.shape,bool); b[0,:]=b[-1,:]=b[:,0]=b[:,-1]=True
out=flood(b,passable)
out=dil(out,2)&~dark  # grow back into gap region but never over outline
jeff=~out
seed=np.zeros_like(jeff); seed[400-y0,470-x0]=True
comp=flood(seed,jeff)
# fill holes
holes=~flood(b,~comp); comp|=holes
print(comp.sum())
np.save('mask.npy',comp)
rgba=np.zeros((y1-y0,x1-x0,4),np.uint8); rgba[...,:3]=sub; rgba[...,3]=comp*255
Image.fromarray(rgba).save('jeff_raw.png')
pv=sub.copy(); pv[~comp]=[255,0,255]; Image.fromarray(pv.astype(np.uint8)).save('jeff_pv.png')
