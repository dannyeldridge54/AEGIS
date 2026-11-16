# Referee report, round 6 (16 Nov 2026, 05:40 UTC): SERAPIS v3.1 draft (papers/v3/serapis_v3.tex)
Reviewer: Claude (internal referee pass against D719–D768). Recommendation: major revision before the Zenodo v3.1 upload.

## Major
1. **Stale abstract.**
   - It still says T_R = 10³–10⁵ GeV and that Affleck–Dine with an essentially massless ν₁ is required. D727–D730 give T_R ≈ (0.8–3)e6 GeV at τ = i, and D744–D745 make inflaton-decay (radiative resonant) leptogenesis viable there, so AD is optional.
   - SERAPIS-E, the derived branch (D692–D693, D756), is not mentioned in the abstract at all.
2. **Missing CP condition (D762–D764).** Both vacua and the SERAPIS-E inflaton line Re τ = ½ lie on CP-conserving loci (Novichkov et al., 1905.11970 §4.3).
   - Under generalised CP: ε_CP = 0 on both branches, and δ_CP ∈ {0, π}.
   - Every leptogenesis PASS in the paper (D731, D745) silently assumes high-energy CP phases (complex R; the PMNS phase drops out of H = Y†Y, D763).
   - Must be stated, with the discriminator: discovery of leptonic CP violation excludes the gCP completion.
   - One concrete source is a second torus modulus fixed off its CP locus by a flux relation (2405.18813; D764–D766). It must NOT involve the inflaton (D765: r doubles).
3. **SERAPIS-E microscopic numbers out of date.**
   - "Im S·Im ρ ≈ 190–245N" was replaced in D696 by N_eff = N − N0; with the unique flux-free configuration (5, 1), Im S·Im ρ = 750–975 (375–488 if a stuck brane is half a unit).
   - "Tadpole and K-theory consistency remains to be checked" is outdated: D696 checked the tadpole (3N + N0 + N_flux = 16), and the K-theory probe conditions are trivially met by D3s.
   - With the flux-relation CP source the configuration becomes 3/3/3+1 (D766/D766a).
4. **Superpartner/wino entry.**
   - The table's wino 0.66–2.9 TeV is the τ = i window. For SERAPIS-E at ρ the gravitino chain (D732–D736) narrows it to 0.67–0.80 TeV for a cuspy halo (post-hoc, not locked). That is the model's sharpest near-term collider test and belongs in the table, labelled post-hoc.
   - The disappearing-track bound should cite ATLAS 2603.08315 (670 GeV observed, supersedes 2201.02472).
5. **Origin of the plateau.** State plainly that, as in the SL(2,Z) attractors of 2408.05203, the plateau is placed in the nilpotent (anti-D3) metric by choice (D768). Every in-model route we tried is closed (D703–D760).
   - What distinguishes SERAPIS-E: one function, E(τ,2), gives plateau and tilt, and its r is ≈ 4.5× below the j/Ê₁ attractors at the same metric.

## Minor
6. The axion paragraph covers τ = i only. For SERAPIS-E, Re τ = ½ is also a CP-symmetric line. D769 computes the two-field test; quote it when finished.
7. The log-derivative species form (D758–D759) is a second plateau candidate with r ≈ 2.1–3.1e-4. One sentence in the SERAPIS-E section (labelled post-hoc, no string source per D760).
8. Sec. VIII ("SERAPIS-E") reads as an appendix to the τ = i paper. Consider promoting it in the introduction's list of points.
9. Title: 24 words, and it leads with the τ = i "square torus" vacuum, which is now the less-motivated branch (D688). Shorten and lead with the testable content.
10. The author email is printed in the paper. A standing project rule says not to put it in public files. The v3 PDF already carried it, so this is Danny's decision: keep it or switch to the Zenodo/ORCID contact.

## Checks done
- Every number cited above was taken from the D-notes and result files, not recomputed. D725, D731, D735 and D745 were reproduced in-session tonight (D763 and D767 regressions identical).
- No frozen prediction changes. All revisions are text, labels and post-hoc additions.
