"use strict";
/**
 * Seeker — Core Agent
 * Autonomous discovery engine. Every evaluation is tracked for UFE,
 * anomalies are detected in real-time, discoveries are recorded,
 * and the agent learns which strategies work via seeded-deterministic runs.
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.SeekerAgent = void 0;
exports.seeker = seeker;
exports.optimize = optimize;
const strategies_1 = require("./strategies");
const rng_1 = require("./rng");
const ufe_1 = require("./ufe");
const language_1 = require("./language");
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
// ─── Default Configuration ───────────────────────────────────────────────────
const DEFAULT_CONFIG = {
    goal: 'minimize',
    reportInterval: 10,
    maxEvals: 0,
    convergenceThreshold: 1e-8,
    explorationRate: 0.3,
    strategies: ['random', 'evolutionary', 'gradient', 'annealing', 'curiosity', 'exploit'],
    verbosity: 'normal',
    persistence: { enabled: false, path: './seeker-state.json', interval: 60 },
    language: 'en',
    seed: 0, // 0 = random seed
    noveltyResolution: 20,
};
// ─── Seeker Agent ────────────────────────────────────────────────────────────
class SeekerAgent {
    constructor(task, config) {
        this.handlers = [];
        this.running = false;
        this.startTime = 0;
        this.lastReportTime = 0;
        this.lastBestTime = 0;
        this.gridIndex = 0;
        this.task = task;
        this.config = { ...DEFAULT_CONFIG, ...config };
        this.msg = (0, language_1.getMessages)(this.config.language);
        // Seeded RNG — deterministic if seed provided
        this.rng = new rng_1.SeededRNG(this.config.seed || undefined);
        this.metaLearner = new strategies_1.MetaLearner(this.config.strategies, this.config.explorationRate, this.rng.fork());
        const minimize = this.isMinimizing();
        this.ufeTracker = new ufe_1.UFETracker(this.task.parameters, minimize, this.config.noveltyResolution);
        this.anomalyDetector = new ufe_1.AnomalyDetector(50);
        this.state = {
            best: null,
            totalEvals: 0,
            history: [],
            strategies: this.metaLearner.getStrategies(),
            discoveries: [],
            runtime: 0,
            phase: 'exploring',
            ufe: {
                totalEvals: 0, usefulEvals: 0, ufeRatio: 0,
                convergenceVelocity: 0, aucc: 0,
                timeToTarget: { pct10: null, pct50: null, pct90: null },
                convergenceCurve: [],
            },
        };
    }
    // ─── Public API ──────────────────────────────────────────────────────────
    on(handler) {
        this.handlers.push(handler);
        return this;
    }
    /** Seed the agent with a known-good starting point (e.g. from another engine) */
    seed(params, score) {
        if (!isFinite(score))
            return this;
        const result = {
            params,
            score,
            timestamp: Date.now(),
            strategy: 'exploit',
        };
        this.state.best = result;
        this.state.history.push(result);
        return this;
    }
    async run(optimum) {
        this.running = true;
        this.startTime = Date.now();
        this.lastReportTime = this.startTime;
        this.lastBestTime = this.startTime;
        this.emit({ type: 'started', config: this.config });
        this.log(`${this.msg.started} (seed=${this.rng.seed})`);
        this.log(`  Task: ${this.task.name} (${this.task.parameters.length} params)`);
        while (this.running) {
            await this.step();
            if (this.config.maxEvals > 0 && this.state.totalEvals >= this.config.maxEvals) {
                this.stop('Max evaluations reached');
                break;
            }
            if (this.checkConvergence()) {
                this.emit({ type: 'converged', result: this.state.best, totalEvals: this.state.totalEvals });
                this.log(`${this.msg.converged} ${this.state.totalEvals} ${this.msg.evalCount}, ${this.msg.bestScore}: ${this.state.best.score.toFixed(6)}`);
                this.running = false;
                break;
            }
            const now = Date.now();
            if (this.config.reportInterval > 0 && (now - this.lastReportTime) / 1000 >= this.config.reportInterval) {
                this.report();
                this.lastReportTime = now;
            }
        }
        this.state.runtime = (Date.now() - this.startTime) / 1000;
        this.state.strategies = this.metaLearner.getStrategies();
        this.state.ufe = this.ufeTracker.getMetrics(optimum);
        if (this.config.persistence.enabled)
            this.saveState();
        return this.state;
    }
    async step() {
        const strategy = this.metaLearner.selectStrategy();
        const params = (0, strategies_1.generateNextPoint)(strategy, this.task.parameters, this.state.best, this.state.history, this.rng, this.task.constraints, this.state.totalEvals, this.gridIndex++);
        const score = await this.task.evaluate(params);
        const result = {
            params, score,
            timestamp: Date.now(),
            strategy: strategy.type,
        };
        this.state.totalEvals++;
        this.state.history.push(result);
        // Keep working history bounded but preserve convergence data in UFETracker
        if (this.state.history.length > 5000) {
            this.state.history = this.state.history.slice(-2500);
        }
        // ── UFE tracking ──
        const ufeResult = this.ufeTracker.record(result);
        // ── Anomaly detection ──
        const anomaly = this.anomalyDetector.check(score);
        if (anomaly) {
            anomaly.result = result;
            this.state.discoveries.push(anomaly);
            this.emit({ type: 'discovery', discovery: anomaly });
        }
        // Check for plateau/shift every 100 evals
        if (this.state.totalEvals % 100 === 0) {
            const plateau = this.anomalyDetector.checkPlateau();
            if (plateau) {
                plateau.result = result;
                this.state.discoveries.push(plateau);
                this.emit({ type: 'discovery', discovery: plateau });
            }
            const shift = this.anomalyDetector.checkShift();
            if (shift) {
                shift.result = result;
                this.state.discoveries.push(shift);
                this.emit({ type: 'discovery', discovery: shift });
            }
        }
        // ── Track improvement ──
        const minimize = this.isMinimizing();
        const previousBest = this.state.best?.score ?? (minimize ? Infinity : -Infinity);
        const isBetter = minimize ? score < previousBest : score > previousBest;
        const improvement = minimize ? (previousBest - score) : (score - previousBest);
        if (!this.state.best || isBetter) {
            this.state.best = result;
            this.lastBestTime = Date.now();
            const reward = this.state.totalEvals === 1
                ? 1.0
                : Math.min(Math.max(improvement, 0.001), 100);
            this.metaLearner.updateStrategy(strategy.type, reward);
            this.emit({ type: 'new_best', result, improvement: Math.max(improvement, 0) });
            if (this.config.verbosity !== 'silent') {
                this.log(`${this.msg.newBest} score=${score.toFixed(6)} (${this.msg.improvement}: ${improvement.toFixed(6)}) [${strategy.type}]`);
            }
            // Major discovery
            if (this.state.totalEvals > 1 && Math.abs(improvement) > Math.abs(previousBest) * 0.05) {
                const discovery = {
                    type: 'new_best',
                    description: `Major improvement: ${previousBest.toFixed(4)} → ${score.toFixed(4)} via ${strategy.type}`,
                    result, confidence: Math.min(Math.abs(improvement) / (Math.abs(previousBest) || 1), 1),
                    timestamp: Date.now(),
                };
                this.state.discoveries.push(discovery);
                this.emit({ type: 'discovery', discovery });
            }
        }
        else {
            this.metaLearner.updateStrategy(strategy.type, 0);
        }
        this.updatePhase();
        this.emit({ type: 'evaluation', result });
        return result;
    }
    stop(reason = 'User requested') {
        this.running = false;
        this.state.runtime = (Date.now() - this.startTime) / 1000;
        this.state.ufe = this.ufeTracker.getMetrics();
        this.emit({ type: 'stopped', reason, state: this.state });
        this.log(`${this.msg.stopped} ${reason}`);
    }
    getState() {
        return {
            ...this.state,
            runtime: (Date.now() - this.startTime) / 1000,
            ufe: this.ufeTracker.getMetrics(),
        };
    }
    getSeed() { return this.rng.seed; }
    setLanguage(lang) {
        this.config.language = lang;
        this.msg = (0, language_1.getMessages)(lang);
    }
    // ─── Internal ────────────────────────────────────────────────────────────
    isMinimizing() {
        const goal = this.config.goal;
        if (!goal)
            return true;
        if (typeof goal === 'string') {
            return !/(maximize|maximise|highest|largest|most|best score)/i.test(goal);
        }
        return goal.minimize !== false;
    }
    updatePhase() {
        const timeSinceBest = (Date.now() - this.lastBestTime) / 1000;
        const oldPhase = this.state.phase;
        if (this.state.totalEvals < 100) {
            this.state.phase = 'exploring';
        }
        else if (timeSinceBest > 30) {
            this.state.phase = 'curious';
        }
        else if (timeSinceBest < 5) {
            this.state.phase = 'exploiting';
        }
        if (oldPhase !== this.state.phase) {
            this.emit({ type: 'phase_change', from: oldPhase, to: this.state.phase });
            if (this.config.verbosity === 'verbose') {
                this.log(`${this.msg.phaseChange} ${oldPhase} → ${this.state.phase}`);
            }
        }
    }
    checkConvergence() {
        if (this.state.totalEvals < 200 || !this.state.best)
            return false;
        const recentWindow = this.state.history.slice(-500);
        if (recentWindow.length < 500)
            return false;
        const minimize = this.isMinimizing();
        const bestFn = minimize ? Math.min : Math.max;
        const recentBest = bestFn(...recentWindow.map(r => r.score));
        const olderSlice = this.state.history.slice(-1000, -500);
        if (olderSlice.length === 0)
            return false;
        const olderBest = bestFn(...olderSlice.map(r => r.score));
        return Math.abs(recentBest - olderBest) < this.config.convergenceThreshold;
    }
    report() {
        const elapsed = (0, language_1.formatDuration)((Date.now() - this.startTime) / 1000);
        const best = this.state.best?.score.toFixed(6) ?? 'N/A';
        const strategies = this.metaLearner.getStrategies();
        const topStrategy = strategies[0];
        const ufe = this.ufeTracker.getMetrics();
        this.log(`${this.msg.progress} ${this.state.totalEvals} ${this.msg.evalCount} | ${this.msg.bestScore}: ${best} | UFE: ${(ufe.ufeRatio * 100).toFixed(1)}% | ${this.msg.timeElapsed}: ${elapsed} | Top: ${topStrategy.type}`);
        this.emit({ type: 'report', state: this.getState() });
    }
    saveState() {
        const statePath = this.config.persistence.path || './seeker-state.json';
        const dir = path.dirname(statePath);
        if (!fs.existsSync(dir))
            fs.mkdirSync(dir, { recursive: true });
        fs.writeFileSync(statePath, JSON.stringify(this.getState(), null, 2));
    }
    emit(event) {
        for (const handler of this.handlers) {
            try {
                handler(event);
            }
            catch { /* ignore handler errors */ }
        }
    }
    log(msg) {
        if (this.config.verbosity === 'silent')
            return;
        console.log(msg);
    }
}
exports.SeekerAgent = SeekerAgent;
// ─── Quick-Start Factories ───────────────────────────────────────────────────
function seeker(task, config) {
    return new SeekerAgent(task, config);
}
async function optimize(fn, parameters, config) {
    const agent = new SeekerAgent({
        id: 'quick-optimize',
        name: 'Quick Optimization',
        evaluate: fn,
        parameters,
    }, { maxEvals: config?.maxEvals || 5000, verbosity: 'minimal', ...config });
    const state = await agent.run();
    return state.best;
}
//# sourceMappingURL=agent.js.map