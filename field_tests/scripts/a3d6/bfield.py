import numpy as np, math, json, mpmath as mp
K=6; r=np.arange(-K,K+1)
M1,M2,N1,N2=[a.flatten() for a in np.meshgrid(r,r,r,r,indexing='ij')]
def G22(T,U,x,y):
    T1,T2=T.real,T.imag; U1,U2=U.real,U.imag
    # Hamiltonian form: |p_R|^2 term; standard: tau2 * sum q^{pL^2/2} qbar^{pR^2/2}
    # pL^2-pR^2 = 2(m1 n1 + m2 n2); pR^2 = |-m1 U + m2 + T n1 + T U n2|^2/(T2 U2)  (one convention)
    pR2=np.abs(-M1*U+M2+T*N1+T*U*N2)**2/(T2*U2)
    pLpR=2*(M1*N1+M2*N2)
    pL2=pR2+pLpR
    return y*np.real(np.sum(np.exp(-np.pi*y*(pL2+pR2)/2*1.0)*np.exp(1j*np.pi*x*pLpR)))
def RN(f,alpha,L=40.0,nx=41,ny=160):
    xs=np.linspace(-0.5,0.5,nx); tot=0.0; wx=np.full(nx,1.0); wx[0]=wx[-1]=0.5; dx=1.0/(nx-1)
    for i,x in enumerate(xs):
        y0=math.sqrt(1-x*x); ys=np.concatenate([np.linspace(y0,4,ny),np.geomspace(4,L,ny)[1:]])
        tot+=wx[i]*dx*np.trapezoid(np.array([f(x,y)/y**2 for y in ys]),ys)
    return tot-(math.log(L) if alpha==1 else L**(alpha-1)/(alpha-1))
def eta(t):
    q=mp.exp(2j*mp.pi*t); return complex(q**(mp.mpf(1)/24)*mp.qp(q))
T0=complex(0.5,1); U0=1j
val=RN(lambda x,y:G22(T0,U0,x,y),1)
dkl=-math.log(T0.imag*U0.imag*abs(eta(T0)*eta(U0))**4)-math.log(8*math.pi*math.exp(1-0.5772156649)/(3*math.sqrt(3)))+0.04523
o=dict(validation_d2=dict(num=val,ref=dkl,diff=val-dkl,ok=abs(val-dkl)<3e-3))
chk=RN(lambda x,y:G22(1j,1j,x,y)**2,2); o['check_b0_R1']=dict(num=chk,ref=-0.662,ok=abs(chk+0.662)<0.02)
if o['validation_d2']['ok'] and o['check_b0_R1']['ok']:
    I={}
    for R in (1,1.25):
        for b in (0,0.25,0.5):
            T=complex(b,R*R); I[f'R={R},b={b}']=RN(lambda x,y,T=T:G22(T,1j,x,y)**2,2)
    o['I']=I
    o['B_only_helps']=all(I[f'R={R},b={b}']>=I[f'R={R},b=0']-1e-3 for R in (1,1.25) for b in (0.25,0.5))
conv=lambda v: bool(v) if type(v).__name__ in ('bool','bool_') else float(v)
print(json.dumps(o,indent=1,default=conv)); json.dump(o,open('field_tests/results/a3_d6_b.json','w'),indent=1,default=conv)
