# AEGIS Python — UFE Cosmology Framework

Python implementation of AEGIS (Autonomous Engine for Generalized Iterative Solving) for UFE (Unified Field Equation) cosmological analysis.

## Quick Start

```bash
cd python
pip install -e .
```

## Usage

```bash
# List all 16 tasks
aegis list-tasks

# Run CMA-ES optimization on a single task
aegis run --task sne-pantheon-fit --max-evals 50000

# Run MCMC posterior sampling with corner plot
aegis mcmc --task h0-tension --nsteps 10000 --corner h0_posterior.png

# ΛCDM recovery validation
aegis validate --task sne-pantheon-fit

# Run all 16 tasks
aegis run-all --output results.json
```

## Python API

```python
from aegis.tasks.definitions import get_task, ALL_TASKS
from aegis.engines.cmaes import CMAESEngine
from aegis.engines.mcmc import MCMCEngine

# Get a task
task = get_task('sne-pantheon-fit')

# Optimize with CMA-ES
engine = CMAESEngine(task, max_evals=50000)
result = engine.run()
print(f"Best χ² = {result['chi2']:.4f}")
print(f"Best params: {result['params']}")

# MCMC posterior sampling
mcmc = MCMCEngine(task, nsteps=10000)
result = mcmc.run(initial_guess=result['params'])
mcmc.corner_plot('posterior.png')
mcmc.save_chains('chains.npz')
```

## UFE Physics

The Unified Field Equation modifies the Friedmann equation with spacetime torsion:

```
H²(z) = H₀² [ Ωr(1+z)⁴ + Ωm(1+β(z))(1+z)³ + ΩΛ ]
```

Where the torsion coupling evolves with redshift:
```
β(z) = β₀ + β₁·z/(1+z)
```

## Tasks

16 optimization tasks testing UFE against real observational data:
- **Cosmic Chronometers**: 31 direct H(z) measurements
- **DESI BAO**: Baryon acoustic oscillation distances
- **Pantheon+ SNe**: 1701 Type Ia supernovae with full STAT+SYS covariance
- **H₀ Tension**: Reconciling Planck vs SH0ES
- **RSD Growth**: Structure formation under torsion
- **Energy Conditions**: Physical viability
- **S₈ Tension**: Weak lensing vs CMB
- **Dark Energy EoS**: Torsion vs w₀wₐCDM
- **Combined Multi-Survey**: Joint CC+BAO+SNe+RSD
- **Model Selection**: ΔBIC vs ΛCDM
- **UFE Emergence**: Quantum-to-cosmos pathway
- And 5 more theoretical validation tasks

## Data

Uses official Pantheon+ data release (Brout et al. 2022) with full statistical + systematic covariance matrix (1701×1701), binned to 40 redshift bins with proper covariance propagation.
