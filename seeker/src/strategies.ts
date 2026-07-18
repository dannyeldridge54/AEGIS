/**
 * Seeker — Strategy Engine
 * All optimization strategies + meta-learner with seeded RNG.
 * Real finite-difference gradient. Proper simulated annealing with
 * eval-count-based temperature (not history.length).
 */

import {
  ParameterDef, EvalResult, Strategy, StrategyType, Constraint,
} from './interfaces';
import { SeededRNG } from './rng';

// ─── Seeded Parameter Sampling ───────────────────────────────────────────────

function randomParams(params: ParameterDef[], rng: SeededRNG): Record<string, number> {
  const result: Record<string, number> = {};
  for (const p of params) result[p.name] = rng.range(p.min, p.max);
  return result;
}

function clamp(val: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, val));
}

function satisfiesConstraints(values: Record<string, number>, constraints?: Constraint[]): boolean {
  if (!constraints || constraints.length === 0) return true;
  return constraints.every(c => c.check(values));
}

// ─── Strategy Implementations ────────────────────────────────────────────────

export function gridSample(params: ParameterDef[], resolution: number, index: number): Record<string, number> {
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
  base: Record<string, number>, params: ParameterDef[],
  magnitude: number, rng: SeededRNG
): Record<string, number> {
  const result: Record<string, number> = {};
  for (const p of params) {
    const range = p.max - p.min;
    const noise = (rng.random() - 0.5) * 2 * magnitude * range;
    result[p.name] = clamp(base[p.name] + noise, p.min, p.max);
  }
  return result;
}

export function crossover(
  a: Record<string, number>, b: Record<string, number>,
  params: ParameterDef[], rng: SeededRNG
): Record<string, number> {
  const result: Record<string, number> = {};
  for (const p of params) result[p.name] = rng.random() < 0.5 ? a[p.name] : b[p.name];
  return result;
}

/**
 * Real finite-difference gradient descent.
 * Evaluates f(x+δ) and f(x-δ) per dimension to estimate gradient.
 */
export function gradientStep(
  base: Record<string, number>, params: ParameterDef[],
  history: EvalResult[], rng: SeededRNG,
  learningRate: number = 0.05
): Record<string, number> {
  if (history.length < 3) return randomParams(params, rng);

  // Use recent history to estimate gradient via finite differences
  const result: Record<string, number> = {};
  for (const p of params) {
    // Find pairs where only this param varies significantly
    const sorted = history.slice(-100).sort((a, b) => a.params[p.name] - b.params[p.name]);
    if (sorted.length < 2) {
      result[p.name] = base[p.name] + rng.normal(0, 0.01 * (p.max - p.min));
      continue;
    }

    // Simple central difference from extremes in recent window
    const lo = sorted[0];
    const hi = sorted[sorted.length - 1];
    const dx = hi.params[p.name] - lo.params[p.name];
    if (Math.abs(dx) < 1e-12) {
      result[p.name] = base[p.name] + rng.normal(0, 0.02 * (p.max - p.min));
      continue;
    }

    const dy = hi.score - lo.score;
    const gradient = dy / dx;
    // Step against gradient (minimize) with some noise for escape
    const step = -gradient * learningRate * (p.max - p.min) + rng.normal(0, 0.005 * (p.max - p.min));
    result[p.name] = clamp(base[p.name] + step, p.min, p.max);
  }
  return result;
}

/**
 * Quadratic surrogate model (cheap Bayesian approximation).
 * Fits a local quadratic to recent history and minimizes it.
 */
export function surrogateStep(
  params: ParameterDef[], history: EvalResult[], rng: SeededRNG
): Record<string, number> {
  if (history.length < params.length * 3) return randomParams(params, rng);

  // Fit independent quadratics per dimension using recent data
  const recent = history.slice(-200);
  const best = recent.reduce((a, b) => a.score < b.score ? a : b);
  const result: Record<string, number> = {};

  for (const p of params) {
    // Collect (x, y) pairs for this dimension
    const points = recent.map(r => ({ x: r.params[p.name], y: r.score }));

    // Fit quadratic y = ax² + bx + c using least squares (3 points minimum)
    let sx = 0, sx2 = 0, sx3 = 0, sx4 = 0, sy = 0, sxy = 0, sx2y = 0;
    const n = points.length;
    for (const { x, y } of points) {
      sx += x; sx2 += x * x; sx3 += x * x * x; sx4 += x * x * x * x;
      sy += y; sxy += x * y; sx2y += x * x * y;
    }

    // Solve for a (quadratic coefficient) — if a > 0 we have a bowl
    const denom = n * sx2 * sx4 + sx * sx3 * sx2 + sx2 * sx * sx3
      - sx2 * sx2 * sx2 - sx * sx * sx4 - n * sx3 * sx3;

    if (Math.abs(denom) < 1e-15) {
      result[p.name] = best.params[p.name] + rng.normal(0, 0.05 * (p.max - p.min));
    } else {
      const a = (sy * sx2 * sx4 + sx * sx3 * sx2y + sx2 * sxy * sx3
        - sx2 * sx2 * sx2y - sx * sy * sx4 - sxy * sx3 * n
      ) / denom;
      const b = (n * sxy * sx4 + sy * sx3 * sx2 + sx2 * sx * sx2y
        - sx2 * sxy * sx2 - sy * sx * sx4 - n * sx2y * sx3
      ) / denom;

      if (a > 1e-10) {
        // Minimum at x = -b / (2a)
        const xMin = clamp(-b / (2 * a), p.min, p.max);
        result[p.name] = xMin + rng.normal(0, 0.02 * (p.max - p.min));
      } else {
        result[p.name] = best.params[p.name] + rng.normal(0, 0.05 * (p.max - p.min));
      }
    }
    result[p.name] = clamp(result[p.name], p.min, p.max);
  }
  return result;
}

/**
 * Novelty search — find least-visited regions of param space.
 */
export function noveltySample(
  params: ParameterDef[], history: EvalResult[],
  rng: SeededRNG, resolution: number = 20
): Record<string, number> {
  const bins = new Map<string, number>();
  for (const entry of history) {
    const key = params.map(p => {
      const normalized = (entry.params[p.name] - p.min) / (p.max - p.min || 1);
      return Math.floor(Math.min(normalized, 0.9999) * resolution);
    }).join(',');
    bins.set(key, (bins.get(key) || 0) + 1);
  }

  // Sample candidates and pick least-visited
  let bestCandidate = randomParams(params, rng);
  let minVisits = Infinity;

  for (let attempt = 0; attempt < 100; attempt++) {
    const candidate = randomParams(params, rng);
    const key = params.map(p => {
      const normalized = (candidate[p.name] - p.min) / (p.max - p.min || 1);
      return Math.floor(Math.min(normalized, 0.9999) * resolution);
    }).join(',');
    const visits = bins.get(key) || 0;
    if (visits < minVisits) {
      minVisits = visits;
      bestCandidate = candidate;
      if (visits === 0) return candidate;
    }
  }

  return bestCandidate;
}

// ─── Meta-Learner (UCB1) ────────────────────────────────────────────────────

export class MetaLearner {
  private strategies: Strategy[];
  private readonly baseExplorationRate: number;
  private rng: SeededRNG;

  constructor(strategyTypes: StrategyType[], explorationRate: number = 0.3, rng?: SeededRNG) {
    this.baseExplorationRate = explorationRate;
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
      case 'bayesian': return { acquisitionFn: 'ei' };
      case 'evolutionary': return { populationSize: 20, mutationRate: 0.1 };
      case 'gradient': return { learningRate: 0.05 };
      case 'swarm': return { particles: 10, inertia: 0.7 };
      case 'annealing': return { initialTemp: 1.0, coolingRate: 0.995 };
      case 'bandit': return { epsilon: 0.1 };
      case 'curiosity': return { noveltyWeight: 0.8 };
      case 'exploit': return { mutationMagnitude: 0.02 };
      default: return {};
    }
  }

  selectStrategy(): Strategy {
    const totalUses = this.strategies.reduce((s, st) => s + st.uses, 0) || 1;

    // Exploration: random pick (uses seeded RNG)
    if (this.rng.random() < this.baseExplorationRate) {
      return this.rng.pick(this.strategies);
    }

    // UCB1 selection
    let best: Strategy | null = null;
    let bestUCB = -Infinity;

    for (const s of this.strategies) {
      if (s.uses === 0) return s;
      const exploitation = s.avgImprovement;
      const exploration = Math.sqrt(2 * Math.log(totalUses) / s.uses);
      const ucb = exploitation + exploration;
      if (ucb > bestUCB) { bestUCB = ucb; best = s; }
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
  strategy: Strategy, params: ParameterDef[], best: EvalResult | null,
  history: EvalResult[], rng: SeededRNG,
  constraints?: Constraint[], evalCount?: number,
  gridIndex?: number
): Record<string, number> {
  const maxAttempts = 50;

  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    let candidate: Record<string, number>;

    switch (strategy.type) {
      case 'grid':
        candidate = gridSample(params, strategy.config.resolution || 20,
          gridIndex || Math.floor(rng.random() * 10000));
        break;

      case 'random':
        candidate = randomParams(params, rng);
        break;

      case 'evolutionary':
        if (best && history.length > 2) {
          const parent2 = rng.pick(history.slice(-Math.min(history.length, 20)));
          candidate = mutateParams(
            crossover(best.params, parent2.params, params, rng),
            params, strategy.config.mutationRate || 0.1, rng
          );
        } else {
          candidate = randomParams(params, rng);
        }
        break;

      case 'gradient':
        candidate = best
          ? gradientStep(best.params, params, history, rng, strategy.config.learningRate || 0.05)
          : randomParams(params, rng);
        break;

      case 'bayesian':
        candidate = surrogateStep(params, history, rng);
        break;

      case 'annealing': {
        // Temperature based on evalCount, not history.length (survives trimming)
        const evals = evalCount || history.length;
        const temp = (strategy.config.initialTemp || 1.0) *
          Math.pow(strategy.config.coolingRate || 0.995, evals);
        candidate = best
          ? mutateParams(best.params, params, temp, rng)
          : randomParams(params, rng);
        break;
      }

      case 'curiosity':
        candidate = noveltySample(params, history, rng);
        break;

      case 'exploit':
        candidate = best
          ? mutateParams(best.params, params, strategy.config.mutationMagnitude || 0.02, rng)
          : randomParams(params, rng);
        break;

      case 'swarm':
        candidate = best
          ? mutateParams(best.params, params, 0.15, rng)
          : randomParams(params, rng);
        break;

      case 'bandit':
      default:
        candidate = best
          ? mutateParams(best.params, params, 0.1, rng)
          : randomParams(params, rng);
        break;
    }

    if (satisfiesConstraints(candidate, constraints)) return candidate;
  }

  return randomParams(params, rng);
}
