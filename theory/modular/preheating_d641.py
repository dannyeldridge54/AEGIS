"""D641 (locked PREREG_D641_PREHEATING). AI-assisted. Estimates + exact fermion mass."""
import math, sympy as sp
MP=2.435e18; mphi=2.1e11; Hinf=3.7e12; rx=2e-6
print("1. Quadratic-coupling preheating (estimates, a = 1):")
rho_end=3*Hinf**2*MP**2   # upper bound
for m0 in (1e9,1e11,1e13):
    g2=m0**2/MP**2
    q_end=g2*(MP/2)**2/(4*Hinf**2)
    Phi_x=math.sqrt(2*rx*rho_end)/mphi   # quadratic regime: rho = m^2 Phi^2/2
    q_x=g2*Phi_x**2/(4*mphi**2)
    Hx=Hinf*math.sqrt(rx)
    bound=m0**4/(3*Hx**2*MP**2)
    print(f"  m0={m0:.0e} GeV: q(end)={q_end:.2e}  q(switch)={q_x:.2e}  rho_chi/rho bound (switch)={bound:.1e}")
print("2. Self-resonance: literature only (see PREREG).")
t,tb,S,Sb=sp.symbols('t tb S Sb'); W0=sp.Integer(1); f=sp.sqrt(2)
z=[t,S]; zb=[tb,Sb]
K=-sp.log(-sp.I*(t-tb))+S*Sb; W=W0+f*S; Wb=W0+f*Sb
G=K+sp.log(W)+sp.log(Wb)
pt={t:sp.I,tb:-sp.I,S:0,Sb:0}
g=sp.Matrix(2,2,lambda i,j: sp.diff(G,z[i],zb[j]))
ginv=g.inv()
Gi=[sp.diff(G,a) for a in z]
# Christoffel Gamma^k_ij = g^{k lbar} d_i g_{j lbar}
def Gam(k,i,j): return sum(ginv[k,l]*sp.diff(g[j,l],z[i]) for l in range(2))
m=sp.Matrix(2,2,lambda i,j: sp.exp(G/2)*(sp.diff(G,z[i],z[j])-sum(Gam(k,i,j)*Gi[k] for k in range(2))+Gi[i]*Gi[j]))
mv=m.subs(pt).applyfunc(sp.simplify); gv=g.subs(pt).applyfunc(sp.simplify); Giv=[sp.simplify(x.subs(pt)) for x in Gi]
m32=sp.simplify(sp.exp(G/2).subs(pt))
ginvv=gv.inv(); Gup=[sum(ginvv[i,j]*sp.conjugate(Giv[j]) for j in range(2)) for i in range(2)]   # G^i = g^{i jbar} G_jbar
# orthonormal basis: e1 along goldstino (G^i normalised), e2 orthogonal (w.r.t. metric g)
v=sp.Matrix(Gup); nv=sp.sqrt(sp.simplify((v.H*gv.T*v)[0]))
e1=v/nv
# find e2: solve e1^dagger g e2 = 0 with e2 = (1, b)
b=sp.symbols('b'); e2=sp.Matrix([1,b])
bsol=sp.solve(sp.simplify((e1.H*gv.T*e2)[0]),b)[0]; e2=sp.Matrix([1,bsol]); e2=e2/sp.sqrt(sp.simplify((e2.H*gv.T*e2)[0]))
mchi=sp.simplify((e2.T*mv*e2)[0])
print(f"3. m3/2 = {m32}; goldstino G^i = {[sp.simplify(x) for x in Gup]}")
print(f"   inflatino (non-goldstino) mass |m_chi|/m3/2 = {sp.nsimplify(sp.simplify(sp.Abs(mchi)/m32))} = {float(sp.Abs(mchi)/m32):.4f}")
r=float(sp.Abs(mchi)/m32)
print(f"   channel phi -> gravitino + inflatino open iff m3/2 (1 + {r:.3f}) < m_phi, i.e. m3/2 < {mphi/(1+r):.2e} GeV")
