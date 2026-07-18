# Torsion Field Theory — Computational Anomaly & Discovery Report

> **Principal Investigator:** Danny Lee Eldridge
> **Date:** 2026-07-18
> **Report Generated:** 2026-07-18 18:49:53 UTC
> **Engines:** AEGIS v1.0 + Seeker v1.0 (Dual Pincer Configuration)
> **Classification:** Preliminary Computational Results — Pre-Print

---

## Abstract

This report summarizes anomalies, breakthroughs, and key insights discovered by
the AEGIS/Seeker autonomous optimization framework while exploring spacetime
torsion parameter spaces. Two independent engines operate in a pincer strategy —
AEGIS sweeping from exploration toward exploitation while Seeker converges from
the opposite direction — ensuring comprehensive coverage of the torsion field
landscape.

Four torsion theory domains are under continuous investigation:

1. **Einstein-Cartan torsion** — 6-component spin-torsion coupling in Riemann-Cartan geometry
2. **Teleparallel f(T) gravity** — Modified gravity via torsion scalar with cosmological H(z) fitting
3. **UFE torsion functional** — Unified field-energy functional Φ(T, S, K) with physical constraints
4. **Torsion wave propagation** — Massive torsion field equation □T + m²T + λT³ = J

---

## 1. Computational Infrastructure

| Metric | Value |
|--------|-------|
| AEGIS uptime | 23s |
| Seeker uptime | 23s |
| Total function evaluations | 133,175 |
| Total optimization runs | 45 |
| Torsion-specific runs | 1 |
| Active anomaly alerts | 140 |
| Breakthrough events | 44 |
| Key insights | 2 |

**Methodology:** Both engines use adaptive meta-learning across 10 optimization
strategies (gradient descent, Bayesian surrogate, simulated annealing, particle
swarm, evolutionary, novelty search, multi-armed bandit, grid search, random
sampling, pure exploitation). Each run is seeded for reproducibility. UFE
(Useful Function Evaluation) tracking measures optimization efficiency.
Strategy selection adapts online based on observed improvement rates.

**Pincer Strategy:** AEGIS begins each cycle with exploration-heavy profiles
(high exploration rate, curiosity-driven strategies) paired with easy tasks, and
progresses toward exploitation-heavy profiles on harder tasks. Seeker does the
reverse. Each cycle they swap direction, guaranteeing complete coverage.

---

## 2. Torsion Parameter Spaces Under Investigation

### 2.1 Einstein-Cartan Torsion (8 parameters)

Explores the antisymmetric torsion tensor T^a_{bc} in 4D Riemann-Cartan spacetime.
The cost function minimizes the Cartan equation residual:

```
Residual = |T^a_{bc} - 8πG · s^a_{bc}|² + λ · T_{scalar}² + trace penalties
```

| Parameter | Range | Description |
|-----------|-------|-------------|
| T01, T02, T03, T12, T13, T23 | [-1, 1] | 6 independent torsion components |
| spinDensity | [0, 10²⁰] | Spin angular momentum density |
| couplingLambda | [-10, 10] | Torsion-curvature coupling strength |

### 2.2 f(T) Teleparallel Gravity (5 parameters)

Fits modified teleparallel gravity models to 21 observational H(z) data points
(Planck 2018 + BAO + cosmic chronometers, z = 0 to z = 2.34).

Four model types compete:
- **Power law:** f(T) = α·T^n
- **Born-Infeld:** f(T) = λ(√(1 + 2T/λ) − 1)
- **Logarithmic:** f(T) = α·T + β·T·ln(T/T₀)
- **Exponential:** f(T) = α·T(1 − e^{β·T₀/T})

Baseline: ΛCDM with H₀ = 67.4 km/s/Mpc, Ω_m = 0.315.

### 2.3 UFE Torsion Functional (8 parameters)

The unified torsion-energy functional bridging quantum to cosmological scales:

```
Φ(T, S, K) = ∫ [α·T² + β·S·K + γ·∇T·∇T + δ·T⁴ + ε·R·T²] dV
```

Physical constraints enforced:
- **Stability:** α > 0 (positive mass² term)
- **Causality:** v² = 2α/γ ≤ c² (subluminal propagation)
- **Unitarity:** δ > 0 (no ghost modes)
- **Energy conditions:** ρ ≥ 0 (weak energy condition)
- **Solar system:** |T₀| < 10⁻¹⁰ (observational bounds)

### 2.4 Torsion Wave Propagation (6 parameters)

Massive torsion field equation sampled at 50 spacetime points:

```
□T + m²T + λT³ = J
```

| Parameter | Range | Description |
|-----------|-------|-------------|
| mass | [0, 10⁻³ eV] | Torsion field mass |
| coupling | [-1, 1] | Quartic self-coupling |
| amplitude | [-10⁵, 10⁵] | Wave amplitude |
| frequency | [0.1, 100] | Angular frequency |
| phase | [0, 2π] | Phase offset |
| sourceStrength | [-10¹⁰, 10¹⁰] | Spin current source J |

---

## 3. Anomalies Detected

140 anomaly event(s) detected across both engines:

### Anomaly 1: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.8096511543897737e+22 (z=7.0σ from rolling mean 400409606714547044352.000000)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 1
  - score: 1.8096511543897737e+22

### Anomaly 2: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.4558069415155652e+23 (z=7.0σ from rolling mean 3.006021153368673e+21)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 1
  - score: 1.4558069415155652e+23

### Anomaly 3: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 7.0161125389178235e+22 (z=7.0σ from rolling mean 1.6708170994162912e+21)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 1
  - score: 7.0161125389178235e+22

### Anomaly 4: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 3.389177026440168e+21 (z=3.3σ from rolling mean 288363146546345738240.000000)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.6617243020163065
  - score: 3.389177026440168e+21

### Anomaly 5: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.2006881628309038e+23 (z=4.4σ from rolling mean 5.347540925863961e+21)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.8871653919949496
  - score: 1.2006881628309038e+23

### Anomaly 6: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.4301857362773925e+23 (z=7.0σ from rolling mean 2.946164600202153e+21)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 1
  - score: 1.4301857362773925e+23

### Anomaly 7: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.3373409077299646e+23 (z=7.0σ from rolling mean 2.908311904725624e+21)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 1
  - score: 1.3373409077299646e+23

### Anomaly 8: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.9564962432902848e+21 (z=4.0σ from rolling mean 192195577944185044992.000000)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.7987656687882999
  - score: 1.9564962432902848e+21

### Anomaly 9: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.7417663886556183e+21 (z=3.9σ from rolling mean 174328368807643643904.000000)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.7877730029189931
  - score: 1.7417663886556183e+21

### Anomaly 10: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.248496242195059e+21 (z=3.4σ from rolling mean 139493041034531274752.000000)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.6730058076723108
  - score: 1.248496242195059e+21

### Anomaly 11: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.4059094343999753e+21 (z=3.1σ from rolling mean 126200907109462720512.000000)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.6142490157400449
  - score: 1.4059094343999753e+21

### Anomaly 12: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 2.456654327085183e+21 (z=5.1σ from rolling mean 144015906739150864384.000000)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 1
  - score: 2.456654327085183e+21

### Anomaly 13: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.9220287220644074e+21 (z=5.9σ from rolling mean 111869622652992733184.000000)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 1
  - score: 1.9220287220644074e+21

### Anomaly 14: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 944818923446738616320.000000 (z=3.8σ from rolling mean 93004618840047026176.000000)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.7618663899973269
  - score: 944818923446738600000

### Anomaly 15: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 2.975525334243644e+21 (z=4.5σ from rolling mean 235283699597823672320.000000)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.9001430654041332
  - score: 2.975525334243644e+21

### Anomaly 16: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 7.361854121189337e+22 (z=3.8σ from rolling mean 5.406051536073692e+21)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.7606691271138023
  - score: 7.361854121189337e+22

### Anomaly 17: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 6.717908732798729e+22 (z=4.2σ from rolling mean 3.9340928385894093e+21)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.8395178451827325
  - score: 6.717908732798729e+22

### Anomaly 18: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 4.728838756222504e+22 (z=3.7σ from rolling mean 2.590511092029664e+21)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.7410646197147259
  - score: 4.728838756222504e+22

### Anomaly 19: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 7.325942179897385e+22 (z=7.0σ from rolling mean 1.6329004395626638e+21)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 1
  - score: 7.325942179897385e+22

### Anomaly 20: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.6749544089379553e+21 (z=4.1σ from rolling mean 157052815433617080320.000000)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.8252047642036798
  - score: 1.6749544089379553e+21

### Anomaly 21: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.4533750841965997e+21 (z=3.3σ from rolling mean 208032099614660395008.000000)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.6514710268990934
  - score: 1.4533750841965997e+21

### Anomaly 22: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.3530050313138468e+21 (z=3.6σ from rolling mean 157953743358299865088.000000)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.7273444510979983
  - score: 1.3530050313138468e+21

### Anomaly 23: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.4835804151011604e+21 (z=5.6σ from rolling mean 113565320500172537856.000000)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 1
  - score: 1.4835804151011604e+21

### Anomaly 24: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 7.448081538873324e+22 (z=7.0σ from rolling mean 1.5563117345127308e+21)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 1
  - score: 7.448081538873324e+22

### Anomaly 25: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 400424296866073608192.000000 (z=3.0σ from rolling mean 51385285272089649152.000000)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.6080158985936043
  - score: 400424296866073600000

### Anomaly 26: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 429209153077629288448.000000 (z=4.1σ from rolling mean 35274469068140560384.000000)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.821438960438711
  - score: 429209153077629300000

### Anomaly 27: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 448241484529463328768.000000 (z=5.1σ from rolling mean 30837852231693897728.000000)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 1
  - score: 448241484529463300000

### Anomaly 28: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 273632110499020767232.000000 (z=4.5σ from rolling mean 23206701174335426560.000000)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.8913565605164793
  - score: 273632110499020770000

### Anomaly 29: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 9.271006581060045e+22 (z=7.0σ from rolling mean 2.0185729410687288e+21)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 1
  - score: 9.271006581060045e+22

### Anomaly 30: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.4290040654988352e+23 (z=7.0σ from rolling mean 3.069056689736794e+21)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 1
  - score: 1.4290040654988352e+23

### Anomaly 31: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 2.3385185011831456e+21 (z=4.4σ from rolling mean 207918197447377158144.000000)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.880165809691643
  - score: 2.3385185011831456e+21

### Anomaly 32: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 7.966390352924898e+22 (z=7.0σ from rolling mean 1.7529589041047273e+21)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 1
  - score: 7.966390352924898e+22

### Anomaly 33: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 3.1137564315015483e+21 (z=4.3σ from rolling mean 311151948322726739968.000000)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.8544208008373211
  - score: 3.1137564315015483e+21

### Anomaly 34: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 9.460876863762286e+22 (z=6.9σ from rolling mean 2.3288053530106821e+21)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 1
  - score: 9.460876863762286e+22

### Anomaly 35: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.8776689848608558e+22 (z=7.0σ from rolling mean 436629980258225029120.000000)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 1
  - score: 1.8776689848608558e+22

### Anomaly 36: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.2102693272562206e+21 (z=4.1σ from rolling mean 133944490485413249024.000000)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.8182922463748626
  - score: 1.2102693272562206e+21

### Anomaly 37: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.5927554462712758e+23 (z=6.2σ from rolling mean 4.983071375528222e+21)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 1
  - score: 1.5927554462712758e+23

### Anomaly 38: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 8.026841152579887e+22 (z=7.0σ from rolling mean 1.6595948634125482e+21)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 1
  - score: 8.026841152579887e+22

### Anomaly 39: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 480231287766117253120.000000 (z=3.2σ from rolling mean 58764699187128074240.000000)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.6334968282872105
  - score: 480231287766117250000

### Anomaly 40: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 8.28524160902557e+22 (z=7.0σ from rolling mean 1.9443295633388863e+21)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 1
  - score: 8.28524160902557e+22

### Anomaly 41: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 6.274089537773232e+21 (z=6.2σ from rolling mean 287128379417751224320.000000)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 1
  - score: 6.274089537773232e+21

### Anomaly 42: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 2.3132782873780376e+21 (z=5.0σ from rolling mean 159550031675084144640.000000)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.9916919967397639
  - score: 2.3132782873780376e+21

### Anomaly 43: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 8.046246545369152e+22 (z=7.0σ from rolling mean 1.8443746328653741e+21)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 1
  - score: 8.046246545369152e+22

### Anomaly 44: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 6.515827804015255e+21 (z=6.4σ from rolling mean 283602739500830654464.000000)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 1
  - score: 6.515827804015255e+21

### Anomaly 45: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 2.4033325679243585e+21 (z=5.7σ from rolling mean 153758911315396165632.000000)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 1
  - score: 2.4033325679243585e+21

### Anomaly 46: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.3822861618773425e+23 (z=6.7σ from rolling mean 3.674004451477811e+21)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 1
  - score: 1.3822861618773425e+23

### Anomaly 47: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 3.949051655331429e+22 (z=7.0σ from rolling mean 984337163895897325568.000000)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 1
  - score: 3.949051655331429e+22

### Anomaly 48: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.555772928623693e+21 (z=3.1σ from rolling mean 195447108796420849664.000000)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.6203664628611496
  - score: 1.555772928623693e+21

### Anomaly 49: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.034811591396781e+23 (z=4.2σ from rolling mean 5.975201100532951e+21)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.8328537784218109
  - score: 1.034811591396781e+23

### Anomaly 50: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.165512795787562e+23 (z=6.0σ from rolling mean 3.9055779177393894e+21)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 1
  - score: 1.165512795787562e+23

### Anomaly 51: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 6.999024666452761e+22 (z=7.0σ from rolling mean 1.574552326164265e+21)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 1
  - score: 6.999024666452761e+22

### Anomaly 52: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.574558079968859e+23 (z=3.4σ from rolling mean 1.669333991808855e+22)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.680579125872081
  - score: 1.574558079968859e+23

### Anomaly 53: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.3746491173858242e+23 (z=3.2σ from rolling mean 1.638058779127275e+22)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.6356670855302841
  - score: 1.3746491173858242e+23

### Anomaly 54: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.4453952140802027e+23 (z=3.9σ from rolling mean 1.2537676326785176e+22)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.789702550199787
  - score: 1.4453952140802027e+23

### Anomaly 55: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.590264309730091e+23 (z=3.3σ from rolling mean 1.932296732748718e+22)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.663326884774015
  - score: 1.590264309730091e+23

### Anomaly 56: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.3533164042121397e+23 (z=3.2σ from rolling mean 2.3445351150740805e+22)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.6312381391272675
  - score: 1.3533164042121397e+23

### Anomaly 57: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.5104474497221307e+23 (z=4.9σ from rolling mean 8.277581277382844e+21)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.9734941670353667
  - score: 1.5104474497221307e+23

### Anomaly 58: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.383003759279955e+23 (z=7.0σ from rolling mean 3.107955492317027e+21)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 1
  - score: 1.383003759279955e+23

### Anomaly 59: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 8.038992097283966e+21 (z=6.5σ from rolling mean 346626955165413539840.000000)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 1
  - score: 8.038992097283966e+21

### Anomaly 60: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:53 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 2.294714896081002e+21 (z=4.8σ from rolling mean 266805436082463408128.000000)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.9544260710342533
  - score: 2.294714896081002e+21

### Anomaly 61: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:52 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.639677589511337e+23 (z=4.2σ from rolling mean 1.250904935409263e+22)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.8360263654432234
  - score: 1.639677589511337e+23

### Anomaly 62: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:52 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.4417214850643369e+23 (z=4.1σ from rolling mean 1.2124445554826774e+22)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.8228133461229008
  - score: 1.4417214850643369e+23

### Anomaly 63: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:52 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.1356646910832897e+23 (z=4.0σ from rolling mean 9.770376516641124e+21)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.7960588260053156
  - score: 1.1356646910832897e+23

### Anomaly 64: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:52 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 8.801363000863695e+22 (z=3.8σ from rolling mean 7.378968269025765e+21)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.7640071605870168
  - score: 8.801363000863695e+22

### Anomaly 65: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:52 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.0792108646922591e+23 (z=3.6σ from rolling mean 9.238803911622153e+21)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.7114517772743004
  - score: 1.0792108646922591e+23

### Anomaly 66: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:52 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.272044507915267e+23 (z=3.1σ from rolling mean 1.6016885582910177e+22)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.6257633862370441
  - score: 1.272044507915267e+23

### Anomaly 67: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:52 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.0760582070051707e+23 (z=3.6σ from rolling mean 8.713745613237914e+21)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.7207977297927919
  - score: 1.0760582070051707e+23

### Anomaly 68: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:52 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 9.726191852779472e+22 (z=3.9σ from rolling mean 6.343099730587142e+21)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.7721092896088265
  - score: 9.726191852779472e+22

### Anomaly 69: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:52 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.3034949026446044e+23 (z=7.0σ from rolling mean 2.8494983907834237e+21)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 1
  - score: 1.3034949026446044e+23

### Anomaly 70: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:52 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 5.562475263842e+21 (z=6.4σ from rolling mean 252132306735107899392.000000)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 1
  - score: 5.562475263842e+21

### Anomaly 71: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:52 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.4442269000175718e+23 (z=3.0σ from rolling mean 1.965183694118975e+22)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.602856597627303
  - score: 1.4442269000175718e+23

### Anomaly 72: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:52 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.3957566365366425e+23 (z=3.4σ from rolling mean 1.236286509864913e+22)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.6744275269238942
  - score: 1.3957566365366425e+23

### Anomaly 73: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:52 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.5542154099391078e+23 (z=4.4σ from rolling mean 9.365767327660205e+21)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.8821405547252971
  - score: 1.5542154099391078e+23

### Anomaly 74: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:52 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.3936563892155402e+23 (z=5.3σ from rolling mean 5.301781836264068e+21)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 1
  - score: 1.3936563892155402e+23

### Anomaly 75: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:52 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.1810920337337059e+23 (z=7.0σ from rolling mean 2.5144690578329877e+21)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 1
  - score: 1.1810920337337059e+23

### Anomaly 76: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:52 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 2.3110050010784465e+21 (z=4.8σ from rolling mean 174127697967107407872.000000)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.9510741127890723
  - score: 2.3110050010784465e+21

### Anomaly 77: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:52 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.948985056738851e+21 (z=4.5σ from rolling mean 160997467065819463680.000000)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.8944690427602543
  - score: 1.948985056738851e+21

### Anomaly 78: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:52 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.1152851825067645e+23 (z=7.0σ from rolling mean 2.356254936784189e+21)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 1
  - score: 1.1152851825067645e+23

### Anomaly 79: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:52 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.6131696333194388e+23 (z=3.0σ from rolling mean 2.420058442474782e+22)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.6022514107947187
  - score: 1.6131696333194388e+23

### Anomaly 80: anomaly: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:52 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1.2153088463401715e+23 (z=3.7σ from rolling mean 9.67183656257832e+21)
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.7475093351782798
  - score: 1.2153088463401715e+23

### Anomaly 81: anomaly: Seeker: Ackley 3D [±30] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:52 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 4.287120 (z=3.2σ from rolling mean 17.181418)
- **Data:**
  - runId: seeker-ackley-3d-r30-evo-explore-c1
  - confidence: 0.6422506041338985
  - score: 4.287120022199538

### Anomaly 82: anomaly: Seeker: Ackley 3D [±30] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:52 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 6.779319 (z=3.0σ from rolling mean 17.871855)
- **Data:**
  - runId: seeker-ackley-3d-r30-evo-explore-c1
  - confidence: 0.6005507336188077
  - score: 6.7793187074573655

### Anomaly 83: anomaly: Seeker: Ackley 3D [±30] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:52 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 7.624939 (z=3.0σ from rolling mean 18.088877)
- **Data:**
  - runId: seeker-ackley-3d-r30-evo-explore-c1
  - confidence: 0.6074707207954877
  - score: 7.624938986364944

### Anomaly 84: anomaly: Seeker: Ackley 3D [±30] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:52 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 4.395836 (z=3.6σ from rolling mean 18.145533)
- **Data:**
  - runId: seeker-ackley-3d-r30-evo-explore-c1
  - confidence: 0.7241605374596649
  - score: 4.395836434102101

### Anomaly 85: anomaly: Seeker: Ackley 3D [±30] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:52 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 4.818094 (z=3.2σ from rolling mean 17.878580)
- **Data:**
  - runId: seeker-ackley-3d-r30-evo-explore-c1
  - confidence: 0.6418496212339859
  - score: 4.8180938258635635

### Anomaly 86: anomaly: Seeker: Ackley 3D [±30] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:52 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 3.583551 (z=3.1σ from rolling mean 17.222169)
- **Data:**
  - runId: seeker-ackley-3d-r30-evo-explore-c1
  - confidence: 0.6235167304317747
  - score: 3.583551172802356

### Anomaly 87: anomaly: Seeker: Ackley 3D [±30] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:52 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 6.882191 (z=3.0σ from rolling mean 17.657464)
- **Data:**
  - runId: seeker-ackley-3d-r30-evo-explore-c1
  - confidence: 0.6068276625464559
  - score: 6.882191240478736

### Anomaly 88: anomaly: Seeker: Ackley 3D [±30] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:52 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 4.510594 (z=3.7σ from rolling mean 17.852615)
- **Data:**
  - runId: seeker-ackley-3d-r30-evo-explore-c1
  - confidence: 0.745496361820692
  - score: 4.510594168882005

### Anomaly 89: anomaly: Seeker: Rastrigin 5D [±20] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:51 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1601.681103 (z=3.1σ from rolling mean 471.937213)
- **Data:**
  - runId: seeker-rastrigin-5d-r20-evo-explore-c1
  - confidence: 0.6172879149352476
  - score: 1601.6811027817364

### Anomaly 90: anomaly: Seeker: Rastrigin 5D [±20] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:51 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1610.972361 (z=3.1σ from rolling mean 473.554101)
- **Data:**
  - runId: seeker-rastrigin-5d-r20-evo-explore-c1
  - confidence: 0.6182921971390044
  - score: 1610.9723605306299

### Anomaly 91: anomaly: Seeker: Rastrigin 5D [±20] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:51 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1860.477723 (z=3.5σ from rolling mean 481.853492)
- **Data:**
  - runId: seeker-rastrigin-5d-r20-evo-explore-c1
  - confidence: 0.691211720678609
  - score: 1860.4777233489203

### Anomaly 92: anomaly: Seeker: Rastrigin 5D [±20] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:51 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 1488.214331 (z=3.1σ from rolling mean 423.207457)
- **Data:**
  - runId: seeker-rastrigin-5d-r20-evo-explore-c1
  - confidence: 0.6118780730958466
  - score: 1488.2143312689577

### Anomaly 93: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 560880869.718215 (z=3.2σ from rolling mean 83256868.303084)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.6449892168115315
  - score: 560880869.7182146

### Anomaly 94: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 510072620.132472 (z=4.4σ from rolling mean 37971721.690696)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.8804732319325994
  - score: 510072620.13247216

### Anomaly 95: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 423751953.736068 (z=4.7σ from rolling mean 27685186.413668)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.9487121899354296
  - score: 423751953.73606765

### Anomaly 96: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 615436041.592152 (z=3.9σ from rolling mean 61814586.228035)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.7742207160387953
  - score: 615436041.5921515

### Anomaly 97: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 499911740.039478 (z=3.8σ from rolling mean 45103928.627683)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.7651474976147224
  - score: 499911740.03947836

### Anomaly 98: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 606215500.813079 (z=5.2σ from rolling mean 45128635.167479)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 1
  - score: 606215500.8130786

### Anomaly 99: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 463881241.333790 (z=5.0σ from rolling mean 33503661.117690)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 1
  - score: 463881241.33379

### Anomaly 100: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 302731536.323681 (z=3.7σ from rolling mean 28833689.842051)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.7474752414647692
  - score: 302731536.32368135

### Anomaly 101: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 416841055.002541 (z=3.7σ from rolling mean 42258538.915762)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.7422579549121313
  - score: 416841055.0025409

### Anomaly 102: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 510741386.515667 (z=5.7σ from rolling mean 33458811.314763)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 1
  - score: 510741386.5156675

### Anomaly 103: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 177114368.657218 (z=3.1σ from rolling mean 25055976.421111)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.6113192740826416
  - score: 177114368.65721813

### Anomaly 104: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 581590093.758485 (z=3.3σ from rolling mean 94192734.383092)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.6538587761378089
  - score: 581590093.7584854

### Anomaly 105: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 601306998.966514 (z=3.9σ from rolling mean 78565530.652903)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.7851795891135553
  - score: 601306998.966514

### Anomaly 106: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 456964402.244679 (z=3.8σ from rolling mean 55279283.134424)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.7527225526772697
  - score: 456964402.24467874

### Anomaly 107: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 355078642.889178 (z=3.4σ from rolling mean 46149142.892950)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.6847906883687942
  - score: 355078642.889178

### Anomaly 108: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 342114714.826501 (z=3.3σ from rolling mean 38725387.320992)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.657830906059715
  - score: 342114714.8265007

### Anomaly 109: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 317467313.610762 (z=3.5σ from rolling mean 34040220.977231)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.6920098533274638
  - score: 317467313.61076224

### Anomaly 110: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 627515855.814964 (z=3.5σ from rolling mean 89638607.659322)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.6937095763231576
  - score: 627515855.8149644

### Anomaly 111: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 626722786.674348 (z=3.5σ from rolling mean 80403175.637610)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.7047887959067085
  - score: 626722786.6743485

### Anomaly 112: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 565060478.521561 (z=3.1σ from rolling mean 83170514.080062)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.6237276470000903
  - score: 565060478.5215605

### Anomaly 113: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 577040305.377200 (z=3.8σ from rolling mean 74307561.432947)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.7689391586182526
  - score: 577040305.3772

### Anomaly 114: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 464325802.405123 (z=3.9σ from rolling mean 56091544.081767)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.7780526361152065
  - score: 464325802.4051232

### Anomaly 115: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 317712630.018777 (z=3.5σ from rolling mean 37771722.953179)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.70776184255214
  - score: 317712630.01877725

### Anomaly 116: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 364072389.282103 (z=4.6σ from rolling mean 27835061.836237)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.913296390955764
  - score: 364072389.28210324

### Anomaly 117: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 592709900.794517 (z=3.4σ from rolling mean 94836094.009388)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.6781025258407337
  - score: 592709900.7945173

### Anomaly 118: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 585023728.832521 (z=3.4σ from rolling mean 87065813.190160)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.6792435133037767
  - score: 585023728.8325208

### Anomaly 119: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 486390076.776226 (z=3.2σ from rolling mean 75390297.503954)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.6389671399566089
  - score: 486390076.7762255

### Anomaly 120: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 608236513.675101 (z=3.4σ from rolling mean 70694387.539346)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.6869977222512021
  - score: 608236513.6751007

### Anomaly 121: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 587600755.513946 (z=3.9σ from rolling mean 57598437.351338)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.7754213390909994
  - score: 587600755.5139462

### Anomaly 122: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 511519585.160368 (z=3.7σ from rolling mean 74544131.927787)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.7489221449865493
  - score: 511519585.1603677

### Anomaly 123: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 502833348.063868 (z=4.5σ from rolling mean 60489879.266053)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.8959764504577205
  - score: 502833348.0638681

### Anomaly 124: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 619886124.904736 (z=3.7σ from rolling mean 71526819.297191)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.7428731180949126
  - score: 619886124.9047359

### Anomaly 125: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 514488548.777323 (z=3.6σ from rolling mean 59893031.373324)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.7266349408724038
  - score: 514488548.7773228

### Anomaly 126: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 470706220.744125 (z=3.6σ from rolling mean 57832131.636797)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.712574898289758
  - score: 470706220.7441255

### Anomaly 127: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 380502291.729022 (z=3.1σ from rolling mean 56818429.615273)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.6111315528291208
  - score: 380502291.72902185

### Anomaly 128: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 390346020.729990 (z=3.4σ from rolling mean 53579600.669675)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.6764001412919453
  - score: 390346020.72999

### Anomaly 129: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 557331349.228565 (z=3.6σ from rolling mean 61322199.837749)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.7121916276337363
  - score: 557331349.2285653

### Anomaly 130: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 592990525.747450 (z=4.0σ from rolling mean 55667737.980006)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.7907128518501871
  - score: 592990525.7474501

### Anomaly 131: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 560569323.698914 (z=3.2σ from rolling mean 68079248.144578)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.6349085914368111
  - score: 560569323.6989143

### Anomaly 132: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 599562580.768010 (z=3.9σ from rolling mean 56695758.161578)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.7835284980960822
  - score: 599562580.7680103

### Anomaly 133: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 622205896.972078 (z=5.0σ from rolling mean 45082121.274256)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 1
  - score: 622205896.9720784

### Anomaly 134: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 437874312.913228 (z=3.3σ from rolling mean 55606476.022657)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.6652035863708663
  - score: 437874312.9132279

### Anomaly 135: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 465052415.299908 (z=3.1σ from rolling mean 68383865.924063)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.6204905878914997
  - score: 465052415.2999084

### Anomaly 136: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 530279280.967363 (z=3.3σ from rolling mean 65292336.345024)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.6605269227878472
  - score: 530279280.96736336

### Anomaly 137: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 513869643.809044 (z=4.0σ from rolling mean 39985100.143292)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.8091013074450737
  - score: 513869643.8090444

### Anomaly 138: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 541546292.782994 (z=5.4σ from rolling mean 30377476.894932)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 1
  - score: 541546292.7829942

### Anomaly 139: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 390646325.510735 (z=6.1σ from rolling mean 17537436.206269)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 1
  - score: 390646325.51073515

### Anomaly 140: anomaly: Seeker: Rosenbrock 2D [±50] [evo-explore]

- **Severity:** WARNING
- **Time:** 2026-07-18 18:49:50 UTC
- **Category:** anomaly
- **Detail:** Anomalous score 621530956.003185 (z=3.6σ from rolling mean 72522457.550476)
- **Data:**
  - runId: seeker-rosenbrock-2d-r50-evo-explore-c1
  - confidence: 0.7207994264242562
  - score: 621530956.0031852

## 4. Breakthroughs

44 breakthrough event(s):

### Breakthrough 1: new best: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** INFO
- **Time:** 2026-07-18 18:49:53 UTC
- **Detail:** Major improvement: 0.0014 → 0.0005 via exploit
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.6598556090739304
  - score: 0.0004612473702227028

### Breakthrough 2: 🔥 Breakthrough: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** BREAKTHROUGH
- **Time:** 2026-07-18 18:49:53 UTC
- **Detail:** Score jumped 0.001356 → 0.000461 (66.0% improvement) via exploit at eval #2764
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - previousBest: 0.0013560340329791146
  - newBest: 0.0004612473702227028
  - improvement: 0.0008947866627564118
  - strategy: exploit
  - eval: 2764
  - params: `{"T01":0.0048354081925455535,"T02":-0.0064482948157352634,"T03":0.009116092410948242,"T12":0.0009387215106181519,"T13":-0.009974624454397146,"T23":0.015764655378725144,"spinDensity":0,"couplingLambda":-2.6135506891868188}`

### Breakthrough 3: new best: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** INFO
- **Time:** 2026-07-18 18:49:53 UTC
- **Detail:** Major improvement: 0.0026 → 0.0014 via exploit
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.4861537532101433
  - score: 0.0013560340329791146

### Breakthrough 4: 🔥 Breakthrough: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** BREAKTHROUGH
- **Time:** 2026-07-18 18:49:53 UTC
- **Detail:** Score jumped 0.002639 → 0.001356 (48.6% improvement) via exploit at eval #2476
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - previousBest: 0.0026389879101981263
  - newBest: 0.0013560340329791146
  - improvement: 0.0012829538772190117
  - strategy: exploit
  - eval: 2476
  - params: `{"T01":0.01768642579452833,"T02":-0.005444479581627,"T03":0.023419544709519877,"T12":-0.023824931097370772,"T13":-0.02025468705491195,"T23":-0.002917726307968032,"spinDensity":0,"couplingLambda":-2.8435524633927884}`

### Breakthrough 5: new best: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** INFO
- **Time:** 2026-07-18 18:49:52 UTC
- **Detail:** Major improvement: 0.0054 → 0.0028 via exploit
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.48807483035490296
  - score: 0.0027618131864778415

### Breakthrough 6: 🔥 Breakthrough: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** BREAKTHROUGH
- **Time:** 2026-07-18 18:49:52 UTC
- **Detail:** Score jumped 0.005395 → 0.002762 (48.8% improvement) via exploit at eval #1379
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - previousBest: 0.005394954868877666
  - newBest: 0.0027618131864778415
  - improvement: 0.002633141682399825
  - strategy: exploit
  - eval: 1379
  - params: `{"T01":-0.01794823842842041,"T02":0.021310198157411624,"T03":-0.030948287023980385,"T12":-0.0017145987353084195,"T13":-0.03401872171250395,"T23":-0.01915512685879258,"spinDensity":0,"couplingLambda":-2.17427409633053}`

### Breakthrough 7: new best: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** INFO
- **Time:** 2026-07-18 18:49:52 UTC
- **Detail:** Major improvement: 0.0114 → 0.0054 via exploit
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.5258278595121065
  - score: 0.005394954868877666

### Breakthrough 8: 🔥 Breakthrough: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** BREAKTHROUGH
- **Time:** 2026-07-18 18:49:52 UTC
- **Detail:** Score jumped 0.011378 → 0.005395 (52.6% improvement) via exploit at eval #1364
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - previousBest: 0.011377629363308007
  - newBest: 0.005394954868877666
  - improvement: 0.005982674494430341
  - strategy: exploit
  - eval: 1364
  - params: `{"T01":-0.008602341250498304,"T02":0.026528640329890982,"T03":-0.025835164670564938,"T12":-0.021526322595327496,"T13":-0.03581716399097187,"T23":-0.046393036275304785,"spinDensity":0,"couplingLambda":-1.7824014073366299}`

### Breakthrough 9: new best: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** INFO
- **Time:** 2026-07-18 18:49:52 UTC
- **Detail:** Major improvement: 0.0151 → 0.0116 via exploit
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.23063229294882245
  - score: 0.01164994247458248

### Breakthrough 10: 🔥 Breakthrough: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** BREAKTHROUGH
- **Time:** 2026-07-18 18:49:52 UTC
- **Detail:** Score jumped 0.015142 → 0.011650 (23.1% improvement) via exploit at eval #1247
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - previousBest: 0.015142229609862657
  - newBest: 0.01164994247458248
  - improvement: 0.003492287135280178
  - strategy: exploit
  - eval: 1247
  - params: `{"T01":-0.03527514072005875,"T02":0.004573168610444482,"T03":0.022290192221572996,"T12":0.04929629952175271,"T13":-0.06915395971381665,"T23":-0.05814606844272187,"spinDensity":0,"couplingLambda":-1.9404528958840122}`

### Breakthrough 11: new best: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** INFO
- **Time:** 2026-07-18 18:49:52 UTC
- **Detail:** Major improvement: 0.0197 → 0.0151 via exploit
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.22944737148806693
  - score: 0.015142229609862657

### Breakthrough 12: 🔥 Breakthrough: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** BREAKTHROUGH
- **Time:** 2026-07-18 18:49:52 UTC
- **Detail:** Score jumped 0.019651 → 0.015142 (22.9% improvement) via exploit at eval #1075
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - previousBest: 0.019651129656263523
  - newBest: 0.015142229609862657
  - improvement: 0.0045089000464008655
  - strategy: exploit
  - eval: 1075
  - params: `{"T01":-0.06817343555416502,"T02":0.043631121793272915,"T03":0.058464751483669024,"T12":0.06494999663719567,"T13":-0.058178675358383,"T23":-0.02493205896029382,"spinDensity":0,"couplingLambda":-1.9377518567719287}`

### Breakthrough 13: new best: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** INFO
- **Time:** 2026-07-18 18:49:52 UTC
- **Detail:** Major improvement: 0.0254 → 0.0197 via exploit
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.22730780188983885
  - score: 0.019651129656263523

### Breakthrough 14: 🔥 Breakthrough: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** BREAKTHROUGH
- **Time:** 2026-07-18 18:49:52 UTC
- **Detail:** Score jumped 0.025432 → 0.019651 (22.7% improvement) via exploit at eval #933
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - previousBest: 0.025432028049883197
  - newBest: 0.019651129656263523
  - improvement: 0.005780898393619675
  - strategy: exploit
  - eval: 933
  - params: `{"T01":-0.05322869485430986,"T02":0.0368369265639416,"T03":0.0918849369174938,"T12":0.055080995947046386,"T13":-0.06479802957396641,"T23":-0.04998046044634442,"spinDensity":0,"couplingLambda":-1.8528807837566974}`

### Breakthrough 15: new best: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** INFO
- **Time:** 2026-07-18 18:49:52 UTC
- **Detail:** Major improvement: 0.0720 → 0.0269 via bayesian
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.6256925654888739
  - score: 0.026948506930607272

### Breakthrough 16: 🔥 Breakthrough: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** BREAKTHROUGH
- **Time:** 2026-07-18 18:49:52 UTC
- **Detail:** Score jumped 0.071996 → 0.026949 (62.6% improvement) via bayesian at eval #629
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - previousBest: 0.07199564968781359
  - newBest: 0.026948506930607272
  - improvement: 0.045047142757206324
  - strategy: bayesian
  - eval: 629
  - params: `{"T01":-0.07852309656791585,"T02":-0.014175461486508292,"T03":0.10517911953159689,"T12":0.09309118849486382,"T13":0.0024176402786499976,"T23":-0.056504654091126955,"spinDensity":0,"couplingLambda":-1.2828331522947356}`

### Breakthrough 17: new best: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** INFO
- **Time:** 2026-07-18 18:49:52 UTC
- **Detail:** Major improvement: 0.1903 → 0.0720 via bayesian
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - confidence: 0.6215859211072707
  - score: 0.07199564968781359

### Breakthrough 18: 🔥 Breakthrough: AEGIS: Einstein-Cartan Torsion [surgical-exploit]

- **Severity:** BREAKTHROUGH
- **Time:** 2026-07-18 18:49:52 UTC
- **Detail:** Score jumped 0.190256 → 0.071996 (62.2% improvement) via bayesian at eval #628
- **Data:**
  - runId: aegis-einstein-cartan-surgical-exploit-c1
  - previousBest: 0.19025626609474677
  - newBest: 0.07199564968781359
  - improvement: 0.11826061640693318
  - strategy: bayesian
  - eval: 628
  - params: `{"T01":0.09660747921236702,"T02":0.05186021237001413,"T03":0.013340160411727489,"T12":-0.19304523261343395,"T13":-0.0015605082199514342,"T23":-0.09504730469987577,"spinDensity":0,"couplingLambda":1.6698748447534595}`

### Breakthrough 19: new best: Seeker: Ackley 3D [±30] [evo-explore]

- **Severity:** INFO
- **Time:** 2026-07-18 18:49:52 UTC
- **Detail:** Major improvement: 4.5106 → 3.5836 via evolutionary
- **Data:**
  - runId: seeker-ackley-3d-r30-evo-explore-c1
  - confidence: 0.20552569381550578
  - score: 3.583551172802356

### Breakthrough 20: 🔥 Breakthrough: Seeker: Ackley 3D [±30] [evo-explore]

- **Severity:** BREAKTHROUGH
- **Time:** 2026-07-18 18:49:52 UTC
- **Detail:** Score jumped 4.510594 → 3.583551 (20.6% improvement) via evolutionary at eval #288
- **Data:**
  - runId: seeker-ackley-3d-r30-evo-explore-c1
  - previousBest: 4.510594168882005
  - newBest: 3.583551172802356
  - improvement: 0.9270429960796487
  - strategy: evolutionary
  - eval: 288
  - params: `{"x0":-0.048701227959257354,"x1":-0.7032441175223139,"x2":0.4145820788409722}`

### Breakthrough 21: new best: Seeker: Ackley 3D [±30] [evo-explore]

- **Severity:** INFO
- **Time:** 2026-07-18 18:49:52 UTC
- **Detail:** Major improvement: 8.4122 → 4.5106 via evolutionary
- **Data:**
  - runId: seeker-ackley-3d-r30-evo-explore-c1
  - confidence: 0.46380085284162176
  - score: 4.510594168882005

### Breakthrough 22: 🔥 Breakthrough: Seeker: Ackley 3D [±30] [evo-explore]

- **Severity:** BREAKTHROUGH
- **Time:** 2026-07-18 18:49:52 UTC
- **Detail:** Score jumped 8.412162 → 4.510594 (46.4% improvement) via evolutionary at eval #172
- **Data:**
  - runId: seeker-ackley-3d-r30-evo-explore-c1
  - previousBest: 8.412162146818375
  - newBest: 4.510594168882005
  - improvement: 3.90156797793637
  - strategy: evolutionary
  - eval: 172
  - params: `{"x0":0.8425084352167931,"x1":0.7232844476476434,"x2":-0.6957309062910424}`

### Breakthrough 23: new best: Seeker: Ackley 3D [±30] [evo-explore]

- **Severity:** INFO
- **Time:** 2026-07-18 18:49:52 UTC
- **Detail:** Major improvement: 17.1759 → 8.4122 via swarm
- **Data:**
  - runId: seeker-ackley-3d-r30-evo-explore-c1
  - confidence: 0.5102337912930037
  - score: 8.412162146818375

### Breakthrough 24: 🔥 Breakthrough: Seeker: Ackley 3D [±30] [evo-explore]

- **Severity:** BREAKTHROUGH
- **Time:** 2026-07-18 18:49:52 UTC
- **Detail:** Score jumped 17.175873 → 8.412162 (51.0% improvement) via swarm at eval #15
- **Data:**
  - runId: seeker-ackley-3d-r30-evo-explore-c1
  - previousBest: 17.17587289051003
  - newBest: 8.412162146818375
  - improvement: 8.763710743691654
  - strategy: swarm
  - eval: 15
  - params: `{"x0":-0.8395766654743888,"x1":-2.8404455742298875,"x2":-2.9642024099456563}`

### Breakthrough 25: new best: Seeker: Ackley 3D [±30] [evo-explore]

- **Severity:** INFO
- **Time:** 2026-07-18 18:49:52 UTC
- **Detail:** Major improvement: 20.3929 → 17.1759 via random
- **Data:**
  - runId: seeker-ackley-3d-r30-evo-explore-c1
  - confidence: 0.1577504884948414
  - score: 17.17587289051003

### Breakthrough 26: 🔥 Breakthrough: Seeker: Ackley 3D [±30] [evo-explore]

- **Severity:** BREAKTHROUGH
- **Time:** 2026-07-18 18:49:52 UTC
- **Detail:** Score jumped 20.392856 → 17.175873 (15.8% improvement) via random at eval #5
- **Data:**
  - runId: seeker-ackley-3d-r30-evo-explore-c1
  - previousBest: 20.392855865022167
  - newBest: 17.17587289051003
  - improvement: 3.2169829745121383
  - strategy: random
  - eval: 5
  - params: `{"x0":1.1010177381304374,"x1":-8.41427559520908,"x2":-9.786999281084626}`

### Breakthrough 27: new best: Seeker: Rastrigin 5D [±20] [evo-explore]

- **Severity:** INFO
- **Time:** 2026-07-18 18:49:51 UTC
- **Detail:** Major improvement: 36.5406 → 23.6160 via evolutionary
- **Data:**
  - runId: seeker-rastrigin-5d-r20-evo-explore-c1
  - confidence: 0.35370652236984995
  - score: 23.61597801907699

### Breakthrough 28: 🔥 Breakthrough: Seeker: Rastrigin 5D [±20] [evo-explore]

- **Severity:** BREAKTHROUGH
- **Time:** 2026-07-18 18:49:51 UTC
- **Detail:** Score jumped 36.540641 → 23.615978 (35.4% improvement) via evolutionary at eval #1768
- **Data:**
  - runId: seeker-rastrigin-5d-r20-evo-explore-c1
  - previousBest: 36.54064111194937
  - newBest: 23.61597801907699
  - improvement: 12.924663092872379
  - strategy: evolutionary
  - eval: 1768
  - params: `{"x0":-1.8196318059078713,"x1":2.1474768992019246,"x2":-1.110225723331725,"x3":0.9583172299131347,"x4":0.076520914908067}`

### Breakthrough 29: new best: Seeker: Rastrigin 5D [±20] [evo-explore]

- **Severity:** INFO
- **Time:** 2026-07-18 18:49:51 UTC
- **Detail:** Major improvement: 41.9632 → 36.5406 via evolutionary
- **Data:**
  - runId: seeker-rastrigin-5d-r20-evo-explore-c1
  - confidence: 0.12922147783722482
  - score: 36.54064111194937

### Breakthrough 30: 🔥 Breakthrough: Seeker: Rastrigin 5D [±20] [evo-explore]

- **Severity:** BREAKTHROUGH
- **Time:** 2026-07-18 18:49:51 UTC
- **Detail:** Score jumped 41.963186 → 36.540641 (12.9% improvement) via evolutionary at eval #1213
- **Data:**
  - runId: seeker-rastrigin-5d-r20-evo-explore-c1
  - previousBest: 41.96318602483721
  - newBest: 36.54064111194937
  - improvement: 5.422544912887844
  - strategy: evolutionary
  - eval: 1213
  - params: `{"x0":0.9628713173244465,"x1":-0.03066715589332414,"x2":2.7940348427738124,"x3":0.8732315275032859,"x4":-2.268578985024199}`

### Breakthrough 31: new best: Seeker: Rastrigin 5D [±20] [evo-explore]

- **Severity:** INFO
- **Time:** 2026-07-18 18:49:51 UTC
- **Detail:** Major improvement: 51.3276 → 43.8160 via evolutionary
- **Data:**
  - runId: seeker-rastrigin-5d-r20-evo-explore-c1
  - confidence: 0.14634698952648728
  - score: 43.81598261799389

### Breakthrough 32: 🔥 Breakthrough: Seeker: Rastrigin 5D [±20] [evo-explore]

- **Severity:** BREAKTHROUGH
- **Time:** 2026-07-18 18:49:51 UTC
- **Detail:** Score jumped 51.327626 → 43.815983 (14.6% improvement) via evolutionary at eval #455
- **Data:**
  - runId: seeker-rastrigin-5d-r20-evo-explore-c1
  - previousBest: 51.32762619051692
  - newBest: 43.81598261799389
  - improvement: 7.511643572523035
  - strategy: evolutionary
  - eval: 455
  - params: `{"x0":-2.535726071848083,"x1":-0.8945372683197581,"x2":-0.7611487592636381,"x3":-0.1131661350869475,"x4":-1.0800527040435566}`

### Breakthrough 33: new best: Seeker: Rastrigin 5D [±20] [evo-explore]

- **Severity:** INFO
- **Time:** 2026-07-18 18:49:51 UTC
- **Detail:** Major improvement: 64.8400 → 51.3276 via evolutionary
- **Data:**
  - runId: seeker-rastrigin-5d-r20-evo-explore-c1
  - confidence: 0.20839516871171582
  - score: 51.32762619051692

### Breakthrough 34: 🔥 Breakthrough: Seeker: Rastrigin 5D [±20] [evo-explore]

- **Severity:** BREAKTHROUGH
- **Time:** 2026-07-18 18:49:51 UTC
- **Detail:** Score jumped 64.839961 → 51.327626 (20.8% improvement) via evolutionary at eval #215
- **Data:**
  - runId: seeker-rastrigin-5d-r20-evo-explore-c1
  - previousBest: 64.83996075034639
  - newBest: 51.32762619051692
  - improvement: 13.512334559829469
  - strategy: evolutionary
  - eval: 215
  - params: `{"x0":-3.049389855427789,"x1":3.194665500566291,"x2":-0.9725485672139187,"x3":2.130931397827808,"x4":-3.9777716258669638}`

### Breakthrough 35: new best: Seeker: Rastrigin 5D [±20] [evo-explore]

- **Severity:** INFO
- **Time:** 2026-07-18 18:49:51 UTC
- **Detail:** Major improvement: 93.6869 → 65.0816 via swarm
- **Data:**
  - runId: seeker-rastrigin-5d-r20-evo-explore-c1
  - confidence: 0.30532862778801445
  - score: 65.08161049665063

### Breakthrough 36: 🔥 Breakthrough: Seeker: Rastrigin 5D [±20] [evo-explore]

- **Severity:** BREAKTHROUGH
- **Time:** 2026-07-18 18:49:51 UTC
- **Detail:** Score jumped 93.686904 → 65.081610 (30.5% improvement) via swarm at eval #53
- **Data:**
  - runId: seeker-rastrigin-5d-r20-evo-explore-c1
  - previousBest: 93.68690448465804
  - newBest: 65.08161049665063
  - improvement: 28.605293988007418
  - strategy: swarm
  - eval: 53
  - params: `{"x0":1.4886134395447699,"x1":-0.8833735524448345,"x2":0.1701487429017945,"x3":1.2892015678540139,"x4":0.5143168900101682}`

### Breakthrough 37: new best: Seeker: Rastrigin 5D [±20] [evo-explore]

- **Severity:** INFO
- **Time:** 2026-07-18 18:49:51 UTC
- **Detail:** Major improvement: 113.5080 → 93.6869 via swarm
- **Data:**
  - runId: seeker-rastrigin-5d-r20-evo-explore-c1
  - confidence: 0.17462265748621414
  - score: 93.68690448465804

### Breakthrough 38: 🔥 Breakthrough: Seeker: Rastrigin 5D [±20] [evo-explore]

- **Severity:** BREAKTHROUGH
- **Time:** 2026-07-18 18:49:51 UTC
- **Detail:** Score jumped 113.507967 → 93.686904 (17.5% improvement) via swarm at eval #48
- **Data:**
  - runId: seeker-rastrigin-5d-r20-evo-explore-c1
  - previousBest: 113.50796739746129
  - newBest: 93.68690448465804
  - improvement: 19.821062912803242
  - strategy: swarm
  - eval: 48
  - params: `{"x0":-0.5754006455738021,"x1":2.3896635361706977,"x2":4.956634672992275,"x3":-0.5237334950901191,"x4":1.8876074262007307}`

### Breakthrough 39: new best: Seeker: Rastrigin 5D [±20] [evo-explore]

- **Severity:** INFO
- **Time:** 2026-07-18 18:49:51 UTC
- **Detail:** Major improvement: 202.5173 → 113.5080 via curiosity
- **Data:**
  - runId: seeker-rastrigin-5d-r20-evo-explore-c1
  - confidence: 0.4395147010857873
  - score: 113.50796739746129

### Breakthrough 40: 🔥 Breakthrough: Seeker: Rastrigin 5D [±20] [evo-explore]

- **Severity:** BREAKTHROUGH
- **Time:** 2026-07-18 18:49:51 UTC
- **Detail:** Score jumped 202.517296 → 113.507967 (44.0% improvement) via curiosity at eval #45
- **Data:**
  - runId: seeker-rastrigin-5d-r20-evo-explore-c1
  - previousBest: 202.517296381104
  - newBest: 113.50796739746129
  - improvement: 89.0093289836427
  - strategy: curiosity
  - eval: 45
  - params: `{"x0":2.825242075755625,"x1":-3.164058612722094,"x2":5.093991164193717,"x3":5.280900004968238,"x4":-0.6181788222229514}`

### Breakthrough 41: new best: Seeker: Rastrigin 5D [±20] [evo-explore]

- **Severity:** INFO
- **Time:** 2026-07-18 18:49:51 UTC
- **Detail:** Major improvement: 337.0655 → 211.4047 via swarm
- **Data:**
  - runId: seeker-rastrigin-5d-r20-evo-explore-c1
  - confidence: 0.37280817046751313
  - score: 211.40473245524248

### Breakthrough 42: 🔥 Breakthrough: Seeker: Rastrigin 5D [±20] [evo-explore]

- **Severity:** BREAKTHROUGH
- **Time:** 2026-07-18 18:49:51 UTC
- **Detail:** Score jumped 337.065508 → 211.404732 (37.3% improvement) via swarm at eval #21
- **Data:**
  - runId: seeker-rastrigin-5d-r20-evo-explore-c1
  - previousBest: 337.0655077136847
  - newBest: 211.40473245524248
  - improvement: 125.66077525844224
  - strategy: swarm
  - eval: 21
  - params: `{"x0":3.0725617223676895,"x1":5.556114294157831,"x2":1.2230339452427321,"x3":8.912258291453043,"x4":-7.216228658333714}`

### Breakthrough 43: new best: Seeker: Rastrigin 5D [±20] [evo-explore]

- **Severity:** INFO
- **Time:** 2026-07-18 18:49:51 UTC
- **Detail:** Major improvement: 730.8687 → 344.0456 via random
- **Data:**
  - runId: seeker-rastrigin-5d-r20-evo-explore-c1
  - confidence: 0.5292648620944618
  - score: 344.04557654694275

### Breakthrough 44: 🔥 Breakthrough: Seeker: Rastrigin 5D [±20] [evo-explore]

- **Severity:** BREAKTHROUGH
- **Time:** 2026-07-18 18:49:51 UTC
- **Detail:** Score jumped 730.868696 → 344.045577 (52.9% improvement) via random at eval #1
- **Data:**
  - runId: seeker-rastrigin-5d-r20-evo-explore-c1
  - previousBest: 730.8686963070555
  - newBest: 344.04557654694275
  - improvement: 386.8231197601128
  - strategy: random
  - eval: 1
  - params: `{"x0":4.8825995111822,"x1":3.5858435059151716,"x2":8.553943191488624,"x3":12.437569721551952,"x4":-4.118989516557017}`

## 5. Best Results by Torsion Domain

### Einstein-Cartan

| Metric | Value |
|--------|-------|
| Best cost (residual) | 4.612474e-4 |
| Total evaluations | 4000 |
| Improvements found | 23 |
| UFE ratio | 87.2% |
| Convergence velocity | 6.596025e+19 |
| Runs completed | 1 |

**Best parameters found:**

| Parameter | Value |
|-----------|-------|
| T01 | 0.00483541 |
| T02 | -0.00644829 |
| T03 | 0.00911609 |
| T12 | 9.387215e-4 |
| T13 | -0.00997462 |
| T23 | 0.0157647 |
| spinDensity | 0.00000 |
| couplingLambda | -2.61355 |

**Strategy contributions** (improvement counts):

- exploit: 15 improvements
- bayesian: 7 improvements
- gradient: 1 improvements

### f(T) Gravity

> No completed runs yet.

### UFE Torsion

> No completed runs yet.

### Torsion Wave

> No completed runs yet.

## 6. Key Insights

1. **Phase shift: Seeker: Ackley 3D [±30] [evo-explore]** — exploring → exploiting at eval #99. Narrowing in on promising region — high convergence rate.
2. **Phase shift: Seeker: Rastrigin 5D [±20] [evo-explore]** — exploring → exploiting at eval #99. Narrowing in on promising region — high convergence rate.

## 7. Physical Interpretation & Discussion

### 7.1 Einstein-Cartan Results

The optimizer searches for torsion tensor configurations satisfying the Cartan
equation T^a_{bc} + δ^a_b T_c − δ^a_c T_b = 8πG s^a_{bc}. Low residual values
indicate physically consistent spin-torsion coupling at the explored spin density
magnitudes. Results near zero residual suggest parameter regimes where torsion
naturally decouples — consistent with the experimental non-observation of torsion
at accessible energy scales.

**Key question:** Do any discovered configurations show anomalously low residuals
at unexpected spin densities? Such configurations could indicate previously
unidentified resonance conditions in spin-torsion coupling.

### 7.2 f(T) Gravity Cosmology

The f(T) task fits modified teleparallel gravity models to 21 H(z) data points
spanning z = 0 to z = 2.34. The chi-squared metric against observational data
directly measures compatibility with observed cosmic expansion history.

**Significance:** Any f(T) model achieving χ² < 21 (≈ 1 per data point) while
requiring fewer fine-tuned parameters than ΛCDM would constitute evidence for
torsion-based modifications to gravity. The Born-Infeld and logarithmic models
are of particular theoretical interest due to their UV-complete behavior.

### 7.3 UFE Torsion Functional

The unified functional Φ(T, S, K) bridges quantum spin-torsion coupling to
macroscopic spacetime torsion. Physical constraints (stability, causality,
unitarity, energy conditions, solar system bounds) dramatically restrict the
viable parameter space.

**Novel aspect:** The gradient energy term γ·∇T·∇T introduces a characteristic
length scale ℓ = √(γ/2α) for torsion field variations. Discovered values of
this scale could point to new physics at specific energy thresholds.

### 7.4 Torsion Wave Propagation

If torsion is massive (m > 0), it propagates as a Proca-like field with finite
range λ_C = ℏ/(mc). The optimizer's best-fit mass values directly predict the
torsion interaction range.

**Experimental testable:** A torsion mass in the range 10⁻⁶ to 10⁻³ eV
would produce measurable spin-dependent forces at laboratory scales (μm to mm
range), potentially detectable by torsion balance experiments or spin-polarized
test mass experiments.

---

## 8. Methodology Notes

### 8.1 Optimization Framework

Both AEGIS and Seeker implement adaptive meta-learning across 10 optimization
strategies. A multi-armed bandit selects strategies based on their empirical
improvement rates, with Thompson sampling to balance exploration of strategy
effectiveness. All runs use seeded Xoshiro256** PRNG for reproducibility.

### 8.2 UFE Tracking

Every function evaluation is classified as "useful" if it either:
- Improves the best-known score, OR
- Explores a novel region of parameter space (discretized grid)

The UFE ratio (useful/total) measures optimization efficiency. The AUCC
(Area Under Convergence Curve) provides a single-number summary of convergence
quality. Time-to-target metrics report evaluations needed to close 10%, 50%,
and 90% of the initial optimality gap.

### 8.3 Anomaly Detection

Anomalies are detected via:
- **Z-score outliers:** Evaluations with |z| > 3σ from running mean
- **Landscape shifts:** Sudden change in the score distribution
- **Constraint boundary clustering:** Solutions clustering at physical constraint boundaries
- **Strategy disruptions:** Unexpected strategy dominance shifts

### 8.4 Pincer Configuration

AEGIS and Seeker operate in opposite-end pincer mode:
- **AEGIS cycle 1:** Exploration-heavy profiles on easy tasks → exploitation-heavy on hard tasks
- **Seeker cycle 1:** Exploitation-heavy on easy tasks → exploration-heavy on hard tasks
- **Each subsequent cycle:** Engines swap direction

This ensures that every (task, strategy-profile) combination is covered from
both the exploration and exploitation perspectives.

---

## 9. Data Availability

All raw data is available via the live monitoring API:

| Endpoint | URL |
|----------|-----|
| AEGIS snapshot | http://localhost:5555/api/snapshot |
| AEGIS alerts | http://localhost:5555/api/alerts |
| Seeker snapshot | http://localhost:5556/api/snapshot |
| Seeker alerts | http://localhost:5556/api/alerts |
| AEGIS run detail | http://localhost:5555/api/run/:id |
| Seeker run detail | http://localhost:5556/api/run/:id |

Full convergence curves, UFE metrics, and parameter histories are available
per-run through the /api/run/:id endpoints.

---

## 10. References

1. Hehl, F.W. et al. (1976). "General relativity with spin and torsion."
   *Rev. Mod. Phys.* 48, 393.
2. Cai, Y.-F., Capozziello, S., et al. (2016). "f(T) teleparallel gravity
   and cosmology." *Rep. Prog. Phys.* 79, 106901.
3. Hammond, R.T. (2002). "Torsion gravity." *Rep. Prog. Phys.* 65, 599.
4. Shapiro, I.L. (2002). "Physical aspects of the space-time torsion."
   *Phys. Rep.* 357, 113.
5. Planck Collaboration (2018). "Planck 2018 results. VI. Cosmological
   parameters." *A&A* 641, A6.

---

*Report generated automatically by the AEGIS/Seeker Autonomous Discovery Framework.*
*Copyright © 2012-2026 Danny Lee Eldridge. All rights reserved.*
