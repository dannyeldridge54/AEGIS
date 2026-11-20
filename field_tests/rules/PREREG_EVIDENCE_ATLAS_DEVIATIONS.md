# PREREG_EVIDENCE_ATLAS — deviations (written before the code change)
## D1 (20 Nov 2026, 06:26 CT; from referee E-R1–E-R5). This makes the count STRICTER, never looser.
New columns on every row:
- timing: 'future-data' (the prediction was locked before the data were released) · 'locked' (locked before computing, but the data were already public: a blind test, weaker) · 'post-hoc' (the model choice was made after seeing these data).
- kind: 'match' (a measured value agrees) · 'bound' (a limit is not violated) · 'comparison' (fit quality against another model).
- inherited: true when the relation predates the Weave or is standard physics the Weave leaves unchanged (Koide 1982; the TM1 mixing pattern and its sum rule; standard BBN at ΔN_eff ≈ 0, including the lithium failure). Inherited rows test the Weave's embedding, not a new prediction.
Headline evidence (replaces rule 4's headline): P rows that are NOT post-hoc and NOT inherited, one per independent test; reported separately by timing and by kind. Post-hoc and inherited passes are shown as 'consistent, not evidence'. Two helium rows become one headline row (LBT 2026, the newer and more precise). Register items not yet in the atlas are added as open rows.
Assignments are written in the code with a one-line reason each; the expected effect is a smaller headline count.

## D2 (20 Nov 2026, 06:33 CT; from the independent referee of the SERAPIS v3.4 note). Stricter again.
- Thread vs ΛCDM headline: counts as a pass only where ΔAIC < −2 (meaningful); with −0.6 / −6.1 / −1.4 that is 1 of 3 sets → status 'tension' (meaningful on DES-Y5 only).
- S₈ of the thread fits: ΛCDM gives the same S₈ with smaller pulls, so the row does not discriminate → not evidence (shown as consistent).
- 12.8 GeV dark baryon: the xenon limit used (D1677) is an unsourced, non-digitised bracket and survival depends on a free portal coupling → status 'open', not evidence, until the LZ curve at 13 GeV is sourced (D1678).
- Wino gamma line: the wino masses are benchmarks and the thermal wino of SERAPIS-E is post-hoc (D784) → post-hoc, not evidence; 2.9 TeV rows fail both the line limit and the relic density (f > 1) and stay listed as fails.
- Arthur-field coupling: stays a strict FAIL, with the caveat that two of three coupled fits did not converge and no b_A error bars exist.

## D3 (20 Nov 2026, 08:40 CT; from the independent referee of the Weave Control note). Bug fix + completeness; stricter, never looser.
- BUG: the code counted the 12.8 GeV dark-matter row as evidence although D2 says it is 'open, not evidence' until the LZ curve at 13 GeV is sourced. Fix: a row with status 'open' never counts as evidence.
- COMPLETENESS (rule 6, failures stay in): the quark level (added 20 Nov) had no atlas rows. Add three: q-eps (zero-parameter ε of the SUGRA (m,0) minimum vs the quark-fit band; label P, timing locked, kind match; FAIL, D1732); q-tauq (heavy τ_q window vs early-universe limits; label A, a hosted mechanism, locked, bound); q-Rmumu (LHCb R_μμ; label S, the Weave adds nothing; locked, match).
- Wording: the summary key 'consistent_not_evidence' means "headline P rows reported but not counted (post hoc or inherited)"; it contains failures (TM2, lithium-7) and must not be described as "consistent". Key kept for compatibility; meaning recorded here.
