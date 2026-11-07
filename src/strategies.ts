// Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights. AEGIS-ID: bdc12bb54b450a80
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

/** Snap discrete parameters (those with a `step`) onto their grid and keep them in range. */
export function quantize(
  values: Record<string, number>,
  params: ParameterDef[]
): Record<string, number> {
  for (const p of params) {
    let v = values[p.name];
    if (!Number.isFinite(v)) v = randomInRange(p.min, p.max);
    if (p.step && p.step > 0) v = p.min + Math.round((v - p.min) / p.step) * p.step;
    values[p.name] = clamp(v, p.min, p.max);
  }
  return values;
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
  const binKey = (values: Record<string, number>) => params.map(p => {
    const range = p.max - p.min || 1;
    const normalized = (values[p.name] - p.min) / range;
    // Clamp so the upper bound falls in the last bin rather than its own extra bin
    return Math.min(resolution - 1, Math.max(0, Math.floor(normalized * resolution)));
  }).join(',');

  for (const entry of history) {
    const key = binKey(entry.params);
    bins.set(key, (bins.get(key) || 0) + 1);
  }

  // Sample candidates and keep the one in the least-visited region
  let bestCandidate = randomParams(params);
  let minVisits = Infinity;

  for (let attempt = 0; attempt < 100; attempt++) {
    const candidate = attempt === 0 ? bestCandidate : randomParams(params);
    const visits = bins.get(binKey(candidate)) || 0;
    if (visits < minVisits) {
      minVisits = visits;
      bestCandidate = candidate;
      if (visits === 0) break;
    }
  }

  return bestCandidate;
}

// ─── Rank helper ─────────────────────────────────────────────────────────────

/** Map finite scores to [0, 1] by rank (1 = best). Robust to scale and outliers. */
function rankRewards(history: EvalResult[], minimize: boolean): { r: EvalResult; reward: number }[] {
  const finite = history.filter(h => Number.isFinite(h.score));
  const sorted = [...finite].sort((a, b) => minimize ? a.score - b.score : b.score - a.score);
  const n = sorted.length;
  return sorted.map((r, i) => ({ r, reward: n > 1 ? 1 - i / (n - 1) : 1 }));
}

function normalize(values: Record<string, number>, params: ParameterDef[]): number[] {
  return params.map(p => (values[p.name] - p.min) / ((p.max - p.min) || 1));
}

// ─── Bayesian-style surrogate search ─────────────────────────────────────────

/**
 * Surrogate-model search: a kernel-regression model of the (rank-transformed)
 * objective predicts each candidate's quality and uncertainty, and the candidate
 * with the best optimistic estimate (UCB) is chosen. Candidates are half global,
 * half around the current best. A light, dependency-free stand-in for a Gaussian process.
 */
export function surrogateSample(
  params: ParameterDef[],
  best: EvalResult | null,
  history: EvalResult[],
  minimize: boolean,
  kappa: number = 1.5,
  stepScale: number = 1,
  constraints?: Constraint[]
): Record<string, number> {
  const data = rankRewards(history.slice(-300), minimize);
  if (data.length < 5 || !best) return randomParams(params);

  const X = data.map(d => normalize(d.r.params, params));
  const y = data.map(d => d.reward);
  const d = params.length;
  const ell = 0.15 * Math.sqrt(d);
  const inv2l2 = 1 / (2 * ell * ell);
  const meanY = y.reduce((a, b) => a + b, 0) / y.length;
  const stdY = Math.sqrt(y.reduce((a, b) => a + (b - meanY) ** 2, 0) / y.length) || 1;

  const acquisition = (c: Record<string, number>): number => {
    const x = normalize(c, params);
    let wSum = 0, wy = 0;
    for (let i = 0; i < X.length; i++) {
      let dist2 = 0;
      for (let j = 0; j < d; j++) dist2 += (x[j] - X[i][j]) ** 2;
      const w = Math.exp(-dist2 * inv2l2);
      wSum += w; wy += w * y[i];
    }
    const mu = (wy + meanY * 0.1) / (wSum + 0.1); // shrink toward the mean where data is thin
    const sigma = stdY / Math.sqrt(1 + wSum);      // fewer nearby points → more uncertain
    return mu + kappa * sigma;
  };

  // Only feasible candidates are scored, so the caller never has to refit for a retry
  let bestCand: Record<string, number> | null = null;
  let bestAcq = -Infinity;
  for (let i = 0; i < 150; i++) {
    const c = i % 2 === 0 ? randomParams(params) : mutateParams(best.params, params, 0.1 * Math.min(1, stepScale * 2));
    if (!satisfiesConstraints(c, constraints)) continue;
    const a = acquisition(c);
    if (a > bestAcq) { bestAcq = a; bestCand = c; }
  }
  return bestCand ?? randomParams(params);
}

// ─── Region bandit ───────────────────────────────────────────────────────────

/**
 * Multi-armed bandit over regions: each dimension is split into bins, every bin is
 * an arm whose reward is the mean rank of the points sampled in it, and a bin is
 * picked per dimension by UCB1. Balances revisiting good regions with trying rare ones.
 */
export function banditSample(
  params: ParameterDef[],
  history: EvalResult[],
  minimize: boolean,
  bins: number = 8
): Record<string, number> {
  const data = rankRewards(history.slice(-1000), minimize);
  const result: Record<string, number> = {};
  const total = Math.max(data.length, 1);
  for (const p of params) {
    const count = new Array(bins).fill(0);
    const sum = new Array(bins).fill(0);
    const bestIn: Array<number | null> = new Array(bins).fill(null); // best coordinate seen per bin
    const bestReward = new Array(bins).fill(-1);
    const range = (p.max - p.min) || 1;
    for (const { r, reward } of data) {
      const v = r.params[p.name];
      const b = Math.min(bins - 1, Math.max(0, Math.floor(((v - p.min) / range) * bins)));
      count[b]++; sum[b] += reward;
      if (reward > bestReward[b]) { bestReward[b] = reward; bestIn[b] = v; }
    }
    let pick = 0, bestUcb = -Infinity;
    for (let b = 0; b < bins; b++) {
      const ucb = count[b] === 0 ? Infinity : sum[b] / count[b] + Math.sqrt(2 * Math.log(total) / count[b]);
      if (ucb > bestUcb || (ucb === bestUcb && Math.random() < 0.5)) { bestUcb = ucb; pick = b; }
    }
    const width = range / bins;
    const lo = p.min + pick * width;
    const anchor = bestIn[pick];
    if (anchor !== null && Math.random() < 0.5) {
      // Exploit the chosen region: sample close to its best point (refines below bin width)
      const spread = width * 0.25 * Math.pow(Math.random(), 2);
      result[p.name] = clamp(anchor + (Math.random() * 2 - 1) * spread, p.min, p.max);
    } else {
      result[p.name] = lo + Math.random() * width;
    }
  }
  return result;
}

// ─── Particle swarm (stateful) ───────────────────────────────────────────────

interface Particle { x: Record<string, number>; v: Record<string, number>; pbest: Record<string, number> | null; pbestScore: number }
interface SwarmState { particles: Particle[]; next: number; pending: WeakMap<object, number> }

function swarmState(strategy: Strategy): SwarmState {
  if (!strategy.config._swarm) {
    // Non-enumerable so checkpoints/JSON of the strategy list stay small and serializable
    Object.defineProperty(strategy.config, '_swarm', {
      value: { particles: [], next: 0, pending: new WeakMap() } as SwarmState,
      enumerable: false, writable: true,
    });
  }
  return strategy.config._swarm;
}

/** Particle swarm optimization: each call advances the next particle one step. */
export function swarmSample(
  strategy: Strategy,
  params: ParameterDef[],
  best: EvalResult | null
): Record<string, number> {
  const st = swarmState(strategy);
  const n = strategy.config.particles || 10;
  const i = st.next++ % n;
  let pt = st.particles[i];
  let x: Record<string, number>;
  if (!pt) {
    x = randomParams(params);
    const v: Record<string, number> = {};
    for (const p of params) v[p.name] = (Math.random() - 0.5) * 0.2 * (p.max - p.min);
    pt = st.particles[i] = { x, v, pbest: null, pbestScore: NaN };
  } else {
    const g = best?.params ?? pt.pbest ?? pt.x;
    const upd = swarmUpdate(pt.x, pt.v, pt.pbest ?? pt.x, g, params, strategy.config.inertia ?? 0.7);
    // Cap velocity at 20% of the range to keep particles inside the box
    for (const p of params) {
      const vmax = 0.2 * (p.max - p.min);
      upd.velocity[p.name] = clamp(upd.velocity[p.name], -vmax, vmax);
    }
    pt.v = upd.velocity;
    x = upd.position;
    pt.x = x;
  }
  st.pending.set(x, i);
  return x;
}

/**
 * Feed an evaluated point back to stateful strategies (currently the particle swarm).
 * Safe to call for any strategy; a no-op when nothing is waiting for the result.
 */
export function observeResult(
  strategy: Strategy,
  params: Record<string, number>,
  score: number,
  minimize: boolean = true
): void {
  if (strategy.type !== 'swarm' || !strategy.config._swarm || !Number.isFinite(score)) return;
  const st: SwarmState = strategy.config._swarm;
  const i = st.pending.get(params);
  if (i === undefined) return;
  st.pending.delete(params);
  const pt = st.particles[i];
  if (!pt) return;
  const better = Number.isNaN(pt.pbestScore) || (minimize ? score < pt.pbestScore : score > pt.pbestScore);
  if (better) { pt.pbest = { ...params }; pt.pbestScore = score; }
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
      case 'bayesian': return { acquisitionFn: 'ucb', kappa: 1.5 };
      case 'evolutionary': return { populationSize: 20, mutationRate: 0.1 };
      case 'gradient': return { learningRate: 0.01, momentum: 0.9 };
      case 'swarm': return { particles: 10, inertia: 0.7 };
      case 'annealing': return { initialTemp: 1.0, coolingRate: 0.995 };
      case 'bandit': return { bins: 8 };
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
  gridIndex?: number,
  minimize: boolean = true,
  /** Multiplier on local mutation sizes (adapted by the agent; 1 = default sizes) */
  stepScale: number = 1
): Record<string, number> {
  let candidate: Record<string, number>;
  const maxAttempts = 50;
  let elite: EvalResult[] | null = null;

  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    switch (strategy.type) {
      case 'grid':
        candidate = gridSample(params, strategy.config.resolution || 20, gridIndex ?? Math.floor(Math.random() * 10000));
        break;
      case 'random':
        candidate = randomParams(params);
        break;
      case 'evolutionary':
        if (best && history.length > 2) {
          // Second parent comes from the elite (top 10 by score), not the oldest samples
          if (!elite) {
            elite = [...history]
              .filter(r => Number.isFinite(r.score))
              .sort((a, b) => minimize ? a.score - b.score : b.score - a.score)
              .slice(0, 10);
          }
          const pool = elite.length > 0 ? elite : history;
          const parent2 = pool[Math.floor(Math.random() * pool.length)];
          candidate = mutateParams(crossover(best.params, parent2.params, params), params, (strategy.config.mutationRate || 0.1) * Math.min(1, stepScale * 2));
        } else {
          candidate = randomParams(params);
        }
        break;
      case 'gradient':
        if (best) {
          candidate = mutateParams(best.params, params, 0.05 * stepScale);
        } else {
          candidate = randomParams(params);
        }
        break;
      case 'annealing': {
        const temp = (strategy.config.initialTemp || 1.0) * Math.pow(strategy.config.coolingRate || 0.995, history.length);
        candidate = best ? annealingSample(best.params, params, Math.max(temp, 0.02 * stepScale)) : randomParams(params);
        break;
      }
      case 'curiosity':
        candidate = noveltySample(params, history);
        break;
      case 'exploit':
        candidate = best ? mutateParams(best.params, params, (strategy.config.mutationMagnitude || 0.02) * stepScale) : randomParams(params);
        break;
      case 'swarm':
        candidate = swarmSample(strategy, params, best);
        break;
      case 'bayesian':
        candidate = surrogateSample(params, best, history, minimize, strategy.config.kappa ?? 1.5, stepScale, constraints);
        break;
      case 'bandit':
        candidate = banditSample(params, history, minimize, strategy.config.bins || 8);
        break;
      default:
        candidate = best ? mutateParams(best.params, params, 0.1) : randomParams(params);
        break;
    }

    quantize(candidate, params);
    if (satisfiesConstraints(candidate, constraints)) {
      return candidate;
    }
  }

  // Fallback: random points, still preferring ones that satisfy the constraints
  for (let attempt = 0; attempt < 200; attempt++) {
    const fallback = quantize(randomParams(params), params);
    if (satisfiesConstraints(fallback, constraints)) return fallback;
  }
  return quantize(randomParams(params), params);
}
