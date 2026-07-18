/**
 * Seeker — Core Agent
 * Autonomous discovery engine. Every evaluation is tracked for UFE,
 * anomalies are detected in real-time, discoveries are recorded,
 * and the agent learns which strategies work via seeded-deterministic runs.
 */
import { Task, AgentConfig, AgentState, EvalResult, EventHandler } from './interfaces';
export declare class SeekerAgent {
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
    on(handler: EventHandler): this;
    /** Seed the agent with a known-good starting point (e.g. from another engine) */
    seed(params: Record<string, number>, score: number): this;
    run(optimum?: number): Promise<AgentState>;
    step(): Promise<EvalResult>;
    stop(reason?: string): void;
    getState(): AgentState;
    getSeed(): number;
    setLanguage(lang: string): void;
    private isMinimizing;
    private updatePhase;
    private checkConvergence;
    private report;
    private saveState;
    private emit;
    private log;
}
export declare function seeker(task: Task, config?: AgentConfig): SeekerAgent;
export declare function optimize(fn: (params: Record<string, number>) => number | Promise<number>, parameters: Array<{
    name: string;
    min: number;
    max: number;
    description?: string;
}>, config?: AgentConfig): Promise<EvalResult>;
//# sourceMappingURL=agent.d.ts.map