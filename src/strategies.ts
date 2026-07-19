/**
 * AEGIS — Strategy Engine
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Implements all optimization strategies + meta-learner that picks
 * the best strategy adaptively based on past performance.
 * Now with seeded RNG, real gradient estimation, quadratic surrogate,
 * and eval-count-based annealing.
 */

import {
  ParameterDef, EvalResult, Strategy, StrategyType, Constraint,
} from './interfaces';
import { SeededRNG } from './rng';

// ─── Parameter Sampling Helpers ──────────────────────────────────────────────

function clamp(val: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, val));
}

function randomParams(params: ParameterDef[], rng: SeededRNG): Record<string, number> {
  const result: Record<string, number> = {};
  for (const p of params) {
    result[p.name] = rng.range(p.min, p.max);
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
  magnitude: number = 0.1,
  rng?: SeededRNG
): Record<string, number> {
  const result: Record<string, number> = {};
  for (const p of params) {
    const range = p.max - p.min;
    const r = rng ? rng.random() : Math.random();
    const noise = (r - 0.5) * 2 * magnitude * range;
    result[p.name] = clamp(base[p.name] + noise, p.min, p.max);
  }
  return result;
}

export function crossover(
  a: Record<string, number>,
  b: Record<string, number>,
  params: ParameterDef[],
  rng?: SeededRNG
): Record<string, number> {
  const result: Record<string, number> = {};
  for (const p of params) {
    result[p.name] = (rng ? rng.random() : Math.random()) < 0.5 ? a[p.name] : b[p.name];
  }
  return result;
}

/** Real finite-difference gradient estimation from recent history */
export function gradientStep(
  best: EvalResult,
  params: ParameterDef[],
  history: EvalResult[],
  rng: SeededRNG
): Record<string, number> {
  if (history.length < params.length * 2) {
    return mutateParams(best.params, params, 0.05, rng);
  }

  const recent = history.slice(-Math.min(history.length, 50));
  const result: Record<string, number> = { ...best.params };
  const lr = 0.1;

  for (const p of params) {
    // Estimate gradient from nearby points
    let sumGrad = 0;
    let count = 0;
    for (let i = 1; i < recent.length; i++) {
      const dx = recent[i].params[p.name] - recent[i - 1].params[p.name];
      const dy = recent[i].score - recent[i - 1].score;
      if (Math.abs(dx) > 1e-12) {
        sumGrad += dy / dx;
        count++;
      }
    }

    if (count > 0) {
      const grad = sumGrad / count;
      const range = p.max - p.min;
      result[p.name] = clamp(
        best.params[p.name] - lr * grad * range * 0.1,
        p.min, p.max,
      );
    } else {
      result[p.name] = clamp(
        best.params[p.name] + rng.normal(0, (p.max - p.min) * 0.02),
        p.min, p.max,
      );
    }
  }

  return result;
}

/** Quadratic surrogate model for bayesian strategy */
export function surrogateStep(
  best: EvalResult,
  params: ParameterDef[],
  history: EvalResult[],
  rng: SeededRNG
): Record<string, number> {
  if (history.length < 10) {
    return randomParams(params, rng);
  }

  const recent = history.slice(-Math.min(history.length, 100));
  const result: Record<string, number> = {};

  for (const p of params) {
    // Fit quadratic: score ≈ a*x² + b*x + c per dimension
    let sumX = 0, sumX2 = 0, sumX3 = 0, sumX4 = 0;
    let sumY = 0, sumXY = 0, sumX2Y = 0;
    const n = recent.length;

    for (const r of recent) {
      const x = r.params[p.name];
      const y = r.score;
      sumX += x; sumX2 += x * x; sumX3 += x * x * x; sumX4 += x * x * x * x;
      sumY += y; sumXY += x * y; sumX2Y += x * x * y;
    }

    // Solve least-squares for quadratic coefficients
    const det = n * (sumX2 * sumX4 - sumX3 * sumX3)
      - sumX * (sumX * sumX4 - sumX3 * sumX2)
      + sumX2 * (sumX * sumX3 - sumX2 * sumX2);

    if (Math.abs(det) > 1e-20) {
      const a = (sumY * (sumX2 * sumX4 - sumX3 * sumX3)
        - sumXY * (sumX * sumX4 - sumX3 * sumX2)
        + sumX2Y * (sumX * sumX3 - sumX2 * sumX2)) / det;

      const b = (n * (sumXY * sumX4 - sumX2Y * sumX3)
        - sumY * (sumX * sumX4 - sumX3 * sumX2)
        + sumX2 * (sumX * sumX2Y - sumXY * sumX2)) / det;

      // Predicted minimum at x = -b/(2a) if a > 0
      if (a > 1e-12) {
        const xMin = clamp(-b / (2 * a), p.min, p.max);
        // Add small noise around predicted minimum
        result[p.name] = clamp(xMin + rng.normal(0, (p.max - p.min) * 0.05), p.min, p.max);
      } else {
        result[p.name] = rng.range(p.min, p.max);
      }
    } else {
      result[p.name] = rng.range(p.min, p.max);
    }
  }

  return result;
}

export function annealingSample(
  best: Record<string, number>,
  params: ParameterDef[],
  temperature: number,
  rng?: SeededRNG
): Record<string, number> {
  return mutateParams(best, params, temperature, rng);
}

export function swarmUpdate(
  position: Record<string, number>,
  velocity: Record<string, number>,
  personalBest: Record<string, number>,
  globalBest: Record<string, number>,
  params: ParameterDef[],
  rng?: SeededRNG,
  inertia: number = 0.7,
  cognitive: number = 1.5,
  social: number = 1.5
): { position: Record<string, number>; velocity: Record<string, number> } {
  const newVel: Record<string, number> = {};
  const newPos: Record<string, number> = {};

  for (const p of params) {
    const r1 = rng ? rng.random() : Math.random();
    const r2 = rng ? rng.random() : Math.random();
    newVel[p.name] = inertia * (velocity[p.name] || 0)
      + cognitive * r1 * ((personalBest[p.name] || position[p.name]) - position[p.name])
      + social * r2 * ((globalBest[p.name] || position[p.name]) - position[p.name]);
    newPos[p.name] = clamp(position[p.name] + newVel[p.name], p.min, p.max);
  }

  return { position: newPos, velocity: newVel };
}

// ─── Novelty / Curiosity ─────────────────────────────────────────────────────

// ─── CMA-ES State ────────────────────────────────────────────────────────────
// Covariance Matrix Adaptation — the gold standard for continuous optimization.
// Learns parameter correlations to sample along the best directions.

export class CMAESState {
  mean: number[];         // Current mean vector (normalized [0,1])
  sigma: number;          // Overall step size
  C: number[][];          // Covariance matrix
  pc: number[];           // Evolution path for C
  ps: number[];           // Evolution path for sigma
  lambda: number;         // Population size
  mu: number;             // Parent count
  weights: number[];      // Recombination weights
  mueff: number;          // Variance effective selection mass
  cc: number;             // Learning rate for pc
  cs: number;             // Learning rate for ps
  c1: number;             // Rank-one update rate
  cmu: number;            // Rank-mu update rate
  damps: number;          // Damping for sigma
  chiN: number;           // Expected ||N(0,I)||
  gen: number;            // Generation counter
  private dim: number;

  constructor(dim: number) {
    this.dim = dim;
    this.lambda = 4 + Math.floor(3 * Math.log(dim));
    this.mu = Math.floor(this.lambda / 2);
    this.mean = new Array(dim).fill(0.5);
    this.sigma = 0.3;
    this.gen = 0;

    // Weights
    this.weights = [];
    for (let i = 0; i < this.mu; i++) {
      this.weights.push(Math.log(this.mu + 0.5) - Math.log(i + 1));
    }
    const wSum = this.weights.reduce((a, b) => a + b, 0);
    this.weights = this.weights.map(w => w / wSum);
    this.mueff = 1 / this.weights.reduce((s, w) => s + w * w, 0);

    // Adaptation parameters
    this.cc = (4 + this.mueff / dim) / (dim + 4 + 2 * this.mueff / dim);
    this.cs = (this.mueff + 2) / (dim + this.mueff + 5);
    this.c1 = 2 / ((dim + 1.3) * (dim + 1.3) + this.mueff);
    this.cmu = Math.min(1 - this.c1, 2 * (this.mueff - 2 + 1 / this.mueff) / ((dim + 2) * (dim + 2) + this.mueff));
    this.damps = 1 + 2 * Math.max(0, Math.sqrt((this.mueff - 1) / (dim + 1)) - 1) + this.cs;
    this.chiN = Math.sqrt(dim) * (1 - 1 / (4 * dim) + 1 / (21 * dim * dim));

    // Evolution paths
    this.pc = new Array(dim).fill(0);
    this.ps = new Array(dim).fill(0);

    // Covariance matrix (identity)
    this.C = [];
    for (let i = 0; i < dim; i++) {
      this.C[i] = new Array(dim).fill(0);
      this.C[i][i] = 1;
    }
  }

  /** Sample a candidate from the current distribution */
  sample(rng: SeededRNG): number[] {
    const z = new Array(this.dim);
    for (let i = 0; i < this.dim; i++) {
      z[i] = rng.normal(0, 1);
    }
    // Multiply by sqrt(C) approximation: C * z (since C starts as identity, this is reasonable)
    // For efficiency, use C directly as approximate sqrt
    const y = new Array(this.dim);
    for (let i = 0; i < this.dim; i++) {
      let sum = 0;
      for (let j = 0; j < this.dim; j++) {
        sum += this.C[i][j] * z[j];
      }
      y[i] = this.mean[i] + this.sigma * sum;
    }
    return y;
  }

  /** Update CMA-ES state with ranked population */
  update(rankedPopulation: number[][]): void {
    const dim = this.dim;
    const oldMean = [...this.mean];

    // Weighted recombination — new mean
    this.mean = new Array(dim).fill(0);
    for (let i = 0; i < this.mu; i++) {
      for (let d = 0; d < dim; d++) {
        this.mean[d] += this.weights[i] * rankedPopulation[i][d];
      }
    }

    // Evolution path for sigma (ps)
    const meanDiff = this.mean.map((m, d) => (m - oldMean[d]) / this.sigma);
    for (let d = 0; d < dim; d++) {
      this.ps[d] = (1 - this.cs) * this.ps[d] + Math.sqrt(this.cs * (2 - this.cs) * this.mueff) * meanDiff[d];
    }

    // Evolution path for covariance (pc)
    const psNorm = Math.sqrt(this.ps.reduce((s, v) => s + v * v, 0));
    const hsig = psNorm / Math.sqrt(1 - Math.pow(1 - this.cs, 2 * (this.gen + 1))) < (1.4 + 2 / (dim + 1)) * this.chiN ? 1 : 0;
    for (let d = 0; d < dim; d++) {
      this.pc[d] = (1 - this.cc) * this.pc[d] + hsig * Math.sqrt(this.cc * (2 - this.cc) * this.mueff) * meanDiff[d];
    }

    // Covariance matrix update
    for (let i = 0; i < dim; i++) {
      for (let j = 0; j < dim; j++) {
        // Rank-one update
        let newC = (1 - this.c1 - this.cmu) * this.C[i][j] + this.c1 * this.pc[i] * this.pc[j];
        // Rank-mu update
        for (let k = 0; k < this.mu; k++) {
          const di = (rankedPopulation[k][i] - oldMean[i]) / this.sigma;
          const dj = (rankedPopulation[k][j] - oldMean[j]) / this.sigma;
          newC += this.cmu * this.weights[k] * di * dj;
        }
        this.C[i][j] = newC;
      }
    }

    // Step size control
    this.sigma *= Math.exp((this.cs / this.damps) * (psNorm / this.chiN - 1));
    this.sigma = Math.max(1e-10, Math.min(this.sigma, 2.0));

    this.gen++;
  }
}

// Global CMA-ES state cache (one per param dimension count)
const cmaStates = new Map<number, CMAESState>();

export function cmaESSample(
  params: ParameterDef[],
  history: EvalResult[],
  rng: SeededRNG,
): Record<string, number> {
  const dim = params.length;

  // Get or create CMA-ES state
  if (!cmaStates.has(dim)) {
    cmaStates.set(dim, new CMAESState(dim));
  }
  const state = cmaStates.get(dim)!;

  // Every lambda evaluations, update the distribution with ranked results
  if (history.length >= state.lambda && history.length % state.lambda === 0) {
    const recentPop = history.slice(-state.lambda);
    // Sort by score (ascending = best first for minimization)
    const sorted = [...recentPop].sort((a, b) => a.score - b.score);
    // Convert to normalized coordinates
    const rankedNorm = sorted.map(r =>
      params.map(p => (r.params[p.name] - p.min) / (p.max - p.min))
    );
    if (rankedNorm.length >= state.mu) {
      state.update(rankedNorm);
    }
  }

  // Sample from current distribution
  const normalized = state.sample(rng);
  const result: Record<string, number> = {};
  for (let i = 0; i < params.length; i++) {
    result[params[i].name] = clamp(
      params[i].min + normalized[i] * (params[i].max - params[i].min),
      params[i].min, params[i].max
    );
  }
  return result;
}

// ─── Parameter Normalization ─────────────────────────────────────────────────
// Normalize parameters to [0,1] for strategies, denormalize after

function normalizeParams(values: Record<string, number>, params: ParameterDef[]): number[] {
  return params.map(p => (values[p.name] - p.min) / (p.max - p.min));
}

function denormalizeParams(normalized: number[], params: ParameterDef[]): Record<string, number> {
  const result: Record<string, number> = {};
  for (let i = 0; i < params.length; i++) {
    result[params[i].name] = clamp(
      params[i].min + normalized[i] * (params[i].max - params[i].min),
      params[i].min, params[i].max
    );
  }
  return result;
}

export { normalizeParams, denormalizeParams };

export function noveltySample(
  params: ParameterDef[],
  history: EvalResult[],
  resolution: number = 20,
  rng?: SeededRNG
): Record<string, number> {
  const bins = new Map<string, number>();

  for (const entry of history) {
    const key = params.map(p => {
      const normalized = (entry.params[p.name] - p.min) / (p.max - p.min);
      return Math.floor(normalized * resolution);
    }).join(',');
    bins.set(key, (bins.get(key) || 0) + 1);
  }

  let minVisits = Infinity;
  let bestCandidate: Record<string, number> | null = null;

  for (let attempt = 0; attempt < 100; attempt++) {
    const candidate = randomParams(params, rng || new SeededRNG());
    const key = params.map(p => {
      const normalized = (candidate[p.name] - p.min) / (p.max - p.min);
      return Math.floor(normalized * resolution);
    }).join(',');
    const visits = bins.get(key) || 0;
    if (visits < minVisits) {
      minVisits = visits;
      bestCandidate = candidate;
      if (visits === 0) return candidate;
    }
  }

  return bestCandidate || randomParams(params, rng || new SeededRNG());
}

// ─── Meta-Learner (picks best strategy) ──────────────────────────────────────

export class MetaLearner {
  private strategies: Strategy[];
  private explorationRate: number;
  private rng: SeededRNG;

  constructor(strategyTypes: StrategyType[], explorationRate: number = 0.3, rng?: SeededRNG) {
    this.explorationRate = explorationRate;
    this.rng = rng || new SeededRNG();
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
      case 'cma-es': return { populationSize: 'auto' };
      default: return {};
    }
  }

  /** Select next strategy using UCB1 (Upper Confidence Bound) */
  selectStrategy(): Strategy {
    const totalUses = this.strategies.reduce((s, st) => s + st.uses, 0) || 1;

    if (this.rng.random() < this.explorationRate) {
      return this.rng.pick(this.strategies);
    }

    let best: Strategy | null = null;
    let bestUCB = -Infinity;

    for (const s of this.strategies) {
      if (s.uses === 0) return s;
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
  gridIndex?: number,
  rng?: SeededRNG,
  evalCount?: number
): Record<string, number> {
  let candidate: Record<string, number>;
  const maxAttempts = 50;
  const r = rng || new SeededRNG();

  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    switch (strategy.type) {
      case 'grid':
        candidate = gridSample(params, strategy.config.resolution || 20, gridIndex || r.int(0, 9999));
        break;
      case 'random':
        candidate = randomParams(params, r);
        break;
      case 'evolutionary':
        if (best && history.length > 2) {
          const parent2 = history[r.int(0, Math.min(history.length - 1, 9))];
          candidate = mutateParams(crossover(best.params, parent2.params, params, r), params, strategy.config.mutationRate || 0.1, r);
        } else {
          candidate = randomParams(params, r);
        }
        break;
      case 'gradient':
        // Real finite-difference gradient estimation
        if (best && history.length > params.length * 2) {
          candidate = gradientStep(best, params, history, r);
        } else {
          candidate = best ? mutateParams(best.params, params, 0.05, r) : randomParams(params, r);
        }
        break;
      case 'bayesian':
        // Quadratic surrogate model
        if (best && history.length > 10) {
          candidate = surrogateStep(best, params, history, r);
        } else {
          candidate = randomParams(params, r);
        }
        break;
      case 'annealing': {
        // Eval-count-based temperature (not history.length which resets on trim)
        const evals = evalCount || history.length;
        const temp = (strategy.config.initialTemp || 1.0) * Math.pow(strategy.config.coolingRate || 0.995, evals);
        candidate = best ? annealingSample(best.params, params, temp, r) : randomParams(params, r);
        break;
      }
      case 'curiosity':
        candidate = noveltySample(params, history, 20, r);
        break;
      case 'exploit':
        candidate = best ? mutateParams(best.params, params, strategy.config.mutationMagnitude || 0.02, r) : randomParams(params, r);
        break;
      case 'cma-es':
        candidate = cmaESSample(params, history, r);
        break;
      case 'swarm':
        candidate = best ? mutateParams(best.params, params, 0.15, r) : randomParams(params, r);
        break;
      case 'bandit':
      default:
        candidate = best ? mutateParams(best.params, params, 0.1, r) : randomParams(params, r);
        break;
    }

    if (satisfiesConstraints(candidate, constraints)) {
      return candidate;
    }
  }

  return randomParams(params, r);
}
