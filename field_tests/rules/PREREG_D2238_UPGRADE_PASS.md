# PREREG D2238 — upgrade pass on the two decisive gaps (Danny 19:41 "deep dive, make the whole setup better, as much as you can"). Before computing.
A. BLANKET (TBR margin; real Monte Carlo, the locked N6-N8 code tools/fusion/mc.py and test_n6n8_rerun.py geometry: steel first wall then PbLi
   sphere, 14 MeV source). Knobs: Li-6 enrichment {50% (baseline), 70%, 90%}; first-wall steel {10 cm (baseline), 5 cm}; PbLi thickness 100 cm.
   6 cases x 20000 histories (8 batches x 2500), seeds fixed. Report TBR +- sem, leakage. Goal: TBR >= 1.05 + 2 sem (design margin).
   Control: the 50%/10 cm case must reproduce N8 (1.0209 +- 0.0041) within 2 sem combined.
B. SEEDED DIVERTOR (Lengyel 1981 model, as used in cfspopcon): required argon concentration in the SOL to radiate the exhaust so that the
   target heat flux becomes ~0 (T_t = 5 eV): c_Ar = q_par_u^2 / (2 kappa0 n_u^2 T_u^2 Int_{T_t}^{T_u} sqrt(T) L_Ar(T) dT), kappa0 = 2390,
   q_par_u = (2/3) P_sep B / (2 pi R lambda_q B_pol) (Eich lambda_q), n_u = 0.4 <n> (ASSUMPTION), T_u from the two-point model
   T_u = (3.5 q_par_u L / kappa0)^(2/7), L = pi q95 R, q95 = 3, L_Ar from our OPEN-ADAS tables. Core penalty if the same concentration leaks
   to the core (compression 1, conservative) and if compression is 3 (DEMO-class assumption): P_fus scales as (1 - Z_Ar c_core)^2 with
   Z_Ar = 16, plus line radiation. Machines: the three D2237 machines. ESTIMATE labels; no referee (credits) - self-check only.
Reading fixed now: blanket "margin met" if TBR >= 1.05 + 2 sem; divertor "workable" if c_Ar(SOL) <= 0.05 and the compression-3 core penalty
costs <= 20% of P_fus.
