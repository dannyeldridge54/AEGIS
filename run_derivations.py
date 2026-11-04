"""Stepped loop: tests, then every derivation script, then (if online) the telemetry scan. Run on a PC with network.
    python run_derivations.py
Needs: numpy scipy sympy pytest. Writes run_derivations_report.json; regenerated theory/*.json are left for review.
"""
import json, os, subprocess, sys, time, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
STEPS = [
    ("tests", "ufe-v2", ["-m", "pytest", "tests", "-q"]),
    ("recheck_math", "ufe-v2", ["recheck_math.py"]),
    ("bi_kahler_lambda", "theory", ["bi_kahler_lambda.py"]),
    ("bi_superpotential", "theory", ["bi_superpotential.py"]),
    ("solar_lowz", "theory", ["solar_lowz.py"]),
]


def online():
    try:
        urllib.request.urlopen("https://services.swpc.noaa.gov/json/", timeout=8)
        return True
    except Exception:
        return False


def main():
    report = []
    for name, cwd, args in STEPS:
        t = time.time()
        p = subprocess.run([sys.executable] + args, cwd=os.path.join(ROOT, cwd), capture_output=True, text=True)
        report.append({"step": name, "ok": p.returncode == 0, "seconds": round(time.time() - t, 1),
                       "tail": (p.stdout + p.stderr).strip().splitlines()[-3:]})
        print(("PASS " if p.returncode == 0 else "FAIL ") + name)
    report.append({"step": "telemetry", "online": online(),
                   "note": "start ufe-v2/START_AEGIS_MONITOR.bat; scanner pulls GWOSC, NIST beacon, NOAA SWPC"})
    json.dump(report, open(os.path.join(ROOT, "run_derivations_report.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
