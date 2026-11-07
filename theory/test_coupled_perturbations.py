import numpy as np
import pytest

from theory.effective_baseline import Baseline, evolve
from theory.coupled_perturbations import equations


def test_zero_perturbations_remain_zero():
    config = Baseline(initial_N=-2)
    background = evolve(config)
    rhs, constraint = equations(config, background, -1, np.zeros(7), .5)
    np.testing.assert_array_equal(rhs, np.zeros(7))
    assert constraint == 0


def test_absent_fluids_do_not_overflow_in_early_coupled_equations():
    config = Baseline(initial_field=0., matter_today=0., radiation_today=0.,
                      initial_N=-200., final_N=-199.)
    background = evolve(config)
    rhs, constraint = equations(config, background, -200., np.zeros(7), 1e-90)
    np.testing.assert_array_equal(rhs, np.zeros(7))
    assert constraint == 0


@pytest.mark.parametrize("epochs,shape", [
    ([], (7, 0)), ([[-1., 0.]], (7, 2)), ([-1., 0.], (6, 2)),
    ([-1., -.5, -.5, 0.], (7, 4)), ([-1., float("nan"), 0.], (7, 3)),
    ([-1., -.1], (7, 2)),
])
def test_coupled_success_cannot_override_malformed_output(monkeypatch, epochs, shape):
    from types import SimpleNamespace
    from theory import coupled_perturbations as coupled
    config = Baseline(initial_N=-1.)
    background = evolve(config)
    monkeypatch.setattr(coupled, "evolve", lambda *args, **kwargs: background)
    monkeypatch.setattr(coupled, "solve_ivp", lambda *args, **kwargs: SimpleNamespace(
        success=True, t=np.array(epochs), y=np.zeros(shape), sol=lambda N: np.zeros(7),
    ))
    with pytest.raises(ValueError, match="full-interval output"):
        coupled.integrate(config, np.zeros(7), .5)


def test_coupled_equations_cannot_mix_background_actions():
    config = Baseline(initial_N=-2)
    background = evolve(config)
    other = Baseline(initial_N=-2, amplitude=3.)
    with pytest.raises(ValueError, match="does not match"):
        equations(other, background, -1, np.zeros(7), .5)


@pytest.mark.parametrize("N,k", [(-1.5, .2), (-1., 1.), (-.5, 3.)])
def test_einstein_constraint_is_preserved_by_coupled_equations(N, k):
    config = Baseline(initial_N=-2)
    background = evolve(config, method="DOP853", rtol=1e-12, atol=1e-14)
    state = np.array([.01, -.02, 0., .003, .005, -.004, .001])
    _, residual = equations(config, background, N, state, k)
    h2, _ = config.background(N, *background.sol(N))
    matter_over_h2 = config.matter_today * np.exp(-3 * N) / h2
    state[2] = -2 * residual / matter_over_h2
    rhs, constraint = equations(config, background, N, state, k)
    assert abs(constraint) < 1e-14
    step = 1e-5
    # Derivative along the full background + perturbation flow, not the
    # algebraic constraint evaluated twice at the same state.
    before = equations(config, background, N - step, state - step * rhs, k)[1]
    after = equations(config, background, N + step, state + step * rhs, k)[1]
    assert (after - before) / (2 * step) == pytest.approx(0., abs=1e-8)


def test_resting_scalar_recovers_fixed_metric_scalar_equation():
    config = Baseline(initial_N=-2, initial_field=0)
    background = evolve(config)
    state = np.array([.1, .2, 0., 0., 0., 0., 0.])
    rhs, _ = equations(config, background, -1, state, .5)
    h2, epsilon = config.background(-1, 0, 0)
    assert rhs[1] == pytest.approx(-(3-epsilon)*.2-(.5*np.exp(1))**2/h2*.1)


@pytest.mark.parametrize("k", [0, -1, float("nan")])
def test_invalid_k_rejected(k):
    config = Baseline(initial_N=-2)
    with pytest.raises(ValueError):
        equations(config, evolve(config), -1, np.zeros(7), k)


def test_integrated_constraint_compatible_state_preserves_constraint():
    import json
    from theory.coupled_perturbations import validate
    config = Baseline(initial_N=-2)
    background = evolve(config)
    state = np.array([.0001, -.0002, 0., .00003, .00005, -.00004, .00001])
    _, residual = equations(config, background, -2, state, .5)
    h2, _ = config.background(-2, *background.sol(-2))
    matter = config.matter_today * np.exp(6) / h2
    state[2] = -2 * residual / matter
    report = validate(config, state, .5)
    assert report["numerical_gate_passed"] is True
    assert report["max_absolute_density_constraint"] < 1e-8
    assert report["max_scaled_equation_residual"] < 1e-5
    assert report["equation_sample_count"] > 0
    assert report["scientific_baseline_ready"] is False
    json.dumps(report, allow_nan=False)


def test_constraint_preserving_stalled_scalar_cannot_pass(monkeypatch):
    from types import SimpleNamespace
    from theory import coupled_perturbations as coupled
    config = Baseline(initial_N=-1., initial_field=0., matter_today=0.,
                      radiation_today=0.)
    background = evolve(config)
    state = np.array([.01, 0., 0., 0., 0., 0., 0.])

    def stalled(*args, **kwargs):
        return SimpleNamespace(
            background=background, t=np.array([-1., 0.]),
            sol=lambda N: np.tile(state[:, None], (1, np.asarray(N).size))
            if np.asarray(N).ndim else state.copy(),
        )

    monkeypatch.setattr(coupled, "integrate", stalled)
    report = coupled.validate(config, state, 1.)
    assert report["max_scaled_state_shift"] == 0
    assert report["max_absolute_density_constraint"] == 0
    assert report["max_scaled_initial_shift"] == 0
    assert report["max_scaled_equation_residual"] > 1e-5
    assert report["numerical_gate_passed"] is False


def test_invalid_initial_constraint_is_not_silently_projected():
    from theory.coupled_perturbations import integrate
    with pytest.raises(ValueError, match="violates"):
        integrate(Baseline(initial_N=-2), [0, 0, .1, 0, 0, 0, 0], .5)


@pytest.mark.parametrize("method", ["RK45", "DOP853"])
def test_integrated_zero_state_remains_zero(method):
    from theory.coupled_perturbations import integrate
    sol = integrate(Baseline(initial_N=-2), np.zeros(7), .5, method=method)
    np.testing.assert_array_equal(sol.sol(np.linspace(-2, 0, 20)), np.zeros((7, 20)))


@pytest.mark.parametrize("method", ["RK45", "DOP853"])
def test_matter_only_growing_mode_matches_exact_newtonian_solution(method):
    from theory.coupled_perturbations import integrate
    config = Baseline(initial_N=-2., initial_field=0., vacuum=0.,
                      radiation_today=0., matter_today=.9)
    k, phi = .5, 1e-5
    epochs = np.linspace(-2., 0., 101)
    wave2 = k**2 * np.exp(epochs) / (config.matter_today / 3)
    # Phi is constant in Einstein-de Sitter; radiation is absent but its
    # passive variables still obey the zero-density fluid equations.
    initial = [0., 0., -2 * phi - 2 * wave2[0] * phi / 3,
               2 * wave2[0] * phi / 3, -4 * phi, 0., phi]
    solution = integrate(config, initial, k, method=method)
    states = solution.sol(epochs)
    np.testing.assert_allclose(states[6], phi, rtol=1e-8, atol=1e-12)
    np.testing.assert_allclose(states[2], -2 * phi - 2 * wave2 * phi / 3,
                               rtol=1e-8, atol=1e-12)
    np.testing.assert_allclose(states[3], 2 * wave2 * phi / 3,
                               rtol=1e-8, atol=1e-12)


@pytest.mark.parametrize("method", ["RK45", "DOP853"])
def test_radiation_acoustic_metric_matches_exact_solution(method):
    from theory.coupled_perturbations import integrate
    config = Baseline(initial_N=-1., initial_field=0., vacuum=0.,
                      radiation_today=.9, matter_today=0.)
    k, primordial_phi = 2., 1e-5
    epochs = np.linspace(-1., 0., 101)
    x = k * np.exp(epochs) / np.sqrt(config.radiation_today)
    shape = (np.sin(x) - x * np.cos(x)) / x**3
    phi = 3 * primordial_phi * shape
    phi_prime = 3 * primordial_phi * (np.sin(x) / x - 3 * shape)
    momentum = phi_prime + phi
    wave2 = 3 * x**2
    radiation_density = -2 * wave2 * phi / 3 - 2 * momentum
    radiation_velocity = wave2 * momentum / 2
    initial = [0., 0., 0., 0., radiation_density[0],
               radiation_velocity[0], phi[0]]
    solution = integrate(config, initial, k, method=method)
    states = solution.sol(epochs)
    np.testing.assert_allclose(states[6], phi, rtol=1e-7, atol=1e-12)
    np.testing.assert_allclose(states[4], radiation_density, rtol=1e-7, atol=1e-12)
    np.testing.assert_allclose(states[5], radiation_velocity, rtol=1e-7, atol=1e-12)


@pytest.mark.parametrize("phi0", [1e-5, -2e-5])
@pytest.mark.parametrize("x", [.01, .005, .001])
def test_adiabatic_series_satisfies_constraints_entropy_and_normalization(phi0, x):
    from theory.coupled_perturbations import radiation_adiabatic_initial_state
    config = Baseline(initial_N=-8., initial_field=0., vacuum=0.,
                      matter_today=0., radiation_today=.9)
    k = x * np.sqrt(config.radiation_today) * np.exp(-config.initial_N)
    state = radiation_adiabatic_initial_state(config, k, primordial_phi=phi0)
    rhs, constraint = equations(config, evolve(config), config.initial_N, state, k)
    assert abs(constraint / phi0) < 1e-14
    assert rhs[6] / phi0 == pytest.approx(-x**2 / 5 + x**4 / 70 - x**6 / 2520,
                                         abs=1e-15)
    assert (state[2] - .75 * state[4]) / phi0 == pytest.approx(
        -3 * x**4 / 32, abs=x**6 + 4 * np.finfo(float).eps)
    assert (state[3] - state[5]) / phi0 == pytest.approx(3 * x**4 / 8, abs=x**6)
    # zeta=-Phi+delta_r/4 -> -3*Phi_primordial/2, in this metric convention.
    assert (-state[6] + state[4] / 4) / phi0 == pytest.approx(-1.5, abs=x**2)
    np.testing.assert_array_equal(state[:2], [0., 0.])


@pytest.mark.parametrize("method", ["RK45", "DOP853"])
def test_adiabatic_initialization_matches_radiation_solution_through_horizon(method):
    from scipy.special import sici
    from theory.coupled_perturbations import integrate, radiation_adiabatic_initial_state
    config = Baseline(initial_N=-7., initial_field=0., vacuum=0.,
                      matter_today=0., radiation_today=.9)
    k, phi0 = 2., 1e-5
    initial = radiation_adiabatic_initial_state(config, k, primordial_phi=phi0)
    sol = integrate(config, initial, k, method=method, rtol=1e-12, atol=1e-18,
                    max_step=(config.final_N - config.initial_N) / 1000)
    epochs = np.linspace(-4., 0., 101)
    x = k * np.exp(epochs) / np.sqrt(config.radiation_today)
    shape = (np.sin(x) - x * np.cos(x)) / x**3
    phi = 3 * phi0 * shape
    momentum = phi + 3 * phi0 * (np.sin(x) / x - 3 * shape)
    states = sol.sol(epochs)
    np.testing.assert_allclose(states[6], phi, rtol=1e-7, atol=1e-13)
    np.testing.assert_allclose(states[4], -2 * momentum - 2 * x**2 * phi,
                               rtol=1e-7, atol=1e-13)
    np.testing.assert_allclose(states[5], 1.5 * x**2 * momentum, rtol=1e-7, atol=1e-13)
    dust_velocity = 9 * phi0 * (1 - np.sin(x) / x)
    dust_integral = np.log(x) + np.euler_gamma - sici(x)[1] + np.sin(x) / x - 1
    dust_density = -1.5 * phi0 + 3 * (phi - phi0) - 9 * phi0 * dust_integral
    np.testing.assert_allclose(states[3], dust_velocity, rtol=1e-7, atol=1e-13)
    np.testing.assert_allclose(states[2], dust_density, rtol=1e-7, atol=1e-13)


def test_adiabatic_series_obeys_all_evolution_equations():
    from dataclasses import replace
    from theory.coupled_perturbations import radiation_adiabatic_initial_state
    config = Baseline(initial_N=-8., initial_field=0., vacuum=0.,
                      matter_today=0., radiation_today=.9)
    k = .009 * np.sqrt(config.radiation_today) * np.exp(-config.initial_N)
    phi0, step = 1e-5, .001

    def at(offset):
        return radiation_adiabatic_initial_state(
            replace(config, initial_N=config.initial_N + offset), k, primordial_phi=phi0,
        )

    derivative = (at(-2 * step) - 8 * at(-step) + 8 * at(step) - at(2 * step)) / (12 * step)
    rhs, _ = equations(config, evolve(config), config.initial_N, at(0), k)
    np.testing.assert_allclose(derivative / phi0, rhs / phi0, rtol=0., atol=1e-10)


def test_adiabatic_solution_is_independent_of_superhorizon_start_epoch():
    from theory.coupled_perturbations import integrate, radiation_adiabatic_initial_state
    trajectories = []
    for start in [-7., -6.]:
        config = Baseline(initial_N=start, initial_field=0., vacuum=0.,
                          matter_today=0., radiation_today=.9)
        initial = radiation_adiabatic_initial_state(config, 2.)
        trajectories.append(integrate(config, initial, 2., rtol=1e-12, atol=1e-15))
    grid = np.linspace(-5., 0., 101)
    np.testing.assert_allclose(trajectories[0].sol(grid), trajectories[1].sol(grid),
                               rtol=1e-7, atol=1e-13)


@pytest.mark.parametrize("change", [
    {"matter_today": .001}, {"radiation_today": 0.}, {"vacuum": .01},
    {"initial_field": .1}, {"initial_field_prime": .001},
])
def test_adiabatic_initialization_rejects_unsupported_backgrounds(change):
    from theory.coupled_perturbations import radiation_adiabatic_initial_state
    kwargs = dict(initial_N=-7., initial_field=0., vacuum=0.,
                  matter_today=0., radiation_today=.9)
    kwargs.update(change)
    with pytest.raises(ValueError, match="only pure radiation"):
        radiation_adiabatic_initial_state(Baseline(**kwargs), 2.)


@pytest.mark.parametrize("k,phi", [
    (0., 1e-5), (-1., 1e-5), (float("nan"), 1e-5), (float("inf"), 1e-5),
    (100., 1e-5), (1e-300, 1e-5), (2., 0.), (2., float("nan")),
    (2., float("inf")), (2., .1), (2., 1e-320),
])
def test_adiabatic_initialization_rejects_invalid_or_unresolved_modes(k, phi):
    from theory.coupled_perturbations import radiation_adiabatic_initial_state
    config = Baseline(initial_N=-7., initial_field=0., vacuum=0.,
                      matter_today=0., radiation_today=.9)
    with pytest.raises(ValueError):
        radiation_adiabatic_initial_state(config, k, primordial_phi=phi)


@pytest.mark.parametrize("start", [-200., 1000.])
def test_adiabatic_initialization_rejects_unresolved_background(start):
    from theory.coupled_perturbations import radiation_adiabatic_initial_state
    config = Baseline(initial_N=start, final_N=start + 1, initial_field=0., vacuum=0.,
                      matter_today=0., radiation_today=.9)
    with pytest.raises(ValueError):
        radiation_adiabatic_initial_state(config, 2.)


def test_adiabatic_trajectory_does_not_promote_scientific_readiness():
    from theory.coupled_perturbations import radiation_adiabatic_initial_state, validate
    config = Baseline(initial_N=-7., initial_field=0., vacuum=0.,
                      matter_today=0., radiation_today=.9)
    initial = radiation_adiabatic_initial_state(config, 2.)
    report = validate(config, initial, 2.)
    assert report["numerical_gate_passed"] is True
    assert report["primordial_initialization_established"] is False
    assert report["scientific_baseline_ready"] is False
    assert report["full_stability_established"] is False


@pytest.mark.parametrize("x,y", [(.0099, .0099), (.005, .002), (.001, .0099)])
@pytest.mark.parametrize("phi0", [1e-5, -2e-5])
def test_mixed_adiabatic_series_satisfies_einstein_constraint_and_entropy(x, y, phi0):
    from theory.coupled_perturbations import mixed_adiabatic_initial_state
    config = Baseline(initial_N=np.log(y), initial_field=0., vacuum=0.,
                      matter_today=.9, radiation_today=.9)
    k = x * np.sqrt(config.radiation_today) / y
    state = mixed_adiabatic_initial_state(config, k, primordial_phi=phi0)
    _, constraint = equations(config, evolve(config), config.initial_N, state, k)
    assert abs(constraint / phi0) < 1e-14
    assert abs((state[2] - .75 * state[4]) / phi0) < x**4
    wave2 = 3 * x**2 / (1 + y)
    assert abs((state[3] - state[5]) / (wave2 * phi0)) < x**2
    np.testing.assert_array_equal(state[:2], [0., 0.])


@pytest.mark.parametrize("x", [.0099, .005, .001])
def test_mixed_initializer_recovers_independent_pure_radiation_series(x):
    from theory.coupled_perturbations import (
        mixed_adiabatic_initial_state, radiation_adiabatic_initial_state,
    )
    config = Baseline(initial_N=-7., initial_field=0., vacuum=0.,
                      matter_today=0., radiation_today=.9)
    k = x * np.sqrt(.9) * np.exp(7)
    np.testing.assert_allclose(
        mixed_adiabatic_initial_state(config, k),
        radiation_adiabatic_initial_state(config, k), rtol=1e-14, atol=1e-20,
    )


def test_mixed_initial_series_obeys_all_evolution_equations():
    from dataclasses import replace
    from theory.coupled_perturbations import mixed_adiabatic_initial_state
    config = Baseline(initial_N=np.log(.009), initial_field=0., vacuum=0.,
                      matter_today=.9, radiation_today=.9)
    k, phi0, step = .9, 1e-5, .001

    def at(offset):
        return mixed_adiabatic_initial_state(
            replace(config, initial_N=config.initial_N + offset), k, primordial_phi=phi0,
        )

    derivative = (at(-2 * step) - 8 * at(-step) + 8 * at(step) - at(2 * step)) / (12 * step)
    rhs, _ = equations(config, evolve(config), config.initial_N, at(0), k)
    np.testing.assert_allclose(derivative / phi0, rhs / phi0, rtol=0., atol=1e-10)


def test_mixed_mode_has_radiation_era_normalization_and_first_matter_correction():
    from theory.coupled_perturbations import mixed_adiabatic_initial_state
    y, phi0 = 1e-4, -2e-5
    config = Baseline(initial_N=np.log(y), initial_field=0., vacuum=0.,
                      matter_today=.9, radiation_today=.9)
    k = 1e-6
    state = mixed_adiabatic_initial_state(config, k, primordial_phi=phi0)
    assert state[6] / phi0 == pytest.approx(1 - y / 16 + 7 * y**2 / 160, abs=y**3)
    assert state[2] / phi0 == pytest.approx(-1.5 - 3 * y / 16, abs=y**2)
    assert state[4] / phi0 == pytest.approx(-2 - y / 4, abs=y**2)
    wave2 = 3 * (k * y)**2 / (.9 * (1 + y))
    for row in [3, 5]:
        assert state[row] / (wave2 * phi0) == pytest.approx(.5 + y / 16, abs=y**2)


@pytest.mark.parametrize("method", ["RK45", "DOP853"])
def test_mixed_superhorizon_mode_matches_independent_quadrature_across_equality(method):
    from scipy.integrate import quad
    from theory.coupled_perturbations import integrate, mixed_adiabatic_initial_state
    config = Baseline(initial_N=np.log(.005), final_N=np.log(100.),
                      initial_field=0., vacuum=0., matter_today=.9, radiation_today=.9)
    k, phi0 = 1e-7, 1e-5
    initial = mixed_adiabatic_initial_state(config, k, primordial_phi=phi0)
    sol = integrate(config, initial, k, method=method, rtol=1e-12, atol=1e-24,
                    max_step=(config.final_N - config.initial_N) / 1000)
    epochs = np.linspace(config.initial_N, config.final_N, 101)
    y = np.exp(epochs)
    phi = np.array([
        1.5 * phi0 * (1 - np.sqrt(1 + ratio) * quad(
            lambda t: t**2 / np.sqrt(1 + ratio * t), 0., 1.,
            epsabs=1e-13, epsrel=1e-13,
        )[0]) for ratio in y
    ])
    states = sol.sol(epochs)
    np.testing.assert_allclose(states[6], phi, rtol=1e-8, atol=1e-14)
    np.testing.assert_allclose(states[2], 3 * (phi - 1.5 * phi0), rtol=1e-8, atol=1e-14)
    np.testing.assert_allclose(states[4], 4 * (phi - 1.5 * phi0), rtol=1e-8, atol=1e-14)
    wave2 = 3 * (k * np.exp(epochs))**2 / (.9 * (1 + y))
    for row in [3, 5]:
        np.testing.assert_allclose(states[row] / wave2, 1.5 * phi0 - phi,
                                   rtol=1e-8, atol=1e-14)
    for N in epochs:
        assert abs(equations(config, sol.background, N, sol.sol(N), k)[1] / phi0) < 1e-8


@pytest.mark.parametrize("method", ["RK45", "DOP853"])
def test_mixed_initial_epoch_independence_through_equality_and_horizon_entry(method):
    from theory.coupled_perturbations import integrate, mixed_adiabatic_initial_state
    trajectories = []
    k = 1.
    for start in [-6., -5.]:
        config = Baseline(initial_N=start, final_N=2., initial_field=0., vacuum=0.,
                          matter_today=.9, radiation_today=.9)
        initial = mixed_adiabatic_initial_state(config, k)
        trajectories.append(integrate(config, initial, k, method=method,
                                      rtol=1e-12, atol=1e-18,
                                      max_step=(config.final_N - start) / 1000))
    grid = np.linspace(-4., 2., 101)
    np.testing.assert_allclose(trajectories[0].sol(grid), trajectories[1].sol(grid),
                               rtol=1e-7, atol=1e-13)
    for sol in trajectories:
        for N in grid:
            assert abs(equations(sol.background.background_config, sol.background,
                                 N, sol.sol(N), k)[1]) < 1e-12


@pytest.mark.parametrize("change,k,phi", [
    ({}, 0., 1e-5), ({}, -1., 1e-5), ({}, float("nan"), 1e-5),
    ({}, float("inf"), 1e-5), ({}, 100., 1e-5), ({}, 1e-300, 1e-5),
    ({}, 1., 0.), ({}, 1., float("nan")), ({}, 1., .01), ({}, 1., 1e-320),
    ({"radiation_today": 0.}, 1., 1e-5), ({"vacuum": .1}, 1., 1e-5),
    ({"initial_field": .1}, 1., 1e-5), ({"initial_field_prime": .1}, 1., 1e-5),
    ({"initial_N": -2.}, 1., 1e-5), ({"initial_N": -200.}, 1., 1e-5),
    ({"initial_N": 1000., "final_N": 1001.}, 1., 1e-5),
])
def test_mixed_initializer_rejects_unsupported_or_unresolved_inputs(change, k, phi):
    from theory.coupled_perturbations import mixed_adiabatic_initial_state
    kwargs = dict(initial_N=-6., initial_field=0., vacuum=0.,
                  matter_today=.9, radiation_today=.9)
    kwargs.update(change)
    with pytest.raises(ValueError):
        mixed_adiabatic_initial_state(Baseline(**kwargs), k, primordial_phi=phi)


def test_mixed_adiabatic_trajectory_keeps_general_readiness_false():
    from theory.coupled_perturbations import mixed_adiabatic_initial_state, validate
    config = Baseline(initial_N=-6., final_N=1., initial_field=0., vacuum=0.,
                      matter_today=.9, radiation_today=.9)
    state = mixed_adiabatic_initial_state(config, 1.)
    report = validate(config, state, 1.)
    assert report["numerical_gate_passed"] is True
    for gate in ["primordial_initialization_established", "scientific_baseline_ready",
                 "full_stability_established"]:
        assert report[gate] is False


def _field_config(**change):
    kwargs = dict(vacuum=2.1, initial_field=.5, initial_field_prime=1e-3,
                  initial_N=-16., final_N=-14.)
    kwargs.update(change)
    return Baseline(**kwargs)


def test_subdominant_field_reduces_to_resting_mixed_series():
    from theory.coupled_perturbations import (
        mixed_adiabatic_initial_state, subdominant_field_adiabatic_initial_state)
    config = Baseline(initial_N=-16., final_N=-14., initial_field=0., vacuum=0.)
    assert np.array_equal(subdominant_field_adiabatic_initial_state(config, 100.),
                          mixed_adiabatic_initial_state(config, 100.))


@pytest.mark.parametrize("change", [
    {}, {"initial_field": 1.2}, {"initial_field_prime": -2e-3}, {"vacuum": 0.},
])
def test_subdominant_field_state_has_independent_small_constraint_residual(change):
    from theory.coupled_perturbations import subdominant_field_adiabatic_initial_state
    config = _field_config(**change)
    state = subdominant_field_adiabatic_initial_state(config, 100.)
    background = evolve(config, method="DOP853", rtol=1e-12, atol=1e-14)
    constraint = equations(config, background, config.initial_N, state, 100.)[1]
    h2, _ = config.background(config.initial_N, config.initial_field, config.initial_field_prime)
    fraction = (config.potential(config.initial_field)[0]
                + h2 * config.initial_field_prime**2 / 2) / (3 * h2)
    # Velocities carry 1/H: with the true H2 the O(f) 00 residual (formerly
    # 3*f*Phi0) cancels, leaving only O(f*x^2*Phi0) series leakage.
    assert abs(constraint) <= 1e-5 * (fraction + 1e-12) * 1e-5
    assert abs(state[0] - config.initial_field_prime * -state[4] / 4) < 1e-18


def test_subdominant_field_residual_scales_with_amplitude_and_passes_larger_phi():
    from theory.coupled_perturbations import (
        integrate, subdominant_field_adiabatic_initial_state)
    config = _field_config()
    background = evolve(config, method="DOP853", rtol=1e-12, atol=1e-14)
    residuals = [abs(equations(config, background, config.initial_N,
                               subdominant_field_adiabatic_initial_state(
                                   config, 100., primordial_phi=phi), 100.)[1])
                 for phi in (1e-5, 1e-3)]
    assert 50 < residuals[1] / residuals[0] < 200
    state = subdominant_field_adiabatic_initial_state(config, 100., primordial_phi=1e-3)
    assert integrate(config, state, 100.).success


def test_subdominant_field_mode_follows_common_time_shift_with_x_squared_leakage():
    from theory.coupled_perturbations import (
        integrate, subdominant_field_adiabatic_initial_state)
    config = _field_config()
    background = evolve(config, method="DOP853", rtol=1e-12, atol=1e-14)

    def leakage(k, modify=False):
        state = subdominant_field_adiabatic_initial_state(config, k)
        if modify:
            state[1] = 0.
        solution = integrate(config, state, k)
        end = solution.sol(config.final_N)
        shift = background.sol(config.final_N)[1] * end[4] / 4
        return abs(end[0] + shift) / abs(shift)

    low, high = leakage(100.), leakage(300.)
    assert low < 1e-3 and 5 < high / low < 15
    assert leakage(100., modify=True) > 100 * low


def test_subdominant_field_solution_is_start_epoch_independent_with_x_squared_error():
    from dataclasses import replace
    from theory.coupled_perturbations import (
        integrate, subdominant_field_adiabatic_initial_state)
    early = _field_config()
    background = evolve(early, method="DOP853", rtol=1e-12, atol=1e-14)
    field, momentum = background.sol(-15.)
    late = replace(early, initial_N=-15., initial_field=float(field),
                   initial_field_prime=float(momentum))
    grid = np.linspace(-15., early.final_N, 9)

    def errors(k):
        runs = [integrate(c, subdominant_field_adiabatic_initial_state(c, k), k,
                          rtol=1e-12, atol=1e-15).sol(grid) for c in (early, late)]
        scale = np.abs(runs[0]).max(axis=1)
        return np.max(np.abs(runs[0] - runs[1]).max(axis=1) / scale)

    low, high = errors(100.), errors(300.)
    assert low < 1e-4 and 5 < high / low < 15


def test_subdominant_field_trajectory_passes_numerical_gate_without_readiness():
    from theory.coupled_perturbations import (
        subdominant_field_adiabatic_initial_state, validate)
    config = _field_config()
    report = validate(config, subdominant_field_adiabatic_initial_state(config, 100.), 100.)
    assert report["numerical_gate_passed"] is True
    assert report["primordial_initialization_established"] is False
    assert report["scientific_baseline_ready"] is False


@pytest.mark.parametrize("change,k,phi,bound", [
    ({"vacuum": 1e19}, 100., 1e-5, 1e-6), ({"initial_field_prime": .1}, 100., 1e-5, 1e-6),
    ({}, 100., 1e-5, 1e-3), ({}, 100., 1e-5, 0.), ({}, 100., 1e-5, float("nan")),
    ({"radiation_today": 0.}, 100., 1e-5, 1e-6), ({}, 0., 1e-5, 1e-6),
    ({}, 100., 0., 1e-6), ({}, 100., float("nan"), 1e-6), ({"initial_N": -8.}, 100., 1e-5, 1e-6),
])
def test_subdominant_field_initializer_rejects_unsupported_inputs(change, k, phi, bound):
    from theory.coupled_perturbations import subdominant_field_adiabatic_initial_state
    with pytest.raises(ValueError):
        subdominant_field_adiabatic_initial_state(
            _field_config(**change), k, primordial_phi=phi, max_field_fraction=bound)
