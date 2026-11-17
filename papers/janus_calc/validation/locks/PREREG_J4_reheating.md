# PREREG J4: Janus one-call reheating → N* vs the base toolkit's exact N* (D979 = run D958c, field_tests/results/repro_nstar_d958.txt)
Model: SERAPIS-E C = 1.15e-6 (paper convention), w = 0, g* = 106.75, matching equation as tools/serapis_calc/nstar.py, V*/V_end from the background.
Reference (exact background + exact MS r): N* = 46.458, 47.985, 48.749, 49.513, 51.042 for T_R = 1e4, 1e6, 1e7, 1e8, 1e10 GeV; n_s = 0.96951, 0.97113, 0.97191, 0.97268, 0.97416.
Pass (fixed now): |ΔN*| ≤ 0.02 and |Δn_s| ≤ 5e-6 at all five T_R → VALIDATED, else NOT VALIDATED.
Script theory/janus/j4_check.py; output field_tests/results/janus_j4_check.txt.
