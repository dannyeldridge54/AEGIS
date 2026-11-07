// Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights. AEGIS-ID: 4309fcdb32ec33c8
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

import * as fs from 'fs';
import * as path from 'path';
import * as http from 'http';
import * as https from 'https';
import { exec, execSync, ExecException } from 'child_process';

// ─── LLM Provider Interface ─────────────────────────────────────────────────

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

// ─── HTTP helper ─────────────────────────────────────────────────────────────

/** POST JSON with a timeout; rejects on network errors and non-2xx responses. */
function postJSON(url: string, body: string, headers: Record<string, string>, timeoutMs: number): Promise<string> {
  return new Promise((resolve, reject) => {
    const parsed = new URL(url);
    const lib = parsed.protocol === 'https:' ? https : http;
    const req = lib.request({
      hostname: parsed.hostname,
      port: parsed.port,
      path: parsed.pathname + parsed.search,
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...headers, 'Content-Length': Buffer.byteLength(body) },
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        const status = res.statusCode || 0;
        if (status < 200 || status >= 300) {
          reject(new Error(`LLM request to ${parsed.host} failed: HTTP ${status} ${data.slice(0, 300)}`));
        } else {
          resolve(data);
        }
      });
    });
    req.setTimeout(timeoutMs, () => req.destroy(new Error(`LLM request to ${parsed.host} timed out after ${timeoutMs} ms`)));
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

// ─── OpenAI Provider ─────────────────────────────────────────────────────────

export class OpenAIProvider implements LLMProvider {
  name = 'openai';
  private apiKey: string;
  private baseUrl: string;
  private defaultModel: string;
  private timeoutMs: number;

  constructor(config?: { apiKey?: string; baseUrl?: string; model?: string; timeoutMs?: number }) {
    this.apiKey = config?.apiKey || process.env.OPENAI_API_KEY || '';
    this.baseUrl = (config?.baseUrl || 'https://api.openai.com/v1').replace(/\/+$/, '');
    this.defaultModel = config?.model || 'gpt-4o-mini';
    this.timeoutMs = config?.timeoutMs || 120000;
  }

  async generate(prompt: string, options?: GenerateOptions): Promise<string> {
    return this.chat([{ role: 'user', content: prompt }], options);
  }

  async chat(messages: ChatMessage[], options?: GenerateOptions): Promise<string> {
    const body = JSON.stringify({
      model: options?.model || this.defaultModel,
      messages,
      temperature: options?.temperature ?? 0.7,
      max_tokens: options?.maxTokens ?? 4096,
      stop: options?.stop,
    });

    const response = await postJSON(`${this.baseUrl}/chat/completions`, body, {
      'Authorization': `Bearer ${this.apiKey}`,
    }, this.timeoutMs);

    const data = JSON.parse(response);
    return data.choices?.[0]?.message?.content || '';
  }
}

// ─── Ollama Provider (Local LLM) ─────────────────────────────────────────────

export class OllamaProvider implements LLMProvider {
  name = 'ollama';
  private baseUrl: string;
  private defaultModel: string;
  private timeoutMs: number;

  constructor(config?: { baseUrl?: string; model?: string; timeoutMs?: number }) {
    this.baseUrl = (config?.baseUrl || 'http://localhost:11434').replace(/\/+$/, '');
    this.defaultModel = config?.model || 'llama3.2';
    this.timeoutMs = config?.timeoutMs || 300000; // local models can be slow
  }

  async generate(prompt: string, options?: GenerateOptions): Promise<string> {
    return this.chat([{ role: 'user', content: prompt }], options);
  }

  async chat(messages: ChatMessage[], options?: GenerateOptions): Promise<string> {
    const body = JSON.stringify({
      model: options?.model || this.defaultModel,
      messages,
      stream: false,
      options: {
        temperature: options?.temperature ?? 0.7,
        num_predict: options?.maxTokens ?? 4096,
      },
    });

    const data = await postJSON(`${this.baseUrl}/api/chat`, body, {}, this.timeoutMs);
    try {
      return JSON.parse(data).message?.content || '';
    } catch {
      return data;
    }
  }
}

// ─── Sandbox Execution Engine ────────────────────────────────────────────────

export interface ExecutionResult {
  stdout: string;
  stderr: string;
  exitCode: number;
  duration: number;
  success: boolean;
}

/**
 * Working directory for generated code.
 *
 * NOT a security boundary: when execution is enabled, code runs as your user with
 * full access to your files and network. Execution is therefore off unless you pass
 * `allowExec: true` (or set AEGIS_ALLOW_EXEC=1). Use a VM/container for untrusted code.
 */
export class Sandbox {
  private workDir: string;
  private timeout: number;
  private allowExec: boolean;

  constructor(config?: { workDir?: string; timeout?: number; allowExec?: boolean }) {
    this.workDir = path.resolve(config?.workDir || path.join(process.cwd(), '.aegis-sandbox'));
    this.timeout = config?.timeout || 30000;
    this.allowExec = config?.allowExec ?? process.env.AEGIS_ALLOW_EXEC === '1'; // opt-in only
    if (!fs.existsSync(this.workDir)) fs.mkdirSync(this.workDir, { recursive: true });
  }

  /** Validate that a path stays within the sandbox */
  private validatePath(relativePath: string): string {
    const resolved = path.resolve(this.workDir, relativePath);
    const rel = path.relative(this.workDir, resolved);
    // `startsWith(workDir)` alone would also accept sibling dirs such as "<workDir>-evil"
    if (rel === '' || rel.startsWith('..') || path.isAbsolute(rel)) {
      throw new Error(`Path traversal blocked: "${relativePath}" resolves outside sandbox`);
    }
    return resolved;
  }

  /** Execute code in a sandboxed environment */
  async execute(code: string, language: string = 'typescript'): Promise<ExecutionResult> {
    if (!this.allowExec) {
      return { stdout: '', stderr: EXEC_DISABLED, exitCode: 1, success: false, duration: 0 };
    }
    const start = Date.now();
    const ext = this.getExtension(language);
    const filename = `aegis_run_${Date.now()}${ext}`;
    const filepath = path.join(this.workDir, filename);

    fs.writeFileSync(filepath, code);

    try {
      const cmd = this.getCommand(filepath, language);
      const result = await this.run(cmd);
      return { ...result, duration: Date.now() - start };
    } finally {
      try { fs.unlinkSync(filepath); } catch {}
      try { fs.unlinkSync(`${filepath}.exe`); } catch {}
    }
  }

  /** Execute a shell command (only within sandbox workDir) */
  async shell(command: string): Promise<ExecutionResult> {
    if (!this.allowExec) {
      return { stdout: '', stderr: EXEC_DISABLED, exitCode: 1, success: false, duration: 0 };
    }
    const start = Date.now();
    const result = await this.run(command);
    return { ...result, duration: Date.now() - start };
  }

  /** Write a file to the sandbox (path-validated) */
  writeFile(relativePath: string, content: string): string {
    const fullPath = this.validatePath(relativePath);
    const dir = path.dirname(fullPath);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(fullPath, content);
    return fullPath;
  }

  /** Read a file from the sandbox (path-validated) */
  readFile(relativePath: string): string | null {
    const fullPath = this.validatePath(relativePath);
    return fs.existsSync(fullPath) ? fs.readFileSync(fullPath, 'utf-8') : null;
  }

  /** List files in sandbox */
  listFiles(subDir?: string): string[] {
    const dir = subDir ? this.validatePath(subDir) : this.workDir;
    if (!fs.existsSync(dir)) return [];
    return fs.readdirSync(dir, { recursive: true }).map(String);
  }

  /** Clean sandbox */
  clean(): void {
    if (fs.existsSync(this.workDir)) {
      fs.rmSync(this.workDir, { recursive: true, force: true });
      fs.mkdirSync(this.workDir, { recursive: true });
    }
  }

  getWorkDir(): string { return this.workDir; }
  canExecute(): boolean { return this.allowExec; }

  private getExtension(lang: string): string {
    const map: Record<string, string> = {
      typescript: '.ts', javascript: '.js', python: '.py',
      rust: '.rs', go: '.go', c: '.c', cpp: '.cpp', java: '.java',
      ruby: '.rb', php: '.php', shell: '.sh', bash: '.sh',
    };
    return map[lang.toLowerCase()] || '.txt';
  }

  private getCommand(filepath: string, lang: string): string {
    const map: Record<string, string> = {
      typescript: `npx ts-node "${filepath}"`,
      javascript: `node "${filepath}"`,
      python: `python "${filepath}"`,
      rust: `rustc "${filepath}" -o "${filepath}.exe" && "${filepath}.exe"`,
      go: `go run "${filepath}"`,
      ruby: `ruby "${filepath}"`,
      php: `php "${filepath}"`,
      shell: `bash "${filepath}"`,
      bash: `bash "${filepath}"`,
    };
    return map[lang.toLowerCase()] || `node "${filepath}"`;
  }

  private run(cmd: string): Promise<{ stdout: string; stderr: string; exitCode: number; success: boolean }> {
    return new Promise((resolve) => {
      exec(cmd, {
        timeout: this.timeout,
        cwd: this.workDir,
        maxBuffer: 10 * 1024 * 1024,
      }, (error: ExecException | null, stdout: string, stderr: string) => {
        resolve({
          stdout: stdout || '',
          stderr: stderr || '',
          exitCode: typeof error?.code === 'number' ? error.code : (error ? 1 : 0),
          success: !error,
        });
      });
    });
  }
}

const EXEC_DISABLED = 'Execution disabled: generated code runs with your full user permissions. '
  + 'Pass allowExec: true (or set AEGIS_ALLOW_EXEC=1) to enable it, ideally inside a VM or container.';

// ─── Coding Agent ────────────────────────────────────────────────────────────

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
  context?: Array<{ path: string; content: string }>;
  /** Max attempts to fix failing tests */
  maxRetries?: number;
}

export interface CodingResult {
  code: string;
  language: string;
  files: Array<{ path: string; content: string }>;
  testsPassed: boolean;
  attempts: number;
  explanation: string;
  executionResult?: ExecutionResult;
}

export class CodingAgent {
  private llm: LLMProvider;
  private sandbox: Sandbox;
  private memory: ChatMessage[] = [];
  private maxMemory = 50;

  constructor(config?: {
    provider?: LLMProvider;
    sandboxDir?: string;
    timeout?: number;
    /** Run generated code (default false — it runs with your full permissions) */
    allowExec?: boolean;
  }) {
    this.llm = config?.provider || new OllamaProvider();
    this.sandbox = new Sandbox({
      workDir: config?.sandboxDir,
      timeout: config?.timeout || 30000,
      allowExec: config?.allowExec,
    });
  }

  // ─── Core Capabilities ───────────────────────────────────────────────────

  /** Generate code from natural language */
  async generate(task: CodingTask): Promise<CodingResult> {
    const lang = task.language || 'typescript';
    const systemPrompt = this.buildSystemPrompt(lang);
    const userPrompt = this.buildGeneratePrompt(task);

    const messages: ChatMessage[] = [
      { role: 'system', content: systemPrompt },
      ...this.memory.slice(-20),
      { role: 'user', content: userPrompt },
    ];

    const response = await this.llm.chat(messages, { temperature: 0.3 });
    const code = this.extractCode(response, lang);
    const files = this.extractFiles(response);

    this.addMemory('user', userPrompt);
    this.addMemory('assistant', response);

    // Write and execute
    if (files.length > 0) {
      for (const f of files) this.sandbox.writeFile(f.path, f.content);
    } else {
      this.sandbox.writeFile(`main${this.getExt(lang)}`, code);
    }

    let testsPassed = false;
    let attempts = 0;
    let lastResult: ExecutionResult | undefined;
    let finalCode = code;

    // Run tests if provided
    if (task.testCode) {
      const maxRetries = task.maxRetries || 3;
      let currentCode = code;

      while (attempts < maxRetries && !testsPassed) {
        attempts++;
        this.sandbox.writeFile(`test${this.getExt(lang)}`, task.testCode);
        this.sandbox.writeFile(`main${this.getExt(lang)}`, currentCode);
        lastResult = await this.sandbox.execute(task.testCode, lang);

        if (lastResult.success) {
          testsPassed = true;
        } else if (!this.sandbox.canExecute()) {
          break; // nothing to fix: the tests were never run
        } else if (attempts < maxRetries) {
          // Auto-fix: send error back to LLM
          currentCode = await this.autoFix(currentCode, lastResult, task, lang);
        }
      }
      finalCode = currentCode;
      if (files.length === 0) this.sandbox.writeFile(`main${this.getExt(lang)}`, finalCode);
    } else {
      // Just run the code
      lastResult = await this.sandbox.execute(code, lang);
      testsPassed = lastResult.success;
      attempts = 1;
    }

    return {
      code: finalCode, // the auto-fixed version, not the first draft
      language: lang,
      files: files.length > 0 ? files : [{ path: `main${this.getExt(lang)}`, content: finalCode }],
      testsPassed,
      attempts,
      explanation: this.extractExplanation(response),
      executionResult: lastResult,
    };
  }

  /** Fix broken code given error output */
  async fix(code: string, error: string, context?: string): Promise<string> {
    const prompt = `Fix this code. Error:\n\`\`\`\n${error}\n\`\`\`\n\nCode:\n\`\`\`\n${code}\n\`\`\`${context ? `\n\nContext: ${context}` : ''}\n\nReturn ONLY the fixed code in a code block.`;

    const response = await this.llm.generate(prompt, { temperature: 0.2 });
    return this.extractCode(response, 'typescript');
  }

  /** Refactor existing code */
  async refactor(code: string, instructions: string): Promise<CodingResult> {
    return this.generate({
      goal: `Refactor this code: ${instructions}`,
      existingCode: code,
    });
  }

  /** Review code and suggest improvements */
  async review(code: string): Promise<string> {
    const prompt = `Review this code for bugs, performance issues, and improvements. Be specific and actionable:\n\n\`\`\`\n${code}\n\`\`\``;
    return this.llm.generate(prompt, { temperature: 0.3 });
  }

  /** Explain code in plain language */
  async explain(code: string): Promise<string> {
    const prompt = `Explain this code clearly and concisely. What does it do, how does it work, and are there any issues?\n\n\`\`\`\n${code}\n\`\`\``;
    return this.llm.generate(prompt, { temperature: 0.3 });
  }

  /** Generate tests for code */
  async generateTests(code: string, framework?: string): Promise<string> {
    const fw = framework || 'jest';
    const prompt = `Write comprehensive tests for this code using ${fw}. Cover edge cases, error paths, and typical usage:\n\n\`\`\`\n${code}\n\`\`\`\n\nReturn only the test code.`;
    const response = await this.llm.generate(prompt, { temperature: 0.3 });
    return this.extractCode(response, 'typescript');
  }

  /** Generate entire project from description */
  async generateProject(description: string, options?: {
    language?: string;
    framework?: string;
    features?: string[];
  }): Promise<Array<{ path: string; content: string }>> {
    const lang = options?.language || 'typescript';
    const prompt = `Generate a complete ${lang} project:\n\nDescription: ${description}\n${options?.framework ? `Framework: ${options.framework}\n` : ''}${options?.features ? `Features: ${options.features.join(', ')}\n` : ''}\n\nReturn ALL files with their paths in this format:\n--- FILE: path/to/file.ts ---\n\`\`\`typescript\n// code here\n\`\`\`\n\nInclude: package.json, main source files, tests, README.`;

    const response = await this.llm.chat([
      { role: 'system', content: 'You are an expert software architect. Generate complete, production-ready project files.' },
      { role: 'user', content: prompt },
    ], { temperature: 0.4, maxTokens: 8192 });

    return this.extractFiles(response);
  }

  // ─── Self-Modification ───────────────────────────────────────────────────

  /** Agent writes a new optimization strategy and registers it */
  async evolveStrategy(
    problemDescription: string,
    currentBestStrategy: string,
    performanceData: string
  ): Promise<string> {
    const prompt = `You are AEGIS, a self-improving optimization agent.

Current best strategy: ${currentBestStrategy}
Performance data: ${performanceData}
Problem: ${problemDescription}

Write a NEW TypeScript optimization strategy function that could outperform the current one.
The function signature must be:
\`\`\`typescript
function suggest(params: Array<{name: string, min: number, max: number}>, best: {params: Record<string,number>, score: number} | null, history: Array<{params: Record<string,number>, score: number}>): Record<string, number>
\`\`\`

Be creative. Use mathematical insights. Think about what the current strategy misses.
Return ONLY the function code.`;

    const response = await this.llm.generate(prompt, { temperature: 0.8 });
    const code = this.extractCode(response, 'typescript');

    // Validate the generated strategy in sandbox
    const testWrapper = `
${code}
// Quick validation
const params = [{name:'x', min:-5, max:5}, {name:'y', min:-5, max:5}];
const result = suggest(params, null, []);
console.log(JSON.stringify(result));
if (typeof result.x !== 'number' || typeof result.y !== 'number') throw new Error('Invalid output');
console.log('STRATEGY_VALID');
`;

    const execResult = await this.sandbox.execute(testWrapper, 'typescript');
    if (execResult.stdout.includes('STRATEGY_VALID') || !this.sandbox.canExecute()) {
      return code; // unvalidated when execution is disabled
    }

    // Retry with fix
    const fixed = await this.fix(code, execResult.stderr, 'This should be a valid optimization strategy function');
    return fixed;
  }

  /** Interactive REPL-style coding session */
  async chat(message: string): Promise<string> {
    this.addMemory('user', message);

    const messages: ChatMessage[] = [
      { role: 'system', content: CODING_SYSTEM_PROMPT },
      ...this.memory.slice(-30),
    ];

    const response = await this.llm.chat(messages, { temperature: 0.5 });
    this.addMemory('assistant', response);

    // Auto-execute code blocks if present
    const code = this.extractCode(response, 'typescript');
    // Only when execution was explicitly enabled; never just because the reply says "run"
    if (this.sandbox.canExecute() && code && response.includes('```') && /\brun (it|this)\b/i.test(message)) {
      const result = await this.sandbox.execute(code, 'typescript');
      if (result.stdout) {
        return `${response}\n\n**Output:**\n\`\`\`\n${result.stdout}\n\`\`\``;
      }
    }

    return response;
  }

  /** Reset conversation memory */
  resetMemory(): void {
    this.memory = [];
  }

  /** Get sandbox for direct access */
  getSandbox(): Sandbox { return this.sandbox; }

  // ─── Internal ────────────────────────────────────────────────────────────

  private async autoFix(code: string, error: ExecutionResult, task: CodingTask, lang: string): Promise<string> {
    const fixPrompt = `The code failed tests. Fix it.

ERROR:
${error.stderr || error.stdout}

ORIGINAL GOAL: ${task.goal}

CURRENT CODE:
\`\`\`${lang}
${code}
\`\`\`

Return ONLY the corrected code in a code block.`;

    const response = await this.llm.generate(fixPrompt, { temperature: 0.2 });
    return this.extractCode(response, lang);
  }

  private buildSystemPrompt(lang: string): string {
    return `You are AEGIS Coding Agent — an autonomous AI programmer.
Language: ${lang}
Rules:
- Write clean, production-quality code
- Include error handling and edge cases
- Use modern language features
- Be concise but complete
- Always wrap code in \`\`\` blocks with language tag
- If multiple files needed, use --- FILE: path --- markers`;
  }

  private buildGeneratePrompt(task: CodingTask): string {
    let prompt = `GOAL: ${task.goal}\n`;
    if (task.existingCode) prompt += `\nEXISTING CODE:\n\`\`\`\n${task.existingCode}\n\`\`\`\n`;
    if (task.testCode) prompt += `\nTESTS TO PASS:\n\`\`\`\n${task.testCode}\n\`\`\`\n`;
    if (task.context?.length) {
      prompt += '\nCONTEXT FILES:\n';
      for (const f of task.context) {
        prompt += `--- ${f.path} ---\n\`\`\`\n${f.content}\n\`\`\`\n`;
      }
    }
    prompt += '\nGenerate the code. Explain your approach briefly, then provide the complete implementation.';
    return prompt;
  }

  private extractCode(response: string, lang: string): string {
    // Try language-specific code block
    const patterns = [
      new RegExp('```' + lang + '\\s*\\n([\\s\\S]*?)```', 'i'),
      new RegExp('```(?:ts|typescript|js|javascript|python|py)\\s*\\n([\\s\\S]*?)```', 'i'),
      /```\s*\n([\s\S]*?)```/,
    ];

    for (const pattern of patterns) {
      const match = response.match(pattern);
      if (match) return match[1].trim();
    }

    return response.trim();
  }

  private extractFiles(response: string): Array<{ path: string; content: string }> {
    const files: Array<{ path: string; content: string }> = [];
    const filePattern = /---\s*FILE:\s*(.+?)\s*---\s*\n```[\w]*\n([\s\S]*?)```/gi;

    let match;
    while ((match = filePattern.exec(response)) !== null) {
      files.push({ path: match[1].trim(), content: match[2].trim() });
    }

    return files;
  }

  private extractExplanation(response: string): string {
    // Get text before first code block
    const idx = response.indexOf('```');
    if (idx > 0) return response.slice(0, idx).trim();
    return '';
  }

  private getExt(lang: string): string {
    const map: Record<string, string> = {
      typescript: '.ts', javascript: '.js', python: '.py',
      rust: '.rs', go: '.go', ruby: '.rb',
    };
    return map[lang.toLowerCase()] || '.ts';
  }

  private addMemory(role: 'user' | 'assistant', content: string): void {
    this.memory.push({ role, content });
    if (this.memory.length > this.maxMemory) {
      this.memory = this.memory.slice(-this.maxMemory / 2);
    }
  }
}

// ─── System Prompt ───────────────────────────────────────────────────────────

const CODING_SYSTEM_PROMPT = `You are AEGIS — an autonomous coding agent with these capabilities:
1. Generate code from natural language descriptions
2. Fix bugs given error output
3. Refactor and improve existing code
4. Write comprehensive tests
5. Generate entire projects from scratch
6. Review code for issues
7. Explain complex code simply
8. Self-improve by writing new optimization strategies

You write clean, modern, production-quality code.
You always handle errors and edge cases.
You prefer TypeScript but support all languages.
You are concise but thorough.

When you write code, always use fenced code blocks with the language specified.
When generating multiple files, use: --- FILE: path/to/file ---`;

// ─── Convenience Factory ─────────────────────────────────────────────────────

/**
 * Create a coding agent with sensible defaults.
 *
 * @example
 * const coder = createCoder({ provider: 'openai' });
 * const result = await coder.generate({ goal: 'Build a REST API for todos' });
 */
export function createCoder(config?: {
  provider?: 'openai' | 'ollama' | LLMProvider;
  model?: string;
  apiKey?: string;
  baseUrl?: string;
  sandboxDir?: string;
  allowExec?: boolean;
}): CodingAgent {
  let provider: LLMProvider;

  if (config?.provider && typeof config.provider === 'object') {
    provider = config.provider;
  } else if (config?.provider === 'openai') {
    provider = new OpenAIProvider({
      apiKey: config.apiKey,
      baseUrl: config.baseUrl,
      model: config.model,
    });
  } else {
    provider = new OllamaProvider({
      baseUrl: config?.baseUrl,
      model: config?.model,
    });
  }

  return new CodingAgent({ provider, sandboxDir: config?.sandboxDir, allowExec: config?.allowExec });
}
