"""PC job J4 (locked PREREG_PCJOBS_J4): Janus/SERAPIS prediction map over (kappa, delta, N*). AI-assisted."""
import math, os, itertools, multiprocessing as mp
from scipy.optimize import brentq
def lnV_y(y,p,kap):
    q=math.exp(-2*math.pi*y); lj=2*math.pi*y+math.log(1+744*q+196884*q*q)
    ljm=lj+math.log(abs(1-1728*math.exp(-lj))); le=-math.pi*y/12+sum(math.log(1-q**k) for k in range(1,6))
    return 2*(0.5*ljm-7/12*lj+p*math.log(lj-math.log(1728)+kap))-math.log(2*y)-4*le
def infl(args):
    kap,dl,N=args
    try:
        p=0.5+dl; qn=1/math.sqrt(2); lv=lambda u:lnV_y(math.exp(u),p,kap)
        d1=lambda u,h=1e-4:(lv(u+h)-lv(u-h))/(2*h)/qn
        d2=lambda u,h=1e-3:((lv(u+h)-2*lv(u)+lv(u-h))/h**2)/qn**2
        eps=lambda u:0.5*d1(u)**2
        us=[0.30+0.005*i for i in range(1300)]; ue=None
        for A,B in zip(us[::-1][1:],us[::-1][:-1]):
            if eps(A)>=1>eps(B): ue=brentq(lambda u:eps(u)-1,A,B); break
        if ue is None: return (kap,dl,N,None,None)
        u=ue; Na=0; du=1e-3
        while Na<N and u<14: Na+=qn*du/abs(d1(u)); u+=du
        g=d1(u); hh=d2(u); ev=0.5*g*g; return (kap,dl,N,1-6*ev+2*(hh+g*g),16*ev)
    except Exception: return (kap,dl,N,None,None)
if __name__=='__main__':
    os.makedirs('results',exist_ok=True)
    grid=list(itertools.product((0.25,0.5,1,2,math.pi,4,5,2*math.pi,7,8),(0,0.0005,0.001,0.0015,0.002,0.0023,0.0026,0.003,0.004,0.006),(50,52,54,55.6,58)))
    data=[('SPT+Planck',0.9636,0.0035),('CMB-SPA',0.9684,0.0030),('SPA+DESI',0.9728,0.0027),('P-ACT-LB',0.9752,0.0030)]
    with mp.Pool(max(1,min(12,(os.cpu_count() or 4)-2))) as P, open('results/J4_janus_map.txt','w') as fo:
        for kap,dl,N,ns,r in P.imap_unordered(infl,grid):
            if ns is None: line=f"kappa={kap:.3f} delta={dl} N*={N}: no end found"
            else:
                tags=[n for n,m,s in data if abs(ns-m)<=2*s and r<0.036]
                line=f"kappa={kap:.3f} delta={dl} N*={N}: n_s={ns:.4f} r={r:.5f} fits={','.join(tags) or 'none'}"
            print(line,flush=True); fo.write(line+'\n'); fo.flush()
    print("J4 DONE",flush=True)
