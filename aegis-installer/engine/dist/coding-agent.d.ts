/**
 * AEGIS — Autonomous Coding Agent
 * Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
 *
 * Full coding AI agent with:
 * - Natural language → code generation
 * - Self-modification (rewrites own strategies)
 * - Sandboxed code execution + test runner
 * - Multi-file project generation
 * - Auto-debugging (fix failing tests)
 * - Code review and refactoring
 *
 * Supports: OpenAI, Ollama (local), Anthropic, or any OpenAI-compatible API
 */
export interface LLMProvider {
    name: string;
    generate(prompt: string, options?: GenerateOptions): Promise<string>;
    chat(messages: ChatMessage[], options?: GenerateOptions): Promise<string>;
}
export interface ChatMessage {
    role: 'system' | 'user' | 'assistant';
    content: string;
}
export interface GenerateOptions {
    temperature?: number;
    maxTokens?: number;
    model?: string;
    stop?: string[];
}
export declare class OpenAIProvider implements LLMProvider {
    name: string;
    private apiKey;
    private baseUrl;
    private defaultModel;
    constructor(config?: {
        apiKey?: string;
        baseUrl?: string;
        model?: string;
    });
    generate(prompt: string, options?: GenerateOptions): Promise<string>;
    chat(messages: ChatMessage[], options?: GenerateOptions): Promise<string>;
    private httpPost;
}
export declare class OllamaProvider implements LLMProvider {
    name: string;
    private baseUrl;
    private defaultModel;
    constructor(config?: {
        baseUrl?: string;
        model?: string;
    });
    generate(prompt: string, options?: GenerateOptions): Promise<string>;
    chat(messages: ChatMessage[], options?: GenerateOptions): Promise<string>;
}
export interface ExecutionResult {
    stdout: string;
    stderr: string;
    exitCode: number;
    duration: number;
    success: boolean;
}
export declare class Sandbox {
    private workDir;
    private timeout;
    private allowExec;
    constructor(config?: {
        workDir?: string;
        timeout?: number;
        allowExec?: boolean;
    });
    /** Validate that a path stays within the sandbox */
    private validatePath;
    /** Execute code in a sandboxed environment */
    execute(code: string, language?: string): Promise<ExecutionResult>;
    /** Execute a shell command (only within sandbox workDir) */
    shell(command: string): Promise<ExecutionResult>;
    /** Write a file to the sandbox (path-validated) */
    writeFile(relativePath: string, content: string): string;
    /** Read a file from the sandbox (path-validated) */
    readFile(relativePath: string): string | null;
    /** List files in sandbox */
    listFiles(subDir?: string): string[];
    /** Clean sandbox */
    clean(): void;
    getWorkDir(): string;
    private getExtension;
    private getCommand;
    private run;
}
export interface CodingTask {
    /** Natural language description of what to build/fix */
    goal: string;
    /** Target language */
    language?: string;
    /** Existing code to modify (if refactoring/fixing) */
    existingCode?: string;
    /** Test code to validate against */
    testCode?: string;
    /** File context (other related files) */
    context?: Array<{
        path: string;
        content: string;
    }>;
    /** Max attempts to fix failing tests */
    maxRetries?: number;
}
export interface CodingResult {
    code: string;
    language: string;
    files: Array<{
        path: string;
        content: string;
    }>;
    testsPassed: boolean;
    attempts: number;
    explanation: string;
    executionResult?: ExecutionResult;
}
export declare class CodingAgent {
    private llm;
    private sandbox;
    private memory;
    private maxMemory;
    constructor(config?: {
        provider?: LLMProvider;
        sandboxDir?: string;
        timeout?: number;
    });
    /** Generate code from natural language */
    generate(task: CodingTask): Promise<CodingResult>;
    /** Fix broken code given error output */
    fix(code: string, error: string, context?: string): Promise<string>;
    /** Refactor existing code */
    refactor(code: string, instructions: string): Promise<CodingResult>;
    /** Review code and suggest improvements */
    review(code: string): Promise<string>;
    /** Explain code in plain language */
    explain(code: string): Promise<string>;
    /** Generate tests for code */
    generateTests(code: string, framework?: string): Promise<string>;
    /** Generate entire project from description */
    generateProject(description: string, options?: {
        language?: string;
        framework?: string;
        features?: string[];
    }): Promise<Array<{
        path: string;
        content: string;
    }>>;
    /** Agent writes a new optimization strategy and registers it */
    evolveStrategy(problemDescription: string, currentBestStrategy: string, performanceData: string): Promise<string>;
    /** Interactive REPL-style coding session */
    chat(message: string): Promise<string>;
    /** Reset conversation memory */
    resetMemory(): void;
    /** Get sandbox for direct access */
    getSandbox(): Sandbox;
    private autoFix;
    private buildSystemPrompt;
    private buildGeneratePrompt;
    private extractCode;
    private extractFiles;
    private extractExplanation;
    private getExt;
    private addMemory;
}
/**
 * Create a coding agent with sensible defaults.
 *
 * @example
 * const coder = createCoder({ provider: 'openai' });
 * const result = await coder.generate({ goal: 'Build a REST API for todos' });
 */
export declare function createCoder(config?: {
    provider?: 'openai' | 'ollama' | LLMProvider;
    model?: string;
    apiKey?: string;
    baseUrl?: string;
    sandboxDir?: string;
}): CodingAgent;
//# sourceMappingURL=coding-agent.d.ts.map