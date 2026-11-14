"""D412 (locked PREREG_D412_PART5): Part 5 (capture/pinning) — dark radiation from the light U(1)_X-charged decay products of x (D407 condition i). AI-assisted.
Species decoupled from the SM bath at T_dec ≫ 100 GeV: ΔN_eff = (4/7) g_eff (10.75/g*_dec)^{4/3}, g_eff = bosons + 7/8 fermions (internal dof)."""
cases = {"1 Weyl fermion (2 dof)": 2 * 7 / 8, "1 Dirac fermion (4 dof)": 4 * 7 / 8, "1 complex scalar (2 dof)": 2.0,
         "massless dark photon (2 dof)": 2.0, "chiral U(1)_X anomaly-free minimum: 3 Weyl (6 dof)": 6 * 7 / 8}
for gdec, lab in ((106.75, "SM g*"), (228.75, "MSSM g*")):
    print(f"decoupling with {lab} = {gdec}")
    for k, g in cases.items():
        d = (4 / 7) * g * (10.75 / gdec) ** (4 / 3)
        print(f"   {k:52s} ΔN_eff = {d:.3f}   vs ACT P-ACT < 0.14 (95%): {'OK' if d < 0.14 else 'EXCLUDED'}")
