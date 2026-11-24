# CubeMind nuclear brief — everything learned, 23 Nov 2026 (from the AEGIS session)

Read this before any reactor or nuclear task. Labels: PUBLISHED = on Zenodo; ESTIMATE = 0-D model result; CORRECTED = an earlier
claim that was withdrawn. Never state a corrected claim as current.

## Published record (all CC-BY 4.0)
1. Reactor chain, plasma to plant (paper 1): doi:10.5281/zenodo.24486255 — 15 of 21 reactor checks IN, 5 EDGE, 1 OUT.
2. Reactor Paper 2 — Exhaust Is the Wall, v2 corrected: doi:10.5281/zenodo.24488731 (v1 24488146).
3. Reactor Paper 3 — Flipping the Shape (negative triangularity): doi:10.5281/zenodo.24488692.
4. The AEGIS Toolkit: doi:10.5281/zenodo.24488137.
5. How the Elements Are Made: doi:10.5281/zenodo.24488090.
6. Fusion Reactor Field Guide: doi:10.5281/zenodo.24488566.
7. Fusion From Zero (beginner guide): doi:10.5281/zenodo.24488584.
8. Reactor chain talk: doi:10.5281/zenodo.24488749.

## The nuclear ladder (levels) and what we know at each
- L1 Nuclides: NUBASE2020 catalog (weave_data/nuclide_catalog.json, 5,823 rows); binding per nucleon peaks near Fe-56/Ni-62.
- L2 Reactions: Bosch-Hale reactivities; D-T is ~100x easier than D-D near 15 keV.
- L3 Plasma: 0-D engine, IPB98 confinement, OPEN-ADAS radiation (weave_data/element_catalog.json, 24 elements); ITER Q=10 reproduced.
- L4 Neutrons: own Monte Carlo; TBR 1.095 +- 0.003 at 90% Li-6, 10 cm steel wall (clears 1.05 margin). Thin-wall (5 cm) jump SUSPECT.
- L5 Exhaust: Lengyel divertor model, Eich heat-flux width; divertor exhaust is the binding engineering limit.
- L6 Plant: net-power balance with house loads; first-wall life 2.3-4.6 full-power years at 20 dpa.

## Results chain (D-notes D2236-D2246), in order
- D2236 helm: steering R and B raises fusion power; exhaust binds. Its 330-600 MW net plants are CORRECTED (D2243a: H-mode passes used a
  too-forgiving power figure).
- D2237 project-lead pass: 98-99% of exhaust heat must be radiated; heat channel < 1 mm.
- D2238 blanket: 90% Li-6 gives TBR 1.095.
- D2239 breathing optimiser: no design meets every limit (exhaust/H-mode squeeze).
- D2240 long-leg divertor: divertor argon 13.8% -> 4.3% (under 5% cap), but core argon then stops the burn.
- D2241 divertor enrichment 3/5/10: closed; best point fails only H-mode access (that pass is also CORRECTED by D2243a).
- D2243 steady helm pass (4,973-design random search, EU-DEMO H-mode rule f_LH = P_sep/P_LH >= 1.2): no design passes; best f_LH 0.38.
- D2244 negative-triangularity mode (assumes H98 ~ 1 without H-mode, from DIII-D/TCV): as locked, R7 B9 559 MW net and R8 B8 542 MW
  net pass every locked limit, but radiate 93-99% of heating from the core. With a core-radiation cap 0.6 (demonstrated) and P_net > 0:
  no design passes; every net-positive design radiates >= 83% in the core. CORRECTION D2244a: only R7 B9 also passes at enrichment 3.

## World context (Field Guide)
Germany: Fusion Action Plan / Fusion 2040, first plant ~2040. Proxima Fusion (stellarator, HTS): Alpha ~2031, Stellaris by 2040.
Gauss Fusion GIGA mid-2040s. W7-X 2025 records (43 s triple product). SPARC 12.2 T, first plasma projected 2027. Negative
triangularity: H98 >~ 1 in L-mode, ELM-free, 45-55% radiated without L-H limit; detachment needs ~0.9 Greenwald.

## Your work queue (lock first, run once, referee, deviations before any rerun, record a D-note)
1. VERIFY THE CORE RADIATION BUDGET (top priority): synchrotron (wall reflectivity, profile peaking) against a published reference;
   bremsstrahlung and argon line radiation code-to-code. Report P_rad,core / (P_alpha + P_aux) for R7 B9 and R8 B8.
2. L-mode (no-pedestal) profiles for negative-triangularity mode; redo D2244 rescore.
3. Stellarator mode: ISS04 confinement, no plasma current, no H-mode threshold; positive control = reproduce a published W7-X point.
4. Audit the thin-first-wall TBR jump (5 cm), and 3-D effects on TBR margin.
5. Global search that can leave no-burn regions (confirm closed windows are real).
Rules: honest labels (ESTIMATE / UNVERIFIED / SUSPECT); never publish; never claim a corrected result; show every calculation.
