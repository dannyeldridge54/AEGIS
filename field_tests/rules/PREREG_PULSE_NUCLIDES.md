# PREREG PULSE-NUCLIDES — every nuclide (NUBASE2020) + an audit of Chronos and the fusion engine (locked before building), 2026-11-23 14:10 CT
Data: NUBASE2020 (Kondev et al., Chin. Phys. C 45, 030001 (2021)) and AME2020 mass excesses, as shipped in pynucastro 3.2.0 (sha256 in
tools/fusion/nubase/SOURCE.txt). Parse the fixed-column format (A, Z, isomer index, mass excess, excitation, half-life + unit, J^pi,
decay modes) for ground states and isomers.
Checks: N1 ground-state count reported (NUBASE2020 abstract: 3340 nuclides) and isomer count; N2 count of ground states marked stable
reported (the commonly quoted figure is 251 stable nuclides); N3 AUDIT: every half-life hard-coded in Chronos (chronos.py T12 and
chronos_a3.py T12x) compared with NUBASE2020 (1 y = 365.2422 d as NUBASE, Chronos uses 365.25 d: compared in seconds); differences
> 0.5% are FLAGGED and listed (no silent edits); N4 AUDIT: the fusion engine's atomic masses (n, H1, D, T, He3, He4) vs
A + ME/931494.10242 keV within 2e-9 u.
Output: field_tests/results/nuclide_catalog.json (compact) + a CubeMind memory packet summary; flagged audit items go to the D-notes.
