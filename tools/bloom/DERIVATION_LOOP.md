# The UFE derivation Loom loop (set 22 Nov 2026, 02:52; Danny: "set up derivation UFE loop loom till done")
**Each tick** is one derivation step, run self-scheduled **every 3 min** (Danny 03:00):
1. Pick the top open item from the queue below.
2. **Referee pre-check (new, from D2051a):** write the textbook formula the step relies on, with its source, before any toy model is built.
3. Lock PREREG + sha256, pushed **before** any reading of numbers or computing.
4. Run: research (2–4 searches or fetches) or compute (a short script in theory/tests/).
5. Write the D-note with its verdict (PASS / FAIL / NULL / FIT / CONDITIONAL). Wrong earlier claims get dated corrections.
6. Update bloom_data.json filters and the queue; run test_bloom.py, which must print READY.
7. Commit and push; send a 3–5 line message to Danny; schedule the next tick.

**Stop rules:**
- **NAILED:** the D2039 battery passes every goalpost with 0 moved knobs, all filters are cleared, and the referees have signed.
- **STALL:** 7 consecutive ticks with no new lead and no closed item → report, and wait for Danny.
- **Danny's live messages always come first.**

## NEXT TASK: follow tools/bloom/DERIVATION_PLAN.md in order. The next open step is **P2b**: fix the factor (1 or 2) of the hypercharge cross term c_a c_b F_a F_b in f₂ − f₃ = −½S∫(F_Y² + 2F_D·F_Y) with F_Y = Σ c_a F_a. That picks branch A (1/12, +0.046) or B (1/6, +0.092) with no knob. Then P3 families, P4 tadpole, P5 massless U(1)_Y, P6 branch, P7 KL, P8 W₀, P9 F-theory, P10 battery.

## Queue (open items, in order). Tick log: tick 1 = D2054 (Q1, partial); tick 2 = D2055 (Q2, CONDITIONAL); tick 3 = D2056 (Q3, FAIL; no-progress count 1); tick 4 = D2057 (Q4, CANDIDATE; count 0); tick 5 = D2058 (Q5 merged, Q6 fact; first full pass done); tick 6 = D2059 + D2060 (all-in-one pass: 1/12 flux ALLOWED via windings; D3 routes FAIL; branch B = mirage + 1/6 flux); D2061 P1/P2; D2062 P2b undetermined; tick 7 = D2064 (single stack cannot give T1, so split stacks are needed); tick 8 = D2065 (CANDIDATE: one integer flux unit on the lepton/right U(1) stack gives α_s 0.1167, two units give 0.1193; next P4 families + P5 tadpole/massless U(1)_Y); tick 9 = D2066 (P4/P5 undetermined; count 1); tick 10 = D2067 (P4/P5 structurally ALLOWED: the IMR families do not depend on the free n's, and an n_d² step keeps the massless U(1)_Y with the tadpole absorbed by hidden branes; next: the size of the α_Y step from the radii; count 0); tick 11 = D2068 (step size: POSSIBLE, 8.8% of natural radii; median |δ(1/α_Y)| = 2.39, against 0.68 needed; next: fix χ from v4's frozen U (ρ, i) and recompute with no free radius); tick 12 = D2069 (radii fixed by the Kähler areas, χ = 1/A = 0.223: 1 hit in 16 (α_s 0.1196), with no look-elsewhere weight; a real Z₆-II projection is needed); tick 13 = D2070 (P7: the two-stage toy holds the volume with m_T²/H² = 24 if β = 3/(8σ) = 0.019, which is FIT (below the natural window); next: derive β ~ 1/σ from an α′ or loop correction); tick 14 = D2071 (β origin FAIL: modular-weight and loop forms give no minimum or need |c| ~ 60–80 with a negative metric; Q2 stays FIT; count 1); tick 15 = D2072 (W₀ from a same-cycle racetrack FAIL: B/A unnatural, |W| 17–96× too small; five W₀ routes failed; count 2); tick 16 = D2073 (Q6 undetermined: ρ is the E₆/E₈ monodromy point, non-perturbative; D(−1) weight 4.3e-3 per instanton; no f formula found; count 3); tick 17 = D2074 (Q5 partial: published Z₆/Z₆′ models are consistent, but their hidden sector is at most Sp(6), with no room shown for SU(12); count 4); tick 18 = D2075 (tadpole estimate FAIL: D3 charge 46 vs budget 4–6; count 5); tick 19 = D2076 (K3 curvature −1 per D7: total 29 or 12, still above 4–6, FAIL; count 6); tick 20 = D2077 (branch B bino relic FAIL; count 7 → **STALL. Loop stopped**; see FRONTIER_2026-11-22.md)
| # | item | current state | first move |
|---|---|---|---|
| Q1 | **mirage** (F^T_vis feeds gauginos at m₃/₂/x ≈ 12 TeV) | FAIL; the tether is void (D2051a); warped D3 incompatible with S = ρ (α_G⁻¹ = 0.87, D2054) | next: the D3-at-singularity twisted f (f = S + c·T_blow); otherwise fold mirage into Q4 |
| Q2 | **Kallosh–Linde stabiliser** (needs m_T ≥ 3.7e3 × KKLT) | CONDITIONAL (D2055): two-stage stabilisation −β(T+T̄)\|X\|² (1112.4488) gives boost ~1.2e5; costs β, γ + minima coincidence | survey: "volume stabilisation during high-scale inflation" since 2015 (e.g. stronger stabilisation, Kähler uplift, inflaton-volume decoupling) |
| Q3 | **W₀ = 5.6e-9 origin** | unexplained (D2044–D2046; dark-condensate-as-W₀ FAIL analytically, D2056) | lock a test of the x ≈ 4π√3 near-coincidence with a computed instanton prefactor |
| Q4 | **T1 seam** (+0.044) | CANDIDATE (D2057): a 1/12 fractional hypercharge-flux quantum gives +0.0458 (p = 0.20, no evidence weight) | derive: is a 1/12 quantum admissible on Z₆-II/ΩR (charge lattice, Freed–Witten, massless U(1)_Y)? |
| Q5 | **tadpole budget** | OPEN; merged with Q4 (D2058) | write v4's explicit brane configuration (stacks, wrappings, fluxes, O7s) on Z₆-II/ΩR. Serves Q4 and Q5 together |
| Q6 | **g_s = 2/√3** | fact (D2058): no SL(2,Z) frame has g_s < 2/√3 | treat in F-theory; E(S, 3/2) is already modular-invariant |

## LOOP 2 (Danny 08:10 "Loom loop 3 min")
**Rules:**
- one locked rung per tick (PREREG + .sha256, then compute, then a D-note, then commit and push), then send_later(3 min);
- **NULL:** a tick with nothing new and nothing computed ends the loop;
- **STALL:** 3 no-progress ticks in a row end the loop;
- formula first (referee rule); corrections as dated notes.

**Queue (from FRONTIER + D2083–D2098):**
- **L1:** tan β ≈ 1.9 against BIM's boundary value of 1. Run the Higgs soft masses and μ, B from M_s to M_S (one loop, top-dominated). Does the radiative splitting m²_Hu < m²_Hd give tan β ≈ 1.9?
- **L2:** v4's dark force as a separate dark U(1) (D2098 owed). Gauge coupling from its brane cycle, then α_D at 12.8 GeV and DM consistency.
- **L3:** the D7 tadpole ledger for the KL racetrack ranks (7, 8) and (14, 15) on T_vis (formula first).
- **L4:** Seed v5 with built-in filters: 3 + 3 families, tadpole + K, the confinement size rule (D2097), unification; L = 4.
- **L5:** the birefringence coupling c_γ/f, derived or fitted (v4 axion on which cycle?).
- **L6:** lock the 4π√3 shared-exponent hypothesis (KKLT branch) against the gauge chain.

**Tick log (loop 2):**
- **Tick 1 (08:15, L1):** D2099 FAIL. The BIM boundary has Bμ too large; there is no light-Higgs vacuum. Lowering B to 1.44 m₃/₂ (tuned) gives tan β ≈ 1.4, below m_h's 1.9. Progress: yes (a new constraint). L1′ added to the queue.
- **One pulsed pass (08:20), D2100:**
  - P1 PASS: dark U(1) ⊂ U(12), α_D = 1.0e-3.
  - P2: tadpole likely over by ×1.9 / ×3.6 (estimate).
  - P3: no unified + exotic-safe PS at L = 4 for these χ.
  - P4: the birefringence axion must be separate (FIT).
  - P5: dropped.
  - P6: CONSISTENT with one O(1) knob μ_W/μ = 0.25; α_s = 0.1181.
  - Queue exhausted. New owed items: Stückelberg check; Z₆-II divisor data; Seed χ/tilt scan; derive μ_W/μ.
