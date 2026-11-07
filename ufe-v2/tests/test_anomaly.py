"""Offline tests for the anomaly scanner. Run: python -m pytest tests/test_anomaly.py"""
import csv, gzip, os, random, sys, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from aegis.anomaly_scanner import (AnomalyScanner, assess_beacon, assess_gw, ks_2samp, compare_sets,
                                   query_anomalies, to_ecsv, to_votable)


def scanner(fetch):
    return AnomalyScanner(tempfile.mkdtemp(), log=lambda m: None, fetch=fetch)


def test_gw_flags_and_object():
    r = assess_gw("A", dict(commonName="A", mass_1_source=80, mass_2_source=3.2, chi_eff=0.7, luminosity_distance=6000))
    assert set(r["flags"].split(";")) == {"upper_mass_gap", "lower_mass_gap", "high_spin", "far_source"}
    assert r["object"] == "black_hole"   # 3.2 Msun is in the lower gap, above the 3 Msun neutron-star cut
    assert assess_gw("B", dict(mass_1_source=30, mass_2_source=1.4))["object"] == "neutron_star_black_hole"


def test_beacon_bias_and_status():
    r = assess_beacon(dict(chainIndex=1, pulseIndex=2, statusCode=1, outputValue="f" * 128))
    assert "bit_bias" in r["flags"] and "beacon_status" in r["flags"]


def test_ks_calibration():
    hits = 0
    for seed in range(200):
        g = random.Random(seed)
        hits += ks_2samp([g.gauss(0, 1) for _ in range(40)], [g.gauss(0, 1) for _ in range(40)])[1] < 1e-3
    assert hits == 0
    g = random.Random(1)
    assert compare_sets([g.gauss(0, 1) for _ in range(100)], [g.gauss(2, 1) for _ in range(100)])["verdict"] == "drift"


def test_telemetry_drift_series_and_restart():
    g = random.Random(5)
    state = {"mu": 10.0}
    rows = lambda t0: [{"time_tag": f"t{t0 + i}", "energy": e, "flux": g.gauss(state["mu"] * (1 if e == "a" else 1000), 1)}
                       for i in range(80) for e in ("a", "b")]
    cur = [rows(0)]
    A = scanner(lambda u, t=30: cur[0])
    A.scan_telemetry()
    cur[0] = rows(1000); A.scan_telemetry()
    assert "xray:a" in A.compare and "xray:b" in A.compare       # channels are compared separately
    state["mu"] = 14.0
    cur[0] = rows(2000); A.scan_telemetry()
    assert A.compare["xray:a"]["verdict"] == "drift"
    B = AnomalyScanner(A.outdir, log=lambda m: None, fetch=lambda u, t=30: cur[0])
    assert B.counts["xray"] == A.counts["xray"] and len(B.history["xray:a"]) > 0
    n = B.counts["xray"]; B.scan_telemetry()
    assert B.counts["xray"] == n                                  # nothing is counted twice after a restart


def test_local_tiles_and_incoming():
    A = scanner(lambda u, t=30: [])
    os.makedirs(A.outdir + "/tiles/L5"); os.makedirs(A.outdir + "/incoming")
    g = random.Random(3)
    for t, mu in enumerate([50, 50, 90]):
        with gzip.open(f"{A.outdir}/tiles/L5/{t:05d}.csv.gz", "wt", newline="") as fh:
            w = csv.writer(fh); w.writerow(["vtan_kms", "ruwe", "dist_pc"])
            for _ in range(300):
                w.writerow([g.gauss(mu, 10), g.gauss(1, .1), g.gauss(500, 50)])
    A.scan_local()
    assert A.compare["star_vtan"]["verdict"] == "drift" and A.compare["star_ruwe"]["verdict"] == "consistent"


def test_query_and_exports():
    doc = {"events": {"A": {"commonName": "A & <x>", "mass_1_source": 80, "mass_2_source": 70},
                      "B": {"commonName": "B", "mass_1_source": 1.4, "mass_2_source": 1.3, "far": 5}}}
    A = scanner(lambda u, t=30: doc); A.scan_gravity()
    rows, facets = query_anomalies(A.outdir, obj="black_hole")
    assert [r["id"] for r in rows] == ["A & <x>"] and facets["wavelength"] == {"gravitational": 1}
    import xml.dom.minidom
    xml.dom.minidom.parseString(to_votable(rows))
    assert to_ecsv(rows).startswith("# %ECSV 1.0")
