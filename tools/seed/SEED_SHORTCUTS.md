# Seed shortcuts: online review, 22 Nov 2026 (D2081)
Nine search rounds were run, and round 9 was null (only repeats). Each item says where it plugs into the Seed.

**Labels:**
- **EXACT:** gives the same answers faster.
- **HEURISTIC:** a stochastic search; it can miss solutions.
- **DIAG:** a diagnostic only, with no measured speedup.

**Not read:** 2611.19950 (a flux-vacua foundation model) was rate-limited and could not be fetched.

## Tier A: exact, cheap, portable now (adopt in Seed v3)
| # | shortcut | source | what it buys the Seed |
|---|---|---|---|
| A1 | **Integer moduli.** The SUSY condition becomes Σ_I Ŷ_a^I/U_I = 0 and Σ X̂U > 0, with the U_I taken as 4 positive coprime integers (Lemma 1) | Loges–Shiu 2112.08391; Gmeiner et al. hep-th/0510170 Eq. 12 | SUSY becomes exact rational arithmetic. It **removes the numerical solver and the whole bug class behind the D2080 limit points** |
| A2 | **Constraint-matrix keying plus dynamic programming.** Key each model by the RREF of its Ŷ matrix, find compatible A-branes as graph cliques, then count with the convolution F_{α∪β} = Σ F_α·F_β over tadpole/K-charges | Loges–Shiu 2206.03506 (1.34e11 models at T = 8) | Replaces ring brute force with an exact count. Each matrix is independent, so the work runs in parallel |
| A3 | **Tadpole-sum partition.** Σ_a S_a = C with S_a = Σ_I N_a U_I X̂_a^I; enumerate the partitions of C, then factorise them into N_a·X̂; bound 0 < Σ X̂U ≤ Σ L̂U | Gmeiner et al. hep-th/0510170 Eq. 24–25 | **Moves N and hidden stacks together.** This is exactly the spin axis D2080 showed is needed |
| A4 | **Duplicate removal** (T-duality, orientation and sign maps, torus permutations) | He–Li–Sun 2112.09632: 202,752 models → **33** inequivalent, distinguished by their gauge-coupling relations | Counts inequivalent models only, so the look-elsewhere count is honest. The Seed's `canon()` already covers part of this |
| A5 | **K-theory parity filter** Σ_a N_a Ŷ_a^I ∈ 2Z | hep-th/0510170 Eq. 21 (cuts the count ×5) | **Missing from v2.** Adding it is a consistency fix |
| A6 | **Moduli-free gauge relation:** 1/α_Y = (2/3)/α_s + 1/α_w at M_s | Blumenhagen–Lüst–Stieberger hep-th/0305146 Eq. 2.9. Conditions: π_d = π_a, stack c on an O-plane, U(3)×Sp(2)×U(1)², MSSM spectrum. This gives M_s ≈ 2.0e16 GeV and α = 0.041 | An **α_s goalpost with no radii scan at all**, valid for this model class. The open question is whether v4's brane set is in the class (check before use) |

## Tier B: search heuristics (for when exact enumeration is too large)
| # | shortcut | source | number |
|---|---|---|---|
| B1 | **Genetic algorithm** (crossover makes large jumps, mutation fine-tunes) | 2112.08391; Abel et al. 2111.07333 | ~1e6 consistent models; the GA was ~3.5× more efficient than RL at saturation |
| B2 | **RL (A3C)**, which learns the filler-brane strategy | Halverson–Nelson–Ruehle 1903.11616 | ×200 vs a random walker |
| B3 | **Simulated annealing / QUBO** (constraints written as an Ising Hamiltonian) | 2306.16801 | SA found a model every 0.66 s, vs 33 s for the GA and 100 s for a random scan; quantum annealing was ~1.3× SA |
| B4 | **Two-method saturation as a completeness test** | 2111.07333, 2111.11466 | Agreement between unlike searches is evidence of exhaustiveness |
| B5 | **Action masking and a dense consistency score** | RL-in-HEP survey 2611.02049 | Rewards are shaped, not sparse |
| B6 | **Rigid stacks first, ρ-independent SUSY** | Ecker–Honecker–Staessens 1509.00048 (T⁶/Z₂×Z₆×ΩR) | **The v4-relevant fork** (Z₆ family) |

## Tier C: flux / W₀ side
| # | shortcut | source | number |
|---|---|---|---|
| C1 | **ISD-biased sampling + rounding**, JIT/vmap | JAXVacua 2306.06160 | >100× faster than plain Python; ~1e6 vacua in 10 h on 4 CPUs |
| C2 | **Conditional VAE on \|W₀\|** | 2506.22551 | ×10³ vs Metropolis; smallest \|W₀\| on T⁶ = 0.0073 |
| C3 | **Bayesian flow network / transformer generation** | 2509.16029 | 65–82% validity |
| C4 | **Homotopy continuation** (finds all solutions) | 1108.1201 | exact but slow (the Paramotopy scan took 75k h for 24,882 vacua) |
| C5 | **Heuristics:** balanced NSNS/RR fluxes give small W₀; autoencoder latent near z₁ ≈ 0; Z₄ orbit reduction; a classifier on flux invariants | 2603.04941, 2610.30273 | SUSY classifier: the top 5% holds 47% of SUSY solutions |

**Honest read on W₀:** v4 needs W₀ = 5.6e-9. Every ML or flux shortcut above reaches only ~1e-3 to 1e-2. The only known route to exponentially small W₀ is perturbatively flat vacua (PFV), and D2045 found that PFV does not apply to the rigid Z₆-II. **No shortcut found tonight closes the W₀ gap.**

## Diagnostics only (no speedup)
- The hidden-tadpole-charge Q_hid clusters with 3-family alignment (2312.07181). It is post hoc and untested as a filter.
- Funnel topography (1907.07693) is a selection principle, not a search speedup.
- MAP-Elites is proven in materials science (2403.03511), but **no string-vacua use was found**. It is a cross-domain idea: an archive keyed on (α_s, M_s) could keep diverse elites.

## Seed v3 plan (not locked yet)
1. Adopt A1, A3, A5 and A4: exact integer SUSY, tadpole partitions with N and hidden stacks free, K-theory, and canonical duplicates.
2. Reproduce Gmeiner's T⁶/(Z₂×Z₂) count on a small L as the positive control.
3. Use A6 for an α_s goalpost on the class where it holds.
4. Then fork to Z₆ (B6).
