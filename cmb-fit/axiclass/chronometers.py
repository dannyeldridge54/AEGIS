"""Separate BC03 chronometer likelihood using the author's MM20 covariance recipe."""
import copy
from pathlib import Path

import numpy as np
from cobaya.likelihood import Likelihood


def load_chronometers(data_path):
    root = Path(data_path)
    data = np.loadtxt(root / "HzTable_MM_BC03.dat", delimiter=",", usecols=(0, 1, 2))
    systematic = np.loadtxt(root / "data_MM20.dat")
    if (data.ndim != 2 or data.shape[1] != 3 or len(data) == 0
            or not np.isfinite(data).all() or np.any(data <= 0)):
        raise ValueError("Invalid BC03 chronometer measurements")
    if (systematic.ndim != 2 or systematic.shape[1] != 5
            or not np.isfinite(systematic).all() or np.any(systematic < 0)
            or np.any(np.diff(systematic[:, 0]) <= 0)):
        raise ValueError("Invalid MM20 systematic interpolation table")
    z, measured, errors = data.T
    if np.any(np.diff(z) <= 0):
        raise ValueError("Chronometer redshifts must be strictly increasing")
    # Match the author's np.interp recipe: endpoint systematics are held constant
    # outside the tabulated range. This convention is a documented limitation,
    # not evidence that the high-z systematics are known to be constant.
    with np.errstate(over="raise", invalid="raise", divide="raise"):
        try:
            imf = measured * (np.interp(z, systematic[:, 0], systematic[:, 1]) / 100)
            sps_ooo = measured * (np.interp(z, systematic[:, 0], systematic[:, 4]) / 100)
            # The author's notebook uses these two terms, not all alternative model columns.
            covariance = np.diag(errors ** 2) + np.outer(imf, imf) + np.outer(sps_ooo, sps_ooo)
        except FloatingPointError as error:
            raise ValueError("Chronometer covariance construction overflowed") from error
    if not np.isfinite(covariance).all():
        raise ValueError("Chronometer covariance must be finite")
    np.linalg.cholesky(covariance)
    return z, measured, covariance


def chronometer_chi2(prediction, measured, covariance):
    prediction = np.asarray(prediction, dtype=float)
    measured = np.asarray(measured, dtype=float)
    covariance = np.asarray(covariance, dtype=float)
    if (prediction.shape != measured.shape or measured.ndim != 1 or measured.size == 0
            or covariance.shape != (len(measured), len(measured))
            or not np.isfinite(prediction).all() or np.any(prediction <= 0)
            or not np.isfinite(measured).all() or np.any(measured <= 0)
            or not np.isfinite(covariance).all()
            or not np.allclose(covariance, covariance.T, rtol=1e-12, atol=0)):
        raise ValueError("Invalid chronometer prediction or covariance")
    with np.errstate(over="raise", invalid="raise", divide="raise"):
        try:
            residual = np.linalg.solve(np.linalg.cholesky(covariance), measured - prediction)
            chi2 = float(residual @ residual)
        except FloatingPointError as error:
            raise ValueError("Chronometer chi-square calculation overflowed") from error
    if not np.isfinite(chi2):
        raise ValueError("Chronometer chi-square must be finite")
    return chi2


class CosmicChronometers(Likelihood):
    data_path: str

    def initialize(self):
        self.redshifts, self.measured, self.covariance = load_chronometers(self.data_path)

    def get_requirements(self):
        return {"Hubble": {"z": self.redshifts}}

    def logp(self, **params_values):
        prediction = self.provider.get_Hubble(self.redshifts, units="km/s/Mpc")
        return -0.5 * chronometer_chi2(prediction, self.measured, self.covariance)


def with_chronometers(base_info, data_path, output):
    """Prepare a separately archived extension without starting a sampler."""
    if "output" in base_info:
        baseline = Path(base_info["output"]).resolve()
        target = Path(output).resolve()
        if target == baseline or baseline in target.parents or target in baseline.parents:
            raise ValueError("Chronometers must use a separate output prefix")
    load_chronometers(data_path)
    info = copy.deepcopy(base_info)
    name = "aegis_cosmic_chronometers_bc03_mm20"
    if name in info["likelihood"]:
        raise ValueError("Chronometer likelihood is already included")
    info["likelihood"][name] = {"external": CosmicChronometers, "data_path": str(data_path)}
    info["output"] = str(output)
    info["resume"] = False
    info["force"] = False
    return info
