# Prize board and big questions for CubeMind (Danny, 22 Nov 2026)
Danny's instruction is to try to crack each one. The honest frame:
- Every idea is a **POSTULATE** until Claude and the referee lock it (sha256) and test it.
- A prize is only "cracked" when the prize body itself accepts the result.
- Prize terms below are as last known (mid-2026). **Check each prize's official page before acting on its terms.**

## A. Mathematics prizes
| Prize | Amount | Status | What a real step looks like | Where it touches the Weave |
|---|---|---|---|---|
| **Clay Millennium: Navier–Stokes** (smoothness or blow-up of 3D flow; vortex stretching is the heart of it) | $1M | open | A proof, or a computer-assisted blow-up with rigorous error bounds (cf. Hou–Chen's 2022+ Euler work) | none directly; the Loom field is a lens, not a PDE proof |
| **Clay: Yang–Mills existence and mass gap** | $1M | open | A rigorous 4D quantum YM construction with a gap Δ > 0 | the Weave's hidden SU(N) condensates *assume* a gap; they do not prove it |
| **Clay: Riemann hypothesis** | $1M | open | A proof; numerics are verification only | modular forms at the knots ρ and i (Eisenstein E(τ,s), j(τ)) are the same toolbox |
| **Clay: P vs NP** | $1M | open | A proof; known barriers are relativization, natural proofs and algebrization | compression ≈ prediction (the Hutter work) is the closest link |
| **Clay: Hodge conjecture** | $1M | open | A proof for general projective varieties | the Weave's Calabi–Yau orbifold cycles are Hodge classes |
| **Clay: Birch and Swinnerton-Dyer** | $1M | open | A proof | elliptic curves; the knots ρ and i are the CM points j = 0 and 1728 |
| Clay: Poincaré | — | SOLVED (Perelman, declined) | — | — |
| **Beal conjecture** (AMS-held) | $1M | open | A proof or a counterexample | none |
| **Collatz** (Bakuage prize) | ¥120M | open | A proof; brute-force checks to 2^71 are already done | none |
| **Erdős problems** (erdosproblems.com) | $25–$10,000 each | many open | Pick small, concrete ones; several were reported resolved with AI help in 2025 | Ramsey: R(3,10) is our M2 track |

## B. Computation prizes (our engines can actually compete here)
| Prize | Amount | Status | Our track |
|---|---|---|---|
| **GIMPS: new Mersenne prime** | $3,000 per discovery | the last find was M136279841 (Oct 2024) | **The "vortex" track** (below). Results count only on GIMPS-assigned exponents, run under Danny's own PrimeNet account |
| **EFF: first prime ≥ 100M digits** | $150,000 | open | the same Mersenne pipeline at p ≥ 332,192,831; each test takes weeks to months on one GPU |
| EFF: first prime ≥ 1B digits | $250,000 | open | out of reach for one PC |
| **Hutter Prize** (enwik9) | €500,000 pool (payout in proportion to the gain) | open | M1 Loom compressor (loomz15 best: −22% vs xz on 10 MB; the record pace is about 0.80 bpc) |
| ARC Prize (AI reasoning) | $1M+ grand prize | open | CubeMind's reasoning loop could enter; off-mission for now |

## C. Physics and astrophysics big questions (no cash prize; the "prize" is a test that holds up)
| Question | Weave status (honest) | The test scientists will look at |
|---|---|---|
| Hubble tension (H0 67 vs 73) | **NOT solved** (H0 ≈ 67.5) | SH0ES vs CMB+BAO; a model must raise H0 without breaking BAO |
| Dynamical dark energy (DESI DR2) | partly: the thread thaws, but w ≥ −1 always, so it cannot match DESI's phantom crossing; w0wa fits better | DESI w0–wa contour; SN calibration (Dovekie vs Y5) |
| S₈ tension | not scored yet (the proxy is uncalibrated) | KiDS/DES/HSC weak lensing vs Planck |
| Neutrino mass | Σm_ν = 0.0587 eV (an input) | DESI pushes Σm_ν < 0.064 eV; a negative-mass preference is a live puzzle |
| Cosmological constant problem | Λ is an input, not derived | — |
| Dark matter identity | 12.8 GeV asymmetric + dark photon + a wino share | LZ/XENONnT at 12.8 GeV; LHC disappearing tracks for the wino |
| Strong CP | θ̄ = 0 from anomaly-free weights | neutron EDM |
| Baryon asymmetry | leptogenesis with M_N ≈ 1.8e11 GeV | — |
| Cosmic birefringence | β ≈ 0.28° accommodated (c_γ/f is free) | ACT + Planck β = 0.277 ± 0.057° |
| Lithium problem | consistent with SM nuclear-rate tensions | — |
| α_s at M_Z | **FAIL** (0.1158 vs 0.1180) | lattice + PDG world average |
| Primordial gravitational waves | **prediction r = 5.4e-4** | LiteBIRD/CMB-S4 (σ(r) ~ 1e-3; a clean test only with delensing) |

## D. The "vortex" track (Mersenne primes, Rodin "vortex math")
- **Already tested (D2004, NULL):** Rodin digit and digital-root rules do not filter Mersenne exponents better than chance. Digital roots of 2^p − 1 follow trivially from p mod 6, so they carry no prime information. Do not re-test them as a shortcut.
- **What we have:**
  - tools/mersenne/mloom.py: a layered sieve N1–N4 plus a Lucas–Lehmer referee (D2005 locked; calibration stopped with DEVIATIONS written);
  - GIMPS_STRUCTURE.md: how PRPLL and mfaktc work, plus a map of the RTX 4070.
- **The real path to the $3,000 / $150,000 prizes:**
  1. Danny makes a PrimeNet account himself (no AI types passwords).
  2. He installs Prime95, or PRPLL + mfaktc for the GPU.
  3. GIMPS assigns the exponents.
  4. CubeMind's job is to schedule, monitor and log, and to postulate sieve improvements tested off-line against GIMPS's known-factor self-test (2,924 factors).
- **A sieve idea counts only if** it removes more candidate exponents per CPU-hour than mfaktc's 420/4620-class wheel at the same false-skip rate (zero skipped primes on the known list).

## E. Encryption (Danny's idea: an encryption tool from our engine's dials)
- **Use now:** weave_vault.py. It is AES-256-GCM with scrypt keys, compressing first and never deleting originals. This is the safe tool for real files.
- **Research:** weave_dials_rng.py turns the dials (A = 7.30, β = 2√2, the knots ρ and i, the slip ladder) into a byte stream with a quick statistical battery.
  - The quick battery passing is necessary, not sufficient.
  - The next bars are NIST SP 800-22, PractRand and dieharder, then public cryptanalysis.
  - Until then it is **not secure** and must never protect real data.
- **CubeMind may:**
  - archive files with ufe_tools/cm_compress.py, which keeps a verified round-trip and the originals;
  - lock archives with weave_vault.py, with Danny typing the passphrase;
  - postulate dial-based designs and score them only with the standard batteries.
