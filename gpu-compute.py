#!/usr/bin/env python3
"""
AEGIS GPU Compute Service — Optional RTX acceleration for comoving distance integrals.
Runs as a local HTTP microservice on port 5558. Falls back gracefully if no GPU.

Endpoints:
  POST /batch-comoving    — batch comoving distances (fixed beta)
  POST /batch-evolving    — batch comoving distances (evolving beta)
  GET  /health            — GPU status + benchmark
  POST /shutdown          — graceful shutdown
"""
import sys, json, time, math
from http.server import HTTPServer, BaseHTTPRequestHandler

# ── Try GPU (CuPy) → CPU fallback (NumPy) ────────────────────────────────────
try:
    import cupy as cp
    xp = cp
    GPU_AVAILABLE = True
    GPU_NAME = cp.cuda.runtime.getDeviceProperties(0)['name'].decode()
    GPU_VRAM = cp.cuda.runtime.memGetInfo()[1] / (1024**3)
except Exception:
    import numpy as cp
    xp = cp
    GPU_AVAILABLE = False
    GPU_NAME = 'none'
    GPU_VRAM = 0

import numpy as np  # always need numpy for I/O

C_LIGHT = 299792.458  # km/s

def batch_comoving(z_arr, H0, omega_m, omega_r, beta, steps=200):
    """Compute comoving distances for array of z values — GPU-vectorized."""
    z = xp.asarray(z_arr, dtype=xp.float64)
    mask = z > 0
    result = xp.zeros_like(z)
    z_pos = z[mask]
    if len(z_pos) == 0:
        return np.zeros(len(z_arr))

    omega_L = 1.0 - omega_m - omega_r
    ln_zp1 = xp.log(1.0 + z_pos)  # (N,)

    # Build integration grid: (N, steps) matrix
    t = xp.linspace(0.0, 1.0, steps + 1, dtype=xp.float64)  # (steps+1,)
    # z_grid[i,j] = exp(ln_zp1[i] * t[j]) - 1
    ln_grid = ln_zp1[:, None] * t[None, :]  # (N, steps+1)
    z_grid = xp.exp(ln_grid) - 1.0  # (N, steps+1)

    # H(z) at each grid point
    zp1 = z_grid + 1.0
    E2 = (omega_r * zp1**4
         + omega_m * (1.0 + beta) * zp1**3
         + omega_L)
    E2 = xp.maximum(E2, 1e-10)
    Hz = H0 * xp.sqrt(E2)  # (N, steps+1)
    inv_Hz = 1.0 / Hz

    # Trapezoidal integration: sum 0.5*(f(z1)+f(z2))*(z2-z1)
    dz = z_grid[:, 1:] - z_grid[:, :-1]  # (N, steps)
    integrand = 0.5 * (inv_Hz[:, :-1] + inv_Hz[:, 1:]) * dz  # (N, steps)
    integral = xp.sum(integrand, axis=1)  # (N,)

    result[mask] = C_LIGHT * integral

    if GPU_AVAILABLE:
        return cp.asnumpy(result)
    return np.asarray(result)


def batch_comoving_evolving(z_arr, H0, omega_m, omega_r, beta0, beta1, steps=1000):
    """Compute comoving distances with redshift-dependent torsion — GPU-vectorized."""
    z = xp.asarray(z_arr, dtype=xp.float64)
    mask = z > 0
    result = xp.zeros_like(z)
    z_pos = z[mask]
    if len(z_pos) == 0:
        return np.zeros(len(z_arr))

    omega_L = 1.0 - omega_m - omega_r
    ln_zp1 = xp.log(1.0 + z_pos)

    t = xp.linspace(0.0, 1.0, steps + 1, dtype=xp.float64)
    ln_grid = ln_zp1[:, None] * t[None, :]
    z_grid = xp.exp(ln_grid) - 1.0

    # Evolving beta: β(z) = β₀ + β₁·z/(1+z)
    zp1 = z_grid + 1.0
    beta_z = beta0 + beta1 * z_grid / zp1

    E2 = (omega_r * zp1**4
         + omega_m * (1.0 + beta_z) * zp1**3
         + omega_L)
    E2 = xp.maximum(E2, 1e-10)
    Hz = H0 * xp.sqrt(E2)
    inv_Hz = 1.0 / Hz

    dz = z_grid[:, 1:] - z_grid[:, :-1]
    integrand = 0.5 * (inv_Hz[:, :-1] + inv_Hz[:, 1:]) * dz
    integral = xp.sum(integrand, axis=1)

    result[mask] = C_LIGHT * integral

    if GPU_AVAILABLE:
        return cp.asnumpy(result)
    return np.asarray(result)


# ── Benchmark ─────────────────────────────────────────────────────────────────
def benchmark():
    """Compute throughput numbers for status reporting."""
    z_test = np.linspace(0.01, 2.5, 1000)
    # Warm up
    batch_comoving(z_test, 70.0, 0.3, 9.34e-5, 0.01, 200)

    iters = 20
    t0 = time.perf_counter()
    for _ in range(iters):
        batch_comoving(z_test, 70.0, 0.3, 9.34e-5, 0.01, 200)
    elapsed = time.perf_counter() - t0
    per_call = elapsed / iters * 1000  # ms
    throughput = 1000 * iters / elapsed  # distances/sec
    return per_call, throughput


# ── HTTP Service ──────────────────────────────────────────────────────────────
class GPUHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # silent

    def _json_response(self, data, status=200):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        length = int(self.headers.get('Content-Length', 0))
        return json.loads(self.rfile.read(length)) if length > 0 else {}

    def do_GET(self):
        if self.path == '/health':
            ms, throughput = benchmark()
            self._json_response({
                'gpu': GPU_AVAILABLE,
                'device': GPU_NAME,
                'vram_gb': round(GPU_VRAM, 1),
                'backend': 'cupy' if GPU_AVAILABLE else 'numpy',
                'batch_1000_ms': round(ms, 2),
                'distances_per_sec': int(throughput),
            })
        else:
            self._json_response({'error': 'not found'}, 404)

    def do_POST(self):
        if self.path == '/shutdown':
            self._json_response({'ok': True})
            sys.exit(0)

        data = self._read_json()

        if self.path == '/batch-comoving':
            t0 = time.perf_counter()
            result = batch_comoving(
                data['z'], data['H0'], data['omega_m'],
                data.get('omega_r', 9.34e-5), data['beta'],
                data.get('steps', 200)
            )
            elapsed = (time.perf_counter() - t0) * 1000
            self._json_response({
                'distances': result.tolist(),
                'compute_ms': round(elapsed, 3),
                'count': len(result),
            })

        elif self.path == '/batch-evolving':
            t0 = time.perf_counter()
            result = batch_comoving_evolving(
                data['z'], data['H0'], data['omega_m'],
                data.get('omega_r', 9.34e-5),
                data['beta0'], data['beta1'],
                data.get('steps', 1000)
            )
            elapsed = (time.perf_counter() - t0) * 1000
            self._json_response({
                'distances': result.tolist(),
                'compute_ms': round(elapsed, 3),
                'count': len(result),
            })

        else:
            self._json_response({'error': 'unknown endpoint'}, 404)


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5558
    ms, throughput = benchmark()
    mode = f'🟢 GPU ({GPU_NAME}, {GPU_VRAM:.1f}GB VRAM)' if GPU_AVAILABLE else '🟡 CPU (NumPy fallback)'
    print(f'AEGIS GPU Compute: {mode}')
    print(f'  Batch 1000 distances: {ms:.2f}ms ({int(throughput):,} dist/sec)')
    print(f'  Listening on http://localhost:{port}')
    sys.stdout.flush()
    server = HTTPServer(('127.0.0.1', port), GPUHandler)
    server.serve_forever()
