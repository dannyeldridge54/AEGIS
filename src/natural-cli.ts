// Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights. AEGIS-ID: f62dce65987e3882
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

import { AegisAgent } from './agent';
import { Task, ParameterDef, AgentConfig } from './interfaces';
import { CodingAgent, createCoder } from './coding-agent';
import { optimize } from './agent';
import * as fs from 'fs';
import * as path from 'path';

type Objective = (params: Record<string, number>) => number | Promise<number>;

/**
 * Load an objective function from a JS (or, under ts-node, TS) module.
 * Accepts `module.exports = fn`, `export default fn`, or a named `evaluate`/`objective` export.
 */
export function loadObjective(modulePath: string): Objective {
  const resolved = path.resolve(modulePath);
  if (!fs.existsSync(resolved)) throw new Error(`Objective module not found: ${resolved}`);
  // eslint-disable-next-line @typescript-eslint/no-var-requires
  const mod = require(resolved);
  const fn = typeof mod === 'function' ? mod
    : typeof mod?.default === 'function' ? mod.default
    : typeof mod?.evaluate === 'function' ? mod.evaluate
    : typeof mod?.objective === 'function' ? mod.objective
    : null;
  if (!fn) throw new Error(`${resolved} must export a function (module.exports = fn, default, evaluate or objective)`);
  return fn;
}

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
export function parseNaturalLanguage(input: string): ParsedGoal {
  const lower = input.toLowerCase();

  // Detect coding tasks
  if (/\b(generate|create|build|write|make|code)\b.*\b(api|app|function|class|module|server|website|script)\b/i.test(input)) {
    return { type: 'code', objective: input, language: detectLanguage(input) };
  }
  if (/\b(review|check|audit|analyze)\b.*\b(code|file|bug|issue)\b/i.test(input)) {
    return { type: 'review', objective: input };
  }
  if (/\b(explain|what does|how does)\b/i.test(input)) {
    return { type: 'explain', objective: input };
  }
  if (/\b(test|write tests|generate tests)\b/i.test(input)) {
    return { type: 'test', objective: input };
  }

  // Detect optimization tasks
  const params = extractParameters(input);
  if (params.length > 0 || /\b(optimize|minimize|maximize|tune|find|search)\b/i.test(input)) {
    const minimize = !/\b(maximize|max)\b/i.test(input);
    return {
      type: 'optimize',
      parameters: params.length > 0 ? params : [{ name: 'x', min: -10, max: 10 }],
      objective: input,
      minimize,
      maxEvals: extractNumber(input, /(\d+)\s*(evals?|iterations?|tries)/i) || 3000,
    };
  }

  return { type: 'unknown', objective: input };
}

/** Extract parameter definitions from natural language */
function extractParameters(input: string): ParameterDef[] {
  const params: ParameterDef[] = [];

  // Pattern: "name (min-max)" or "name between min and max" or "name from min to max"
  const patterns = [
    /(\w+)\s*[\(（]\s*([\d.e-]+)\s*[-–to]+\s*([\d.e-]+)\s*[\)）]/gi,
    /(\w+)\s+(?:between|from)\s+([\d.e-]+)\s+(?:and|to)\s+([\d.e-]+)/gi,
    /(\w+)\s*:\s*([\d.e-]+)\s*[-–]\s*([\d.e-]+)/gi,
  ];

  for (const pattern of patterns) {
    let match;
    while ((match = pattern.exec(input)) !== null) {
      const name = match[1].replace(/^(the|my|a)\s*/i, '');
      const key = name.toLowerCase().replace(/\s+/g, '_');
      let lo = parseFloat(match[2]);
      let hi = parseFloat(match[3]);
      if (!Number.isFinite(lo) || !Number.isFinite(hi) || lo === hi) continue;
      if (lo > hi) [lo, hi] = [hi, lo];
      if (params.some(p => p.name === key)) continue;
      params.push({ name: key, min: lo, max: hi, description: name });
    }
  }

  // Common parameter names with sensible defaults
  if (params.length === 0) {
    const knownParams: Record<string, [number, number]> = {
      'learning_rate': [0.0001, 0.1], 'lr': [0.0001, 0.1],
      'dropout': [0, 0.8], 'batch_size': [8, 256],
      'layers': [1, 12], 'neurons': [16, 1024],
      'workers': [1, 64], 'threads': [1, 32],
      'cache': [64, 8192], 'timeout': [100, 30000],
      'temperature': [0, 2], 'epochs': [1, 100],
      'momentum': [0, 0.99], 'weight_decay': [0, 0.1],
    };

    for (const [name, [min, max]] of Object.entries(knownParams)) {
      if (input.toLowerCase().includes(name.replace('_', ' ')) || input.toLowerCase().includes(name)) {
        params.push({ name, min, max, description: name.replace('_', ' ') });
      }
    }
  }

  return params;
}

function extractNumber(input: string, pattern: RegExp): number | null {
  const match = input.match(pattern);
  return match ? parseInt(match[1]) : null;
}

function detectLanguage(input: string): string {
  const lower = input.toLowerCase();
  if (/\b(typescript|ts)\b/.test(lower)) return 'typescript';
  if (/\b(python|py)\b/.test(lower)) return 'python';
  if (/\b(rust)\b/.test(lower)) return 'rust';
  if (/\b(go|golang)\b/.test(lower)) return 'go';
  if (/\b(java)\b/.test(lower)) return 'java';
  if (/\b(ruby)\b/.test(lower)) return 'ruby';
  return 'typescript'; // default
}

// ─── Natural Language Runner ─────────────────────────────────────────────────

export async function runNatural(input: string, options?: {
  file?: string;
  verbose?: boolean;
  language?: string;
  /** Path to a module exporting the objective function to optimize */
  objective?: string;
  maxEvals?: number;
}): Promise<void> {
  const parsed = parseNaturalLanguage(input);
  const verbose = options?.verbose ?? true;

  if (verbose) {
    console.log(`\n🧠 Understood: ${parsed.type.toUpperCase()}`);
  }

  switch (parsed.type) {
    case 'optimize': {
      if (verbose) {
        console.log(`   Parameters: ${parsed.parameters!.map(p => `${p.name} [${p.min}, ${p.max}]`).join(', ')}`);
        console.log(`   Goal: ${parsed.minimize ? 'minimize' : 'maximize'}`);
        console.log(`   Budget: ${parsed.maxEvals} evaluations\n`);
      }

      let fn: Objective;
      if (options?.objective) {
        fn = loadObjective(options.objective);
      } else {
        // Without a real objective there is nothing meaningful to optimize: say so plainly
        console.log('⚠  No objective given (--objective <file.js>). Running a DEMO objective');
        console.log('   (sum of squares of the parameters); the result says nothing about your problem.\n');
        fn = (params) => Object.values(params).reduce((sum, v) => sum + v * v, 0);
      }

      const result = await optimize(fn, parsed.parameters!, {
        maxEvals: options?.maxEvals || parsed.maxEvals,
        verbosity: verbose ? 'normal' : 'silent',
        goal: { description: input, minimize: parsed.minimize !== false },
      });

      if (!Number.isFinite(result.score)) {
        console.log(`\n⚠  No valid score: the objective returned NaN/Infinity for every point.`);
        console.log(`   It received only: ${parsed.parameters!.map(p => p.name).join(', ')}.`);
        console.log(`   Name every parameter it uses with a range, e.g. "layers between 1 and 12".`);
        break;
      }
      console.log(`\n✅ Optimization complete!`);
      console.log(`   Best score: ${result.score.toFixed(6)}`);
      console.log(`   Parameters: ${JSON.stringify(result.params, null, 2)}`);
      break;
    }

    case 'code': {
      const coder = createCoder();
      if (verbose) console.log(`   Language: ${parsed.language}\n   Generating...\n`);
      const result = await coder.generate({
        goal: parsed.objective!,
        language: parsed.language || options?.language,
      });
      console.log(result.explanation || '');
      console.log(`\n\`\`\`${result.language}\n${result.code}\n\`\`\``);
      if (result.files.length > 1) {
        console.log(`\n📁 ${result.files.length} files generated`);
      }
      break;
    }

    case 'review': {
      const coder = createCoder();
      let code = '';
      if (options?.file && fs.existsSync(options.file)) {
        code = fs.readFileSync(options.file, 'utf-8');
      } else {
        console.log('⚠ No file specified. Use --file <path>');
        return;
      }
      const review = await coder.review(code);
      console.log(review);
      break;
    }

    case 'explain': {
      const coder = createCoder();
      let code = '';
      if (options?.file && fs.existsSync(options.file)) {
        code = fs.readFileSync(options.file, 'utf-8');
      } else {
        console.log('⚠ No file specified. Use --file <path>');
        return;
      }
      const explanation = await coder.explain(code);
      console.log(explanation);
      break;
    }

    case 'test': {
      const coder = createCoder();
      let code = '';
      if (options?.file && fs.existsSync(options.file)) {
        code = fs.readFileSync(options.file, 'utf-8');
      }
      const tests = await coder.generateTests(code);
      console.log(tests);
      break;
    }

    default:
      console.log(`🤔 Not sure what to do with: "${input}"`);
      console.log('   Try: "optimize X between A and B" or "generate a REST API"');
  }
}
