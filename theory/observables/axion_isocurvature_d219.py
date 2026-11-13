"""D219: strong CP alongside the Twist — what kind of QCD axion is allowed with H_inf = 1.5e13 GeV (r = 0.0036)? AI-assisted estimate.
Pre-inflationary axion (PQ broken during inflation): quantum spread dtheta = H/(2 pi f); isocurvature S = 2 (Om_a/Om_c) dtheta/theta with
Om_a/Om_c = (theta/theta_DM)^2 and theta_DM(f) from the standard misalignment estimate Om_a h^2 ~ 0.12 (f/9e11 GeV)^1.165 theta^2.
Planck: P_S/P_R < ~0.04 -> S_rms < 9.2e-6 (P_R = 2.1e-9)."""
import math
H = 1.5e13; Smax = math.sqrt(0.04 * 2.1e-9)
print(f"H_inf = {H:.1e} GeV; isocurvature limit S_rms < {Smax:.1e}")
for f in (1e10, 1e12, 1e14, 1e16):
    th_dm = min(math.pi, math.sqrt((9e11 / f) ** 1.165))       # theta giving all of the dark matter
    dth = H / (2 * math.pi * f)
    # largest theta allowed by isocurvature: S = 2 theta^2/th_dm^2 * dth/theta = 2 theta dth/th_dm^2
    th_max = Smax * th_dm ** 2 / (2 * dth)
    frac = (max(th_max, 0) / th_dm) ** 2
    ok = "theta below its own quantum spread -> excluded" if th_max < dth else f"axion DM fraction <= {min(frac,1):.1e}"
    print(f"f = {f:.0e} GeV: dtheta = {dth:.1e}, theta_DM = {th_dm:.2e}, isocurvature theta_max = {th_max:.1e} -> {ok}")
print("PQ restored during inflation needs f < ~H_inf ~ 1e13 GeV (and post-inflation dynamics): post-inflation axion DM, m_a ~ 40-180 ueV (lattice, Buschmann et al. 2021);")
for f in (1e10, 1e11):
    print(f"   f = {f:.0e} GeV -> m_a = {5.7e-6 * 1e12 / f * 1e6:.0f} ueV")
