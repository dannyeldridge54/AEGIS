"""D639 (locked PREREG_D639_SOFT_MASSES). AI-assisted. Exact sympy evaluation of V to O(|Q|^2)."""
import sympy as sp
t,tb,S,Sb,Q,Qb=sp.symbols('t tb S Sb Q Qb')
W0=sp.Integer(1); f=sp.sqrt(2)*W0
z=[t,S,Q]; zb=[tb,Sb,Qb]
W=W0+f*S; Wb=W0+f*Sb
Kh=-sp.log(-sp.I*(t-tb))+S*Sb
def V(K):
    Kz=[sp.diff(K,a) for a in z]; Kzb=[sp.diff(K,b) for b in zb]
    M=sp.Matrix(3,3,lambda i,j: sp.diff(K,z[i],zb[j]))
    DW=[sp.diff(W,z[i])+Kz[i]*W for i in range(3)]; DWb=[sp.diff(Wb,zb[i])+Kzb[i]*Wb for i in range(3)]
    pt={t:sp.I,tb:-sp.I,S:0,Sb:0}
    return K,M,DW,DWb,pt
def soft(K,label):
    K,M,DW,DWb,pt=V(K)
    # D639 deviation D1: substitute the point before inverting (Q kept symbolic)
    M=M.subs(pt); DW=[d.subs(pt) for d in DW]; DWb=[d.subs(pt) for d in DWb]
    Minv=M.inv()
    Vf=sp.exp(K.subs(pt))*(sum(Minv[j,i]*DW[i]*DWb[j] for i in range(3) for j in range(3))-3*W.subs(pt)*Wb.subs(pt))
    VQQ=sp.diff(Vf,Q,Qb).subs({Q:0,Qb:0})
    V0=Vf.subs({Q:0,Qb:0})
    KQQ=sp.diff(K,Q,Qb).subs({Q:0,Qb:0}).subs(pt)
    m32sq=sp.exp(K.subs({Q:0,Qb:0}).subs(pt))*W0**2
    r=sp.nsimplify(sp.simplify(VQQ/KQQ/m32sq))
    print(f"{label}: V0/m3/2^2 = {sp.simplify(V0/m32sq)}, m_Q^2/m3/2^2 = {r} = {float(r):.6g}",flush=True)
soft(Kh+Q*Qb,"A canonical")
soft(-3*sp.log(sp.exp(-Kh/3)-Q*Qb/3),"B sequestered")
soft(Kh+Q*Qb/(-sp.I*(t-tb)),"C modular weight n=1")
