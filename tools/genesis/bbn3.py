# (c) Danny Lee Eldridge · AEGIS Community License
"""BBN v3 (lock PREREG_GENESIS_BBN3): v2 background + weak rates, 6-species network with SKM-1993 rates."""
import math, numpy as np
from scipy.integrate import solve_ivp
from tools.genesis.bbn2 import background, rates, MN, BD, HBARC, NA
K9=1/0.0861733   # T9 per MeV
def skm(T9, s=1.0):
    T=T9; t3=T**(1/3); t23=t3*t3; t43=T*t3; t53=T*t23
    r=dict(
    npg=4.742e4*(1-0.8504*math.sqrt(T)+0.4895*T-0.09623*T**1.5+8.471e-3*T*T-2.80e-4*T**2.5),
    dpg=s*2.65e3*T**(-2/3)*math.exp(-3.720/t3)*(1+0.112*t3+1.99*t23+1.56*T+0.162*t43+0.324*t53),
    ddn=s*3.95e8*T**(-2/3)*math.exp(-4.259/t3)*(1+0.098*t3+0.765*t23+0.525*T+9.61e-3*t43+0.0167*t53),
    ddp=s*4.17e8*T**(-2/3)*math.exp(-4.258/t3)*(1+0.098*t3+0.518*t23+0.355*T-0.010*t43-0.018*t53),
    he3np=7.21e8*(1-0.508*math.sqrt(T)+0.228*T),
    tdn=s*(1.063e11*T**(-2/3)*math.exp(-4.559/t3-(T/0.0754)**2)*(1+0.092*t3-0.375*t23-0.242*T+33.82*t43+55.42*t53)+8.047e8*T**(-2/3)*math.exp(-0.4857/T)),
    he3dp=s*(5.021e10*T**(-2/3)*math.exp(-7.144/t3-(T/0.270)**2)*(1+0.058*t3+0.603*t23+0.245*T+6.97*t43+7.19*t53)+5.212e8/math.sqrt(T)*math.exp(-1.762/T)))
    return {k:v/NA for k,v in r.items()}   # <sigma v> in cm^3/s
def run(eta=6.127e-10, dneff=0.0, s=1.0, Tsw=0.2):
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
        n,p,d,tr,h3,h4=y; Tm=Ti(tt); B=nbi(tt); r=skm(Tm*K9,s); lnp,lpn=lam(tt)
        R_np=B*r['npg']*n*p; R_g=lgam(Tm,r['npg'])*d
        R_dp=B*r['dpg']*d*p; R_ddn=0.5*B*r['ddn']*d*d; R_ddp=0.5*B*r['ddp']*d*d
        R_hn=B*r['he3np']*h3*n; R_td=B*r['tdn']*tr*d; R_hd=B*r['he3dp']*h3*d
        dn=-lnp*n+lpn*p-R_np+R_g+R_ddn-R_hn+R_td
        dp=lnp*n-lpn*p-R_np+R_g-R_dp+R_ddp+R_hn+R_hd
        dd=R_np-R_g-R_dp-2*R_ddn-2*R_ddp-R_td-R_hd
        dt=R_ddp+R_hn-R_td
        dh3=R_dp+R_ddn-R_hn-R_hd
        dh4=R_td+R_hd
        return [dn,dp,dd,dt,dh3,dh4]
    tsw=float(np.interp(-Tsw,-T,t)); X0=1/(1+math.exp(1.2933/T[0]))
    sa=solve_ivp(lambda tt,y:[-lam(tt)[0]*y[0]+lam(tt)[1]*(1-y[0])],(t[0],tsw),[X0],method='BDF',rtol=1e-8,atol=1e-14)
    n0=sa.y[0,-1]; Tm=Ti(tsw); r=skm(Tm*K9,s); d0=nbi(tsw)*r['npg']*n0*(1-n0)/lgam(Tm,r['npg'])
    sol=solve_ivp(f,(tsw,t[-1]),[n0,1-n0-d0,d0,0,0,0],method='BDF',rtol=1e-7,atol=1e-18,dense_output=True)
    n,p,d,tr,h3,h4=sol.y[:,-1]
    tt=np.geomspace(tsw,t[-1],300); Y=sol.sol(tt)
    return dict(Yp_He=4*h4, D_H=d/p, He3_H=(h3+tr)/p, ok=sol.success, T=np.array([Ti(x) for x in tt]), Y=Y)
