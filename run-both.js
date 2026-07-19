/**
 * AEGIS + Seeker — 24/7 Dual Pincer Runner
 *
 * AEGIS starts from the EXPLORATION end of the spectrum:
 *   wide ranges → high dimensionality → curiosity-driven → random
 *   ...and progressively tightens toward exploitation.
 *
 * Seeker starts from the EXPLOITATION end:
 *   narrow focus → low dimensionality → gradient/bayesian → surgical
 *   ...and progressively opens toward exploration.
 *
 * They meet in the middle. Every configuration gets covered.
 * Each full cycle reverses direction — AEGIS/Seeker swap ends.
 *
 * AEGIS Monitor: http://localhost:5555
 * Seeker Monitor: http://localhost:5556
 */

const aegis = require('./dist/index.js');
const seeker = require('./seeker/dist/index.js');

// ═══════════════════════════════════════════════════════════════════════════════
// THE SPECTRUM — ordered from pure exploration (index 0) to pure exploitation
// ═══════════════════════════════════════════════════════════════════════════════

// ── Speed Controls (adjustable via env vars OR runtime API on :5557) ─────────
// Usage: EVAL_SCALE=2 node run-both.js      (double all eval budgets)
//        EVAL_SCALE=0.5 node run-both.js    (halve all — faster cycles)
//        DELAY_MS=0 node run-both.js        (zero delay between tasks)
let EVAL_SCALE = parseFloat(process.env.EVAL_SCALE || '1');
let DELAY_MS = parseInt(process.env.DELAY_MS || '50');
const CONTROL_PORT = parseInt(process.env.CONTROL_PORT || '5557');
console.log(`⚙️  Speed: EVAL_SCALE=${EVAL_SCALE}x  DELAY_MS=${DELAY_MS}ms  Control: http://localhost:${CONTROL_PORT}`);

// Base eval budgets (before EVAL_SCALE multiplier)
const BASE_EVALS = [800, 1200, 1000, 1000, 1000, 1000, 2000, 1200, 1000, 1500, 2000];

const spectrum = [
  { tag: 'chaos-scan',       baseIdx: 0,  config: { explorationRate: 0.95, strategies: ['random', 'curiosity'] } },
  { tag: 'wide-swarm',       baseIdx: 1,  config: { explorationRate: 0.85, strategies: ['swarm', 'curiosity', 'random'] } },
  { tag: 'evo-explore',      baseIdx: 2,  config: { explorationRate: 0.75, strategies: ['evolutionary', 'swarm', 'curiosity', 'random'] } },
  { tag: 'diverse-mix',      baseIdx: 3,  config: { explorationRate: 0.65, strategies: ['evolutionary', 'swarm', 'random', 'annealing'] } },
  { tag: 'annealing-hot',    baseIdx: 4,  config: { explorationRate: 0.60, strategies: ['annealing', 'swarm', 'curiosity'] } },
  { tag: 'balanced',         baseIdx: 5,  config: { explorationRate: 0.50 } },
  { tag: 'full-suite-deep',  baseIdx: 6,  config: { explorationRate: 0.50 } },
  { tag: 'bayesian-refine',  baseIdx: 7,  config: { explorationRate: 0.35, strategies: ['bayesian', 'gradient', 'annealing', 'exploit'] } },
  { tag: 'gradient-anneal',  baseIdx: 8,  config: { explorationRate: 0.25, strategies: ['gradient', 'annealing', 'exploit'] } },
  { tag: 'surgical-exploit', baseIdx: 9,  config: { explorationRate: 0.10, strategies: ['gradient', 'bayesian', 'exploit'] } },
  { tag: 'pure-refine',      baseIdx: 10, config: { explorationRate: 0.05, strategies: ['gradient', 'exploit'] } },
];

// Dynamic config getter — applies current EVAL_SCALE at call time
function getProfileConfig(profile) {
  return { ...profile.config, maxEvals: Math.round(BASE_EVALS[profile.baseIdx] * EVAL_SCALE) };
}

const SPECTRUM_LEN = spectrum.length;

// ═══════════════════════════════════════════════════════════════════════════════
// REAL COSMOLOGY TASKS — No more toy benchmarks
// Every task fits real observational data or computes real physics
// ═══════════════════════════════════════════════════════════════════════════════

// ── Planck 2018 baseline constants ──────────────────────────────────────────
const H0_PLANCK = 67.4;  // km/s/Mpc
const OMEGA_M0 = 0.315;
const OMEGA_R0 = 9.34e-5;
const SIGMA8_0 = 0.811;
const RS_PLANCK = 147.09; // sound horizon in Mpc
const C_LIGHT = 299792.458; // km/s

// ── Torsion-modified Friedmann equation ─────────────────────────────────────
// H²(z) = H₀² [ Ωr(1+z)⁴ + Ωm(1+β)(1+z)³ + ΩΛ ]
// β = torsion coupling, modifies matter sector
function torsionHubble(z, H0, omega_m, omega_r, beta) {
  const omega_L = 1 - omega_m - omega_r;
  const zp1 = 1 + z;
  const E2 = omega_r * Math.pow(zp1, 4)
    + omega_m * (1 + beta) * Math.pow(zp1, 3)
    + omega_L;
  return H0 * Math.sqrt(Math.max(E2, 1e-10));
}

// Redshift-dependent torsion: β(z) = β₀ + β₁·z/(1+z)
// Allows early universe (high z → β₀+β₁) to differ from late universe (z=0 → β₀)
function torsionHubbleEvolving(z, H0, omega_m, omega_r, beta0, beta1) {
  const beta_z = beta0 + beta1 * z / (1 + z);
  const omega_L = 1 - omega_m - omega_r;
  const zp1 = 1 + z;
  const E2 = omega_r * Math.pow(zp1, 4)
    + omega_m * (1 + beta_z) * Math.pow(zp1, 3)
    + omega_L;
  return H0 * Math.sqrt(Math.max(E2, 1e-10));
}

function comovingDistanceEvolving(z, H0, omega_m, omega_r, beta0, beta1, steps = 1000) {
  if (z <= 0) return 0;
  const lnZp1 = Math.log(1 + z);
  const dlnZp1 = lnZp1 / steps;
  let integral = 0;
  for (let i = 0; i < steps; i++) {
    const z1 = Math.exp(i * dlnZp1) - 1;
    const z2 = Math.exp((i + 1) * dlnZp1) - 1;
    const dz = z2 - z1;
    integral += 0.5 * (1 / torsionHubbleEvolving(z1, H0, omega_m, omega_r, beta0, beta1)
      + 1 / torsionHubbleEvolving(z2, H0, omega_m, omega_r, beta0, beta1)) * dz;
  }
  return C_LIGHT * integral;
}

function comovingDistance(z, H0, omega_m, omega_r, beta, steps = 200) {
  if (z <= 0) return 0;
  // Use log-spaced steps for better accuracy at high z
  const lnZp1 = Math.log(1 + z);
  const dlnZp1 = lnZp1 / steps;
  let integral = 0;
  for (let i = 0; i < steps; i++) {
    const z1 = Math.exp(i * dlnZp1) - 1;
    const z2 = Math.exp((i + 1) * dlnZp1) - 1;
    const dz = z2 - z1;
    integral += 0.5 * (1 / torsionHubble(z1, H0, omega_m, omega_r, beta)
      + 1 / torsionHubble(z2, H0, omega_m, omega_r, beta)) * dz;
  }
  return C_LIGHT * integral; // Mpc
}

// Growth factor (Carroll et al. 1992 approximation)
function growthFactor(z, omega_m, beta) {
  const a = 1 / (1 + z);
  const omega_L = 1 - omega_m;
  const OmZ = omega_m * (1 + beta) * Math.pow(1 + z, 3)
    / (omega_m * (1 + beta) * Math.pow(1 + z, 3) + omega_L);
  const OLZ = omega_L
    / (omega_m * (1 + beta) * Math.pow(1 + z, 3) + omega_L);
  const D = (5 / 2) * OmZ / (
    Math.pow(OmZ, 4/7) - OLZ + (1 + OmZ / 2) * (1 + OLZ / 70)
  );
  return D / (1 + z);
}

// ── TASK 1: Cosmic Chronometer H(z) Fit ─────────────────────────────────────
// 31 direct H(z) measurements from differential galaxy ages
const CC_DATA = [
  { z: 0.070, H: 69.0, sigma: 19.6 }, { z: 0.090, H: 69.0, sigma: 12.0 },
  { z: 0.120, H: 68.6, sigma: 26.2 }, { z: 0.170, H: 83.0, sigma: 8.0 },
  { z: 0.179, H: 75.0, sigma: 4.0 }, { z: 0.199, H: 75.0, sigma: 5.0 },
  { z: 0.200, H: 72.9, sigma: 29.6 }, { z: 0.270, H: 77.0, sigma: 14.0 },
  { z: 0.280, H: 88.8, sigma: 36.6 }, { z: 0.352, H: 83.0, sigma: 14.0 },
  { z: 0.380, H: 83.0, sigma: 13.5 }, { z: 0.400, H: 95.0, sigma: 17.0 },
  { z: 0.440, H: 82.6, sigma: 7.8 }, { z: 0.480, H: 97.0, sigma: 62.0 },
  { z: 0.593, H: 104.0, sigma: 13.0 }, { z: 0.600, H: 87.9, sigma: 6.1 },
  { z: 0.680, H: 92.0, sigma: 8.0 }, { z: 0.730, H: 97.3, sigma: 7.0 },
  { z: 0.781, H: 105.0, sigma: 12.0 }, { z: 0.875, H: 125.0, sigma: 17.0 },
  { z: 0.880, H: 90.0, sigma: 40.0 }, { z: 0.900, H: 117.0, sigma: 23.0 },
  { z: 1.037, H: 154.0, sigma: 20.0 }, { z: 1.300, H: 168.0, sigma: 17.0 },
  { z: 1.363, H: 160.0, sigma: 33.6 }, { z: 1.430, H: 177.0, sigma: 18.0 },
  { z: 1.530, H: 140.0, sigma: 14.0 }, { z: 1.750, H: 202.0, sigma: 40.0 },
  { z: 1.965, H: 186.5, sigma: 50.4 },
];

const cosmicChronTask = {
  id: 'cc-hubble-fit', name: 'Cosmic Chronometer H(z) — Torsion Fit',
  evaluate: (p) => {
    let chi2 = 0;
    for (const d of CC_DATA) {
      const Hpred = torsionHubble(d.z, p.H0, p.omega_m, OMEGA_R0, p.beta);
      chi2 += ((d.H - Hpred) / d.sigma) ** 2;
    }
    return chi2;
  },
  parameters: [
    { name: 'H0', min: 60, max: 80, description: 'Hubble constant km/s/Mpc' },
    { name: 'omega_m', min: 0.20, max: 0.45, description: 'Matter density Ωm₀' },
    { name: 'beta', min: -0.5, max: 0.5, description: 'Torsion coupling β' },
  ],
};

// ── TASK 2: DESI DR1 BAO Fit ────────────────────────────────────────────────
// Baryon Acoustic Oscillation distance measurements from DESI 2024
const DESI_BAO = [
  { z: 0.295, DV_rs: 7.93, sigma: 0.15 },
  { z: 0.510, DM_rs: 13.62, sigma: 0.25, DH_rs: 20.98, DH_sig: 0.61 },
  { z: 0.706, DM_rs: 16.85, sigma: 0.32, DH_rs: 20.08, DH_sig: 0.60 },
  { z: 0.930, DM_rs: 21.71, sigma: 0.28, DH_rs: 17.88, DH_sig: 0.35 },
  { z: 1.317, DM_rs: 27.79, sigma: 0.69, DH_rs: 13.82, DH_sig: 0.42 },
  { z: 2.330, DM_rs: 39.71, sigma: 0.94, DH_rs: 8.52, DH_sig: 0.17 },
];

const desiBAOTask = {
  id: 'desi-bao-fit', name: 'DESI DR1 BAO — Torsion Distances',
  evaluate: (p) => {
    let chi2 = 0;
    const rs = p.rs; // sound horizon
    for (const d of DESI_BAO) {
      const DM = comovingDistance(d.z, p.H0, p.omega_m, OMEGA_R0, p.beta);
      const DH = C_LIGHT / torsionHubble(d.z, p.H0, p.omega_m, OMEGA_R0, p.beta);
      if (d.DV_rs) {
        const DV = Math.pow(d.z * DM * DM * DH, 1/3);
        chi2 += ((DV / rs - d.DV_rs) / d.sigma) ** 2;
      }
      if (d.DM_rs) {
        chi2 += ((DM / rs - d.DM_rs) / d.sigma) ** 2;
      }
      if (d.DH_rs) {
        chi2 += ((DH / rs - d.DH_rs) / d.DH_sig) ** 2;
      }
    }
    return chi2;
  },
  parameters: [
    { name: 'H0', min: 60, max: 80, description: 'Hubble constant' },
    { name: 'omega_m', min: 0.20, max: 0.45, description: 'Matter density' },
    { name: 'beta', min: -0.5, max: 0.5, description: 'Torsion coupling' },
    { name: 'rs', min: 130, max: 160, description: 'Sound horizon r_s (Mpc)' },
  ],
};

// ── TASK 3: Pantheon+ SNe Ia Distance Modulus ───────────────────────────────
// Subset of key Pantheon+ Type Ia supernovae measurements
const SNE_DATA = [
  { z: 0.01, mu: 33.11, sigma: 0.15 }, { z: 0.02, mu: 34.73, sigma: 0.12 },
  { z: 0.03, mu: 35.58, sigma: 0.11 }, { z: 0.05, mu: 36.64, sigma: 0.10 },
  { z: 0.08, mu: 37.65, sigma: 0.09 }, { z: 0.12, mu: 38.51, sigma: 0.08 },
  { z: 0.20, mu: 39.59, sigma: 0.07 }, { z: 0.30, mu: 40.39, sigma: 0.06 },
  { z: 0.40, mu: 41.01, sigma: 0.06 }, { z: 0.50, mu: 41.50, sigma: 0.06 },
  { z: 0.60, mu: 41.91, sigma: 0.07 }, { z: 0.80, mu: 42.57, sigma: 0.08 },
  { z: 1.00, mu: 43.07, sigma: 0.09 }, { z: 1.20, mu: 43.47, sigma: 0.10 },
  { z: 1.50, mu: 43.92, sigma: 0.12 }, { z: 1.80, mu: 44.27, sigma: 0.15 },
];

const sneTask = {
  id: 'sne-pantheon-fit', name: 'Pantheon+ SNe Ia — Torsion Luminosity Distance',
  evaluate: (p) => {
    let chi2 = 0;
    for (const d of SNE_DATA) {
      const dL = (1 + d.z) * comovingDistance(d.z, p.H0, p.omega_m, OMEGA_R0, p.beta);
      const mu_pred = 5 * Math.log10(Math.max(dL, 1e-10)) + 25;
      chi2 += ((d.mu - mu_pred) / d.sigma) ** 2;
    }
    // Absolute magnitude nuisance parameter
    chi2 += ((p.M_B + 19.25) / 0.03) ** 2; // M_B ≈ -19.25
    return chi2;
  },
  parameters: [
    { name: 'H0', min: 60, max: 80, description: 'Hubble constant' },
    { name: 'omega_m', min: 0.20, max: 0.45, description: 'Matter density' },
    { name: 'beta', min: -0.5, max: 0.5, description: 'Torsion coupling' },
    { name: 'M_B', min: -19.5, max: -19.0, description: 'SNe absolute magnitude' },
  ],
};

// ── TASK 4: H₀ Tension Resolver ─────────────────────────────────────────────
// Can torsion reconcile Planck (67.4) vs SH0ES (73.0)?
const h0TensionTask = {
  id: 'h0-tension', name: 'H₀ Tension — Evolving Torsion Resolution',
  evaluate: (p) => {
    // CMB constraint: angular size of sound horizon at last scattering
    // θ* = r_s / d_C (both comoving!) — NOT r_s / D_A
    const z_star = 1089;
    const DC_star = comovingDistanceEvolving(z_star, p.H0, p.omega_m, p.omega_r, p.beta0, p.beta1, 1000);
    const theta_star_pred = RS_PLANCK / DC_star;
    const theta_star_obs = 0.010411; // rad, from Planck
    // Fractional deviation with 0.3% tolerance
    const cmb_frac = (theta_star_pred / theta_star_obs - 1) / 0.003;
    const cmb_chi2 = cmb_frac * cmb_frac; // no cap needed now — values are navigable

    // Local H₀ from SH0ES: 73.04 ± 1.04 (late universe, β(z≈0) ≈ β₀)
    const shoes_chi2 = ((p.H0 - 73.04) / 1.04) ** 2;

    // Planck CMB H₀: 67.4 ± 0.5 (early universe inference, for reference)
    // Don't directly penalize — let the CMB θ* constraint handle this

    // Low-z H(z) from cosmic chronometers (uses evolving torsion)
    let cc_chi2 = 0;
    for (const d of CC_DATA.slice(0, 10)) { // z < 0.5
      const Hpred = torsionHubbleEvolving(d.z, p.H0, p.omega_m, p.omega_r, p.beta0, p.beta1);
      cc_chi2 += ((d.H - Hpred) / d.sigma) ** 2;
    }

    // BAO constraint at intermediate z (uses evolving torsion)
    let bao_chi2 = 0;
    const bao_points = [
      { z: 0.38, DV_obs: 1477, sigma: 16 },  // BOSS DR12
      { z: 0.51, DV_obs: 1877, sigma: 19 },
      { z: 0.61, DV_obs: 2140, sigma: 22 },
    ];
    for (const b of bao_points) {
      const DC = comovingDistanceEvolving(b.z, p.H0, p.omega_m, p.omega_r, p.beta0, p.beta1, 200);
      const Hz = torsionHubbleEvolving(b.z, p.H0, p.omega_m, p.omega_r, p.beta0, p.beta1);
      const DV = Math.pow(DC * DC * b.z * C_LIGHT / Hz, 1/3); // volume-averaged distance
      bao_chi2 += ((DV - b.DV_obs) / b.sigma) ** 2;
    }

    const total = cmb_chi2 + shoes_chi2 + 0.5 * cc_chi2 + 0.3 * bao_chi2;
    return isFinite(total) ? total : 1e6;
  },
  parameters: [
    { name: 'H0', min: 64, max: 76, description: 'Hubble constant (tension range)' },
    { name: 'omega_m', min: 0.25, max: 0.40, description: 'Matter density' },
    { name: 'omega_r', min: 5e-5, max: 2e-4, description: 'Radiation density' },
    { name: 'beta0', min: -0.15, max: 0.15, description: 'Torsion coupling at z=0 (late universe)' },
    { name: 'beta1', min: -0.5, max: 0.5, description: 'Torsion evolution: β(z) = β₀ + β₁·z/(1+z)' },
  ],
};

// ── TASK 5: Growth Factor fσ₈ — Redshift Space Distortions ──────────────────
const RSD_DATA = [
  { z: 0.15, fsigma8: 0.490, sigma: 0.145 }, // 2dFGRS
  { z: 0.38, fsigma8: 0.497, sigma: 0.045 }, // BOSS DR12
  { z: 0.51, fsigma8: 0.460, sigma: 0.038 }, // BOSS DR12
  { z: 0.61, fsigma8: 0.436, sigma: 0.034 }, // BOSS DR12
  { z: 0.70, fsigma8: 0.448, sigma: 0.043 }, // VIPERS
  { z: 0.80, fsigma8: 0.470, sigma: 0.080 }, // GAMA
  { z: 0.85, fsigma8: 0.315, sigma: 0.095 }, // FastSound
  { z: 1.40, fsigma8: 0.482, sigma: 0.116 }, // eBOSS QSO
];

const rsdGrowthTask = {
  id: 'rsd-growth', name: 'RSD fσ₈ — Structure Growth under Torsion',
  evaluate: (p) => {
    let chi2 = 0;
    for (const d of RSD_DATA) {
      const D = growthFactor(d.z, p.omega_m, p.beta);
      const OmZ = p.omega_m * (1 + p.beta) * Math.pow(1 + d.z, 3)
        / (p.omega_m * (1 + p.beta) * Math.pow(1 + d.z, 3) + (1 - p.omega_m));
      const f = Math.pow(OmZ, p.gamma); // growth rate with torsion-modified index
      const fsigma8_pred = f * p.sigma8 * D;
      chi2 += ((d.fsigma8 - fsigma8_pred) / d.sigma) ** 2;
    }
    return chi2;
  },
  parameters: [
    { name: 'omega_m', min: 0.20, max: 0.45, description: 'Matter density' },
    { name: 'beta', min: -0.5, max: 0.5, description: 'Torsion coupling' },
    { name: 'sigma8', min: 0.70, max: 0.90, description: 'σ₈ amplitude' },
    { name: 'gamma', min: 0.40, max: 0.70, description: 'Growth index (GR ≈ 0.55)' },
  ],
};

// ── TASK 6: Energy Condition Checker ────────────────────────────────────────
// Find torsion params that satisfy all 4 energy conditions across z
const energyConditionTask = {
  id: 'energy-conditions', name: 'Energy Conditions — Torsion Viability',
  evaluate: (p) => {
    let violations = 0;
    const zSample = [0, 0.1, 0.3, 0.5, 1, 2, 5, 10, 50, 100, 500, 1089];
    for (const z of zSample) {
      const zp1 = 1 + z;
      const rho_m = p.omega_m * (1 + p.beta) * Math.pow(zp1, 3);
      const rho_r = OMEGA_R0 * Math.pow(zp1, 4);
      const rho_L = 1 - p.omega_m - OMEGA_R0;
      const rho_total = rho_m + rho_r + rho_L;
      const p_total = rho_r / 3 - rho_L; // matter p=0, radiation p=ρ/3, Λ p=-ρ

      // Weak: ρ ≥ 0
      if (rho_total < 0) violations += 1;
      // Null: ρ + p ≥ 0
      if (rho_total + p_total < 0) violations += 1;
      // Strong: ρ + 3p ≥ 0 (expected to fail at late times for accelerating universe)
      // Dominant: ρ ≥ |p|
      if (rho_total < Math.abs(p_total)) violations += 0.5;

      // Torsion-specific: spin-torsion energy must be positive
      const rho_torsion = p.beta * p.omega_m * Math.pow(zp1, 3);
      if (rho_torsion < -0.1 * rho_total) violations += 2; // torsion can't overwhelm matter
    }
    // Also require H²(z) > 0 everywhere
    for (const z of zSample) {
      const H = torsionHubble(z, H0_PLANCK, p.omega_m, OMEGA_R0, p.beta);
      if (isNaN(H) || H <= 0) violations += 5;
    }
    return violations;
  },
  parameters: [
    { name: 'omega_m', min: 0.20, max: 0.45, description: 'Matter density' },
    { name: 'beta', min: -0.5, max: 0.5, description: 'Torsion coupling' },
  ],
};

// ── TASK 7: S₈ Tension — Weak Lensing vs CMB ──────────────────────────────
// S₈ = σ₈ √(Ωm/0.3) — Planck gives 0.834, weak lensing gives ~0.76
const s8TensionTask = {
  id: 's8-tension', name: 'S₈ Tension — Weak Lensing vs CMB',
  evaluate: (p) => {
    const S8 = p.sigma8 * Math.sqrt(p.omega_m / 0.3);
    // Planck: S₈ = 0.834 ± 0.016
    const planck_chi2 = ((S8 - 0.834) / 0.016) ** 2;
    // KiDS-1000: S₈ = 0.759 ± 0.024
    const kids_chi2 = ((S8 - 0.759) / 0.024) ** 2;
    // DES Y3: S₈ = 0.776 ± 0.017
    const des_chi2 = ((S8 - 0.776) / 0.017) ** 2;

    // Also fit fσ₈ growth to check consistency
    let growth_chi2 = 0;
    for (const d of RSD_DATA.slice(0, 4)) {
      const D = growthFactor(d.z, p.omega_m, p.beta);
      const OmZ = p.omega_m * (1 + p.beta) * Math.pow(1 + d.z, 3)
        / (p.omega_m * (1 + p.beta) * Math.pow(1 + d.z, 3) + (1 - p.omega_m));
      const f = Math.pow(OmZ, 0.55);
      const fsigma8_pred = f * p.sigma8 * D;
      growth_chi2 += ((d.fsigma8 - fsigma8_pred) / d.sigma) ** 2;
    }

    return planck_chi2 + kids_chi2 + des_chi2 + 0.3 * growth_chi2;
  },
  parameters: [
    { name: 'omega_m', min: 0.20, max: 0.45, description: 'Matter density' },
    { name: 'sigma8', min: 0.65, max: 0.90, description: 'σ₈ amplitude' },
    { name: 'beta', min: -0.5, max: 0.5, description: 'Torsion coupling' },
  ],
};

// ── TASK 8: Dark Energy Equation of State ───────────────────────────────────
// w(z) = w₀ + wa · z/(1+z) — can torsion mimic evolving dark energy?
const wDETask = {
  id: 'dark-energy-eos', name: 'Dark Energy EoS — Torsion vs w₀wₐCDM',
  evaluate: (p) => {
    // H²(z) with w(z) dark energy + torsion
    function Hz(z) {
      const zp1 = 1 + z;
      const w = p.w0 + p.wa * z / zp1;
      const omega_L = 1 - p.omega_m - OMEGA_R0;
      const DE = omega_L * Math.pow(zp1, 3 * (1 + p.w0 + p.wa))
        * Math.exp(-3 * p.wa * z / zp1);
      const E2 = OMEGA_R0 * Math.pow(zp1, 4)
        + p.omega_m * (1 + p.beta) * Math.pow(zp1, 3)
        + DE;
      return p.H0 * Math.sqrt(Math.max(E2, 1e-10));
    }
    let chi2 = 0;
    for (const d of CC_DATA) {
      chi2 += ((d.H - Hz(d.z)) / d.sigma) ** 2;
    }
    // BAO subset
    for (const d of DESI_BAO.filter(x => x.DV_rs)) {
      let integral = 0;
      const steps = 100, dz = d.z / steps;
      for (let i = 0; i < steps; i++) {
        const z1 = i * dz, z2 = (i + 1) * dz;
        integral += 0.5 * (C_LIGHT / Hz(z1) + C_LIGHT / Hz(z2)) * dz;
      }
      const DH = C_LIGHT / Hz(d.z);
      const DV = Math.pow(d.z * integral * integral * DH, 1/3);
      chi2 += ((DV / p.rs - d.DV_rs) / d.sigma) ** 2;
    }
    // Physical: w₀ near -1, wa near 0 preferred
    chi2 += 0.1 * ((p.w0 + 1) / 0.3) ** 2;
    return chi2;
  },
  parameters: [
    { name: 'H0', min: 60, max: 80, description: 'Hubble constant' },
    { name: 'omega_m', min: 0.20, max: 0.45, description: 'Matter density' },
    { name: 'beta', min: -0.3, max: 0.3, description: 'Torsion coupling' },
    { name: 'w0', min: -1.5, max: -0.5, description: 'DE equation of state today' },
    { name: 'wa', min: -1.0, max: 1.0, description: 'DE evolution parameter' },
    { name: 'rs', min: 130, max: 160, description: 'Sound horizon' },
  ],
};

// ── TASK 9: Combined Multi-Survey Fit ───────────────────────────────────────
// Joint fit to CC + BAO + SNe + RSD — the ultimate test
const combinedFitTask = {
  id: 'combined-multisurvey', name: 'Combined Multi-Survey — Full Torsion Fit',
  evaluate: (p) => {
    let chi2 = 0;
    // CC
    for (const d of CC_DATA) {
      const Hpred = torsionHubble(d.z, p.H0, p.omega_m, OMEGA_R0, p.beta);
      chi2 += ((d.H - Hpred) / d.sigma) ** 2;
    }
    // BAO
    for (const d of DESI_BAO) {
      const DM = comovingDistance(d.z, p.H0, p.omega_m, OMEGA_R0, p.beta);
      const DH = C_LIGHT / torsionHubble(d.z, p.H0, p.omega_m, OMEGA_R0, p.beta);
      if (d.DV_rs) {
        const DV = Math.pow(d.z * DM * DM * DH, 1/3);
        chi2 += ((DV / p.rs - d.DV_rs) / d.sigma) ** 2;
      }
      if (d.DM_rs) chi2 += ((DM / p.rs - d.DM_rs) / d.sigma) ** 2;
      if (d.DH_rs) chi2 += ((DH / p.rs - d.DH_rs) / d.DH_sig) ** 2;
    }
    // SNe
    for (const d of SNE_DATA) {
      const dL = (1 + d.z) * comovingDistance(d.z, p.H0, p.omega_m, OMEGA_R0, p.beta);
      const mu_pred = 5 * Math.log10(Math.max(dL, 1e-10)) + 25;
      chi2 += ((d.mu - mu_pred) / d.sigma) ** 2;
    }
    // RSD growth
    for (const d of RSD_DATA) {
      const D = growthFactor(d.z, p.omega_m, p.beta);
      const OmZ = p.omega_m * (1 + p.beta) * Math.pow(1 + d.z, 3)
        / (p.omega_m * (1 + p.beta) * Math.pow(1 + d.z, 3) + (1 - p.omega_m));
      const f = Math.pow(OmZ, 0.55);
      const fsigma8_pred = f * p.sigma8 * D;
      chi2 += ((d.fsigma8 - fsigma8_pred) / d.sigma) ** 2;
    }
    return chi2;
  },
  parameters: [
    { name: 'H0', min: 60, max: 80, description: 'Hubble constant' },
    { name: 'omega_m', min: 0.20, max: 0.45, description: 'Matter density' },
    { name: 'beta', min: -0.5, max: 0.5, description: 'Torsion coupling' },
    { name: 'rs', min: 130, max: 160, description: 'Sound horizon' },
    { name: 'sigma8', min: 0.70, max: 0.90, description: 'σ₈ amplitude' },
  ],
};

// ── TASK 10: Torsion Model Selection — ΔBIC vs ΛCDM ────────────────────────
// Can torsion beat ΛCDM on information criteria?
const modelSelectionTask = {
  id: 'model-selection-bic', name: 'Model Selection — ΔBIC vs ΛCDM',
  evaluate: (p) => {
    // Torsion model chi² (CC + BAO)
    let torsion_chi2 = 0;
    for (const d of CC_DATA) {
      const Hpred = torsionHubble(d.z, p.H0, p.omega_m, OMEGA_R0, p.beta);
      torsion_chi2 += ((d.H - Hpred) / d.sigma) ** 2;
    }
    for (const d of DESI_BAO) {
      const DM = comovingDistance(d.z, p.H0, p.omega_m, OMEGA_R0, p.beta);
      const DH = C_LIGHT / torsionHubble(d.z, p.H0, p.omega_m, OMEGA_R0, p.beta);
      if (d.DV_rs) {
        const DV = Math.pow(d.z * DM * DM * DH, 1/3);
        torsion_chi2 += ((DV / p.rs - d.DV_rs) / d.sigma) ** 2;
      }
      if (d.DM_rs) torsion_chi2 += ((DM / p.rs - d.DM_rs) / d.sigma) ** 2;
      if (d.DH_rs) torsion_chi2 += ((DH / p.rs - d.DH_rs) / d.DH_sig) ** 2;
    }
    // ΛCDM baseline (β=0)
    let lcdm_chi2 = 0;
    for (const d of CC_DATA) {
      const Hpred = torsionHubble(d.z, H0_PLANCK, OMEGA_M0, OMEGA_R0, 0);
      lcdm_chi2 += ((d.H - Hpred) / d.sigma) ** 2;
    }
    for (const d of DESI_BAO) {
      const DM = comovingDistance(d.z, H0_PLANCK, OMEGA_M0, OMEGA_R0, 0);
      const DH = C_LIGHT / torsionHubble(d.z, H0_PLANCK, OMEGA_M0, OMEGA_R0, 0);
      if (d.DV_rs) {
        const DV = Math.pow(d.z * DM * DM * DH, 1/3);
        lcdm_chi2 += ((DV / RS_PLANCK - d.DV_rs) / d.sigma) ** 2;
      }
      if (d.DM_rs) lcdm_chi2 += ((DM / RS_PLANCK - d.DM_rs) / d.sigma) ** 2;
      if (d.DH_rs) lcdm_chi2 += ((DH / RS_PLANCK - d.DH_rs) / d.DH_sig) ** 2;
    }
    const N = CC_DATA.length + DESI_BAO.length;
    const k_torsion = 4; // H0, omega_m, beta, rs
    const k_lcdm = 3;    // H0, omega_m, rs (no beta)
    const BIC_torsion = torsion_chi2 + k_torsion * Math.log(N);
    const BIC_lcdm = lcdm_chi2 + k_lcdm * Math.log(N);
    const deltaBIC = BIC_torsion - BIC_lcdm; // negative = torsion wins
    // Return chi² but penalize if torsion doesn't beat ΛCDM
    return torsion_chi2 + Math.max(0, deltaBIC) * 5;
  },
  parameters: [
    { name: 'H0', min: 60, max: 80, description: 'Hubble constant' },
    { name: 'omega_m', min: 0.20, max: 0.45, description: 'Matter density' },
    { name: 'beta', min: -0.5, max: 0.5, description: 'Torsion coupling' },
    { name: 'rs', min: 130, max: 160, description: 'Sound horizon' },
  ],
};

// ═══════════════════════════════════════════════════════════════════════════════
// ALL-PHYSICS TASK LIST — 100% real cosmology, zero toy benchmarks
// 10 observational tasks + 5 torsion field theory = 15 unique physics domains
// Each appears at multiple spectrum tiers for full exploration/exploitation
// ═══════════════════════════════════════════════════════════════════════════════

const tasksByDifficulty = [
  // ── Tier 1: Small parameter spaces (2-3 params) ───────────────────────────
  energyConditionTask,                                // 2 params — viability
  aegis.einsteinCartanTask,                           // EC torsion — 8 params
  s8TensionTask,                                      // 3 params — S₈ tension
  aegis.fTGravityTask,                                // f(T) — 5 params

  // ── Tier 2: Medium (3-5 params) ───────────────────────────────────────────
  cosmicChronTask,                                    // CC H(z) — 3 params
  aegis.ufeTorsionTask,                               // UFE Mexican hat — 8 params
  rsdGrowthTask,                                      // fσ₈ growth — 4 params
  aegis.torsionWaveTask,                              // Wave — 7 params
  desiBAOTask,                                        // DESI BAO — 4 params
  aegis.crossDomainTask,                              // Cross-domain — 10 params

  // ── Tier 3: Hard (4-6 params, joint fits) ─────────────────────────────────
  sneTask,                                            // Pantheon+ SNe — 4 params
  aegis.einsteinCartanTask,                           // EC again — exploitation profile
  h0TensionTask,                                      // H₀ tension — 4 params
  aegis.fTGravityTask,                                // f(T) again
  modelSelectionTask,                                 // ΔBIC — 4 params
  aegis.ufeTorsionTask,                               // UFE again

  // ── Tier 4: Extreme (5-6 params, combined fits) ───────────────────────────
  wDETask,                                            // w₀wₐCDM + torsion — 6 params
  aegis.crossDomainTask,                              // Cross-domain again
  combinedFitTask,                                    // FULL multi-survey — 5 params
  aegis.torsionWaveTask,                              // Wave again
  combinedFitTask,                                    // Combined again — max budget
  aegis.crossDomainTask,                              // Cross-domain — max budget

  // ── Tier 5: Critical repeat — highest budget profiles ─────────────────────
  h0TensionTask,                                      // H₀ tension — max exploitation
  aegis.ufeTorsionTask,                               // UFE — max exploitation
  modelSelectionTask,                                 // Model selection — final
  combinedFitTask,                                    // Combined — final pass
];

const TASK_COUNT = tasksByDifficulty.length;

// ═══════════════════════════════════════════════════════════════════════════════
// PINCER SCHEDULER
//
// AEGIS sweeps exploration → exploitation on easy → hard tasks
// Seeker sweeps exploitation → exploration on hard → easy tasks
// They meet in the middle. Each cycle they swap direction.
// ═══════════════════════════════════════════════════════════════════════════════

function buildPincerQueue(startFromExploration) {
  const queue = [];

  if (startFromExploration) {
    // Pair easy tasks with exploration, hard tasks with exploitation
    for (let t = 0; t < TASK_COUNT; t++) {
      // Map task index [0..TASK_COUNT-1] onto spectrum [0..SPECTRUM_LEN-1]
      const spectrumIdx = Math.round(t * (SPECTRUM_LEN - 1) / Math.max(TASK_COUNT - 1, 1));
      const task = tasksByDifficulty[t];
      const profile = spectrum[spectrumIdx];
      queue.push({ task, profile });
    }
  } else {
    // Pair easy tasks with exploitation, hard tasks with exploration
    for (let t = 0; t < TASK_COUNT; t++) {
      const spectrumIdx = Math.round((TASK_COUNT - 1 - t) * (SPECTRUM_LEN - 1) / Math.max(TASK_COUNT - 1, 1));
      const task = tasksByDifficulty[t];
      const profile = spectrum[spectrumIdx];
      queue.push({ task, profile });
    }
  }

  return queue;
}

// ═══════════════════════════════════════════════════════════════════════════════
// LAUNCH
// ═══════════════════════════════════════════════════════════════════════════════

console.log(`
╔═══════════════════════════════════════════════════════════════════════╗
║       _    _____ ____ ___ ____                                       ║
║      / \\  | ____/ ___|_ _/ ___|                                      ║
║     / _ \\ |  _|| |  _ | |\\___ \\   +  Seeker                          ║
║    / ___ \\| |__| |_| || | ___) |     Discovery Engine                ║
║   /_/   \\_\\_____\\____|___|____/                                      ║
║                                                                       ║
║   24/7 PINCER STRATEGY — Converging from Opposite Ends               ║
║                                                                       ║
║   AEGIS  ◀━━ EXPLORATION ━━━━━━━━━━━━━━ EXPLOITATION ━━▶ Seeker      ║
║              wide / random / curiosity    gradient / surgical         ║
║                        ╲                ╱                              ║
║                          ╲  CONVERGE  ╱                               ║
║                            ╲  HERE  ╱                                 ║
║                              ╲    ╱                                   ║
║                                ╲╱                                     ║
║                     (swap ends each cycle)                            ║
║                                                                       ║
║   ${String(TASK_COUNT).padStart(2)} tasks × ${String(SPECTRUM_LEN).padStart(2)} profiles — smart pairing           ║
║   Each cycle: alternate direction for full coverage                   ║
║                                                                       ║
║   AEGIS  Monitor: http://localhost:5555                               ║
║   Seeker Monitor: http://localhost:5556                               ║
╚═══════════════════════════════════════════════════════════════════════╝
`);

const aegisMonitor = aegis.createMonitor({ port: 5555 });
const seekerMonitor = seeker.createMonitor({ port: 5556 });

// Spatial anomaly + equation writer integration
const { computeSpatialAnomalies, HZ_OBSERVATIONS, createEquationWriter } = aegis;
const aegisWriter = createEquationWriter ? createEquationWriter('AEGIS') : null;
const seekerWriter = createEquationWriter ? createEquationWriter('Seeker') : null;

function logSpatialAnomalies(engine, runId, bestParams, monitor) {
  try {
    if (!bestParams || !computeSpatialAnomalies) return;
    // Only compute for f(T) and cross-domain runs that have f(T) params
    const hasAlpha = bestParams.alpha !== undefined || bestParams.fT_alpha !== undefined;
    const hasN = bestParams.n !== undefined || bestParams.fT_n !== undefined;
    if (!hasAlpha || !hasN) return;

    const fTParams = {
      alpha: bestParams.alpha || bestParams.fT_alpha || 0,
      beta: bestParams.beta || 0,
      n: bestParams.n || bestParams.fT_n || 1,
      lambda: bestParams.lambda || bestParams.lambda_quartic || 100,
      modelType: bestParams.modelType || 0,
    };

    const anomalies = computeSpatialAnomalies(fTParams);
    const significant = anomalies.filter(a => a.significance === 'high' || a.significance === 'moderate');

    if (significant.length > 0) {
      const high = significant.filter(a => a.significance === 'high');
      const mod = significant.filter(a => a.significance === 'moderate');
      console.log(`\n🌌 [${engine}] ${runId} — ${high.length} HIGH + ${mod.length} MODERATE spatial anomalies:`);
      for (const a of significant) {
        const icon = a.significance === 'high' ? '🔴' : '🟡';
          console.log(`   ${icon} z=${(a.z||0).toFixed(3)} | ${a.survey} | RA ${a.ra} Dec ${a.dec}`);
          console.log(`      ${a.anomalyType}: Δ=${(a.deviation_sigma||0).toFixed(1)}σ | ${a.fieldDescription}`);
          console.log(`      d=${(a.comovingDist_Mpc||0).toFixed(0)} Mpc | lookback ${(a.lookbackTime_Gyr||0).toFixed(1)} Gyr | ref: ${a.reference}`);
      }

      // Register as alert
      monitor.registerAlert({
        id: `spatial-${runId}`,
        title: `${significant.length} sky anomalies from ${runId}`,
        severity: 'critical',
        category: 'anomaly',
        detail: significant.map(a => `z=${(a.z||0).toFixed(3)} ${a.survey} ${a.anomalyType} ${(a.deviation_sigma||0).toFixed(1)}σ`).join('; '),
        data: { anomalyCount: significant.length, topAnomaly: significant[0] },
      });
    }
  } catch (e) {
    // Silent — don't crash the runner
  }
}

function synthesizeEquation(writer, taskId, params, score) {
  if (!writer) return null;
  try {
    // Use writeDiscovery — the proper API that dispatches to the right method
    // It expects an EvalResult-like object with .params
    const fakeResult = { params: { ...params }, score };
    const eq = writer.writeDiscovery('AEGIS/Seeker', taskId, fakeResult, score);
    if (eq) {
      return { plaintext: eq.plaintext || '', latex: eq.latex || '', eq };
    }
    return null;
  } catch (e) { return null; }
}

function logEquation(engine, runId, taskId, bestParams, bestScore, writer) {
  try {
    if (!writer || !bestParams) return;
    if (!taskId.match(/ufe-torsion|cross-domain|ft-gravity|einstein-cartan|torsion-wave/)) return;
    if (bestScore > 500) return;

    const eq = synthesizeEquation(writer, taskId, bestParams, bestScore);
    if (eq) {
      console.log(`\n📐 [${engine}] Equation from ${runId} (score ${bestScore.toFixed(2)}):`);
      console.log(`   ${eq.plaintext || eq.latex || 'N/A'}`);
    }
  } catch (e) {
    // Silent
  }
}

aegisMonitor.startDashboard();
seekerMonitor.startDashboard();

let aegisCycle = 0, seekerCycle = 0;
let aegisTotal = 0, seekerTotal = 0;

// ═══════════════════════════════════════════════════════════════════════════════
// CROSS-POLLINATION — engines share best discoveries
// When one engine finds a good solution, the other uses it as a seed point
// ═══════════════════════════════════════════════════════════════════════════════
// ═══════════════════════════════════════════════════════════════════════════════
// STATE PERSISTENCE — survive restarts without losing discoveries
// ═══════════════════════════════════════════════════════════════════════════════
const STATE_FILE = require('path').join(__dirname, 'ufe-state.json');

function saveState() {
  try {
    const state = {
      aegisBests, seekerBests, worstScores, pollinationCounts,
      bestKnown, bestEquation,
      aegisCycle, seekerCycle, aegisTotal, seekerTotal,
      savedAt: new Date().toISOString(),
    };
    require('fs').writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
  } catch (e) { console.error('⚠️ State save failed:', e.message); }
}

function loadState() {
  try {
    if (!require('fs').existsSync(STATE_FILE)) return false;
    const state = JSON.parse(require('fs').readFileSync(STATE_FILE, 'utf8'));
    Object.assign(aegisBests, state.aegisBests || {});
    Object.assign(seekerBests, state.seekerBests || {});
    Object.assign(worstScores, state.worstScores || {});
    Object.assign(pollinationCounts, state.pollinationCounts || {});
    Object.assign(bestKnown, state.bestKnown || {});
    if (state.bestEquation) bestEquation = state.bestEquation;
    if (state.aegisCycle) aegisCycle = state.aegisCycle;
    if (state.seekerCycle) seekerCycle = state.seekerCycle;
    if (state.aegisTotal) aegisTotal = state.aegisTotal;
    if (state.seekerTotal) seekerTotal = state.seekerTotal;
    const taskCount = Object.keys(state.aegisBests || {}).length;
    console.log(`📂 Loaded state from ${state.savedAt} — ${taskCount} tasks, ${state.aegisTotal + state.seekerTotal} total runs`);
    return true;
  } catch (e) { console.error('⚠️ State load failed:', e.message); return false; }
}

const bestKnown = {}; // { taskId: { params, score, source } }

function recordBest(taskId, params, score, source) {
  if (!isFinite(score) || !params) return;
  const prev = bestKnown[taskId];
  // Strictly less than — don't log "beats" for equal scores
  if (!prev || score < prev.score) {
    const improved = prev ? prev.score - score : 0;
    bestKnown[taskId] = { params: { ...params }, score, source };
    if (prev && prev.source !== source && improved > 1e-6) {
      console.log(`\n🔄 [CROSS-POLLINATION] ${source} beat ${prev.source} on ${taskId}: ${score.toFixed(4)} < ${prev.score.toFixed(4)} (Δ${improved.toFixed(4)})`);
      countPollination(taskId);
    }
    // Save breakthroughs immediately
    if (improved > 0.01 || !prev) saveState();
  }
}

function getSeedParams(taskId, source) {
  const known = bestKnown[taskId];
  // Only seed from the OTHER engine's discovery
  if (known && known.source !== source) {
    // Add jitter to break plateaus — 2% random perturbation
    const jittered = { ...known.params };
    for (const key of Object.keys(jittered)) {
      if (typeof jittered[key] === 'number' && isFinite(jittered[key])) {
        const scale = Math.abs(jittered[key]) || 1;
        jittered[key] += (Math.random() - 0.5) * 0.04 * scale;
      }
    }
    return { params: jittered, score: known.score };
  }
  return null;
}

async function runAegisLoop() {
  while (true) {
    aegisCycle++;
    // AEGIS: odd cycles start from exploration, even from exploitation
    const fromExploration = aegisCycle % 2 === 1;
    const direction = fromExploration ? 'EXPLORE → EXPLOIT' : 'EXPLOIT → EXPLORE';
    const queue = buildPincerQueue(fromExploration);

    console.log(`\n[AEGIS] ━━ Cycle ${aegisCycle} ━━ ${direction} ━━ ${queue.length} runs`);

    for (const { task, profile } of queue) {
      aegisTotal++;
      const runId = `aegis-${task.id}-${profile.tag}-c${aegisCycle}`;
      const runName = `AEGIS: ${task.name} [${profile.tag}]`;

      aegisMonitor.registerRun(runId, runName);
      const agent = new aegis.AegisAgent(task, {
        ...getProfileConfig(profile),
        seed: aegisTotal * 1000 + Date.now() % 10000,
        verbosity: 'silent',
      });
      // Cross-pollinate: seed from Seeker's best discovery
      const seedData = getSeedParams(task.id, 'AEGIS');
      if (seedData) {
        agent.seed(seedData.params, seedData.score);
        console.log(`   🧬 [AEGIS] Seeded ${task.name} with Seeker's best (${seedData.score.toFixed(2)})`);
      }
      agent.on(aegisMonitor.createHandler(runId));

      try {
        const result = await agent.run(task.optimum);
        // Record best for cross-pollination
        const bp = result && result.best ? result.best.params : null;
        const bs = result && result.best ? result.best.score : null;
        if (bp && isFinite(bs)) {
          recordBest(task.id, bp, bs, 'AEGIS');
          updateScoreboard(task.id, bs, 'AEGIS');
          updateBestEquation('AEGIS', task.id, bp, bs, aegisWriter);
        }
        // Log spatial anomalies + equations for torsion runs
        if (bp && task.id.match(/ft-gravity|cross-domain|ufe-torsion|einstein-cartan|torsion-wave/)) {
          logSpatialAnomalies('AEGIS', runId, bp, aegisMonitor);
          logEquation('AEGIS', runId, task.id, bp, bs, aegisWriter);
        }
      } catch (err) {
        console.error(`[AEGIS] Error: ${task.name} [${profile.tag}]: ${err.message}`);
      }
      await new Promise(r => setTimeout(r, DELAY_MS));
    }
    console.log(`[AEGIS] Cycle ${aegisCycle} done — ${aegisTotal} lifetime runs`);
  }
}

async function runSeekerLoop() {
  while (true) {
    seekerCycle++;
    // Seeker: odd cycles start from exploitation (opposite of AEGIS), even from exploration
    const fromExploration = seekerCycle % 2 === 0;
    const direction = fromExploration ? 'EXPLORE → EXPLOIT' : 'EXPLOIT → EXPLORE';
    const queue = buildPincerQueue(fromExploration);

    console.log(`\n[Seeker] ━━ Cycle ${seekerCycle} ━━ ${direction} ━━ ${queue.length} runs`);

    for (const { task, profile } of queue) {
      seekerTotal++;
      const runId = `seeker-${task.id}-${profile.tag}-c${seekerCycle}`;
      const runName = `Seeker: ${task.name} [${profile.tag}]`;

      seekerMonitor.registerRun(runId, runName);
      const agent = new seeker.SeekerAgent(task, {
        ...getProfileConfig(profile),
        seed: seekerTotal * 2000 + Date.now() % 10000,
        verbosity: 'silent',
      });
      // Cross-pollinate: seed from AEGIS's best discovery
      const seedData = getSeedParams(task.id, 'Seeker');
      if (seedData) {
        agent.seed(seedData.params, seedData.score);
        console.log(`   🧬 [Seeker] Seeded ${task.name} with AEGIS's best (${seedData.score.toFixed(2)})`);
      }
      agent.on(seekerMonitor.createHandler(runId));

      try {
        const result = await agent.run(task.optimum);
        // Record best for cross-pollination
        const bp = result && result.best ? result.best.params : null;
        const bs = result && result.best ? result.best.score : null;
        if (bp && isFinite(bs)) {
          recordBest(task.id, bp, bs, 'Seeker');
          updateScoreboard(task.id, bs, 'Seeker');
          updateBestEquation('Seeker', task.id, bp, bs, seekerWriter);
        }
        // Log spatial anomalies + equations for torsion runs
        if (bp && task.id.match(/ft-gravity|cross-domain|ufe-torsion|einstein-cartan|torsion-wave/)) {
          logSpatialAnomalies('Seeker', runId, bp, seekerMonitor);
          logEquation('Seeker', runId, task.id, bp, bs, seekerWriter);
        }
      } catch (err) {
        console.error(`[Seeker] Error: ${task.name} [${profile.tag}]: ${err.message}`);
      }
      await new Promise(r => setTimeout(r, DELAY_MS));
    }
    console.log(`[Seeker] Cycle ${seekerCycle} done — ${seekerTotal} lifetime runs`);
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// SCOREBOARD + EQUATION TRACKER — pushes to both monitors for dashboard display
// ═══════════════════════════════════════════════════════════════════════════════

// Track per-engine best scores, worst scores (for progress baseline), and cross-pollination counts
const aegisBests = {};  // { taskId: score }
const seekerBests = {}; // { taskId: score }
const worstScores = {}; // { taskId: score } — highest score ever seen, used as progress baseline
const pollinationCounts = {}; // { taskId: count }

// Target scores for progress calculation (χ² targets — lower is better)
const TASK_TARGETS = {
  'energy-conditions': 0,
  'einstein-cartan': 0.001,
  'torsion-wave': 0.01,
  'rsd-growth': 2,
  's8-tension': 8,
  'desi-bao-fit': 10,
  'dark-energy-eos': 10,
  'cc-hubble-fit': 12,
  'ft-gravity': 12,
  'model-selection-bic': 20,
  'sne-pantheon-fit': 50,
  'ufe-cross-domain': 50,
  'combined-multisurvey': 100,
  'h0-tension': 10,
  'ufe-torsion': 100,
};

// Nice display names
const TASK_NAMES = {
  'energy-conditions': 'Energy Conditions',
  'einstein-cartan': 'Einstein-Cartan Torsion',
  'torsion-wave': 'Torsion Wave Dispersion',
  'rsd-growth': 'RSD fσ₈ Growth',
  's8-tension': 'S₈ Tension',
  'desi-bao-fit': 'DESI DR1 BAO',
  'dark-energy-eos': 'Dark Energy EoS w₀wₐ',
  'cc-hubble-fit': 'Cosmic Chronometer H(z)',
  'ft-gravity': 'f(T) Teleparallel',
  'model-selection-bic': 'Model Selection ΔBIC',
  'sne-pantheon-fit': 'Pantheon+ SNe Ia',
  'ufe-cross-domain': 'UFE Cross-Domain Unified',
  'combined-multisurvey': 'Combined Multi-Survey',
  'h0-tension': 'H₀ Tension Resolver',
  'ufe-torsion': 'UFE Torsion Mexican Hat',
};

function updateScoreboard(taskId, score, engine) {
  if (!isFinite(score)) return;
  // Track worst score seen (progress baseline)
  if (!worstScores[taskId] || score > worstScores[taskId]) worstScores[taskId] = score;
  if (engine === 'AEGIS') {
    if (!aegisBests[taskId] || score < aegisBests[taskId]) aegisBests[taskId] = score;
  } else {
    if (!seekerBests[taskId] || score < seekerBests[taskId]) seekerBests[taskId] = score;
  }
}

function countPollination(taskId) {
  pollinationCounts[taskId] = (pollinationCounts[taskId] || 0) + 1;
}

// Best equation tracker
let bestEquation = null;

function updateBestEquation(engine, taskId, params, score, writer) {
  try {
    if (!writer || !params || !isFinite(score)) return;
    if (score > 500) return;
    if (!taskId.match(/ufe-torsion|cross-domain|ft-gravity|einstein-cartan|torsion-wave/)) return;
    if (bestEquation && score >= bestEquation.score) return;
    const eq = synthesizeEquation(writer, taskId, params, score);
    if (eq) {
      bestEquation = {
        plaintext: eq.plaintext || eq.latex || 'N/A',
        latex: eq.latex || '',
        params: { ...params },
        score,
        engine,
        taskId,
      };
      console.log(`\n🏆 [EQUATION UPDATED] ${engine} → ${taskId} (score ${score.toFixed(4)}):`);
      console.log(`   ${bestEquation.plaintext}`);
    }
  } catch (e) { /* silent */ }
}

function pushScoreboardToMonitors() {
  const allTaskIds = Object.keys(TASK_TARGETS);
  const rows = allTaskIds.map(taskId => {
    const aScore = aegisBests[taskId] ?? null;
    const sScore = seekerBests[taskId] ?? null;
    const bestScore = (aScore !== null && sScore !== null) ? Math.min(aScore, sScore)
      : aScore !== null ? aScore : sScore;
    const bestEngine = bestScore === aScore ? 'AEGIS' : 'Seeker';
    const target = TASK_TARGETS[taskId];
    // Progress: use actual worst score seen as baseline, not a guess
    const worstSeen = worstScores[taskId] || null;
    let progress = 0;
    if (bestScore !== null) {
      if (bestScore <= target) {
        progress = 100;
      } else if (worstSeen !== null && worstSeen > target) {
        // Real progress = how far we've come from worst to target
        // Use log scale for scores spanning many orders of magnitude
        const logBest = Math.log10(Math.max(bestScore, 1e-12));
        const logWorst = Math.log10(Math.max(worstSeen, 1e-12));
        const logTarget = Math.log10(Math.max(target, 1e-12));
        if (logWorst > logTarget) {
          progress = Math.max(0, Math.min(99, (1 - (logBest - logTarget) / (logWorst - logTarget)) * 100));
        } else {
          // Linear fallback when log scale doesn't make sense
          progress = Math.max(0, Math.min(99, (1 - (bestScore - target) / (worstSeen - target)) * 100));
        }
      }
    }
    // Status — based on ratio of best score to target
    let status = 'exploring';
    if (bestScore !== null) {
      if (bestScore <= target) status = 'converged';
      else if (target > 0 && bestScore <= target * 2) status = 'improving';
      else if (target > 0 && bestScore <= target * 10) status = 'grinding';
      else if (target === 0 && bestScore < 1) status = 'improving';
      else if (target === 0 && bestScore < 100) status = 'grinding';
      else status = 'exploring';
    }
    return {
      task: TASK_NAMES[taskId] || taskId,
      taskId,
      aegisScore: aScore,
      seekerScore: sScore,
      bestScore,
      bestEngine,
      target,
      progress,
      pollinations: pollinationCounts[taskId] || 0,
      status,
    };
  }).sort((a, b) => {
    // Sort: converged first, then by progress descending
    const statusOrder = { converged: 0, improving: 1, grinding: 2, exploring: 3 };
    const aOrd = statusOrder[a.status] ?? 4;
    const bOrd = statusOrder[b.status] ?? 4;
    if (aOrd !== bOrd) return aOrd - bOrd;
    return b.progress - a.progress;
  });

  aegisMonitor.setScoreboard(rows);
  seekerMonitor.setScoreboard(rows);
  if (bestEquation) {
    aegisMonitor.setEquation(bestEquation);
    seekerMonitor.setEquation(bestEquation);
  }
}

// Push scoreboard every 5 seconds
setInterval(pushScoreboardToMonitors, 5000);

// Status printer + state persistence (every 60s)
setInterval(() => {
  const aegisDir = aegisCycle % 2 === 1 ? 'EXPLORE→EXPLOIT' : 'EXPLOIT→EXPLORE';
  const seekerDir = seekerCycle % 2 === 0 ? 'EXPLORE→EXPLOIT' : 'EXPLOIT→EXPLORE';
  console.log(`\n${'━'.repeat(70)}`);
  console.log(`AEGIS  │ cycle ${aegisCycle} (${aegisDir}) │ ${aegisTotal} total runs`);
  console.log(`Seeker │ cycle ${seekerCycle} (${seekerDir}) │ ${seekerTotal} total runs`);
  aegisMonitor.printStatus();
  seekerMonitor.printStatus();
  saveState(); // persist discoveries to disk
}, 60000);

// ═══════════════════════════════════════════════════════════════════════════════
// RUNTIME CONTROL API — adjust speed from dashboard without restarting
// ═══════════════════════════════════════════════════════════════════════════════
const controlServer = require('http').createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') { res.writeHead(200); res.end(); return; }

  // GET /config — current settings
  if (req.url === '/config' && req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      evalScale: EVAL_SCALE,
      delayMs: DELAY_MS,
      aegisCycle,
      seekerCycle,
      aegisTotal,
      seekerTotal,
      baseEvals: BASE_EVALS,
      effectiveEvals: BASE_EVALS.map(b => Math.round(b * EVAL_SCALE)),
      spectrumTags: spectrum.map(s => s.tag),
    }));
    return;
  }

  // POST /config — update settings live
  if (req.url === '/config' && req.method === 'POST') {
    let body = '';
    req.on('data', c => body += c);
    req.on('end', () => {
      try {
        const update = JSON.parse(body);
        if (update.evalScale !== undefined) {
          EVAL_SCALE = Math.max(0.1, Math.min(10, parseFloat(update.evalScale)));
          console.log(`⚙️  [CONTROL] EVAL_SCALE changed to ${EVAL_SCALE}x`);
        }
        if (update.delayMs !== undefined) {
          DELAY_MS = Math.max(0, Math.min(5000, parseInt(update.delayMs)));
          console.log(`⚙️  [CONTROL] DELAY_MS changed to ${DELAY_MS}ms`);
        }
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ ok: true, evalScale: EVAL_SCALE, delayMs: DELAY_MS }));
      } catch (e) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: e.message }));
      }
    });
    return;
  }

  res.writeHead(404); res.end('Not found');
});
controlServer.listen(CONTROL_PORT, () => {
  console.log(`🎛️  Control API: http://localhost:${CONTROL_PORT}/config`);
});

// Load persisted state before starting
loadState();
pushScoreboardToMonitors(); // show restored scores immediately

Promise.all([runAegisLoop(), runSeekerLoop()]).catch(err => {
  console.error('Fatal error:', err);
});

process.on('SIGINT', () => {
  console.log('\nSaving state before shutdown...');
  saveState();
  aegisMonitor.stopDashboard();
  seekerMonitor.stopDashboard();
  process.exit(0);
});
