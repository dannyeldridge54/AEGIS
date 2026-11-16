# PREREG D810: orbit-charge coefficient η/Δx with the correct local coordinate (accuracy queue item 4; Jl tick 49)
Locked before computing, 2026-11-16.
Problem: D790 read the charge with w centred at ρ = (½, √3/2), but some runs settle at another image of ρ (e.g. (½, 0.2887)). Those read-outs (x₀ = 0.499, 0.49) are invalid (D790/D791). The valid ones (x₀ = 0.45 → η = −0.103, x₀ = 0.40 → +0.199) gave |η| ≈ 2Δx with opposite signs. The D796 estimate gave ~9Δx.
Method: import V, rhs, rho_tot and the inflation stage unchanged from theory/modular/inflaton_ad_d790.py. Re-implement only the read-out:
- the centre c = the image of ρ nearest the field's final position (images of ρ under SL(2,Z) words with entries |·| ≤ 3);
- w = (τ − c)/(τ − c̄); χ = √2|w| (Möbius-invariant normalisation);
- η = 2⟨Im(w̄ ẇ)⟩/(⟨ρ⟩/m), averaged over the last 30 time units before ρ_tot = 1e-4 V_end, as in D790.
Runs: x₀ = 0.48, 0.45, 0.40 (Δx = 0.02, 0.05, 0.10) and the mirror x₀ = 0.55 (CP check: η must flip sign versus 0.45).
Outputs: η, the centre c, η/Δx.
Expectations (pre-stated):
- (i) the mirror check holds (η(0.55) = −η(0.45) within 5%);
- (ii) |η|/Δx lies between 1 and 10;
- (iii) the sign is not monotonic in Δx (the orbit winds), so |η| ≈ k|Δx| is the meaningful statement.
Verdict: report k = median |η|/Δx and decide between D790's ~2 and D796's ~9. Wall time cap 15 min; if exceeded, report the completed runs. No reruns; fixes go in DEVIATIONS first.
