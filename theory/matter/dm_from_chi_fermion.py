"""Development 106 numbers (estimate): dark matter from the decays of chi's fermion partner.
(1) Number: instant preheating makes bosons and fermions alike at the crossing (occupation exp(-pi k^2/(g phidot)) for both,
    Greene-Kofman / Peloso-Sorbo); in the chi multiplet the complex scalar (2 dof) and the Majorana fermion (2 dof) are made in
    equal numbers, with equal mass g|phi - phi0|. So n_chitilde ~ n_chi.
(2) chi decays to the Higgs (D105) making the bath: rho_r = rho_chi = n m_chi; chitilde's own decay doubles it.
    n_chitilde / s = n / ((4/3) * 2 rho_chi / T) = (3/8) T / m_chi.
(3) Branching to a dark-matter pair through a virtual graviton: ~ (m_chi/M_P)^2 / (16 pi^2 * C), C ~ 3-30 (phase space).
Dark matter today: rho_DM/s = 0.44 eV -> m_DM = 0.44e-9 GeV / (n_DM/s). AI-assisted, order of magnitude."""
import math
MP = 2.435e18; T = 4e14; m = 0.052 * MP
ns = 3 / 8 * T / m
for C in (3, 10, 30):
    BR = (m / MP) ** 2 / (16 * math.pi ** 2 * C); nDM = ns * BR
    print(f"C {C}: chi-tilde n/s {ns:.1e}, BR {BR:.1e}, n_DM/s {nDM:.1e} -> m_DM for the observed amount {0.44e-9 / nDM:.2f} GeV")
