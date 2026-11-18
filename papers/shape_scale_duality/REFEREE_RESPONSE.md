<!-- AEGIS-FP N4WDHMEYTEMPOAKO · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License) -->
# Referee response — Shape, Scale and Duality (doi:10.5281/zenodo.24339574)

## 18 Nov pass
Verdict on v1: MAJOR REVISION (one numerical error; framing overclaims; no conclusion reversed). All fixes applied in the .tex (v2); rebuilt twice with pdflatex, no undefined references.

Numbers checked from the repo root with python3 (tools/serapis_calc, tools/lattice/lattice_lab.py, field_tests/results/*_2026-11-18.txt, D1276–D1287):
- Epstein s=2,3,4 (5.78334/6.02680, 4.04/11.11/19.80%): reproduced.
- Flip table values: reproduced with lattice_lab (θ−1 at α=1: 0.159595, 0.231536, 0.285764, 0.348752, 0.392541, 0.434176, 0.455763; Δ(1.25): FCC−BCC −8.95e-4, D5−D5* −2.08e-3, E6 −1.60e-3, E7 −2.59e-3, E8 ≤2e-15).
- E8 at α=2 = 1+240e^{−4π} (to 3e-8); E6/E7 convergence 3e-11: reproduced.
- Flow (3600 steps, three starts), moduli counts 0/2/35/299, audited point n_s=0.97439, r=4.82e-4: consistent with D1279 and P5.

### Required issues and changes
1. **Hessian numbers used the wrong Eisenstein normalisation (changes abstract numbers).** v1 quoted ρ: [+3.562,+3.562] V0; i: V=0.1011 V0, [−1.279,+5.779] V0. These came from potentials.py, which uses E_fourier = Σ'/(2ζ(4)). The published model (P3 Eq. for V; pipeline.py/landscape.py with lam=1) uses E = Σ' y²/|m+nτ|⁴, the same convention in which the paper itself quotes E(ρ,2)=5.78334. Recomputed in that convention: ρ: [+7.711,+7.711] V0; i: V=0.1958 V0, [−2.216,+10.012] V0; ratio −0.2214 unchanged; bare E Hessian at i [−3.4268,+15.4805]. Signs, saddle/minimum verdict and all conclusions unchanged. The P5 audit's bare ratio (−3.4278/15.4783) confirms it used the Σ' convention. Convention now stated after Eq. (1); erratum sentence added to the method note. Recommend a D-note correcting D1280's numbers (D1280 qualitative verdict stands).
2. **"The familiar E(ρ,2) and E(i,2)"**: now explicit that 5.78334/6.02680 are E in the convention of Eq. (1) (2.67173/2.78420 after dividing by 2ζ(4)).
3. **Hessian coordinates undefined**: now "with respect to x and y, in units of V0"; signs coordinate-independent, canonical masses need the kinetic metric.
4. **Flip rule presented as our finding (overclaim).** Now stated with its two-line Poisson proof for a duality-closed family, labelled "known in substance" with Cohn–Kumar–Schürmann (PRE 80, 061116, 2009), which also has E6 (low density)/E6* (high density). Hypothesis made explicit: the rule needs one lattice to win for all α>1; constancy is numerical.
5. **"E6/E7 predicted before computed" overstated.** For any L ≠ L*, the tie at α=1 and the sign change of θ_L−θ_L* are automatic from Poisson. Text now says the content of the computation is which member is lower above α=1.
6. **Invalid reason for E6/E7 being non-self-dual.** "Gram determinant 3, 2" does not decide similarity to the dual (D4 has det 4 and is similar to its dual). Replaced by minimal-vector counts (E6 72 vs E6* 54; E7 126 vs E7* 56).
7. **Optimality statements.** Separated universal optimality (all configurations; d=8, 24, CKMRV) from Montgomery (among 2D lattices); added that the d=3 FCC/BCC statement is unproven (Sarnak–Strömbergsson); the families compared in d=3–5 are now listed.
8. **Table I inconsistent with its caption** (header said Δ at 1.25, rows mixed tie values and Δ). Table now has separate columns: θ−1 at α=1 and Δ(1.25), all recomputed; "self-dual" column renamed "L ≃ L*" (similar to dual).
9. **Flow claim "a torus started at any shape flows to it"**: now "every tested starting shape" (three starts). The 3600-step stall is explained as an exact-symmetry/round-off effect, not a physical holding.
10. **Rankin's theorem**: Cassels, Ennola, Diananda added (completion for all s>0); noted it also follows from Montgomery via a Mellin transform.
11. **String section.** "T-duality is the same Poisson map" softened to "shown to be a symmetry by the same Poisson resummation"; analogy flagged as structural (Narain lattice is Lorentzian). The v1 sentence that "a momentum lattice alone" flips "at the self-dual radius" was wrong in 1D (every 1D lattice is similar to its dual); replaced by the correct statement (momenta on Λ*, windings on Λ, similar only if Λ is). Narain (1986) cited. ACD optimality labelled conjectural (bootstrap-identified, constructed from codes); JHEP 11, 118 (2022) added.
12. **Notation clash ρ.** The Kähler combination is now Im S Im T₁ (as in P3), with a note that P5 writes Im S Im ρ.
13. **Abstract–body**: abstract rewritten to match every change above and to label known vs computed.
14. **Bibliography**: verified Resummino-independent refs; added Cassels, Ennola, Diananda, Cohn–Kumar–Schürmann, Sarnak–Strömbergsson, Narain; ACD journal reference. Archive URL wrapped in \url (removed overfull box).

### Headline-claim flags
- Abstract (i) numbers change (Hessians, V(i)); the qualitative claim does not.
- Abstract (iii) is reframed: the flip rule is no longer presented as a new finding, and the E6/E7 "prediction" is downgraded to "which member wins".
- Abstract (iv) wording softened; the shape-only match is unchanged.
