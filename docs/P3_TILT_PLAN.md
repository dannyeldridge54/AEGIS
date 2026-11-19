# Tilt-source plan for the P3 route (Danny 19 Nov 07:21 CT: chose "Tilt source")

Target (D1485/D1494/D1497): the in-band DILMIX strip needs a plateau tilt V ∝ P·(1 + C·g), g = P/(1 − P) (≈ x = λ(E − E_ρ) for form A),
with C ≈ 1–2e-6 in the λ = 1 frame ⇔ C_phys = C·a ≈ 2e-3 – 0.1 for a = 1/λ ≈ 2e3–5e4 (D1486 benchmarks). Weak coupling g_s* ≈ 5e-5–5e-4.
Already closed elsewhere (do not redo): BHK one-loop (D1040; and D1497: g_s² short by 10⁴–10⁶), GS route (D1048), DKL s = 1 log (STRINGS_PLAN).
Rules: our own D-numbers and files; formulas fetched from the literature (tables/equations read, not from memory); each candidate locked before numbers;
for each: (i) functional shape it adds to V(τ) along x = ½, (ii) its natural coefficient size in the physical frame, (iii) fast-SR test whether that shape with that
size lands in band (D1485 machinery). A candidate "works" only if (ii) and (iii) agree without tuning beyond O(1).

- T1 [done D1501] Exact form-A Kähler expansion: keep the next order of e^K·V_F in ξ/𝒱 (BBHL/BBCQ formula, fetched) instead of truncating at the plateau x/(1+x) — does it generate a (1 + κx)-type factor with κ = O(1) in units where C_phys = κ? Shape and κ.
- T2 [next] D⁴R⁴ (α′⁵, coefficient E(τ,5/2) — Green–Vanhove/Green–Russo–Vanhove, fetched): its 4D potential contribution along the dilaton, relative to the α′³ term; shape ∝ E(τ,5/2)/𝒱^{?} — does it act as a tilt, and how big?
- T3 [next] τ-dependent flux superpotential: W₀(τ) = ∫G₃∧Ω, G₃ = F₃ − τH₃ ⇒ |W₀|² is quadratic in τ — after the dilaton is no longer fixed by fluxes (it is the inflaton here), V_LVS ∝ |W₀(τ)|²/𝒱³ adds a y²-type factor. Shape vs the needed tilt; size set by the flux ratio.
- T4 [next] Uplift τ-dependence: anti-D3 (∝ e^{4A}/𝒱^{4/3}, warp factor depends on g_s via KS throat) or D-term uplift ∝ g_s^{?}/𝒱² — shape along y and size.
- T5 [next] Summary card: which candidate (if any) gives C_phys ≈ 2e-3–0.1 naturally; hand-off note for the P3 chat.
