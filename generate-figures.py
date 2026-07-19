#!/usr/bin/env python3
"""
AEGIS Paper Figures — Generate publication-quality plots for both papers.
Requires: matplotlib, numpy, json

Figures produced:
  1. convergence.pdf — Score convergence over optimization cycles
  2. h0_comparison.pdf — H0 measurements with torsion prediction
  3. posteriors.pdf — MCMC posterior distributions
  4. blind_test.pdf — Blind BAO prediction residuals
"""
import json, os, sys
import numpy as np

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
except ImportError:
    print('ERROR: matplotlib required. Install with: pip install matplotlib')
    sys.exit(1)

OUT_DIR = 'field-equation-papers/figures'
os.makedirs(OUT_DIR, exist_ok=True)

# Load data
mcmc = {}
try:
    mcmc = json.load(open('mcmc-results.json'))
except Exception:
    print('Warning: mcmc-results.json not found, skipping posterior plots')

state = {}
try:
    state = json.load(open('ufe-state.json'))
except Exception:
    print('Warning: ufe-state.json not found, skipping convergence plot')


# ── Figure 1: Scoreboard Summary ─────────────────────────────────────────────
def fig_scoreboard():
    tasks = {
        'Einstein-Cartan': -1.96,
        'UFE Torsion': 0.0,
        'Energy Cond.': 0.0,
        'Torsion Wave': 0.005,
        'H$_0$ Tension': 2.86,
        'RSD Growth': 3.27,
        'S$_8$ Tension': 11.0,
        'CC Hubble': 15.5,
        'DESI BAO': 13.9,
        'Dark Energy': 14.6,
        'Model Select': 29.4,
        'SNe Pantheon': 166.4,
        'Cross-Domain': 214.9,
        'Combined': 608.0,
    }
    targets = {
        'Einstein-Cartan': 1, 'UFE Torsion': 1, 'Energy Cond.': 1, 'Torsion Wave': 0.01,
        'H$_0$ Tension': 5, 'RSD Growth': 5, 'S$_8$ Tension': 8, 'CC Hubble': 15,
        'DESI BAO': 10, 'Dark Energy': 15, 'Model Select': 20,
        'SNe Pantheon': 50, 'Cross-Domain': 50, 'Combined': 100,
    }

    fig, ax = plt.subplots(figsize=(10, 6))
    names = list(tasks.keys())
    scores = [tasks[n] for n in names]
    targs = [targets[n] for n in names]

    colors = []
    for n in names:
        if tasks[n] <= targets[n]:
            colors.append('#2ecc71')  # green = converged
        elif tasks[n] <= targets[n] * 3:
            colors.append('#f39c12')  # orange = improving
        else:
            colors.append('#e74c3c')  # red = stuck

    y_pos = np.arange(len(names))
    bars = ax.barh(y_pos, [max(0.001, abs(s)) for s in scores], color=colors, edgecolor='white', linewidth=0.5)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(names, fontsize=9)
    ax.set_xscale('log')
    ax.set_xlabel('Cost Function Score (log scale)', fontsize=11)
    ax.set_title('AEGIS UFE Optimization: 15-Task Scoreboard', fontsize=13, fontweight='bold')

    # Target lines
    for i, (name, targ) in enumerate(zip(names, targs)):
        ax.plot(targ, i, 'k|', markersize=15, markeredgewidth=2)

    ax.legend(['Target'], loc='lower right', fontsize=9)
    ax.invert_yaxis()
    ax.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    path = os.path.join(OUT_DIR, 'scoreboard.pdf')
    fig.savefig(path, dpi=150)
    plt.close()
    print(f'  Saved {path}')


# ── Figure 2: H0 Tension Diagram ─────────────────────────────────────────────
def fig_h0():
    measurements = [
        ('Planck 2018 (CMB)', 67.4, 0.5, '#3498db'),
        ('ACT DR6 (CMB)', 67.9, 1.5, '#2980b9'),
        ('TRGB (Freedman)', 69.8, 1.7, '#27ae60'),
        ('CCHP (Freedman 2024)', 69.96, 1.05, '#16a085'),
        ('AEGIS Torsion', 72.15, 1.36, '#e74c3c'),
        ('SH0ES (Riess)', 73.04, 1.04, '#e67e22'),
        ('TDCOSMO (Lensing)', 74.2, 1.6, '#f39c12'),
    ]

    fig, ax = plt.subplots(figsize=(8, 5))
    for i, (label, h0, err, color) in enumerate(measurements):
        ax.errorbar(h0, i, xerr=err, fmt='o', color=color, capsize=5,
                   markersize=8, linewidth=2, capthick=1.5)
        ax.text(h0 + err + 0.5, i, f'{h0:.1f} $\\pm$ {err:.1f}',
               va='center', fontsize=9, color=color)

    # Tension band
    ax.axvspan(67.4 - 0.5, 67.4 + 0.5, alpha=0.08, color='blue', label='Planck 1$\\sigma$')
    ax.axvspan(73.04 - 1.04, 73.04 + 1.04, alpha=0.08, color='orange', label='SH0ES 1$\\sigma$')

    ax.set_yticks(range(len(measurements)))
    ax.set_yticklabels([m[0] for m in measurements], fontsize=10)
    ax.set_xlabel('$H_0$ (km s$^{-1}$ Mpc$^{-1}$)', fontsize=12)
    ax.set_title('Hubble Constant Measurements & Torsion Resolution', fontsize=13, fontweight='bold')
    ax.set_xlim(63, 80)
    ax.invert_yaxis()
    ax.legend(loc='lower right', fontsize=9)
    ax.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    path = os.path.join(OUT_DIR, 'h0_tension.pdf')
    fig.savefig(path, dpi=150)
    plt.close()
    print(f'  Saved {path}')


# ── Figure 3: MCMC Posteriors ─────────────────────────────────────────────────
def fig_posteriors():
    if 'h0-tension' not in mcmc:
        print('  Skipping posteriors: no MCMC data for h0-tension')
        return

    h0_data = mcmc['h0-tension']
    params = list(h0_data.keys())

    fig, axes = plt.subplots(1, len(params), figsize=(3.5 * len(params), 3.5))
    if len(params) == 1:
        axes = [axes]

    for ax, param in zip(axes, params):
        d = h0_data[param]
        mean, std = d['mean'], d['std']
        lo68, hi68 = d['lo68'], d['hi68']

        # Simulate distribution from stats
        x = np.linspace(mean - 4 * std, mean + 4 * std, 200)
        y = np.exp(-0.5 * ((x - mean) / std) ** 2)

        ax.fill_between(x, y, alpha=0.3, color='#3498db')
        ax.axvline(mean, color='#e74c3c', linewidth=1.5, label=f'Best: {mean:.3f}')
        ax.axvline(lo68, color='gray', linewidth=1, linestyle='--', label=f'68% CI')
        ax.axvline(hi68, color='gray', linewidth=1, linestyle='--')
        ax.set_xlabel(param, fontsize=11)
        ax.set_ylabel('Posterior', fontsize=10)
        ax.legend(fontsize=8)
        ax.set_yticks([])

    fig.suptitle('H$_0$ Tension Resolver: Parameter Posteriors (MCMC)', fontsize=12, fontweight='bold')
    plt.tight_layout()
    path = os.path.join(OUT_DIR, 'posteriors.pdf')
    fig.savefig(path, dpi=150)
    plt.close()
    print(f'  Saved {path}')


# ── Figure 4: Blind Prediction Residuals ──────────────────────────────────────
def fig_blind():
    # Observed DESI BAO data
    bao_data = [
        {'z': 0.295, 'type': 'DV/rs', 'obs': 7.93, 'sigma': 0.15, 'pred': 7.52},
        {'z': 0.510, 'type': 'DM/rs', 'obs': 13.62, 'sigma': 0.25, 'pred': 12.67},
        {'z': 0.510, 'type': 'DH/rs', 'obs': 20.98, 'sigma': 0.61, 'pred': 21.92},
        {'z': 0.706, 'type': 'DM/rs', 'obs': 16.85, 'sigma': 0.32, 'pred': 16.75},
        {'z': 0.706, 'type': 'DH/rs', 'obs': 20.08, 'sigma': 0.60, 'pred': 19.75},
        {'z': 0.930, 'type': 'DM/rs', 'obs': 21.71, 'sigma': 0.28, 'pred': 20.91},
        {'z': 0.930, 'type': 'DH/rs', 'obs': 17.88, 'sigma': 0.35, 'pred': 17.49},
        {'z': 1.317, 'type': 'DM/rs', 'obs': 27.79, 'sigma': 0.69, 'pred': 27.03},
        {'z': 1.317, 'type': 'DH/rs', 'obs': 13.82, 'sigma': 0.42, 'pred': 14.24},
        {'z': 2.330, 'type': 'DM/rs', 'obs': 39.71, 'sigma': 0.94, 'pred': 38.42},
        {'z': 2.330, 'type': 'DH/rs', 'obs': 8.52, 'sigma': 0.17, 'pred': 8.88},
    ]

    pulls = [(d['pred'] - d['obs']) / d['sigma'] for d in bao_data]
    labels = [f"z={d['z']} {d['type']}" for d in bao_data]

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ['#2ecc71' if abs(p) < 1 else '#f39c12' if abs(p) < 2 else '#e74c3c' for p in pulls]
    y_pos = np.arange(len(pulls))
    ax.barh(y_pos, pulls, color=colors, edgecolor='white', linewidth=0.5)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel('Pull (predicted - observed) / $\\sigma$', fontsize=11)
    ax.set_title('Blind BAO Prediction Residuals (trained on CC+SNe+CMB$\\theta^*$ only)',
                fontsize=11, fontweight='bold')

    # Reference bands
    ax.axvspan(-1, 1, alpha=0.1, color='green', label='$<1\\sigma$')
    ax.axvspan(-2, -1, alpha=0.05, color='orange')
    ax.axvspan(1, 2, alpha=0.05, color='orange', label='$1$-$2\\sigma$')
    ax.axvline(0, color='black', linewidth=0.8)

    ax.legend(loc='lower right', fontsize=9)
    ax.invert_yaxis()
    ax.set_xlim(-4.5, 4.5)
    ax.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    path = os.path.join(OUT_DIR, 'blind_test.pdf')
    fig.savefig(path, dpi=150)
    plt.close()
    print(f'  Saved {path}')


# ── Generate all ──────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print('AEGIS Paper Figure Generator')
    fig_scoreboard()
    fig_h0()
    fig_posteriors()
    fig_blind()
    print(f'\nAll figures saved to {OUT_DIR}/')
