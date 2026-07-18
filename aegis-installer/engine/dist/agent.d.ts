/**
 * AEGIS — Core Agent
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * The main autonomous agent that self-learns, adapts strategies,
 * and optimizes any objective with zero configuration.
 * Now with seeded RNG, UFE tracking, and anomaly detection.
 */
import { Task, AgentConfig, AgentState, EvalResult, EventHandler } from './interfaces';
export declare class AegisAgent {
    private task;
    private config;
    private state;
    private metaLearner;
    private handlers;
    private running;
    private startTime;
    private lastReportTime;
    private lastBestTime;
    private gridIndex;
    private msg;
    private rng;
    private ufeTracker;
    private anomalyDetector;
    constructor(task: Task, config?: AgentConfig);
    /** Subscribe to agent events */
    on(handler: EventHandler): this;
    /** Seed the agent with a known-good starting point (e.g. from another engine) */
    seed(params: Record<string, number>, score: number): this;
    /** Run the agent (async, runs until convergence or maxEvals) */
    run(optimum?: number): Promise<AgentState>;
    /** Run a single step */
    step(): Promise<EvalResult>;
    /** Stop the agent */
    stop(reason?: string): void;
    /** Get current state */
    getState(): AgentState;
    /** Change language at runtime */
    setLanguage(lang: string): void;
    private isMinimizing;
    private updatePhase;
    private checkConvergence;
    private report;
    private saveState;
    private emit;
    private log;
}
export declare function aegis(task: Task, config?: AgentConfig): AegisAgent;
export declare function optimize(fn: (params: Record<string, number>) => number | Promise<number>, parameters: Array<{
    name: string;
    min: number;
    max: number;
    description?: string;
}>, config?: AgentConfig): Promise<EvalResult>;
//# sourceMappingURL=agent.d.ts.map