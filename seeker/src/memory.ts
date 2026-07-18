/**
 * Seeker — Persistent Memory System
 * Records everything. Learns from every run.
 * Knowledge graph + episodic memory + semantic search.
 */

import * as fs from 'fs';
import * as path from 'path';
import { UFEMetrics, Discovery } from './interfaces';

export interface MemoryEntry {
  id: string;
  type: 'fact' | 'episode' | 'strategy_insight' | 'discovery' | 'failure' | 'ufe_record';
  content: string;
  tags: string[];
  importance: number;
  timestamp: number;
  references?: string[];
  metadata?: Record<string, any>;
}

export interface KnowledgeNode {
  id: string;
  label: string;
  type: 'concept' | 'parameter' | 'strategy' | 'result' | 'task';
  properties: Record<string, any>;
}

export interface KnowledgeEdge {
  from: string;
  to: string;
  relation: string;
  weight: number;
}

export class Memory {
  private entries: MemoryEntry[] = [];
  private nodes: Map<string, KnowledgeNode> = new Map();
  private edges: KnowledgeEdge[] = [];
  private storePath: string;
  private maxEntries = 10000;

  constructor(storePath?: string) {
    this.storePath = storePath || path.join(process.cwd(), '.seeker-memory.json');
    this.load();
  }

  remember(entry: Omit<MemoryEntry, 'id' | 'timestamp'>): string {
    const id = `mem_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
    this.entries.push({ ...entry, id, timestamp: Date.now() });
    this.trimMemory();
    return id;
  }

  search(query: string, limit: number = 10): MemoryEntry[] {
    const terms = query.toLowerCase().split(/\s+/);
    const scored = this.entries.map(entry => {
      const text = `${entry.content} ${entry.tags.join(' ')}`.toLowerCase();
      let score = 0;
      for (const term of terms) {
        if (text.includes(term)) score += 1;
        if (entry.tags.some(t => t.toLowerCase() === term)) score += 2;
      }
      const age = (Date.now() - entry.timestamp) / (7 * 24 * 3600000);
      score *= Math.exp(-age * 0.1);
      score *= (1 + entry.importance);
      return { entry, score };
    }).filter(s => s.score > 0);

    scored.sort((a, b) => b.score - a.score);
    return scored.slice(0, limit).map(s => s.entry);
  }

  recent(n: number = 20, type?: MemoryEntry['type']): MemoryEntry[] {
    let filtered = type ? this.entries.filter(e => e.type === type) : this.entries;
    return filtered.slice(-n);
  }

  /** Record a full run with UFE metrics and discoveries */
  learnFromRun(taskName: string, result: {
    bestScore: number;
    bestParams: Record<string, number>;
    topStrategy: string;
    totalEvals: number;
    discoveries: number;
    ufe?: UFEMetrics;
    allDiscoveries?: Discovery[];
  }): void {
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

  recallStrategy(taskDescription: string, nParams: number): string | null {
    const insights = this.search(`${taskDescription} ${nParams}d strategy`, 5)
      .filter(e => e.type === 'strategy_insight');
    if (insights.length === 0) return null;
    const match = insights[0].content.match(/(\w+) performed best/);
    return match?.[1] || null;
  }

  // ─── Knowledge Graph ───────────────────────────────────────────────────

  addNode(node: KnowledgeNode): void { this.nodes.set(node.id, node); }
  addEdge(from: string, to: string, relation: string, weight: number = 1): void {
    this.edges.push({ from, to, relation, weight });
  }

  relatedTo(nodeId: string, depth: number = 2): KnowledgeNode[] {
    const visited = new Set<string>([nodeId]);
    let frontier = [nodeId];
    for (let d = 0; d < depth; d++) {
      const nextFrontier: string[] = [];
      for (const current of frontier) {
        const connected = this.edges
          .filter(e => e.from === current || e.to === current)
          .map(e => e.from === current ? e.to : e.from)
          .filter(id => !visited.has(id));
        for (const id of connected) { visited.add(id); nextFrontier.push(id); }
      }
      frontier = nextFrontier;
    }
    visited.delete(nodeId);
    return [...visited].map(id => this.nodes.get(id)!).filter(Boolean);
  }

  graphStats(): { nodes: number; edges: number; types: Record<string, number> } {
    const types: Record<string, number> = {};
    for (const node of this.nodes.values()) types[node.type] = (types[node.type] || 0) + 1;
    return { nodes: this.nodes.size, edges: this.edges.length, types };
  }

  // ─── Persistence ───────────────────────────────────────────────────────

  save(): void {
    const data = { entries: this.entries, nodes: [...this.nodes.entries()], edges: this.edges };
    const dir = path.dirname(this.storePath);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(this.storePath, JSON.stringify(data));
  }

  load(): void {
    if (!fs.existsSync(this.storePath)) return;
    try {
      const data = JSON.parse(fs.readFileSync(this.storePath, 'utf-8'));
      this.entries = data.entries || [];
      this.nodes = new Map(data.nodes || []);
      this.edges = data.edges || [];
    } catch { /* fresh start */ }
  }

  clear(): void { this.entries = []; this.nodes.clear(); this.edges = []; }
  getSize(): number { return this.entries.length; }

  private trimMemory(): void {
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
