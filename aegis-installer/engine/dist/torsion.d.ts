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
import { Task } from './interfaces';
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
export declare function computeTorsionScalar(components: number[]): number;
export declare function computeTraceVector(components: number[], dim?: number): number[];
export declare function computeAxialTorsion(components: number[]): number;
/**
 * Einstein-Cartan field equation cost:
 * Minimizing this finds torsion configurations that satisfy
 * the Cartan equation: T^a_{bc} + δ^a_b T_c - δ^a_c T_b = 8πG s^a_{bc}
 *
 * Where s^a_{bc} is the spin angular momentum tensor.
 */
export declare function einsteinCartanResidual(params: Record<string, number>): number;
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
export declare function fTGravity_PowerLaw(T: number, alpha: number, n: number): number;
export declare function fTGravity_BornInfeld(T: number, lambda: number): number;
export declare function fTGravity_Logarithmic(T: number, alpha: number, beta: number, T0: number): number;
export declare function fTGravity_Exponential(T: number, alpha: number, beta: number, T0: number): number;
export interface HzObservation {
    z: number;
    H: number;
    sigma: number;
    method: string;
    survey: string;
    reference: string;
    ra: string;
    dec: string;
    skyArea_deg2: number;
    comovingDist_Mpc: number;
    lookbackTime_Gyr: number;
    fieldDescription: string;
}
export declare const HZ_OBSERVATIONS: HzObservation[];
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
export declare function computeSpatialAnomalies(params: Record<string, number>): SpatialAnomaly[];
/**
 * f(T) model fitness against cosmological expansion data.
 * The Friedmann equation in f(T) gravity:
 *   H² = (8πG/3)ρ - f/6 + Tf_T/3
 *
 * Where f_T = df/dT and T = -6H² in FLRW metric.
 */
export declare function fTCosmologyResidual(params: Record<string, number>): number;
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
export declare function ufeTorsionFunctional(params: Record<string, number>): number;
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
export declare function crossDomainUFE(params: Record<string, number>): number;
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
export declare function torsionWaveResidual(params: Record<string, number>): number;
/** Einstein-Cartan torsion optimization task */
export declare const einsteinCartanTask: Task;
/** f(T) teleparallel gravity cosmology task */
export declare const fTGravityTask: Task;
/** UFE torsion field theory task — v3 with hard non-trivial barriers */
export declare const ufeTorsionTask: Task;
/** Torsion wave propagation task — v2 with dispersion relation */
export declare const torsionWaveTask: Task;
/** Cross-domain unified torsion task — v3 with non-trivial barriers */
export declare const crossDomainTask: Task;
/** All torsion tasks bundled */
export declare const torsionTasks: {
    einsteinCartan: Task;
    fTGravity: Task;
    ufeTorsion: Task;
    torsionWave: Task;
    crossDomain: Task;
};
//# sourceMappingURL=torsion.d.ts.map