# PREREG D2255 — Lever map: how much better confinement or divertor opens a working design? (locked 2026-11-24)

Why: D2251 closed every NT design at core-radiation caps 0.60/0.67/0.85 and named the levers: confinement above H98 = 1, a divertor
taking more than P_sep/R = 17 MW/m (liquid-metal class), or a stellarator. This study measures the smallest lever values that open
a window, with an EXHAUSTIVE grid (answers R113's 'thin search' point).

Engine: D2251 engine unchanged (NT mode, f_reflect 0.6, Albajar synchrotron, ADAS argon, Lengyel divertor, D2243 consistent Psep).
Physics lever (three passes): H98 = 1.0, 1.2, 1.4 (IPB98 multiplier; 1.2-1.4 is above what NT has shown at reactor-relevant conditions:
LABELLED HYPOTHETICAL). Exhaustive grid per pass: R [6, 7, 8, 9]; B [5, 6, 7, 8, 9]; core Ar [0.0005, 0.001, 0.002, 0.003, 0.005];
leg [3, 5]; P_aux [10, 30, 50]; n_u/<n> 0.6; eta [3, 10]; density 0.9 n_G; blanket 90% Li-6 (1,200 points per pass).
Engineering lever (applied post hoc, no physics change): divertor limit P_sep/R <= 17 (today's design value), 25, 35 MW/m
(liquid-metal / advanced divertor claims; LABELLED UNPROVEN).
All other limits as D2251 (Greenwald, beta_N 2.8, wall 2, coil 20 T HTS, SOL argon 5%, core argon, TBR, P_sep >= 1 MW, P_net > 0)
with core radiated fraction cap 0.85 (highest reported in NT) and 0.67 (EU-DEMO) reported.
Output (fixed now): a 3 x 3 map (H98 x P_sep/R limit) per cap: number of feasible designs, eta-3 count, best P_net design.
Verdict per cell: OPEN / CLOSED. Headline: the weakest lever combination that opens a window, and whether any window exists at
H98 1.0 + P_sep/R 17 (should reproduce D2251's CLOSED - control).
Control: H98 1.0 pass must contain D2251's most-ready R9 B9 Ar 0.5% P_aux 10 point behaviour (burns or solver-marginal; f_rad > 0.85).
Labels: ESTIMATE; levers above today's evidence are HYPOTHETICAL / UNPROVEN. Referee: independent review; fixes only via _DEVIATIONS.md.
