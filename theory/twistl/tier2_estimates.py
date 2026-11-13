"""Tier 2 (3) the cliff's gravitational-wave burst and small-scale features; (4) TWIST-L's quantum stability. AI-assisted, estimates.
(3) Instant preheating at the crossing: chi modes with k ~ sqrt(g phi_dot) are made in a burst; GWs sourced at that scale.
    Today's frequency f0 = (k/2pi) (a_e/a_0), a_e/a_0 = (T0/T_RH)(g0s/g*s)^{1/3}; amplitude Omega_GW h^2 ~ Omega_r h^2 (rho_chi/rho)^2 (aH/k)^2.
(4) Loops: S (m_S^2 >= 8 H^2) and gravitons give Coleman-Weinberg dV ~ m^4/(64 pi^2); relative to V ~ 3 H^2 M_P^2. The log factor's own
    next (two-loop) correction for a running coupling is ~ (b2/b1^2) g^2 ln ln / ln ~ 10% of the log term -> shifts b along the locked curve."""
import math
MP, H, g = 2.435e18, 1.5e13, 0.1
phid = math.sqrt(6) * H * MP                  # kination: phi_dot ~ sqrt(6) H M_P
k = math.sqrt(g * phid)
TRH, T0, gs = 4e14, 2.35e-13, 106.75
ratio = (T0 / TRH) * (3.91 / gs) ** (1 / 3)
f0 = k / (2 * math.pi) * ratio * 1.519e24       # GeV -> Hz
for share in (0.008, 0.0055):
    Ogw = 4.2e-5 * share ** 2 * (H / k) ** 2
    print(f"(3) heat share {share}: GW burst today at f ~ {f0:.1e} Hz with Omega_GW h^2 ~ {Ogw:.0e} (BBN/N_eff limit ~1e-6; ultra-high-frequency proposals need >~1e-1 at GHz)")
print("    small-scale lumps: the cliff acts ~0 e-folds before the end, on scales ~1/(a_e H_e) — far below any astrophysical scale; no PBHs of interest")
for mS2 in (8, 22):
    dV = (mS2 * (H / MP) ** 2) ** 2 / (64 * math.pi ** 2) / (3 * (H / MP) ** 2)
    print(f"(4) S loop (m_S^2 = {mS2} H^2): dV/V ~ {dV:.0e}")
print(f"(4) graviton loops: dV/V ~ H^2/M_P^2 ~ {(H/MP)**2:.0e}")
print("(4) two-loop correction to the running coupling behind the log factor: ~10% change in the effective b -> moves the prediction along the locked n_s-r curve, not off it")
