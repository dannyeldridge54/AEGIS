import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from chronometers import chronometer_chi2, load_chronometers, with_chronometers


@pytest.fixture
def data_path(tmp_path):
    np.savetxt(tmp_path / "HzTable_MM_BC03.dat", [[.2, 75, 4], [.4, 85, 6]], delimiter=",")
    np.savetxt(tmp_path / "data_MM20.dat", [[.1, 1, 2, 3, 4], [.5, 1, 2, 3, 4]])
    return tmp_path


def test_covariance_matches_reference_terms(data_path):
    z, h, covariance = load_chronometers(data_path)
    expected = np.diag([16, 36]) + np.outer(h * .01, h * .01) + np.outer(h * .04, h * .04)
    np.testing.assert_allclose(covariance, expected)
    assert chronometer_chi2(h, h, covariance) == 0
    prediction = h + 2
    assert chronometer_chi2(prediction, h, covariance) == pytest.approx(
        (h - prediction) @ np.linalg.inv(covariance) @ (h - prediction))


@pytest.mark.parametrize("prediction", [[75], [75, np.nan], [75, -1]])
def test_bad_prediction_fails(prediction):
    with pytest.raises(ValueError):
        chronometer_chi2(prediction, [75, 85], np.eye(2))


def test_out_of_range_systematics_use_authors_endpoint_interpolation(data_path):
    np.savetxt(data_path / "HzTable_MM_BC03.dat", [[.2, 75, 4], [2, 85, 6]], delimiter=",")
    np.savetxt(data_path / "data_MM20.dat", [[.1, 1, 2, 3, 4], [.5, 1, 2, 3, 4]])
    z, h, covariance = load_chronometers(data_path)
    fractional = np.array([.01, .01])
    expected = np.diag([16, 36]) + np.outer(h * fractional, h * fractional)
    expected += np.outer(h * .04, h * .04)
    np.testing.assert_allclose(covariance, expected)


def test_separate_extension_preserves_baseline(data_path):
    base = {"output": str(data_path / "baseline"), "likelihood": {"bao.test": None}}
    info = with_chronometers(base, data_path, data_path / "extension")
    assert base["likelihood"] == {"bao.test": None}
    assert len(info["likelihood"]) == 2
    assert not info["resume"] and not info["force"]
    with pytest.raises(ValueError, match="separate"):
        with_chronometers(base, data_path, data_path / "baseline" / "child")
    with pytest.raises(ValueError, match="separate"):
        with_chronometers(base, data_path, data_path)


def test_bad_covariance_fails():
    with pytest.raises(ValueError):
        chronometer_chi2([75, 85], [75, 85], [[1, 2], [0, 1]])
    with pytest.raises(np.linalg.LinAlgError):
        chronometer_chi2([75, 85], [75, 85], [[1, 2], [2, 1]])


@pytest.mark.parametrize("scale", [1., 1e-12, 1e12])
def test_covariance_symmetry_is_independent_of_units(scale):
    covariance = scale * np.array([[1., .9], [0., 1.]])
    with pytest.raises(ValueError, match="covariance"):
        chronometer_chi2([76, 86], [75, 85], covariance)
    symmetric = scale * np.array([[1., .2], [.2, 1.]])
    assert chronometer_chi2([76, 86], [75, 85], symmetric) * scale == pytest.approx(5 / 3)


def test_empty_measurements_cannot_report_perfect_fit():
    with pytest.raises(ValueError):
        chronometer_chi2([], [], np.empty((0, 0)))


@pytest.mark.parametrize("measured", [[0], [-1]])
def test_nonpositive_measurements_rejected(measured):
    with pytest.raises(ValueError):
        chronometer_chi2([75], measured, [[1]])


def test_finite_inputs_cannot_export_infinite_chi_square():
    with pytest.raises(ValueError, match="overflowed"):
        chronometer_chi2([1e308], [75], [[1]])


@pytest.mark.parametrize("huge_errors", [True, False])
def test_loader_rejects_covariance_overflow(data_path, huge_errors):
    rows = [[.2, 75, 1e200], [.4, 85, 1e200]] if huge_errors else [
        [.2, 1e200, 4], [.4, 1e200, 6]
    ]
    np.savetxt(data_path / "HzTable_MM_BC03.dat", rows, delimiter=",")
    with pytest.raises(ValueError, match="covariance construction overflowed"):
        load_chronometers(data_path)


def test_loader_rejects_covariance_underflow(data_path):
    np.savetxt(data_path / "HzTable_MM_BC03.dat",
               [[.2, 75, 1e-200], [.4, 85, 1e-200]], delimiter=",")
    np.savetxt(data_path / "data_MM20.dat",
               [[.1, 0, 0, 0, 0], [.5, 0, 0, 0, 0]])
    with pytest.raises(np.linalg.LinAlgError):
        load_chronometers(data_path)
