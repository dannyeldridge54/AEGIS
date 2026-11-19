# PREREG_D1657_G6C_MASSIVE_DP — can a massive dark photon rescue P-M? (Janus genesis G6c; locked 2026-11-19 ~23:22Z before any number)
Literature read this tick (search snippets, arXiv):
- 1705.00619: for m' ≤ 2m_e the dark photon decays only to 3γ (loop, α⁴) and is generically long-lived; decays between BBN and the CMB are not allowed; ε ≳ 1e-12 can bring it into thermal equilibrium.
- 2109.04852: "very dark" photons, ε ≲ 1e-10, have lifetimes > 1 s; decays later than 1 s (1e13 s) inject energy that interferes with BBN (CMB).
- 1711.08251: a MASSLESS mediator for annihilating the symmetric ADM part is effectively ruled out (halo ellipticity) — independent of N_eff.
- 2510.13770, 2602.20237: ADM with χχ̄ → A'A' depleting the symmetric part and A' decaying to SM fermions before BBN is a standard, studied setup.
Requirements (locked): (Q1) m_A' > 2m_e = 1.022 MeV (open e⁺e⁻ channel); (Q2) m_A' < m_DM = 5.03 GeV (symmetric part annihilates to A'A'); (Q3) τ(A' → e⁺e⁻) < 1 s ⇒ ε > ε_min(m); also report ε for τ < 0.1 s [estimate: decay well before neutrino decoupling ~1 MeV so the dumped energy does not shift N_eff].
Width [estimate, standard leading-order formula, not fetched]: Γ(A' → e⁺e⁻) = (ε²α m/3)(1 + 2m_e²/m²)√(1 − 4m_e²/m²); only the e⁺e⁻ channel counted (conservative: more channels open above 2m_μ ⇒ shorter τ).
Compute ε_min(τ = 1 s) and ε(τ = 0.1 s) at m_A' = 2, 10, 100, 1000 MeV; ΔN_eff after the decay → 0 if A' decays while still coupled-in-time before neutrino decoupling [estimate].
Verdict rule: window OPEN if Q1–Q3 can be met together with ε well below O(1e-3) (ε ≤ 1e-6 at m ≥ 10 MeV counts as "comfortably below collider reach" — collider/beam-dump limits NOT fetched, flagged); CLOSED otherwise. Lab bounds on ε are an explicit follow-up (G6d).
Script: field_tests/scripts/janus_g/g6c_massive_dp.py → field_tests/results/D1657_G6c_massive_dp.json
