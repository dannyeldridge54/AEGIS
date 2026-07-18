/**
 * AEGIS — Statistical Engine
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Bootstrap confidence intervals, Mann-Whitney U, Wilcoxon signed-rank,
 * Cohen's d effect size, ELO rating. Powers all model comparisons.
 */

export interface CIResult {
  mean: number;
  lower: number;
  upper: number;
  std: number;
  n: number;
}

export interface TestResult {
  test: string;
  pValue: number;
  effectSize: number;
  significant: boolean;
  direction: 'a_better' | 'b_better' | 'no_difference';
}

// ─── Bootstrap Confidence Interval ───────────────────────────────────────────

export function bootstrapCI(data: number[], nBoot: number = 10000, alpha: number = 0.05): CIResult {
  const n = data.length;
  if (n === 0) return { mean: NaN, lower: NaN, upper: NaN, std: 0, n: 0 };
  if (n === 1) return { mean: data[0], lower: data[0], upper: data[0], std: 0, n: 1 };

  const mean = data.reduce((a, b) => a + b, 0) / n;
  const std = Math.sqrt(data.reduce((a, b) => a + (b - mean) ** 2, 0) / (n - 1));

  const bootMeans: number[] = [];
  for (let b = 0; b < nBoot; b++) {
    let sum = 0;
    for (let i = 0; i < n; i++) {
      sum += data[Math.floor(Math.random() * n)];
    }
    bootMeans.push(sum / n);
  }

  bootMeans.sort((a, b) => a - b);
  const lo = Math.floor(bootMeans.length * (alpha / 2));
  const hi = Math.floor(bootMeans.length * (1 - alpha / 2));

  return { mean, lower: bootMeans[lo], upper: bootMeans[hi], std, n };
}

// ─── Mann-Whitney U Test ─────────────────────────────────────────────────────

export function mannWhitneyU(a: number[], b: number[]): TestResult {
  const na = a.length, nb = b.length;
  if (na === 0 || nb === 0) {
    return { test: 'Mann-Whitney U', pValue: 1, effectSize: 0, significant: false, direction: 'no_difference' };
  }

  let u = 0;
  for (const ai of a) {
    for (const bi of b) {
      if (ai < bi) u++;
      else if (ai === bi) u += 0.5;
    }
  }

  const meanU = (na * nb) / 2;
  const stdU = Math.sqrt((na * nb * (na + nb + 1)) / 12);
  if (stdU === 0) {
    return { test: 'Mann-Whitney U', pValue: 1, effectSize: 0, significant: false, direction: 'no_difference' };
  }

  const z = (u - meanU) / stdU;
  const pValue = 2 * (1 - normalCDF(Math.abs(z)));
  const effectSize = (2 * u) / (na * nb) - 1;

  let direction: TestResult['direction'] = 'no_difference';
  if (pValue < 0.05) {
    const meanA = a.reduce((s, v) => s + v, 0) / na;
    const meanB = b.reduce((s, v) => s + v, 0) / nb;
    direction = meanA < meanB ? 'a_better' : 'b_better';
  }

  return { test: 'Mann-Whitney U', pValue, effectSize: Math.abs(effectSize), significant: pValue < 0.05, direction };
}

// ─── Wilcoxon Signed-Rank Test ───────────────────────────────────────────────

export function wilcoxonSignedRank(a: number[], b: number[]): TestResult {
  const n = Math.min(a.length, b.length);
  if (n === 0) {
    return { test: 'Wilcoxon Signed-Rank', pValue: 1, effectSize: 0, significant: false, direction: 'no_difference' };
  }

  const diffs: Array<{ diff: number; absDiff: number }> = [];
  for (let i = 0; i < n; i++) {
    const diff = a[i] - b[i];
    if (diff !== 0) diffs.push({ diff, absDiff: Math.abs(diff) });
  }

  if (diffs.length === 0) {
    return { test: 'Wilcoxon Signed-Rank', pValue: 1, effectSize: 0, significant: false, direction: 'no_difference' };
  }

  diffs.sort((x, y) => x.absDiff - y.absDiff);
  const nr = diffs.length;
  let wPlus = 0, wMinus = 0;
  for (let i = 0; i < nr; i++) {
    const rank = i + 1;
    if (diffs[i].diff > 0) wPlus += rank;
    else wMinus += rank;
  }

  const w = Math.min(wPlus, wMinus);
  const meanW = nr * (nr + 1) / 4;
  const stdW = Math.sqrt(nr * (nr + 1) * (2 * nr + 1) / 24);
  if (stdW === 0) {
    return { test: 'Wilcoxon Signed-Rank', pValue: 1, effectSize: 0, significant: false, direction: 'no_difference' };
  }

  const z = (w - meanW) / stdW;
  const pValue = 2 * (1 - normalCDF(Math.abs(z)));
  const effectSize = Math.abs(z) / Math.sqrt(nr);

  let direction: TestResult['direction'] = 'no_difference';
  if (pValue < 0.05) {
    direction = wPlus < wMinus ? 'a_better' : 'b_better';
  }

  return { test: 'Wilcoxon Signed-Rank', pValue, effectSize, significant: pValue < 0.05, direction };
}

// ─── Cohen's d ───────────────────────────────────────────────────────────────

export function cohensD(a: number[], b: number[]): number {
  const na = a.length, nb = b.length;
  if (na < 2 || nb < 2) return 0;
  const meanA = a.reduce((s, v) => s + v, 0) / na;
  const meanB = b.reduce((s, v) => s + v, 0) / nb;
  const varA = a.reduce((s, v) => s + (v - meanA) ** 2, 0) / (na - 1);
  const varB = b.reduce((s, v) => s + (v - meanB) ** 2, 0) / (nb - 1);
  const pooledStd = Math.sqrt(((na - 1) * varA + (nb - 1) * varB) / (na + nb - 2));
  if (pooledStd === 0) return 0;
  return (meanA - meanB) / pooledStd;
}

// ─── ELO Rating ──────────────────────────────────────────────────────────────

export class ELORating {
  private ratings: Map<string, number> = new Map();
  private readonly K: number;
  private initialRating: number;

  constructor(k: number = 32, initialRating: number = 1500) {
    this.K = k;
    this.initialRating = initialRating;
  }

  register(id: string): void {
    if (!this.ratings.has(id)) this.ratings.set(id, this.initialRating);
  }

  recordMatch(idA: string, idB: string, scoreA: number): void {
    this.register(idA);
    this.register(idB);
    const rA = this.ratings.get(idA)!;
    const rB = this.ratings.get(idB)!;
    const eA = 1 / (1 + Math.pow(10, (rB - rA) / 400));
    const eB = 1 - eA;
    this.ratings.set(idA, rA + this.K * (scoreA - eA));
    this.ratings.set(idB, rB + this.K * ((1 - scoreA) - eB));
  }

  getRating(id: string): number {
    return this.ratings.get(id) || this.initialRating;
  }

  getLeaderboard(): Array<{ id: string; elo: number }> {
    return [...this.ratings.entries()]
      .map(([id, elo]) => ({ id, elo: Math.round(elo) }))
      .sort((a, b) => b.elo - a.elo);
  }
}

// ─── Helper ──────────────────────────────────────────────────────────────────

function normalCDF(x: number): number {
  const a1 = 0.254829592, a2 = -0.284496736, a3 = 1.421413741;
  const a4 = -1.453152027, a5 = 1.061405429, p = 0.3275911;
  const sign = x < 0 ? -1 : 1;
  x = Math.abs(x) / Math.sqrt(2);
  const t = 1.0 / (1.0 + p * x);
  const y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-x * x);
  return 0.5 * (1.0 + sign * y);
}
