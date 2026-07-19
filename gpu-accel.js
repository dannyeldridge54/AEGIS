'use strict';
// ─────────────────────────────────────────────────────────────────────────────
// GPU ACCELERATOR — Optional GPU batch compute for comoving distance integrals
// Auto-detects gpu-compute.py service on port 5558. Falls back to CPU silently.
// ─────────────────────────────────────────────────────────────────────────────
const http = require('http');
const { spawn } = require('child_process');
const path = require('path');

const GPU_PORT = 5558;
const GPU_HOST = '127.0.0.1';
let gpuAvailable = false;
let gpuProcess = null;
let gpuInfo = null;

// ── HTTP helpers ─────────────────────────────────────────────────────────────
function postJSON(endpoint, data) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify(data);
    const req = http.request({
      hostname: GPU_HOST, port: GPU_PORT, path: endpoint,
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) },
      timeout: 10000,
    }, (res) => {
      let chunks = [];
      res.on('data', c => chunks.push(c));
      res.on('end', () => {
        try { resolve(JSON.parse(Buffer.concat(chunks).toString())); }
        catch (e) { reject(e); }
      });
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('GPU timeout')); });
    req.write(body);
    req.end();
  });
}

function getJSON(endpoint) {
  return new Promise((resolve, reject) => {
    const req = http.request({
      hostname: GPU_HOST, port: GPU_PORT, path: endpoint,
      method: 'GET', timeout: 5000,
    }, (res) => {
      let chunks = [];
      res.on('data', c => chunks.push(c));
      res.on('end', () => {
        try { resolve(JSON.parse(Buffer.concat(chunks).toString())); }
        catch (e) { reject(e); }
      });
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('GPU timeout')); });
    req.end();
  });
}

// ── Lifecycle ────────────────────────────────────────────────────────────────

/** Start GPU compute service if Python + CuPy/NumPy available. Returns status. */
async function initGPU() {
  // Check if already running
  try {
    gpuInfo = await getJSON('/health');
    gpuAvailable = true;
    return gpuInfo;
  } catch (_) { /* not running, try to start */ }

  // Try to start gpu-compute.py
  const scriptPath = path.join(__dirname, 'gpu-compute.py');
  try {
    require('fs').accessSync(scriptPath);
  } catch (_) {
    console.log('⚡ GPU: gpu-compute.py not found, using CPU-only mode');
    return null;
  }

  return new Promise((resolve) => {
    gpuProcess = spawn('python', [scriptPath, String(GPU_PORT)], {
      stdio: ['ignore', 'pipe', 'pipe'],
      detached: false,
    });

    let started = false;
    const timeout = setTimeout(() => {
      if (!started) {
        console.log('⚡ GPU: Python startup timed out, using CPU-only mode');
        resolve(null);
      }
    }, 15000);

    gpuProcess.stdout.on('data', async (data) => {
      const line = data.toString().trim();
      if (line) console.log(`  ${line}`);
      if (!started && line.includes('Listening')) {
        started = true;
        clearTimeout(timeout);
        try {
          gpuInfo = await getJSON('/health');
          gpuAvailable = true;
          resolve(gpuInfo);
        } catch (e) {
          console.log('⚡ GPU: Health check failed, using CPU-only mode');
          resolve(null);
        }
      }
    });

    gpuProcess.stderr.on('data', (data) => {
      const msg = data.toString().trim();
      // Ignore CuPy CUDA_PATH warning
      if (msg && !msg.includes('CUDA path could not be detected') && !msg.includes('warnings.warn')) {
        console.error(`  GPU stderr: ${msg}`);
      }
    });

    gpuProcess.on('error', () => {
      clearTimeout(timeout);
      console.log('⚡ GPU: Python not available, using CPU-only mode');
      resolve(null);
    });

    gpuProcess.on('exit', (code) => {
      gpuAvailable = false;
      gpuProcess = null;
      if (!started) {
        clearTimeout(timeout);
        console.log(`⚡ GPU: Python exited (code ${code}), using CPU-only mode`);
        resolve(null);
      }
    });
  });
}

/** Shutdown GPU service gracefully. */
function shutdownGPU() {
  if (gpuProcess) {
    try { postJSON('/shutdown', {}).catch(() => {}); } catch (_) {}
    setTimeout(() => {
      if (gpuProcess) {
        try { gpuProcess.kill(); } catch (_) {}
        gpuProcess = null;
      }
    }, 1000);
  }
  gpuAvailable = false;
}

// ── Batch compute ────────────────────────────────────────────────────────────

/**
 * Batch compute comoving distances on GPU (or CPU fallback).
 * @param {number[]} zArr - Array of redshift values
 * @param {number} H0 - Hubble constant
 * @param {number} omega_m - Matter density
 * @param {number} omega_r - Radiation density
 * @param {number} beta - Torsion coupling
 * @param {number} [steps=200] - Integration steps
 * @returns {Promise<number[]>} Array of comoving distances in Mpc
 */
async function batchComovingDistance(zArr, H0, omega_m, omega_r, beta, steps = 200) {
  if (!gpuAvailable || zArr.length < 3) return null; // fall back to JS for tiny batches
  try {
    const res = await postJSON('/batch-comoving', { z: zArr, H0, omega_m, omega_r, beta, steps });
    return res.distances;
  } catch (_) {
    return null; // GPU failed, caller uses JS fallback
  }
}

/**
 * Batch compute evolving comoving distances on GPU.
 * @param {number[]} zArr - Array of redshift values
 * @param {number} H0 - Hubble constant
 * @param {number} omega_m - Matter density
 * @param {number} omega_r - Radiation density
 * @param {number} beta0 - Torsion coupling at z=0
 * @param {number} beta1 - Torsion coupling evolution
 * @param {number} [steps=1000] - Integration steps
 * @returns {Promise<number[]>} Array of comoving distances in Mpc
 */
async function batchComovingDistanceEvolving(zArr, H0, omega_m, omega_r, beta0, beta1, steps = 1000) {
  if (!gpuAvailable || zArr.length < 3) return null;
  try {
    const res = await postJSON('/batch-evolving', { z: zArr, H0, omega_m, omega_r, beta0, beta1, steps });
    return res.distances;
  } catch (_) {
    return null;
  }
}

/** @returns {{ gpu: boolean, device: string, vram_gb: number, backend: string }} */
function getGPUInfo() {
  return gpuInfo || { gpu: false, device: 'none', backend: 'cpu-only' };
}

function isGPUAvailable() { return gpuAvailable; }

module.exports = {
  initGPU, shutdownGPU, isGPUAvailable, getGPUInfo,
  batchComovingDistance, batchComovingDistanceEvolving,
};
