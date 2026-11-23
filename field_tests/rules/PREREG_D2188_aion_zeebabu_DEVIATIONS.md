# D2188 DEVIATIONS (written before any fix or rerun), 2026-11-23 ~08:00 CT
Referee R76: physics core verified (null vectors re-derived, convention right, h+ BRs, mu->e gamma normalisation
reproduces 1402.4491's 1.6e-6 at MEG 5.7e-13, mbb bands recomputed by hand, NuFIT inputs, JS=Py 4e-16).
Defects and fixes:
DEV-1 (blocker): cite the originals: Zee NPB 264 (1986) 99; Babu PLB 203 (1988) 132; Babu & Macesanu hep-ph/0212058;
  Nebot et al. arXiv:0711.0483; plus Herrero-Garcia et al. 1402.4491 (formulas used). Footer + docstring.
DEV-2 (major): the split-Gaussian 1-sigma MC bands ignore the theta23 octant and the flat NO delta; they are REMOVED
  from the headline output and replaced by 3-sigma scan ranges (delta over [0,360), s23^2, s12^2, s13^2 over their
  NuFIT 6.0 3-sigma ranges, both octants), for |f-ratios|, h+ BRs and the |f_mutau| ceiling. The MC bands are kept
  only as "indicative 1-sigma (Gaussian approx.)" in the JSON.
DEV-3 (major): state the mu->e gamma scope: h+-only; the k++ contribution has opposite chirality and adds
  incoherently, so the |f_mutau| ceiling is conservative and depends on m_h only.
DEV-4 (major): DESI wording: "in tension with the DESI DR2+CMB LCDM bound (< 0.0642 eV, 95%); model-dependent;
  applies to any IO model with m3 = 0, not specific to Zee-Babu."
DEV-5..7 (minor): add the overall-scale caveat (tool predicts flavour ratios only, not the scale or the loop function
  I(m_k/m_h); perturbativity and mu bounds push m_h, m_k to the few-TeV scale per 1402.4491); credit Babu & Saad by
  name for 2412.14562; collapse the duplicate ph branch; docstring M proportional to f m_l g* m_l f^T.
DEV-8 (tone, NOT adopted): the referee suggested dropping the lantern banner and the Weave DOI. Danny explicitly asked
  for the lantern header on every gift packet tied to the GitHub; it stays, kept short and humble.
T1/T2 are unaffected (re-run after the edits as a check).

DEV-9 (R76b minor, wording only): the 3-sigma scan is labelled "envelope of the 1D 3-sigma ranges (conservative, ignores correlations)".
