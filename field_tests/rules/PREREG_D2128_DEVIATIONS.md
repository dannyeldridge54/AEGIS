# D2128 DEVIATIONS (written before the rerun; the first run's P0 PASS is kept as is)

**1. Target misread (P2).** The PREREG target "d adjoints = 4" misread Table 29. "(1,1,1,**4**_Adj,1)" gives the **dimension** of the U(2) adjoint (4 = 3 + 1), in the same notation as 3_Sym and 1_Anti in the same table. So the correct target is **one** adjoint multiplet on d, and 0 on a, b, c, e.
- **Consequence elsewhere:** our K5 β coefficient b_d = 28 (D2112) used φ_Adj = 4 and is wrong. With one adjoint, b_d = 22. The ΔN_eff hidden-multiplet count (D2119 R1-10) also used 4 adjoints. Both are corrected in D2128a; no other verdict depends on them qualitatively.

**2. N=2 sector sign (internal-consistency diagnostic, not target-driven).**
- With the literal one-vanishing-angle rule φ = ½δδ(|I^{(jk)}| − f_j f_k), **6 of the 82** N=2 sectors violate the basic consistency requirement φ ≥ |χ_sector| with φ ≡ χ (mod 2). Example: a c(ωe′) sector with χ = 1 but φ = 0.
- We tested 7 sign conventions for the exceptional term against this requirement alone, without looking at the Table 28/29 targets. **Only φ = ½δδ(|I^{(jk)}| + sgn(I^{(jk)})·f_j f_k) is consistent in all 82 sectors.** This is the natural analogue of the three-angle formula (|I| + sgn(I)ΣI^{Z₂}). Our per-torus f-factors carry the opposite sign convention to HRS's I^{Z₂(i),(jk)}.
- **This rule is adopted.** The P0 calibration (chirality sums, 50/50) is unaffected because it does not use φ.

The rerun evaluates P1–P4 with these two corrections. Nothing else changes.
