"""
MCMC engine using emcee (affine-invariant ensemble sampler).

Produces publishable posterior chains with proper convergence diagnostics.
This addresses the key critique: "release MCMC chains."
"""

import numpy as np
from typing import Dict, List, Optional, Tuple

try:
    import emcee
    HAS_EMCEE = True
except ImportError:
    HAS_EMCEE = False

try:
    import corner
    HAS_CORNER = True
except ImportError:
    HAS_CORNER = False


class MCMCEngine:
    """Ensemble MCMC sampler for UFE posterior estimation."""

    def __init__(self, task: dict, nwalkers: int = None, nsteps: int = 5000,
                 burnin: int = 1000, seed: int = 42):
        if not HAS_EMCEE:
            raise ImportError("emcee required: pip install emcee")

        self.task = task
        self.params = task['parameters']
        self.dim = len(self.params)
        self.nwalkers = nwalkers or max(2 * self.dim + 2, 32)
        self.nsteps = nsteps
        self.burnin = burnin
        self.seed = seed

        self.names = [p['name'] for p in self.params]
        self.lower = np.array([p['min'] for p in self.params])
        self.upper = np.array([p['max'] for p in self.params])

        self.sampler = None
        self.chains = None

    def _log_prior(self, theta: np.ndarray) -> float:
        """Uniform prior within bounds."""
        if np.all((theta >= self.lower) & (theta <= self.upper)):
            return 0.0
        return -np.inf

    def _log_likelihood(self, theta: np.ndarray) -> float:
        """Log-likelihood = -χ²/2."""
        p = {self.names[i]: float(theta[i]) for i in range(self.dim)}
        chi2 = self.task['evaluate'](p)
        if not np.isfinite(chi2):
            return -np.inf
        return -0.5 * chi2

    def _log_posterior(self, theta: np.ndarray) -> float:
        """Log-posterior = log-prior + log-likelihood."""
        lp = self._log_prior(theta)
        if not np.isfinite(lp):
            return -np.inf
        return lp + self._log_likelihood(theta)

    def run(self, initial_guess: dict = None, verbose: bool = True) -> dict:
        """Run MCMC sampling.

        Args:
            initial_guess: Dict of parameter values to initialize walkers around.
                          If None, uses center of bounds.
            verbose: Print progress updates.

        Returns:
            Dict with chains, stats, and convergence diagnostics.
        """
        np.random.seed(self.seed)

        # Initialize walkers
        if initial_guess:
            x0 = np.array([initial_guess.get(n, (lo + hi) / 2)
                           for n, lo, hi in zip(self.names, self.lower, self.upper)])
        else:
            x0 = (self.lower + self.upper) / 2.0

        # Small perturbation around initial guess
        spread = 0.01 * (self.upper - self.lower)
        pos = x0 + spread * np.random.randn(self.nwalkers, self.dim)
        pos = np.clip(pos, self.lower + 1e-10, self.upper - 1e-10)

        # Run sampler
        self.sampler = emcee.EnsembleSampler(
            self.nwalkers, self.dim, self._log_posterior
        )

        if verbose:
            print(f"Running MCMC: {self.nwalkers} walkers × {self.nsteps} steps")
            print(f"Parameters: {', '.join(self.names)}")

        self.sampler.run_mcmc(pos, self.nsteps, progress=verbose)

        # Extract chains (post burn-in)
        self.chains = self.sampler.get_chain(discard=self.burnin, flat=True)

        return self._analyze()

    def _analyze(self) -> dict:
        """Compute posterior statistics and convergence diagnostics."""
        chains = self.chains
        stats = {}

        for i, name in enumerate(self.names):
            col = chains[:, i]
            median = np.median(col)
            q16, q84 = np.percentile(col, [16, 84])
            mean = np.mean(col)
            std = np.std(col)
            stats[name] = {
                'mean': float(mean),
                'std': float(std),
                'median': float(median),
                'lower_1sigma': float(q16),
                'upper_1sigma': float(q84),
                'error_minus': float(median - q16),
                'error_plus': float(q84 - median),
            }

        # Autocorrelation time (convergence diagnostic)
        try:
            tau = self.sampler.get_autocorr_time(quiet=True)
            converged = np.all(self.nsteps / tau > 50)
        except Exception:
            tau = np.full(self.dim, np.nan)
            converged = False

        # Best-fit (MAP)
        log_prob = self.sampler.get_log_prob(flat=True, discard=self.burnin)
        best_idx = np.argmax(log_prob)
        best_params = {self.names[i]: float(chains[best_idx, i])
                       for i in range(self.dim)}
        best_chi2 = -2.0 * log_prob[best_idx]

        return {
            'task_id': self.task['id'],
            'task_name': self.task['name'],
            'stats': stats,
            'best_fit': best_params,
            'best_chi2': float(best_chi2),
            'n_samples': len(chains),
            'n_walkers': self.nwalkers,
            'n_steps': self.nsteps,
            'burnin': self.burnin,
            'autocorr_time': {self.names[i]: float(tau[i]) for i in range(self.dim)},
            'converged': bool(converged),
            'acceptance_fraction': float(np.mean(self.sampler.acceptance_fraction)),
        }

    def corner_plot(self, filename: str = None, **kwargs):
        """Generate corner plot of posterior distributions."""
        if not HAS_CORNER:
            raise ImportError("corner required: pip install corner")
        if self.chains is None:
            raise RuntimeError("Run MCMC first")

        import matplotlib.pyplot as plt

        labels = [_latex_label(n) for n in self.names]
        fig = corner.corner(
            self.chains,
            labels=labels,
            quantiles=[0.16, 0.5, 0.84],
            show_titles=True,
            title_kwargs={"fontsize": 12},
            **kwargs,
        )
        fig.suptitle(f"AEGIS MCMC: {self.task['name']}", fontsize=14, y=1.02)

        if filename:
            fig.savefig(filename, dpi=150, bbox_inches='tight')
            print(f"Saved corner plot: {filename}")
        return fig

    def save_chains(self, filename: str):
        """Save chains to numpy file for reproducibility."""
        if self.chains is None:
            raise RuntimeError("Run MCMC first")
        np.savez(filename,
                 chains=self.chains,
                 names=self.names,
                 task_id=self.task['id'])
        print(f"Saved {len(self.chains)} samples to {filename}")


def _latex_label(name: str) -> str:
    """Convert parameter name to LaTeX label."""
    labels = {
        'H0': r'$H_0$',
        'omega_m': r'$\Omega_m$',
        'omega_r': r'$\Omega_r$',
        'beta': r'$\beta$',
        'beta0': r'$\beta_0$',
        'beta1': r'$\beta_1$',
        'sigma8': r'$\sigma_8$',
        'gamma': r'$\gamma$',
        'rs': r'$r_s$',
        'M_B': r'$M_B$',
        'w0': r'$w_0$',
        'wa': r'$w_a$',
    }
    return labels.get(name, name)
