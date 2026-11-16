"""D851 (locked PREREG_D851). Phase distribution over CP-odd racetrack minima. AI-assisted."""
import numpy as np, math, itertools, warnings
from scipy.optimize import minimize
warnings.filterwarnings('ignore')
def Vf(s,t,W0,A,B,a,b):
    T=s+1j*t; ea=A*np.exp(1j*a*T); eb=B*np.exp(1j*b*T)
    W=W0+ea+eb; DW=1j*a*ea+1j*b*eb+(3j/(2*t))*W
    return (2*t)**-3*((4*t*t/3)*np.abs(DW)**2-3*np.abs(W)**2)
def find(N1,N2,W0,B,n):
    A=1.0; L=N1*N2//math.gcd(N1,N2); a,b=2*math.pi/N1,2*math.pi/N2
    S=np.linspace(0,L,n,endpoint=False); Tt=np.linspace(1,60,n)
    SS,TT=np.meshgrid(S,Tt,indexing='ij'); VV=Vf(SS,TT,W0,A,B,a,b)
    P=np.pad(VV,((1,1),(0,0)),mode='wrap'); P=np.pad(P,((0,0),(1,1)),mode='edge')
    c=P[1:-1,1:-1]; loc=np.ones_like(c,bool)
    for di in (-1,0,1):
        for dj in (-1,0,1):
            if di or dj: loc&=c<P[1+di:P.shape[0]-1+di,1+dj:P.shape[1]-1+dj]
    mins=[]
    for i,j in zip(*np.where(loc)):
        r=minimize(lambda x:Vf(x[0],x[1],W0,A,B,a,b)*1e12,[S[i],Tt[j]],method='Nelder-Mead',options=dict(xatol=1e-9,fatol=1e-20,maxiter=4000))
        s0,t0=r.x; s0%=L
        if not (1<t0<60): continue
        h=1e-4*max(1,t0); f=lambda x,y:Vf(x,y,W0,A,B,a,b)
        fxx=(f(s0+h,t0)-2*f(s0,t0)+f(s0-h,t0))/h**2; fyy=(f(s0,t0+h)-2*f(s0,t0)+f(s0,t0-h))/h**2
        fxy=(f(s0+h,t0+h)-f(s0+h,t0-h)-f(s0-h,t0+h)+f(s0-h,t0-h))/(4*h*h)
        if fxx>0 and fxx*fyy-fxy**2>0:
            if not any(abs(s0-m[0])<1e-5*L and abs(t0-m[1])<1e-5 for m in mins): mins.append((s0,t0,f(s0,t0)))
    dist=lambda x:min(x%L,L-x%L,abs(x%L-L/2))
    odd=[m for m in mins if dist(m[0])>1e-3*L and m[1]>2]; even=[m for m in mins if dist(m[0])<=1e-3*L]
    return L,odd,even
pts=[(N1,N2,W0,B) for N1,N2 in itertools.combinations(range(5,11),2) for W0 in (1e-4,-1e-4,1e-3,-1e-3,1e-2,-1e-2) for B in (0.5,-0.5,1,-1,2,-2)]
th1=[];th2=[];deep_odd=0;ratios=[];dS=0;nodd_tot=0;rob=[]
for k,(N1,N2,W0,B) in enumerate(pts):
    L,odd,even=find(N1,N2,W0,B,400)
    for s0,t0,v in odd:
        th1.append(2*math.pi*s0/N1); th2.append(2*math.pi*s0/N2)
    allm=odd+even
    if allm:
        best=min(allm,key=lambda m:m[2])
        if best in odd: deep_odd+=1
        elif odd: ratios.append(min(m[2] for m in odd)/best[2])
    if even and odd:
        up=abs(min(m[2] for m in even)); nodd_tot+=len(odd); dS+=sum(1 for m in odd if m[2]+up>0)
    if k%10==0:
        _,o2,_=find(N1,N2,W0,B,700); rob.append((len(odd),len(o2)))
s1=np.abs(np.sin(th1)); s2=np.abs(np.sin(th2))
print(f"CP-odd minima (t>2): {len(th1)} over {len(pts)} points")
print(f"(a) |sin th1|>0.1: {np.mean(s1>0.1):.3f}  >0.5: {np.mean(s1>0.5):.3f} | |sin th2|>0.1: {np.mean(s2>0.1):.3f}  >0.5: {np.mean(s2>0.5):.3f}")
print("    histogram |sin th1| (10 bins 0..1):",np.histogram(s1,bins=10,range=(0,1))[0].tolist())
print(f"(b) points whose deepest minimum is CP-odd: {deep_odd}/{len(pts)} = {deep_odd/len(pts):.3f}; median V_odd,best/V_best (CP-even deepest): {np.median(ratios):.3e} (n={len(ratios)})")
agree=sum(1 for x,y in rob if x==y)
print(f"(c) robustness 400 vs 700 grid: {agree}/{len(rob)} agree; pairs={rob}")
print(f"(d) uplift by |V_even,deepest|: {dS}/{nodd_tot} CP-odd minima become dS ({dS/max(nodd_tot,1):.3f})")
