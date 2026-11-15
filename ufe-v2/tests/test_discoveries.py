"""Boundary tests for the D716 discovery rules (run before the rules touch real data)."""
import csv, gzip, math
from aegis import discoveries as D

def row(**kw):
    r = dict(source_id="1", ra="10", dec="20", dist_pc="100", g_mag="10", bp_rp="1.0", ruwe="1.0", pmra="0", pmdec="0",
             rv="", vtan_kms="10", astrometric_quality_pass="True", flags="")
    r.update({k: str(v) for k, v in kw.items()}); return r

def mg(g, d): return g + 5 - 5 * math.log10(d)

def test_nearby_boundary():
    assert "nearby" in D.classify(row(dist_pc=20.0))
    assert "nearby" not in D.classify(row(dist_pc=20.01))

def test_white_dwarf_cut():
    # bp_rp 0.5 -> cut M_G > 11.15. At 50 pc, M_G = g - 3.495
    assert "white_dwarf_candidate" in D.classify(row(dist_pc=50, bp_rp=0.5, g_mag=14.7))      # M_G 11.2
    assert "white_dwarf_candidate" not in D.classify(row(dist_pc=50, bp_rp=0.5, g_mag=14.6))  # M_G 11.1
    assert "white_dwarf_candidate" not in D.classify(row(dist_pc=50, bp_rp=1.3, g_mag=25))    # too red

def test_giant_fast_hyper_red_wobble():
    assert "luminous_giant" in D.classify(row(dist_pc=1000, g_mag=7.9))       # M_G -2.1
    assert "luminous_giant" not in D.classify(row(dist_pc=1000, g_mag=8.1))
    assert "fast_mover" in D.classify(row(pmra=800, pmdec=601))               # 1000.6 mas/yr
    assert "fast_mover" not in D.classify(row(pmra=600, pmdec=799))
    assert "hypervelocity_candidate" in D.classify(row(vtan_kms=500, rv=340))  # 3D 604.6
    assert "hypervelocity_candidate" not in D.classify(row(vtan_kms=500, rv=300))
    assert "hypervelocity_candidate" in D.classify(row(vtan_kms=601))          # tangential only
    assert "very_red" in D.classify(row(bp_rp=4.1)) and "very_red" not in D.classify(row(bp_rp=4.0))
    bad = row(ruwe=12, astrometric_quality_pass="False", dist_pc=5)
    c = D.classify(bad)
    assert "strong_wobble" in c and "nearby" not in c                          # quality gate except RUWE

def test_catalogue_keeps_top_n(tmp_path):
    d = tmp_path / "L5"; d.mkdir()
    with gzip.open(d / "00001.csv.gz", "wt", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(row().keys())); w.writeheader()
        for i in range(10):
            w.writerow(row(source_id=i, dist_pc=5 + i))                        # all nearby
    res = D.scan_tiles(d, top_n=3)
    assert res["counts"]["nearby"] == 10 and res["rows_read"] == 10
    assert [s["id"] for s in res["stars"]["nearby"]] == ["0", "1", "2"]       # closest first
