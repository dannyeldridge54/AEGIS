import logging
import math
import os
import sys
from types import MethodType, SimpleNamespace

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import early_late_spa as E


@pytest.mark.parametrize("ignore_prior", [False, True])
def test_guard_skips_non_reproducible_restart(monkeypatch, ignore_prior):
    from cobaya.samplers.minimize.minimize import Minimize

    checked = {}

    def record_process_results(
        self, results, successes, affine_transform_baselines, transform_matrices
    ):
        checked["successes"] = successes[0]

    monkeypatch.setattr(Minimize, "run", lambda self: None)
    monkeypatch.setattr(Minimize, "process_results", record_process_results)
    E._guard_minimizer()

    class Model:
        def logposterior(self, point, cached=False):
            value = {0: -math.inf, 1: -3.0, 2: -1250.015}[int(point[0])]
            return SimpleNamespace(logpost=value, loglike=value)

    instance = SimpleNamespace(
        method="bobyqa",
        ignore_prior=ignore_prior,
        model=Model(),
        log=logging.getLogger(__name__),
        _scales=np.ones(1),
        _bounds=np.array([[0.0, 2.5]]),
    )

    def inv_affine_transform(self, point):
        return np.clip(
            point * self._scales + self._affine_transform_baseline,
            self._bounds[:, 0],
            self._bounds[:, 1],
        )

    instance.inv_affine_transform = MethodType(inv_affine_transform, instance)

    bad = SimpleNamespace(x=np.array([0.0]), f=100000.0)
    good = SimpleNamespace(x=np.array([0.0]), f=3.0)
    relative_tolerance_false_positive = SimpleNamespace(x=np.array([0.0]), f=1250.0)
    Minimize.process_results(
        instance,
        ([bad, good, relative_tolerance_false_positive],),
        ([True, True, True],),
        ([np.array([0.0]), np.array([1.0]), np.array([2.0])],),
        ([np.eye(1), np.eye(1), np.eye(1)],),
    )

    assert checked["successes"] == [False, True, False]
