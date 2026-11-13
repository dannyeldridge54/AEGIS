"""Development 59 (exploratory): the Twist's primordial gravitational-wave background today. AI-assisted.
Standard radiation-era transfer (e.g. Watanabe & Komatsu 2006 form): Omega_GW h^2 ~ (3/128) Omega_r h^2 A_t (g*/g0)^(-1/3)-type
estimate; here Omega_GW h^2 = (1/24) Omega_r h^2 r A_s (g_*/g_*0)^(-1/3) (f/f_*)^(n_t), n_t = -r/8 (consistency),
with Omega_r h^2 = 4.18e-5. Kination after the cliff (N_k ~ 2 at the derived heat share) boosts only modes entering
before radiation domination: f > f_RH ~ 2.6e-8 Hz (T_RH/GeV) (g/106.75)^(1/6) ~ 1e7 Hz. Order-of-magnitude."""
import math
As, Orh2 = 2.1e-9, 4.18e-5
for r in (0.0034, 0.0040):
    base = Orh2 * r * As / 24 * (106.75 / 3.36) ** (-1 / 3)
    for f, lab in ((1e-3, "LISA"), (0.1, "DECIGO/BBO"), (100, "LIGO/ET")):
        nt = -r / 8; om = base * (f / 7.7e-17) ** nt
        print(f"r {r}: Omega_GW h^2 at {lab} ({f:g} Hz) ~ {om:.1e}")
for T in (3e14, 5e14):
    print(f"kination boost starts at f ~ {2.6e-8 * T:.0e} Hz (T_RH {T:.0e} GeV), max factor ~ e^(N_k) ~ 10")
print("Reach (rough): LISA ~1e-13, BBO ~1e-17, DECIGO ~1e-18, ET ~1e-12")
