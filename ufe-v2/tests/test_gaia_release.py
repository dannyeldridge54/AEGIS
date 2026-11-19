"""DR4 prep (PREREG_STAR_MAPPER_DR4_DEVIATIONS): DR3 defaults unchanged; DR4 settings swap table, NULL missing columns, flag parallax-only."""
import importlib, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

DR3_RANGE = ("FROM gaiadr3.gaia_source AS g LEFT OUTER JOIN external.gaiaedr3_distance AS d ON g.source_id = d.source_id "
             "WHERE g.source_id BETWEEN 1 AND 100 AND g.parallax_over_error > 5 ORDER BY g.source_id")

def _load(monkeypatch, **env):
    for k in ("AEGIS_GAIA_TABLE", "AEGIS_DIST_TABLE", "AEGIS_GAIA_MISSING", "AEGIS_GAIA_LABEL"):
        monkeypatch.delenv(k, raising=False)
    for k, v in env.items():
        monkeypatch.setenv(k, v)
    import aegis.star_scanner as s, aegis.sweep as w
    return importlib.reload(s), importlib.reload(w)

def test_dr3_default_frozen(monkeypatch):
    s, w = _load(monkeypatch)
    assert w.adql_range(1, 100, 0, 8000).endswith(DR3_RANGE)
    assert "d.r_med_geo, d.r_lo_geo, d.r_hi_geo" in w.adql_range(1, 100, 0, 8000)

def test_dr4_mode(monkeypatch):
    s, w = _load(monkeypatch, AEGIS_GAIA_TABLE="gaiadr4.gaia_source", AEGIS_DIST_TABLE="none",
                 AEGIS_GAIA_MISSING="ruwe", AEGIS_GAIA_LABEL="Gaia DR4")
    q = w.adql_range(1, 100, 0, 8000)
    assert "gaiadr3" not in q and "gaiaedr3" not in q and "JOIN" not in q
    assert "NULL AS ruwe" in q and "NULL AS r_med_geo" in q
    r = s.assess(dict(source_id=1, ra=10, dec=20, parallax=2.0, parallax_error=0.1, pmra=5, pmdec=5))
    assert r["dist_pc"] == 500.0 and "distance_parallax_only" in r["flags"]
    _load(monkeypatch)   # restore DR3 module state for other tests
