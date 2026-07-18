"use strict";
/**
 * Seeker — Data Recorder
 * Scripts every evaluation to disk. CSV + JSON logs.
 * Export convergence curves, discovery logs, strategy stats.
 * The black box flight recorder for optimization runs.
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
exports.DataRecorder = void 0;
exports.createRecorder = createRecorder;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
class DataRecorder {
    constructor(config) {
        this.evalBuffer = [];
        this.discoveryBuffer = [];
        this.evalCount = 0;
        this.csvStream = null;
        this.discoveryStream = null;
        this.paramNames = [];
        this.initialized = false;
        this.config = {
            dir: config.dir,
            runId: config.runId,
            logEvals: config.logEvals !== false,
            logDiscoveries: config.logDiscoveries !== false,
            logStrategies: config.logStrategies !== false,
            flushInterval: config.flushInterval || 100,
        };
        if (!fs.existsSync(this.config.dir)) {
            fs.mkdirSync(this.config.dir, { recursive: true });
        }
    }
    /** Initialize with parameter names (call before recording) */
    init(paramNames) {
        this.paramNames = paramNames;
        this.initialized = true;
        if (this.config.logEvals) {
            const csvPath = path.join(this.config.dir, `${this.config.runId}-evals.csv`);
            this.csvStream = fs.createWriteStream(csvPath, { flags: 'w' });
            const header = ['eval_num', 'score', 'strategy', 'timestamp', 'useful', ...paramNames].join(',');
            this.csvStream.write(header + '\n');
        }
        if (this.config.logDiscoveries) {
            const discPath = path.join(this.config.dir, `${this.config.runId}-discoveries.jsonl`);
            this.discoveryStream = fs.createWriteStream(discPath, { flags: 'w' });
        }
    }
    /** Record a single evaluation */
    recordEval(result, useful) {
        this.evalCount++;
        if (!this.initialized || !this.csvStream)
            return;
        const paramValues = this.paramNames.map(n => result.params[n]?.toFixed(8) || '0');
        const line = [
            this.evalCount,
            result.score.toFixed(10),
            result.strategy,
            result.timestamp,
            useful ? 1 : 0,
            ...paramValues,
        ].join(',');
        this.csvStream.write(line + '\n');
    }
    /** Record a discovery */
    recordDiscovery(discovery) {
        if (!this.discoveryStream)
            return;
        this.discoveryStream.write(JSON.stringify({
            eval: this.evalCount,
            type: discovery.type,
            description: discovery.description,
            confidence: discovery.confidence,
            score: discovery.result.score,
            timestamp: discovery.timestamp,
        }) + '\n');
    }
    /** Write strategy performance snapshot */
    recordStrategies(strategies) {
        if (!this.config.logStrategies)
            return;
        const stratPath = path.join(this.config.dir, `${this.config.runId}-strategies.json`);
        const data = strategies.map(s => ({
            type: s.type,
            uses: s.uses,
            score: s.score,
            avgImprovement: s.avgImprovement,
        }));
        fs.writeFileSync(stratPath, JSON.stringify(data, null, 2));
    }
    /** Write final run summary */
    writeSummary(state) {
        const summaryPath = path.join(this.config.dir, `${this.config.runId}-summary.json`);
        fs.writeFileSync(summaryPath, JSON.stringify({
            runId: this.config.runId,
            totalEvals: state.totalEvals,
            bestScore: state.best?.score,
            bestParams: state.best?.params,
            bestStrategy: state.best?.strategy,
            runtime: state.runtime,
            phase: state.phase,
            discoveries: state.discoveries.length,
            ufe: state.ufe,
            strategies: state.strategies.map(s => ({
                type: s.type, uses: s.uses, score: s.score, avgImprovement: s.avgImprovement,
            })),
        }, null, 2));
    }
    /** Export convergence curve as CSV */
    exportConvergenceCurve(ufe) {
        const curvePath = path.join(this.config.dir, `${this.config.runId}-convergence.csv`);
        const lines = ['eval,best_score'];
        for (const [evalIdx, score] of ufe.convergenceCurve) {
            lines.push(`${evalIdx},${score.toFixed(10)}`);
        }
        fs.writeFileSync(curvePath, lines.join('\n'));
    }
    /** Create an event handler for plugging into agent.on() */
    createHandler() {
        return (event) => {
            if (event.type === 'evaluation') {
                // We need the 'useful' flag from the UFE tracker — recorded externally
            }
            if (event.type === 'discovery') {
                this.recordDiscovery(event.discovery);
            }
            if (event.type === 'report') {
                this.recordStrategies(event.state.strategies);
            }
            if (event.type === 'stopped' || event.type === 'converged') {
                const state = event.state || event;
                if (state.strategies)
                    this.recordStrategies(state.strategies);
            }
        };
    }
    /** Close all streams */
    close() {
        this.csvStream?.end();
        this.discoveryStream?.end();
    }
}
exports.DataRecorder = DataRecorder;
/**
 * Quick factory: create a recorder and wire it to an agent.
 *
 * @example
 * const rec = createRecorder('my-run', './data');
 * rec.init(task.parameters.map(p => p.name));
 * agent.on(rec.createHandler());
 */
function createRecorder(runId, dir = './seeker-data') {
    return new DataRecorder({ runId, dir });
}
//# sourceMappingURL=recorder.js.map