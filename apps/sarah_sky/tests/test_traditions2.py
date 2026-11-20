"""1.7.0 panels: Arabic mansions, Chinese lodges, planetary hours, sky events, I Ching, runes, journal — render, no page errors."""
import pathlib, subprocess, sys, time, socket, pytest
pw = pytest.importorskip("playwright.sync_api")
ROOT = pathlib.Path(__file__).resolve().parents[1]
def free_port():
    s = socket.socket(); s.bind(("", 0)); p = s.getsockname()[1]; s.close(); return p
@pytest.fixture(scope="module")
def server():
    port = free_port()
    proc = subprocess.Popen([sys.executable, str(ROOT / "serve.py"), "--port", str(port), "--no-browser"], stdout=subprocess.DEVNULL)
    time.sleep(1.0); yield f"http://localhost:{port}/index.html"; proc.terminate()
def test_new_panels(server):
    with pw.sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 390, "height": 844}); errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.goto(server); pg.wait_for_timeout(2500)
        pg.evaluate("document.getElementById('sarahOverlays').open = true")
        for cb, out, want in [("ovManazil", "manazilOut", "mansion"), ("ovXiu", "xiuOut", "lodge"), ("ovHours", "hoursOut", "hour"),
                              ("ovEvents", "eventsOut", "Next lunar eclipse"), ("ovIching", "ichingOut", "moving"), ("ovRunes", "runesOut", "Draw three"),
                              ("ovJournal", "journalOut", "Save entry")]:
            pg.check("#" + cb); assert want in pg.inner_text("#" + out), cb
        pg.click("#rune3"); assert pg.inner_text("#runesOut").count("Situation") == 1
        pg.fill("#jText", "test entry"); pg.click("#jSave"); assert "test entry" in pg.inner_text("#journalOut")
        r = pg.evaluate("[SarahTraditions2.hexOf([1,1,1,1,1,1]).n, SarahTraditions2.hexOf([0,0,0,0,0,0]).n, SarahTraditions2.hexOf([1,0,1,0,1,0]).n]")
        assert r == [1, 2, 63]
        b.close(); app = [e for e in errors if "HiPS" not in e and "fetch" not in e.lower() and "CDS ID" not in e and "starting url" not in e]; assert not app, app   # telescope tiles are offline here
