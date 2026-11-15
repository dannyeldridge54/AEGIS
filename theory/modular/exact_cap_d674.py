"""D674 (locked PREREG_D674_EXACT_CAP). AI-assisted."""
import math
src=open('theory/modular/running_d632.py').read().splitlines()[:41]
g={}; exec("\n".join(src),g)
def ystar(e,N):
    B=g['background'](e); return g['spectra'](B,N,1.0)[2],B
for N in (46.08,49.21):
    e0,e1=1.7e-4,2.3e-4
    y0,_=ystar(e0,N); y1,_=ystar(e1,N)
    for it in range(12):
        e2=e1+(25-y1)*(e1-e0)/(y1-y0)
        y2,B=ystar(e2,N); print(f"  N*={N} iter {it}: eps={e2:.5e} y*={y2:.4f}",flush=True)
        if abs(y2-25)<0.01: break
        e0,y0,e1,y1=e1,y1,e2,y2
    S=[-0.1,-0.05,0,0.05,0.1]; lp=[]
    for x in S:
        P,Pt,ys=g['spectra'](B,N,math.exp(x)); lp.append(math.log(P))
        if x==0: r=Pt/P
    ns=[1+(lp[i+1]-lp[i-1])/(S[i+1]-S[i-1]) for i in (1,2,3)]; a=(ns[2]-ns[0])/0.1
    print(f"CAP N*={N}: eps_max={e2:.4e} y*={y2:.3f} n_s={ns[1]:.5f} r={r:.4e} alpha_s={a:.3e}",flush=True)
