"""D757 (locked PREREG_D757). AI-assisted."""
import math, numpy as np
def E(x,y,M=60):
    m=np.arange(-M,M+1)[:,None]; n=np.arange(-M,M+1)[None,:]
    d=np.abs(m+n*(x+1j*y))**4; d[M,M]=np.inf; return float((y**2/d).sum())
h=1e-3
for y in (1,2,5):
    lap=y**2*((E(0.5+h,y)-2*E(0.5,y)+E(0.5-h,y))+(E(0.5,y+h)-2*E(0.5,y)+E(0.5,y-h)))/h**2
    print(f"check y={y}: Delta_hyp E / E = {lap/E(0.5,y):.4f} (expect 2)")
ys=np.linspace(1,30,59)
for c in (1e-4,1e-3,1e-2):
    out=[]
    for y in ys:
        e=E(0.5,y,40); ey=(E(0.5,y+h,40)-E(0.5,y-h,40))/(2*h)
        Ku=complex(0,1/(2*y))-0.5j*c*ey; Kinv=4*y*y/(1+2*c*e)
        V=math.exp(c*e)*(Kinv*abs(Ku)**2-1)/(2*y)
        out.append((y,c*e,V))
    s=" ".join(f"y={y:.0f}:cE={ce:.2f},V={V:.3g}" for y,ce,V in out[::8])
    print(f"c'={c:g}: {s}")
