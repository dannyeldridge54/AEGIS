import sys

import pytest

from theory import spiral_w


@pytest.mark.parametrize("action", ["validate", "mirror_ramos"])
@pytest.mark.parametrize("passed", [True, False])
def test_validation_cli_propagates_result(monkeypatch, passed, action):
    monkeypatch.setattr(sys, "argv", ["spiral_w.py", action])
    monkeypatch.setattr(spiral_w, action, lambda: passed)
    if passed:
        assert spiral_w.main() is None
    else:
        with pytest.raises(SystemExit) as error:
            spiral_w.main()
        assert error.value.code == 1


@pytest.mark.parametrize("arguments", [[], ["unknown"], ["validate", "scan"]])
def test_invalid_command_does_not_execute_work(monkeypatch, arguments):
    monkeypatch.setattr(sys, "argv", ["spiral_w.py", *arguments])
    monkeypatch.setattr(spiral_w, "validate", lambda: pytest.fail("Unexpected execution"))
    with pytest.raises(SystemExit, match="Usage"):
        spiral_w.main()


@pytest.mark.parametrize("kin,potential", [(3.0, 1.0), (4.0, 1.0), (-1.0, 1.0),
                                         (float("nan"), 1.0), (0.0, -3.0)])
def test_invalid_friedmann_states_fail_explicitly(kin, potential):
    with pytest.raises(ValueError):
        spiral_w._friedmann_h2(1.0, 1.0, potential, kin)


def test_valid_friedmann_constraint():
    assert spiral_w._friedmann_h2(0.9, 0.0, 1.2, 0.9) == pytest.approx(1.0)


def test_closure_does_not_turn_failed_integration_into_a_residual(monkeypatch):
    from types import SimpleNamespace
    failed = SimpleNamespace(success=False, message="fixture integration failure")
    monkeypatch.setattr(spiral_w, "solve", lambda *a, **kw: (failed, None))
    with pytest.raises(ValueError, match="fixture integration failure"):
        spiral_w.closed(0.0, 0.0, 0.0)


@pytest.mark.parametrize("parameters", [{"F": 0}, {"N1": spiral_w.N0}, {"cp0": float("nan")}])
def test_invalid_solver_inputs_are_rejected(parameters):
    with pytest.raises(ValueError):
        spiral_w.solve(1.0, 0.0, 0.0, 0.0, **parameters)


def test_invalid_initial_kinetic_state_is_not_frozen():
    with pytest.raises(ValueError, match="kinetic denominator"):
        spiral_w.solve(1.0, 0.0, 0.0, 0.0, cp0=3.0)
