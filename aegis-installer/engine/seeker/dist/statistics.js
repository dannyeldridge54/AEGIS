"use strict";
/**
 * Seeker — Statistical Engine
 * Bootstrap confidence intervals, Mann-Whitney U, Wilcoxon signed-rank,
 * Cohen's d effect size. Powers all model comparisons.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.ELORating = void 0;
exports.bootstrapCI = bootstrapCI;
exports.mannWhitneyU = mannWhitneyU;
exports.wilcoxonSignedRank = wilcoxonSignedRank;
exports.cohensD = cohensD;
// ─── Bootstrap Confidence Interval ───────────────────────────────────────────
/**
 * Compute bootstrap 95% CI for the mean.
 * Uses percentile method with 10,000 resamples.
 */
function bootstrapCI(data, nBoot = 10000, alpha = 0.05) {
    const n = data.length;
    if (n === 0)
        return { mean: NaN, lower: NaN, upper: NaN, std: 0, n: 0 };
    if (n === 1)
        return { mean: data[0], lower: data[0], upper: data[0], std: 0, n: 1 };
    const mean = data.reduce((a, b) => a + b, 0) / n;
    const std = Math.sqrt(data.reduce((a, b) => a + (b - mean) ** 2, 0) / (n - 1));
    const bootMeans = [];
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
    return {
        mean,
        lower: bootMeans[lo],
        upper: bootMeans[hi],
        std,
        n,
    };
}
// ─── Mann-Whitney U Test (non-parametric) ────────────────────────────────────
/**
 * Two-sample Mann-Whitney U test.
 * Tests whether one sample tends to have larger values than the other.
 * Uses normal approximation for n > 20.
 */
function mannWhitneyU(a, b) {
    const na = a.length, nb = b.length;
    if (na === 0 || nb === 0) {
        return { test: 'Mann-Whitney U', pValue: 1, effectSize: 0, significant: false, direction: 'no_difference' };
    }
    // Compute U statistic
    let u = 0;
    for (const ai of a) {
        for (const bi of b) {
            if (ai < bi)
                u++;
            else if (ai === bi)
                u += 0.5;
        }
    }
    const meanU = (na * nb) / 2;
    const stdU = Math.sqrt((na * nb * (na + nb + 1)) / 12);
    if (stdU === 0) {
        return { test: 'Mann-Whitney U', pValue: 1, effectSize: 0, significant: false, direction: 'no_difference' };
    }
    const z = (u - meanU) / stdU;
    const pValue = 2 * (1 - normalCDF(Math.abs(z)));
    // Rank-biserial correlation as effect size
    const effectSize = (2 * u) / (na * nb) - 1;
    let direction = 'no_difference';
    if (pValue < 0.05) {
        // Lower scores are better (minimization context)
        const meanA = a.reduce((s, v) => s + v, 0) / na;
        const meanB = b.reduce((s, v) => s + v, 0) / nb;
        direction = meanA < meanB ? 'a_better' : 'b_better';
    }
    return {
        test: 'Mann-Whitney U',
        pValue,
        effectSize: Math.abs(effectSize),
        significant: pValue < 0.05,
        direction,
    };
}
// ─── Wilcoxon Signed-Rank Test (paired) ──────────────────────────────────────
/**
 * Paired Wilcoxon signed-rank test.
 * For comparing two models on the same benchmarks (paired observations).
 */
function wilcoxonSignedRank(a, b) {
    const n = Math.min(a.length, b.length);
    if (n === 0) {
        return { test: 'Wilcoxon Signed-Rank', pValue: 1, effectSize: 0, significant: false, direction: 'no_difference' };
    }
    // Compute differences and their ranks
    const diffs = [];
    for (let i = 0; i < n; i++) {
        const diff = a[i] - b[i];
        if (diff !== 0)
            diffs.push({ diff, absDiff: Math.abs(diff) });
    }
    if (diffs.length === 0) {
        return { test: 'Wilcoxon Signed-Rank', pValue: 1, effectSize: 0, significant: false, direction: 'no_difference' };
    }
    // Rank by absolute difference
    diffs.sort((x, y) => x.absDiff - y.absDiff);
    const nr = diffs.length;
    let wPlus = 0, wMinus = 0;
    for (let i = 0; i < nr; i++) {
        const rank = i + 1;
        if (diffs[i].diff > 0)
            wPlus += rank;
        else
            wMinus += rank;
    }
    const w = Math.min(wPlus, wMinus);
    const meanW = nr * (nr + 1) / 4;
    const stdW = Math.sqrt(nr * (nr + 1) * (2 * nr + 1) / 24);
    if (stdW === 0) {
        return { test: 'Wilcoxon Signed-Rank', pValue: 1, effectSize: 0, significant: false, direction: 'no_difference' };
    }
    const z = (w - meanW) / stdW;
    const pValue = 2 * (1 - normalCDF(Math.abs(z)));
    // Effect size: r = z / sqrt(n)
    const effectSize = Math.abs(z) / Math.sqrt(nr);
    let direction = 'no_difference';
    if (pValue < 0.05) {
        direction = wPlus < wMinus ? 'a_better' : 'b_better';
    }
    return {
        test: 'Wilcoxon Signed-Rank',
        pValue,
        effectSize,
        significant: pValue < 0.05,
        direction,
    };
}
// ─── Cohen's d (effect size) ─────────────────────────────────────────────────
/**
 * Cohen's d: standardized mean difference.
 * |d| < 0.2 = negligible, 0.2-0.5 = small, 0.5-0.8 = medium, >0.8 = large
 */
function cohensD(a, b) {
    const na = a.length, nb = b.length;
    if (na < 2 || nb < 2)
        return 0;
    const meanA = a.reduce((s, v) => s + v, 0) / na;
    const meanB = b.reduce((s, v) => s + v, 0) / nb;
    const varA = a.reduce((s, v) => s + (v - meanA) ** 2, 0) / (na - 1);
    const varB = b.reduce((s, v) => s + (v - meanB) ** 2, 0) / (nb - 1);
    const pooledStd = Math.sqrt(((na - 1) * varA + (nb - 1) * varB) / (na + nb - 2));
    if (pooledStd === 0)
        return 0;
    return (meanA - meanB) / pooledStd;
}
// ─── ELO Rating ──────────────────────────────────────────────────────────────
class ELORating {
    constructor(k = 32, initialRating = 1500) {
        this.ratings = new Map();
        this.K = k;
        this.initialRating = initialRating;
    }
    register(id) {
        if (!this.ratings.has(id))
            this.ratings.set(id, this.initialRating);
    }
    /** Record a match result. scoreA: 1 = A wins, 0 = B wins, 0.5 = draw */
    recordMatch(idA, idB, scoreA) {
        this.register(idA);
        this.register(idB);
        const rA = this.ratings.get(idA);
        const rB = this.ratings.get(idB);
        const eA = 1 / (1 + Math.pow(10, (rB - rA) / 400));
        const eB = 1 - eA;
        this.ratings.set(idA, rA + this.K * (scoreA - eA));
        this.ratings.set(idB, rB + this.K * ((1 - scoreA) - eB));
    }
    getRating(id) {
        return this.ratings.get(id) || this.initialRating;
    }
    getLeaderboard() {
        return [...this.ratings.entries()]
            .map(([id, elo]) => ({ id, elo: Math.round(elo) }))
            .sort((a, b) => b.elo - a.elo);
    }
}
exports.ELORating = ELORating;
// ─── Helper: Normal CDF approximation ───────────────────────────────────────
function normalCDF(x) {
    const a1 = 0.254829592;
    const a2 = -0.284496736;
    const a3 = 1.421413741;
    const a4 = -1.453152027;
    const a5 = 1.061405429;
    const p = 0.3275911;
    const sign = x < 0 ? -1 : 1;
    x = Math.abs(x) / Math.sqrt(2);
    const t = 1.0 / (1.0 + p * x);
    const y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-x * x);
    return 0.5 * (1.0 + sign * y);
}
//# sourceMappingURL=statistics.js.map