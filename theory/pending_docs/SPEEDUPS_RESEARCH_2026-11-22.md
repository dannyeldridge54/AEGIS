# Speed-ups for cosmological inference — survey for our pipeline

Pipeline under review: Cobaya 3.6.2 + CAMB 2.0.5 (custom PPF w(a) table, "thread" quintessence) minimising with BOBYQA (best_of 2) on Planck PR4 HiLLiPoP/LoLLiPoP/CamSpec NPIPE + PR4 lensing + DESI DR2 BAO + Pantheon+/Union3/DES-Dovekie SN + ACT DR6 lite + SPT-3G D1 lite. One fit takes ~45–90 min on 2 cores (CAMB ~2.1 s per call, so ~1,300–2,600 calls). Two BOBYQA runs differ by 3–4 in chi2.

Compiled 2026-11-22. Every link below was found by web search or fetched during this session. Figures in quotation marks are as the paper or docs state them. Text in *italics* is my own assessment, not a reported figure.

Column key:
- **w(a)?** — can it handle our custom PPF w(a) table? Yes / No / Retrain = yes if retrained on our own CAMB / Unknown.
- **Effort** — effort to adopt in our pipeline: L (low), M (medium) or H (high).

---

## 1. Neural / ML emulators of CMB and matter spectra

| # | Name | Link | Speeds up | Reported speed-up / accuracy (source) | w(a)? | Effort |
|---|---|---|---|---|---|---|
| 1 | CosmoPower (original) | https://arxiv.org/abs/2106.03846 | Boltzmann-code calls (Cl, P(k)) | "speed-up factor up to O(10^4) to the complete inference pipeline"; Planck 2018 posteriors "in just a few seconds"; P(k) error <0.4%; CMB error ≤10% of SO shot noise (abstract) | Retrain | M |
| 2 | CosmoPower framework + CAMB emulator suite (Cobaya wrapper) | https://arxiv.org/abs/2405.07903 | CAMB calls inside Cobaya | "≲1/50 of the evaluation time"; CAMB ~20 s vs CosmoPower ~0.1 s; ΛCDM CMB chain ~10 h → ~20 min; +Σmν chain 28 h → ~100 min; parameters "well within 0.1σ". Includes a **w0wa** emulator, the weakest case: outliers up to ~80% of cosmic variance at small scales | Retrain (pre-trained w0wa is not our w(a)) | M |
| 3 | cosmopower-organization high-accuracy emulators (class_sz) | https://arxiv.org/abs/2303.01591 ; repo https://github.com/cosmopower-organization | TT/TE/EE/PK + derived parameters | "accurate to better than 0.5% out to ℓ = 10^4"; ≈60 ms vs O(1 min) for high-precision CLASS/CAMB (~1000×); models ΛCDM, wCDM (w ∈ [−2, −0.33]), Neff, Σmν | No (constant w only); Retrain | M |
| 4 | CosmoPower-JAX | https://arxiv.org/abs/2305.06347 ; https://github.com/dpiras/cosmopower-jax | Emulator + gradients on GPU, enabling HMC | O(10^3) speed-up vs nested sampling without emulators (37 parameters); 157-parameter case "3 days … as opposed to the estimated 6 years" | Retrain | M–H |
| 5 | CONNECT | https://arxiv.org/abs/2205.15726 | CLASS calls; iterative training set built from MCMC | CLASS evaluations "reduced by two orders of magnitude"; posteriors differ "by typically less than 0.01–0.1 standard deviations" | Retrain (CLASS-based, so needs a CLASS port of our w(a)) | H |
| 6 | CONNECT profile likelihoods | https://arxiv.org/abs/2308.06379 | Profile-likelihood optimisation | "additional speed-up of 1–2 orders of magnitude" vs simulated annealing; one profile point converges in < 1 min on 1 core vs "a few days" with CLASS | Retrain (CLASS) | H |
| 7 | CONNECT evidence for inflation | https://arxiv.org/html/2406.03968v2 | Nested-sampling evidence | CLASS + PolyChord ~30,000 CPU-h vs CONNECT ~125 CPU-h (+150 CPU-h training); ~240× when training cost is shared; ln Z agree (−1860.4±0.54 vs −1861.1±0.55) | Retrain (CLASS) | H |
| 8 | **OLÉ** (Online Learning Emulator) | https://arxiv.org/abs/2503.13183 ; https://github.com/svenguenther/OLE | Learns the theory output on the fly during a Cobaya/MontePython run with CAMB/CLASS | "increasing the efficiency by a factor of 30–350, including data acquisition and training"; ×4 more with candl gradients | **Yes** (trains on your own CAMB as it runs) | L–M |
| 9 | GP + PCA uncertainty-aware emulator (OLÉ precursor) | https://arxiv.org/abs/2307.01138 | Theory calls, with active learning | 126 theory calls vs 58,924 for MCMC; "reduce the number of simulation calls by a factor of" ~500, "save about 96% of the computational costs"; parameter biases ≤5% | Yes (trains on your own code) | M |
| 10 | Capse.jl | https://arxiv.org/abs/2307.14339 ; docs https://cosmologicalemulators.github.io/Capse.jl/dev | CMB Cl emulation (Julia, autodiff) | "a few microseconds" per prediction; errors "below 0.1σ" for CMB-S4 scales; "three to six orders of magnitude" more efficient; trains "in an hour's time on a 8-cores CPU"; Planck TT+TE+EE analysis "in less than a second" | Retrain | H (Julia stack) |
| 11 | PICO | https://arxiv.org/abs/astro-ph/0606709 | CAMB Cl + WMAP likelihood (polynomial interpolation) | ~3000× faster than CAMB (flat); ~2000× faster than WMAP3 likelihood; total 1–2 orders of magnitude | Retrain (historical) | H |
| 12 | CosmoNet | https://arxiv.org/abs/astro-ph/0608174 ; non-flat follow-up https://arxiv.org/abs/astro-ph/0703445 | Cl via neural network | ~7×10^4× faster than CAMB; errors "typically 2-3% of cosmic variance" | Retrain (historical) | H |
| 13 | CosmicNet I | https://arxiv.org/abs/1907.05764 | Neural network inside CLASS for source functions | Qualitative only: perturbation step "not a bottleneck … anymore" | Unknown | H |
| 14 | CosmicNet II | https://arxiv.org/abs/2207.05707 | Emulated perturbation module of CLASS (extended cosmologies) | ~150× on the perturbation module; ~3× overall for CMB Cl; ~50× for P(k); ~1% accuracy | Retrain (CLASS) | H |
| 15 | Attention-based NN CMB emulators | https://arxiv.org/abs/2505.22574 | CMB TT/TE/EE emulation (CAMB-trained) | Outlier fraction (Δχ² > 0.2) <10% for Planck/SO/S4/HD with ~2–4×10^5 training vectors; no speed figure in abstract | Retrain | H |
| 16 | syren-new (symbolic regression) | https://arxiv.org/abs/2410.14623 | Linear/non-linear P(k), σ8 with w0wa + ν | "at least an order of magnitude faster" than numerical emulators; RMS error 0.1% σ8, 0.3% linear P(k), 1.3% non-linear | No (w0wa only) | L (but not for CMB) |
| 17 | Effort.jl | https://arxiv.org/abs/2501.04639 ; docs https://cosmologicalemulators.github.io/Effort.jl/dev/ | EFT galaxy-clustering multipoles | ~15 μs per multipole; PT-challenge analysis ~10 min on a laptop | Retrain | H (not needed for BAO) |
| 18 | PyBird-JAX | https://arxiv.org/abs/2507.20990 | One-loop galaxy P(k) | 1.2 ms on CPU / 0.2 ms on GPU; "3-4 orders of magnitude speed-up over PyBird" | Retrain | H (not needed for BAO) |
| 19 | CosmoPower emulators for interacting DE | https://arxiv.org/abs/2508.10876 | Non-linear P(k) for dark-scattering DE | ~O(10^4) speed-up; "months on CPU cores to a few days on GPUs" | Retrain (shows custom-DE retraining works) | M–H |

## 2. Differentiable Boltzmann codes and gradient-based samplers

| # | Name | Link | Speeds up | Reported speed-up / accuracy (source) | w(a)? | Effort |
|---|---|---|---|---|---|---|
| 20 | DISCO-DJ I | https://arxiv.org/abs/2311.03291 | Differentiable EB solver (JAX), exact Jacobians | Agrees "at the per-mille level" with CAMB/CLASS; no runtime benchmark given (authors expect a further 2–3× from optimisation); supports CPL w0+wa(1−a) fluid | No (CPL only; custom w(a) needs a code change) | H |
| 21 | SymBoltz.jl | https://arxiv.org/abs/2509.24740 | Symbolic-numeric, approximation-free EB solver (Julia) | Spectra agree "up to 0.1%"; performance "comparable to existing approximation-based codes"; autodiff for any output; models are swappable components | Yes, in principle (designed for adding models) | H |
| 22 | Bolt.jl | https://www.github.com/xzackli/Bolt.jl | Differentiable Boltzmann code (Julia, forward-mode AD) | No speed claims; gradients of CMB TT and P(k) | Unknown | H |
| 23 | gCAMB (GPU CAMB port) | https://arxiv.org/abs/2509.25110 ; code https://github.com/lstorchi/CAMB/tree/gpuport | CAMB itself on GPU | High-accuracy run 329.9 s → 54.0 s vs 32 CPU cores (~6×); ">100×" vs 1 serial core; differences below cosmic variance; flat universe only; DE models not discussed | Unknown | M–H (needs GPU) |
| 24 | jax-cosmo | https://arxiv.org/abs/2302.05163 | Differentiable background, P(k), Limber Cl | No timings in abstract; fast exact Fisher matrices; no CMB Boltzmann solver | Partial (background only) | M |
| 25 | BlackJAX | https://arxiv.org/abs/2402.10797 | HMC/NUTS/SMC/nested slice sampling in JAX | Library paper; speed depends on a differentiable likelihood | Yes (needs a differentiable model) | M–H |
| 26 | NumPyro | https://arxiv.org/abs/1912.11554 | NUTS/HMC in JAX | Library; needs a JAX model | Yes (needs a differentiable model) | M–H |
| 27 | GPU nested sampling + CosmoPower-JAX | https://arxiv.org/abs/2509.13307 | Evidence + posteriors on GPU | CMB 6-D: ~12 s vs ~1 h PolyChord on CPU ("nearly 300×"); NUTS+harmonic ~2 min; models include **w0wa** | Retrain | H |
| 28 | flowMC | https://arxiv.org/abs/2211.06397 | Normalising-flow-enhanced MCMC (JAX) | Qualitative speed claims only | Yes (sampler) | M–H |

## 3. Likelihood speed-ups (lite / compressed / JAX ports / nuisance handling)

| # | Name | Link | Speeds up | Reported speed-up / accuracy (source) | w(a)? | Effort |
|---|---|---|---|---|---|---|
| 29 | candl (differentiable CMB likelihoods) | https://arxiv.org/abs/2401.13433 ; https://github.com/Lbalkenhol/candl | SPT/ACT likelihoods in JAX, with gradients | Abstract gives no benchmark. Datasets: SPT-3G D1 T&E (multifreq & **lite**), SPT-3G 2018, ACT DR6/DR4 TT/TE/EE (lite), ACT DR6 lensing; Planck via clipy (docs) | Yes (theory-agnostic) | L–M |
| 30 | spt_candl_data (official SPT-3G D1 release) | https://github.com/SouthPoleTelescope/spt_candl_data ; overview https://pole.uchicago.edu/public/data/omori26/likelihoods/overview.html | SPT-3G D1 likelihood with Cobaya templates | No timings | Yes | L |
| 31 | clipy (pure-Python/JAX Planck clik) | https://github.com/benabed/clipy ; https://pypi.org/project/clipy-like/ | Planck plik/plik-lite/simall/commander/lensing without Fortran clik; JAX optional | No explicit speed claims; JAX float32 can shift lnL by up to ~1e-4 | Yes | L–M |
| 32 | Plik-lite / CosMOPED (foreground-marginalised Planck) | https://arxiv.org/abs/1909.05869 ; Planck 2018 V https://arxiv.org/abs/1907.12875 | Removes Planck foreground nuisance parameters | CosMOPED ΛCDM "consistent with the uncompressed likelihood to within 0.1σ" (no speed number) | Yes (but validated on ΛCDM) | L |
| 33 | CamSpec-NPIPE-lite & likelihood-choice study | https://arxiv.org/abs/2510.09430 | Lite PR4 likelihood with only 3 calibration parameters | No runtimes; Plik-lite vs CamSpec-NPIPE-lite best-fit Δχ² 2.88/3.83; Ωbh² ~1σ shift for Planck alone; P-ACT shifts ≤0.7σ; foreground marginalisation needed for truncated combinations | Yes | L |
| 34 | HiLLiPoP / LoLLiPoP (PR4, Python) | https://github.com/planck-npipe ; https://pypi.org/project/planck-2020-hillipop/ | Already pure-Python Cobaya likelihoods | No lite variant found. *Many foreground nuisance parameters, which enlarge the BOBYQA dimension* | Yes | — (current) |
| 35 | ACT DR6 lite (DR6-ACT-lite) | https://github.com/ACTCollaboration/DR6-ACT-lite ; settings https://github.com/ACTCollaboration/ACT-DR6-parameters | Foregrounds marginalised to A_act, P_act | Reproduces the full likelihood to "significantly less than 0.1sigma" (ΛCDM only). **Requires CosmoRec** and the ACT camb.yaml accuracy settings, which raise CAMB cost | Yes (ΛCDM-validated) | — (current) |
| 36 | Analytic marginalisation over nuisance parameters (Hadzhiyska et al.) | https://arxiv.org/abs/2301.11895 | Removes linear/Gaussian nuisance parameters from the sampled set | Linearised method "by a factor 3-10"; DES-Y1 ~338 h → ~32 h; overall ~2–15× | Yes | M |
| 37 | Analytic methods for cosmological likelihoods (Taylor & Kitching) | https://arxiv.org/abs/1003.1136 | Analytic marginalisation of amplitude/offset nuisances (e.g. SN M, calibrations) | Methods paper | Yes | L–M |

## 4. CAMB / CLASS accuracy and parallelisation; Cobaya fast/slow

| # | Name | Link | Speeds up | Reported speed-up / accuracy (source) | w(a)? | Effort |
|---|---|---|---|---|---|---|
| 38 | Fast/slow decorrelation and dragging (Lewis 2013) | https://arxiv.org/abs/1304.4473 | MCMC with many fast nuisance parameters | "speedup by a factor of five or more" on Planck; scales ~O(1+N_fast/N_slow) | Yes | L (MCMC only, not BOBYQA) |
| 39 | Cobaya mcmc: blocking / oversample_power / drag / measure_speeds | https://cobaya.readthedocs.io/en/devel/sampler_mcmc.html | Automatic speed hierarchy | oversample_power default 0.4; drag default False; Rminus1_stop 0.01 | Yes | L |
| 40 | Cobaya paper (speed hierarchy, theory caching) | https://arxiv.org/abs/2005.05290 | Recomputes only the components whose inputs changed | Framework description | Yes | L |
| 41 | CAMB accuracy stability checker | https://camb.readthedocs.io/en/latest/check_accuracy.html | Finds the cheapest AccuracyBoost / lSampleBoost / lens_potential_accuracy that meet a Δχ² target (`--find-minimal-boosts`, `--chi2-config so`) | Reports CPU/wall times per setting; no headline numbers | Yes | L |
| 42 | CAMB OpenMP / ReadMe accuracy notes | https://camb.info/readme.html ; https://www.github.com/cmbant/CAMB | Thread parallelism; `do_late_rad_truncation` | "fully internally parallelized", ~16 processors with good efficiency; scalar errors rarely >0.3% | Yes | L |
| 43 | Optimising Boltzmann codes for the Planck era (Hamann et al.) | https://arxiv.org/abs/0903.0382 | Choosing precision parameters for accuracy per unit time | Table 5 (CLASS-like settings): default χ² error 5.8 in 2.7 s; tuned "Setting 3" χ² error 0.016 in 17.4 s vs 0.5 in 17.6 s for accuracy_level = 2 (~30× better at the same cost) | Yes | L–M |
| 44 | Planck intermediate XVI (profile likelihoods with MINUIT) | https://arxiv.org/abs/1311.1657 | Reducing Boltzmann numerical noise for minimisers | "We therefore need the numerical noise to be much less than unity"; RMS χ² noise in an ωb scan 0.02 (default) → 0.005 (high-precision CLASS) at ~2× cost; settings listed in their Table 1 | Yes | L |
| 45 | HyRec-2 | https://arxiv.org/abs/2007.14114 ; https://www.github.com/nanoomlee/HYREC-2 | Recombination step | "under one millisecond on a standard laptop", faster than RECFAST and highly accurate. *Possibly a cheaper alternative to the CosmoRec that ACT DR6 lite asks for (not validated by ACT)* | Yes | M |
| 46 | CLASS I overview (OpenMP, precision files) | https://arxiv.org/abs/1104.2932 | Alternative Boltzmann code with OpenMP | Background reference | Needs port | H |

## 5. Minimiser robustness and speed

| # | Name | Link | Speeds up | Reported speed-up / accuracy (source) | w(a)? | Effort |
|---|---|---|---|---|---|---|
| 47 | Cobaya `minimize` options | https://cobaya.readthedocs.io/en/devel/sampler_minimize.html | BOBYQA/scipy/iminuit settings | Defaults: best_of 2, `override_bobyqa: rhoend 0.05` (deliberately loose "because cosmological likelihoods often have numerical noise"); covmat used to rescale; "works best when run on top of a Monte Carlo sample"; MPI recommended for multiple starts | Yes | L |
| 48 | Py-BOBYQA / DFO-LS noise robustness | https://arxiv.org/abs/1804.00154 | Restarts on stagnation for noisy objectives | "restarting the solver when stagnation is detected is a cheap and effective mechanism for achieving robustness"; Py-BOBYQA "comparable to or better than" other DFO solvers on noisy problems | Yes | L |
| 49 | Escaping local minima with Py-BOBYQA | https://arxiv.org/abs/1812.11343 ; user guide https://numericalalgorithmsgroup.github.io/pybobyqa/build/html/userguide.html | `seek_global_minimum` adaptive restarts | Adaptive restarts reached the global minimum with fewer evaluations; best Py-BOBYQA variant on noisy problems at high accuracy; heuristic, no guarantee | Yes | L |
| 50 | iminuit (MIGRAD / HESSE) | https://pypi.org/project/iminuit/ ; ASCL https://ui.adsabs.harvard.edu/abs/2021ascl.soft08024D/abstract | Quasi-Newton minimiser with EDM convergence check; Cobaya exposes `override_iminuit` | Planck XVI used MIGRAD → MIGRAD → HESSE with an EDM cut (see #44) | Yes | L–M |
| 51 | desilike profilers (minuit / bobyqa / scipy) | https://desilike.readthedocs.io/en/latest/api/profilers.html | Multi-start `niterations` over MPI; minuit with JAX gradients | Documentation; seek_global_minimum is "no guarantees" | Yes | M |
| 52 | PROSPECT | https://arxiv.org/abs/2312.02972 ; https://pypi.org/project/prospect-public/ | Simulated-annealing global optimiser / profiles (Cobaya + MontePython) | Works "well against noisy likelihoods with many local optima"; 2–3 independent runs per point; starts from MCMC bins within Δln L ≈ 5; no runtimes | Yes | M |
| 53 | Procoli | https://arxiv.org/abs/2401.14225 ; https://pypi.org/project/procoli/ | Simulated-annealing profiles (MontePython) | "fast and accessible"; validated on mocks; no timings | Yes (MontePython, not Cobaya) | M–H |
| 54 | Profile likelihoods: When, Why and How (Herold et al.) | https://arxiv.org/abs/2408.07700 | Practical guide (pinc annealing with CLASS) | Notes failed minimisations / local minima in degenerate directions; bounds on h used to keep w0 minimisations stable; suggests emulators for cost | Yes | L (reading) |

## 6. Samplers

| # | Name | Link | Speeds up | Reported speed-up / accuracy (source) | w(a)? | Effort |
|---|---|---|---|---|---|---|
| 55 | PolyChord | https://arxiv.org/abs/1502.01856 | Nested sampling that "can fully exploit a hierarchy of parameter speeds"; in Cobaya | Evidence + multimodal | Yes | L |
| 56 | nautilus | https://arxiv.org/abs/2306.16923 ; https://www.github.com/johannesulf/nautilus | Neural-boosted importance nested sampling | Cosmology 7-D: ~80,000 evaluations, "two orders of magnitude fewer" than the 3–10×10^6 of a reference analysis | Yes (needs a wrapper around the Cobaya model) | M |
| 57 | pocoMC | https://arxiv.org/abs/2207.05652 | Preconditioned (flow) Monte Carlo | "approximately 50 and 25 times faster" than nested sampling on two tests; more in higher dimensions | Yes (wrapper) | M |
| 58 | dynesty | https://arxiv.org/abs/1904.02180 | Dynamic nested sampling | Library | Yes (wrapper) | M |
| 59 | emcee | https://arxiv.org/abs/1202.3665 | Affine-invariant ensemble | Library. *In the nautilus Rosenbrock test emcee needed ~10^11 evaluations, so it is a poor fit for a 2 s likelihood* | Yes | M |
| 60 | TMNRE / swyft | https://arxiv.org/abs/2111.08030 | Simulation-based marginal posteriors (CMB example) | "orders of magnitude fewer simulator calls" than MCMC | Yes | H |

## 7. Importance sampling, post-processing, likelihood emulation, evidence

| # | Name | Link | Speeds up | Reported speed-up / accuracy (source) | w(a)? | Effort |
|---|---|---|---|---|---|---|
| 61 | Cobaya `post` (importance reweighting) | https://cobaya.readthedocs.io/en/devel/post.html | Add/remove likelihoods without resampling; the theory is recomputed only if needed | "much faster when new likelihoods don't require a full theory recomputation"; the new posterior must lie inside the old one | Yes | L |
| 62 | GPry | https://arxiv.org/abs/2211.02045 ; docs https://gpry.readthedocs.io/ | Emulates the posterior directly with a GP + active learning (Cobaya interface) | "reduce[s] the number of required posterior evaluations by two orders of magnitude"; Planck 2018 ΛCDM in ~500 theory evaluations; worth it for likelihoods ≳0.1 s | Yes (likelihood-level) | L–M |
| 63 | BAMBI | https://arxiv.org/abs/1110.2997 ; https://github.com/farhanferoz/BAMBI | Neural-network likelihood emulation inside MultiNest | Historical | Yes | H |
| 64 | MCEvidence | https://arxiv.org/abs/1704.03472 ; https://github.com/yabebalFantaye/MCEvidence | Evidence from existing MCMC chains (k-NN), so no nested sampling needed | Used for "No evidence for extensions…" (1704.03467) | Yes | L |
| 65 | harmonic (learned harmonic mean) | https://arxiv.org/abs/2405.05969 | Evidence from posterior samples via normalising flows | Paired with NUTS in #27 (~2 min CMB 6-D) | Yes | M |

---

## Ranked TOP 10 for our pipeline

Criteria: works with a custom CAMB w(a), works inside Cobaya with PR4 likelihoods, fixes the 3–4 χ² minimiser wobble, and gives the most gain for the least effort.

1. **Fix minimiser settings (#47, #48, #49, #44).** Start from an MCMC covmat. Run a two-stage BOBYQA: a coarse stage with rhoend 0.05, then a polish stage with rhoend ~0.005 and `seek_global_minimum`/restarts. Use best_of ≥4 under MPI. Raise CAMB precision only for the polish stage. *This targets the wobble directly. The default rhoend 0.05 is loose by design, and Planck XVI shows default-precision χ² noise is ~0.02 rms in a single direction, so a 3–4 gap is most likely premature stopping or different basins, not noise alone (my inference).* Effort L.
2. **OLÉ (#8).** The only emulator that plugs into Cobaya + CAMB and learns our own w(a) model on the fly: "30–350×" including training. Use it for the global search and sampling, then do the final polish with true CAMB. Effort L–M.
3. **Cut the nuisance dimension (#33, #36, #37, #32).** Options: CamSpec-NPIPE-lite (3 calibration parameters) in place of, or as a cross-check for, HiLLiPoP's foreground set; analytic marginalisation of SN M and calibrations. Fewer BOBYQA dimensions means fewer evaluations and fewer flat directions. Effort L–M.
4. **Tune CAMB cost (#41, #42, #43, #45).** Set OpenMP threads equal to the number of cores. Run `check_accuracy --find-minimal-boosts` for our ℓmax and data. Check whether the ACT-recommended CosmoRec and high lens_potential_accuracy are needed in every stage (use them in the polish only). Effort L.
5. **Warm starts plus Cobaya `post` across SN variants (#61).** Pantheon+, Union3 and DES-Dovekie share the CMB+BAO part, so start each minimisation from the previous best fit and covmat, and reweight chains instead of rerunning them. Effort L.
6. **iminuit MIGRAD/HESSE polish (#50, #44).** Use it once the noise has been reduced (high-precision CAMB or an emulator). EDM gives a convergence test, and HESSE gives the local covariance for free. Effort L–M.
7. **GPry (#62).** For full posteriors in our w(a) model at a ~2 s likelihood: ~100× fewer evaluations, with a Cobaya interface. Effort L–M.
8. **PROSPECT (#52).** Simulated annealing, Cobaya-native, robust to noisy and multimodal likelihoods. Use it for profiles of the w(a) parameters and as an independent check on the BOBYQA best fit. Effort M.
9. **CosmoPower retrained on our CAMB w(a), with the Cobaya wrapper (#2, #1).** A persistent emulator (CAMB ~20 s → 0.1 s in their test; chain 10 h → 20 min). Training needs O(10^4–10^5) CAMB runs, which is worth it if we will run many fits. Effort M.
10. **Gradient path: CosmoPower-JAX + candl + clipy (#4, #29, #31, #27).** Differentiable SPT/ACT likelihoods and Planck via clipy allow NUTS or GPU nested sampling (~300× in their CMB test). HiLLiPoP/LoLLiPoP have no JAX port, so this needs Planck substitutes. Effort H; long-term.

## Recommended plan

**Step 0 — diagnose the wobble (½ day, no new code).**
- Evaluate χ² at both BOBYQA end points with default CAMB and with boosted accuracy (AccuracyBoost/lSampleBoost ~2).
- Scan χ² along the line between them in ~20 steps. A smooth valley means BOBYQA stopped early or found two basins. A jagged line means numerical noise.
- Print the nuisance-parameter differences between the two solutions to see which directions are flat.

**Step 1 — minimiser settings (1 day; expect the wobble to drop to ≲0.5 χ² — *my estimate*).**
- Set `covmat:` from an existing chain (or a short MCMC).
- Run stage A: BOBYQA with the default rhoend 0.05 at normal CAMB accuracy.
- Run stage B: start from A's best fit with `override_bobyqa: {rhoend: 0.005, seek_global_minimum: true}` (check that the Cobaya 3.6.2 pass-through accepts it), CAMB boosted, and best_of 4 under `mpirun -n 4` if 4 cores are available.
- Optionally finish with iminuit MIGRAD + HESSE.

**Step 2 — CAMB cost trimming (1 day; expect ~1.5–2× per call — *my estimate*, to verify with timings).**
- Set `OMP_NUM_THREADS` to the number of cores.
- Use the check_accuracy minimal boosts for the data we actually use.
- Use CosmoRec/high accuracy only in the polish stage.
- Make sure BAO/SN-only evaluations don't request Cl.

**Step 3 — dimension reduction (1–2 days).**
- Analytically marginalise SN M and calibrations where the likelihood allows it.
- Cross-check the HiLLiPoP results against CamSpec-NPIPE-lite, which has far fewer nuisance parameters.

**Step 4 — OLÉ (2–4 days).**
- Wrap our CAMB+w(a) Cobaya run with OLÉ.
- Use the emulator for the global stage and for any MCMC, then polish with true CAMB (a few hundred calls, ~10–20 min).
- The paper reports 30–350× for sampling. *For a single best fit, I expect 45–90 min → ~15–25 min, dominated by the true-CAMB polish (estimate).*

**Step 5 (only if we run many models or profiles).**
- Retrain CosmoPower on our w(a) model; later consider the JAX/candl/clipy gradient path for NUTS or GPU nested sampling.

Expected overall: about **3–5× faster per fit and a reproducible best fit (≲0.5 χ² spread)** after Steps 1–4. Sampling and profiling should gain 1–2 orders of magnitude from OLÉ or GPry. *These are estimates; the per-step factors quoted from papers apply to their setups, not ours.*
