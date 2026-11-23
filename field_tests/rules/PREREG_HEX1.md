# PREREG HEX-1 — the hexagon: a centre engine and six node engines in one loop (locked before build/run), 2026-11-23 10:55 CT

Danny 10:44: web it out; every path gets an engine that fully derives; nuclear first-class; "like a hexagon ... all 6 points is
another engine that takes the information that corresponds to that layer and does the same thing ... feed it back to the centre or
another node for postulations ... make it a loop".

Build tools/rings/hex.py on the Ring Engine (D2191) and AEGIS Core (CORE-1):
- BUS: one shared table of quantities; every write carries (node, value, label LIVE/LINEAR/STORED/INPUT, sweep).
- CENTRE: publishes where the fields settle (adopted vacuum point) and the knobs (C, T_R, s_m32); scores the Bloom's 13 terms with
  the Bloom's lnL and BIC (comparable to D2191); judges postulates.
- SIX NODES (each: read bus -> derive with existing tools in-process -> write bus -> local score -> postulates):
  N1 NUCLEAR: Hoyle/carbon window from the forces node's alpha_s shift (weave_nuclear), proton-mass shift (weave_proton), BBN Yp and
     D/H from omega_b and dNeff (janus_astro.bbn, PRIMAT table); local data Yp = 0.245 +- 0.003, D/H = (2.547 +- 0.025)e-5 (PDG 2024).
     Chronos (decay/medical/safeguards) is attached as the node's calculator, on demand.
  N2 FORCES: wino and gluino masses from m32 (AMSB, linear in s_m32 from the adopted 0.687 / 4.93 TeV), alpha_s via the D1937 lever,
     HL-LHC wino pair cross-section at 13.6 TeV (tools/lhc/xsec, valid 100-2000 GeV) -> events at 3000 fb^-1.
  N3 NEUTRINOS/LEPTONS: TM1 theta12, m_bb, Sum m_nu (ring 1); charged-lepton Koide Q (weave_koide) as a check.
  N4 INFLATION: exact SERAPIS pattern (n_s, r, running, N*) at (C, T_R).
  N5 DARK SECTOR: leptogenesis viability and wino relic fraction at T_R (weave_genesis, weave_wino); dNeff (stored 0) to N1.
  N6 LATE UNIVERSE: Janus-LT distances and growth at z = 0.5, 1 (h 0.6736, omega_b 0.02237, omega_c 0.12, w0 -1, wa 0) with
     Sum m_nu from N3 recorded; alpha drift (stored).
- LOOP: sweep the nodes until every bus value changes by < 1e-12 relative (max 6 sweeps) = "where it settles"; then every node may
  post postulates (a knob move with its reason). The centre re-runs the whole hexagon at each postulate and accepts it only if the
  global target (lnL - BIC) rises; moving a knob not already counted costs +1 knob. Rounds repeat until one accepts nothing (NULL).
  v1 postulates: N4 proposes the C that maximises its own n_s/r/running likelihood; N2 proposes the s_m32 that zeroes the alpha_s pull
  through the lever; N1 proposes nothing unless the Hoyle window is left (then it flags the forces node).
Tests:
- H1 settle: the sweep converges (<= 6 sweeps) and a second full loop from the settled state changes nothing (idempotent).
- H2 fidelity: every LIVE bus value equals its standalone tool or Ring Engine value (rel <= 1e-12).
- H3 speed: one full hexagon pass <= 2 s cold, <= 50 ms warm; a full postulate round <= 60 s.
- H4 loop honesty: every postulate is logged with before/after target and accept/reject; the loop ends on a NULL round.
- H5 nuclear: N1 reports Hoyle radius/inside, the proton-mass shift, Yp and D/H with pulls against the PDG values.
Fails recorded as failed-as-locked; fixes via DEVIATIONS first; one rerun.
