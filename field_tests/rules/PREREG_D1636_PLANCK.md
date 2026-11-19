# PREREG D1636 — full-Planck arm (PC job), companion to PREREG_D1636_rt_full_likelihood.md

Locked before any number. Danny 15:55 CT 19 Nov 2026: "Start the other on pc".
Script: cmb-fit/rt_planck_fit.py (helper session). Engine and data identical to the stored cmp_lcdmP* / cmp_w0waP* fits:
CAMB 2.0.5 + Cobaya 3.6.2 (PC venv), Planck 2018 lowl TT + lowl EE + plik-lite TTTEEE + lensing, DESI DR2 BAO (desi_bao_all),
one SN set (Pantheon+ default, Union3, DESY5). Minimiser: bobyqa, best of 4.

Runs (PC queue): gate; rtP; rtP_union3; rtP_desy5; w0waP_desy5 (missing reference).
Model rtP: V = V_L(1 − A e^{−βφ}), A = 7.2983, β = 2√2, frozen at a = 1e-3 with A e^{−βφ_i} = u_i ∈ (1e-6, 0.3]
(u_i ≳ 0.25 rolls into V < 0 before today; such points are rejected); V_L from flatness; w(a) → CAMB PPF table; H₀ sampled
(no θ → H₀ search), other parameters as the stored ΛCDM fits.

Gate (first): rtP at u_i = 1e-6 at the stored ΛCDM best fit must reproduce its χ² within 1.0. If FAIL, the rtP fits are reported as
"engine not validated".
Report per SN set: χ²_min and per-likelihood χ² for rtP, ΛCDM (stored), w₀w_a (stored / new desy5); Δχ² vs ΛCDM; ΔAIC (k = 1 rtP, 2 w₀w_a);
rtP's best u_i and CPL (w₀, w_a) fit over 0 < z < 2.
Verdicts as in PREREG_D1636_rt_full_likelihood.md (ΔAIC < 0 preferred; < −6 strongly; competitive with w₀w_a if AIC within 2).
Caveats stated regardless: post-DESI-DR2 model; V_L set by hand; PPF fluid approximation for the field's perturbations.
Fixes only through PREREG_D1636_PLANCK_DEVIATIONS.md, written before any rerun.
