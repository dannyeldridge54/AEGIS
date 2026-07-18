/**
 * Seeker — Self-Evolving Strategy Engine
 * Strategies that learn to modify their own hyperparameters.
 * Meta-optimizes mutation rate, temperature schedule, learning rate, etc.
 * Uses seeded RNG for reproducible evolution.
 */
import { ParameterDef, StrategyType } from './interfaces';
export interface EvolutionConfig {
    generations?: number;
    populationSize?: number;
    mutationRate?: number;
    eliteRatio?: number;
    seed?: number;
}
interface StrategyGenome {
    type: StrategyType;
    config: Record<string, number>;
    fitness: number;
    generation: number;
}
/**
 * Self-evolving strategy system.
 * Treats strategy hyperparameters as their own optimization problem.
 * The meta-meta-learner evolves these automatically.
 */
export declare class SelfEvolver {
    private population;
    private generation;
    private config;
    private bestGenome;
    private rng;
    constructor(config?: EvolutionConfig);
    private initPopulation;
    /** Evaluate a genome by running a mini-optimization */
    evaluateGenome(genome: StrategyGenome, task: {
        evaluate: (p: Record<string, number>) => number;
        parameters: ParameterDef[];
    }, budget?: number): Promise<number>;
    /** Run one generation of evolution */
    evolveGeneration(task: {
        evaluate: (p: Record<string, number>) => number;
        parameters: ParameterDef[];
    }): Promise<void>;
    /** Full evolution run — returns the best strategy configuration */
    evolve(task: {
        evaluate: (p: Record<string, number>) => number;
        parameters: ParameterDef[];
    }, verbose?: boolean): Promise<{
        type: StrategyType;
        config: Record<string, number>;
    }>;
}
export {};
//# sourceMappingURL=self-evolve.d.ts.map