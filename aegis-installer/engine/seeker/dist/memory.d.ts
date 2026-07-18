/**
 * Seeker — Persistent Memory System
 * Records everything. Learns from every run.
 * Knowledge graph + episodic memory + semantic search.
 */
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
export declare class Memory {
    private entries;
    private nodes;
    private edges;
    private storePath;
    private maxEntries;
    constructor(storePath?: string);
    remember(entry: Omit<MemoryEntry, 'id' | 'timestamp'>): string;
    search(query: string, limit?: number): MemoryEntry[];
    recent(n?: number, type?: MemoryEntry['type']): MemoryEntry[];
    /** Record a full run with UFE metrics and discoveries */
    learnFromRun(taskName: string, result: {
        bestScore: number;
        bestParams: Record<string, number>;
        topStrategy: string;
        totalEvals: number;
        discoveries: number;
        ufe?: UFEMetrics;
        allDiscoveries?: Discovery[];
    }): void;
    recallStrategy(taskDescription: string, nParams: number): string | null;
    addNode(node: KnowledgeNode): void;
    addEdge(from: string, to: string, relation: string, weight?: number): void;
    relatedTo(nodeId: string, depth?: number): KnowledgeNode[];
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