# Accuracy queue (Jl accuracy track; top open item first). Status: open / in progress / done (D###) / retired (D###)

1. [done D807] Referee merge: papers/v3/REFEREE_v3.1_round7_independent.md (agent running since 06:17 CT). Fix valid items via correction notes; add the D806 qualifier (the α_s leg is beyond 2030s reach) to the title/abstract framing. Rebuild. (A0)
1b. [done D808] Referee deferrals: split the ~900-word SERAPIS-E paragraph (minor 10); covariant m₃/₂ window to match wino 0.67–1.85 TeV; extend tab:repro beyond D639 or point to MANIFEST.md; τ = i Σm_ν range 0.059–0.064 clause (minor 9).
2. [done D808] Map hygiene: wino_window title is stale (says 0.67–0.80 TeV, ~15%; current 0.67–1.85 TeV thermal, D784). Fix the map title only (no physics).
3. [done D809] gravitino_wino (estimate) → compute the gravitino→wino yield with the current T_R and m₃/₂ windows, locked. (A1)
4. [done D810] D796 orbit-charge coefficient: the estimate gives ~9Δx, the D790 simulation ~2Δx. Compute η/Δx from the D790 code at 3 small offsets, locked, and settle which is right. (A1)
5. [done D811] D802 additive remnant: compute the no-scale-breaking curvature term at i explicitly (the covariant-completion W₀), locked. (A1)
6. [done D812] Exactness audit: list every n_s/r/α_s in serapis_v3.tex with its source (exact MS / frozen pipeline / slow roll). Recompute any paper number that is slow-roll only, exactly. (A2)
6a. [done D813–D817] MS recomputation: done for D725, D729 (+interpolation), D613 consistency, D722 method; one per tick, locked, via spectra() from exact_ns_d588.py.
6b. [done D820] Literature check: LiteBIRD/SO forecast σ(r) for r ≈ 5e-4 (paper says ~1e-4 needed, beyond plans; sheet says 5e-5 optimistic). Fix whichever is wrong.
7. [done D821] Error budget for the frozen τ = i band and SERAPIS-E band: N* (reheating range), exact vs SR, parameter window, convention. Table in the prediction sheet. (A3)
8. [done D822] Prune: logderiv_plateau (no string source, D760) → retire unless a unique prediction is found; SERAPIS-Δ (D800, disfavoured) → record as retired. (A4)
9. [done D823] eps_tilt at τ = i: state that it is fitted; check whether a BHK-type tilt can exist on the τ = i branch (D802 says multiplicative, so no vacuum mass, but a tilt?). Derive or record "not derivable". (A1)
10. [deep, needs Danny's OK] P3 anti-D3 annulus computation.
Not derivable (tests only): P1 CP phases (DUNE/Hyper-K), halo_profile (astrophysics).
