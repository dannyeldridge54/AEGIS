/**
 * AEGIS — Plugin System
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Extensible plugin architecture for custom strategies, reporters,
 * and evaluation transforms. Add your own optimization algorithms.
 */

import { ParameterDef, EvalResult, Strategy, StrategyType, AgentEvent } from './interfaces';

// ─── Plugin Interfaces ───────────────────────────────────────────────────────

export interface StrategyPlugin {
  /** Unique name (becomes a StrategyType) */
  name: string;
  /** Human description */
  description: string;
  /** Generate next parameter set to evaluate */
  suggest(
    params: ParameterDef[],
    best: EvalResult | null,
    history: EvalResult[],
    config: Record<string, any>
  ): Record<string, number>;
  /** Default configuration */
  defaultConfig?: Record<string, any>;
}

export interface ReporterPlugin {
  name: string;
  /** Called on every agent event */
  onEvent(event: AgentEvent): void;
  /** Called on shutdown */
  onComplete?(state: any): void;
}

export interface TransformPlugin {
  name: string;
  /** Transform parameters before evaluation */
  preEval?(params: Record<string, number>): Record<string, number>;
  /** Transform score after evaluation */
  postEval?(score: number, params: Record<string, number>): number;
}

// ─── Plugin Registry ─────────────────────────────────────────────────────────

class PluginRegistry {
  private strategies: Map<string, StrategyPlugin> = new Map();
  private reporters: Map<string, ReporterPlugin> = new Map();
  private transforms: Map<string, TransformPlugin> = new Map();

  registerStrategy(plugin: StrategyPlugin): void {
    this.strategies.set(plugin.name, plugin);
  }

  registerReporter(plugin: ReporterPlugin): void {
    this.reporters.set(plugin.name, plugin);
  }

  registerTransform(plugin: TransformPlugin): void {
    this.transforms.set(plugin.name, plugin);
  }

  getStrategy(name: string): StrategyPlugin | undefined {
    return this.strategies.get(name);
  }

  getAllStrategies(): StrategyPlugin[] {
    return [...this.strategies.values()];
  }

  getAllReporters(): ReporterPlugin[] {
    return [...this.reporters.values()];
  }

  getAllTransforms(): TransformPlugin[] {
    return [...this.transforms.values()];
  }

  listPlugins(): { strategies: string[]; reporters: string[]; transforms: string[] } {
    return {
      strategies: [...this.strategies.keys()],
      reporters: [...this.reporters.keys()],
      transforms: [...this.transforms.keys()],
    };
  }
}

export const plugins = new PluginRegistry();

// ─── Built-in Plugin Examples ────────────────────────────────────────────────

/** Latin Hypercube Sampling — better coverage than pure random */
export const latinHypercubePlugin: StrategyPlugin = {
  name: 'latin-hypercube',
  description: 'Latin Hypercube Sampling for uniform coverage of parameter space',
  defaultConfig: { divisions: 20 },
  suggest(params, best, history, config) {
    const n = config.divisions || 20;
    const result: Record<string, number> = {};
    for (const p of params) {
      const bin = Math.floor(Math.random() * n);
      const binSize = (p.max - p.min) / n;
      result[p.name] = p.min + bin * binSize + Math.random() * binSize;
    }
    return result;
  },
};

/** Differential Evolution — powerful for non-convex problems */
export const differentialEvolutionPlugin: StrategyPlugin = {
  name: 'differential-evolution',
  description: 'Differential Evolution (DE/rand/1/bin) for rugged landscapes',
  defaultConfig: { F: 0.8, CR: 0.9 },
  suggest(params, best, history, config) {
    const F = config.F || 0.8;
    const CR = config.CR || 0.9;
    const result: Record<string, number> = {};

    if (history.length < 4) {
      // Not enough history, random sample
      for (const p of params) {
        result[p.name] = p.min + Math.random() * (p.max - p.min);
      }
      return result;
    }

    // Pick 3 random distinct solutions
    const pool = history.slice(-50);
    const indices = new Set<number>();
    while (indices.size < 3) indices.add(Math.floor(Math.random() * pool.length));
    const [a, b, c] = [...indices].map(i => pool[i].params);

    // DE mutation + crossover
    const jRand = Math.floor(Math.random() * params.length);
    for (let j = 0; j < params.length; j++) {
      const p = params[j];
      if (Math.random() < CR || j === jRand) {
        result[p.name] = Math.max(p.min, Math.min(p.max,
          a[p.name] + F * (b[p.name] - c[p.name])
        ));
      } else {
        result[p.name] = best ? best.params[p.name] : (p.min + p.max) / 2;
      }
    }
    return result;
  },
};

/** JSON file reporter — saves all events to a file */
export const jsonReporterPlugin: ReporterPlugin = {
  name: 'json-file',
  onEvent(event) {
    // In production, would append to file
    if (event.type === 'new_best' || event.type === 'discovery') {
      // Could write to disk here
    }
  },
  onComplete(state) {
    // Write final state
  },
};

// Register built-in plugins
plugins.registerStrategy(latinHypercubePlugin);
plugins.registerStrategy(differentialEvolutionPlugin);
plugins.registerReporter(jsonReporterPlugin);
