# PREREG D446 — cloud run: full capture integration with the stringy FI term + remnant count over all bounces (Danny 19:16 CT "Start a cloud run on things u need")
Locked before computing. Script theory/deep/cloud_capture_d446.py = D437 integrator (same start state, radiation background, hard elastic wall,
D1 stopping rule) with ξ replaced by ζ(x)(M_s/M_P)², ζ = (1/π)[atan(x/10) − atan(x/400)] + c, c = −f(29.6) computed exactly (root at 29.6000;
fixes the D442 rounding). Soft potential V = m_s²|ζ|(M_s/M_P)² (M_P units). Scan M_s/M_P ∈ {0.03, 0.0675, 0.1, 0.3}, m_s ∈ {1e4, 1e5} GeV.
Outputs per case: first hit (N, T), number of reflections, min x after first reflection, first return (N, T), final offset at N − N_e = 20.
Remnant per wall hit (D444a method, conservative): rate R = g²ζ′(x_E)(M_s/M_P)² M_P² ẋ, m²_* = (R/2)^{2/3}, V_res = m_s² m²_*/g², summed as
Σ V_res/s(T) [GeV], g = 0.7, compared with DM 4.3e-10 GeV.
Readings: CAPTURES (returns and final offset < 1e-2) / FAILS TO PIN, per case; remnant total reported (expected ≫ DM; tests whether bounces
dominate over the first hit). No reruns to chase; fixes via PREREG_D446_CLOUD_CAPTURE_DEVIATIONS.md first.
