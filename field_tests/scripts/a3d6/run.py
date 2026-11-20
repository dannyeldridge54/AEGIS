import numpy as np, json, math, mpmath as mp
def G11(R,x,y,K=12):
    m=np.arange(-K,K+1); M,W=np.meshgrid(m,m)
    return np.sqrt(y)*np.real(np.sum(np.exp(-np.pi*y*(M**2/R**2+W**2*R**2))*np.exp(2j*np.pi*x*M*W)))
def RN(f,alpha,L=60.0,nx=81,ny=400):
    # integral over F_L of f dx dy / y^2, minus subtraction
    xs=np.linspace(-0.5,0.5,nx); tot=0.0
    wx=np.full(nx,1.0); wx[0]=wx[-1]=0.5; dx=1.0/(nx-1)
    for i,x in enumerate(xs):
        y0=math.sqrt(1-x*x)
        # dense near bottom, log-spaced
        ys=np.concatenate([np.linspace(y0,4,ny),np.geomspace(4,L,ny)[1:]])
        vals=np.array([f(x,y)/y**2 for y in ys])
        tot+=wx[i]*dx*np.trapz(vals,ys)
    sub=math.log(L) if alpha==1 else L
    return tot-sub
# validation d=2 at T=U=i: rectangular torus R1=R2=1 -> T=U=i
val=RN(lambda x,y:G11(1,x,y)**2,1)
eta=complex(mp.eta(1j)) if hasattr(mp,'eta') else None
q=mp.exp(-2*mp.pi); etai=float(q**(1/24)*mp.qp(q))
dkl=-math.log(etai**8)-math.log(8*math.pi*math.exp(1-0.5772156649)/(3*math.sqrt(3)))
o=dict(validation=dict(numeric=val,DKL=dkl,diff=val-dkl,pass_=abs(val-dkl)<2e-3))
if o['validation']['pass_']:
    I={}
    for R in (1,1.25,1.5,2,3):
        I[str(R)]=RN(lambda x,y,R=R:G11(R,x,y)**4,2)
    o['I']=I; o['min']=min(I.values()); o['positive']=o['min']>0
print(json.dumps(o,indent=1)); json.dump(o,open('field_tests/results/a3_d6.json','w'),indent=1)
