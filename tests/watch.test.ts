import * as fs from 'fs';
import * as os from 'os';
import * as path from 'path';
import * as http from 'http';
import { AegisDaemon } from '../src';

const wait = (ms: number) => new Promise((r) => setTimeout(r, ms));
async function until(cond: () => boolean, ms = 8000) {
  const t = Date.now();
  while (!cond()) { if (Date.now() - t > ms) throw new Error('timed out'); await wait(50); }
}

function daemonWith(watch: string, watchInterval: number) {
  const daemon = new AegisDaemon({ workDir: fs.mkdtempSync(path.join(os.tmpdir(), 'aegis-w-')), apiPort: 0, dashboardPort: 0, enableMemory: false });
  daemon.addJob({
    id: 'job', name: 'job', schedule: 'once', watch, watchInterval,
    task: { id: 'job', name: 'job', evaluate: (p) => p.x ** 2, parameters: [{ name: 'x', min: -1, max: 1 }] },
    config: { maxEvals: 50 },
  });
  return daemon;
}
const runs = (d: AegisDaemon) => d.getJobStates()[0].runs;

describe('daemon watch', () => {
  let log: jest.SpyInstance;
  beforeAll(() => { log = jest.spyOn(console, 'log').mockImplementation(() => {}); });
  afterAll(() => log.mockRestore());

  test('a changed file re-runs a finished job', async () => {
    const file = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'aegis-f-')), 'data.csv');
    fs.writeFileSync(file, 'a');
    const d = daemonWith(file, 0.1);
    await d.start();
    try {
      await until(() => runs(d) === 1);
      await wait(300);
      expect(runs(d)).toBe(1); // nothing changed, no rerun
      fs.writeFileSync(file, 'ab');
      await until(() => runs(d) === 2);
    } finally { d.stop(); }
  }, 15000);

  test('a changed URL re-runs the job', async () => {
    let body = 'v1';
    const server = http.createServer((_, res) => res.end(body));
    await new Promise<void>((r) => server.listen(0, '127.0.0.1', r));
    const url = `http://127.0.0.1:${(server.address() as any).port}/data`;
    const d = daemonWith(url, 0.1);
    await d.start();
    try {
      await until(() => runs(d) === 1);
      await wait(400);
      expect(runs(d)).toBe(1);
      body = 'v2';
      await until(() => runs(d) === 2);
    } finally { d.stop(); server.close(); }
  }, 15000);
});
