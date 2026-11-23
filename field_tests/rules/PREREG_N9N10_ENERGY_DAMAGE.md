# PREREG N9+N10 (23 Nov 2026 15:10 CT) — neutron ladder: blanket energy multiplication and first-wall damage (same MC, same sphere)
Plan tools/fusion/NEUTRON_LADDER.md; hints tools/fusion/hints/n9n10.json. MC: tools/fusion/mc.py as it stands after the N6-N8 referee
(any N6-N8 fix applies here too). Geometry/materials: the N6-N8 workshop sphere. Collision estimators per source neutron:
heating-local MT901 (steel + Pb-Li), damage energy MT444 and He production MT207 in the steel shell (500-510 cm).
Derived: M = E_deposited / 14.06 MeV; FW dpa/fpy per MW/m2 = [0.8 T_dam/(2*40 eV)] / N_atoms(steel shell) x S(1 MW/m2) x 3.156e7 s,
with S(1 MW/m2) = 1e6 W/m2 x 4 pi (5 m)^2 / (14.06 MeV); He appm/dpa from MT207 / NRT dpa (C atoms included in N_atoms).
## Goalposts (locked; literature bands, held out)
E1 M within 1.05-1.35 (Pb-Li band H7).
E2 can-fail: M with heating-local replaced by neutron-only MT301 must be lower by > 3% (photon energy matters).
D1 steel-shell average NRT dpa per fpy per MW/m2 within 5-15 (rule of thumb ~10 at the front face; the 10 cm average is lower).
D2 He/dpa within 7-16 appm/dpa.
Referee after; DEVIATIONS before any fix; one rerun.
