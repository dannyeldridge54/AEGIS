# CONNECTIONS 1 — method note (23 Nov 2026 14:50 CT). EXPLORATORY (Danny 14:42: "postulate the connections ... test connections ... see if you can get a balance")
Target imbalance: the forces ring needs delta(alpha_3^-1 at M12) = -0.282 to reach alpha_s 0.118 (D2212). Rule: a connection counts only if its
parameter is fixed or bounded by ANOTHER ring (not by alpha_s); every knock-on (M12, alpha^-1, proton lifetime, wino/DM, T_R) is reported.
Postulates: P1 heavy KK/string threshold tied to Re T; P2 colour-triplet (Wilson-line split) threshold tied to the proton-decay ring;
P3 S-T mixing normalisation kappa in f_a = T + kappa m_a^2 S tied to the reheat ring (x = flux/alpha^-1); P4 sparticle-spectrum thresholds tied to
the m3/2 lever and the wino dark matter. Referee judges; no goalposts.

## Referee R105 (after the scan; /tmp rerun of weave_rg2 with a triplet pair)
- P2 WRONG SIGN (my error, also in the script note): with M_T >> sfermions the triplet is a full supermultiplet; light triplets LOWER alpha_s
  (0.5 M12 -> 0.1130, 0.1 M12 -> 0.1091), as in Murayama-Pierce; effective coefficient ~1.2/2pi, not 12/5. Raising alpha_s would need M_T ~ 4 M12 (outside the EFT).
  Proton: dim-5 at 5e15 GeV safe (~1e37-1e39 yr, order of magnitude); dim-6 stays above Super-K. Factor-2 doublet-triplet split not derived.
- P4 right sign but bounded: gluino x1.2 +0.0009 (band edge); scalars x0.5 would drag the AMSB wino to ~0.35 TeV, below the dark-ring window -> ~+0.001 usable.
- P3 tunable, untied; P1 undetermined. Ranking P4 > P3 > P1 > P2. Baseline offset 0.1147 (/tmp) vs 0.1142 (repo) to reconcile.
- Next derivation: non-universal one-loop string threshold of the actual N = 6 D7 stack, Delta_a ~ b_a^{N=2} ln(Re T |eta(T)|^4) + flux piece;
  Delta_3 - Delta_{1,2} fixes sign and size.
