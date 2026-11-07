"""The field's theory claims as tests: if an algebra step or a stated number changes, this fails.
Sources: theory/*.py and the Nieh-Yan derivation (the-twist-torsion-cosmology results_notes/NIEH_YAN_PERIOD.md)."""
import math
import os
import sys

import pytest

THEORY = os.path.join(os.path.dirname(__file__), "..", "..", "theory")
sys.path.insert(0, os.path.abspath(THEORY))
sp = pytest.importorskip("sympy")

LAM = -2 * math.sqrt(2 / 3)


def test_kahler_metric_and_lambda():
    P, Pb = sp.symbols("Phi Phibar")
    K = -3 * sp.log(-sp.exp(P + Pb) * (P + Pb) / 3)
    g = sp.simplify(sp.diff(K, P, Pb))
    assert sp.simplify(g - 3 / (P + Pb) ** 2) == 0
    chi = sp.symbols("chi", real=True)
    phi = -sp.exp(sp.sqrt(sp.Rational(2, 3)) * chi)
    resid = g.subs({P: phi, Pb: phi}) - sp.Rational(3, 4) * sp.exp(LAM * chi)
    for c in (-1.3, -0.4, 0.0, 0.7, 1.9):
        assert abs(float(resid.subs(chi, c))) < 1e-12


def test_constant_W_potential_extrema():
    phi = sp.symbols("phi", negative=True)
    V = sp.Rational(81, 2) * (-phi - 1) * sp.exp(-6 * phi) / phi ** 2
    crit = sorted(sp.solve(sp.diff(V, phi), phi))
    assert crit == [sp.Rational(-2, 3), sp.Rational(-1, 2)]
    d2 = sp.diff(V, phi, 2)
    assert d2.subs(phi, sp.Rational(-1, 2)) < 0            # GR point: a maximum
    assert d2.subs(phi, sp.Rational(-2, 3)) > 0            # the minimum


def test_nieh_yan_period_and_F():
    kappa, G = 1.0, 1 / (8 * math.pi)                      # reduced Planck units; l = sqrt(G)
    period = kappa / (math.pi * G)                         # Delta beta = kappa/(pi l^2)
    assert period == pytest.approx(8.0)
    F = math.sqrt(1.5) * period / (2 * math.pi)            # linear Nieh-Yan map phi = sqrt(3/2) beta
    assert F == pytest.approx(4 / math.pi * math.sqrt(1.5))
    assert round(math.log10(F), 3) == 0.193                # the TF-P run name fF0.1930


def test_matter_like_angle_coupling():
    assert -LAM / 2 == pytest.approx(math.sqrt(2 / 3))      # d ln m / d chi = 0.816
    assert 0.073 / (-LAM / 2) == pytest.approx(0.0894, abs=1e-3)   # f bound from Babu-Amendola


def test_F_absorbed_by_dilaton():
    pytest.importorskip("scipy")
    import f_dilaton_degeneracy as d
    out = d.run()
    assert out["verdict"].startswith("DEGENERATE")
    assert max(r["max_diff"] for r in out["cases"]) < 1e-6


def test_dilaton_pinning_values():
    import dilaton_pinning as p
    pts = {x["abs_phi"]: x for x in p.run()["points"]}
    assert pts[1.0]["F_MPl"] == pytest.approx(1.5594, abs=1e-4)
    assert pts[0.5]["F_MPl"] == pytest.approx(4 / math.pi * math.sqrt(6), abs=1e-3)
    assert pts[0.5]["is_extremum_of_V"] and not pts[0.5]["rests_there_with_constant_uplift"]
    assert pts[2 / 3]["rests_there_with_constant_uplift"]


def test_alpha1_inflation_squeeze():
    import alpha1_inflation_squeeze as a
    out = a.run()
    assert 76 < out["N_for_central_ACT_ns"] < 78
    assert out["r_range_1sigma"][0] < 0.002 < out["r_range_1sigma"][1]
