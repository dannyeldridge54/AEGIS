import csv, gzip, json, pathlib, subprocess, sys
TOOL = pathlib.Path(__file__).resolve().parents[1] / "tools" / "export_from_sweep.py"
COLS = ["source_id", "ra", "dec", "g_mag", "bp_rp", "ruwe", "vtan_kms", "dist_pc", "confirmed", "flags", "flag_notes"]

def tile(path, rows):
    with gzip.open(path, "wt", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS); w.writeheader(); w.writerows(rows)

def row(i, flags="", ruwe=1.0):
    return dict(source_id=i, ra=10 + i * 0.01, dec=-5 + i * 0.01, g_mag=15, bp_rp=1.0, ruwe=ruwe, vtan_kms=50, dist_pc=1000,
                confirmed="True", flags=flags, flag_notes="note" if flags else "")

def test_export_counts_and_selection(tmp_path):
    cm = tmp_path / "cm"; (cm / "tiles" / "L5").mkdir(parents=True)
    tile(cm / "tiles/L5/00001.csv.gz", [row(1), row(2, "high_velocity"), row(3, "astrometric_excess", 2.0), row(4, "astrometric_excess", 5.0)])
    tile(cm / "tiles/L5/00002.csv.gz", [row(5, "distance_mismatch"), row(6, "astrometric_excess;high_velocity", 3.0), row(7)])
    json.dump({"level": 5, "done": {"1": {"n": 4}, "2": {"n": 3}}}, open(cm / "sweep_state.json", "w"))
    out = tmp_path / "out"
    subprocess.run([sys.executable, str(TOOL), "--cosmos-map", str(cm), "--out", str(out), "--max-ruwe", "1"], check=True, capture_output=True)
    cov = json.load(open(out / "aegis_coverage.json")); fl = json.load(open(out / "aegis_flags.json"))
    assert cov["stars"] == 7 and cov["rows_read"] == 7 and cov["coverage_moc"] == {"5": [1, 2]}
    ids = [s["id"] for s in fl["stars"]]
    assert set(ids) == {"2", "5", "6", "4"}          # all HV/DM (incl. 6), and only the top-RUWE excess star (4, RUWE 5)
    assert fl["counts_in_sweep"]["astrometric_excess"] == 3 and fl["counts_in_sweep"]["high_velocity"] == 2
    assert "not discoveries" in fl["status"]
