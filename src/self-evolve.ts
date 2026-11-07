// Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights. AEGIS-ID: 442dc80aec31b4bf
/**
 * AEGIS — Self-Evolving Strategy Engine
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Inspired by Gödel Agent / EvolveR — strategies that learn to
 * modify their own parameters based on performance feedback.
 * The agent literally rewrites its own optimization approach.
 */

import { ParameterDef, EvalResult, StrategyType } from './interfaces';
import { generateNextPoint } from './strategies';

/** Valid range of every evolvable hyperparameter, per strategy type. */
const STRATEGY_SPACE: Array<{ type: StrategyType; paramRanges: Record<string, [number, number]> }> = [
  { type: 'evolutionary', paramRanges: { mutationRate: [0.01, 0.5], populationSize: [5, 50] } },
  { type: 'annealing', paramRanges: { initialTemp: [0.1, 5.0], coolingRate: [0.9, 0.999] } },
  { type: 'gradient', paramRanges: { learningRate: [0.001, 0.5], momentum: [0, 0.99] } },
  { type: 'exploit', paramRanges: { mutationMagnitude: [0.005, 0.2] } },
  { type: 'curiosity', paramRanges: { noveltyWeight: [0.3, 1.0] } },
];

function rangesFor(type: StrategyType): Record<string, [number, number]> {
  return STRATEGY_SPACE.find(s => s.type === type)?.paramRanges || {};
}

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
export class SelfEvolver {
  private population: StrategyGenome[] = [];
  private generation = 0;
  private config: Required<EvolutionConfig>;
  private bestGenome: StrategyGenome | null = null;

  constructor(config?: EvolutionConfig) {
    this.config = {
      generations: config?.generations || 20,
      populationSize: config?.populationSize || 12,
      mutationRate: config?.mutationRate || 0.3,
      eliteRatio: config?.eliteRatio || 0.25,
    };

    this.initPopulation();
  }

  private initPopulation(): void {
    for (let i = 0; i < this.config.populationSize; i++) {
      const template = STRATEGY_SPACE[i % STRATEGY_SPACE.length];
      const config: Record<string, number> = {};
      for (const [key, [min, max]] of Object.entries(template.paramRanges)) {
        config[key] = min + Math.random() * (max - min);
      }
      this.population.push({
        type: template.type,
        config,
        fitness: 0,
        generation: 0,
      });
    }
  }

  /**
   * Evaluate a genome by running a short optimization driven by that genome's
   * strategy and hyperparameters. Fitness is the negated best score reached
   * (higher = better), so every genome is judged on the same scale.
   */
  async evaluateGenome(
    genome: StrategyGenome,
    task: { evaluate: (p: Record<string, number>) => number | Promise<number>; parameters: ParameterDef[] },
    budget: number = 200
  ): Promise<number> {
    const strategy = { type: genome.type, score: 0, uses: 0, avgImprovement: 0, config: genome.config };
    const history: EvalResult[] = [];
    let best: EvalResult | null = null;
    // A short random warm-up gives every genome the same kind of starting point
    const warmup = Math.min(10, Math.floor(budget / 4));

    for (let i = 0; i < budget; i++) {
      const params = i < warmup
        ? generateNextPoint({ ...strategy, type: 'random' }, task.parameters, null, history)
        : generateNextPoint(strategy, task.parameters, best, history, undefined, i);
      const raw = await task.evaluate(params);
      const score = Number.isFinite(raw) ? raw : Infinity;
      const result: EvalResult = { params, score, timestamp: Date.now(), strategy: genome.type };
      history.push(result);
      if (!best || score < best.score) best = result;
    }

    return best && Number.isFinite(best.score) ? -best.score : -Infinity;
  }

  /**
   * Run one generation of evolution.
   */
  async evolveGeneration(
    task: { evaluate: (p: Record<string, number>) => number | Promise<number>; parameters: ParameterDef[] }
  ): Promise<void> {
    // Evaluate all genomes
    for (const genome of this.population) {
      genome.fitness = await this.evaluateGenome(genome, task);
    }

    // Sort by fitness
    this.population.sort((a, b) => b.fitness - a.fitness);

    // Track best
    if (!this.bestGenome || this.population[0].fitness > this.bestGenome.fitness) {
      this.bestGenome = { ...this.population[0], config: { ...this.population[0].config } };
    }

    // Selection + mutation
    const eliteCount = Math.ceil(this.config.populationSize * this.config.eliteRatio);
    const elites = this.population.slice(0, eliteCount);
    const newPop: StrategyGenome[] = [...elites];

    while (newPop.length < this.config.populationSize) {
      const parent = elites[Math.floor(Math.random() * elites.length)];
      const child: StrategyGenome = {
        type: parent.type,
        config: { ...parent.config },
        fitness: 0,
        generation: this.generation + 1,
      };

      // Mutate config values (±50%), clamped to each hyperparameter's valid range
      const ranges = rangesFor(child.type);
      for (const key of Object.keys(child.config)) {
        if (Math.random() < this.config.mutationRate) {
          child.config[key] *= 0.5 + Math.random();
          const r = ranges[key];
          if (r) child.config[key] = Math.min(r[1], Math.max(r[0], child.config[key]));
        }
      }

      newPop.push(child);
    }

    this.population = newPop;
    this.generation++;
  }

  /**
   * Full evolution run — returns the best strategy configuration found.
   */
  async evolve(
    task: { evaluate: (p: Record<string, number>) => number | Promise<number>; parameters: ParameterDef[] },
    verbose: boolean = true
  ): Promise<{ type: StrategyType; config: Record<string, number> }> {
    if (verbose) {
      console.log(`[AEGIS-Evolve] Self-evolving strategy over ${this.config.generations} generations...`);
    }

    for (let g = 0; g < this.config.generations; g++) {
      await this.evolveGeneration(task);

      if (verbose && g % 5 === 0) {
        const best = this.population[0];
        console.log(`  Gen ${g}: best=${best.type} best score=${(-best.fitness).toFixed(6)} config=${JSON.stringify(best.config)}`);
      }
    }

    const winner = this.bestGenome || this.population[0];
    if (verbose) {
      console.log(`[AEGIS-Evolve] Winner: ${winner.type} with config:`, winner.config);
    }

    return { type: winner.type, config: winner.config };
  }
}
