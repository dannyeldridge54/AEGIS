# Quantum-side work list (8 Nov 2026)

AI-assisted working notes following the literature check ("Where the Twist falls short", Claude doc). Order-of-magnitude
estimates, not results; nothing here is a test. Each item that predicts a number gets a locked rule before any data.

## 1. Can the angle's mass be derived? (instanton height)
- Kaul & Sengupta (arXiv:1411.4793): Nieh–Yan (torsional) instantons give a vacuum energy −2K e^(−S) cos η, with η the
  inverse BI parameter. So a quantum-gravity cosine exists; its height e^(−S)·K is not computed anywhere.
- With V = Λ⁴(1 − cos θ), width F = 1.559 M_P (reduced M_P = 2.435×10²⁷ eV): m² = Λ⁴/F².
  - m = 10⁻²⁶ eV → Λ⁴ ≈ 1.4×10³ eV⁴; m = 10⁻²⁵ eV → Λ⁴ ≈ 1.4×10⁵ eV⁴.
  - If Λ⁴ ≈ M_P⁴ e^(−S) (K ~ M_P⁴ assumed): **S ≈ 245 (10⁻²⁶ eV) to 241 (10⁻²⁵ eV)**. Dark energy (~2.2 meV)⁴ needs
    S ≈ 280.
- Done 9 Nov: theory/INSTANTON_HEIGHT.md (not derived: S ≈ 240 needs β ~ 10⁵ or f ~ 0.008 M_P; at F = 1.559 M_P, S ≈ 1.2).

## 2. Where could n = 3 come from? (early role)
- STEP2_RESULT.md (31 Oct): (1 − cos x)³ = 5/2 − (15/4) cos x + (3/2) cos 2x − (1/4) cos 3x needs two exact
  cancellations (Σk²a_k = 0, Σk⁴a_k = 0). Instanton series and chiral anomalies give a mass term (n = 1-like).
- Open possibilities, none worked out: (a) a symmetry that forbids the 1- and 2-instanton contributions to the mass
  term (e.g. a Z₃ acting on the angle, so only charge-3 sectors contribute at low order); (b) the early boost is not the
  BI angle at all but another field; (c) the shape is effective, from the dilaton and angle moving together.
- Data side: the deferred n = 1 test (DRAFT_POWER_N1_AXICLASS.md) says how much n = 3 is actually required.

## 3. The angle's dark-matter share and its starting angle
- Standard misalignment estimate (Ω_a h² ≈ 0.1 (F/10¹⁷ GeV)² (m/10⁻²² eV)^½ θ_i²): with F = 1.559 M_P ≈ 3.8×10¹⁸ GeV
  and m ≈ 10⁻²⁵ eV, f ≈ 5% needs **θ_i ≈ 0.03 rad**.
- The early role starts near θ_i ≈ 2.4–2.8 rad. If both are the same angle they conflict. Either the early boost and the
  late share are different fields, or something resets the angle between them (worth a note, no test yet).

## 4. Field-space curvature (done 8 Nov)
- Axiodilaton (arXiv:2512.13544): (M_p²/2)[(∂χ)² + e^(−2ζχ)(∂𝔞)²]; ours (∂χ)² + F_P² e^(λχ)(∂θ)². So ζ = −λ/2 and
  our λ = −2√(2/3) is their no-scale ζ = √(2/3).
- Their |ζ| ≲ 0.05 bounds dark matter's mass change with the dilaton when the axion is all of dark matter. Ours is
  β = √(2/3) f ≈ 0.04–0.05 with f ≈ 5–6%: at their limit, consistent. Independently confirms that the angle cannot be
  all of dark matter (β = 0.816 ruled out).

## 5. Holst mixing (before the next FP test)
- Pollari (arXiv:2308.03145): with Holst (α) and Nieh–Yan (β) fields both present, the kinetic terms carry
  M_P²/(α² + M_P²) and an α–β cross term that no field redefinition removes. Our FP test compares Nieh–Yan and Holst
  without that mixing. Next FP rule should include it, or state why it vanishes for our field content.

## 6. DES Y6 number (done 8 Nov)
- Our S8-WL Part 1 uses DES Y6 cosmic shear with NLA alignments, 0.798 (+0.014/−0.015) (arXiv:2602.10065). The same
  paper's TATT value is 0.783 (+0.019/−0.015). Our Part 2 (DES Y3) uses TATT. State both in write-ups.
