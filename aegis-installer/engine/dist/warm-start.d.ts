/**
 * AEGIS — Warm Start / History Resume
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Save agent state to disk and resume from where you left off.
 * Never lose progress — pause, shutdown, resume anytime.
 */
import { AgentState, EvalResult } from './interfaces';
export interface WarmStartData {
    taskId: string;
    state: AgentState;
    savedAt: string;
    version: string;
}
/**
 * Save agent state to disk for later resumption.
 */
export declare function saveCheckpoint(taskId: string, state: AgentState, filePath?: string): string;
/**
 * Load a checkpoint from disk.
 */
export declare function loadCheckpoint(filePath: string): WarmStartData | null;
/**
 * Find the most recent checkpoint for a task.
 */
export declare function findLatestCheckpoint(taskId: string, searchDir?: string): string | null;
/**
 * Auto-save handler — attach to agent events for periodic saving.
 *
 * @example
 * const saver = autoSave('my-task', 60); // save every 60s
 * agent.on(saver.handler);
 */
export declare function autoSave(taskId: string, intervalSec?: number): {
    handler: (event: any) => void;
    forceSave: (state: AgentState) => void;
};
/**
 * Merge history from a checkpoint into fresh agent state
 * (warm-starts the meta-learner with prior knowledge).
 */
export declare function warmStartFrom(checkpoint: WarmStartData): {
    history: EvalResult[];
    best: EvalResult | null;
};
//# sourceMappingURL=warm-start.d.ts.map