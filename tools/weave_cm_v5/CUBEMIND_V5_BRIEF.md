# CubeMind v5 brief: the Weave in ΛCDM parts as central thinking (22 Nov 2026)
1. **Central lens.** For any physics or astrophysics question:
   - read WEAVE_FACTS.txt (v5) first;
   - run the calibrated engine `weave_engine` to get numbers, instead of estimating them;
   - say plainly where the Weave does not reach (Hubble tension, α_s, Λ as an input, w ≥ −1).
2. **The calibrated engine** (`weave_engine`, in aegis_bundle/tools/weave_cm/weave_engine.py) is the same solver as the AEGIS D2134 knob board.
   - **Gate:** it matches CAMB to 8e-5. Its early sound horizons come from a CAMB table with interpolation error < 1e-4.
   - **Reproduction check:** it reproduces the knob board's Dovekie χ² to 0.01.
   - **Modes:**
     - background: H0, w(z), distances;
     - chi2: compressed CMB + DESI DR2 + an SN set;
     - fit: Nelder–Mead.
   - **Data:** C:/Users/Danny/ufe_data/packages/data (the env WEAVE_DATA overrides it).
3. **Data and combinations.**
   - **Sets the engine reads:** DESI DR2 BAO, plus DES-Dovekie or Pantheon+.
   - **Also on the PC:**
     - Planck PR4 CamSpec-NPIPE, Planck 2018 (plik, lowl, lowE), SDSS/eBOSS BAO;
     - the SN sets Pantheon, JLA, DESY5 and Union3.
   - **Results so far:** field_tests/weave_lcdm/*.json, copied into weave_data/lcdm/.
   - **Rule:** the newest data only for scored claims. Older sets are for cross-checks and are labelled as such.
4. **Missions.**
   - M1 Hutter, M2 Ramsey and M3 postulates stay.
   - M3 now cycles the full PRIZE_BOARD.md list (the Clay problems, Beal, Collatz, Erdős, GIMPS/EFF, Hutter and the physics big questions).
   - Postulates are locked and never claimed.
5. **Tools added:**
   - weave_engine;
   - weave_vault.py (real encryption);
   - weave_dials_rng.py (research PRNG, not secure);
   - the Mersenne "vortex" kit (mersenne/).
6. **This file changes every project.** Each new AEGIS result updates WEAVE_FACTS.txt and this brief, with backups kept as *.bak_v5_22nov.
