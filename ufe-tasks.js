'use strict';
// -------------------------------------------------------------------------------
// UFE TASKS MODULE � shared between main thread and worker threads
// Extracted from run-both.js for worker_threads parallelism
// -------------------------------------------------------------------------------
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
    { name: 'H0', min: 60, max: 100, description: 'Hubble constant' },
    { name: 'omega_m', min: 0.15, max: 0.45, description: 'Matter density' },
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

module.exports = {
  H0_PLANCK, OMEGA_M0, OMEGA_R0, SIGMA8_0, RS_PLANCK, C_LIGHT,
  torsionHubble, torsionHubbleEvolving,
  comovingDistance, comovingDistanceEvolving, growthFactor,
  CC_DATA,
  cosmicChronTask, desiBAOTask, sneTask, h0TensionTask,
  rsdGrowthTask, energyConditionTask, s8TensionTask,
  wDETask, combinedFitTask, modelSelectionTask,
};
