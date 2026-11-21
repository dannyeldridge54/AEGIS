# The Weave balance board, round 1 (21 Nov 2026, 17:55 CT)
Nine node agents (independent and read-only, one per node) reported on their nodes. See WEAVE_NODE_CHARTER.md for the nodes and the endpoint. The coordinator merged the reports here.

## State of every node
| node | state | what it is doing | the main strain | cheapest honest move |
|---|---|---|---|---|
| N1 Fold and knots | **STRAINED** | Z₆-II fixes tori 1–2 at ρ and leaves one free modulus, U₃ | U₃ has no stabiliser (U = i is a choice, D1907); no tadpole check | Literature and locked check of Z₆-II tadpoles and U₃ stabilisation, or label U₃ = i TRUST |
| N2 S, the dilaton | **STRAINED** | The E(S, 3/2) plateau fixes the shape; the tilt C sets n_s | Tilt C is **FIT 1** (n_s in band by construction); the m_φ readings are one reading; m_φ ≈ 5e12 is unreconciled with flux stabilisation of S; N* vs T_R unchecked; g_s > 1 | Recompute N* from the real reheating history, and relabel C as FIT |
| N3 T, the volumes | **STRAINED** | One-modulus KKLT gives m₃/₂ for everything | A = 0.54 is effectively fixed by the wino window (FIT); the volume constants are unstated; other moduli are asserted heavy, not shown | Relabel A and 𝒱 as FIT. Then compute the full Z₆-II moduli spectrum and tadpoles (expensive) |
| N4 U, matter and flavour | **TRUST** | Froggatt–Nielsen textures with one fitted spurion size; lepton and neutrino rungs | \|u\| is a FIT with no home; the neutrino ratio margin is thin (1.33 % vs 1 %, no error bar); Koide δ is TRUST | Relabel \|u\| as FIT. Test whether θ-steps at i or ρ give a step of about 0.026 |
| N5 S–T forces | **STRAINED** | α_s 0.1140 single-stack; the split-stack A₃/A₂ ≈ 0.75 is a FIT | α_s is a powered test only with one stack plus a computed threshold spectrum plus correct y_t and DR→MS. **None of these holds today.** The verdict fields are wrong (D1940 "PASS" should say FIT; D1938 "FAIL" should say NO-POWER; D1944 should say CONDITIONAL) | Fix y_t (MSSM β) and DR→MS. Then compute the D7 threshold band, and pre-register that α_s counts only if the band is < 0.001 |
| N6 Spectrum and dark matter | **INDETERMINATE** | Wino at 686.5 GeV on the collider edge; non-thermal winos; m_X = 12.8 GeV | The wino margin is about 0; the wino DM share is **about 20 %**, not "10–40 %"; m_X rests on an assumed 11/28 and on the failing asymmetry | Digitise the Fermi limit (2507.15934 Fig. 6) and the latest disappearing-track limit; add a DM budget that sums to 1 |
| N7 S–T reheating and genesis | **STRAINED** | Leptogenesis lives only as a branching requirement | Derived Br(φ → NN) is at most 5.1 % against 9.5 % needed. At natural p it falls short by ×4 to ×16 | Routes, cheapest first: (1) scan M_N, since Y_B ∝ M_N³, but this re-inputs a derived quantity; (2) raise T_R ×1.9, which squeezes the wino margin; (3) resonant leptogenesis, which needs a flavour model; (4) Affleck–Dine, already walled in by D790–D792 |
| N8 Late universe and the thread | **TRUST** | Nothing derived; every Kähler thread is excluded | No slope source exists. Only α_DEF can be run, and only as an estimate. D1853 already fails | **Relabel V_thread as TRUST** (a phenomenological w(z)) |
| N9 Battery and data | **INDETERMINATE** | 78 rows: 12 done, 55 run, 3 future, 5 need, 1 indeterminate, 1 open; about 20 of the RUN rows are locked | Many RUN rows are bounds that cannot kill. Stale rows: B1 α_s, B10 proton, the B4 lock (assumes the excluded thawing thread), A18 | Score D1 (JUNO: 0.3184 is 1.05σ from data; TM2 is 3.6σ off). Then E3, B3/B11, C10, E1 |

**Balance status: 0 of 9 BALANCED. 2 TRUST (N4, N8), 2 INDETERMINATE (N6, N9), 5 STRAINED.** The endpoint is not reached.

## The pattern across all nine reports
1. **Many "passes" are fits.** The tilt C, the KKLT prefactor A, the quark spurion |u|, the split-stack ratio A₃/A₂ and n_X/n_B = 11/28 are all fitted. An honest count is needed: real predictions vs fits vs TRUST.
2. **U₃ is the shared bottleneck** (N1, N3, N4). It is the only free modulus, it has no stabiliser, and it is asked to host the neutrinos, the dark mirror and possibly the quark spurion.
3. **m₃/₂ is tuned to the wino window** (N3, N6, and N5 through α_s). The one real collider kill test, the wino, has about zero margin.
4. **The S–T seam has no derived mechanism** for α_s (only a fit) or for the baryon asymmetry (Br short ×2–16).
5. **The verdict files still overclaim** in places: D1940 PASS, D1938 FAIL, D1944's unconditional FAIL, and the stale battery rows. Relabelling them costs nothing and strains nothing.

## Moves chosen for round 2 (predicted knock-ons: none strain another node)
1. **Honest relabel pass** (all nodes, zero cost). Fix the verdict fields and the stale battery rows; label C, A, 𝒱, |u|, A₃/A₂, 11/28 as FIT and V_thread, U₃ = i, Koide δ as TRUST; publish the prediction / FIT / TRUST count.
2. **N2:** recompute N* from the real reheating history (m_φ ≈ 5e12, T_R = 3.7e8), then n_s.
3. **N5:** fix y_t (MSSM β above m_s, y_t(M_Z) ≈ 0.96) and add DR→MS.
4. **N9 / N6:** score D1 (JUNO), then lock and score E3 (the Fermi limit, digitised).
5. **N7:** an M_N scan, as a **diagnostic only**. It moves a derived input, so it is not adopted without a referee.

Deferred (high cost, high value): N1/N3 Z₆-II tadpoles, U₃ stabilisation and the full moduli spectrum; the N5 D7 threshold spectrum.

## Checks on this board
- **C5 claim lint:** the board uses no overclaim words. "BALANCED" appears only in the endpoint definition and the status count.
- **C6 four corners:** only n_s has all four corners. α_s, the wino, the baryon asymmetry and dark energy each lack at least two.
- **Referee:** an independent referee reviews this board before round 2 runs.
