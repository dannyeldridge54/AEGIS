# PREREG D2153: how every finished fit counts in the engine (locked 22 Nov 2026, 21:52 CT, before the pending fits finish)

Danny (21:47): "Can we plug these tests into the engine and have it count?"

## Rule (fixed now; no change after results land)
1. A fit counts only if it was run by a committed, locked script (weave_lcdm_pr4.py / weave_extcmb2.py) under PREREG_D2132 / D2135 / D2151.
2. One ENTRY = one Weave (W) fit and one LCDM (L) fit on the same likelihood set (same CMB variant, same BAO, same SN). Each entry is scored once with the D2132 rule:
   dchi2 = chi2_eff(W) - chi2_eff(L); < -2 PREFERRED, <= +2 CONSISTENT, <= +6 MILD TENSION, > +6 DISFAVOURED.
3. The tally lists every entry and counts entries per class. It does NOT add dchi2 across entries: the entries share Planck/ACT/SPT, DESI and overlapping SN data, so a sum would count the same data several times.
4. Headline entry stays the declared baseline: Planck PR4 (HiLLiPoP) + DESI DR2 + DES-Dovekie. All other entries are robustness checks and are reported as such.
5. A crashed or time-capped run does not count and is listed as "not run". A rerun of a crash is allowed only after a DEVIATIONS note (crash fixes, never result-chasing).
6. Model C (free-CPL comparison) results are stored as evidence but are not part of the W-vs-L tally.
7. CubeMind re-derives each entry's dchi2 blind; its grade is recorded next to the entry but never changes the verdict (the tool's number is the count).

Implementation: tools/weave_cm_v5b/weave_verify.py gains weave_tally(), which rebuilds weave_data/lcdm/WEAVE_TALLY.json from all stored pairs each step.
