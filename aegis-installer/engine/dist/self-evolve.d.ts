/**
 * AEGIS — Self-Evolving Strategy Engine
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Inspired by Gödel Agent / EvolveR — strategies that learn to
 * modify their own parameters based on performance feedback.
 * The agent literally rewrites its own optimization approach.
 */
import { ParameterDef, StrategyType } from './interfaces';
export interface EvolutionConfig {
    /** How many generations to evolve strategy configs */
    generations?: number;
    /** Population of strategy variants per generation */
    populationSize?: number;
    /** Mutation rate for strategy hyperparameters */
    mutationRate?: number;
    /** What fraction of top strategies survive */
    eliteRatio?: number;
}
interface StrategyGenome {
    type: StrategyType;
    config: Record<string, number>;
    fitness: number;
    generation: number;
}
/**
 * Self-evolving strategy system.
 * Treats strategy hyperparameters as their own optimization problem:
 * - What mutation rate works best?
 * - What temperature schedule for annealing?
 * - What population size for evolutionary?
 *
 * The meta-meta-learner evolves these automatically.
 */
export declare class SelfEvolver {
    private population;
    private generation;
    private config;
    private bestGenome;
    constructor(config?: EvolutionConfig);
    private initPopulation;
    /**
     * Evaluate a genome by running a mini-optimization and measuring improvement.
     */
    evaluateGenome(genome: StrategyGenome, task: {
        evaluate: (p: Record<string, number>) => number;
        parameters: ParameterDef[];
    }, budget?: number): Promise<number>;
    /**
     * Run one generation of evolution.
     */
    evolveGeneration(task: {
        evaluate: (p: Record<string, number>) => number;
        parameters: ParameterDef[];
    }): Promise<void>;
    /**
     * Full evolution run — returns the best strategy configuration found.
     */
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