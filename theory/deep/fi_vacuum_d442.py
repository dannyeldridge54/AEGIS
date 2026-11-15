import math
from scipy.optimize import minimize_scalar
MP=2.435e18; Ms=0.1*MP; g=0.7
z=lambda x:(math.atan(x/10)-math.atan(x/400))/math.pi-0.3728
for ms in (1e4,1e5):
    V=lambda x:(ms**2*abs(z(x))*Ms**2) if z(x)<0 else (0.5*g**2*z(x)**2*Ms**4)
    r=minimize_scalar(V,bounds=(29.0,30.2),method='bounded',options={'xatol':1e-14})
    vm=V(r.x)
    print(f"m_s={ms:.0e}: x_min={r.x:.12f} zeta={z(r.x):.2e} V_min={vm:.3e} GeV^4 (ratio to 1e26: {vm/1e26:.1e}); V at x_E-1e-3: {V(29.599):.2e}")
    ok=vm<=1e23
print("analytic: V>=0 everywhere and V=0 at zeta=0 (x_E) -> exact minimum 0; grid value limited by float precision")
print("VERDICT:", "REMOVES D427 PIECE" if ok else "KEEPS D427 PIECE")
