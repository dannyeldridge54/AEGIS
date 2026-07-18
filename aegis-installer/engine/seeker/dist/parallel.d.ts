/**
 * Seeker — Parallel Batch Evaluator
 * Runs evaluations in parallel batches with UFE tracking,
 * seeded RNG, concurrency limits, timeout, and retry logic.
 */
import { Task, AgentConfig, AgentState } from './interfaces';
export interface ParallelConfig extends AgentConfig {
    concurrency?: number;
    evalTimeout?: number;
    retries?: number;
    batchSize?: number;
}
/**
 * Parallel batch optimizer with full UFE tracking.
 * Ideal for network calls, simulations, or any async evaluation.
 */
export declare function parallelOptimize(task: Task, config?: ParallelConfig, optimum?: number): Promise<AgentState>;
//# sourceMappingURL=parallel.d.ts.map