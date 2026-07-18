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
export interface MemoryEntry {
    id: string;
    type: 'fact' | 'episode' | 'strategy_insight' | 'code_pattern' | 'failure' | 'discovery';
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
    type: 'concept' | 'parameter' | 'strategy' | 'result' | 'code' | 'task';
    properties: Record<string, any>;
}
export interface KnowledgeEdge {
    from: string;
    to: string;
    relation: string;
    weight: number;
}
export declare class Memory {
    private entries;
    private nodes;
    private edges;
    private storePath;
    private maxEntries;
    constructor(storePath?: string);
    /** Remember something */
    remember(entry: Omit<MemoryEntry, 'id' | 'timestamp'>): string;
    /** Search memory by text (TF-IDF inspired scoring) */
    search(query: string, limit?: number): MemoryEntry[];
    /** Get recent memories */
    recent(n?: number, type?: MemoryEntry['type']): MemoryEntry[];
    /** Learn from an optimization run (auto-stores insights) */
    learnFromRun(taskName: string, result: {
        bestScore: number;
        bestParams: Record<string, number>;
        topStrategy: string;
        totalEvals: number;
        discoveries: number;
    }): void;
    /** Recall what worked for similar tasks */
    recallStrategy(taskDescription: string, nParams: number): string | null;
    /** Add a concept to the knowledge graph */
    addNode(node: KnowledgeNode): void;
    /** Connect two concepts */
    addEdge(from: string, to: string, relation: string, weight?: number): void;
    /** Find related concepts */
    relatedTo(nodeId: string, depth?: number): KnowledgeNode[];
    /** Get graph stats */
    graphStats(): {
        nodes: number;
        edges: number;
        types: Record<string, number>;
    };
    save(): void;
    load(): void;
    clear(): void;
    getSize(): number;
    private trimMemory;
}
//# sourceMappingURL=memory.d.ts.map