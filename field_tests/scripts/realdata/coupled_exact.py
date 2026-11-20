import numpy as np, math, json
src=open('field_tests/scripts/realdata/coupled.py').read().split("old=ns['Ecalc']")[0]; exec(src)
ex=open('field_tests/scripts/realdata/exact.py').read().split("def E_exact")[0]; exec(ex)   # g, dg, cc
def E_coupled_exact(Om,Or,Ob,amp,bc):
    y2=A/amp; phii=math.log(y2)/beta; Oc=Om-Ob
    def run(VL):
        def f(N,s):
            p,q=s; a=math.exp(N); rb=3*Ob*a**-3; rc=3*Oc*a**-3*math.exp(bc*(p-phii)); rr=3*Or*a**-4
            V=VL*g(p); dV=VL*dg(p); H2=(rb+rc+rr+V)/(3-q*q/2); eps=(rb+rc+4*rr/3+H2*q*q)/(2*H2)
            return [q,-(3-eps)*q-(dV+bc*rc)/H2]
        return solve_ivp(f,(math.log(1e-3),0),[phii,0],rtol=1e-8,atol=1e-11,dense_output=True)
    def H2end(VL):
        s=run(VL); p,q=s.y[:,-1]; return (3*Ob+3*Oc*math.exp(bc*(p-phii))+3*Or+VL*g(p))/(3-q*q/2)-1
    grid=[0.25*2**k for k in range(14)]; vals=[H2end(v) for v in grid]; VL=None
    for a_,b_,fa,fb in zip(grid,grid[1:],vals,vals[1:]):
        if fa<0<fb: VL=brentq(H2end,a_,b_,xtol=1e-10); break
    if VL is None: return None,None
    s=run(VL); N=np.log(1/(1+zg)); P,Q=s.sol(N); a=1/(1+zg)
    rb=3*Ob*a**-3; rc=3*Oc*a**-3*np.exp(bc*(P-phii)); rr=3*Or*a**-4; V=VL*np.array([g(p) for p in P])
    return np.sqrt((rb+rc+rr+V)/(3-Q*Q/2)),(rc,P)
old=ns['Ecalc']
def Ecalc3(kind,Om,Or,par):
    if kind=='cx':
        amp,bc,Ob=par; E,_=E_coupled_exact(Om,Or,Ob,amp,bc); return E
    return old(kind,Om,Or,par)
ns['Ecalc']=Ecalc3
oldchi=ns['chi2_all']
def chi2x(kind,Om,h,ob,par):
    if kind=='cx': par=(par[0],par[1],ob/h**2)
    return oldchi(kind,Om,h,ob,par)
ns['chi2_all']=chi2x
starts=[[0.3122,0.6732,0.02232,0.9,-0.062],[0.312,0.673,0.0223,0.5,-0.06],[0.312,0.673,0.0223,1.5,-0.06],[0.312,0.673,0.0223,3.0,-0.05]]
c,x=ns['fit']('cx',starts,ns['B3']+[(0.005,5),(-2,2)])
out=dict(chi2=c,x=x,d=c-1650.3800547143892)
Om,h,ob,amp,bc=x; Or=ns['og']*(1+0.2271*ns['Neff'])/h**2
E,(rc,P)=E_coupled_exact(Om,Or,ob/h**2,amp,bc); a=1/(1+zg); Om_eff=(3*ob/h**2+rc[0])/3
rde=E**2-Om_eff*a**-3-Or*a**-4; w=-1-np.gradient(np.log(np.abs(rde)),np.log(a))/3
out['w_eff']={str(z):float(np.interp(z,zg,w)) for z in (0,0.5,1,2)}
out['amp_on_bound']=abs(amp-5)<1e-3 or abs(amp-0.005)<1e-4
out['fix_stands']=out['d']<=-9 and not out['amp_on_bound'] and abs(bc)<=0.1
print(json.dumps(out,indent=1)); json.dump(out,open('/home/claude/aegis/field_tests/results/coupled_exact.json','w'),indent=1)
