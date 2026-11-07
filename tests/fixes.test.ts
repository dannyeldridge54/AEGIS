import { AegisAgent, optimize, parallelOptimize, multiOptimize } from '../src';
import { generateNextPoint, noveltySample, MetaLearner } from '../src/strategies';

describe('robustness fixes', () => {
  test('NaN scores never become the best result', async () => {
    let n = 0;
    const res = await optimize(
      (p) => (n++ === 0 ? NaN : (p.x - 1) ** 2),
      [{ name: 'x', min: -5, max: 5 }],
      { maxEvals: 300, verbosity: 'silent' }
    );
    expect(Number.isFinite(res.score)).toBe(true);
    expect(res.score).toBeLessThan(0.5);
  });

  test('maximize goal is honoured', async () => {
    const res = await optimize(
      (p) => -((p.x - 3) ** 2),
      [{ name: 'x', min: -10, max: 10 }],
      { maxEvals: 500, verbosity: 'silent', goal: 'maximize accuracy' }
    );
    expect(res.score).toBeGreaterThan(-0.5);
  });

  test('discrete parameters respect step', async () => {
    const seen: number[] = [];
    await optimize(
      (p) => { seen.push(p.layers); return (p.layers - 4) ** 2; },
      [{ name: 'layers', min: 1, max: 12, step: 1 } as any],
      { maxEvals: 200, verbosity: 'silent' }
    );
    expect(seen.every((v) => Number.isInteger(v) && v >= 1 && v <= 12)).toBe(true);
  });

  test('constraints are respected', async () => {
    const seen: Array<Record<string, number>> = [];
    const agent = new AegisAgent({
      id: 'c', name: 'c',
      evaluate: (p) => { seen.push(p); return p.x + p.y; },
      parameters: [{ name: 'x', min: 0, max: 1 }, { name: 'y', min: 0, max: 1 }],
      constraints: [{ params: ['x', 'y'], check: (v) => v.x + v.y >= 0.5 }],
    }, { maxEvals: 300, verbosity: 'silent' });
    await agent.run();
    expect(seen.every((p) => p.x + p.y >= 0.5)).toBe(true);
  });

  test('evolutionary parents come from the best samples', () => {
    const params = [{ name: 'x', min: 0, max: 100 }];
    // 20 bad old samples near 90, then good recent ones near 10
    const history = [
      ...Array.from({ length: 20 }, () => ({ params: { x: 90 }, score: 100, timestamp: 0, strategy: 'random' as const })),
      ...Array.from({ length: 10 }, () => ({ params: { x: 10 }, score: 1, timestamp: 0, strategy: 'random' as const })),
    ];
    const strat = { type: 'evolutionary' as const, score: 0, uses: 0, avgImprovement: 0, config: { mutationRate: 0.01 } };
    for (let i = 0; i < 50; i++) {
      const p = generateNextPoint(strat, params, history[25], history);
      expect(p.x).toBeLessThan(20);
    }
  });

  test('novelty sampling prefers unvisited regions', () => {
    const params = [{ name: 'x', min: 0, max: 1 }];
    const history = Array.from({ length: 500 }, () => ({ params: { x: Math.random() * 0.9 }, score: 0, timestamp: 0, strategy: 'random' as const }));
    let high = 0;
    for (let i = 0; i < 50; i++) if (noveltySample(params, history).x >= 0.9) high++;
    expect(high).toBeGreaterThan(40);
  });

  test('parallelOptimize terminates when every evaluation fails', async () => {
    const state = await parallelOptimize({
      id: 'f', name: 'f',
      evaluate: () => { throw new Error('boom'); },
      parameters: [{ name: 'x', min: 0, max: 1 }],
    }, { maxEvals: 1000, verbosity: 'silent', retries: 0 });
    expect(state.best).toBeNull();
  });

  test('parallelOptimize honours maximize goal', async () => {
    const state = await parallelOptimize({
      id: 'm', name: 'm',
      evaluate: async (p) => -((p.x - 0.7) ** 2),
      parameters: [{ name: 'x', min: 0, max: 1 }],
    }, { maxEvals: 400, verbosity: 'silent', goal: { description: 'max', minimize: false } });
    expect(state.best!.score).toBeGreaterThan(-0.01);
  });

  test('multiOptimize returns a non-dominated front quickly', async () => {
    const t0 = Date.now();
    const front = await multiOptimize(
      [
        { name: 'a', evaluate: (p) => p.x ** 2 },
        { name: 'b', evaluate: (p) => (p.x - 2) ** 2 },
      ],
      [{ name: 'x', min: -2, max: 4 }],
      { maxEvals: 2000, verbosity: 'silent' }
    );
    expect(Date.now() - t0).toBeLessThan(5000);
    expect(front.solutions.length).toBeGreaterThan(3);
    for (const s of front.solutions) {
      expect(s.params.x).toBeGreaterThanOrEqual(-0.05);
      expect(s.params.x).toBeLessThanOrEqual(2.05);
    }
  });

  test('getState before run reports zero runtime', () => {
    const agent = new AegisAgent({ id: 'r', name: 'r', evaluate: () => 0, parameters: [{ name: 'x', min: 0, max: 1 }] }, { verbosity: 'silent' });
    expect(agent.getState().runtime).toBe(0);
  });

  test('MetaLearner rewards stay comparable', () => {
    const ml = new MetaLearner(['random', 'exploit'], 0);
    ml.updateStrategy('random', 1);
    expect(ml.getStrategies()[0].type).toBe('random');
  });
});
