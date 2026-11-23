# PROM-7 DEVIATIONS (written before any fix). Locked run: all goals PASS (P1, P2, C1, C2); P3 H98 1.86 vs 1.8.
Referee R90 (sonnet, read-only; sensitivity runs in /tmp): PASS with caveats.
- DEV-1 (fair, published input; affects P2) SPARC composition. The locked run used f_DT 0.85 via a Be-only proxy -> Z_eff 1.32, but SPARC
  publishes Z_eff 1.5 (H4). With Z_eff 1.5 under the Be proxy, P2 = 100 MW (FAIL). SPARC's published mix (Rodriguez-Fernandez 2020): 3He
  minority 5% of n_e + lumped low-Z impurity Z = 9 (+ W 1.5e-5). That mix meets BOTH published numbers exactly at zero ash:
  f_He3 = 0.05, f_Z9 = 0.05/9 = 0.00556 -> f_DT = 0.850, Z_eff = 1.500. Fix: composition() accepts extra species {Z: f}; SPARC uses
  He3 (Z 2) and Z9; Be 0. He ash stays self-consistent on top (engine rule, as for ITER). Z9 line radiation: no ADAS data -> bremsstrahlung only (stated).
- DEV-2 (fair, H13) ARC pedestal temperature 4 keV (published scaling step) instead of 0.39 <T> = 5.46 keV (+~2%).
- DEV-3 (classification) P1 is nearly unfalsifiable once both exponents are solved to the published peaking: relabel P1 as a CONSISTENCY
  check of composition + reactivity integration, not a prediction. The predictive test is P2 (and P3).
- DEV-4 (wording) P2 point: P_loss/P_LH 0.96 -> "marginal H-mode" (TRANSP's own Pnet/Pthr 0.70 is also below 1); with H98 imposed, P_LH is a label, not a check.
One rerun with DEV-1, DEV-2, same goalposts.
