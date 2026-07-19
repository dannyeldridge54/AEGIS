'use strict';
// ─────────────────────────────────────────────────────────────────────────────
// GPU DISTANCE TABLE — Fast comoving distance lookup via precomputed tables
// Optional: if dist-tables/ doesn't exist, falls back to direct integration.
// Generate tables: python gpu-distancetable.py [--gpu]
// ─────────────────────────────────────────────────────────────────────────────
const fs = require('fs');
const path = require('path');

const TABLE_DIR = path.join(__dirname, 'dist-tables');
let table = null;     // Float64Array
let meta = null;      // grid metadata
let zIndex = null;    // Map<z_value → column index>
let loaded = false;

// ── Load table ───────────────────────────────────────────────────────────────
function loadDistanceTable() {
  const metaPath = path.join(TABLE_DIR, 'comoving.json');
  const binPath = path.join(TABLE_DIR, 'comoving.bin');

  if (!fs.existsSync(metaPath) || !fs.existsSync(binPath)) {
    return false;
  }

  try {
    meta = JSON.parse(fs.readFileSync(metaPath, 'utf8'));
    const buf = fs.readFileSync(binPath);
    table = new Float64Array(buf.buffer, buf.byteOffset, buf.byteLength / 8);

    // Build z→index map (with tolerance for floating point)
    zIndex = new Map();
    for (let i = 0; i < meta.z_values.length; i++) {
      zIndex.set(Math.round(meta.z_values[i] * 1e6), i);
    }

    loaded = true;
    const sizeMB = (table.byteLength / (1024 * 1024)).toFixed(1);
    console.log(`📊 Distance table: ${meta.shape.join('×')} (${sizeMB}MB), ${meta.gpu ? 'GPU' : 'CPU'}-computed in ${meta.compute_time_s}s`);
    return true;
  } catch (e) {
    console.log(`📊 Distance table: failed to load (${e.message}), using direct integration`);
    return false;
  }
}

// ── Fast trilinear interpolation ─────────────────────────────────────────────
function tableLookup(z, H0, omega_m, beta) {
  if (!loaded) return null;

  // Find z index (exact match via rounded key)
  const zKey = Math.round(z * 1e6);
  const iz = zIndex.get(zKey);
  if (iz === undefined) return null; // z not in table, fall back

  const [nH, nO, nB, nZ] = meta.shape;

  // Compute fractional grid indices
  const fH = (H0 - meta.H0.min) / (meta.H0.max - meta.H0.min) * (nH - 1);
  const fO = (omega_m - meta.omega_m.min) / (meta.omega_m.max - meta.omega_m.min) * (nO - 1);
  const fB = (beta - meta.beta.min) / (meta.beta.max - meta.beta.min) * (nB - 1);

  // Clamp to grid
  if (fH < 0 || fH > nH - 1 || fO < 0 || fO > nO - 1 || fB < 0 || fB > nB - 1) {
    return null; // out of grid range, fall back
  }

  const iH0 = Math.min(Math.floor(fH), nH - 2);
  const iO0 = Math.min(Math.floor(fO), nO - 2);
  const iB0 = Math.min(Math.floor(fB), nB - 2);
  const iH1 = iH0 + 1;
  const iO1 = iO0 + 1;
  const iB1 = iB0 + 1;
  const tH = fH - iH0;
  const tO = fO - iO0;
  const tB = fB - iB0;

  // Index into flat array: table[iH][iO][iB][iz] → iH*(nO*nB*nZ) + iO*(nB*nZ) + iB*nZ + iz
  const sO = nB * nZ;
  const sH = nO * sO;

  const i000 = iH0 * sH + iO0 * sO + iB0 * nZ + iz;
  const i100 = iH1 * sH + iO0 * sO + iB0 * nZ + iz;
  const i010 = iH0 * sH + iO1 * sO + iB0 * nZ + iz;
  const i001 = iH0 * sH + iO0 * sO + iB1 * nZ + iz;
  const i110 = iH1 * sH + iO1 * sO + iB0 * nZ + iz;
  const i101 = iH1 * sH + iO0 * sO + iB1 * nZ + iz;
  const i011 = iH0 * sH + iO1 * sO + iB1 * nZ + iz;
  const i111 = iH1 * sH + iO1 * sO + iB1 * nZ + iz;

  // Trilinear interpolation
  return (
    table[i000] * (1 - tH) * (1 - tO) * (1 - tB) +
    table[i100] * tH * (1 - tO) * (1 - tB) +
    table[i010] * (1 - tH) * tO * (1 - tB) +
    table[i001] * (1 - tH) * (1 - tO) * tB +
    table[i110] * tH * tO * (1 - tB) +
    table[i101] * tH * (1 - tO) * tB +
    table[i011] * (1 - tH) * tO * tB +
    table[i111] * tH * tO * tB
  );
}

/** Check if table is loaded and ready. */
function isTableLoaded() { return loaded; }

/** Get table metadata. */
function getTableInfo() {
  if (!loaded) return null;
  return {
    shape: meta.shape,
    size_mb: meta.size_mb,
    device: meta.device,
    gpu: meta.gpu,
    z_count: meta.z_values.length,
    compute_time_s: meta.compute_time_s,
  };
}

module.exports = { loadDistanceTable, tableLookup, isTableLoaded, getTableInfo };
