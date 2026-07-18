/**
 * Seeker — Warm Start / Checkpoint Resume
 * Save state. Resume anytime. Never lose progress.
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

const SEEKER_VERSION = '1.0.0';

export function saveCheckpoint(taskId: string, state: AgentState, filePath?: string): string {
  const savePath = filePath || path.join(process.cwd(), `.seeker-checkpoint-${taskId}.json`);
  const dir = path.dirname(savePath);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

  const data: WarmStartData = {
    taskId,
    state: { ...state, history: state.history.slice(-1000) },
    savedAt: new Date().toISOString(),
    version: SEEKER_VERSION,
  };

  fs.writeFileSync(savePath, JSON.stringify(data, null, 2));
  return savePath;
}

export function loadCheckpoint(filePath: string): WarmStartData | null {
  if (!fs.existsSync(filePath)) return null;
  try { return JSON.parse(fs.readFileSync(filePath, 'utf-8')); }
  catch { return null; }
}

export function findLatestCheckpoint(taskId: string, searchDir?: string): string | null {
  const dir = searchDir || process.cwd();
  const fullPath = path.join(dir, `.seeker-checkpoint-${taskId}.json`);
  return fs.existsSync(fullPath) ? fullPath : null;
}

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
    forceSave: (state: AgentState) => { saveCheckpoint(taskId, state); lastSave = Date.now(); },
  };
}

export function warmStartFrom(checkpoint: WarmStartData): { history: EvalResult[]; best: EvalResult | null } {
  return { history: checkpoint.state.history, best: checkpoint.state.best };
}
