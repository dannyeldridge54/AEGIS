// preprocess-pantheon.js
// Precomputes Cholesky factor of Pantheon+ covariance matrix for χ² evaluation
const fs = require('fs');
const path = require('path');

console.log('=== Pantheon+ Full Covariance Preprocessor ===');
console.time('Total');

// 1. Read data file
console.log('Reading Pantheon+SH0ES.dat...');
const datLines = fs.readFileSync('data/pantheon/Pantheon+SH0ES.dat', 'utf8').trim().split('\n');
const header = datLines[0].split(/\s+/);
const zIdx = header.indexOf('zHD');
const mbIdx = header.indexOf('m_b_corr');
const mbErrIdx = header.indexOf('m_b_corr_err_DIAG');
const isCalIdx = header.indexOf('IS_CALIBRATOR');

console.log(`  Columns: z=${zIdx}, m_b=${mbIdx}, err=${mbErrIdx}, isCal=${isCalIdx}`);

const N = datLines.length - 1; // 1701
const z = new Float64Array(N);
const mb = new Float64Array(N);
const mbErr = new Float64Array(N);
const isCal = new Int8Array(N);

for (let i = 0; i < N; i++) {
  const cols = datLines[i + 1].split(/\s+/);
  z[i] = parseFloat(cols[zIdx]);
  mb[i] = parseFloat(cols[mbIdx]);
  mbErr[i] = parseFloat(cols[mbErrIdx]);
  isCal[i] = parseInt(cols[isCalIdx]);
}

console.log(`  ${N} supernovae loaded`);
console.log(`  z range: [${z[0].toFixed(4)}, ${z[N-1].toFixed(4)}]`);
console.log(`  Calibrators: ${isCal.reduce((s,v) => s+v, 0)}`);

// 2. Read covariance matrix
console.log('Reading covariance matrix (31MB)...');
console.time('  Read cov');
const covData = fs.readFileSync('data/pantheon/Pantheon+SH0ES_STAT+SYS.cov', 'utf8');
const covLines = covData.trim().split('\n');
const Ncov = parseInt(covLines[0]);
console.log(`  Matrix size: ${Ncov}x${Ncov}`);
console.timeEnd('  Read cov');

if (Ncov !== N) {
  console.error(`ERROR: Data has ${N} rows but cov is ${Ncov}x${Ncov}`);
  process.exit(1);
}

// Parse into flat array
console.log('Parsing covariance values...');
console.time('  Parse');
const C = new Float64Array(N * N);
for (let i = 0; i < N * N; i++) {
  C[i] = parseFloat(covLines[i + 1]);
}
console.timeEnd('  Parse');

// 3. Cholesky decomposition: C = L * L^T
// L is lower triangular, stored as flat N*N
console.log('Computing Cholesky decomposition (this may take a minute)...');
console.time('  Cholesky');
const L = new Float64Array(N * N);

for (let i = 0; i < N; i++) {
  for (let j = 0; j <= i; j++) {
    let sum = C[i * N + j];
    for (let k = 0; k < j; k++) {
      sum -= L[i * N + k] * L[j * N + k];
    }
    if (i === j) {
      if (sum <= 0) {
        console.error(`  Non-positive diagonal at ${i}: ${sum}`);
        // Add small regularization
        sum = 1e-10;
      }
      L[i * N + j] = Math.sqrt(sum);
    } else {
      L[i * N + j] = sum / L[j * N + j];
    }
  }
  if (i % 200 === 0) process.stdout.write(`  Row ${i}/${N}\r`);
}
console.log('');
console.timeEnd('  Cholesky');

// 4. Save preprocessed data
// For the task we need: z[], mb[], and L[] (Cholesky factor)
// χ² = ||L⁻¹(m_obs - m_model)||²  (forward substitution)
// Save L as binary for efficiency

console.log('Saving preprocessed data...');

// Save metadata + arrays as binary
const metadata = {
  N,
  zMin: Math.min(...z),
  zMax: Math.max(...z),
  nCalibrators: isCal.reduce((s,v) => s+v, 0)
};

// Save z and mb as JSON (small)
fs.writeFileSync('data/pantheon/pantheon_preprocessed.json', JSON.stringify({
  metadata,
  z: Array.from(z),
  mb: Array.from(mb),
  mbErr: Array.from(mbErr),
  isCal: Array.from(isCal)
}));
console.log('  Saved pantheon_preprocessed.json');

// Save Cholesky factor as binary (23MB as Float64)
const cholBuf = Buffer.from(L.buffer);
fs.writeFileSync('data/pantheon/cholesky_L.bin', cholBuf);
console.log(`  Saved cholesky_L.bin (${(cholBuf.length / 1024 / 1024).toFixed(1)} MB)`);

console.timeEnd('Total');
console.log('\nDone! Ready for full-covariance χ² evaluation.');
