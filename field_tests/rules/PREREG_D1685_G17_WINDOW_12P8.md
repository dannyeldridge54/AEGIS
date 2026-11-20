# PREREG_D1685_G17_WINDOW_12P8 — the dark-photon window up to m_X = 12.8 GeV (Janus genesis G17; locked 2026-11-20 ~00:58Z before any number)
Input change (other chat, read-only): D1676 gives the dark particle m_X = 12.8 GeV (non-SUSY chemical equilibrium), replacing D1631's 5.03 GeV. The window condition m_A' < m_X (D1657 Q2) therefore extends to 12.8 GeV.
Method: D1664's script logic unchanged (same DarkCast mirror db9a0f6, same visible-limit selection, same BBN floor and SN band), with the mass grid's upper end set to 12.8 GeV (400 log-spaced points in [0.02, 12.8] GeV). Implemented as g6e_darkcast.py with one argument for the top mass (default 5.03 keeps D1664 reproducible).
Outputs: open ε interval at 5, 8, 10, 12.8 GeV; any mass in 5–12.8 GeV with < 1 decade open; R0: the rows ≤ 5.03 GeV must reproduce D1664's widest-decade values at the shared masses within 1 % (grid differs, so compare at nearest masses).
Note (not scored): D1677's direct-detection cut (UNSOURCED bracket, D1684) would lower the upper ε edge; reported alongside, not applied.
Script: field_tests/scripts/janus_g/g6e_darkcast.py <limits> 12.8 → field_tests/results/D1685_G17_window_12p8.json
