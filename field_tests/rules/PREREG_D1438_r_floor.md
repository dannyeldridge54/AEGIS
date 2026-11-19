# PREREG D1438 — does the SERAPIS r floor (band r 4.55–5.7e-4) get detected by 2030s B-mode surveys?

Locked 2026-11-19 (UTC) before computing (JANUS tick 34). Node: band_e (frozen). Band r 4.55e-4 … 5.7e-4 (D1399/D1428);
exact points ρ A1 r = 4.82095e-4, τ = i NA12 r = 4.8335e-4.
Forecasts [literature]: arXiv:2212.04115 Table 5, "Forecast upper limits on r at 95 % confidence level", fiducial r = 0 (Table 1),
10⁴ r<: SO 99, SO+SPHEREx 98, S4 34, S4+SPHEREx 33, LiteBIRD 0.98, LiteBIRD+S4(ℓ>200) 0.98, +CHIME+SPHEREx 0.97.
Method [estimate]: Gaussian, one-sided 95 % ⇒ σ(r) = UL/1.645 (one-sided; stated). Also report the two-sided reading UL/1.96 as a bracket.
Significance S = r/σ(r) at r = 4.55e-4, 4.82e-4, 5.7e-4. Detection threshold 3σ (evidence), 5σ (discovery).
Caveat stated up front: σ at fiducial r = 0 ignores tensor cosmic variance at r ≠ 0 and delensing details ⇒ S is an upper-ish estimate.
Verdict rule: band "testable by r" if the weakest point (4.55e-4) reaches ≥ 3σ with the best survey; "decided by r" if ≥ 5σ.
A non-detection by LiteBIRD at r < 1e-4 (95 %) would KILL band_e/band_i (r floor). No reruns; fixes only via PREREG_D1438_DEVIATIONS.md first.
