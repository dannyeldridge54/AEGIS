"""Q11 (PREREG_Q11_SUGRA_MINIMA): direct minima of the (m,n) SUGRA potential, 2201.02020 conventions."""
import numpy as np
from scipy.optimize import minimize
N=np.arange(1,61)
def sig(k): return np.array([sum(d**k for d in range(1,n+1) if n%d==0) for n in N],float)
S1,S3,S5=sig(1),sig(3),sig(5)
def forms(t):
    q=np.exp(2j*np.pi*t); qn=q**N
    E2=1-24*np.sum(S1*qn); E4=1+240*np.sum(S3*qn); E6=1-504*np.sum(S5*qn)
    eta=np.exp(2j*np.pi*t/24)*np.prod(1-qn)
    j=1728*E4**3/(E4**3-E6**2); jp=-2j*np.pi*j*E6/E4
    return E2,E4,E6,eta,j,jp
def V(x,m,n):
    t=x[0]+1j*x[1]; y=x[1]
    if y<=0.3 or abs(t)<1-1e-12 or x[0]<-0.5 or x[0]>0: return 1e9
    E2,E4,E6,eta,j,jp=forms(t)
    logH2=m*np.log(abs(j-1728))+(2*n/3)*np.log(abs(j)) if n else m*np.log(abs(j-1728))
    W2=np.exp(logH2)/abs(eta)**12
    dl=(m/2)*jp/(j-1728)+((n/3)*jp/j if n else 0)-(1j*np.pi/2)*E2+3j/(2*y)
    return (2*y)**-3*W2*((4*y*y/3)*abs(dl)**2-3)
def minimum(m,n):
    best=None
    for x0 in np.linspace(-0.499,-0.01,12):
        for y0 in np.linspace(0.87,1.6,10):
            if x0**2+y0**2<1: continue
            r=minimize(V,[x0,y0],args=(m,n),method='Nelder-Mead',options=dict(xatol=1e-9,fatol=1e-14,maxiter=4000))
            if best is None or r.fun<best.fun: best=r
    return best.x[0]+1j*best.x[1], best.fun
w=np.exp(2j*np.pi/3)
if __name__=='__main__':
    ref={1:-0.484+0.884j,2:-0.492+0.875j,3:-0.495+0.872j}
    ok=True
    for m,tr in ref.items():
        t,v=minimum(m,0); d=abs(t-tr); ok&=d<=0.003
        print(f"VALID m={m}: tau={t.real:.5f}{t.imag:+.5f}i ref={tr} |dtau|={d:.4f} {'OK' if d<=0.003 else 'FAIL'} V={v:.3e}")
    print('VALIDATION', 'PASS' if ok else 'FAIL')
    if ok:
        bad=[]
        for m in range(1,33):
            t,v=minimum(m,0); e=t-w; f=np.sqrt(3)*0.0145/(m+1/16); r=abs(e)/f
            if 8<=m<=16 and abs(r-1)>0.2: bad.append(m)
            print(f"m={m:2d} tau={t.real:.6f}{t.imag:+.6f}i |eps|={abs(e):.5f} arg={np.degrees(np.angle(e)):6.1f} ratio_to_formula={r:.3f}")
        print('RUNG-8 RULE:', 'extrap label REMOVED' if not bad else f'formula off >20% at m={bad}: use computed')
        for m in (1,2,3):
            for n in (1,2,3):
                t,v=minimum(m,n); print(f"mixed ({m},{n}): tau={t.real:.5f}{t.imag:+.5f}i |tau|={abs(t):.5f} {'arc' if abs(abs(t)-1)<1e-3 else 'off-arc'} {'CP-cons' if (abs(abs(t)-1)<1e-3 or abs(t.real)<1e-4 or abs(t.real+0.5)<1e-4) else 'CP-violating'}")
