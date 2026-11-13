### Step 4 — The engine: the superpotential W and the energy landscape V

**The superpotential W = √3 · m · S · F(T).** *What it is:* in supergravity, the energy landscape is not written directly; it comes from a "recipe" function W. **S** is a helper field that stays at zero (it is held there by the ground's shape) and only switches the energy on. **m** sets the overall energy scale. *How we know it:* the form is a standard no-scale supergravity construction; **m** is measured from the size of the CMB ripples: m ≈ 5×10¹³ GeV. *What it does to spacetime:* through V below, it sets how fast space grows at each stage. *Joins into:* the landscape V.

**The landscape V = m² |F(T)|² / (4x²).** *What it is:* the potential energy of the field at each value of T — the hills and valleys it rolls on. *How we know it:* follows exactly from W and K (no extra choices). *What it does to spacetime:* when V is large and flat, it acts like a cosmological constant and space inflates; where V drops steeply, the field speeds up and its energy turns into motion. *How it works with the field:* the field rolls downhill in V, with the curved ground (Step 2) setting how easily it moves in size versus angle. *Joins into:* the shape function F(T).

---

### Step 5 — The shape: F(T) = T/√(1 + T/μ) · e^{−n(1 − e^{−πT/4})}

This one function draws the whole history — a plateau, a cliff and a tail. In the mirrored form used here the field starts at small size x and moves to larger x. (Updated 13 Nov 2026, Development 79: the cliff factor used to be e^{−nT/(T+m2)}; see the box below.)

**The plateau (small x).** *What it is:* for small x the cliff factor is nearly 1 and the landscape is nearly flat: V ≈ ¼ · m² · e^{−(2n·π/4)x}. *How we know it:* its shape is fixed by the 3 (Step 2); its height is set by m. *What it does to spacetime:* drives inflation (Step 6).

**The cliff (x ≈ 4/(πn) ≈ 0.01), set by n.** *What it is:* the factor e^{−n(1 − e^{−πT/4})} switches from 1 to e^{−n} once (π/4)·n·x passes about 1 — the landscape drops by a factor e^{−2n}. The number π/4 is the same one that appears in the hidden SU(8) force (Step 8): e^{−πT/4} = e^{−2πT/8} is the mark an SU(8) condensate leaves, and it makes the cliff repeat every 8 in the twist angle, the angle's own period. *How we know it:* **n ≈ 127** is chosen to match the size of dark energy today (the cliff's depth sets how much energy is left on the tail, Step 11) — chosen, not predicted. The cliff must be steep enough for inflation to end there. *What it does to spacetime:* ends inflation; the field's energy turns into motion and then heat. *Joins into:* reheating and the kick (Steps 7–8).

> **Why the cliff was reshaped.** With the old factor e^{−nT/(T+m2)}, a little of the cliff's slope lingers far down the tail (it fades only like 1/x). A locked test (TAIL-F) showed that at the heat our reheating produces, this lingering slope makes today's dark energy too stiff, and the data reject it (Δχ² +29). The new factor gives exactly the same inflation (n_s 0.9642, r 0.0038) but its lingering slope fades like e^{−x}, so the tail has the clean √(2/3) slope whatever the reheating. This change was made after seeing that result, so only new data can test it.

**The tail (far past the cliff), set by μ.** *What it is:* after the drop, V ≈ m² e^{−2n} / (4(1 + x/μ)) — flat until x ≈ μ, then sloping down as e^{−√(2/3)φ}. *How we know it:* **μ ≲ 1** is chosen so the field freezes on the sloping part, where the base theory's slope √(2/3) applies; with the reshaped cliff the field freezes at x ≈ 450, far down that slope; this choice was informed by data already seen and is tested on new data (DESI DR3). *What it does to spacetime:* the leftover energy is dark energy (Step 11).

---

### Step 6 — Inflation on the plateau

**Inflation.** *What it is:* a burst in which space grew by a factor of about e⁵⁵ or more in a tiny fraction of a second. *How we know it:* the CMB is smooth across regions that could never have touched otherwise, and its ripples have exactly the pattern inflation predicts. *What it does to spacetime:* flattens and smooths it, and stretches tiny quantum wobbles in the field into the seeds of all galaxies. *How it works with the field:* the field creeps along the plateau, slowed by the expansion itself.

**E-folds (N).** *What it is:* the count of how many times space grew by a factor e ≈ 2.718. The CMB scales we see left the horizon N* ≈ 55 e-folds before inflation ended. *How we know it:* calculated from the model's energy at the end of inflation and the heat after it.

**The ripple tilt n_s and the wave strength r.** *What they are:* n_s says whether large or small ripples are slightly stronger (n_s < 1: large ones slightly stronger). r is how strong the gravitational waves from inflation are compared with the density ripples. *How we know them:* the Twist predicts n_s = 0.963–0.965 and r = 0.0034–0.0040 (frozen, locked); two corrections found later — the stiff "kination" phase after the cliff adds about 2 e-folds, and quantum loops — move the best estimate to n_s ≈ 0.965–0.968, r ≈ 0.0035. Measured n_s: about 0.964 from Planck + DESI (agrees), about 0.973 when ACT and SPT are added (about 4σ tension). r is not yet measured; LiteBIRD (launch planned ~2032) can see it. *Joins into:* the CMB tests.

**The Hubble rate during inflation, H ≈ 10¹³ GeV.** *What it is:* how fast space was growing then. *How we know it:* calculated from the plateau height. *Why it matters:* every light field picks up quantum jitter of size H/2π — important for dark matter (Step 10) and for the hidden field's uneven-matter check (safe by ~100×).

---

### Step 7 — The cliff: inflation ends and the universe heats up

**Kination.** *What it is:* a short era (about 2 e-folds) right after the cliff when the universe's energy is mostly the field's motion. Such energy thins out faster than heat (as a⁻⁶ instead of a⁻⁴), so heat soon takes over. *How we know it:* calculated in the model.

**Instant preheating (coupling g).** *What it is:* the inflaton is coupled to another field χ by g²φ²χ²/2. As the inflaton races past the cliff, χ is suddenly light and is created in a burst; the χ particles then decay into ordinary particles — heat. *How we know it:* the mechanism is standard (Felder, Kofman & Linde); the inflaton's speed comes from the model; **g ≈ 0.1** is a natural choice, not fitted. *What it does to spacetime:* fills it with a hot plasma — the start of the hot Big Bang. *Result:* about 0.04–0.4% of the energy becomes heat at once (0.13% at the central values), and the **reheating temperature T_RH ≈ 2–4×10¹⁴ GeV**. The field's motion still dominates for a while afterwards ("kination") until the heat takes over. The χ field must be part of a supersymmetric pair, or its quantum energy would spoil the plateau. *Joins into:* matter-making (Step 9) and dark matter (Step 10).

---

### Step 8 — The kick and the hidden partner

**The hidden partner field σ (a hidden axion).** *What it is:* a second angle-like field from a hidden sector that does not touch ordinary particles directly. *How we know it:* the kick cannot come from the twist field alone (a rule of supergravity, **holomorphy**, forces any angle term to come with e^{−A x}, which kills it); a hidden partner is the simplest fix. Its mass is set by the observed amount of matter: **m_σ ≈ 3×10¹⁰ GeV** (from a fit through three runs; an earlier estimate of 3–6×10⁹ GeV was withdrawn after its own check failed).

**The linking term Λ⁴ · e^{−A x} · [1 − cos(A y − σ/f)].** *What it is:* a wave-shaped energy that ties the twist angle y to the hidden field σ. *How we know it:* this is exactly the term a hidden force with **8 colours (SU(8))** leaves behind when it condenses — and 8 is the angle's period from Step 3. During inflation it is a billion times too small to matter (checked). *How it works with the field:* at the cliff, σ and y are pulled toward each other; that pull **spins the twist angle** — the kick.

**Decay of σ (coupling y ≈ 0.1).** *What it is:* σ must disappear afterwards or it would hold half the universe's energy. A small coupling lets it decay into heat. *How we know it:* checked — it removes σ almost completely and costs only a little of the matter.

---

### Step 9 — Making matter

**The spinning angle and spin-biased reactions.** *What it is:* through the Nieh–Yan coupling (Step 3), a spinning angle acts on the hot plasma like a small energy difference between left- and right-spinning particles. *How we know it:* standard physics of "spontaneous baryogenesis"; the chemical-balance factor μ_ℓ/μ_A = 0.523 is calculated.

**The Weinberg operator (neutrino masses).** *What it is:* the tiny interaction that gives neutrinos their mass. In the hot plasma it lets lepton number change, so the spin bias turns into a **lepton excess**. *How we know it:* neutrino masses are measured (oscillations); the Twist needs the sum Σm_ν below ~0.064 eV (normal ordering).

**Sphalerons (28/79).** *What it is:* processes in the Standard Model that turn a lepton excess into a matter (baryon) excess; 28/79 of it ends up as baryons. *How we know it:* textbook Standard Model.

**Result.** The matter excess comes out at the observed size — about 6 extra protons and neutrons for every 10 billion particles of light — with m_σ ≈ 3×10¹⁰ GeV. *What it does to spacetime:* this leftover matter is all the stars, planets and people.

**Heavy partner particles (R-parity).** *What it is:* in supergravity every particle has a heavy partner; at this temperature some are made. They must be allowed to decay (a small "R-parity-violating" coupling between about 10⁻⁵ and 10⁻³), or they would be left over. *How we know it:* estimated; this is an added assumption, stated as one.

---

### Step 10 — Dark matter

**Gravity-only dark matter.** *What it is:* a particle that interacts with ordinary matter only through gravity. It is made in the hot plasma when two ordinary particles swap a graviton. *How we know it:* the production rate is calculated (Clery, Mambrini, Olive & Verner); with the Twist's heat, and allowing for the kination phase (which makes less of it), it gives the observed amount for a mass of about **1–6×10⁸ GeV** (estimate). Inflation itself would make far too many light scalar particles (by 10²²+), so it must be a **fermion**. *What it does to spacetime:* provides the extra gravity that holds galaxies together. *Prediction:* dark-matter detectors keep seeing nothing.

---

### Step 11 — The tail and dark energy

**Dark energy.** *What it is:* the energy that makes the expansion speed up today (about 69% of everything). *How we know it:* supernovae, BAO and the CMB. In the Twist it is the energy left on the tail: its size is set by the cliff depth (n ≈ 124) — a number chosen to match, not predicted.

**Thawing and w.** *What it is:* w is the ratio of pressure to energy; w = −1 is a pure cosmological constant. On the tail the field was frozen for most of history and is now just starting to roll ("thawing"), so w rises slightly above −1: **w₀ ≈ −0.90**, changing slowly (**w_a ≈ −0.15**). *How we know it:* calculated from the slope √(2/3). *Tested by:* DESI, which today prefers w₀ ≈ −0.80 and w_a ≈ −0.73 — the Twist cannot go below w_a = −0.40 (locked).

**The dark-matter coupling β (FLAG-1 version).** *What it is:* an optional small energy exchange between dark energy and dark matter, β ≈ 0.04. *How we know it:* fitted to data (the one extra number in FLAG-1). *What it does:* makes dark energy look as if it crosses w = −1 to someone who assumes ordinary dark matter, pushing the apparent w_a to about −0.27. The **pure Twist** (β = 0) needs no extra number and fits the newest Planck + DESI data better than standard cosmology (Δχ² −3.85).

---

### Step 12 — What it predicts for the sky we can measure

- Structure grows about **3% more slowly** than in standard cosmology (fσ₈), and the lensing ratio E_G is about 5% higher; S₈ ≈ 0.79. *Tested by:* DESI full-shape, Euclid.
- BAO distances within about 1% of standard cosmology, with a specific pattern by redshift (frozen).
- No CMB polarization rotation (birefringence β = 0) — measured today at about 0.3°, a ~5σ tension, waiting for a calibration-independent measurement.
- A gravitational-wave hum from inflation of about 4×10⁻¹⁸ — too faint for LISA; only CMB B-modes (LiteBIRD) or a future DECIGO-class mission.

### Step 13 — How it could be proved wrong (all locked before the data)

| Test | The Twist says | It fails if |
|---|---|---|
| n_s | 0.963–0.965 (best estimate 0.965–0.968) | Simons Observatory confirms ~0.973 |
| r | 0.0034–0.0040 (locked rule uses 0.0037–0.0040) | a measurement with error ≤ 0.002 finds r < 0.002 or r > 0.008 (95%) |
| w_a | ≥ −0.40 | DESI DR3 finds w_a + 3σ < −0.40 |
| Birefringence | 0 | a calibration-independent β at 5σ |
| Lab tests (6) | no fifth force, no drifting constants, c_gw = c, a tiny spin push of ~3×10⁻³⁴ eV | any confirmed detection |
| Dark matter | gravity-only fermion | a confirmed signal in a dark-matter detector |

### Step 14 — What is still open
- n_s with ACT/SPT data, w_a from DESI, and birefringence: three live tensions.
- The hidden SU(8) is matched in form, not built in full.
- Several numbers are estimates (hidden mass from a fit through three runs; fermion dark-matter argument).
- Heavy partners need an added assumption (R-parity violation).
