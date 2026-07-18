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
import { EvalResult } from './interfaces';
interface DiscoveredEquation {
    id: string;
    timestamp: number;
    engine: string;
    domain: string;
    title: string;
    latex: string;
    plaintext: string;
    parameters: Record<string, {
        value: number;
        unit: string;
        description: string;
    }>;
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
    coordinates: {
        ra: string;
        dec: string;
    };
    survey: string;
    redshiftRange: string;
    expectedSignal: string;
    detectionMethod: string;
}
export declare class EquationWriter {
    private outputDir;
    private discoveries;
    private bestByDomain;
    constructor(outputDir?: string);
    writeDiscovery(engine: string, taskId: string, result: EvalResult, score: number): DiscoveredEquation | null;
    private synthesizeEinsteinCartan;
    private synthesizeFTGravity;
    private synthesizeUFETorsion;
    private synthesizeTorsionWave;
    private synthesizeCrossDomain;
    private ecLatex;
    private ftLatex;
    private ufeLatex;
    private waveLatex;
    private crossLatex;
    private ecPlaintext;
    private ftPlaintext;
    private ufePlaintext;
    private wavePlaintext;
    private crossPlaintext;
    private classifyDomain;
    private findSpinSources;
    private computeFTDeviations;
    private predictH0;
    private computeW0;
    private writeEquationFile;
    private writeMasterIndex;
    /** Get all discoveries */
    getDiscoveries(): DiscoveredEquation[];
    /** Get best per domain */
    getBest(): Map<string, {
        score: number;
        eq: DiscoveredEquation;
    }>;
}
export declare function createEquationWriter(outputDir?: string): EquationWriter;
export {};
//# sourceMappingURL=equation-writer.d.ts.map