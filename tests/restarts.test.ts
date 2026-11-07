import { AegisAgent, optimize, benchmarkFunctions } from '../src';

describe('restarts and step adaptation', () => {
  test('restarts happen on a multimodal function and are reported', async () => {
    const f = benchmarkFunctions.schwefel;
    const agent = new AegisAgent(f, { maxEvals: 3000, verbosity: 'silent' });
    const state = await agent.run();
    expect(agent.getRestarts()).toBeGreaterThan(0);
    expect(state.discoveries.some(d => d.type === 'restart')).toBe(true);
  });

  test('restartAfter: 0 disables restarts', async () => {
    const agent = new AegisAgent(benchmarkFunctions.rastrigin, { maxEvals: 2000, verbosity: 'silent', restartAfter: 0 });
    await agent.run();
    expect(agent.getRestarts()).toBe(0);
  });

  test('global best is never lost across restarts', async () => {
    const seen: number[] = [];
    const agent = new AegisAgent(benchmarkFunctions.styblinskiTang, { maxEvals: 2000, verbosity: 'silent' });
    agent.on(e => { if (e.type === 'evaluation') seen.push(e.result.score); });
    const state = await agent.run();
    expect(state.best!.score).toBe(Math.min(...seen));
  });

  test('adaptive steps refine to high precision', async () => {
    const res = await optimize(benchmarkFunctions.sphere5d.evaluate, benchmarkFunctions.sphere5d.parameters, { maxEvals: 3000, verbosity: 'silent' });
    expect(res.score).toBeLessThan(1e-3);
  });

  test('Styblinski-Tang reaches the global optimum in most runs', async () => {
    const f = benchmarkFunctions.styblinskiTang;
    let hits = 0;
    for (let i = 0; i < 10; i++) {
      const r = await optimize(f.evaluate, f.parameters, { maxEvals: 3000, verbosity: 'silent' });
      if (r.score - f.optimum < 1) hits++;
    }
    expect(hits).toBeGreaterThanOrEqual(6); // ~90% expected; original code ~65%
  }, 60000);

  test('unlimited runs still terminate by convergence', async () => {
    const agent = new AegisAgent({ id: 'c', name: 'c', evaluate: (p) => (p.x - 1) ** 2, parameters: [{ name: 'x', min: -5, max: 5 }] }, { verbosity: 'silent' });
    const state = await agent.run();
    expect(state.totalEvals).toBeLessThan(20000);
  }, 20000);
});
