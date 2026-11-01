# Lock attractor: results (PREREGISTRATION_LOCK_ATTRACTOR.md, locked 09:12:55)

**Code:** `lock_attractor.py`. **Data:** LOCK_ATTRACTOR_RESULTS.json and LOCK_ATTRACTOR_PHASE.json.

## Validation (passed before the scans)

- **Energy conservation:** ρ_φ integrated separately from its continuity equation agrees with ρ_φ rebuilt from (φ, φ')
  to **4.6 × 10⁻¹²** (β = 0) and **3.8 × 10⁻⁹** (β = 0.1). The pre-registered limit is 10⁻⁶.
  - A first version used a numerical derivative on a grid; it cannot reach 10⁻⁶, so it was replaced before any scan.
- **Release estimate:** m_eff = H predicts the roll begins at z ≈ 9,200; the solver shows it begins (φ moved 1% of F)
  at z ≈ 11,500. That is 25% agreement for an order-of-magnitude estimate. The peak of f_EDE follows later, at z ≈ 3,409
  for the central Λ⁴.
- **Tolerance:** z_peak is unchanged at rtol 10⁻⁹.

## Verdicts (rules as written)

**All 30 settings are NO LOCK.** S = max/min of z_peak over two decades of Λ⁴:

| Case | Range of S | Best S | At equality throughout? | Verdict |
|---|---|---|---|---|
| A, uncoupled (F 0.1, 0.2; three θ_i) | 3.46–3.56 | 3.46 | no | NO LOCK, matching the no-lock reference (≈ 3.2) |
| B, β ≤ 0.1 (allowed coupling) | 2.85–12.9 | **2.85** (F 0.2, hilltop start, β 0.1) | no (z 3,892–11,099) | NO LOCK |
| B, β = 0.3 (strong) | 2.02–10.3 | 2.02 (F 0.1, θ 2.7) | no (z 1,275–2,581); f 0.023, not relevant | NO LOCK |

**Case C (fixed points with constant local λ, for λ = 0.1, 1, 3 and β = 0, 0.1):** **no saddle at equality.** Every
fixed point lies where Ω_r = 1, where Ω_m ≈ 1, or on the radiation-scaling line (Ω_m = 0). Equality is a transient
between them, not a point the flow can hold.

**Cross-check with gate V3:** the coupled matter-era point (β = 0.1) has x² = 0.00473 = 2β²f_c²/3 with
f_c = ω_c/(ω_b + ω_c). It matches the Coupled Twist build independently.

## Overall

**NO LOCK.** The onset of the early field follows m_eff ≈ H, so it is set by the energy scale Λ, a parameter. A
dark-matter coupling makes it a little less sensitive (S from 3.5 to 2.9 for allowed β) but does not pin it to equality.
The minimal twist field, with or without the coupling, does not derive the lock.

**What this rules out, and what remains:**
- **Ruled out:** a lock from the field alone, or from a constant CDM coupling.
- **Remains:** a saddle at equality needs couplings that depend on the field *and* on both radiation and matter, like
  Ramadan, Karwal & Sakstein's construction (2023). Their model is disfavoured by data, and nothing in the minimal
  torsion action supplies such couplings.
- **The paper's statement** "the lock is a phenomenological choice" now rests on a test, not only on argument.

## Scope note (online check after the result)

**Not tested here:** the **chameleon EDE** construction (Karwal, Raveri, Jain, Khoury & Trodden 2021, arXiv:2106.13290).
It pairs a *quartic* potential with an exponential CDM coupling. The authors present the coupling as a possible answer
to the same "why then" (equality) problem.

Our NO LOCK covers the twist potential (cos³, and the plain cosine via the phase-space case) with a constant coupling
β. It does not rule out a chameleon-type effective minimum. Testing that would be a separate, pre-registered study,
with a potential the torsion construction does not supply.