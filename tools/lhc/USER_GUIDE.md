# CERN+1 and AEGIS toolkits — user guide

Run any command with `python -m tools.aegis_cli <command>` from the AEGIS folder, or with the one-file program: `aegis <command>` (double-click it for a menu).
Every example below was run on 18 Nov 2026; the output shown is real.

CERN+1 is independent work and is not affiliated with or endorsed by CERN. Free for individuals, scientists and students; business use needs the AEGIS Commercial License.

## Self-test (9 checks against published values)
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

9/9 passed in 0.6s
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

## What the numbers mean
- **Cross sections** (fb): production rate of each wino pair. The quoted spread is interpolation and route error only; add the Resummino PDF and scale uncertainty (5–15%, larger above 1.5 TeV).
- **Lifetime**: `dm_MeV` is the charged–neutral mass gap; `ctau_cm` the mean decay length; `BR_*` the branching ratios.
- **Limit**: the mass below which the wino is excluded, with the band from cross-section and mass-gap theory uncertainty, next to ATLAS's published value.
- **Future**: wino mass reach in TeV for low and high background assumptions.
- **Janus**: `ns` spectral index, `r` tensor-to-scalar ratio, `alpha_s` running, `beta_s` running of the running.

Support: built by one person with the help of AI. To donate, email dannyeldridge54@gmail.com.