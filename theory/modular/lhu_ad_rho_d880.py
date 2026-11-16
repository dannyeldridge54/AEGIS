"""D880 (locked PREREG_D880). LH_u AD at rho with late reheating T2. AI-assisted."""
target=8.7e-11
for T2 in (1e5,3e5,1e6):
    for m32 in (2.5e5,7e5):
        for d in (0.1,1.0):
            pre=1e-11*d*(m32/1e3)*min(1.0,(T2/1e8)**(1/3))
            m=1e-8*(pre/target)**(2/3)
            print(f"T2={T2:.0e} m32={m32:.1e} delta={d}: required m_nu1={m:.2e} eV")
