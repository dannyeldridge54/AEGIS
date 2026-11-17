# Level S plan: string one-loop masses for Project H (started 16 Nov 2026)
Goal: decide, by computation, whether a gauge-charged scalar χ on the anti-D5 branes of the ADS T⁴/Z₂ orientifold (hep-th/9908023) gets a POSITIVE one-loop mass² ∝ E(U,2)/A on a T² factor (Project H's open condition, D964–D968, D983).
Rule: each stage must reproduce an independent route before it is used; results go through locks as usual.
- S0 DONE: theta/eta; abstruse identity θ₃⁴ − θ₄⁴ − θ₂⁴ = 0 (selftest).
- S1 DONE: field-theory one-loop potential on R⁴ × T² for a bulk boson with a Wilson line/position shift: KK proper-time sum = Poisson winding sum (1e-8 on four tori), curvature = E_paper(U,2)/(π³A) (1e-4). Sign rule: fermions enter with weight −1, so m² ∝ +(N_B − N_F)E(U,2)/A (D983).
- S2 NEXT: open-string annulus for a D-brane stack on T² with a Wilson line: A(a) = ∫dt/t³ · [oscillator theta/eta ratio] · Σ_p e^{−πt α′|p+a|²}. Tests: (i) supersymmetric ratio vanishes identically (S0); (ii) massless-level truncation reproduces S1 exactly; (iii) Kitazawa 0805.0824 9-brane-on-circle result (sign opposite to the vacuum amplitude).
- S3: Möbius strip + the BSB (anti-D5) projection: oscillator content of the anti-D5 sector (bosonic excess +128, D968); compute d²A/dχ² for a gauge-charged position/charged scalar; extract sign and U-dependence; compare with S1's E(U,2) form and with the field-theory sign rule. Lock before running.
- S4: write-up; if positive with E(U,2), Project H's sign condition moves from derived (field theory) to computed (string).
Parallel: outreach email to string theorists (draft only, papers/outreach/STRING_EXPERT_DRAFT.md) — sent only on Danny's "Send".

## S3 input data (ADS hep-th/9908023, extracted 16 Nov 20:05 CT) [literature]
- Direct annulus eq. (9): A = ¼{(Q_o+Q_v)(N²P + D²W) + 2ND(Q_s′+Q_c′)(η/θ₄)² + (R_N²+R_D²)(Q_o−Q_v)(2η/θ₂)² + 2R_N R_D(−O₄S₄ − C₄O₄ + V₄C₄ + S₄V₄)(η/θ₃)²}; Q_o = V₄O₄ − C₄C₄, Q_v = O₄V₄ − S₄S₄ (each a boson−fermion supersymmetric pair): the annulus is supersymmetric.
- Direct Möbius eq. (12): M = −¼{NP(Ô₄V̂₄ + V̂₄Ô₄ − Ŝ₄Ŝ₄ − Ĉ₄Ĉ₄) − DW(Ô₄V̂₄ + V̂₄Ô₄ + Ŝ₄Ŝ₄ + Ĉ₄Ĉ₄) − …}: in the D̄5 term bosons and fermions enter with the SAME sign (the O5 charge reversed), so supersymmetry is broken by the Möbius amplitude in the D̄5 sector only.
- Tadpoles: N = D = 32, R_N = R_D = 0; D̄5 gauge group USp(16)×USp(16). Massless D̄5 spectrum: USp vectors (adjoint = symmetric 136), scalars in (16,16) quartets, fermions in antisymmetric 120's and (16,16): NO gauginos. Per USp(16): boson adjoint 136 vs fermion antisymmetric 120 → mismatch 16 per factor.
- D̄5 vacuum energy positive, V = c e^{−φ₁₀} = c/g²_YM, c > 0 (eq. 18).
S3 task (next, lock first): add a Wilson line / position shift a for a χ charged under USp(16) on the D̄5 stack wrapping the T² (P → P(a) for charged states; the Möbius only sees states mapped to themselves, i.e. shift 2a); compute d²(A + M)/da² at a = 0 from the full theta-function amplitudes (S2 machinery, Ô/V̂/Ŝ/Ĉ in the "hatted" Möbius basis), sign and U-dependence; field-theory cross-check: massless level = (adjoint 136 − antisym 120) mismatch × S1's E(U,2)/A form.
