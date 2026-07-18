/**
 * Seeker — Strategy Engine
 * All optimization strategies + meta-learner with seeded RNG.
 * Real finite-difference gradient. Proper simulated annealing with
 * eval-count-based temperature (not history.length).
 */
import { ParameterDef, EvalResult, Strategy, StrategyType, Constraint } from './interfaces';
import { SeededRNG } from './rng';
export declare function gridSample(params: ParameterDef[], resolution: number, index: number): Record<string, number>;
export declare function mutateParams(base: Record<string, number>, params: ParameterDef[], magnitude: number, rng: SeededRNG): Record<string, number>;
export declare function crossover(a: Record<string, number>, b: Record<string, number>, params: ParameterDef[], rng: SeededRNG): Record<string, number>;
/**
 * Real finite-difference gradient descent.
 * Evaluates f(x+δ) and f(x-δ) per dimension to estimate gradient.
 */
export declare function gradientStep(base: Record<string, number>, params: ParameterDef[], history: EvalResult[], rng: SeededRNG, learningRate?: number): Record<string, number>;
/**
 * Quadratic surrogate model (cheap Bayesian approximation).
 * Fits a local quadratic to recent history and minimizes it.
 */
export declare function surrogateStep(params: ParameterDef[], history: EvalResult[], rng: SeededRNG): Record<string, number>;
/**
 * Novelty search — find least-visited regions of param space.
 */
export declare function noveltySample(params: ParameterDef[], history: EvalResult[], rng: SeededRNG, resolution?: number): Record<string, number>;
export declare class MetaLearner {
    private strategies;
    private readonly baseExplorationRate;
    private rng;
    constructor(strategyTypes: StrategyType[], explorationRate?: number, rng?: SeededRNG);
    private defaultConfig;
    selectStrategy(): Strategy;
    updateStrategy(type: StrategyType, improvement: number): void;
    getStrategies(): Strategy[];
}
export declare function generateNextPoint(strategy: Strategy, params: ParameterDef[], best: EvalResult | null, history: EvalResult[], rng: SeededRNG, constraints?: Constraint[], evalCount?: number, gridIndex?: number): Record<string, number>;
//# sourceMappingURL=strategies.d.ts.map