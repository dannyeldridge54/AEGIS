# PREREG RING-1 — one program for the Unified Field's layers (locked before build/run), 2026-11-23 10:45 CT

Danny 10:34: "1 program with speed like yesterday that does the layers ... the rings and where they all settle ... weave it into
1 thing with fastest deriving fits". Source of the layers: UFE v4 (WEAVE_UNIFIED_EQUATION.md: geometry, fields, rings 0-4, the
pattern) and the Bloom's 13 data terms (tools/bloom/bloom_data.json). Nothing new is derived here; this wires what exists.

Build (tools/rings/rings.py): one pass, in-process (no subprocess), memoised, in this order:
  L0 geometry + settle: the adopted vacuum point (weave_point) printed with its labels — where every field settles.
  Ring 0 rung step: weave_rung for the quark rungs (readout only; no data term).
  Ring 1 leptons/neutrinos: TM1 sin^2(theta12) = 1 - 2/(3 cos^2 theta13) from NuFIT 6.0 s13^2 = 0.02224 [LIVE];
         m_bb max and Sigma m_nu from weave_mbb(s12) [LIVE].
  Ring 2 forces: weave_rg one-loop readout; alpha_s stays the Bloom value [STORED] (rg2's alpha_s_unif is a different
         quantity/scheme from the Bloom's 0.1142; not wired until reconciled).
  Ring 3 reheating: weave_genesis(T_R) and weave_wino(T_R) as pass/fail filters; wino, gluino, proton through the Bloom's
         measured lever lnm32 (D1937) [LINEAR RESPONSE].
  Ring 4 thread: alpha_drift [STORED].
  Pattern: serapis_point(C, T_R) exact in-process -> n_s, r, running [LIVE].
  Stored as-is: dNeff, delta_CP, alpha_s, alpha_drift.
Score: the Bloom's own lnL_term per term and target = lnL - 0.5 k ln N, with k = the Bloom's fitted knobs + every knob this
program fits (BIC is charged honestly).
Fit (v1): knob C over [1.0e-6, 1.6e-6] (bounded scalar), T_R fixed at the adopted 8.94e8 GeV, m32 lever s fixed at 1.
Tests:
- R1 speed: one full pass <= 1.5 s cold, <= 50 ms warm (memoised); the C fit <= 30 s.
- R2 fidelity: every LIVE node equals the standalone tool on the same inputs (rel <= 1e-12; serapis via registry worker).
- R3 baseline: at the adopted point, report each LIVE term vs the Bloom's stored "ours" (difference reported, not gated).
- R4 fit: report target before/after, the fitted C, and the Bloom verdict; fitting C counts as +1 knob unless C replaces I1
  (it does not in v1: counted +1).
- R5 map: all 13 terms labelled LIVE / LINEAR RESPONSE / STORED; the count of each reported.
Fails recorded as failed-as-locked; fixes via DEVIATIONS first; one rerun.
