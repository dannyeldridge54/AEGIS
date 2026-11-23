# PREREG D2187: "Zurvan", our own electroweak-naturalness (Delta_EW) toolkit, a gift for Prof. Howard Baer (OU)
Locked 2026-11-23 ~07:35 CT, before any code is written or run.

## What it is
Zurvan (named for the Persian god of boundless time, Weave time-god naming) reads an SLHA spectrum file
(Isajet/SoftSUSY/SPheno output) and returns Delta_EW and its ordered contributions, following the
definition in Baer et al. (DEW4SLHA, arXiv:2111.03096):
  m_Z^2/2 = [(m_Hd^2 + Sd) - (m_Hu^2 + Su) tan^2b]/(tan^2b - 1) - mu^2,  Delta_EW = 2 max|C_i| / m_Z^2.
Our own route: the radiative terms Su = (1/2v_u) dV1/dv_u, Sd = (1/2v_d) dV1/dv_d are obtained by
NUMERICALLY differentiating the one-loop Coleman-Weinberg potential built from field-dependent mass
matrices (DR-bar, Q from the SLHA file), sector by sector. Sectors in v1: stops, sbottoms, staus,
top, bottom, tau (third family). NOT in v1 (stated in output): first/second-family sfermions,
charginos/neutralinos, Higgs bosons, W/Z, the 2-loop gluino terms. DEW4SLHA includes those; Zurvan v1 is
a leading-sector tool and says so.
It also carries the RPV decaying-wino calculator from D2186b (no change to its physics).

## Locked tests
T1 (formula check): the stop-sector Su(t1), Su(t2), Sd(t1), Sd(t2) from Zurvan's numerical CW derivative must
   agree with the closed forms printed in arXiv:2111.03096 (Eqs. for Sigma_u^u(t1,2), Sigma_d^d(t1,2),
   with Delta_t as printed) to within 1% on three locked test points:
   P1 natural: mQ3=1500, mtR=1300, At=-2500, mu=250, tanb=10, Q=sqrt(mt1 mt2)
   P2 heavy mixing: mQ3=3000, mtR=2000, At=-5000, mu=300, tanb=20
   P3 Weave mini-split: mQ3=mtR=159000, At=0, mu=87600, tanb=1.9
   (y_t = 0.85 at Q for P1/P2, 0.6 for P3 (rough running); g=0.65, g'=0.36; m_Hu^2 chosen per point.)
   If a printed formula disagrees and our CW derivation is independently confirmed by a second numerical
   step size, we record it as a convention difference, NOT a pass.
T2 (closure): the browser JS version must reproduce the Python Delta_EW and the top-3 contributions to 0.1%
   on all three points.
T3 (report, no pass/fail): Delta_EW for the Weave mini-split benchmark P3. Expected very large (unnatural by
   Baer's measure); reported honestly.

## Honesty rules
No claim that Zurvan replaces DEW4SLHA. No claim it is "better" in accuracy; its additions are: runs in a
browser with no install, shows per-sector contributions with an independent CW cross-check, and bundles the
RPV decaying-wino calculator. Referee ping-pong until NULL before anything is sent.
