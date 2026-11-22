# The UFE derivation Loom loop (set 22 Nov 2026, 02:52; Danny: "set up derivation UFE loop loom till done")
**Each tick** is one derivation step, run self-scheduled about every 5 min:
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

## Queue (open items, in order). Tick log: tick 1 = D2054 (Q1, partial); tick 2 = D2055 (Q2, CONDITIONAL); tick 3 = D2056 (Q3, FAIL; no-progress count 1); tick 4 = D2057 (Q4, CANDIDATE; count 0); tick 5 = D2058 (Q5 merged, Q6 fact; first full pass done)
| # | item | current state | first move |
|---|---|---|---|
| Q1 | **mirage** (F^T_vis feeds gauginos at m₃/₂/x ≈ 12 TeV) | FAIL; the tether is void (D2051a); warped D3 incompatible with S = ρ (α_G⁻¹ = 0.87, D2054) | next: the D3-at-singularity twisted f (f = S + c·T_blow); otherwise fold mirage into Q4 |
| Q2 | **Kallosh–Linde stabiliser** (needs m_T ≥ 3.7e3 × KKLT) | CONDITIONAL (D2055): two-stage stabilisation −β(T+T̄)\|X\|² (1112.4488) gives boost ~1.2e5; costs β, γ + minima coincidence | survey: "volume stabilisation during high-scale inflation" since 2015 (e.g. stronger stabilisation, Kähler uplift, inflaton-volume decoupling) |
| Q3 | **W₀ = 5.6e-9 origin** | unexplained (D2044–D2046; dark-condensate-as-W₀ FAIL analytically, D2056) | lock a test of the x ≈ 4π√3 near-coincidence with a computed instanton prefactor |
| Q4 | **T1 seam** (+0.044) | CANDIDATE (D2057): a 1/12 fractional hypercharge-flux quantum gives +0.0458 (p = 0.20, no evidence weight) | derive: is a 1/12 quantum admissible on Z₆-II/ΩR (charge lattice, Freed–Witten, massless U(1)_Y)? |
| Q5 | **tadpole budget** | OPEN; merged with Q4 (D2058) | write v4's explicit brane configuration (stacks, wrappings, fluxes, O7s) on Z₆-II/ΩR. Serves Q4 and Q5 together |
| Q6 | **g_s = 2/√3** | fact (D2058): no SL(2,Z) frame has g_s < 2/√3 | treat in F-theory; E(S, 3/2) is already modular-invariant |
