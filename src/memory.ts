/**
 * AEGIS — Persistent Memory System
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Long-term memory that persists across sessions:
 * - Knowledge graph (entities, relationships, facts)
 * - Episodic memory (past runs, what worked, what failed)
 * - Semantic search over memory
 * - Auto-learning from results
 */

import * as fs from 'fs';
import * as path from 'path';

export interface MemoryEntry {
  id: string;
  type: 'fact' | 'episode' | 'strategy_insight' | 'code_pattern' | 'failure' | 'discovery';
  content: string;
  tags: string[];
  importance: number; // 0-1
  timestamp: number;
  references?: string[]; // IDs of related entries
  metadata?: Record<string, any>;
}

export interface KnowledgeNode {
  id: string;
  label: string;
  type: 'concept' | 'parameter' | 'strategy' | 'result' | 'code' | 'task';
  properties: Record<string, any>;
}

export interface KnowledgeEdge {
  from: string;
  to: string;
  relation: string; // 'improves', 'causes', 'requires', 'contradicts', 'similar_to'
  weight: number;
}

export class Memory {
  private entries: MemoryEntry[] = [];
  private nodes: Map<string, KnowledgeNode> = new Map();
  private edges: KnowledgeEdge[] = [];
  private storePath: string;
  private maxEntries = 10000;

  constructor(storePath?: string) {
    this.storePath = storePath || path.join(process.cwd(), '.aegis-memory.json');
    this.load();
  }

  // ─── Episodic Memory ─────────────────────────────────────────────────────

  /** Remember something */
  remember(entry: Omit<MemoryEntry, 'id' | 'timestamp'>): string {
    const id = `mem_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
    this.entries.push({ ...entry, id, timestamp: Date.now() });
    this.trimMemory();
    return id;
  }

  /** Search memory by text (TF-IDF inspired scoring) */
  search(query: string, limit: number = 10): MemoryEntry[] {
    const terms = query.toLowerCase().split(/\s+/);
    const scored = this.entries.map(entry => {
      const text = `${entry.content} ${entry.tags.join(' ')}`.toLowerCase();
      let score = 0;
      for (const term of terms) {
        if (text.includes(term)) score += 1;
        // Exact match in tags gets bonus
        if (entry.tags.some(t => t.toLowerCase() === term)) score += 2;
      }
      // Recency bonus (decay over 7 days)
      const age = (Date.now() - entry.timestamp) / (7 * 24 * 3600000);
      score *= Math.exp(-age * 0.1);
      // Importance bonus
      score *= (1 + entry.importance);
      return { entry, score };
    }).filter(s => s.score > 0);

    scored.sort((a, b) => b.score - a.score);
    return scored.slice(0, limit).map(s => s.entry);
  }

  /** Get recent memories */
  recent(n: number = 20, type?: MemoryEntry['type']): MemoryEntry[] {
    let filtered = type ? this.entries.filter(e => e.type === type) : this.entries;
    return filtered.slice(-n);
  }

  /** Learn from an optimization run (auto-stores insights) */
  learnFromRun(taskName: string, result: {
    bestScore: number;
    bestParams: Record<string, number>;
    topStrategy: string;
    totalEvals: number;
    discoveries: number;
  }): void {
    this.remember({
      type: 'episode',
      content: `Task "${taskName}": best=${result.bestScore.toFixed(6)} after ${result.totalEvals} evals. Top strategy: ${result.topStrategy}. Params: ${JSON.stringify(result.bestParams)}`,
      tags: [taskName, result.topStrategy, 'optimization_result'],
      importance: Math.min(1, result.discoveries * 0.2 + 0.3),
    });

    // Store strategy insight
    this.remember({
      type: 'strategy_insight',
      content: `For "${taskName}" (${Object.keys(result.bestParams).length} params), ${result.topStrategy} performed best`,
      tags: [result.topStrategy, `${Object.keys(result.bestParams).length}d`],
      importance: 0.6,
    });
  }

  /** Recall what worked for similar tasks */
  recallStrategy(taskDescription: string, nParams: number): string | null {
    const insights = this.search(`${taskDescription} ${nParams}d strategy`, 5)
      .filter(e => e.type === 'strategy_insight');
    if (insights.length === 0) return null;
    // Extract strategy name from most relevant insight
    const match = insights[0].content.match(/(\w+) performed best/);
    return match?.[1] || null;
  }

  // ─── Knowledge Graph ─────────────────────────────────────────────────────

  /** Add a concept to the knowledge graph */
  addNode(node: KnowledgeNode): void {
    this.nodes.set(node.id, node);
  }

  /** Connect two concepts */
  addEdge(from: string, to: string, relation: string, weight: number = 1): void {
    this.edges.push({ from, to, relation, weight });
  }

  /** Find related concepts */
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
        for (const id of connected) {
          visited.add(id);
          nextFrontier.push(id);
        }
      }
      frontier = nextFrontier;
    }

    visited.delete(nodeId);
    return [...visited].map(id => this.nodes.get(id)!).filter(Boolean);
  }

  /** Get graph stats */
  graphStats(): { nodes: number; edges: number; types: Record<string, number> } {
    const types: Record<string, number> = {};
    for (const node of this.nodes.values()) {
      types[node.type] = (types[node.type] || 0) + 1;
    }
    return { nodes: this.nodes.size, edges: this.edges.length, types };
  }

  // ─── Persistence ─────────────────────────────────────────────────────────

  save(): void {
    const data = {
      entries: this.entries,
      nodes: [...this.nodes.entries()],
      edges: this.edges,
    };
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

  clear(): void {
    this.entries = [];
    this.nodes.clear();
    this.edges = [];
  }

  getSize(): number { return this.entries.length; }

  private trimMemory(): void {
    if (this.entries.length > this.maxEntries) {
      // Keep important + recent
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
