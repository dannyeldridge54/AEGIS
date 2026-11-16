"""D783 (locked PREREG_D783). AI-assisted."""
import math
MP=2.435e18; gs_=106.75; Yobs=8.75e-11; pref=(90/(math.pi**2*gs_))**0.25
T2=lambda M,L: pref*math.sqrt(M**5/(192*math.pi**3*L**4)*MP)
Lmax=lambda M,T: (pref**2*MP*M**5/(192*math.pi**3*T**2))**0.25
print("(a) T2 [GeV] grid:")
for M in (4.3e11,7.1e11,1e12):
    print(f"  M={M:.1e}: "+", ".join(f"L={L:.0e}->{T2(M,L):.2e}" for L in (1e15,3e15,1e16,3e16,1e17,2.4e18)))
    print(f"     Lambda_max(T2>=1e5)={Lmax(M,1e5):.2e}  Lambda_max(T2>=3e6)={Lmax(M,3e6):.2e}")
print("M_s estimate (M_P g_s^{1/4}/sqrt(4 pi V), V=(Im rho)^1.5):")
for P in (375,975):
    for g in (0.1,0.5):
        rho=P*g; V=rho**1.5; Ms=MP*g**0.25/math.sqrt(4*math.pi*V)
        print(f"  ImS*Imrho={P} g_s={g}: Im rho={rho:.1f}, V={V:.0f}, M_s={Ms:.2e}")
print("(b) required epsilon:")
for M in (4.3e11,1e12):
    for T in (1e5,3e6):
        for lab,k in (("L-violating",28/79),("B-violating",1.0)):
            e=Yobs/(k*0.75*T/M); print(f"  M={M:.1e} T2={T:.0e} {lab}: eps_req={e:.2e} {'<=0.04 plausible' if e<=0.04 else 'TOO LARGE'}")
