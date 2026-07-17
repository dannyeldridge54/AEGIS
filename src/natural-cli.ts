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
      params.push({
        name: name.toLowerCase().replace(/\s+/g, '_'),
        min: parseFloat(match[2]),
        max: parseFloat(match[3]),
        description: name,
      });
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

      // Create a synthetic objective if no real one provided
      // In production, this would connect to the user's actual function
      const demoFn = (params: Record<string, number>) => {
        return Object.values(params).reduce((sum, v) => sum + v * v, 0);
      };

      const result = await optimize(demoFn, parsed.parameters!, {
        maxEvals: parsed.maxEvals,
        verbosity: verbose ? 'normal' : 'silent',
      });

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
