"""Night vision: toggles, turns the rendered page red-only, dims, persists across reload and pages, no JS errors."""
import pytest
pw = pytest.importorskip("playwright.sync_api")
from test_app_browser import server  # noqa: F401  (reuse the local server fixture)

def _pixel(pg):
    shot = pg.screenshot(clip={"x": 600, "y": 400, "width": 1, "height": 1})
    from PIL import Image; import io
    return Image.open(io.BytesIO(shot)).convert("RGB").getpixel((0, 0))

def test_night_vision(server):
    with pw.sync_playwright() as p:
        b = p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
        pg = b.new_page(viewport={"width": 1280, "height": 800}); errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.goto(server); pg.wait_for_selector("#nightBtn")
        pg.evaluate("document.body.style.background='rgb(40,200,120)'")   # a known green/blue-heavy colour
        pg.click("#nightBtn")
        assert pg.get_attribute("#nightBtn", "aria-pressed") == "true"
        r, g, bl = _pixel(pg)
        assert g == 0 and bl == 0, (r, g, bl)                              # only red survives
        pg.fill("#nvLevel", "30"); pg.dispatch_event("#nvLevel", "input")
        r2, _, _ = _pixel(pg); assert r2 < r                                # dimmer
        pg.reload(); pg.wait_for_selector("#nightBtn")
        assert pg.evaluate("document.documentElement.classList.contains('night')")
        assert pg.input_value("#nvLevel") == "30"
        pg.goto(server.replace("index.html", "ar.html")); pg.wait_for_timeout(500)
        assert pg.evaluate("document.documentElement.classList.contains('night')")   # carries to Point & See
        pg.click("#nvOff"); assert not pg.evaluate("document.documentElement.classList.contains('night')")
        app_errors = [e for e in errors if "HiPS" not in e and "fetch" not in e.lower() and "CDS ID" not in e]
        assert not app_errors, app_errors
        b.close()
