/**
 * AEGIS — Warm Start / History Resume
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Save agent state to disk and resume from where you left off.
 * Never lose progress — pause, shutdown, resume anytime.
 */

import * as fs from 'fs';
import * as path from 'path';
import { AgentState, EvalResult } from './interfaces';

export interface WarmStartData {
  taskId: string;
  state: AgentState;
  savedAt: string;
  version: string;
}

const AEGIS_VERSION = '1.0.0';

/**
 * Save agent state to disk for later resumption.
 */
export function saveCheckpoint(
  taskId: string,
  state: AgentState,
  filePath?: string
): string {
  const savePath = filePath || path.join(process.cwd(), `.aegis-checkpoint-${taskId}.json`);
  const dir = path.dirname(savePath);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

  const data: WarmStartData = {
    taskId,
    state: {
      ...state,
      // Trim history to save space
      history: state.history.slice(-1000),
    },
    savedAt: new Date().toISOString(),
    version: AEGIS_VERSION,
  };

  fs.writeFileSync(savePath, JSON.stringify(data, null, 2));
  return savePath;
}

/**
 * Load a checkpoint from disk.
 */
export function loadCheckpoint(filePath: string): WarmStartData | null {
  if (!fs.existsSync(filePath)) return null;
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  } catch {
    return null;
  }
}

/**
 * Find the most recent checkpoint for a task.
 */
export function findLatestCheckpoint(taskId: string, searchDir?: string): string | null {
  const dir = searchDir || process.cwd();
  const pattern = `.aegis-checkpoint-${taskId}.json`;
  const fullPath = path.join(dir, pattern);
  return fs.existsSync(fullPath) ? fullPath : null;
}

/**
 * Auto-save handler — attach to agent events for periodic saving.
 *
 * @example
 * const saver = autoSave('my-task', 60); // save every 60s
 * agent.on(saver.handler);
 */
export function autoSave(taskId: string, intervalSec: number = 60) {
  let lastSave = Date.now();

  return {
    handler: (event: any) => {
      if (event.type === 'report' || event.type === 'stopped') {
        const now = Date.now();
        if (now - lastSave >= intervalSec * 1000 || event.type === 'stopped') {
          saveCheckpoint(taskId, event.state || event);
          lastSave = now;
        }
      }
    },
    forceSave: (state: AgentState) => {
      saveCheckpoint(taskId, state);
      lastSave = Date.now();
    },
  };
}

/**
 * Merge history from a checkpoint into fresh agent state
 * (warm-starts the meta-learner with prior knowledge).
 */
export function warmStartFrom(
  checkpoint: WarmStartData
): { history: EvalResult[]; best: EvalResult | null } {
  return {
    history: checkpoint.state.history,
    best: checkpoint.state.best,
  };
}
