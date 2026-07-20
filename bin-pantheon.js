// bin-pantheon.js
// Bins 1701 Pantheon+ SNe into 40 redshift bins with propagated covariance
// Standard approach: C_bin = W * C_full * W^T  where W is the binning weight matrix
const fs = require('fs');

console.log('=== Pantheon+ Binning with Full Covariance Propagation ===');
console.time('Total');

// Load preprocessed data
const data = JSON.parse(fs.readFileSync('data/pantheon/pantheon_preprocessed.json'));
const { z, mb, mbErr, isCal } = data;
const N = z.length;
console.log(`Loaded ${N} supernovae`);

// Load full covariance
console.log('Loading covariance matrix...');
const covLines = fs.readFileSync('data/pantheon/Pantheon+SH0ES_STAT+SYS.cov', 'utf8').trim().split('\n');
const Ncov = parseInt(covLines[0]);
const C = new Float64Array(N * N);
for (let i = 0; i < N * N; i++) C[i] = parseFloat(covLines[i + 1]);
console.log('Covariance loaded');

// Define 40 redshift bins (log-spaced from 0.01 to 2.3)
const NBINS = 40;
const zMin = 0.01;
const zMax = 2.3;
const logZmin = Math.log10(zMin);
const logZmax = Math.log10(zMax);
const binEdges = [];
for (let i = 0; i <= NBINS; i++) {
  binEdges.push(Math.pow(10, logZmin + i * (logZmax - logZmin) / NBINS));
}

// Assign SNe to bins (inverse-variance weighted mean per bin)
const binIndices = new Array(NBINS).fill(null).map(() => []);
for (let i = 0; i < N; i++) {
  if (z[i] < zMin || z[i] >= zMax) continue;
  for (let b = 0; b < NBINS; b++) {
    if (z[i] >= binEdges[b] && z[i] < binEdges[b + 1]) {
      binIndices[b].push(i);
      break;
    }
  }
}

// Filter out empty bins
const usedBins = [];
for (let b = 0; b < NBINS; b++) {
  if (binIndices[b].length > 0) usedBins.push(b);
}
console.log(`${usedBins.length} non-empty bins out of ${NBINS}`);

const Nbin = usedBins.length;

// Compute weight matrix W (Nbin x N)
// For each bin, weight_i = (1/sigma_i^2) / sum(1/sigma_j^2) for j in bin
// This is inverse-variance weighting
const W = new Float64Array(Nbin * N); // row-major
const binZ = new Float64Array(Nbin);
const binMu = new Float64Array(Nbin);

for (let b = 0; b < Nbin; b++) {
  const indices = binIndices[usedBins[b]];
  let sumW = 0;
  let sumWz = 0;
  let sumWmu = 0;
  
  for (const idx of indices) {
    const w = 1.0 / (mbErr[idx] * mbErr[idx]);
    W[b * N + idx] = w;
    sumW += w;
    sumWz += w * z[idx];
    sumWmu += w * mb[idx];
  }
  
  // Normalize weights
  for (const idx of indices) {
    W[b * N + idx] /= sumW;
  }
  
  binZ[b] = sumWz / sumW;
  binMu[b] = sumWmu / sumW;
}

console.log(`Bin redshifts: [${binZ[0].toFixed(4)} ... ${binZ[Nbin-1].toFixed(4)}]`);

// Propagate covariance: C_bin = W * C * W^T  (Nbin x Nbin)
console.log('Propagating covariance through binning (W * C * W^T)...');
console.time('  Propagate');

// First compute WC = W * C  (Nbin x N)
const WC = new Float64Array(Nbin * N);
for (let i = 0; i < Nbin; i++) {
  const indices_i = binIndices[usedBins[i]];
  for (let j = 0; j < N; j++) {
    let sum = 0;
    for (const k of indices_i) {
      sum += W[i * N + k] * C[k * N + j];
    }
    WC[i * N + j] = sum;
  }
  if (i % 10 === 0) process.stdout.write(`  WC row ${i}/${Nbin}\r`);
}

// Then C_bin = WC * W^T  (Nbin x Nbin)
const Cbin = new Float64Array(Nbin * Nbin);
for (let i = 0; i < Nbin; i++) {
  for (let j = 0; j < Nbin; j++) {
    let sum = 0;
    const indices_j = binIndices[usedBins[j]];
    for (const k of indices_j) {
      sum += WC[i * N + k] * W[j * N + k];
    }
    Cbin[i * Nbin + j] = sum;
  }
}
console.log('');
console.timeEnd('  Propagate');

// Invert Cbin (40x40 — trivial via Gaussian elimination)
console.log('Inverting binned covariance (Gaussian elimination)...');
const CbinInv = new Float64Array(Nbin * Nbin);

// Copy Cbin and create identity for augmented matrix
const aug = new Float64Array(Nbin * 2 * Nbin);
for (let i = 0; i < Nbin; i++) {
  for (let j = 0; j < Nbin; j++) {
    aug[i * 2 * Nbin + j] = Cbin[i * Nbin + j];
  }
  aug[i * 2 * Nbin + Nbin + i] = 1.0;
}

// Gaussian elimination with partial pivoting
for (let col = 0; col < Nbin; col++) {
  // Find pivot
  let maxVal = Math.abs(aug[col * 2 * Nbin + col]);
  let maxRow = col;
  for (let row = col + 1; row < Nbin; row++) {
    const val = Math.abs(aug[row * 2 * Nbin + col]);
    if (val > maxVal) { maxVal = val; maxRow = row; }
  }
  // Swap rows
  if (maxRow !== col) {
    for (let j = 0; j < 2 * Nbin; j++) {
      const tmp = aug[col * 2 * Nbin + j];
      aug[col * 2 * Nbin + j] = aug[maxRow * 2 * Nbin + j];
      aug[maxRow * 2 * Nbin + j] = tmp;
    }
  }
  // Eliminate
  const pivot = aug[col * 2 * Nbin + col];
  for (let j = 0; j < 2 * Nbin; j++) aug[col * 2 * Nbin + j] /= pivot;
  for (let row = 0; row < Nbin; row++) {
    if (row === col) continue;
    const factor = aug[row * 2 * Nbin + col];
    for (let j = 0; j < 2 * Nbin; j++) {
      aug[row * 2 * Nbin + j] -= factor * aug[col * 2 * Nbin + j];
    }
  }
}

// Extract inverse
for (let i = 0; i < Nbin; i++) {
  for (let j = 0; j < Nbin; j++) {
    CbinInv[i * Nbin + j] = aug[i * 2 * Nbin + Nbin + j];
  }
}

// Verify: C * C^-1 should be identity
let maxErr = 0;
for (let i = 0; i < Nbin; i++) {
  for (let j = 0; j < Nbin; j++) {
    let sum = 0;
    for (let k = 0; k < Nbin; k++) sum += Cbin[i * Nbin + k] * CbinInv[k * Nbin + j];
    const expected = (i === j) ? 1 : 0;
    maxErr = Math.max(maxErr, Math.abs(sum - expected));
  }
}
console.log(`  Inversion verification: max|C*C^-1 - I| = ${maxErr.toExponential(2)}`);

// Compute diagonal errors for reference
const binErr = new Float64Array(Nbin);
for (let i = 0; i < Nbin; i++) binErr[i] = Math.sqrt(Cbin[i * Nbin + i]);

// Save results
const result = {
  description: 'Pantheon+ 1701 SNe binned into redshift bins with FULL covariance propagation (STAT+SYS)',
  source: 'PantheonPlusSH0ES/DataRelease - Brout et al. 2022',
  nSNe: N,
  nBins: Nbin,
  binZ: Array.from(binZ),
  binMu: Array.from(binMu),
  binErr: Array.from(binErr),
  covBin: Array.from(Cbin),   // Nbin x Nbin, row-major
  covBinInv: Array.from(CbinInv), // inverse, Nbin x Nbin, row-major
  binCounts: usedBins.map(b => binIndices[b].length)
};

fs.writeFileSync('data/pantheon/pantheon_binned_fullcov.json', JSON.stringify(result, null, 0));
console.log(`\nSaved: data/pantheon/pantheon_binned_fullcov.json`);
console.log(`  ${Nbin} bins, z=[${binZ[0].toFixed(4)}, ${binZ[Nbin-1].toFixed(4)}]`);
console.log(`  Bin counts: min=${Math.min(...result.binCounts)}, max=${Math.max(...result.binCounts)}`);
console.log(`  Diagonal errors: [${binErr[0].toFixed(4)}, ${binErr[Nbin-1].toFixed(4)}]`);

// Print bin summary
console.log('\n  Bin | z_eff  | μ_obs  | σ_diag | N_SNe');
console.log('  ----|--------|--------|--------|------');
for (let i = 0; i < Nbin; i += Math.max(1, Math.floor(Nbin/10))) {
  console.log(`  ${String(i).padStart(3)} | ${binZ[i].toFixed(4)} | ${binMu[i].toFixed(3)} | ${binErr[i].toFixed(4)} | ${result.binCounts[i]}`);
}

console.timeEnd('Total');
