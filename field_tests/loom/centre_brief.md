# Centre brief (input for the centre referee N0)

## Still point (three tandem axes)
T_R 1.52e+09, m3/2 2.46e+05, u 0.02663, chi2 12.8
- T (ln m3/2): eigenvalue 100, 1σ step 0.100, INWARD (restoring, stiff)
- S (ln T_R): eigenvalue 1077, 1σ step 0.030, INWARD (restoring, stiff)
- U (ln u): eigenvalue 1108, 1σ step 0.030, INWARD (restoring, stiff)

## Resonance lock map (centre outwards)
- L1 torus (centre, rung step): LOCKED {'quark_window': 0.0285}
- L2 pyramid (i, neutrinos): LOCKED-BY-FIT {'nu_ratio': 0.2852, 'MN_top': 2.2069, 'MN_bottom': 1.8104}
- L3 turnover (rho, leptons): TRUST (no margin; cannot {}
- L4 cube (three tori together): NO LOCK {'rung_agreement': -0.0029}
- L5 fold (volumes, m3/2): LOCKED-BY-FIT {'wino': 0.1805}
- L6 dilaton (inflation): LOCKED-BY-FIT {'n_s': 1.214}
- L7 forces (S-T seam): LOCKED-BY-FIT {'alpha_s': 2.0, 'split_natural': 0.7986}
- L8 cosmology (reheating, genesis): LOCKED-BY-FIT {'gravitino_box': 1.05, 'leptogenesis': 0.1884}
- L9 late universe (thread): TRUST (no margin; cannot {}
- fits spent: ['MN', 'm32', 'TR', 'split']

## Method tests (3 axes)
- coverage 0.892 (bar 0.90), false-balance 0.136 (bar 0.20), dof 3, chi2/dof 4.3
- real-data pulls: {'n_s': -0.71, 'alpha_s': -3.5, 'lnY': 0.01, 'u': 0.0, 'wino_bound': 0.28, 'box': 0.0}

## Where the compass arrows point (review)
- m3/2: RAISE (net +4.00)
- b_prime: LOWER (net -3.00)
- brane threshold: RAISE (net +3.00)
- p in M_N ∝ (Re S)^p: RAISE (net +3.00)
- S-coupled hidden gauge groups: LOWER (net -3.00)
- tan_beta: RAISE (net +1.00)
- Delta3 threshold: RAISE (net +1.00)
- non-universal threshold: RAISE (net +1.00)

## Last knock-ons
- D1885a: flux-6 electron corner offset for Koide delta ⇒ numerics: degenerate-class artefact
- D1894b: one shared rung step (the arrow) ⇒ variables: eps confused with u
- D1946: derive Br(phi->NN) from M_N(S) ⇒ leptogenesis: Br(phi->NN) max 5.1 % < 9.5 % after the 64 pi fix (D1946a)
- D1947: update the wino collider bound with current data (660 -> 660-700 GeV) ⇒ spectrum: derived wino 686.5 GeV now INDETERMINATE at the edge
- D1972: layered resonance: rebalance all knobs together centre-out (3 sweeps) ⇒ predictivity: 4 fits spent (M_N x1.49, m3/2 x1.22, T_R x1.49, A3/A2 0.74); cube layer: lepton/neutrino rung mismatch 15.3 % unresolvable by knobs
