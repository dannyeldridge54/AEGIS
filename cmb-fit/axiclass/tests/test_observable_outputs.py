import importlib.util
from pathlib import Path

import numpy as np
import pytest


PATH = Path(__file__).resolve().parents[1] / "observable_outputs.py"
spec = importlib.util.spec_from_file_location("observable_outputs_test", PATH)
outputs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(outputs)


def test_background_order_and_no_extrapolation():
    background = {"z": [2., 1., 0.], "field": [4., 2., 0.]}
    assert outputs.interpolate_background(background, "field", [0., .5, 2.]) == [0., 1., 4.]
    with pytest.raises(ValueError):
        outputs.interpolate_background(background, "field", [3.])


@pytest.mark.parametrize("background", [
    {"z": [0., 0.], "field": [1., 2.]},
    {"z": [0., 1.], "field": [1.]},
    {"z": [0., float("nan")], "field": [1., 2.]},
    {"z": [0., 1.], "field": [1., float("inf")]},
])
def test_invalid_background_is_explicit(background):
    with pytest.raises(ValueError):
        outputs.interpolate_background(background, "field", [0.])


def test_output_grid_and_finite_contract():
    assert outputs.REDSHIFTS[0] == 0.
    assert outputs.REDSHIFTS[-1] == 2.5
    assert len(outputs.WAVENUMBERS) == 100
    assert np.all(np.diff(outputs.WAVENUMBERS) > 0)
    assert outputs.finite_values([[1., 2.]], "test") == [[1., 2.]]
    with pytest.raises(ValueError):
        outputs.finite_values([float("nan")], "test")


@pytest.mark.parametrize("redshifts", [[], [0.]])
@pytest.mark.parametrize("epochs", [[], [0.]])
def test_empty_or_single_epoch_background_is_explicitly_rejected(epochs, redshifts):
    with pytest.raises(ValueError, match="dimensions"):
        outputs.interpolate_background(
            {"z": epochs, "field": [1.] * len(epochs)}, "field", redshifts
        )


@pytest.fixture
def mock_model(monkeypatch):
    from types import SimpleNamespace
    import cobaya.model

    derived = {"H0": 67., "sigma8": .8, "Omega_m": .3, "age": 13.8}
    background = {"z": [0., 3.], "(.)rho_b": [.05, .05],
                  "(.)rho_cdm": [.25, .25], "(.)rho_crit": [1., 1.]}
    solver = SimpleNamespace(
        get_current_derived_parameters=lambda names: derived,
        get_background=lambda: background, rs_drag=lambda: 147.,
        Hubble=lambda z: .0002, angular_distance=lambda z: 100.,
        luminosity_distance=lambda z: 100., effective_f_sigma8=lambda z: .4,
        pk_lin=lambda k, z: 1., pk=lambda k, z: 1.,
    )
    spectra = {key: np.ones(2501) for key in ("tt", "te", "ee", "bb", "pp")}
    spectra["ell"] = np.arange(2501)

    class Model:
        parameterization = SimpleNamespace(sampled_params=lambda: {})
        theory = {"classytwist": SimpleNamespace(classy=solver)}
        likelihood = {"survey": None}
        provider = SimpleNamespace(get_Cl=lambda **kwargs: spectra)
        loglikes = [-1.]

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def add_requirements(self, requirements):
            pass

        def logposterior(self, *args, **kwargs):
            return SimpleNamespace(logpost=-1., loglikes=self.loglikes)

    model = Model()
    monkeypatch.setattr(cobaya.model, "get_model", lambda config: model)
    return model, derived, spectra


@pytest.mark.parametrize("key", ["H0", "sigma8", "Omega_m", "age"])
def test_export_rejects_nonfinite_derived_parameters(mock_model, key):
    _, derived, _ = mock_model
    derived[key] = float("nan")
    with pytest.raises(ValueError, match="derived parameter"):
        outputs.evaluate_observables({}, {})


@pytest.mark.parametrize("multipoles", [np.arange(3), np.arange(2501) + .5,
                                       np.arange(2501)[::-1]])
def test_export_rejects_invalid_multipole_coverage(mock_model, multipoles):
    _, _, spectra = mock_model
    spectra["ell"] = multipoles
    with pytest.raises(ValueError, match="CMB multipoles"):
        outputs.evaluate_observables({}, {})


@pytest.mark.parametrize("loglikes", [[], [-1., -2.], [[-1.]]])
def test_export_rejects_incomplete_likelihood_results(mock_model, loglikes):
    model, _, _ = mock_model
    model.loglikes = loglikes
    with pytest.raises(ValueError, match="Likelihood results"):
        outputs.evaluate_observables({}, {})


def test_complete_export_has_matching_spectra_and_strict_json(mock_model):
    import json
    result = outputs.evaluate_observables({}, {})
    assert len(result["cmb"]["ell"]) == len(result["cmb"]["tt"]) == 2499
    assert result["chi2_by_likelihood"] == {"survey": 2.}
    json.dumps(result, allow_nan=False)


@pytest.mark.parametrize("spectrum", [np.ones((2501, 1)), np.array(1.)])
def test_export_requires_one_dimensional_spectra(mock_model, spectrum):
    _, _, spectra = mock_model
    spectra["tt"] = spectrum
    with pytest.raises(ValueError, match="CMB spectrum"):
        outputs.evaluate_observables({}, {})


def test_export_rejects_overflowing_likelihood_contribution(mock_model):
    model, _, _ = mock_model
    model.loglikes = [-1e308]
    with pytest.raises(ValueError, match="Likelihood contribution"):
        outputs.evaluate_observables({}, {})


@pytest.mark.parametrize("case", ["negative_component", "sum_overflow", "ratio_overflow", "s8_overflow"])
def test_export_rejects_invalid_normalized_matter_quantities(mock_model, case):
    model, derived, _ = mock_model
    background = model.theory["classytwist"].classy.get_background()
    if case == "negative_component":
        background["(.)rho_b"] = [-.01, -.01]
    elif case == "sum_overflow":
        background["(.)rho_b"] = background["(.)rho_cdm"] = [1e308, 1e308]
    elif case == "ratio_overflow":
        background["(.)rho_crit"] = [1e-320, 1e-320]
    else:
        background["(.)rho_cdm"] = [1., 1.]
        derived["sigma8"] = 1e308
    with pytest.raises(ValueError, match="matter|S8"):
        outputs.evaluate_observables({}, {})


def test_finite_s8_avoids_overflow_in_intermediate_normalization(mock_model):
    model, derived, _ = mock_model
    background = model.theory["classytwist"].classy.get_background()
    background["(.)rho_b"] = [0., 0.]
    background["(.)rho_cdm"] = [1e308, 1e308]
    derived["sigma8"] = 1e-154
    result = outputs.evaluate_observables({}, {})
    assert result["S8"] == pytest.approx(1 / np.sqrt(.3))
