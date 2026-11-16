# PREREG D750: reverse ladder from "a test before 2035" — the neutrino-sector predictions (m_ββ, Σm_ν, m_β)
Locked 2026-11-16 before computing. Script: theory/modular/falsifiers_d750.py. Output: field_tests/results/falsifiers_d750.txt.
Reverse path: r is untestable before 2035 (D749), so ask which SERAPIS outputs ARE testable sooner. Candidates: neutrino observables fixed by tonight's results (NO; m₁ = 1e-4 – 5e-3 eV from radiative leptogenesis at τ = i, D745; m₁ ≈ 0 for the frozen Σm_ν, D605).
## Computation (fixed now)
- PMNS (from memory, labelled): θ12 = 33.4°, θ13 = 8.6°, θ23 = 49°, δ = 230°; Δm²₂₁ = 7.42e-5, Δm²₃₁ = 2.5e-3 eV².
- m₁ ∈ {0, 1e-4, 1e-3, 5e-3} eV; Majorana phases α₂₁, α₃₁ on a 72 × 72 grid over [0, 2π).
- m_ββ = |Σ U_ei² m_i e^{iα}| (min and max per m₁); Σm_ν; m_β = √(Σ|U_ei|² m_i²).
## Output and statement rule
Report the predicted ranges. Then state the falsifiers using these sensitivities (from memory, labelled):
- next-generation 0νββ reach (LEGEND-1000, nEXO, CUPID): m_ββ ≈ 1e-2 – 2e-2 eV;
- KATRIN final: m_β ≈ 0.3 eV; Project 8 goal: ~0.04 eV;
- cosmology around 2030 (DESI final + Euclid + CMB): σ(Σm_ν) ≈ 0.015–0.02 eV.
A signal above the predicted max, or a robust cosmological bound below the predicted Σ min, would falsify the NO/small-m₁ branch. Arithmetic only, no fitting.
