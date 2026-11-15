"""Start the AEGIS Sky Map on this computer and open it in the browser.   python serve.py   (Python 3.8+, nothing to install)
Use --lan to let other devices on the school network open it (it prints the address), --port to change the port."""
import argparse, functools, http.server, os, socket, threading, webbrowser

class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map, ".js": "text/javascript", ".mjs": "text/javascript",
                      ".webmanifest": "application/manifest+json", ".json": "application/json", ".svg": "image/svg+xml"}
    def log_message(self, *a): pass

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--port", type=int, default=8780); ap.add_argument("--lan", action="store_true")
    ap.add_argument("--no-browser", action="store_true"); a = ap.parse_args()
    root = os.path.dirname(os.path.abspath(__file__))
    host = "0.0.0.0" if a.lan else "127.0.0.1"
    srv = http.server.ThreadingHTTPServer((host, a.port), functools.partial(Handler, directory=root))
    url = f"http://localhost:{a.port}/index.html"
    print(f"AEGIS Sky Map is running at {url}")
    if a.lan:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.connect(("10.255.255.255", 1)); ip = s.getsockname()[0]; s.close()
            print(f"Other devices on this network: http://{ip}:{a.port}/index.html")
        except OSError: pass
    print("Close this window (or press Ctrl+C) to stop.")
    if not a.no_browser: threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try: srv.serve_forever()
    except KeyboardInterrupt: pass

if __name__ == "__main__":
    main()
