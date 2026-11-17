# PREREG B4 — Li-7 from a full BBN network (PRyMordial) (Djl B) — locked 2026-11-17
Code: PRyMordial (github.com/vallima/PRyMordial, commit 725d8a8d), cloned to an isolated scratch directory, pure Python. Run with its own default rates and its small network (12 reactions), via the Python path (no Julia).
Settings (only these changed from defaults):
- Omegabh2 = 0.02242 (Planck 2018 +BAO, D1082); its default is 0.02230.
- Default τn 878.4 s; ΔN_eff = 0.
Also run at its default Ωbh2 0.02230, for reproducibility of its own README/demo numbers.
Outputs: Y_p (CMB), D/H, ³He/H, ⁷Li/H.
Checks (reported, not code validation):
- L1: ⁷Li/H vs the quoted standard-BBN 4.94 ± 0.72e-10 (D1100, Yeh+2021 / Fields & Olive 2022). CONSISTENT if within 1σ.
- L2: Y_p and D/H vs our PRIMAT table (D1082: 0.24721, 2.4393e-5), with the relative difference reported.
- L3: ⁷Li/H vs the Spite plateau 1.6 ± 0.3e-10, giving the ratio and σ.
Script theory/wiring/b4_li7.py: it runs PRyMordial with cwd set to its directory and runs nothing else from that tree.
If the run fails, record NULL and stop (no debugging into the external code this tick).
