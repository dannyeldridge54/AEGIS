/**
 * AEGIS — Strategy Engine
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Implements all optimization strategies + meta-learner that picks
 * the best strategy adaptively based on past performance.
 */

import {
  ParameterDef, EvalResult, Strategy, StrategyType, Constraint,
} from './interfaces';

// ─── Parameter Sampling Helpers ──────────────────────────────────────────────

function randomInRange(min: number, max: number): number {
  return min + Math.random() * (max - min);
}

function clamp(val: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, val));
}

function randomParams(params: ParameterDef[]): Record<string, number> {
  const result: Record<string, number> = {};
  for (const p of params) {
    result[p.name] = randomInRange(p.min, p.max);
  }
  return result;
}

function satisfiesConstraints(
  values: Record<string, number>,
  constraints?: Constraint[]
): boolean {
  if (!constraints || constraints.length === 0) return true;
  return constraints.every(c => c.check(values));
}

// ─── Strategy Implementations ────────────────────────────────────────────────

export function gridSample(
  params: ParameterDef[],
  resolution: number,
  index: number
): Record<string, number> {
  const result: Record<string, number> = {};
  let remaining = index;
  for (const p of params) {
    const step = (p.max - p.min) / (resolution - 1);
    const gridIdx = remaining % resolution;
    remaining = Math.floor(remaining / resolution);
    result[p.name] = p.min + gridIdx * step;
  }
  return result;
}

export function mutateParams(
  base: Record<string, number>,
  params: ParameterDef[],
  magnitude: number = 0.1
): Record<string, number> {
  const result: Record<string, number> = {};
  for (const p of params) {
    const range = p.max - p.min;
    const noise = (Math.random() - 0.5) * 2 * magnitude * range;
    result[p.name] = clamp(base[p.name] + noise, p.min, p.max);
  }
  return result;
}

export function crossover(
  a: Record<string, number>,
  b: Record<string, number>,
  params: ParameterDef[]
): Record<string, number> {
  const result: Record<string, number> = {};
  for (const p of params) {
    result[p.name] = Math.random() < 0.5 ? a[p.name] : b[p.name];
  }
  return result;
}

export function gradientEstimate(
  base: Record<string, number>,
  params: ParameterDef[],
  scores: Map<string, number>,
  evaluate: (p: Record<string, number>) => number,
  stepSize: number = 0.01
): Record<string, number> {
  const result: Record<string, number> = {};
  for (const p of params) {
    const range = p.max - p.min;
    const delta = stepSize * range;
    const plus = { ...base, [p.name]: clamp(base[p.name] + delta, p.min, p.max) };
    const minus = { ...base, [p.name]: clamp(base[p.name] - delta, p.min, p.max) };
    const gradient = (evaluate(plus) - evaluate(minus)) / (2 * delta);
    result[p.name] = clamp(base[p.name] - gradient * delta * 10, p.min, p.max);
  }
  return result;
}

export function annealingSample(
  best: Record<string, number>,
  params: ParameterDef[],
  temperature: number
): Record<string, number> {
  return mutateParams(best, params, temperature);
}

export function swarmUpdate(
  position: Record<string, number>,
  velocity: Record<string, number>,
  personalBest: Record<string, number>,
  globalBest: Record<string, number>,
  params: ParameterDef[],
  inertia: number = 0.7,
  cognitive: number = 1.5,
  social: number = 1.5
): { position: Record<string, number>; velocity: Record<string, number> } {
  const newVel: Record<string, number> = {};
  const newPos: Record<string, number> = {};

  for (const p of params) {
    const r1 = Math.random();
    const r2 = Math.random();
    newVel[p.name] = inertia * (velocity[p.name] || 0)
      + cognitive * r1 * ((personalBest[p.name] || position[p.name]) - position[p.name])
      + social * r2 * ((globalBest[p.name] || position[p.name]) - position[p.name]);
    newPos[p.name] = clamp(position[p.name] + newVel[p.name], p.min, p.max);
  }

  return { position: newPos, velocity: newVel };
}

// ─── Novelty / Curiosity ─────────────────────────────────────────────────────

export function noveltySample(
  params: ParameterDef[],
  history: EvalResult[],
  resolution: number = 20
): Record<string, number> {
  // Discretize space and find least-visited region
  const bins = new Map<string, number>();

  for (const entry of history) {
    const key = params.map(p => {
      const normalized = (entry.params[p.name] - p.min) / (p.max - p.min);
      return Math.floor(normalized * resolution);
    }).join(',');
    bins.set(key, (bins.get(key) || 0) + 1);
  }

  // Sample from least-visited regions
  let bestKey = '';
  let minVisits = Infinity;

  for (let attempt = 0; attempt < 100; attempt++) {
    const candidate = randomParams(params);
    const key = params.map(p => {
      const normalized = (candidate[p.name] - p.min) / (p.max - p.min);
      return Math.floor(normalized * resolution);
    }).join(',');
    const visits = bins.get(key) || 0;
    if (visits < minVisits) {
      minVisits = visits;
      bestKey = key;
      if (visits === 0) return candidate;
    }
  }

  // Return random point in least-visited bin
  return randomParams(params);
}

// ─── Meta-Learner (picks best strategy) ──────────────────────────────────────

export class MetaLearner {
  private strategies: Strategy[];
  private explorationRate: number;

  constructor(strategyTypes: StrategyType[], explorationRate: number = 0.3) {
    this.explorationRate = explorationRate;
    this.strategies = strategyTypes.map(type => ({
      type,
      score: 1.0,
      uses: 0,
      avgImprovement: 0,
      config: this.defaultConfig(type),
    }));
  }

  private defaultConfig(type: StrategyType): Record<string, any> {
    switch (type) {
      case 'grid': return { resolution: 20 };
      case 'random': return {};
      case 'bayesian': return { acquisitionFn: 'ei', kappa: 2.5 };
      case 'evolutionary': return { populationSize: 20, mutationRate: 0.1 };
      case 'gradient': return { learningRate: 0.01, momentum: 0.9 };
      case 'swarm': return { particles: 10, inertia: 0.7 };
      case 'annealing': return { initialTemp: 1.0, coolingRate: 0.995 };
      case 'bandit': return { epsilon: 0.1 };
      case 'curiosity': return { noveltyWeight: 0.8 };
      case 'exploit': return { mutationMagnitude: 0.02 };
      default: return {};
    }
  }

  /** Select next strategy using UCB1 (Upper Confidence Bound) */
  selectStrategy(): Strategy {
    const totalUses = this.strategies.reduce((s, st) => s + st.uses, 0) || 1;

    // Exploration: random pick
    if (Math.random() < this.explorationRate) {
      return this.strategies[Math.floor(Math.random() * this.strategies.length)];
    }

    // UCB1 selection
    let best: Strategy | null = null;
    let bestUCB = -Infinity;

    for (const s of this.strategies) {
      if (s.uses === 0) return s; // Try unused strategies first
      const exploitation = s.avgImprovement;
      const exploration = Math.sqrt(2 * Math.log(totalUses) / s.uses);
      const ucb = exploitation + exploration;
      if (ucb > bestUCB) {
        bestUCB = ucb;
        best = s;
      }
    }

    return best || this.strategies[0];
  }

  /** Update strategy performance after evaluation */
  updateStrategy(type: StrategyType, improvement: number): void {
    const s = this.strategies.find(st => st.type === type);
    if (!s) return;
    s.uses++;
    s.avgImprovement = (s.avgImprovement * (s.uses - 1) + improvement) / s.uses;
    s.score = s.avgImprovement;
  }

  getStrategies(): Strategy[] {
    return [...this.strategies].sort((a, b) => b.score - a.score);
  }
}

// ─── Generate Next Point ─────────────────────────────────────────────────────

export function generateNextPoint(
  strategy: Strategy,
  params: ParameterDef[],
  best: EvalResult | null,
  history: EvalResult[],
  constraints?: Constraint[],
  gridIndex?: number
): Record<string, number> {
  let candidate: Record<string, number>;
  const maxAttempts = 50;

  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    switch (strategy.type) {
      case 'grid':
        candidate = gridSample(params, strategy.config.resolution || 20, gridIndex || Math.floor(Math.random() * 10000));
        break;
      case 'random':
        candidate = randomParams(params);
        break;
      case 'evolutionary':
        if (best && history.length > 2) {
          const parent2 = history[Math.floor(Math.random() * Math.min(history.length, 10))];
          candidate = mutateParams(crossover(best.params, parent2.params, params), params, strategy.config.mutationRate || 0.1);
        } else {
          candidate = randomParams(params);
        }
        break;
      case 'gradient':
        if (best) {
          candidate = mutateParams(best.params, params, 0.05);
        } else {
          candidate = randomParams(params);
        }
        break;
      case 'annealing': {
        const temp = (strategy.config.initialTemp || 1.0) * Math.pow(strategy.config.coolingRate || 0.995, history.length);
        candidate = best ? annealingSample(best.params, params, temp) : randomParams(params);
        break;
      }
      case 'curiosity':
        candidate = noveltySample(params, history);
        break;
      case 'exploit':
        candidate = best ? mutateParams(best.params, params, strategy.config.mutationMagnitude || 0.02) : randomParams(params);
        break;
      case 'swarm':
        candidate = best ? mutateParams(best.params, params, 0.15) : randomParams(params);
        break;
      case 'bayesian':
      case 'bandit':
      default:
        candidate = best ? mutateParams(best.params, params, 0.1) : randomParams(params);
        break;
    }

    if (satisfiesConstraints(candidate, constraints)) {
      return candidate;
    }
  }

  // Fallback to random valid point
  return randomParams(params);
}
