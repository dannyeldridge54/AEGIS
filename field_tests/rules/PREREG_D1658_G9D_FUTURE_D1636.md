# PREREG_D1658_G9D_FUTURE_D1636 — the dark thread's future from the full-likelihood best fits (Janus genesis G9d; locked 2026-11-19 ~23:30Z before any number)
Inputs (read-only, other chat's D1636): field_tests/results/D1636/rt10_{pantheonplus,union3,desy5}.json — best u_i (= A e^{−βφ_i} on the ASYMPTOTIC curve, PREREG_D1636_rt_full_likelihood), Ω_m ("Om"), CPL w₀.
Model: D1653's 2D exact-shape code (g9b_tau_plane.py, unchanged) with Ω_m set per dataset. Two starts per dataset:
 (a) same-u: amp = u_i on the exact curve;
 (b) matched: amp chosen on a 16-point log grid in [0.03, 0.36] (exact curve, x = ½) and linearly interpolated so the exact-curve CPL w₀ (a ∈ [1/3, 1]) equals D1636's w₀.
Each start run at δx = 0 and δx = 1e-3 to a = 50.
Outputs: CPL (w₀, w_a); a where acceleration ends (or "none by a = 50"); end class (i / ρ / other, D1653 rule); late ⟨w⟩.
Reading (locked, descriptive): "acceleration still ends" if every matched run has an end of acceleration by a = 50; report the range of a_end; "end point" = classes of the matched runs. No pass/fail; this updates D1644/D1655 to the full-likelihood starts.
Script: field_tests/scripts/janus_g/g9d_future_d1636.py → field_tests/results/D1658_G9d_future_d1636.json
