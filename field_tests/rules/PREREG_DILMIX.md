# PREREG DILMIX — roadmap branch 2, pre-registered: mix the one-power (A) and α′³-square (B) plateaus on E(τ,3/2)

Locked 2026-11-19 before computing (Danny 04:28 "get ahead of calculations").
Motivation (D1479): A gives r 5.6–6.3e-4 (too high once tilted), B gives r 1.2e-4 (too low); a mixture P = α·x/(1+x) + (1−α)·[1 − 1/(1+x)²],
x = E(τ,3/2) − E(ρ,3/2), sits between.
Implementation: pipeline e = P/(1 − P) via the grid mapping (as form B in DILATON32), λ = 1, start by the DILATON32 D1 rule; the tilt
term reads C·g/λ with g = P/(1 − P) (declared approximation, as B). α ∈ {0.25, 0.5, 0.75}; C ∈ {1.25e-6, 2.5e-6}; T_R = 8.94e8.
Rule: "in band" / "near" as PREREG_SMSCAN. Any in-band point ⇒ record (α, C) as the target for the physics question "which
construction gives that mixture". No reruns to chase results; fixes only via PREREG_DILMIX_DEVIATIONS.md written first.
