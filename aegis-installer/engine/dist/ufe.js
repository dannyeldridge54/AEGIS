"use strict";
/**
 * AEGIS — UFE Tracker & Anomaly Detector
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Tracks Useful Function Evaluations, convergence curves, anomalies,
 * and discovery events. The recording backbone of every AEGIS run.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.AnomalyDetector = exports.UFETracker = void 0;
class UFETracker {
    constructor(params, minimize = true, resolution = 20) {
        this.params = params;
        this.usefulCount = 0;
        this.totalCount = 0;
        this.curve = [];
        this.initialScore = null;
        this.totalImprovement = 0;
        this.noveltyGrid = new Map();
        this.minimize = minimize;
        this.bestSoFar = minimize ? Infinity : -Infinity;
        this.resolution = resolution;
    }
    /** Record an evaluation and determine if it was useful */
    record(result) {
        this.totalCount++;
        const improved = this.minimize
            ? result.score < this.bestSoFar
            : result.score > this.bestSoFar;
        if (this.initialScore === null)
            this.initialScore = result.score;
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
        if (useful)
            this.usefulCount++;
        // Record convergence point
        this.curve.push([this.totalCount, this.bestSoFar]);
        return { useful, novelRegion, improved };
    }
    /** Compute full UFE metrics snapshot */
    getMetrics(optimum) {
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
    computeAUCC() {
        if (this.curve.length < 2)
            return 1;
        const n = this.totalCount;
        let area = 0;
        for (let i = 1; i < this.curve.length; i++) {
            const [x0, y0] = this.curve[i - 1];
            const [x1, y1] = this.curve[i];
            area += ((x1 - x0) / n) * ((y0 + y1) / 2);
        }
        const scores = this.curve.map(c => c[1]);
        const sMin = Math.min(...scores);
        const sMax = Math.max(...scores);
        const range = sMax - sMin || 1;
        return area / range;
    }
    computeTimeToTarget(optimum) {
        if (optimum === undefined || this.initialScore === null) {
            return { pct10: null, pct50: null, pct90: null };
        }
        const initialGap = Math.abs(this.initialScore - optimum);
        if (initialGap < 1e-12)
            return { pct10: 0, pct50: 0, pct90: 0 };
        const targets = {
            pct10: optimum + (this.minimize ? 1 : -1) * initialGap * 0.9,
            pct50: optimum + (this.minimize ? 1 : -1) * initialGap * 0.5,
            pct90: optimum + (this.minimize ? 1 : -1) * initialGap * 0.1,
        };
        const result = { pct10: null, pct50: null, pct90: null };
        for (const [evalIdx, bestScore] of this.curve) {
            if (result.pct10 === null && (this.minimize ? bestScore <= targets.pct10 : bestScore >= targets.pct10))
                result.pct10 = evalIdx;
            if (result.pct50 === null && (this.minimize ? bestScore <= targets.pct50 : bestScore >= targets.pct50))
                result.pct50 = evalIdx;
            if (result.pct90 === null && (this.minimize ? bestScore <= targets.pct90 : bestScore >= targets.pct90))
                result.pct90 = evalIdx;
        }
        return result;
    }
    toBinKey(params) {
        return this.params.map(p => {
            const range = p.max - p.min || 1;
            const normalized = (params[p.name] - p.min) / range;
            return Math.floor(Math.min(normalized, 0.9999) * this.resolution);
        }).join(',');
    }
    get regionsExplored() { return this.noveltyGrid.size; }
    get totalRegions() { return Math.pow(this.resolution, this.params.length); }
    get coverageRatio() { return this.regionsExplored / this.totalRegions; }
}
exports.UFETracker = UFETracker;
// ─── Anomaly Detector ────────────────────────────────────────────────────────
class AnomalyDetector {
    constructor(windowSize = 50) {
        this.scores = [];
        this.windowSize = windowSize;
    }
    /** Check if a score is anomalous (>3σ from rolling mean) */
    check(score) {
        this.scores.push(score);
        if (this.scores.length < this.windowSize)
            return null;
        const window = this.scores.slice(-this.windowSize);
        const mean = window.reduce((a, b) => a + b, 0) / window.length;
        const variance = window.reduce((a, b) => a + (b - mean) ** 2, 0) / window.length;
        const stddev = Math.sqrt(variance);
        if (stddev < 1e-12)
            return null;
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
    checkPlateau() {
        if (this.scores.length < this.windowSize * 2)
            return null;
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
    checkShift() {
        if (this.scores.length < this.windowSize * 2)
            return null;
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
    variance(arr) {
        const mean = arr.reduce((a, b) => a + b, 0) / arr.length;
        return arr.reduce((a, b) => a + (b - mean) ** 2, 0) / arr.length;
    }
}
exports.AnomalyDetector = AnomalyDetector;
//# sourceMappingURL=ufe.js.map