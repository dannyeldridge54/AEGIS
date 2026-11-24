- R89 (23 Nov 2026, PROM-6 devices): misses = T root + SPARC dilution proxy + ARC peaking; ARC tau_E target internally inconsistent; negative
  line radiation unclipped. -> DEV-1..5. Locked FAIL kept.
- R90 (23 Nov 2026, PROM-7 profiles): PASS with caveats; SPARC P2 pass rested on Z_eff 1.32 vs published 1.5 (Be proxy) -> DEV-1 (3He + Z9
  mix meets both); P1 near-unfalsifiable -> consistency check; ARC T_ped 4 keV; "marginal H-mode".
- R91 (23 Nov 2026, PROM-8 SPARC ash/composition): A1 pass not like-with-like (ITER-calibrated 0.6 P_rad,core vs POPCON all-radiation
  separatrix P_loss; synchrotron included vs omitted). -> DEV-1/2 rerun; A2 relabelled composition check.
- R92 (23 Nov 2026, PROM-9 tree): L1/L8/L3 stale goalposts (already corrected in FUSION-1 DEVs); L4 SPARC popcon branch matches cfspopcon
  (tau 0.674 vs 0.673 s at 7.3 keV) yet runs hot (218 MW): steep point, ~20-30% tau optimism amplified. No bug. -> DEV-1 relock, DEV-2 V/n/kappa_A.
- R93 (23 Nov 2026, N1 birth spectrum): sound; shift agreement within MC noise at 5 keV; B2/B4 weak; check FWHM definition -> DEV-1/2 rerun.
- R94 (23 Nov 2026, N3/N4 resonances): BUG - channel-spin sign of AJ ignored (Mn-55 l=1) -> 32% max error in an interference minimum; R3 336 eV
  unsourced (tape ER 340.79 eV). Agreement genuine (NJOY reconr grid). -> DEV-1/2 rerun.
- R95 (23 Nov 2026, N5 Doppler): holds; discriminating; second exponential untested (>1 eV) and thermal check self-referential; edge leak top ~100 eV.
  -> DEV-1 (extend to 1e-5 eV vs NJOY), DEV-2 (exclude top 200 eV).
- R96 (23 Nov 2026, N6-N8 transport): BUG Kalbach-Mann branches swapped (TBR-blind); T4 strawman -> yield-1 can-fail; 8 batches thin;
  "consistent with", not "validated"; target-at-rest is the main untested approximation.
- R97 (23 Nov 2026, N9/N10): no bug; He/dpa failure from the workshop steel's 5 wt% C (78% of He) -> Fe-only scoring; front cm 10.7 dpa/fpy/MWm2.
- R100 (23 Nov 2026, N11 activation): sound, no bug; goalposts weak (A4 tautology, A2 by half-life, A1 T-dependent); headline is the 0 s total.
- R101 (23 Nov 2026, N12): C1/C2 failures are my test errors (pump term omitted; hold = 1 + lambda I0/b, not t_d -> inf); idealised TBR margin ~1%.
- R102 (23 Nov 2026, JET-1 beam-target): model correct; J4 definition mismatch (FAIL stands; sigma peak 108 keV); thermal targets +12.5% (fair fix);
  open: fraction type (current vs power), losses, inputs n_i/n_e, E_b, Te -> overshoot is model+input, not a bug.
- R103 (23 Nov 2026, HARDEN-1): balance real but bookkeeping-only; B3 not independent (Li-6 MT205 == MT105) - not claimed.
- R104 (23 Nov 2026, resonance run 1): d_as is a fit; computed Yukawa 2-loop is -0.0002..-0.0006 (wrong sign); Weave alpha_s 0.1140-0.1147; D/H independent tension.
- R105 (23 Nov 2026, connections 1): P2 wrong sign (light triplets lower alpha_s); P4 partial (~+0.001 usable); no single connection closes alpha_s; next: D7 one-loop threshold.
- R106 (23 Nov 2026, stage map): BLOCKED used to exit the loop - reverted; honest map 4: 27 IN, 5 EDGE, 5 OUT.
- R107 (23 Nov 2026, stage map cycle 3 SPARC): radas units OK; reproduction "0.1%" true but not discriminating; 140/Q11 goalpost not cfspopcon's PRD cell (GOALPOST); P_aux compare vs absorbed+ohmic; BUG hollow density from frozen n_ped -> rerun by PROM-8 recipe: 121 MW / 7.99 MW -> EDGE ceiling.
- R108 (23 Nov 2026, ping-pong leveling, standing referee rounds 1-5): JET model inputs (Ti/Te fixed, D2219, still OUT); alpha_s MS->DR (D2220) + top decoupling (D2221) -> 0.11446 OUT; D/H omega_b error -> -2.07 OUT (prereg EDGE rule overruled by map band); wiring/housekeeping OK (D2222); EDGE sweep all final. Round 5: NULL - BALANCED (no actionable non-tuning finding left); 4 OUTs OBSTRUCTED by named missing inputs.
- R110 (23 Nov 2026, D2236 helm): run 1 BLOCKER - P_sep double-subtracted core radiation; control incompatible with new limit; missing TBR check; rerun audit: HTS 1.28 GW rests on unvalidated synchrotron reflection (not reportable); Nb3Sn-class 330-600 MW reportable with labels; P_sep/R binds.

## R111 (D2243 steady helm pass, 23 Nov 2026) — round 1 NOT BALANCED (2 BLOCKER, 3 MAJOR, 2 MINOR); round 2 NULL — BALANCED
F1 L-H on lenient P_loss vs exhaust Psep (BLOCKER, fixed DEV-1); F2 negative Psep passes via Lengyel clamp (BLOCKER, DEV-2); F3 Psep/R
limit missing (DEV-3); F4 convention label (DEV-4); F5 synchrotron budget unverified (flagged); F6 grid count; F7 impurity iterations.
Consequence: correction D2243a on D2236-D2241 L-H passes.
