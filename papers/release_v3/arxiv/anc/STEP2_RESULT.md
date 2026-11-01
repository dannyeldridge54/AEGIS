# Step 2: can geometry produce the potential V = Λ⁴[1 − cos(φ/F)]³?

31 October 2026, about 21:00 CT. Code: `step2_potential.py` (sympy and numpy). Data test:
PREREGISTRATION_POWER_N.md.

## 1. What makes n = 3 special: a flat bottom

| Power | Near the minimum | Behaviour once released |
|---|---|---|
| n = 1 | x²/2 (a mass term) | Decays like matter (w = 0) |
| n = 2 | x⁴/4 | Decays like radiation (w = 1/3) |
| **n = 3** | **x⁶/8** | **Decays faster than radiation (w = 1/2)** |

- **As harmonics:** (1 − cos x)³ = 5/2 − (15/4) cos x + (3/2) cos 2x − (1/4) cos 3x.
- **Two cancellations:** with a₁, a₂, a₃ = −15/4, 3/2, −1/4, both Σ k² a_k = 0 and Σ k⁴ a_k = 0. Checked exactly.
- **So n = 3 is not "a cosine cubed by chance".** It is a sum of harmonics tuned to cancel both the x² and the x⁴ terms.
  Any derivation must produce **two exact cancellations**.

## 2. What the natural mechanisms give

- **The Nieh–Yan term alone gives no potential.**
  - N = d(e^a ∧ T_a) is the derivative of a globally defined 3-form, so its integral over a closed spacetime is zero.
  - It has no topological sectors of the kind that give axions their potential (instantons).
  - Coupling the field to it (Mercuri) makes the field axion-like (shift-symmetric), but the potential must come from
    somewhere else.
- **An instanton-type series, a_k ∝ (−r)^k or (−r)^k/k (any 0 < r < 1):** the x² coefficient at the minimum is always
  positive (checked for r = 0.1–0.8). There is always a mass term, so it **behaves like n = 1**.
- **An anomaly with a confining force** (how the QCD axion gets its potential; Lattanzi & Mercuri identify the
  Barbero–Immirzi field with it):
  - The chiral potential V = −√(1 − 4z/(1+z)² sin²(x/2)) has an x² term, so it also **behaves like n = 1**.
  - Its scale is set by the confining force. QCD gives about 75 MeV, far above the ~0.5 eV needed and switching on far
    too early, so a new hidden force confining near the eV scale would be needed.

**Conclusion:** the natural routes give **n = 1-like potentials**, with a mass term at the bottom. Getting n = 3 needs
two exact cancellations, the same "coincidence of scales" that McDonough & Scalisi met in string theory. **Geometry
does not obviously give cos³.**

## 3. The deciding question: does the data need n = 3?

If a natural shape fits about as well, the derivation problem mostly disappears. Pre-registered in
PREREGISTRATION_POWER_N.md, with deviations logged:

- **n = 1:** CAMB's solver cannot run it (non-finite likelihood at every tested point). It is deferred to AxiCLASS. The
  published literature finds n = 1 fails as early dark energy, because it decays like matter.
- **n = 2:** running now on the combined data (`spa_edelock_n2`), started 21:0x CT.

**Rule:** D₂ = χ²(n = 2) − χ²(n = 3).
- If D₂ < 2, n = 3 is **not needed**, and a more natural shape is fine.
- If D₂ > 4, the data **require** the flat bottom, and geometry must explain the two cancellations.

## Where this leaves the theory

- **If n = 2 fits as well:** the target becomes a potential with an x⁴ bottom. That is one cancellation, Σ k² a_k = 0,
  instead of two. Easier, but still not automatic.
- **If n = 3 is required:** the potential's shape stays assumed (as in the paper), and the honest statement is that
  neither geometry nor string theory currently explains it.
- Either way, the Nieh–Yan route cannot supply a potential by itself. It needs a confining sector or another source.

## Result (2026-10-31, fit finished 21:13 CT): n = 2 on the combined data, **n = 3 REQUIRED** (by the rule)

| Power | χ² | Δχ² vs ΛCDM | f_EDE | θ_i | H₀ |
|---|---|---|---|---|---|
| n = 3 (`spa_edelock`) | 2396.77 | −5.63 | 0.070 | 2.74 | 70.15 |
| n = 2 (`spa_edelock_n2`) | 2407.12 | **+4.72** | 0.067 | 2.30 | 70.29 |

**Rule:** D₂ = 2407.12 − 2396.77 = **+10.35 > 4**, so the data **require** the flat-bottomed n = 3 shape.

**Robustness note (not part of the verdict):**
- **Only 1 of 4 restarts succeeded,** because CAMB's solver fails over much of the n = 2 parameter space; that is also
  why it started at θ_i = 2.5.
- **The n = 2 best point is worse than ΛCDM,** which n = 2 contains (f → 0). So the search did not reach its true
  minimum, and the real n = 2 cost could be smaller.
- **A converged n = 2 fit could improve on ΛCDM somewhat;** published EDE work generally finds n = 2 helps less than
  n = 3. With CAMB's solver we cannot tell how much. A cleaner n = 2 test needs AxiCLASS, which also handles n = 1. The
  verdict stands by the rule, with this caveat attached.

**What it means:** the improvement in the data comes specifically from the flat (x⁶) bottom of the n = 3 potential: the
early energy must fade faster than radiation.
- That is exactly the shape that needs **two exact harmonic cancellations**, which neither geometry nor the natural
  mechanisms provide (sections 1–2 above).
- So the honest position is: **the data favour a potential shape that physics does not yet explain.** That is the same
  open problem the string-theory EDE papers report.
