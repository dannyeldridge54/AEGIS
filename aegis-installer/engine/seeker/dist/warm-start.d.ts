/**
 * Seeker — Warm Start / Checkpoint Resume
 * Save state. Resume anytime. Never lose progress.
 */
import { AgentState, EvalResult } from './interfaces';
export interface WarmStartData {
    taskId: string;
    state: AgentState;
    savedAt: string;
    version: string;
}
export declare function saveCheckpoint(taskId: string, state: AgentState, filePath?: string): string;
export declare function loadCheckpoint(filePath: string): WarmStartData | null;
export declare function findLatestCheckpoint(taskId: string, searchDir?: string): string | null;
export declare function autoSave(taskId: string, intervalSec?: number): {
    handler: (event: any) => void;
    forceSave: (state: AgentState) => void;
};
export declare function warmStartFrom(checkpoint: WarmStartData): {
    history: EvalResult[];
    best: EvalResult | null;
};
//# sourceMappingURL=warm-start.d.ts.map