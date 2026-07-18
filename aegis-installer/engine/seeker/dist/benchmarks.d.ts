/**
 * Seeker — Benchmark Suite
 * Standard test functions + UFE-aware benchmarking with known optima.
 */
import { Task, UFEMetrics } from './interfaces';
export declare const benchmarkFunctions: Record<string, Task & {
    optimum: number;
    optimumParams: Record<string, number>;
}>;
export interface BenchmarkResult {
    function: string;
    score: number;
    optimum: number;
    gap: number;
    accuracy: number;
    evals: number;
    time: number;
    params: Record<string, number>;
    ufe: UFEMetrics;
}
export declare function runBenchmarks(config?: {
    maxEvals?: number;
    functions?: string[];
    verbose?: boolean;
    seed?: number;
}): Promise<BenchmarkResult[]>;
//# sourceMappingURL=benchmarks.d.ts.map