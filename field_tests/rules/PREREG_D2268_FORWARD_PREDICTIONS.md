# PREREG D2268 — Forward predictions, locked before the next data (27 Nov 2026)

Model point: the adopted Hexagon/rings engine point (C = 1.25e-6, T_R = 8.94e8 GeV, s_m32 = 1; D2210, tools/rings/rings.py), tau-sector at rho
(E-only vacuum; D2264). Values as the engine gives them today. These are scored ONLY against data released after this commit.

| # | Quantity | Our value | Scored by (next release) | Fails if |
|---|---|---|---|---|
| P1 | sin^2 theta12 | 0.318 | JUNO next releases (first data: 0.3092 +- 0.0087) | JUNO central stays <= 0.312 with error <= 0.002 (ours > 3 sigma) |
| P2 | mass ordering | normal | JUNO / DUNE / Hyper-K ordering result | inverted ordering at >= 3 sigma |
| P3 | sum m_nu | 0.0588 eV | DESI DR3, Euclid, CMB lensing | upper bound < 0.058 eV at 95% (with NO prior removed) |
| P4 | m_bb | 3.8 meV | next-generation 0vbb (LEGEND-1000, nEXO) | detection with m_bb > 15 meV |
| P5 | n_s | 0.9745 | Simons Observatory, CMB-S4-class | measured n_s outside 0.9745 +- 3 sigma_new |
| P6 | r | 4.8e-4 | BICEP/Keck, SO, LiteBIRD | detection r > 2e-3 at >= 3 sigma |
| P7 | running alpha_s(CMB) | -1.0e-3 | SO/CMB-S4 + LSS | |alpha_s - (-1.0e-3)| > 3 sigma_new |
| P8 | birefringence ratio beta_reio/beta_rec | 0.997-0.999 | LiteBIRD-class reionisation-bump EB | ratio outside 0.95-1.05 at >= 3 sigma |
| P9 | isotropic beta | ~0.28 deg (POST-DATA, consistency only) | any new independent beta | new beta inconsistent with 0.28 at >= 3 sigma |
| P10 | wino (dark matter) mass | 0.687 TeV (band 0.67-0.70) | LHC Run 3 / HL-LHC disappearing tracks; CTA gamma lines | wino excluded across 0.67-0.70 TeV |
| P11 | dark energy | evolving, w0 + wa < -1 region (w0 -0.78 to -0.86) | DESI DR3, Euclid | DR3+SN combined back to w = -1 within 1 sigma |

Known weak spots carried, not hidden: alpha_s = 0.1142 (-4.2 sigma, OUT now); tau vacuum fork rho vs i (D2264-D2266) OPEN.
Any later change of the model point does NOT update these numbers; a new lock is needed.
