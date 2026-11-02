# Pre-registration: three UFE consistency checks: early role (ER), LQG value (LQ), inflation (IN)

**Locked:** 2026-11-02 15:50:03
**Written** before any number below was computed. Danny, 2 Nov: "all" (PATH_DECISION_2026-11-02.md, UFE gaps 1–3).

**Common setup:**
- The BI field in N = 1 supergravity (Gates, Ketov & Yunes, arXiv:0906.4978, eqs. 5.36–5.37): Φ = ϕ + i a,
  K = −3 ln(−Ω/3), Ω = e^{2ϕ}·2ϕ, ϕ < 0. Reduced Planck units.
- Canonical dilaton: |ϕ| = e^{√(2/3)χ}.
- Matter in Reading A (supergravity Jordan frame): ln A = −ϕ − ½ ln(2|ϕ|/3); the GR point is ϕ = −½
  (SOLAR_GATE_RESULTS.md).
- **Tier for all three: HYPOTHESIS → at most MEANING.** They test consistency of an embedding, not data fits.

## ER. Can the dilaton's relaxation to its GR point supply the early energy?

- **Integration** (`ufe_checks.py`): flat background from z = 10⁸ to 0 with radiation, matter coupled through A(χ), and the
  dilaton with no potential; χ' = 0 at the start. Ω_χ = (dχ/dN)²/6.
- Radiation is traceless and does not source the dilaton (e± annihilation kicks ignored; stated).
- Present densities Ω_r, Ω_m are fixed to the ΛCDM halofit best fit; dark energy is a constant Λ in the background
  (its role here is only the late expansion).
- **Scan:** starting |ϕ|ᵢ on a log grid from 0.05 to 5 (100 values).
- **Verdict:**
  - **VIABLE** if some |ϕ|ᵢ gives Ω_χ(z = 3500) in [0.03, 0.12], Ω_χ(z = 500) ≤ 0.01 (the energy must decay),
    |Δχ| < 0.0072 today (Cassini), and |A²(z_BBN = 4×10⁸)/A²(0) − 1| < 0.10 (Newton constant at BBN).
  - **WRONG SHAPE** if Ω_χ(3500) in [0.03, 0.12] is reached but any other condition fails.
  - **TOO SMALL** if Ω_χ(3500) never reaches 0.03.

## LQ. Does the BI field today sit at the LQG value of the Immirzi parameter?

- **Mapping (assumption, stated):** Re Φ multiplies R and Im Φ multiplies the Holst term, so 1/γ = a/ϕ. The dilaton
  is at its GR point today (|ϕ| = ½, required by SSG). The canonical axion is ã = √6·a there (kinetic term
  3(∂a)²/(4ϕ²)), and ã is identified with the Twist field φ measured from the minimum of its cosine potential.
  Hence **|γ_today| = √6 / (2 |φ_today|)**.
- **φ_today:** from CLASS (`phi_scf` at z = 0) at the two Late Twist best fits (Pantheon+ `gF0.4m-0.3_nlfix`;
  DES Y5 `gF0m0.102_desy5_nlfix`), evaluated as in LZ.
- **LQG values (two declared):** γ = 0.2375 (Domagała–Lewandowski / Meissner counting) and 0.2740 (Ghosh–Mitra counting).
- **Verdict:**
  - **MATCH** if both fits give |γ_today| within 10% of the same LQG value.
  - **PARTIAL** if only one fit does.
  - **NO MATCH** otherwise.
- Look-elsewhere: 2 LQG values × 2 fits, and the mapping has convention freedom. Even a MATCH stays MEANING tier.

## IN. Does the α = 1 geometry give acceptable inflation?

- **Prediction** (α-attractor T-model, α = 1 from K = −3 ln; the potential's form is assumed, stated):
  n_s = 1 − 2/N, r = 12/N², for N = 50–60 e-folds.
- **Data:** n_s = 0.974 ± 0.003 (ACT DR6 + Planck + lensing + DESI DR1; Louis et al., arXiv:2503.14452, abstract);
  r < 0.036 (BICEP/Keck 2018, 95%).
- **Pull:** (0.974 − n_s(N)) / 0.003, at N = 60 (most favourable within the range).
- **Verdict:**
  - **CONSISTENT** if pull ≤ 2 and r below its bound.
  - **TENSION** if 2 < pull ≤ 3.
  - **DISFAVOURED** if pull > 3.
- Also reported: the N needed for pull = 2. Our own fits have early energy, which is known to raise the preferred n_s;
  that is reported, not used.

## Expectations (not rules)

- ER: WRONG SHAPE. A coupled dilaton gives a plateau through the matter era, not a peak at z ≈ 3500.
- LQ: NO MATCH (no reason it should).
- IN: TENSION. ACT DR6 is known to push Starobinsky-like models.
