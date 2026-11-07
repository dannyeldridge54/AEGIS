import json
import math

import pytest

from theory.effective_baseline import Baseline, validate


@pytest.mark.parametrize("first,second", [(0, 0), (1e-4, 0), (0, 1e-4), (-1e-4, 2e-4)])
def test_independent_corrections_and_background_gates(first, second):
    config = Baseline(first_order=first, second_order=second)
    x, step = 0.3, 1e-5
    gradient = (config.potential(x + step)[0] - config.potential(x - step)[0]) / (2 * step)
    assert config.potential(x)[1] == pytest.approx(gradient, rel=1e-7)
    report = validate(config)
    assert report["numerical_gate_passed"] is True
    assert report["max_scaled_field_velocity_shift"] < 1e-7
    assert report["comparison_methods"] == ["RK45", "DOP853"]
    assert report["continuity_sample_count"] > 0
    assert report["max_raychaudhuri_residual"] < 1e-5
    assert report["max_scaled_field_equation_residual"] < 1e-5
    assert report["scientific_baseline_ready"] is False
    json.dumps(report, allow_nan=False)


def test_constant_field_limit_recovers_lambda_background():
    config = Baseline(initial_field=0)
    h2, _ = config.background(0, 0, 0)
    assert h2 == pytest.approx((config.matter_today + config.radiation_today + config.vacuum) / 3)


def test_absent_fluids_do_not_overflow_at_early_epochs():
    from theory.effective_baseline import evolve
    config = Baseline(initial_field=0., matter_today=0., radiation_today=0.,
                      initial_N=-200., final_N=-199.)
    assert config.background(-200., 0., 0.) == pytest.approx((config.vacuum / 3, 0.))
    solution = evolve(config)
    assert tuple(solution.sol(-199.)) == (0., 0.)


@pytest.mark.parametrize("method", ["RK45", "DOP853"])
def test_evolved_lambda_limit_matches_analytic_expansion_and_raychaudhuri(method):
    import numpy as np
    from theory.effective_baseline import evolve
    config = Baseline(initial_field=0, initial_field_prime=0)
    solution = evolve(config, method=method)
    for N in np.linspace(config.initial_N, config.final_N, 101):
        field, prime = solution.sol(N)
        assert field == 0
        assert prime == 0
        matter = config.matter_today * math.exp(-3 * N)
        radiation = config.radiation_today * math.exp(-4 * N)
        expected_h2 = (matter + radiation + config.vacuum) / 3
        expected_epsilon = (3 * matter + 4 * radiation) / (
            2 * (matter + radiation + config.vacuum)
        )
        h2, epsilon = config.background(N, field, prime)
        assert h2 == pytest.approx(expected_h2, rel=1e-12)
        assert epsilon == pytest.approx(expected_epsilon, rel=1e-12)


@pytest.mark.parametrize("kwargs", [{"decay": 0}, {"first_order": math.nan},
                                  {"initial_field_prime": 3}, {"matter_today": -1},
                                  {"final_N": -9}])
def test_invalid_baselines_fail(kwargs):
    with pytest.raises(ValueError):
        Baseline(**kwargs)


@pytest.mark.parametrize("state", [(math.nan, 0, 0), (0, 0, math.inf), (0, 0, 3)])
def test_invalid_background_states_fail(state):
    with pytest.raises(ValueError):
        Baseline().background(*state)


def test_velocity_disagreement_cannot_hide_behind_expansion(monkeypatch):
    import numpy as np
    from types import SimpleNamespace
    from theory import effective_baseline as module
    def fixture(config, **kwargs):
        state = np.array([0.0, 0.0]) if kwargs else np.array([0.0, 1e-6])
        return SimpleNamespace(sol=lambda N: state, t=np.array([config.initial_N, config.final_N]))
    monkeypatch.setattr(module, "evolve", fixture)
    report = module.validate(Baseline(initial_field=0))
    assert report["max_relative_H2_shift"] < 1e-7
    assert report["max_scaled_field_velocity_shift"] > 1e-7
    assert report["numerical_gate_passed"] is False


def test_validation_includes_solver_steps_and_halves_step_limit():
    report = validate(Baseline())
    assert report["sample_count"] > 201
    assert report["maximum_sample_gap_N"] <= report["refined_max_step_N"] * (1 + 1e-12)
    assert report["coarse_max_step_N"] == 2 * report["refined_max_step_N"]


@pytest.mark.parametrize("limit", [0, -1, math.inf, math.nan])
def test_invalid_step_limits_fail(limit):
    from theory.effective_baseline import evolve
    with pytest.raises(ValueError, match="Maximum integration step"):
        evolve(Baseline(), max_step=limit)


def test_nonfinite_expansion_comparison_cannot_pass(monkeypatch):
    import numpy as np
    from types import SimpleNamespace
    from theory import effective_baseline as module
    monkeypatch.setattr(module, "evolve", lambda config, **kwargs: SimpleNamespace(
        sol=lambda N: np.array([0.0, 0.0]),
        t=np.array([config.initial_N, config.final_N])
    ))
    monkeypatch.setattr(module.Baseline, "background", lambda *args: (math.nan, 0))
    with pytest.raises(ValueError, match="Expansion comparison"):
        module.validate(Baseline())


def test_wrong_raychaudhuri_cannot_pass_lambda_limit(monkeypatch):
    original = Baseline.background

    def wrong_derivative(self, *state):
        h2, epsilon = original(self, *state)
        return h2, epsilon + 0.1

    monkeypatch.setattr(Baseline, "background", wrong_derivative)
    report = validate(Baseline(initial_field=0))
    assert report["max_relative_H2_shift"] < 1e-7
    assert report["max_continuity_residual_over_total_density"] == 0
    assert report["max_raychaudhuri_residual"] == pytest.approx(0.2, abs=1e-7)
    assert report["numerical_gate_passed"] is False


def test_common_stalled_field_cannot_pass_conservation_and_solver_agreement(monkeypatch):
    import numpy as np
    from types import SimpleNamespace
    from theory import effective_baseline as module

    config = Baseline()
    monkeypatch.setattr(module, "evolve", lambda config, **kwargs: SimpleNamespace(
        sol=lambda N: np.array([config.initial_field, 0.0]),
        t=np.array([config.initial_N, config.final_N]),
    ))
    report = validate(config)
    assert report["max_relative_H2_shift"] == 0
    assert report["max_scaled_field_velocity_shift"] == 0
    assert report["max_continuity_residual_over_total_density"] == 0
    assert report["max_raychaudhuri_residual"] < 1e-5
    assert report["max_scaled_field_equation_residual"] > 1e-5
    assert report["numerical_gate_passed"] is False


def test_shared_wrong_initial_condition_cannot_pass_exact_lambda_evolution(monkeypatch):
    import numpy as np
    from types import SimpleNamespace
    from theory import effective_baseline as module

    monkeypatch.setattr(module, "evolve", lambda config, **kwargs: SimpleNamespace(
        sol=lambda N: np.array([0.0, 0.0]),
        t=np.array([config.initial_N, config.final_N]),
    ))
    report = validate(Baseline(initial_field=0.5))
    assert report["max_scaled_field_equation_residual"] == 0
    assert report["max_relative_H2_shift"] == 0
    assert report["max_scaled_initial_state_shift"] == 0.5
    assert report["numerical_gate_passed"] is False


@pytest.mark.parametrize("epochs", [
    [-8.0, -1.0], [-7.0, 0.0], [-8.0, 0.0, -1.0],
    [-8.0, -8.0, 0.0], [-8.0, math.nan, 0.0], [-8.0],
])
def test_success_flag_cannot_override_missing_or_invalid_epoch_coverage(monkeypatch, epochs):
    import numpy as np
    from types import SimpleNamespace
    from theory import effective_baseline as module

    monkeypatch.setattr(module, "solve_ivp", lambda *args, **kwargs: SimpleNamespace(
        success=True, sol=lambda N: np.array([0.0, 0.0]),
        y=np.zeros((2, len(epochs))), t=np.array(epochs),
    ))
    with pytest.raises(ValueError, match="requested epoch interval"):
        module.evolve(Baseline(initial_field=0))


def test_background_success_cannot_override_wrong_state_count(monkeypatch):
    import numpy as np
    from types import SimpleNamespace
    from theory import effective_baseline as module
    monkeypatch.setattr(module, "solve_ivp", lambda *args, **kwargs: SimpleNamespace(
        success=True, sol=lambda N: np.zeros(2),
        y=np.zeros((3, 2)), t=np.array([-8., 0.]),
    ))
    with pytest.raises(ValueError, match="requested epoch interval"):
        module.evolve(Baseline())
