"""D752 (locked PREREG_D752). AI-assisted; estimates labelled."""
import math
MP=2.435e18; Vs=4.8e15**4; rho_end=Vs/2; lnk=5.404; g=106.75
N0=67-lnk+0.25*math.log(Vs**2/(MP**4*rho_end))-(1/12)*math.log(g)
print(f"instant-reheating N* = {N0:.2f}  (attractor n_s = {1-2/N0:.4f})")
for fac in (1/3,1,3):
    flat=3.6e-16*(5e-4/0.1)*fac; boost_max=1.1e-6/flat
    lnratio=3*math.log(boost_max); dN=lnratio/12; N=N0+dN; ns=1-2/N
    Tk=(rho_end*math.exp(-lnratio)*30/(math.pi**2*g))**0.25
    print(f"Omega_flat x{fac:.2f}: max rho_end/rho_k = e^{lnratio:.1f}, kination ends at T ~ {Tk:.1e} GeV, max dN* = {dN:.2f}, N*max = {N:.2f}, attractor n_s max = {ns:.4f}; "
          f"gap to 0.970: {(0.970-ns)/0.0016:.1f} sigma (1-sigma reading) / {(0.970-ns)/0.0008:.1f} (95% reading); at central 0.972: {(0.972-ns)/0.0016:.1f} / {(0.972-ns)/0.0008:.1f}")
