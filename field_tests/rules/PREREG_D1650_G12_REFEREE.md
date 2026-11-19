# PREREG_D1650_G12_REFEREE — whole-chain referee of the genesis pathway (Janus genesis G12; locked 2026-11-19 ~22:52Z before any check runs)
Scope: genesis D-notes D1626–D1647 (both chats; D1636 excluded — no result yet) and their result jsons.
Mechanical checks (script field_tests/scripts/janus_g/g12_referee.py):
K-order: for every genesis lock (PREREG_GENESIS_DE/DE2/DE3/MATTER/BBN2/BBN3/LI7, PREREG_RC2_START, PREREG_D1637/1638/1641/1644/1646/1647) the PREREG file's first commit precedes the first commit of its result json (git log --diff-filter=A, author time). Each DEVIATIONS file precedes the rerun result it governs.
K-arith (re-run from jsons): (a) Ω_DM/Ω_b·m_p = m_DM (5.36 × 0.938 ≈ 5.03); (b) D1637 m, T_R(κ) from V∞ and V''; (c) D1641 (D−2)/32 rows; (d) D1646 ξ and ΔN_eff formulas; (e) D1638 pass points satisfy dmax ≤ 6.18 and w ≥ −1; (f) D1644 m/H_Λ = √3/2.
K-physics sanity: (g) perturbative reheating consistency: Γ < H_end and T_R < m for both κ ends (D1637); (h) the mirror formula 7.4 = (2/(7/4))(11/4)^{4/3} + 3; (i) D1642 quantum spread ≪ window.
Reading checks (by hand, listed in the note): labels honest ([derived] vs [estimate] vs postulate); every assumption on the card's open list; corrections made as new notes (D1626a, D1643, D1641 step 6, D1644 run 1 kept).
Pass rule: PASS if no check finds an error that changes a stated verdict. Errors that change a verdict → FAIL, each becomes a new G-lead (G13…). Nits (wording, data bounds used without a fetched source) are listed, do not fail.
Stated limitation: this referee is the same agent that wrote most Janus notes (not independent); the other chat's notes are read cold.
