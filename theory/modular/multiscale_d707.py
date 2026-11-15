"""D710 (locked PREREG_D707_MULTISCALE): SERAPIS multi-scale tests. AI-assisted."""
import math, numpy as np, camb
from scipy.special import erfc
from scipy.integrate import quad
BAND=(0.970,0.975); NS=0.9725; R=5e-4; AL=-1.0e-3; BE=-3.8e-5; AS=2.1e-9
print("T1 n_s by release (band 0.970-0.975)")
for name,c,s in (("WMAP9 2012",0.972,0.013),("Planck 2013",0.9603,0.0073),("Planck 2015",0.9655,0.0062),("Planck 2018",0.9649,0.0042),("P-ACT-LB 2025",0.974,0.003),("SPA Dec2025",0.9682,0.0032),("SPA+DESI Dec2025",0.9728,0.0029)):
    near=0 if BAND[0]<=c<=BAND[1] else min(abs(c-BAND[0]),abs(c-BAND[1]))/s
    far=max(abs(c-BAND[0]),abs(c-BAND[1]))/s
    print(f"  {name}: {c}±{s}  nearest-edge {near:.2f}σ, far-edge {far:.2f}σ, centre {(NS-c)/s:+.2f}σ")
print("T2 running (pred -1.0e-3, band -0.85..-1.06e-3)")
for name,c,s in (("Planck 2018",-0.0045,0.0067),("ACT DR6",0.0062,0.0052),("ACT+P+SPT",0.0080,0.0057),("Planck+eBOSS Lya",-0.0108,0.0022)):
    print(f"  {name}: {c}±{s}  pull {(AL-c)/s:+.2f}σ")
print("T3 neutrino mass sum (NO, m1=0)")
m2=math.sqrt(7.41e-5); m3=math.sqrt(2.51e-3); S=m2+m3
print(f"  m2={m2:.4f} m3={m3:.4f} sum={S:.4f} eV")
for name,L in (("Planck 2018",0.12),("DESI DR1+CMB",0.072),("DESI DR2+CMB",0.0642),("DESI DR2 FC",0.053)):
    print(f"  {name} < {L}: {'PASS' if S<L else 'EXCLUDED'} (margin {L-S:+.4f} eV)")
print("T4 Lyman-alpha (z=3, k_p=0.009 s/km): data D2=0.310±0.020, n=-2.340±0.006")
def run(ns,a=0.0,b=0.0,kmax=300):
    p=camb.CAMBparams(); p.set_cosmology(H0=67.4,ombh2=0.0224,omch2=0.120,mnu=0.06)
    p.InitPower.set_params(As=AS,ns=ns,nrun=a,nrunrun=b,pivot_scalar=0.05)
    p.set_matter_power(redshifts=[10.0,3.0],kmax=kmax); p.NonLinear=camb.model.NonLinear_none
    res=camb.get_results(p); return p,res
out={}
for name,ns,a,b in (("LCDM P18",0.9649,0,0),("SERAPIS low",0.970,-0.94e-3,-3.8e-5),("SERAPIS mid",0.9725,-1.0e-3,-3.8e-5),("SERAPIS high",0.975,-1.06e-3,-3.8e-5),("SERAPIS mid no-run",0.9725,0,0)):
    p,res=run(ns,a,b)
    kh,z,pk=res.get_matter_power_spectrum(minkh=1e-3,maxkh=200,npoints=800)
    h=0.674; Hz=res.hubble_parameter(3.0)  # km/s/Mpc
    kp=0.009*Hz/(1+3.0)  # 1/Mpc
    iz=list(z).index(3.0); k=kh*h; P=pk[iz]/h**3
    lnk=np.log(k); lnD=np.log(k**3*P/(2*np.pi**2))
    f=lambda x: np.interp(x,lnk,lnD)
    D2=math.exp(f(math.log(kp))); nL=(f(math.log(kp)+0.01)-f(math.log(kp)-0.01))/0.02-3
    # sigma(M) at z=10 (top-hat), Om h^2 rho
    iz10=list(z).index(10.0); P10=pk[iz10]/h**3
    rho=2.775e11*h**2*(0.0224+0.120+0.06/93.14)/h**2*h**2  # M_sun/Mpc^3 (Omega_m rho_crit)
    sig={}
    for M in (1e9,1e10,1e11):
        Rr=(3*M/(4*np.pi*rho))**(1/3); x=k*Rr; W=3*(np.sin(x)-x*np.cos(x))/x**3
        sig[M]=math.sqrt(np.trapezoid(k**3*P10*W**2/(2*np.pi**2),lnk))
    out[name]=(D2,nL,sig)
    print(f"  {name}: k_p={kp:.3f}/Mpc Delta2_L={D2:.4f} (pull {(D2-0.310)/0.020:+.2f}) n_L={nL:.4f} (pull {(nL+2.340)/0.006:+.2f})")
print("T5 early halos z=10, Press-Schechter n(>M) ratio vs LCDM P18")
base=out["LCDM P18"][2]
for name in out:
    s=out[name][2]
    print("  "+name+": "+"; ".join(f"M={M:.0e}: sigma={s[M]:.4f} ratio={erfc(1.686/s[M]/math.sqrt(2))/erfc(1.686/base[M]/math.sqrt(2)):.3f}" for M in s))
print("T6 mu-distortion (estimate, Taylor spectrum, Chluba-type window)")
def D2T(k,ns,a,b):
    L=math.log(k/0.05); return AS*math.exp((ns-1)*L+a/2*L*L+b/6*L**3)
Wmu=lambda k:2.27*(math.exp(-(k/1360)**2/(1+(k/260)**0.3+k/340))-math.exp(-(k/32)**2))
mu=lambda ns,a,b: quad(lambda lk: D2T(math.exp(lk),ns,a,b)*Wmu(math.exp(lk)),math.log(1),math.log(1e5),limit=200)[0]
m0=mu(0.9649,0,0)
for name,ns,a,b in (("LCDM",0.9649,0,0),("SERAPIS low",0.970,-0.94e-3,-3.8e-5),("SERAPIS mid",0.9725,-1.0e-3,-3.8e-5),("SERAPIS high",0.975,-1.06e-3,-3.8e-5)):
    v=mu(ns,a,b); print(f"  {name}: mu={v:.3e} ratio={v/m0:.3f}")
print("T7 f_NL local =",[round(5/12*(1-n),4) for n in BAND],"vs Planck -0.9±5.1: pull",[round((5/12*(1-n)+0.9)/5.1,2) for n in BAND])
print("T8 GW energy density today")
fs=0.05*2.998e8/(2*math.pi*3.086e22)
for name,f in (("PTA 1e-8 Hz",1e-8),("LISA 3e-3 Hz",3e-3),("DECIGO/BBO 0.1 Hz",0.1)):
    print(f"  {name}: Omega_GW h^2 = {4.2e-5/24*0.389*R*AS*(f/fs)**(-R/8):.2e}  (f*={fs:.2e} Hz)")
print("T9 PBH: P_R(end)/P_R* ~ eps*/eps_end =",R/16,"-> P_R(end) ~",AS*R/16,"vs ~1e-2 needed")
print("T10 m_bb (NO, m1=0)")
s12,s13=0.303,0.0222; a_=m2*s12*(1-s13); b_=m3*s13
print(f"  |m2 s12^2 c13^2 ± m3 s13^2| in [{abs(a_-b_)*1e3:.2f}, {(a_+b_)*1e3:.2f}] meV")
