"""D723 (locked PREREG_D723). AI-assisted."""
import math
MP=2.435e18; g=106.75; v=174.0
yDmax=0.07e-9/v; print(f"neutrino bound: y_D < {yDmax:.2e}")
for TR in (6.7e8,6.7e10):
    H=1.66*math.sqrt(g)*TR**2/MP; yth=math.sqrt(8*math.pi*H/TR)
    print(f"T_R={TR:.1e}: thermalisation needs y_D > {yth:.2e}  (ratio needed/allowed = {yth/yDmax:.1e})")
    for TSM in (30,70):
        Br=(TSM/TR)**2; ratio=1/Br
        dil=(10.75/g)**(4/3)            # SM bath heated relative to N2 after reheating (N2 decoupled)
        # at BBN: rho_N2/rho_nu_one_species ; rho_nu_one = (7/8)*2*(pi^2/30)T_nu^4; SM bath rho at T_R = (pi^2/30) g T^4
        # rho_N2/rho_SM,R = ratio ; then scale: rho_N2 ~ a^-4, rho_SM gets entropy boost
        frac_at_BBN = ratio*dil*(g/10.75)          # rho_N2/rho_SM(BBN) with g*(BBN)=10.75
        dNeff = frac_at_BBN*10.75/(7/4)            # rho_SM(BBN) = 10.75 * (pi^2/30)T^4 ; one nu = 7/4 * (pi^2/30)T^4
        print(f"   T_R,SM={TSM} GeV: Br_SM={Br:.1e}, Delta N_eff ~ {dNeff:.1e}")
