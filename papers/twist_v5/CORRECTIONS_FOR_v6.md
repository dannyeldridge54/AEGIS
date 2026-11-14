# Corrections queued for v6 of the Twist paper (found after v5 was published on 13 Nov 2026, 19:25 CT)

## 1. Section 5.2 (Gravitino) and assumption 4: replace the text (D267, D269)

The current v5 text says: "Supersymmetry breaking comes from a separate, unspecified sector … m_3/2 = 10¹¹–10¹⁴ GeV".

Replace it with:

> W = √3 m S T vanishes at S = 0, so the inflaton sector does not fix m_3/2. In this field space, any supersymmetry-breaking superpotential gives m_3/2 = |W|/(2x)^{3/2} on real T [Zwirner, arXiv:2504.06190; Ellis et al., arXiv:1809.10114].
>
> **A constant W₀ is excluded.** It changes m_3/2 by a factor 5.7×10⁸ between the CMB point and today. Either the gravitino is super-Planckian during inflation, or it is ≲ 3×10⁴ GeV today. In the second case, thermal production at T_RH ≈ 5.6×10¹⁴ GeV violates nucleosynthesis bounds.
>
> Two options remain:
>
> **(i) A light gravitino from low-scale gauge mediation.** m_3/2 ≈ 0.8–4.7 eV today, between the Higgs-mass lower limit [Ibe & Yanagida, arXiv:1608.01610] and the cosmological upper limit [Osato et al., arXiv:1601.07386]. Along the Twist's history it is 0.5–3 GeV during inflation (≪ H) and a few keV at the cliff, so it is harmless. Keeping V ≈ 0 at every x makes the SUSY-breaking scale slide as x^{−3/2} too. Superpartner masses would then change by ~30% between nucleosynthesis and today, shifting α_em by ~10⁻³ through thresholds (estimate). So this option needs the shield to cover the SUSY-breaking scale seen by the Standard Model (D272).
>
> **(ii) W ⊃ w T^{3/2} plus a constant uplift.** This gives an x-independent m_3/2.
> - It leaves the plateau intact: a full supergravity check finds V changes by ≤ 0.6% for m_3/2 ≤ 10¹³ GeV.
> - It gives the angle a tachyonic mass −2 m_3/2². Kähler-only stabilisers do not cure this: m_θ² stays −2 m_3/2² for any b(T − T̄)⁴ or b(T − T̄)² term (D270). A cure needs the uplift sector to couple to the angle, which makes the angle heavy (~m_3/2).
> - It needs m_3/2 ≲ 6×10⁸ GeV, so that the angle stays light while matter forms.
> - It needs m_3/2 ≳ 10⁸ GeV, so that gravitino decay releases ≲ 15% of the energy.
> - It therefore works only for m_3/2 ≈ 10⁸–10⁹ GeV (estimate), with R-parity violation.
>
> Neither option is derived. Adopt (i).

## 2. Section 2.2 (coupling): result of the alternative reading

D268 is running. Insert its result here: the matter yield when the Nieh–Yan current couples to ∂(y/x) instead of to the canonical angle.

## 3. Table of assumptions, item 4

Replace the item with: "Supersymmetry breaking: a near-massless gravitino with superpartner masses not tied to m_3/2 (adopted); W ∝ T^{3/2} plus uplift needs the uplift sector to stabilise the angle and works at best for m_3/2 ≈ 10⁸–10⁹ GeV; a constant W₀ is excluded."

## 4. Section 5.1 (fifth force): add precedents (D273)

Add after the shield paragraph:

> In generic supergravity quintessence, every MSSM soft term and fermion mass depends on the field through e^{K/2}, and Cassini then requires a tuned cancellation [Brax & Martin, hep-th/0605228]. The shield must therefore also keep the Standard Model's supersymmetry-breaking scale independent of x. The no-scale isometry protects the field's own lightness from gravitino-induced masses [Brax, Davis & Sakstein, arXiv:1212.4392], but not its couplings to matter.

## 5. Exploratory note §1.3–1.4: locked PC results (D277)

- **m_σ.** Replace "confirmation pending" with: "the locked confirmation run gives 1.25× observed at m_σ = 5.8×10¹⁰ GeV, the same in TWIST-K; entropy dilution ×4.6".
- **§1.4 Isocurvature.** Replace "unverified" with: "the locked sensitivity run gives |d ln Y/d ln σ₀| = 3.70, which passes the locked limit of 5. S_B ≈ 3.7×10⁻⁵ against a bound of 5×10⁻⁵ at f = 0.1 M_P is marginal, and requires f ≳ 0.1 M_P. The yield is very sensitive to the angle's starting value (y₀ = 0.01 multiplies it by about 9000), so the heavy angle during inflation is essential." The earlier "8× below the bound" is withdrawn.

## 6. Gravitino consequences (D279)

Add to §5.2 option (i): "The gravitino is a thermal warm relic, making up m_3/2/86 eV ≈ 1–5% of the dark matter, with ΔN_eff ≈ 0.02–0.05. The main dark-matter candidate is unaffected."

## 7. A new stated assumption: the reheating field χ has modular weight 3/2 (D286)

Add to the assumptions list:

> **The reheating field χ enters the Kähler potential as |χ|²/(T + T̄)^{3/2}.** Its physical mass is then independent of x, and its one-loop correction to the plateau is negligible, as D156 assumes.
>
> The other placements fail:
> - Inside the no-scale log, the one-loop term would be an order-one ∝ 1/x deformation (dV/V ≈ 7 at the CMB point).
> - With a flat Kähler term, it would be larger still.

## 8. Option (i) needs a non-minimal SUSY-breaking sector (D291)

Add to §5.2:

> The 0.8–4.7 eV window is open only in non-minimal models, such as vector-mediated D-term breaking [Hook, McGehee & Murayama, arXiv:1801.10160] or strongly coupled messengers [Lu & Shirai, arXiv:1712.02359]. Minimal gauge mediation is excluded. A cosmic-shear bound below ~1 eV would remove this option.

## 9. A supersymmetry-breaking sector with x-independent scales (D292; supersedes the two-option text in item 1)

Replace the §5.2 options with:

> **W ⊃ w T^{3/2} + μ² X, with the Polonyi field X at modular weight 3:** K ⊃ |X|²(T + T̄)^{−3}[1 + c((T − T̄)/(T + T̄))²].
>
> - Along real T, exactly: V = μ⁴ − 3w²/8, the same for every x. A single cosmological-constant tuning sets it to zero.
> - m_3/2 = w/2^{3/2} and F_X = μ², both x-independent.
> - The angle mass is (4c − 2) m_3/2², so the angle is stable for c > 1/2.
> - With messengers at modular weight 3/2, the gauge-mediated soft masses do not slide. This removes the α_em drift of D289.
> - The eV gravitino window (D291) is realised in this sector.
> - The modular weights are assumed, not derived.

## 10. Condition on the SUSY-breaking sector (D294)

Add to §5.2:

> X = 0 is shifted by a Polonyi tadpole to X ≈ 2√6/(12q − 2) M_P. That shift is x-independent in canonical units. The sector must also give the sgoldstino a mass far above m_3/2 (q ≳ 10⁷); otherwise its late oscillations overclose the universe. This holds for dynamical SUSY breaking at √F ~ 10⁵ GeV, but not for a bare Polonyi field.
