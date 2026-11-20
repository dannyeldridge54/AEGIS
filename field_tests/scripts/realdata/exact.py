import numpy as np, math, json
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
cc=2*(math.pi**2/6)/1.2020569031595942; beta=2*math.sqrt(2); A=16*(math.pi**2/6)/(3*1.2020569031595942)
def g(p):
    u=math.exp(-beta*p); return ((2/3)*(1.5-2*cc*u/(1+cc*u)))**2
def dg(p):
    u=math.exp(-beta*p); du=-beta*u; f=(2/3)*(1.5-2*cc*u/(1+cc*u)); df=(2/3)*(-2*cc/(1+cc*u)**2)*du
    return 2*f*df
def E_exact(zg,Om,Or,amp):
    y2=A/amp; phii=math.log(y2)/beta
    def run(VL):
        def f(N,s):
            p,q=s; a=math.exp(N); rm=3*Om*a**-3; rr=3*Or*a**-4; H2=(rm+rr+VL*g(p))/(3-q*q/2); eps=(rm+4*rr/3+H2*q*q)/(2*H2)
            return [q,-(3-eps)*q-VL*dg(p)/H2]
        return solve_ivp(f,(math.log(1e-3),0),[phii,0],rtol=1e-8,atol=1e-11,dense_output=True)
    def H2end(VL):
        s=run(VL); p,q=s.y[:,-1]; return (3*Om+3*Or+VL*g(p))/(3-q*q/2)-1
    grid=[0.5*2**k for k in range(12)]; vals=[H2end(v) for v in grid]; VL=None
    for a_,b_,fa,fb in zip(grid,grid[1:],vals,vals[1:]):
        if fa<0<fb: VL=brentq(H2end,a_,b_,xtol=1e-10); break
    if VL is None: return None
    s=run(VL); N=np.log(1/(1+zg)); P,Q=s.sol(N); a=1/(1+zg)
    rm=3*Om*a**-3; rr=3*Or*a**-4; Vv=VL*np.array([g(p) for p in P])
    return np.sqrt((rm+rr+Vv)/(3-Q*Q/2))
out={}
# (a) BAO+SN
src=open('field_tests/scripts/realdata/run.py').read().split("out={}")[0]; ns={}; exec(src,ns)
c,x=ns['fit'](lambda Om,amp:E_exact(ns['zg'],Om,ns['Or'],amp),[[0.305,0.17],[0.305,0.3],[0.31,0.1]],[(0.1,0.6),(0.005,5)])
out['a_BAO_SN']=dict(chi2=c,x=x,d=c-1645.329050928889,leading=-7.0135353085033785)
print(json.dumps(out),flush=True)
# (b) +CMB: patch Ecalc thread branch
src2=open('field_tests/scripts/realdata/cmb.py').read().split("c0,x=fit('lcdm'")[0]; ns2={}; exec(src2,ns2)
old=ns2['Ecalc']
def Ecalc2(kind,Om,Or,par):
    if kind=='thread': return E_exact(ns2['zg'],Om,Or,par)
    return old(kind,Om,Or,par)
ns2['Ecalc']=Ecalc2
c,x=ns2['fit']('thread',[[0.311,0.671,0.02244,0.16],[0.311,0.671,0.02244,0.3]],ns2['B3']+[(0.005,5)])
out['b_BAO_SN_CMB']=dict(chi2=c,x=x,d=c-1650.3800547143892,leading=-4.835376192902686)
out['leading_adequate']=abs(out['a_BAO_SN']['d']-out['a_BAO_SN']['leading'])<=1 and abs(out['b_BAO_SN_CMB']['d']-out['b_BAO_SN_CMB']['leading'])<=1
print(json.dumps(out,indent=1)); json.dump(out,open('/home/claude/aegis/field_tests/results/realdata_exact.json','w'),indent=1)
