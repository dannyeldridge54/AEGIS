import * as fs from 'fs';
import * as os from 'os';
import * as path from 'path';
import { loadTaskFile } from '../src/cli';
import { parseNaturalLanguage, loadObjective } from '../src/natural-cli';

const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'aegis-cli-'));
fs.writeFileSync(path.join(dir, 'obj.js'), 'module.exports = (p) => p.x * 2;');
fs.writeFileSync(path.join(dir, 'named.js'), 'exports.evaluate = (p) => p.x + 1;');
fs.writeFileSync(path.join(dir, 'none.js'), 'exports.foo = 1;');
const write = (name: string, obj: unknown) => { const f = path.join(dir, name); fs.writeFileSync(f, JSON.stringify(obj)); return f; };

describe('CLI task files', () => {
  test('loads a valid task with the objective resolved relative to the file', async () => {
    const f = write('ok.json', { name: 'My Task', objective: './obj.js', parameters: [{ name: 'x', min: 0, max: 1 }], goal: 'maximize', maxEvals: 10 });
    const { task, goal, maxEvals } = loadTaskFile(f);
    expect(task.name).toBe('My Task');
    expect(task.id).toBe('my-task');
    expect(await task.evaluate({ x: 3 })).toBe(6);
    expect(goal).toBe('maximize');
    expect(maxEvals).toBe(10);
  });

  test('rejects bad task files with a clear message', () => {
    expect(() => loadTaskFile(write('a.json', { parameters: [{ name: 'x', min: 0, max: 1 }] }))).toThrow(/objective/);
    expect(() => loadTaskFile(write('b.json', { objective: './obj.js', parameters: [] }))).toThrow(/parameters/);
    expect(() => loadTaskFile(write('c.json', { objective: './obj.js', parameters: [{ name: 'x', min: 2, max: 1 }] }))).toThrow(/min < max/);
    expect(() => loadTaskFile(write('d.json', { objective: './missing.js', parameters: [{ name: 'x', min: 0, max: 1 }] }))).toThrow(/not found/);
    const bad = path.join(dir, 'bad.json'); fs.writeFileSync(bad, '{nope');
    expect(() => loadTaskFile(bad)).toThrow(/could not read/);
  });

  test('loadObjective accepts named exports and rejects modules without a function', () => {
    expect(loadObjective(path.join(dir, 'named.js'))({ x: 1 })).toBe(2);
    expect(() => loadObjective(path.join(dir, 'none.js'))).toThrow(/must export a function/);
  });
});

describe('natural language parsing', () => {
  test('extracts ranges, orders min/max and detects maximize', () => {
    const g = parseNaturalLanguage('maximize accuracy with lr between 0.1 and 0.0001 and layers from 1 to 12');
    expect(g.type).toBe('optimize');
    expect(g.minimize).toBe(false);
    expect(g.parameters).toEqual(expect.arrayContaining([
      expect.objectContaining({ name: 'lr', min: 0.0001, max: 0.1 }),
      expect.objectContaining({ name: 'layers', min: 1, max: 12 }),
    ]));
  });

  test('recognises coding requests', () => {
    expect(parseNaturalLanguage('generate a REST api for todos in python')).toMatchObject({ type: 'code', language: 'python' });
  });
});
