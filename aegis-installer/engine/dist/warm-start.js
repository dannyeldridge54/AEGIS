"use strict";
/**
 * AEGIS — Warm Start / History Resume
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Save agent state to disk and resume from where you left off.
 * Never lose progress — pause, shutdown, resume anytime.
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.saveCheckpoint = saveCheckpoint;
exports.loadCheckpoint = loadCheckpoint;
exports.findLatestCheckpoint = findLatestCheckpoint;
exports.autoSave = autoSave;
exports.warmStartFrom = warmStartFrom;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const AEGIS_VERSION = '1.2.0';
/**
 * Save agent state to disk for later resumption.
 */
function saveCheckpoint(taskId, state, filePath) {
    const savePath = filePath || path.join(process.cwd(), `.aegis-checkpoint-${taskId}.json`);
    const dir = path.dirname(savePath);
    if (!fs.existsSync(dir))
        fs.mkdirSync(dir, { recursive: true });
    const data = {
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
function loadCheckpoint(filePath) {
    if (!fs.existsSync(filePath))
        return null;
    try {
        return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
    }
    catch {
        return null;
    }
}
/**
 * Find the most recent checkpoint for a task.
 */
function findLatestCheckpoint(taskId, searchDir) {
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
function autoSave(taskId, intervalSec = 60) {
    let lastSave = Date.now();
    return {
        handler: (event) => {
            if (event.type === 'report' || event.type === 'stopped') {
                const now = Date.now();
                if (now - lastSave >= intervalSec * 1000 || event.type === 'stopped') {
                    saveCheckpoint(taskId, event.state || event);
                    lastSave = now;
                }
            }
        },
        forceSave: (state) => {
            saveCheckpoint(taskId, state);
            lastSave = Date.now();
        },
    };
}
/**
 * Merge history from a checkpoint into fresh agent state
 * (warm-starts the meta-learner with prior knowledge).
 */
function warmStartFrom(checkpoint) {
    return {
        history: checkpoint.state.history,
        best: checkpoint.state.best,
    };
}
//# sourceMappingURL=warm-start.js.map