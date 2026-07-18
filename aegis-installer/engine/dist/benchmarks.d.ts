/**
 * AEGIS — Benchmark Suite
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Standard optimization benchmarks to prove AEGIS performance.
 * Includes well-known test functions used in optimization literature.
 */
import { Task } from './interfaces';
export declare const benchmarkFunctions: {
    /** Rosenbrock (2D) — hard banana valley. Global min: f(1,1) = 0 */
    rosenbrock: Task & {
        optimum: number;
        optimumParams: Record<string, number>;
    };
    /** Rastrigin (2D) — highly multimodal. Global min: f(0,0) = 0 */
    rastrigin: Task & {
        optimum: number;
        optimumParams: Record<string, number>;
    };
    /** Ackley (2D) — many local minima, one global. Global min: f(0,0) = 0 */
    ackley: Task & {
        optimum: number;
        optimumParams: Record<string, number>;
    };
    /** Sphere (5D) — simple convex. Global min: f(0,...,0) = 0 */
    sphere5d: Task & {
        optimum: number;
        optimumParams: Record<string, number>;
    };
    /** Schwefel (3D) — deceptive, global min far from origin */
    schwefel: Task & {
        optimum: number;
        optimumParams: Record<string, number>;
    };
    /** Styblinski-Tang (4D) — multiple local minima */
    styblinskiTang: Task & {
        optimum: number;
        optimumParams: Record<string, number>;
    };
    /** Griewank (3D) — interactions between variables */
    griewank: Task & {
        optimum: number;
        optimumParams: Record<string, number>;
    };
};
export interface BenchmarkResult {
    function: string;
    score: number;
    optimum: number;
    gap: number;
    accuracy: number;
    evals: number;
    time: number;
    params: Record<string, number>;
}
/**
 * Run AEGIS against standard benchmark functions.
 * Compare results against known optima.
 */
export declare function runBenchmarks(config?: {
    maxEvals?: number;
    functions?: string[];
    verbose?: boolean;
}): Promise<BenchmarkResult[]>;
//# sourceMappingURL=benchmarks.d.ts.map