import { AegisAgent, optimize } from '../src';
import { MetaLearner } from '../src/strategies';

describe('AEGIS Agent', () => {
  test('optimize finds minimum of quadratic', async () => {
    const result = await optimize(
      (p) => (p.x - 2) ** 2 + (p.y + 3) ** 2,
      [
        { name: 'x', min: -10, max: 10 },
        { name: 'y', min: -10, max: 10 },
      ],
      { maxEvals: 1000, verbosity: 'silent' }
    );

    expect(result.score).toBeLessThan(1.0);
    expect(Math.abs(result.params.x - 2)).toBeLessThan(2.0);
    expect(Math.abs(result.params.y + 3)).toBeLessThan(2.0);
  });

  test('agent handles single parameter', async () => {
    const result = await optimize(
      (p) => Math.abs(p.x - 5),
      [{ name: 'x', min: 0, max: 10 }],
      { maxEvals: 500, verbosity: 'silent' }
    );

    expect(result.score).toBeLessThan(0.5);
  });

  test('agent respects maxEvals', async () => {
    const agent = new AegisAgent({
      id: 'test-max',
      name: 'Test',
      evaluate: (p) => p.x ** 2,
      parameters: [{ name: 'x', min: -5, max: 5 }],
    }, { maxEvals: 100, verbosity: 'silent' });

    const state = await agent.run();
    expect(state.totalEvals).toBe(100);
  });

  test('agent tracks discoveries', async () => {
    const agent = new AegisAgent({
      id: 'test-disc',
      name: 'Discovery Test',
      evaluate: (p) => (p.x - 1) ** 2,
      parameters: [{ name: 'x', min: -10, max: 10 }],
    }, { maxEvals: 500, verbosity: 'silent' });

    const state = await agent.run();
    expect(state.best).not.toBeNull();
    expect(state.best!.score).toBeLessThan(5);
  });

  test('agent emits events', async () => {
    const events: string[] = [];
    const agent = new AegisAgent({
      id: 'test-events',
      name: 'Events Test',
      evaluate: (p) => p.x ** 2,
      parameters: [{ name: 'x', min: -5, max: 5 }],
    }, { maxEvals: 50, verbosity: 'silent' });

    agent.on((e) => events.push(e.type));
    await agent.run();

    expect(events).toContain('started');
    expect(events).toContain('evaluation');
    expect(events).toContain('new_best');
  });

  test('multi-dimensional Rosenbrock converges', async () => {
    const result = await optimize(
      (p) => Math.pow(1 - p.x, 2) + 100 * Math.pow(p.y - p.x * p.x, 2),
      [
        { name: 'x', min: -5, max: 5 },
        { name: 'y', min: -5, max: 5 },
      ],
      { maxEvals: 3000, verbosity: 'silent' }
    );

    expect(result.score).toBeLessThan(5.0);
  });

  test('language switching works', () => {
    const agent = new AegisAgent({
      id: 'lang-test',
      name: 'Lang',
      evaluate: (p) => p.x,
      parameters: [{ name: 'x', min: 0, max: 1 }],
    }, { language: 'ja', verbosity: 'silent' });

    // Should not throw
    agent.setLanguage('es');
    agent.setLanguage('zh');
    agent.setLanguage('invalid-should-fallback-to-en');
  });
});

describe('MetaLearner', () => {
  test('selects unused strategies first', () => {
    const ml = new MetaLearner(['random', 'evolutionary', 'gradient'], 0);
    const first = ml.selectStrategy();
    expect(first.uses).toBe(0);
  });

  test('updates strategy performance', () => {
    const ml = new MetaLearner(['random', 'evolutionary'], 0);
    ml.updateStrategy('random', 5.0);
    ml.updateStrategy('random', 3.0);
    ml.updateStrategy('evolutionary', 1.0);

    const strategies = ml.getStrategies();
    expect(strategies[0].type).toBe('random');
    expect(strategies[0].avgImprovement).toBe(4.0);
  });

  test('explores with configured rate', () => {
    const ml = new MetaLearner(['random', 'evolutionary'], 1.0); // 100% exploration
    ml.updateStrategy('random', 100);
    ml.updateStrategy('evolutionary', 0);

    // With 100% exploration, should sometimes pick evolutionary despite worse score
    let pickedEvolutionary = false;
    for (let i = 0; i < 50; i++) {
      if (ml.selectStrategy().type === 'evolutionary') {
        pickedEvolutionary = true;
        break;
      }
    }
    expect(pickedEvolutionary).toBe(true);
  });
});
