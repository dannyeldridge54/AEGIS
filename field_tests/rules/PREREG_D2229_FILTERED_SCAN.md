# PREREG D2229 — filtered Z6-II visible-sector scan for the forces-ring derivation (Danny 17:53: "run a pulse, breathing ping-pong in the
# same session, steering knobs, with ref"). Written before computing, 23 Nov 2026.
Base: tools/seed/z6p_scan.py (D2146 step 3a, T6/Z6' ABa, rho = 1/2, same bulk list z6p_checks3.json, same fractional cycles and filters:
Sym_a = 0, 3 quark doublets, 6 right-handed quarks with one sign, all 12 tadpoles).
Two filters added UP FRONT (the D2228 conclusion):
  F1 tree split: only (a, b) bulk pairs with |ln((V_b/V_a)/1.02)| < ln 1.15 (V = (P+Q) - (2/3) rho (V-U)); at rho = 1/2 this means V_b = V_a
     (78 of 400 ordered bulk pairs).
  F2 massless hypercharge on every survivor: sum_k Y_k N_k (c_k - c_k') = 0 with 6Y = (1, 0, +-3, +-3, 0...) (D2167 test, all four signs).
Also recorded per F1+F2 survivor: chiral visible-hidden intersections (T3), extra massless U(1) count.
Breathing: the scan prints counts every 10 min (inhale = progress, exhale = referee look); cap 60 min (PARTIAL if hit). Steering knob = the
lattice complex structure rho: this breath is rho = 1/2 only; another rho needs its own SUSY bulk list and its own lock (next breath, only
if this one is empty or blocked). No filter is loosened after counts are seen.
Reading fixed now: zero F1+F2 survivors -> the tree-unified massless-Y brane route is closed on Z6-II at rho = 1/2 (in the scanned range);
any -> the first such survivor's N=2 sector content (tori 2 and 3) is the input for Delta b32, Delta b12 (D2225 line Db32 + 0.7 Db12 ~ -3).
Referee in parallel on the code (same session); DEVIATIONS before any fix; one rerun.
