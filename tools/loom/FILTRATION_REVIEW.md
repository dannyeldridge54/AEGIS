# How our filtration works, what it caught, what is missing, and the "set a target and nail it" protocol (22 Nov 2026)

## 1. The filtration chain as it ran on 21–22 Nov (each stage, and what it caught)
| # | stage | what it does | caught tonight |
|---|---|---|---|
| F0 | **lock** (PREREG + sha256, pushed first) | fixes the question and the pass rule before any number exists | stopped every "move the goalpost" case |
| F1 | **calibration / controls** | must reproduce known answers and known nulls | Z35/Z40 (D2018/D2019), planted 2-block graphs, the M = 9 U1 control (D2020), the K = 11/12 SAT controls (D2003) |
| F2 | **independent methods** | 2–3 implementations must agree | gluing + SAT + numba (D2003); v1 vs v3 U1 |
| F3 | **held-out data** | gains must survive data never used to tune | the outer rings, trigram, IGN and BOOST were rejected (D2010, D2014) |
| F4 | **filters and bridges** (F1–F7, B1–B4) | hard physics limits and null relations | the hidden E8×E8 failed ΔN_eff and the gravitino box (D2009) |
| F5 | **look-elsewhere** | counts trials before calling a hit | the U₃ = 2i "hit" downgraded to NO-POWER (D2022) |
| F6 | **centre balance** | a change must not break another field | U₃ off i breaks "neutrinos at i" (D2022) |
| F7 | **referee** | independent review before a claim | D1897/D1907/D1935/D1942 (earlier rounds) |
| F8 | **dated corrections** | a wrong number becomes a note, never a silent edit | v7 comment bug; counts 12→11 and 21→20 (D2023a/b) |

## 2. What best practice has that we are missing
1. **A global likelihood** (GAMBIT; Cobaya/MontePython for cosmology).
   - Replace the separate pass/fail bars with **one joint log-likelihood** over all 20 datasets, with nuisance parameters for the theory errors.
   - That gives every agent the same scalar target to "nail", and the centre a principled way to trade off fields: the rank-1 m₃/₂ Jacobian becomes visible as a ridge.
2. **A parameter penalty** (Bayesian evidence, or AIC/BIC as a cheap stand-in).
   - Every fitted knob costs log-evidence. This is the quantitative version of "extra knobs = FIT": a knob is kept only if it buys more likelihood than it costs.
3. **Blind analysis.**
   - Freeze the pipeline with the data value hidden or offset, then unblind once.
   - Our locks fix the rule but not our view of the data while we build; blinding closes that loophole.
4. **An automatic trials ledger** (look-elsewhere, done the unified Bayesian/frequentist way).
   - Every scan records its trial count, and every reported significance is corrected by it.
   - D2022 did this by hand; it should be automatic.
5. **Injection-recovery tests.**
   - Plant a known signal in synthetic data and check the full chain recovers it, with the right uncertainty.
   - This is F1 for the physics fits. We have it for search code, not for fits.
6. **Tension metrics between datasets** (suspiciousness, Q_DMAP).
   - Before combining CMB + BAO + SNe, test whether they agree within the model. Otherwise combining them hides a conflict (the DES-Y5-only preference for the thread).
7. **Posterior predictive checks.** After a fit, simulate new data from it and ask whether the real data look typical.
8. **Referees at every gate,** not only at the end. Three kinds:
   - **lock referee** (is the test well posed and powerful?);
   - **compute referee** (code review, units, conventions; the aegis-check C1–C7);
   - **centre referee** (balance plus look-elsewhere before any claim).

   Heterogeneous referees (different method or model) catch different errors; D1942 was the template.
9. **More scales (a scale ladder) for every result:**
   - compression: 200 kB → 3 MB → 10 MB → 100 MB → 1 GB (the event state flipped sign between 200 kB and 3 MB);
   - physics: tree → 1-loop → 2-loop → thresholds (Δ₃ moved from −0.90 to −0.15 to −0.094);
   - Ramsey: small-n analogues → n = 35 → n = 40.

   A result counts only if it is stable across its last two rungs.

## 3. The protocol: set a target and nail it
1. **Target:** one scalar.
   - Physics: ln L_global − ½·(#fitted knobs)·ln N, a BIC-style penalty, over all datasets the agent owns.
   - Compression: bytes on held-out data.
   - Ramsey: α ≤ 9, or a closed case.
2. **Agents:** at most 9 knobs each (core standard). The centre runs the bandit over agents (loomcore.Centre).
3. **Gates, each with its referee:**
   - lock;
   - calibration and injection;
   - compute check;
   - held-out / blinded run;
   - trials correction;
   - centre balance plus tension metric;
   - independent referee.
4. **Scales:** a result has to hold on the last two scale rungs.
5. **Stop rules:**
   - **NAILED:** the target is met on held-out or post-lock data with all gates passed.
   - **STALL:** 7 nulls; switch to exploring.
   - **FIT:** the target is met only by adding fitted knobs; recorded, never claimed.

## 4. What this changes now
- `derivation_agents.json` gains, per agent, its likelihood terms, its knob budget and its gate referees.
- LOOM_CORE_STANDARD goes to v1.1 (sections 8–9).
- The first implementation target is a minimal global-likelihood engine over the tracked datasets, with a BIC penalty. With it, T1 (the seam) and T2 (the wino) are traded off by one number.
