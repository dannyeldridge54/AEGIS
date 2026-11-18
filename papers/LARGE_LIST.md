# The large list — everything open across AEGIS + CubeMind (17 Nov 2026). Rule (Danny, 16:31 CT): whenever an item hits a wall, start the next one.
Each item: lock first, run, record (D-note or CubeMind RESULTS.md). Status: OPEN / RUNNING / BLOCKED(reason) / DONE(ref).

## AEGIS — Janus (inflation)
1. JMF7 adiabatic-limit check — DONE (D1206)
2. Janus-MF three fields vs PyTransport — DONE (D1207)
3. Janus-MF curved field space vs PyTransport NC — DONE (D1217: |Δn_s| 8.1e-7, VALIDATED)
4. J7k the three listed ASPIC models — DONE (D1215: HI scored, RPQTI/KMIII listed)
5. Two-parameter ASPIC model scans — DONE (D1218: 16/16 Janus better; PSNI ×3 listed → follow-up 5b with J7d2 bisection)
6. Third-order slow-roll (N3LO) — DONE (D1219: better 16/16 but ×2.88 < locked ×3 → NOT CONFIRMED; follow-up 6b on small-ε points)
## AEGIS — Janus-LT / Hyperion (late universe)
7. L11 Cobaya MCMC check of L7 — DONE (D1205)
8. CosmoPower emulator trial (PC, Python 3.11 env) — OPEN
9. Janus-LT growth + SN joint w0wa — DONE (D1213) (A_s prior fetched: Planck 2018 VI Table 2, TT,TE,EE+lowE+lensing ln(10^10 A_s) = 3.044 ± 0.014, n_s 0.9649 ± 0.0042, τ 0.0544 ± 0.0073; label as an approximation in w0wa — A_s from a ΛCDM fit; σ8 via L9c machinery with w0wa growth)
10. L7 uses DESI DR2 BAO already (tools/janus_lt/desi.py, arXiv 2503.14738 Table IV) — DONE (D1042)
## AEGIS — strings / KALUZA
11. S4E2 independent check of S4e masses — NOT RUN (timeout; V2 informational) (D1214)
12. S4e normalisation convention — DONE (D1216: 4 locked conventions, NOT EXPLAINED; quote ratios + C0). 6D masses step still OPEN
## LOCKBENCH / tools
13. Selftest on the PC env (report mismatches vs ENV.lock) — QUEUED on PC (SELFTEST.job)
14. Ledger upkeep helper (lists missing D-notes; verdicts stay hand-curated — auto-parsing misread lines) — DONE (papers/dash/make_csv.py)
## CubeMind
15. M1 EmoBank appraiser (PC) — RUNNING · 16. M0 embedder (PC) — QUEUED · 17. M2 memory on/off (PC) — QUEUED · 18. Phase 7 AEGIS tools (PC) — QUEUED
19. Phase C2 agreement-vote confidence (PC) — RUNNING · 20. Forge drafter run on skills_wanted.jsonl — QUEUED on PC (FORGE.job)
21. Reranker test after M0 — OPEN · 22. Speculative decoding test — BLOCKED (download needs Danny's OK on the desk)
23. Grading loop: gpt-oss plain / qwen3-coder+verify / qwen3:14b arms to 300 → Phase 3/4 comparisons — RUNNING
24. M3 affect weight — BLOCKED until M1 passes
25. Janus-MF-NC at sphere radius R ≠ 1: unphysical n_s in both python NC and nc-jit (R=1.5 −0.83, R=2 3.49); pole hypothesis refuted; next: PyTransport NC at R=1.5 to tell a shared formulation bug from a real instability — OPEN (D1223); JMF9's VALIDATED verdict covers R=1 only
