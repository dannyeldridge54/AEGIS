# PREREG PROM-1 — Prometheus loop, cycle 1 (locked before computing), 2026-11-23 11:20 CT
Loop (Danny 10:58): breathe in 20 hints from published sources -> lock -> breathe out (build/compute) -> referee -> DEVIATIONS -> one rerun
-> score against the whole network -> repeat until a cycle accepts nothing (NULL). Working name "Prometheus" (Danny may rename).
Cycle 1 target: S3 ITER check (FUSION-1 rerun: P_fus 340 MW, Q 6.8, P_loss 62 < P_LH). Hints: tools/fusion/hints/cycle1.json (20; act on 1-8).
Changes (all in tools/fusion/fusion.py, S3 only):
 C1 radiation correction (hint 1): P_L = P_alpha + P_aux - 0.6 * P_rad(rho < 0.75); local radiation profiles: bremsstrahlung from the
    profiles; line radiation shaped like n_e^2 (L_z flat, interim, labelled) and scaled to the 27 MW INPUT; synchrotron all inside 0.75 (labelled).
 C2 pedestal profiles (hint 6): T_ped 3.5 keV, n_ped 0.8e20, pedestal top at rho 0.94 (12.5 cm / 2.0 m), T_sep 0.1 keV, n_sep 0.4e20;
    core (1 - (rho/rho_ped)^2)^alpha with alpha_n 0.1, alpha_T 1.0; volume element 2 rho d rho.
 C3 helium ash self-consistent (hint 4): f_He = (alpha birth rate) * 5 tau_E / (V <n_e>), iterated with the power balance (replaces the 3.2% input).
Goalposts (both ITER columns, the 400 MW one is held out — never used to tune):
 P1 500 MW column (n 1.13e20, P_aux 50): P_fus 500 +- 20%, tau_E 3.4 s +- 15%, W 353 MJ +- 15%, beta_N 2.0 +- 15%, P_loss >= P_LH.
 P2 400 MW column (n 1.01e20, P_aux 40, held out): P_fus 400 +- 20%, tau_E 3.7 s +- 15%, Q 10 +- 30%.
 P3 f_He from C3 within [2%, 5%] (table 3.2% average).
 P4 no other section's goalposts change (S1, S2, S4-S7 rerun unchanged).
Accept rule: the cycle's change is kept only if P1 and P2 both improve on the FUSION-1 rerun (distance to the column values) — otherwise it
is recorded and reverted. Referee R84 after the build; deviations first; one rerun.
