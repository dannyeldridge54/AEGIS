/**
 * AEGIS — Torsion Field Theory Module
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Spacetime torsion as optimization variables for UFE discovery.
 * Covers Einstein-Cartan, teleparallel f(T), and custom UFE torsion fields.
 *
 * The agent explores torsion parameter spaces to find:
 *  • Stable spin-torsion coupling configurations
 *  • Optimal f(T) gravity models matching observational data
 *  • Novel torsion geometries that minimize action functionals
 *  • Anomalies in the torsion landscape (new physics signatures)
 */

import { Task, ParameterDef } from './interfaces';

// ─── Torsion Tensor Components ───────────────────────────────────────────────

/**
 * Torsion tensor T^a_{bc} in Einstein-Cartan theory.
 * Antisymmetric in lower indices: T^a_{bc} = -T^a_{cb}
 * Related to spin density via the Cartan equation.
 */
export interface TorsionTensor {
  /** Torsion components T^a_{bc} indexed as [a][b][c] */
  components: number[][][];
  /** Spacetime dimension (default 4) */
  dimension: number;
  /** Trace vector T_a = T^b_{ba} */
  traceVector: number[];
  /** Axial vector S_a = ε_{abcd} T^{bcd} */
  axialVector: number[];
  /** Torsion scalar T = T^a_{bc} T_a^{bc} */
  scalar: number;
}

/**
 * Contorsion tensor K^a_{bc} — difference between
 * the connection with torsion and the Levi-Civita connection.
 * K^a_{bc} = ½(T^a_{bc} + T_b^a_c + T_c^a_b)
 */
export interface ContorsionTensor {
  components: number[][][];
  /** Superpotential S_a^{bc} for teleparallel formulation */
  superpotential: number[][][];
}

// ─── Einstein-Cartan Torsion ─────────────────────────────────────────────────

/**
 * Einstein-Cartan action with torsion:
 * S = ∫ (R + λT²)√(-g) d⁴x
 *
 * Where T² = T^a_{bc} T_a^{bc} is the torsion scalar squared.
 * The coupling λ controls how strongly torsion affects geometry.
 *
 * Parameters to optimize:
 *  - spinDensity: magnitude of the source spin density tensor
 *  - couplingLambda: torsion-curvature coupling strength
 *  - torsionComponents: independent T^a_{bc} values (6 in 4D due to antisymmetry)
 */
export function computeTorsionScalar(components: number[]): number {
  // T² = Σ T^a_{bc} T_a^{bc} (contracted with metric)
  // For a simplified 4D model with 6 independent components
  return components.reduce((sum, t) => sum + t * t, 0);
}

export function computeTraceVector(components: number[], dim: number = 4): number[] {
  // T_a = T^b_{ba} — trace over first and last index
  const trace = new Array(dim).fill(0);
  const idx = 0;
  for (let a = 0; a < dim; a++) {
    for (let b = 0; b < dim; b++) {
      trace[a] += components[Math.min(a * dim + b, components.length - 1)] || 0;
    }
  }
  return trace;
}

export function computeAxialTorsion(components: number[]): number {
  // Axial (pseudoscalar) part: S = ε_{abcd} T^{abcd}
  // Simplified: totally antisymmetric contraction
  if (components.length < 4) return 0;
  return components[0] * components[3] - components[1] * components[2];
}

/**
 * Einstein-Cartan field equation cost:
 * Minimizing this finds torsion configurations that satisfy
 * the Cartan equation: T^a_{bc} + δ^a_b T_c - δ^a_c T_b = 8πG s^a_{bc}
 *
 * Where s^a_{bc} is the spin angular momentum tensor.
 */
export function einsteinCartanResidual(params: Record<string, number>): number {
  const {
    T01, T02, T03, T12, T13, T23,  // 6 independent torsion components
    spinDensity,                      // spin source magnitude
    couplingLambda,                   // torsion-curvature coupling
  } = params;

  const torsionComponents = [T01, T02, T03, T12, T13, T23];
  const T2 = computeTorsionScalar(torsionComponents);
  const trace = computeTraceVector(torsionComponents);
  const axial = computeAxialTorsion(torsionComponents);

  // Cartan equation residual: |T - 8πG·s|²
  const G = 6.674e-11;
  const sourceStrength = 8 * Math.PI * G * spinDensity;

  // Field equation residual
  let residual = 0;
  for (const t of torsionComponents) {
    residual += (t - sourceStrength) ** 2;
  }

  // Action contribution: R + λT² should be stationary
  const actionTerm = couplingLambda * T2;

  // Trace constraint: T_a should be consistent with source
  const traceResidual = trace.reduce((s, v) => s + v * v, 0);

  // Total cost (minimize to find valid torsion configurations)
  return residual + 0.1 * actionTerm + 0.01 * traceResidual + 0.001 * axial * axial;
}

// ─── Teleparallel f(T) Gravity ───────────────────────────────────────────────

/**
 * Teleparallel gravity replaces curvature R with torsion scalar T.
 * f(T) generalizes the TEGR Lagrangian.
 *
 * Common f(T) models:
 *  - Power law: f(T) = α·T^n
 *  - Born-Infeld: f(T) = λ(√(1 + 2T/λ) - 1)
 *  - Logarithmic: f(T) = α·T + β·T·ln(T/T₀)
 *  - Exponential: f(T) = α·T(1 - e^{β·T₀/T})
 *
 * The agent finds optimal f(T) model parameters that match
 * observational data (SNIa, BAO, CMB).
 */

export function fTGravity_PowerLaw(T: number, alpha: number, n: number): number {
  return alpha * Math.pow(Math.abs(T), n) * Math.sign(T);
}

export function fTGravity_BornInfeld(T: number, lambda: number): number {
  return lambda * (Math.sqrt(1 + 2 * T / lambda) - 1);
}

export function fTGravity_Logarithmic(T: number, alpha: number, beta: number, T0: number): number {
  if (Math.abs(T) < 1e-30) return 0;
  return alpha * T + beta * T * Math.log(Math.abs(T / T0));
}

export function fTGravity_Exponential(T: number, alpha: number, beta: number, T0: number): number {
  if (Math.abs(T) < 1e-30) return 0;
  return alpha * T * (1 - Math.exp(beta * T0 / T));
}

// ─── Observational H(z) Data with Full Spatial Source Information ─────────────
//
// Each data point comes from a real survey, pointing at a real patch of sky.
// When the optimizer finds a deviation from ΛCDM at a specific redshift,
// these coordinates tell astrophysicists exactly WHERE IN SPACE to verify.

export interface HzObservation {
  z: number;              // redshift
  H: number;              // H(z) in km/s/Mpc
  sigma: number;          // 1σ uncertainty in km/s/Mpc
  method: string;         // measurement technique
  survey: string;         // survey/instrument name
  reference: string;      // publication reference
  ra: string;             // right ascension of survey center (J2000)
  dec: string;            // declination of survey center (J2000)
  skyArea_deg2: number;   // sky coverage in square degrees
  comovingDist_Mpc: number; // comoving distance at this z (Planck cosmology)
  lookbackTime_Gyr: number; // lookback time at this z
  fieldDescription: string; // what's physically at this location
}

export const HZ_OBSERVATIONS: HzObservation[] = [
  {
    z: 0.0, H: 67.4, sigma: 0.5,
    method: 'CMB (inverse distance ladder)',
    survey: 'Planck 2018',
    reference: 'Planck Collaboration, A&A 641, A6 (2020)',
    ra: 'Full sky', dec: 'Full sky',
    skyArea_deg2: 41253,
    comovingDist_Mpc: 0, lookbackTime_Gyr: 0,
    fieldDescription: 'CMB last scattering surface projected to z=0. Full-sky measurement.',
  },
  {
    z: 0.07, H: 69.0, sigma: 19.6,
    method: 'Differential age (cosmic chronometers)',
    survey: 'SDSS DR8 — Moresco+ 2012 sample',
    reference: 'Zhang et al., RAA 14, 1221 (2014)',
    ra: '12h 20m', dec: '+10° 00\'',
    skyArea_deg2: 7500,
    comovingDist_Mpc: 296, lookbackTime_Gyr: 0.95,
    fieldDescription: 'Passively evolving galaxies in SDSS North Galactic Cap. Age-dating ellipticals.',
  },
  {
    z: 0.09, H: 69.0, sigma: 12.0,
    method: 'Differential age (cosmic chronometers)',
    survey: 'SDSS DR7 — red galaxies',
    reference: 'Jimenez et al., ApJ 593, 622 (2003); Simon et al. (2005)',
    ra: '11h 50m', dec: '+15° 00\'',
    skyArea_deg2: 6670,
    comovingDist_Mpc: 380, lookbackTime_Gyr: 1.22,
    fieldDescription: 'SDSS main galaxy sample, luminous red galaxies at low-z.',
  },
  {
    z: 0.12, H: 68.6, sigma: 26.2,
    method: 'Differential age (cosmic chronometers)',
    survey: 'SDSS DR8 — passively evolving galaxies',
    reference: 'Zhang et al., RAA 14, 1221 (2014)',
    ra: '12h 00m', dec: '+12° 00\'',
    skyArea_deg2: 7500,
    comovingDist_Mpc: 502, lookbackTime_Gyr: 1.59,
    fieldDescription: 'Early-type galaxies with no ongoing star formation. SDSS spectroscopic sample.',
  },
  {
    z: 0.17, H: 83.0, sigma: 8.0,
    method: 'Differential age (cosmic chronometers)',
    survey: 'SDSS + GEMS (Galaxy Evolution from Morphologies and SEDs)',
    reference: 'Simon, Verde & Jimenez, PRD 71, 123001 (2005)',
    ra: '10h 46m', dec: '-04° 45\'',
    skyArea_deg2: 800,
    comovingDist_Mpc: 703, lookbackTime_Gyr: 2.18,
    fieldDescription: 'HST/ACS parallel field galaxies. Chandra Deep Field South region.',
  },
  {
    z: 0.20, H: 72.9, sigma: 29.6,
    method: 'Differential age (cosmic chronometers)',
    survey: 'SDSS DR8 — LRGs',
    reference: 'Zhang et al., RAA 14, 1221 (2014)',
    ra: '12h 30m', dec: '+20° 00\'',
    skyArea_deg2: 7500,
    comovingDist_Mpc: 820, lookbackTime_Gyr: 2.49,
    fieldDescription: 'SDSS Luminous Red Galaxies. North Galactic Cap spectroscopic survey.',
  },
  {
    z: 0.27, H: 77.0, sigma: 14.0,
    method: 'Differential age (cosmic chronometers)',
    survey: 'SDSS + 2SLAQ (2dF-SDSS LRG & QSO Survey)',
    reference: 'Simon, Verde & Jimenez, PRD 71, 123001 (2005)',
    ra: '11h 00m', dec: '+00° 00\'',
    skyArea_deg2: 2000,
    comovingDist_Mpc: 1090, lookbackTime_Gyr: 3.21,
    fieldDescription: '2dF + SDSS joint LRG sample along celestial equator.',
  },
  {
    z: 0.28, H: 88.8, sigma: 36.6,
    method: 'Differential age (cosmic chronometers)',
    survey: 'SDSS DR8',
    reference: 'Zhang et al., RAA 14, 1221 (2014)',
    ra: '13h 00m', dec: '+25° 00\'',
    skyArea_deg2: 7500,
    comovingDist_Mpc: 1130, lookbackTime_Gyr: 3.30,
    fieldDescription: 'SDSS spectroscopic galaxies, Coma-Virgo supercluster direction.',
  },
  {
    z: 0.35, H: 82.7, sigma: 8.4,
    method: 'BAO (galaxy clustering)',
    survey: 'SDSS-III BOSS LOWZ',
    reference: 'Chuang & Wang, MNRAS 435, 255 (2013)',
    ra: '12h 00m', dec: '+30° 00\'',
    skyArea_deg2: 8500,
    comovingDist_Mpc: 1390, lookbackTime_Gyr: 3.87,
    fieldDescription: 'BOSS LOWZ sample — 300K luminous red galaxies. BAO peak at ~105 h⁻¹ Mpc.',
  },
  {
    z: 0.40, H: 95.0, sigma: 17.0,
    method: 'Differential age (cosmic chronometers)',
    survey: 'SDSS + BOSS early data',
    reference: 'Simon, Verde & Jimenez, PRD 71, 123001 (2005)',
    ra: '14h 00m', dec: '+35° 00\'',
    skyArea_deg2: 3000,
    comovingDist_Mpc: 1570, lookbackTime_Gyr: 4.28,
    fieldDescription: 'Evolved galaxies at intermediate redshift. Boötes void direction.',
  },
  {
    z: 0.44, H: 82.6, sigma: 7.8,
    method: 'BAO (WiggleZ survey)',
    survey: 'WiggleZ Dark Energy Survey',
    reference: 'Blake et al., MNRAS 425, 405 (2012)',
    ra: '00h 55m', dec: '-27° 00\'',
    skyArea_deg2: 800,
    comovingDist_Mpc: 1710, lookbackTime_Gyr: 4.58,
    fieldDescription: 'WiggleZ 0h field — emission-line galaxies in the South Galactic Cap. Phoenix constellation.',
  },
  {
    z: 0.48, H: 97.0, sigma: 62.0,
    method: 'Differential age (cosmic chronometers)',
    survey: 'SDSS + archival spectra',
    reference: 'Stern et al., JCAP 02, 008 (2010)',
    ra: '10h 00m', dec: '+05° 00\'',
    skyArea_deg2: 4000,
    comovingDist_Mpc: 1850, lookbackTime_Gyr: 4.87,
    fieldDescription: 'Red envelope galaxies in SDSS. Leo-Virgo direction.',
  },
  {
    z: 0.57, H: 96.8, sigma: 3.4,
    method: 'BAO (galaxy clustering)',
    survey: 'SDSS-III BOSS CMASS (DR11)',
    reference: 'Anderson et al., MNRAS 441, 24 (2014)',
    ra: '12h 30m', dec: '+35° 00\'',
    skyArea_deg2: 8500,
    comovingDist_Mpc: 2150, lookbackTime_Gyr: 5.45,
    fieldDescription: 'BOSS CMASS — 900K massive galaxies. Highest precision BAO measurement at this epoch. Coma Berenices / Canes Venatici direction.',
  },
  {
    z: 0.59, H: 104.0, sigma: 13.0,
    method: 'Differential age (cosmic chronometers)',
    survey: 'BOSS spectroscopic (Moresco+ 2016)',
    reference: 'Moresco et al., JCAP 05, 014 (2016)',
    ra: '13h 00m', dec: '+30° 00\'',
    skyArea_deg2: 8500,
    comovingDist_Mpc: 2220, lookbackTime_Gyr: 5.56,
    fieldDescription: 'BOSS massive passively-evolving galaxies. D4000 spectral break age-dating.',
  },
  {
    z: 0.60, H: 87.9, sigma: 6.1,
    method: 'BAO (WiggleZ survey)',
    survey: 'WiggleZ Dark Energy Survey',
    reference: 'Blake et al., MNRAS 425, 405 (2012)',
    ra: '03h 10m', dec: '-28° 00\'',
    skyArea_deg2: 800,
    comovingDist_Mpc: 2250, lookbackTime_Gyr: 5.61,
    fieldDescription: 'WiggleZ 3h field — emission-line galaxies. Fornax constellation, near Fornax cluster.',
  },
  {
    z: 0.68, H: 92.0, sigma: 8.0,
    method: 'Differential age (cosmic chronometers)',
    survey: 'BOSS spectroscopic (Moresco+ 2012)',
    reference: 'Moresco et al., JCAP 08, 006 (2012)',
    ra: '14h 15m', dec: '+35° 00\'',
    skyArea_deg2: 7000,
    comovingDist_Mpc: 2520, lookbackTime_Gyr: 6.08,
    fieldDescription: 'Massive red galaxies at z~0.7. Boötes direction. 4000Å break method.',
  },
  {
    z: 0.73, H: 97.3, sigma: 7.0,
    method: 'BAO (WiggleZ survey)',
    survey: 'WiggleZ Dark Energy Survey',
    reference: 'Blake et al., MNRAS 425, 405 (2012)',
    ra: '22h 00m', dec: '-30° 00\'',
    skyArea_deg2: 800,
    comovingDist_Mpc: 2690, lookbackTime_Gyr: 6.37,
    fieldDescription: 'WiggleZ 22h field — emission-line galaxies. Aquarius / Piscis Austrinus.',
  },
  {
    z: 0.78, H: 105.0, sigma: 12.0,
    method: 'Differential age (cosmic chronometers)',
    survey: 'BOSS spectroscopic (Moresco+ 2016)',
    reference: 'Moresco et al., JCAP 05, 014 (2016)',
    ra: '12h 00m', dec: '+30° 00\'',
    skyArea_deg2: 8500,
    comovingDist_Mpc: 2840, lookbackTime_Gyr: 6.63,
    fieldDescription: 'BOSS galaxies at z~0.8. Virgo/Coma direction. Universe was 7.2 Gyr old.',
  },
  {
    z: 0.88, H: 90.0, sigma: 40.0,
    method: 'Differential age (cosmic chronometers)',
    survey: 'SDSS + archival spectra',
    reference: 'Stern et al., JCAP 02, 008 (2010)',
    ra: '16h 00m', dec: '+40° 00\'',
    skyArea_deg2: 3000,
    comovingDist_Mpc: 3120, lookbackTime_Gyr: 7.10,
    fieldDescription: 'Red galaxies near z~0.9. Hercules / Corona Borealis direction.',
  },
  {
    z: 1.04, H: 154.0, sigma: 20.0,
    method: 'Differential age (cosmic chronometers)',
    survey: 'zCOSMOS 20k spectroscopic survey',
    reference: 'Simon, Verde & Jimenez, PRD 71, 123001 (2005); Moresco+ (2012)',
    ra: '10h 00m 29s', dec: '+02° 12\' 21"',
    skyArea_deg2: 1.7,
    comovingDist_Mpc: 3540, lookbackTime_Gyr: 7.80,
    fieldDescription: 'COSMOS field — HST/ACS deep imaging. 2 sq. deg. of deep multi-band data. Sextans constellation.',
  },
  {
    z: 1.30, H: 168.0, sigma: 17.0,
    method: 'Differential age (cosmic chronometers)',
    survey: 'UDS (UKIDSS Ultra-Deep Survey) + archival spectra',
    reference: 'Simon, Verde & Jimenez, PRD 71, 123001 (2005)',
    ra: '02h 17m 48s', dec: '-05° 05\' 55"',
    skyArea_deg2: 0.77,
    comovingDist_Mpc: 4180, lookbackTime_Gyr: 8.72,
    fieldDescription: 'UKIDSS UDS field — deepest near-IR survey. 0.77 sq. deg. in Cetus/Fornax border.',
  },
  {
    z: 1.43, H: 177.0, sigma: 18.0,
    method: 'Differential age (cosmic chronometers)',
    survey: 'zCOSMOS deep spectroscopy',
    reference: 'Simon, Verde & Jimenez, PRD 71, 123001 (2005); Moresco+ (2012)',
    ra: '10h 00m 29s', dec: '+02° 12\' 21"',
    skyArea_deg2: 1.7,
    comovingDist_Mpc: 4500, lookbackTime_Gyr: 9.10,
    fieldDescription: 'COSMOS field at z>1.4. Universe was ~4.8 Gyr old. Galaxy stellar mass buildup epoch.',
  },
  {
    z: 1.53, H: 140.0, sigma: 14.0,
    method: 'Differential age (cosmic chronometers)',
    survey: 'BOSS + 3D-HST grism spectroscopy',
    reference: 'Moresco, MNRAS 450, L16 (2015)',
    ra: '12h 36m 50s', dec: '+62° 12\' 58"',
    skyArea_deg2: 625,
    comovingDist_Mpc: 4700, lookbackTime_Gyr: 9.33,
    fieldDescription: 'GOODS-North / Hubble Deep Field region. Ursa Major. Among deepest spectroscopy ever obtained.',
  },
  {
    z: 1.75, H: 202.0, sigma: 40.0,
    method: 'Differential age (cosmic chronometers)',
    survey: 'BOSS + archival deep spectra',
    reference: 'Simon, Verde & Jimenez, PRD 71, 123001 (2005)',
    ra: '14h 20m', dec: '+53° 00\'',
    skyArea_deg2: 2000,
    comovingDist_Mpc: 5100, lookbackTime_Gyr: 9.90,
    fieldDescription: 'Deep spectroscopic fields toward Boötes. Universe was ~3.9 Gyr old. Peak cosmic SFR epoch.',
  },
  {
    z: 2.34, H: 222.0, sigma: 7.0,
    method: 'BAO (Lyman-α forest)',
    survey: 'SDSS-III BOSS Lyman-α (DR11)',
    reference: 'Delubac et al., A&A 574, A59 (2015)',
    ra: '12h 00m', dec: '+20° 00\'',
    skyArea_deg2: 8500,
    comovingDist_Mpc: 5870, lookbackTime_Gyr: 10.87,
    fieldDescription: 'Lyman-α forest — intergalactic hydrogen absorption against 137K background QSOs. Universe was 2.9 Gyr old. Cosmic noon.',
  },
  {
    z: 2.36, H: 226.0, sigma: 8.0,
    method: 'BAO (Lyman-α cross-correlation with QSOs)',
    survey: 'SDSS-III BOSS Lyman-α × QSO (DR11)',
    reference: 'Font-Ribera et al., JCAP 05, 027 (2014)',
    ra: '12h 00m', dec: '+20° 00\'',
    skyArea_deg2: 8500,
    comovingDist_Mpc: 5900, lookbackTime_Gyr: 10.90,
    fieldDescription: 'QSO-Lyman-α cross-correlation. Same sky as Ly-α forest but independent statistical measurement.',
  },
];

/**
 * Compute per-data-point deviations between f(T) model and observations.
 * Returns spatial anomaly data: WHERE in space the torsion model diverges.
 */
export interface SpatialAnomaly {
  z: number;
  H_observed: number;
  H_LCDM: number;
  H_fT: number;
  deviation_kmsMpc: number;
  deviation_sigma: number;
  chi2_contribution: number;
  ra: string;
  dec: string;
  survey: string;
  reference: string;
  comovingDist_Mpc: number;
  lookbackTime_Gyr: number;
  fieldDescription: string;
  skyArea_deg2: number;
  anomalyType: 'excess' | 'deficit' | 'consistent';
  significance: 'high' | 'moderate' | 'low';
}

export function computeSpatialAnomalies(params: Record<string, number>): SpatialAnomaly[] {
  const { alpha, beta, n, lambda, modelType } = params;
  const H0 = 67.4;
  const OmegaM = 0.315;
  const anomalies: SpatialAnomaly[] = [];

  for (const obs of HZ_OBSERVATIONS) {
    const Hz_LCDM = H0 * Math.sqrt(OmegaM * Math.pow(1 + obs.z, 3) + (1 - OmegaM));
    const T = -6 * Hz_LCDM * Hz_LCDM;

    let fT: number;
    const mType = Math.round(modelType);
    switch (mType) {
      case 0: fT = fTGravity_PowerLaw(T, alpha, n); break;
      case 1: fT = fTGravity_BornInfeld(T, Math.abs(lambda) || 1); break;
      case 2: fT = fTGravity_Logarithmic(T, alpha, beta, -6 * H0 * H0); break;
      case 3: fT = fTGravity_Exponential(T, alpha, beta, -6 * H0 * H0); break;
      default: fT = fTGravity_PowerLaw(T, alpha, n);
    }

    const correction = fT / (6 * H0 * H0);
    const Hz_fT = Hz_LCDM * Math.sqrt(Math.max(0.01, 1 + correction));
    const deviation = Hz_fT - obs.H;
    const deviation_sigma = Math.abs(deviation) / obs.sigma;
    const chi2_i = (deviation / obs.sigma) ** 2;

    anomalies.push({
      z: obs.z,
      H_observed: obs.H,
      H_LCDM: Hz_LCDM,
      H_fT: Hz_fT,
      deviation_kmsMpc: deviation,
      deviation_sigma,
      chi2_contribution: chi2_i,
      ra: obs.ra,
      dec: obs.dec,
      survey: obs.survey,
      reference: obs.reference,
      comovingDist_Mpc: obs.comovingDist_Mpc,
      lookbackTime_Gyr: obs.lookbackTime_Gyr,
      fieldDescription: obs.fieldDescription,
      skyArea_deg2: obs.skyArea_deg2,
      anomalyType: Math.abs(deviation_sigma) < 1 ? 'consistent' : deviation > 0 ? 'excess' : 'deficit',
      significance: deviation_sigma > 3 ? 'high' : deviation_sigma > 2 ? 'moderate' : 'low',
    });
  }

  return anomalies;
}

/**
 * f(T) model fitness against cosmological expansion data.
 * The Friedmann equation in f(T) gravity:
 *   H² = (8πG/3)ρ - f/6 + Tf_T/3
 *
 * Where f_T = df/dT and T = -6H² in FLRW metric.
 */
export function fTCosmologyResidual(params: Record<string, number>): number {
  const { alpha, beta, n, lambda, modelType } = params;
  const H0 = 67.4;
  const OmegaM = 0.315;

  let chi2 = 0;
  for (const obs of HZ_OBSERVATIONS) {
    const Hz_LCDM = H0 * Math.sqrt(OmegaM * Math.pow(1 + obs.z, 3) + (1 - OmegaM));
    const T = -6 * Hz_LCDM * Hz_LCDM;

    let fT: number;
    const mType = Math.round(modelType);
    switch (mType) {
      case 0: fT = fTGravity_PowerLaw(T, alpha, n); break;
      case 1: fT = fTGravity_BornInfeld(T, Math.abs(lambda) || 1); break;
      case 2: fT = fTGravity_Logarithmic(T, alpha, beta, -6 * H0 * H0); break;
      case 3: fT = fTGravity_Exponential(T, alpha, beta, -6 * H0 * H0); break;
      default: fT = fTGravity_PowerLaw(T, alpha, n);
    }

    const correction = fT / (6 * H0 * H0);
    const Hz_fT = Hz_LCDM * Math.sqrt(Math.max(0.01, 1 + correction));
    chi2 += ((Hz_fT - obs.H) / obs.sigma) ** 2;
  }

  const regularization = 0.01 * (alpha * alpha + beta * beta + n * n);
  return chi2 + regularization;
}

// ─── Custom UFE Torsion Field (v2 — Non-trivial Physics) ─────────────────────

/**
 * Danny's UFE Torsion Field Theory — Version 2.
 *
 * Unified torsion-energy functional with Mexican-hat symmetry breaking,
 * fermion source coupling, and cosmological boundary conditions.
 *
 * The upgraded UFE action:
 *
 *   S_UFE = ∫ d⁴x √(-g) [ L_torsion + L_source + L_cosmo ]
 *
 * Where:
 *
 *   L_torsion = -μ²·T² + λ·T⁴ + γ·(∂T)² + ε·R·T²
 *     → Mexican-hat potential V(T) = -μ²T² + λT⁴  (spontaneous torsion condensation)
 *     → Vacuum expectation value: T_vev = ±μ/√(2λ)
 *     → Torsion mass around VEV: m_T² = 4μ² (massive propagating torsion)
 *
 *   L_source = κ_f · (ψ̄ γ⁵ ψ) · T + κ_g · G_μν T^μν
 *     → Fermion axial current couples to torsion (Hehl minimal coupling)
 *     → Einstein tensor back-reaction on torsion
 *
 *   L_cosmo = -ρ_Λ · f(T/T_vev) + Ω_T · T²/(T² + T_c²)
 *     → Torsion contribution to dark energy via f(T/T_vev)
 *     → Screening mechanism: torsion decouples when T >> T_c
 *
 * Physical constraints:
 *   1. Mexican hat: μ² > 0, λ > 0 (spontaneous breaking, bounded below)
 *   2. Causality: v² = γ/(2μ²) ≤ 1
 *   3. Fermion coupling: |κ_f| < 4π (perturbative)
 *   4. Cosmological: torsion dark energy fraction Ω_T < 0.73
 *   5. Solar system: |T_vev| < 10⁻¹⁰ m⁻² (PPN bounds)
 *   6. Nucleosynthesis: torsion decoupled by T_BBN ~ 1 MeV
 */
export function ufeTorsionFunctional(params: Record<string, number>): number {
  const {
    mu2,        // μ² — mass² parameter (positive for symmetry breaking)
    lambda,     // λ — quartic coupling (positive for stability)
    gamma,      // γ — gradient/kinetic term
    epsilon,    // ε — curvature-torsion mixing R·T²
    kappa_f,    // κ_f — fermion axial coupling
    kappa_g,    // κ_g — graviton-torsion coupling
    T0,         // background torsion field value (natural units)
    nDensity,   // fermion number density (natural units, ~n_baryon)
  } = params;

  // ── Mexican-hat potential: V(T) = -μ²T² + λT⁴ ──
  const T2 = T0 * T0;
  const T4 = T2 * T2;
  const V_mexican = -mu2 * T2 + lambda * T4;

  // Vacuum expectation value (if symmetry is broken)
  const T_vev = mu2 > 0 && lambda > 0 ? Math.sqrt(mu2 / (2 * lambda)) : 0;

  // Torsion mass around VEV: m² = V''(T_vev) = -2μ² + 12λT_vev² = 4μ²
  const m_T2 = 4 * mu2;

  // Kinetic/gradient energy
  // For homogeneous background: (∂T)² ~ 0, but we penalize large gradients
  const kinetic = 0.5 * gamma * T2 * 0.01; // approximate

  // Curvature-torsion mixing (use observed cosmological R ~ 6H₀²(2Ω_m - Ω_Λ + 2))
  const H0_natural = 2.2e-18; // H₀ in s⁻¹ → natural units
  const R_cosmo = 12 * H0_natural * H0_natural; // de Sitter-like
  const mixing = epsilon * R_cosmo * T2;

  // ── Fermion source: L_source = κ_f · n_f · T ──
  // Axial current <ψ̄γ⁵ψ> ~ spin-polarized fraction of fermion density
  const spinPolarization = 0.01; // ~1% spin alignment in cosmological context
  const axialSource = kappa_f * nDensity * spinPolarization * T0;

  // Graviton back-reaction: κ_g · G_μν T^μν ~ κ_g · R · T²
  const gravitonSource = kappa_g * R_cosmo * T2;

  // ── Cosmological sector ──
  // Torsion dark energy contribution: ρ_T = V(T_vev) + kinetic
  const rho_torsion = Math.abs(V_mexican) + kinetic;
  // Critical density today
  const rho_crit = 3 * H0_natural * H0_natural / (8 * Math.PI * 6.674e-11);
  // Dark energy fraction from torsion
  const Omega_T = rho_crit > 0 ? rho_torsion / rho_crit : 0;

  // Screening: torsion effects suppressed at high densities
  const T_screen = T_vev > 0 ? T2 / (T2 + T_vev * T_vev) : 1;

  // ── Total action density (to be made stationary) ──
  const action = V_mexican + kinetic + mixing + axialSource + gravitonSource;

  // ── Field equation residual ──
  // δS/δT = 0 → -2μ²T + 4λT³ + γ□T + 2εRT + κ_f·n·p = 0
  // For homogeneous background (□T = 0):
  const fieldEqn = -2 * mu2 * T0 + 4 * lambda * T0 * T2
    + 2 * epsilon * R_cosmo * T0
    + kappa_f * nDensity * spinPolarization;
  const fieldResidual = fieldEqn * fieldEqn;

  // ── Physical constraint penalties ──
  let penalty = 0;

  // 1. Mexican hat requires μ² > 0 AND λ > 0
  if (mu2 <= 0) penalty += 50 * mu2 * mu2;
  if (lambda <= 0) penalty += 50 * lambda * lambda;

  // 2. Causality: propagation speed v² = γ/(2μ²) ≤ 1
  if (mu2 > 0 && gamma > 0) {
    const v2 = gamma / (2 * mu2);
    if (v2 > 1) penalty += 20 * (v2 - 1);
  }

  // 3. Perturbativity: |κ_f| < 4π
  if (Math.abs(kappa_f) > 4 * Math.PI) penalty += 10 * (Math.abs(kappa_f) - 4 * Math.PI) ** 2;

  // 4. Cosmological bound: Ω_T should contribute to but not exceed dark energy
  const omega_target = 0.68;
  const cosmoPenalty = (Omega_T - omega_target) ** 2;

  // 5. NON-TRIVIAL TORSION — hard log-barrier near T₀ = 0
  // The whole point is to find T₀ ≈ ±T_vev, NOT T₀ = 0.
  // Log-barrier: blows up as |T₀| → 0, forcing optimizer away from vacuum.
  const absT0 = Math.abs(T0);
  const T0_floor = 1e-20; // absolute minimum — below this is numerical noise
  const logBarrier = absT0 > T0_floor
    ? 100 * Math.max(0, -Math.log10(absT0) - 5) ** 2  // penalize |T₀| < 1e-5
    : 1e6; // nuclear option: T₀ at machine epsilon → massive penalty

  // 6. VEV proximity: T₀ must sit near the VEV, not at zero
  // Weight 10x (was 0.1x — that's why optimizer cheated)
  const vevResidual = T_vev > 0
    ? ((absT0 - T_vev) / (T_vev + 1e-30)) ** 2
    : 100; // no VEV possible → heavy penalty (forces μ²>0, λ>0)

  // 7. Minimum VEV scale: T_vev must be physically meaningful
  // Below ~1e-15 (natural units) torsion is unobservable
  const minVevScale = 1e-15;
  const vevScalePenalty = T_vev > 0 && T_vev < minVevScale
    ? 50 * (Math.log10(minVevScale / T_vev)) ** 2
    : 0;

  // 8. BBN consistency: torsion mass must decouple before nucleosynthesis
  const m_T = Math.sqrt(Math.max(0, m_T2));
  const bbnScale = 5.07e9;
  const bbnPenalty = m_T < bbnScale ? (1 - m_T / bbnScale) ** 2 : 0;

  // ── Cost function: find NON-TRIVIAL solutions to the field equation ──
  // The log-barrier and VEV proximity are weighted heavily to prevent
  // the optimizer from collapsing to the trivial T₀=0 vacuum.
  return fieldResidual
    + 10 * vevResidual      // 100x stronger than before
    + logBarrier             // hard wall against T₀→0
    + vevScalePenalty        // VEV must be physically real
    + penalty
    + 0.5 * cosmoPenalty
    + 0.3 * bbnPenalty;
}

// ─── Cross-Domain UFE: Unified Torsion Coupling ──────────────────────────────

/**
 * Cross-domain coupling: links Einstein-Cartan, f(T), and wave propagation
 * into a single unified optimization.
 *
 * The full UFE field equation system:
 *
 *   (I)   Cartan equation:  T^a_{bc} = 8πG·s^a_{bc}     (microscopic)
 *   (II)  Modified Friedmann: H² = (8πG/3)ρ - f(T)/6     (cosmological)
 *   (III) Wave equation: □T + m²T + λT³ = J               (propagation)
 *   (IV)  VEV condition: T₀ = μ/√(2λ)                     (symmetry breaking)
 *
 * Consistency requires:
 *   - The torsion scalar from (I) feeds into f(T) in (II)
 *   - The mass m in (III) equals 2μ from the Mexican hat
 *   - The wave source J comes from the spin density in (I)
 *   - The VEV (IV) is compatible with cosmological bounds from (II)
 */
export function crossDomainUFE(params: Record<string, number>): number {
  const {
    // Shared torsion parameters
    T_scalar,       // torsion scalar magnitude
    mu2,            // Mexican hat mass² parameter
    lambda_quartic, // quartic self-coupling

    // Einstein-Cartan sector
    spinDensity,    // spin source magnitude
    ec_coupling,    // torsion-curvature coupling

    // f(T) sector
    fT_alpha,       // f(T) model amplitude
    fT_n,           // f(T) power law exponent

    // Wave sector
    wave_freq,      // torsion wave frequency
    wave_source,    // spin current source

    // Cosmological
    H0_rescaled,    // H₀ in units of 70 km/s/Mpc
  } = params;

  const H0 = H0_rescaled * 70.0; // km/s/Mpc
  const OmegaM = 0.315;

  // ── (I) Einstein-Cartan residual ──
  const G = 6.674e-11;
  const ec_source = 8 * Math.PI * G * spinDensity;
  const ec_residual = (T_scalar - ec_source) ** 2
    + ec_coupling * T_scalar * T_scalar;

  // ── (II) f(T) cosmology ──
  const T_cosmo = -6 * H0 * H0; // T = -6H² in FLRW
  const fT = fT_alpha * Math.pow(Math.abs(T_cosmo), fT_n) * Math.sign(T_cosmo);
  // Modified Friedmann: deviation from ΛCDM
  const Hz_predicted = H0 * Math.sqrt(Math.max(0.01, OmegaM + (1 - OmegaM) + fT / (6 * H0 * H0)));
  const cosmo_residual = ((Hz_predicted - 67.4) / 3.37) ** 2; // 5% uncertainty on H₀

  // ── (III) Wave equation consistency ──
  // Mass from Mexican hat: m_T² = 4μ²
  const mT2 = 4 * mu2;
  // Wave equation at VEV: □T + m²T + λT³ = J
  const T_vev = mu2 > 0 && lambda_quartic > 0 ? Math.sqrt(mu2 / (2 * lambda_quartic)) : 0;
  // For standing wave perturbation around VEV:
  // ω² = m² + 3λT_vev²·k² (dispersion relation)
  const omega2 = mT2 + 3 * lambda_quartic * T_vev * T_vev;
  const wave_residual = omega2 > 0
    ? (wave_freq * wave_freq - omega2) ** 2 / (omega2 * omega2 + 1e-30)
    : 10;

  // Source consistency: J should match spin density
  const J_expected = 8 * Math.PI * G * spinDensity * T_vev;
  const source_residual = (wave_source - J_expected) ** 2 / (J_expected * J_expected + 1e-30);

  // ── (IV) Cross-domain consistency ──
  // The torsion scalar from EC must be compatible with the f(T) torsion
  const ec_fT_consistency = T_scalar !== 0
    ? ((T_scalar * T_scalar - Math.abs(T_cosmo)) / (Math.abs(T_cosmo) + 1e-30)) ** 2
    : 0;

  // VEV must be within observational bounds AND physically meaningful
  const vev_penalty = T_vev > 0
    ? Math.max(0, Math.log10(T_vev) - (-10)) ** 2
    : 50; // no VEV → heavy penalty

  // Mexican hat stability
  let stability_penalty = 0;
  if (mu2 <= 0) stability_penalty += 20;
  if (lambda_quartic <= 0) stability_penalty += 20;

  // Non-trivial torsion barrier: T_scalar must not collapse to zero
  const absT = Math.abs(T_scalar);
  const crossLogBarrier = absT > 1e-20
    ? 50 * Math.max(0, -Math.log10(absT) - 5) ** 2
    : 1e5;

  // VEV proximity: T_scalar should be near the VEV, not zero
  const crossVevResidual = T_vev > 1e-20
    ? 5 * ((absT - T_vev) / (T_vev + 1e-30)) ** 2
    : 50;

  // ── Total unified cost ──
  return ec_residual
    + 0.5 * cosmo_residual
    + 0.3 * wave_residual
    + 0.2 * source_residual
    + 0.1 * ec_fT_consistency
    + vev_penalty
    + stability_penalty
    + crossLogBarrier
    + crossVevResidual;
}

/**
 * Torsion wave equation residual — Version 2.
 * Upgraded with Mexican-hat dispersion and fermion source.
 *
 * The massive torsion wave around VEV:
 *   □δT + m_T²·δT + 3λ·T_vev²·δT = J_spin
 *
 * where δT = T - T_vev is the perturbation,
 * m_T² = 4μ² is the torsion mass from symmetry breaking,
 * and J_spin is the spin current from fermion matter.
 *
 * Dispersion relation: ω² = k² + m_T² + 3λT_vev²
 * Group velocity: v_g = k/ω (always subluminal for m_T > 0)
 */
export function torsionWaveResidual(params: Record<string, number>): number {
  const {
    mu2,           // Mexican hat mass² parameter
    lambda_q,      // quartic self-coupling
    amplitude,     // wave amplitude δT
    frequency,     // wave angular frequency ω
    wavenumber,    // spatial wavenumber k
    phase,         // phase offset
    J_spin,        // spin current source
  } = params;

  // Torsion mass and VEV from Mexican hat
  const mT2 = 4 * Math.max(0, mu2);
  const T_vev = mu2 > 0 && lambda_q > 0 ? Math.sqrt(mu2 / (2 * lambda_q)) : 0;
  const effectiveMass2 = mT2 + 3 * lambda_q * T_vev * T_vev;

  // Sample wave equation residual: □δT + m_eff²·δT = J
  // □ = -∂²/∂t² + ∂²/∂x² (Minkowski signature -+++)
  let totalResidual = 0;
  const nPoints = 80;

  for (let i = 0; i < nPoints; i++) {
    const t = (i / nPoints) * 4 * Math.PI;

    // Wave ansatz: δT(t,x) = A·sin(ωt - kx + φ)
    const arg = frequency * t - wavenumber * t * 0.3 + phase; // simplified 1D
    const dT = amplitude * Math.sin(arg);
    const d2T_dt2 = -amplitude * frequency * frequency * Math.sin(arg);
    const d2T_dx2 = -amplitude * wavenumber * wavenumber * Math.sin(arg);

    // □δT = -d²/dt² + d²/dx² (signature -+++)
    const boxT = -d2T_dt2 + d2T_dx2;

    // Non-linear term: 3λ·T_vev · δT² (from expansion around VEV)
    const nonlinear = 3 * lambda_q * T_vev * dT * dT;

    // Field equation: □δT + m_eff²·δT + nonlinear = J_spin
    const residual = boxT + effectiveMass2 * dT + nonlinear - J_spin;
    totalResidual += residual * residual;
  }
  totalResidual /= nPoints;

  // Dispersion relation check: ω² = k² + m_eff²
  const dispersion = (frequency * frequency - wavenumber * wavenumber - effectiveMass2);
  const dispersionResidual = dispersion * dispersion / (effectiveMass2 * effectiveMass2 + 1e-30);

  // Causality: group velocity v_g = k/ω must be ≤ 1
  const v_group = frequency > 0 ? Math.abs(wavenumber) / frequency : 0;
  const causalityPenalty = v_group > 1 ? 50 * (v_group - 1) ** 2 : 0;

  // Stability: μ² > 0, λ > 0
  let stability = 0;
  if (mu2 <= 0) stability += 20;
  if (lambda_q <= 0) stability += 20;

  // Physical amplitude bounds
  const ampPenalty = Math.abs(amplitude) > 1e6 ? (amplitude / 1e6) ** 2 : 0;

  return totalResidual
    + 0.5 * dispersionResidual
    + causalityPenalty
    + stability
    + 0.001 * ampPenalty;
}

// ─── Pre-built Tasks for AEGIS/Seeker ────────────────────────────────────────

/** Einstein-Cartan torsion optimization task */
export const einsteinCartanTask: Task = {
  id: 'einstein-cartan',
  name: 'Einstein-Cartan Torsion',
  evaluate: einsteinCartanResidual,
  parameters: [
    { name: 'T01', min: -1, max: 1, description: 'Torsion T^0_{01}' },
    { name: 'T02', min: -1, max: 1, description: 'Torsion T^0_{02}' },
    { name: 'T03', min: -1, max: 1, description: 'Torsion T^0_{03}' },
    { name: 'T12', min: -1, max: 1, description: 'Torsion T^1_{12}' },
    { name: 'T13', min: -1, max: 1, description: 'Torsion T^1_{13}' },
    { name: 'T23', min: -1, max: 1, description: 'Torsion T^2_{23}' },
    { name: 'spinDensity', min: 0, max: 1e20, description: 'Spin density magnitude' },
    { name: 'couplingLambda', min: -10, max: 10, description: 'Torsion-curvature coupling' },
  ],
};

/** f(T) teleparallel gravity cosmology task */
export const fTGravityTask: Task = {
  id: 'ft-gravity',
  name: 'f(T) Teleparallel Gravity',
  evaluate: fTCosmologyResidual,
  parameters: [
    { name: 'alpha', min: -5, max: 5, description: 'f(T) primary coupling' },
    { name: 'beta', min: -5, max: 5, description: 'f(T) secondary coupling' },
    { name: 'n', min: 0.5, max: 3, description: 'Power law exponent' },
    { name: 'lambda', min: 0.01, max: 1000, description: 'Born-Infeld scale' },
    { name: 'modelType', min: 0, max: 3, step: 1, description: '0=power, 1=BI, 2=log, 3=exp' },
  ],
};

/** UFE torsion field theory task — v3 with hard non-trivial barriers */
export const ufeTorsionTask: Task = {
  id: 'ufe-torsion',
  name: 'UFE Torsion Field (Mexican Hat v3)',
  evaluate: ufeTorsionFunctional,
  parameters: [
    { name: 'mu2', min: 1e-5, max: 1e20, description: 'μ² mass parameter (must be positive for SSB)' },
    { name: 'lambda', min: 1e-4, max: 10, description: 'λ quartic coupling (must be positive)' },
    { name: 'gamma', min: 0.01, max: 10, description: 'γ kinetic/gradient term' },
    { name: 'epsilon', min: -2, max: 2, description: 'ε curvature-torsion mixing' },
    { name: 'kappa_f', min: -10, max: 10, description: 'κ_f fermion axial coupling' },
    { name: 'kappa_g', min: -5, max: 5, description: 'κ_g graviton-torsion coupling' },
    { name: 'T0', min: 1e-12, max: 1e-3, description: 'Background torsion (forced non-zero)' },
    { name: 'nDensity', min: 1, max: 1e6, description: 'Fermion number density (natural units)' },
  ],
};

/** Torsion wave propagation task — v2 with dispersion relation */
export const torsionWaveTask: Task = {
  id: 'torsion-wave',
  name: 'Torsion Wave Dispersion',
  evaluate: torsionWaveResidual,
  parameters: [
    { name: 'mu2', min: 0.01, max: 1e15, description: 'μ² from Mexican hat' },
    { name: 'lambda_q', min: 0.001, max: 5, description: 'λ quartic coupling' },
    { name: 'amplitude', min: -1e3, max: 1e3, description: 'Wave amplitude δT' },
    { name: 'frequency', min: 0.1, max: 1000, description: 'Angular frequency ω' },
    { name: 'wavenumber', min: 0.01, max: 500, description: 'Spatial wavenumber k' },
    { name: 'phase', min: 0, max: 6.283, description: 'Phase offset' },
    { name: 'J_spin', min: -100, max: 100, description: 'Spin current source' },
  ],
};

/** Cross-domain unified torsion task — v3 with non-trivial barriers */
export const crossDomainTask: Task = {
  id: 'ufe-cross-domain',
  name: 'UFE Cross-Domain Unified v3',
  evaluate: crossDomainUFE,
  parameters: [
    { name: 'T_scalar', min: 1e-10, max: 1, description: 'Torsion scalar magnitude (forced non-zero)' },
    { name: 'mu2', min: 1e-3, max: 1e10, description: 'μ² mass parameter (positive for SSB)' },
    { name: 'lambda_quartic', min: 1e-3, max: 5, description: 'Quartic self-coupling (positive)' },
    { name: 'spinDensity', min: 1, max: 1e15, description: 'Spin source (non-zero)' },
    { name: 'ec_coupling', min: -5, max: 5, description: 'EC torsion-curvature coupling' },
    { name: 'fT_alpha', min: -3, max: 3, description: 'f(T) amplitude' },
    { name: 'fT_n', min: 0.5, max: 2.5, description: 'f(T) power law index' },
    { name: 'wave_freq', min: 0.1, max: 500, description: 'Torsion wave frequency' },
    { name: 'wave_source', min: -100, max: 100, description: 'Wave spin current source' },
    { name: 'H0_rescaled', min: 0.9, max: 1.1, description: 'H₀ in units of 70 km/s/Mpc' },
  ],
};

/** All torsion tasks bundled */
export const torsionTasks = {
  einsteinCartan: einsteinCartanTask,
  fTGravity: fTGravityTask,
  ufeTorsion: ufeTorsionTask,
  torsionWave: torsionWaveTask,
  crossDomain: crossDomainTask,
};
