# PREREG D2049: Forge full optimisation, rung 1 (Danny 02:18 "Forge full opt"). Locked before scoring.
**Build:** loomz20 = loomz18 plus knobs. Defaults reproduce v18 exactly (45,781 on d200k with RCTX = 1). The -O3 -march=native -ffp-contract=off build is bit-identical.

**New base** = the D2025 winner: RCTX = 1, SKIP off, with the best-build env.

**Ratio arms:**
- APM count-rate (ZPAQ SSE, tick 6): (APMLIM = 255, APMSTART = 30) and (APMLIM = 1023, APMSTART = 63).
- At 200 kB they were +0.01% and +0.32% (sanity only, not scored).

**Speed arms:**
- ESKIP = 48: skip the mixer update when |err| < 48/4096 (fx2-cmix).
- The -O3 build.

**Slices (never used):** enwik8 [50, 51) MB, plus a 3 MB rung at [60, 63) MB.

**Pass rules:**
- A ratio arm must be ≥ 0.05% smaller than BASE on both slices.
- A speed arm must be ≥ 10% faster (wall time on the same machine) with ≤ 0.02% loss in size (≡ output for the O3 build).
- Round-trip on the best arm.
