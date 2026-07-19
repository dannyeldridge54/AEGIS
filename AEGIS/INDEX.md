# AEGIS/Seeker — Discovered Equations Index

*Last updated: 2026-07-19T05:21:21.015Z*

| # | Domain | Title | Score | Confidence | Sky Targets | File |
|---|--------|-------|-------|------------|-------------|------|
| 1 | Einstein-Cartan Torsion | Cartan Equation Solution — Spin-Torsion Coupling | -1.957e+0 | HIGH | PSR J0537-6910; PSR J1748-2446ad; Crab Pulsar (PSR B0531+21) | ec-1784438474714 |
| 2 | f(T) Teleparallel Gravity | f(T) Power Law Model — Cosmological Fit | 1.737e+1 | HIGH | eBOSS QSO; eBOSS QSO; eBOSS QSO; eBOSS QSO; Lyman-α Forest | ft-1784438474717 |
| 3 | Torsion Wave Propagation | Torsion Wave Dispersion Relation | 5.274e-3 | HIGH | LIGO Livingston / Hanford; GW170817 remnant | wave-1784438474720 |
| 4 | f(T) Teleparallel Gravity | f(T) Power Law Model — Cosmological Fit | 1.713e+1 | HIGH | eBOSS QSO; eBOSS QSO; eBOSS QSO; eBOSS QSO; Lyman-α Forest | ft-1784438481013 |

## Best Per Domain

### Einstein-Cartan Torsion

**Cartan Equation Solution — Spin-Torsion Coupling** (score: -1.9566e+0, confidence: HIGH)

```
EINSTEIN-CARTAN TORSION SOLUTION
================================
Cartan equation: T^a_bc + δ^a_b T_c - δ^a_c T_b = 8πG · s^a_bc

Torsion components (m⁻¹):
  T⁰₀₁ = 0.982973    T⁰₀₂ = -0.995286    T⁰₀₃ = -0.994990
  T¹₁₂ = 1.008014    T¹₁₃ = -1.002408    T²₂₃ = 0.844616

|T| = 2.3835e+0 m⁻¹
λ (coupling) = -13.8408
σ (spin density) = 1.5488e-2 J·s/m³
```

**Where to look:**

- **PSR J0537-6910** (RA 05h 37m 47s, Dec -69° 10' 20")
  - Survey: millisecond pulsar | z: distance: 49.6 kpc (LMC)
  - Signal: Spin-torsion coupling at σ ~ ~10³⁸ J·s/m³
  - Method: Pulsar timing residuals, gravitational wave phase shift

- **PSR J1748-2446ad** (RA 17h 48m 52s, Dec -24° 46' 48")
  - Survey: millisecond pulsar | z: distance: 7.7 kpc
  - Signal: Spin-torsion coupling at σ ~ ~10³⁹ J·s/m³
  - Method: Pulsar timing residuals, gravitational wave phase shift

- **Crab Pulsar (PSR B0531+21)** (RA 05h 34m 32s, Dec +22° 00' 52")
  - Survey: young pulsar | z: distance: 2.0 kpc
  - Signal: Spin-torsion coupling at σ ~ ~10³⁷ J·s/m³
  - Method: Pulsar timing residuals, gravitational wave phase shift

### f(T) Teleparallel Gravity

**f(T) Power Law Model — Cosmological Fit** (score: 1.7134e+1, confidence: HIGH)

```
f(T) TELEPARALLEL GRAVITY — POWER LAW MODEL
==================================================
Modified Friedmann: H² = (8πG/3)ρ - f(T)/6 + T·f_T/3

Parameters:
  α = 0.008361
  β = 2.735042
  n = 0.9999
  Λ_BI = 200.7530

Cosmological fit: χ²/d.o.f. against 21 H(z) data points
```

**Where to look:**

- **eBOSS QSO** (RA 14h 00m, Dec +30° 00')
  - Survey: SDSS-IV eBOSS | z: z = 1.04 ± 0.05
  - Signal: H(z) deviation: +30.5 km/s/Mpc (24.7%) from ΛCDM
  - Method: Galaxy clustering BAO

- **eBOSS QSO** (RA 14h 00m, Dec +30° 00')
  - Survey: SDSS-IV eBOSS | z: z = 1.30 ± 0.05
  - Signal: H(z) deviation: +24.7 km/s/Mpc (17.3%) from ΛCDM
  - Method: Galaxy clustering BAO

- **eBOSS QSO** (RA 14h 00m, Dec +30° 00')
  - Survey: SDSS-IV eBOSS | z: z = 1.53 ± 0.05
  - Signal: H(z) deviation: -22.1 km/s/Mpc (-13.6%) from ΛCDM
  - Method: Lyman-α forest BAO + QSO

- **eBOSS QSO** (RA 14h 00m, Dec +30° 00')
  - Survey: SDSS-IV eBOSS | z: z = 1.75 ± 0.05
  - Signal: H(z) deviation: +20.7 km/s/Mpc (11.4%) from ΛCDM
  - Method: Lyman-α forest BAO + QSO

- **Lyman-α Forest** (RA 12h 00m, Dec +20° 00')
  - Survey: SDSS-IV eBOSS | z: z = 2.34 ± 0.05
  - Signal: H(z) deviation: -15.5 km/s/Mpc (-6.5%) from ΛCDM
  - Method: Lyman-α forest BAO + QSO

### Torsion Wave Propagation

**Torsion Wave Dispersion Relation** (score: 5.2740e-3, confidence: HIGH)

```
TORSION WAVE DISPERSION
=======================
Wave equation: □δT + m²_eff·δT + 3λT_vev·(δT)² = J_spin

Dispersion: ω² = k² + m²_eff   (massive Klein-Gordon type)

Parameters:
  μ² = 9.9508e-3 eV²
  λ_q = 0.012815
  m_eff = 2.3394e-1 eV
  T_vev = 6.2309e-1 m⁻²
  ω = 0.2296 s⁻¹
  k = 0.0101 m⁻¹
  v_group = 0.044131 c   (subluminal ✓)
  Amplitude = -2.123e+0
  J_spin = -4.137e-2
```

**Where to look:**

- **LIGO Livingston / Hanford** (RA All-sky, Dec All-sky)
  - Survey: LISA (0.1 mHz - 0.1 Hz) | z: local (d < 500 Mpc)
  - Signal: Torsion wave at f = 3.65e-2 Hz, amplitude 2.12e+0
  - Method: Strain signal from torsion-graviton mixing, look for anomalous polarization modes

- **GW170817 remnant** (RA 13h 09m 48s, Dec -23° 22' 53")
  - Survey: LIGO O5+ | z: z ≈ 0.01 (40 Mpc)
  - Signal: Post-merger torsion oscillation at m_T frequency
  - Method: GW post-merger signal deviation from GR prediction

