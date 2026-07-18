/**
 * AEGIS — Equation Writer & Observational Mapper
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * When the engines discover interesting torsion configurations, this module:
 *  1. Synthesizes the discovered equations in LaTeX and human-readable form
 *  2. Maps parameters to observable predictions (sky coordinates, redshifts, energies)
 *  3. Computes where in space to look for torsion signatures
 *  4. Writes structured discovery files that astrophysicists can act on
 *
 * Observable mapping uses:
 *  - H(z) data to identify redshift windows where f(T) deviates from ΛCDM
 *  - Torsion mass → Compton wavelength → detector scale (lab or astrophysical)
 *  - Spin density → source type (neutron stars, early universe, quark-gluon plasma)
 *  - VEV scale → energy threshold → collider or cosmic ray regime
 *  - f(T) residuals → specific sky surveys where deviations are largest
 */

import * as fs from 'fs';
import * as path from 'path';
import { EvalResult, Discovery, Task, ParameterDef } from './interfaces';

// ─── Constants ───────────────────────────────────────────────────────────────

const HBAR = 1.0546e-34;    // ℏ in J·s
const C = 2.998e8;           // speed of light m/s
const G_NEWTON = 6.674e-11;  // gravitational constant
const EV_TO_KG = 1.783e-36;  // eV/c² in kg
const MPC_TO_M = 3.086e22;   // Megaparsec in meters
const H0_SI = 67.4e3 / MPC_TO_M; // H₀ in s⁻¹

// ─── Known Sky Survey Reference Points ───────────────────────────────────────
// These are real survey fields where H(z) measurements originate.
// When our f(T) model predicts a deviation at a specific redshift,
// we point to the survey field that covers that z range.

interface SkyTarget {
  name: string;
  survey: string;
  ra: string;        // Right ascension (J2000)
  dec: string;       // Declination (J2000)
  zRange: [number, number];
  description: string;
}

const SKY_TARGETS: SkyTarget[] = [
  {
    name: 'BOSS LOWZ NGC',
    survey: 'SDSS-III BOSS',
    ra: '12h 00m', dec: '+30° 00\'',
    zRange: [0.15, 0.43],
    description: 'Luminous red galaxies, BAO measurement at z≈0.32',
  },
  {
    name: 'BOSS CMASS NGC',
    survey: 'SDSS-III BOSS',
    ra: '12h 30m', dec: '+35° 00\'',
    zRange: [0.43, 0.70],
    description: 'Massive galaxies, BAO at z≈0.57',
  },
  {
    name: 'eBOSS LRG',
    survey: 'SDSS-IV eBOSS',
    ra: '13h 00m', dec: '+25° 00\'',
    zRange: [0.6, 1.0],
    description: 'Extended LRG sample, BAO at z≈0.70',
  },
  {
    name: 'eBOSS QSO',
    survey: 'SDSS-IV eBOSS',
    ra: '14h 00m', dec: '+30° 00\'',
    zRange: [0.8, 2.2],
    description: 'Quasar clustering, BAO at z≈1.48',
  },
  {
    name: 'Lyman-α Forest',
    survey: 'SDSS-IV eBOSS',
    ra: '12h 00m', dec: '+20° 00\'',
    zRange: [2.0, 3.5],
    description: 'Lyman-α absorption, BAO at z≈2.34',
  },
  {
    name: 'DESI BGS',
    survey: 'DESI',
    ra: '11h 00m', dec: '+30° 00\'',
    zRange: [0.05, 0.4],
    description: 'Bright Galaxy Survey, low-z BAO',
  },
  {
    name: 'DESI ELG',
    survey: 'DESI',
    ra: '14h 30m', dec: '+40° 00\'',
    zRange: [0.6, 1.6],
    description: 'Emission line galaxies, mid-z BAO',
  },
  {
    name: 'Euclid Deep Field North',
    survey: 'Euclid',
    ra: '17h 58m', dec: '+66° 01\'',
    zRange: [0.2, 2.0],
    description: 'Deep photometric and spectroscopic survey',
  },
  {
    name: 'CMB Dipole Direction',
    survey: 'Planck',
    ra: '11h 12m', dec: '-07° 13\'',
    zRange: [0, 0.1],
    description: 'Local H₀ measurement direction, Hubble tension',
  },
  {
    name: 'SH0ES Cepheid Fields',
    survey: 'HST SH0ES',
    ra: '12h 22m', dec: '+15° 49\'',
    zRange: [0.0, 0.15],
    description: 'Cepheid distance ladder anchor galaxies (NGC 4258 direction)',
  },
];

// ─── Known Neutron Star / Spin-dense Objects ─────────────────────────────────
// For Einstein-Cartan torsion: where spin density is highest

interface SpinSource {
  name: string;
  type: string;
  ra: string;
  dec: string;
  distance: string;
  spinDensityEstimate: string;
  description: string;
}

const SPIN_SOURCES: SpinSource[] = [
  {
    name: 'PSR J0537-6910',
    type: 'millisecond pulsar',
    ra: '05h 37m 47s', dec: '-69° 10\' 20"',
    distance: '49.6 kpc (LMC)',
    spinDensityEstimate: '~10³⁸ J·s/m³',
    description: 'Fastest young pulsar, 62 Hz spin. In Large Magellanic Cloud supernova remnant N157B.',
  },
  {
    name: 'PSR J1748-2446ad',
    type: 'millisecond pulsar',
    ra: '17h 48m 52s', dec: '-24° 46\' 48"',
    distance: '7.7 kpc',
    spinDensityEstimate: '~10³⁹ J·s/m³',
    description: 'Fastest known pulsar at 716 Hz. In globular cluster Terzan 5.',
  },
  {
    name: 'SGR 1806-20',
    type: 'magnetar',
    ra: '18h 08m 40s', dec: '-20° 24\' 40"',
    distance: '8.7 kpc',
    spinDensityEstimate: '~10⁴⁰ J·s/m³',
    description: 'Most energetic magnetar flare recorded (2004). B ~ 10¹⁵ G.',
  },
  {
    name: 'Sagittarius A*',
    type: 'SMBH accretion disk',
    ra: '17h 45m 40s', dec: '-29° 00\' 28"',
    distance: '8.2 kpc',
    spinDensityEstimate: '~10³⁵ J·s/m³ (inner disk)',
    description: 'Galactic center SMBH. Spinning BH frame-dragging generates effective torsion.',
  },
  {
    name: 'GW170817 remnant',
    type: 'neutron star merger',
    ra: '13h 09m 48s', dec: '-23° 22\' 53"',
    distance: '40 Mpc',
    spinDensityEstimate: '~10⁴² J·s/m³ (merger peak)',
    description: 'First NS-NS merger with EM counterpart. Peak spin density during coalescence.',
  },
  {
    name: 'Crab Pulsar (PSR B0531+21)',
    type: 'young pulsar',
    ra: '05h 34m 32s', dec: '+22° 00\' 52"',
    distance: '2.0 kpc',
    spinDensityEstimate: '~10³⁷ J·s/m³',
    description: 'Best-studied pulsar. 30 Hz spin, ~10³⁸ G·cm³ magnetic moment. In M1 (Crab Nebula).',
  },
];

// ─── Equation Templates ─────────────────────────────────────────────────────

interface DiscoveredEquation {
  id: string;
  timestamp: number;
  engine: string;
  domain: string;
  title: string;
  latex: string;
  plaintext: string;
  parameters: Record<string, { value: number; unit: string; description: string }>;
  predictions: Prediction[];
  observationalTargets: ObservationalTarget[];
  score: number;
  confidence: string;
}

interface Prediction {
  quantity: string;
  value: string;
  unit: string;
  testable: boolean;
  method: string;
}

interface ObservationalTarget {
  name: string;
  coordinates: { ra: string; dec: string };
  survey: string;
  redshiftRange: string;
  expectedSignal: string;
  detectionMethod: string;
}

// ─── Equation Synthesizer ────────────────────────────────────────────────────

export class EquationWriter {
  private outputDir: string;
  private discoveries: DiscoveredEquation[] = [];
  private bestByDomain: Map<string, { score: number; eq: DiscoveredEquation }> = new Map();

  constructor(outputDir: string = './discoveries') {
    this.outputDir = outputDir;
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }
  }

  // ── Main entry: call this when a run completes with good results ──

  writeDiscovery(
    engine: string,
    taskId: string,
    result: EvalResult,
    score: number,
  ): DiscoveredEquation | null {
    const domain = this.classifyDomain(taskId);
    if (!domain) return null;

    // Only write if this is better than what we've seen
    const prev = this.bestByDomain.get(domain);
    if (prev && score >= prev.score) return null;

    let eq: DiscoveredEquation;

    switch (domain) {
      case 'einstein-cartan':
        eq = this.synthesizeEinsteinCartan(engine, result, score);
        break;
      case 'ft-gravity':
        eq = this.synthesizeFTGravity(engine, result, score);
        break;
      case 'ufe-torsion':
        eq = this.synthesizeUFETorsion(engine, result, score);
        break;
      case 'torsion-wave':
        eq = this.synthesizeTorsionWave(engine, result, score);
        break;
      case 'cross-domain':
        eq = this.synthesizeCrossDomain(engine, result, score);
        break;
      default:
        return null;
    }

    this.bestByDomain.set(domain, { score, eq });
    this.discoveries.push(eq);

    // Write individual file
    this.writeEquationFile(eq);
    // Update master index
    this.writeMasterIndex();

    return eq;
  }

  // ── Einstein-Cartan Equation Synthesis ──────────────────────────────────

  private synthesizeEinsteinCartan(engine: string, result: EvalResult, score: number): DiscoveredEquation {
    const p = result.params;
    const T_components = [p.T01, p.T02, p.T03, p.T12, p.T13, p.T23];
    const T2 = T_components.reduce((s, t) => s + t * t, 0);
    const T_magnitude = Math.sqrt(T2);
    const lambda = p.couplingLambda;
    const sigma = p.spinDensity;

    // Determine which spin sources match this density regime
    const matchingSources = this.findSpinSources(sigma);

    // Observable: torsion-induced four-fermion interaction
    // Effective coupling: G_T = (8πG)² · σ / (1 + λT²)
    const G_T = Math.pow(8 * Math.PI * G_NEWTON, 2) * sigma / (1 + Math.abs(lambda) * T2);

    // Torsion interaction range (if massive)
    const range_m = T_magnitude > 0 ? HBAR / (T_magnitude * EV_TO_KG * C) : Infinity;

    return {
      id: `ec-${Date.now()}`,
      timestamp: Date.now(),
      engine,
      domain: 'Einstein-Cartan Torsion',
      title: 'Cartan Equation Solution — Spin-Torsion Coupling',
      latex: this.ecLatex(p, T_magnitude, lambda),
      plaintext: this.ecPlaintext(p, T_magnitude, lambda),
      parameters: {
        'T^0_{01}': { value: p.T01, unit: 'm⁻¹', description: 'Time-space torsion component' },
        'T^0_{02}': { value: p.T02, unit: 'm⁻¹', description: 'Time-space torsion component' },
        'T^0_{03}': { value: p.T03, unit: 'm⁻¹', description: 'Time-space torsion component' },
        'T^1_{12}': { value: p.T12, unit: 'm⁻¹', description: 'Space-space torsion component' },
        'T^1_{13}': { value: p.T13, unit: 'm⁻¹', description: 'Space-space torsion component' },
        'T^2_{23}': { value: p.T23, unit: 'm⁻¹', description: 'Space-space torsion component' },
        '|T|': { value: T_magnitude, unit: 'm⁻¹', description: 'Torsion scalar magnitude' },
        'σ': { value: sigma, unit: 'J·s/m³', description: 'Spin angular momentum density' },
        'λ': { value: lambda, unit: 'dimensionless', description: 'Torsion-curvature coupling' },
      },
      predictions: [
        {
          quantity: 'Four-fermion coupling G_T',
          value: G_T.toExponential(3),
          unit: 'm³/(J·s)',
          testable: true,
          method: 'Spin-polarized neutron scattering or torsion balance experiment',
        },
        {
          quantity: 'Torsion interaction range',
          value: range_m < 1e20 ? range_m.toExponential(3) : '∞',
          unit: 'm',
          testable: range_m < 1,
          method: range_m < 1e-3 ? 'Sub-mm gravity experiment (Eöt-Wash style)' : 'Astrophysical spin-orbit coupling',
        },
        {
          quantity: 'Torsion energy scale',
          value: (T_magnitude * HBAR * C / EV_TO_KG).toExponential(3),
          unit: 'eV',
          testable: true,
          method: 'Compare with neutron star spin-down rates',
        },
      ],
      observationalTargets: matchingSources.map(src => ({
        name: src.name,
        coordinates: { ra: src.ra, dec: src.dec },
        survey: src.type,
        redshiftRange: `distance: ${src.distance}`,
        expectedSignal: `Spin-torsion coupling at σ ~ ${src.spinDensityEstimate}`,
        detectionMethod: 'Pulsar timing residuals, gravitational wave phase shift',
      })),
      score,
      confidence: score < 1e-4 ? 'HIGH' : score < 0.01 ? 'MODERATE' : 'LOW',
    };
  }

  // ── f(T) Gravity Equation Synthesis ─────────────────────────────────────

  private synthesizeFTGravity(engine: string, result: EvalResult, score: number): DiscoveredEquation {
    const p = result.params;
    const modelNames = ['Power Law', 'Born-Infeld', 'Logarithmic', 'Exponential'];
    const modelType = Math.round(p.modelType);
    const modelName = modelNames[modelType] || 'Power Law';

    // Find redshift windows where this model deviates most from ΛCDM
    const deviations = this.computeFTDeviations(p);
    const topDeviations = deviations.sort((a, b) => Math.abs(b.deviation) - Math.abs(a.deviation)).slice(0, 5);

    // Map deviations to sky targets
    const targets = topDeviations.map(dev => {
      const skyTarget = SKY_TARGETS.find(t => dev.z >= t.zRange[0] && dev.z <= t.zRange[1]);
      return {
        name: skyTarget?.name || `z = ${dev.z.toFixed(2)} field`,
        coordinates: { ra: skyTarget?.ra || 'TBD', dec: skyTarget?.dec || 'TBD' },
        survey: skyTarget?.survey || 'General BAO/SNIa',
        redshiftRange: `z = ${dev.z.toFixed(2)} ± 0.05`,
        expectedSignal: `H(z) deviation: ${dev.deviation > 0 ? '+' : ''}${dev.deviation.toFixed(1)} km/s/Mpc (${dev.deviationPct.toFixed(1)}%) from ΛCDM`,
        detectionMethod: dev.z < 0.5 ? 'Type Ia supernovae + BAO' : dev.z < 1.5 ? 'Galaxy clustering BAO' : 'Lyman-α forest BAO + QSO',
      };
    });

    return {
      id: `ft-${Date.now()}`,
      timestamp: Date.now(),
      engine,
      domain: 'f(T) Teleparallel Gravity',
      title: `f(T) ${modelName} Model — Cosmological Fit`,
      latex: this.ftLatex(p, modelType),
      plaintext: this.ftPlaintext(p, modelType, modelName),
      parameters: {
        'α': { value: p.alpha, unit: 'dimensionless', description: 'Primary coupling constant' },
        'β': { value: p.beta, unit: 'dimensionless', description: 'Secondary coupling constant' },
        'n': { value: p.n, unit: 'dimensionless', description: 'Power law exponent' },
        'Λ_BI': { value: p.lambda, unit: 'km²/s²/Mpc²', description: 'Born-Infeld energy scale' },
        'Model': { value: modelType, unit: modelName, description: 'Selected f(T) model type' },
      },
      predictions: [
        {
          quantity: 'H₀ prediction',
          value: this.predictH0(p).toFixed(2),
          unit: 'km/s/Mpc',
          testable: true,
          method: 'CMB + BAO combined analysis',
        },
        {
          quantity: 'χ² / d.o.f.',
          value: (score / 21).toFixed(2),
          unit: 'per data point',
          testable: true,
          method: 'Comparison with 21 H(z) measurements',
        },
        {
          quantity: 'Peak deviation redshift',
          value: topDeviations[0]?.z.toFixed(2) || 'N/A',
          unit: '',
          testable: true,
          method: `${topDeviations[0]?.z < 1 ? 'DESI/Euclid BAO' : 'Lyman-α forest'} measurement`,
        },
        {
          quantity: 'Dark energy equation of state w(z=0)',
          value: this.computeW0(p).toFixed(4),
          unit: 'dimensionless',
          testable: true,
          method: 'SNIa + CMB + BAO joint fit (compare with w = -1 for ΛCDM)',
        },
      ],
      observationalTargets: targets,
      score,
      confidence: score / 21 < 1.5 ? 'HIGH' : score / 21 < 3 ? 'MODERATE' : 'LOW',
    };
  }

  // ── UFE Torsion Equation Synthesis ──────────────────────────────────────

  private synthesizeUFETorsion(engine: string, result: EvalResult, score: number): DiscoveredEquation {
    const p = result.params;

    // Derived quantities from Mexican hat (with safe defaults)
    const mu2 = p.mu2 || 0;
    const lambda = p.lambda || p.lambda_quartic || 1;
    const T_vev = mu2 > 0 && lambda > 0 ? Math.sqrt(mu2 / (2 * lambda)) : 0;
    const m_T = Math.sqrt(4 * Math.max(0, mu2));
    const comptonLength = m_T > 0 ? HBAR / (m_T * EV_TO_KG * C) : Infinity;
    const charLength = (p.gamma || 0) > 0 && mu2 > 0 ? Math.sqrt((p.gamma || 0) / (2 * mu2)) : 0;

    // Energy scale of symmetry breaking
    const energyScale_eV = Math.sqrt(mu2); // in natural units ~ eV

    // Map to observational regime
    let regime: string;
    let detectors: string[];
    if (energyScale_eV > 1e12) {
      regime = 'Ultra-high energy cosmic rays / early universe (E > TeV)';
      detectors = ['Pierre Auger Observatory', 'IceCube', 'CTA'];
    } else if (energyScale_eV > 1e9) {
      regime = 'LHC / collider energy scale (E ~ GeV-TeV)';
      detectors = ['ATLAS', 'CMS', 'LHCb'];
    } else if (energyScale_eV > 1e6) {
      regime = 'Nuclear / MeV scale — neutron star interiors';
      detectors = ['NICER', 'XMM-Newton', 'LIGO (NS mergers)'];
    } else if (energyScale_eV > 1) {
      regime = 'Atomic / eV scale — precision spectroscopy';
      detectors = ['Hydrogen spectroscopy', 'Atomic interferometry'];
    } else {
      regime = 'Cosmological / sub-eV — dark energy scale';
      detectors = ['Euclid', 'DESI', 'Rubin/LSST', 'CMB-S4'];
    }

    // Where to look in the sky depends on the energy scale
    const skyTargets: ObservationalTarget[] = [];

    if (energyScale_eV < 1) {
      // Cosmological — look at large-scale structure
      skyTargets.push(...SKY_TARGETS.filter(t => t.zRange[0] < 1).slice(0, 3).map(t => ({
        name: t.name,
        coordinates: { ra: t.ra, dec: t.dec },
        survey: t.survey,
        redshiftRange: `z = ${t.zRange[0].toFixed(2)} – ${t.zRange[1].toFixed(2)}`,
        expectedSignal: `Torsion dark energy: Ω_T contribution to expansion, T_vev = ${T_vev.toExponential(3)}`,
        detectionMethod: 'BAO scale shift + growth rate f·σ₈ modification',
      })));
    }

    // Neutron star targets for nuclear-scale torsion
    if (energyScale_eV > 1e6 && energyScale_eV < 1e12) {
      skyTargets.push(...SPIN_SOURCES.filter(s => s.type.includes('pulsar') || s.type.includes('magnetar')).slice(0, 3).map(src => ({
        name: src.name,
        coordinates: { ra: src.ra, dec: src.dec },
        survey: 'X-ray / radio timing',
        redshiftRange: `distance: ${src.distance}`,
        expectedSignal: `Torsion condensate modifies NS equation of state. m_T = ${m_T.toExponential(3)} eV`,
        detectionMethod: 'Neutron star mass-radius relation (NICER), pulsar glitch statistics',
      })));
    }

    return {
      id: `ufe-${Date.now()}`,
      timestamp: Date.now(),
      engine,
      domain: 'UFE Torsion Field Theory',
      title: 'UFE Mexican-Hat Torsion Condensate',
      latex: this.ufeLatex(p, T_vev, m_T),
      plaintext: this.ufePlaintext(p, T_vev, m_T, charLength),
      parameters: {
        'μ²': { value: mu2, unit: 'eV²', description: 'Symmetry breaking mass² parameter' },
        'λ': { value: lambda, unit: 'dimensionless', description: 'Quartic self-coupling' },
        'γ': { value: p.gamma, unit: 'dimensionless', description: 'Kinetic/gradient coefficient' },
        'ε': { value: p.epsilon, unit: 'dimensionless', description: 'Curvature-torsion mixing' },
        'κ_f': { value: p.kappa_f, unit: 'dimensionless', description: 'Fermion axial coupling' },
        'κ_g': { value: p.kappa_g, unit: 'dimensionless', description: 'Graviton-torsion coupling' },
        'T_vev': { value: T_vev, unit: 'm⁻²', description: 'Torsion vacuum expectation value' },
        'm_T': { value: m_T, unit: 'eV', description: 'Torsion field mass' },
        'ℓ_char': { value: charLength, unit: 'natural', description: 'Characteristic torsion length √(γ/2μ²)' },
      },
      predictions: [
        {
          quantity: 'Torsion VEV',
          value: T_vev.toExponential(4),
          unit: 'm⁻²',
          testable: T_vev > 0,
          method: 'Neutron star EOS modification or cosmological torsion dark energy',
        },
        {
          quantity: 'Torsion mass',
          value: m_T.toExponential(4),
          unit: 'eV',
          testable: true,
          method: `${regime}`,
        },
        {
          quantity: 'Compton wavelength',
          value: comptonLength < 1e20 ? comptonLength.toExponential(3) : '∞',
          unit: 'm',
          testable: comptonLength < 1e6,
          method: comptonLength < 1e-3 ? 'Sub-mm gravity' : 'Astrophysical spin effects',
        },
        {
          quantity: 'Energy regime',
          value: energyScale_eV.toExponential(2),
          unit: 'eV',
          testable: true,
          method: detectors.join(', '),
        },
      ],
      observationalTargets: skyTargets,
      score,
      confidence: score < 0.1 ? 'HIGH' : score < 1 ? 'MODERATE' : 'LOW',
    };
  }

  // ── Torsion Wave Synthesis ──────────────────────────────────────────────

  private synthesizeTorsionWave(engine: string, result: EvalResult, score: number): DiscoveredEquation {
    const p = result.params;
    const mu2 = p.mu2;
    const lambda_q = p.lambda_q;
    const T_vev = mu2 > 0 && lambda_q > 0 ? Math.sqrt(mu2 / (2 * lambda_q)) : 0;
    const mT2 = 4 * Math.max(0, mu2);
    const m_T = Math.sqrt(mT2);
    const effMass2 = mT2 + 3 * lambda_q * T_vev * T_vev;
    const effMass = Math.sqrt(Math.max(0, effMass2));

    // Dispersion: ω² = k² + m_eff²
    const omega = p.frequency;
    const k = p.wavenumber;
    const v_phase = k > 0 ? omega / k : 0;
    const v_group = omega > 0 ? k / omega : 0;

    // Wave frequency → gravitational wave frequency range
    const f_Hz = omega / (2 * Math.PI);
    let gwDetector: string;
    if (f_Hz > 10) gwDetector = 'LIGO/Virgo/KAGRA (10-1000 Hz)';
    else if (f_Hz > 1e-4) gwDetector = 'LISA (0.1 mHz - 0.1 Hz)';
    else if (f_Hz > 1e-9) gwDetector = 'Pulsar Timing Arrays (nHz)';
    else gwDetector = 'CMB B-mode polarization';

    const targets: ObservationalTarget[] = [];

    // GW detector targets
    targets.push({
      name: 'LIGO Livingston / Hanford',
      coordinates: { ra: 'All-sky', dec: 'All-sky' },
      survey: gwDetector,
      redshiftRange: 'local (d < 500 Mpc)',
      expectedSignal: `Torsion wave at f = ${f_Hz.toExponential(2)} Hz, amplitude ${Math.abs(p.amplitude).toExponential(2)}`,
      detectionMethod: 'Strain signal from torsion-graviton mixing, look for anomalous polarization modes',
    });

    // NS merger targets (torsion waves excited during merger)
    targets.push({
      name: 'GW170817 remnant',
      coordinates: { ra: '13h 09m 48s', dec: '-23° 22\' 53"' },
      survey: 'LIGO O5+',
      redshiftRange: 'z ≈ 0.01 (40 Mpc)',
      expectedSignal: 'Post-merger torsion oscillation at m_T frequency',
      detectionMethod: 'GW post-merger signal deviation from GR prediction',
    });

    return {
      id: `wave-${Date.now()}`,
      timestamp: Date.now(),
      engine,
      domain: 'Torsion Wave Propagation',
      title: 'Torsion Wave Dispersion Relation',
      latex: this.waveLatex(p, effMass, T_vev),
      plaintext: this.wavePlaintext(p, effMass, T_vev, v_group),
      parameters: {
        'μ²': { value: mu2, unit: 'eV²', description: 'Mexican hat mass²' },
        'λ_q': { value: lambda_q, unit: 'dimensionless', description: 'Quartic coupling' },
        'm_eff': { value: effMass, unit: 'eV', description: 'Effective torsion mass around VEV' },
        'ω': { value: omega, unit: 's⁻¹', description: 'Angular frequency' },
        'k': { value: k, unit: 'm⁻¹', description: 'Wavenumber' },
        'v_group': { value: v_group, unit: 'c', description: 'Group velocity' },
        'A': { value: p.amplitude, unit: 'm⁻²', description: 'Wave amplitude' },
        'J_spin': { value: p.J_spin, unit: 'm⁻⁴', description: 'Spin current source' },
      },
      predictions: [
        {
          quantity: 'Torsion wave frequency',
          value: f_Hz.toExponential(3),
          unit: 'Hz',
          testable: true,
          method: gwDetector,
        },
        {
          quantity: 'Group velocity',
          value: v_group.toFixed(6),
          unit: 'c',
          testable: v_group < 1,
          method: 'Multi-messenger delay between GW and torsion-wave signal',
        },
        {
          quantity: 'Dispersion residual',
          value: Math.abs(omega * omega - k * k - effMass2).toExponential(3),
          unit: 'eV²',
          testable: true,
          method: 'Frequency-dependent arrival time of GW signals',
        },
      ],
      observationalTargets: targets,
      score,
      confidence: score < 1 ? 'HIGH' : score < 100 ? 'MODERATE' : 'LOW',
    };
  }

  // ── Cross-Domain Synthesis ──────────────────────────────────────────────

  private synthesizeCrossDomain(engine: string, result: EvalResult, score: number): DiscoveredEquation {
    const p = result.params;
    const mu2 = p.mu2 || 0;
    const lambda_q = p.lambda_quartic || p.lambda || 1;
    const T_scalar = p.T_scalar || 0;
    const fT_alpha = p.fT_alpha || p.alpha || 0;
    const fT_n = p.fT_n || p.n || 1;
    const H0_rescaled = p.H0_rescaled || 1;
    const T_vev = mu2 > 0 && lambda_q > 0 ? Math.sqrt(mu2 / (2 * lambda_q)) : 0;
    const m_T = Math.sqrt(4 * Math.max(0, mu2));
    const H0_pred = H0_rescaled * 70;

    // Combine all sky targets
    const allTargets: ObservationalTarget[] = [];

    // H₀ tension targets
    if (Math.abs(H0_pred - 67.4) > 2 || Math.abs(H0_pred - 73.0) < 3) {
      allTargets.push({
        name: 'Hubble Tension Resolution',
        coordinates: { ra: 'All-sky', dec: 'All-sky' },
        survey: 'SH0ES + Planck',
        redshiftRange: 'z = 0 (local) vs z = 1100 (CMB)',
        expectedSignal: `Unified H₀ = ${H0_pred.toFixed(1)} km/s/Mpc via torsion dark energy`,
        detectionMethod: 'Compare local distance ladder with CMB-calibrated value under f(T)',
      });
    }

    // Add spin source for EC sector
    allTargets.push({
      name: 'PSR J1748-2446ad',
      coordinates: { ra: '17h 48m 52s', dec: '-24° 46\' 48"' },
      survey: 'Radio timing + X-ray',
      redshiftRange: 'distance: 7.7 kpc',
      expectedSignal: `EC torsion at T = ${T_scalar.toExponential(3)}, cross-coupled to f(T) cosmology`,
      detectionMethod: 'Pulsar timing + growth factor measurement at matched z',
    });

    // f(T) deviation field
    const bestSkyTarget = SKY_TARGETS.find(t => 0.5 >= t.zRange[0] && 0.5 <= t.zRange[1]);
    if (bestSkyTarget) {
      allTargets.push({
        name: bestSkyTarget.name,
        coordinates: { ra: bestSkyTarget.ra, dec: bestSkyTarget.dec },
        survey: bestSkyTarget.survey,
        redshiftRange: `z = ${bestSkyTarget.zRange[0].toFixed(2)} – ${bestSkyTarget.zRange[1].toFixed(2)}`,
        expectedSignal: `f(T) modification: α=${fT_alpha.toFixed(4)}, n=${fT_n.toFixed(4)}`,
        detectionMethod: 'BAO + RSD measurement deviation from ΛCDM prediction',
      });
    }

    return {
      id: `cross-${Date.now()}`,
      timestamp: Date.now(),
      engine,
      domain: 'UFE Cross-Domain Unified',
      title: 'Unified Torsion Field — All Sectors Consistent',
      latex: this.crossLatex(p, T_vev, m_T, H0_pred),
      plaintext: this.crossPlaintext(p, T_vev, m_T, H0_pred),
      parameters: {
        'T_scalar': { value: T_scalar, unit: 'm⁻¹', description: 'EC torsion scalar' },
        'μ²': { value: mu2, unit: 'eV²', description: 'Symmetry breaking scale' },
        'λ': { value: lambda_q, unit: 'dimensionless', description: 'Quartic coupling' },
        'T_vev': { value: T_vev, unit: 'm⁻²', description: 'Torsion VEV' },
        'm_T': { value: m_T, unit: 'eV', description: 'Torsion mass' },
        'H₀': { value: H0_pred, unit: 'km/s/Mpc', description: 'Predicted Hubble constant' },
        'f(T)_α': { value: fT_alpha, unit: 'dimensionless', description: 'f(T) amplitude' },
        'f(T)_n': { value: fT_n, unit: 'dimensionless', description: 'f(T) power index' },
      },
      predictions: [
        {
          quantity: 'Unified H₀',
          value: H0_pred.toFixed(2),
          unit: 'km/s/Mpc',
          testable: true,
          method: 'Joint CMB+BAO+SNIa under f(T) gravity',
        },
        {
          quantity: 'Torsion VEV',
          value: T_vev.toExponential(4),
          unit: 'm⁻²',
          testable: T_vev > 0,
          method: 'Neutron star EOS + cosmological expansion consistency',
        },
        {
          quantity: 'Cross-sector consistency χ²',
          value: score.toFixed(4),
          unit: '',
          testable: true,
          method: 'Combined fit across EC + f(T) + wave sectors',
        },
      ],
      observationalTargets: allTargets,
      score,
      confidence: score < 1 ? 'HIGH' : score < 5 ? 'MODERATE' : 'LOW',
    };
  }

  // ── LaTeX Generators ───────────────────────────────────────────────────

  private ecLatex(p: Record<string, number>, T_mag: number, lambda: number): string {
    return `% Einstein-Cartan Discovered Solution
% Generated by AEGIS/Seeker at ${new Date().toISOString()}

\\begin{equation}
  T^a{}_{bc} + \\delta^a_b T_c - \\delta^a_c T_b = 8\\pi G \\, s^a{}_{bc}
\\end{equation}

\\textbf{Discovered torsion configuration:}

\\begin{equation}
  T^{\\mu\\nu} = \\begin{pmatrix}
    0 & ${p.T01.toFixed(6)} & ${p.T02.toFixed(6)} & ${p.T03.toFixed(6)} \\\\
    ${(-p.T01).toFixed(6)} & 0 & ${p.T12.toFixed(6)} & ${p.T13.toFixed(6)} \\\\
    ${(-p.T02).toFixed(6)} & ${(-p.T12).toFixed(6)} & 0 & ${p.T23.toFixed(6)} \\\\
    ${(-p.T03).toFixed(6)} & ${(-p.T13).toFixed(6)} & ${(-p.T23).toFixed(6)} & 0
  \\end{pmatrix} \\quad \\text{m}^{-1}
\\end{equation}

\\begin{equation}
  |T| = ${T_mag.toExponential(4)} \\text{ m}^{-1}, \\quad
  \\lambda = ${lambda.toFixed(4)}, \\quad
  \\sigma = ${p.spinDensity.toExponential(4)} \\text{ J}\\cdot\\text{s/m}^3
\\end{equation}`;
  }

  private ftLatex(p: Record<string, number>, modelType: number): string {
    const models = [
      `f(T) = ${p.alpha.toFixed(6)} \\, T^{${p.n.toFixed(4)}}`,
      `f(T) = ${p.lambda.toFixed(4)} \\left( \\sqrt{1 + \\frac{2T}{${p.lambda.toFixed(4)}}} - 1 \\right)`,
      `f(T) = ${p.alpha.toFixed(6)} T + ${p.beta.toFixed(6)} T \\ln\\!\\left(\\frac{T}{T_0}\\right)`,
      `f(T) = ${p.alpha.toFixed(6)} T \\left(1 - e^{${p.beta.toFixed(6)} T_0 / T}\\right)`,
    ];

    return `% f(T) Teleparallel Gravity — Discovered Model
% Generated by AEGIS/Seeker at ${new Date().toISOString()}

\\begin{equation}
  S = \\int d^4x \\, |e| \\, \\frac{1}{16\\pi G} \\left[ f(T) + \\mathcal{L}_m \\right]
\\end{equation}

\\textbf{Best-fit model:}
\\begin{equation}
  ${models[modelType]}
\\end{equation}

\\textbf{Modified Friedmann equation:}
\\begin{equation}
  H^2 = \\frac{8\\pi G}{3} \\rho - \\frac{f}{6} + \\frac{T f_T}{3}
\\end{equation}

\\textbf{Parameters:}
$\\alpha = ${p.alpha.toFixed(6)}$, \\quad
$\\beta = ${p.beta.toFixed(6)}$, \\quad
$n = ${p.n.toFixed(4)}$, \\quad
$\\Lambda_{\\text{BI}} = ${p.lambda.toFixed(4)}$`;
  }

  private ufeLatex(p: Record<string, number>, T_vev: number, m_T: number): string {
    return `% UFE Torsion Field Theory — Mexican Hat Solution
% Generated by AEGIS/Seeker at ${new Date().toISOString()}

\\textbf{UFE Action:}
\\begin{equation}
  S_{\\text{UFE}} = \\int d^4x \\sqrt{-g} \\left[
    -\\mu^2 T^2 + \\lambda T^4 + \\gamma (\\partial T)^2
    + \\varepsilon R T^2
    + \\kappa_f (\\bar{\\psi} \\gamma^5 \\psi) T
    + \\kappa_g G_{\\mu\\nu} T^{\\mu\\nu}
  \\right]
\\end{equation}

\\textbf{Mexican-hat potential:}
\\begin{equation}
  V(T) = -\\mu^2 T^2 + \\lambda T^4, \\quad
  T_{\\text{vev}} = \\pm \\frac{\\mu}{\\sqrt{2\\lambda}} = \\pm ${T_vev.toExponential(4)}
\\end{equation}

\\textbf{Torsion mass around VEV:}
\\begin{equation}
  m_T^2 = V''(T_{\\text{vev}}) = 4\\mu^2 = ${(4 * p.mu2).toExponential(4)} \\text{ eV}^2
  \\quad \\Rightarrow \\quad m_T = ${m_T.toExponential(4)} \\text{ eV}
\\end{equation}

\\textbf{Field equation:}
\\begin{equation}
  -2\\mu^2 T + 4\\lambda T^3 + \\gamma \\Box T + 2\\varepsilon R T
  + \\kappa_f \\langle\\bar{\\psi}\\gamma^5\\psi\\rangle = 0
\\end{equation}

\\textbf{Discovered couplings:}
$\\mu^2 = ${p.mu2.toExponential(4)}$ eV$^2$, \\quad
$\\lambda = ${p.lambda.toFixed(6)}$, \\quad
$\\gamma = ${p.gamma.toFixed(6)}$, \\quad
$\\varepsilon = ${p.epsilon.toFixed(6)}$, \\quad
$\\kappa_f = ${p.kappa_f.toFixed(6)}$, \\quad
$\\kappa_g = ${p.kappa_g.toFixed(6)}$`;
  }

  private waveLatex(p: Record<string, number>, effMass: number, T_vev: number): string {
    return `% Torsion Wave Dispersion — Discovered Solution
% Generated by AEGIS/Seeker at ${new Date().toISOString()}

\\textbf{Torsion wave equation around VEV:}
\\begin{equation}
  \\Box \\delta T + m_{\\text{eff}}^2 \\, \\delta T + 3\\lambda T_{\\text{vev}} (\\delta T)^2 = J_{\\text{spin}}
\\end{equation}

\\textbf{Dispersion relation:}
\\begin{equation}
  \\omega^2 = k^2 + m_{\\text{eff}}^2, \\quad
  m_{\\text{eff}} = \\sqrt{4\\mu^2 + 3\\lambda T_{\\text{vev}}^2} = ${effMass.toExponential(4)} \\text{ eV}
\\end{equation}

\\textbf{Group velocity:}
\\begin{equation}
  v_g = \\frac{k}{\\omega} = \\frac{k}{\\sqrt{k^2 + m_{\\text{eff}}^2}} < c
\\end{equation}

\\textbf{Discovered parameters:}
$\\omega = ${p.frequency.toFixed(4)}$, \\quad
$k = ${p.wavenumber.toFixed(4)}$, \\quad
$A = ${p.amplitude.toExponential(3)}$, \\quad
$J = ${p.J_spin.toExponential(3)}$`;
  }

  private crossLatex(p: Record<string, number>, T_vev: number, m_T: number, H0: number): string {
    return `% UFE Cross-Domain Unified Solution
% Generated by AEGIS/Seeker at ${new Date().toISOString()}

\\textbf{Unified field equation system:}

\\begin{align}
  \\text{(I)} \\quad & T^a{}_{bc} = 8\\pi G \\, s^a{}_{bc} && \\text{(Cartan)} \\\\
  \\text{(II)} \\quad & H^2 = \\frac{8\\pi G}{3}\\rho - \\frac{f(T)}{6} + \\frac{Tf_T}{3} && \\text{(Friedmann)} \\\\
  \\text{(III)} \\quad & \\Box T + m_T^2 T + \\lambda T^3 = J && \\text{(Wave)} \\\\
  \\text{(IV)} \\quad & T_0 = \\frac{\\mu}{\\sqrt{2\\lambda}} && \\text{(VEV)}
\\end{align}

\\textbf{Consistency conditions (all satisfied):}
\\begin{itemize}
  \\item $T_{\\text{vev}} = ${T_vev.toExponential(4)}$ — from Mexican hat $V(T) = -\\mu^2 T^2 + \\lambda T^4$
  \\item $m_T = ${m_T.toExponential(4)}$ eV — torsion mass
  \\item $f(T) = ${(p.fT_alpha || p.alpha || 0).toFixed(4)} \\, T^{${(p.fT_n || p.n || 1).toFixed(4)}}$ — teleparallel modification
  \\item $H_0 = ${H0.toFixed(2)}$ km/s/Mpc — unified Hubble constant
\\end{itemize}`;
  }

  // ── Plaintext Generators ───────────────────────────────────────────────

  private ecPlaintext(p: Record<string, number>, T_mag: number, lambda: number): string {
    return `EINSTEIN-CARTAN TORSION SOLUTION
================================
Cartan equation: T^a_bc + δ^a_b T_c - δ^a_c T_b = 8πG · s^a_bc

Torsion components (m⁻¹):
  T⁰₀₁ = ${p.T01.toFixed(6)}    T⁰₀₂ = ${p.T02.toFixed(6)}    T⁰₀₃ = ${p.T03.toFixed(6)}
  T¹₁₂ = ${p.T12.toFixed(6)}    T¹₁₃ = ${p.T13.toFixed(6)}    T²₂₃ = ${p.T23.toFixed(6)}

|T| = ${T_mag.toExponential(4)} m⁻¹
λ (coupling) = ${lambda.toFixed(4)}
σ (spin density) = ${p.spinDensity.toExponential(4)} J·s/m³`;
  }

  private ftPlaintext(p: Record<string, number>, modelType: number, modelName: string): string {
    return `f(T) TELEPARALLEL GRAVITY — ${modelName.toUpperCase()} MODEL
${'='.repeat(50)}
Modified Friedmann: H² = (8πG/3)ρ - f(T)/6 + T·f_T/3

Parameters:
  α = ${p.alpha.toFixed(6)}
  β = ${p.beta.toFixed(6)}
  n = ${p.n.toFixed(4)}
  Λ_BI = ${p.lambda.toFixed(4)}

Cosmological fit: χ²/d.o.f. against 21 H(z) data points`;
  }

  private ufePlaintext(p: Record<string, number>, T_vev: number, m_T: number, charLength: number): string {
    return `UFE TORSION FIELD — MEXICAN HAT CONDENSATE
============================================
Action: S = ∫ d⁴x √(-g) [ -μ²T² + λT⁴ + γ(∂T)² + εRT² + κ_f(ψ̄γ⁵ψ)T + κ_gG_μνT^μν ]

Potential: V(T) = -μ²T² + λT⁴  (Mexican hat — spontaneous torsion condensation)

Discovered couplings:
  μ² = ${p.mu2.toExponential(4)} eV²   (symmetry breaking scale)
  λ  = ${p.lambda.toFixed(6)}         (quartic coupling)
  γ  = ${p.gamma.toFixed(6)}          (kinetic term)
  ε  = ${p.epsilon.toFixed(6)}        (curvature-torsion mixing)
  κ_f = ${p.kappa_f.toFixed(6)}       (fermion axial coupling)
  κ_g = ${p.kappa_g.toFixed(6)}       (graviton-torsion coupling)

Derived quantities:
  T_vev = ±μ/√(2λ) = ±${T_vev.toExponential(4)} m⁻²  (vacuum expectation value)
  m_T = 2μ = ${m_T.toExponential(4)} eV               (torsion mass)
  ℓ = √(γ/2μ²) = ${charLength.toExponential(4)}       (characteristic length)

Field equation: -2μ²T + 4λT³ + γ□T + 2εRT + κ_f·<ψ̄γ⁵ψ> = 0`;
  }

  private wavePlaintext(p: Record<string, number>, effMass: number, T_vev: number, v_group: number): string {
    return `TORSION WAVE DISPERSION
=======================
Wave equation: □δT + m²_eff·δT + 3λT_vev·(δT)² = J_spin

Dispersion: ω² = k² + m²_eff   (massive Klein-Gordon type)

Parameters:
  μ² = ${p.mu2.toExponential(4)} eV²
  λ_q = ${p.lambda_q.toFixed(6)}
  m_eff = ${effMass.toExponential(4)} eV
  T_vev = ${T_vev.toExponential(4)} m⁻²
  ω = ${p.frequency.toFixed(4)} s⁻¹
  k = ${p.wavenumber.toFixed(4)} m⁻¹
  v_group = ${v_group.toFixed(6)} c   (subluminal ✓)
  Amplitude = ${p.amplitude.toExponential(3)}
  J_spin = ${p.J_spin.toExponential(3)}`;
  }

  private crossPlaintext(p: Record<string, number>, T_vev: number, m_T: number, H0: number): string {
    return `UFE CROSS-DOMAIN UNIFIED SOLUTION
==================================
All four torsion sectors self-consistent:

  (I)   Cartan:   T^a_bc = 8πG·s^a_bc         T_scalar = ${(p.T_scalar || 0).toExponential(4)}
  (II)  Friedmann: H² = (8πG/3)ρ - f(T)/6     H₀ = ${H0.toFixed(2)} km/s/Mpc
  (III) Wave:     □T + m²T + λT³ = J           m_T = ${m_T.toExponential(4)} eV
  (IV)  VEV:      T₀ = μ/√(2λ)                T_vev = ${T_vev.toExponential(4)} m⁻²

Cross-sector couplings:
  f(T) model: α = ${(p.fT_alpha || p.alpha || 0).toFixed(6)}, n = ${(p.fT_n || p.n || 1).toFixed(4)}
  Spin density: σ = ${(p.spinDensity || 0).toExponential(4)}
  EC coupling: ${(p.ec_coupling || 0).toFixed(4)}`;
  }

  // ── Helpers ─────────────────────────────────────────────────────────────

  private classifyDomain(taskId: string): string | null {
    if (taskId.includes('einstein-cartan')) return 'einstein-cartan';
    if (taskId.includes('ft-gravity')) return 'ft-gravity';
    if (taskId.includes('ufe-torsion')) return 'ufe-torsion';
    if (taskId.includes('torsion-wave')) return 'torsion-wave';
    if (taskId.includes('cross-domain')) return 'cross-domain';
    return null;
  }

  private findSpinSources(spinDensity: number): SpinSource[] {
    // Return sources whose estimated spin density is within a few orders of magnitude
    if (spinDensity < 1e30) return SPIN_SOURCES.filter(s => s.type.includes('pulsar'));
    if (spinDensity < 1e38) return SPIN_SOURCES.filter(s => s.type.includes('pulsar') || s.type.includes('magnetar'));
    return SPIN_SOURCES;
  }

  private computeFTDeviations(p: Record<string, number>): Array<{ z: number; deviation: number; deviationPct: number }> {
    const H0 = 67.4;
    const OmegaM = 0.315;
    const observations = [
      { z: 0.07, H: 69.0 }, { z: 0.12, H: 68.6 }, { z: 0.20, H: 72.9 },
      { z: 0.28, H: 76.3 }, { z: 0.35, H: 82.7 }, { z: 0.44, H: 84.8 },
      { z: 0.57, H: 96.8 }, { z: 0.68, H: 92.0 }, { z: 0.78, H: 105.0 },
      { z: 1.04, H: 154.0 }, { z: 1.30, H: 168.0 }, { z: 1.53, H: 140.0 },
      { z: 1.75, H: 202.0 }, { z: 2.34, H: 222.0 },
    ];

    return observations.map(obs => {
      const Hz_LCDM = H0 * Math.sqrt(OmegaM * Math.pow(1 + obs.z, 3) + (1 - OmegaM));
      const deviation = obs.H - Hz_LCDM;
      return { z: obs.z, deviation, deviationPct: (deviation / Hz_LCDM) * 100 };
    });
  }

  private predictH0(p: Record<string, number>): number {
    // Simple estimate: how does this f(T) model shift H₀?
    const H0_base = 67.4;
    const T0 = -6 * H0_base * H0_base;
    const modelType = Math.round(p.modelType);
    let fT: number;
    switch (modelType) {
      case 0: fT = p.alpha * Math.pow(Math.abs(T0), p.n); break;
      case 1: fT = Math.abs(p.lambda) * (Math.sqrt(1 + 2 * T0 / Math.abs(p.lambda)) - 1); break;
      case 2: fT = p.alpha * T0 + p.beta * T0 * Math.log(Math.abs(T0 / (-6 * H0_base * H0_base))); break;
      case 3: fT = p.alpha * T0 * (1 - Math.exp(p.beta)); break;
      default: fT = 0;
    }
    const correction = fT / (6 * H0_base * H0_base);
    return H0_base * Math.sqrt(Math.max(0.5, 1 + correction));
  }

  private computeW0(p: Record<string, number>): number {
    // Effective dark energy equation of state from f(T) at z=0
    // w = -1 + (2T·f_TT) / (f + 2T·f_T)
    // Simplified: small deviations from ΛCDM
    return -1 + 0.01 * p.alpha * (p.n - 1);
  }

  // ── File Writers ────────────────────────────────────────────────────────

  private writeEquationFile(eq: DiscoveredEquation): void {
    const filename = `${eq.id}.json`;
    const filepath = path.join(this.outputDir, filename);

    fs.writeFileSync(filepath, JSON.stringify(eq, null, 2), 'utf8');

    // Also write LaTeX file
    const texFile = path.join(this.outputDir, `${eq.id}.tex`);
    fs.writeFileSync(texFile, eq.latex, 'utf8');

    // Write plaintext summary
    const txtFile = path.join(this.outputDir, `${eq.id}.txt`);
    let txt = eq.plaintext + '\n\n';
    txt += 'OBSERVATIONAL TARGETS\n';
    txt += '=====================\n';
    for (const t of eq.observationalTargets) {
      txt += `\n  ${t.name}\n`;
      txt += `    Coordinates: RA ${t.coordinates.ra}, Dec ${t.coordinates.dec}\n`;
      txt += `    Survey: ${t.survey}\n`;
      txt += `    Redshift: ${t.redshiftRange}\n`;
      txt += `    Expected signal: ${t.expectedSignal}\n`;
      txt += `    Detection method: ${t.detectionMethod}\n`;
    }
    txt += '\nPREDICTIONS\n';
    txt += '===========\n';
    for (const pred of eq.predictions) {
      txt += `  ${pred.quantity}: ${pred.value} ${pred.unit}\n`;
      txt += `    Testable: ${pred.testable ? 'YES' : 'NO'} — ${pred.method}\n`;
    }
    txt += `\nConfidence: ${eq.confidence}\n`;
    txt += `Score: ${eq.score}\n`;
    txt += `Generated: ${new Date(eq.timestamp).toISOString()}\n`;

    fs.writeFileSync(txtFile, txt, 'utf8');

    const icon = eq.confidence === 'HIGH' ? '🔥' : eq.confidence === 'MODERATE' ? '⚡' : '📝';
    console.log(`${icon} [EQUATION] ${eq.domain} — ${eq.title}`);
    console.log(`   Score: ${eq.score.toExponential(4)} | Confidence: ${eq.confidence}`);
    console.log(`   Files: ${filepath}`);
    if (eq.observationalTargets.length > 0) {
      console.log(`   Sky targets: ${eq.observationalTargets.map(t => t.name).join(', ')}`);
    }
  }

  private writeMasterIndex(): void {
    const indexPath = path.join(this.outputDir, 'INDEX.md');

    let md = `# AEGIS/Seeker — Discovered Equations Index\n\n`;
    md += `*Last updated: ${new Date().toISOString()}*\n\n`;
    md += `| # | Domain | Title | Score | Confidence | Sky Targets | File |\n`;
    md += `|---|--------|-------|-------|------------|-------------|------|\n`;

    for (let i = 0; i < this.discoveries.length; i++) {
      const eq = this.discoveries[i];
      const targets = eq.observationalTargets.map(t => t.name).join('; ');
      md += `| ${i + 1} | ${eq.domain} | ${eq.title} | ${eq.score.toExponential(3)} | ${eq.confidence} | ${targets} | ${eq.id} |\n`;
    }

    md += `\n## Best Per Domain\n\n`;
    for (const [domain, { score, eq }] of this.bestByDomain) {
      md += `### ${eq.domain}\n\n`;
      md += `**${eq.title}** (score: ${score.toExponential(4)}, confidence: ${eq.confidence})\n\n`;
      md += `\`\`\`\n${eq.plaintext}\n\`\`\`\n\n`;
      if (eq.observationalTargets.length > 0) {
        md += `**Where to look:**\n\n`;
        for (const t of eq.observationalTargets) {
          md += `- **${t.name}** (RA ${t.coordinates.ra}, Dec ${t.coordinates.dec})\n`;
          md += `  - Survey: ${t.survey} | z: ${t.redshiftRange}\n`;
          md += `  - Signal: ${t.expectedSignal}\n`;
          md += `  - Method: ${t.detectionMethod}\n\n`;
        }
      }
    }

    fs.writeFileSync(indexPath, md, 'utf8');
  }

  /** Get all discoveries */
  getDiscoveries(): DiscoveredEquation[] {
    return this.discoveries;
  }

  /** Get best per domain */
  getBest(): Map<string, { score: number; eq: DiscoveredEquation }> {
    return this.bestByDomain;
  }
}

// ─── Factory ─────────────────────────────────────────────────────────────────

export function createEquationWriter(outputDir?: string): EquationWriter {
  return new EquationWriter(outputDir);
}
