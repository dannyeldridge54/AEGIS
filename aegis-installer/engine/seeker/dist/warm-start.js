"use strict";
/**
 * Seeker — Warm Start / Checkpoint Resume
 * Save state. Resume anytime. Never lose progress.
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
const SEEKER_VERSION = '1.0.0';
function saveCheckpoint(taskId, state, filePath) {
    const savePath = filePath || path.join(process.cwd(), `.seeker-checkpoint-${taskId}.json`);
    const dir = path.dirname(savePath);
    if (!fs.existsSync(dir))
        fs.mkdirSync(dir, { recursive: true });
    const data = {
        taskId,
        state: { ...state, history: state.history.slice(-1000) },
        savedAt: new Date().toISOString(),
        version: SEEKER_VERSION,
    };
    fs.writeFileSync(savePath, JSON.stringify(data, null, 2));
    return savePath;
}
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
function findLatestCheckpoint(taskId, searchDir) {
    const dir = searchDir || process.cwd();
    const fullPath = path.join(dir, `.seeker-checkpoint-${taskId}.json`);
    return fs.existsSync(fullPath) ? fullPath : null;
}
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
        forceSave: (state) => { saveCheckpoint(taskId, state); lastSave = Date.now(); },
    };
}
function warmStartFrom(checkpoint) {
    return { history: checkpoint.state.history, best: checkpoint.state.best };
}
//# sourceMappingURL=warm-start.js.map