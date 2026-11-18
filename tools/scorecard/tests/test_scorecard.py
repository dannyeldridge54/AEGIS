# AEGIS-FP HL2K5YCEAULIJ2CN · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
import math, pytest
from scipy.optimize import brentq
from scipy.integrate import quad
from inflation_scorecard import core
from inflation_scorecard.janus import janus

SERAPIS = core.Model("SERAPIS", (0.970, 0.975), 5e-4, -1.0e-3, -3.8e-5, 0.0587, 3.044)

def by(rows, ds, group=None):
    return next(r for r in rows if r.dataset == ds and (group is None or r.group == group))

def test_reproduces_D710_D711_noncamb():
    rows = core.score(SERAPIS, core.load_constraints())
    assert by(rows, "Planck 2013").pull == pytest.approx(1.33, abs=0.01)
    assert by(rows, "Planck 2018", "n_s by release").pull == pytest.approx(1.21, abs=0.01)
    assert by(rows, "SPA + DESI BAO").pull == 0.0
    assert by(rows, "ACT DR6 (P-ACT-LB)").pull == pytest.approx(-1.38, abs=0.01)
    assert by(rows, "Planck + eBOSS Lya (Rogers & Poulin)").pull == pytest.approx(4.45, abs=0.01)
    assert by(rows, "DESI DR1 Lya P1D + BAO + CMB").pull == pytest.approx(-0.59, abs=0.01)
    assert by(rows, "DESI DR2 + CMB").verdict == "consistent"
    assert by(rows, "DESI DR2 + CMB (Feldman-Cousins)").verdict == "excluded"
    assert by(rows, "ACT DR6", "N_eff").pull == pytest.approx(1.42, abs=0.01)

def test_reproduces_D710_D711_camb():
    pytest.importorskip("camb")
    rows = core.score(SERAPIS, core.load_constraints(), use_camb=True)
    assert by(rows, "eBOSS (via Fairbairn et al.) slope").pull == pytest.approx(6.65, abs=0.05)
    assert by(rows, "DESI DR1 P1D slope").pull == pytest.approx(0.47, abs=0.05)
    assert by(rows, "HSC + BOSS (Luo et al. 2025)").pull == pytest.approx(0.33, abs=0.05)

def test_janus_attractor_limit():
    ns = 0.965; p = math.sqrt(2 / 3)
    r = 2 * ((1 - ns) / p) ** 2          # rho = 1 -> x = 0
    J = janus(ns, r, p, 0.5)
    assert J.x == pytest.approx(0, abs=1e-12)
    assert J.alpha_s == pytest.approx(-(1 - ns) ** 2 / 2)
    assert J.beta_s == pytest.approx(-(1 - ns) ** 3 / 2)

@pytest.mark.parametrize("ns,r,a", [(0.9606, 3.752e-4, -7.872e-4), (0.9662, 4.319e-4, -9.009e-4),
                                    (0.9701, 4.754e-4, -9.880e-4), (0.9746, 4.920e-4, -1.018e-3)])
def test_janus_serapis_e_D692(ns, r, a):
    J = janus(ns, r, 2 * math.sqrt(2), 1.0)          # exact MS points from D692
    assert abs(J.alpha_s / a - 1) < 0.06               # D692: 3.5-5%

@pytest.mark.parametrize("N", [50, 55, 60])
def test_janus_T_model(N):
    V = lambda f: math.tanh(f / math.sqrt(6)) ** 2
    h = 1e-3
    d1 = lambda f: (V(f + h) - V(f - h)) / (2 * h)
    d2 = lambda f: (V(f + h) - 2 * V(f) + V(f - h)) / h ** 2
    d3 = lambda f: (V(f + 2*h) - 2*V(f + h) + 2*V(f - h) - V(f - 2*h)) / (2 * h ** 3)
    eps = lambda f: 0.5 * (d1(f) / V(f)) ** 2
    fe = brentq(lambda f: eps(f) - 1, 0.1, 5)
    fs = brentq(lambda f: quad(lambda x: V(x) / d1(x), fe, f)[0] - N, fe + 0.1, 20)
    e, eta, xi = eps(fs), d2(fs) / V(fs), d1(fs) * d3(fs) / V(fs) ** 2
    ns, r, a = 1 - 6 * e + 2 * eta, 16 * e, 16 * e * eta - 24 * e * e - 2 * xi
    J = janus(ns, r, math.sqrt(2 / 3), 0.0)
    assert abs(J.alpha_s / a - 1) < 0.02               # measured 1.2-1.5% (first-order slow roll)
