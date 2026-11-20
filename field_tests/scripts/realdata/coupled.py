import numpy as np, math, json
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
src=open('field_tests/scripts/realdata/cmb.py').read().split("c0,x=fit('lcdm'")[0]; ns={}; exec(src,ns)
A=ns['A']; beta=ns['beta']; zg=ns['zg']
def E_coupled(Om,Or,Ob,amp,bc):
    phii=math.log(A/amp)/beta; Oc=Om-Ob
    def run(VL):
        def f(N,s):
            p,q=s; a=math.exp(N); rb=3*Ob*a**-3; rc=3*Oc*a**-3*math.exp(bc*(p-phii)); rr=3*Or*a**-4
            V=VL*(1-A*math.exp(-beta*p)); dV=VL*A*beta*math.exp(-beta*p)
            H2=(rb+rc+rr+V)/(3-q*q/2)
            # eps = -dlnH/dN = (rho+P)/(2 H^2)  with rho+P = rb+rc+4/3 rr + H2 q^2
            eps=(rb+rc+4*rr/3+H2*q*q)/(2*H2)
            return [q,-(3-eps)*q-(dV+bc*rc)/H2]
        return solve_ivp(f,(math.log(1e-3),0),[phii,0],rtol=1e-8,atol=1e-11,dense_output=True)
    def H2end(VL):
        s=run(VL); p,q=s.y[:,-1]; V=VL*(1-A*math.exp(-beta*p))
        return (3*Ob+3*Oc*math.exp(bc*(p-phii))+3*Or+V)/(3-q*q/2)-1
    grid=[0.25*2**k for k in range(13)]; vals=[H2end(v) for v in grid]; VL=None
    for a_,b_,fa,fb in zip(grid,grid[1:],vals,vals[1:]):
        if fa<0<fb: VL=brentq(H2end,a_,b_,xtol=1e-10); break
    if VL is None: return None,None
    s=run(VL); N=np.log(1/(1+zg)); P,Q=s.sol(N); a=1/(1+zg)
    rb=3*Ob*a**-3; rc=3*Oc*a**-3*np.exp(bc*(P-phii)); rr=3*Or*a**-4; V=VL*(1-A*np.exp(-beta*P))
    H2=(rb+rc+rr+V)/(3-Q*Q/2); return np.sqrt(H2),(rc,P)
old=ns['Ecalc']
def Ecalc2(kind,Om,Or,par):
    if kind=='coupled':
        amp,bc,Ob=par; E,_=E_coupled(Om,Or,Ob,amp,bc); return E
    return old(kind,Om,Or,par)
ns['Ecalc']=Ecalc2
oldchi=ns['chi2_all']
def chi2c(kind,Om,h,ob,par):
    if kind=='coupled': par=(par[0],par[1],ob/h**2)
    return oldchi(kind,Om,h,ob,par)
ns['chi2_all']=chi2c
c,x=ns['fit']('coupled',[[0.311,0.671,0.02244,0.16,0.0],[0.31,0.675,0.0224,0.2,0.3],[0.31,0.675,0.0224,0.2,-0.3],[0.31,0.67,0.0224,0.3,1.0]],ns['B3']+[(0.005,0.9),(-2,2)])
out=dict(chi2=c,x=x,d=c-1650.3800547143892)
Om,h,ob,amp,bc=x; Or=ns['og']*(1+0.2271*ns['Neff'])/h**2
E,(rc,P)=E_coupled(Om,Or,ob/h**2,amp,bc)
# effective DE seen by uncoupled observer: rho_de_eff = E^2 - Om_eff_today a^-3 - Or a^-4, Om_eff_today = (rb+rc)/3 at a=1
a=1/(1+zg); Om_eff=(3*ob/h**2+rc[0])/3
rde=E**2-Om_eff*a**-3-Or*a**-4; w=-1-np.gradient(np.log(np.abs(rde)),np.log(a))/3
out['w_eff']={str(z):float(np.interp(z,zg,w)) for z in (0,0.5,1,2)}
out['closes_gap']=out['d']<=-9
print(json.dumps(out,indent=1)); json.dump(out,open('/home/claude/aegis/field_tests/results/coupled_thread.json','w'),indent=1)
