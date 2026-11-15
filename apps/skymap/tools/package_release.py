"""Build a ready-to-unzip release: dist/aegis-skymap-<version>.zip containing only what the app needs to run."""
import pathlib, re, zipfile
ROOT = pathlib.Path(__file__).resolve().parents[1]
VERSION = re.search(r'VERSION = "skymap-([^"]+)"', (ROOT / "sw.js").read_text()).group(1)
INCLUDE = ["index.html", "manifest.webmanifest", "sw.js", "serve.py", "START_SKY_MAP.bat", "start_sky_map.sh", "README.md", "INSTALL.md",
           "TEACHERS.md", "LICENSE", "COMMERCIAL.md", "THIRD_PARTY_NOTICES.md", "css", "js", "vendor", "data", "icons", "tools/export_from_sweep.py"]
def main():
    out = ROOT / "dist"; out.mkdir(exist_ok=True); z = out / f"aegis-skymap-{VERSION}.zip"
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for item in INCLUDE:
            p = ROOT / item
            for f in ([p] if p.is_file() else sorted(x for x in p.rglob("*") if x.is_file())):
                zf.write(f, f"aegis-skymap-{VERSION}/" + str(f.relative_to(ROOT)))
    print(z, f"{z.stat().st_size / 1e6:.1f} MB")
if __name__ == "__main__":
    main()
