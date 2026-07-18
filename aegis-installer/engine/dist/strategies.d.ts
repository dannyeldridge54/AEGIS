/**
 * AEGIS — Strategy Engine
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Implements all optimization strategies + meta-learner that picks
 * the best strategy adaptively based on past performance.
 * Now with seeded RNG, real gradient estimation, quadratic surrogate,
 * and eval-count-based annealing.
 */
import { ParameterDef, EvalResult, Strategy, StrategyType, Constraint } from './interfaces';
import { SeededRNG } from './rng';
export declare function gridSample(params: ParameterDef[], resolution: number, index: number): Record<string, number>;
export declare function mutateParams(base: Record<string, number>, params: ParameterDef[], magnitude?: number, rng?: SeededRNG): Record<string, number>;
export declare function crossover(a: Record<string, number>, b: Record<string, number>, params: ParameterDef[], rng?: SeededRNG): Record<string, number>;
/** Real finite-difference gradient estimation from recent history */
export declare function gradientStep(best: EvalResult, params: ParameterDef[], history: EvalResult[], rng: SeededRNG): Record<string, number>;
/** Quadratic surrogate model for bayesian strategy */
export declare function surrogateStep(best: EvalResult, params: ParameterDef[], history: EvalResult[], rng: SeededRNG): Record<string, number>;
export declare function annealingSample(best: Record<string, number>, params: ParameterDef[], temperature: number, rng?: SeededRNG): Record<string, number>;
export declare function swarmUpdate(position: Record<string, number>, velocity: Record<string, number>, personalBest: Record<string, number>, globalBest: Record<string, number>, params: ParameterDef[], rng?: SeededRNG, inertia?: number, cognitive?: number, social?: number): {
    position: Record<string, number>;
    velocity: Record<string, number>;
};
export declare function noveltySample(params: ParameterDef[], history: EvalResult[], resolution?: number, rng?: SeededRNG): Record<string, number>;
export declare class MetaLearner {
    private strategies;
    private explorationRate;
    private rng;
    constructor(strategyTypes: StrategyType[], explorationRate?: number, rng?: SeededRNG);
    private defaultConfig;
    /** Select next strategy using UCB1 (Upper Confidence Bound) */
    selectStrategy(): Strategy;
    updateStrategy(type: StrategyType, improvement: number): void;
    getStrategies(): Strategy[];
}
export declare function generateNextPoint(strategy: Strategy, params: ParameterDef[], best: EvalResult | null, history: EvalResult[], constraints?: Constraint[], gridIndex?: number, rng?: SeededRNG, evalCount?: number): Record<string, number>;
//# sourceMappingURL=strategies.d.ts.map