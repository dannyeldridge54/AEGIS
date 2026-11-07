"""Separate matched growth extension; never alter the frozen baseline suite."""
import copy
from pathlib import Path

import numpy as np


GROWTH_LIKELIHOOD = "bao.sdss_dr12_consensus_final"


def validate_growth_data(packages_path):
    root = Path(packages_path) / "data" / "bao_data"
    measurements = root / "sdss_DR12Consensus_final.dat"
    covariance = root / "final_consensus_covtot_dM_Hz_fsig.txt"
    rows = []
    for line in measurements.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        redshift, value, observable = line.split()
        rows.append((float(redshift), float(value), observable))
    expected = [(z, observable) for z in (.38, .51, .61)
                for observable in ("DM_over_rs", "bao_Hz_rs", "f_sigma8")]
    if [(z, observable) for z, _, observable in rows] != expected:
        raise ValueError("SDSS DR12 combined BAO/growth measurement order does not match its covariance")
    if not all(np.isfinite(z) and np.isfinite(value) and value > 0 for z, value, _ in rows):
        raise ValueError("Nonfinite or nonpositive SDSS DR12 measurements")
    cov = np.loadtxt(covariance)
    if cov.shape != (len(rows), len(rows)) or not np.isfinite(cov).all():
        raise ValueError("Invalid SDSS DR12 joint covariance dimensions or entries")
    if not np.allclose(cov, cov.T, rtol=1e-12, atol=0):
        raise ValueError("SDSS DR12 covariance is not symmetric")
    np.linalg.cholesky(cov)
    return {"measurements_file": str(measurements), "covariance_file": str(covariance),
            "redshifts": [.38, .51, .61], "observables": ["DM_over_rs", "bao_Hz_rs", "f_sigma8"],
            "joint_data_points": len(rows),
            "qualification": "Published compressed BAO+RSD consensus, not a raw galaxy full-shape likelihood."}


def with_galaxy_growth(base_info, output):
    """Use SDSS joint BAO+RSD instead of overlapping uncorrelated BAO combinations."""
    if "output" in base_info and Path(output).resolve() == Path(base_info["output"]).resolve():
        raise ValueError("Growth extension must use a separate output prefix")
    info = copy.deepcopy(base_info)
    if not any(name.startswith("bao.") for name in info["likelihood"]):
        raise ValueError("Expected a baseline BAO likelihood to replace")
    for name in list(info["likelihood"]):
        if name.startswith("bao."):
            del info["likelihood"][name]
    info["likelihood"][GROWTH_LIKELIHOOD] = None
    info["output"] = str(output)
    info["resume"] = False
    info["force"] = False
    return info
