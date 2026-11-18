"""Browser smoke test (needs Playwright + Chromium). The telescope image server is not required: the test checks the app's own layers and panels."""
import pathlib, subprocess, sys, time, socket, pytest
pw = pytest.importorskip("playwright.sync_api")
ROOT = pathlib.Path(__file__).resolve().parents[1]

def free_port():
    s = socket.socket(); s.bind(("127.0.0.1", 0)); p = s.getsockname()[1]; s.close(); return p

@pytest.fixture(scope="module")
def server():
    port = free_port()
    proc = subprocess.Popen([sys.executable, str(ROOT / "serve.py"), "--port", str(port), "--no-browser"], stdout=subprocess.DEVNULL)
    time.sleep(1.0); yield f"http://localhost:{port}/index.html"; proc.terminate()

def test_app_loads_layers_and_panels(server):
    with pw.sync_playwright() as p:
        b = p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
        pg = b.new_page(viewport={"width": 1280, "height": 800}); errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.goto(server); pg.wait_for_function("window.__skymap && window.__skymap.layers && window.__skymap.layers.planets", timeout=20000)
        layers = pg.evaluate("Object.keys(window.__skymap.layers)")
        assert {"constellations", "conNames", "stars", "messier", "planets"} <= set(layers)
        pg.fill("#search", "Andromeda"); pg.press("#search", "Enter"); pg.wait_for_selector("#info:not([hidden])")
        assert "Andromeda" in pg.inner_text("#infoBody")
        pg.fill("#search", "M42"); pg.press("#search", "Enter"); pg.wait_for_timeout(300)
        assert "M42" in pg.inner_text("#infoBody")
        pg.click("button[data-tab=tonight]"); pg.fill("#lat", "35.5"); pg.fill("#lon", "-97.5"); pg.click("#setLoc")
        assert "Jupiter" in pg.inner_text("#panelBody")
        for tab in ("tour", "learn", "aegis", "about", "layers"):
            pg.click(f"button[data-tab={tab}]"); assert pg.inner_text("#panelBody").strip()
        app_errors = [e for e in errors if "HiPS" not in e and "fetch" not in e.lower() and "CDS ID" not in e]
        assert not app_errors, app_errors
        b.close()
