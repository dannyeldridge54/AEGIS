import numpy as np, math, json
src=open('field_tests/scripts/realdata/run.py').read().split("out={}")[0]; exec(src)
def thread_general(Om,amp,sign=+1,ki=0.0):
    phii=math.log(A/amp)/beta
    def V(p,VL): return VL*(1-sign*A*math.exp(-beta*p))
    def dV(p,VL): return VL*sign*A*beta*math.exp(-beta*p)
    def run(VL):
        # initial velocity: kinetic fraction ki of field energy; q = dphi/dN ; H^2 q^2/2 = ki/(1-ki) * V ; uphill for original V means +phi direction
        def f(N,s):
            p,q=s; a=math.exp(N); rm=3*Om*a**-3; rr=3*Or*a**-4; H2=(rm+rr+V(p,VL))/(3-q*q/2); eps=(rm+4*rr/3+H2*q*q)/(2*H2)
            return [q,-(3-eps)*q-dV(p,VL)/H2]
        a0=1e-3; rm=3*Om*a0**-3; rr=3*Or*a0**-4; Vi=V(phii,VL)
        K=ki/(1-ki)*Vi if ki>0 else 0.0
        H2i=rm+rr+Vi+K; q0=math.sqrt(2*K/H2i) if K>0 else 0.0
        return solve_ivp(f,(math.log(a0),0),[phii,q0],rtol=1e-8,atol=1e-11,dense_output=True)
    def H2end(VL):
        s=run(VL); p,q=s.y[:,-1]; return (3*Om+3*Or+V(p,VL))/(3-q*q/2)-1
    grid=[0.5*2**k for k in range(12)]; vals=[H2end(v) for v in grid]; VL=None
    for a_,b_,fa,fb in zip(grid,grid[1:],vals,vals[1:]):
        if fa<0<fb: VL=brentq(H2end,a_,b_,xtol=1e-10); break
    if VL is None: return None
    s=run(VL); N=np.log(1/(1+zg)); P,Q=s.sol(N); a=1/(1+zg)
    rm=3*Om*a**-3; rr=3*Or*a**-4; Vv=VL*(1-sign*A*np.exp(-beta*P)); H2=(rm+rr+Vv)/(3-Q*Q/2)
    return np.sqrt(H2)
out={}
c,x=fit(lambda Om,amp:thread_general(Om,amp,-1),[[0.31,0.2],[0.31,0.5],[0.30,0.05]],[(0.1,0.6),(0.005,5)]); out['R1_flipped']=dict(chi2=c,x=x)
c,x=fit(lambda Om,amp,k:thread_general(Om,amp,+1,k),[[0.31,0.17,0.1],[0.31,0.1,0.5],[0.30,0.3,0.3]],[(0.1,0.6),(0.005,0.9),(0.0,0.9)]); out['R2_reverse_roll']=dict(chi2=c,x=x)
# R3: mirror of D1692 best thread w(a)
Eb=E_thread(0.30486804720759364,0.17400386251509176)
a=1/(1+zg); lnE2=np.log(Eb**2)
# recover w(a) of DE from Eb: rho_de = E^2 - Om a^-3 - Or a^-4 ; w = -1 - dln rho/(3 dln a)
Om0=0.30486804720759364; rde=Eb**2-Om0*a**-3-Or*a**-4; lna=np.log(a); w=-1-np.gradient(np.log(rde),lna)/3
wfun=lambda aa: np.interp(aa,a[::-1],w[::-1])
def E_R3(Om):
    am=np.clip(1/3+1-a,1/3,1); wr=np.where(a>=1/3,wfun(am),wfun(1.0))
    # integrate rho_de(a)/rho_de(1) = exp(-3 ∫_1^a (1+w)/a' da')
    order=np.argsort(a); aa=a[order]; ww=wr[order]
    I=np.concatenate([[0],cumulative_trapezoid((1+ww)/aa,aa)]); I=I-np.interp(1.0,aa,I)
    f=np.exp(-3*I); fz=np.empty_like(f); fz[order]=f
    return np.sqrt(Om*(1+zg)**3+Or*(1+zg)**4+(1-Om-Or)*fz)
c,x=fit(E_R3,[[0.30],[0.32]],[(0.1,0.6)]); out['R3_time_mirror']=dict(chi2=c,x=x,note='post-hoc shape')
for k in list(out):
    out[k]['dchi2_vs_LCDM']=out[k]['chi2']-1645.329050928889; out[k]['dchi2_vs_thread']=out[k]['chi2']-1638.3155156203857
print(json.dumps(out,indent=1)); json.dump(out,open('/home/claude/aegis/field_tests/results/realdata_reverse.json','w'),indent=1)
