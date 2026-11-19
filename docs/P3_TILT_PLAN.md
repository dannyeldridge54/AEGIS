# Tilt-source plan for the P3 route (Danny 19 Nov 07:21 CT: chose "Tilt source")

Target (D1485/D1494/D1497): the in-band DILMIX strip needs a plateau tilt V ∝ P·(1 + C·g), g = P/(1 − P) (≈ x = λ(E − E_ρ) for form A),
with C ≈ 1–2e-6 in the λ = 1 frame ⇔ C_phys = C·a ≈ 2e-3 – 0.1 for a = 1/λ ≈ 2e3–5e4 (D1486 benchmarks). Weak coupling g_s* ≈ 5e-5–5e-4.
Already closed elsewhere (do not redo): BHK one-loop (D1040; and D1497: g_s² short by 10⁴–10⁶), GS route (D1048), DKL s = 1 log (STRINGS_PLAN).
Rules: our own D-numbers and files; formulas fetched from the literature (tables/equations read, not from memory); each candidate locked before numbers;
for each: (i) functional shape it adds to V(τ) along x = ½, (ii) its natural coefficient size in the physical frame, (iii) fast-SR test whether that shape with that
size lands in band (D1485 machinery). A candidate "works" only if (ii) and (iii) agree without tuning beyond O(1).

- T1 [done D1501] Exact form-A Kähler expansion: keep the next order of e^K·V_F in ξ/𝒱 (BBHL/BBCQ formula, fetched) instead of truncating at the plateau x/(1+x) — does it generate a (1 + κx)-type factor with κ = O(1) in units where C_phys = κ? Shape and κ.
- T2 [done D1503: F⁴ wrong shape; D⁴R⁴ NULL] D⁴R⁴ (α′⁵, coefficient E(τ,5/2) — Green–Vanhove/Green–Russo–Vanhove, fetched): its 4D potential contribution along the dilaton, relative to the α′³ term; shape ∝ E(τ,5/2)/𝒱^{?} — does it act as a tilt, and how big?
- T3 [done D1504: not a tilt; FLAG ξ̂/𝒱̂ ≫ 1 on the path]
- T3b [done D1505: flag stands, ξ/𝒱 ≈ 251 at all benchmarks; CORRECTION frame map x +7.1]
- T3c [done D1506: FRAME-DEPENDENT, physical n_s ≈ 0.965 for the DILMIX centre] physical-frame n_s, r of the DILMIX centre and A1 (λ = 1/a, a 2e3/9.9e3/5e4) vs the λ = 1 values — fast SR, lock first
- T4 [next] Uplift τ-dependence: anti-D3 (∝ e^{4A}/𝒱^{4/3}, warp factor depends on g_s via KS throat) or D-term uplift ∝ g_s^{?}/𝒱² — shape along y and size.
- T5 [next] Summary card: which candidate (if any) gives C_phys ≈ 2e-3–0.1 naturally; hand-off note for the P3 chat.
- T3d [done D1509: 0/72 in band; sliver α≈0.125, C≈1.45–1.74e-6] in-band search in the PHYSICAL frame (λ = 1/a, pure-power-law limit): DILMIX (α, C) map with x = λ(E − E_ρ) at a = 9931 (results converge in a) — where is the band now, and what C does it need? (fast SR, lock first)
- T3e [next] fine grid around the sliver in the physical frame: α ∈ {0.05, 0.075, …, 0.2} × C ∈ {1.3, 1.4, …, 2.0}e-6 at λ = 1/9931; confirm/kill the sliver; then exact-MS spot check of the best point (pipeline with λ = 1/9931, own file)
