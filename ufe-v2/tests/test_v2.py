"""Acceptance tests for AEGIS UFE v2. Run: python -m pytest tests/test_v2.py  (or python tests/test_v2.py)"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from aegis.cosmo_v2 import LCDM, LegacyBeta, TorsionField, derived
from scipy.integrate import quad

def test_flatness_exact():
    for m in [LCDM(0.70, 0.12), LegacyBeta(0.70, 0.12, 0.2, 0.5), TorsionField(0.73, 0.144, 8.92, 0.214)]:
        assert abs(m.E(np.array([1.0]))[0] - 1) < 1e-12, m.name

def test_planck_baseline():
    d = derived(LCDM(0.6736, 0.1200))
    assert abs(d["rs"] - 144.27) < 0.02 and abs(d["rd"] - 147.10) < 0.02
    assert abs(d["DCs"] - 13894.4) < 1.0

def test_distance_accuracy_vs_quad():
    m = LCDM(0.6736, 0.12); d = derived(m)
    ex = 2997.92458 / m.h * quad(lambda z: 1 / m.E(np.array([1 / (1 + z)]))[0], 0, d["zs"], limit=500)[0]
    assert abs(d["DCs"] / ex - 1) < 1e-5            # 30x tighter than Planck's theta* error

def test_field_reproduces_paper():
    m = TorsionField(0.728, 0.14408, np.log10(8.3457e8), 0.2139)
    d = derived(m)
    assert abs(m.f - 0.183) < 0.002 and abs(m.zc - 3540) < 20
    assert abs(d["rs"] - 133.48) < 0.05 and abs(m.w_late - 0.5) < 0.02

def test_field_screened_at_bbn():
    m = TorsionField(0.728, 0.144, 8.92, 0.214); a = 2.35e-10
    frac = m.extra(np.array([a]))[0] / (m.wm / a**3 + 9.34e-5 * 0.6736**2 / a**4)
    assert frac < 1e-20

def test_lcdm_limit():
    """v0 -> 0 switches the torsion field off and must recover LCDM."""
    m0 = derived(LCDM(0.70, 0.13)); m1 = derived(TorsionField(0.70, 0.13, -2.0, 0.2))
    assert abs(m1["rs"] / m0["rs"] - 1) < 1e-8

def test_late_release_stays_flat():
    """A field released late (dark-energy-like regime) must still give E(a=1) = 1 and finite distances."""
    m = TorsionField(0.70, 0.13, 4.0, 0.2); d = derived(m)
    assert abs(m.E(np.array([1.0]))[0] - 1) < 1e-12 and np.isfinite(d["DCs"])

def test_legacy_constant_beta_is_matter_rescaling():
    """v1 constant-beta model is exactly LCDM with omega_m -> omega_m (1+beta): no new physics."""
    b = 0.2; m1 = LegacyBeta(0.70, 0.12, b, 0.0); wm_eff = (0.12 + 0.02237) * (1 + b)
    m0 = LCDM(0.70, wm_eff - 0.02237)
    a = np.logspace(-6, 0, 50)
    assert np.allclose(m1.E(a), m0.E(a), rtol=1e-12)

def test_star_scanner_coordinates():
    """ICRS -> Galactic transform against IAU reference points."""
    from aegis.star_scanner import to_galactic
    l, b, _ = to_galactic(266.40499, -28.93617)          # Galactic Centre
    assert min(l, 360 - l) < 1e-3 and abs(b) < 1e-3
    l, b, _ = to_galactic(269.4520, 4.6934)              # Barnard's star (l 31.0087, b 14.0628)
    assert abs(l - 31.0087) < 1e-3 and abs(b - 14.0628) < 1e-3

def test_star_scanner_confirmation_and_flags():
    from aegis.star_scanner import assess
    ok = assess(dict(source_id="1", ra=10, dec=20, parallax=10, parallax_error=0.1, pmra=5, pmdec=5, radial_velocity="",
                     phot_g_mean_mag=12, bp_rp=0.8, ruwe=1.0, r_med_geo=100, r_lo_geo=99, r_hi_geo=101))
    assert ok["confirmed"] and ok["flags"] == ""
    fast = assess(dict(source_id="2", ra=10, dec=20, parallax=1, parallax_error=0.05, pmra=100, pmdec=60, radial_velocity="",
                       phot_g_mean_mag=15, bp_rp=1.0, ruwe=1.1, r_med_geo=1000, r_lo_geo=960, r_hi_geo=1040))
    assert "high_velocity" in fast["flags"]

if __name__ == "__main__":
    for k, f in list(globals().items()):
        if k.startswith("test_"):
            f(); print("PASS", k)
