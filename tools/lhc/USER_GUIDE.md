<!-- AEGIS-FP PUIMVMCV2JXDXHQR · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License) -->
# CERN+1 and AEGIS toolkits — user guide

Run any command with `python -m tools.aegis_cli <command>` from the AEGIS folder, or with the one-file program: `aegis <command>` (double-click it for a menu).
Every example below was run on 18 Nov 2026; the output shown is real.

CERN+1 is independent work and is not affiliated with or endorsed by CERN. Free for individuals, scientists and students; business use needs the AEGIS Commercial License.

## Self-test (11 checks against published values)
```
aegis test
```
Output:
```
PASS  CERN+1 dm(1 TeV) [MeV]: 164.108 (expected 164.11 ± 0.05)
PASS  CERN+1 c*tau(1 TeV) [cm]: 5.83071 (expected 5.831 ± 0.01)
PASS  CERN+1 ATLAS 136/fb recast [GeV]: 666.617 (expected 666.6 ± 0.5)
PASS  CERN+1 ATLAS 36/fb recast [GeV]: 447.827 (expected 447.8 ± 0.5)
PASS  CERN+1 exact Poisson N95 (b=n=3): 5.39545 (expected 5.395 ± 0.01)
PASS  Lattice Lab E6 energy at alpha=1.25: 0.104582 (expected 0.10458 ± 5e-05)
PASS  Lattice Lab hexagonal planes in E8: 1120 (expected 1120 ± 0)
PASS  Janus calc phi^2 n_s at N*=60 (exact numerical vs slow-roll 1-2/60.5): 0.966439 (expected 0.9669421487603306 ± 0.002)
PASS  Janus calc phi^2 r at N*=60 (vs slow-roll 8/60.5): 0.132189 (expected 0.1322314049586777 ± 0.003)
PASS  Hyperion MWPotential2014 v_c at R0 [km/s] (Bovy 2015 normalisation: 220): 220 (expected 220.0 ± 0.5)
PASS  Hyperion BBN Y_p at omega_b=0.02236 (PRIMAT, Pitrou+2021: 0.24709): 0.247183 (expected 0.24709 ± 0.0003)

11/11 passed in 1.6s
```

## Wino pair cross sections at 700 GeV, 14 TeV
```
aegis cern xsec 700 14
```
Output:
```
{
 "C1N2p": {
  "sigma_fb": 8.780762319836754,
  "route_spread": 0.007386300822042641,
  "scaling": 8.748333643866168,
  "loglinear": 8.81319099580734
 },
 "C1N2m": {
  "sigma_fb": 3.279917759025885,
  "route_spread": 0.007442687137039228,
  "scaling": 3.267712058168061,
  "loglinear": 3.2921234598837095
 },
 "C1C1": {
  "sigma_fb": 5.646324695796284,
  "route_spread": 0.0077159439052518295,
  "scaling": 5.6245413334844825,
  "loglinear": 5.668108058108085
 },
 "total_fb": 17.707004774658923,
 "mass_GeV": 700.0,
 "sqrt_s_TeV": 14.0,
 "note": "interpolation/scaling error ~1%; add the Resummino PDF+scale uncertainty (5-15%)"
}
```

## Higgsino pair cross sections at 500 GeV, 14 TeV
```
aegis cern higgsino 500 14
```
Output:
```
{
 "N1C1p": 9.95585313634676,
 "N1C1m": 4.207753271677155,
 "C1C1": 7.828613549152232,
 "N1N2": 7.260014904845716,
 "total_fb": 29.252234862021865,
 "mass_GeV": 500.0,
 "sqrt_s_TeV": 14.0,
 "note": "Resummino aNNLO+NNLL tables (2304.11915 Tab. 4); other energies by Drell-Yan scaling"
}
```

## Chargino lifetime at 1 TeV
```
aegis cern life 1000
```
Output:
```
{
 "dm_MeV": 164.10841056185092,
 "Gamma_GeV": 3.3842704948438434e-15,
 "tau_ns": 0.19449153308012132,
 "ctau_cm": 5.8307094762277885,
 "BR_pi": 0.9786043880364436,
 "BR_e": 0.02057423991613105,
 "BR_mu": 0.0008213720474253162
}
```

## ATLAS 136 fb⁻¹ disappearing-track limit with theory band
```
aegis cern limit ATLAS_136
```
Output:
```
{
 "m_limit_GeV": 661.4721749182042,
 "xsec_band_GeV": 9.972573688851185,
 "dm_band_GeV": 0.08103147801818977,
 "total_GeV": 9.972902891334936,
 "published_GeV": 660.0
}
```

## ATLAS 36.1 fb⁻¹ limit
```
aegis cern limit ATLAS_36
```
Output:
```
{
 "m_limit_GeV": 446.42891236144595,
 "xsec_band_GeV": 5.4954868084130055,
 "dm_band_GeV": 0.05062606352032617,
 "total_GeV": 5.495719994663932,
 "published_GeV": 460.0
}
```

## Future-collider reach
```
aegis cern future
```
Output:
```
{
 "HL-LHC": {
  "low_bkg_TeV": 0.9744431085489977,
  "high_bkg_TeV": 0.801418240492046
 },
 "HE-LHC": {
  "low_bkg_TeV": 1.6835880548994777,
  "high_bkg_TeV": 1.3599551855481475
 },
 "FCC-hh": {
  "low_bkg_TeV": 3.7412072845354998,
  "high_bkg_TeV": 2.875516513374163
 }
}
```

## Lattice Lab: hexagonal planes in E8
```
aegis lattice hexagons E8
```
Output:
```
{"lattice": "E8", "min_norm": 1.9999999999999873, "min_vectors": 240, "at_120deg_per_vector": [56], "hexagonal_planes": 1120, "example_plane_gram": [[2.0, -1.0], [-1.0, 2.0]], "shape": "tau=rho (hexagon)"}
```

## Lattice Lab: energy of E6 at α = 1.25 and 2
```
aegis lattice energy E6 1.25,2
```
Output:
```
{"lattice": "E6", "d": 6, "energy": {"1.25": 0.10458150082432871, "2.0": 0.002055919212555546}}
```

## Janus: n_s, r, α_s for V = φ²/2 at N* = 60
```
aegis janus "0.5*phi**2" 60
```
Output:
```
{
 "V": "0.5*phi**2",
 "N_star": 60.0,
 "ns": 0.9664468048271635,
 "r": 0.13218861700871157,
 "alpha_s": -0.0005662789069318062,
 "beta_s": -1.8515743327097914e-05
}
```

## Hyperion: primordial helium and deuterium at the Planck baryon density
Needs the `camb` package (`pip install camb`); not included in the one-file program.
```
aegis hyperion bbn 0.02237
```
Output:
```
{
 "omega_b_h2": 0.02237,
 "dNeff": 0.0,
 "Y_p_nucleon": 0.2471871417270726,
 "Y_p_mass": 0.2458601841277483,
 "D/H": 2.4482576081094778e-05,
 "note": "PRIMAT 2021 tables via CAMB; Y_p_nucleon = 4 n_He/n_b, Y_p_mass = helium mass fraction"
}
```
Y_p_nucleon is CAMB's convention (4 n_He/n_b); Y_p_mass is the helium mass fraction that observers quote (LBT 2026: 0.2458 ± 0.0013).

## Hyperion: Milky Way orbit of Barnard's Star
Inputs: ra, dec (degrees), distance (pc), proper motions pmra, pmdec (mas/yr), radial velocity (km/s). Default potential McMillan17 (needs `galpy`); add `MWPotential2014` as a 7th argument for the older model.
```
aegis hyperion orbit 269.452 4.6934 1.8266 -802.8 10362.4 -110.5
```
Output:
```
{
 "model": "McMillan17",
 "l_deg": 31.00869365619361,
 "b_deg": 14.062737225315729,
 "xyz_kpc": [
  -8.20848024081269,
  0.0009128043849150689,
  0.021239986053722133
 ],
 "v_kms": [
  -130.0833339368338,
  250.22484817476806,
  26.038000078414168
 ],
 "r_peri_kpc": 6.207267505245889,
 "r_apo_kpc": 14.322420838710412,
 "z_max_kpc": 0.6331264844064163,
 "eccentricity": 0.39528867645248633
}
```
r_peri / r_apo: closest and farthest distance from the Galactic centre over 3 Gyr; z_max: greatest height above the disc; eccentricity 0 = circular. The same code computes the Star Mapper orbit feed (validated by lock A8d).

## Late universe: distances to redshift 1 (Planck 2018 cosmology)
Optional extra arguments, in order: H0, ω_b, ω_c, w0, wa, Σm_ν. Checked against astropy's Planck18 to 3 parts in 100,000.
```
aegis late dist 1.0
```
Output:
```
{
 "z": 1.0,
 "params": {
  "H0": 67.66,
  "ombh2": 0.02242,
  "omch2": 0.11933,
  "w0": -1.0,
  "wa": 0.0,
  "mnu": 0.06
 },
 "D_M_comoving_Mpc": 3395.6712667990764,
 "D_A_angular_Mpc": 1697.8356333995382,
 "D_L_luminosity_Mpc": 6791.342533598153,
 "D_H_Mpc": 2485.2619968153786,
 "H_z_kms_Mpc": 120.62811018884723,
 "note": "flat FLRW, photons + 3.046 neutrino species (one massive), CPL dark energy w0 + wa(1-a); agrees with astropy Planck18 to 3e-5"
}
```

## Late universe: an evolving dark energy (w0 = −0.75, wa = −0.86) against DESI DR2 BAO
```
aegis late desi -0.75 -0.86
```
Output:
```
{
 "params": {
  "H0": 67.66,
  "ombh2": 0.02242,
  "omch2": 0.11933,
  "w0": -0.75,
  "wa": -0.86,
  "mnu": 0.06
 },
 "r_d_Mpc": 147.09,
 "chi2": 13.189449685391663,
 "n_points": 13,
 "data": "DESI DR2 BAO, arXiv:2503.14738 Table IV",
 "note": "r_d fixed (default Planck 2018: 147.09 Mpc); no fitting is done here"
}
```
For comparison, ΛCDM (`aegis late desi`) gives χ² = 26.5 on the same 13 numbers, so these values fit the DESI BAO points better, as DESI reported. r_d is held fixed; nothing is fitted. `aegis late growth 0.5` gives the linear growth factor and rate.

## Inflation Scorecard: SERAPIS-E's band against current data
Needs `pyyaml`. Give n_s as one value or a min-max band; add `--r`, `--alpha-s`, `--neff`, `--sum-mnu` as wanted. `--out file.md` saves the table.
```
aegis scorecard --label SERAPIS-E --ns 0.970 0.975 --r 0.0005
```
Output (first rows):
```
| Probe | Dataset | Comparison | Pull (σ) | Verdict | arXiv |
|---|---|---|---|---|---|
| n_s by release | WMAP9 | 0.972 ± 0.013: nearest edge 0.00σ, far edge 0.23σ | +0.00 | consistent | 1212.5226 |
| n_s by release | Planck 2013 | 0.9603 ± 0.0073: nearest edge 1.33σ, far edge 2.01σ | +1.33 | consistent | 1303.5082 |
| n_s by release | Planck 2015 | 0.9655 ± 0.0062: nearest edge 0.73σ, far edge 1.53σ | +0.73 | consistent | 1502.02114 |
| n_s by release | Planck 2018 | 0.9649 ± 0.0042: nearest edge 1.21σ, far edge 2.40σ | +1.21 | consistent | 1807.06211 |
| n_s by release | P-ACT-LB (ACT DR6) | 0.974 ± 0.003: nearest edge 0.00σ, far edge 1.33σ | +0.00 | consistent | 2503.14452 |
| n_s by release | SPA (SPT+Planck+ACT) | 0.9682 ± 0.0032: nearest edge 0.56σ, far edge 2.13σ | +0.56 | consistent | 2512.10613 |
| n_s by release | SPA + DESI BAO | 0.9728 ± 0.0029: nearest edge 0.00σ, far edge 0.97σ | +0.00 | consistent | 2512.10613 |
| running α_s | Planck 2018 | -0.0045 ± 0.0067 | +0.67 | consistent | 1807.06211 |
| running α_s | ACT DR6 (P-ACT-LB) | 0.0062 ± 0.0052 | -1.19 | consistent | 2503.14454 |
| running α_s | ACT+Planck+SPT | 0.008 ± 0.0057 | -1.40 | consistent | 2511.01612 |
| running α_s | DESI DR1 Lya P1D + BAO + CMB | 0.0014 ± 0.0041 | -0.34 | consistent | 2601.21432 |
| running α_s | Planck + eBOSS Lya (Rogers & Poulin) | -0.0108 ± 0.0022 | +4.91 | fail | 2511.01612 |
```
Each row is one published constraint with its arXiv number; the σ column is the distance from the band's nearest edge.

## What the numbers mean
- **Cross sections** (fb): production rate of each wino pair. The quoted spread is interpolation and route error only; add the Resummino PDF and scale uncertainty (5–15%, larger above 1.5 TeV).
- **Lifetime**: `dm_MeV` is the charged–neutral mass gap; `ctau_cm` the mean decay length; `BR_*` the branching ratios.
- **Limit**: the mass below which the wino is excluded, with the band from cross-section and mass-gap theory uncertainty, next to ATLAS's published value.
- **Future**: wino mass reach in TeV for low and high background assumptions.
- **Janus**: `ns` spectral index, `r` tensor-to-scalar ratio, `alpha_s` running, `beta_s` running of the running.

Support: built by one person with the help of AI. To donate, email dannyeldridge54@gmail.com.