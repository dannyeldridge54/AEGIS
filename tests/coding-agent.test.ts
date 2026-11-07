import * as fs from 'fs';
import * as os from 'os';
import * as path from 'path';
import * as http from 'http';
import { Sandbox, CodingAgent, OpenAIProvider, LLMProvider } from '../src';

const tmp = () => fs.mkdtempSync(path.join(os.tmpdir(), 'aegis-sbx-'));

describe('coding agent safety', () => {
  const prevEnv = process.env.AEGIS_ALLOW_EXEC;
  beforeAll(() => { delete process.env.AEGIS_ALLOW_EXEC; });
  afterAll(() => { if (prevEnv !== undefined) process.env.AEGIS_ALLOW_EXEC = prevEnv; });

  test('execution is disabled unless explicitly enabled', async () => {
    const sb = new Sandbox({ workDir: tmp() });
    const r = await sb.execute('console.log("hi")', 'javascript');
    expect(r.success).toBe(false);
    expect(r.stderr).toMatch(/disabled/i);
    expect((await sb.shell('echo hi')).success).toBe(false);
  });

  test('execution works when enabled', async () => {
    const sb = new Sandbox({ workDir: tmp(), allowExec: true });
    const r = await sb.execute('console.log(6*7)', 'javascript');
    expect(r.success).toBe(true);
    expect(r.stdout.trim()).toBe('42');
  });

  test('paths outside the sandbox, including sibling prefixes, are blocked', () => {
    const dir = tmp();
    const sb = new Sandbox({ workDir: path.join(dir, 'box') });
    expect(() => sb.writeFile('../box-evil/x.txt', 'x')).toThrow(/outside sandbox/);
    expect(() => sb.writeFile('/etc/aegis-x', 'x')).toThrow(/outside sandbox/);
    expect(() => sb.writeFile('../../x', 'x')).toThrow(/outside sandbox/);
    expect(sb.writeFile('sub/ok.txt', 'ok')).toBe(path.join(dir, 'box', 'sub', 'ok.txt'));
  });

  test('generate() returns the auto-fixed code, not the first draft', async () => {
    const replies = [
      'Draft:\n```javascript\nmodule.exports = (a, b) => a - b;\n```',
      '```javascript\nmodule.exports = (a, b) => a + b;\n```',
    ];
    const provider: LLMProvider = {
      name: 'fake',
      chat: async () => replies.shift()!,
      generate: async () => replies.shift()!,
    };
    const agent = new CodingAgent({ provider, sandboxDir: tmp(), allowExec: true });
    const res = await agent.generate({
      goal: 'add two numbers',
      language: 'javascript',
      testCode: `const add = require(require('path').join(process.cwd(), 'main.js')); if (add(2, 3) !== 5) { console.error('bad'); process.exit(1); }`,
    });
    expect(res.testsPassed).toBe(true);
    expect(res.attempts).toBe(2);
    expect(res.code).toContain('a + b');
  });

  test('LLM HTTP errors are reported instead of returning empty text', async () => {
    const server = http.createServer((_, res) => { res.statusCode = 401; res.end('{"error":"bad key"}'); });
    await new Promise<void>((r) => server.listen(0, '127.0.0.1', r));
    const port = (server.address() as any).port;
    try {
      const llm = new OpenAIProvider({ apiKey: 'x', baseUrl: `http://127.0.0.1:${port}/v1` });
      await expect(llm.generate('hi')).rejects.toThrow(/HTTP 401/);
    } finally {
      server.close();
    }
  });
});
