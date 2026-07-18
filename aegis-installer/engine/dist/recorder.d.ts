/**
 * AEGIS — Data Recorder
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Scripts every evaluation to disk. CSV + JSON logs.
 * Export convergence curves, discovery logs, strategy stats.
 * The black box flight recorder for optimization runs.
 */
import { EvalResult, Discovery, AgentState, UFEMetrics, AgentEvent, Strategy } from './interfaces';
export interface RecorderConfig {
    dir: string;
    runId: string;
    logEvals?: boolean;
    logDiscoveries?: boolean;
    logStrategies?: boolean;
    flushInterval?: number;
}
export declare class DataRecorder {
    private config;
    private evalCount;
    private csvStream;
    private discoveryStream;
    private paramNames;
    private initialized;
    constructor(config: RecorderConfig);
    init(paramNames: string[]): void;
    recordEval(result: EvalResult, useful: boolean): void;
    recordDiscovery(discovery: Discovery): void;
    recordStrategies(strategies: Strategy[]): void;
    writeSummary(state: AgentState): void;
    exportConvergenceCurve(ufe: UFEMetrics): void;
    createHandler(): (event: AgentEvent) => void;
    close(): void;
}
export declare function createRecorder(runId: string, dir?: string): DataRecorder;
//# sourceMappingURL=recorder.d.ts.map