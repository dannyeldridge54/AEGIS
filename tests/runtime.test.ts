import * as fs from 'fs';
import * as os from 'os';
import * as path from 'path';
import * as http from 'http';
import { AegisAgent, AegisDaemon, Swarm, SelfEvolver, Memory } from '../src';
import { writeFileAtomic } from '../src/fs-util';

const tmp = () => fs.mkdtempSync(path.join(os.tmpdir(), 'aegis-test-'));

function get(port: number, p: string, host = '127.0.0.1'): Promise<{ status: number; headers: http.IncomingHttpHeaders; body: string }> {
  return new Promise((resolve, reject) => {
    http.get({ host, port, path: p }, (res) => {
      let body = '';
      res.on('data', (c) => (body += c));
      res.on('end', () => resolve({ status: res.statusCode || 0, headers: res.headers, body }));
    }).on('error', reject);
  });
}

describe('runtime behaviour', () => {
  let log: jest.SpyInstance;
  beforeAll(() => { log = jest.spyOn(console, 'log').mockImplementation(() => {}); });
  afterAll(() => log.mockRestore());

  test('agent.stop() works during a synchronous objective', async () => {
    let n = 0;
    const agent = new AegisAgent({
      id: 's', name: 's',
      // Always improving, so the run never converges on its own: only stop() can end it
      evaluate: () => { const t = Date.now(); while (Date.now() - t < 1) { /* busy */ } return -(n++); },
      parameters: [{ name: 'x', min: -1, max: 1 }],
    }, { verbosity: 'silent' }); // unlimited evals
    setTimeout(() => agent.stop('test'), 150);
    const state = await agent.run();
    expect(state.totalEvals).toBeGreaterThan(0);
    expect(state.totalEvals).toBeLessThan(1000);
  }, 5000);

  test('daemon API answers while a CPU-bound job runs, on localhost only, without wildcard CORS', async () => {
    const port = 40000 + Math.floor(Math.random() * 5000);
    const daemon = new AegisDaemon({ workDir: tmp(), apiPort: port, dashboardPort: 0, enableMemory: false });
    daemon.addJob({
      id: 'busy', name: 'busy', schedule: 'once',
      task: {
        id: 'busy', name: 'busy',
        evaluate: (p) => { const t = Date.now(); while (Date.now() - t < 1) { /* busy */ } return p.x ** 2; },
        parameters: [{ name: 'x', min: -1, max: 1 }],
      },
      config: { maxEvals: 3000 },
    });
    await daemon.start();
    try {
      await new Promise((r) => setTimeout(r, 1300)); // first tick starts the job
      const t0 = Date.now();
      const res = await get(port, '/api/status');
      expect(Date.now() - t0).toBeLessThan(500);
      expect(res.status).toBe(200);
      expect(res.headers['access-control-allow-origin']).toBeUndefined();
      expect(JSON.parse(res.body).jobs[0].status).toBe('running');
      const missing = await get(port, '/api/job/nope');
      expect(missing.status).toBe(404);
    } finally {
      daemon.stop();
    }
  }, 15000);

  test('swarm agents interleave', async () => {
    const order: string[] = [];
    const mk = (id: string) => ({
      id, name: id,
      evaluate: (p: Record<string, number>) => { order.push(id); const t = Date.now(); while (Date.now() - t < 1) { /* busy */ } return p.x ** 2; },
      parameters: [{ name: 'x', min: -1, max: 1 }],
    });
    const swarm = new Swarm();
    swarm.addAgent('a', mk('a'));
    swarm.addAgent('b', mk('b'));
    await swarm.run(200);
    // If agents were sequential, all 'a' evaluations would precede all 'b' evaluations
    expect(order.lastIndexOf('a')).toBeGreaterThan(order.indexOf('b'));
  });

  test('SelfEvolver keeps hyperparameters in range and returns a usable config', async () => {
    const evolver = new SelfEvolver({ generations: 4, populationSize: 6, mutationRate: 1 });
    const winner = await evolver.evolve({
      evaluate: (p) => (p.x - 0.3) ** 2 + (p.y + 0.2) ** 2,
      parameters: [{ name: 'x', min: -1, max: 1 }, { name: 'y', min: -1, max: 1 }],
    }, false);
    if (winner.type === 'annealing') {
      expect(winner.config.coolingRate).toBeLessThanOrEqual(0.999);
    }
    for (const v of Object.values(winner.config)) expect(Number.isFinite(v)).toBe(true);
  });

  test('SelfEvolver fitness reflects the genome (exploit beats random search)', async () => {
    const evolver = new SelfEvolver();
    const task = {
      evaluate: (p: Record<string, number>) => Object.values(p).reduce((s, v) => s + v * v, 0),
      parameters: Array.from({ length: 6 }, (_, i) => ({ name: `x${i}`, min: -5, max: 5 })),
    };
    let exploit = 0, curiosity = 0;
    for (let i = 0; i < 5; i++) {
      exploit += await evolver.evaluateGenome({ type: 'exploit', config: { mutationMagnitude: 0.05 }, fitness: 0, generation: 0 } as any, task, 300);
      curiosity += await evolver.evaluateGenome({ type: 'curiosity', config: {}, fitness: 0, generation: 0 } as any, task, 300);
    }
    expect(exploit).toBeGreaterThan(curiosity);
  });

  test('memory search with an empty query returns nothing', () => {
    const mem = new Memory(path.join(tmp(), 'm.json'));
    mem.remember({ type: 'fact', content: 'hello', tags: [], importance: 0.5 });
    expect(mem.search('   ')).toEqual([]);
    expect(mem.search('hello').length).toBe(1);
  });

  test('writeFileAtomic replaces content and leaves no temp files', () => {
    const dir = tmp();
    const f = path.join(dir, 'sub', 'state.json');
    writeFileAtomic(f, '1');
    writeFileAtomic(f, '2');
    expect(fs.readFileSync(f, 'utf-8')).toBe('2');
    expect(fs.readdirSync(path.dirname(f))).toEqual(['state.json']);
  });
});
