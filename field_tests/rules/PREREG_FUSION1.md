# PREREG FUSION-1 — the fusion engine, goal at the top, fractal network beneath (locked before build/run), 2026-11-23 11:00 CT

Danny 10:50: "do the fusion itself. Set that as the goal ... build the engine, set the goalposts, fully derive it, ping-pong,
self-balancing dials, referee every section ... then go back through all suggestions and fixes ... a full fit, derivation, everything."
Danny 10:50: not a hexagon — whatever shape is needed; the geometry is fractal (any engine opens into its own network; links run
backwards and sideways; new shapes form). So: tools/fusion/net.py = a recursive engine graph (an Engine may hold child Engines;
edges may point anywhere, including back up); settle = iterate the graph (children first) to a fixed point; dials = bounded
optimisation of named knobs against named constraints; postulates judged by the parent.

Goal (top node): net electricity from D-T fusion. Sections (child engines), each with goalposts against published values:
S1 REACTIONS. Bosch & Hale (1992) <sigma v> for D-T, D-D(n), D-D(p), D-He3 (coefficients: D-T and D-D from the
   tokamak_neutron_source listing, D-He3 from the paper as recalled, flagged until checked); Q-values from atomic masses (AME/CODATA).
   G1 D-T <sv>(10 keV) = 1.136e-16 cm^3/s and (20 keV) = 4.330e-16 within 0.5% (Bosch-Hale table values as recalled, flagged).
   G2 Q(D-T) = 17.589 MeV +- 0.002; neutron share 14.07/17.59 = 0.7997 +- 0.001 (two-body kinematics).
S2 IGNITION (0-D power balance, D-T 50:50, bremsstrahlung C_B = 5.35e-37 W m^3 keV^-1/2, Z_eff = 1).
   G3 minimum ignition triple product n T tau_E in [2.6, 3.4]e21 keV s m^-3 at T in [11, 16] keV (Wesson, Tokamaks: ~3e21 at ~14 keV).
   G4 ideal-ignition temperature (alpha heating = bremsstrahlung) in [4.0, 4.8] keV (textbook ~4.4 keV).
S3 TOKAMAK OPERATING POINT (self-balancing dials). ITER design inputs: R 6.2 m, a 2.0 m, kappa 1.85, B 5.3 T, I_p 15 MA,
   V 830 m^3, P_aux 50 MW, M 2.5, parabolic profiles (density exponent 0.1, temperature exponent 1.0), Z_eff 1.7, IPB98(y,2) scaling.
   Dials: <T> and <n> solved for power balance at fixed n = 1.0e20 m^-3; then the optimiser maximises Q subject to Greenwald
   n <= I_p/(pi a^2) 1e20 and beta_N <= 2.8.
   G5 at the ITER design point: P_fus in [350, 650] MW and Q in [6, 15] (ITER design 500 MW, Q = 10; a 0-D model, so wide band).
   G6 tau_E(IPB98) in [3.0, 4.4] s (design ~3.7 s).
S4 INERTIAL FUSION (OU's hub, IFE-STARFIRE). Burn fraction Phi = rhoR/(rhoR + 6 g/cm^2); specific yield; gain bookkeeping.
   G7 specific D-T yield = 3.37e11 J/g +- 0.5%; Phi(rhoR = 3) = 1/3 exactly.
   G8 NIF records reproduced as gain bookkeeping only (data, not derivations): Dec 2022 3.15 MJ / 2.05 MJ = 1.54; Feb 2025 gain 2.44
      (yield 5.0 MJ from 2.05 MJ); 8.6 MJ (2025) recorded with laser energy unknown in the source read.
   G9 plant condition: driver efficiency x target gain >= 10 -> required gain at 10% driver efficiency = 100.
S5 FUEL CYCLE. Tritium burn per GW of fusion power; Li-6 use; inventory with decay (Chronos tritium) and a breeding-ratio balance.
   G10 tritium burned = 55.8 kg per GW-full-power-year +- 0.5% (one T per 17.589 MeV; 3.15576e7 s).
S6 NEUTRONS AND MATERIALS. Neutron wall load from fusion power and first-wall area; damage via a published dpa-per-fluence
   conversion read from Gilbert et al. (arXiv:1311.5079) and labelled E.
   G11 ITER-like 500 MW over the first-wall area gives a mean neutron wall load reported with the area used (no tight goalpost: area
      to be sourced); G12 the dpa conversion is quoted with its source and conditions.
S7 STARS (fusion in nature). Gamow peak E0 = (b kT / 2)^(2/3), b = pi alpha Z1 Z2 sqrt(2 mu c^2); width 4 sqrt(E0 kT / 3).
   G13 p+p at 15.7 MK: E0 = 5.9 keV +- 3% (Clayton / standard texts); D-T Gamow peak at a 10 keV plasma reported.
Tests per section are run once; each section goes to an adversarial referee as soon as it is built; all referee findings are
fixed together at the end via DEVIATIONS written first; one rerun. Values marked "as recalled" are checked by the referee.
