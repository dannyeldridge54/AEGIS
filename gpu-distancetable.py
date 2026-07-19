#!/usr/bin/env python3
"""
AEGIS GPU Distance Table Generator
Precomputes comoving distances on a 3D grid (H0, omega_m, beta) × z-values.
Writes binary Float64 lookup tables that Node.js can mmap for ~1µs/eval interpolation.

Usage:
  python gpu-distancetable.py [--gpu] [--output dist-tables/]
"""
import sys, os, time, struct, json
import numpy as np

try:
    import cupy as cp
    GPU = True
    DEVICE = cp.cuda.runtime.getDeviceProperties(0)['name'].decode()
except Exception:
    cp = np  # fallback
    GPU = False
    DEVICE = 'CPU'

C_LIGHT = 299792.458  # km/s
OMEGA_R0 = 9.34e-5

# ── Grid definition ──────────────────────────────────────────────────────────
# Covers the full parameter ranges used by all tasks
GRID = {
    'H0':      {'min': 55, 'max': 105, 'steps': 80},
    'omega_m': {'min': 0.10, 'max': 0.50, 'steps': 60},
    'beta':    {'min': -0.55, 'max': 0.55, 'steps': 50},
}

# All unique z-values from tasks (sorted)
Z_VALUES = sorted(list(set([
    # CC data
    0.07, 0.09, 0.12, 0.17, 0.1791, 0.1993, 0.2, 0.27, 0.28, 0.3519,
    0.3802, 0.4, 0.4004, 0.4247, 0.4497, 0.4783, 0.48, 0.593, 0.68,
    0.75, 0.781, 0.875, 0.88, 0.9, 1.037, 1.3, 1.363, 1.43, 1.53, 1.75, 1.965,
    # DESI BAO
    0.295, 0.510, 0.706, 0.930, 1.317, 2.330,
    # SNe
    0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.20, 0.30, 0.40, 0.50,
    0.60, 0.80, 1.00, 1.20, 1.50, 1.80,
    # BAO points from H0 tension
    0.38, 0.51, 0.61,
])))

def compute_table(z_arr, H0_arr, om_arr, beta_arr):
    """Compute comoving distances: (nH, nO, nB, nZ) grid — fully vectorized on GPU."""
    xp = cp if GPU else np
    
    z = xp.asarray(z_arr, dtype=xp.float64)        # (nZ,)
    H0 = xp.asarray(H0_arr, dtype=xp.float64)      # (nH,)
    om = xp.asarray(om_arr, dtype=xp.float64)       # (nO,)
    beta = xp.asarray(beta_arr, dtype=xp.float64)   # (nB,)
    
    nZ = len(z)
    nH = len(H0)
    nO = len(om)
    nB = len(beta)
    steps = 200
    
    # Allocate result: (nH, nO, nB, nZ)
    result = xp.zeros((nH, nO, nB, nZ), dtype=xp.float64)
    
    # Process each z-value (avoids building massive 5D arrays)
    t_frac = xp.linspace(0.0, 1.0, steps + 1, dtype=xp.float64)
    
    for iz in range(nZ):
        zval = float(z[iz])
        if zval <= 0:
            continue
        
        ln_zp1 = np.log(1.0 + zval)
        # z-grid for this redshift: (steps+1,)
        z_grid = xp.exp(ln_zp1 * t_frac) - 1.0
        zp1_grid = z_grid + 1.0
        dz_grid = z_grid[1:] - z_grid[:-1]  # (steps,)
        
        # For each (H0, omega_m, beta) combo, compute integral
        # Reshape for broadcasting: H0(nH,1,1,1), om(1,nO,1,1), beta(1,1,nB,1), z_grid(1,1,1,steps+1)
        H0_4d = H0[:, None, None, None]
        om_4d = om[None, :, None, None]
        beta_4d = beta[None, None, :, None]
        zp1_4d = zp1_grid[None, None, None, :]  # (1,1,1,steps+1)
        
        omega_L = 1.0 - om_4d - OMEGA_R0
        E2 = (OMEGA_R0 * zp1_4d**4
              + om_4d * (1.0 + beta_4d) * zp1_4d**3
              + omega_L)
        E2 = xp.maximum(E2, 1e-10)
        Hz = H0_4d * xp.sqrt(E2)  # (nH, nO, nB, steps+1)
        inv_Hz = 1.0 / Hz
        
        # Trapezoidal: sum 0.5*(f[i]+f[i+1])*dz[i]
        dz_4d = dz_grid[None, None, None, :]  # (1,1,1,steps)
        integrand = 0.5 * (inv_Hz[:,:,:,:-1] + inv_Hz[:,:,:,1:]) * dz_4d
        integral = xp.sum(integrand, axis=3)  # (nH, nO, nB)
        
        result[:, :, :, iz] = C_LIGHT * integral
        
        if (iz + 1) % 10 == 0:
            print(f'  z {iz+1}/{nZ}...', flush=True)
    
    if GPU:
        return cp.asnumpy(result)
    return result


def main():
    output_dir = 'dist-tables'
    if '--output' in sys.argv:
        output_dir = sys.argv[sys.argv.index('--output') + 1]
    
    os.makedirs(output_dir, exist_ok=True)
    
    mode = f'GPU ({DEVICE})' if GPU else 'CPU (NumPy)'
    print(f'AEGIS Distance Table Generator - {mode}')
    
    # Build parameter grids
    H0_arr = np.linspace(GRID['H0']['min'], GRID['H0']['max'], GRID['H0']['steps'])
    om_arr = np.linspace(GRID['omega_m']['min'], GRID['omega_m']['max'], GRID['omega_m']['steps'])
    beta_arr = np.linspace(GRID['beta']['min'], GRID['beta']['max'], GRID['beta']['steps'])
    
    nH, nO, nB, nZ = len(H0_arr), len(om_arr), len(beta_arr), len(Z_VALUES)
    total = nH * nO * nB * nZ
    print(f'  Grid: {nH}×{nO}×{nB}×{nZ} = {total:,} distances')
    print(f'  H0: [{GRID["H0"]["min"]}, {GRID["H0"]["max"]}]')
    print(f'  Ωm: [{GRID["omega_m"]["min"]}, {GRID["omega_m"]["max"]}]')
    print(f'  β:  [{GRID["beta"]["min"]}, {GRID["beta"]["max"]}]')
    print(f'  z:  {nZ} values, [{Z_VALUES[0]:.3f}, {Z_VALUES[-1]:.3f}]')
    
    t0 = time.perf_counter()
    table = compute_table(Z_VALUES, H0_arr, om_arr, beta_arr)
    elapsed = time.perf_counter() - t0
    
    print(f'  Computed in {elapsed:.1f}s ({total/elapsed:,.0f} dist/sec)')
    
    # Save as binary Float64 + metadata JSON
    table_path = os.path.join(output_dir, 'comoving.bin')
    meta_path = os.path.join(output_dir, 'comoving.json')
    
    table.astype(np.float64).tofile(table_path)
    size_mb = os.path.getsize(table_path) / (1024 * 1024)
    
    meta = {
        'shape': [nH, nO, nB, nZ],
        'H0': {'min': float(GRID['H0']['min']), 'max': float(GRID['H0']['max']), 'steps': nH},
        'omega_m': {'min': float(GRID['omega_m']['min']), 'max': float(GRID['omega_m']['max']), 'steps': nO},
        'beta': {'min': float(GRID['beta']['min']), 'max': float(GRID['beta']['max']), 'steps': nB},
        'z_values': Z_VALUES,
        'table_file': 'comoving.bin',
        'dtype': 'float64',
        'size_mb': round(size_mb, 1),
        'compute_time_s': round(elapsed, 1),
        'device': DEVICE,
        'gpu': GPU,
    }
    
    with open(meta_path, 'w') as f:
        json.dump(meta, f, indent=2)
    
    print(f'  Saved: {table_path} ({size_mb:.1f} MB)')
    print(f'  Meta:  {meta_path}')
    
    # Verify accuracy: spot-check a few distances
    print('\n  Accuracy check (vs direct integration):')
    from numpy import interp as np_interp
    test_cases = [
        (70.0, 0.3, 0.0, 0.5),
        (73.0, 0.25, 0.1, 1.0),
        (67.4, 0.315, -0.05, 2.33),
    ]
    
    for H0, om, beta, z_test in test_cases:
        # Direct integration
        omega_L = 1.0 - om - OMEGA_R0
        ln_zp1 = np.log(1.0 + z_test)
        steps = 200
        t_frac = np.linspace(0.0, 1.0, steps + 1)
        z_grid = np.exp(ln_zp1 * t_frac) - 1.0
        zp1 = z_grid + 1.0
        E2 = OMEGA_R0 * zp1**4 + om * (1.0 + beta) * zp1**3 + omega_L
        Hz = H0 * np.sqrt(np.maximum(E2, 1e-10))
        dz = np.diff(z_grid)
        integral = np.sum(0.5 * (1.0/Hz[:-1] + 1.0/Hz[1:]) * dz)
        direct = C_LIGHT * integral
        
        # Table lookup (trilinear interpolation)
        iH = (H0 - GRID['H0']['min']) / (GRID['H0']['max'] - GRID['H0']['min']) * (nH - 1)
        iO = (om - GRID['omega_m']['min']) / (GRID['omega_m']['max'] - GRID['omega_m']['min']) * (nO - 1)
        iB = (beta - GRID['beta']['min']) / (GRID['beta']['max'] - GRID['beta']['min']) * (nB - 1)
        
        iH0 = int(np.clip(iH, 0, nH-2)); iH1 = iH0 + 1; fH = iH - iH0
        iO0 = int(np.clip(iO, 0, nO-2)); iO1 = iO0 + 1; fO = iO - iO0
        iB0 = int(np.clip(iB, 0, nB-2)); iB1 = iB0 + 1; fB = iB - iB0
        
        # Find z index
        iz = min(range(nZ), key=lambda i: abs(Z_VALUES[i] - z_test))
        
        # Trilinear
        v = (table[iH0,iO0,iB0,iz] * (1-fH)*(1-fO)*(1-fB)
           + table[iH1,iO0,iB0,iz] * fH*(1-fO)*(1-fB)
           + table[iH0,iO1,iB0,iz] * (1-fH)*fO*(1-fB)
           + table[iH0,iO0,iB1,iz] * (1-fH)*(1-fO)*fB
           + table[iH1,iO1,iB0,iz] * fH*fO*(1-fB)
           + table[iH1,iO0,iB1,iz] * fH*(1-fO)*fB
           + table[iH0,iO1,iB1,iz] * (1-fH)*fO*fB
           + table[iH1,iO1,iB1,iz] * fH*fO*fB)
        
        err = abs(v - direct) / direct * 100
        print(f'    H0={H0}, Ωm={om}, β={beta}, z={z_test}: direct={direct:.2f}, table={v:.2f}, err={err:.4f}%')


if __name__ == '__main__':
    main()
