import importlib.util
from pathlib import Path
import tempfile

import numpy as np
import pytest


PATH = Path(__file__).resolve().parents[1] / "observational_coverage.py"
spec = importlib.util.spec_from_file_location("observational_coverage_test", PATH)
coverage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(coverage)


def test_extension_preserves_baseline_and_replaces_overlapping_bao():
    base = {"likelihood": {"bao.desi_dr2.desi_bao_all": None, "planck_2018_lensing.native": None,
                          "sn.pantheonplus": None, "benchmark_w0wa_domain": {"external": "domain"}},
            "params": {"omega_b": {"prior": {"min": .019, "max": .026}}},
            "theory": {"classytwist": {"extra_args": {"non_linear": "halofit"}}},
            "output": "baseline", "sampler": {"minimize": {"best_of": 4}}}
    result = coverage.with_galaxy_growth(base, "separate")
    assert "bao.desi_dr2.desi_bao_all" in base["likelihood"]
    assert list(k for k in result["likelihood"] if k.startswith("bao.")) == [coverage.GROWTH_LIKELIHOOD]
    for key in ("params", "theory", "sampler"):
        assert result[key] == base[key]
    assert "benchmark_w0wa_domain" in result["likelihood"]
    assert result["output"] == "separate"
    assert result["force"] is False


def test_missing_baseline_bao_is_explicit():
    with pytest.raises(ValueError):
        coverage.with_galaxy_growth({"likelihood": {}}, "separate")


def test_reusing_baseline_output_is_rejected():
    with pytest.raises(ValueError):
        coverage.with_galaxy_growth({"output": "baseline", "likelihood": {"bao.example": None}}, "baseline")


def test_measurement_and_covariance_validation():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory) / "data" / "bao_data"
        root.mkdir(parents=True)
        rows = "".join(f"{z} 1 {observable}\n" for z in (.38, .51, .61)
                       for observable in ("DM_over_rs", "bao_Hz_rs", "f_sigma8"))
        (root / "sdss_DR12Consensus_final.dat").write_text(rows)
        cov = root / "final_consensus_covtot_dM_Hz_fsig.txt"
        np.savetxt(cov, np.eye(9))
        assert coverage.validate_growth_data(directory)["joint_data_points"] == 9
        np.savetxt(cov, np.eye(8))
        with pytest.raises(ValueError):
            coverage.validate_growth_data(directory)
        np.savetxt(cov, np.zeros((9, 9)))
        with pytest.raises(np.linalg.LinAlgError):
            coverage.validate_growth_data(directory)


@pytest.mark.parametrize("scale", [1., 1e-12, 1e12])
def test_growth_covariance_symmetry_is_independent_of_units(tmp_path, scale):
    root = tmp_path / "data" / "bao_data"
    root.mkdir(parents=True)
    rows = "".join(f"{z} 1 {observable}\n" for z in (.38, .51, .61)
                   for observable in ("DM_over_rs", "bao_Hz_rs", "f_sigma8"))
    (root / "sdss_DR12Consensus_final.dat").write_text(rows)
    covariance = scale * np.eye(9)
    covariance[0, 1] = scale * .9
    path = root / "final_consensus_covtot_dM_Hz_fsig.txt"
    np.savetxt(path, covariance)
    with pytest.raises(ValueError, match="symmetric"):
        coverage.validate_growth_data(tmp_path)
    covariance[1, 0] = covariance[0, 1]
    np.savetxt(path, covariance)
    assert coverage.validate_growth_data(tmp_path)["joint_data_points"] == 9
