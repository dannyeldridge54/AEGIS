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

## Queue (open items, in order). Tick log: tick 1 = D2054 (Q1, partial)
| # | item | current state | first move |
|---|---|---|---|
| Q1 | **mirage** (F^T_vis feeds gauginos at m₃/₂/x ≈ 12 TeV) | FAIL; the tether is void (D2051a); warped D3 incompatible with S = ρ (α_G⁻¹ = 0.87, D2054) | next: the D3-at-singularity twisted f (f = S + c·T_blow); otherwise fold mirage into Q4 |
| Q2 | **Kallosh–Linde stabiliser** (needs m_T ≥ 3.7e3 × KKLT) | FAIL on every route tried | survey: "volume stabilisation during high-scale inflation" since 2015 (e.g. stronger stabilisation, Kähler uplift, inflaton-volume decoupling) |
| Q3 | **W₀ = 5.6e-9 origin** | unexplained (D2044–D2046) | lock a test of the x ≈ 4π√3 near-coincidence with a computed instanton prefactor |
| Q4 | **T1 seam** (+0.044) | unnatural in explicit Z₆′ (D2047) | thresholds for v4's own brane set (D7, IIB) |
| Q5 | **tadpole budget** | FLAG | write the D7/O7 charge budget |
| Q6 | **g_s = 2/√3** | CONDITIONAL | S-duality at ρ |
