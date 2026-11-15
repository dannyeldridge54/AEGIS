# PREREG D439 — does the screening condensate of D438 disturb the inflation plateau? (cycle 26, "pp"; PARTS 2+5 link, CENTRE)
Locked before computing. Toy of D438: ζ(x) = (1/π)[atan(x/10) − atan(x/400)] − 0.3728 (units M_s²).
Model of the residual: φ screens the D-term (D ≈ 0); its Hubble-induced mass c_H H² (c_H ∈ {1, 3}) leaves
δV = c_H H² |ζ(x)| M_s² / Q (Q = 1), with V_inf = 3H²M_P², so δV/V = (c_H/3)|ζ(x)| (M_s/M_P)².
Canonical field: dφ/dx = √(3/2)/x (K = −3 ln(T+T̄), real direction).
Compute at the CMB point x* = 1.3e-4 (and scan x ∈ [1e-5, 1]): δε = ½(d ln(1+δV/V)/dφ)² + cross term with the plateau
slope [√(2ε0)·d(δV/V)/dφ, ε0 from r = 0.0046 → ε0 = r/16], δη = d²(δV/V)/dφ², δn_s = 2δη − 6δε, δr = 16δε.
Cases M_s/M_P ∈ {0.1, 1}.
PASS criteria (all): |δn_s| < 1e-4 (below B1 tolerance), |δr| < 1e-4, max δV/V < 1% for x ≤ 1.
Verdict labels: "SAFE" (all pass at M_s/M_P = 1), "SAFE IF M_s ≤ 0.1 M_P", "DISTURBS".
No reruns to chase; fixes only via PREREG_D439_SCREEN_INFL_DEVIATIONS.md written first.
