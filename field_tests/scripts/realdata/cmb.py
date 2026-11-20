import numpy as np, math, json, sys
from scipy.integrate import solve_ivp, cumulative_trapezoid, quad
from scipy.optimize import minimize, brentq
exec(open('field_tests/scripts/realdata/run.py').read().split("Orh2=4.18e-5")[0])
c=299792.458; og=2.4729e-5; Neff=3.044; onu=0.00064
mu_c=np.array([0.01041,0.02223,0.14208]); Cc=1e-9*np.array([[0.006621,0.12444,-1.1929],[0.12444,21.344,-94.001],[-1.1929,-94.001,1488.4]]); Cci=np.linalg.inv(Cc)
zg=np.linspace(0,2.5,2501)
A=16*(math.pi**2/6)/(3*1.2020569031595942); beta=2*math.sqrt(2)
def zstar(ob,om):
    g1=0.0783*ob**-0.238/(1+39.5*ob**0.763); g2=0.560/(1+21.1*ob**1.81)
    return 1048*(1+0.00124*ob**-0.738)*(1+g1*om**g2)
def rd_fit(ob,obc): return 55.154*math.exp(-72.3*(onu+0.0006)**2)/(obc**0.25351*ob**0.12807)
def make_Ehigh(Om,Or,rde25,kind,par):
    def Eh(z):
        if kind=='cpl':
            w0,wa=par; a=1/(1+z); f=a**(-3*(1+w0+wa))*math.exp(-3*wa*(1-a)); de=(1-Om-Or)*f
        elif kind=='ls':
            de=(1-Om-Or)*(1 if z<par else -1)
        else: de=rde25
        return math.sqrt(max(Om*(1+z)**3+Or*(1+z)**4+de,1e-30))
    return Eh
def thetastar(h,ob,Om,Or,Elow,Eh):
    obc=Om*h*h-onu; om=Om*h*h; zs=zstar(ob,om); H0=100*h
    Dlow=np.trapezoid(1/Elow,zg)
    Dhigh=quad(lambda z:1/Eh(z),2.5,zs,limit=400)[0]
    DM=c/H0*(Dlow+Dhigh)
    Rb=lambda z:3*ob/(4*og)/(1+z)
    rs=quad(lambda z:c/math.sqrt(3*(1+Rb(z)))/(H0*Eh(z)),zs,1e7,limit=400)[0]
    return rs/DM, obc
cal=None
def Ecalc(kind,Om,Or,par):
    if kind=='lcdm': E=np.sqrt(Om*(1+zg)**3+Or*(1+zg)**4+1-Om-Or)
    elif kind=='cpl':
        w0,wa=par; a=1/(1+zg); E=np.sqrt(Om*(1+zg)**3+Or*(1+zg)**4+(1-Om-Or)*a**(-3*(1+w0+wa))*np.exp(-3*wa*(1-a)))
    elif kind=='ls': E=np.sqrt(np.maximum(Om*(1+zg)**3+Or*(1+zg)**4+(1-Om-Or)*np.where(zg<par,1,-1),1e-12))
    elif kind=='thread':
        amp=par; phii=math.log(A/amp)/beta
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
        s,V=run(VL); N=np.log(1/(1+zg)); P,Q=s.sol(N); a=1/(1+zg); rm=3*Om*a**-3; rr=3*Or*a**-4; Vv=VL*(1-A*np.exp(-beta*P))
        E=np.sqrt((rm+rr+Vv)/(3-Q*Q/2))
    return E
def chi2_all(kind,Om,h,ob,par):
    Or=og*(1+0.2271*Neff)/h**2
    E=Ecalc(kind,Om,Or,par)
    if E is None or not np.all(np.isfinite(E)): return 1e9
    rde25=E[-1]**2-Om*(3.5)**3-Or*(3.5)**4
    Eh=make_Ehigh(Om,Or,rde25,kind,par)
    th,obc=thetastar(h,ob,Om,Or,E,Eh); th*=cal
    d=np.array([th,ob,obc])-mu_c; cc=float(d@Cci@d)
    Dc=np.concatenate([[0],cumulative_trapezoid(1/E,zg)])*c/(100*h); rd=rd_fit(ob,obc)
    DcI=lambda z: np.interp(z,zg,Dc); EI=lambda z: np.interp(z,zg,E)
    t=[]
    for z,q in zip(bz,bq):
        DM=DcI(z); DH=c/(100*h)/EI(z)
        t.append((DM if q=='DM_over_rs' else DH if q=='DH_over_rs' else (z*DM*DM*DH)**(1/3))/rd)
    t=np.array(t); cb=float((bv-t)@bci@(bv-t))
    mm=5*np.log10((1+zhel)*DcI(zcmb)); dl=mm-mu; cs=float(dl@ic@dl-(dl@ic).sum()**2/Csum)
    return cc+cb+cs
# calibration at Planck 2018 LCDM
h0=0.6736; ob0=0.02237; oc0=0.1200; Om0=(ob0+oc0+onu)/h0**2; Or0=og*(1+0.2271*Neff)/h0**2
E0=Ecalc('lcdm',Om0,Or0,None); Eh0=make_Ehigh(Om0,Or0,1-Om0-Or0,'lcdm',None)
th0,_=thetastar(h0,ob0,Om0,Or0,E0,Eh0); cal=0.0104110/th0
out=dict(calibration=cal); print(json.dumps(out),flush=True)
if abs(cal-1)>0.005: json.dump(out,open('/home/claude/aegis/field_tests/results/realdata_cmb.json','w')); sys.exit()
def fit(kind,starts,bounds):
    def obj(x):
        if any(not(lo<=v<=hi) for v,(lo,hi) in zip(x,bounds)): return 1e9
        Om,h,ob=x[:3]; par=x[3:] if len(x)>4 else (x[3] if len(x)==4 else None)
        return chi2_all(kind,Om,h,ob,par)
    best=None
    for s in starts:
        r=minimize(obj,s,method='Nelder-Mead',options=dict(xatol=1e-5,fatol=1e-3,maxiter=1500))
        if best is None or r.fun<best.fun: best=r
    return float(best.fun),[float(v) for v in best.x]
B3=[(0.2,0.45),(0.6,0.8),(0.018,0.026)]
c0,x=fit('lcdm',[[0.31,0.68,0.0223]],B3); out['LCDM']=dict(chi2=c0,x=x); out['sanity']=0.66<=x[1]<=0.70 and 0.29<=x[0]<=0.33
print(json.dumps(out),flush=True)
if out['sanity']:
    c1,x=fit('cpl',[[0.31,0.68,0.0223,-0.8,-0.6],[0.32,0.67,0.0223,-0.7,-1.0]],B3+[(-2,0),(-4,2)]); out['CPL']=dict(chi2=c1,x=x,d=c1-c0)
    c2,x=fit('thread',[[0.31,0.68,0.0223,0.17],[0.31,0.68,0.0223,0.3]],B3+[(0.005,0.9)]); out['thread']=dict(chi2=c2,x=x,d=c2-c0)
    c3,x=fit('ls',[[0.31,0.68,0.0223,1.8],[0.31,0.68,0.0223,2.4]],B3+[(0.3,2.49)]); out['LsCDM']=dict(chi2=c3,x=x,d=c3-c0)
    out['thread_supported']=out['thread']['d']<=-4
print(json.dumps(out,indent=1)); json.dump(out,open('/home/claude/aegis/field_tests/results/realdata_cmb.json','w'),indent=1)
