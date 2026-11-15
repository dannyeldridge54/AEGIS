# PREREG D467 — does the bounce injection respect D463's ε_h ≤ 5.5e-5 in the rescaled geometry? (cycle 52, "pppp"; fifth pass PART 5)
Locked before computing. Use the D460 integrator run(m_s, r, NEND) (unchanged), r = 1.43e-4 (D452, a = 3846, g_s = 0.5), NEND = 32,
m_s ∈ {1e-9, 1, 1e4} GeV. Its 'rem' = Σ V_res/s over wall hits (D446 conservative per-hit estimate). Convert to an energy share at capture:
ε_h = rem·(4/3)/T_cap, T_cap = 1.5e11 GeV (conservative: injections at later, colder hits count as if at T_cap; true share there is larger per hit, so also report
max over hits is not available — state this). Verdict: "WITHIN D463" if ε_h ≤ 5.5e-5 for all m_s; "EXCEEDS for m_s ≥ …" otherwise.
Note for the reading: the per-hit estimate overcounts at large m_s (D446). No reruns; fixes via _DEVIATIONS first.
