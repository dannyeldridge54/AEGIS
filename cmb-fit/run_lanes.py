# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights. AEGIS-ID: 8942fc94be6e8856
"""Many fits at once until the question is settled.

    python run_lanes.py [LANES]       start LANES workers (default 5, 3 CPU threads each)

Workers pull jobs in order from results/lanes/queue.json, which can be extended while this runs (append
{"name": ..., "env": {...}}). Each job is one `cmbfit_compare.py NAME` fit; its log is results/lanes/NAME.log and
results/lanes/status.json records running / done / failed with times. After every job COMPARE.md is rebuilt.
While it runs it holds Cube Mind's GPU lock, so Cube Mind's learning loop and queued model jobs stay paused.
Stop gracefully: create results/lanes/STOP (running fits finish; no new ones start). Exits by itself after
IDLE_EXIT_S seconds with nothing left to do.
"""
import datetime
import json
import os
import subprocess
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.join(HERE, "results", "lanes")
QUEUE = os.path.join(LANES, "queue.json")
STATUS = os.path.join(LANES, "status.json")
STOP = os.path.join(LANES, "STOP")
PY = os.path.join(HERE, "venv312", "Scripts", "python.exe")
CUBE_MIND = r"C:\Users\Danny\Desktop\CubeMind_side_project\agent"
THREADS = 3
IDLE_EXIT_S = 6 * 3600
BELOW_NORMAL = 0x4000
_LOCK = threading.Lock()
_REPORT = threading.Lock()
_BUSY = {}


def now():
    return datetime.datetime.now().isoformat(timespec="seconds")


def load(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def save(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1)
    os.replace(tmp, path)


def claim(lane):
    with _LOCK:
        status = load(STATUS, {})
        for job in load(QUEUE, []):
            if job["name"] not in status:
                status[job["name"]] = {"status": "running", "lane": lane, "start": now(), "env": job.get("env", {})}
                save(STATUS, status)
                return job
    return None


def finish(name, ok, seconds, note=""):
    with _LOCK:
        status = load(STATUS, {})
        status[name].update(status="done" if ok else "failed", end=now(), minutes=round(seconds / 60, 1), note=note)
        save(STATUS, status)
    with _REPORT:
        with open(os.path.join(LANES, "report.log"), "a", encoding="utf-8") as log:
            subprocess.call([PY, "cmbfit_compare.py", "report"], cwd=HERE, stdout=log, stderr=subprocess.STDOUT,
                            creationflags=BELOW_NORMAL if os.name == "nt" else 0)


def run_job(lane, job):
    name = job["name"]
    out = os.path.join(HERE, "results", f"cmp_{name}.json")
    env = dict(os.environ, OMP_NUM_THREADS=str(THREADS), PYTHONUNBUFFERED="1", PYTHONUTF8="1",
               **{k: str(v) for k, v in job.get("env", {}).items()})
    start = time.time()
    with open(os.path.join(LANES, name + ".log"), "a", encoding="utf-8") as log:
        log.write(f"=== {now()} lane {lane} start {name} env={job.get('env', {})}\n")
        log.flush()
        subprocess.call([PY, "cmbfit_compare.py", name], cwd=HERE, env=env, stdout=log, stderr=subprocess.STDOUT,
                        creationflags=BELOW_NORMAL if os.name == "nt" else 0)
    ok = os.path.exists(out) and os.path.getmtime(out) >= start      # cmbfit_compare prints FAILED but exits 0
    finish(name, ok, time.time() - start, "" if ok else "no new result file; see the log")


def lane(i):
    idle_since = time.time()
    while not os.path.exists(STOP):
        job = claim(i)
        if job is None:
            _BUSY[i] = False
            if not any(_BUSY.values()) and time.time() - idle_since > IDLE_EXIT_S:
                return
            time.sleep(20)
            continue
        _BUSY[i] = True
        run_job(i, job)
        idle_since = time.time()


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    global THREADS
    THREADS = int(sys.argv[2]) if len(sys.argv) > 2 else THREADS
    os.makedirs(LANES, exist_ok=True)
    if os.path.exists(STOP):
        os.remove(STOP)                                   # a STOP from an earlier session must not block this one
    sys.path.insert(0, CUBE_MIND)
    try:
        import gpu_queue                                  # pause Cube Mind's learning and its queued model jobs
        held = gpu_queue.acquire("ufe_fits")
    except Exception as e:                                # the fits still run if Cube Mind is not reachable
        gpu_queue, held = None, False
        print("could not take Cube Mind's GPU lock:", e, flush=True)
    print(f"{now()} {n} lanes x {THREADS} threads; GPU lock held: {held}", flush=True)
    threads = [threading.Thread(target=lane, args=(i,), daemon=False) for i in range(n)]
    try:
        for t in threads:
            t.start()
            time.sleep(5)                                 # stagger start-up so likelihood loading does not collide
        for t in threads:
            t.join()
    finally:
        if gpu_queue and held:
            gpu_queue.release()
        print(f"{now()} all lanes stopped", flush=True)


if __name__ == "__main__":
    main()
