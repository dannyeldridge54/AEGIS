# DEVIATIONS A3f — compact.tov absolute pressure tolerance (written before any rerun) — 2026-11-17
D1: compact.tov hard-coded atol = [P_c·1e-16, 1e-30]. For realistic neutron stars, P_c·1e-16 is 0.4–5× the surface pressure, so the event radius was uncontrolled (D1090, diagnostic CONFIRMED: with P_c·1e-30 the radius agrees with ns.tov_tidal to 3e-13–8e-11).
Change: the default atol for P becomes P_c·1e-30. No other change. The unused `atol` argument stays as is.
This affects the A0/A0s TOV checks (uniform-density Schwarzschild, n = 1 polytrope, Oppenheimer–Volkoff 0.7102 M_⊙) and A3a–A3d N4. All are re-run under PREREG_A3f.
