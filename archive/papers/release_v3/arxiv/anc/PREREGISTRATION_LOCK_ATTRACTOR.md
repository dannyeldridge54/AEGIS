# Pre-registration: can the equality lock come from the dynamics? (phase-space study)

**Written:** 2026-11-01 09:12:55 CT. The time is from the clock, inserted by the same command that hashes and commits this file. No
code for this study had been written or run.

**Locking:** SHA-256 hashed and committed when written; never edited afterwards.

## Question

The Locked Twist puts the peak of the early field's energy share at matter–radiation equality **by hand**. Can the
field's own dynamics put it there, so that the peak redshift is insensitive to the field's energy scale Λ? That would
turn the lock from an assumption into a result. Known route: a saddle point at equality (Ramadan, Karwal & Sakstein
2023).

## Setup

**Background:** flat; radiation, baryons, CDM; no late dark energy (irrelevant before z ≈ 100). The ratio ω_r/ω_m gives
z_eq ≈ 3400, from the Planck-like values used in our fits.

**Field:** canonical φ (in M_Pl units), V = Λ⁴[1 − cos(φ/F)]^n.

**Equations,** in N = ln a:
- the Klein–Gordon equation with Hubble friction;
- for case B, the CDM coupling of PREREGISTRATION_COUPLED_TWIST.md: m_c ∝ e^{βφ}, ρ_c a³ ∝ e^{β(φ−φ_i)}, with source
  −βρ_c.

**Code:** a new script `lock_attractor.py`, checked first against the uncoupled case (energy conservation to 10⁻⁶) and
against the radiation-era release estimate m_eff ≈ H.

**The quantity:** z_peak, the redshift of the peak of f_EDE = ρ_φ/ρ_tot.

**Scans:**

| Case | Settings | Λ⁴ |
|---|---|---|
| A, uncoupled | n = 3; F ∈ {0.1, 0.2} M_Pl; θ_i ∈ {2.7, 3.1} | varied over **two decades** |
| B, CDM-coupled | n = 3; F ∈ {0.1, 0.2}; θ_i ∈ {2.7, 3.1, π − 10⁻³}; β ∈ {0.01, 0.03, 0.1, 0.3} | the same two decades |
| C, phase space | the uncoupled and coupled systems in the variables (x, y, Ω_r) with local λ = −V_φ/V | — |

**Range of Λ⁴ for every case:** centred on the value that puts z_peak at z_eq for the uncoupled case with the same F
and θ_i.

**Case C detail:** list the fixed points found and their stability, and state whether any **saddle lies at equality**,
i.e. whether it exists only while Ω_r and Ω_m are both of order 1.

## Rules (for each case A and B setting)

**S** = max(z_peak) / min(z_peak) over the two decades of Λ⁴. **Relevant** means the peak f_EDE lies in 0.03–0.12 for at
least the central Λ⁴.

| Verdict | Rule |
|---|---|
| **LOCK DERIVED** | S < 1.5, **and** every z_peak within [z_eq/1.5, 1.5 z_eq], **and** relevant |
| **PARTIAL** | S < 1.5 but not at equality, **or** at equality but S between 1.5 and 2.5 |
| **NO LOCK** | anything else |

**Reference without a lock:** release when m_eff ≈ H in the radiation era gives z_peak ∝ Λ, so two decades of Λ⁴ give
S ≈ 3.2.

**Overall:**
- **LOCK DERIVED** if any case B setting with β ≤ 0.1 meets the rule. β ≤ 0.1 is consistent with coupled-quintessence
  bounds.
- If it holds only for β = 0.3, report it as **LOCK DERIVED ONLY WITH STRONG COUPLING**, which is in tension with
  bounds.
- Otherwise, report the best S found and the verdict.

## Expectation, written in advance

**NO LOCK** is the likely outcome.
- **Uncoupled:** the release is set by m_eff ≈ H, a parameter coincidence.
- **With the coupling:** the CDM force grows like Ω_c and does switch on near equality, so it could seed the release
  from the hilltop. But near the hilltop any seed grows fast once |m_eff| > H, so the timing should follow m_eff ≈ H
  again, with only a logarithmic dependence on the seed.

A LOCK DERIVED result would be a surprise and would need independent checks. Either way, the result goes into the paper's
"what geometry does and does not fix" section.

**This adds one more test to the programme's trial count.**
