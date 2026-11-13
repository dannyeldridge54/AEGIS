"""Development 91: can the tail field screen itself (chameleon-style) so Cassini/MICROSCOPE are safe? AI-assisted.
Effective potential V(phi) + rho e^{beta phi} with V = V0 e^{-lam phi} (the Twist's tail, lam = sqrt(2/3)) and matter coupling
beta (D90: ~0.41 for the sequestered form). At density rho the minimum has lam V = beta rho e^{beta phi}, and the mass there is
m^2 = lam (lam + beta) V_min ~ beta (lam + beta) rho / M_P^2 (units M_P = 1 for phi). Thin-shell screening of a body needs its
Compton wavelength inside it to be much smaller than its radius (Khoury-Weltman); for the Sun and Earth we compare."""
import math
G = 6.674e-11; c = 2.998e8
lam, beta = math.sqrt(2 / 3), 0.41
for name, rho, R in (("Sun (mean)", 1410.0, 6.96e8), ("Earth (mean)", 5510.0, 6.37e6), ("interplanetary", 1e-20, None)):
    m2 = beta * (lam + beta) * 8 * math.pi * G * rho          # s^-2  (rho/M_P^2 with M_P^-2 = 8 pi G)
    lc = c / math.sqrt(m2)                                     # Compton wavelength, m
    txt = f"radius {R:.1e} m -> {'screened' if R and lc < 0.01 * R else 'NOT screened'}" if R else "free space"
    print(f"{name}: Compton wavelength {lc:.1e} m ({lc / 1.496e11:.1e} AU); {txt}")
