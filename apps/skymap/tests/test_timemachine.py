"""Time machine: motion maths matches a hand calculation; lines and stars move; slider/Now/close work; no JS errors."""
import pytest
pw = pytest.importorskip("playwright.sync_api")
from test_app_browser import server  # noqa: F401

def test_time_machine(server):
    with pw.sync_playwright() as p:
        b = p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
        pg = b.new_page(viewport={"width": 1280, "height": 800}); errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.goto(server); pg.wait_for_function("window.__skymap && window.__skymap.timeMachine", timeout=20000)
        # Sirius over 1,000 yr: dec moves -1.205"/yr -> -0.3347 deg; RA by -0.553"/yr / cos(dec) -> -0.1604 deg (small-angle)
        ra, dec = pg.evaluate("window.__skymap.timeMachine.move(101.2872,-16.7161,[-553,-1205],1000)")
        import math
        r = math.radians
        sep = math.degrees(math.acos(math.sin(r(dec)) * math.sin(r(-16.7161)) + math.cos(r(dec)) * math.cos(r(-16.7161)) * math.cos(r(ra - 101.2872))))
        assert abs(sep - math.hypot(553, 1205) * 1000 / 3.6e6) < 1e-6, sep          # exact: arc travelled = mu * t (0.36828 deg)
        # flat-sky estimate agrees to within its own second-order error (mu_a* mu_d t^2 tan(dec) ~ 3e-4 deg)
        assert abs((dec + 16.7161) - (-0.33472)) < 5e-4 and abs((ra - 101.2872) - (-0.16038)) < 5e-4, (ra, dec)
        assert pg.evaluate("window.__skymap.timeMachine.move(10,20,null,5e4)") == [10, 20]
        pg.click("#tmBtn"); assert pg.is_visible("#tmBar")
        def first_line():
            return pg.evaluate("JSON.stringify(window.__skymap.layers.constellations.overlayItems.slice(0,3).map(o=>o.raDecArray))")
        before = first_line()
        pg.evaluate("window.__skymap.timeMachine.setYears(50000)"); pg.wait_for_timeout(300)
        assert pg.evaluate("Math.abs(window.__skymap.timeYears - 50000) < 2000")
        assert "AD" in pg.inner_text("#tmYear")
        assert first_line() != before                                   # constellation lines moved
        pg.click("#tmNow"); pg.wait_for_timeout(300)
        assert pg.evaluate("window.__skymap.timeYears") == 0 and first_line() == before   # exact return to today
        pg.evaluate("window.__skymap.timeMachine.setYears(-80000)"); pg.wait_for_timeout(300)
        assert "BC" in pg.inner_text("#tmYear")
        pg.click("#tmX"); assert not pg.is_visible("#tmBar") and pg.evaluate("window.__skymap.timeYears") == 0
        app_errors = [e for e in errors if "HiPS" not in e and "fetch" not in e.lower() and "CDS ID" not in e]
        assert not app_errors, app_errors
        b.close()
