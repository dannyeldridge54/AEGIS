# AEGIS-FP 3BRUZ3HI2AJR3UAO · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Level 6: N* from the matching equation (Planck 2018 X eq. 47 form, as used in D719; w = 0 between end of inflation and reheating).
N* = 67 - ln(k/a0H0) + 1/4 ln(V*^2/(M_P^4 rho_end)) + 1/12 ln(rho_th/rho_end) - 1/12 ln(g*)."""
import math
MP = 2.435e18; AS = 2.1e-9
def Nstar(r, V_ratio_star_end, TR, g=106.75, k=0.05, H0=67.4):
    lnk = math.log(k/(H0/299792.458))
    Vs = 1.5*math.pi**2*AS*r*MP**4; rho_end = 1.5*Vs/V_ratio_star_end; rho_th = math.pi**2/30*g*TR**4
    return 67-lnk+0.25*math.log(Vs**2/(MP**4*rho_end))+(1/12)*math.log(rho_th/rho_end)-(1/12)*math.log(g)
