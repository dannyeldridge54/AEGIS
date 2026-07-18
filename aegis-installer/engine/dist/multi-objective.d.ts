/**
 * AEGIS — Multi-Objective Optimizer (Pareto Front)
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Supports multiple competing objectives simultaneously.
 * Returns the full Pareto frontier — the set of non-dominated solutions.
 */
import { ParameterDef } from './interfaces';
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
}
/**
 * Multi-objective optimization using NSGA-II inspired approach.
 * Returns the Pareto frontier of non-dominated solutions.
 */
export declare function multiOptimize(objectives: MultiObjective[], parameters: ParameterDef[], options?: {
    maxEvals?: number;
    populationSize?: number;
    verbosity?: 'silent' | 'minimal' | 'normal';
}): Promise<ParetoFront>;
//# sourceMappingURL=multi-objective.d.ts.map