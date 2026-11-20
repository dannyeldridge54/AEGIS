import numpy as np, math, json, sys
from scipy.integrate import solve_ivp, cumulative_trapezoid
from scipy.optimize import minimize, brentq
D='/home/claude/data_dl/'
bm=np.loadtxt(D+'desi_bao/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_mean.txt',dtype=str)
bz=bm[:,0].astype(float); bv=bm[:,1].astype(float); bq=bm[:,2]
bc=np.loadtxt(D+'desi_bao/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_cov.txt'); bci=np.linalg.inv(bc)
rows=[l.split() for l in open(D+'sn/desy5/4_DISTANCES_COVMAT/DES-Dovekie_HD.csv') if l.startswith('SN:')]
zcmb=np.array([float(r[3]) for r in rows]); zhel=np.array([float(r[4]) for r in rows]); mu=np.array([float(r[5]) for r in rows])
d=np.load(D+'sn/desy5/4_DISTANCES_COVMAT/STAT+SYS.npz'); n=int(d['nsn'][0]); ic=np.zeros((n,n)); ic[np.triu_indices(n)]=d['cov']; il=np.tril_indices(n,-1); ic[il]=ic.T[il]
assert n==len(mu), (n,len(mu))
Csum=ic.sum()
Orh2=4.18e-5; h=0.68; Or=Orh2/h**2
zg=np.concatenate([np.linspace(0,2.5,2501)])
def chi2_from_E(E):   # E(z) on zg
    Dc=np.concatenate([[0],cumulative_trapezoid(1/E,zg)])   # in c/H0
    DcI=lambda z: np.interp(z,zg,Dc); EI=lambda z: np.interp(z,zg,E)
    th=[]
    for z,q in zip(bz,bq):
        DM=DcI(z); DH=1/EI(z)
        th.append(DM if q=='DM_over_rs' else DH if q=='DH_over_rs' else (z*DM*DM*DH)**(1/3))
    th=np.array(th); a=(th@bci@bv)/(th@bci@th); cb=float((bv-a*th)@bci@(bv-a*th))
    mm=5*np.log10((1+zhel)*DcI(zcmb)); dl=mm-mu; cs=float(dl@ic@dl-(dl@ic).sum()**2/Csum)
    return cb+cs, cb, cs
def E_lcdm(Om): return np.sqrt(Om*(1+zg)**3+Or*(1+zg)**4+1-Om-Or)
def E_cpl(Om,w0,wa):
    a=1/(1+zg); f=a**(-3*(1+w0+wa))*np.exp(-3*wa*(1-a)); return np.sqrt(Om*(1+zg)**3+Or*(1+zg)**4+(1-Om-Or)*f)
def E_ls(Om,zd):
    OL=1-Om-Or; s=np.where(zg<zd,1.0,-1.0)
    E2=Om*(1+zg)**3+Or*(1+zg)**4+OL*s
    return np.sqrt(np.maximum(E2,1e-12))
A=16*(math.pi**2/6)/(3*1.2020569031595942); beta=2*math.sqrt(2)
def E_thread(Om,amp):
    phii=math.log(A/amp)/beta
    def run(VL):
        V=lambda p:VL*(1-A*math.exp(-beta*p)); dV=lambda p:VL*A*beta*math.exp(-beta*p)
        def f(N,s):
            p,q=s; a=math.exp(N); rm=3*Om*a**-3; rr=3*Or*a**-4; H2=(rm+rr+V(p))/(3-q*q/2); eps=(rm+4*rr/3+H2*q*q)/(2*H2)
            return [q,-(3-eps)*q-dV(p)/H2]
        return solve_ivp(f,(math.log(1e-3),0),[phii,0],rtol=1e-8,atol=1e-11,dense_output=True),V
    def H2end(VL):
        s,V=run(VL); p,q=s.y[:,-1]; return (3*Om+3*Or+V(p))/(3-q*q/2)-1
    grid=[0.5*2**k for k in range(12)]; vals=[H2end(v) for v in grid]; VL=None
    for a_,b_,fa,fb in zip(grid,grid[1:],vals,vals[1:]):
        if fa<0<fb: VL=brentq(H2end,a_,b_,xtol=1e-10); break
    if VL is None: return None
    s,V=run(VL); N=np.log(1/(1+zg)); P,Q=s.sol(N)
    a=1/(1+zg); rm=3*Om*a**-3; rr=3*Or*a**-4; Vv=VL*(1-A*np.exp(-beta*P)); H2=(rm+rr+Vv)/(3-Q*Q/2)
    return np.sqrt(H2)
def fit(fun,x0,bounds):
    def obj(x):
        if any(not(lo<=v<=hi) for v,(lo,hi) in zip(x,bounds)): return 1e9
        E=fun(*x)
        if E is None or not np.all(np.isfinite(E)): return 1e9
        return chi2_from_E(E)[0]
    best=None
    for start in x0:
        r=minimize(obj,start,method='Nelder-Mead',options=dict(xatol=1e-4,fatol=1e-3,maxiter=400))
        if best is None or r.fun<best.fun: best=r
    return float(best.fun),[float(v) for v in best.x]
out={}
c0,x=fit(E_lcdm,[[0.30],[0.32]],[(0.1,0.6)]); out['LCDM']=dict(chi2=c0,x=x)
out['sanity_ok']=0.28<=x[0]<=0.34
print(json.dumps(out),flush=True)
if not out['sanity_ok']: json.dump(out,open('/home/claude/aegis/field_tests/results/realdata_neg.json','w'),indent=1); sys.exit()
c,x=fit(E_cpl,[[0.31,-0.8,-0.5],[0.33,-0.7,-1.0],[0.30,-1,0]],[(0.1,0.6),(-2,0),(-4,2)]); out['CPL']=dict(chi2=c,x=x,dchi2=c-c0)
c,x=fit(E_ls,[[0.30,1.5],[0.30,2.0],[0.31,1.0]],[(0.1,0.6),(0.3,2.49)]); out['LsCDM']=dict(chi2=c,x=x,dchi2=c-c0)
c,x=fit(E_thread,[[0.31,0.15],[0.31,0.25],[0.30,0.05]],[(0.1,0.6),(0.005,0.9)]); out['Weave_thread']=dict(chi2=c,x=x,dchi2=c-c0)
out['neg_space_preferred']=out['LsCDM']['chi2']<out['Weave_thread']['chi2']-2
out['thread_vs_CPL']=out['Weave_thread']['chi2']-out['CPL']['chi2']
print(json.dumps(out,indent=1))
json.dump(out,open('/home/claude/aegis/field_tests/results/realdata_neg.json','w'),indent=1)
