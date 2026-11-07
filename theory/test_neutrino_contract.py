import math

import pytest

from theory.neutrino_contract import neutrino_radiation_adiabatic_contract as contract


def at_tau(rnu, k, tau, psi=1e-5):
    """Dimensional MB-convention quantities (theta, sigma) for fixed k."""
    mode = contract(rnu, k * tau, primordial_psi=psi)
    return mode, mode["theta_over_calH"] / tau, mode["sigma_nu"]


@pytest.mark.parametrize("rnu", [0., .1, .405, .9])
def test_traceless_einstein_equation_is_exact_at_leading_order(rnu):
    kt = 3e-3
    m = contract(rnu, kt, primordial_psi=2e-5)
    # k^2(phi-psi) = (3/2) a^2 (4/3) rho_nu sigma, a^2 rho_nu = 3 Rnu / tau^2
    lhs = kt**2 * (m["phi"] - m["psi"])
    rhs = 1.5 * (4 / 3) * 3 * rnu * m["sigma_nu"]
    assert lhs == pytest.approx(rhs, rel=1e-12, abs=1e-30)


@pytest.mark.parametrize("rnu", [0., .2, .6])
def test_momentum_constraint_and_matter_velocity(rnu):
    kt, psi = 2e-3, 1e-5
    m = contract(rnu, kt, primordial_psi=psi)
    # k^2 calH psi = (1/2)*(4/3)*3*theta_r/calH*calH^3 with theta_nu=theta_gamma
    assert kt**2 * psi == pytest.approx(2 * m["theta_over_calH"], rel=1e-12)


@pytest.mark.parametrize("rnu", [0., .3, .8])
def test_velocity_and_shear_evolution_equations_at_leading_order(rnu):
    k, tau, psi, h = 1.0, 4e-3, 1e-5, 1e-6
    d = lambda f: (f(tau + h) - f(tau - h)) / (2 * h)
    theta = lambda t: at_tau(rnu, k, t, psi)[1]
    sigma = lambda t: at_tau(rnu, k, t, psi)[2]
    m, th, sg = at_tau(rnu, k, tau, psi)
    # theta' = k^2 (delta/4 + psi - sigma): sigma term is O(k^4 tau^2), neglected
    assert d(theta) == pytest.approx(k**2 * (m["delta_nu"] / 4 + m["psi"]), rel=1e-8)
    # sigma' = (4/15) theta_nu
    assert d(sigma) == pytest.approx(4 * th / 15, rel=1e-8)
    # dust: theta_m' = -calH theta_m + k^2 psi with calH=1/tau
    assert d(theta) == pytest.approx(-th / tau + k**2 * psi, rel=1e-8)


def test_density_constraint_residual_is_order_k_tau_squared():
    rnu, psi = .4, 1e-5
    residual = []
    for kt in (4e-3, 2e-3):
        m = contract(rnu, kt, primordial_psi=psi)
        # tau^2*(k^2 phi + 3calH(calH psi) + a^2 delta rho/2), a^2 rho=3/tau^2
        rho_delta = 3 * m["delta_gamma"]
        residual.append(abs(kt**2 * m["phi"] + 3 * m["psi"] + rho_delta / 2))
    assert residual[0] / residual[1] == pytest.approx(4, rel=1e-9)
    assert residual[0] < 1e-9


def test_vanishing_neutrinos_reproduce_perfect_radiation_initializer():
    from theory.effective_baseline import Baseline
    from theory.coupled_perturbations import radiation_adiabatic_initial_state
    config = Baseline(initial_N=-14., matter_today=0., vacuum=0.,
                      initial_field=0., initial_field_prime=0., radiation_today=1e-4)
    k = 1.0
    x = k * math.exp(config.initial_N) / math.sqrt(config.radiation_today)
    state = radiation_adiabatic_initial_state(config, k, primordial_phi=1e-5)
    m = contract(0., math.sqrt(3) * x, primordial_psi=1e-5)
    assert m["phi"] == m["psi"] and m["sigma_nu"] * 0 == 0
    assert state[6] == pytest.approx(m["phi"], rel=x**2)
    assert state[4] == pytest.approx(m["delta_gamma"], rel=x**2)
    assert state[5] == pytest.approx(m["theta_over_calH"], rel=x**2)
    assert state[2] == pytest.approx(m["delta_matter"], rel=x**2)


def test_known_ratio_and_rejections():
    m = contract(.405, 1e-3)
    assert m["phi"] / m["psi"] == pytest.approx(1 + .162)
    for args in ((-.1, 1e-3), (1., 1e-3), (.2, 0.), (.2, .02), (float("nan"), 1e-3),
                 (.2, float("inf"))):
        with pytest.raises(ValueError):
            contract(*args)
    for psi in (0., 2e-3, float("nan")):
        with pytest.raises(ValueError):
            contract(.2, 1e-3, primordial_psi=psi)
