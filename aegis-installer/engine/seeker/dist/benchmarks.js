"use strict";
/**
 * Seeker — Benchmark Suite
 * Standard test functions + UFE-aware benchmarking with known optima.
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
exports.benchmarkFunctions = void 0;
exports.runBenchmarks = runBenchmarks;
// ─── Standard Test Functions ─────────────────────────────────────────────────
exports.benchmarkFunctions = {
    rosenbrock: {
        id: 'rosenbrock', name: 'Rosenbrock 2D',
        evaluate: (p) => Math.pow(1 - p.x, 2) + 100 * Math.pow(p.y - p.x * p.x, 2),
        parameters: [{ name: 'x', min: -5, max: 5 }, { name: 'y', min: -5, max: 5 }],
        optimum: 0, optimumParams: { x: 1, y: 1 },
    },
    rastrigin: {
        id: 'rastrigin', name: 'Rastrigin 2D',
        evaluate: (p) => {
            const A = 10;
            return A * 2 + (p.x * p.x - A * Math.cos(2 * Math.PI * p.x)) + (p.y * p.y - A * Math.cos(2 * Math.PI * p.y));
        },
        parameters: [{ name: 'x', min: -5.12, max: 5.12 }, { name: 'y', min: -5.12, max: 5.12 }],
        optimum: 0, optimumParams: { x: 0, y: 0 },
    },
    ackley: {
        id: 'ackley', name: 'Ackley 2D',
        evaluate: (p) => {
            const a = 20, b = 0.2, c = 2 * Math.PI;
            return -a * Math.exp(-b * Math.sqrt(0.5 * (p.x * p.x + p.y * p.y)))
                - Math.exp(0.5 * (Math.cos(c * p.x) + Math.cos(c * p.y))) + a + Math.E;
        },
        parameters: [{ name: 'x', min: -5, max: 5 }, { name: 'y', min: -5, max: 5 }],
        optimum: 0, optimumParams: { x: 0, y: 0 },
    },
    sphere5d: {
        id: 'sphere-5d', name: 'Sphere 5D',
        evaluate: (p) => Object.values(p).reduce((s, v) => s + v * v, 0),
        parameters: Array.from({ length: 5 }, (_, i) => ({ name: `x${i}`, min: -10, max: 10 })),
        optimum: 0, optimumParams: Object.fromEntries(Array.from({ length: 5 }, (_, i) => [`x${i}`, 0])),
    },
    schwefel: {
        id: 'schwefel', name: 'Schwefel 3D',
        evaluate: (p) => {
            const vals = Object.values(p);
            return 418.9829 * vals.length - vals.reduce((s, xi) => s + xi * Math.sin(Math.sqrt(Math.abs(xi))), 0);
        },
        parameters: [
            { name: 'x', min: -500, max: 500 },
            { name: 'y', min: -500, max: 500 },
            { name: 'z', min: -500, max: 500 },
        ],
        optimum: 0, optimumParams: { x: 420.9687, y: 420.9687, z: 420.9687 },
    },
    styblinskiTang: {
        id: 'styblinski-tang', name: 'Styblinski-Tang 4D',
        evaluate: (p) => {
            const vals = Object.values(p);
            return vals.reduce((s, xi) => s + (xi ** 4 - 16 * xi ** 2 + 5 * xi), 0) / 2;
        },
        parameters: Array.from({ length: 4 }, (_, i) => ({ name: `x${i}`, min: -5, max: 5 })),
        optimum: -39.16599 * 4, optimumParams: Object.fromEntries(Array.from({ length: 4 }, (_, i) => [`x${i}`, -2.903534])),
    },
    griewank: {
        id: 'griewank', name: 'Griewank 3D',
        evaluate: (p) => {
            const vals = Object.values(p);
            const sumSq = vals.reduce((s, v) => s + v * v / 4000, 0);
            const prodCos = vals.reduce((prod, v, i) => prod * Math.cos(v / Math.sqrt(i + 1)), 1);
            return sumSq - prodCos + 1;
        },
        parameters: [
            { name: 'x', min: -600, max: 600 },
            { name: 'y', min: -600, max: 600 },
            { name: 'z', min: -600, max: 600 },
        ],
        optimum: 0, optimumParams: { x: 0, y: 0, z: 0 },
    },
};
// ─── Benchmark Runner ────────────────────────────────────────────────────────
async function runBenchmarks(config) {
    const maxEvals = config?.maxEvals || 5000;
    const verbose = config?.verbose !== false;
    const funcNames = config?.functions || Object.keys(exports.benchmarkFunctions);
    const results = [];
    if (verbose) {
        console.log('╔═══════════════════════════════════════════════════════════╗');
        console.log('║           Seeker Benchmark Suite v1.0                     ║');
        console.log('╠═══════════════════════════════════════════════════════════╣');
        console.log(`║  Budget: ${String(maxEvals).padEnd(6)} evals per function                  ║`);
        console.log(`║  Functions: ${funcNames.length}                                          ║`);
        console.log(`║  Seed: ${String(config?.seed || 'random').padEnd(10)}                                   ║`);
        console.log('╚═══════════════════════════════════════════════════════════╝\n');
    }
    for (const name of funcNames) {
        const fn = exports.benchmarkFunctions[name];
        if (!fn)
            continue;
        const { SeekerAgent } = await Promise.resolve().then(() => __importStar(require('./agent')));
        const agent = new SeekerAgent(fn, {
            maxEvals, verbosity: 'silent',
            seed: config?.seed,
        });
        const start = Date.now();
        const state = await agent.run(fn.optimum);
        const time = (Date.now() - start) / 1000;
        const result = state.best;
        const gap = Math.abs(result.score - fn.optimum);
        const accuracy = fn.optimum === 0
            ? Math.max(0, 1 - gap)
            : Math.max(0, 1 - gap / Math.abs(fn.optimum));
        const benchResult = {
            function: fn.name, score: result.score, optimum: fn.optimum,
            gap, accuracy: Math.min(1, accuracy), evals: maxEvals,
            time, params: result.params, ufe: state.ufe,
        };
        results.push(benchResult);
        if (verbose) {
            const status = gap < 1 ? '✅' : gap < 10 ? '⚠️' : '❌';
            console.log(`${status} ${fn.name.padEnd(22)} score=${result.score.toFixed(4).padStart(12)} | gap=${gap.toFixed(4).padStart(10)} | UFE=${(state.ufe.ufeRatio * 100).toFixed(1)}% | ${time.toFixed(2)}s`);
        }
    }
    if (verbose) {
        console.log('\n────────────────────────────────────────────────────');
        const avgAccuracy = results.reduce((s, r) => s + r.accuracy, 0) / results.length;
        const avgUFE = results.reduce((s, r) => s + r.ufe.ufeRatio, 0) / results.length;
        const totalTime = results.reduce((s, r) => s + r.time, 0);
        const perfect = results.filter(r => r.gap < 1).length;
        console.log(`Summary: ${perfect}/${results.length} near-optimal | Avg accuracy: ${(avgAccuracy * 100).toFixed(1)}% | Avg UFE: ${(avgUFE * 100).toFixed(1)}% | Total: ${totalTime.toFixed(1)}s`);
    }
    return results;
}
//# sourceMappingURL=benchmarks.js.map