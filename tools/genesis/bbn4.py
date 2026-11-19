# (c) Danny Lee Eldridge · AEGIS Community License
"""BBN v4 (lock PREREG_GENESIS_LI7): v3 network + Be7, Li7."""
import math, numpy as np
from scipy.integrate import solve_ivp
from tools.genesis.bbn2 import background, rates, MN, BD, HBARC, NA
from tools.genesis.bbn3 import skm, K9
from tools.genesis import li7rates as L
def run(eta=6.127e-10, dneff=0.0, Tsw=0.2):
    bg=background(dneff); lna,T,Tnu,t=bg['lna'],bg['T'],bg['Tnu'],bg['t']
    Z3=1.2020569031595942
    nb=eta*2*Z3/math.pi**2*(T[-1]/HBARC)**3*np.exp(3*(lna[-1]-lna))
    Ti=lambda tt: float(np.interp(tt,t,T)); nbi=lambda tt: float(np.interp(tt,t,nb))
    idx=np.unique(np.linspace(0,len(t)-1,160).astype(int))
    tab=np.array([rates(T[i],Tnu[i]) for i in idx]); tg=t[idx]
    l1=np.log(tab[:,0]); l2=np.log(np.maximum(tab[:,1],1e-300))
    lam=lambda tt:(math.exp(np.interp(tt,tg,l1)),math.exp(np.interp(tt,tg,l2)))
    def lgam(Tm,sv): return sv*(4/3)*(MN*Tm/(4*math.pi))**1.5/HBARC**3*math.exp(-BD/Tm)
    def f(tt,y):
        n,p,d,tr,h3,h4,be,li=y; Tm=Ti(tt); B=nbi(tt); T9=Tm*K9; r=skm(T9); lnp,lpn=lam(tt)
        R_np=B*r['npg']*n*p; R_g=lgam(Tm,r['npg'])*d
        R_dp=B*r['dpg']*d*p; R_ddn=0.5*B*r['ddn']*d*d; R_ddp=0.5*B*r['ddp']*d*d
        R_hn=B*r['he3np']*h3*n; R_td=B*r['tdn']*tr*d; R_hd=B*r['he3dp']*h3*d
        R_ha=B*L.he3ag(T9)/NA*h3*h4; R_ta=B*L.tag(T9)/NA*tr*h4; R_bn=B*L.be7np(T9)/NA*be*n; R_lp=B*L.li7pa(T9)/NA*li*p
        dn=-lnp*n+lpn*p-R_np+R_g+R_ddn-R_hn+R_td-R_bn
        dp=lnp*n-lpn*p-R_np+R_g-R_dp+R_ddp+R_hn+R_hd+R_bn-R_lp
        dd=R_np-R_g-R_dp-2*R_ddn-2*R_ddp-R_td-R_hd
        dt=R_ddp+R_hn-R_td-R_ta
        dh3=R_dp+R_ddn-R_hn-R_hd-R_ha
        dh4=R_td+R_hd-R_ha-R_ta+2*R_lp
        return [dn,dp,dd,dt,dh3,dh4,R_ha-R_bn,R_ta+R_bn-R_lp]
    tsw=float(np.interp(-Tsw,-T,t)); X0=1/(1+math.exp(1.2933/T[0]))
    sa=solve_ivp(lambda tt,y:[-lam(tt)[0]*y[0]+lam(tt)[1]*(1-y[0])],(t[0],tsw),[X0],method='BDF',rtol=1e-8,atol=1e-14)
    n0=sa.y[0,-1]; Tm=Ti(tsw); r=skm(Tm*K9); d0=nbi(tsw)*r['npg']*n0*(1-n0)/lgam(Tm,r['npg'])
    sol=solve_ivp(f,(tsw,t[-1]),[n0,1-n0-d0,d0,0,0,0,0,0],method='BDF',rtol=1e-7,atol=1e-22,dense_output=True)
    n,p,d,tr,h3,h4,be,li=sol.y[:,-1]
    tt=np.geomspace(tsw,t[-1],300)
    return dict(Yp_He=4*h4,D_H=d/p,He3_H=(h3+tr)/p,Li_H=(li+be)/p,Be_frac=be/(li+be),ok=sol.success,T=np.array([Ti(x) for x in tt]),Y=sol.sol(tt))
