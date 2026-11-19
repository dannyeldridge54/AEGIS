# (c) Danny Lee Eldridge · AEGIS Community License
"""Weave matter-genesis toolkit (D1632). Textbook-level physics, labelled [toy] where simplified.
P-M: one asymmetry shared by visible baryons and a mirror dark baryon (asymmetric dark matter)."""
import math, numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
ZETA3=1.2020569031595942; MP_GEV=0.938272; MN_MEV=939.565; ME_MEV=0.51099895
MPL_MEV=1.22091e22          # Planck mass (non-reduced), MeV
TAU_N=878.4; Q=1.2933; B_D=2.2246
K_TO_MEV=8.617333e-11
def eta_from_obh2(obh2=0.02237, Tcmb=2.7255):
    """baryon-to-photon ratio: eta = 273.9e-10 * Omega_b h^2 (for T=2.7255 K)"""
    return 273.9e-10*obh2*(2.7255/Tcmb)**3
def dm_mass(obh2=0.02237, och2=0.1200, sharing=1.0):
    """P-M: m_DM = (Omega_c/Omega_b) m_p / s, s = n_DM/n_B"""
    return (och2/obh2)*MP_GEV/sharing
def gstar(T, dneff=0.0):
    s=0.5*(1+math.tanh((T-0.3)/0.08))
    return 3.36+(10.75-3.36)*s+1.75*dneff
def hubble(T, dneff=0.0):   # 1/s, T in MeV
    H=math.sqrt(8*math.pi**3*gstar(T,dneff)/90)*T*T/MPL_MEV   # MeV
    return H/6.582119569e-22                                     # -> 1/s
def lam_np(T):
    x=Q/T; return 255.0/(TAU_N*x**5)*(12+6*x+x*x)
def bbn(eta, dneff=0.0, T0=10.0, T1=0.03):
    """[toy] neutron fraction X_n(T) and Helium Y_p = 2 X_n(T_D). Returns dict with arrays."""
    def f(lnT, y):
        T=math.exp(lnT); Xn=y[0]; lnp=lam_np(T); lpn=math.exp(-Q/T)*lnp
        dXdt=lpn*(1-Xn)-lnp*Xn-Xn/TAU_N*(1 if T<0.5 else 0)
        dtdlnT=-1/hubble(T,dneff)   # radiation era, T ~ 1/a
        return [dXdt*dtdlnT, dtdlnT]
    Xeq=1/(1+math.exp(Q/T0))
    sol=solve_ivp(f,(math.log(T0),math.log(T1)),[Xeq,0.0],rtol=1e-8,atol=1e-12,dense_output=True)
    # deuterium bottleneck: X_D/(X_n X_p) ~ 6.0*eta*(T/m_N)^{3/2} e^{B_D/T} = 1
    g=lambda T: math.log(6.0*eta*(T/MN_MEV)**1.5)+B_D/T
    TD=brentq(g,0.02,0.5)
    XnD=sol.sol(math.log(TD))[0]; tD=sol.sol(math.log(TD))[1]
    T=np.geomspace(T0,T1,300); Xn=sol.sol(np.log(T))[0]
    return dict(T=T,Xn=Xn,TD=TD,tD=tD,XnD=XnD,Yp=2*XnD)
def saha_xe(z, eta):
    """[toy] hydrogen ionisation fraction from Saha"""
    T=2.7255*(1+z)*K_TO_MEV*1e6   # eV
    me=ME_MEV*1e6; hbarc=1.973269804e-5  # eV cm
    ngam=2*ZETA3/math.pi**2*(T/hbarc)**3; nb=eta*ngam*0.76
    S=(me*T/(2*math.pi))**1.5/hbarc**3*math.exp(-13.6057/T)/nb
    return (-S+math.sqrt(S*S+4*S))/2
def recombination_z(eta, xe=0.5):
    return brentq(lambda z: saha_xe(z,eta)-xe, 500, 3000)
def mirror_dneff(xi):
    """mirror photon + 3 mirror neutrinos at temperature ratio xi (approximation)"""
    return (8/7*(11/4)**(4/3)+3)*xi**4    # = 7.4 xi^4
LADDER=[  # [lit] standard cosmology; times in seconds
 ("quarks -> protons, neutrons",1e-6),("BBN: H, D, He, Li (ionized)",180),("recombination: neutral atoms",380e3*3.156e7),
 ("first stars: C, N, O ... Fe",1.5e8*3.156e7),("mergers: r-process Au, Pt, U (+ brief A>260)",5e8*3.156e7),
 ("AGB stars: s-process Ba, Sr, Pb",1e9*3.156e7),("today",13.8e9*3.156e7)]
def sonify(path, seconds_per_step=1.2):
    """art/analogy only: each ladder step is a note, pitch rising with log(time). Uses tools/sound."""
    from tools.sound import engine as E
    lt=np.log10([t for _,t in LADDER]); f=E.map_series(lt,160,660)
    y=np.concatenate([E.note(fr,seconds_per_step,'triangle',0.4,vib=0.004) for fr in f])
    E.write_wav(path,E.softclip(y)); return path
