/**
 * AEGIS — UFE Tracker & Anomaly Detector
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Tracks Useful Function Evaluations, convergence curves, anomalies,
 * and discovery events. The recording backbone of every AEGIS run.
 */
import { UFEMetrics, EvalResult, Discovery, ParameterDef } from './interfaces';
export declare class UFETracker {
    private params;
    private bestSoFar;
    private usefulCount;
    private totalCount;
    private curve;
    private initialScore;
    private totalImprovement;
    private noveltyGrid;
    private readonly resolution;
    private readonly minimize;
    constructor(params: ParameterDef[], minimize?: boolean, resolution?: number);
    /** Record an evaluation and determine if it was useful */
    record(result: EvalResult): {
        useful: boolean;
        novelRegion: boolean;
        improved: boolean;
    };
    /** Compute full UFE metrics snapshot */
    getMetrics(optimum?: number): UFEMetrics;
    private computeAUCC;
    private computeTimeToTarget;
    private toBinKey;
    get regionsExplored(): number;
    get totalRegions(): number;
    get coverageRatio(): number;
}
export declare class AnomalyDetector {
    private scores;
    private windowSize;
    constructor(windowSize?: number);
    /** Check if a score is anomalous (>3σ from rolling mean) */
    check(score: number): Discovery | null;
    /** Detect plateau (variance collapsed) */
    checkPlateau(): Discovery | null;
    /** Detect landscape shift (distribution of scores changed) */
    checkShift(): Discovery | null;
    private variance;
}
//# sourceMappingURL=ufe.d.ts.map