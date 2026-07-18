"use strict";
/**
 * Seeker — Persistent Memory System
 * Records everything. Learns from every run.
 * Knowledge graph + episodic memory + semantic search.
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
exports.Memory = void 0;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
class Memory {
    constructor(storePath) {
        this.entries = [];
        this.nodes = new Map();
        this.edges = [];
        this.maxEntries = 10000;
        this.storePath = storePath || path.join(process.cwd(), '.seeker-memory.json');
        this.load();
    }
    remember(entry) {
        const id = `mem_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
        this.entries.push({ ...entry, id, timestamp: Date.now() });
        this.trimMemory();
        return id;
    }
    search(query, limit = 10) {
        const terms = query.toLowerCase().split(/\s+/);
        const scored = this.entries.map(entry => {
            const text = `${entry.content} ${entry.tags.join(' ')}`.toLowerCase();
            let score = 0;
            for (const term of terms) {
                if (text.includes(term))
                    score += 1;
                if (entry.tags.some(t => t.toLowerCase() === term))
                    score += 2;
            }
            const age = (Date.now() - entry.timestamp) / (7 * 24 * 3600000);
            score *= Math.exp(-age * 0.1);
            score *= (1 + entry.importance);
            return { entry, score };
        }).filter(s => s.score > 0);
        scored.sort((a, b) => b.score - a.score);
        return scored.slice(0, limit).map(s => s.entry);
    }
    recent(n = 20, type) {
        let filtered = type ? this.entries.filter(e => e.type === type) : this.entries;
        return filtered.slice(-n);
    }
    /** Record a full run with UFE metrics and discoveries */
    learnFromRun(taskName, result) {
        // Episode
        this.remember({
            type: 'episode',
            content: `Task "${taskName}": best=${result.bestScore.toFixed(6)} after ${result.totalEvals} evals. Top: ${result.topStrategy}. Params: ${JSON.stringify(result.bestParams)}`,
            tags: [taskName, result.topStrategy, 'optimization_result'],
            importance: Math.min(1, result.discoveries * 0.2 + 0.3),
        });
        // Strategy insight
        this.remember({
            type: 'strategy_insight',
            content: `For "${taskName}" (${Object.keys(result.bestParams).length} params), ${result.topStrategy} performed best`,
            tags: [result.topStrategy, `${Object.keys(result.bestParams).length}d`],
            importance: 0.6,
        });
        // UFE record
        if (result.ufe) {
            this.remember({
                type: 'ufe_record',
                content: `UFE for "${taskName}": ratio=${(result.ufe.ufeRatio * 100).toFixed(1)}% useful=${result.ufe.usefulEvals}/${result.ufe.totalEvals} AUCC=${result.ufe.aucc.toFixed(4)}`,
                tags: [taskName, 'ufe'],
                importance: 0.5,
                metadata: { ufe: result.ufe },
            });
        }
        // Record each discovery
        if (result.allDiscoveries) {
            for (const disc of result.allDiscoveries) {
                this.remember({
                    type: 'discovery',
                    content: disc.description,
                    tags: [taskName, disc.type],
                    importance: disc.confidence,
                });
            }
        }
    }
    recallStrategy(taskDescription, nParams) {
        const insights = this.search(`${taskDescription} ${nParams}d strategy`, 5)
            .filter(e => e.type === 'strategy_insight');
        if (insights.length === 0)
            return null;
        const match = insights[0].content.match(/(\w+) performed best/);
        return match?.[1] || null;
    }
    // ─── Knowledge Graph ───────────────────────────────────────────────────
    addNode(node) { this.nodes.set(node.id, node); }
    addEdge(from, to, relation, weight = 1) {
        this.edges.push({ from, to, relation, weight });
    }
    relatedTo(nodeId, depth = 2) {
        const visited = new Set([nodeId]);
        let frontier = [nodeId];
        for (let d = 0; d < depth; d++) {
            const nextFrontier = [];
            for (const current of frontier) {
                const connected = this.edges
                    .filter(e => e.from === current || e.to === current)
                    .map(e => e.from === current ? e.to : e.from)
                    .filter(id => !visited.has(id));
                for (const id of connected) {
                    visited.add(id);
                    nextFrontier.push(id);
                }
            }
            frontier = nextFrontier;
        }
        visited.delete(nodeId);
        return [...visited].map(id => this.nodes.get(id)).filter(Boolean);
    }
    graphStats() {
        const types = {};
        for (const node of this.nodes.values())
            types[node.type] = (types[node.type] || 0) + 1;
        return { nodes: this.nodes.size, edges: this.edges.length, types };
    }
    // ─── Persistence ───────────────────────────────────────────────────────
    save() {
        const data = { entries: this.entries, nodes: [...this.nodes.entries()], edges: this.edges };
        const dir = path.dirname(this.storePath);
        if (!fs.existsSync(dir))
            fs.mkdirSync(dir, { recursive: true });
        fs.writeFileSync(this.storePath, JSON.stringify(data));
    }
    load() {
        if (!fs.existsSync(this.storePath))
            return;
        try {
            const data = JSON.parse(fs.readFileSync(this.storePath, 'utf-8'));
            this.entries = data.entries || [];
            this.nodes = new Map(data.nodes || []);
            this.edges = data.edges || [];
        }
        catch { /* fresh start */ }
    }
    clear() { this.entries = []; this.nodes.clear(); this.edges = []; }
    getSize() { return this.entries.length; }
    trimMemory() {
        if (this.entries.length > this.maxEntries) {
            this.entries.sort((a, b) => {
                const scoreA = a.importance + (a.timestamp / Date.now());
                const scoreB = b.importance + (b.timestamp / Date.now());
                return scoreB - scoreA;
            });
            this.entries = this.entries.slice(0, this.maxEntries / 2);
            this.entries.sort((a, b) => a.timestamp - b.timestamp);
        }
    }
}
exports.Memory = Memory;
//# sourceMappingURL=memory.js.map