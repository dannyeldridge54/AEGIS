# PREREG A2d — TaylorF2 tidal phase vs LALSuite (Hyperion roadmap A2b tides; Djl D) — locked 2026-11-17
Source (fetched): Vines, Flanagan & Hinderer 2011 (arXiv:1101.1673), Eqs. 3.9–3.10:
- ψ = (3/(128 η x^{5/2}))[1 + ψ01 λ̂ + ψ10 x + ψ11 x λ̂]
- λ̂ = λ x⁵/M⁵
- ψ01 = −(24/χ_A)(1 + 11χ_B)
- ψ11 = −(5/(28χ_A))(3179 − 919χ_A − 2286χ_A² + 260χ_A³)
- summed over both bodies; χ_A = m_A/M, χ_B = 1 − χ_A; λ_A = Λ_A m_A⁵ (G = c = 1).
Transcription check (arithmetic, done before the lock): the equal-mass limit reproduces the paper's Eq. 3.11 coefficients −624 and −3115/2.
Code (written after this lock): gw.taylorf2_tidal_dphase(f, M1, M2, Lam1, Lam2).
Test: LAL TaylorF2 (phase order 7, spin 0, PNTidalOrder = 6PN) with tides minus without tides, phase −unwrap(angle h), vs our δψ.
- Residual after removing a linear (constant + f) fit.
- Cases: (1.4, 1.4) with Λ = (300, 300); (1.35, 1.45) with (400, 250); (1.2, 1.8) with (800, 100).
- f from 20 Hz to the ISCO cut 0.8 f_ISCO (as A2a/A2b).
- Pass: max |residual| ≤ 1e-6 rad in every case.
Reported: the same comparison at PNTidalOrder = 5PN with only our ψ01 term; and the size of the 6.5PN/7PN tidal terms (LAL ALL minus 6PN).
A2d VALIDATED iff all three 6PN cases pass. Fixes only via DEVIATIONS.
Script theory/janus_astro/a2d_check.py.
