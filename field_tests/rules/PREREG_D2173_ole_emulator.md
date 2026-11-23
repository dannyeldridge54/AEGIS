# PREREG D2173 — fast CMB route: OLÉ online-learning emulator in front of CAMB (tool build + validation)
Locked 2026-11-23 ~00:58 CT before installing or computing. Danny 00:54 ("Do that"). Label: TOOL. No verdict of any locked test changes because of this tool.
Source: Günther et al., OLÉ (arXiv:2503.13183; docs ole.readthedocs.io), reported 30–350× speed-up inside Cobaya; trains on our own CAMB outputs, so our thread w(a) is emulated without retraining a public emulator.
Where: Danny's PC (venv312, py3.12; cloud has 2 cores and OLÉ pins jaxlib 0.4.27, unavailable for the cloud Python).
Validation (pre-stated), after the running PC fits finish, on the already-finished pair HiLLiPoP + DESI DR2 + Pantheon+ (L and W), same seeds/settings, BEST_OF=2:
 V1 |chi2_eff(OLÉ) − chi2_eff(CAMB, posted json)| ≤ 0.5 for each model;
 V2 the W−L Δχ²_eff agrees with the posted +2.46 within 0.5;
 V3 wall time ≤ 1/5 of the CAMB run of the same fit.
Adopt (registry 'fast_cmb_ole') only if V1–V3 pass. Even then: exploratory scans and new pairs may use it, but every verdict that goes into a paper is confirmed with plain CAMB. If OLÉ cannot run Cobaya's minimizer, record that and fall back to its MCMC-only use (DEVIATIONS note first).
