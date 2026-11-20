"""Parallel Weave data builder (Danny 20 Nov 13:15 "make it as fast as the PC can take").
N worker processes (default: logical CPUs - 4, so Ollama/GPU feeding and the desktop keep headroom) each loop weave_sweep.run on
their own shard files (no write races). One BLAS thread per worker. Heartbeat: weave_data/pool_heartbeat.txt. Disk guard as in weave_sweep.
Run from CubeMind_janus:  python aegis_tools/aegis_bundle/tools/weave_cm/weave_pool.py"""
import os, sys, time, pathlib, multiprocessing as mp
for k in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'): os.environ[k] = '1'
HERE = pathlib.Path(__file__).resolve().parent
DATA = pathlib.Path(os.environ.get('WEAVE_DATA') or (HERE.parents[2] / 'weave_data'))


def worker(i):
    sys.path.insert(0, str(HERE)); import weave_sweep as WS
    os.environ.setdefault('WEAVE_CURRENT', str(HERE.parents[2] / 'aegis_tools' / 'aegis_current'))
    while True:
        try:
            r = WS.run(str(DATA), seconds=int(os.environ.get('WEAVE_POOL_S', '90')), shard=f'_w{i}')
            if r.get('weave_sweep') == 'paused by disk guard': time.sleep(600)
        except Exception as e:
            with open(DATA / f'pool_errors.log', 'a', encoding='utf-8') as f: f.write(f'{time.ctime()} w{i} {type(e).__name__}: {e}\n')
            time.sleep(30)
        (DATA / 'pool_heartbeat.txt').write_text(str(time.time()))


if __name__ == '__main__':
    mp.freeze_support(); DATA.mkdir(parents=True, exist_ok=True)
    n = int(os.environ.get('WEAVE_POOL_N', str(max(1, (os.cpu_count() or 8) - 4))))
    ps = [mp.Process(target=worker, args=(i,), daemon=True) for i in range(n)]
    for p in ps: p.start()
    (DATA / 'pool_heartbeat.txt').write_text(str(time.time())); print(f'weave_pool: {n} workers -> {DATA}', flush=True)
    while True:
        for i, p in enumerate(ps):
            if not p.is_alive(): ps[i] = mp.Process(target=worker, args=(i,), daemon=True); ps[i].start()
        time.sleep(30)
