# PREREG D2083: Seed v4, the Pati-Salam fork with an α_s prediction. Same space as D2082 (T⁶/(Z₂×Z₂), tilted T³, |n|, |m| ≤ 3, χ ∈ {1/2, 1, 3/2, 2, 3}³). Locked before running.

**Formulas (quoted from He–Li–Sun 2112.09632; the referee formula-first rule is satisfied):**
- **Three-family conditions (Eq. 3.3/3.4):** I_ab + I_ab′ = 3, and (I_ac, I_ac′) = (−3, 0) or (0, −3). Intersection numbers use our m̃ convention, which equals their 2^{−k}Π(n l − n l) with l = 2m̃.
- **Gauge kinetic function (Eq. 3.5–3.8):** Re f_x = (Re S/4)·[X⁰ − χ₂χ₃X¹ − χ₁χ₃X² − χ₁χ₂X³]_x = (Re S/4)·Re z_x, and g_x⁻² = Re f_x. So **α_x⁻¹ ∝ Re z_x**, fixed by the wrappings and χ.
- **Hypercharge (Eq. 3.9, SM normalisation):** α_Y⁻¹ = (2/3)α_a⁻¹ + α_c⁻¹.

**Stacks and filters:**
- a: U(4) with N_a = 8; b: U(2)_L with N_b = 4; c: U(2)_R with N_c = 4. All are SUSY branes, distinct.
- The three-family conditions above.
- Exact tadpole + K-theory completion by hidden SUSY stacks: count ≥ 1, using the D2082 DP with residual = target − 8X_a − 4X_b − 4X_c.
- **Not filtered (stated):** chiral exotics. The PS → SM Higgsing is taken at M_s. The hypercharge is non-abelian (from SU(4) × SU(2)_R), so it is automatically massless.

**Fit and predict (the same one-loop MSSM-from-M_Z scheme as D2078/D2079, kept for comparability):**
- **Inputs:** α₂⁻¹(M_Z) = 29.59 and α_Y⁻¹(M_Z) = 98.37; b = (b_Y, b₂, b₃) = (11, 1, −3).
- **Unknowns:** an overall K (with α_x⁻¹(M_s) = K·Re z_x) and L = ln(M_s/M_Z). These are solved from the b and Y equations, then α_s(M_Z) is predicted.
- **Physical** means K > 0 and 0 < L < 38.8.
- **Goalposts:**
  - G1: α_s = 0.1180 ± 0.0009, hit if within 2σ;
  - G2: M_s ≥ 4e15 GeV.
- **Unit counted:** a (topology, χ) point. Inequivalent topologies are also reported.

**Positive control (injection, must pass or stop):** synthetic unified couplings (Re z_a = Re z_b = Re z_c) must give α_s = 0.1168 ± 0.0010 and M_s = 2.0e16 GeV (± 10%), the one-loop MSSM unification values computed by hand in this lock.

**Verdict rule:** SIGNAL only if joint hits (G1 & G2) ≥ 3 **and** hits / near ≥ 3 × 0.09, where:
- "near" means |α_s − 0.118| ≤ 0.02 and G2 holds;
- 0.09 is the uniform-density chance that a near point falls in the ±2σ window.

Otherwise NULL. Look-elsewhere: every (topology, χ) point is counted.
