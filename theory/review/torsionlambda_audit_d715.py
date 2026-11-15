"""D715 (locked PREREG_D715): TorsionΛ background vs Planck 2018 compressed priors. AI-assisted."""
import math
from scipy.integrate import quad
c=299792.458; wb=0.02237
def zstar(wm):
    g1=0.0783*wb**-0.238/(1+39.5*wb**0.763); g2=0.560/(1+21.1*wb**1.81)
    return 1048*(1+0.00124*wb**-0.738)*(1+g1*wm**g2)
def run(name,beta,Om,lam,Or,H0,renorm=False):
    if renorm: lam=1-Or-Om*(1+beta)
    E=lambda z: math.sqrt(Or*(1+z)**4+Om*(1+beta)*(1+z)**3+lam)
    h=H0/100; Omeff=Om*(1+beta); zs=zstar(Omeff*h*h)
    chi=c/H0*quad(lambda z:1/E(z),0,zs,limit=500)[0]
    Rb=lambda z: 3*wb/(4*2.47e-5)/(1+z)   # 3 rho_b / 4 rho_gamma, omega_gamma = 2.47e-5
    rs=c/H0*quad(lambda z: 1/(E(z)*math.sqrt(3*(1+Rb(z)))),zs,1e7,limit=500)[0]
    R_eff=math.sqrt(Omeff)*H0*chi/c; R_bare=math.sqrt(Om)*H0*chi/c; lA=math.pi*chi/rs
    print(f"{name}: E(0)={E(0):.4f} z*={zs:.1f} R(Om_eff)={R_eff:.4f} ({(R_eff-1.7502)/0.0046:+.1f}σ)  R(bare Om, as coded)={R_bare:.4f} ({(R_bare-1.7502)/0.0046:+.1f}σ)  l_A={lA:.2f} ({(lA-301.471)/0.090:+.1f}σ)")
    return R_eff,lA
print("Planck 2018 compressed: R = 1.7502 ± 0.0046, l_A = 301.471 ± 0.090")
run("(a) defaults beta=0, H0=67.4",0,0.315,0.685,9.1e-5,67.4)
run("(a') LCDM check Om=0.3153 h=0.6736",0,0.3153,1-0.3153-9.1e-5,9.1e-5,67.36)
run("(b) beta=0.192, H0=72.95, lambda=0.685 (E(0)!=1)",0.192,0.315,0.685,9.1e-5,72.95)
run("(c) as (b), lambda renormalised",0.192,0.315,0,9.1e-5,72.95,renorm=True)
print("Degeneracy: E depends on (beta, Om) only through Om*(1+beta):")
a=run("  (c') beta=0, Om'=0.315*1.192",0,0.315*1.192,0,9.1e-5,72.95,renorm=True)
