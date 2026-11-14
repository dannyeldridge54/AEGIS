# A candidate M-theory home for the Twist: the G₂ block split

> **Status after review (D323–D324, 14 Nov 06:15 CT): works at tree level only. At one loop the SM couplings move as d(1/α_a)/d ln x = −b_a/4π (Kaplunovsky–Louis), giving d ln α_em/d ln x ≈ 7×10⁻³. Five fixes were tested and all fail. Kept as a record, not as a candidate home.**

13–14 Nov 2026, built from D309–D315. This is an exploratory proposal, not a derivation.

## Why not heterotic

In the weakly coupled heterotic string, α_GUT = e^{2φ}α′³/(16πV) [Witten, hep-th/9602070]. Keeping the gauge couplings fixed while a volume-type modulus grows therefore drives the string coupling strong (D309; D204, D209).

Minimal Z₃/Z₇ orbifolds also cannot cancel the duality anomaly with the bare MSSM spectrum [Ibáñez & Lüst, hep-th/9202046; D302, D293]. Heterotic M-theory's matter-neutral direction moves the Standard Model coupling (D208).

## The proposal

M-theory on a G₂ manifold. Gauge groups and chiral matter sit at singularities along 3-cycles.

1. **Moduli.** K = −3 ln V_X with V_X = Π s_i^{a_i} and Σa_i = 7/3 [Acharya, Bobkov, Kane, Kumar et al.]. Split the moduli into two blocks:
   - a **rolling block** with Σa = 1 and collective modulus T₂ (the Twist's α = 1 field);
   - a **fixed block** with Σa = 4/3 (T₁).

   This gives K = −3 ln(T₂+T̄₂) − 4 ln(T₁+T̄₁), the (4,3) seven-disk split [Gunaydin, Kallosh, Linde & Yamada, arXiv:2008.01494; D311].
2. **Standard Model.** It sits on a 3-cycle with gauge kinetic function f_SM = Σ N_i z_i and N_i = 0 on the rolling block. Its gauge couplings are then exactly x-independent (D312).

   Its matter metric is K̃ = κ(s)/V_X, by locality [Acharya & Bobkov, JHEP 09 (2010) 001]. The overall volume cancels in the physical Yukawas, so they are x-independent provided κ depends only on fixed-block moduli near the singularity (D312).
3. **Fixed block.** It is stabilised by two hidden condensates on T₁-only cycles, by the ABKKV mechanism [hep-th/0606262]. The minimum must be supersymmetric with W = 0, or tuned; otherwise its e^K ∝ x^{−3} energy adds to the tail (D315).
4. **Rolling block.** Its potential comes from the Twist sector: a stabiliser S with W = √3 m S T₂, and a cliff from an SU(8)-type hidden condensate on an N₂ = 1 cycle, W ∝ e^{−πT₂/4} (D314). That condensate is strongly coupled on the plateau, as in D136.
5. **SUSY breaking.** W ⊃ w T₂^{3/2} + μ²X, with X weighted (T₂+T̄₂)^{−3}. This gives V = μ⁴ − 3w²/8, the same at every x, with x-independent m_3/2 and F_X (D292, D294, D295). The construction carries over unchanged to the block split (D314). An eV gravitino from a non-minimal mediation sector is allowed (D291).

## What is not shown

- The plateau → cliff → tail potential from actual G₂ data.
- The singularity structure that gives chiral matter and the required metrics (X at weight 3, χ at weight 3/2).
- That κ depends only on local moduli.
- Control of the cliff condensate on the plateau.
- ~~Varying M₁₁/M_P. This affects only heavy states.~~ Withdrawn (D323): M₁₁/M_P ∝ V_X^{−1/2} slides with x and feeds into the SM couplings logarithmically, giving d ln α_em/d ln x ≈ 7×10⁻³ (estimate), far beyond the clock bound.

## Question 12 for M-theory experts

> In a G₂ compactification with the Standard Model on an associative 3-cycle that has no homology component along a three-modulus block (Σa = 1), and the remaining moduli stabilised supersymmetrically with W = 0 by condensates on cycles built from those moduli alone:
>
> 1. Is that block a flat direction with K = −3 ln(T + T̄)?
> 2. Are the Standard Model gauge couplings and Yukawas independent of it to the 10⁻⁸ level required by atomic clocks?


**Addendum (D319, 14 Nov 05:40 CT).** In this picture the cliff depth n becomes integers (ranks, wrapping numbers) times a logarithm of one-loop condensate prefactors, via the ABKKV vacuum condition A₂/A₁ = α⁻¹exp[−(b₁N¹ − b₂N²)·s] (hep-th/0701034). Question 12 gains a sub-question: can these prefactors fix Re T₁ to the ~0.3% level that today's Λ ∝ e^{−2n} needs?

**Addendum (D321, 14 Nov 06:00 CT).** Smooth twisted-connected-sum G₂ manifolds contain rigid associatives S¹×S² localised in one building block (Corti–Haskins–Nordström–Pacini, arXiv:1207.4470), and others glued across the neck (arXiv:2209.00156). These could give an M2-instanton cliff term in place of the condensate, with the same small-volume control caveat. The SM cycle (N₂ = 0) needs ADE singularities, which smooth TCS manifolds lack, so it requires a singular G₂. Sub-question for question 12: does a singular TCS-type G₂ realise the (4,3) Kähler split with the SM cycle in the fixed block?

**Addendum (D322).** One-loop thresholds on a 3-cycle Q of ADE singularities are the Ray–Singer torsion of Q (Friedmann–Witten, hep-th/0211269), explicit for lens spaces S³/Z_q. So (a) [withdrawn, D323: only the local part; the volume-dependent part remains] and (b) n becomes a finite, computable set of values from discrete data, and a lens-space scan could test whether α_h⁻¹ ≈ 39.8 is reachable.

**Referee caveats (D323, 14 Nov 06:10 CT).** (1) The block split fixes the shield at tree level only. At one loop the sliding M₁₁/M_P gives the D289-sized α drift. Question 12 must ask how that is removed. (2) The two non-diagonal directions of the rolling block are unstabilised. (3) W = 0 for the fixed block is a racetrack tuning.
