"""D788 (locked PREREG_D788). AI-assisted."""
import math
MP=2.435e18; pref=(90/(math.pi**2*106.75))**0.25
Lmax=lambda M,T: (pref**2*MP*M**5/(192*math.pi**3*T**2))**0.25
for M in (4.3e11,1e12):
    for T in (1e5,3e6):
        L=Lmax(M,T); e=(M/L)**2/(8*math.pi); req=8.75e-11/(0.75*T/M)
        print(f"(a) M={M:.1e} T2={T:.0e}: Lambda={L:.2e}, eps_max(dim6)={e:.1e}, eps_req={req:.1e} -> {'OK' if e>=req else 'FAIL'}")
print("(b) P5 mediator: y needed for eps_req range:")
for req in (2e-5,1.2e-3):
    y=math.sqrt(8*math.pi*req); print(f"   eps_req={req:.0e}: y >= {y:.3f}")
for M in (4.3e11,1e12):
    for T in (1e5,3e6):
        L=Lmax(M,T)
        for y in (0.05,0.2,1.0):
            print(f"   M={M:.1e} T2>={T:.0e}: Lambda_eff<={L:.2e} -> M_X <= {L*y:.2e} for y1=y2={y}")
