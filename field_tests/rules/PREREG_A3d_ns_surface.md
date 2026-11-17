# PREREG A3d — neutron-star surface: well-posed cross-code check (Djl D) — locked 2026-11-17
Follows A3b and A3c, which were NOT VALIDATED only on N4 (radii 1.0e-6 to 1.1e-5 apart).
Diagnosis: at P → 0 the surface radius is ill-conditioned. dP/dr → 0 as ρ → 0, so each integrator's event location carries its own tolerance error. That is a property of the surface definition, not a physics difference.
Code change, made with this lock: compact.tov gains p_surf (default 0.0, so earlier behaviour is unchanged); the event becomes P = p_surf.
Test N4′:
- Stop both codes at the same finite surface, ρ_surf = 1e4 g/cm³. This is ns.tov_tidal's default convention, an outer-crust density, labelled CONVENTION.
- compact.tov uses p_surf = P_SLy(ρ_surf) from the same crust polytrope piece.
- Grid: SLy, log ρ_c = 14.8, 15.0, 15.2 (the A3c grid).
- Pass: M and R relative differences ≤ 1e-7.
Reported: the surface sensitivity R(ρ_surf → 1e-3) − R(ρ_surf = 1e4), in metres, for each star (ns code).
A3d VALIDATED iff N4′ passes. Together with A3c's N1–N3, the NS module is then validated. Fixes only via DEVIATIONS.
Script: theory/janus_astro/a3d_check.py (written after this lock).
