# PREREG N11 ACTIVATION (23 Nov 2026 14:20 CT) — neutron ladder: what the first-wall iron becomes
Plan tools/fusion/NEUTRON_LADDER.md; hints tools/fusion/hints/n11.json. preflight.py OK before computing.
Method: mc.py (post-audit) on the workshop sphere; collision-estimator reaction rates per source neutron in the FRONT 1 cm steel for
Fe-54(n,g) MT102, Fe-56(n,2n) MT16, Fe-54(n,p) MT103, Fe-56(n,p) MT103, Fe-58(n,g) MT102, Fe-54(n,a) MT107 (Fe atoms only; the workshop's C is
excluded as in N10). Normalised to 1 MW/m2 of 14.0 MeV neutron wall load (source energy), 1 full-power year; Bateman single-step (H4) with
NUBASE2020 half-lives (element cards). Report specific activity (Bq per kg of Fe) and dominant nuclides at 0 s, 1 d, 30 d, 1 y, 10 y, 100 y.
Goalposts (locked):
A1 Mn-56 is the largest contributor at shutdown (0 s).
A2 at 1 y cooling the top two are Fe-55 and Mn-54 (either order); at 10 y Fe-55 is the largest.
A3 front-cm Fe He production 60-160 appm per fpy per MW/m2 (H1 range scaled to ~1 MW/m2; spectrum differs: wide band).
A4 can-fail: with Fe-54(n,g) and Fe-56(n,2n) rates set to zero, Fe-55 must NOT be the largest at 10 y.
Referee after; DEVIATIONS before any fix; one rerun.
