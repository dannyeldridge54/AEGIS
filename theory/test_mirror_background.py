import numpy as np
import pytest

from theory.mirror_background import prepare_background


def background():
    return {"z": [3, 0, 1], "H [1/Mpc]": [4, 1, 2],
            "(.)p_scf": [-2, -2, -2], "(.)rho_scf": [2, 2, 2],
            "(.)rho_g": [1, 1, 1], "(.)rho_ur": [1, 1, 1],
            "(.)rho_crit": [10, 10, 10]}


def test_unsorted_background_normalizes_at_today():
    expansion, w, h, radiation = prepare_background(background(), [0, 1, 3])
    np.testing.assert_allclose(expansion, [1, 2, 4])
    np.testing.assert_allclose(w, [-1, -1, -1])
    assert h == pytest.approx(2997.92458)
    assert radiation == pytest.approx(0.2)


@pytest.mark.parametrize("key,value", [
    ("z", [3, 0.1, 1]), ("z", [1, 0, 1]), ("z", [float("nan"), 0, 1]),
    ("H [1/Mpc]", [4, 0, 2]), ("(.)rho_scf", [2, 0, 2]),
    ("(.)rho_crit", [10, -1, 10]), ("(.)rho_g", [-1, 1, 1]),
    ("(.)p_scf", [-2]), ("(.)rho_ur", [[1, 1, 1]]),
])
def test_invalid_background_is_rejected(key, value):
    data = background()
    data[key] = value
    with pytest.raises(ValueError):
        prepare_background(data, [0, 3])


@pytest.mark.parametrize("redshifts", [[4], [-1], [float("nan")], []])
def test_no_interpolation_clamping(redshifts):
    with pytest.raises(ValueError):
        prepare_background(background(), redshifts)


def test_missing_column_is_explicit():
    data = background()
    del data["(.)rho_crit"]
    with pytest.raises(ValueError, match="Missing CLASS background column"):
        prepare_background(data, [0])


@pytest.mark.parametrize("key,value", [
    ("(.)rho_scf", [1e-320] * 3),
    ("(.)rho_crit", [1e-320] * 3),
    ("H [1/Mpc]", [1e308, 1e-320, 2]),
])
def test_finite_inputs_cannot_produce_infinite_normalized_values(key, value):
    data = background()
    data[key] = value
    with pytest.raises(ValueError, match="normalization"):
        prepare_background(data, [0, 3])
