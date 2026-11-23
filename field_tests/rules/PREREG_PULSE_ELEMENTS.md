# PREREG PULSE-ELEMENTS — side pulse: atomic data for every element in the public ADAS set (locked before building), 2026-11-23 13:55 CT
Danny 12:04/12:08: while heading for the goalpost, pulse out and collect data on all the other elements; build a full list; grab as much
data as possible. Data: 24 elements (H, He, Li, Be, B, C, N, O, F, Ne, Al, Si, S, Cl, Ar, Cr, Fe, Ni, Cu, Ge, Kr, Mo, Xe, W), 96 ADF11 files
(SCD, ACD, PLT, PRB; preferred year 89, else 96, 85, 50, 12), manifest with sha256 (tools/fusion/adas/all/MANIFEST.json).
Catalogue per element at n_e = 1e19, 1e20, 1e21 m^-3 and 41 temperatures 1 eV - 20 keV (log grid): coronal charge fractions (stored as
mean charge and the dominant charge state), line cooling sum f_z PLT_z, recombination+bremsstrahlung cooling sum f_z PRB_z.
Checks (an element failing any is FLAGGED and kept out of the usable catalogue):
 C1 fractions sum to 1 within 1e-10 everywhere; C2 mean charge non-decreasing with T within 1e-6 (coronal balance); C3 at 20 keV the
 mean charge is >= 0.9 Z for Z <= 18 (light elements essentially stripped); C4 cooling curves finite and positive, and no jump between
 adjacent grid temperatures larger than a factor 30 (no parse artefacts).
Output: field_tests/results/element_catalog.json + a CubeMind memory packet (one record per element, topic "atomic data").
