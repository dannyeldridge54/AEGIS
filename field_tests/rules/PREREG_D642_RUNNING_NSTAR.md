# PREREG D642 (W4): running α_s at the paper's N* bracket (46.1–49.2)
Locked before computation, 2026-11-15. Script theory/modular/running_nstar_d642.py = running_d632.py lines 1–41 verbatim (exec) + a loop over ε ∈ {0, 1.3e-4, 1.6e-4} and N* ∈ {46.08, 49.21} (D602 bracket ends). Same finite-difference stencil as D632. Output results/running_nstar_d642.txt.
Report n_s, α_s, ratio to −(1−n_s)²/2. The Chronos α_s band in the paper becomes [min, max] over ε ∈ {1.3, 1.6}e-4 and these N*. Lock D633 is NOT changed; the paper will report both. No reruns.
