# PREREG D404 — bridge 4: reionization-to-recombination birefringence ratio (locked 14:35 CT 14 Nov 2026, before running)

For a single thawing axion that is both dark energy and the birefringence field (Twist-2 variant, D393/D403), the large-angle
(reionization, z_re ~ 7–10) and small-angle (recombination, z = 1089) polarisation rotations share the same field history, so their
ratio ρ_β = β_reio/β_rec is free of c_γ and θ_i to the extent the field is frozen before z_re.
Script: theory/twist2/bridge4_d404.py (locked D393 integrator), grid f ∈ {0.5, 1, 2} M_P, θ_i ∈ {0.3, 0.5, 1.0, 1.5}, z_re ∈ {7, 8, 10}.
Prediction stated as: ρ_β = 1 − ε with ε the largest grid value of 1 − ρ_β (theory band [1 − ε, 1]).
Reading/scoring: any future measurement of β from the reionization bump (ℓ ≲ 10) and from ℓ ≳ 100 with ρ_β outside [1 − ε − 2σ, 1 + 2σ] puts the
single-axion variant OUT OF BALANCE (it would point to a field that moved before reionization, e.g. an early axion). If a current
measurement exists it is scored the same way; if only limits exist, they are reported, not scored.
No reruns; fixes via a DEVIATIONS file written first.
