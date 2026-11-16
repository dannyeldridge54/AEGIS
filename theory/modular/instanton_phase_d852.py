"""D852 (locked PREREG_D852). Instanton phase Delta = 2 pi dn Re T over racetrack minima. AI-assisted."""
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
d1=[];d2=[];e1=[]
for N1,N2,W0,B in pts:
    L,odd,even=find(N1,N2,W0,B,400)
    for s0,t0,v in odd: d1.append(2*math.pi*s0); d2.append(4*math.pi*s0)
    for s0,t0,v in even: e1.append(2*math.pi*s0)
a1=np.abs(np.sin(d1)); a2=np.abs(np.sin(d2)); b1=np.abs(np.sin(e1))
print(f"CP-odd minima: {len(d1)}; CP-even minima: {len(e1)}")
print(f"Delta1 (dn=1): |sin|>0.1 {np.mean(a1>0.1):.3f}, >0.5 {np.mean(a1>0.5):.3f}; hist {np.histogram(a1,bins=10,range=(0,1))[0].tolist()}")
print(f"Delta2 (dn=2): |sin|>0.1 {np.mean(a2>0.1):.3f}, >0.5 {np.mean(a2>0.5):.3f}")
print(f"CP-even minima: max |sin Delta1| = {b1.max():.2e} (expected 0 since L/2 integer or half-integer -> check)")
