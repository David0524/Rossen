import numpy as np, json
from PIL import Image
ref=Image.open('../assets/jeff_ref.png').convert('RGB'); R=np.array(ref).astype(np.float32)
x0,y0=250,190
mask=np.load('mask.npy'); h,w=mask.shape
def dil(m,r):
    o=m.copy()
    for _ in range(r):
        n=o.copy(); n[1:]|=o[:-1]; n[:-1]|=o[1:]; n[:,1:]|=o[:,:-1]; n[:,:-1]|=o[:,1:]; o=n
    return o
# ---- plate: clone paper over Jeff
full=np.zeros(R.shape[:2],bool); full[y0:y0+h,x0:x0+w]=mask
hole=dil(full,7); hole[886:]=False; hole[878:904,360:640]=True
P=R.copy(); ys,xs=np.nonzero(hole)
dx=np.where(xs<560,440,300)
P[ys,xs]=R[ys,xs+dx]
Image.fromarray(P.astype(np.uint8)).resize((1920,1080),Image.LANCZOS).save('../assets/plate.png')
# ---- sprite with logo flag
spr=np.zeros((h,w,4),np.uint8); spr[...,:3]=R[y0:y0+h,x0:x0+w]; spr[...,3]=mask*255
S=Image.fromarray(spr)
logo=Image.open('../assets/logo_handdrawn.png').convert('RGBA')
src=[(228,382),(1306,218),(1311,699),(226,853)]  # TL TR BR BL in logo
c=np.array([418.5-x0,666-y0]); u=np.array([.952,.307]); v=np.array([-.422,.907]); HW,HH=55,27
dst=[c-u*HW-v*HH,c+u*HW-v*HH,c+u*HW+v*HH,c-u*HW+v*HH]
# perspective coeffs mapping dst(output)->src(input)
A=[];B=[]
for (X,Y),(x,y) in zip(dst,src):
    A.append([X,Y,1,0,0,0,-x*X,-x*Y]); B.append(x)
    A.append([0,0,0,X,Y,1,-y*X,-y*Y]); B.append(y)
coef=np.linalg.solve(np.array(A),np.array(B))
flag=logo.transform((w,h),Image.PERSPECTIVE,tuple(coef),Image.BICUBIC)
S.alpha_composite(flag)
spr=np.array(S)
# ---- split legs
HEM=640; SPLIT=256
body=spr.copy(); body[HEM+14:]=0
legL=spr.copy(); legL[:HEM-10]=0; legL[:,SPLIT:]=0
legR=spr.copy(); legR[:HEM-10]=0; legR[:,:SPLIT]=0
for n,a in [('jeff_body',body),('jeff_legL',legL),('jeff_legR',legR),('jeff_full',spr)]:
    Image.fromarray(a).save(f'../assets/{n}.png')
json.dump({'w':w,'h':h,'refX':x0,'refY':y0,'hem':HEM,'split':SPLIT},open('../assets/jeff.json','w'))
# preview
pv=Image.new('RGBA',(w,h),(240,235,220,255)); pv.alpha_composite(S); pv.crop((80,380,280,560)).resize((600,540)).save('flag_pv.png')
