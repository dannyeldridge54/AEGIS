"""D534 (locked PREREG_D534_STIFF_ROOM). AI-assisted."""
import math
MP=2.435e18; As=2.1e-9; r=0.0012; TRH=5.5e10
Vs=1.5*math.pi**2*As*r*MP**4; Ve=0.1*Vs; phi=MP
mmin=(TRH**2*MP)**(1/3)
print(f"V*^(1/4)={Vs**0.25:.2e} GeV, V_end^(1/4)={Ve**0.25:.2e} GeV, m_min={mmin:.2e} GeV")
for lab,m in (("SERAPIS-1",4.0e13),("m_min",mmin)):
    q=0.5*m*m*phi*phi; print(f"{lab}: m={m:.2e}: quadratic term at phi_end = {q:.2e} vs V_end = {Ve:.2e} -> ratio {q/Ve:.1f}")
q=0.5*mmin**2*phi**2
if q<Ve:
    # sextic dominates at phi_end; choose phi_c with V_end = (m^2/2)phi^2 (phi/phi_c)^4
    pc=phi*(q/Ve)**0.25; rc=mmin**2*pc**2; print(f"PASS: phi_c={pc/MP:.2f} M_P, max N* gain = {math.log(Ve/rc)/9:.2f}")
else: print("FAIL: quadratic term already exceeds V_end at m_min -> no stiff phase; trade-off is sharp")
