# PREREG A8b (track X, Hyperion -> Star Mapper; manual Djl 17 Nov 06:22 CT): Gaia's own ICRS->Galactic convention (written before running)
Source (fetched): Gaia DR3 documentation §4.1.7 (gea.esac.esa.int, ssec_cu3ast_intro_tansforms), Eq. 4.62 matrix A_G' to 16 decimals, and the DEFINING angles α_G = 192.85948°, δ_G = +27.12825°, l_Ω = 32.93192° ("should be regarded as exact"; the matrix is derived from them).
Consequence for A8a/D1071: mapper_feed's constants (192.85948, 27.12825, l_NCP = 122.93192 = l_Ω + 90) ARE the exact Gaia/Hipparcos definition, so D1071's "rounded constants" diagnosis is wrong (correction D1071a); the 7e-6 deg offset is astropy's different realisation of the Galactic frame, not a Hyperion error.
Code: tools/janus_astro/mapper_feed.py unchanged. Script theory/janus_astro/a8b_check.py (never run before this lock).
Tests:
G1 mapper_feed.T_ICRS_GAL vs Gaia A_G' (all 9 elements): max |Δ| ≤ 1e-12.
G2 (l, b) for the 200 A8a synthetic stars (seed 2026) vs (l, b) computed with A_G' directly: ≤ 1e-9 deg.
G3 geometry: a star at the Sun's position (d → 0) with zero heliocentric velocity maps to the Sun's Galactocentric position (x = −√(R0² + z²) rotated, z = z_sun) and velocity V_SUN: ≤ 1e-12 kpc, 1e-9 km/s; and the Galactic Centre direction (l = 0, b = 0 converted to ICRS with A_G'ᵀ, d = √(R0² + z_sun²)) maps to the origin: ≤ 1e-12 kpc.
Pass G1–G3 → A8b VALIDATED (coordinates follow Gaia's convention exactly).
Reported (not scored): the astropy offsets in (l, b) and in Galactocentric position/velocity for the 200 stars.
Output field_tests/results/janus_astro_a8b.txt. No reruns to chase; DEVIATIONS first.
