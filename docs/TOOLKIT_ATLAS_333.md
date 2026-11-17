# AEGIS Toolkit Atlas — 333 wireable toolkits in Janus strings (17 Nov 2026)
Items 1–50 and Strings 1–8 are in the chat of 17 Nov 06:51 (summarised at the end). Items 51–333 continue below.
Each entry: **toolkit** — candidate referee code or data (to be confirmed before use; nothing is wired until it passes its own locked validation) — what it feeds (→).
Rule for every string: lock first, validate each toolkit against its referee, prove the wire loses nothing and the loop closes, then report the joint prediction.

---
## String 9 — Particle physics engine (SERAPIS's particles ↔ colliders ↔ cosmology)
51. Supersymmetric spectrum generator — SOFTSUSY / SPheno / FlexibleSUSY → wino mass splitting, gravitino → String 2
52. Model-file generator — FeynRules / SARAH → all particle toolkits
53. Event generator — Pythia 8 → collider + annihilation spectra
54. Event generator (cross-check) — Herwig 7 → same
55. Matrix elements — MadGraph5_aMC@NLO → wino production at LHC/FCC
56. LHC recast — CheckMATE / MadAnalysis 5 → wino exclusion
57. Simplified-model limits — SModelS → wino, gravitino
58. Disappearing-track reach — published ATLAS/CMS limits → wino window (D736)
59. Higgs couplings — Lilith / HiggsTools → modulus/Higgs mixing limits
60. Flavour observables — flavio → modular-flavour lepton/quark sector
61. Electroweak precision — HEPfit / PDG global fit → new-state limits
62. Running couplings — RunDec / SM RGEs (PDG) → gauge-coupling unification at M_s
63. Proton decay — Super-K/Hyper-K limits + operator formulas → Z₃/matter-parity checks (D787)
64. Neutrinoless double beta — published nuclear matrix elements + KamLAND-Zen limits → Majorana mass (SERAPIS m₁ ≈ 0)
65. Leptogenesis Boltzmann — ULYSSES → D731/D986 leptogenesis
66. Affleck–Dine dynamics — published AD formulas (cross-check numerics) → ρ/τ=i AD windows
67. Gravitino cosmology — published BBN + overclosure limits → reheating T_R (String 1)
68. Moduli decays — published moduli-problem formulas → T_R, dark radiation
69. Dark radiation ΔN_eff — CLASS/CAMB N_eff + Planck/ACT limits → light-state budget
70. Axion/ALP limits — AxionLimits compilation → Kähler-axion (P1′) checks
71. Dark photon limits — published compilation → hidden-sector states
72. Direct detection — DDCalc / WIMpy + LZ/XENONnT limits → wino (loop-suppressed) check
73. Neutrino detectors (DM) — IceCube/SK published limits → wino annihilation in the Sun
74. Precision QED/atomic tests — PDG → constants
75. Lattice QCD inputs — FLAG averages → hadronic inputs for nuclear rates

## String 10 — Nuclear astrophysics network (fusion ↔ explosions ↔ elements)
76. Reaction network solver — pynucastro → all burning stages
77. Large network — SkyNet / WinNet → r-process
78. Nuclear masses — AME2020 tables → networks
79. Nuclear reaction cross sections — TALYS → rates where unmeasured
80. Evaluated nuclear data — ENDF/B-VIII via OpenMC tools → neutron captures
81. Weak rates — published Fuller/Langanke tables → supernova cores
82. Neutrino–nucleus cross sections — GENIE → supernova neutrinos (item 6)
83. r-process yields — SkyNet + published merger ejecta → Galactic chemistry (33)
84. s-process yields — published AGB yields (FRUITY/Monash) → chemistry (33)
85. Type Ia yields — published W7/delayed-detonation tables → iron, chemistry
86. Core-collapse yields — published (Sukhbold et al.) tables → chemistry
87. Kilonova light — published models / Redback → GW counterparts (30)
88. Supernova light curves — sncosmo → distances (Hyperion late universe)
89. Supernova spectra — published SuperNu/STELLA grids → explosion physics
90. Pre-supernova neutrinos — SNEWPY → neutrino detectors
91. Neutron-star cooling — published cooling curves → EoS (4)
92. Neutron-star crusts — published crust EoS → tidal deformability (A3)
93. Nuclear EoS from theory — published Skyrme/RMF/χEFT bands → neutron stars
94. Heavy-ion EoS constraints — published HIC bands → neutron stars
95. Radioactive heating (²⁶Al, ⁶⁰Fe) — published yields → Galactic gamma lines

## String 11 — Explosions and transients (stars ↔ GW ↔ light)
96. GRB afterglows — afterglowpy → GW counterparts
97. GRB prompt / jets — published jet models → afterglows
98. Tidal disruption events — published TDE models (MOSFiT) → black-hole masses
99. Multi-transient fitter — MOSFiT / Redback → all transients
100. Fast radio burst populations — published (frbpoppy) → FRB dispersion (29)
101. Magnetar models — published spin-down formulas → FRBs, kilonovae
102. X-ray binaries — XSPEC/PyXspec models → black-hole spins
103. Black-hole spin from disks — KERRBB (XSPEC) → Kerr ISCO (A0)
104. Accretion disks — published Shakura–Sunyaev/slim-disk formulas → X-ray binaries, AGN
105. AGN SEDs — published templates → galaxies
106. Quasar luminosity function — published fits → reionization (13)
107. Relativistic jets — published blazar models → gamma rays
108. Novae — published yields → chemistry
109. Pulsar populations — PsrPopPy → pulsar timing (28)
110. Pulsar emission geometry — published models → neutron stars

## String 12 — Gravitational-wave astronomy (Hyperion GW ↔ populations ↔ cosmology)
111. Precessing waveforms — IMRPhenomXPHM (LALSuite) → parameter estimation
112. EOB waveforms — SEOBNRv5 (LALSuite/pySEOBNR) → cross-check
113. Surrogate waveforms — NRSur7dq4 (LALSuite) → high-mass binaries
114. Tidal waveforms — IMRPhenomPv2_NRTidalv2 → neutron-star EoS (A3)
115. Parameter estimation — bilby → GW catalogue reanalysis
116. Fast PE — RIFT → cross-check
117. Detection statistics — PyCBC → SNR/horizons (A2c)
118. Population synthesis — COMPAS → merger rates
119. Population synthesis (cross-check) — COSMIC → same
120. Binary stellar evolution — BPASS → populations, galaxy light
121. Star-formation history of the universe — published Madau–Dickinson fits → merger rates
122. Standard sirens — published formulas + Janus-LT distances → H0
123. LISA sources — LISA Data Challenge tools → massive black holes, Galactic binaries
124. LISA Galactic binaries — published foreground models → LISA noise
125. Extreme mass ratio inspirals — FastEMRIWaveforms → LISA
126. Stochastic GW backgrounds (astrophysical) — published models → SERAPIS GW (A7c) foreground
127. Cosmic strings GW — published spectra → string-theory checks
128. Domain walls GW — published spectra → modular-symmetry breaking
129. Primordial black holes — BlackHawk → PBH limits (D710 nulls)
130. Numerical relativity — Einstein Toolkit / GRChombo (published runs) → waveform validation

## String 13 — Cosmological simulations (Hyperion structure ↔ galaxies)
131. N-body cosmology — Gadget-4 → halo statistics
132. Fast N-body — FastPM / COLA (published) → many cosmologies quickly
133. Hydrodynamic cosmology — RAMSES / Enzo (published runs) → baryonic effects
134. Halo finders — Rockstar / AHF → halo catalogues
135. Merger trees — consistent-trees → galaxy models
136. Semi-analytic galaxies — Galacticus → galaxy populations
137. Emulators — published (EuclidEmulator, BACCO) → nonlinear P(k)
138. Halofit / HMcode — CAMB → nonlinear P(k)
139. Baryonic feedback — published HMcode-2020 parameters → weak lensing
140. Intrinsic alignments — CCL → weak lensing
141. Weak lensing likelihoods — published DES/KiDS/HSC → σ8, S8 (D710)
142. Galaxy clustering — published DESI full-shape → growth
143. Redshift-space distortions — published fσ8 → growth (Janus-LT)
144. Cluster abundance — published SPT/eROSITA counts → σ8, neutrino mass (A7d)
145. SZ effect — published tSZ models / CCL → clusters
146. X-ray clusters — published scaling relations → cluster masses
147. CMB lensing — published Planck/ACT lensing → σ8, Σm_ν
148. Lyman-α forest — published P1D (DESI) → small-scale power (D711)
149. Galaxy bias models — published (CCL, halomod) → clustering
150. Cosmic voids — published void models → modified gravity tests

## String 14 — CMB and early universe detail (Chronos ↔ CMB ↔ inflation)
151. Boltzmann code — CLASS → cross-check of CAMB
152. CMB likelihoods — Cobaya + Planck/ACT/SPT → n_s, r (SERAPIS scoring)
153. Inflation library — ASPIC (already matched by Chronos Clock) → model benchmarks
154. Non-Gaussianity — published f_NL bispectrum codes → two-field (J6)
155. Isocurvature — CLASS isocurvature modes → D587, D790
156. Spectral distortions — published (CosmoTherm-style formulas) → μ, y (D710 nulls)
157. Reheating dynamics — published lattice results (e.g. CosmoLattice) → T_R, w
158. Preheating — CosmoLattice → oscillation phase (D730)
159. Primordial magnetic fields — published constraints → plasma (19)
160. CMB polarization foregrounds — published dust/synchrotron models → r detection
161. B-mode forecasts — published LiteBIRD/CMB-S4 → r test of SERAPIS
162. Delensing — published forecasts → r sensitivity
163. CMB anomalies — published statistics → large-scale checks
164. Birefringence — published constraints → axion couplings (old Twist line)
165. Recombination (precision) — CosmoRec → HyRec cross-check (12)

## String 15 — High-energy astrophysics (dark matter ↔ gamma rays ↔ neutrinos)
166. Gamma-ray analysis — fermipy (Fermi-LAT) → wino continuum (2507.15934)
167. IACT analysis — gammapy → H.E.S.S./CTA line limits (A7a/A7b)
168. CTA sensitivity — published IRFs + gammapy → wino window test (D736)
169. Galactic diffuse emission — GALPROP outputs → backgrounds
170. Dwarf galaxies J-factors — published (Geringer-Sameth) → halo-independent wino test
171. Galaxy clusters DM — published J/D factors → DM checks
172. Neutrino telescopes — IceCube public data + likelihoods → DM, sources
173. UHE neutrinos — published cosmogenic fluxes → cosmic rays (20)
174. Antiprotons — published AMS-02 + propagation → wino (10)
175. Positrons — published AMS-02 → DM/pulsars
176. Synchrotron from DM — published radio limits → wino
177. 511 keV line — published INTEGRAL → light DM
178. X-ray lines — published (3.5 keV) limits → sterile states
179. Gamma-ray bursts at TeV — published LHAASO → Lorentz invariance tests
180. Cosmic-ray composition — published Auger/TA → sources

## String 16 — Stars in detail (Hyperion stars ↔ spectra ↔ Mapper)
181. Stellar atmospheres — PHOENIX grids → spectra
182. Stellar atmospheres (cross-check) — Kurucz ATLAS9 / MARCS grids → same
183. Spectral synthesis — Turbospectrum / MOOG → abundances (34)
184. Spectroscopic pipelines — iSpec → abundances
185. Bolometric corrections — published (Gaia DR3 BC, MIST BC tables) → luminosities for the Mapper
186. Isochrones — MIST / PARSEC → ages for Mapper stars
187. White-dwarf cooling — published (LPCODE/Bédard) tracks → Galactic age, Mapper
188. Brown dwarfs — published Sonora models → Mapper faint end
189. Stellar rotation / gyrochronology — published relations → ages
190. Stellar activity — published relations → exoplanet noise
191. Binary stars — published Gaia DR3 orbits → masses
192. Eclipsing binaries — PHOEBE → radii, masses (checks asteroseismology)
193. Interferometric radii — published catalogues → radius checks
194. Variable stars (Cepheids) — published period–luminosity → distance ladder, H0
195. RR Lyrae — published relations → halo distances (Mapper)
196. Red clump standard candles — published → distances
197. Stellar winds — published mass-loss recipes → evolution (44)
198. Massive stars — published Geneva tracks → feedback
199. Wolf–Rayet / LBV — published models → explosions
200. Stellar magnetism — published dynamo relations → activity

## String 17 — Milky Way and Local Group (Mapper ↔ dynamics ↔ dark matter)
201. Milky Way mass models — published (McMillan 2017) → potential cross-check (A5a)
202. Rotation curve data — published Gaia/APOGEE curves → Galaxy mass
203. Vertical dynamics (Oort problem) — published → local DM density ρ_⊙ (wino limits)
204. Escape speed — published RAVE/Gaia → halo mass (A5a v_esc)
205. Stellar streams — gala + published stream catalogues → halo shape
206. Globular clusters — published Baumgardt catalogue → orbits (Mapper)
207. Satellite galaxies — published catalogues → halo, DM
208. LMC influence — published LMC models → reflex motion
209. Galactic bar and spiral arms — published potentials → orbits
210. Bulge kinematics — published → bulge mass
211. Galactic Center — published Sgr A* mass/distance (GRAVITY) → R₀
212. Hypervelocity stars — published → Galactic Center, potential
213. Open clusters — published Gaia catalogues → ages, disk
214. Solar neighbourhood census — published (Gaia Catalogue of Nearby Stars) → Mapper completeness
215. Interstellar extinction law — published (Fitzpatrick) → dust (38)
216. HI/CO gas maps — published (HI4PI) → Galaxy gas mass
217. Galactic magnetic field — published (JF12) → cosmic rays
218. Local Group dynamics — published timing argument → MW+M31 mass
219. Andromeda — published → second disk galaxy test
220. Dark-matter subhalos — published lensing/stream limits → DM nature

## String 18 — Galaxies and the cosmic web (Hyperion ↔ light ↔ chemistry)
221. Galaxy rotation curves — SPARC data → halo profiles (cored vs cusp, D982)
222. Tully–Fisher / RAR — published → DM tests
223. Strong lensing galaxies — PyAutoLens → inner density slopes
224. Galaxy morphology — published → galaxy models
225. Galaxy stellar mass function — published → semi-analytic models
226. Star-formation laws — published Kennicutt–Schmidt → chemistry, gas
227. Initial mass function — published (Kroupa/Chabrier) → populations (17)
228. Galaxy metallicity relations — published → chemistry (33)
229. Circumgalactic medium — published absorption → baryons
230. Intergalactic medium — published Lyα (String 13) → reionization
231. High-z galaxies (JWST) — published UV luminosity functions → reionization
232. Dust in galaxies — published SED dust models → SED fitting
233. Galaxy mergers — published rates → black-hole growth
234. Supermassive black holes — published M–σ → AGN, LISA
235. Black-hole seeds — published models → LISA sources (123)

## String 19 — Solar system and planets (Mapper ↔ N-body ↔ planets)
236. Planetary ephemerides — JPL DE440 via astropy/jplephem → solar system, Gaia frame
237. Asteroid orbits — published (MPC) + REBOUND → solar-system dynamics
238. Comet dynamics — REBOUND + published → Oort cloud
239. Planet formation — published pebble-accretion models → exoplanet populations
240. Exoplanet population synthesis — published (Bern model) → occurrence rates
241. Transit fitting — batman / exoplanet → planets (50)
242. Radial-velocity fitting — radvel → planets
243. Exoplanet atmospheres retrieval — TauREx / petitRADTRANS → chemistry (40)
244. Planetary interiors — BurnMan → mass–radius of planets
245. Habitability — published habitable-zone formulas → planets
246. Gaia astrometric planets — published DR3/DR4 → Mapper (DR4 epoch astrometry, Dec 2026)
247. Debris disks — published → planet formation
248. Solar wind — published (PLUTO MHD runs) → heliosphere
249. Space weather — SunPy + published → solar activity
250. Solar irradiance — published → Earth energy input

## String 20 — Earth and laboratory anchors (constants ↔ measurement)
251. Fundamental constants — CODATA (scipy.constants) → everything (A0 T9)
252. Atomic clocks / variation of constants — published limits → moduli, string couplings
253. Gravity tests (fifth force) — published Eöt-Wash limits → light moduli
254. Equivalence principle — published MICROSCOPE → moduli couplings
255. Solar-system tests of GR — published Cassini/PPN → modified gravity
256. Lunar laser ranging — published → G-dot, moduli
257. Seismology — ObsPy (Earth structure) → GW detector noise (seismic wall)
258. Geodesy / Earth tides — published → detector calibration
259. Atmospheric neutrinos — published → neutrino oscillations (5)
260. Reactor neutrinos — published (JUNO) → mass ordering (SERAPIS NO prediction)
261. Accelerator neutrinos — published (DUNE/T2K/NOvA) → δ_CP (gCP test, D762)
262. Tritium beta decay — published KATRIN → absolute neutrino mass
263. Muon g−2 — published → new-physics loops
264. EDMs — published electron/neutron EDM limits → CP violation (P1′)
265. Dark-matter lab searches (axions) — published haloscope limits → axions (70)

## String 21 — Plasma, fluids and radiation (energy engine)
266. MHD solver — Athena++ (published tests) → plasma, disks
267. Hydro solver — PLUTO (published tests) → jets, winds
268. Radiation hydrodynamics — published benchmarks → explosions
269. Turbulence statistics — published → star formation
270. Magnetic reconnection — published rates → flares, jets
271. Shock acceleration — published DSA formulas → cosmic rays
272. Synchrotron / inverse Compton — published (naima) → high-energy SEDs
273. Thermal bremsstrahlung — published → clusters, X-rays
274. Line radiative transfer — published (RADEX) → molecular clouds
275. Dust radiative transfer — SKIRT (published) → galaxies
276. Polarized radiative transfer — published → magnetic fields
277. Photon–photon absorption — published EBL models → TeV gamma rays (167)
278. Extragalactic background light — published (Domínguez) → gamma-ray opacity
279. Cosmic infrared background — published → star formation history
280. Radio continuum — published → star formation, AGN

## String 22 — Data, statistics and computing spine (the hub for all strings)
281. Sky catalogues cross-match — astroquery + CDS XMatch → Mapper
282. Large-table engine — published Gaia TAP / pyvo → Mapper DR4 (Dec 2026)
283. HEALPix tools — healpy → maps (48)
284. Image tools — astropy / photutils → photometry
285. Spectra tools — specutils → spectroscopy
286. Time series — lightkurve → asteroseismology (21)
287. Sampler (MCMC) — emcee → fits
288. Nested sampling — dynesty / UltraNest → evidences (model comparison)
289. Hamiltonian MC — numpyro → large joint fits
290. Emulators / ML surrogates — published (CosmoPower) → fast likelihoods
291. Gaussian processes — george / celerite → noise models
292. Differentiable cosmology — JAX-cosmo → gradient fits
293. Symbolic algebra — SymPy (already used) → derivations
294. Modular forms / number theory — PARI/GP / SageMath → E(τ,s), j, η (SERAPIS core)
295. Arbitrary precision — mpmath (already used) → checks
296. Validation harness — pytest + the AEGIS lock tools → every toolkit
297. Workflow / queue — tools/calcq (AEGIS) → PC runs
298. Provenance — PREREG/DEVIATIONS/D-notes (AEGIS method) → audit trail
299. Visualization — matplotlib / Sky Map → outputs
300. Release packaging — Zenodo + GitHub (AEGIS) → publication

## String 23 — String theory and geometry (SERAPIS's foundation)
301. Calabi–Yau data — published Kreuzer–Skarke database → moduli spaces
302. CY topology tools — CYTools → Kähler cones, intersection numbers
303. Flux vacua statistics — published (JAXVacua-style) → flux tadpoles (D933)
304. Period computations — published (PFE solvers) → complex structure
305. Orientifold tadpoles — published formulas + AEGIS Level S → D3/D5 counts
306. One-loop string amplitudes — AEGIS Level S (S0–S4) → Project H (D985)
307. Modular invariant potentials — AEGIS serapis_calc → SERAPIS plateau
308. Swampland bounds — published (distance, dS) → D993 checks
309. Species scale — published formulas → D706/D760
310. Moduli stabilisation (KKLT/LVS) — published formulas → uplift (P3)
311. Brane SUSY breaking backgrounds — AEGIS S4 (Dudas–Mourad) → χ local mass (D988)
312. Heterotic thresholds — published (DKL) → ρ tilt (D991)
313. Modular flavour symmetry — published (Γ_N groups) → lepton sector (D777)
314. Generalised CP — published → δ_CP prediction (D762)
315. Compactification phenomenology — published (string-scale, couplings) → M_s, g_s

## String 24 — Foundations and cross-checks (closing the big loop)
316. Quantum field theory loops — Package-X / FeynCalc → one-loop masses
317. Effective field theory matching — published (Wilson coefficients) → operators (Weinberg, D891)
318. Renormalisation group for SUSY — SOFTSUSY (51) → spectrum running
319. Thermal field theory — published rates → reheating, leptogenesis
320. Boltzmann solvers (generic) — published (DRAKE) → relic densities (7)
321. Bound states (wino onium) — published → Sommerfeld (A7b)
322. Sommerfeld NLO — published potentials → A7b one-loop line
323. Electroweak phase transition — published (CosmoTransitions) → GW (24)
324. Baryogenesis (EW) — published → alternatives to leptogenesis
325. Topological defects — published → cosmic strings (127)
326. Black-hole thermodynamics — BlackHawk (129) → PBH evaporation
327. Quantum gravity phenomenology — published bounds → Lorentz violation (179)
328. Information/entropy bounds — published → holographic checks
329. Dimensional analysis / units engine — astropy.units → every wire
330. Cross-tool consistency monitor — AEGIS wiring tests (W1, W2…) → all strings
331. Prediction tracker — tools/tracker (AEGIS) → future data scoring
332. Scorecard — tools/scorecard (AEGIS) → inflation model ranking
333. CubeMind learning loop — AEGIS method as training (Danny's goal) → the whole atlas

---
## Strings 1–8 (items 1–50, from the chat)
S1 First three minutes (1, 2, 5, 6) · S2 Dark-matter loop (7–14) · S3 Sound of the universe (24–30) · S4 Living stars (3, 4, 21–23, 36, 44) · S5 Galaxy's memory (33, 34, 38, 39, 41, 42, 49) · S6 Light of galaxies (15–20, 35) · S7 First molecules (31, 32, 37, 40) · S8 Structure and planets (43, 45–48, 50).

## How the 24 strings join
Chronos Clock (early) ⇄ S1, S9, S14, S23, S24 · Hyperion (late) ⇄ S3, S12, S13, S18 · Star Mapper ⇄ S4, S5, S16, S17, S19 · Dark matter (S2) ⇄ S9, S15, S17 · Nuclear (S10) ⇄ S1, S4, S11 · Hub: S22 (data/statistics) and S8/S330 (joint fits, consistency monitor) wire everything into one likelihood.
Build order recommended: S2 → S1 → S5 → S4 → S15 → S17 → S3 → S10 → S9 → S12 → S13 → S16 → rest.
