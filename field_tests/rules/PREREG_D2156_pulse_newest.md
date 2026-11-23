# PREREG D2156: the pulsing Loom re-run on tonight's newest data (locked 22 Nov 2026 ~22:30 CT, before running)
Danny 22:25: go back to the same method we use every time: all the dials, the pulsing/looping sonar triangulation, checking each node before it, watching the scales on each side.

Base: tools/loom/resonance10.py, variant VC (10 layers, shells + spine, 3 breaths inhale/exhale, layer locks at 3 passing passes, 7-null solver), UNCHANGED.
New variant VN = VC plus three scales fed by tonight's results (no other change):
- L6 dilaton: add n_s_PACT = 2 - |n_s - 0.9743| / 0.0034 (P-ACT-LB, newest CMB combination quoted in the preprint).
- L8 cosmology: add dark_baryon_window = min(ln(m_X/3), ln(15/m_X)) with m_X = 12.81 GeV x (1 - Omega_wino/0.12) (Omega_wino from the same layer's gravitino-box reading); window [3, 15] GeV is the D1676 locked window.
- L9 late universe (was TRUST, no margin): add thread_PR4 = 2 - max(dchi2_eff over finished W/L entries) = 2 - 2.46 (Pantheon+), the D2132 consistency line. L9 has no knobs, so this scale is fixed by data.
Readout: per breath, which layers lock; which layers that locked in VC fail to lock in VN (off balance); fits spent; every off-balance node goes to the balance ledger.
Expectation stated before running: L9 cannot lock (margin -0.46); L7 (alpha_s) already fails in VC; L6 may tighten; L8 should still lock.
Not evidence: a deterministic consistency map (D1948).
