<!-- AEGIS-FP RLNA2AHP2TZPGRET · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License) -->
# Referee response — CERN+1 v2 (18 Nov 2026)
Referee verdict: NOT READY (all numbers reproduced). Applied:
1 window floor: stated as post-hoc, set from ATLAS (arXiv:2603.08315); recast "reproduces the edge".
2 FCC-hh: locked comparison vs band edge stated (low −17% pass, high −36% fail; −42% vs 6.5); background bands differ (0.2×/5× vs 1×/10×); HL-LHC high variant 0.80 vs 0.5 in abstract.
3 recast caveat: benchmark-anchored, efficiency constant in mass; tests the mass fall-off.
4 HL-LHC: 975 GeV (no syst) and 896 GeV with 20% bkg syst (pyhf N95 = 28.6, recomputed) → 26% / 19% coverage; ITk not modelled.
5 "more accurate" section retitled "What the toolkit adds"; unpropagated PDF/scale error stated; lifetime effect 1.4%; no SModelS/CheckMATE comparison yet.
6 stale "planned modules" sentence removed.
7 abstract converted to prose. 8 SU(2) dropped from T3. 9 κ = −0.163 ± 0.002. 10 μν phase-space wording; BR(π) ≈ 97.9% above 300 GeV.
11 exact Poisson has no bkg uncertainty; ATLAS N95 used. 12 bibliography completed (Resummino authors + EPJC 83, 707; Han–Mukhopadhyay–Wang PRD 98, 035026; AT36 title; Janus-LHC rename explained).
13 independence disclaimer as title footnote. 14 τ0, Φ, βγ, N_b, SR, Run-2 background 3.0 ± 0.7 defined.
Added: D1307 computed boost distribution (661.5 / 446.6 GeV).

## Pass 2 — second-pass referee (18 Nov 2026)
Verdict: READY (after the changes below). All 14 round-1 fixes confirmed. Numbers re-checked against field_tests/results/lhc1–lhc8
and tools/lhc (re-run): kappa −0.161/−0.163/−0.165; LOO 0.016%/0.30%; dm, ctau, BRs; 666.6/447.8 and 661.5/446.6 GeV; pyhf 5.00 vs
Poisson 5.40 at b=n=3; HL-LHC 975.1 GeV (N95 17.6, b 66.2) and 895.6 GeV (pyhf N95 28.6, 20% bkg); coverage 25.9%/19.2%; T1–T3;
future-collider table and kappa=0 diagnostic — all reproduce. Independence/no-endorsement footnote kept.
Changes:
1. Window edge: arXiv:2603.08315 is a different (newer, 137 fb^-1) ATLAS search whose wino-like limit is 670 GeV. "Our recast reproduces
   the edge" -> "our recast of the 136 fb^-1 search (661.5 GeV) lies 1.3% below that edge" (abstract and body).
2. Failures: abstract and rule 5 now list all three locked failures (dm window, T1, FCC-hh high background); rule 5 said "one".
3. "Every step was pre-registered" -> "main tests pre-registered; departures stated". Disclosed: (a) the mu-nu phase-space suppression
   departs from PREREG_LHC2 (lock ignored it; including it lowers BR(mu nu) ~2% -> 0.08% and raises ctau ~2%, recomputed);
   (b) the 20% background-systematic HL-LHC variant was added at review, not locked (975 GeV was locked at 800–1050).
4. "a 1.4% effect at the limit" was ambiguous/wrong: lifetime at the limit is 1.3% below 0.2 ns, and this moves the limit by 0.5%
   (669.8 vs 666.6 GeV, recomputed with fixed 0.2 ns).
5. HL-LHC numbers labelled as fixed beta-gamma = 0.5 (the headline Run-2 limits use the boost distribution).
6. BR(pi) 97.9% -> 97.8–97.9% above 300 GeV (results: 0.9784–0.9786).
7. "The experiments' chain is MadGraph/Pythia/Delphes" -> standard reinterpretation chain (experiments use full simulation).
8. Speed claim marked "not benchmarked here"; pyhf labelled asymptotic.
9. Bibliography: AT26 given its full title (verified on arXiv); AT136 full title; thebibliography width 99. Verified (web): Fiaschi et al.
   EPJC 83, 707 (2023); Han–Mukhopadhyay–Wang PRD 98, 035026 (2018).
Build: pdflatex x2, no undefined references, no overfull boxes.
