import math
from types import SimpleNamespace

import numpy as np
import pytest

from theory import spiral_w as model


def test_coupled_trajectory_conserves_scalar_energy_and_converges():
    V0, baseline, potential = model.closed(1.0, 1.0, 0.15)
    refined, refined_potential = model.solve(V0, 1.0, 1.0, 0.15, rtol=1e-11, atol=1e-13)
    assert baseline.success and refined.success
    assert model.H2_of(baseline, potential, 0)[0] == pytest.approx(1, abs=1e-8)
    for N in np.linspace(-math.log(3.5), -0.001, 40):
        step = 1e-4
        h2, rho, pressure = model.H2_of(baseline, potential, N)
        derivative = (
            model.H2_of(baseline, potential, N + step)[1]
            - model.H2_of(baseline, potential, N - step)[1]
        ) / (2 * step)
        residual = derivative + 3 * (rho + pressure)
        assert abs(residual) / max(abs(rho), 1e-12) < 1e-5
        assert model.H2_of(refined, refined_potential, N)[0] == pytest.approx(h2, rel=1e-7)


def test_effective_report_evaluates_exact_redshift_one(monkeypatch):
    monkeypatch.setattr(model, "_w_chi_eff_at", lambda sol, V, V0, kap, lam, z: z)
    result = model.w_chi_eff_fit(None, None, 1, 1, 1)
    assert result["w_eff_z1"] == 1.0


def test_effective_equation_of_state_rejects_zero_density(monkeypatch):
    monkeypatch.setattr(model, "H2_of", lambda *args: (1, 0, 0))
    sol = SimpleNamespace(sol=lambda N: (0, 0, 0, 0))
    with pytest.raises(ValueError, match="singular denominator"):
        model._w_chi_eff_at(sol, lambda *args: 0, 0, 0, 0, 0)


def test_dense_output_cannot_extrapolate_or_hide_failure():
    sol, potential = model.solve(1.0, 0.0, 0.0, 0.0)
    with pytest.raises(ValueError, match="outside"):
        model.H2_of(sol, potential, 0.01)
    sol.success = False
    with pytest.raises(ValueError, match="failed integration"):
        model.H2_of(sol, potential, 0)


def test_failed_cpl_optimizer_is_not_reported_as_a_fit(monkeypatch):
    monkeypatch.setattr(model, "H2_of", lambda *args: (1, 1, -1))
    monkeypatch.setattr(model, "least_squares",
                        lambda *args, **kwargs: SimpleNamespace(success=False, message="iteration limit"))
    with pytest.raises(ValueError, match="iteration limit"):
        model.cpl_fit(SimpleNamespace(background_densities=(0.3, 9e-5)), None)


@pytest.mark.parametrize("density,redshifts", [(-0.1, [0]), (0.1, [-1]), (0.1, [float("nan")])])
def test_invalid_coupled_background_inputs(density, redshifts):
    with pytest.raises(ValueError):
        model.coupled_exp_w(1, 0, density, 0.2, 1e-4, redshifts)


def test_matter_angle_refuses_unconverged_normalization(monkeypatch, capsys):
    monkeypatch.setenv("MA_GRID", "[[1], [1], [0.1]]")
    sol = SimpleNamespace(sol=lambda N: (0, 0, 0, 1))
    monkeypatch.setattr(model, "closed", lambda *args, **kwargs: (1, sol, None))
    monkeypatch.setattr(model, "H2_of", lambda *args: (1, 1, 0))
    monkeypatch.setattr(model, "cpl_fit", lambda *args: pytest.fail("Unconverged fit"))
    monkeypatch.setattr(model.json, "dump", lambda result, stream, **kwargs: None)
    import io
    monkeypatch.setattr("builtins.open", lambda *args, **kwargs: io.StringIO())
    model.matter_angle()
    assert "clean fits 0" in capsys.readouterr().out
    assert model.OM == 0.30


def test_true_equation_of_state_does_not_divide_zero_density(monkeypatch):
    monkeypatch.setattr(model, "H2_of", lambda *args: (1, 0, 0))
    with pytest.raises(ValueError, match="positive density"):
        model.w_true(None, None)


@pytest.mark.parametrize("h2", [0, -1, float("nan"), float("inf")])
def test_cpl_rejects_invalid_expansion_before_optimization(monkeypatch, h2):
    monkeypatch.setattr(model, "H2_of", lambda *args: (h2, 0, 0))
    monkeypatch.setattr(model, "least_squares", lambda *args, **kwargs: pytest.fail("Invalid optimizer input"))
    with pytest.raises(ValueError, match="finite positive expansion"):
        model.cpl_fit(None, None)


def test_class_mirror_has_no_discarded_slope_search():
    import ast
    from pathlib import Path
    source = Path(model.__file__).with_name("spiral_class_mirror.py")
    tree = ast.parse(source.read_text(encoding="utf-8"))
    calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)
             and isinstance(node.func, ast.Attribute) and node.func.attr == "coupled_exp_w"]
    # Only the same-parameter comparison remains, inside the two-beta loop.
    assert len(calls) == 1
    assert isinstance(calls[0].args[-1], ast.Name) and calls[0].args[-1].id == "ZS"


@pytest.mark.parametrize("h", [0, -1, float("nan"), float("inf")])
def test_invalid_hubble_input_does_not_launch_shooting(monkeypatch, h):
    monkeypatch.setattr(model, "coupled_exp_w", lambda *args: pytest.fail("Invalid shooting input"))
    with pytest.raises(ValueError, match="Hubble parameter"):
        model.class_mu1_guess(1, 0, 0.05, 0.25, 1e-4, h)


def test_ramos_mirror_rejects_failed_independent_integration(monkeypatch):
    import scipy.integrate
    monkeypatch.setattr(scipy.integrate, "solve_ivp",
                        lambda *args, **kwargs: SimpleNamespace(success=False, message="fixture failure"))
    with pytest.raises(ValueError, match="fixture failure"):
        model.mirror_ramos()


def test_trajectory_retains_its_own_cosmology(monkeypatch):
    sol, potential = model.solve(1.0, 0.0, 0.0, 0.0)
    before = model.H2_of(sol, potential, 0)
    fit_before = model.cpl_fit(sol, potential)
    monkeypatch.setattr(model, "OM", 0.8)
    monkeypatch.setattr(model, "ORAD", 0.1)
    assert model.H2_of(sol, potential, 0) == before
    assert model.cpl_fit(sol, potential) == fit_before


def test_small_angle_potential_does_not_round_to_zero():
    _, potential = model.solve(0, 0, 1, 1e-10, F=1)
    angle = 1e-10
    assert potential(0, angle) > 0
    assert potential(0, angle) == pytest.approx(angle**2 / 2, rel=1e-12, abs=0)
    step = angle * 1e-3
    derivative = (potential(0, angle + step) - potential(0, angle - step)) / (2 * step)
    assert derivative == pytest.approx(math.sin(angle), rel=1e-10, abs=0)


def test_background_cannot_mix_coupling_or_potential():
    sol, potential = model.solve(1, 1, 1, 0.15)
    with pytest.raises(ValueError, match="coupling"):
        model.H2_of(sol, potential, 0, lam=0)
    with pytest.raises(ValueError, match="potential"):
        model.H2_of(sol, lambda c, t: 1, 0)


def test_final_closure_integration_failure_is_rejected(monkeypatch):
    successful = SimpleNamespace(success=True)
    failed = SimpleNamespace(success=False, message="final fixture failure")
    calls = iter([successful, successful, failed])
    monkeypatch.setattr(model, "solve", lambda *args, **kwargs: (next(calls), None))
    monkeypatch.setattr(model, "H2_of", lambda *args: (1, 1, -1))
    monkeypatch.setattr(model, "brentq", lambda *args, **kwargs: 1)
    with pytest.raises(ValueError, match="final fixture failure"):
        model.closed(0, 0, 0)


def test_final_closure_residual_is_rechecked(monkeypatch):
    monkeypatch.setattr(model, "solve",
                        lambda *args, **kwargs: (SimpleNamespace(success=True), None))
    values = iter([1, 1, 1.001])
    monkeypatch.setattr(model, "H2_of", lambda *args: (next(values), 1, -1))
    monkeypatch.setattr(model, "brentq", lambda *args, **kwargs: 1)
    with pytest.raises(ValueError, match="Final closure residual"):
        model.closed(0, 0, 0)


@pytest.mark.parametrize("kwargs", [{"dense": False}, {"N1": -1}, {"N1": math.nan}])
def test_closure_rejects_uncheckable_configuration_before_solving(monkeypatch, kwargs):
    monkeypatch.setattr(model, "solve", lambda *args, **kw: pytest.fail("Invalid closure executed"))
    with pytest.raises(ValueError):
        model.closed(0, 0, 0, **kwargs)


def test_explicit_dense_closure_option_does_not_duplicate_keyword():
    _, sol, potential = model.closed(0, 0, 0, dense=True)
    assert model.H2_of(sol, potential, 0)[0] == pytest.approx(1, abs=1e-8)
