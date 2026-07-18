/**
 * Seeker — UFE Tracker
 * Tracks Useful Function Evaluations, convergence curves, anomalies,
 * and discovery events. The recording backbone of every Seeker run.
 */

import { UFEMetrics, EvalResult, Discovery, ParameterDef } from './interfaces';
import { SeededRNG } from './rng';

export class UFETracker {
  private bestSoFar: number;
  private usefulCount = 0;
  private totalCount = 0;
  private curve: Array<[number, number]> = [];
  private initialScore: number | null = null;
  private totalImprovement = 0;
  private noveltyGrid: Map<string, number> = new Map();
  private readonly resolution: number;
  private readonly minimize: boolean;

  constructor(
    private params: ParameterDef[],
    minimize: boolean = true,
    resolution: number = 20,
  ) {
    this.minimize = minimize;
    this.bestSoFar = minimize ? Infinity : -Infinity;
    this.resolution = resolution;
  }

  /** Record an evaluation and determine if it was useful */
  record(result: EvalResult): { useful: boolean; novelRegion: boolean; improved: boolean } {
    this.totalCount++;
    const improved = this.minimize
      ? result.score < this.bestSoFar
      : result.score > this.bestSoFar;

    if (this.initialScore === null) this.initialScore = result.score;

    if (improved) {
      const delta = Math.abs(this.bestSoFar === Infinity || this.bestSoFar === -Infinity
        ? result.score
        : this.bestSoFar - result.score);
      this.totalImprovement += delta;
      this.bestSoFar = result.score;
    }

    // Novelty check: discretize param space and check if this bin is new
    const binKey = this.toBinKey(result.params);
    const visits = this.noveltyGrid.get(binKey) || 0;
    const novelRegion = visits === 0;
    this.noveltyGrid.set(binKey, visits + 1);

    const useful = improved || novelRegion;
    if (useful) this.usefulCount++;

    // Record convergence point
    this.curve.push([this.totalCount, this.bestSoFar]);

    return { useful, novelRegion, improved };
  }

  /** Compute full UFE metrics snapshot */
  getMetrics(optimum?: number): UFEMetrics {
    const ufeRatio = this.totalCount > 0 ? this.usefulCount / this.totalCount : 0;
    const velocity = this.usefulCount > 0 ? this.totalImprovement / this.usefulCount : 0;

    return {
      totalEvals: this.totalCount,
      usefulEvals: this.usefulCount,
      ufeRatio,
      convergenceVelocity: velocity,
      aucc: this.computeAUCC(),
      timeToTarget: this.computeTimeToTarget(optimum),
      convergenceCurve: [...this.curve],
    };
  }

  /** Area Under Convergence Curve — normalized to [0,1] budget range */
  private computeAUCC(): number {
    if (this.curve.length < 2) return 1;

    const n = this.totalCount;
    let area = 0;
    for (let i = 1; i < this.curve.length; i++) {
      const [x0, y0] = this.curve[i - 1];
      const [x1, y1] = this.curve[i];
      // Trapezoidal rule
      area += ((x1 - x0) / n) * ((y0 + y1) / 2);
    }

    // Normalize by score range
    const scores = this.curve.map(c => c[1]);
    const sMin = Math.min(...scores);
    const sMax = Math.max(...scores);
    const range = sMax - sMin || 1;

    return area / range;
  }

  /** Time-to-target: evals needed to close 10/50/90% of initial gap */
  private computeTimeToTarget(optimum?: number): UFEMetrics['timeToTarget'] {
    if (optimum === undefined || this.initialScore === null) {
      return { pct10: null, pct50: null, pct90: null };
    }

    const initialGap = Math.abs(this.initialScore - optimum);
    if (initialGap < 1e-12) return { pct10: 0, pct50: 0, pct90: 0 };

    const targets = {
      pct10: optimum + (this.minimize ? 1 : -1) * initialGap * 0.9,
      pct50: optimum + (this.minimize ? 1 : -1) * initialGap * 0.5,
      pct90: optimum + (this.minimize ? 1 : -1) * initialGap * 0.1,
    };

    const result: UFEMetrics['timeToTarget'] = { pct10: null, pct50: null, pct90: null };
    for (const [evalIdx, bestScore] of this.curve) {
      const reached = this.minimize ? bestScore <= targets.pct10 : bestScore >= targets.pct10;
      if (reached && result.pct10 === null) result.pct10 = evalIdx;

      const reached50 = this.minimize ? bestScore <= targets.pct50 : bestScore >= targets.pct50;
      if (reached50 && result.pct50 === null) result.pct50 = evalIdx;

      const reached90 = this.minimize ? bestScore <= targets.pct90 : bestScore >= targets.pct90;
      if (reached90 && result.pct90 === null) result.pct90 = evalIdx;
    }

    return result;
  }

  private toBinKey(params: Record<string, number>): string {
    return this.params.map(p => {
      const range = p.max - p.min || 1;
      const normalized = (params[p.name] - p.min) / range;
      return Math.floor(Math.min(normalized, 0.9999) * this.resolution);
    }).join(',');
  }

  /** How many unique regions have been explored */
  get regionsExplored(): number { return this.noveltyGrid.size; }
  get totalRegions(): number { return Math.pow(this.resolution, this.params.length); }
  get coverageRatio(): number { return this.regionsExplored / this.totalRegions; }
}

// ─── Anomaly Detector ────────────────────────────────────────────────────────

export class AnomalyDetector {
  private scores: number[] = [];
  private windowSize: number;

  constructor(windowSize: number = 50) {
    this.windowSize = windowSize;
  }

  /** Check if a score is anomalous (>3σ from rolling mean) */
  check(score: number): Discovery | null {
    this.scores.push(score);
    if (this.scores.length < this.windowSize) return null;

    const window = this.scores.slice(-this.windowSize);
    const mean = window.reduce((a, b) => a + b, 0) / window.length;
    const variance = window.reduce((a, b) => a + (b - mean) ** 2, 0) / window.length;
    const stddev = Math.sqrt(variance);

    if (stddev < 1e-12) return null;
    const zScore = Math.abs(score - mean) / stddev;

    if (zScore > 3) {
      return {
        type: 'anomaly',
        description: `Anomalous score ${score.toFixed(6)} (z=${zScore.toFixed(1)}σ from rolling mean ${mean.toFixed(6)})`,
        result: { params: {}, score, timestamp: Date.now(), strategy: 'random' },
        confidence: Math.min(1, zScore / 5),
        timestamp: Date.now(),
      };
    }

    return null;
  }

  /** Detect plateau (variance collapsed) */
  checkPlateau(): Discovery | null {
    if (this.scores.length < this.windowSize * 2) return null;

    const recent = this.scores.slice(-this.windowSize);
    const older = this.scores.slice(-this.windowSize * 2, -this.windowSize);

    const recentVar = this.variance(recent);
    const olderVar = this.variance(older);

    if (recentVar < 1e-10 && olderVar > 1e-8) {
      return {
        type: 'plateau',
        description: `Plateau detected: variance collapsed from ${olderVar.toExponential(2)} to ${recentVar.toExponential(2)}`,
        result: { params: {}, score: recent[recent.length - 1], timestamp: Date.now(), strategy: 'random' },
        confidence: 0.8,
        timestamp: Date.now(),
      };
    }

    return null;
  }

  /** Detect landscape shift (distribution of scores changed) */
  checkShift(): Discovery | null {
    if (this.scores.length < this.windowSize * 2) return null;

    const recent = this.scores.slice(-this.windowSize);
    const older = this.scores.slice(-this.windowSize * 2, -this.windowSize);

    const recentMean = recent.reduce((a, b) => a + b, 0) / recent.length;
    const olderMean = older.reduce((a, b) => a + b, 0) / older.length;
    const pooledStd = Math.sqrt((this.variance(recent) + this.variance(older)) / 2) || 1;
    const d = Math.abs(recentMean - olderMean) / pooledStd;

    if (d > 1.5) {
      return {
        type: 'landscape_shift',
        description: `Landscape shift: mean moved from ${olderMean.toFixed(4)} to ${recentMean.toFixed(4)} (d=${d.toFixed(2)})`,
        result: { params: {}, score: recentMean, timestamp: Date.now(), strategy: 'random' },
        confidence: Math.min(1, d / 3),
        timestamp: Date.now(),
      };
    }

    return null;
  }

  private variance(arr: number[]): number {
    const mean = arr.reduce((a, b) => a + b, 0) / arr.length;
    return arr.reduce((a, b) => a + (b - mean) ** 2, 0) / arr.length;
  }
}
