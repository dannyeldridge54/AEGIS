import json
from types import SimpleNamespace

import numpy as np
import pytest

from aegis import data_v2 as data
from aegis import likelihood_v2 as likelihood


@pytest.fixture
def sn_path(tmp_path):
    path = tmp_path / "supernovae.json"
    path.write_text(json.dumps({
        "nBins": 2, "binZ": [.1, .2], "binMu": [40., 41.],
        "covBin": [1., .2, .2, 1.],
    }))
    return path


@pytest.mark.parametrize("changes", [
    {"binZ": [.1, .1]}, {"binZ": [0., .2]}, {"binMu": [40.]},
    {"binMu": [40., float("nan")]}, {"nBins": True},
    {"covBin": [1., 2., 2., 1.]},
    {"covBin": [1e-12, 9e-13, 0., 1e-12]},
])
def test_invalid_supernova_inputs_cannot_enter_likelihood(sn_path, changes):
    value = json.loads(sn_path.read_text())
    value.update(changes)
    sn_path.write_text(json.dumps(value))
    with pytest.raises((ValueError, np.linalg.LinAlgError)):
        data.load_pantheon_binned(sn_path)


def test_supernova_marginalization_is_stable_under_common_offset(sn_path, monkeypatch):
    distances = SimpleNamespace(DC=lambda z: 1 / (1 + np.asarray(z)), DV=lambda z: 1.,
                                DH=lambda z: 1.)
    monkeypatch.setattr(likelihood, "derived", lambda _: {
        "D": distances, "rd": 1., "theta": likelihood.THETA_REF,
    })
    model = SimpleNamespace(wb=data.OMEGA_B_PRIOR[0], h=.7)
    fit = likelihood.Likelihood(sn_path)
    mu = np.full_like(fit.zsn, 25.)
    for offset in (0., 1e8):
        fit.msn = mu + offset + np.array([-1., 1.])
        parts = fit.parts(model)
        assert parts["sn"] == pytest.approx(2.5, rel=1e-12, abs=1e-12)
        assert parts["M_B"] == pytest.approx(offset, abs=1e-6)


def test_nonfinite_likelihood_cannot_reach_optimizer_as_nan(sn_path, monkeypatch, caplog):
    distances = SimpleNamespace(DC=lambda z: np.full_like(z, np.nan),
                                DV=lambda z: 1., DH=lambda z: 1.)
    monkeypatch.setattr(likelihood, "derived", lambda _: {
        "D": distances, "rd": 1., "theta": likelihood.THETA_REF,
    })
    fit = likelihood.Likelihood(sn_path)
    model = SimpleNamespace(wb=data.OMEGA_B_PRIOR[0], h=.7)
    with pytest.raises(ValueError, match="finite"):
        fit.parts(model)
    assert fit.chi2(model) == 1e12
    assert "Rejected" in caplog.text


def test_programming_errors_are_not_hidden_as_optimizer_penalties(sn_path, monkeypatch):
    fit = likelihood.Likelihood(sn_path)

    def broken(_):
        raise TypeError("broken model interface")

    monkeypatch.setattr(fit, "parts", broken)
    with pytest.raises(TypeError, match="broken model interface"):
        fit.chi2(None)
