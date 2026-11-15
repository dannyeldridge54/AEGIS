"""D678 (locked PREREG_D678_JANUS_STRIP). AI-assisted."""
import math, numpy as np
src=open('theory/modular/running_d632.py').read().splitlines()[:41]
g={}; exec("\n".join(src),g)
res={}
for N,eps in ((46.08,(0,0.5e-4,1.0e-4,1.5e-4,2.0e-4,2.5e-4,2.836e-4)),(49.21,(0,0.5e-4,1.0e-4,1.5e-4,2.045e-4))):
    res[N]=[]
    for e in eps:
        B=g['background'](e); S=[-0.1,-0.05,0,0.05,0.1]; lp=[]
        for x in S:
            P,Pt,ys=g['spectra'](B,N,math.exp(x)); lp.append(math.log(P))
            if x==0: r=Pt/P; y0=ys
        ns=[1+(lp[i+1]-lp[i-1])/(S[i+1]-S[i-1]) for i in (1,2,3)]; a=(ns[2]-ns[0])/0.1
        res[N].append((ns[1],r)); print(f"N*={N} eps={e:.3e}: y*={y0:.2f} n_s={ns[1]:.5f} r={r:.4e} alpha_s={a:.3e}",flush=True)
for N in res:
    n=np.array([p[0] for p in res[N]]); r=np.array([p[1] for p in res[N]])
    c=np.polyfit(n-0.97,r,2); print(f"edge N*={N}: r = {c[2]:.4e} + {c[1]:.4e}(n_s-0.97) + {c[0]:.4e}(n_s-0.97)^2 ; n_s range {n.min():.4f}-{n.max():.4f}")
    res[N]=(c,n.min(),n.max())
lo=max(res[46.08][1],res[49.21][1]); hi=min(res[46.08][2],res[49.21][2])
w=[]
for ns in np.linspace(lo,hi,20):
    r1=np.polyval(res[46.08][0],ns-0.97); r2=np.polyval(res[49.21][0],ns-0.97); w.append(abs(r1-r2)/((r1+r2)/2))
print(f"overlap n_s {lo:.4f}-{hi:.4f}: max fractional width in r at fixed n_s = {max(w):.3f}")
