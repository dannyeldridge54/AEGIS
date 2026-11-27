# PREREG D2284 — Threshold inputs for the rings engine and the target region for alpha_s (locked 27 Nov 2026)
**Model (one loop, MSSM running, k_Y = 5/3; formula fixed per D2282a F2).** For each N = 2 stabiliser subgroup j (fixed plane j):
delta_a = sum_j b'^j_a Ehat_j / (4 pi), b'^j_a = b^{N=2,j}_a |G_j|/|G|, Ehat_j = E1hat(T_j) + E1hat(U_j), U_j = rho (frozen, 1.0335).
With alpha_1, alpha_2 held to data and b = (33/5, 1, -3):
- Delta(1/alpha_s(M_Z)) = delta_3 - (12/7) delta_2 + (5/7) delta_1 =: Btilde / (4 pi)  [Btilde = sum_j Ehat_j (b'^j_3 - 12/7 b'^j_2 + 5/7 b'^j_1)]
- Delta ln M12 = -2 pi (delta_1 - delta_2)/(28/5); proton lifetime x exp(4 Delta ln M12).
**Engine change.** tools/rings/thresholds.py applies these to the alpha_s and proton terms on top of the m3/2 lever (wino, gluino unchanged:
thresholds depend on T, U only).
**Computed (run once).** At s_m32 = 1 (wino centred): the Btilde interval giving |pull(alpha_s)| <= 1 and <= 2; the Dtilde = sum_j Ehat_j (b'^j_1 - b'^j_2)
range allowed by the proton bound; and the combined Bloom lnL change vs no thresholds. Also the old conflict check: with Btilde at the centre,
does s_m32 = 1 keep wino IN and alpha_s IN at once (PASS = yes).
**Pass criteria fixed now.** Target region reported; conflict check PASS/FAIL. Model 1 is NOT scored here (its b' are not yet computed).
