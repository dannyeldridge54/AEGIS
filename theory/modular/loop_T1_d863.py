"""D863 (locked PREREG_D863). Racetrack CP-odd minima with a one-loop c'/t Kähler term. AI-assisted."""
import numpy as np, math, warnings
from scipy.optimize import minimize
warnings.filterwarnings('ignore')
N1,N2=5,6; a,b=2*math.pi/N1,2*math.pi/N2; L=30
def Vf(s,t,W0,B,c):
    T=s+1j*t; ea=np.exp(1j*a*T); eb=B*np.exp(1j*b*T); W=W0+ea+eb; WT=1j*a*ea+1j*b*eb
    K=-3*np.log(2*t)+c/t; K1=-3/t-c/t**2; K2=3/t**2+2*c/t**3
    KT=K1/(2j); Kinv=4/K2
    return np.exp(K)*(Kinv*np.abs(WT+KT*W)**2-3*np.abs(W)**2)
def mins(W0,B,c):
    S=np.linspace(0,L,400,endpoint=False); Tt=np.linspace(1,60,400)
    SS,TT=np.meshgrid(S,Tt,indexing='ij'); VV=Vf(SS,TT,W0,B,c)
    P=np.pad(VV,((1,1),(0,0)),mode='wrap'); P=np.pad(P,((0,0),(1,1)),mode='edge')
    cc=P[1:-1,1:-1]; loc=np.ones_like(cc,bool)
    for di in (-1,0,1):
        for dj in (-1,0,1):
            if di or dj: loc&=cc<P[1+di:P.shape[0]-1+di,1+dj:P.shape[1]-1+dj]
    out=[]
    for i,j in zip(*np.where(loc)):
        r=minimize(lambda x:Vf(x[0],x[1],W0,B,c)*1e12,[S[i],Tt[j]],method='Nelder-Mead',options=dict(xatol=1e-9,fatol=1e-20,maxiter=4000))
        s0,t0=r.x; s0%=L
        if not (2<t0<60): continue
        h=1e-4*t0; f=lambda x,y:Vf(x,y,W0,B,c)
        fxx=(f(s0+h,t0)-2*f(s0,t0)+f(s0-h,t0))/h**2; fyy=(f(s0,t0+h)-2*f(s0,t0)+f(s0,t0-h))/h**2
        fxy=(f(s0+h,t0+h)-f(s0+h,t0-h)-f(s0-h,t0+h)+f(s0-h,t0-h))/(4*h*h)
        d=min(s0,L-s0,abs(s0-L/2))
        if fxx>0 and fxx*fyy-fxy**2>0 and d>1e-3*L and not any(abs(s0-m[0])<1e-4 and abs(t0-m[1])<1e-4 for m in out): out.append((s0,t0))
    return sorted(out)
summary={}
for W0 in (4e-3,-4e-3):
    for B in (0.5,-0.5,1,-1,2,-2):
        base=mins(W0,B,0.0); line=f"W0={W0:+.0e} B={B:+}: c'=0 -> {len(base)} odd" + (f" (t={base[0][1]:.3f})" if base else "")
        for c in (0.008,-0.008,0.08,-0.08,0.8,-0.8):
            m=mins(W0,B,c); same=len(m)==len(base)
            shift=max([max(abs(x[0]-y[0])/L,abs(x[1]-y[1])/y[1]) for x,y in zip(m,base)],default=0.0) if same else float('nan')
            ok=same and shift<0.01; summary.setdefault(abs(c),[]).append(ok)
            line+=f" | c'={c:+.3f}: {len(m)} ({'shift %.1e'%shift if same else 'COUNT CHANGED'})"
        print(line,flush=True)
for c,v in sorted(summary.items()): print(f"|c'|={c}: survive in {sum(v)}/{len(v)} (W0,B,sign) cases")
