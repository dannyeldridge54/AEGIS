"""Dark-sky window: real times for Oklahoma City, no full darkness at Reykjavik in June, and the Tonight panel shows it."""
import json, pathlib, shutil, subprocess, pytest
ROOT = pathlib.Path(__file__).resolve().parents[1]
NODE = shutil.which("node")

def _run(iso, lat, lon):
    js = (f'const A=require("{ROOT}/vendor/astronomy.browser.min.js"),D=require("{ROOT}/js/dark.js");'
          f'console.log(JSON.stringify(D.darkWindow(A,new Date("{iso}"),{lat},{lon})))')
    return json.loads(subprocess.check_output([NODE, "-e", js]))

@pytest.mark.skipif(not NODE, reason="needs node")
def test_okc_night():
    evening, morning = _run("2026-11-20T03:00:00Z", 35.47, -97.52), _run("2026-11-19T10:00:00Z", 35.47, -97.52)
    assert evening["sunset"].startswith("2026-11-19T23:2")          # about 5:21 pm CST
    assert evening["dusk"] < evening["dawn"] < evening["sunrise"]
    assert 600 <= evening["darkMin"] <= 700 and 0 <= evening["moonFreeMin"] <= evening["darkMin"]
    assert morning["sunset"].startswith("2026-11-18")                 # before sunrise: still last night
    late_morning = _run("2026-11-19T15:00:00Z", 35.47, -97.52)
    assert late_morning["sunset"].startswith("2026-11-19")            # Sun up: tonight is the coming night

@pytest.mark.skipif(not NODE, reason="needs node")
def test_no_darkness_reykjavik_june():
    r = _run("2026-06-21T12:00:00Z", 64.1, -21.9)
    assert r["dusk"] is None and r["darkMin"] == 0

pw = pytest.importorskip("playwright.sync_api")
from test_app_browser import server  # noqa: F401,E402

def test_panel_shows_window(server):
    with pw.sync_playwright() as p:
        b = p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
        pg = b.new_page(viewport={"width": 1280, "height": 800}); errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.goto(server); pg.wait_for_selector("button[data-tab=tonight]")
        pg.click("button[data-tab=tonight]"); pg.fill("#lat", "35.5"); pg.fill("#lon", "-97.5"); pg.click("#setLoc")
        pg.wait_for_selector("#darkWin")
        txt = pg.inner_text("#darkWin")
        assert "Dark sky tonight" in txt and "Sunset" in txt and "Moon down" in txt
        app_errors = [e for e in errors if "HiPS" not in e and "fetch" not in e.lower() and "CDS ID" not in e]
        assert not app_errors, app_errors
        b.close()
