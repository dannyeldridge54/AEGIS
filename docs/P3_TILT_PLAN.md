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
- T4 [done D1520: uplift not the tilt — warped anti-D3 / D-term red, fixed-Z ∝ y but ×3.6e3] Uplift τ-dependence: anti-D3 (∝ e^{4A}/𝒱^{4/3}, warp factor depends on g_s via KS throat) or D-term uplift ∝ g_s^{?}/𝒱² — shape along y and size.
- T5 [next] Summary card: which candidate (if any) gives C_phys ≈ 2e-3–0.1 naturally; hand-off note for the P3 chat.
- T3d [done D1509: 0/72 in band; sliver α≈0.125, C≈1.45–1.74e-6] in-band search in the PHYSICAL frame (λ = 1/a, pure-power-law limit): DILMIX (α, C) map with x = λ(E − E_ρ) at a = 9931 (results converge in a) — where is the band now, and what C does it need? (fast SR, lock first)
- T3e [done D1510: SLIVER CONFIRMED 20/56, α 0.05–0.125, C 1.3–2.0e-6; best (0.1,1.8e-6)] fine grid around the sliver in the physical frame: α ∈ {0.05, 0.075, …, 0.2} × C ∈ {1.3, 1.4, …, 2.0}e-6 at λ = 1/9931; confirm/kill the sliver; then exact-MS spot check of the best point (pipeline with λ = 1/9931, own file)
- T3f [done D1512: exact MS IN BAND n_s 0.97198 r 5.463e-4] exact-MS spot check of (α 0.1, C 1.8e-6) in the physical frame with the shared pipeline (own file): lam = 1/9930.9, pipeline tilt convention C_pipe = C·λ (pipeline uses C·g/λ), ymax ≈ 2e5, more grid points; forecast n_s 0.97197, r 5.462e-4

## T5 — Summary card and hand-off note for the P3 chat (written 19 Nov 2026 ~14:55 UTC; Danny decides whether to pass it on)

**Physical target (D1506–D1512).** The P3 runs and our forecasts use the λ = 1 frame; the D1486 compactification has λ = 1/a ≈ 2e-5–5e-4, and the two frames
give different n_s, r (Δn_s ≈ −0.006 for the DILMIX centre) because E_ρ and the y^{−1/2} term of E(τ,3/2) do not rescale (M6). In the physical frame the
in-band DILMIX region is a sliver at **α 0.05–0.125, C 1.3–2.0e-6** (D1510, 20/56), mostly the α′³-square form B (which e^K gives exactly, D1501) plus a
small one-power admixture. Exact MS check (D1512): **(α 0.1, C 1.8e-6), λ = 1/9930.9 → n_s 0.97198, r 5.463e-4 — IN BAND.**
Three independent constructions agree the band needs an effective approach exponent ≈ 1.8–2.05 plus a tilt ≈ 1–2e-6 (our D1490, D1495; P3 D1516).

**Regime flag (M5, D1504–D1505).** On the inflationary path ξ̂/𝒱̂ ≈ 2x* ≈ 250 at every D1486 benchmark (set by n_s, r, not by conventions): the α′³ term
exceeds the tree volume term ~250×, outside the BBHL expansion (hep-th/0412239 Eq. 3.8, pole at ξ̂ = 𝒱̂).

**Tilt source — candidates closed.** BHK g_s² loop: 10⁴–10⁶ too small (D1497, D1040). Next α′³ order (small-u): C_phys ≈ 12, 10²–10⁴ too big (D1501; and not
applicable on the path because of M5). F⁴/R⁴: wrong shape, ∝ 1/y (D1503). Flux W(τ): K^{ττ̄}|D_τW|² = |W|², no ξ-shape (D1504). Uplift: warped anti-D3 and
D-term have the wrong sign; fixed-throat anti-D3 grows ∝ y but ~3.6e3× too strongly (D1520). GS and DKL closed earlier (D1048, STRINGS_PLAN).
**Open:** D⁴R⁴ / E(τ,5/2) (no 4D formula found, D1503); a genuinely non-perturbative ξ̂ ≫ 𝒱̂ treatment (M5) may change the plateau itself.

**Forecast track record.** 21 P3 exact points (DILATON32, SMSCAN, DILMIX, LVSDIL, DILTR) forecast by our fast second-order SR before the runs: |Δn_s| ≤ 5.3e-6,
|Δr/r| ≤ 0.04 % in every case — the SR engine can screen P3 candidates in seconds instead of ~30 min per exact point.
