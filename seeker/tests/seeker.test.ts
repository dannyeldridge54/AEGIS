import { SeekerAgent, optimize } from '../src';
import { SeededRNG } from '../src/rng';
import { MetaLearner } from '../src/strategies';
import { UFETracker } from '../src/ufe';
import { bootstrapCI, mannWhitneyU, wilcoxonSignedRank, cohensD, ELORating } from '../src/statistics';

// ─── Seeded RNG ──────────────────────────────────────────────────────────────

describe('SeededRNG', () => {
  test('produces deterministic sequences', () => {
    const a = new SeededRNG(42);
    const b = new SeededRNG(42);
    const seqA = Array.from({ length: 100 }, () => a.random());
    const seqB = Array.from({ length: 100 }, () => b.random());
    expect(seqA).toEqual(seqB);
  });

  test('different seeds produce different sequences', () => {
    const a = new SeededRNG(1);
    const b = new SeededRNG(2);
    const match = Array.from({ length: 20 }, () => a.random() === b.random()).every(v => v);
    expect(match).toBe(false);
  });

  test('range respects bounds', () => {
    const rng = new SeededRNG(99);
    for (let i = 0; i < 1000; i++) {
      const v = rng.range(-5, 5);
      expect(v).toBeGreaterThanOrEqual(-5);
      expect(v).toBeLessThan(5);
    }
  });

  test('fork produces different child', () => {
    const parent = new SeededRNG(42);
    const child = parent.fork();
    expect(child.seed).not.toBe(parent.seed);
  });
});

// ─── UFE Tracker ─────────────────────────────────────────────────────────────

describe('UFETracker', () => {
  test('tracks useful evaluations', () => {
    const params = [{ name: 'x', min: 0, max: 10 }];
    const tracker = new UFETracker(params, true);

    // First eval is always useful (novel region)
    const r1 = tracker.record({ params: { x: 5 }, score: 10, timestamp: 0, strategy: 'random' });
    expect(r1.useful).toBe(true);

    // Improvement is useful
    const r2 = tracker.record({ params: { x: 3 }, score: 5, timestamp: 0, strategy: 'random' });
    expect(r2.improved).toBe(true);
    expect(r2.useful).toBe(true);

    const metrics = tracker.getMetrics();
    expect(metrics.usefulEvals).toBeGreaterThan(0);
    expect(metrics.ufeRatio).toBeGreaterThan(0);
    expect(metrics.convergenceCurve.length).toBe(2);
  });

  test('computes time-to-target with known optimum', () => {
    const params = [{ name: 'x', min: -10, max: 10 }];
    const tracker = new UFETracker(params, true);

    // Start far from optimum, converge
    tracker.record({ params: { x: 8 }, score: 64, timestamp: 0, strategy: 'random' });
    tracker.record({ params: { x: 4 }, score: 16, timestamp: 0, strategy: 'random' });
    tracker.record({ params: { x: 1 }, score: 1, timestamp: 0, strategy: 'random' });
    tracker.record({ params: { x: 0.1 }, score: 0.01, timestamp: 0, strategy: 'random' });

    const metrics = tracker.getMetrics(0);
    // Should have found 90% gap closure
    expect(metrics.timeToTarget.pct90).not.toBeNull();
  });
});

// ─── Statistics ──────────────────────────────────────────────────────────────

describe('Statistics', () => {
  test('bootstrapCI returns valid CI', () => {
    const data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    const ci = bootstrapCI(data);
    expect(ci.mean).toBeCloseTo(5.5, 1);
    expect(ci.lower).toBeLessThan(ci.mean);
    expect(ci.upper).toBeGreaterThan(ci.mean);
    expect(ci.n).toBe(10);
  });

  test('mannWhitneyU detects difference', () => {
    const a = [1, 2, 3, 4, 5];
    const b = [10, 11, 12, 13, 14];
    const result = mannWhitneyU(a, b);
    expect(result.significant).toBe(true);
    expect(result.direction).toBe('a_better');
  });

  test('mannWhitneyU returns not significant for same distributions', () => {
    const a = [1, 3, 5, 7, 9, 2, 4, 6, 8, 10];
    const b = [2, 4, 6, 8, 10, 1, 3, 5, 7, 9];
    const result = mannWhitneyU(a, b);
    expect(result.significant).toBe(false);
  });

  test('cohensD computes effect size', () => {
    const a = [1, 2, 3, 4, 5];
    const b = [6, 7, 8, 9, 10];
    const d = cohensD(a, b);
    expect(Math.abs(d)).toBeGreaterThan(2);
  });

  test('ELO rating updates correctly', () => {
    const elo = new ELORating(32);
    elo.register('a');
    elo.register('b');

    // A wins 10 times
    for (let i = 0; i < 10; i++) elo.recordMatch('a', 'b', 1);

    expect(elo.getRating('a')).toBeGreaterThan(elo.getRating('b'));
    const board = elo.getLeaderboard();
    expect(board[0].id).toBe('a');
  });
});

// ─── Seeker Agent ────────────────────────────────────────────────────────────

describe('SeekerAgent', () => {
  test('optimize finds minimum of quadratic', async () => {
    const result = await optimize(
      (p) => (p.x - 2) ** 2 + (p.y + 3) ** 2,
      [
        { name: 'x', min: -10, max: 10 },
        { name: 'y', min: -10, max: 10 },
      ],
      { maxEvals: 1000, verbosity: 'silent', seed: 42 }
    );

    expect(result.score).toBeLessThan(1.0);
  });

  test('deterministic with same seed', async () => {
    const run = async (seed: number) => {
      const result = await optimize(
        (p) => p.x ** 2 + p.y ** 2,
        [
          { name: 'x', min: -5, max: 5 },
          { name: 'y', min: -5, max: 5 },
        ],
        { maxEvals: 200, verbosity: 'silent', seed }
      );
      return result.score;
    };

    const a = await run(123);
    const b = await run(123);
    expect(a).toBe(b);
  });

  test('agent tracks UFE metrics', async () => {
    const agent = new SeekerAgent({
      id: 'ufe-test', name: 'UFE Test',
      evaluate: (p) => p.x ** 2,
      parameters: [{ name: 'x', min: -5, max: 5 }],
    }, { maxEvals: 100, verbosity: 'silent', seed: 42 });

    const state = await agent.run(0);
    expect(state.ufe.totalEvals).toBe(100);
    expect(state.ufe.usefulEvals).toBeGreaterThan(0);
    expect(state.ufe.ufeRatio).toBeGreaterThan(0);
    expect(state.ufe.convergenceCurve.length).toBe(100);
  });

  test('agent detects discoveries', async () => {
    const agent = new SeekerAgent({
      id: 'disc-test', name: 'Discovery Test',
      evaluate: (p) => (p.x - 1) ** 2,
      parameters: [{ name: 'x', min: -10, max: 10 }],
    }, { maxEvals: 500, verbosity: 'silent', seed: 42 });

    const state = await agent.run();
    expect(state.discoveries.length).toBeGreaterThan(0);
  });

  test('emits events', async () => {
    const events: string[] = [];
    const agent = new SeekerAgent({
      id: 'events-test', name: 'Events Test',
      evaluate: (p) => p.x ** 2,
      parameters: [{ name: 'x', min: -5, max: 5 }],
    }, { maxEvals: 50, verbosity: 'silent', seed: 42 });

    agent.on((e) => events.push(e.type));
    await agent.run();

    expect(events).toContain('started');
    expect(events).toContain('evaluation');
    expect(events).toContain('new_best');
  });

  test('respects maxEvals', async () => {
    const agent = new SeekerAgent({
      id: 'max-test', name: 'Max Test',
      evaluate: (p) => p.x ** 2,
      parameters: [{ name: 'x', min: -5, max: 5 }],
    }, { maxEvals: 100, verbosity: 'silent' });

    const state = await agent.run();
    expect(state.totalEvals).toBe(100);
  });
});

// ─── MetaLearner ─────────────────────────────────────────────────────────────

describe('MetaLearner', () => {
  test('selects unused strategies first', () => {
    const rng = new SeededRNG(42);
    const ml = new MetaLearner(['random', 'evolutionary', 'gradient'], 0, rng);
    const first = ml.selectStrategy();
    expect(first.uses).toBe(0);
  });

  test('updates strategy performance', () => {
    const rng = new SeededRNG(42);
    const ml = new MetaLearner(['random', 'evolutionary'], 0, rng);
    ml.updateStrategy('random', 5.0);
    ml.updateStrategy('random', 3.0);
    ml.updateStrategy('evolutionary', 1.0);

    const strategies = ml.getStrategies();
    expect(strategies[0].type).toBe('random');
    expect(strategies[0].avgImprovement).toBe(4.0);
  });
});
