"""D643 (locked PREREG_D643_MATTER_WEIGHTS). AI-assisted."""
import sympy as sp, mpmath as mp, math
t,tb,S,Sb,Q,Qb=sp.symbols('t tb S Sb Q Qb')
W0=sp.Integer(1); f=sp.sqrt(2)
z=[t,S,Q]; zb=[tb,Sb,Qb]; W=W0+f*S; Wb=W0+f*Sb
Kh=-sp.log(-sp.I*(t-tb))+S*Sb
pt={t:sp.I,tb:-sp.I,S:0,Sb:0}
def soft(K):
    Kz=[sp.diff(K,a) for a in z]; Kzb=[sp.diff(K,b) for b in zb]
    M=sp.Matrix(3,3,lambda i,j: sp.diff(K,z[i],zb[j])).subs(pt)
    DW=[(sp.diff(W,z[i])+Kz[i]*W).subs(pt) for i in range(3)]; DWb=[(sp.diff(Wb,zb[i])+Kzb[i]*Wb).subs(pt) for i in range(3)]
    Minv=M.inv()
    Vf=sp.exp(K.subs(pt))*(sum(Minv[j,i]*DW[i]*DWb[j] for i in range(3) for j in range(3))-3*W.subs(pt)*Wb.subs(pt))
    VQQ=sp.diff(Vf,Q,Qb).subs({Q:0,Qb:0}); KQQ=sp.diff(K,Q,Qb).subs({Q:0,Qb:0}).subs(pt)
    m32=sp.exp(K.subs({Q:0,Qb:0}).subs(pt))
    return sp.nsimplify(sp.simplify(VQQ/KQQ/m32))
print("1. m_Q^2/m3/2^2 vs matter weight k:")
for k in (0,sp.Rational(1,3),sp.Rational(2,3),1,sp.Rational(4,3),2):
    r=soft(Kh+Q*Qb/(-sp.I*(t-tb))**k)
    print(f"   k={k}: {r}  (1-k = {1-k})",flush=True)
mp.mp.dps=30
def L(tau): return -mp.log(2*mp.im(tau)*abs(mp.kleinj(tau) if False else 1)) if False else -mp.log(2*mp.im(tau)*abs(mp.eta(tau))**4)
h=mp.mpf('1e-8')
dx=(L(1j+h)-L(1j-h))/(2*h); dy=(L(1j+1j*h)-L(1j-1j*h))/(2*h)
print(f"2. dL/dx at i = {mp.nstr(dx,5)}, dL/dy at i = {mp.nstr(dy,5)}  -> d_tau L = {mp.nstr((dx-1j*dy)/2,5)}")
print("3. Loop-scale estimates (m3/2 = 1.05e11-1.2e11 GeV):")
for m32 in (1.05e11,1.2e11):
    print(f"   m3/2={m32:.2e}: one-loop scalar m3/2/4pi={m32/(4*math.pi):.1e}; AMSB gaugino b g^2 m3/2/16pi^2 (b g^2=0.5..3.3)={0.5*m32/(16*math.pi**2):.1e}..{3.3*m32/(16*math.pi**2):.1e}; two-loop AMSB scalar g^2 m3/2/16pi^2={0.5*m32/(16*math.pi**2):.1e}; Higgs bound 2e10")
