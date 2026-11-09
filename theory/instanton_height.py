"""Numbers for theory/INSTANTON_HEIGHT.md (V5, 9 Nov 2026). Order-of-magnitude bookkeeping, not a derivation.
Heights from V = Lambda^4 (1 - cos(d/F)) with m^2 = Lambda^4/F^2; instanton height Lambda^4 = 2 K e^-S."""
import json, math
MP = 2.435e27            # reduced Planck mass, eV
F = 1.559 * MP           # late width, Nieh-Yan derivation
masses = {"Pantheon+": 1.41e-25, "DES-Dovekie": 1.26e-25, "Union3": 1.45e-25}   # spiral_l_score.json (approx.)
GS = math.pi * math.sqrt(6) / 4       # Hebecker et al. 2016 eq. 4.20: S = GS * n * M_P / f
KS = math.pi / (3 * math.sqrt(2))     # Kaul & Sengupta: S = KS * F_a * Q
out = {"late": {}}
for k, m in masses.items():
    L4 = m * m * F * F
    S = {f"K=M_P^4/10^{j}": math.log(2 * MP**4 / 10**j / L4) for j in (0, 4, 8)}
    out["late"][k] = {"m_eV": m, "Lambda4_eV4": L4, "S_needed": S}
S0 = sum(v["S_needed"]["K=M_P^4/10^0"] for v in out["late"].values()) / 3
out["S_from_GS_n1_at_F"] = GS * MP / F
out["f_for_S_n1_over_MP"] = GS / S0
out["n_for_S_at_F"] = S0 / (GS * MP / F)
out["KS_Fa_for_S_Q1"] = S0 / KS
out["KS_beta_for_S"] = (S0 / KS) ** 2 + 1 / 8
out["KS_Fa_at_F_via_GS_match"] = (GS / KS) * MP / F
out["KS_beta_at_F"] = out["KS_Fa_at_F_via_GS_match"] ** 2 + 1 / 8
# early role: Locked Twist, n = 3, stored edelockP (Pantheon+)
h, Om, zc, fde, th = 0.7053, 0.3002, 3553.83, 0.0780, 2.7736
rho_c0 = 8.096e-11 * h * h            # eV^4
rho_m0 = Om * rho_c0
omr = 4.18e-5 / (h * h) * (1 + 0.2271 * 3.044) / (1 + 0.2271 * 3.046)  # radiation incl. neutrinos (approx.)
rho_zc = rho_m0 * (1 + zc)**3 + omr * rho_c0 * (1 + zc)**4
V_ede = fde / (1 - fde) * rho_zc
L4e = V_ede / (1 - math.cos(th))**3
out["early"] = {"rho_total_zc_eV4": rho_zc, "V_EDE_zc_eV4": V_ede, "Lambda4_eV4": L4e,
                "S_needed_K=M_P^4": math.log(2 * MP**4 / L4e)}
out["late_S_mean_K=M_P^4"] = S0
out["dS_early_minus_late"] = out["early"]["S_needed_K=M_P^4"] - S0
json.dump(out, open("instanton_height.json", "w"), indent=1)
print(json.dumps(out, indent=1))
