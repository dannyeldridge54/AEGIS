import { parallelOptimize } from '../src/parallel';
import { Swarm } from '../src/swarm';
import { SelfEvolver } from '../src/self-evolve';
import { multiOptimize } from '../src/multi-objective';
import { DataRecorder } from '../src/recorder';
import { Task } from '../src/interfaces';
import * as fs from 'fs';
import * as path from 'path';

const simpleTask: Task = {
  id: 'test', name: 'Test Quadratic',
  evaluate: (p) => (p.x - 2) ** 2 + (p.y + 1) ** 2,
  parameters: [
    { name: 'x', min: -10, max: 10 },
    { name: 'y', min: -10, max: 10 },
  ],
};

describe('Parallel Optimizer', () => {
  test('finds minimum with UFE tracking', async () => {
    const state = await parallelOptimize(simpleTask, {
      maxEvals: 500, concurrency: 4, verbosity: 'silent', seed: 42,
    });

    expect(state.best).not.toBeNull();
    expect(state.best!.score).toBeLessThan(10);
    expect(state.totalEvals).toBe(500);
    expect(state.ufe.totalEvals).toBe(500);
    expect(state.ufe.usefulEvals).toBeGreaterThan(0);
    expect(state.ufe.convergenceCurve.length).toBeGreaterThan(0);
  });

  test('deterministic with same seed', async () => {
    const a = await parallelOptimize(simpleTask, { maxEvals: 200, verbosity: 'silent', seed: 99 });
    const b = await parallelOptimize(simpleTask, { maxEvals: 200, verbosity: 'silent', seed: 99 });
    expect(a.best!.score).toBe(b.best!.score);
  });
});

describe('Swarm', () => {
  test('runs agents in parallel and finds global best', async () => {
    const swarm = new Swarm({ seed: 42 });
    swarm.addAgent('a', simpleTask, 'explorer', { maxEvals: 200 });
    swarm.addAgent('b', simpleTask, 'exploiter', { maxEvals: 200 });

    const result = await swarm.run();
    expect(result.globalBest).not.toBeNull();
    expect(result.agentResults.length).toBe(2);
    expect(result.totalEvals).toBeGreaterThan(0);
  });

  test('partition divides parameter space', async () => {
    const swarm = Swarm.partition(simpleTask, 3, { maxEvals: 300, seed: 42 });
    expect(swarm.getAgentCount()).toBe(3);

    const result = await swarm.run();
    expect(result.globalBest).not.toBeNull();
  });
});

describe('Self-Evolve', () => {
  test('evolves strategy hyperparameters', async () => {
    const evolver = new SelfEvolver({ generations: 3, populationSize: 6, seed: 42 });
    const result = await evolver.evolve({
      evaluate: (p) => (p.x - 1) ** 2,
      parameters: [{ name: 'x', min: -5, max: 5 }],
    }, false);

    expect(result.type).toBeDefined();
    expect(result.config).toBeDefined();
  });
});

describe('Multi-Objective', () => {
  test('finds Pareto front', async () => {
    const result = await multiOptimize(
      [
        { name: 'f1', evaluate: (p) => p.x ** 2, minimize: true },
        { name: 'f2', evaluate: (p) => (p.x - 2) ** 2, minimize: true },
      ],
      [{ name: 'x', min: -5, max: 5 }],
      { maxEvals: 500, verbosity: 'silent', seed: 42 },
    );

    expect(result.solutions.length).toBeGreaterThan(0);
    expect(result.ufe.totalEvals).toBe(500);
    expect(result.totalEvals).toBe(500);
  });
});

describe('DataRecorder', () => {
  const testDir = path.join(__dirname, '.test-recorder-output');

  beforeAll(() => {
    if (!fs.existsSync(testDir)) fs.mkdirSync(testDir, { recursive: true });
  });

  afterAll(() => {
    if (fs.existsSync(testDir)) {
      fs.rmSync(testDir, { recursive: true });
    }
  });

  test('writes eval CSV and discovery JSONL', async () => {
    const recorder = new DataRecorder({ dir: testDir, runId: 'test-run' });
    recorder.init(['x', 'y']);

    recorder.recordEval({ params: { x: 1, y: 2 }, score: 5, timestamp: Date.now(), strategy: 'random' }, true);
    recorder.recordEval({ params: { x: 3, y: 4 }, score: 3, timestamp: Date.now(), strategy: 'gradient' }, false);

    recorder.recordDiscovery({
      type: 'anomaly', description: 'test anomaly',
      result: { params: { x: 1, y: 2 }, score: 5, timestamp: Date.now(), strategy: 'random' },
      confidence: 0.9, timestamp: Date.now(),
    });

    recorder.close();

    // Wait for streams to flush
    await new Promise(resolve => setTimeout(resolve, 100));

    const csvPath = path.join(testDir, 'test-run-evals.csv');
    const discPath = path.join(testDir, 'test-run-discoveries.jsonl');
    expect(fs.existsSync(csvPath)).toBe(true);
    expect(fs.existsSync(discPath)).toBe(true);

    const csv = fs.readFileSync(csvPath, 'utf-8');
    expect(csv).toContain('eval_num,score,strategy');
    expect(csv.split('\n').length).toBeGreaterThan(2);
  });
});
