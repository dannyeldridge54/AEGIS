"use strict";
/**
 * AEGIS — Benchmark Suite
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Standard optimization benchmarks to prove AEGIS performance.
 * Includes well-known test functions used in optimization literature.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.benchmarkFunctions = void 0;
exports.runBenchmarks = runBenchmarks;
const agent_1 = require("./agent");
// ─── Standard Test Functions ─────────────────────────────────────────────────
exports.benchmarkFunctions = {
    /** Rosenbrock (2D) — hard banana valley. Global min: f(1,1) = 0 */
    rosenbrock: {
        id: 'rosenbrock', name: 'Rosenbrock 2D',
        evaluate: (p) => Math.pow(1 - p.x, 2) + 100 * Math.pow(p.y - p.x * p.x, 2),
        parameters: [{ name: 'x', min: -5, max: 5 }, { name: 'y', min: -5, max: 5 }],
        optimum: 0, optimumParams: { x: 1, y: 1 },
    },
    /** Rastrigin (2D) — highly multimodal. Global min: f(0,0) = 0 */
    rastrigin: {
        id: 'rastrigin', name: 'Rastrigin 2D',
        evaluate: (p) => {
            const A = 10;
            return A * 2 + (p.x * p.x - A * Math.cos(2 * Math.PI * p.x)) + (p.y * p.y - A * Math.cos(2 * Math.PI * p.y));
        },
        parameters: [{ name: 'x', min: -5.12, max: 5.12 }, { name: 'y', min: -5.12, max: 5.12 }],
        optimum: 0, optimumParams: { x: 0, y: 0 },
    },
    /** Ackley (2D) — many local minima, one global. Global min: f(0,0) = 0 */
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
    /** Sphere (5D) — simple convex. Global min: f(0,...,0) = 0 */
    sphere5d: {
        id: 'sphere-5d', name: 'Sphere 5D',
        evaluate: (p) => Object.values(p).reduce((s, v) => s + v * v, 0),
        parameters: Array.from({ length: 5 }, (_, i) => ({ name: `x${i}`, min: -10, max: 10 })),
        optimum: 0, optimumParams: Object.fromEntries(Array.from({ length: 5 }, (_, i) => [`x${i}`, 0])),
    },
    /** Schwefel (3D) — deceptive, global min far from origin */
    schwefel: {
        id: 'schwefel', name: 'Schwefel 3D',
        evaluate: (p) => {
            const vals = Object.values(p);
            const d = vals.length;
            return 418.9829 * d - vals.reduce((s, xi) => s + xi * Math.sin(Math.sqrt(Math.abs(xi))), 0);
        },
        parameters: [
            { name: 'x', min: -500, max: 500 },
            { name: 'y', min: -500, max: 500 },
            { name: 'z', min: -500, max: 500 },
        ],
        optimum: 0, optimumParams: { x: 420.9687, y: 420.9687, z: 420.9687 },
    },
    /** Styblinski-Tang (4D) — multiple local minima */
    styblinskiTang: {
        id: 'styblinski-tang', name: 'Styblinski-Tang 4D',
        evaluate: (p) => {
            const vals = Object.values(p);
            return vals.reduce((s, xi) => s + (xi ** 4 - 16 * xi ** 2 + 5 * xi), 0) / 2;
        },
        parameters: Array.from({ length: 4 }, (_, i) => ({ name: `x${i}`, min: -5, max: 5 })),
        optimum: -39.16599 * 4, optimumParams: Object.fromEntries(Array.from({ length: 4 }, (_, i) => [`x${i}`, -2.903534])),
    },
    /** Griewank (3D) — interactions between variables */
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
/**
 * Run AEGIS against standard benchmark functions.
 * Compare results against known optima.
 */
async function runBenchmarks(config) {
    const maxEvals = config?.maxEvals || 5000;
    const verbose = config?.verbose !== false;
    const funcNames = config?.functions || Object.keys(exports.benchmarkFunctions);
    const results = [];
    if (verbose) {
        console.log('╔═══════════════════════════════════════════════════════════╗');
        console.log('║           AEGIS Benchmark Suite v1.0                      ║');
        console.log('╠═══════════════════════════════════════════════════════════╣');
        console.log(`║  Budget: ${maxEvals} evals per function                         ║`);
        console.log(`║  Functions: ${funcNames.length}                                          ║`);
        console.log('╚═══════════════════════════════════════════════════════════╝\n');
    }
    for (const name of funcNames) {
        const fn = exports.benchmarkFunctions[name];
        if (!fn)
            continue;
        const start = Date.now();
        const result = await (0, agent_1.optimize)(fn.evaluate, fn.parameters, {
            maxEvals,
            verbosity: 'silent',
        });
        const time = (Date.now() - start) / 1000;
        const gap = Math.abs(result.score - fn.optimum);
        const accuracy = fn.optimum === 0
            ? Math.max(0, 1 - gap)
            : Math.max(0, 1 - gap / Math.abs(fn.optimum));
        const benchResult = {
            function: fn.name,
            score: result.score,
            optimum: fn.optimum,
            gap,
            accuracy: Math.min(1, accuracy),
            evals: maxEvals,
            time,
            params: result.params,
        };
        results.push(benchResult);
        if (verbose) {
            const status = gap < 1 ? '✅' : gap < 10 ? '⚠️' : '❌';
            console.log(`${status} ${fn.name.padEnd(22)} score=${result.score.toFixed(4).padStart(12)} | gap=${gap.toFixed(4).padStart(10)} | ${time.toFixed(2)}s`);
        }
    }
    if (verbose) {
        console.log('\n────────────────────────────────────────────────────');
        const avgAccuracy = results.reduce((s, r) => s + r.accuracy, 0) / results.length;
        const totalTime = results.reduce((s, r) => s + r.time, 0);
        const perfect = results.filter(r => r.gap < 1).length;
        console.log(`Summary: ${perfect}/${results.length} near-optimal | Avg accuracy: ${(avgAccuracy * 100).toFixed(1)}% | Total: ${totalTime.toFixed(1)}s`);
    }
    return results;
}
// ─── CLI Entry ───────────────────────────────────────────────────────────────
if (require.main === module) {
    const evals = parseInt(process.argv[2]) || 5000;
    runBenchmarks({ maxEvals: evals }).catch(console.error);
}
//# sourceMappingURL=benchmarks.js.map