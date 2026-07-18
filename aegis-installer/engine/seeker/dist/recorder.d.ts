/**
 * Seeker — Data Recorder
 * Scripts every evaluation to disk. CSV + JSON logs.
 * Export convergence curves, discovery logs, strategy stats.
 * The black box flight recorder for optimization runs.
 */
import { EvalResult, Discovery, AgentState, UFEMetrics, AgentEvent, Strategy } from './interfaces';
export interface RecorderConfig {
    /** Output directory */
    dir: string;
    /** Run/session ID (used in filenames) */
    runId: string;
    /** Write CSV of every evaluation */
    logEvals?: boolean;
    /** Write discoveries as they happen */
    logDiscoveries?: boolean;
    /** Write strategy stats periodically */
    logStrategies?: boolean;
    /** Flush interval in evals (default: 100) */
    flushInterval?: number;
}
export declare class DataRecorder {
    private config;
    private evalBuffer;
    private discoveryBuffer;
    private evalCount;
    private csvStream;
    private discoveryStream;
    private paramNames;
    private initialized;
    constructor(config: RecorderConfig);
    /** Initialize with parameter names (call before recording) */
    init(paramNames: string[]): void;
    /** Record a single evaluation */
    recordEval(result: EvalResult, useful: boolean): void;
    /** Record a discovery */
    recordDiscovery(discovery: Discovery): void;
    /** Write strategy performance snapshot */
    recordStrategies(strategies: Strategy[]): void;
    /** Write final run summary */
    writeSummary(state: AgentState): void;
    /** Export convergence curve as CSV */
    exportConvergenceCurve(ufe: UFEMetrics): void;
    /** Create an event handler for plugging into agent.on() */
    createHandler(): (event: AgentEvent) => void;
    /** Close all streams */
    close(): void;
}
/**
 * Quick factory: create a recorder and wire it to an agent.
 *
 * @example
 * const rec = createRecorder('my-run', './data');
 * rec.init(task.parameters.map(p => p.name));
 * agent.on(rec.createHandler());
 */
export declare function createRecorder(runId: string, dir?: string): DataRecorder;
//# sourceMappingURL=recorder.d.ts.map