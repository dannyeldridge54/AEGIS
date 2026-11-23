# PREREG N1 BIRTH (23 Nov 2026 13:35 CT) — neutron ladder rung 1: the D-T neutron birth spectrum from first principles
Plan: tools/fusion/NEUTRON_LADDER.md. Hints: tools/fusion/hints/n1.json.
## Build (tools/fusion/neutron_birth.py)
Monte Carlo: D and T velocities from Maxwellians at T_i; each pair weighted by sigma_BH(E_cm) * v_rel (Bosch-Hale 1992 cross section, H5);
relativistic kinematics: invariant mass -> CM neutron momentum from the two-body decay (nuclear masses, CODATA via scipy), isotropic in the
CM, boosted to the lab. Weighted mean and variance of the lab neutron energy. 2e6 pairs per temperature, fixed seed.
## Goalposts (locked; Ballabio 1998 fits are the held-out reference, computed by others with full relativistic MC)
B1 mean shift <E_n> - E0 within +-5% of Ballabio at T = 5, 10, 20 keV (E0 from H3).
B2 FWHM = 2 sqrt(2 ln2) sigma within +-2% of Ballabio at T = 5, 10, 20 keV.
B3 can-fail: the same MC WITHOUT the sigma*v_rel weighting must miss B1 by more than 20% at 10 keV (shows the reactivity weighting matters).
B4 E0 (reactants at rest) equals S1's relativistic split 14.028 MeV within 1 keV (atomic vs nuclear masses consistent).
Referee after; DEVIATIONS before any fix; one rerun.
