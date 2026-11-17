# PREREG A5b — spherical Jeans dispersions (Hyperion roadmap A5, Djl D) — locked 2026-11-17
Code (written after this lock): tools/janus_astro/jeans.py; check theory/janus_astro/a5b_check.py.
Method: σ_r²(r) = [ν(r) r^{2β}]⁻¹ ∫_r^∞ ν(r') r'^{2β} G M(r')/r'² dr' (spherical Jeans, constant β; Binney & Tremaine 2008 §4.8).
Our side uses analytic enclosed masses and our own quadrature, not galpy forces. Units: G = 1 (galpy natural units).
Referee: galpy 1.12.1 galpy.df.jeans.sigmar (natural units ro = vo = 1).
Cases: potential NFW (amp 1, a 1) or Hernquist (amp 1, a 1; galpy M(r) = (amp/2) x²/(1+x)²). Tracers: the self-consistent density (dens=None) or a Hernquist tracer with a = 0.5. β ∈ {0, 0.5}. r ∈ {0.1, 0.5, 1, 3, 10}.
- T1: max |σ_r(ours)/σ_r(galpy) − 1| ≤ 1e-5 over all cases.
- T2 (exact): point mass M = 1 with power-law tracer ν ∝ r^-γ, γ ∈ {3, 3.5}, β ∈ {0, 0.5}. σ_r² = GM/((γ + 1 − 2β) r), checked to ≤ 1e-6 relative at r = 0.3, 1, 5.
- R (reported): a Milky Way NFW halo (galpy MWPotential2014 halo component spherical part only) σ_r at 8 kpc for a Hernquist tracer. This is not scored.
A5b VALIDATED iff T1 and T2 pass. Fixes only via DEVIATIONS before any rerun.
