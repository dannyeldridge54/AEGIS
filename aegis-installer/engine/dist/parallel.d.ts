/**
 * AEGIS — Parallel Batch Evaluator
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Runs evaluations in parallel batches for massive speedup on async tasks.
 * Supports concurrency limits, timeout, and retry logic.
 */
import { Task, AgentConfig, AgentState } from './interfaces';
export interface ParallelConfig extends AgentConfig {
    /** Number of concurrent evaluations (default: 4) */
    concurrency?: number;
    /** Timeout per evaluation in ms (default: 30000) */
    evalTimeout?: number;
    /** Retry failed evaluations (default: 1) */
    retries?: number;
    /** Batch size (default: concurrency * 2) */
    batchSize?: number;
}
/**
 * Parallel batch optimizer — evaluates multiple parameter sets concurrently.
 * Ideal for network calls, simulations, or any async evaluation function.
 *
 * @example
 * const result = await parallelOptimize({
 *   id: 'api-tune',
 *   name: 'API Config Tuning',
 *   evaluate: async (p) => await benchmarkEndpoint(p),
 *   parameters: [...],
 * }, { concurrency: 8, maxEvals: 5000 });
 */
export declare function parallelOptimize(task: Task, config?: ParallelConfig): Promise<AgentState>;
//# sourceMappingURL=parallel.d.ts.map