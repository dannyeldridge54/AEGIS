/**
 * Seeker — UFE Tracker
 * Tracks Useful Function Evaluations, convergence curves, anomalies,
 * and discovery events. The recording backbone of every Seeker run.
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
    /** Area Under Convergence Curve — normalized to [0,1] budget range */
    private computeAUCC;
    /** Time-to-target: evals needed to close 10/50/90% of initial gap */
    private computeTimeToTarget;
    private toBinKey;
    /** How many unique regions have been explored */
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