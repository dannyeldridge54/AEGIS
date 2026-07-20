"""
CMA-ES (Covariance Matrix Adaptation Evolution Strategy) engine.

Uses the `cma` package for production runs, with a pure-numpy fallback.
This is the primary optimizer in AEGIS — handles high-dimensional
parameter spaces with correlated parameters.
"""

import numpy as np
from typing import Callable, Dict, List, Optional, Tuple

try:
    import cma as _cma
    HAS_CMA = True
except ImportError:
    HAS_CMA = False


class CMAESEngine:
    """CMA-ES optimizer for UFE task fitting."""

    def __init__(self, task: dict, sigma0: float = 0.3, popsize: int = None,
                 max_evals: int = 100_000, seed: int = None):
        self.task = task
        self.params = task['parameters']
        self.dim = len(self.params)
        self.sigma0 = sigma0
        self.popsize = popsize or (4 + int(3 * np.log(self.dim))) * 2
        self.max_evals = max_evals
        self.seed = seed

        # Bounds
        self.lower = np.array([p['min'] for p in self.params])
        self.upper = np.array([p['max'] for p in self.params])
        self.names = [p['name'] for p in self.params]

        # State
        self.best_x = None
        self.best_val = np.inf
        self.history = []
        self.n_evals = 0

    def _vec_to_dict(self, x: np.ndarray) -> dict:
        """Convert parameter vector to named dict."""
        return {self.names[i]: float(x[i]) for i in range(self.dim)}

    def _evaluate(self, x: np.ndarray) -> float:
        """Evaluate objective with bounds checking."""
        # Clip to bounds
        x = np.clip(x, self.lower, self.upper)
        p = self._vec_to_dict(x)
        val = self.task['evaluate'](p)
        self.n_evals += 1
        if val < self.best_val:
            self.best_val = val
            self.best_x = x.copy()
        return val

    def run(self, verbose: bool = True) -> dict:
        """Run CMA-ES optimization."""
        x0 = (self.lower + self.upper) / 2.0
        sigma_scaled = self.sigma0 * np.mean(self.upper - self.lower)

        if HAS_CMA:
            return self._run_cma(x0, sigma_scaled, verbose)
        else:
            return self._run_fallback(x0, verbose)

    def _run_cma(self, x0, sigma, verbose):
        """Run using the cma package (production quality)."""
        opts = {
            'bounds': [self.lower.tolist(), self.upper.tolist()],
            'maxfevals': self.max_evals,
            'popsize': self.popsize,
            'verbose': -9 if not verbose else 1,
            'tolfun': 1e-8,
        }
        if self.seed is not None:
            opts['seed'] = self.seed

        es = _cma.CMAEvolutionStrategy(x0, sigma, opts)

        while not es.stop():
            solutions = es.ask()
            values = [self._evaluate(np.array(x)) for x in solutions]
            es.tell(solutions, values)
            self.history.append(self.best_val)

            if verbose and es.countiter % 50 == 0:
                print(f"  Gen {es.countiter}: best chi2 = {self.best_val:.4f}  "
                      f"({self.n_evals} evals)")

        return self._result()

    def _run_fallback(self, x0, verbose):
        """Pure numpy CMA-ES fallback (simplified)."""
        dim = self.dim
        mean = x0.copy()
        sigma = self.sigma0 * np.mean(self.upper - self.lower) * 0.5
        C = np.eye(dim)
        ps = np.zeros(dim)

        mu = self.popsize // 2
        weights = np.log(mu + 0.5) - np.log(np.arange(1, mu + 1))
        weights /= weights.sum()
        mueff = 1.0 / (weights ** 2).sum()

        cs = (mueff + 2) / (dim + mueff + 5)
        ds = 1 + 2 * max(0, np.sqrt((mueff - 1) / (dim + 1)) - 1) + cs
        cc = (4 + mueff / dim) / (dim + 4 + 2 * mueff / dim)
        c1 = 2 / ((dim + 1.3) ** 2 + mueff)
        cmu_val = min(1 - c1, 2 * (mueff - 2 + 1 / mueff) / ((dim + 2) ** 2 + mueff))
        chiN = np.sqrt(dim) * (1 - 1 / (4 * dim) + 1 / (21 * dim ** 2))

        pc = np.zeros(dim)
        gen = 0

        while self.n_evals < self.max_evals:
            # Sample population
            try:
                L = np.linalg.cholesky(C)
            except np.linalg.LinAlgError:
                C = np.eye(dim)
                L = np.eye(dim)

            pop = []
            vals = []
            for _ in range(self.popsize):
                z = np.random.randn(dim)
                x = mean + sigma * L @ z
                x = np.clip(x, self.lower, self.upper)
                v = self._evaluate(x)
                pop.append((x, z, v))
                vals.append(v)

            # Sort by fitness
            idx = np.argsort(vals)
            pop = [pop[i] for i in idx]

            # Update mean
            old_mean = mean.copy()
            mean = sum(weights[i] * pop[i][0] for i in range(mu))

            # Update evolution paths
            delta = (mean - old_mean) / sigma
            ps = (1 - cs) * ps + np.sqrt(cs * (2 - cs) * mueff) * np.linalg.solve(L, delta)
            sigma *= np.exp(cs / ds * (np.linalg.norm(ps) / chiN - 1))

            # Update covariance
            pc = (1 - cc) * pc + np.sqrt(cc * (2 - cc) * mueff) * delta
            C = ((1 - c1 - cmu_val) * C
                 + c1 * np.outer(pc, pc)
                 + cmu_val * sum(weights[i] * np.outer(pop[i][0] - old_mean, pop[i][0] - old_mean)
                                  for i in range(mu)) / sigma ** 2)

            # Symmetrize
            C = (C + C.T) / 2
            np.fill_diagonal(C, np.maximum(np.diag(C), 1e-20))

            self.history.append(self.best_val)
            gen += 1

            if verbose and gen % 50 == 0:
                print(f"  Gen {gen}: best chi2 = {self.best_val:.4f}  "
                      f"({self.n_evals} evals)")

            # Convergence
            if sigma < 1e-10:
                break

        return self._result()

    def _result(self) -> dict:
        """Format result dict."""
        params = self._vec_to_dict(self.best_x) if self.best_x is not None else {}
        return {
            'chi2': self.best_val,
            'params': params,
            'n_evals': self.n_evals,
            'task_id': self.task['id'],
            'task_name': self.task['name'],
            'history': self.history,
        }


class SeekerEngine:
    """Seeker: exploratory random search for escaping local minima.

    Complements CMA-ES by randomly sampling the parameter space
    and injecting good solutions. Equivalent to the JS Seeker engine.
    """

    def __init__(self, task: dict, n_samples: int = 10_000, seed: int = None):
        self.task = task
        self.params = task['parameters']
        self.dim = len(self.params)
        self.n_samples = n_samples
        self.names = [p['name'] for p in self.params]
        self.lower = np.array([p['min'] for p in self.params])
        self.upper = np.array([p['max'] for p in self.params])
        if seed is not None:
            np.random.seed(seed)

    def search(self, verbose: bool = True) -> dict:
        """Run random search, return best result."""
        best_val = np.inf
        best_x = None

        for i in range(self.n_samples):
            x = self.lower + np.random.rand(self.dim) * (self.upper - self.lower)
            p = {self.names[j]: float(x[j]) for j in range(self.dim)}
            val = self.task['evaluate'](p)
            if val < best_val:
                best_val = val
                best_x = x.copy()

            if verbose and (i + 1) % 2000 == 0:
                print(f"  Seeker {i + 1}/{self.n_samples}: best = {best_val:.4f}")

        params = {self.names[j]: float(best_x[j]) for j in range(self.dim)}
        return {
            'chi2': best_val,
            'params': params,
            'n_evals': self.n_samples,
            'task_id': self.task['id'],
        }
