import json
import math

import numpy as np
import pytest

from theory.effective_baseline import Baseline
from theory.effective_modes import evolve_mode, validate_mode


@pytest.mark.parametrize("c1,c2", [(0., 0.), (1e-4, -2e-4), (-1e-4, 2e-4)])
@pytest.mark.parametrize("field", [0.1, 0.7, 2.0])
def test_curvature_matches_independent_gradient_difference(c1, c2, field):
    config = Baseline(first_order=c1, second_order=c2, decay=.8)
    step = 1e-5
    expected = (config.potential(field + step)[1] - config.potential(field - step)[1]) / (2 * step)
    assert config.potential_curvature(field) == pytest.approx(expected, rel=1e-7, abs=1e-9)


def test_n3_minimum_and_hilltop_curvature():
    config = Baseline()
    assert config.potential_curvature(0) == 0
    assert config.potential_curvature(math.pi * config.decay) == pytest.approx(
        -12 * config.amplitude / config.decay**2
    )


@pytest.mark.parametrize("method", ["RK45", "DOP853"])
def test_de_sitter_massless_zero_k_mode_matches_exact_decay(method):
    config = Baseline(initial_field=0., matter_today=0., radiation_today=0.,
                      initial_N=-2., final_N=0.)
    sol = evolve_mode(config, 0., 2., .3, method=method)
    epochs = np.linspace(-2., 0., 101)
    delta = epochs - config.initial_N
    np.testing.assert_allclose(sol.sol(epochs)[0], 2 + .1 * (1 - np.exp(-3 * delta)),
                               rtol=1e-9, atol=1e-10)
    np.testing.assert_allclose(sol.sol(epochs)[1], .3 * np.exp(-3 * delta),
                               rtol=1e-8, atol=1e-10)


def test_hilltop_zero_k_growth_matches_analytic_constant_mass():
    config = Baseline(initial_field=math.pi, matter_today=0., radiation_today=0.,
                      initial_N=-1., final_N=0.)
    h2, _ = config.background(-1., math.pi, 0.)
    mass_ratio = config.potential_curvature(math.pi) / h2
    growth = (-3 + math.sqrt(9 - 4 * mass_ratio)) / 2
    sol = evolve_mode(config, 0., 1., growth)
    assert sol.sol(0.)[0] == pytest.approx(math.exp(growth), rel=1e-8)
    assert sol.sol(0.)[0] > 1


@pytest.mark.parametrize("k", [0.5, 3.0])
@pytest.mark.parametrize("method", ["RK45", "DOP853"])
def test_finite_k_de_sitter_mode_matches_exact_wave(k, method):
    config = Baseline(initial_field=0., matter_today=0., radiation_today=0.,
                      initial_N=-1., final_N=0.)
    hubble = math.sqrt(config.vacuum / 3)
    initial_x = k * math.exp(-config.initial_N) / hubble
    initial = math.cos(initial_x) + initial_x * math.sin(initial_x)
    initial_prime = -initial_x**2 * math.cos(initial_x)
    sol = evolve_mode(config, k, initial, initial_prime, method=method)
    epochs = np.linspace(-1., 0., 101)
    x = k * np.exp(-epochs) / hubble
    np.testing.assert_allclose(sol.sol(epochs)[0], np.cos(x) + x * np.sin(x),
                               rtol=1e-7, atol=1e-8)
    np.testing.assert_allclose(sol.sol(epochs)[1], -x**2 * np.cos(x),
                               rtol=1e-7, atol=1e-7)


def test_mode_convergence_does_not_claim_full_stability():
    report = validate_mode(Baseline(initial_N=-2.), .5)
    assert report["numerical_gate_passed"] is True
    assert report["max_scaled_mode_equation_residual"] < 1e-5
    assert report["max_scaled_initial_mode_shift"] < 1e-10
    assert report["mode_equation_sample_count"] > 0
    assert report["full_stability_established"] is False
    assert report["scientific_baseline_ready"] is False
    json.dumps(report, allow_nan=False)


@pytest.mark.parametrize("kwargs", [
    {"k_over_Href": -1}, {"k_over_Href": math.inf},
    {"k_over_Href": 0, "initial_mode": math.nan},
    {"k_over_Href": 0, "max_step": 0},
])
def test_invalid_mode_inputs_rejected(kwargs):
    with pytest.raises(ValueError):
        evolve_mode(Baseline(), **kwargs)


@pytest.mark.parametrize("wrong_state", [(0., 0.), (1., 0.)])
def test_shared_wrong_mode_cannot_pass_agreement(monkeypatch, wrong_state):
    from types import SimpleNamespace
    from theory import effective_modes as modes
    config = Baseline(initial_field=0., initial_N=-1., matter_today=0.,
                      radiation_today=0.)
    background = modes.evolve(config)

    def fake(*args, **kwargs):
        return SimpleNamespace(
            sol=lambda N: np.tile(np.array(wrong_state)[:, None], (1, np.asarray(N).size))
            if np.asarray(N).ndim else np.array(wrong_state),
            t=np.array([-1., 0.]), background=background,
        )

    monkeypatch.setattr(modes, "evolve_mode", fake)
    report = modes.validate_mode(config, 1.)
    assert report["max_scaled_mode_state_shift"] == 0
    if wrong_state[0] == 0:
        assert report["max_scaled_initial_mode_shift"] == 1
    else:
        assert report["max_scaled_mode_equation_residual"] > 1e-5
    assert report["numerical_gate_passed"] is False


@pytest.mark.parametrize("epochs,shape", [
    ([], (2, 0)), ([-1.], (2, 1)), ([-1., 0.], (3, 2)),
    ([-1., -.5, -.75, 0.], (2, 4)),
    ([-1., -.5, -.5, 0.], (2, 4)),
    ([-1., math.nan, 0.], (2, 3)),
    ([-1., -.1], (2, 2)),
])
def test_mode_success_cannot_override_malformed_output(monkeypatch, epochs, shape):
    from types import SimpleNamespace
    from theory import effective_modes as modes
    config = Baseline(initial_N=-1.)
    background = modes.evolve(config)
    monkeypatch.setattr(modes, "evolve", lambda *args, **kwargs: background)
    monkeypatch.setattr(modes, "solve_ivp", lambda *args, **kwargs: SimpleNamespace(
        success=True, t=np.array(epochs), y=np.zeros(shape),
        sol=lambda N: np.zeros(2),
    ))
    with pytest.raises(ValueError, match="full-interval output"):
        modes.evolve_mode(config, .5)
