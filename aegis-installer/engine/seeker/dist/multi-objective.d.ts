/**
 * Seeker — Multi-Objective Optimizer (Pareto Front)
 * NSGA-II inspired. UFE-tracked. Seeded RNG.
 * Returns the full Pareto frontier of non-dominated solutions.
 */
import { ParameterDef, UFEMetrics } from './interfaces';
export interface MultiObjective {
    name: string;
    evaluate: (params: Record<string, number>) => number | Promise<number>;
    minimize?: boolean;
    weight?: number;
}
export interface ParetoResult {
    params: Record<string, number>;
    scores: Record<string, number>;
    dominated: boolean;
    crowdingDistance: number;
}
export interface ParetoFront {
    solutions: ParetoResult[];
    totalEvals: number;
    runtime: number;
    ufe: UFEMetrics;
}
/**
 * Multi-objective optimization using NSGA-II inspired approach.
 * Returns Pareto frontier with UFE metrics.
 */
export declare function multiOptimize(objectives: MultiObjective[], parameters: ParameterDef[], options?: {
    maxEvals?: number;
    populationSize?: number;
    verbosity?: 'silent' | 'minimal' | 'normal';
    seed?: number;
}): Promise<ParetoFront>;
//# sourceMappingURL=multi-objective.d.ts.map