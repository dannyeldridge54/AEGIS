# PREREG D1405 — Janus relation, any κ: closed form α_s = −½(1−n_s)²ρ[1+κ(ρ−1)], sign rule, and band_i at its own κ = ½

Locked 2026-11-19 (UTC) before computing (JANUS tick 5, node janus; also the D1402a correction).
Hand algebra from D669's relation (x = (ρ−1)/(1+κρ)): 1+x = ρ(1+κ)/(1+κρ), 1+κ²x = (1+κ)(1−κ+κρ)/(1+κρ),
1−κx = (1+κ)/(1+κρ) ⇒ α_s = −½(1−n_s)²·ρ·[1 + κ(ρ−1)]. κ = 1 recovers D1399's −p²r/4.
  R1 closed form: PASS if max |code/closed − 1| < 1e-10 over n_s 0.968–0.976, r 4–6e-4, κ ∈ {0.25, 0.5, 1, 2}, p = 2.8284.
  R2 sign (for κ > 0, the physical range κ = q/p): α_s ≥ 0 iff ρ < 1 and κ ≥ 1/(1−ρ). Report ρ over both bands; if ρ > 1
     everywhere, the relation forbids positive running for any κ > 0 — a sharp, falsifiable statement (PASS = derived and
     confirmed numerically by scanning κ ∈ [0.01, 10]).
  R3 correction D1402a: band_i (τ = i, own κ = ½ per D1263) n_s 0.970–0.975, r 4.8–5.7e-4, α_s on a 41×41 grid with κ = ½;
     pulls vs ACT DR6 P-ACT-LB 0.0062 ± 0.0052. PASS if all |pull| < 2. Relation error at τ = i is 10.8 % (D1263) — stated.
No reruns to chase results; fixes only via PREREG_D1405_DEVIATIONS.md written first.
