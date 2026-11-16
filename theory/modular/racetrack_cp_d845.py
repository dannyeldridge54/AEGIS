"""D845 (locked PREREG_D845). CP-odd minima of a real-coefficient racetrack. AI-assisted."""
import numpy as np, math, itertools
from scipy.optimize import minimize
def Vf(s,t,W0,A,B,a,b):
    T=s+1j*t; ea=A*np.exp(1j*a*T); eb=B*np.exp(1j*b*T)
    W=W0+ea+eb; Wt=1j*a*ea+1j*b*eb; KT=3j/(2*t)
    DW=Wt+KT*W
    return (2*t)**-3*((4*t*t/3)*np.abs(DW)**2-3*np.abs(W)**2)
tot=0; withodd=0; examples=[]
for N1,N2 in itertools.combinations(range(5,11),2):
    L=N1*N2//math.gcd(N1,N2); a,b=2*math.pi/N1,2*math.pi/N2
    for W0 in (1e-4,-1e-4,1e-3,-1e-3,1e-2,-1e-2):
        for B in (0.5,-0.5,1,-1,2,-2):
            A=1.0; tot+=1
            S=np.linspace(0,L,400,endpoint=False); Tt=np.linspace(1,60,400)
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
                if fxx>0 and fxx*fyy-fxy**2>0: mins.append((s0,t0,f(s0,t0)))
            def dist(x): return min(x%L,L-x%L,abs(x%L-L/2))
            odd=[m for m in mins if dist(m[0])>1e-3*L and m[1]>2]
            even=[m for m in mins if dist(m[0])<=1e-3*L]
            if odd:
                withodd+=1
                if len(examples)<8:
                    ev=min([m[2] for m in even]) if even else float('nan')
                    o=min(odd,key=lambda m:m[2])
                    examples.append(f"N=({N1},{N2}) W0={W0:+.0e} B={B:+} : CP-odd min s={o[0]:.4f} (L={L}) t={o[1]:.3f} V={o[2]:.3e}; deepest CP-even V={ev:.3e}; n_odd={len(odd)} n_even={len(even)}")
print(f"parameter points: {tot}; with >=1 CP-odd minimum (t>2): {withodd} ({100*withodd/tot:.1f}%)")
for e in examples: print(e)
