import { optimize, MetaLearner, parallelOptimize } from '../src';
import { generateNextPoint, observeResult, surrogateSample, banditSample } from '../src/strategies';

const sphere = (p: Record<string, number>) => Object.values(p).reduce((s, v) => s + v * v, 0);
const params3 = [0, 1, 2].map(i => ({ name: `x${i}`, min: -5, max: 5 }));

async function median(strategy: string, runs = 7) {
  const s: number[] = [];
  for (let i = 0; i < runs; i++) s.push((await optimize(sphere, params3, { maxEvals: 600, verbosity: 'silent', strategies: [strategy as any] })).score);
  return s.sort((a, b) => a - b)[Math.floor(runs / 2)];
}

describe('real swarm / bayesian / bandit strategies', () => {
  test.each(['swarm', 'bayesian', 'bandit'])('%s beats pure random search', async (st) => {
    expect(await median(st)).toBeLessThan(await median('random'));
  }, 30000);

  test('swarm feedback updates the particle personal best', () => {
    const ml = new MetaLearner(['swarm'], 0);
    const strat = ml.selectStrategy();
    const x = generateNextPoint(strat, params3, null, []);
    observeResult(strat, x, 1.23);
    const particles = strat.config._swarm.particles;
    expect(particles[0].pbestScore).toBe(1.23);
    expect(JSON.stringify(ml.getStrategies())).not.toContain('_swarm'); // state stays out of checkpoints
  });

  test('surrogate proposes near good points once it has data', () => {
    const p = [{ name: 'x', min: 0, max: 1 }];
    const history = Array.from({ length: 60 }, (_, i) => { const x = i / 59; return { params: { x }, score: (x - 0.8) ** 2, timestamp: 0, strategy: 'random' as const }; });
    const best = history.reduce((a, b) => (b.score < a.score ? b : a));
    let near = 0;
    for (let i = 0; i < 20; i++) if (Math.abs(surrogateSample(p, best, history, true, 0.5).x - 0.8) < 0.2) near++;
    expect(near).toBeGreaterThan(14);
  });

  test('bandit favours the bin with the best results', () => {
    const p = [{ name: 'x', min: 0, max: 1 }];
    const history = Array.from({ length: 400 }, () => { const x = Math.random(); return { params: { x }, score: x < 0.125 ? 0 : 1 + x, timestamp: 0, strategy: 'random' as const }; });
    let low = 0;
    for (let i = 0; i < 50; i++) if (banditSample(p, history, true).x < 0.125) low++;
    expect(low).toBeGreaterThan(25);
  });

  test('parallel runner works with the stateful swarm', async () => {
    const state = await parallelOptimize({ id: 'p', name: 'p', evaluate: async (p) => sphere(p), parameters: params3 }, { maxEvals: 400, verbosity: 'silent', strategies: ['swarm'] });
    expect(state.best!.score).toBeLessThan(1);
  });
});
