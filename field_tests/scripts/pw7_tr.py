"""PW7: copy of NA6 tr_2p1 with M_H list (9.8e10, 1e12 reference)."""
"""D725 (locked PREREG_D725). AI-assisted."""
import cmath, math, numpy as np, scipy.linalg as sl
s=open('theory/modular/tr_takagi_d721.py').read(); exec(s[s.index('def sig'):s.index('def takagi')])
def Mphys(t,c):
    Y=Yd(t); M=np.zeros((3,3),complex); M[:2,:2]=A(Y); M[:2,2]=c*Y; M[2,:2]=c*Y; return 2*t.imag*M
def takagi(M,tol=1e-9):
    W,S,Vh=np.linalg.svd(M); Q=W.conj().T@M@W.conj(); U=W.astype(complex).copy(); i=0
    while i<len(S):
        j=i
        while j+1<len(S) and abs(S[j+1]-S[i])<tol*max(S[0],1): j+=1
        blk=slice(i,j+1); R=sl.sqrtm(Q[blk,blk]/S[i]); U[:,blk]=W[:,blk]@R; i=j+1
    res=np.abs(U.conj().T@M@U.conj()-np.diag(S)).max(); return S,U,res
rho=complex(0.5,math.sqrt(3)/2); y=rho.imag; h=1e-6
MP=2.435e18; m=3.1746e13; gs=106.75; can=y*math.sqrt(2)
for c in (0.3,1,3):
    M0=Mphys(rho,c); S,U,res=takagi(M0); dM=(Mphys(rho+1j*h,c)-Mphys(rho-1j*h,c))/(2*h)
    P=U.conj().T@dM@U.conj()
    print(f"c={c}: SV={np.round(S,6)} (heavy index 0? {S[0]>S[1]+1e-9}), Takagi residual {res:.1e}")
    iH=int(np.argmax([abs(S[k]-S[(k+1)%3])+abs(S[k]-S[(k+2)%3]) for k in range(3)])); L=[k for k in range(3) if k!=iH]
    PLL=P[np.ix_(L,L)]; ev,O=np.linalg.eigh(PLL.real); Pp=O.T@PLL@O
    print(f"   heavy idx {iH}: P_HH={P[iH,iH]:.3e} (Re should be ~0); P_HL={np.round(P[iH,L],4)}")
    print(f"   light block P_LL={np.round(PLL,5).tolist()}; splitting rates Re-eig={np.round(ev,5)}; rotated diag={np.round(np.diag(Pp),5)}, offdiag={Pp[0,1]:.4e}")
    for dl in (1e-4,1e-5):
        Sd=np.linalg.svd(Mphys(rho+1j*dl,c),compute_uv=False); sl_=sorted([Sd[k] for k in range(3)])
        lo=sorted(S)[:2] if iH==0 else None
        print(f"   delta={dl:g}: SVs {np.round(Sd,8)}, light shifts/delta {np.round([(sl_[0]-S[L[0]])/dl,(sl_[1]-S[L[0]])/dl],4)}")
    # channels
    for MH in (9.8e10,1e12):
        sc=MH/S[iH]; ML=S[L[0]]*sc; xs={iH:MH/m, L[0]:ML/m, L[1]:ML/m}
        Gt=0; rows=[]
        Pfull=P.copy(); Pfull[np.ix_(L,L)]=Pp
        idx=[iH,L[0],L[1]]
        for a in range(3):
            for b in range(a,3):
                i_,j_=idx[a],idx[b]; xi,xj=xs[i_],xs[j_]
                if xi+xj>=1: continue
                g=abs(Pfull[i_,j_] if a!=b else Pfull[i_,i_])*sc*can/MP
                if a==b: G=g*g*m*(1-4*xi*xi)**1.5/(16*math.pi)
                else:
                    lam=(1-(xi+xj)**2)*(1-(xi-xj)**2); G=g*g*m*math.sqrt(lam)*(1-(xi+xj)**2)/(8*math.pi)
                if G>0: rows.append(f"{'HLL'[a]}{'HLL'[b]}:g={g:.2e}"); Gt+=G
        TR=(90/(math.pi**2*gs))**0.25*math.sqrt(Gt*MP) if Gt>0 else 0
        yD=math.sqrt(0.05e-9*ML)/174
        print(f"   M_heavy={MH:.0e}: M_light={ML:.2e} GeV, open: {rows}, T_R={TR:.3e} GeV, seesaw y_D(M_light)={yD:.2e}")
