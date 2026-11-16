"""D741 (locked PREREG_D741). AI-assisted."""
import cmath, math, numpy as np
s=open('theory/modular/tr_takagi_d721.py').read(); exec(s[s.index('def sig'):s.index('def takagi')])
Robs=7.42e-5/2.5e-3
for name,t in (("tau=i",1j),("rho",complex(0.5,math.sqrt(3)/2))):
    Y=Yd(t); no=io=0; hits=[]
    for lb in np.linspace(-2,2,400):
        for ph in np.linspace(0,2*math.pi,24,endpoint=False):
            b=10**lb*cmath.exp(1j*ph)
            M=np.zeros((3,3),complex); M[:2,:2]=A(Y); M[:2,2]=b*Y; M[2,:2]=b*Y
            m=np.sort(np.linalg.svd(M,compute_uv=False)); dlo=m[1]**2-m[0]**2; dhi=m[2]**2-m[1]**2
            isNO=dlo<dhi; no+=isNO; io+=not isNO
            R=min(dlo,dhi)/max(dlo,dhi)
            if abs(R-Robs)<0.1*Robs:
                sc=math.sqrt(2.5e-3/max(dlo,dhi)) if isNO else math.sqrt(2.5e-3/(m[2]**2-m[0]**2))
                hits.append((10**lb,ph,'NO' if isNO else 'IO',m[0]/m[2],sc*m.sum()))
    print(f"{name}: NO {no}, IO {io} of {no+io}; R-matching points: {len(hits)}")
    for o in ('NO','IO'):
        h=[x for x in hits if x[2]==o]
        if h:
            print(f"   {o}: {len(h)} pts, |b| {min(x[0] for x in h):.3g}-{max(x[0] for x in h):.3g}, m_light/m_heavy {min(x[3] for x in h):.3f}-{max(x[3] for x in h):.3f}, Sigma m_nu {min(x[4] for x in h):.4f}-{max(x[4] for x in h):.4f} eV")
