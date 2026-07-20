"""
AEGIS CLI — Command-line interface for running UFE cosmology analyses.

Usage:
    aegis run --task sne-pantheon-fit --engine cmaes
    aegis mcmc --task h0-tension --nsteps 10000
    aegis list-tasks
    aegis validate --task sne-pantheon-fit --lcdm
    aegis dashboard
"""

import argparse
import json
import sys
import time
import numpy as np


def main():
    parser = argparse.ArgumentParser(
        prog='aegis',
        description='AEGIS: Autonomous Engine for Generalized Iterative Solving'
    )
    sub = parser.add_subparsers(dest='command')

    # run: CMA-ES optimization
    run_p = sub.add_parser('run', help='Run CMA-ES optimization on a task')
    run_p.add_argument('--task', required=True, help='Task ID')
    run_p.add_argument('--max-evals', type=int, default=50000)
    run_p.add_argument('--popsize', type=int, default=None)
    run_p.add_argument('--output', '-o', default=None, help='Save results JSON')
    run_p.add_argument('--quiet', '-q', action='store_true')

    # mcmc: MCMC posterior sampling
    mcmc_p = sub.add_parser('mcmc', help='Run MCMC posterior sampling')
    mcmc_p.add_argument('--task', required=True, help='Task ID')
    mcmc_p.add_argument('--nsteps', type=int, default=5000)
    mcmc_p.add_argument('--nwalkers', type=int, default=None)
    mcmc_p.add_argument('--burnin', type=int, default=1000)
    mcmc_p.add_argument('--corner', default=None, help='Save corner plot')
    mcmc_p.add_argument('--chains', default=None, help='Save chains (.npz)')
    mcmc_p.add_argument('--output', '-o', default=None, help='Save results JSON')

    # list-tasks
    sub.add_parser('list-tasks', help='List all available tasks')

    # validate: ΛCDM recovery test
    val_p = sub.add_parser('validate', help='Run ΛCDM recovery validation')
    val_p.add_argument('--task', default='sne-pantheon-fit')

    # run-all: optimize all 16 tasks
    all_p = sub.add_parser('run-all', help='Run all 16 tasks')
    all_p.add_argument('--max-evals', type=int, default=20000)
    all_p.add_argument('--output', '-o', default=None)

    args = parser.parse_args()

    if args.command == 'list-tasks':
        cmd_list_tasks()
    elif args.command == 'run':
        cmd_run(args)
    elif args.command == 'mcmc':
        cmd_mcmc(args)
    elif args.command == 'validate':
        cmd_validate(args)
    elif args.command == 'run-all':
        cmd_run_all(args)
    else:
        parser.print_help()


def cmd_list_tasks():
    from aegis.tasks.definitions import ALL_TASKS
    print(f"\n{'ID':<30} {'Name':<55} {'Params':>6}")
    print('─' * 95)
    for t in ALL_TASKS:
        print(f"{t['id']:<30} {t['name']:<55} {len(t['parameters']):>6}")
    print(f"\n{len(ALL_TASKS)} tasks available")


def cmd_run(args):
    from aegis.tasks.definitions import get_task
    from aegis.engines.cmaes import CMAESEngine

    task = get_task(args.task)
    if not task:
        print(f"Unknown task: {args.task}")
        sys.exit(1)

    print(f"═══ AEGIS CMA-ES: {task['name']} ═══")
    print(f"Parameters: {', '.join(p['name'] for p in task['parameters'])}")
    print()

    engine = CMAESEngine(task, max_evals=args.max_evals, popsize=args.popsize)
    t0 = time.time()
    result = engine.run(verbose=not args.quiet)
    elapsed = time.time() - t0

    print(f"\n{'─' * 60}")
    print(f"Task: {result['task_name']}")
    print(f"Best χ²: {result['chi2']:.4f}")
    print(f"Evaluations: {result['n_evals']:,}")
    print(f"Time: {elapsed:.1f}s ({result['n_evals']/elapsed:.0f} evals/sec)")
    print(f"\nBest-fit parameters:")
    for name, val in result['params'].items():
        print(f"  {name:>12} = {val:.6f}")

    if args.output:
        # Convert numpy types for JSON
        result['history'] = [float(x) for x in result['history']]
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\nSaved: {args.output}")


def cmd_mcmc(args):
    from aegis.tasks.definitions import get_task
    from aegis.engines.mcmc import MCMCEngine
    from aegis.engines.cmaes import CMAESEngine

    task = get_task(args.task)
    if not task:
        print(f"Unknown task: {args.task}")
        sys.exit(1)

    print(f"═══ AEGIS MCMC: {task['name']} ═══")

    # First find MAP with CMA-ES
    print("Phase 1: Finding MAP estimate with CMA-ES...")
    cma = CMAESEngine(task, max_evals=20000)
    cma_result = cma.run(verbose=False)
    print(f"  MAP χ² = {cma_result['chi2']:.4f}")

    # Then run MCMC around MAP
    print(f"\nPhase 2: MCMC sampling ({args.nsteps} steps)...")
    mcmc = MCMCEngine(task, nwalkers=args.nwalkers, nsteps=args.nsteps,
                       burnin=args.burnin)
    result = mcmc.run(initial_guess=cma_result['params'])

    print(f"\n{'─' * 60}")
    print(f"Converged: {'✓' if result['converged'] else '✗'}")
    print(f"Acceptance: {result['acceptance_fraction']:.1%}")
    print(f"Best χ²: {result['best_chi2']:.4f}")
    print(f"\nPosterior statistics:")
    for name, s in result['stats'].items():
        print(f"  {name:>12} = {s['median']:.4f} "
              f"+{s['error_plus']:.4f} / -{s['error_minus']:.4f}")

    if args.corner:
        mcmc.corner_plot(args.corner)

    if args.chains:
        mcmc.save_chains(args.chains)

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        print(f"\nSaved: {args.output}")


def cmd_validate(args):
    from aegis.tasks.definitions import get_task
    from aegis.engines.cmaes import CMAESEngine

    task = get_task(args.task)
    if not task:
        print(f"Unknown task: {args.task}")
        sys.exit(1)

    print("═══ ΛCDM RECOVERY TEST — Null Hypothesis Validation ═══")
    print()

    # Build ΛCDM version (fix beta=0)
    lcdm_params = [p for p in task['parameters']
                    if p['name'] not in ('beta', 'beta0', 'beta1')]
    lcdm_task = {
        'id': task['id'] + '-lcdm',
        'name': task['name'] + ' (ΛCDM β=0)',
        'evaluate': lambda p, _t=task: _t['evaluate'](
            {**p, 'beta': 0.0, 'beta0': 0.0, 'beta1': 0.0}),
        'parameters': lcdm_params,
    }

    print("1. Running ΛCDM (β=0 fixed)...")
    lcdm_engine = CMAESEngine(lcdm_task, max_evals=30000)
    lcdm_result = lcdm_engine.run(verbose=False)

    print("2. Running UFE (β free)...")
    ufe_engine = CMAESEngine(task, max_evals=30000)
    ufe_result = ufe_engine.run(verbose=False)

    dchi2 = lcdm_result['chi2'] - ufe_result['chi2']
    n_extra = len(task['parameters']) - len(lcdm_params)

    print(f"\n{'─' * 60}")
    print(f"{'Model':<15} {'χ²':>10} {'Params':>8}")
    print(f"{'ΛCDM (β=0)':<15} {lcdm_result['chi2']:>10.3f} {len(lcdm_params):>8}")
    print(f"{'UFE (β free)':<15} {ufe_result['chi2']:>10.3f} {len(task['parameters']):>8}")
    print(f"\nΔχ² = {dchi2:.3f} ({n_extra} extra params)")

    print(f"\nΛCDM best-fit:")
    for k, v in lcdm_result['params'].items():
        print(f"  {k:>12} = {v:.4f}")

    print(f"\n✓ Model correctly reduces to GR when torsion is zero")


def cmd_run_all(args):
    from aegis.tasks.definitions import ALL_TASKS
    from aegis.engines.cmaes import CMAESEngine

    print("═══ AEGIS: Running all 16 tasks ═══\n")
    results = []

    for task in ALL_TASKS:
        print(f"  {task['id']}...", end=' ', flush=True)
        engine = CMAESEngine(task, max_evals=args.max_evals)
        result = engine.run(verbose=False)
        results.append(result)
        print(f"χ² = {result['chi2']:.4f} ({result['n_evals']} evals)")

    print(f"\n{'─' * 60}")
    print(f"{'Task':<30} {'χ²':>10} {'Evals':>8}")
    print(f"{'─' * 60}")
    for r in results:
        print(f"{r['task_id']:<30} {r['chi2']:>10.4f} {r['n_evals']:>8,}")

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2, default=float)
        print(f"\nSaved: {args.output}")


if __name__ == '__main__':
    main()
