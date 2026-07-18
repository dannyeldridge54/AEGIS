/**
 * AEGIS — Natural Language CLI
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Talk to AEGIS in plain English. No code needed.
 *
 * Examples:
 *   aegis "optimize my neural network learning rate between 0.0001 and 0.1"
 *   aegis "find the minimum of x² + y² + z²"
 *   aegis "tune server workers (1-64) and cache (64-4096 MB) to minimize latency"
 *   aegis "generate a REST API for todo items"
 *   aegis "review this file for bugs" --file src/main.ts
 */
import { ParameterDef } from './interfaces';
interface ParsedGoal {
    type: 'optimize' | 'code' | 'review' | 'explain' | 'test' | 'unknown';
    parameters?: ParameterDef[];
    objective?: string;
    minimize?: boolean;
    language?: string;
    code?: string;
    maxEvals?: number;
}
/** Parse natural language into structured task */
export declare function parseNaturalLanguage(input: string): ParsedGoal;
export declare function runNatural(input: string, options?: {
    file?: string;
    verbose?: boolean;
    language?: string;
}): Promise<void>;
export {};
//# sourceMappingURL=natural-cli.d.ts.map