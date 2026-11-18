"""D1291 (locked): shells of self-dual champions vs Eisenstein/modular q-expansions; self-Poisson test for non-self-dual ones."""
import numpy as np, math, itertools
src=open('field_tests/e6e7_flip.py').read().split('al=np.array')[0]; ns={}; exec(src,ns); norms, cartan = ns['norms'], ns['cartan']
def sig3(n): return sum(d**3 for d in range(1,n+1) if n%d==0)
N=6
E4=[1]+[240*sig3(n) for n in range(1,N+1)]
def mul(a,b): return [sum(a[i]*b[k-i] for i in range(k+1)) for k in range(min(len(a),len(b)))]
# Delta = q prod (1-q^n)^24
P=[1]+[0]*N
for n in range(1,N+1):
    for _ in range(24):
        P=[P[k]-(P[k-n] if k>=n else 0) for k in range(N+1)]
Delta=[0]+P[:N]
E8f=mul(E4,E4); E12=mul(E8f,E4); Leech=[E12[k]-720*Delta[k] for k in range(N+1)]
# E8 enumeration to norm 12
q=norms(cartan(8),12.0001); v,c=np.unique(np.round(q).astype(int),return_counts=True); e8=dict(zip(v.tolist(),c.tolist()))
print("P1 E8 shells  :",[e8.get(2*n,0) for n in range(N+1)]); print("   240*sigma3  :",E4)
print("   P1", "PASS" if all(e8.get(2*n,0)==E4[n] for n in range(N+1)) else "FAIL")
print("P2 E4^2 coeffs:",E8f[:4]," (D1288 enumerated: 1,480,61920,1050240)", "PASS" if E8f[:4]==[1,480,61920,1050240] else "FAIL")
print("P3 E4^3-720Delta:",Leech[:4]," (D1289 enumerated: 1,0,196560)", "PASS" if Leech[:3]==[1,0,196560] else "FAIL", "; next coeff",Leech[3],"(lit 16773120)")
# P4 self-Poisson violation for non-self-dual champions at alpha=1.25
def theta(G,al,Q=12.0):
    n=len(G); G=G/np.linalg.det(G)**(1/n); qq=norms(G,Q); return np.exp(-np.pi*np.outer(al,qq)).sum(1),n
FCC=np.array([[2,1,1],[1,2,1],[1,1,2]],float)
def Dn(n):
    C=2*np.eye(n)
    for i in range(n-2): C[i,i+1]=C[i+1,i]=-1
    C[n-3,n-1]=C[n-1,n-3]=-1; return C
for name,G in (('FCC',FCC),('D5',Dn(5)),('E6',cartan(6)),('E7',cartan(7)),('E8',cartan(8)),('D4',Dn(4))):
    (t,n)=theta(G,np.array([1.25,0.8])); viol=t[0]-(1.25**(-n/2))*t[1]
    print(f"P4 {name:4s} self-Poisson violation theta(1.25) - 1.25^(-d/2) theta(0.8) = {viol:+.3e}")
# Cross-check (identity, not a locked prediction): Epstein zeta = Mellin transform of the Gaussian energy,
# Z(s) = pi^s/Gamma(s) * Int_0^inf (theta(a)-1) a^(s-1) da, using Poisson for a<1. d=2 hex and square, s=2,3.
from scipy.integrate import quad
for name,G in (('square',np.eye(2)),('hex',np.array([[1,0.5],[0.5,1]]))):
    Gn=G/np.sqrt(np.linalg.det(G)); qq=norms(Gn,40.0); qq=qq[qq>1e-12]
    th=lambda a: np.exp(-np.pi*a*qq).sum()
    for s in (2,3):
        hi=quad(lambda a: th(a)*a**(s-1),1,np.inf,limit=200)[0]
        lo=quad(lambda a: (a**-1*(1+th(1/a))-1)*a**(s-1),0,1,limit=200)[0]   # d=2: theta(a)=a^{-1} theta*(1/a), lattice self-dual up to rotation
        Z=math.pi**s/math.gamma(s)*(hi+lo)
        print(f"Mellin {name:6s} s={s}: Z={Z:.6f}")
