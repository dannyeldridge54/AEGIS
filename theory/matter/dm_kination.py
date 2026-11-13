"""Development 85 (estimate): kination after the cliff suppresses gravity-only dark-matter production from the bath.
PIDM freeze-in (pidm_abundance.py) assumed radiation domination from T_RH down. In the Twist the bath forms during
kination: H is larger than radiation alone gives, by sqrt(1 + rho_k/rho_r), rho_k/rho_r = (T/T_RH)^2 / f_eff.
For UV freeze-in (rate R ~ T^8/M_P^4, m << T) the yield is dY ~ T^4/H dT, so
    Y_kin / Y_rad = int_0^1 t^2 / sqrt(1 + t^2/f_eff) dt / (1/3).
f_eff, the radiation share when the bath forms, is taken from the kination e-folds of D84 (dN = 1/4 ln(1/f_eff)
for pure kination: 1.94 -> f_eff = 4.3e-4; range from 0.04-0.4% heat). On the light branch Omega ~ m Y, so the
dark-matter mass needed rises by Y_rad/Y_kin. AI-assisted; an estimate (no full Boltzmann run)."""
import math
from scipy.integrate import quad
for dN, lab in ((2.23, "heat 0.04%"), (1.94, "heat 0.13%"), (1.66, "heat 0.4%")):
    f = math.exp(-4 * dN); r = quad(lambda t: t * t / math.sqrt(1 + t * t / f), 0, 1)[0] * 3
    print(f"{lab}: f_eff {f:.1e}, yield suppressed x{1 / r:.0f}; light-branch DM mass 3.5e6-1.9e7 GeV -> "
          f"{3.5e6 / r:.1e}-{1.9e7 / r:.1e} GeV (still far below T_RH)")
