/**
 * AEGIS — Auto-Documentation Generator
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Automatically generates README, API docs, and usage examples
 * from source code analysis (no LLM needed for basic docs).
 */
export interface DocConfig {
    projectName: string;
    description: string;
    author?: string;
    license?: string;
    sourceDir?: string;
    outputDir?: string;
}
/** Generate complete API documentation */
export declare function generateDocs(config: DocConfig): string;
/** Generate and write docs to file */
export declare function writeDocs(config: DocConfig): string;
//# sourceMappingURL=auto-docs.d.ts.map