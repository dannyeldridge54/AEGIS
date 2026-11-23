# Overnight plan (Danny 01:17: "Messenger chill ... once this is fully tested fit ping loop negative space then full ping pong derivatives make emu and everything. Im going to bed")
Messaging: quiet. SendUserMessage only for a verdict-class result (a locked test scored) or a failure needing him; otherwise record in D-notes and push.
Phase 1 — finish the fits (score each by its lock, D-note, push): ACT pair (D2151), C_union3_camspec (D2135), D2169 tight pair, then launch D2177 SPT best-of-4 on the PC.
Phase 2 — fit ping loop + negative space: builder/referee ping-pong over all scored fits (Planck HiLLiPoP/CamSpec, SPT, ACT): where does each χ² piece come from, what does each CMB set forbid (negative-space walls), is the not-CMB-robust split explained by the fixed n_s on high-ℓ data. Until a NULL round.
Phase 3 — D2173 emulator race on the PC (OLE vs loom_fast) on HiLLiPoP+Pantheon+; adopt the passer; then build the local Cl emulator (A1 item c) under a new lock.
Phase 4 — full ping-pong derivations on the queue: D2161 full-Planck neutrino; α_s thresholds; hypercharge+coupling brane scan; dark photon mass/mixing; Higgs Θ/V0 + top Yukawa; O6 displacement of the hidden U(1). Each locked first, refereed, until NULL.
Paper v2 is NOT published without Danny's word: prepare it (D2176a correction + SPT/ACT + D2172), leave as draft.
Rules: lock before computing; DEVIATIONS before reruns; no reruns to chase; never kill or relaunch a PC job without checking its launch log first (D2151 DEV-1 lesson).

Update 01:26 CT (Danny: "Forget prize stuff"): all prize work dropped from this plan and the queue — no Mersenne/GIMPS, Hutter, Beal or other prize items. D2174/D2175 stay recorded as done; no follow-ups. Focus: the Weave fits, ping-pong/negative space, emulator, UFE derivations.
Also: D2169 tight pair will hit its 7000 s cloud timeout (~02:24 CT) still on start 1/4. Write PREREG_D2169 DEVIATIONS (move to PC, no timeout) BEFORE any rerun; no result has been seen.

Update 01:31 CT (Danny: "Before neg space ... schedule these all, fold into 1 run"): NEW PHASE 1b = D2178 battery (one lock, one driver tools/battery/run_battery.py, one report). Order T1 profile u_i → T2 freed inputs → T3 Planck+ACT+SPT → T4 growth → T5 GoF → T6 BBN → T8 forecasts → T7 MCMC/evidence (only after D2173 passes). Runs before Phase 2 (negative space). T5/T6 are cheap (from existing best fits) — do them in the cloud right away.

Update 06:12 CT: OLE parked (D2173 DEV-2: dependency clash). Danny 06:10 "Test sweep after": T1 u_i profile sweep (9 grid pts × HiLLiPoP+Dovekie and SPT+Dovekie) runs on the PC as soon as D2177/D2169 free cores, using weave_lcdm_pr4c.py / weave_extcmb4.py with FIX_UI and LOOM_WARM warm starts from each pair's free W best fit (same prior box; allowed by D2173 A1). Our own local Cl emulator (A1 item c) is built after the sweep, not before.
