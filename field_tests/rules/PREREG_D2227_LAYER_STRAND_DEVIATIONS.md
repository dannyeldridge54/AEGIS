# D2227 DEVIATIONS (no result was produced; written before the first complete run)
- DEV-0 harness crash: chain() also calls weave_rg2, whose bracket fails at extreme spectra (first failing point aborted the whole run).
  m3/2 needs only chain's first two lines; the script now computes m3/2 with exactly those lines (x = 2 pi sigma/N; W0 = A e^-x (1 + 2x/3);
  m3/2 = sqrt(g_s/2)/Vol W0 M_P) and never calls weave_rg2 (alpha_s comes from the ring engine's lever as locked). Nothing else changes.
