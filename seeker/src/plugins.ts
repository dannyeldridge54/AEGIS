/**
 * Seeker — Plugin System
 * Extensible strategies, reporters, and transforms.
 * Includes DE and Latin Hypercube built-in.
 */

import { ParameterDef, EvalResult, Strategy, StrategyType, AgentEvent } from './interfaces';
import { SeededRNG } from './rng';

export interface StrategyPlugin {
  name: string;
  description: string;
  suggest(
    params: ParameterDef[], best: EvalResult | null,
    history: EvalResult[], config: Record<string, any>,
    rng: SeededRNG
  ): Record<string, number>;
  defaultConfig?: Record<string, any>;
}

export interface ReporterPlugin {
  name: string;
  onEvent(event: AgentEvent): void;
  onComplete?(state: any): void;
}

export interface TransformPlugin {
  name: string;
  preEval?(params: Record<string, number>): Record<string, number>;
  postEval?(score: number, params: Record<string, number>): number;
}

class PluginRegistry {
  private strategies: Map<string, StrategyPlugin> = new Map();
  private reporters: Map<string, ReporterPlugin> = new Map();
  private transforms: Map<string, TransformPlugin> = new Map();

  registerStrategy(plugin: StrategyPlugin): void { this.strategies.set(plugin.name, plugin); }
  registerReporter(plugin: ReporterPlugin): void { this.reporters.set(plugin.name, plugin); }
  registerTransform(plugin: TransformPlugin): void { this.transforms.set(plugin.name, plugin); }

  getStrategy(name: string): StrategyPlugin | undefined { return this.strategies.get(name); }
  getAllStrategies(): StrategyPlugin[] { return [...this.strategies.values()]; }
  getAllReporters(): ReporterPlugin[] { return [...this.reporters.values()]; }
  getAllTransforms(): TransformPlugin[] { return [...this.transforms.values()]; }

  listPlugins(): { strategies: string[]; reporters: string[]; transforms: string[] } {
    return {
      strategies: [...this.strategies.keys()],
      reporters: [...this.reporters.keys()],
      transforms: [...this.transforms.keys()],
    };
  }
}

export const plugins = new PluginRegistry();

// ─── Built-in Plugins ────────────────────────────────────────────────────────

export const latinHypercubePlugin: StrategyPlugin = {
  name: 'latin-hypercube',
  description: 'Latin Hypercube Sampling for uniform parameter space coverage',
  defaultConfig: { divisions: 20 },
  suggest(params, _best, _history, config, rng) {
    const n = config.divisions || 20;
    const result: Record<string, number> = {};
    for (const p of params) {
      const bin = rng.int(0, n - 1);
      const binSize = (p.max - p.min) / n;
      result[p.name] = p.min + bin * binSize + rng.random() * binSize;
    }
    return result;
  },
};

export const differentialEvolutionPlugin: StrategyPlugin = {
  name: 'differential-evolution',
  description: 'DE/rand/1/bin for rugged landscapes',
  defaultConfig: { F: 0.8, CR: 0.9 },
  suggest(params, best, history, config, rng) {
    const F = config.F || 0.8;
    const CR = config.CR || 0.9;
    const result: Record<string, number> = {};

    if (history.length < 4) {
      for (const p of params) result[p.name] = rng.range(p.min, p.max);
      return result;
    }

    const pool = history.slice(-50);
    const indices = new Set<number>();
    while (indices.size < 3) indices.add(rng.int(0, pool.length - 1));
    const [a, b, c] = [...indices].map(i => pool[i].params);

    const jRand = rng.int(0, params.length - 1);
    for (let j = 0; j < params.length; j++) {
      const p = params[j];
      if (rng.random() < CR || j === jRand) {
        result[p.name] = Math.max(p.min, Math.min(p.max, a[p.name] + F * (b[p.name] - c[p.name])));
      } else {
        result[p.name] = best ? best.params[p.name] : (p.min + p.max) / 2;
      }
    }
    return result;
  },
};

plugins.registerStrategy(latinHypercubePlugin);
plugins.registerStrategy(differentialEvolutionPlugin);
